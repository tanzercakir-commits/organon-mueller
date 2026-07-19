# wordalgebra — a general matrix-word identity solver (spec 01)

**Date**: 2026-07-18 · **Branch**: `feature/wordalgebra-solver` (off main,
merged only via a reviewed PR) · **Mode**: multi-phase, test-and-guard
discipline, quality over speed.

## 1. Why

The collaborator's briefs (TANZER_1, TANZER_2) are two instances of ONE
shape: *identity checking/discovery over a matrix word-algebra*. Today
each new brief needs bespoke hand-written code. The engine already has
the parts (enumeration, numeric-screen → symbolic-proof, coefficient
extraction, evidence discipline) but they are wired to specific
algebras. This module lifts them into a general, parametrized solver so
that a brief becomes a **specification fed to the engine**, not new code.

Success test (the whole point): the general solver must re-solve BOTH
TANZER_1 and TANZER_2 from a spec alone, reproducing the hand-derived
results exactly — backward validation.

## 2. The problem shape it covers (scope — deliberately bounded)

A brief is: a fixed **basis** $B^0,\dots,B^{d-1}$ (the "middle" family,
e.g. $\Sigma^\mu$); a parametrized **generator** $Z(\alpha)$ (e.g.
$Z=\alpha_\mu B^\mu$); a set of unary **operations**
$\{\text{id},*,{}^T,\dagger,{}^{-1}\}$ that build the **alphabet** of
letters $\{Z,Z^*,Z^T,Z^\dagger,Z^{-1},\dots\}$; an optional polynomial
**constraint** on the parameters (e.g. $\alpha\!\cdot\!\alpha=1$); and a
**query**: for words $A,B$ over the alphabet and middle $\mathrm{mid}$
in the basis, classify the sandwich

$$A\,\mathrm{mid}^\mu\,B \;=\; C^\mu_{\;\nu}\,\mathrm{mid}^\nu$$

by its coefficient matrix $C$ — is it $I$ (an identity $=\mathrm{mid}$),
a scalar multiple, a named matrix ($\Lambda$-type), or does the sandwich
not expand in the basis at all?

Out of scope for spec 01 (possible later): word depth > 1 beyond a
capped product set; non-matrix coefficients; bases without a
well-defined expansion.

## 3. Architecture (new, framing-neutral package)

`src/organon_mueller/wordalgebra/` — carries NO Λ/Σ̄/Mueller framing;
the specific problems are spec instances, not baked in.

```
wordalgebra/
  spec.py       BriefSpec (basis, generator, n_params, operations,
                constraint, middles, query); validation with K26 reasons
  alphabet.py   build the labelled alphabet from generator + operations
                (id, conj, T, dagger, inv), inverse via a supplied rule
  expand.py     express a matrix in the basis: trace-orthogonal
                extraction when tr(B^i B^j) is diagonal, else a Gram
                linear solve; residual test => "no expansion"
  solve.py      enumerate alphabet x alphabet x middles; numeric screen
                on the constraint surface (sampled); symbolic
                certification of survivors; classify C; result table
  report.py     deterministic, evidence-labelled table generator
                (GENERATED, never hand-typed — the L3/UI-3 lesson)
```

Reuse: the verified `lorentz.core.SIGMA` is available as a ready basis
for the TANZER specs (its equality to the collaborator's Σ is already a
theorem), but the solver itself takes ANY basis.

## 4. Method (per candidate sandwich)

1. **Numeric screen** on the constraint surface: sample parameter
   points satisfying the constraint (constructed, not rejection-sampled),
   build matrices, test the query to tolerance at ≥2 independent points.
2. **Symbolic certification**: for survivors, prove exactly (expand ==
   0, or reduce modulo the constraint ideal); for the rest, a numeric
   counterexample on the surface is a rigorous disproof.
3. **Coefficient extraction**: $C^\mu_{\;\nu}$ via trace-orthogonality
   (if the basis is trace-orthogonal) or a Gram solve; a nonzero
   residual after projection ⇒ "no expansion" (certified).
4. **Classify** $C$: identity $I$; scalar$\cdot I$ (report the scalar);
   a supplied named target (e.g. $\Lambda$); else "expands, other".

## 5. Backward-validation targets (acceptance heart)

- **TANZER_2 spec**: basis Σ, $Z=\alpha_\mu\Sigma^\mu$, constraint
  $\alpha\!\cdot\!\alpha=1$, operations $\{$id,*,T,†,inv$\}$, query
  "$C=I$". The solver must return EXACTLY the four identities and the
  Σ-built / transpose-built family split — cross-checked cell-for-cell
  against the hand-derived `studies/tanzer2` result (which stays on its
  own branch; the values are re-encoded in the test).
- **TANZER_1 spec**: same basis/generator, generic α (no constraint or
  $\alpha\!\cdot\!\alpha=1$ as given), query allowing a **matrix**
  coefficient — the solver must reproduce the five given identities,
  including the Λ-type $Z^\dagger\Sigma^\mu Z=\Lambda^\mu_{\;\nu}
  \Sigma^\nu$ (C = a nontrivial matrix), and the sandwich ones.

If the solver reproduces both from specs alone, generality is proven by
construction.

## 6. Discipline

Every phase: probe (for any new mechanism) → impl → test → adversarial
review by the SAME reviewer → fix → next. `studies/`-style isolation is
NOT used here — this is a first-class library module, so it lives in the
package and IS part of the suite and its count/guards. K26 on every
malformed-spec path. No hand-typed tables. main untouched until a
reviewed PR; at push time, `git diff --stat main..branch` is checked so
only wordalgebra files ship (the cross-branch-contamination lesson).

## 7. Acceptance

All phases green; both TANZER specs reproduced from spec alone;
full suite + guards green with updated counts; adversarial review PASS;
the collaborator's TANZER_2 re-solved end-to-end by the engine and
checked against the hand-derived answer. Version bump decided at PR
time (new public capability ⇒ minor).

**STOP after each phase for a quota/quality check is NOT required here
(user: "acele yok, kalite amaç") — proceed phase to phase, but keep each
phase reviewed before building on it.**
