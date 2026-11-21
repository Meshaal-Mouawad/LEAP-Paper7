from pathlib import Path
p=Path(__file__).with_name('extract_readonly.py');s=p.read_text()
start=s.index('# Supplementary engine revisions');end=s.index("print('Inventorying Paper 7 input archives'",start)
s=s[:start]+'''# Import the nine supplied cases without executing input scripts or source code.
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
csvout('authentic_approval_records.csv',['approval_id','original_status','human_approver_role','timestamp','exact_kpi_or_finding','authorization_scope','source_hash_or_commit','policy_version','expiry','revocation','evidence_path','evidence_sha256','source_query'],[])
csvout('adjudication_blind.csv',['pair_id','stratum','before_evidence','after_evidence','reviewer_code','initial_decision','manual_signature_reference','decision_timestamp','reason','disagreement','resolution','resolution_signature_reference'],blind)
write('recorded_source_behavior.json',json.dumps({'provenance':authority.name+'!'+prefix+'data/python_source_execution_tests.json','recorded_checks':json.loads(z.read(prefix+'data/python_source_execution_tests.json')),'collection_action':'Copied recorded observations; no new code execution and no authorization inference'},indent=2)+'\\n')
# Keep the 24 prior constructed cases in their own stratum; never import matcher predictions into reviewer sheets.
pilot_member=prefix+'inputs/LEAP_Paper7_Source_Revision_Pilot_20261119.zip'
pz=zipfile.ZipFile(io.BytesIO(z.read(pilot_member)));pr=json.loads(pz.read('analysis/proxy_case_records.json'))
assert len(pr)==24
pilotrows=[]
for i,row in enumerate(pr,1):
 pilotrows.append((row['case_id'],'CONSTRUCTED_PILOT',row['family'],row['variant'],row['source_path'],row['source_sha256_before'],row['source_sha256_after'],json.dumps(row['reference_full_outputs_before']),json.dumps(row['reference_full_outputs_after']),authority.name+'!'+pilot_member+'!analysis/proxy_case_records.json#/'+str(i-1)))
csvout('constructed_pilot/recorded_case_inventory.csv',['case_id','stratum','family','variant','source_path','before_sha256','after_sha256','recorded_before_outputs','recorded_after_outputs','provenance'],pilotrows)
write('constructed_pilot/README.md','24 prior constructed cases; recorded outputs copied with exact row locators. No pilot case is an authentic authorization or an extra historical transition. Constructed after sources are not regenerated. Matcher predictions and human labels are not imported.\\n')
''' + s[end:]
s=s.replace("'provided_nine_transition_archive':'LOCATED_NOT_IMPORTED' if found_named else 'NOT_LOCATED','provided_nine_transitions_imported':0,'constructed_pilot_cases_imported':0,'supplementary_engine_pairs':len(pairs)","'provided_nine_transition_archive':'VERIFIED_AND_IMPORTED','provided_nine_transitions_imported':len(pairs),'constructed_pilot_cases_imported':len(pilotrows),'supplementary_engine_pairs':0")
s=s.replace("The three supplementary pairs are recoverable engine code revisions, not the nine named archived KPI-source transitions. They do not supply business authorizations or observed before/after finding outputs. No missing original transition has been fabricated.","Nine supplied historical source-file transitions are retained under real_revisions/. All 18 snapshots are verified against the supplied manifest and checked against locally available Git objects. Constructed pilot cases are inventoried separately. No new source transition was invented.")
s=s.replace("The rows currently supplied concern supplementary engine revisions only, and cannot establish business-authorization outcomes. Do not mistake them for the nine requested KPI transitions.","The 18 rows provide two reviewer slots for each of nine historical source transitions. No matcher predictions or automatic KEEP/REVOKE judgments are included. Any missing approval/finding/policy evidence must remain blank or UNKNOWN.")
a=s.index('The requested Paper7_RealRevision_Authority_Gate_20261119.zip was not located');b=s.index('\n\n## Coverage limits',a)
s=s[:a]+'''The Sponsor supplied the local path LEAP_Paper7_Real_Revision_Authority_Gate_20261119.zip after the initial filename search. All input manifest members and all 18 before/after source hashes were verified. Exact input/archive checks and local Git byte comparisons are in verification/. Nine original historical transitions are imported without technical matcher predictions. The 24 constructed pilot case records are copied to constructed_pilot/recorded_case_inventory.csv with original row locators and recorded outputs; no cases are regenerated. Historical source finding outputs remain UNKNOWN where not supplied. Recorded Python behavior checks are copied separately to recorded_source_behavior.json and are not treated as business authorization outcomes.''' + s[b:]
s=s.replace("'realrevision_authority_gate' in", "'authority_gate' in")
s=s.replace("No execution of repository code, database writes, network access, or Git mutations.","No execution of repository code, database writes, network access, or Git mutations. Input authority archive is required; use --archive for a non-default path.")
p.write_text(s)
