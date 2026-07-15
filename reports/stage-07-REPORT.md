# STAGE 7 — REPORT (Language Extension + Phase B Iteration Assessment)

**Date**: 2026-07-13 · **Spec**: `specs/stage-07.md` · **Mode**: autonomous
**Result**: COMPLETED — 92/92 tests green; **Sum+Scale in the language**; **I15 won by
the engine** (campaign: {I1, I10, I15}); Phase B closed.

---

## 1. Language extension (design note verbatim + one K24-approved addition)

- New nodes: `Sum`, `Scale`, `ScalarAtom`, `ScalarConj` — scalars are OPAQUE
  (M10/K23: no scalar-arithmetic node; scalar multiplication is encoded by nested Scale).
- Axioms: the soundness-approved table in the design note + the post-audit
  reviewer-verified **scale-over-sum** pair (added via the K24 process —
  otherwise Scale(c, Sum) shapes would produce spurious "underivable" results).
- Layers: numeric/symbolic evaluation with scalars; K17 independence
  extended to scalars; fingerprint is **scale-relative** (Frobenius-normalized;
  margin measured: 2.2e-7 ≫ 1e-12 jitter; ZERO key unreachable).
- Honest knobs: `max_sums>1` now raises NotImplementedError instead of silently dropping;
  the engine records conj_normal as it actually runs it in extended mode.

## 2. Acceptance results

- **A (I15 expansion)**: (pZ_a+qZ_b)·conj(·) ≡ four-term nested-Scale form
  — PROVEN + symbolic-exact + numeric ✅
- **B (cross-term realness)**: t ≡ conj(t) PROVEN — and by M26 for
  ALL complex coefficients (faithful verbatim to the paper's Eq. (10) quantification;
  reviewer additionally verified fidelity against the paper-side structure) ✅
- **C (campaign)**: recovered = {I1, I10, **I15**}; M22 basis raised;
  I16/I18/I4/I11/I17 moved to the `interpreted_scalars` key ✅
- **D (K11)**: old language/API untouched; enumeration sentinels stable ✅
- **E (mini-harvest, sweep-02 artifact)**: dimension-6: 340 terms → 202 verified;
  dimension-7: 1036 → 722 verified; **0 refuted, 0 underivable, 0 demoted**;
  16 fingerprint collisions — reviewer verified all of them are honest
  (X vs X+X proportional family; no lost pair) ✅

## 3. Independent audit

Verdict: **PASS**. Reviewer: independently verified all new rules with 200 draws;
axiom-interaction attacks (13 targeted fake pairs + 394
random cross-bucket pairs) found no unsound merges; reproduced sweep-02
field-by-field. Two documentation defects were fixed:

| Finding | Action |
|---|---|
| D1: M26's AL claim was over-correction — AL-type identities ARE expressible in this language via UNSIGNED partition (even-perm sum = odd-perm sum) (reviewer numerically verified S₄); what is unreachable is the enumeration | ✅ spec M26 and extensions doc rewritten with the fine distinction |
| D2: extensions doc contradicted the old vocabulary | ✅ document rewritten with the new table |
| Scale-over-sum derivation gap | ✅ rule added with K24 approval + test |
| Dishonest knobs (max_sums, conj_normal recording) | ✅ fixed |

## 4. PHASE B ITERATION ASSESSMENT (A3–A7 retrospective, v1 iter tradition)

**Numbers**: 5 stages; tests 56→92; library 21 identities + 3 engine-wins;
sweep artifacts 2 (22,560 + 924 pairs, all verified, 0 refutations);
5 adversarial audits, 5 PASS, ~15 applied reviewer suggestions.

**What worked well**:
1. **The layered verification architecture proved itself twice**: egglog
   caught the large-graph pathology (A3) and all the small bugs; the user
   directive ("tests are the only fuse") aligned with the architecture.
2. **Reviewer agents didn't just find bugs, they produced mathematics**: the fragment-completeness
   THEOREM (A6), the dagger-inexpressibility proof (A5), the AL fine distinction (A7).
3. Negative-result discipline (M24): "empty channel" observations crowned with a theorem.

**What was learned/fixed**: dimension-arithmetic error (A2 spec), pytest exit-code
masking (A6), over-correction reflex (A7 M26) — all recorded precedent.

**Carried forward to Phase C**: the `guarded_atoms` extension is a precondition of the
decomposition deriver (extensions doc priority); egglog probe at every version bump;
the underivable channel has still produced no candidate — the FIRST candidates will
probably come from Phase C's restricted-atom classes.

## 5. Next stage (autonomous continuation)

**Stage 8 — Phase C start: symmetry-conditional decomposition deriver (AO2016
automation)**: `guarded_atoms` design + symbolic derivation of the Type 1/2/3
decomposition equations (AO 55,2543 Table 2) — the goal being for the engine
itself to produce the hand-derived table in the library.
