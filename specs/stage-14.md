# STAGE 14 — N-Dimer / Ensemble Generalization (Phase D 3/4)

**Date**: 2026-07-13 · **Source**: "OA in an ensemble of randomly oriented
chiral and achiral plasmonic dimers" (Kuntman & Kuntman, project PDF) ·
**Mode**: autonomous

## 0. Probe (MANDATORY — done: probes/probe-ensemble-prespec.py)

- **Q1-Q2 ✓** 3D scalar reduction (rank-1 projectors; drive phases
  e^{∓ikr_z/2}) == Eqs. 21-24; forward Jones == Eqs. 26-29; γ_z formula
  correct BUT **label slip (M30 #5)**: γ_z = −2µαδ·**(n×m)_z**·sin(kr_z)
  — the paper writes "(m×n)_z" ((n×m)_z error 2.7e-17, (m×n)_z 2.2e-2).
- **Q3 ✓** γ_x == Eq. 33 exactly (x′=−z, y′=y frame + r_x phases);
  two-term split (γx1 independent of coupling — metasurface point) ✓.
- **Q4 — M30 #6**: Eq. 9's printed prefix −2iεαµ is WRONG (µ = εα/(1−(αδ)²)
  already contains εα); the derived correct prefix is **−2iµ** (numeric: printed=False,
  mu-only=True). The bracket contents are correct.
- **Q5 ✓** ensemble claims (4000 samples, seeded): achiral Σγ_z/N ~ 3e-4
  (≈1/√N noise), chiral+coupled 2.6e-2 ≠ 0, uncoupled γ_z ≡ 0
  pointwise (1e-19). In a rigid dimer δ is rotation-invariant (inner products
  preserved) — the rationale for the paper's note "µ,α,δ do not depend on orientation".
- **K33**: the paper's γ = i(J₁₂−J₂₁) = 2×HVector.gamma (without the ½).

## 1. Goals — `dipoles/ensemble.py`

1. `coupling_delta_3d(m,n,u,A,B)` = (n·m)A + (n·u)(m·u)B (M28, Green).
2. Symbolic derivations + K28 anchors: `forward_jones_3d` (Eqs. 26-29),
   `gamma_z_3d` (Eq. 31, (n×m)_z label note), `transverse_jones_3d` →
   γ_x (Eq. 33 + 34-35 split), `backscatter_jones_3d` → γ₋z (with CORRECTED
   prefix; M30 #6 note). δ=0 ⇒ γ_z ≡ 0 symbolic theorem.
3. `is_chiral(m,n,r)` (m×n·r ≠ 0) + numeric layer `jones_3d_numeric`
   (K26: finiteness + resonance guard |1−(αδ)²|).
4. `ensemble_gamma(direction, chiral, d, ...)`: seeded deterministic
   orthogonal-dimer ensembles (Fig. 2 geometry r = d(m−n+z)/√3, achiral
   Z=0) — Q5 claims as tests.
5. **Depolarization bridge (FIRST end-to-end)**: `ensemble_covariance` =
   ⟨|h⟩⟨h|⟩ (with our ½-carrying HVector), trace-normalize → rank>1 PSD; two-
   orientation mixture rank-2 → fed into `propose_decompositions`
   (K21: the result is REASONED — success is not required, the composition and guards
   working IS required).

## 2. Decision

**M37**: the ensemble module does not touch the dimer/general modules; the γ definition
is in the paper convention (2×h₄) under the name `gamma_paper` — does not get
confused with HVector.gamma (K33).

## 3. Acceptance

Eqs. 21-24/26-29/31/33 anchors symbolic; Eq. 9 corrected-prefix anchor
(M30 #6 reasoned); δ=0 theorem; chirality predicate; ensemble Q5 triple
(seeded, N=800 CI-fast); bridge test (rank-2 PSD trace-1 + reasoned
propose report); K26 guards; 192 existing tests green.

**STOP HERE**
