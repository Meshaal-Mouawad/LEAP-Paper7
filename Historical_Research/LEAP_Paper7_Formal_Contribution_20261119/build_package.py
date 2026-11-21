#!/usr/bin/env python3
"""Rebuild the manifest and self-excluding ZIP from this delivery directory."""
import csv, hashlib, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ZIP=ROOT/(ROOT.name+'.zip')
MANIFEST=ROOT/'MANIFEST_SHA256.csv'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and p not in (ZIP,MANIFEST) and '__pycache__' not in p.parts)
with MANIFEST.open('w',newline='') as out:
 writer=csv.writer(out);writer.writerow(['path','bytes','sha256'])
 for p in files:writer.writerow([p.relative_to(ROOT).as_posix(),p.stat().st_size,digest(p)])
with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as out:
 for p in files+[MANIFEST]:out.write(p,(Path(ROOT.name)/p.relative_to(ROOT)).as_posix())
with zipfile.ZipFile(ZIP) as archive:
 assert archive.testzip() is None
 expected={(Path(ROOT.name)/p.relative_to(ROOT)).as_posix() for p in files+[MANIFEST]}
 assert set(archive.namelist())==expected
 for p in files+[MANIFEST]:
  assert archive.read((Path(ROOT.name)/p.relative_to(ROOT)).as_posix())==p.read_bytes()
with MANIFEST.open() as inp:
 rows=list(csv.DictReader(inp))
assert len(rows)==len(files)
for row in rows:
 p=ROOT/row['path']
 assert p.stat().st_size==int(row['bytes']) and digest(p)==row['sha256']
print({'manifest_files':len(files),'zip_entries':len(files)+1,'zip_bytes':ZIP.stat().st_size,'zip_sha256':digest(ZIP)})
