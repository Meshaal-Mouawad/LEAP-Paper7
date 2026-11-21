from pathlib import Path
import re,hashlib,json
R=Path('/mnt/data/Paper7_M1M6_Revision_20261119')
a=(R/'gold/Paper7.tex').read_text();b=(R/'work/Paper7.tex').read_text()
res={}
for label in ['tab:intervention-taxonomy','tab:results','tab:attributes']:
 def get(s):
  pos=s.index('\\label{'+label+'}')
  begin=s.rfind('\\begin{table}',0,pos)
  end=s.index('\\end{table}',pos)+len('\\end{table}')
  return s[begin:end]
 res[label]={'byte_identical':get(a)==get(b)}
for name in ['method_pipeline.pdf','necessity_witness.pdf','trace_mismatches.pdf']:
 x=(R/'gold'/name).read_bytes();y=(R/'work'/name).read_bytes()
 res[name]={'sha256':hashlib.sha256(y).hexdigest(),'byte_identical':x==y}
props=re.compile(r'\\begin\{proposition\}(?:\[[^\]]*\])?(?:\\label\{[^}]+\})?(.*?)\\end\{proposition\}',re.S)
old=props.findall(a);new=props.findall(b)
res['original_proposition_count']=len(old)
res['new_proposition_count']=len(new)
res['propositions_1_2_3_byte_identical']=all(old[i]==new[i] for i in range(3))
res['original_decision_only_proposition_semantics_preserved']=('$(r_i,v_i,m_i)$' in old[3] and '$(\\Delta_i,v_i,m_i)$' in new[4] and old[3].replace('r_i','\\Delta_i')==new[4])
res['frozen_reproduction_zip_sha256']=hashlib.sha256(Path('/workspace/scratch/ca19aaee5426/research/paper7_risk_alarm/revision_20261118/deliverables/LEAP_Paper7_Reproduction_20261118.zip').read_bytes()).hexdigest()
assert all(v['byte_identical'] for v in res.values() if isinstance(v,dict) and 'byte_identical' in v)
assert res['propositions_1_2_3_byte_identical']
assert res['original_decision_only_proposition_semantics_preserved']
(R/'reports/PROTECTED_CONTENT_AUDIT.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
