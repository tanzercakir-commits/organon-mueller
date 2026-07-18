# organon-mueller

[![PyPI](https://img.shields.io/pypi/v/organon-mueller)](https://pypi.org/project/organon-mueller/)
[![Python](https://img.shields.io/pypi/pyversions/organon-mueller)](https://pypi.org/project/organon-mueller/)
[![CI](https://github.com/tanzercakir-commits/organon-mueller/actions/workflows/ci.yml/badge.svg)](https://github.com/tanzercakir-commits/organon-mueller/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A symbolic engine for the **Stokes–Mueller algebra of polarization optics**:
it decomposes depolarizing Mueller matrices into nondepolarizing components,
discovers and certifies algebraic identities of the underlying state algebra,
models coupled oriented dipoles, and reports every result as
evidence-labelled LaTeX — with each mathematical statement gated by a written
verification contract.

> **Status: experimental research software.** Results are labelled by evidence
> class — **verified** (machine-checked against published equations/tables:
> symbolic-exact or seeded-numeric) or **candidate** (beyond the published
> results; no novelty or physics claim — that judgement is left to human
> experts, per [`docs/novelty-protocol.md`](docs/novelty-protocol.md)).
>
> Released under the [MIT License](LICENSE).

## What it does

- **Represents** a pure polarization state in six isomorphic ways — Jones
  matrix `J`, Mueller matrix `M = ZZ*`, covariance matrix `H`, covariance
  vector `|h⟩ = (τ, α, β, γ)`, Z-matrix, and biquaternion — with exact,
  symbolically proven conversions between all of them [1, 2, 3].
- **Decomposes** depolarizing Mueller matrices into symmetry-conditioned
  nondepolarizing components: the six fundamental variants and three
  composite types of the symmetry-conditioned decomposition [4], *derived*
  from rank-1 minor conditions (not transcribed from the published tables),
  plus a rank-3 three-term zone that goes beyond the published cases.
- **Discovers** algebraic identities by equality saturation over a
  covariance-vector term language (egglog), with every candidate certified
  by engine-independent symbolic proof; guarded atoms open a
  Horn-conditional channel (`P(x) → t₁ = t₂`).
- **Models** coupled oriented dipoles [5, 6, 7]: the three-term scattering
  decomposition as a theorem, mode hybridization, optical activity, Perrin
  reciprocity, and ensemble statistics — bridged back to the decomposition
  layer through the covariance representation.
- **Carries a Lorentz face** (`organon_mueller.lorentz`): the Σ^μ / Z =
  α_μΣ^μ / Λ = ZZ* algebra of the SL(4,ℂ)-style construction — the Σ^μ
  basis coincides exactly with the engine's Z-matrix basis. Verified and
  completed identity families in guard-free theorem form, a self-recovery-
  gated term language, and a fully decided 128-sandwich discovery sweep
  (40 proven expansions / 88 symbolic negative certificates,
  `reports/sweep-lorentz-01.json`).
- **Reports** any of the above as deterministic, evidence-labelled LaTeX.

## Installation

Requires Python ≥ 3.10 (the discovery engine needs ≥ 3.11).

From [PyPI](https://pypi.org/project/organon-mueller/):

```bash
pip install organon-mueller                # base
pip install "organon-mueller[ui]"          # + local web interface
pip install "organon-mueller[discovery]"   # + discovery engine (egglog)
pip install "organon-mueller[mcp]"         # + MCP server surface
```

For development, from a clone:

```bash
pip install -e ".[test,discovery,mcp,ui]"
python -m pytest -q                     # full suite: 411 tests collected (discovery self-skips on py3.10)
```

## Quickstart

Interactive (no code) — the local web interface:

```bash
organon-ui       # opens http://127.0.0.1:7860 (needs the ui extra)
```

As a library:

```python
from organon_mueller import HVector

h = HVector.generic("a")   # generic complex (tau, alpha, beta, gamma)
M = h.to_mueller()         # M = Z Z*
Z = h.to_z()
q = h.to_quaternion()      # tau*1 + i*alpha*i + i*beta*j + i*gamma*k
```

```python
import numpy as np
from organon_mueller.decomposition import decompose

# a depolarizing Mueller matrix -> a symmetric + a generic pure component
result = decompose(mueller=my_4x4_matrix, symmetry="type1")
print(result.alpha1, result.m1, result.m2)
```

Full demonstration (decomposition against a published worked example,
rank-3 recovery, the hypothesis bridge, the dipole engine):

```bash
python examples/demo.py
```

## Usage surfaces

| Surface | For | Entry |
|---|---|---|
| Python package | scripting / integration | `import organon_mueller` |
| Local web UI | interactive use, no code (localhost only) | [`docs/README-ui.md`](docs/README-ui.md) |
| MCP server | tool use from an assistant | [`docs/README-mcp.md`](docs/README-mcp.md) |
| Static web viewer | reading results in a browser (no terminal) | `web/index.html` |

Nothing is hosted or exposed by the project. The local web UI binds to
127.0.0.1 only (no tunnel, no public link); the MCP server and static
viewer are **code + tests only** — running them is your decision.

## Verification contract (the trust anchor)

No mathematical statement reaches `main` without passing the layers in
[`docs/VERIFICATION.md`](docs/VERIFICATION.md): exact symbolic proof · seeded
numeric checks · regression against the 21 identities of the known-identity
library (each tied to a published equation) · engine-independent
certification of every discovery candidate · an independent adversarial
review of every change set (each reviewer re-derives the mathematics from
scratch) · a 3-version CI matrix. Numeric confidence is never a substitute
for a passing test.

## Architecture

Layered, with one-way dependencies: `algebra → identities/conditions →
discovery / decomposition / dipoles → reporting → mcp_server → web / ui`,
plus a `safe_parse` security layer guarding deserialization. See
[`docs/architecture.md`](docs/architecture.md) for the layer map and the
index of design decisions, and
[`docs/user-guide.md`](docs/user-guide.md) for a task-oriented walkthrough.

Every change lands with a written spec ([`specs/`](specs/)) and a closing
report ([`reports/`](reports/)); nothing untested reaches `main`.

## References

The algorithms implement, verify against, and extend results from:

1. E. Kuntman, M. A. Kuntman, O. Arteaga, *Vector and matrix states for
   Mueller matrices of nondepolarizing optical media*, J. Opt. Soc. Am. A
   **34**, 80 (2017).
2. E. Kuntman, M. A. Kuntman, O. Arteaga, *Quaternion algebra for
   Stokes–Mueller formalism*, arXiv:1705.07147 (2017).
3. E. Kuntman, M. A. Kuntman, J. Sancho-Parramon, O. Arteaga, *Formalism of
   optical coherence and polarization based on material media states*,
   Phys. Rev. A **95**, 063819 (2017).
4. E. Kuntman, O. Arteaga, *Decomposition of a depolarizing Mueller matrix
   into its nondepolarizing components by using symmetry conditions*,
   Appl. Opt. **55**, 2543 (2016).
5. M. A. Kuntman, E. Kuntman, J. Sancho-Parramon, O. Arteaga, *Light
   scattering by coupled oriented dipoles: decomposition of the scattering
   matrix*, Phys. Rev. B **98**, 045410 (2018).
6. M. A. Kuntman, E. Kuntman, O. Arteaga, *Asymmetric scattering and
   reciprocity in a plasmonic dimer*, Symmetry **12**, 1790 (2020).
7. M. A. Kuntman, E. Kuntman, *Plasmonic dimers in a solution: a
   theoretical approach to the optical activity in an ensemble of randomly
   oriented chiral and achiral plasmonic dimers*, preprint.

## License

[MIT](LICENSE).
