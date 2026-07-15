# STAGE 10 — Rank-3 Decomposition + Discovery Bridge (Phase C, publication-candidate region)

**Date**: 2026-07-13 · **Previous**: stage-09 (composite types + guarded atoms) ·
**Mode**: autonomous

---

## 0. Pre-implementation probe (stage-9 lesson — MANDATORY, done)

`H = α_A·H_A + α_B·H_B + α_G·|u⟩⟨u|` (two fundamental-symmetric pures + generic
pure; rank 3, trace 1). Probe results (`probes/probe-rank3-prespec.py`,
seed 20260713):

- **{type1, type2}**: sequential peel EXACT (5/5 trials, ~1e-12) — B's center
  parameter LINEAR from the center minor, its edge LINEAR from the row-0 edge minor
  (neither touches type-1's corner support); B is extracted, the residual is
  rescaled and DELEGATED to the stage-8 rank-2 solver.
- **{type1, type3}**: same — EXACT with sign-adjusted minors (5/5). (In the
  first version of the probe there was a sign error in the edge formula; the probe caught it,
  it was fixed — the probe mechanism worked again.)
- **{type2, type3}**: the supports FULLY overlap; 12/12 multi-start LSQ
  converged to the same zero-residual solution (= the truth) → IDENTIFIABLE.
  Exact path: with COMBINATION VARIABLES (σ=k₂+e₃, p=w₂+v₃, m=w₂−v₃,
  s=k̄₂+ē₃, d=k̄₂−ē₃) the T₂+T₃ sum is a 7-parameter Hermitian pattern;
  the corner minor is LINEAR in σ (the squares simplify), p/m/s/d LINEAR in turn →
  back-construction (w₂,v₃,k̄₂,ē₃ → k₂=|w₂|²/k̄₂, e₃=|v₃|²/ē₃) + **consistency
  guard k₂+e₃ = σ** (over-determination = K26 opportunity).

## 1. Goals

1. `decomposition/rank3.py`:
   - `derive_rank3(pair)` (M28 continues): over a generic Hermitian the residual's
     minors are solved SEQUENTIALLY with SymPy; structural guards (K29 extends):
     each minor linear in its own unknown + conj-free + does not touch the
     symbols of other components NOT YET SOLVED; violation throws.
     Pairs: (1,2), (1,3) → (center, edge) + delegation; (2,3) →
     (σ,p,m,s,d) + back-construction.
   - `decompose_rank3(covariance, pair, ...)`: K26 guard set — trace-1,
     rank==3, denominator~0 (missing-anisotropy: e.g. corner denominator α_G|u₀−u₃|² —
     the generic pure MUST CARRY the missing anisotropy, the rank-3 generalization of the
     paper's theme), primary real+positive, α's ∈(0,1), {2,3} consistency
     guard, residual pure PSD + rank-1. Delegation: rescale the {1,B} residual
     → stage-8 `decompose` (inherits all of its guards).
2. `propose_decompositions(cov)` (fingerprint→minor bridge v0): TRIES candidate
   classes by rank (rank 2: fundamental+composite; rank 3: three
   pairs), returns successes with result+tag, failures with REASONS
   (no silent elimination — spirit of K21).
3. Sweep (discovery): deterministic synthetic sweep (3 pairs × seeds +
   negative controls) → `reports/sweep-03-rank3.json` (K21 artifact).

## 2. Architectural decisions

- **M33**: The rank-3 solver does NOT TOUCH the stage-8/9 paths; delegation is one-way
  (rank3 → rank2). Variants (a/b minor options) are absent in this stage —
  canonical set + clear guard messages; a/b extension is noted to A11.
- **M34 (K28 adaptation — honesty)**: This region is beyond-the-paper: NO EXTERNAL ANCHOR
  like a table. Instead of K28's "one-to-one with the paper" anchor, three layers:
  (i) the probe-verified hand derivation is fixed in the spec (above),
  (ii) the deriver's output is symbolically compared with these hand formulas,
  (iii) an independent auditor does its own derivation. NO CLAIM of physics-interpretation/novelty
  — novelty-protocol step 5 is WITH THE HUMAN; the report says "candidate".

## 3. Strict rules

K31. Rank-3 minor selections carry a structural guard sensitive to the solution ORDER
(a minor touching an unsolved symbol throws). K32. The {2,3} consistency residual
|k₂+e₃−σ| is a MANDATORY check in the solver — data that cannot pass is rejected (no silent
patching).

## 4. Acceptance

- The deriver passes the structural guards on 3 pairs; symbolically one-to-one with the
  hand formulas (M34-ii).
- Roundtrip: 3 pairs × 3 deterministic examples, exact recovery (test
  tolerances α 1e-8, components 1e-6; observed errors ~1e-15).
- Degenerate guards: same-type pair; deliberate u₀=u₃ / u₁=u₂ degeneracies;
  rank≠3; trace≠1; {2,3} consistency violation — all REASONED errors.
- Cross-pair honesty: a wrong pair either falls in a guard or in the delegation
  guard — NO silent plausible-but-wrong.
- `propose_decompositions`: finds the correct fundamental in a rank-2 synthetic, the correct
  pair in a rank-3 synthetic; elimination reasoned.
- sweep-03 JSON deterministic; 126 old tests green.

**STOP HERE**
