# STAGE 1 — Library Expansion + Serialization + egglog Spike

**Date**: 2026-07-13
**Previous stage**: stage-00 (representation layer + 14 identities, 36/36 green)

---

## 1. Context

Stage 0 laid the ground. This stage advances on three fronts: (a) the identity library
expands with identities from PRA 95,063819 (coherent superposition) and JOSA A 34,80 /
Appl. Opt. 55,2543 (symmetry classes); (b) the MCP-preparation serialization layer
(decision M4) is written; (c) the egglog discovery-engine candidate is tried out with a
time-boxed spike — the findings of this spike will shape the Stage 2 spec.

## 2. Goals

1. Seven new identities (I15–I21), with source + condition metadata, bound to regression.
2. `serialize.py`: HVector JSON round-trip (SymPy srepr based), JSON dump of library
   metadata, LaTeX generation helpers.
3. egglog spike: setup + modeling of the quaternion unit-algebra fragment with equality
   saturation; findings in `docs/egglog-spike.md`.
4. `docs/ROADMAP.md`: frozen-N draft (to be frozen at the end of Stage 2).

## 3. Architectural decisions

- **M7. Library growth is backward-immutable**: the keys and checks of I1–I14 are FROZEN;
  new identities are only added (the library counterpart of the v1 engine-stability
  principle).
- **M8. Serialization via srepr**: SymPy expressions are carried as an `srepr` string
  (lossless); JSON schema {"tau": srepr, ...}. NO `eval` —
  `sympy.parsing.sympy_parser` not, `sympy.sympify(..., no strict)` instead of
  `sp.parse_expr`? No: srepr restoration is done with `sympy.sympify`
  (srepr output is considered safe for sympify; validation of external input is the job of
  the MCP stage, noted here).
- **M9. The spike does not leak into production code**: the egglog trial stays separately
  under `spikes/`, takes no `src/` dependency; egglog is NOT ADDED to pyproject.

## 4. Strict rules

- K6. Stage 0 API signatures do not change (only additions).
- K7. M2 discipline in the new identities too: symbolic priority, seed in the numerical.
- K8. Spike time is limited; if there is a blockage in egglog it is written as a finding,
  the stage is not blocked.

## 5. Deliverable

- `src/organon_mueller/identities/known.py`: I15–I21 added.
- `src/organon_mueller/serialize.py` + `tests/test_serialize.py`
- `tests/test_fixtures.py`: synthetic-QWP superposition fixture.
- `spikes/egglog_quaternion.py` + `docs/egglog-spike.md`
- `docs/ROADMAP.md`
- `reports/stage-01-REPORT.md`, README status table up to date.

## 6. Verification

| # | Identity | Source | Condition | Mode |
|---|---|---|---|---|
| I15 | Z=aZ_a+bZ_b ⇒ M=|a|²M_a+|b|²M_b+(ab*Z_aZ_b*+a*bZ_bZ_a*); cross term real | PRA 95,063819 Eq.(10) | coherent | symbolic |
| I16 | Z_b=e^{iφ}Z_a, a=b=1/√2 ⇒ M=M_a(1+cosφ) | PRA Eq.(25-26) | coherent | symbolic |
| I17 | Covariance map linear: H(ΣwᵢMᵢ)=ΣwᵢHᵢ; convex mixture rank-2 + trace-condition violation | Cloude 1986; Gil | depolarizing | symbolic+numerical |
| I18 | (1+i)/2·pol_H + (1−i)/2·pol_V superposition = QWP state, M as expected | PRA Eq.(15) | coherent | symbolic |
| I19 | (τ,α,0,0) generator ⇒ Type-1 block-diagonal M symmetry | JOSA A Eq.(31); AO Eq.(7) | class2_ta | symbolic |
| I20 | (τ,0,β,0) generator ⇒ Type-2 M symmetry | JOSA A Eq.(31); AO Eq.(8) | class2_tb | symbolic |
| I21 | (τ,0,0,γ) generator ⇒ Type-3 M symmetry | JOSA A Eq.(31); AO Eq.(9) | class2_tg | symbolic |

Serialization: round-trip generic + random numerical; JSON schema validity.
Spike acceptance: the quaternion unit relations (ij=k, i²=−1, ...) are saturated in the
e-graph and the derivation i·j·k ≡ −1 is shown, OR the obstacle is reported.

## 7. Delivery format

To the user's `C:\Projects\organon-mueller` clone together with Stage 0;
if the bridge is closed, zip + automatic retry.

## 8. Special warnings

1. The reality proof of I15 relies on the I10 commutation — verify it in the test with an
   independent expand, do not build a call chain to I10.
2. In the symmetry generators, explicitly list the "must be zero" entries (pattern test),
   not just "equality".
3. Float precision in the srepr→sympify round-trip: `Float(x, precision)` is preserved; in
   the test use srepr-equality instead of exact equality.
4. The egglog Python API is evolving fast; write the version into the spike report.

## 9. Out of scope

- The discovery engine itself (Stage 2+, according to spike findings)
- Decomposition deriver, dipole module
- MCP server implementation (only serialization preparation)
- General rank-3/4 decompositions for depolarizing H

**STOP HERE**
