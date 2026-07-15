# Architecture

## Layer map

```
                        ┌──────────────────────────────┐
                        │  web/  (static result viewer) │  presentation only
                        └───────────────┬──────────────┘
                                        │ reads JSON (textContent-only)
                        ┌───────────────┴──────────────┐
                        │  mcp_server/  (tool surface)  │  numeric inputs only
                        └───────────────┬──────────────┘
                                        │
                        ┌───────────────┴──────────────┐
                        │  reporting/  (LaTeX, evidence │
                        │  labels, determinism)         │
                        └───────────────┬──────────────┘
             ┌──────────────────────────┼──────────────────────────┐
             │                          │                          │
     ┌───────┴────────┐        ┌────────┴────────┐        ┌────────┴────────┐
     │  discovery/    │        │ decomposition/  │        │   dipoles/      │
     │  (egglog +     │        │ (AO2016 derive, │        │ (PRB/Symmetry/  │
     │  symbolic cert)│        │  rank-2/3)      │        │  ensemble)      │
     └───────┬────────┘        └────────┬────────┘        └────────┬────────┘
             │                          │                          │
             └──────────────────────────┼──────────────────────────┘
                                        │  (all build on ↓; bridges are one-way)
                    ┌───────────────────┴───────────────────┐
                    │  algebra/ · identities/ · conditions   │  representations,
                    │  · verify · serialize                  │  known facts, guards
                    └───────────────────┬───────────────────┘
                                        │
                              ┌─────────┴─────────┐
                              │  safe_parse.py    │  security: restricted srepr
                              │  (STAGE-2 GATE)   │  parser, never eval/sympify
                              └───────────────────┘
```

## Layer responsibilities & dependency direction

- **`algebra/`** — the six isomorphic representations (`J`, `M`, `H`, `|h⟩`,
  `Z`, biquaternion) and their exact conversions. Depends on nothing else.
- **`identities/`, `conditions.py`** — the known-identity library (21 entries
  with sources + Horn side-conditions) and the guard-predicate vocabulary.
- **`verify.py`, `serialize.py`** — symbolic/numeric equality helpers
  (`DEFAULT_SEED = 20260713`); lossless `srepr`/JSON + LaTeX. Deserialization
  routes through `safe_parse` (the GATE).
- **`discovery/`** — term enumeration, egglog equality saturation, engine-
  independent symbolic certification, guarded atoms, sweeps. Never trusts the
  engine alone (K9/K10): every candidate is re-checked symbolically.
- **`decomposition/`** — AO2016 symmetry-conditioned deriver (`derive`,
  `solve`, `composite`), the beyond-paper `rank3` zone, and the hypothesis
  bridge. Equations are *derived* from rank-1 minors, never transcribed (M28).
- **`dipoles/`** — coupled-dipole symbolic engine (`dimer`, `hybrid`,
  `general`, `ensemble`). Writes **only** into `algebra.HVector` (M35); its
  outputs feed the decomposition layer through the covariance representation.
- **`reporting/`** — deterministic evidence-labelled LaTeX; labels are tied to
  the verification layers, and the template verbs follow the label.
- **`mcp_server/`, `web/`** — external surfaces. Numeric/enum inputs only; no
  expression text crosses the boundary (so nothing reaches `sympify`); not
  hosted by the project.

The bridges between the middle-tier modules are **one-way**: discovery and
decomposition are independent; `dipoles → algebra` only; the Symmetry-general
dipole module does not touch the PRB module (M36); the ensemble module is
separate (M37). Cross-module physical consistency is enforced by permanent
sentinel tests.

## Design decisions (M-series) and strict rules (K-series)

Each stage records its decisions (`M`) and non-negotiable rules (`K`) in its
`specs/stage-NN.md`; retrospectives collate them per phase
([`phase-c-retrospective.md`](phase-c-retrospective.md),
[`phase-d-retrospective.md`](phase-d-retrospective.md)). Index of the
load-bearing ones:

| Key | Summary |
|---|---|
| M7 | Known-identity keys are frozen; the library only grows. |
| M15 | Fingerprints are a heuristic bucket, never a proof. |
| M18 | No large shared e-graph — isolated per-pair proof graphs (egglog congruence pathology). |
| M19 | `underivable` candidates require exact symbolic certification. |
| M28 | Decomposition equations are *derived* from rank-1 minors, never transcribed. |
| M29 | Standard-basis covariance ≠ Π-basis covariance; never mixed. |
| M30 | OCR/print unreliability: anchor entries carry print-artifact notes (eight diagnoses to date). |
| M31 | Composite decomposition lives in a separate module. |
| M32 | Guarded (Horn-conditional) finding = the four-part evidence quadruple. |
| M33 | Rank-3 solver is one-way layered onto the rank-2 solver; no a/b variants yet. |
| M34 | Beyond-paper zones (no table to anchor) use a three-layer substitute: probe-verified hand derivation + deriver match + independent reviewer. |
| M35 | `dipoles → algebra.HVector` is the only bridge out of the dipole layer. |
| M36 | Symmetry-general dipole module does not touch the PRB module (sentinel-tested). |
| M37 | Ensemble module is separate; `gamma_paper = 2 × HVector.gamma` (naming guard). |
| K9/K10 | The discovery engine is never the sole verifier; candidates re-checked symbolically. |
| K19 | Recovery/boundary features are keyed (interpreted_scalars, guarded_atoms, dagger, …). |
| K21 | Nothing is silently dropped: skips/failures carry reasons in artifacts. |
| K24 | A new rewrite rule requires a soundness analysis + reviewer approval. |
| K26 | No wrong-but-plausible output: every inapplicable configuration raises with a reason. |
| K28 | Paper-table anchors are entered by hand and compared by exact symbolic zero. |
| K29/K31 | Minor selections carry structural (and order-aware) guards; violations raise. |
| K32 | Overdetermination consistency checks are mandatory (e.g. rank-3 {2,3} `k₂+e₃=σ`). |
| K33 | PDF-based anchors cite equation numbers with print-artifact notes; homonym-different-object naming warnings. |

## Security boundary

External input never reaches `sympy.sympify` (which routes through `eval`).
`safe_parse.safe_parse_srepr` parses serialized expressions with an `ast`-walk
over a whitelist and rejects everything outside a restricted grammar
(injection, attribute access, magnitude/DoS bombs, non-finite values). The MCP
tools accept numbers and enum strings only. See
[`VERIFICATION.md`](VERIFICATION.md) and `tests/test_security.py`.
