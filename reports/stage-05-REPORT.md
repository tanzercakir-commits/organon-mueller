# STAGE 5 — REPORT

**Date**: 2026-07-13 · **Spec**: `specs/stage-05.md` · **Mode**: autonomous
**Result**: COMPLETED — 80/80 tests green; the recovery campaign works;
the term language's boundary map was drawn; the egglog upstream draft is ready (not submitted).

---

## 1. Recovery campaign result

The engine rediscovered ON ITS OWN the subset of the hand-coded I1–I21 library that is translatable
into the term language, by passing it through three layers (e-graph proof + numerical +
symbolic-exact, K20):

| Status | Identities | Note |
|---|---|---|
| **Recovered (2)** | I1 (Z·Z\*=Z\*·Z **and** M-reality in the t≡conj(t) form), I10 (commutation + serial Mueller law) | 4/4 pairs passed the three layers; harvest-proof tested |
| **Structural (2)** | I7, I8 | The definition of the language's semantics (the engine cannot "discover" its own interpretation function) — the auditor separately defended the honesty of this category; their symbolic proofs are already in the suite |
| **Untranslatable (17)** | the rest | Each with named missing-property keys (K19) |

The union of missing properties → `docs/term-language-extensions.md` (prioritized):
1) `addition`+`scalars` (coherent superposition, I15-I18) → **Stage 6+ main target**;
2) `guarded_atoms` (I4, I12-I13, I19-I21) → Phase C link;
3) `dagger`+`stokes_sort` (I9, I13-I14) — the auditor proved the INEXPRESSIBILITY of dagger in the
   current language with a degree argument;
4) `entry_level` — will not enter the e-graph, will stay in the SymPy layer;
5) `constants`.
The M22 monotonicity guard: as the language expands, the recovery set can only GROW.

## 2. egglog upstream draft (M23 — NOT SUBMITTED)

`docs/egglog-upstream-issue-draft.md`: English, package-independent,
self-contained repro. Reduced with delta-debug: **a single ground rule +
29 registered terms** — child classes merge, syntactically identical parents
do not merge (congruence violation); depends on the registration ORDER (passes if the pair is registered
first); seminaive/extra-iteration ineffective. The auditor ran the draft code verbatim
and verified the whole control table and the **1-minimality** of the 29 terms (each single
removal destroys the bug). Submission awaits user approval.

## 3. Independent audit

Verdict: **PASS** (conditional on two document-line corrections — done).
The auditor questioned the verdict of each of the 21 records one by one: the fidelity of the
I1-reality translation (elementwise conj ⇔ reality), the legitimacy of the "structural"
category of I7/I8, the inexpressibility of dagger (the degree-homogeneity
argument), and the partial-shadow sweep (the I15 cross-term = equivalent to I10, already
recovered). Applied suggestions: the extension table was corrected to the union
semantics (I18/I2 row errors), an unknown-status guard + layer-based error logging were added
to the campaign, the pathology↔draft cross-reference and the I15 partial-shadow note were recorded.

## 4. Next stage (autonomous continuation; user directive: interval 5 min)

**Stage 6 — New-candidate sweep #1 + literature comparison discipline**:
a systematic sweep in the current language fragment (2-3 atoms, deep size); if the `underivable`
channel comes out empty (the axioms appear complete) this ITSELF is a reportable
completeness observation; in parallel the design note for the `addition`+`scalars` extension
(Stage 7 spec input). A literature comparison template for the "new" claim.
