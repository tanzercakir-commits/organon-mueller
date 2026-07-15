# STAGE 14 — REPORT (N-Dimer / Ensemble Generalization, Phase D 3/4)

**Date**: 2026-07-13 · **Spec**: `specs/stage-14.md` · **Mode**: autonomous
**Result**: COMPLETED — 203/203 tests green; **the 3D formalism of the
OA-in-ensemble preprint was derived and anchored; TWO new print diagnoses (M30 #5-#6)
were confirmed against the PDF by the reviewer; the depolarization bridge —
dipole physics → decomposition layer — FIRST end-to-end test.**

## 1. Deliverables (`dipoles/ensemble.py`)

- 3D rank-1 scalar reduction (M28) — reviewer confirmed with full 6×6 solution;
  δ = (n·m)A + (n·u)(m·u)B; anchors: Eqs. 21-24, 26-29 (forward Jones),
  Eq. 31 γ_z, Eq. 33 + 34-35 γ_x separation (γx1 survives in the coupling-free limit —
  metasurface point; the honest form of the paper's statement "does not depend on α and δ"
  is in the test comment), CORRECTED Eq. 9 γ₋z.
- **δ=0 ⇒ γ_z ≡ 0 symbolic theorem** (no OA in coupling-free chiral
  dimers in forward scattering — the paper's central claim).
- Chirality predicate (m×n·r); rigid-dimer δ rotation-invariance
  (justification for ensemble constancy — reviewer confirmed with 1.6e-16).
- Ensemble statistics (seeded, deterministic): chiral+coupled
  Σγ_z ≠ 0; achiral Σγ_z ~ 0 but Σ|γ_z| ≠ 0 (non-ideal ensemble OA);
  coupling-free pointwise 0. Thresholds were extended with reviewer sub-seed statistics
  (with a note on numpy's lack of stream-stability guarantee).
- **Depolarization bridge**: `ensemble_covariance` = ⟨|h⟩⟨h|⟩ trace-1;
  2-orientation mixture rank-2 PSD → `propose_decompositions` JUSTIFIED
  report (3 composite successes + 3 justified rejections — K21).

## 2. M30 series (this stage: #5-#8)

- **#5 Eq. 31**: parenthesis (n_xm_y−m_xn_y) correct algebra = **(n×m)_z**;
  label "(m×n)_z" is sign-reversed (probe + reviewer symbolic).
- **#6 Eq. 9**: prefactor −2iεαµ printed; µ = εα/(1−(αδ)²) already contains εα —
  the derived correct prefactor is **−2iµ** (εα double-counting).
- **#7 Eq. 30**: "i(J₁₂−J₁₂)" — the second should be J₂₁ (obvious typo).
- **#8 Eq. 32**: k dropped in the phases (e^{ir_x/2} → e^{ikr_x/2}).

## 3. Independent audit

Verdict: **PASS** (1 MINOR + 2 trivial — resolved: ensemble thresholds,
unused import, empty-sample guard; d=|r| vs paper-d note).
Reviewer: full 6×6 3D solution ↔ scalar reduction (3.3e-16); anchor
verification from the PDF; frame handedness consistency (with stage-13);
Haar-uniform sampling check; independent reconstruction of the bridge covariance (difference 0.0).

## 4. Next stage (autonomous continuation — Phase D closure)

**Stage 15 — Iterate + feedback window #2**: Phase D retrospective
(M35-M37, K33 sweep, debts); dipole addendum to the Kuntman package (PRB +
Symmetry + ensemble findings, M30 #3-#8 diagnoses — SUBMISSION again
with the user); Phase E preparation (LaTeX report generator + MCP server —
sympify security gate).
