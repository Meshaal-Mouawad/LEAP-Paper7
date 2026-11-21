#!/usr/bin/env python3
from pathlib import Path
import csv,hashlib,ast,re,json
ROOT=Path(__file__).resolve().parent.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def fingerprint(path,b):
 txt=b.decode('utf8','replace')
 if path.endswith('.py'):return ast.dump(ast.parse(txt),include_attributes=False)
 if path.endswith(('.sql','.tsql')):return re.sub(r'\s+','', '\n'.join(v.split('--',1)[0] for v in txt.splitlines())).lower()
 if path.endswith('.abap'):return re.sub(r'\s+','', '\n'.join(v for v in txt.splitlines() if not v.lstrip().startswith('*'))).lower()
 return txt
rows=list(csv.DictReader((ROOT/'data/real_source_revisions.csv').open()))
for r in rows:
 d=ROOT/'cases'/r['case_id'];ext=Path(r['source_path']).suffix
 a=(d/('before'+ext)).read_bytes();b=(d/('after'+ext)).read_bytes()
 assert sha(a)==r['before_sha256'] and sha(b)==r['after_sha256'],r['case_id']
 assert (fingerprint(r['source_path'],a)==fingerprint(r['source_path'],b))==(r['technical_code_representation_equal']=='true'),r['case_id']
assert len(rows)==9
print('VERIFIED 9 actual archived source pairs and all stored content hashes; no independent authorization labels present')
