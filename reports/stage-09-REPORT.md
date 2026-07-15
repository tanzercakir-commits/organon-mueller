# STAGE 9 — REPORT (Phase C: Composite Symmetries + Guarded Atoms First Half)

**Date**: 2026-07-13 · **Spec**: `specs/stage-09.md` · **Mode**: autonomous
**Result**: COMPLETED — 126/126 tests green; **composite types (1-2, 1-3, 2-3)
derived by a three-parameter ordered-minor solution and matched Table 4
symbolically verbatim 3/3**; the FIRST filled output of the `underivable`
channel was produced (three Horn-conditional identities, with M32 quadruple proof).

---

## 1. Deliverables

### (a) `decomposition/composite.py` — composite types (M31: separate module)
- **Templates (Table 3)**: three primaries {x, g, h} — center in 1-2/1-3
  x=α₁B + α₁G, α₁H; corner in 2-3 x=α₁A + α₁G\*, α₁H\*; dependents from rank-1
  relations (AB=GG\*, GH\*=MB, BC=HH\* / 2-3: AB=GG\*, HG\*=AY, AC=HH\*).
- **Ordered minor derivation** (M28 discipline continues): the x-minor solved without g/h,
  then the g-minor (linear, conj(g)-free, h-free), then the h-minor; every structural
  violation throws (K29). **Exact symbolic zero** against the Table-4 anchors (K28).
- **`decompose_composite`**: K26 guards — rank-2, denominator~0 (missing-type
  anisotropy/overlap), primary real+positive, α₁∈(0,1), H₂ PSD + rank-1,
  **trace-1 convention guard** (below).

### (b) `discovery/guards.py` — guarded atoms (first half of the design note)
- `GuardedAtom(name, guard)`: an `Atom` subclass — the e-graph and axioms
  do NOT SEE the guard (zero soundness cost, K24 untouched); `provable()` thus becomes
  the very question "is it derivable without the guard".
- Restricted generators (K30: the restriction enters by parameter construction, no assumption
  injection): hermitian → 4 real; unitary → τ real + imaginary vector;
  class2_ta/tb/tg → (τ,α,0,0)/(τ,0,β,0)/(τ,0,0,γ). Numeric + symbolic.
- `_validated_guards` (post-audit): the guards dictionary is cross-verified against the
  embedded labels in the terms — a mislabeled dictionary cannot silently produce a Horn
  proof, it throws.

## 2. Verification results

- **Table 4**: 3/3 types symbolically verbatim (`sp.simplify(difference) == 0`).
- **Roundtrip**: 3 types × 3 deterministic examples, exact recovery
  (α₁ ~1e-8, H's ~1e-7; reviewer observed ~1e-15).
- **Guarded campaign (M32 quadruple proof)**: three findings — class2_ta ({1,i}),
  class2_tb ({1,j}, added by audit suggestion 2), class2_tg ({1,k}):
  guarded symbolic-EXACT ✓ · guarded numeric ✓ · e-graph proof ✗ ·
  unguarded symbolic ✗ → `is_conditional_identity` correct in all three.
  The mixed guard (ta×tg) negative control does not change ✓. **These are known
  facts** (the {1,q} planes of the quaternion are commutative) — the goal was proof of the
  channel mechanism, there is NO CLAIM of novelty (protocol unchanged).
- **Degenerate guards**: same-symmetry mixture rejected by denominator collapse in all three
  composite types (parametrized test, audit suggestion 3); rank≠2
  explicit error.
- Old 110 tests + new 16 = **126/126 green** (py3.12 local; CI matrix
  runs on push).

## 3. Spec correction — probe win BEFORE implementation

The first draft target `unitary(a) → (a·conj(a))·b ≡ b·(a·conj(a))` came out WRONG in the
numeric probe and was recorded into the spec with a retraction note: elementwise
conj ≠ dagger (hh†=1 requires the quaternion-Hermitian conjugate; ZZ\* is a retarder
Mueller, not scalar·I — consistent with stage-7's "dagger is inexpressible in the
language" theorem). Lesson: **a numeric probe is mandatory before campaign targets are
written into the spec** — the wrong target was eliminated without touching the code at all.

## 4. Independent audit

Verdict: **PASS** (2 document-level defects + 3 suggestions — all applied):
- D1: the mixed y-interpretation in the composite.py 2-3 template was fixed
  (Y\* = H\*G/A → the scaled h·conj(g)/x chain written out explicitly).
- D2: the spec's "guard ∈ CONDITIONS keys" statement was fixed —
  GUARD_KEYS EXTENDS CONDITIONS with class2_ta/tb/tg.
- Suggestion 1 → the **trace-1 convention guard** was added both to `decompose_composite` and
  (same hazard by inheritance) to stage-8 `decompose`: a scaled covariance would silently
  return a scaled α₁ (would be a K26 violation).
- Suggestion 2 → class2_tb added to the campaign (three planes, full symmetry).
- Suggestion 3 → the missing-anisotropy test parametrized over the three types.
- The reviewer's guard-dictionary concern → the `_validated_guards` cross-check.

Reviewer note (documented): when a composite-symmetric H₁ is mixed with a second
component of ANOTHER type, the cross-type solution may also give a physically valid
alternative decomposition — no uniqueness claim, and the paper does not make one either; the
result returned to the user carries the `symmetry` label explicitly.

## 5. A10 groundwork (bridge to rank-3)

For rank-3 the remaining object is H − α₁H₁ₛ − α₂H₂ₛ; the minors of the two symmetric
components can be solved IN ORDER (this stage's three-unknown ordered mechanism
generalizes verbatim). Fingerprint→minor bridge: the discovery engine's buckets
propose the candidate symmetry class, the minor machine solves exactly. **Stage 10 =
rank-3 discovery sweep** — a publication-candidate region (Kuntman-Arteaga did not
sweep rank-3 systematically); step 5 of the novelty protocol (human approval) applies.

## 6. Next stage (autonomous continuation)

**Stage 10 — Rank-3 decomposition + discovery sweep**: three-term decomposition
(2 symmetric + 1 generic pure), ordered-minor generalization, synthetic
roundtrips, degenerate guards; the first bridge with the discovery engine (proposing a
symmetry candidate from fingerprint buckets).
