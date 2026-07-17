# MILESTONE L0 — Lorentz Representation Layer (FROZEN-7 opening)

**Date**: 2026-07-17 · **Mode**: stage-gated interactive (user quota-gates
each stage) · **Language**: English

## 0. FROZEN-7 declaration

Third-generation roadmap, frozen at SEVEN stages (tradition: v1
frozen-55 → v2 FROZEN-22 → this): L0 representation layer · L1 verify
the five given identities · L2 find the five missing Σ̄ identities ·
L3 mini-report #1 + feedback window · L4 term-language extension
(T/†/inverse) + self-recovery gate · L5 discovery sweep · L6
consolidation + v1.2.0 closure. The count does not change; changes go to
the user as a critical-decision note. Source: the collaborator's written
work order of 2026-07-17 (Σ^μ definitions + three tasks), archived in the
project. Execution cadence: STOP at the end of every stage; the user
gates continuation.

## 1. Goal

A `lorentz/` sibling module (like `dipoles/`) exposing the Lorentz face
of the Z-matrix algebra: the Σ^μ basis (which the pre-implementation
probe showed to be EXACTLY the engine's existing Z-matrix basis — the
bridge is a theorem, not an analogy), Z(α) = α_μΣ^μ, Σ̄^μ, the guarded
inverse, Λ = ZZ*, and boost/rotation parametrizations, all with exact
symbolic anchor tests.

## 2. Pre-implementation probe (done; seeds/symbolic)

- Σ^μ equals the engine Z-basis (numeric 4/4, to be locked symbolically).
- Σ^T = Σ* (hence Σ† = Σ) for all four.
- **Theorem (guard-free):** Z(α)·Z̄(α) = (α·α)·I with α·α ≡ α₀²−α₁²−α₂²−α₃²
  — the spec's inverse formula is its α·α = 1 corollary (a genuine
  Horn-conditional statement; M32 machinery's first real workload).
- **Theorem:** Λ^T g Λ = (α·α)(α·α)* · g for GENERIC complex α
  (g = diag(1,−1,−1,−1)); under the guard α·α = 1 this is the Lorentz
  property Λ^TgΛ = g.
- Anchors: α = (cosh(φ/2), sinh(φ/2)n̂) reproduces the textbook boost
  matrix exactly; α = (cos(θ/2), i·sin(θ/2)n̂) reproduces the rotation
  block (z-rotation lands with R[1][2] = +sin θ — a CONVENTION, recorded
  M29-style per the spec's own "sign differences are conventions" note).

## 3. Work items

1. `src/organon_mueller/lorentz/` — `SIGMA`, `SIGMA_BAR`, `METRIC`,
   `z_matrix`, `z_bar_matrix`, `minkowski_square`, `z_inverse` (guard
   documented), `lorentz_matrix`, `boost_alpha`, `rotation_alpha`.
   The Σ literals are transcribed from the spec (authoritative source);
   the equality with the engine basis is a TEST, not an assumption.
2. `tests/test_lorentz.py` — exact symbolic: engine-basis bridge,
   Clifford relations, Σ^T=Σ*/hermiticity, the two theorems above (both
   orders Z·Z̄ and Z̄·Z), guarded inverse, ZZ*=Z*Z + Λ real, boost and
   rotation anchors; one seeded numeric sanity (seed 20260716).
3. Doc-count claims bumped (README/ROADMAP); ROADMAP gains the FROZEN-7
   block with L0 marked.

## 4. Acceptance

Full suite green with updated counts; adversarial review PASS (same
reviewer; focus: the two theorems re-derived independently, anchor
matrices checked against the literature, convention notes honest, no
overclaim — everything here is evidence class symbolic-proof except the
seeded sanity). STOP after review; push queued until the user provides
the new PAT. No claim about Task 1–3 outcomes is made in this stage.

**STOP HERE**
