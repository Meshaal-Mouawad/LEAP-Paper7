#!/usr/bin/env python3
"""Controlled source-revision authorization proxy; no human approval labels.
Uses the fixed audit grid in pre_registered_protocol.json and exact archived Git sources.
The reference is output equivalence on the full grid; candidates see only their declared inputs.
"""
import ast, csv, hashlib, json, re, sqlite3, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROTOCOL = json.loads((HERE/'pre_registered_protocol.json').read_text())
GIT_DIR = ROOT/'inputs/LEAPRepository/.git'

def git_source(path):
    snap = ROOT/'inputs/source_snapshot'/path
    if not GIT_DIR.is_dir() and snap.is_file():
        return snap.read_text(encoding='utf-8')
    p=subprocess.run(['git',f'--git-dir={GIT_DIR}','show',f'main:{path}'],capture_output=True)
    if p.returncode: raise RuntimeError((path,p.stderr))
    return p.stdout.decode('utf-8')

def sha(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()

def must_replace(text, old, new, n=1):
    if text.count(old)!=n: raise AssertionError((old, text.count(old), n))
    return text.replace(old,new)

src={k:git_source(k) for k in PROTOCOL['original_sources']}
y=src['phase3/BestKPItest_iso_kpis/yield_correct.sql']
yo=src['phase3/BestKPItest_iso_kpis/yield_wrong_operator.sql']
yv=src['phase3/BestKPItest_iso_kpis/yield_wrong_variables.sql']
u=src['phase3/BestKPItest_iso_kpis/utilization_correct.sql']
uw=src['phase3/BestKPItest_iso_kpis/utilization_wrong.sql']
p=src['sample_project/python_kpi.py']
e=src['sample_projects/leap_enterprise_scenarios/kpi_environment_emissions_intensity.py']

cases=[]
def add(family,variant,base,changed,reason,source_path,created=True):
    cases.append(dict(family=family,variant=variant,base=base,changed=changed,transformation=reason,
                      source_path=source_path,controlled=created))

add('yield','exact_same',y,y,'same source positive control','phase3/BestKPItest_iso_kpis/yield_correct.sql',False)
add('yield','comment_only',y,'-- Comment-only change for pilot; synthetic\n'+y,'control: added comment', 'phase3/BestKPItest_iso_kpis/yield_correct.sql')
add('yield','spacing',y,must_replace(y,'good_output_mass / raw_input_mass','good_output_mass/raw_input_mass'),'control: SQL whitespace change','phase3/BestKPItest_iso_kpis/yield_correct.sql')
add('yield','equiv_factor',y,must_replace(y,'* 100','* (10 * 10)'),'controlled algebraic equivalent on audit grid','phase3/BestKPItest_iso_kpis/yield_correct.sql')
add('yield','wrong_operator',y,yo,'archived intentionally incorrect operator example','phase3/BestKPItest_iso_kpis/yield_wrong_operator.sql',False)
add('yield','wrong_variables',y,yv,'archived intentionally incorrect variable example','phase3/BestKPItest_iso_kpis/yield_wrong_variables.sql',False)
add('yield','sparse_hidden_37',y,must_replace(y,'(good_output_mass / raw_input_mass) * 100','CASE WHEN raw_input_mass = 37 THEN 0 ELSE (good_output_mass / raw_input_mass) * 100 END'),'controlled mutation affecting a non-probe denominator','phase3/BestKPItest_iso_kpis/yield_correct.sql')
add('yield','two_wrong_variants',yo,yv,'comparison of two different archived incorrect snippets','phase3/BestKPItest_iso_kpis/yield_wrong_variables.sql',False)
add('utilization','exact_same',u,u,'same source positive control','phase3/BestKPItest_iso_kpis/utilization_correct.sql',False)
add('utilization','comment_only',u,'-- Reviewed comment, synthetic\n'+u,'control: added comment','phase3/BestKPItest_iso_kpis/utilization_correct.sql')
add('utilization','spacing',u,must_replace(u,'actual_production_time / planned_operation_time','actual_production_time/planned_operation_time'),'control: SQL whitespace change','phase3/BestKPItest_iso_kpis/utilization_correct.sql')
add('utilization','equiv_factor',u,must_replace(u,'/ planned_operation_time','/ (planned_operation_time * 1)'),'controlled arithmetic equivalence','phase3/BestKPItest_iso_kpis/utilization_correct.sql')
add('utilization','wrong_formula',u,uw,'archived intentionally incorrect formula example','phase3/BestKPItest_iso_kpis/utilization_wrong.sql',False)
add('utilization','sparse_hidden_37',u,must_replace(u,'actual_production_time / planned_operation_time','CASE WHEN planned_operation_time = 37 THEN 0 ELSE actual_production_time / planned_operation_time END'),'controlled mutation affecting a non-probe planned time','phase3/BestKPItest_iso_kpis/utilization_correct.sql')
add('throughput','exact_same',p,p,'same source positive control','sample_project/python_kpi.py',False)
add('throughput','comment_only',p,'# controlled comment-only change\n'+p,'control: added comment','sample_project/python_kpi.py')
add('throughput','spacing',p,must_replace(p,'    throughput =','\n    throughput ='),'control: extra blank line','sample_project/python_kpi.py')
add('throughput','local_rename',p,must_replace(must_replace(p,'throughput = ','daily_rate = '),'return throughput','return daily_rate'),'controlled local variable renaming','sample_project/python_kpi.py')
add('throughput','multiplier25',p,must_replace(p,'* 24','* 25'),'controlled arithmetic error in original function','sample_project/python_kpi.py')
add('throughput','sparse_hidden13',p,must_replace(p,'    throughput =','    if hours_online == 13:\n        return -1.0\n    throughput ='),'controlled branch at untested input','sample_project/python_kpi.py')
add('emissions','exact_same',e,e,'same source positive control','sample_projects/leap_enterprise_scenarios/kpi_environment_emissions_intensity.py',False)
add('emissions','comment_only',e,'# controlled comment-only change\n'+e,'control: added comment','sample_projects/leap_enterprise_scenarios/kpi_environment_emissions_intensity.py')
add('emissions','denominator_plus1',e,must_replace(e,'    return total_co2e_kg / net_exported_mwh','    return total_co2e_kg / (net_exported_mwh + 1)'),'controlled arithmetic change','sample_projects/leap_enterprise_scenarios/kpi_environment_emissions_intensity.py')
add('emissions','sparse_hidden1',e,must_replace(e,'    return total_co2e_kg / net_exported_mwh','    if net_exported_mwh == 1:\n        return None\n    return total_co2e_kg / net_exported_mwh'),'controlled branch at untested input','sample_projects/leap_enterprise_scenarios/kpi_environment_emissions_intensity.py')

# The original SQL files include an extraneous Markdown closing code fence.
# Remove this parser artifact only in a temporary execution view; retain original bytes and hashes.
def clean_sql(code):
    return re.sub(r'\s*`{2,}\s*$', '',code).strip()

def sql_signature(code):
    code = clean_sql(code)
    code = '\n'.join(line for line in code.splitlines() if not line.lstrip().startswith('--'))
    return re.sub(r'\s+',' ',code.strip()).lower()

def python_signature(code):
    tree=ast.parse(code)
    funcs=[x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))]
    assert len(funcs)==1
    return ast.dump(funcs[0],include_attributes=False)

def execute_sql(code, family, rows):
    conn=sqlite3.connect(':memory:')
    try:
        if family=='yield':
            conn.execute('CREATE TABLE production_data(good_output_mass REAL, raw_input_mass REAL, scrap_mass REAL)')
            conn.executemany('INSERT INTO production_data VALUES(?,?,?)',rows)
        else:
            conn.execute('CREATE TABLE operations_data(actual_production_time REAL,planned_operation_time REAL,maintenance_down_time REAL)')
            conn.executemany('INSERT INTO operations_data VALUES(?,?,?)',rows)
        q=clean_sql(code)
        result=conn.execute(q).fetchall()
        return [x[0] for x in result]
    finally: conn.close()

def execute_python(code,family,rows):
    tree=ast.parse(code)
    f=[node for node in tree.body if isinstance(node,ast.FunctionDef)]
    assert len(f)==1, 'one function only'
    module=ast.Module(body=[f[0]],type_ignores=[])
    ast.fix_missing_locations(module)
    env={'__builtins__':{},'float':float}
    exec(compile(module,'<archived_pilot_source>','exec'),env)
    fun=env[f[0].name]
    return [fun(*row) for row in rows]

def vec_eq(a,b):
    if len(a)!=len(b):return False
    for x,y in zip(a,b):
        if x is None or y is None:
            if x is not y: return False
        elif abs(x-y)>1e-9*max(1,abs(x),abs(y)):
            return False
    return True

def dispatch(code,family,sparse=False):
    grp='sql' if family in ('yield','utilization') else 'python'
    name='sql_sparse_grid' if sparse else 'sql_reference_grid'
    pn='python_sparse_grid' if sparse else 'python_reference_grid'
    if grp=='sql':
        grid=PROTOCOL[name]['production_data' if family=='yield' else 'operations_data']
        return execute_sql(code,family,grid)
    return execute_python(code,family,PROTOCOL[pn][family])

out=[]
for c in cases:
    fam=c['family'];a,b=c['base'],c['changed']
    ref_a,ref_b=dispatch(a,fam),dispatch(b,fam)
    sp_a,sp_b=dispatch(a,fam,True),dispatch(b,fam,True)
    ref=vec_eq(ref_a,ref_b)
    cand={
        'raw_file_sha256_match':sha(a)==sha(b),
        'unchanged_kpi_identity_or_finding_presence':True,  # KPI identity and presence frozen in this experiment
        'syntax_fingerprint_match':(sql_signature(a)==sql_signature(b)) if fam in ('yield','utilization') else (python_signature(a)==python_signature(b)),
        'sparse_output_probe_match':vec_eq(sp_a,sp_b)
    }
    out.append({
        'case_id':f"{fam}/{c['variant']}",
        'family':fam,
        'variant':c['variant'],
        'archived_variant':not c['controlled'],
        'source_path':c['source_path'],
        'source_sha256_before':sha(a),
        'source_sha256_after':sha(b),
        'declared_transformation':c['transformation'],
        'reference_output_equivalent_on_full_grid':ref,
        'reference_full_outputs_before':ref_a,
        'reference_full_outputs_after':ref_b,
        'sparse_outputs_before':sp_a,
        'sparse_outputs_after':sp_b,
        'candidate_predictions':cand,
    })

(ROOT/'analysis/proxy_case_records.json').write_text(json.dumps(out,indent=2))
with (ROOT/'analysis/proxy_predictions.csv').open('w',newline='') as f:
    cols=['case_id','family','archived_variant','reference_output_equivalent_on_full_grid']+list(out[0]['candidate_predictions'])
    w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
    for x in out:
        w.writerow({**{k:x[k] for k in cols if k in x},**x['candidate_predictions']})

summary={ 'scope':'controlled proxy, not actual approval outcomes', 'cases':len(out),
          'families':len(set(x['family'] for x in out)),
          'reference_true':sum(x['reference_output_equivalent_on_full_grid'] for x in out),
          'reference_false':sum(not x['reference_output_equivalent_on_full_grid'] for x in out),
          'methods':{} }
for method in out[0]['candidate_predictions']:
    tn=tp=fn=fp=0
    for x in out:
        true=x['reference_output_equivalent_on_full_grid']; pred=x['candidate_predictions'][method]
        if pred and true:tp+=1
        elif pred and not true:fp+=1
        elif not pred and true:fn+=1
        else:tn+=1
    summary['methods'][method]={'valid_retained_TP':tp,'invalid_retained_FP':fp,
                               'valid_revoked_FN':fn,'invalid_revoked_TN':tn}
(ROOT/'analysis/proxy_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
