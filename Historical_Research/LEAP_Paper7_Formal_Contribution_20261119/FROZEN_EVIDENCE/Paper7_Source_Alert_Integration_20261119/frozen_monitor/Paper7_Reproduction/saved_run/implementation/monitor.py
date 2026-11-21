"""Paper 7 new version-bound governance episode monitor; offline only."""
from math import isfinite

def numeric(v):
    if isinstance(v,bool) or not isinstance(v,(int,float)) or not isfinite(v): raise ValueError('finite numeric value required')
    return float(v)

def version(v):
    if not isinstance(v,str) or not v: raise ValueError('nonempty version required')
    return v

def validate(e,policy,last):
    try:
        scale={'s':1.,'ms':.001}[e['unit']]
        t=numeric(e['t'])*scale
        if last is not None and t<=last: raise ValueError('nonmonotone time')
        version(e['c']);version(e['p'])
        for x in ('D','C','E','F'):
            if numeric(policy[x])<0:raise ValueError('negative duration')
        for k in ('o','s'):
            if k in e:
                z=e[k];version(z['c']);version(z['p'])
                numeric(z['at' if k=='o' else 'until'])
                if k=='o' and z['value'] is not None and type(z['value']) is not bool: raise ValueError('invalid observation')
        return t,scale
    except (KeyError,TypeError) as exc: raise ValueError('invalid event schema') from exc

def monitor(trace, policy, base_severity='High', mode='bound'):
    active=False; positive=negative=opened=None; prior=None; last=None; outputs=[]
    for e in trace:
        t,scale=validate(e,policy,last);last=t
        reset=None
        if prior is not None and (e['c'],e['p'])!=prior and mode!='timer_only':
            reset='POLICY_CHANGE' if e['p']!=prior[1] else 'CONTEXT_CHANGE'
            active=False; positive=negative=opened=None
        prior=(e['c'],e['p'])
        o=e.get('o'); reason=None
        bind=mode not in ('timer_only','no_evidence_binding')
        if o is None: reason='MISSING'
        elif bind and o['c']!=e['c']: reason='CONTEXT_MISMATCH'
        elif bind and o['p']!=e['p']: reason='POLICY_MISMATCH'
        elif t-o['at']*scale<0: reason='FUTURE'
        elif mode!='no_freshness' and t-o['at']*scale>policy['F']: reason='STALE'
        elif o['value'] is None:reason='CONFLICT'
        if reason:
            positive=negative=None; state='UNKNOWN'
        else:
            if o['value']:
                negative=None
                if not active:
                    if positive is None:positive=t
                    if t-positive>=policy['D']:active=True;opened=t
            else:
                positive=None
                if active:
                    if negative is None:negative=t
                    if t-negative>=policy['C']: active=False;opened=negative=None
                else:negative=None
            state=('ESCALATED' if t-opened>=policy['E'] else 'ACTIVE') if active else ('PENDING' if positive is not None else 'CLEAR')
            s=e.get('s')
            suppress=bool(s and t<s['until']*scale and ((s['c']==e['c'] and s['p']==e['p']) or mode in ('timer_only','no_suppression_binding')))
            if suppress and active: state='SUPPRESSED'
            reason=reset or ('SUPPRESSION' if state=='SUPPRESSED' else 'STATE')
        severity='HIGH' if state=='ESCALATED' else (base_severity if state=='ACTIVE' else ('UNKNOWN' if state=='UNKNOWN' else 'NONE'))
        outputs.append(dict(state=state,active=active,severity=severity,reason=reason))
    return outputs

def snapshot_baseline(trace, policy, base_severity='High'):
    """Per-snapshot LEAP finding value, no experimental lifecycle imposed."""
    out=[];last=None
    for e in trace:
        t,scale=validate(e,policy,last);last=t
        v=e.get('o',{}).get('value')
        state='UNKNOWN' if v is None else ('ACTIVE' if v else 'CLEAR')
        out.append(dict(state=state,active=v is True,severity=base_severity if v is True else ('UNKNOWN' if v is None else 'NONE'),reason='SNAPSHOT'))
    return out
