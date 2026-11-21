"""Paper 7 reference oracle v2: required unit validation corrected after freeze.

Frozen v1 is preserved in oracle.py; all valid benchmark outputs remain unchanged.

Uses complete-prefix replay and backward reconstruction of evidence runs, rather
than importing or calling the incremental monitor. AI-agent implementation;
not independent human adjudication. All times are normalized to seconds.
"""
from math import isfinite


def _number(v):
    if isinstance(v, bool) or not isinstance(v, (float, int)) or not isfinite(v):
        raise ValueError('finite numeric time/duration required')
    return float(v)


def _identity(v):
    if not isinstance(v, str) or not v:
        raise ValueError('nonempty context and policy strings required')
    return v


def _normal(trace, policy):
    if not isinstance(policy, dict):
        raise ValueError('policy must be a mapping')
    durations = {}
    for key in ('D', 'C', 'E', 'F'):
        try:
            durations[key] = _number(policy[key])
        except KeyError as error:
            raise ValueError('missing policy duration') from error
        if durations[key] < 0:
            raise ValueError('negative duration')
    rows = []
    prev_t = None
    for event in trace:
        try:
            if not isinstance(event, dict):
                raise ValueError('event mapping required')
            unit = event['unit']
            if unit not in ('s', 'ms'):
                raise ValueError('invalid unit')
            scale = 1.0 if unit == 's' else 0.001
            time = _number(event['t']) * scale
            context, version = _identity(event['c']), _identity(event['p'])
            if prev_t is not None and time <= prev_t:
                raise ValueError('event time must strictly increase')
            prev_t = time
            observed = None
            if 'o' in event:
                obs = event['o']
                if not isinstance(obs, dict):
                    raise ValueError('observation mapping required')
                if obs['value'] is not None and type(obs['value']) is not bool:
                    raise ValueError('observation value must be bool/null')
                observed = {'value':obs['value'], 'c':_identity(obs['c']),
                            'p':_identity(obs['p']), 'at':_number(obs['at'])*scale}
            deferred = False
            if 's' in event:
                sup = event['s']
                if not isinstance(sup, dict):
                    raise ValueError('suppression mapping required')
                sc, sp = _identity(sup['c']), _identity(sup['p'])
                until = _number(sup['until'])*scale
                deferred = sc == context and sp == version and time < until
        except (KeyError, TypeError) as error:
            raise ValueError('malformed event') from error
        reason = None
        if observed is None:
            reason = 'MISSING'
        elif observed['c'] != context:
            reason = 'CONTEXT_MISMATCH'
        elif observed['p'] != version:
            reason = 'POLICY_MISMATCH'
        elif time - observed['at'] < 0:
            reason = 'FUTURE'
        elif time - observed['at'] > durations['F']:
            reason = 'STALE'
        elif observed['value'] is None:
            reason = 'CONFLICT'
        value = None if reason else observed['value']
        rows.append({'t':time, 'c':context, 'p':version, 'quality':reason,
                     'v':value,'suppressed':deferred})
    return rows, durations


def _replay_prefix(rows, end, durations):
    """Reconstruct active episode and qualification from whole prefix."""
    # Current context begins immediately after the last identity change.
    begin = end
    while begin and (rows[begin-1]['c'],rows[begin-1]['p']) == (rows[end]['c'],rows[end]['p']):
        begin -= 1
    opened = None
    for k in range(begin,end+1):
        row = rows[k]
        if row['quality'] is not None:
            continue
        # Qualification is based on the maximal contiguous valid equal-value run.
        start = k
        while start > begin and rows[start-1]['quality'] is None and rows[start-1]['v'] is row['v']:
            start -= 1
        elapsed = row['t'] - rows[start]['t']
        if row['v'] and opened is None and elapsed >= durations['D']:
            opened = row['t']
        elif not row['v'] and opened is not None and elapsed >= durations['C']:
            opened = None
    pending = opened is None and rows[end]['quality'] is None and rows[end]['v'] is True
    return opened, pending


def oracle(trace, policy, base_severity='High'):
    rows, durations = _normal(trace, policy)
    outputs=[]
    for end,row in enumerate(rows):
        opened,pending=_replay_prefix(rows,end,durations)
        active=opened is not None
        if row['quality']:
            state,severity,reason='UNKNOWN','UNKNOWN',row['quality']
        else:
            state=('ESCALATED' if row['t']-opened >= durations['E'] else 'ACTIVE') if active else ('PENDING' if pending else 'CLEAR')
            if active and row['suppressed']:
                state='SUPPRESSED'
            severity='HIGH' if state=='ESCALATED' else (base_severity if state=='ACTIVE' else 'NONE')
            if end and row['p'] != rows[end-1]['p']:
                reason='POLICY_CHANGE'
            elif end and row['c'] != rows[end-1]['c']:
                reason='CONTEXT_CHANGE'
            else:
                reason='SUPPRESSION' if state=='SUPPRESSED' else 'STATE'
        outputs.append({'state':state,'active':active,'severity':severity,'reason':reason})
    return outputs
