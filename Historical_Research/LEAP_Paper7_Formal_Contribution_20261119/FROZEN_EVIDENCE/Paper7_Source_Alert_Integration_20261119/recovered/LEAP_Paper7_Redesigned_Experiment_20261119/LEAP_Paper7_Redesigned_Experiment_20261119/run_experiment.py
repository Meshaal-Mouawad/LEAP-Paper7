#!/usr/bin/env python3
"""Fixed-input dual-output revision experiment for LEAP source examples.

Only standard-library modules are used. All inputs are preserved in cases/.
The study evaluates technical outputs, not organizational authorizations.
"""
from __future__ import annotations
import ast, csv, hashlib, importlib.util, json, os, re, sqlite3, subprocess, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
os.environ['LEAP_ENABLE_AI'] = '0'

def getmod(name):
    spec = importlib.util.spec_from_file_location(name, BASE / 'src' / (name + '.py'))
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

extractor = getmod('kpi_extractor')
generator = getmod('ai_generator')

SELECTED_FIELDS = ('description', 'objective', 'formula_description', 'used_in_kpis', 'input_measure', 'unit_of_measure', 'reporting_source', 'comments')

def digest(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def canonical(o):
    return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(',',':'))

def read_case(case, side):
    files = list((BASE / 'cases' / case).glob(side + '.*'))
    if len(files) != 1:
        raise ValueError(f'Expected one source for {case} {side}')
    return files[0], files[0].read_text(encoding='utf-8')

def fingerprint(file, text):
    if file.suffix == '.py':
        tree = ast.parse(text)
        return digest(ast.dump(tree, include_attributes=False).encode('utf-8')), 'PYTHON_AST'
    if file.suffix == '.abap':
        lines = []
        for line in text.splitlines():
            if line.lstrip().startswith('*'):
                continue
            lines.append(line.split('"',1)[0])
        stripped='\n'.join(lines)
        dtype='ABAP_COMMENT_STRIPPED_TOKENS'
    else:
        stripped=re.sub(r'/\*.*?\*/', '', text, flags=re.S)
        stripped='\n'.join(line.split('--',1)[0] for line in stripped.splitlines())
        dtype='SQL_COMMENT_STRIPPED_TOKENS'
    tokens=re.findall(r"'(?:''|[^'])*'|[A-Za-z_][\w]*|\d+(?:\.\d+)?|[^\s]",stripped)
    return digest(canonical([t if t.startswith("'") else t.lower() for t in tokens]).encode()),dtype

def dossier(file, text):
    lang=extractor._detect_language_by_extension(file.suffix)
    discovered=extractor._extract_from_text(text,lang)
    rows=[]
    for x in discovered:
        name=str(x.get('name') or '')
        details=generator.generate_kpi_details(name,text)
        rows.append({'kpi_name':name,'details':{k:str(details.get(k,'') or '') for k in SELECTED_FIELDS}})
    rows.sort(key=canonical)
    return {'candidate_count':len(rows),'entries':rows, 'signature':digest(canonical(rows).encode())}

def py_run(path, sample):
    runner='''import json,runpy,sys\np=sys.argv[1]\ntry:\n  d=runpy.run_path(p)\n  if 'calculate_demo_throughput' in d:\n    v=[d['calculate_demo_throughput'](*q) for q in [(100.,10.),(120.,0.),(180.,24.),(12.5,2.5)]]\n    print('FIXED_RESULTS:'+json.dumps(v))\nexcept Exception as e:\n  print('FIXED_ERROR:'+type(e).__name__)\n  sys.exit(12)\n'''
    try:
        p=subprocess.run([sys.executable,'-I','-B','-c',runner,str(path)],capture_output=True,text=True,timeout=4,env={'PYTHONNOUSERSITE':'1','PYTHONDONTWRITEBYTECODE':'1'})
    except subprocess.TimeoutExpired:
        return {'status':'TIMEOUT','values':[]}
    output=[line.strip() for line in p.stdout.splitlines() if line.strip()]
    if p.returncode != 0:
        status = next((s.partition(':')[2] for s in output if s.startswith('FIXED_ERROR:')),'ERROR')
        return {'status':status,'values':output}
    return {'status':'OK','values':output}

def sql_run(text):
    conn=sqlite3.connect(':memory:')
    conn.execute('CREATE TABLE unit_energy_summary (total_energy_mmbtu REAL, reference_energy_mmbtu REAL)')
    conn.executemany('INSERT INTO unit_energy_summary VALUES (?,?)',[(200,100),(0,100),(250,0)])
    conn.execute('CREATE TABLE batch_quality_summary (on_spec_batches REAL, total_batches REAL)')
    conn.executemany('INSERT INTO batch_quality_summary VALUES (?,?)',[(8,10),(0,8),(10,0),(12,12)])
    try:
        match=re.search(r'(?is)\bCREATE\s+VIEW\s+([a-zA-Z_][\w]*)\s+AS\b',text)
        if match:
            conn.executescript(text)
            cursor=conn.execute('SELECT * FROM "'+match.group(1)+'"')
        else:
            cursor=conn.execute(text)
        cols=[x[0] for x in cursor.description]
        values=[list(r) for r in cursor.fetchall()]
        return {'status':'OK','columns':cols,'rows':values}
    except sqlite3.Error as e:
        return {'status':type(e).__name__,'diagnostic':str(e).split(':')[0]}
    finally:
        conn.close()

def run_case(file,text):
    if file.suffix == '.py':
        # Writes a temporary copy only for executable, fixed-function calls.
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'isolated.py';path.write_text(text,encoding='utf8')
            return py_run(path, text)
    if file.suffix in ('.sql','.tsql'):
        return sql_run(text)
    return {'status':'NOT_EXECUTED','reason':'ABAP runtime unavailable'}

def load_manifest():
    with (BASE / 'case_manifest.csv').open(encoding='utf8',newline='') as f:
        return list(csv.DictReader(f))

def assess(case, before_file,before,after_file,after, stratum):
    fpb,method=fingerprint(before_file,before)
    fpa,_=fingerprint(after_file,after)
    db=dossier(before_file,before)
    da=dossier(after_file,after)
    rb=run_case(before_file,before)
    ra=run_case(after_file,after)
    if 'NOT_EXECUTED' in (rb['status'],ra['status']):
        ex='NOT_TESTED'
    elif rb['status']=='OperationalError' or ra['status']=='OperationalError':
        ex='UNRESOLVED_INPUT_BINDINGS'
    elif rb==ra and rb['status']=='OK':
        ex='EQUAL'
    else:
        ex='DIFFERENT'
    return {
     'case_id':case, 'stratum':stratum,'language':before_file.suffix.lstrip('.'),
     'source_bytes_changed':digest(before.encode())!=digest(after.encode()),
     'file_sha256_before':digest(before.encode()),'file_sha256_after':digest(after.encode()),
     'structure_sha256_before':fpb,'structure_sha256_after':fpa,
     'structure_changed':fpb!=fpa,'structure_method':method,
     'dossier_changed':db['signature']!=da['signature'],
     'dossier_before_count':db['candidate_count'],'dossier_after_count':da['candidate_count'],
     'dossier_before':db['entries'],'dossier_after':da['entries'],
     'dossier_before_sha256':db['signature'],'dossier_after_sha256':da['signature'],
     'runtime_status':ex,'runtime_before':rb,'runtime_after':ra,
     'baseline_exact_file_rechecks':digest(before.encode())!=digest(after.encode()),
     'baseline_structure_rechecks':fpb!=fpa,
     'baseline_dossier_rechecks':db['signature']!=da['signature'],
     'dual_endpoint_rechecks':fpb!=fpa or db['signature']!=da['signature'],
    }

def main():
    rows=[]
    for meta in load_manifest():
        case=meta['case_id'];pb,b=read_case(case,'before');pa,a=read_case(case,'after')
        assert digest(b.encode()) == meta['before_sha256'],case+' before mismatch'
        assert digest(a.encode()) == meta['after_sha256'],case+' after mismatch'
        rows.append(assess(case,pb,b,pa,a,'ARCHIVED_REVISION'))
    # Two deliberate controls using one unchanged archived source as the origin.
    p,base=read_case('P7R08','after')
    assert r'\times 24' in base and ') * 24' in base
    variants = [
       ('CTRL_DOC',base.replace(r'\times 24',r'\times 25',1)),
       ('CTRL_CODE',base.replace(') * 24',') * 25',1)),
    ]
    for name,modified in variants:
        rows.append(assess(name,p,base,p,modified,'CONTROL_CONSTRUCTED'))
    out=BASE/'outputs';out.mkdir(exist_ok=True)
    (out/'all_case_details.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    with (out/'version_transition_events.csv').open('w',newline='',encoding='utf8') as f:
        keys=['case_id','stratum','file_sha256_before','file_sha256_after','structure_sha256_before','structure_sha256_after','dossier_before_sha256','dossier_after_sha256','structure_changed','dossier_changed','dual_endpoint_rechecks']
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows({k:r[k] for k in keys} for r in rows)
    fields=['case_id','stratum','language','source_bytes_changed','structure_changed','dossier_changed','dossier_before_count','dossier_after_count','runtime_status','baseline_exact_file_rechecks','baseline_structure_rechecks','baseline_dossier_rechecks','dual_endpoint_rechecks']
    with (out/'paired_endpoints.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows({k:r[k] for k in fields} for r in rows)
    real=[r for r in rows if r['stratum']=='ARCHIVED_REVISION']
    executable=[r for r in real if r['runtime_status'] not in ('NOT_TESTED','UNRESOLVED_INPUT_BINDINGS')]
    runtime_same=[r for r in executable if r['runtime_status']=='EQUAL']
    counts={
      'archived_source_pairs':len(real),'constructed_controls':len(rows)-len(real),
      'changed_files':sum(r['source_bytes_changed'] for r in real),
      'structure_changed':sum(r['structure_changed'] for r in real),
      'dossier_changed':sum(r['dossier_changed'] for r in real),
      'dual_endpoint_change':sum(r['dual_endpoint_rechecks'] for r in real),
      'runtime_attempted_pairs':sum(r['runtime_status']!='NOT_TESTED' for r in real),
      'runtime_comparable_pairs':len(executable),'runtime_equal':len(runtime_same),
      'runtime_unresolved_bindings':sum(r['runtime_status']=='UNRESOLVED_INPUT_BINDINGS' for r in real),
      'runtime_different':sum(r['runtime_status']=='DIFFERENT' for r in executable),
      'runtime_equal_with_dossier_change':sum(r['dossier_changed'] for r in runtime_same),
      'file_only_changes_on_both_signatures':sum((not r['structure_changed']) and (not r['dossier_changed']) for r in real),
      'dossier_change_missed_by_structure_only':sum(r['dossier_changed'] and (not r['structure_changed']) for r in real),
      'structure_change_missed_by_dossier_only':sum(r['structure_changed'] and (not r['dossier_changed']) for r in real),
    }
    (out/'summary.json').write_text(json.dumps(counts,indent=2)+'\n',encoding='utf8')
    print(json.dumps(counts,indent=2))
    for r in rows:
        print(r['case_id'],r['stratum'], 'struct',r['structure_changed'],'doc',r['dossier_changed'],'runtime',r['runtime_status'])
    # Hard checks for control discrimination: each output differs in isolation.
    ctrl_doc=next(r for r in rows if r['case_id']=='CTRL_DOC')
    ctrl_code=next(r for r in rows if r['case_id']=='CTRL_CODE')
    assert (not ctrl_doc['structure_changed']) and ctrl_doc['dossier_changed'] and ctrl_doc['runtime_status']=='EQUAL', 'documentation control failed'
    assert ctrl_code['structure_changed'] and (not ctrl_code['dossier_changed']) and ctrl_code['runtime_status']=='DIFFERENT', 'execution control failed'
    print('CONTROL_CHECKS_PASS')

if __name__=='__main__':
    main()
