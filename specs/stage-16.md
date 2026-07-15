# STAGE 16 — LaTeX Report Generator (PHASE E opening)

**Date**: 2026-07-14 · **Mode**: autonomous · **Probe note**: NO new mathematical
mechanism → no numeric probe needed; environment probe done
(pdflatex/latexmk/xelatex available → PDF compilation tested, skipif-guarded
in CI).

## 1. Goals — `reporting/` module

1. **Evidence-class labels** (A15 lesson being institutionalized): each report
   block carries `evidence ∈ {symbolic-proof, numeric-deterministic, candidate}`;
   labels bind to the VERIFICATION.md layer 1/2/novelty-channel;
   template verbs are chosen by label ("proven" only for symbolic-proof).
2. **Block generators** (M28 spirit: from result objects, not from hand-written
   text): `decomposition_section` (DecompositionResult / CompositeResult
   / Rank3Result — the α's, component matrices, guard info),
   `propose_section` (score-sorted table + REASONED rejections — K21),
   `guarded_finding_section` (M32 four-fold evidence table + candidate language),
   `dipole_section` (γ-map values + ensemble statistics).
3. **Determinism**: same input → byte-for-byte same LaTeX (test); \today and
   timestamp FORBIDDEN (date is an explicit parameter); numeric rounding fixed
   (6 digits); seeds/reproduction info in every block (K21).
4. **Security** (A17 MCP preparation): the generator writes LaTeX ONLY from our own
   result objects — external input is not sympify'd (consistent with the STAGE-2 GATE);
   free text (titles, rejection rationales) is LaTeX-escaped;
   pdflatex is called with `-no-shell-escape`.
5. **PDF compilation**: `compile_pdf` (nonstopmode, no-shell-escape; raises
   with an error-log tail); test `skipif(no pdflatex)` — honest
   optionality in CI.
6. **First scenario**: `build_kuntman_report()` — dumps demo.main() results
   into the report; `docs/kuntman-package/sample-report.tex` SAMPLE output
   (not a submission); PDF compilability under test.
7. No physics-interpretation CLAIM in the template; novelty step-5 footnote fixed.

## 2. Guarded-atoms 2nd half — scope DECISION (retrospective debt)

**DEFERRED to A20.** Rationale: (i) Phase E's need is that novelty-channel
outputs BE REPORTABLE — `guarded_finding_section` delivers this at this stage;
(ii) unitary/hermitian campaigns produce new known-truths (the mechanism proof
was completed in A9 with the class2 planes) — a natural part of the
consolidation sweep (A20); (iii) squeezing it in
dilutes Phase E's external-surface security focus (A17 GATE).

## 3. Acceptance

Determinism test (byte-for-byte); three decomposition types + propose + guarded +
dipole blocks render; evidence-label mapping mandatory (unknown label
raises); escape test; \today/timestamp prohibition test; Kuntman sample
report is produced + compiled with pdflatex (skipif'd); 204 existing tests green.

**STOP HERE**
