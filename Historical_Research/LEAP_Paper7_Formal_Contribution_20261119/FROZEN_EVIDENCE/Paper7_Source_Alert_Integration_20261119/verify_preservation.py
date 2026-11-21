#!/usr/bin/env python3
"""Verify recovered research bytes without rerunning historical experiments."""
import hashlib,json
from pathlib import Path
base=Path(__file__).resolve().parent
rows=json.loads((base/'preserved_input_manifest.json').read_text())
failures=[]
for row in rows:
 p=base/row['path']
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:
  failures.append(row['path'])
result={'files_checked':len(rows),'unchanged':len(rows)-len(failures),'failures':failures}
print(json.dumps(result,indent=2))
raise SystemExit(bool(failures))
