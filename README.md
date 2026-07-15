# organon-mueller

An experimental system that automates the Stokes–Mueller polarization algebra
of the Kuntman–Arteaga formalism, pairing a **symbolic decomposition/derivation
engine** with an **identity-discovery engine** — every result gated by a
written verification contract.

Successor to [Organon v1](https://github.com/tanzercakir-commits/Organon), a
first-order-logic physics reasoning system (frozen at `v1.0`). v2 narrows the
logic to the **equational fragment of FOL** (Birkhoff rules) with
**Horn-conditional guards** (`P(x) → t₁ = t₂`), and deepens the domain to the
algebra of polarized light: Jones matrices, Mueller matrices, covariance
vectors/matrices, Z-matrix states and biquaternions.

> **Status: experimental research software.** Results are labelled by evidence
> class — **verified** (machine-checked against published equations/tables:
> symbolic-exact or seeded-numeric) or **candidate** (beyond the published
> results; no novelty or physics claim — that judgement is left to human
> experts, per [`docs/novelty-protocol.md`](docs/novelty-protocol.md)).
>
> **No licence yet.** Licensing is deliberately deferred and is the author's
> decision; until a `LICENSE` file is added, no usage rights are granted.

## What it does

- **Represents** a pure state in six isomorphic ways (`J`, `M = ZZ*`, covariance
  `H`, `|h⟩`, `Z`, biquaternion) with exact conversions, following JOSA A **34**,
  80 (2017) and PRA **95**, 063819 (2017).
- **Decomposes** depolarizing Mueller matrices into symmetry-conditioned
  nondepolarizing components — the six fundamental variants and three composite
  types of Appl. Opt. **55**, 2543 (2016), *derived* from rank-1 minor
  conditions (not transcribed), plus a beyond-paper rank-3 three-term zone.
- **Discovers** algebraic identities by equality saturation over a covariance-
  vector term language (egglog), with every candidate certified by engine-
  independent symbolic proof; guarded atoms open a Horn-conditional channel.
- **Models** coupled oriented dipoles (PRB **98**, 045410 (2018); Symmetry
  **12**, 1790 (2020); an OA-in-ensemble preprint): the three-term scattering
  decomposition as a theorem, hybridization, optical activity, Perrin
  reciprocity, and ensemble statistics — bridged back to the decomposition
  layer through the covariance representation.
- **Reports** any of the above as deterministic, evidence-labelled LaTeX.

## Three usage surfaces

| Surface | For | Entry |
|---|---|---|
| Python package | scripting / integration | `import organon_mueller` |
| MCP server | tool use from an assistant | [`docs/README-mcp.md`](docs/README-mcp.md) |
| Static web viewer | reading results in a browser (no terminal) | `web/index.html` |

The MCP server and web viewer are **code + tests only**; the project does not
host or expose them anywhere — running them is your decision.

## Quickstart

```bash
pip install -e ".[test]"             # base (Python >= 3.10)
pip install -e ".[test,discovery]"   # + discovery engine (egglog needs Python >= 3.11)
pip install -e ".[test,discovery,mcp]"  # + MCP server surface

python -m pytest -q                  # full suite: 286 tests collected (discovery self-skips on py3.10)
```

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

Run the feedback-package demo (decomposition, rank-3 recovery, the dipole
engine): `python docs/kuntman-package/demo.py`.

## Verification contract (the trust anchor)

No mathematical statement reaches `main` without passing the layers in
[`docs/VERIFICATION.md`](docs/VERIFICATION.md): exact symbolic proof · seeded
numeric checks · known-identity regression against the papers · engine-
independent certification of every discovery candidate · an independent
adversarial review of every stage (each reviewer re-derives the mathematics
from scratch) · a 3-version CI matrix. Non-integer confidence is never a
substitute for a passing test.

## Architecture & workflow

Layered, with one-way dependencies: `algebra → identities/conditions →
discovery / decomposition / dipoles → reporting → mcp_server → web`, plus a
`safe_parse` security layer guarding deserialization. See
[`docs/architecture.md`](docs/architecture.md) for the layer map and the
index of design decisions (M-series) and strict rules (K-series), and
[`docs/user-guide.md`](docs/user-guide.md) for a task-oriented walkthrough.

Milestone discipline inherited from v1: every stage has a spec in
[`specs/`](specs/) and a closing report in [`reports/`](reports/); the roadmap
is frozen at 22 stages ([`docs/ROADMAP.md`](docs/ROADMAP.md)). Nothing untested
reaches `main`.

## References

- E. Kuntman, M. A. Kuntman, O. Arteaga, *Vector and matrix states for Mueller
  matrices of nondepolarizing optical media*, JOSA A **34**, 80 (2017).
- E. Kuntman, M. A. Kuntman, O. Arteaga, *Quaternion algebra for
  Stokes–Mueller formalism*, arXiv:1705.07147 (2017).
- E. Kuntman, M. A. Kuntman, J. Sancho-Parramon, O. Arteaga, *Formalism of
  optical coherence and polarization based on material media states*, Phys.
  Rev. A **95**, 063819 (2017).
- E. Kuntman, O. Arteaga, *Decomposition of a depolarizing Mueller matrix into
  its nondepolarizing components by using symmetry conditions*, Appl. Opt.
  **55**, 2543 (2016).
- M. A. Kuntman, E. Kuntman, J. Sancho-Parramon, O. Arteaga, *Light scattering
  by coupled oriented dipoles: decomposition of the scattering matrix*, Phys.
  Rev. B **98**, 045410 (2018).
- M. A. Kuntman, E. Kuntman, O. Arteaga, *Asymmetric scattering and reciprocity
  in a plasmonic dimer*, Symmetry **12**, 1790 (2020).
