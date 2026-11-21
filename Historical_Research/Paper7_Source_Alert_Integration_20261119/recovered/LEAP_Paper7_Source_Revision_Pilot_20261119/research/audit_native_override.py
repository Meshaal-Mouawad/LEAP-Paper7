#!/usr/bin/env python3
"""Audits the archived LEAP approval handling against pre-existing governance rules.
Only the four selected Python function AST nodes are compiled in isolation.
All created authorization records are controlled tests, never historical approvals.
"""
import ast,hashlib,json,subprocess,csv
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
GIT=ROOT/'inputs/LEAPRepository/.git'

def show(path, commit='main'):
 snap=ROOT/'inputs/source_snapshot'/path
 if not GIT.is_dir() and commit=='main' and snap.is_file(): return snap.read_text(encoding='utf-8')
 p=subprocess.run(['git',f'--git-dir={GIT}','show',f'{commit}:{path}'],capture_output=True)
 if p.returncode:raise RuntimeError(p.stderr.decode())
 return p.stdout.decode()

def sha(s):return hashlib.sha256(s.encode()).hexdigest()

code=show('bluebook_generator/main.py')
policy=show('.ai/GOVERNANCE_SPEC.md')
rules=show('.ai/BUSINESS_RULES.md')
assert 'If KPI id and code hash match' in policy
assert 'suppress review alerts' in policy
assert 'Overrides marked with status "APPROVED_BY_BUSINESS"' in rules
assert 'SHA256 file signatures' in rules

if GIT.is_dir():
    all_py=subprocess.run(['git',f'--git-dir={GIT}','grep','-n','source_file_signature','main','--','*.py'],capture_output=True,text=True)
    use_sites=all_py.stdout.splitlines()
else:
    use_sites=(ROOT/'inputs/tracked_python_signature_grep.txt').read_text().splitlines()
assert len(use_sites)==1 and 'current_signature =' in use_sites[0],use_sites

nodes=ast.parse(code).body
selected_names={'_definition_override_candidates','_apply_definition_override'}
funcs=[n for n in nodes if isinstance(n,ast.FunctionDef) and n.name in selected_names]
assert len(funcs)==2
source_slice='\n\n'.join(ast.get_source_segment(code,n) for n in funcs)
(ROOT/'analysis/native_archived_functions_used.py').write_text(source_slice+'\n')
selected_fields=set()
for node in nodes:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DEFINITION_OVERRIDE_FIELDS' for t in node.targets):
  selected_fields=ast.literal_eval(node.value)
assert 'objective' in selected_fields
# Compile only the two selected native functions; no full app execution or imports.
ns={'Path':Path,'DEFINITION_OVERRIDE_FIELDS':selected_fields}
mod=ast.Module(body=funcs,type_ignores=[]);ast.fix_missing_locations(mod)
exec(compile(mod,'<archived LEAP main.py selected functions>','exec'),ns)
apply=ns['_apply_definition_override']

source=show('sample_project/python_kpi.py')
changed=source.replace('* 24','* 25')
assert source!=changed
old_sig=sha(source); new_sig=sha(changed)

base={'name':'DemoThroughput','file_path':'sample_project/python_kpi.py',
      'source_file_display':'sample_project/python_kpi.py'}
def run_case(case,expected_valid):
    kp={**base,**case['kpi']}
    override=case['override']
    detail={'objective':'original objective','formula_description':'original formula'}
    result=apply(kp,detail,{base['name']:override} if override is not None else {})
    applied=result.get('objective')=='controlled approved text'
    returned_status=result.get('_override_status')
    return {'case_id':case['id'],'reference_expected_approved':expected_valid,
            'applied_fields':applied,'native_status_returned':returned_status,
            'matches_spec':applied==expected_valid,
            'case':case['explanation']}

def led(status='APPROVED_BY_BUSINESS',signature=None):
 v={'status':status,'fields':{'objective':'controlled approved text'},'source':'controlled test ledger'}
 if signature is not None:v['file_signature']=signature
 return v

cases=[
 ({'id':'S1-approved-matching-signature','kpi':{'source_file_signature':old_sig},'override':led(signature=old_sig),'explanation':'Approved signature equals source signature'},True),
 ({'id':'S2-approved-source-revised','kpi':{'source_file_signature':new_sig},'override':led(signature=old_sig),'explanation':'Signed approval for old KPI source evaluated against formula-changed source'},False),
 ({'id':'S3-approved-unsigned-source-revised','kpi':{'source_file_signature':new_sig},'override':led(signature=''),'explanation':'Unsigned old approval evaluated against formula-changed source'},False),
 ({'id':'S4-approved-unsigned-unchanged','kpi':{'source_file_signature':old_sig},'override':led(signature=''),'explanation':'Unsigned approval despite unchanged code; signature evidence absent'},False),
 ({'id':'S5-pending-matching-signature','kpi':{'source_file_signature':old_sig},'override':led(status='PENDING',signature=old_sig),'explanation':'Pending human review and correct source signature'},False),
 ({'id':'S6-rejected-matching-signature','kpi':{'source_file_signature':old_sig},'override':led(status='REJECTED',signature=old_sig),'explanation':'Explicit rejected approval status and correct source signature'},False),
 ({'id':'S7-approved-signature-missing-from-kpi','kpi':{},'override':led(signature=old_sig),'explanation':'Source unchanged but extractor did not populate source_file_signature'},True),
 ({'id':'S8-approved-code_hash-without-signature','kpi':{'code_hash':old_sig},'override':led(signature=old_sig),'explanation':'Only code_hash is provided; matcher expects source_file_signature'},True),
 ({'id':'S9-approved-no-ledger','kpi':{'source_file_signature':old_sig},'override':None,'explanation':'No override; original details retained'},False),
]
res=[run_case(c,expected) for c,expected in cases]
# One explicit name-mismatch control, even with valid evidence.
a={'name':'DifferentKPI','source_file_signature':old_sig}
x=apply({**base,**a},{'objective':'original objective'}, {'DemoThroughput':led(signature=old_sig)})
res.append({'case_id':'S10-different-kpi-name','reference_expected_approved':False,'applied_fields':x['objective']=='controlled approved text','native_status_returned':x.get('_override_status'),'matches_spec':x['objective']=='original objective','case':'Approval for other KPI must not bind to this source finding'})

ledger_contents={}
for path in ['kb/overrides.json','bluebook_generator/kb/overrides.json','docs/governance_overrides.json']:
  j=json.loads(show(path))
  block=j.get('kpis',{})
  ledger_contents[path]={'approval_entries':len(block),'sha256':sha(show(path))}
  assert not block, path

out={'source_revision':'main','source_sha256':sha(code),
    'rules_sha256':sha(rules),'policy_sha256':sha(policy),
    'source_signature_reference': 'SHA256 of archived source file text',
    'production_ledgers':ledger_contents,
    'source_file_signature_occurrences_across_tracked_python':use_sites,
    'tested_functions':['main.py::_definition_override_candidates','main.py::_apply_definition_override'],
    'test_cases':res,
    'pass_count':sum(x['matches_spec'] for x in res),
    'fail_count':sum(not x['matches_spec'] for x in res),
    'note':'These are controlled test ledgers and a code-level proxy. No actual human authorization is inferred.'}
(ROOT/'analysis/native_override_test_results.json').write_text(json.dumps(out,indent=2))
with (ROOT/'analysis/native_override_tests.csv').open('w',newline='') as f:
 cols=['case_id','reference_expected_approved','applied_fields','native_status_returned','matches_spec','case']
 w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(res)
print(json.dumps({'passed':out['pass_count'],'failed':out['fail_count'],'failed_cases':[x['case_id'] for x in res if not x['matches_spec']], 'ledgers':ledger_contents},indent=2))
