# Addendum — coupled-dipole engine (feedback package #1, part 2)

*Same labeling as the main README: **verified** = machine-checked against
your published equations/tables; **candidate** = beyond them, no claim.
Interpretation remains yours (novelty protocol, human-final step).*

## Verified against PRB 98, 045410 (2018)

- **The three-term decomposition (Eq. 25) as a theorem**: we solve the
  coupled 4x4 dipole system symbolically and prove T =
  γ[α₁J₁ + α₂J₂ + α₁α₂ΛJ_int] exactly — the decomposition is *derived*,
  not assumed. The closed forms (14)-(17), the determinant structure
  det(A) = λ₁λ₂(λ₁λ₂ − Λ²) behind Eq. (42), the hybrid frequencies
  (45)-(46), and the hybrid-basis identity |t⟩ = ν₊|h₊⟩ + ν₋|h₋⟩ with
  the g₁ = g₂ orthogonality (basis defined in Eqs. 61-64; the
  orthogonality statement appears near Eqs. 73-74) are all reproduced
  symbolically (permanent tests); the Eq. (70) inversion at (90°, 135°)
  matches.
- **Your covariance-vector convention (Eq. 29) is exactly our JOSA A
  34, 80 convention** — sentinel-tested in both directions, so dimer
  physics flows directly into the covariance/Mueller machinery.
- The dephased-detector mechanism (Eqs. 35-37) reproduces: the
  interaction term alone acquires a fourth (circular) component,
  vanishing iff χ = 0 or parallel dipoles, purely circular at χ = π.

## Verified against Symmetry 12, 1790 (2020)

- The general-geometry Jones (Eq. A11) re-derived from the coupled
  system (far-field bookkeeping resolved: A11 corresponds to
  T = e₂p₁ + p₂, i.e. a global e₂ absorbed); special case (A12/Eq. 3-4)
  exact. The 90° matrices J_A = g[[0,0],[µ,1]], J_B = g[[0,−µ],[0,1]]
  are derived from radiation projection and satisfy J_B = R(J_A).
- **Perrin's reciprocity as a general symbolic theorem**: with
  R(J) = σJᵀσ (your Eq. 1), amp_B = (σu*)†R(J)(σv*) = v†Ju for ANY
  Jones matrix — your Eqs. (8)-(13) construction follows as the special
  case (I_B = (|x|²+|y|²)·I_A, your Eq. 13).

## Verified against the OA-in-ensemble preprint

- The 3D rank-1 scalar reduction (your Eqs. 16-24), verified exact to
  ~3e-16 against the full 3D dyadic 6x6 solve (the planar xy-block
  analog was additionally proven exact symbolically in review); the
  forward Jones (26)-(29); γ_z (31); γ_x and its split (33)-(35),
  including the point that γ_x1 survives the uncoupled limit (the
  metasurface observation).
- **δ = 0 ⇒ γ_z ≡ 0 for every orientation, as a symbolic theorem** (your
  central forward-scattering statement), plus the ensemble statistics
  (chiral-coupled Σγ_z ≠ 0; achiral Σγ_z = 0 with Σ|γ_z| ≠ 0; uncoupled
  pointwise zero) reproduced with deterministic sampling.
- Bridge (candidate zone): ensemble-averaged covariances ⟨|h⟩⟨h|⟩ of
  finite orientation mixtures feed our symmetry-conditioned
  decomposition solvers end-to-end.

## Suspected print artifacts — we would be grateful for confirmation

*(None affects any physical conclusion; each was found by cross-checking
the papers' own internal equations, and each was independently
re-derived by a separate reviewer.)*

| # | Paper | Location | Note |
|---|---|---|---|
| 1 | PRB 98, 045410 | Eq. (37), p. 045410-4 | printed at 2× the scale of the paper's own Eq. (29) half-convention (at χ=0 it should reduce to Eq. (32)) |
| 2 | PRB 98, 045410 | Eq. (39), p. 045410-5 | numerator prints ηᵢωᵢ; the paper's own Eqs. (44)-(45) require ηᵢωᵢ² |
| 3 | ensemble preprint | Eq. (31), Appendix | the bracket (n_xm_y − m_xn_y) is correct and equals (n×m)_z; the label prints "(m×n)_z" |
| 4 | ensemble preprint | Eq. (9), main text | prefactor prints −2iεαµ; since µ = εα/(1−(αδ)²) already contains εα, the derived prefactor is −2iµ |
| 5 | ensemble preprint | Eq. (30), Appendix | prints "i(J₁₂ − J₁₂)" — second index should be J₂₁ |
| 6 | ensemble preprint | Eq. (32), Appendix | path phases print e^{ir_x/2}; the k is dropped |

(The two Appl. Opt. 55, 2543 diagnoses — Eq. 17 h₀₃ and Eq. 21 [1,3] —
are in the main README.)

## Try it

```bash
python docs/kuntman-package/demo.py   # section 4 = dipole engine
```
