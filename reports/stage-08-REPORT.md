# STAGE 8 — REPORT (Phase C opening: Symmetry-Conditional Decomposition Deriver v0)

**Date**: 2026-07-13 · **Spec**: `specs/stage-08.md` · **Mode**: autonomous
**Result**: COMPLETED — 110/110 tests green; **the engine ITSELF derived
the entire set of six equations of AO2016 Table 2 from rank-1 minor conditions and
matched the paper symbolically verbatim**; the paper's §6 numerical example was
reproduced at print precision.

---

## 1. Deliverables (`decomposition/` package)

- **`covariance.py`**: AO2016-convention covariance H↔M + Type 1/2/3
  templates (Table 1, primary outer/center parametrization).
  **Convention finding → THEOREM**: reading the paper's Eq. (2) literally as a kron
  yields a non-PSD cousin; the true H is its index
  reshuffle, and the reviewer PROVED the identity R(σᵢ⊗σⱼ)=σᵢ⊗σⱼ\* — meaning
  the paper's H is the standard Cloude/Gil covariance (conjugate dropped in print).
- **`derive.py` (M28)**: the equations are NOT COPIED from the table — over a generic Hermitian
  H, selected 2×2 minors of the remainder (H − α₁H₁ₛ) are solved with SymPy;
  structural guards (the x-minor cannot touch w; the w-minor is conj-free) throw on violation.
  All six of the six variants matched the hand-entered Table-2 anchors with
  **exact symbolic zero** difference (K28).
- **`solve.py`**: numerical solver — rank-2/denominator/α₁∈(0,1)/PSD/rank-1
  guards (K26: no silent wrong result); `variant="auto"` orders by the paper's
  numerical recommendation (large |denominator| first); tolerance parameters
  (exact data: strict default; 4-decimal literature data: loose).

## 2. Verification results

- **A**: 6/6 variants symbolically verbatim (2b/3b "overbar" reading confirmed by the reviewer's
  independent derivation + the paper's own Eq. (20) label; 3a
  conjugate-sided — anchor interpretations documented in the test file).
- **B (paper §6 anchor)**: α₁=0.3000; α₁E=0.1433; α₁V=0.0289+0.0112i;
  α₁Ē=0.0067; H₁ entries 0.4777/0.0962+0.0372i; M₁ and M₂ recovered
  at ~1e-3 (4-decimal print noise). **Two print errors diagnosed**
  (Eq. 17 h03: 0.0161→0.1608; Eq. 21 [1,3]): via self-consistency with the paper's
  OWN derived values — 0.0161 does not fit any consistent reconstruction.
- **C**: synthetic exact roundtrip 3 types × 2 variants (reviewer with a different seed:
  5×6 repeats: worst error 1.1e-15).
- **D**: same-symmetry overlap and rank≠2 rejected with an explicit error;
  in the near-degenerate sweep (ε→1e-8) no silent garbage — exact down to ε=1e-4,
  below which the guard engages with a message.
- Basis-separation sentinel: standard and Π covariances cannot be mixed (M29).

## 3. Independent audit

Verdict: **PASS** (3 document-level defects — fixed: the auto-variant
contract was actually implemented per the paper's recommendation; the convention
docstring upgraded from "empirical" to "proven" + a print-error note;
2b/3b overbar justification moved into the test file). The reviewer's own
derivations: the reshuffle theorem, the independent SymPy solution of the six variants,
the symbolically exact recovery of α₁=2/7 in fully-rational roundtrips.

## 4. guarded_atoms design (A9 input)

`docs/design-note-guarded-atoms.md`: guards enter the interpretation layer, NOT the
axiom (zero soundness cost, K24 untouched); guarded-true-but-
unproven pairs fall into the `underivable` channel with a guard label = Horn-conditional
identity candidates (the channel's FIRST filled output is expected here). The reviewer
closed the τ=0 type measure-zero class concern (in a division-free language the polynomial
identity theorem suffices) and added two forward-looking obligations (generator
fidelity; when interpreted_scalars arrives, denominator side-conditions must be written into the guard).

## 5. Next stage (autonomous continuation)

**Stage 9 — Rank-2 general solver**: Table 4 types (1-2, 1-3, 2-3) into the deriver's
scope; the first half of the guarded_atoms implementation (generators +
campaign connection); the first test of the decomposition-discovery bridge.
