# MILESTONE L2 — The Five Missing Σ̄ Identities (FROZEN-7)

**Date**: 2026-07-17 · **Mode**: stage-gated interactive · **Language**:
English

## 1. Goal

The work order's Task 2: find the five identities "in terms of Σ̄" that
mirror Task 1 — they are not given in the spec; they must be DISCOVERED,
then locked.

## 2. Method (probe first)

The Σ basis is trace-orthogonal — tr(Σ^μΣ^ν) = 4δ^{μν}, and likewise
for Σ̄ (locked as a lemma test). So for the Λ-type identity the unknown
coefficient matrix C in Z Σ̄^μ Z† = C^μ_ν Σ̄^ν is EXTRACTED exactly by
traces, then IDENTIFIED against closed-form candidates
(`probes/probe-lorentz-task2.py`, committed).

## 3. Findings (probe, then locked by tests)

- **LT6 (Λ-type):** Z Σ̄^μ Z† = C^μ_ν Σ̄^ν with **C = gΛᵀg = Λ(Z̄)**,
  guard-free over generic complex α. Wrong candidates — plain Λ, Λᵀ,
  gΛg — are pinned FALSE by negative tests: the closed form is forced.
- **BONUS theorem** (the equality of the two identifications, found on
  the way): **Λ(Z̄) = g Λ(Z)ᵀ g**, guard-free.
- **On the guard q = 1:** ΛᵀgΛ = g makes C = Λ⁻¹ (locked: Λ·C = I
  exactly for boost and rotation), so LT6 becomes the spec-mirror form
  **Σ̄^μ = Λ^μ_ν Z Σ̄^ν Z†** — the exact dual of Task-1's I1: the
  sandwich swaps (Z⁻¹)†…Z⁻¹ ↔ Z…Z†.
- **LT7–LT10 (sandwich family):** with Σ̄ in the middle the SAME scalar
  factors appear as in the Σ family — Z*Σ̄Z̄* = q̄Σ̄, Z̄*Σ̄Z* = q̄Σ̄,
  ZᵀΣ̄Z̄ᵀ = qΣ̄, Z̄ᵀΣ̄Zᵀ = qΣ̄. On the guard these are the spec-style
  forms Σ̄^μ = Z* Σ̄^μ (Z⁻¹)* etc., boosts and rotations alike (J1–J5,
  exp-rewrite zero test per the L1 lesson).

## 4. Work items

`lorentz/identities.py` Task-2 section (LORENTZ_TASK2 registry LT6–LT10,
`verify_task2()`, `spec_form_holds_bar(alpha, which)` J1–J5 with the
guard enforced, `bonus_lambda_zbar_theorem()`);
`lorentz/__init__.py` exports; `probes/probe-lorentz-task2.py`
(committed); `tests/test_lorentz_task2.py` (13 tests: trace lemma both
bases, registry, LT6 direct with BOTH identifications, three negative
pins, bonus theorem, LT7–10 direct, C = Λ⁻¹ on the guard, J1–J5 for
boost+rotation ×5, guard/label errors). No new input surfaces — α never
enters as text (standing L0 note).

## 5. Acceptance

Full suite green with updated counts (368 → 381); adversarial review
PASS (same reviewer; re-derive LT6–LT10 + bonus independently, check the
pins pin, check the duality claim J1 ↔ I1, verb discipline, count
consistency). Push to main after review (PAT supplied by the user);
the l2-wip safety-checkpoint branch (billing-pause artifact) is then
deleted. STOP.

**STOP HERE**
