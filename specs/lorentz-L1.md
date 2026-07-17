# MILESTONE L1 — The Five Task-1 Identities (FROZEN-7)

**Date**: 2026-07-17 · **Mode**: stage-gated interactive · **Language**:
English

## 1. Goal

Verify the work order's five Task-1 identities — in their strongest
provable form — and resolve the spec's sign-convention warning into an
explicit table.

## 2. Findings (probe first, then locked by tests)

- **Stronger than asked:** each of the five identities is the q = 1
  corollary of a GUARD-FREE theorem over generic complex α (q ≡ α·α):
  LT1 Z†Σ^μZ = Λ^μ_νΣ^ν (Λ = ZZ*); LT2/LT3 conjugate sandwiches equal
  q̄Σ^μ; LT4/LT5 transpose sandwiches equal qΣ^μ; plus the chain lemma
  Λ(Z)·Λ(Z̄) = q q̄ I which turns LT1 into the spec's literal I1.
- **Sign table:** under the L0 parametrizations, ALL FIVE hold exactly
  as written for boosts AND rotations — no sign flip needed. The one
  convention the mathematics forces: Λ^μ_ν is the ROW-index reading;
  the column reading is FALSE and is pinned by a negative test.
- **Conjugation lemma** (the mechanism behind the spec's warning):
  Z(α)* = Z(α*)ᵀ (guard-free, from Σ* = Σᵀ); at the parameter level
  conjugation reverses rotations (α_rot(θ)* = α_rot(−θ)) and fixes
  boosts.
- **Honest records:** (a) the first symbolic check of the spec forms
  false-negatived on half-angle hyperbolics — a SIMPLIFICATION weakness,
  resolved by exponential rewrite (encoded in `_spec_zero`); (b) an
  early chat-level phrasing of the conjugation lemma (without the
  transpose) was WRONG and was caught by this milestone's own test
  before review — the corrected statement is the one above.

## 3. Work items

`lorentz/identities.py` (registry in the known-identity-library
tradition: key/statement/spec_form/check; `verify_task1()`;
`spec_form_holds(alpha, which)` with the guard enforced, K26 reasons);
`probes/probe-lorentz-task1.py` (committed); `tests/test_lorentz_task1.py`
(12 tests: five theorems independently re-stated, chain lemma, negative
index pin, spec forms for boost+rotation ×5, guard/argument errors,
conjugation lemma). Input note (reviewer, L0): α never enters as TEXT —
this stage adds no text inputs; any future surface exposing α must be
floats-only or `safe_parse`.

## 4. Acceptance

Full suite green with updated counts; adversarial review PASS (same
reviewer; re-derive the five theorems + chain lemma independently, check
the negative pin really pins, confirm the sign table's honesty). STOP
after review; push queued (PAT ready on the user's side, to be supplied).

**STOP HERE**
