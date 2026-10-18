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


# ---------------------------------------------------------------------------
# mongodump --archive format reader (single-file dump, optionally gzipped)
# Layout: magic 0x8199e26d | prelude header doc | collection-metadata docs | -1
#         then blocks: namespace header {db, collection, EOF, CRC} | docs... | -1
# ---------------------------------------------------------------------------
import struct
MAGIC = 0x8199e26d
TERM = 0xFFFFFFFF

def _open_archive(zf, member):
    raw = zf.open(member)
    head = raw.read(2); raw.close(); raw = zf.open(member)
    fh = gzip.GzipFile(fileobj=raw) if head == b'\x1f\x8b' else raw
    return io.BufferedReader(fh, buffer_size=4 << 20)

def _read_doc(fh):
    """Return (raw_bytes or None for terminator); raises EOFError at end."""
    b = fh.read(4)
    if len(b) < 4: raise EOFError
    n = struct.unpack('<I', b)[0]
    if n == TERM: return None
    rest = fh.read(n - 4)
    if len(rest) < n - 4: raise EOFError
    return b + rest

def archive_info(zf, member):
    """Read only the prelude: tool/server versions and the list of collections."""
    fh = _open_archive(zf, member)
    magic = struct.unpack('<I', fh.read(4))[0]
    if magic != MAGIC: raise ValueError(f'not a mongodump archive (magic {magic:#x})')
    header = bson.decode(_read_doc(fh))
    cols = []
    while True:
        d = _read_doc(fh)
        if d is None: break
        m = bson.decode(d); cols.append({'db': m.get('db'), 'collection': m.get('collection'), 'size': m.get('size')})
    return header, cols

def stream_archive(zf, member, repos, out_dir, only_resolved=True, batch=20000, log=print):
    """One pass over the archive; flatten documents of the wanted collections."""
    fh = _open_archive(zf, member)
    assert struct.unpack('<I', fh.read(4))[0] == MAGIC
    _read_doc(fh)                                   # prelude header
    while _read_doc(fh) is not None: pass           # collection metadata
    wanted = {r.lower(): r for r in repos}
    writers, rows, seen, kept = {}, {r: [] for r in repos}, {r: 0 for r in repos}, {r: 0 for r in repos}
    current, expect_header, n_blocks = None, True, 0
    def flush(r):
        if rows[r]:
            t = pa.Table.from_pylist(rows[r], schema=SCHEMA)
            if r not in writers: writers[r] = pq.ParquetWriter(f'{out_dir}/{r}.parquet', SCHEMA)
            writers[r].write_table(t); rows[r] = []
    try:
        while True:
            d = _read_doc(fh)
            if d is None: expect_header = True; continue
            if expect_header:
                h = bson.decode(d); n_blocks += 1
                current = wanted.get(str(h.get('collection', '')).lower()); expect_header = False
                continue
            if current is None: continue            # skip documents of other collections cheaply
            doc = bson.decode(d); seen[current] += 1
            if only_resolved and not g(doc, 'fields.resolution'): continue
            rows[current].append(flatten(doc, current)); kept[current] += 1
            if len(rows[current]) >= batch:
                flush(current)
                if kept[current] % 100000 < batch: log(f'  {current}: seen {seen[current]:,}, kept {kept[current]:,}')
    except EOFError:
        pass
    for r in repos: flush(r)
    for w in writers.values(): w.close()
    return {r: {'issues_in_dump': seen[r], 'resolved_kept': kept[r]} for r in repos}, n_blocks
