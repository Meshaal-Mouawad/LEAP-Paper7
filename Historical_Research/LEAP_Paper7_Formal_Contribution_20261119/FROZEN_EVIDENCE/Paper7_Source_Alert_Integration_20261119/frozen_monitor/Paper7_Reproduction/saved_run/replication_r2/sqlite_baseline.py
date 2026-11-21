"""Independent SQLite runtime baseline. Python only validates/loads SQL inputs."""
import math
import sqlite3
from pathlib import Path
SQL=Path(__file__).with_name('monitor.sql').read_text()

def finite(value):
    if type(value) not in (int,float) or not math.isfinite(value):
        raise ValueError('finite numeric timestamp or duration required')
    return float(value)

def identity(value):
    if type(value) is not str or not value:
        raise ValueError('nonempty identity required')
    return value

def normalize(trace, policy):
    try:
        durations=[finite(policy[k]) for k in ('D','C','E','F')]
        if any(x<0 for x in durations): raise ValueError('negative duration')
        rows=[]; previous=None
        for idx,event in enumerate(trace,1):
            unit=event['unit']
            if unit not in ('s','ms'): raise ValueError('unknown time unit')
            scale=1.0 if unit=='s' else 0.001
            t=finite(event['t'])*scale
            c,p=identity(event['c']),identity(event['p'])
            if previous is not None and t<=previous: raise ValueError('non-increasing time')
            previous=t
            present=int('o' in event)
            oc=op=at=value=None
            if present:
                obs=event['o']; value=obs['value']
                if value is not None and type(value) is not bool: raise ValueError('strict bool/null observation')
                oc,op=identity(obs['c']),identity(obs['p']); at=finite(obs['at'])*scale
            suppressed=int('s' in event); sc=sp=until=None
            if suppressed:
                sup=event['s']; sc,sp=identity(sup['c']),identity(sup['p']); until=finite(sup['until'])*scale
            rows.append((idx,t,c,p,present,oc,op,at,value,suppressed,sc,sp,until))
    except (KeyError,TypeError,AttributeError) as exc:
        raise ValueError('malformed policy or event') from exc
    return rows,durations

def sqlite_monitor(trace,policy,base_severity='High'):
    rows,durations=normalize(trace,policy)
    with sqlite3.connect(':memory:') as db:
        db.execute('CREATE TABLE events(idx INTEGER PRIMARY KEY,t REAL,c TEXT,p TEXT,obs_present INTEGER,oc TEXT,op TEXT,at REAL,value INTEGER,sup_present INTEGER,sc TEXT,sp TEXT,until_time REAL)')
        db.execute('CREATE TABLE policy(D REAL,C REAL,E REAL,F REAL)')
        db.execute('CREATE TABLE params(base_severity TEXT)')
        db.executemany('INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',rows)
        db.execute('INSERT INTO policy VALUES(?,?,?,?)',durations)
        db.execute('INSERT INTO params VALUES(?)',(base_severity,))
        return [dict(state=state,active=bool(active),severity=severity,reason=reason)
                for idx,state,active,severity,reason in db.execute(SQL)]
