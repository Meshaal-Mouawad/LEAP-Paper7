"""Paper 7 policy encoded as states of authentic pinned PyContract.

No LEAP monitor, reference oracle or SQLite baseline is imported. The external
engine owns event dispatch, state retention and replacement. Policy guards and
verdict formatting are the study-specific PyContract specification.
"""
from pathlib import Path
import sys,math,contextlib,io
sys.path.insert(0,str(Path(__file__).resolve().parent/'upstream'))
import pycontract as pc


def _finite(x):
    if type(x) not in (float,int) or not math.isfinite(x):raise ValueError('finite number required')
    return float(x)

def _identity(x):
    if type(x) is not str or not x:raise ValueError('nonempty identity required')
    return x

def validate(trace,policy):
    try:
        params={k:_finite(policy[k]) for k in ('D','C','E','F')}
        if min(params.values())<0:raise ValueError('negative policy duration')
        events=[];previous=None
        for x in trace:
            if x['unit'] not in ('s','ms'):raise ValueError('unsupported time unit')
            factor=1 if x['unit']=='s' else .001
            t=_finite(x['t'])*factor
            if previous is not None and t<=previous:raise ValueError('non-increasing event time')
            previous=t
            e={'t':t,'c':_identity(x['c']),'p':_identity(x['p'])}
            if 'o' in x:
                o=x['o'];v=o['value']
                if v is not None and type(v) is not bool:raise ValueError('strict bool/null required')
                e['o']={'value':v,'c':_identity(o['c']),'p':_identity(o['p']),'at':_finite(o['at'])*factor}
            if 's' in x:
                s=x['s'];e['s']={'c':_identity(s['c']),'p':_identity(s['p']),'until':_finite(s['until'])*factor}
            events.append(e)
    except (KeyError,TypeError,AttributeError) as error:raise ValueError('malformed packet or policy') from error
    return events,params


class PolicyState(pc.State):
    """Shared version/quality guards; concrete states encode the lifecycle."""
    def transition(self,e):
        m=self.monitor
        m.transitions_executed+=1
        reason=None
        reset=self.p is not None and (self.c!=e['c'] or self.p!=e['p'])
        if reset:
            reason='POLICY_CHANGE' if self.p!=e['p'] else 'CONTEXT_CHANGE'
        current=self
        if reset or self.p is None:
            current=GovernanceMonitor.Dormant(e['c'],e['p'])
            current.set_monitor_to(m)
        quality=None
        if 'o' not in e:quality='MISSING'
        else:
            o=e['o']
            if o['c']!=e['c']:quality='CONTEXT_MISMATCH'
            elif o['p']!=e['p']:quality='POLICY_MISMATCH'
            elif e['t']<o['at']:quality='FUTURE'
            elif e['t']-o['at']>m.params['F']:quality='STALE'
            elif o['value'] is None:quality='CONFLICT'
        if quality:
            if isinstance(current,(GovernanceMonitor.Raised,GovernanceMonitor.Recovering)):
                target=GovernanceMonitor.Raised(e['c'],e['p'],current.opened)
            else:target=GovernanceMonitor.Dormant(e['c'],e['p'])
            output={'state':'UNKNOWN','active':isinstance(target,GovernanceMonitor.Raised),'severity':'UNKNOWN','reason':quality}
        else:
            target=current.observe(e['t'],e['o']['value'],m.params)
            active=isinstance(target,(GovernanceMonitor.Raised,GovernanceMonitor.Recovering))
            if active:
                state='ESCALATED' if e['t']-target.opened>=m.params['E'] else 'ACTIVE'
                s=e.get('s')
                if s is not None and s['c']==e['c'] and s['p']==e['p'] and e['t']<s['until']:state='SUPPRESSED'
            else:state='PENDING' if isinstance(target,GovernanceMonitor.Qualifying) else 'CLEAR'
            severity='HIGH' if state=='ESCALATED' else m.base_severity if state=='ACTIVE' else 'NONE'
            output={'state':state,'active':active,'severity':severity,'reason':reason or ('SUPPRESSION' if state=='SUPPRESSED' else 'STATE')}
        m.outputs.append(output)
        return target


class GovernanceMonitor(pc.Monitor):
    def __init__(self,params,base_severity):
        self.params=params;self.base_severity=base_severity;self.outputs=[];self.transitions_executed=0
        super().__init__()
        self.option_print_summary=False

    @pc.initial
    @pc.data
    class Dormant(PolicyState):
        c:str|None=None
        p:str|None=None
        def observe(self,t,value,P):
            if not value:return self
            return GovernanceMonitor.Raised(self.c,self.p,t) if P['D']==0 else GovernanceMonitor.Qualifying(self.c,self.p,t)

    @pc.data
    class Qualifying(PolicyState):
        c:str
        p:str
        started:float
        def observe(self,t,value,P):
            if not value:return GovernanceMonitor.Dormant(self.c,self.p)
            if t-self.started>=P['D']:return GovernanceMonitor.Raised(self.c,self.p,t)
            return self

    @pc.data
    class Raised(PolicyState):
        c:str
        p:str
        opened:float
        def observe(self,t,value,P):
            if value:return self
            return GovernanceMonitor.Dormant(self.c,self.p) if P['C']==0 else GovernanceMonitor.Recovering(self.c,self.p,self.opened,t)

    @pc.data
    class Recovering(PolicyState):
        c:str
        p:str
        opened:float
        started:float
        def observe(self,t,value,P):
            if value:return GovernanceMonitor.Raised(self.c,self.p,self.opened)
            if t-self.started>=P['C']:return GovernanceMonitor.Dormant(self.c,self.p)
            return self


def pycontract_monitor(trace,policy,base_severity='High',audit=False):
    events,params=validate(trace,policy)
    pc.Monitor.reset()
    m=GovernanceMonitor(params,base_severity)
    state_log=[]
    for event in events:
        m.eval(event)  # Authentic upstream Monitor.eval -> eval_states -> State.eval.
        if len(m.states)!=1:raise RuntimeError('expected exactly one live PyContract state')
        state_log.append(type(next(iter(m.states))).__name__)
    if m.event_count!=len(events) or m.transitions_executed!=len(events):
        raise RuntimeError('upstream dispatch count mismatch')
    with contextlib.redirect_stdout(io.StringIO()):
        m.end()
    if m.errors_found():raise RuntimeError('PyContract engine reports unexpected terminal error')
    return (m.outputs,{'engine_events':m.event_count,'state_transitions':m.transitions_executed,'state_classes':state_log}) if audit else m.outputs
