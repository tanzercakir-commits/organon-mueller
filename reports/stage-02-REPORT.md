# STAGE 2 — REPORT

**Date**: 2026-07-13
**Spec**: `specs/stage-02.md`
**Result**: COMPLETED — 56/56 tests green; the engine rediscovered known structure on its
own; 100% of the harvested candidates passed independent verification;
**FROZEN-22 declared**.
**Mode**: Autonomous execution from this stage on (user mandate 2026-07-13);
trust anchor `docs/VERIFICATION.md`.

---

## 1. Deliverables

- **`discovery/` package (hybrid engine v0)**:
  - `terms.py`: abstract term language (Atom/Mul/Conj), deterministic enumeration.
  - `axioms.py`: egglog rule set — associativity (both directions), conj involution,
    **order-preserving** conj distribution ((AB)\*=A\*B\*), I10 commutation **only at
    the atom level** (soundness boundary; the free-variable form is unsound —
    rationale in the module docstring, with a numerical counterexample).
  - `interpret.py`: term → concrete Z-matrix value (SymPy/NumPy); numerical equivalence test
    independent of the engine.
  - `engine.py`: enumerate → saturate → harvest (extract-grouping + check-confirmation)
    → verify pipeline; `DiscoveryResult(sound, verified, refuted,
    extraction_collisions, ...)`. K9/K10: an unverifiable candidate is not silently eliminated,
    it breaks the build.
- `docs/VERIFICATION.md`: 6-layer verification contract + honest boundaries.
- `docs/ROADMAP.md`: **FROZEN-22** (6 phases, 22 stages — now immutable).
- pyproject `[discovery]` extra (egglog>=13); CI `.[test,discovery]`.

## 2. Verification results

- Suite: **56/56 green** (~32 s; on an egglog-less install the discovery tests are
  skipped cleanly).
- **Rediscovery acceptance** (size-9 saturation, 5698 terms, 0.15 s):
  R1 conj-involution ✅ · R2 a·conj(b)≡conj(b)·a ✅ · R3 serial Mueller product
  (a·b)·conj(a·b) ≡ (a·conj(a))·(b·conj(b)) ✅
- **Negative controls**: a·b ≢ b·a ✅ · conj(a)·conj(b) ≢ conj(b)·conj(a) ✅
  (saturation does not "invent" commutativity; both are also genuinely unequal numerically)
- **Full harvest** (size 7): 570 terms → 64 e-classes → **506 candidate pairs, 506/506
  verified, 0 refuted, 0 extraction collisions**.

## 3. Independent audit

Verdict: **PASS**. The auditor, with a different seed (seed 7): confirmed the soundness boundary in both
directions numerically (the free rule was refuted 20/20; the atom rule
passed 20/20), re-verified the 506 pairs (0 errors), and also verified the pairwise
DISTINCTNESS of the 64 class anchors (the engine neither over-merges nor — at this
size — under-merges). Three of its suggestions were applied:

| Suggestion | Action |
|---|---|
| `equivalent` was swallowing a generic Exception | ✅ only `EggSmolError` is caught; an operational error can no longer masquerade as "not equal" |
| The defensive-split was invisible | ✅ `extraction_collisions` counter + zero guarantee in test |
| The axioms docstring's derivability statement was missing | ✅ corrected to "assoc + conj distribution" |

## 4. Decisions

1. **FROZEN-22** declaration (decision M14) — a change only with a critical-decision note.
2. The hybrid boundary (M10) is a permanent architectural principle: egglog is never the sole verifier.
3. Loss of completeness is a deliberate choice: the engine may find too few but
   cannot find wrong ones — the spec guarantees only soundness.
4. Correction record: the dimension-arithmetic error in the spec's first draft (R3
   terms are 8/9, not "7") was explicitly corrected inside the spec.

## 5. Next stage (autonomous continuation)

**Stage 3 — Term enumeration + complexity bounds (Phase B)**: atom count
and size scaling strategy, optimization of the extract bottleneck (21 s @ size 9),
design note for scalar placeholders.
