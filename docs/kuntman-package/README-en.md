# organon-mueller — feedback package #1 (for the Kuntman–Arteaga group)

*Status: experimental research software; results below are labeled
**verified** (machine-checked against your published tables/examples) or
**candidate** (beyond the published tables — no novelty or physics claim
is made; interpretation is deliberately left to you).*

## What this is

An experimental engine that automates the Stokes–Mueller algebra of your
papers (JOSA A **34**, 80 (2017); Phys. Rev. A **95**, 063819 (2017);
Appl. Opt. **55**, 2543 (2016); coupled-dipole work is the next planned
phase). Two pillars: a **discovery engine** (equality saturation over the
covariance-vector term language, every candidate certified by exact
symbolic proof) and a **decomposition deriver** (the symmetry-conditioned
decompositions of AO2016, *derived* — not transcribed — from rank-1 minor
conditions).

## Verified against your publications

- **Table 2 (AO2016), all six variants**: the engine derives the
  equation sets from the 2×2 minors of H − α₁H₁ₛ and matches the printed
  table symbolically (exact zero difference), including the a/b variant
  structure and the paper's numerical-health advice for choosing between
  them.
- **Section 6 numeric example**: reproduced to print precision
  (α₁ = 0.3000, α₁E = 0.1433, α₁V = 0.0289+0.0112i, α₁Ē = 0.0067; both
  component Mueller matrices to ~1e-3).
- **Composite types 1-2 / 1-3 / 2-3 (Tables 3–4)**: three-parameter
  sequential-minor derivation, symbolically identical to Table 4, exact
  synthetic roundtrips.
- **Covariance convention**: we prove R(σᵢ⊗σⱼ) = σᵢ⊗σⱼ* (index
  reshuffle), i.e. the H of AO2016 is exactly the standard Cloude/Gil
  covariance; Eq. (2) read literally (no conjugate) gives a non-PSD
  cousin. This resolved our initial confusion and is now a regression
  test.
- **Two suspected print artifacts** (we would be grateful for a
  confirmation): in Eq. (17) the imaginary part of h₀₃ prints as 0.0161
  but is inconsistent with the paper's own Eqs. (18)–(20), which our
  pipeline reproduces exactly with 0.1608; Eq. (21)'s [1,3] entry
  carries a second, analogous artifact.

## Candidate zone (beyond the published tables — no claims)

- **Rank-3 three-term decompositions** H = α_A H_A + α_B H_B + α_G|u⟩⟨u|
  with {H_A, H_B} of two different fundamental types: {1,2} and {1,3}
  solve by a sequential peel, {2,3} through combination variables with a
  mandatory overdetermination check. The missing-anisotropy conditions
  generalize per pair — the guard denominators are α_G|u₁−u₂|² for
  {1,2}, α_G|u₁+u₂|² for {1,3}, and α_G|u₀−u₃|² for {2,3}.
- **Non-uniqueness observation**: a covariance built as two type-2 pures
  + generic also admits an *exact* type-1 + type-2 + generic split
  (closed form verified to 1e-16). Within a fixed pair hypothesis,
  {2,3} is provably unique. So a rank-3 result is *a* decomposition,
  not *the* decomposition — selecting the physical one is exactly the
  kind of question we would value your view on.
- **Horn-conditional identity channel**: guard-constrained generators
  (e.g. the three class-2 quaternion planes) produce
  "true-under-guard + underivable-without-it" statements with a
  four-part evidence record; currently populated with known facts as a
  mechanism proof.
- A note on the demo's hypothesis "scores": the score is only a
  numerical-health heuristic (the smallest guard denominator on the
  data) used to order attempts — acceptance is decided solely by the
  exact solvers, and a rejected hypothesis can legitimately outscore an
  accepted one. All candidate outputs are gated by our written novelty
  protocol (`docs/novelty-protocol.md`), whose final step — deciding
  whether anything is physically interesting or new — is explicitly
  reserved for humans, i.e. for you.

## Verification contract (summary)

No mathematical statement enters the repository without passing: exact
symbolic proof (SymPy, expand-based zero test) · deterministic seeded
numeric checks · known-identity regression against the papers ·
engine-independent certification of every discovery candidate · an
independent adversarial review of every stage (each reviewer re-derives
the mathematics from scratch) · a 3-version CI matrix. Details:
`docs/VERIFICATION.md`.

## Try it

```bash
pip install -e ".[test]"
python docs/kuntman-package/demo.py
```

## Questions where your feedback would help most

1. Do the two print-artifact diagnoses (Eq. 17 / Eq. 21) match your
   records?
2. Is the rank-3 three-term zone relevant to your current program, and
   is the non-uniqueness behavior expected/known to you?
3. Are our conventions (standard-basis covariance via the reshuffle,
   trace-1 normalization, scaled-parameter templates) the ones you use
   day to day?
4. Next phase is a coupled-dipole symbolic module (re-deriving the
   PRB 98, 045410 results); which outputs would be most useful to you?
