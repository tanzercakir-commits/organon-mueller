# STAGE 12 — Coupled-Dipole Symbolic Engine (PHASE D opening)

**Date**: 2026-07-13 · **Source**: PRB 98, 045410 (project PDF read; the Symmetry
12, 1790 (2020) coupled-oscillator appendix also read — its e₁/e₂ delayed
geometry and 90° scattering/reciprocity is in the A13 scope) · **Mode**: autonomous

## 0. Pre-implementation probe (MANDATORY — done, to be copied into probes/)

`scratch/probe_dipoles.py` (seed 20260713), 6 random complex
parameter trials:
- **Q1 ✓** 4×4 direct solution == closed forms (Eq. 14-17) == decomposition
  T = γ[α₁J₁+α₂J₂+α₁α₂ΛJ_int] (Eq. 25), ~1e-12.
- **Q2 ✓** det(A) == λ₁λ₂(λ₁λ₂−Λ²) (Eq. 42 structure).
- **Q3 ✓** hybrid frequencies: the quartic roots == Eq. 45 closed form;
  identical dipoles ω₀√(1±ηΛ) (Eq. 46).
- **Q4 ✓** hybrid-basis identity |t⟩ = ν₊|h₊⟩+ν₋|h₋⟩ and, when g₁=g₂,
  ⟨h₊|h₋⟩=0 (for every φ pair — general-theorem candidate).
- **Q5 ✓** inverse solution of Eq. 70 (φ₁=90°, φ₂=135°).
- **Q6 — PRINT-FACTOR NOTE (M30)**: the components of Eq. 37 are printed at 2×
  scale relative to the paper's OWN Eq. 29 (with ½) convention; the ½-consistent
  value is h₄ = −(i/2)sin(φ₁−φ₂)(1−e^{iχ}). The directional claims (χ=0 or
  φ₁=φ₂ → 0; χ=π → pure 4th component) are unaffected — the anchor is in the ½ form,
  the reasoning is in the test.

## 1. Goals

1. `dipoles/dimer.py`: projector Jones J(φ); Λ = C₁C₂δ₁+S₁S₂δ₂; the SymPy
   setup and solution of the 4×4 coupled system (**M28: T is derived directly from the
   system**); the decomposition theorem T == γ[α₁J₁+α₂J₂+α₁α₂ΛJ_int] symbolically
   EXACT (K28 anchor Eq. 25-27); covariance bridge `jones_to_hvector`
   (paper Eq. 29 == JOSA A HVector — sentinel test); |h⟩₁/|h⟩₂/|h⟩_int
   anchors (Eq. 31-32); series combination Eq. 33 (4th component i·sin(φ₁−φ₂)
   — chirality from the series arrangement); dephased J'_int (Eq. 36) + h₄ anchor
   (with ½, M30 note) — **groundwork for A13 γ-automation**; special cases
   Ta/Tb (Eq. 53-54) anchors; Λ=0 degeneracy (0°,90°) vs Λ≠0
   (−45°,45°) sentinel.
2. `dipoles/hybrid.py`: Lorentzian α(ω); det structure THEOREM (Eq. 42,
   symbolic); ω± derivation == Eq. 45/46 (K28); ν±, hybrid basis |h±⟩
   (Eq. 63-64); **general theorems (symbolic)**: |t⟩ = ν₊|h₊⟩+ν₋|h₋⟩ for every
   (g₁,g₂,g_int,φ₁,φ₂); g₁=g₂ ⇒ ⟨h₊|h₋⟩=0 for every (φ₁,φ₂)
   (from the identity |h₁+h₂|² = 1+cos²Δφ = |h_int|²); general coefficient solution
   `decomposition_coefficients` (3×3 linear; singularity guard — φ₁=φ₂
   dependent vectors) + Eq. 70 special-case anchor; I = I⁺+I⁻ (g₁=g₂).
3. Numeric layer: deterministic random-parameter equality tests;
   K26 guards (resonance denominator |1−α₁α₂Λ²|, singularity of the coefficient solution,
   finite input).

## 2. Decisions

- **M35**: The dipole module does NOT TOUCH the decomposition/discovery layers; the bridge is one-way
  (dipoles → algebra.HVector). The Symmetry-2020 geometry
  (delay phases, 90° scattering, JA/JB reciprocity transform Eq. 1)
  is in A13; the χ-dephasing mechanism is the core of the γ-generation there.
- **K33**: Every anchor based on PDF-reading is entered with an equation number + a
  print-factor/artifact note if any (the M30 discipline continues).

## 3. Acceptance

The decomposition theorem symbolically exact; the det theorem; the ω± anchor; the hybrid-basis
identity + orthogonality general theorem; the Eq. 31-33 anchors; Eq. 70;
Ta/Tb; the Λ sentinels; the dephased h₄ (with the ½ note); the convention sentinel
(Eq. 29 == HVector); the numeric equalities seeded; the K26 guards; 156
old tests green.

**STOP HERE**
