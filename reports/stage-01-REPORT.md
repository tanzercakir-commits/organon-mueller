# STAGE 1 — REPORT

**Date**: 2026-07-13
**Spec**: `specs/stage-01.md`
**Result**: COMPLETED — 49/49 tests green, library at 21 identities (21/21 recovered), egglog spike SUCCESSFUL

---

## 1. Deliverables

- **Seven new identities (I15–I21)** — I1–I14 frozen (decision M7), additions only:
  - I15: coherent superposition expansion + reality of the cross term (PRA Eq. 10)
  - I16: interference analog M = M_a(1+cosφ) (PRA Eq. 25-26)
  - I17: linearity of the covariance map + depolarization of the mixture (rank 2)
  - I18: "artificial quarter-wave plate" superposition → real QWP Mueller (PRA Eq. 15)
  - I19–I21: (τ,α,0,0)/(τ,0,β,0)/(τ,0,0,γ) generators → Type-1/2/3 M symmetries,
    **full literature pattern**: zero positions + (anti)symmetric pairs + diagonal
    equalities + quadratic relation (e.g. M01²+M22²+M23² = M00²)
- **Serialization layer** (`serialize.py`): HVector JSON round-trip (srepr,
  lossless — symbols, exact rationals, Floats preserved), library
  metadata JSON dump, LaTeX helpers. MCP preparation (decisions M4/M8).
- **egglog spike** (`spikes/egglog_quaternion.py` + `docs/egglog-spike.md`):
  egglog-python 13.2.0; the quaternion unit algebra was saturated WITHOUT a
  commutativity axiom; 4 equivalences including i·j·k≡−1 were derived. **Stage 2 proposal: hybrid
  architecture** (egglog = term-structure equivalence, SymPy = coefficient verification).
- **`docs/ROADMAP.md`**: ~22-stage, 6-phase draft (frozen-N declaration at the end of Stage 2).
- README status table updated.

## 2. Verification

- `pytest`: **49/49 green**. `verify_all()`: **21/21**.
- CI matrix unchanged (3.10/3.11/3.12) — will run on push.

## 3. Independent audit (focused, Stage-1 diff only)

Verdict: **PASS**. The auditor verified I18 from scratch via an independent route (M_ij = ½tr(σᵢJσⱼJ†),
without using the package machinery); I20 at 50 random parameters via the same independent
route; added its own negative controls to the spike (i·j ≢ j·i is preserved —
saturation does not "invent" commutativity). Findings and actions taken:

| Finding | Action |
|---|---|
| I19–I21 verified a subset of the literature pattern (diagonal + quadratic missing) | ✅ completed — the pattern is now the whole of AO Eq. (7)-(9) |
| I15 expansion leg is a tautology from bilinearity; the load-bearing leg is reality | ✅ recorded in the registry statement (so it does not enter the discovery engine's "found" counter) |
| I17 symbolic leg is a tautology by construction | ✅ recorded in the statement |
| `sympify` injection surface (auditor ran `__import__`) | ✅ fixed in the module docstring as a **STAGE-2 GATE**: before the external surface is opened, a restricted parser + rejection test are mandatory |

## 4. Decisions and open questions

1. **Hybrid discovery architecture** (egglog structure / SymPy coefficient) — proposed as the
   basis of the Stage 2 spec; approval in the Stage 2 spec.
2. egglog did not enter pyproject (decision M9); planned as a `[discovery]` extra in Stage 2.
3. LICENSE still open (user decision).
4. Stage 0's open question (τ=0 classes) stands; to be addressed in the discovery engine design.

## 5. Next stage proposal

**Stage 2 — Discovery engine core v0**: hybrid egglog+SymPy architecture; Z-algebra
term language (product + conjugate + scalar placeholders), canonical form/extraction,
first enumeration at a small complexity bound; acceptance criterion: the engine rediscovering, on its own, structural
identities like I1/I8/I10. At the end, the **frozen-N declaration**.

## 6. Proposed commit (Stage 0 + 1 together, first push)

```
git add -A
git commit -m "Stage 0-1: representation layer, 21-identity regression library, serialization, egglog spike

Stage 0: six isomorphic representations (J, M, H, |h>, Z, biquaternion),
known-identity regression core, condition predicates, literature fixtures, CI.
Stage 1: coherent-superposition and symmetry-class identities (full literature
patterns), JSON/LaTeX serialization layer, successful egglog feasibility spike
(noncommutative quaternion fragment), staged roadmap draft.
Both stages independently reviewed (adversarial PASS)."
git push
```
