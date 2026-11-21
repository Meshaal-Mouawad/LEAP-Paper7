#!/usr/bin/env python3
"""Narrow code-level diagnostics for two genuine Python KPI source revisions.
Does not generate human approval/deferral labels.
"""
from pathlib import Path
import ast,csv,json,contextlib,io
root=Path(__file__).resolve().parent.parent
rows={r['case_id']:r for r in csv.DictReader((root/'data/real_source_revisions.csv').open())}
results=[]

# Python throughput: identical function AST after documentation and formatting edits.
for cid in ('P7R02','P7R08'):
 case=root/'cases'/cid
 a=ast.parse((case/'before.py').read_text())
 b=ast.parse((case/'after.py').read_text())
 assert ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False)
 results.append({'case_id':cid,'check':'PYTHON_AST_IDENTICAL','outcome':'PASS',
                 'scope':'Same executable AST across source versions; no human authorization inference'})

# KPI100: safe isolated execution with source-level allowed AST nodes only.
def run_tiny(src):
 tree=ast.parse(src)
 allowed=(ast.Module,ast.Assign,ast.Expr,ast.Name,ast.Load,ast.Store,ast.Constant,
          ast.BinOp,ast.Div,ast.Mult,ast.Call)
 assert all(isinstance(x,allowed) for x in ast.walk(tree))
 # whitelist builtin function and assigned names only
 assert set(n.id for n in ast.walk(tree) if isinstance(n,ast.Name)) <= {'inventory','daily_cogs','days_of_working_inventory','print'}
 out=io.StringIO()
 with contextlib.redirect_stdout(out):
  try:
   exec(compile(tree,'source_kpi100','exec'),{'__builtins__':{'print':print}}, {})
   return {'status':'OK','output':out.getvalue().strip()}
  except Exception as ex:
   return {'status':type(ex).__name__,'output':''}
case=root/'cases/P7R09'
a=run_tiny((case/'before.py').read_text());b=run_tiny((case/'after.py').read_text())
assert a['status']=='NameError' and b['status']=='OK' and b['output']=='Days of Working Inventory: 7300.0'
results.append({'case_id':'P7R09','check':'ISOLATED_RECORDED_SOURCE_EXECUTION',
                'before':a,'after':b,'outcome':'PASS',
                'scope':'Before lacks local declarations; after supplies placeholders. Different standalone behavior, not a business approval outcome'})
(root/'data/python_source_execution_tests.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
