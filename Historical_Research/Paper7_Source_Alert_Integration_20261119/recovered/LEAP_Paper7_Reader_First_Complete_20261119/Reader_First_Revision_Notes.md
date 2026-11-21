# Paper 7 — reader-first reconstruction and verification

**Revision target:** *Version Comparisons Preserve Governance Alert Decisions Across Evidence and Policy Revisions*  
**Rejected baseline:** `LEAP_Paper7_Final_Revised_M1M6_20261119.pdf` (22 pages), matching `LEAP_Paper7_Final_LaTeX_M1M6_20261119.zip`.  
**Revised manuscript:** `LEAP_Paper7_Reader_First_Revised_20261119.pdf` (25 pages).  
**Status:** Substantive narrative revision completed; no claim of independent external acceptance or submission.

## Why the previous manuscript failed

The baseline opened Section 2.1 with “The source-documentation system is LEAP.” It did not expand LEAP or establish the source-to-documentation workflow before introducing its findings, dispatcher, review flag, and predicate families. That forced the reader to know an earlier paper. Later sections frequently led with notation, control names, benchmark counts, and implementations before supplying their scientific purpose. The paper's central empirical contrast—the warning shown to a reviewer versus the underlying active episode—was sound, but its significance was not sustained as the narrative through the paper.

## Repaired argument

**Problem →** A review finding and a deferral can refer to different revisions of source evidence and policy.  
**Prior capability →** LEAP reconstructs source-linked KPI knowledge records, while runtime monitors and alert-management systems provide complementary abstractions, temporal state and notification controls.  
**Gap →** The version comparisons required to preserve the displayed decision may differ from those required to preserve the reason for that decision.  
**Response →** An event-based applicability contract separates source observations, active episodes and displayed warnings, and specifies version-bound deferrals.  
**Evidence →** Five formal propositions, constructed omission witnesses, and a finite replay of 4,935 traces/26,430 events, including a 987-trace held-out base comparison.  
**Contribution →** Three joint comparisons preserve the decision components; five preserve the specified reason; obsolete deferrals can alter displayed decisions while leaving episode activity unchanged.

## Source grounding

The foundational LEAP manuscript supplied in the project explains LEAP as **Literate Programming for Automated KPI Extraction**, a source-linked KPI knowledge architecture that reconstructs source context, formulas, business interpretation, provenance, ownership, and review status and publishes an **Interactive Bluebook**. The revised Introduction names that expansion and explains the output at first use, with the pre-existing `mouawad2026architecture` citation. Section 2.1 now explains what an input source check does and how its Boolean finding becomes an event observation. The bibliographic entry was preserved rather than silently replaced with a different manuscript/version identity.

## Cold-reader checks against the revised manuscript

| Reader question | Where the paper answers it | Internal review finding |
|---|---|---|
| What is LEAP and why does it exist? | Introduction ¶2; §2.1 ¶1 | The purpose, inputs, operations and browsable output are defined and cited. |
| What is `REVIEW_REQUIRED`? | §2.1 ¶2 | A source-check flag calling for review, not an adjudicated source-code defect. |
| How does a source finding become a warning? | §2.1 worked example; §3.1–3.2; Figure 1 | The path from lexical observation through timing, authority checks and the display is explicit. |
| What are events, traces, observations, episodes and deferrals? | Introduction ¶5; §3.1–3.2 | Terms appear with their purpose and required information before formal use. |
| Why can activity be correct when the display is wrong? | Introduction worked case; §3.2; Results; Discussion | A version-mismatched deferral changes the displayed state, not the underlying episode. |
| Why do three and five Boolean comparisons differ? | §4, Propositions 3–5 and accompanying interpretation | Decisions and reason labels are distinct outputs requiring different information. |
| What was evaluated and against what? | §5.1–5.4 and §6 | The finite templates, family split, reference, ablations, scoring units and implementation checks are introduced in context. |
| What can a researcher conclude and what remains to be tested? | §7–9 | The contract-specific result is stated, followed by a dedicated limitations section. |

These are **sequential internal editorial checks**, not independent external peer-review results.

## Protected scientific record

The change is narrative and structural. A machine comparison against the rejected LaTeX baseline confirms that all **five propositions, five proofs, two numbered equation environments, one displayed-math block, four ordinary tables, one longtable, and three figure environments** are byte-identical. The `.bib`, `.bbl`, figure PDF/SVG files, plot CSV, and figure-generation script are also byte-identical. The frozen reproduction archive is packaged without changes.

The reported outcomes are unaltered: **4,935 traces, 26,430 events; 987/987 active-episode agreement versus 957/987 complete-decision agreement without deferral-version binding; 30 changed traces and 48 changed event decisions**. No experiments were added or rescored for this prose revision.

## Production checks

- The edited LaTeX compiled through successive `pdflatex` runs with the supplied frozen `.bbl` file.
- Final PDF: **25 letter-sized pages**; citations and cross-references resolved.
- Final LaTeX log: no undefined citations, undefined cross-references, missing glyph warnings, or overfull boxes.
- All 25 pages were rendered for visual inspection, including the three figures, five tables, references, and page transitions.
- A PDF text-boundary check found **0 spans outside the page boundaries**.
- The final source ZIP contains the editable LaTeX, `.bib`, `.bbl`, class/style, figure PDFs and SVGs, and a build script.

## Version and release assessment

**The earlier 22-page draft remains rejected on reader-first presentation.** The new version is a substantially reconstructed manuscript, not an approved submission record. It is appropriate for a fresh scientific and editorial review. Current journal-only requirements and the accuracy of author-only declarations were not independently reverified in this narrative-repair task.
