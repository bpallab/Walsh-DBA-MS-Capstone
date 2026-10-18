"""Data acquisition and preparation for the QM640 capstone.

Three real, public ITSM datasets are used:

* ServiceNow incident event log (UCI ML Repository, id 498, CC BY 4.0)
* Rabobank ITSM log, BPI Challenge 2014 (4TU.ResearchData)
* The Public Jira Dataset (Montgomery, Lueders & Maalej, 2022; Zenodo v7, CC BY 4.0)

Downloads need open internet access (run in Google Colab). Every function
that touches the network is separate from the functions that parse files,
so parsing can be tested offline.
"""
from __future__ import annotations

import io
import json
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

UCI_SERVICENOW_ZIP = (
    "https://archive.ics.uci.edu/static/public/498/"
    "incident+management+process+enriched+event+log.zip"
)
# 4TU.ResearchData article ids for the four BPI Challenge 2014 files
BPI2014_ARTICLES = {
    "incident": 12692378,
    "interaction": 12692411,
    "incident_activity": 12706424,
    "change": 12716234,
}
JIRA_ZENODO_RECORD = 15719919  # v7, 2025-06-23, anonymised, 5.8 GB zip


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def snake(name: str) -> str:
    """'CI Name (aff)' -> 'ci_name_aff', '# Reassignments' -> 'n_reassignments'."""
    name = name.strip().replace("#", "n ")
    name = re.sub(r"[^0-9a-zA-Z]+", "_", name)
    return re.sub(r"_+", "_", name).strip("_").lower()


def download(url: str, dest: Path, chunk: int = 1 << 20) -> Path:
    """Stream a URL to disk (skips if the file already exists)."""
    import requests

    dest = Path(dest)
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        tmp = dest.with_suffix(dest.suffix + ".part")
        with open(tmp, "wb") as fh:
            for block in r.iter_content(chunk):
                fh.write(block)
        tmp.rename(dest)
    return dest


# ---------------------------------------------------------------------------
# ServiceNow (UCI 498)
# ---------------------------------------------------------------------------
def fetch_servicenow(raw_dir: Path) -> Path:
    """Download and unzip the UCI ServiceNow event log; returns the CSV path."""
    raw_dir = Path(raw_dir) / "servicenow"
    z = download(UCI_SERVICENOW_ZIP, raw_dir / "servicenow.zip")
    with zipfile.ZipFile(z) as zf:
        zf.extractall(raw_dir)
    csvs = sorted(raw_dir.rglob("*.csv"))
    if not csvs:
        raise FileNotFoundError(f"No CSV found after unzipping {z}")
    return csvs[0]


SN_DATES = ["opened_at", "sys_created_at", "sys_updated_at", "resolved_at", "closed_at"]


def load_servicenow_events(csv_path: Path) -> pd.DataFrame:
    """Read the event log; '?' means unknown, as the source documentation states."""
    df = pd.read_csv(csv_path, na_values=["?"], low_memory=False)
    for c in SN_DATES:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], dayfirst=True, errors="coerce")
    return df


def servicenow_to_incidents(events: pd.DataFrame) -> pd.DataFrame:
    """One row per incident: the last recorded event, plus derived measures."""
    ev = events.sort_values(["number", "sys_mod_count", "sys_updated_at"])
    inc = ev.groupby("number", as_index=False).tail(1).copy()
    inc["resolution_hours"] = (inc["resolved_at"] - inc["opened_at"]).dt.total_seconds() / 3600
    # Forrester-style friction count: distinct teams that handled the ticket
    inc["friction_count"] = inc["reassignment_count"].fillna(0).astype(int) + 1
    inc["n_events"] = ev.groupby("number")["number"].transform("size").loc[inc.index]
    return inc.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Rabobank, BPI Challenge 2014 (4TU)
# ---------------------------------------------------------------------------
def bpi2014_file_urls(article_id: int) -> list[dict]:
    """Ask the 4TU API for the download links of one dataset.

    4TU.ResearchData exposes a Figshare-compatible API. If this call fails,
    download the CSV manually from https://data.4tu.nl/collections/_/5065469/1
    and place it in data/raw/bpi2014/.
    """
    import requests

    for url in (
        f"https://data.4tu.nl/v2/articles/{article_id}/files",
        f"https://data.4tu.nl/v2/articles/{article_id}",
    ):
        try:
            r = requests.get(url, timeout=60)
            if r.ok:
                data = r.json()
                files = data if isinstance(data, list) else data.get("files", [])
                if files:
                    return files
        except (requests.RequestException, json.JSONDecodeError):
            continue
    return []


def fetch_bpi2014(raw_dir: Path) -> dict[str, Path]:
    raw_dir = Path(raw_dir) / "bpi2014"
    out: dict[str, Path] = {}
    for name, art in BPI2014_ARTICLES.items():
        existing = [p for p in raw_dir.glob("*") if name.replace("_", "") in p.name.lower().replace("_", "")]
        if existing:
            out[name] = existing[0]
            continue
        files = bpi2014_file_urls(art)
        if not files:
            print(f"[manual] could not resolve {name}; download it from 4TU into {raw_dir}")
            continue
        f = files[0]
        url = f.get("download_url") or f.get("url")
        fname = f.get("name", f"{name}.csv")
        out[name] = download(url, raw_dir / fname)
        if out[name].suffix == ".zip":
            with zipfile.ZipFile(out[name]) as zf:
                zf.extractall(raw_dir)
    return out


def load_bpi_csv(path: Path) -> pd.DataFrame:
    """BPI 2014 files are semicolon-separated with day-first timestamps."""
    with open(path, encoding="latin-1") as fh:
        header = fh.readline()
    sep = ";" if header.count(";") > header.count(",") else ","  # files differ
    df = pd.read_csv(path, sep=sep, decimal="," if sep == ";" else ".", low_memory=False, encoding="latin-1")
    df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]  # trailing separators
    df.columns = [snake(c) for c in df.columns]
    for c in df.columns:
        if any(k in c for k in ("time", "date", "start", "end")) and pd.api.types.is_string_dtype(df[c]):
            parsed = pd.to_datetime(df[c], format="%d/%m/%Y %H:%M:%S", errors="coerce")
            if parsed.notna().mean() < 0.5:
                parsed = pd.to_datetime(df[c], format="%d-%m-%Y %H:%M", errors="coerce")
            if parsed.notna().mean() > 0.5:
                df[c] = parsed
    return df


def bpi_incident_measures(inc: pd.DataFrame) -> pd.DataFrame:
    """Friction count and time-to-action measures for Rabobank incidents."""
    inc = inc.copy()
    reas = [c for c in inc.columns if "reassign" in c]
    if reas:
        inc["friction_count"] = pd.to_numeric(inc[reas[0]], errors="coerce").fillna(0).astype(int) + 1
    open_c = next((c for c in inc.columns if c.startswith("open_time")), None)
    res_c = next((c for c in inc.columns if c.startswith("resolved_time")), None)
    if open_c and res_c:
        for c in (open_c, res_c):
            inc[c] = pd.to_datetime(inc[c], dayfirst=True, errors="coerce")
        inc["resolution_hours"] = (inc[res_c] - inc[open_c]).dt.total_seconds() / 3600
    return inc


# ---------------------------------------------------------------------------
# Public Jira Dataset (Zenodo v7)
# ---------------------------------------------------------------------------
def jira_zip_url() -> str:
    return (
        f"https://zenodo.org/records/{JIRA_ZENODO_RECORD}/files/"
        "2025-06-23%20ThePublicJiraDataset.zip?download=1"
    )


JIRA_FIELDS = {
    "key": "key",
    "fields.summary": "summary",
    "fields.description": "description",
    "fields.issuetype.name": "issuetype",
    "fields.priority.name": "priority",
    "fields.status.name": "status",
    "fields.resolution.name": "resolution",
    "fields.created": "created",
    "fields.resolutiondate": "resolutiondate",
    "fields.assignee": "assignee",
    "fields.project.key": "project",
}


def _get(doc: dict, dotted: str):
    cur = doc
    for part in dotted.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
    return cur


def flatten_jira_issue(doc: dict, repository: str) -> dict:
    """Flatten one Jira REST document into the columns used in the study."""
    row = {"repository": repository}
    for src, dst in JIRA_FIELDS.items():
        v = _get(doc, src)
        if dst == "assignee" and isinstance(v, dict):
            v = v.get("key") or v.get("name") or v.get("accountId")
        row[dst] = v
    f = doc.get("fields", {}) or {}
    row["components"] = [c.get("name") for c in (f.get("components") or []) if isinstance(c, dict)]
    row["labels"] = list(f.get("labels") or [])
    links = []
    for ln in f.get("issuelinks") or []:
        t = (ln.get("type") or {}).get("name")
        other = ln.get("outwardIssue") or ln.get("inwardIssue") or {}
        direction = "outward" if "outwardIssue" in ln else "inward"
        links.append({"type": t, "direction": direction, "key": other.get("key")})
    row["issuelinks"] = links
    row["n_comments"] = len(((f.get("comment") or {}).get("comments")) or [])
    hist = ((doc.get("changelog") or {}).get("histories")) or []
    assignee_changes = sum(
        1 for h in hist for it in (h.get("items") or []) if (it.get("field") or "").lower() == "assignee"
    )
    row["n_assignee_changes"] = assignee_changes
    row["friction_count"] = max(assignee_changes, 1)
    return row


def jira_frame(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    for c in ("created", "resolutiondate"):
        if c in df:
            df[c] = pd.to_datetime(df[c], errors="coerce", utc=True)
    df["is_duplicate_resolution"] = df["resolution"].fillna("").str.lower().eq("duplicate")
    df["has_duplicate_link"] = df["issuelinks"].apply(
        lambda ls: any((l.get("type") or "").lower() == "duplicate" for l in ls)
    )
    df["resolution_hours"] = (df["resolutiondate"] - df["created"]).dt.total_seconds() / 3600
    return df


# ---------------------------------------------------------------------------
# profiling (used for the synopsis screenshots and Appendix A)
# ---------------------------------------------------------------------------
def profile(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Column-level profile: type, missing share, distinct values, example."""
    rows = []
    for c in df.columns:
        s = df[c]
        try:
            nunique = s.nunique(dropna=True)
        except TypeError:  # list-valued columns
            nunique = s.astype(str).nunique()
        ex = s.dropna().iloc[0] if s.notna().any() else None
        rows.append({
            "dataset": name,
            "variable": c,
            "dtype": str(s.dtype),
            "missing_pct": round(100 * s.isna().mean(), 1),
            "distinct": int(nunique),
            "example": str(ex)[:60],
        })
    return pd.DataFrame(rows)
