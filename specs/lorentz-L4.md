# MILESTONE L4 — Term Language + Self-Recovery Gate (FROZEN-7)

**Date**: 2026-07-17 · **Mode**: stage-gated interactive · **Language**:
English

## 1. Goal

Extend the engine's term machinery to the Lorentz face so that the L5
discovery sweep (the work order's Task 3) has a trustworthy substrate:
a term language over conjugation-type operators, and the v2 tradition's
credibility precondition — the **self-recovery gate**: the machinery
must FIND the ten known identities ITSELF before it is allowed to hunt
for new ones (A5 recovery-campaign tradition).

## 2. Term language (scope for this stage)

- **Alphabet** (8 letters): {Z, Z*, Zᵀ, Z†} × {plain, bar}, i.e.
  Z, Z*, Zᵀ, Z†, Z̄, Z̄*, Z̄ᵀ, Z̄†, all polynomial in α — generic
  complex α, guard-free.
- **Inverse convention (M29-style note):** Z⁻¹ = q⁻¹Z̄, so inverses
  are covered by the bar letters UP TO the scalar q; the alphabet
  deliberately stays polynomial (no denominators, no q ≠ 0 guard in
  the enumeration itself).
- **Sandwich space:** X · mid^μ · Y with X, Y in the alphabet and
  mid ∈ {Σ, Σ̄} — 8×8×2 = 128 sandwiches, the exact shape family of
  the work order's Tasks 1–2. Longer words, other middles: L5 scope.
- **Classification target:** C^μ_ν extracted by trace-orthogonality in
  the mid family's own dual basis; matched (numerically, two fixed
  seeds, genuinely complex α) against s·B with
  s ∈ {1, q, q̄, qq̄} and B ∈ {I, Λ, Λᵀ, Λ̄, Λ̄ᵀ}.
  Base aliases via the L2 bonus theorem are recorded once:
  Λ̄ = gΛᵀg and Λ̄ᵀ = gΛg (the g-conjugates are NOT separate bases).
- **Certifier:** a generic symbolic prover (expand == 0) for any
  classified sandwich — a code path INDEPENDENT of
  `identities.py`'s per-theorem checks, so gate certification is a
  genuine re-derivation.

## 3. Self-recovery gate (acceptance heart)

The enumeration — numeric screen plus symbolic certification, no
lookup of the known registry anywhere in the path — must find and
prove all ten:

| # | sandwich | class |
|---|----------|-------|
| LT1 | Z† Σ Z | (1, Λ) |
| LT2/3 | Z* Σ Z̄* and Z̄* Σ Z* | (q̄, I) |
| LT4/5 | Zᵀ Σ Z̄ᵀ and Z̄ᵀ Σ Zᵀ | (q, I) |
| LT6 | Z Σ̄ Z† | (1, Λ̄) |
| LT7/8 | Z* Σ̄ Z̄* and Z̄* Σ̄ Z* | (q̄, I) |
| LT9/10 | Zᵀ Σ̄ Z̄ᵀ and Z̄ᵀ Σ̄ Zᵀ | (q, I) |

Negative control: at least one sandwich known to match nothing (e.g.
Z Σ Z) must classify as no-match. Determinism: both seeds must agree.

## 4. Scope discipline

The enumeration will surface MORE matches than the ten (the sandwich
space is symmetric). In L4 these are reported as COUNTS only —
no statement-level claims; their certification and any candidate-channel
reporting is L5's job (no-novelty-claim rules apply there). This
boundary keeps L4's evidence ledger clean.

## 5. Process lesson (recorded at closing; reviewer-endorsed)

The L4 full-suite run caught the docs count-guard failing: L3's ROADMAP
annotation contained the substring "Task-2 test", which the guard's
deliberately dumb regex legitimately reads as a "2 tests" claim. L3's
own suite run predated that annotation edit, so L3 closed green while
its pushed commit's CI went red — the guard worked, but CI was the
discovery point instead of the local run. Same failure family as the
v2 governance-docs-lag BLOCKER: **an artifact edited after the last
verification run carries an unverified claim.** Rule adopted for every
stage closing: any post-suite edit to guard-read docs (README/ROADMAP)
invalidates "suite green" — re-run `tests/test_docs.py` after the
final doc edit (ideally the full suite is the last act before commit).
CI is the backstop, not the discovery point.

## 6. Acceptance

Probe first (classification approach validated); `lorentz/terms.py` +
tests (letters correctness, extraction lemma, positive/negative
classifications, THE GATE: 10/10 found + 10/10 symbolically certified
through the terms path, determinism); full suite green with updated
counts; adversarial review PASS (same reviewer; special charge: verify
the gate is genuinely self-recovery — no registry/lookup leak into the
enumeration or certification path); push. STOP.

**STOP HERE**
