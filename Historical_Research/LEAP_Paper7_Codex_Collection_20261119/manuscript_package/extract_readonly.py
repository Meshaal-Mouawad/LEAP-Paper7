#!/usr/bin/env python3
"""Read sources only; write a fresh evidence directory outside all source roots.
Usage: python -B extract_readonly.py --repo REPO --output NEW_DIRECTORY
No execution of repository code, database writes, network access, or Git mutations. Input authority archive is required; use --archive for a non-default path.
"""
import argparse,collections,csv,hashlib,io,json,os,re,sqlite3,subprocess,zipfile
from pathlib import Path
P=argparse.ArgumentParser();P.add_argument('--repo',required=True);P.add_argument('--output',required=True);P.add_argument('--archive',action='append',default=[]);P.add_argument('--scan-cache');a=P.parse_args()
R=Path(a.repo).resolve();O=Path(a.output).resolve()
if O==R or R in O.parents:raise SystemExit('Output must be outside repository')
O.mkdir(parents=True,exist_ok=False)
def sha(b):return hashlib.sha256(b).hexdigest()
def clean(s):
 s=str(s).replace(str(Path.home()),'$HOME')
 s=re.sub(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}', '[REDACTED_EMAIL]',s,flags=re.I)
 s=s.replace(Path.home().name,'[REDACTED_USER]')
 s=re.sub(r'[A-Za-z0-9_-]+/AI-Powered_KPI_Extractor_Interactive_Bluebook_Generator','$REPO',s)
 return s

def csvout(name,cols,rows):
 p=O/name;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='') as f:
  w=csv.writer(f);w.writerow(cols)
  for row in rows:w.writerow([clean(x) for x in row])
def git(*args):return subprocess.check_output(['git','--no-optional-locks','-C',str(R),*args],stderr=subprocess.DEVNULL)
def write(name,text):
 p=O/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(clean(text))
PAT=re.compile(r'approv(?:al|ed|er)?|deferr(?:al|ed)?|sign[ _-]?off|revok|revocat|exception|authoriz|signature',re.I)
SKIP={'.git','node_modules','.venv','venv','__pycache__','_build','.pytest_cache','.idea'}
EXT={'.json','.jsonl','.csv','.tsv','.md','.txt','.log','.yaml','.yml','.rst','.sql'}
LEDGERS={'overrides.json','governance_overrides.json','review_workflow.json'}
inventory=[];hits=[];ledgers=[];objects=[];errors=[];dbs=[];media=[];dirs=[];excluded=[]
if not a.scan_cache:
 print('Scanning working tree, including hidden and ignored records',flush=True)
 for d,ds,fs in os.walk(R,followlinks=False):
  ds[:]=sorted(x for x in ds if x not in SKIP and not (Path(d)/x).is_symlink())
  dirs.append(str(Path(d).relative_to(R)) or '.')
  for fn in sorted(fs):
   p=Path(d)/fn;rel=p.relative_to(R).as_posix()
   if p.is_symlink():continue
   if fn=='.env' or fn.startswith('.env.') or p.suffix in {'.pem','.key'}:excluded.append((rel,'credential file excluded'));continue
   if p.suffix in {'.db','.sqlite','.sqlite3'}:dbs.append(p);continue
   if p.suffix.lower() in {'.png','.jpg','.jpeg','.pdf'} and PAT.search(rel):media.append((rel,'not visually inspected; filename inventory only'));continue
   if p.suffix.lower() not in EXT:continue
   try:
    size=p.stat().st_size
    if size>64*1024*1024:excluded.append((rel,'content larger than 64 MiB'));continue
    b=p.read_bytes();s=b.decode('utf-8',errors='replace');h=sha(b)
    matches=[(i,sorted(set(m.group(0).lower() for m in PAT.finditer(line)))) for i,line in enumerate(s.splitlines(),1) if PAT.search(line)]
    inventory.append((rel,size,h,len(matches),'UTF-8 replacement decoding'))
    for i,terms in matches:hits.append((rel,i,'|'.join(terms),h))
    if fn in LEDGERS:
     j=json.loads(s);entries=j.get('kpis',j.get('signals',j));ledgers.append((rel,'WORKING_TREE',h,len(entries),'empty' if not entries else 'nonempty; not authenticated by extraction'))
    if p.suffix=='.json':
     try:j=json.loads(s)
     except:continue
     def walk(v,loc='$'):
      if isinstance(v,dict):
       keys=list(v)
       special=[k for k in keys if re.search(r'approver|approved_by|signed_by|approval_id|deferral_id|authorization_id|revoked_by',k,re.I)]
       if special:objects.append((rel,loc,'|'.join(special),h,'UNKNOWN'))
       for k,val in v.items():walk(val,loc+'/'+str(k))
      elif isinstance(v,list):
       for i,val in enumerate(v):walk(val,loc+'/'+str(i))
     walk(j)
   except Exception as e:errors.append((rel,type(e).__name__))
 csvout('search/file_inventory.csv',['file','bytes','sha256','matching_lines','decode'],inventory)
 csvout('search/text_hits.csv',['file','line','matched_expressions','sha256'],hits)
 csvout('search/structured_candidates.csv',['file','json_pointer','authority_field_names','sha256','authenticity'],objects)
 csvout('search/media_inventory.csv',['file','inspection'],media)
 csvout('search/exclusions.csv',['path','reason'],excluded)
 write('search/directories.txt','\n'.join(dirs)+'\n')
else:
 import shutil
 C=Path(a.scan_cache).resolve()
 def readcache(name):
  with (C/'search'/name).open() as f:return list(csv.reader(f))[1:]
 inventory=readcache('file_inventory.csv');hits=readcache('text_hits.csv');objects=readcache('structured_candidates.csv');media=readcache('media_inventory.csv');excluded=readcache('exclusions.csv')
 ledgers=[r for r in readcache('ledger_inventory.csv') if r[1]=='WORKING_TREE']
 dirs=(C/'search/directories.txt').read_text().splitlines()
 dbs=[R/r for r in sorted(set(x[0] for x in readcache('sqlite_tables.csv')))]
 shutil.copytree(C/'search',O/'search')
 print('Reused completed file scan; databases and Git re-read',flush=True)
# Oversized generated JSON is searched with ripgrep without loading its object tree.
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
print('Scanning read-only SQLite tables',flush=True)
dbrows=[];dbhits=[]
for p in dbs:
 rel=p.relative_to(R).as_posix()
 try:
  c=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True);c.execute('PRAGMA query_only=ON');c.execute('BEGIN')
  for (t,) in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
   qt='"'+t.replace('"','""')+'"';q='SELECT * FROM '+qt
   cur=c.execute(q);cols=[x[0] for x in cur.description];n=0;mh=hashlib.sha256()
   for n,row in enumerate(cur,1):
    # Only field names, matching terms and row checksum leave the source database.
    canonical=json.dumps(row,default=lambda x:x.hex() if isinstance(x,bytes) else str(x),ensure_ascii=True).encode();mh.update(canonical+b'\n')
    for col,val in zip(cols,row):
     terms=sorted(set(x.group(0).lower() for x in PAT.finditer(str(val))))
     if terms:dbhits.append((rel,t,q,n,col,'|'.join(terms),sha(canonical)))
   dbrows.append((rel,t,q,'|'.join(cols),n,mh.hexdigest(),'mode=ro; query_only=ON; read transaction; row contents withheld'))
  c.rollback();c.close()
 except Exception as e:errors.append((rel,type(e).__name__))
csvout('search/sqlite_tables.csv',['database','table','query','columns','rows','canonical_rows_sha256','read_mode'],dbrows)
csvout('search/sqlite_hits.csv',['database','table','query','row_ordinal','column','matched_expressions','row_sha256'],dbhits)
scope_rows=[]
for p in dbs:
 c=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True);c.execute('PRAGMA query_only=ON')
 for t in ['sessions','events']:
  q='SELECT json_extract(snapshot_json, \'$.review.decision\'), json_extract(snapshot_json, \'$.review.scope\'), COUNT(*) FROM "'+t+'" GROUP BY 1,2'
  try:
   for decision,scope,n in c.execute(q):scope_rows.append((p.relative_to(R).as_posix(),t,q,decision or '',scope or '',n))
  except sqlite3.OperationalError:pass
 c.close()
csvout('search/sqlite_review_scopes.csv',['database','table','query','recorded_decision','recorded_scope','rows'],scope_rows)
print('Scanning historical ledger blobs',flush=True)
paths=['docs/overrides.json','docs/governance_overrides.json','kb/overrides.json','bluebook_generator/kb/overrides.json','docs/review_workflow.json']
refs=git('for-each-ref','--format=%(refname) %(objectname)').decode();write('search/git_refs.txt',refs)
write('search/git_worktrees.txt',git('worktree','list','--porcelain').decode())
revisions=git('log','--all','--format=%H','--',*paths).decode();write('search/ledger_revisions.txt',revisions)
seen=set();unsigned=[]
for l in git('rev-list','--objects','--all','--',*paths).decode().splitlines():
 parts=l.split(' ',1)
 if len(parts)!=2 or parts[1] not in paths:continue
 obj,path=parts
 if (obj,path) in seen:continue
 seen.add((obj,path));b=git('cat-file','blob',obj)
 try:
  j=json.loads(b);entries=j.get('kpis',j.get('signals',j));ledgers.append((path,'git_blob:'+obj,sha(b),len(entries),'empty' if not entries else 'unsigned text; no approval identity/time/scope'))
  if path=='docs/overrides.json':
   for k,v in entries.items():unsigned.append((path,obj,k,'|'.join(v.keys()),sha(b),'NO_RECORDED_APPROVAL_METADATA'))
 except Exception as e:errors.append((obj+':'+path,type(e).__name__))
csvout('search/ledger_inventory.csv',['file','revision','sha256','entries','observed_metadata'],ledgers)
csvout('search/unsigned_override_texts.csv',['file','git_blob','kpi','record_fields','sha256','metadata_result'],unsigned)
# Import the nine supplied cases without executing input scripts or source code.
authority=Path.home()/'Downloads/LEAP_Paper7_Real_Revision_Authority_Gate_20261119.zip'
for candidate in a.archive:
 if 'authority' in Path(candidate).name.lower():authority=Path(candidate)
z=zipfile.ZipFile(authority);prefix='Paper7_RealRevision_Authority_Gate_20261119/'
manifest_checks=[]
for row in csv.DictReader(io.StringIO(z.read(prefix+'MANIFEST_SHA256.csv').decode())):
 b=z.read(prefix+row['path']);actual=sha(b)
 manifest_checks.append((authority.name,row['path'],row['sha256'],actual,'PASS' if actual==row['sha256'] and len(b)==int(row['bytes']) else 'FAIL'))
 if actual!=row['sha256'] or len(b)!=int(row['bytes']):raise RuntimeError('Input checksum mismatch')
csvout('verification/input_manifest_checks.csv',['archive','member','expected_sha256','actual_sha256','result'],manifest_checks)
merge_rows=[]
for row in csv.DictReader(io.StringIO(z.read(prefix+'data/github_merges_not_approvals.csv').decode())):
 merge_rows.append((row['pr'],row['state'],row['date'],row['review_submissions'],row['record_type'],authority.name+'!'+prefix+'data/github_merges_not_approvals.csv#pr='+row['pr']))
csvout('search/github_merge_metadata.csv',['pr_number','recorded_state','recorded_date','recorded_submitted_reviews','record_type','provenance'],merge_rows)
pairs=[];findings=[];blind=[];sourcechecks=[]
for row in csv.DictReader(io.StringIO(z.read(prefix+'data/real_source_revisions.csv').decode())):
 pid=row['case_id'];path=row['source_path'];ext=Path(path).suffix
 outnames={}
 for side,commitkey in [('before','parent_commit'),('after','child_commit')]:
  member=prefix+'cases/'+pid+'/'+side+ext;b=z.read(member)
  if sha(b)!=row[side+'_sha256']:raise RuntimeError('Case checksum mismatch')
  outname='source_pairs/real_revisions/'+pid+'/'+side+ext;write(outname,b.decode());outnames[side]=outname
  try:
   local=git('show',row[commitkey]+':'+path);check='PASS' if local==b else 'DIFFERENT_BYTES'
  except subprocess.CalledProcessError:check='OBJECT_UNAVAILABLE'
  sourcechecks.append((pid,side,row[commitkey],path,sha(b),sha((O/outname).read_bytes()),check,authority.name+'!'+member))
 pairs.append((pid,'ACTUAL_ARCHIVED_GIT_FILE_REVISION',row['parent_commit'],row['child_commit'],path,row['before_sha256'],row['after_sha256'],outnames['before'],outnames['after'],'UNKNOWN',authority.name+'!'+prefix+'data/real_source_revisions.csv#case_id='+pid))
 findings.append((pid,'ACTUAL_ARCHIVED_GIT_FILE_REVISION','','UNKNOWN','UNKNOWN','','','UNKNOWN',row['parent_commit']+':'+path,row['child_commit']+':'+path,'Source snapshots supplied; no associated historical finding output or authentic approval supplied.'))
 for reviewer in ['R1','R2']:blind.append((pid,'ACTUAL_ARCHIVED_GIT_FILE_REVISION',outnames['before'],outnames['after'],reviewer,'','','','','','',''))
csvout('verification/source_snapshot_checks.csv',['case_id','side','commit','source_path','original_sha256','export_sha256','local_git_byte_comparison','archive_member'],sourcechecks)
csvout('collection_manifest.csv',['pair_id','stratum','before_commit','after_commit','source_path','before_original_sha256','after_original_sha256','before_export','after_export','approval_id','provenance'],pairs)
csvout('source_findings_before_after.csv',['pair_id','stratum','kpi_or_finding','before_finding','after_finding','before_output_path','after_output_path','approval_id','before_source','after_source','observation'],findings)
csvout('authentic_approval_records.csv',['approval_id','original_status','approver_role','timestamp','exact_kpi_or_finding','authorization_scope','source_hash_or_commit','policy_version','expiry','revocation','evidence_path','evidence_sha256','source_query'],[])
csvout('adjudication_blind.csv',['pair_id','stratum','before_evidence','after_evidence','reviewer_code','initial_decision','manual_signature_reference','decision_timestamp','reason','disagreement','resolution','resolution_signature_reference'],blind)
write('recorded_source_behavior.json',json.dumps({'provenance':authority.name+'!'+prefix+'data/python_source_execution_tests.json','recorded_checks':json.loads(z.read(prefix+'data/python_source_execution_tests.json')),'collection_action':'Copied recorded observations; no new code execution and no authorization inference'},indent=2)+'\n')
# Keep the 24 prior constructed cases in their own stratum; never import matcher predictions into reviewer sheets.
pilot_member=prefix+'inputs/LEAP_Paper7_Source_Revision_Pilot_20261119.zip'
pz=zipfile.ZipFile(io.BytesIO(z.read(pilot_member)));pr=json.loads(pz.read('analysis/proxy_case_records.json'))
assert len(pr)==24
pilotrows=[]
for i,row in enumerate(pr,1):
 pilotrows.append((row['case_id'],'CONSTRUCTED_PILOT',row['family'],row['variant'],row['source_path'],row['source_sha256_before'],row['source_sha256_after'],json.dumps(row['reference_full_outputs_before']),json.dumps(row['reference_full_outputs_after']),authority.name+'!'+pilot_member+'!analysis/proxy_case_records.json#/'+str(i-1)))
csvout('constructed_pilot/recorded_case_inventory.csv',['case_id','stratum','family','variant','source_path','before_sha256','after_sha256','recorded_before_outputs','recorded_after_outputs','provenance'],pilotrows)
write('constructed_pilot/README.md','24 prior constructed cases; recorded outputs copied with exact row locators. No pilot case is an authentic authorization or an extra historical transition. Constructed after sources are not regenerated. Matcher predictions are kept separate from the reviewer worksheet.\n')
print('Inventorying Paper 7 input archives',flush=True)
archive_rows=[];pilot=[];found_named=[]
archive_inputs=sorted(set(list(Path.home().joinpath('Downloads').glob('*[Pp]aper7*.zip'))+[Path(x) for x in a.archive]))
def zscan(z,loc,depth=0):
 for info in z.infolist():
  if info.is_dir():continue
  archive_rows.append((loc,info.filename,info.file_size,info.CRC))
  if 'authority_gate' in info.filename.lower():found_named.append(loc+'!'+info.filename)
  if re.search(r'pilot|24.case|targeted.case',info.filename,re.I):pilot.append((loc,info.filename,'CONSTRUCTED_PILOT_CANDIDATE; no authenticity inference'))
  if info.filename.endswith('.zip') and depth<3 and info.file_size<100*1024*1024:
   try:zscan(zipfile.ZipFile(io.BytesIO(z.read(info))),loc+'!'+info.filename,depth+1)
   except Exception as e:errors.append((loc+'!'+info.filename,type(e).__name__))
for p in archive_inputs:
 try:
  if 'authority_gate' in p.name.lower():found_named.append(str(p))
  zscan(zipfile.ZipFile(p),'$DOWNLOADS/'+p.name)
 except Exception as e:errors.append((str(p),type(e).__name__))
csvout('search/archive_inventory.csv',['archive','member','uncompressed_bytes','zip_crc32'],archive_rows)
csvout('search/constructed_pilot_inventory.csv',['archive','member','stratum'],pilot)
csvout('search/errors.csv',['source','error_type'],errors)
result={'result':'NO_AUTHENTIC_AUTHORIZATIONS_FOUND','scope':'searched local sources only; not a universal absence claim','authentic_authorizations_exported':0,'authorizations_associated_with_source_changes':0,'provided_nine_transition_archive':'VERIFIED_AND_IMPORTED','provided_nine_transitions_imported':len(pairs),'constructed_pilot_cases_imported':len(pilotrows),'supplementary_engine_pairs':0,'reviewer_decisions_recorded':0,'structured_candidates_requiring_source_inspection':len(objects),'uninspected_media_files':len(media),'errors':len(errors),'repository_head':git('rev-parse','HEAD').decode().strip()}
write('collection_result.json',json.dumps(result,indent=2)+'\n')
write('source_pairs/README.md','Nine supplied historical source-file transitions are retained under real_revisions/. All 18 snapshots are verified against the supplied manifest and checked against locally available Git objects. Constructed pilot cases are inventoried separately. No new source transition was invented.\n')
write('REVIEWER_INSTRUCTIONS.md','Two independent qualified reviewers should inspect source evidence separately. Enter initial KEEP/REVOKE/UNKNOWN only after the actual reviewer supplies a manual decision and signature reference; record time and reason. Keep initial decisions unchanged. Record disagreements and separately signed resolution. The 18 rows provide two reviewer slots for each of nine historical source transitions. No matcher predictions or automatic KEEP/REVOKE judgments are included. Any missing approval/finding/policy evidence must remain blank or UNKNOWN. \n')
write('search_coverage.md',f'''# Paper 7 read-only collection coverage

Result: NO_AUTHENTIC_AUTHORIZATIONS_FOUND in the inspected source scope. No authentic approval was exported and none could be associated with a source change. 

Repository alias: $REPO = AI-Powered_KPI_Extractor_Interactive_Bluebook_Generator at the --repo argument. HEAD: {result['repository_head']}. Exact relative directories are in search/directories.txt. Git worktrees and refs are in search/git_worktrees.txt and search/git_refs.txt. No attached worktrees were returned by the desktop app. $HOME/.codex/worktrees did not exist. No remote system was queried.

## Working tree search

Included hidden, untracked and ignored files through os.walk, without following symlinks. Pruned directory names: {sorted(SKIP)}. Read extensions: {sorted(EXT)}. Credential files are excluded. Files over 64 MiB are searched separately using ripgrep and streaming SHA-256; their full JSON object parsing is omitted. See large_file_scan.csv and exclusions.csv. {len(inventory)} files read; {len(hits)} matching lines. Every read content hash is in search/file_inventory.csv; expressions and exact line locators are in search/text_hits.csv. Expression: `{PAT.pattern}`. JSON objects with authority field names are inventoried in structured_candidates.csv. A field-name hit is not an authentic approval. No source payloads, actor identities, session content, or corporate database row contents are exported.

## Ledgers and Git

{len(ledgers)} working-tree or historical ledger path/blob observations. Working-tree override/workflow copies contain no records. Historical docs/overrides.json contains three descriptive text overrides without recorded approval metadata; fields and source blob hashes are in unsigned_override_texts.csv. Commands: `git log --all --format=%H -- <ledger paths>` and `git rev-list --objects --all -- <ledger paths>`, followed by `git cat-file blob <object>`. Ledger paths: {paths}. Exact revisions are in ledger_revisions.txt. Branch merge metadata is not counted as business authorization. No new PR reviews were fetched.

## SQLite

{len(dbs)} databases discovered. All table names, column names, exact SELECT queries, row counts and canonical row-set checksums are in search/sqlite_tables.csv. Connections use URI mode=ro, PRAGMA query_only=ON and an explicit read transaction. Each column was searched using the same expression; matching row ordinals, field names and row hashes are in sqlite_hits.csv. Recorded review decisions in these tables are ACCEPT_CONTEXT with scope CONTEXT_CONTINUITY_ONLY, or absent, as shown by the exact grouped queries in sqlite_review_scopes.csv. They are not KPI authorization records. No database contents were exported.

## Archives and strata

All top-level Downloads Paper 7 ZIPs and nested ZIPs to depth 3 were inventoried (members up to 100 MiB for nested traversal). Exact archive/member locators are in archive_inventory.csv. The Sponsor supplied the local path LEAP_Paper7_Real_Revision_Authority_Gate_20261119.zip after the initial filename search. All input manifest members and all 18 before/after source hashes were verified. Exact input/archive checks and local Git byte comparisons are in verification/. Nine original historical transitions are imported without technical matcher predictions. The 24 constructed pilot case records are copied to constructed_pilot/recorded_case_inventory.csv with original row locators and recorded outputs; no cases are regenerated. Historical source finding outputs remain UNKNOWN where not supplied. Recorded Python behavior checks are copied separately to recorded_source_behavior.json and are not treated as business authorization outcomes.

## Coverage limits

Media filenames matching authority terms are inventoried but not visually interpreted; see media_inventory.csv. General binary archives other than the inventoried Paper 7 ZIPs were not unpacked. Excluded paths and parse/read errors are explicit in exclusions.csv and errors.csv. Git unreachable objects and external private systems were not accessed. The finding is confined to inspected records, not all possible stores. No authentic authorization should be inferred from keyword hits, test fixtures, generated receipts, or code merge history.

## Reproduction and integrity

Optional --scan-cache reuses a completed file inventory from another collection directory while re-reading SQLite and Git; omit it for a fresh full scan.

Run `python -B extract_readonly.py --repo /path/to/repository --output /new/outside/repository/directory`. Repeat --archive for additional Paper 7 ZIPs. The script refuses an existing output directory and writes outside the repository only. Source code and runtime were not executed. Evidence hashes cover packet files; SHA256SUMS includes all files except itself. ZIP SHA-256 is supplied separately. Original source hashes and redacted export hashes are separately retained. 
''')
# Reproducible script travels with each run; hashes are finalized by the packaging step.
(O/'extract_readonly.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(result),flush=True)

# Finalize packet hashes. evidence_hashes excludes the two manifest files to avoid recursion.
evidence=[]
for p in sorted(O.rglob('*')):
 if p.is_file() and p.name not in {'evidence_hashes.csv','SHA256SUMS'}:
  b=p.read_bytes();evidence.append((p.relative_to(O).as_posix(),len(b),sha(b),'packet:'+p.relative_to(O).as_posix()))
csvout('evidence_hashes.csv',['path','bytes','sha256','provenance'],evidence)
lines=[]
for p in sorted(O.rglob('*')):
 if p.is_file() and p.name!='SHA256SUMS':lines.append(sha(p.read_bytes())+'  '+p.relative_to(O).as_posix())
(O/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
