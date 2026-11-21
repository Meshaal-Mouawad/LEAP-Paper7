"""Reconstruct the Nov-19 Paper 7 PDF revisions from the Nov-18 editable source,
then implement independent review M1-M4/M6 without altering frozen experiments.
"""
from pathlib import Path
import re, difflib
root=Path('/mnt/data/Paper7_M1M6_Revision_20261119')
src=(root/'gold/Paper7.tex').read_text()
bib=(root/'gold/Paper7_References.bib').read_text()
def replace_once(old,new,label):
 global src
 n=src.count(old)
 if n!=1:raise ValueError(f'{label}: expected 1 match got {n} for {old[:75]}')
 src=src.replace(old,new,1)
def bib_add(entry):
 global bib
 key=re.search(r'@\w+\{([^,]+)',entry).group(1)
 if '{'+key+',' in bib:raise ValueError('duplicate bib key '+key)
 bib+='\n'+entry.strip()+'\n'

# Restore science-unchanged prose and two previously added references from the latest
# Nov 19 (22-page) PDF; the Nov 18 Gold source is the latest recoverable editable source.
replace_once('The full monitor matched all 987 base sequences from three held-out rule families sharing 329 temporal templates.',
 'The full monitor matched a separately implemented contract reference on all 987 base sequences from three held-out rule families sharing 329 temporal templates.', 'restore final abstract')
replace_once('In a constructed audit case, positive findings begin at one second and qualify the current revision for a warning at three seconds. The monitor also receives a deferral that expires at four seconds and names a different evidence revision. A monitor checking only its expiry hides the warning at three seconds. A monitor checking the authorized revision shows it. Both record the same active episode. The difference is in what the reviewer sees at the qualifying event.',
 'In a constructed audit case, positive findings begin at one second and qualify the current revision for a warning at three seconds. At two seconds, the monitor receives a deferral that names a different evidence revision and expires at four seconds. A monitor that skips the deferral\'s version check hides the warning at three seconds. A monitor checking the authorized revision shows it. Both record the same active episode and show the warning at expiry. The difference is in what the reviewer sees at the qualifying event.', 'restore audit example')
replace_once('or evidence-age checks affect the displayed warning', 'or stale-evidence checks affect the displayed warning','restore Q2')
replace_once('At a context or policy change it first resets the active episode and all timers.',
 'Decisions are made only at supplied events; qualification and clearing use elapsed time across successive valid observations of the same value. At a context or policy change it first resets the active episode and all timers.', 'restore timing statement')
replace_once('For valid evidence, an active episode becomes escalated at the first event at least $E$ seconds after activation.',
 'After qualification and clearing updates, a valid and still-active episode becomes escalated at the first supplied event at least $E$ seconds after activation.', 'restore escalation ordering')
replace_once("A version-sensitive review monitor can decide what to display from three comparisons: whether the current version pair changed, whether a supplied observation matches that pair, and whether a supplied deferral matches it.",
 "With observation values, times, packet presence, expiry, policy parameters and rule severity retained, a version-sensitive review monitor can replace version identifiers with three comparisons: whether the current version pair changed, whether a supplied observation matches that pair, and whether a supplied deferral matches it.", 'restore conclusion')

# Restore two journaled bibliography changes from Nov 19 PDF.
bib_add(r'''@article{hinov2026assurance,
  author = {Nikolay Hinov},
  title = {Evidence-Grounded Runtime Assurance for AI-Assisted Power-Electronics Design: Three-State Constraint Semantics and Deterministic Validation},
  journal = {Eng},
  year = {2026},
  volume = {7},
  number = {10},
  pages = {495},
  doi = {10.3390/eng7100495},
  url = {https://www.mdpi.com/2673-4117/7/10/495}
}''')
bib_add(r'''@inproceedings{legunsen2019evolution,
  author = {Owolabi Legunsen and Yi Zhang and Milica Hadzi-Tanovic and Grigore Ro{\c{s}}u and Darko Marinov},
  title = {Techniques for Evolution-Aware Runtime Verification},
  booktitle = {2019 IEEE 12th International Conference on Software Testing, Verification and Validation (ICST)},
  pages = {300--311},
  year = {2019},
  publisher = {IEEE},
  doi = {10.1109/ICST.2019.00037},
  url = {https://doi.org/10.1109/ICST.2019.00037}
}''')
replace_once('These systems connect observations or findings to the objects and versions that give them meaning.\n\nSuppressing a notification',
'''These systems connect observations or findings to the objects and versions that give them meaning.

Hinov invalidates dependent evidence when a design or its requirements change and checks replacements through an executable evidence contract. Across the constructed design cases, global abstention reproduces the final gate decisions and loses information about which constraints are unresolved \cite{hinov2026assurance}.

Suppressing a notification''','restore Hinov paragraph')
replace_once('The constructed audit case uses that separation to expose a display error with an unchanged active interval.\n\nVersion-sensitive exceptions',
'''The constructed audit case uses that separation to expose a display error with an unchanged active interval.

Legunsen et al. monitor successive Java versions and withhold messages for violations of the same property at likely corresponding source locations \cite{legunsen2019evolution}. That filtering decision follows prior occurrence across program versions. The review contract evaluates the authority and expiry of an explicit deferral while retaining episode activity.

Version-sensitive exceptions''','restore evolution-aware predecessor')
replace_once('Temporal engineering compliance \\cite{ratiu2026runtime} & Changes to related engineering artifacts; incremental checking of temporal constraints. & Feedback on process deviations as artifact histories evolve. \\\\\nAlertmanager',
'''Temporal engineering compliance \\cite{ratiu2026runtime} & Changes to related engineering artifacts; incremental checking of temporal constraints. & Feedback on process deviations as artifact histories evolve. \\\\
Evidence-grounded design assurance \\cite{hinov2026assurance} & Changes to a design or its requirements; invalidation and replacement of dependent evidence. & Final gate and per-constraint verdicts, with localization not retained under global abstention. \\\\
Evolution-aware verification \\cite{legunsen2019evolution} & Successive program versions, monitored properties and corresponding source locations. & Newly occurring violations after filtering likely repeated violation messages. \\\\
Alertmanager''','restore Table2 rows')
replace_once('Present study & Current, observation and suppression bindings; interface projections and a specified review lifecycle. & Necessary applicability distinctions, sufficient comparison representations, complete decision sequences and active-episode intervals.',
 'Present study & Current, observation and suppression bindings; interface projections and a specified review lifecycle. & Single-field omission witnesses, sufficient comparison representations, complete decision sequences and active-episode intervals.', 'restore final Table2 precision')

# M4: verified full text, DOI 10.1109/ICSE55347.2025.00099, ICSE 2025 pp. 103-115.
bib_add(r'''@inproceedings{guan2025imop,
  author = {Kevin Guan and Owolabi Legunsen},
  title = {Instrumentation-Driven Evolution-Aware Runtime Verification},
  booktitle = {Proceedings of the 2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE)},
  pages = {103--115},
  year = {2025},
  publisher = {IEEE},
  doi = {10.1109/ICSE55347.2025.00099},
  url = {https://www.cs.cornell.edu/~legunsen/pubs/GuanAndLegunsenIMOPICSE2025.pdf}
}''')
replace_once('That filtering decision follows prior occurrence across program versions. The review contract evaluates the authority and expiry of an explicit deferral while retaining episode activity.',
'''That filtering decision follows prior occurrence across program versions. Guan and Legunsen subsequently developed instrumentation-driven evolution-aware runtime verification: their iMOP framework reuses instrumentation for unchanged code while monitoring all specifications in new revisions. They evaluated 2,028 revisions of 66 projects with 160 monitored specifications, measuring runtime overhead and preservation of newly detected violations \cite{guan2025imop}. This work studies efficient monitoring as programs evolve. The present contract instead studies whether the evidence and policy versions named by an observation or deferral permit the required displayed review decision and its prescribed reason.

The review contract evaluates the authority and expiry of an explicit deferral while retaining episode activity.''', 'M4 journal comparison')
replace_once('Evolution-aware verification \\cite{legunsen2019evolution} & Successive program versions, monitored properties and corresponding source locations. & Newly occurring violations after filtering likely repeated violation messages. \\\\\nAlertmanager',
'''Evolution-aware verification \\cite{legunsen2019evolution} & Successive program versions, monitored properties and corresponding source locations. & Newly occurring violations after filtering likely repeated violation messages. \\\\
Instrumentation-driven evolution-aware RV \\cite{guan2025imop} & Reuse of instrumentation across revisions; changed-code reinstrumentation; all specifications monitored. & Monitoring overhead and detection of new violations over 2,028 revisions in 66 projects. \\\\
Alertmanager''', 'M4 Table2')

# M3: explicitly enumerate archived categorical severities without changing experimental outputs.
start=r'''\begin{tabularx}{\linewidth}{@{}lX@{}}\toprule
Family & Source-evidence pattern \\\midrule
Privacy & Personal-identifier tokens without masking/encryption-related substrings.\\
Restricted execution & Tokens such as \code{eval}, \code{exec}, or \code{os.system}.\\
Audit completeness & Modification tokens with one or more missing audit-signature elements.\\
Data transfer & Personal-data and movement tokens without consent/agreement tokens.\\
Lineage signing & Lineage tokens without signature-related tokens.\\\bottomrule
\end{tabularx}'''
new=r'''\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{.18\linewidth}X>{\raggedright\arraybackslash\ttfamily\scriptsize}p{.32\linewidth}@{}}\toprule
Family & Source-evidence pattern & Archived severity label \\\midrule
Privacy & Personal-identifier tokens without masking/encryption-related substrings. & CRITICAL\_PRIVACY\_ALERT\\
Restricted execution & Tokens such as \code{eval}, \code{exec}, or \code{os.system}. & SECURITY\_VULNERABILITY\\
Audit completeness & Modification tokens with one or more missing audit-signature elements. & COMPLIANCE\_AUDIT\_GAP\\
Data transfer & Personal-data and movement tokens without consent/agreement tokens. & REGULATORY\_RISK\\
Lineage signing & Lineage tokens without signature-related tokens. & AUDIT\_INCOMPLETE\\\bottomrule
\end{tabularx}'''
replace_once(start,new,'M3 Table1 mapping')
replace_once('The companion source inventory identifies the adapters and their archived versions.',
 'The companion source inventory identifies the adapters and their archived versions. Table~\\ref{tab:recovery} also reports the exact categorical severity attached to each family in the frozen design inventory; these labels are carried into active-event decisions.', 'M3 provenance')
replace_once('Recovered source-review predicates used as Boolean observation adapters. The evaluated predicate is the stated lexical check.',
 'Recovered source-review predicates and their archived categorical severity labels. The evaluated predicates are lexical checks; severity labels are taken from the frozen study design inventory.', 'M3 Table1 caption')

# M2: reset reason label R_i is categorical; Delta_i is a Boolean change indicator.
replace_once('and let $r_i$ be the selected reset label, or empty when no reset occurs.',
 'and let $R_i$ be the selected reset-reason label, or empty when no reset occurs.', 'M2 reset definition')
replace_once('r_i, & q_i=\\varnothing\\ \\land\\ r_i\\ne\\varnothing,', 'R_i, & q_i=\\varnothing\\ \\land\\ R_i\\ne\\varnothing,', 'M2 Eq branch')
replace_once('q_i=r_i=\\varnothing\\ \\land\\ d_i=\\text{SUPPRESSED}', 'q_i=R_i=\\varnothing\\ \\land\\ d_i=\\text{SUPPRESSED}', 'M2 Eq suppression')
replace_once('The following encoding uses $r_i$ as a Boolean change indicator. Let $k_i=(c_i,p_i)$ denote the current evidence-context and policy pair at event $i$. Let $r_i$ indicate that $k_i$ differs from $k_{i-1}$, with $r_1=0$.',
 'The following encoding uses $\\Delta_i$ as a Boolean change indicator. Let $k_i=(c_i,p_i)$ denote the current evidence-context and policy pair at event $i$. Let $\\Delta_i$ indicate that $k_i$ differs from $k_{i-1}$, with $\\Delta_1=0$.', 'M2 joint change definition')
replace_once('The triple $(r_i,v_i,m_i)$ suffices', 'The triple $(\\Delta_i,v_i,m_i)$ suffices','M2 triple')
replace_once('The monitor resets when $r_i$ is true.', 'The monitor resets when $\\Delta_i$ is true.', 'M2 triple proof')

# M1: retain original six-comparison proposition and add stronger corollary.
anchor='''An evidence service can send these comparison results in place of version names. This preserves reason labels that distinguish evidence changes or mismatches from policy changes or mismatches. The next result asks which comparisons suffice when the receiving monitor reports only the decision components.'''
addition=r'''The six comparisons are sufficient but retain one distinction that the specified reason rule never outputs. In particular, the reason \code{SUPPRESSION} is selected only after an applicable suppression actually changes the display. An inapplicable suppression does not produce separate context-mismatch or policy-mismatch reasons.

\begin{proposition}[Five-comparison sufficiency for decisions and reasons]\label{prop:five-comparison}
For every admissible trace, the complete sequence of displayed states, activity flags, severity labels and specified reasons is determined by the retained non-version inputs and at most five Boolean comparisons per event:
\[
(\Delta^c_i,\Delta^p_i,O^c_i,O^p_i,S^{\mathrm{joint}}_i).
\]
Here $\Delta^c_i$ and $\Delta^p_i$ indicate changes in the current evidence context and policy version since the preceding event (both false initially); $O^c_i$ and $O^p_i$ indicate matches of the observation's two version fields when present; and $S^{\mathrm{joint}}_i$ is true exactly when a present suppression matches both current versions. Packet presence, observation values, event and observation times, expiry, policy durations and rule severity remain available.
\end{proposition}
\begin{proof}
Induct on the event index. The two current-change indicators uniquely select the reset and its reason, including policy precedence when both change. For a present observation, $O^c_i$ and $O^p_i$ select the applicable context- or policy-mismatch reason in the specified order. All other validity checks use retained values and times. Consequently, the timer and episode transitions agree. The suppression overlay depends only on the episode's active status, the retained expiry and $S^{\mathrm{joint}}_i$. The reason rule selects an observation-validity label first, then a reset label, then \code{SUPPRESSION} only if the overlay is displayed, and otherwise \code{STATE}. It never outputs which suppression field mismatched. Therefore the two separate suppression comparisons can be replaced by their conjunction without changing any of the four output components. The updated timers and activity provide the induction hypothesis for the next event.
\end{proof}
This result gives a five-comparison decision-and-reason interface. It sharpens the preceding six-comparison result under the paper's fixed reason vocabulary; the claim is sufficiency rather than minimality. The next result asks which comparisons suffice when the receiving monitor reports only the decision components.'''
replace_once(anchor,addition,'M1 five comparison corollary')

# Update all contribution/contract interpretations consistently.
replace_once('Six separate comparisons also preserve the reason label.',
 'Five comparisons also preserve the specified reason label by retaining separate current-change and observation-match indicators while combining the two suppression matches.', 'M1 abstract')
replace_once('and six separate comparisons that also preserve the specified reason.',
 'and five comparisons that also preserve the specified reason.', 'M1 contribution')
replace_once('the three- and six-comparison proofs use the specified comparisons',
 'the three- and five-comparison proofs use the specified comparisons', 'M1 contract')
replace_once('Propositions~3 and~4 then establish sufficient comparisons for the specified policy and separate preservation of a decision from preservation of its reason.',
 'Propositions~3 and~4, together with Proposition~\\ref{prop:five-comparison}, establish sufficient comparisons for the specified policy and separate preservation of a decision from preservation of its reason.', 'M1 theorem intro')
replace_once('For a retrospective implementation check of the six separate comparisons,',
 'For a retrospective implementation check of the original six separate comparisons,', 'M1 re-encoding')
replace_once('A monitor reporting the specified reasons can use the six separate comparisons to retain the source of a reset or observation mismatch.',
 'A monitor reporting the specified reasons can use five comparisons: separate current-version change and observation-version match indicators together with a joint suppression match.', 'M1 discussion')
replace_once('Keeping the evidence and policy comparisons separate also allows the monitor to identify the source of a reset or observation mismatch.',
 'Five comparisons additionally preserve the contract\'s reason label: separate change and observation-match indicators identify the source of a reset or observation mismatch, while one joint comparison suffices for suppression.', 'M1 conclusion')

# M6: caption content scientific only; process and renderer versions live in research materials and supplement.
snippet=' Figure preparation and verification code used OpenAI ChatGPT/Codex assistance; the original vector export records Matplotlib 3.10.8.'
assert src.count(snippet)==2, 'M6 caption duplication count changed'
src=src.replace(snippet,'')
replace_once('OpenAI ChatGPT and Codex also assisted with figure preparation and verification code. Figure~\\ref{fig:mismatches} plots complete-decision and active-episode mismatches from saved outputs for the 987 held-out base traces. The accompanying script recomputes these counts, checks the plotted SVG labels and coordinates, and exports the retained SVGs with Inkscape 1.4. The original SVG metadata identifies Matplotlib 3.10.8.',
 'Figure~\\ref{fig:mismatches} plots complete-decision and active-episode mismatches from saved outputs for the 987 held-out base traces. Its underlying counts are recomputed from archived event-level decisions. Editable figure source and reproduction steps are supplied with the research materials.', 'M6 repeated methods prose')
replace_once('Editable figures and the literature-discovery records accompany the manuscript.',
 'Editable figures, the original renderer metadata (Matplotlib 3.10.8), figure-verification code, and the literature-discovery records accompany the manuscript.', 'M6 location of figure metadata')

# Provide a method-specific direct verification pointer for this supplementary proof.
replace_once('This replay uses the original monitor and examines a representation property separately from the held-out implementation comparison.',
 'This replay uses the original monitor and examines a representation property separately from the held-out implementation comparison. A post-review five-comparison canonicalization check uses the same frozen packets, changes only the version representation, and separately compares decisions and reasons with the retained reference; it is reported with the supplement rather than counted in the original evaluation.', 'M1 test method pointer')

(root/'work/Paper7.tex').write_text(src)
(root/'work/Paper7_References.bib').write_text(bib)
print('Wrote',len(src),'chars /',len(bib),'bib chars')
print('Bib entries',len(re.findall(r'@\w+\{',bib)))
print('Propositions',src.count('\\begin{proposition}'),'proofs',src.count('\\begin{proof}'))
# archive targeted revision in edit log, preserve the reconstructed Gold source separately.
(root/'reports/source_gold_to_targeted.diff').write_text(''.join(difflib.unified_diff((root/'gold/Paper7.tex').read_text().splitlines(True),src.splitlines(True),fromfile='Gold_Nov18/Paper7.tex',tofile='Targeted_M1M6/Paper7.tex')))
