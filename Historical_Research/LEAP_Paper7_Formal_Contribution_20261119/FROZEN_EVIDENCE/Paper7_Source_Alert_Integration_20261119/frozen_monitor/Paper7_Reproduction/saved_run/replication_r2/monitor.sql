-- Independent Paper 7 full-policy baseline in SQLite recursive SQL.
-- Inputs: events with normalized times and strictly validated scalar types;
-- policy(D,C,E,F); params(base_severity). No Python monitor/oracle is called.
WITH RECURSIVE
previous AS (
  SELECT *, lag(c) OVER (ORDER BY idx) AS prev_c,
            lag(p) OVER (ORDER BY idx) AS prev_p FROM events
),
classified AS (
  SELECT *,
    CASE WHEN idx>1 AND p<>prev_p THEN 'POLICY_CHANGE'
         WHEN idx>1 AND c<>prev_c THEN 'CONTEXT_CHANGE' ELSE NULL END AS reset_reason,
    CASE WHEN obs_present=0 THEN 'MISSING'
         WHEN oc<>c THEN 'CONTEXT_MISMATCH'
         WHEN op<>p THEN 'POLICY_MISMATCH'
         WHEN t-at<0 THEN 'FUTURE'
         WHEN t-at>(SELECT F FROM policy) THEN 'STALE'
         WHEN value IS NULL THEN 'CONFLICT' ELSE NULL END AS quality,
    CASE WHEN sup_present=1 AND sc=c AND sp=p AND t<until_time THEN 1 ELSE 0 END AS suppressed
  FROM previous
),
-- Each event traverses four SQL phases: reset, qualify, activate/clear, output.
-- opened_at NULL is inactive; qualification clocks retain physical event time.
replay(idx,phase,positive_start,negative_start,opened_at) AS (
  SELECT 0,3,NULL,NULL,NULL
  UNION ALL
  SELECT
    e.idx,
    CASE WHEN r.phase=3 THEN 0 ELSE r.phase+1 END,
    CASE
      WHEN r.phase=3 AND e.reset_reason IS NOT NULL THEN NULL
      WHEN r.phase=0 AND (e.quality IS NOT NULL OR e.value=0) THEN NULL
      WHEN r.phase=0 AND e.value=1 AND r.opened_at IS NULL THEN coalesce(r.positive_start,e.t)
      ELSE r.positive_start END,
    CASE
      WHEN r.phase=3 AND e.reset_reason IS NOT NULL THEN NULL
      WHEN r.phase=0 AND (e.quality IS NOT NULL OR e.value=1 OR r.opened_at IS NULL) THEN NULL
      WHEN r.phase=0 AND e.value=0 AND r.opened_at IS NOT NULL THEN coalesce(r.negative_start,e.t)
      WHEN r.phase=1 AND e.quality IS NULL AND e.value=0 AND r.opened_at IS NOT NULL
           AND e.t-r.negative_start>=(SELECT C FROM policy) THEN NULL
      ELSE r.negative_start END,
    CASE
      WHEN r.phase=3 AND e.reset_reason IS NOT NULL THEN NULL
      WHEN r.phase=1 AND e.quality IS NULL AND e.value=1 AND r.opened_at IS NULL
           AND e.t-r.positive_start>=(SELECT D FROM policy) THEN e.t
      WHEN r.phase=1 AND e.quality IS NULL AND e.value=0 AND r.opened_at IS NOT NULL
           AND e.t-r.negative_start>=(SELECT C FROM policy) THEN NULL
      ELSE r.opened_at END
  FROM replay r JOIN classified e ON e.idx=CASE WHEN r.phase=3 THEN r.idx+1 ELSE r.idx END
),
verdicts AS (
  SELECT e.idx, e.quality, e.reset_reason, r.opened_at IS NOT NULL AS active,
    CASE WHEN e.quality IS NOT NULL THEN 'UNKNOWN'
         WHEN r.opened_at IS NOT NULL AND e.suppressed=1 THEN 'SUPPRESSED'
         WHEN r.opened_at IS NOT NULL AND e.t-r.opened_at>=(SELECT E FROM policy) THEN 'ESCALATED'
         WHEN r.opened_at IS NOT NULL THEN 'ACTIVE'
         WHEN r.positive_start IS NOT NULL THEN 'PENDING' ELSE 'CLEAR' END AS state
  FROM replay r JOIN classified e ON e.idx=r.idx WHERE r.phase=3
)
SELECT idx,state,active,
  CASE WHEN state='UNKNOWN' THEN 'UNKNOWN'
       WHEN state='ACTIVE' THEN (SELECT base_severity FROM params)
       WHEN state='ESCALATED' THEN 'HIGH' ELSE 'NONE' END AS severity,
  CASE WHEN quality IS NOT NULL THEN quality
       WHEN reset_reason IS NOT NULL THEN reset_reason
       WHEN state='SUPPRESSED' THEN 'SUPPRESSION' ELSE 'STATE' END AS reason
FROM verdicts ORDER BY idx;
