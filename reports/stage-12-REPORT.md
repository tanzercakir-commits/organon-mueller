# STAGE 12 — REPORT (PHASE D Opening: Coupled-Dipole Symbolic Engine)

**Date**: 2026-07-13 · **Spec**: `specs/stage-12.md` · **Mode**: autonomous
**Result**: COMPLETED — 179/179 tests green; **the main results of PRB 98, 045410
were symbolically re-derived and are verbatim with the paper**; the
reviewer independently re-did every derivation and **also DID mathematically CONFIRM
our two print-inconsistency diagnoses** (the M30 series is growing).

## 1. Deliverables (`dipoles/` package)

- **`dimer.py`**: projector Jones; Λ = C₁C₂δ₁+S₁S₂δ₂; **decomposition theorem
  (Eq. 25)**: the T DERIVED from the 4×4 coupled system == γ[α₁J₁+α₂J₂+α₁α₂ΛJ_int],
  fully symbolic (M28); covariance bridge `jones_to_hvector` — the paper's
  Eq. 29 == our JOSA A HVector convention (bidirectional sentinel);
  dephased J'_int (**the mechanism of A13 γ-automation**: h₄ =
  −(i/2)sinΔφ(1−e^{iχ}); χ=0 or parallel → 0; χ=π → purely circular);
  numerical evaluator (K26: finiteness+resonance guards).
- **`hybrid.py`**: det THEOREM det(A)=λ₁λ₂(λ₁λ₂−Λ²); ω± derivation ==
  Eq. 45/46; hybrid basis — **two general theorems**: |t⟩=ν₊|h₊⟩+ν₋|h₋⟩ (for every
  generic g,φ) and g₁=g₂ ⇒ ⟨h₊|h₋⟩=0 (from the |h₁+h₂|²=|h_int|²=1+cos²Δφ
  identity); general-angle coefficient solution + Eq. 70 anchor; guards
  (singularity — det=sin³Δφ/2, reviewer derivation; t₄≠0 out of span; strong
  coupling ω₋² < 0; double root).

## 2. M30 print-inconsistencies (reviewer-confirmed)

- **Eq. 37**: printed 2× scaled relative to the paper's own Eq. 29 (with ½)
  convention (at χ=0 it also contradicts its own Eq. 32). The direction claims
  are sound. Probe Q6's "False" output is this discovery itself — the archive note
  is in the probe file.
- **Eq. 39 vs Eq. 44**: the printed Lorentzian numerator is ηω, the paper's Eq. 44
  (and the 4ω₁²ω₂²η₁η₂Λ² term of Eq. 45) requires ηω² — the Eq.-44-consistent
  form was implemented, the `lorentzian`↔Eq.44 link is test-anchored.
- Eq. 33 series-product h-vector printed with a cosΔφ/2 factor (scale-free report).
  Chirality refinement: the 4th component (i/4)sin2Δφ — zero in parallel OR
  perpendicular (the product of crossed projectors annihilates) cases.

## 3. Independent audit

Verdict: **PASS** (4 MINOR + 2 DOC — all resolved): the angle finiteness
guard; t₄≠0 silent information loss → explicit rejection (K26); strong-coupling imaginary
frequency + double-root behavior; the I=I⁺+I⁻ and lorentzian consistency tests;
the probe archive note; the chirality wording correction. The reviewer's independent
derivations: K=diag(δ₁,δ₂) from the Green geometry (the B-term is even in û —
sign-independent); Eq. 25 from scratch (projector scalar reduction); the
det theorem; ω±; the Eq. 33 factor; the two M30 diagnoses; Eq. 70; the
COMPLETENESS of the singularity guard (φ₁=φ₂ mod π the only singular configuration).

## 4. Next stage (autonomous continuation)

**Stage 13 — γ (optical activity) direction-general automation**: the dephased-χ
mechanism + Symmetry 12, 1790 (2020) geometry (e₁/e₂ retardation phases, 90°
scattering JA/JB, Eq. 1 reciprocity transform); target: a γ(χ,φ₁,φ₂) map for an
arbitrary observation direction and reciprocity tests (with the M35 bridge, a candidate
guarded-atom connection to the discovery engine).
