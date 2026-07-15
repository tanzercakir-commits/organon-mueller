# STAGE 11 — Iter + Kuntman Feedback Window #1 (Phase C closure)

**Date**: 2026-07-13 · **Previous**: stage-10 (rank-3 + bridge v0) · **Mode**: autonomous
**Probe note**: this stage has NO new campaign/sweep target → pre-spec
numeric probe not needed (the rule stands in place).

---

## 1. Goals

### (a) Phase C retrospective
`docs/phase-c-retrospective.md`: consistency sweep of the A8-A10 decisions
(M28-M34) and strict rules (K26-K32); technical-debt inventory; lessons
(the two gains of probe-before-spec; the self-catch of the pytest-pipe
violation; the framing of the non-uniqueness finding).

### (b) Accumulated obligations — implement or REASONABLY defer
1. **IMPLEMENT — bridge v1 pre-ranking**: to `propose_decompositions` add a cheap
   structure-score: the min of the denominator magnitudes of the hypothesis's
   derived expressions (a generalization of the paper's "large denominator = numeric
   health" advice). It ONLY RANKS — elimination is still in the exact solvers and
   reasoned (K21). The scores go into the report (`ProposeReport.scores`).
2. **IMPLEMENT — guard-generator fidelity meta-test**: every new key added to
   GUARD_KEYS cannot be tested without a numeric AND symbolic generator
   (the structural form of design-note obligation 1).
3. **DEFER — rank-3 a/b minor variants** (M33): the canonical set + clear
   guard messages stand. Reason: the variant denominators diverge only in measure-zero
   degeneracies (e.g. u₁=0 vs u₂=0); measured/noisy real data does not land exactly
   on these points, tolerances exist; it opens when experimental
   data arrives (after the Kuntman window).
4. **DEFER — interpreted_scalars denominator side-conditions** (design-note
   obligation 2): the feature is not yet IN the language (K19 key); recorded as
   conditional debt in the retrospective.
5. Stage-10 auditor suggestions: all applied at the stage-10 closure
   (primary="center" construction, finiteness guards, K32/u₀=u₃/cross-pair
   tests, zero-matrix guard) — verified in the retrospective.

### (c) Kuntman feedback package (NO external contact — sending is with the user)
`docs/kuntman-package/`: `README-tr.md` + `README-en.md` (what was
automated: Table 1-4 derivations; the §6 example at print precision
+ 2 print-error diagnoses; rank-3 CANDIDATE results + non-uniqueness observation;
verification-contract summary; feedback questions) + `demo.py`
(runnable: the §6 decomposition, rank-3 roundtrip, with bridge scores) +
smoke test. Language: "candidate/aday" — NO CLAIM; novelty-protocol step 5
emphasis in both languages.

### (d) VERIFICATION.md update
Weave the Phase C additions into the layers: pre-spec probe rule; M34 (three-layer
substitute in the region without a paper anchor); K32-type over-determination
guards; run-time invariant guards. NO layer weakening
(addition only — a critical-decision is not triggered).

## 2. Acceptance

- Bridge scores: present + deterministic in all tried hypotheses; the score of the
  correct hypothesis is finite-positive; the success set is THE SAME as in the score-free
  form (ranking changes behavior, does not change the result set).
- Meta-test: GUARD_KEYS ↔ generators one-to-one.
- demo.py smoke test: verifies α₁=0.3 in §6 at ~1e-3, exact recovery
  in a rank-3 synthetic.
- 149 old tests green; retrospective + package + VERIFICATION current.

**STOP HERE**
