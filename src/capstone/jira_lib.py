"""Stream the Public Jira Dataset MongoDB dump straight out of the zip and
flatten each issue into compact columns. No MongoDB server is needed when the
dump is in directory format (<collection>.bson or .bson.gz)."""
import gzip, io, json, re, zipfile
import pyarrow as pa, pyarrow.parquet as pq
import bson

STR = pa.string(); I = pa.int64()
SCHEMA = pa.schema([(c, STR) for c in ['repository','key','project','issuetype','priority','status','resolution','created','resolutiondate','summary','description','components','labels','assignee']]
                   + [('n_comments', I), ('last_comment', STR), ('issuelinks', STR), ('n_links', I), ('has_duplicate_link', pa.bool_()),
                      ('n_assignee_changes', I), ('n_component_changes', I), ('n_priority_changes', I), ('n_type_changes', I), ('n_history_items', I)])

TARGET_REPOS = ["Apache", "RedHat", "MongoDB"]

def g(d, path):
    for p in path.split('.'):
        if not isinstance(d, dict): return None
        d = d.get(p)
    return d

def name_of(x):
    if isinstance(x, dict): return x.get('name') or x.get('value') or x.get('key')
    return x

def trunc(s, n):
    if not isinstance(s, str): return None
    s = re.sub(r'\{code[^}]*\}.*?\{code\}', ' [code] ', s, flags=re.S)   # shorten code blocks
    s = re.sub(r'\s+', ' ', s).strip()
    return s[:n]

def flatten(doc, repo):
    f = doc.get('fields') or {}
    links = []
    for ln in f.get('issuelinks') or []:
        t = (ln.get('type') or {})
        if 'outwardIssue' in ln: links.append({'type': t.get('name'), 'dir': 'out', 'label': t.get('outward'), 'key': (ln['outwardIssue'] or {}).get('key')})
        elif 'inwardIssue' in ln: links.append({'type': t.get('name'), 'dir': 'in', 'label': t.get('inward'), 'key': (ln['inwardIssue'] or {}).get('key')})
    comments = (f.get('comment') or {}).get('comments') or []
    hist = (doc.get('changelog') or {}).get('histories') or []
    changes = {}
    for h in hist:
        for it in h.get('items') or []:
            fld = (it.get('field') or '').lower()
            changes[fld] = changes.get(fld, 0) + 1
    assignee = f.get('assignee')
    return {
        'repository': repo,
        'key': doc.get('key'),
        'project': name_of(g(f, 'project.key')) or name_of(f.get('project')),
        'issuetype': name_of(f.get('issuetype')),
        'priority': name_of(f.get('priority')),
        'status': name_of(f.get('status')),
        'resolution': name_of(f.get('resolution')),
        'created': str(f.get('created')) if f.get('created') else None,
        'resolutiondate': str(f.get('resolutiondate')) if f.get('resolutiondate') else None,
        'summary': trunc(f.get('summary'), 300),
        'description': trunc(f.get('description'), 2000),
        'components': json.dumps([name_of(c) for c in f.get('components') or []]),
        'labels': json.dumps(list(f.get('labels') or [])),
        'assignee': str((assignee.get('key') or assignee.get('name') or assignee.get('accountId')) if isinstance(assignee, dict) else assignee) if assignee else None,
        'n_comments': len(comments),
        'last_comment': trunc(comments[-1].get('body'), 800) if comments else None,
        'issuelinks': json.dumps(links),
        'n_links': len(links),
        'has_duplicate_link': any((l['type'] or '').lower() == 'duplicate' for l in links),
        'n_assignee_changes': changes.get('assignee', 0),
        'n_component_changes': changes.get('component', 0),
        'n_priority_changes': changes.get('priority', 0),
        'n_type_changes': changes.get('issuetype', 0),
        'n_history_items': sum(changes.values()),
    }

def dump_members(names, repos=TARGET_REPOS):
    """Map repo -> zip member holding its BSON collection."""
    out = {}
    for r in repos:
        pat = re.compile(rf'(^|/){re.escape(r)}\.bson(\.gz)?$', re.I)
        m = [n for n in names if pat.search(n)]
        if m: out[r] = m[0]
    return out

def stream_repo(zf, member, repo, writer_path, only_resolved=True, batch=20000, log=print):
    raw = zf.open(member)
    fh = gzip.GzipFile(fileobj=raw) if member.endswith('.gz') else raw
    fh = io.BufferedReader(fh, buffer_size=1 << 20)
    rows, n_seen, n_kept, writer = [], 0, 0, None
    for doc in bson.decode_file_iter(fh):
        n_seen += 1
        if only_resolved and not g(doc, 'fields.resolution'):
            continue
        rows.append(flatten(doc, repo)); n_kept += 1
        if len(rows) >= batch:
            t = pa.Table.from_pylist(rows, schema=SCHEMA); writer = writer or pq.ParquetWriter(writer_path, SCHEMA); writer.write_table(t); rows = []
            if n_kept % 100000 < batch: log(f'  {repo}: seen {n_seen:,}, kept {n_kept:,}')
    if rows:
        t = pa.Table.from_pylist(rows, schema=SCHEMA); writer = writer or pq.ParquetWriter(writer_path, SCHEMA); writer.write_table(t)
    if writer: writer.close()
    return n_seen, n_kept
