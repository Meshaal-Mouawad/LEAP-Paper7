"""Verify all packaged files using only the Python standard library."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parents[1]
manifest=root/'PACKAGE_SHA256SUMS'
count=0
for line in manifest.read_text().splitlines():
    expected,name=line.split('  ',1)
    path=root/name
    assert path.is_file(),name
    assert hashlib.sha256(path.read_bytes()).hexdigest()==expected,name
    count+=1
print(f'PASS: {count} packaged files match PACKAGE_SHA256SUMS')
