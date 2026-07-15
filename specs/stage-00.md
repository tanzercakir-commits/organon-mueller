# STAGE 0 — Repo Skeleton + Representation Layer + Known-Identity Regression Core

**Date**: 2026-07-13
**Project**: organon-mueller (Organon_V2)
**Previous stage**: — (first stage)

---

## 1. Context

Organon v1 (FOL-based physics reasoning system, frozen-55, `v1.0`) is closed. The
sub-problem of v2: **automated identity discovery in the Stokes-Mueller polarization
formalism**. Domain references: Kuntman et al. 2016–2020 publications
(JOSA A 34,80; PRA 95,063819; PRB 98,045410; Applied Optics 55,2543; JOSA A quaternion).

The logical framework of v2: the **equational fragment** of FOL (equational logic, Birkhoff
rules) + **Horn-conditional rules** (P(x) → t₁ = t₂). The discovery engine (egglog) comes in
later stages; this stage lays the ground on which the engine will run.

## 2. Goals

1. Repo skeleton: `specs/`, `reports/`, `src/organon_mueller/`, `tests/`, CI.
2. **Representation layer**: six isomorphic representations — Jones J (2×2), Mueller M (4×4),
   covariance matrix H (4×4 Hermitian), covariance vector |h⟩ = (τ,α,β,γ)ᵀ,
   Z matrix (4×4), h biquaternion — and the transformations among them.
3. **Known-identity library (core)**: fundamental identities from the literature, recorded
   with source + side-condition (guard) metadata.
4. **Regression tests**: each known identity is verified symbolically (SymPy) and/or
   numerically (NumPy random sampling). Target: 100% recovery of the known.
5. CI: GitHub Actions, pytest on every push.

## 3. Architectural decisions

- **M1. Source representation |h⟩**: the internal state is the quadruple (τ,α,β,γ); the other
  five representations are generated from it. Rationale: rank-1 H ↔ |h⟩ is one-to-one; Z, J, h
  are all linear in the same parameters.
- **M2. Double verification**: every identity is first attempted symbolically; if symbolic is
  costly, numerical sampling (N≥50 random complex parameters, tol=1e-9) is accepted. Which
  mode it was verified in is kept in the identity record.
- **M3. Side conditions first-class**: every identity carries a `conditions` field
  (e.g. `nondepolarizing`, `tau_real`, `unitary`). This is the seed of the Horn-conditional
  rule infrastructure.
- **M4. API stateless and serializable**: functional core; inputs/outputs are SymPy
  expressions/matrices. A JSON bridge for later MCP server wrapping comes in subsequent stages.
- **M5. Conventions fixed to the Kuntman-Arteaga papers**: Pauli order
  (σ0,σ1,σ2,σ3), the A matrix, the explicit form of Z, and the quaternion signs as in JOSA A 34,80
  and arXiv:1705.07147. Literature with different conventions (Gil et al.) is mapped via
  transformation; the core does not change.
- **M6. egglog is ABSENT at this stage**: the discovery engine is Stage 2+ (spike first). This
  stage is only the ground.

## 4. Strict rules

- K1. No untested transformation/identity goes into `main`.
- K2. Fixed seed in numerical tests — CI must be deterministic.
- K3. No print/side-effect inside `src/organon_mueller`; pure functions.
- K4. Python ≥3.10; dependencies: sympy, numpy (test: pytest). No other dependency is added.
- K5. File/directory names as in this spec; the runner-immutability principle continues here
  as "the representation layer API is immutable" (in Stage 1+ signatures do not change,
  only additions).

## 5. Deliverable

```
organon-mueller/
├── README.md                       (project intro, v1 link, status)
├── pyproject.toml                  (src-layout, pip install -e ".[test]")
├── .gitignore
├── .github/workflows/ci.yml        (pytest, py3.11 + py3.12)
├── specs/stage-00.md               (this file)
├── reports/stage-00-REPORT.md
├── src/organon_mueller/
│   ├── __init__.py                 (version + top-level API export)
│   ├── algebra/
│   │   ├── __init__.py
│   │   ├── basis.py                (Pauli, A, Πij, quaternion basis matrices 1,I,J,K)
│   │   ├── quaternion.py           (BiQuaternion: Hamilton product, bar/†, matrix representation)
│   │   └── states.py               (HVector + all transformations + Stokes helpers)
│   ├── conditions.py               (predicates: nondepolarizing, hermitian_state, unitary_state)
│   ├── verify.py                   (symbolic/numerical verification helpers, sampler)
│   └── identities/
│       ├── __init__.py
│       └── known.py                (Identity record + KNOWN_IDENTITIES library)
└── tests/
    ├── test_basis.py
    ├── test_quaternion.py
    ├── test_isomorphisms.py
    ├── test_known_identities.py
    └── test_conditions.py
```

## 6. Verification (this stage's "recover the known" list)

| # | Identity | Source | Condition | Mode |
|---|---|---|---|---|
| I1 | M = ZZ\* = Z\*Z | JOSA A 34,80 Eq.(34) | nondepolarizing | symbolic |
| I2 | M = A(J⊗J\*)A⁻¹ consistent with I1 | standard + Eq.(35) | — | symbolic |
| I3 | det Z = (τ²−α²−β²−γ²)² | JOSA A 34,80 Eq.(48) | — | symbolic |
| I4 | Explicit form of Z⁻¹ (sign flip) | Eq.(50) | det≠0 | symbolic |
| I5 | ⟨h|h⟩ = M₀₀ | Eq.(17) | — | symbolic |
| I6 | tr(MᵀM) = 4M₀₀² | Gil-Bernabeu | nondepolarizing | numerical |
| I7 | h₂h₁ ↔ Z₂|h₁⟩ (quaternion product) | arXiv:1705.07147 Eq.(21-23) | — | symbolic |
| I8 | Z = τ1+iαI+iβJ+iγK (matrix representation = Z) | Eq.(13) | — | symbolic |
| I9 | s′ = hsh† ↔ |s′⟩ = M|s⟩ and S′ = ZSZ† | Eq.(10),(26) | — | numerical |
| I10 | Z_iZ_j\* = Z_j\*Z_i (commutation) → M(Z₂Z₁)=M₂M₁ | JOSA A 34,80 Eq.(38) | — | symbolic+numerical |
| I11 | Rotation: |h(θ)⟩=R(θ)|h⟩, h(θ)=rhr†, M(θ)=R(θ)MR(−θ) | Eq.(30-34) | — | numerical |
| I12 | Hermitian state: τ,α,β,γ ∈ ℝ ⇒ M = Mᵀ | Eq.(46),(53) | hermitian_state | numerical |
| I13 | Unitary state: τ∈ℝ, α,β,γ∈iℝ ⇒ MMᵀ = M₀₀²·I | Eq.(54-56) | unitary_state | numerical |
| I14 | Rank(H)=1 ⇔ nondepolarizing; H=|h⟩⟨h|; Mij=tr(ΠijH) | Cloude/Gil | — | numerical |

Acceptance criterion: 14/14 verified; entire pytest suite green; CI file syntactically valid.

## 7. Delivery format

Files are written to the user's `C:\Projects\organon-mueller` clone +
`reports/stage-00-REPORT.md` result report + suggested commit message. Push is on the user.

## 8. Special warnings

1. Complex conjugate in SymPy: parameters with `sympy.symbols(..., complex=True)`;
   use `conjugate()`, and watch out for `.H` instead of `.T` (H = conjugate transpose).
2. The quaternion Hermitian conjugate h† = τ\*1+iα\*i+iβ\*j+iγ\*k — NOT the naive component-wise
   `conjugate` (see biquaternion: h† = conj(bar(h)) components).
3. Numerical rank test: threshold 1e-9·λ_max; do not use an absolute threshold.
4. R(θ) is in 2θ (Mueller space); the quaternion rotator r = cosθ·1 + sinθ·k
   (arXiv Eq.(33)) — watch out for the θ/2 confusion.
5. Windows clone: files are written with LF; add `__pycache__`, `.pytest_cache`,
   `*.egg-info`, `.venv` to .gitignore.

## 9. Out of scope

- egglog / discovery engine (Stage 2+, spike first)
- Decomposition deriver, dipole module (Stage 3+)
- MCP server / web UI / LaTeX report generator (packaging stages)
- LICENSE choice (user decision — repo private, no urgency)
- General rank-2/3/4 operations for depolarizing M (only predicate level exists)

**STOP HERE** — do not go outside this spec; when uncertain write an "open question" to the REPORT.
