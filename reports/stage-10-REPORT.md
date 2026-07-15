# STAGE 10 — REPORT (Phase C: Rank-3 Three-Term Decomposition + Discovery Bridge)

**Date**: 2026-07-13 · **Spec**: `specs/stage-10.md` · **Mode**: autonomous
**Result**: COMPLETED — 149/149 tests green; **first results in the beyond-paper
region**: rank-3 decomposition derived for three pairs (symbolically verbatim against
probe-verified hand formulas + verbatim against the reviewer's independent
derivations), the **non-uniqueness finding** verified in closed form, and the
discovery→minor bridge v0 working.

---

## 1. Deliverables

- **`decomposition/rank3.py`**: `H = α_A·H_A + α_B·H_B + α_G·|u⟩⟨u|`.
  - {1,2} and {1,3}: ORDERED PEEL — the support of type-1 is only the corners; B's
    center parameter solved LINEARLY from the center minor, its edge from the edge minor
    (structural guard: the selected minors CANNOT TOUCH the unsolved component —
    K31); B is extracted, and the remainder is DELEGATED to the stage-8 solver
    (all its guards inherited — M33 one-way layering).
  - {2,3}: the supports fully overlap → COMBINATION VARIABLES (σ,p,m,s,d);
    five minors linear IN ORDER; after reconstruction the **k₂+e₃=σ over-determination
    is a MANDATORY consistency guard (K32)**.
  - `propose_decompositions` (bridge v0): tries all hypotheses by rank;
    failures are JUSTIFIED (K21 — no silent elimination).
  - `sweep_rank3` → `reports/sweep-03-rank3.json`: 12/12 synthetic
    recovery (worst α error 2.4e-15), negative controls justified.
- **`probes/probe-rank3-prespec.py`**: the pre-spec probe taken into the repo
  (proof of spec §0; the probe caught the sign error in the type-3 edge formula —
  the mechanism worked again).

## 2. Main finding: NON-UNIQUENESS (candidate observation — not a claim)

Data CONSTRUCTED as two type-2 pure + generic also gave an EXACT valid
decomposition under the {1,2} hypothesis (reconstruction 3e-17; all components
pure/PSD). The reviewer extracted its closed form: T₁(P=W=P̄=δ/K̄)+T₂′, δ=KK̄−|W|²,
α₁=2δ/K̄ — matched the code output at 1e-16. **Result framing**: in rank-3 the solution
is "*a* decomposition, not *the* decomposition"; the sweep artifact ALSO verifies the
accepted alternatives (`accepted_alternative_verified`), the physics choice is left to
the human/novelty protocol. On the other hand the reviewer raised uniqueness for {2,3} to
an IN-HYPOTHESIS analytic proof: the five formulas depend only on H → every valid
{2,3}+generic decomposition is forced (unique).

## 3. Independent audit

Verdict: **PASS** (1 MAJOR + 3 MINOR + 1 DOC — all resolved):
- MAJOR: the K32 guard had no test coverage → a deterministic regression test added with
  the all-REAL covariance family (s,d self-consistently real → the realness guards pass)
  (seed 0, throws with |k₂+e₃−σ|=2.8e-02).
- MINOR: center-only pure (edge w=0, a legitimate Table-1 point) collapsed to the
  zero matrix in the outer-primary template construction → construction done with a
  guarded-positive CENTER primary; the boundary family is now solved EXACTLY (test).
- MINOR: NaN leaked past the |trace−1| comparisons and gave a raw collapse in eigvalsh
  → a finiteness guard added to all three solvers; the bridge now returns a justified
  report (test).
- MINOR: cross-pair honesty extended to the full 3×2 direction matrix, and the u₀=u₃
  degeneracy to a test consistent with the spec acceptance.
- DOC: the fact that in {2,3} the s/d REALNESS checks carry the actual elimination burden
  (each one an over-determination in its own right; K32 engages at a finer stratum) was
  recorded in the module docstring.
- The reviewer's independent derivations: the five {2,3} formulas, the two peel pairs,
  the denominator≡missing-anisotropy interpretations ({1,2}: α_G|u₁−u₂|²; {1,3}:
  α_G|u₁+u₂|²; {2,3}: α_G|u₀−u₃|² — intermediate singular factors symbolically
  simplify) — ALL matched verbatim.

## 4. M34 honesty framework (record)

There is NO paper anchor in this region; in place of K28 three layers were put:
probed hand derivation (spec §0) + deriver-hand symbolic verbatim (tests) + reviewer
independent derivation. NO novelty/physics CLAIM was made — the sweep note and the report
say "candidate"; novelty-protocol step 5 (human) unchanged.

## 5. Next stage (autonomous continuation)

**Stage 11 — Iter + Kuntman feedback window #1** (FROZEN-22, Phase C
closure): Phase C retrospective; accumulated obligations (rank-3 a/b minor
variants, bridge v1 fingerprint pre-ordering, guarded-atoms second-half
obligations); a Turkish/English summary package presentable to Kuntman is
PREPARED (NO external contact — the sharing decision rests with the user via the
critical-decision protocol).
