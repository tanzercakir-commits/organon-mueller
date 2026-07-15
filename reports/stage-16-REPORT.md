# STAGE 16 — REPORT (PHASE E Opening: LaTeX Report Generator)

**Date**: 2026-07-14 · **Spec**: `specs/stage-16.md` · **Mode**: autonomous
**Result**: COMPLETED — 215/215 tests green; `reporting/` module + a sample report
for the Kuntman package (`sample-report.tex`, compiles with pdflatex).

## 1. Deliverables

- **Evidence-class discipline institutionalized**: each block `evidence ∈
  {symbolic-proof, numeric-deterministic, candidate}` (bound to the VERIFICATION.md
  layers); template VERBS according to the label ("proven" only for
  symbolic-proof); an unknown label throws.
- **Block generators**: three decomposition types (+rank-3 non-uniqueness note on each
  result), score-ordered hypothesis table (justified rejections, "score orders,
  does not accept" framing), M32 quadruple-evidence table (candidate language),
  dipole γ-map + ensemble statistics (per-row statistics label).
- **Determinism**: byte-for-byte identical output (sha256 confirmed across processes);
  \today/timestamp forbidden (tested); fixed rounding + **sub-threshold magnitude
  scientific notation** rule.
- **Security** (A17 preparation): LaTeX only from our own result objects;
  free text escaped (injection probes: \input, \write18, $(rm)
  — all ineffective, reviewer verified); pdflatex -no-shell-escape.

## 2. Independent audit — again two rounds

Initial verdict **FAIL (conditional)**, D1 MAJOR: `_fmt` printed 6.7e-16 as "0"
— turning a machine-precision residue into a PRECISION claim, exactly the violation
of the contract this stage institutionalizes (the mirror image of the A15 lesson).
Fix: sub-threshold magnitudes fall to deterministic scientific notation
(\ensuremath wrapper — valid in both text/math modes); NaN/Inf
throws (K26); the fixed rounding-rule sentence is in every report's footnote.
+ D2 (tolerance claim refined), D3 (statistics label per-row),
D4 (real math \alpha, \mathrm{i}), process-language leak cleanup.
Re-verification: **PASS** (including injection/compilation/determinism probes).
The sample report now honestly prints the residues (6.7×10⁻¹⁶ etc.).

## 3. Scope decision (record)

Guarded-atoms 2nd half **deferred to A20** (spec §2 justified): what Phase E
needs is the novelty channel being REPORTABLE — `guarded_finding_section`
delivered this; new campaigns are the job of the consolidation sweep.

## 4. Next stage (autonomous continuation)

**Stage 17 — MCP server**: FIRST the serialize.py sympify STAGE-2 GATE
security hardening (external input never goes to raw sympify under any
condition); the external surface only after that. The report generator is the server's main output channel.
