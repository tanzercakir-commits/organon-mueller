# Phase D Retrospective (A12–A15) — stage-15

## 1. What was built

The `dipoles/` package in four steps: the PRB engine (A12: Eq. 25
decomposition THEOREM, ω±, hybrid basis) → orientation-general γ (A13:
Symmetry A11, Perrin general theorem, JA/JB+R) → 3D dimer + ensemble
(A14: δ=0⇒γ_z≡0 theorem, ensemble statistics, depolarization bridge) → this
closure (A15). The bridge chain is complete: **Green function → coupled
dipoles → Jones → HVector → covariance → decomposition layer** — tested
end-to-end (A14).

## 2. Decision/rule scan

- **M35 (dipoles → algebra one-way bridge)** ✅ — dipoles only writes to
  HVector; it did not touch the discovery/decomposition layers.
- **M36 (the Symmetry-general module does not touch the PRB module)** ✅ —
  agreement proven by a SENTINEL (in the φ₁=−π/2, e₁=e₂=1 configuration the
  two modules give the same J; the auditor also verified the u→−u invariance).
- **M37 (ensemble is a separate module; the naming γ_paper = 2×HVector.gamma)**
  ✅ — together with K33 same-name-different-object warnings (Symmetry δ's ≠
  PRB δ's; paper-γ ≠ the h-vector γ component).
- **K33 (PDF anchors with equation number + printing-note)** ✅ — Phase D's six
  M30 records (#3-#8) are the product of this discipline (#1-2 are Phase C/K28
  fixtures); each anchor is positioned in its test docstring.

## 3. M30 cumulative table (eight diagnoses — all independently confirmed)

| # | Source | Location | Diagnosis |
|---|---|---|---|
| 1 | AO2016 | Eq. 17 | h₀₃ imaginary part 0.0161 → 0.1608, consistent with the derived value |
| 2 | AO2016 | Eq. 21 [1,3] | similar digit artifact (−0.0037 → −0.0372) |
| 3 | PRB 98,045410 | Eq. 37 | 2× scale relative to its own Eq. 29 ½-convention |
| 4 | PRB 98,045410 | Eq. 39 | numerator ηω; its own Eq. 44-45 requires ηω² |
| 5 | ensemble preprint | Eq. 31 | parenthesis correct; label (m×n)_z → (n×m)_z |
| 6 | ensemble preprint | Eq. 9 | prefix −2iεαµ → −2iµ (εα double counting) |
| 7 | ensemble preprint | Eq. 30 | "i(J₁₂−J₁₂)" typesetting (→ J₂₁) |
| 8 | ensemble preprint | Eq. 32 | k dropped in the phases |

Lesson: the **pre-spec numeric probe** caught a convention/printing surprise
before it entered the code in all three derivation stages (A12 Q6, A13 Q1
phase accounting, A14 Q4 prefix); A15 was probe-free (no new mechanism). #1-2,
on the other hand, are the product of the K28-era fixture discipline
(Phase C). A permanent part of the rule execution chain.

## 4. Debt inventory

| Debt | Status | Rationale/window |
|---|---|---|
| rank-3 a/b minor variants | DEFERRED (since A11) | measure-zero degenerations; when experimental data arrives |
| guarded-atoms 2nd half (unitary/hermitian campaigns) | OPEN | scope evaluation at the start of Phase E — a note for the A16 spec |
| N>2 coupled dipole chain | DEFERRED | A14 delivered the 2-dipole with FULL 3D geometry+ensemble (the ensemble side of the FROZEN-22 heading); the N>2 linear system is a mechanical generalization, but the publication motivation (which N-configurations?) depends on Kuntman window #2 feedback |
| Fano deep-dive | DEFERRED | PRB itself says "future work"; the engine is ready (the ν± machinery) |
| interpreted_scalars side-conditions | CONDITIONAL DEBT (unchanged) | the feature is not in the language |

## 5. Handoff to Phase E

Packaging vision (user, project head): the end user CANNOT USE a terminal →
A16 LaTeX report generator (first-class output), A17 MCP server (sympify
STAGE-2 GATE security requirement — serialize.py note: hardening is MANDATORY
before the external surface is opened), A18 optional web UI, A19 docs. The
engine + decomposition + dipole layers are the CONTENT sources of the report
generator; the Kuntman package + its addendum are the report's FIRST real
usage scenario.
