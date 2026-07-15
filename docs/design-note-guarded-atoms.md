# Design Note — Conditional Atom Classes (guarded_atoms; implementation A9+)

Source requirement: `docs/term-language-extensions.md` priority 2 — the I4,
I12, I13, I19-I21 family and the discovery-side connection of the Phase C
decomposition deriver.

## Principle: guards are NOT AXIOMS, they enter the INTERPRETATION layer

A direct consequence of the stage-2/3/7 soundness lessons: every new e-graph
rule is an unsound-merge risk and demands a K24 process. For guarded atoms
this is NOT NEEDED — the constraint is placed on the atom's GENERATOR:

```
GuardedAtom(name, guard)   guard ∈ CONDITIONS keys
                           (hermitian_state, unitary_state, class2_ta, ...)
interpretation (numeric):  constrained random HVector (e.g. hermitian: real parameters)
interpretation (symbolic): constrained generic parameters (e.g. tau real, alpha real, ...)
e-graph:                   like an atom — NO extra rule at all
```

## Discovery semantics (the real payoff)

When a pair of guarded atoms passes through the three layers, its meaning is:
"identity UNDER the guard condition" — i.e. a Horn-conditional identity:
`hermitian(a) → t₁(a) = t₂(a)`.

- Since the e-graph does not know the guards, these pairs typically remain
  UNPROVEN → they fall into the `underivable` channel **with a guard label** =
  exactly the conditional-identity CANDIDATES we are looking for. (The channel
  has been empty to date — the first candidates are expected from here; the
  novelty-protocol chain is applied unchanged.)
- The symbolic layer automatically applies the guard with constrained
  parameters (the exact proof becomes "under the condition"); the numeric layer
  with constrained sampling.
- Optional forward step (a separate K24 round): compiling frequently-verified
  guarded-equivalence families into guard-specific GROUND rules (e.g. a·conj(a)
  relations for hermitian a) — but only with auditor soundness approval.

## Decomposition bridge (Phase C)

AO2016 Type 1/2/3 pure states = the covariance face of the guarded atom
classes. The A9+ target: a discovery scan with `class2_*` guarded atoms makes
the symmetry templates of the decomposition deriver visible from the discovery
side too (e.g. in pairs with type-1 atoms, M-symmetry patterns should surface
on their own as underivable candidates — the discovery-face of I19-I21).

## Fingerprint and seeds

Guarded generators use a separate seed space (K14 extends); the bucket key is
unchanged (scale-relative). Sampling adequacy per guard (risk of a false
positive in degenerate subspaces: e.g. in the tau=0 class some expressions may
look identical) → the symbolic-exact layer remains mandatory (M19 unchanged).

## Forward obligations (stage-8 auditor addendum)

1. **Generator fidelity**: each guard's symbolic parametrization must be
   GENERIC and faithful for its own class — otherwise the scope of the
   "guard → identity" ruling becomes an over-claim. (In today's undivided
   language, generic-true ⇒ whole-class-true: the polynomial identity theorem;
   including measure-zero layers like τ=0.)
2. **Denominator obligation**: when `interpreted_scalars` (values of the
   1/det kind) arrive, sympy simplification's silent ≠0 assumptions must be
   written as an ADDITIONAL guard component of the certified Horn identities
   (the `det_nonzero` key in CONDITIONS is exactly for this).

## Acceptance draft (input to the A9 spec)

1. GuardedAtom node + constrained generators (hermitian, unitary, class2_ta/tb/tg).
2. Campaign: the guarded-pair counterparts of I12/I13 pass through the three
   layers (with the criterion "symbolic-exact under the guard" instead of an
   e-graph proof — the classification scheme reports this distinction).
3. Scan: in a 2-guarded-atom configuration, the FIRST non-empty output of the
   underivable channel is expected; it flows into the novelty-protocol, NO
   CLAIM is produced.

## Second-half closure — negative result (stage 20)

The deferred "second half" (hermitian/unitary guarded campaigns) was
resolved by a pre-implementation probe
(`probes/probe-guarded-hermitian-unitary.py`, seed 20260713): a scan of
all size-≤4 `Mul`/`Conj` term pairs over two guarded atoms found **no**
enumeration-reachable Horn-conditional identity in either the
`hermitian_state` or `unitary_state` class (the `class2` control
reproduces the known commutation finding).

This is the theory-consistent outcome, not a gap. A hermitian state
(`|h⟩` real) or a unitary state (`|h⟩` = τ real + imaginary vector part)
constrains the covariance-vector COMPONENTS; but the algebraic facts that
distinguish a hermitian/unitary MATRIX (`Z = Z†`, `Z Z† = I`) are
*dagger* properties, and stage-7 proved the transpose/dagger is
inexpressible in this elementwise-conjugation term language. No dagger
property can surface as a term identity, so these guarded classes have an
empty reachable Horn channel. Recorded here per K21 (an empty channel is
a first-class result) and locked by
`tests/test_guarded_atoms.py::test_no_reachable_horn_identity_in_hermitian_unitary`.
