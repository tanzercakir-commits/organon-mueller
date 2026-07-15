# STAGE 11 — REPORT (Phase C Closure: Iter + Kuntman Window #1)

**Date**: 2026-07-13 · **Spec**: `specs/stage-11.md` · **Mode**: autonomous
**Result**: COMPLETED — 156/156 tests green; **PHASE C CLOSED (A8–A11)**;
the Kuntman feedback package is READY FOR REVIEW (sending = critical decision,
rests with the user).

---

## 1. Deliverables

- **`docs/kuntman-package/`**: README-tr.md + README-en.md (verified /
  candidate distinction clear; two print-error diagnoses; 4 feedback questions) +
  `demo.py` (three demonstrations: §6 example α₁=0.3000; rank-3 synthetic ~1e-15;
  scored bridge) + smoke test. The reviewer verified EVERY load-bearing claim in the
  package against the repo AND against the paper's PDF (fact-check table in the audit
  record) — the two print-error diagnoses were confirmed independently from the PDF.
- **Bridge v1** (accumulated obligation CLOSED): `ProposeReport.scores` —
  denominator-health score; ORDERS the attempts, never eliminates (test:
  the success set is verbatim with the unscored exact-solver set). The demo shows an
  honest example: a rejected hypothesis can be scored higher than an accepted one
  (score ≠ correctness; framing in the README+demo output).
- **Guard-generator fidelity meta-test** (obligation made structural):
  GUARD_KEYS ↔ generators bidirectional (an unknown key throws in both generators).
- **`docs/phase-c-retrospective.md`**: full sweep of M28–M34 + K26–K32
  (including M30=OCR correction — the first draft said "M30 not assigned", I
  falsified it with my own grep); the debt table; 4 lessons.
- **VERIFICATION.md Phase C additions**: the pre-spec probe rule; the M34
  three-layer substitution; K32-type over-determination guards;
  runtime invariant guards; post-acceptance verification. ADDITIONS ONLY —
  no layer weakened.

## 2. Deferred debts (justified)

- rank-3 a/b minor variants: the variant denominators separate only at
  measure-zero degeneracies; they open up in the experimental-data window.
- interpreted_scalars denominator side-conditions: the feature is not in the language (K19);
  a mandatory acceptance item at the stage it enters the language.
- guarded-atoms 2nd half: between Phase D-E; for now the honest scope (generator +
  fidelity) is preserved.

## 3. Independent audit

Verdict: **PASS** (1 MAJOR + 9 MINOR — all resolved). MAJOR:
in the READMEs three guard denominators were covered under a single parenthesis as "peel"
pairs — α_G|u₀−u₃|² is actually {2,3}'s; the pair labels were written out
explicitly (this document's exact target audience would check this). The MINORs:
demo/README α₁ consistency (variant="a" fixed — noted as a health≠correctness
example), the score framing for the external reader, stale
docstrings, refinement of the VERIFICATION probe statement, K27/K30
sweep, API consistency (scores={}), lru-cache usage, meta-test
bidirectionality. The reviewer's fact-check table: 12 of 14 claims OK, 2
fixed (denominator coverage, α₁ notation).

## 4. Phase C balance sheet

4 stages · 4 audits PASS · tests 110→156 · all of Tables 1-4 derived and
verbatim with the paper · §6 at print precision + 2 print-error diagnoses
(confirmed against the PDF) · the beyond-paper rank-3 region opened (M34
framework, non-uniqueness finding, {2,3} in-hypothesis uniqueness proof) ·
the underivable channel filled for the first time (M32) · two probe wins.

## 5. Next stage (autonomous continuation — PHASE D OPENING)

**Stage 12 — Coupled-dipole symbolic engine** (PRB 98, 045410 re-derivation):
the spec will be written by reading the project files' Plasmon_hybridization and
Asymmetric_Scattering PDFs; the dimer Jones/covariance structures will be connected to
the existing representation layer. If the Kuntman package feedback arrives, the Phase D
internal ordering may be updated (FROZEN-22 fixed).
