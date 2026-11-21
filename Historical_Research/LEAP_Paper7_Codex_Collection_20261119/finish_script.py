from pathlib import Path
p=Path(__file__).with_name('extract_readonly.py');s=p.read_text()
a=s.index("print('Scanning read-only SQLite")
s=s[:a]+'''# Oversized generated JSON is searched with ripgrep without loading its object tree.
large=[]
for rel,reason in excluded:
 if reason!='content larger than 64 MiB':continue
 p=R/rel;h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 q=['rg','--text','--ignore-case','--count','--no-heading','--no-filename','--',PAT.pattern,str(p)]
 found=subprocess.run(q,capture_output=True,text=True)
 if found.returncode not in (0,1):errors.append((rel,'ripgrep_failed'))
 large.append((rel,p.stat().st_size,h.hexdigest(),found.stdout.strip() or '0','rg --text --ignore-case --count --no-heading --no-filename -- '+PAT.pattern+' '+rel,'content searched; full JSON object parsing omitted'))
csvout('search/large_file_scan.csv',['file','bytes','sha256','matching_lines','query','inspection'],large)
''' +s[a:]
a=s.index("print('Scanning historical ledger blobs")
s=s[:a]+'''scope_rows=[]
for p in dbs:
 c=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True);c.execute('PRAGMA query_only=ON')
 for t in ['sessions','events']:
  q='SELECT json_extract(snapshot_json, \\'$.review.decision\\'), json_extract(snapshot_json, \\'$.review.scope\\'), COUNT(*) FROM "'+t+'" GROUP BY 1,2'
  try:
   for decision,scope,n in c.execute(q):scope_rows.append((p.relative_to(R).as_posix(),t,q,decision or '',scope or '',n))
  except sqlite3.OperationalError:pass
 c.close()
csvout('search/sqlite_review_scopes.csv',['database','table','query','recorded_decision','recorded_scope','rows'],scope_rows)
''' +s[a:]
s=s.replace('Files over 64 MiB are listed in exclusions.','Files over 64 MiB are searched separately using ripgrep and streaming SHA-256; their full JSON object parsing is omitted. See large_file_scan.csv and exclusions.csv.')
s=s.replace('Context session/event state is software workflow evidence, not a supplied human authorization instrument.','Recorded review decisions in these tables are ACCEPT_CONTEXT with scope CONTEXT_CONTINUITY_ONLY, or absent, as shown by the exact grouped queries in sqlite_review_scopes.csv. They are not KPI authorization records.')
p.write_text(s);compile(s,str(p),'exec')
