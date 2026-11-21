# Paper 7 — Provisional scientific reconstruction (research-stage text)

**Status: working narrative, not a submission manuscript.** The claim below is limited to the completed tests. No recorded human authorization outcome has yet been established.

## Candidate title

When Source Revisions Change Review Authority: Comparing Evidence-Bound Approval Strategies in KPI Documentation

## Research argument

Automated documentation systems can reconstruct business-metric definitions from source code, but reviewing a definition often requires human approval. A previously accepted explanation or deferral has a particular scope: it concerns identified source evidence under a stated policy. When that source changes, a review system must determine whether the original decision still applies. Reusing an obsolete authorization can keep a relevant warning out of view; invalidating an unchanged approval can interrupt legitimate work. The scientific problem is therefore not merely detecting that code changed, but establishing what an earlier authorization was permitted to cover and whether the changed evidence still falls inside that scope.

LEAP, a literate-programming system that extracts key performance indicators from SQL and Python, offers a source-grounded setting for examining this problem. Its archived governance specification requires source-linked review controls and business-approved overrides. An audit of the archived implementation identified a mismatch between that documented authority rule and the code that applies definition overrides. The matcher allows an override with a missing source signature to modify generated fields, while pending and rejected status records also reach the field-update path. Ten controlled input cases reproduced six such specification mismatches. The archived main-branch ledgers contain no active signed approvals, so these findings identify executable control weaknesses rather than observed user incidents.

A separate controlled experiment compared four authorization-matching strategies on 24 source pairs derived from archived SQL and Python KPI examples. An independently fixed audit-input grid served as the bounded source-output reference. Exact file matching rejected ten equivalent-but-edited pairs, an identity-only rule retained ten changed-output pairs, syntax fingerprinting rejected five equivalent pairs, and a sparse behavioral probe retained four changes whose effects occurred outside its sampled inputs. The resulting reviewer-facing differences were traced through the unchanged episode monitor: authorization mismatches changed the displayed state and reason, while leaving episode activity intact. The experiment establishes distinct trade-offs among source-matching policies on its controlled cases.

The resulting publishable research question must be answered against genuine, independently adjudicated approvals: **When a source-linked finding changes, what evidence warrants retaining an earlier review deferral, and which strategy preserves human authorization outcomes most accurately?** The present technical study establishes the experimental instrumentation and source-level failure cases. The absence of authenticated historical approval transitions means the broader scientific contribution awaits that reference evidence.

## Proposed article architecture after the authorization reference is established

1. Begin with the concrete source-revision approval problem and one fully traced real review case.
2. Explain source findings, accepted suppressions, version matching, and their demonstrated prior solutions with the closest literature.
3. State an authorization contract derived from authentic review decisions and source provenance.
4. Present distinct source revisions and independently adjudicated approval outcomes before introducing the matching strategies.
5. Compare unsafe retention, needless revocation, unknown references, and reviewer-facing display consequences.
6. Explain how the results advance warning-evolution research and why the selected method is supported by the actual outcomes.
7. Consolidate limitations in a dedicated final section.

The original Paper 7 sufficiency propositions remain available as supporting formal machinery; the constructed 4,935-trace evaluation retains its documented evidence role.
