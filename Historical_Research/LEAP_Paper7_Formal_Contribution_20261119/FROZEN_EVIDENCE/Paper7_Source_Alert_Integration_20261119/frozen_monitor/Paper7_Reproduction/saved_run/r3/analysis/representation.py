"""Compare the endpoint-specific interface with the frozen reference."""
import json
import sys
from pathlib import Path
from collections import Counter

root = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'implementation'))
from monitor import monitor

def encode(events):
    prev = None
    for e in events:
        key = (e['c'],e['p'])
        packet = {k:e[k] for k in ('unit','t')}
        packet['reset'] = prev is not None and prev != key
        for ch in ('o','s'):
            if ch in e:
                raw=e[ch]
                packet[ch]={k:raw[k] for k in (('value','at') if ch=='o' else ('until',))}
                packet[ch]['applies'] = (raw['c'],raw['p']) == key
        yield packet
        prev = key

def decode(events):
    epoch = False
    for e in events:
        epoch ^= e['reset']
        key=str(epoch)
        packet=dict(t=e['t'],unit=e['unit'],c=key,p='fixed')
        for ch in ('o','s'):
            if ch in e:
                fields=dict(e[ch])
                fields['c']=key if fields.pop('applies') else 'other'
                fields['p']='fixed'
                packet[ch]=fields
        yield packet

def rows(name):
    with (root/'benchmark'/name).open() as f:
        yield from map(json.loads,f)

policy=json.loads((root/'benchmark/policy.json').read_text())
difference=Counter()
counts={'traces':0,'events':0,'decision_trace_mismatches':0,'reason_event_mismatches':0}
for case,ref in zip(rows('traces.jsonl'),rows('reference.jsonl'),strict=True):
    assert case['id']==ref['id']
    actual=monitor(decode(encode(case['trace'])),policy,case['severity'])
    gold=ref['outputs']
    counts['traces']+=1
    counts['events']+=len(gold)
    counts['decision_trace_mismatches']+=any(any(a[k]!=b[k] for k in ['state','active','severity']) for a,b in zip(actual,gold,strict=True))
    counts['reason_event_mismatches']+=sum(a['reason']!=b['reason'] for a,b in zip(actual,gold))
    difference.update((b['reason'],a['reason']) for a,b in zip(actual,gold) if b['reason']!=a['reason'])
counts['reason_pairs']={str(k):v for k,v in difference.items()}
print(json.dumps(counts))
