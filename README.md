# organon-mueller

Automated identity discovery for the Stokes-Mueller formalism of polarization
optics — term enumeration, equality saturation, and symbolic verification.

Successor to [Organon v1](https://github.com/tanzercakir-commits/Organon), a
first-order-logic physics reasoning system (frozen at `v1.0`). v2 narrows the
logic to the **equational fragment of FOL** (Birkhoff rules) with
**Horn-conditional guards** (`P(x) -> t1 = t2`), and deepens the domain to the
algebra of polarized light: Jones matrices, Mueller matrices, covariance
vectors/matrices, Z-matrix states and biquaternions, following the
Kuntman–Arteaga state formalism.

## Status

**Stage 2** — discovery engine core v0 (hybrid equality saturation + SymPy
verification). Roadmap frozen at 22 stages: [`docs/ROADMAP.md`](docs/ROADMAP.md).
Trust anchor: the verification contract in [`docs/VERIFICATION.md`](docs/VERIFICATION.md).

| Layer | State |
|---|---|
| Six isomorphic representations (`J`, `M`, `H`, `\|h>`, `Z`, quaternion) + conversions | done |
| Known-identity library with sources & side conditions | done — 21 identities recovered |
| Coherent superposition & symmetry-class identities (PRA 95, 063819; AO 55, 2543) | done |
| Condition predicates / Horn-guard vocabulary | done |
| JSON serialization (MCP-readiness) + LaTeX output | done |
| egglog feasibility spike (noncommutative quaternion fragment) | done — success, hybrid architecture proposed |
| Discovery engine core: enumerate → saturate → harvest → verify (100%) | done — rediscovers I10 family; sound-by-construction guards |
| Scalar-coefficient terms, canonical-form tuning, novelty search | phase B |
| Symmetry-conditioned decomposition deriver | phase C |
| Coupled-dipole symbolic module | phase D |
| MCP server / web UI / LaTeX reports | phase E |

## Quickstart

```bash
pip install -e ".[test]"            # base (Python >= 3.10)
pip install -e ".[test,discovery]"  # + discovery engine (egglog needs Python >= 3.11)
pytest                              # known-identity regression suite
```

```python
from organon_mueller import HVector, verify_all

h = HVector.generic("a")        # generic complex (tau, alpha, beta, gamma)
M = h.to_mueller()              # M = Z Z*
Z = h.to_z()
q = h.to_quaternion()           # tau*1 + i*alpha*i + i*beta*j + i*gamma*k

verify_all()                    # {'I1': True, ..., 'I14': True}
```

## Workflow

Milestone discipline inherited from Organon v1: every stage has a spec in
[`specs/`](specs/) and a closing report in [`reports/`](reports/). Nothing
untested reaches `main`; CI re-runs the known-identity regression suite on
every push.

## References

- E. Kuntman, M. A. Kuntman, O. Arteaga, *Vector and matrix states for Mueller
  matrices of nondepolarizing optical media*, JOSA A **34**, 80 (2017).
- E. Kuntman, M. A. Kuntman, O. Arteaga, *Quaternion algebra for
  Stokes-Mueller formalism*, arXiv:1705.07147 / JOSA A (2019).
- E. Kuntman, M. A. Kuntman, J. Sancho-Parramon, O. Arteaga, *Formalism of
  optical coherence and polarization based on material media states*, Phys.
  Rev. A **95**, 063819 (2017).
- E. Kuntman, O. Arteaga, *Decomposition of a depolarizing Mueller matrix into
  its nondepolarizing components by using symmetry conditions*, Appl. Opt.
  **55**, 2543 (2016).
- M. A. Kuntman, E. Kuntman, J. Sancho-Parramon, O. Arteaga, *Light scattering
  by coupled oriented dipoles: decomposition of the scattering matrix*, Phys.
  Rev. B **98**, 045410 (2018).
