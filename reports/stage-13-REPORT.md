# STAGE 13 — REPORT (γ Direction-General Automation, Phase D 2/4)

**Date**: 2026-07-13 · **Spec**: `specs/stage-13.md` · **Mode**: autonomous
**Result**: COMPLETED — 192/192 tests green; **the general geometry of Symmetry 12,
1790 (2020) App. A was derived (Eq. A11 symbolically verbatim), the Perrin
reciprocity theorem was symbolically proven for EVERY J, and the direction/phase
map of γ was closed at theorem level.**

## 1. Deliverables (`dipoles/general.py`)

- **General solution**: scalar-reduced coupled system (M28) → `forward_jones
  _general` == **Eq. A11 (hand-entered anchor, K28)**; the A12 special case; the
  probe solved the phase accounting: T = e₂p₁+p₂ (the reviewer confirmed with physical
  path phases: the paper's A11 carries a global e₂ — in the docstring).
- **Reciprocity**: R(J) = σJᵀσ (the Eq. 1 pattern + involution); derived
  JA = g[[0,0],[µ,1]], JB = g[[0,−µ],[0,1]] anchors; **the JB == R(JA)
  theorem** (both sides derived independently — not by construction).
- **Perrin theorem (general, symbolic)**: amp_B = (σu*)†R(J)(σv*) == v†Ju
  → I_B = I_A, for EVERY J; the paper's Eq. 8-13 elliptical-polarizer special
  case additionally anchored (I_B = (|x|²+|y|²)·I_A — Eq. 13 verbatim).
- **γ-map theorem**: h₄ = i·e₁α₁α₂Δ₁(1−e₂²)/(2N); the zero set is COMPLETE
  (reviewer verified): no coupling ∨ Δ₁=0 (θ=±π/2 the coupled-but-blind branch
  tested) ∨ e₂²=1 (co-planar / λ/2 offsets are γ-blind in the forward direction).
  In the 90° direction h₄(JA) = −igµ/2 ≠ 0 (asymmetric-scattering signature — a known
  fact, no novelty claim).
- **K33 naming warning**: the Symmetry paper's δ₁ₛ/δ₂ₛ ≠ PRB's δ₁/δ₂
  (namesakes, different objects) — the `_s` suffix in the module + docstring.
- **M36 sentinel**: in the φ₁=−π/2, e₁=e₂=1 configuration the general solver ==
  the stage-12 PRB decomposition (with the δ₁=A, δ₂=A+B mapping); the u→−u invariance
  is reviewer-confirmed.

## 2. Independent audit

Verdict: **PASS** (2 LOW + 1 cosmetic — all resolved: the A11 anchor was made
fully hand-written + symmetry_deltas moved to a separate test;
in the numerical layer, explicit rejection instead of silent clipping of a complex angle;
cleanup of an unused unpack; the θ=π/2 coupled-blind branch test). The reviewer:
proved that the xy-block reduction from the full 3D dyadic Green 6×6 solution is
EXACT (the rank-1 in-plane projectors (û·p)û annihilate the z-component);
wrote A11 from the PDF itself and found it verbatim; re-derived JA/JB from the raw 3D
radiation; and verified the Perrin σ-identity and the completeness of the γ zero-set.

## 3. Next stage (autonomous continuation)

**Stage 14 — N-dimer / ensemble generalization**: the project file
OAinanenseble.pdf will be read before the spec; the generalization of the
scalar-reduction structure of N coupled dipoles + the covariance/Mueller correspondence
of the ensemble average (depolarization bridge — a candidate first physical connection
with the decomposition layer).
