#!/usr/bin/env python3
"""Optional original-extractor comparison with a separately supplied source archive."""
from __future__ import annotations
import importlib.util, json, sys, tempfile
from pathlib import Path
from zipfile import ZipFile
root=Path(__file__).resolve().parent

def load(p,n):
    spec=importlib.util.spec_from_file_location(n,p)
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

def main(archive):
    with ZipFile(archive) as z, tempfile.TemporaryDirectory() as tmp:
        member=next(n for n in z.namelist() if n.endswith('bluebook_generator/kpi_extractor.py') and not n.startswith('__MACOSX/'))
        origin=Path(tmp)/'original_extractor.py'
        origin.write_bytes(z.read(member))
        first=load(origin,'origin_extractor')
        second=load(root/'src/kpi_extractor.py','fixed_extractor')
        count=0
        for f in sorted((root/'cases').glob('P7R*/*')):
            data=f.read_text(encoding='utf8')
            lang=first._detect_language_by_extension(f.suffix)
            assert first._extract_from_text(data,lang)==second._extract_from_text(data,lang),f.name
            count+=1
    print(json.dumps({'checked_snapshots':count,'result':'PASS'}))
if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('Usage: python verify_parser_snapshot.py SOURCE_ARCHIVE.zip')
    main(sys.argv[1])
