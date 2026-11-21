"""Run the unchanged Paper7 reproduction functions and retain each command log.

Usage: python retain_replay.py SOURCE_DIRECTORY NEW_RUN_DIRECTORY
The source manifest is verified before copying. The destination must not exist.
"""
from pathlib import Path
import datetime,hashlib,importlib.util,json,platform,shutil,sqlite3,subprocess,sys,time

def main():
    source=Path(sys.argv[1]).resolve();destination=Path(sys.argv[2]).resolve()
    if destination.exists():raise SystemExit('Use a new destination; existing runs are preserved.')
    manifest=[]
    for line in (source/'SHA256SUMS').read_text().splitlines():
        expected,name=line.split('  ',1)
        actual=hashlib.sha256((source/name).read_bytes()).hexdigest()
        if actual!=expected:raise RuntimeError('Input checksum mismatch: '+name)
        manifest.append({'path':name,'sha256':actual})
    shutil.copytree(source,destination)
    logs=destination/'fresh_execution';logs.mkdir()
    (logs/'verified_input_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    spec=importlib.util.spec_from_file_location('paper7_reproduce',source/'reproduce.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    commands=[]
    def logged_run(root,script,*args):
        idx=len(commands)+1;start=time.perf_counter();command=[sys.executable,'-B',script,*args]
        result=subprocess.run(command,cwd=root,capture_output=True,text=True)
        stem=f'{idx:02d}_{Path(script).stem}'
        (logs/(stem+'.stdout.log')).write_text(result.stdout)
        (logs/(stem+'.stderr.log')).write_text(result.stderr)
        row={'sequence':idx,'command':command,'cwd':'.','exit_code':result.returncode,
             'elapsed_seconds':time.perf_counter()-start,'stdout':stem+'.stdout.log','stderr':stem+'.stderr.log'}
        commands.append(row);(logs/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
        if result.returncode:raise RuntimeError(f'{script} failed; inspect {stem} logs')
        return result.stdout
    module.run=logged_run
    start=time.perf_counter();began=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        result=module.reproduce(destination)
    except BaseException as error:
        (logs/'failure.json').write_text(json.dumps({'error':repr(error),'began_utc':began},indent=2)+'\n')
        raise
    import pandas
    result.update(began_utc=began,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  elapsed_seconds=time.perf_counter()-start,pandas=pandas.__version__,platform=platform.platform(),
                  input_files_verified=len(manifest),commands_executed=len(commands),all_commands_exit_zero=all(x['exit_code']==0 for x in commands))
    (logs/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
