# egglog Spike Findings (Stage 1)

**Date**: 2026-07-13 · **egglog-python**: 13.2.0 · **Result**: SUCCESS

## What was tried

The non-commutative skeleton of the Stokes-Mueller formalism — the quaternion
unit algebra {1, i, j, k} + negation — was modeled with rewrite rules in an
egglog e-graph (`spikes/egglog_quaternion.py`). The commutativity axiom was
deliberately NOT GIVEN; the Hamilton relations (i²=j²=k²=−1, ij=k, ji=−k, ...)
+ two-way associativity + centrality of negation were entered as rules.

After saturation, four equivalences were verified with `check`:

| Query | Result |
|---|---|
| i·j·k ≡ −1 | PASS |
| (i·j)·(j·k) ≡ j | PASS |
| k·(k·k) ≡ −k | PASS |
| (j·i)·k ≡ 1 | PASS |

## Findings

1. **Non-commutative product is natural**: it is obtained by not giving a rule;
   the e-graph keeps all parenthesizations in a single equivalence class. There
   is NO fundamental obstacle to v2's Z-matrix / quaternion products.
2. **Scalar (complex) coefficients are not yet modeled** — this is the real
   open question. Two options: (a) embedding the coefficients into egglog as
   rational pairs (re, im), (b) a **hybrid architecture**: egglog only for
   term-structure equivalence (structural equivalence), with coefficient
   arithmetic and verification in SymPy.
   **Recommendation: (b) hybrid** — it does not push the float/complex
   correctness risk into the e-graph, and reuses Stage 0-1's SymPy verification
   pipeline as is.
3. **API notes**: `vars_("a b c", Q)` in a single call; a single-name `vars_`
   returns a generator (a trap). Rule scheduling is `ruleset(...)` +
   `egraph.run(rs.saturate())`; the equivalence test is `egraph.check(eq(l).to(r))`.
4. **Scale**: this fragment saturates in milliseconds. The real discovery load
   (term enumeration × canonical form) is Stage 2's measurement subject.

## Inputs to Stage 2

- If the hybrid architecture is accepted: the abstract term algebra on the
  egglog side (Z-product, conjugate `conj` unary, `mueller(z) = z * conj(z)`
  embedding), parameter-level verification on the SymPy side.
- Extraction (smallest term) should be tried for canonical form generation.
- A candidate identity = syntactically distinct term pairs that land in the
  same e-class after saturation; the complexity bound is applied in
  enumeration.
- egglog was NOT a pyproject dependency (decision M9); in Stage 2 it can be
  added as a `discovery` extra: `pip install organon-mueller[discovery]`.
