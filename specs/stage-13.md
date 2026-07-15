# STAGE 13 — γ Direction-General Automation (Phase D 2/4)

**Date**: 2026-07-13 · **Source**: Symmetry 12, 1790 (2020) App. A +
stage-12 dephased mechanism · **Mode**: autonomous

## 0. Probe (MANDATORY — done: probes/probe-gamma-prespec.py, seed 20260713)

- **Q1 ✓ (phase accounting resolved)**: the far-field weight that produces Eq. A11 is
  **T = e₂·p₁ + p₂** (~1e-17 in 5 trials) — dipole-2 is closer to the detector by r_z;
  the paper multiplied the single-particle terms so as to carry e₂ onto them.
- **Q2 ✓** scalar reduction (p₁ = P₁ŷ, p₂ = P₂n̂(θ), coupling scalar
  n̂ᵢᵀMn̂ⱼ, M = e₁k²(A·I + B·wwᵀ), w=(C₁C₂,S₁)) == the full 2×2 solution.
- **Q3 ✓** JA = g[[0,0],[µ,1]], JB = g[[0,−µ],[0,1]] derivation: scalar
  system + radiation projection (only p_y radiates to +x; the −z local frame
  H′=−x sign flip) — one-to-one with the paper; **JB == R(JA)** ✓.
- **Q4 ✓** General Perrin: with R(J) = σJᵀσ (σ=diag(1,−1)),
  amp_B = (σu*)†R(J)(σv*) == v†Ju = amp_A — for EVERY J (5 trials exact).
- **Q5 ✓** Forward-direction γ: h₄ = i·e₁α₁α₂Δ₁(1−e₂²)/(2N); e₂²=1 (same plane
  or multiples of λ/2) → 0.

**K33 note**: the Symmetry paper's definitions δ₁=k²(A+S₁²B), δ₂=k²(C₁C₂S₁B)
are DIFFERENT from PRB's definitions δ₁=k²A, δ₂=k²(A+B) (homonym but different
objects); in the module the naming `delta1_s/delta2_s` + a docstring warning.

## 1. Goals — `dipoles/general.py`

1. `coupling_matrix(phi1, phi2, A, B, e1)` = e₁(A·I₂ + B·wwᵀ) (M28:
   from Green, not from a table); `symmetry_deltas` (δ₁ₛ, δ₂ₛ, Δ₁, Δ₂
   expressions — K33 naming).
2. `solve_dimer_general(theta, phi1, phi2, alpha1, alpha2, A, B, e1, e2, E0)`
   — symbolic solution with scalar reduction; `forward_jones_general` (T =
   e₂p₁+p₂ accounting) — **Eq. A11 anchor (K28, symbolically one-to-one)**;
   special case Eq. A12 (φ₁=−45°, θ=φ₂=0: J = g[[1,e₁αδ],[e₁αδ,1]],
   δ=−k²B/2) anchor.
3. `reciprocity_transform(J)` = σJᵀσ; properties: involution, Eq. 1
   pattern; `case_A_jones/case_B_jones` (90° scattering, derived) —
   JA/JB anchors + **the JB == R(JA) theorem**.
4. **Perrin theorem (symbolic, general)**: for every J and normalized u,v
   amp_B == amp_A (the σ-identity above) → I_B = I_A; the paper's
   Eq. 8-13 elliptic-polarizer special case is also anchored.
5. **γ-map**: `forward_gamma_general` — h₄ = i·e₁α₁α₂Δ₁(1−e₂²)/(2N)
   THEOREM (over the J derived from A11, via jones_to_hvector); zero
   conditions (Δ₁=0 OR e₂²=1 OR no coupling) symbolic; the 90°-direction
   h₄(JA) = −igµ/2 ≠ 0 record (the γ-signature of asymmetric scattering).
6. K26 guards: finiteness + N~0 resonance in the numeric evaluators.

## 2. Decisions

**M36**: The Symmetry-geometry module does NOT TOUCH stage-12 `dimer.py` (the PRB
geometry is the same-plane special case; consistency test: at e₂=1, θ and
w-compatible configuration the two modules must give the same J — sentinel).

## 3. Acceptance

Eq. A11 symbolically one-to-one; the A12 special case; JA/JB + JB==R(JA); the general
Perrin symbolic; the Eq. 8-13 anchor; the γ-theorem + zero conditions; the PRB-consistency
sentinel; the K26 guards; 179 old tests green.

**STOP HERE**
