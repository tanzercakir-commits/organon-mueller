# MILESTONE L5 — Discovery Sweep over the Sandwich Space (FROZEN-7)

**Date**: 2026-07-18 · **Mode**: stage-gated interactive · **Language**:
English

## 1. Goal

The work order's Task 3: hunt for further identities in various forms
of Z, Σ^μ, Σ̄^μ, Λ. Scope for this stage: COMPLETE the 128-sandwich
space X·mid^μ·Y opened in L4 — every sandwich must end in exactly one
of: proven identity (with closed-form coefficient matrix) or proven
non-identity (negative certificate). Longer words stay out of scope
(possible L6+ extension gated on collaborator feedback).

## 2. Method (probes committed)

Probe 1 certified the six L4 extras symbolically and identified 4 of
the 24 expansion-unmatched coefficient matrices with second-kind
quadratics (ZZᵀ-type). Probe 2 extended the candidate library to ALL
ordered two-letter products (64 pairs) plus I and g, with a
family-swap channel — and identified the remaining 20/20. Result:
**zero dark sandwiches**.

## 3. Findings (probe-first; locked by the L5 tests)

- **Λ-family closure (6 new theorems):** LT1/LT6 sit inside an
  8-member family: (Z†,Σ,Z)→Λ, (Z,Σ,Z†)→Λᵀ, (Z̄,Σ,Z̄†)→Λ̄ᵀ,
  (Z̄†,Σ,Z̄)→Λ̄, (Z,Σ̄,Z†)→Λ̄, (Z†,Σ̄,Z)→Λ̄ᵀ, (Z̄,Σ̄,Z̄†)→Λ,
  (Z̄†,Σ̄,Z̄)→Λᵀ — all scalar 1, all guard-free.
- **Pair-product structure (24 new theorems):** every remaining
  expanding sandwich has C = a two-letter product, scalar 1 — e.g.
  Z Σ^μ Z = (ZZᵀ)^μ_ν Σ^ν and Z Σ^μ Z̄ = (ZᵀZ̄)^μ_ν Σ^ν. The four
  Λ-forms are themselves pairs (Λ = Z·Z*, Λᵀ = Z†·Zᵀ, Λ̄ = Z̄·Z̄*,
  Λ̄ᵀ = Z̄†·Z̄ᵀ), so the UNIFYING OBSERVATION reads: **for every
  expanding sandwich, C is a product of two alphabet letters up to a
  scalar in {1, q, q̄, qq̄}** — proven case-by-case (40/40); a
  single-formula universal proof is deliberately NOT claimed
  (candidate for the collaborator discussion, report #2).
- **Completeness:** the space partitions 40 expanding / 88
  non-expanding, and all 88 negatives carry symbolic certificates
  (residual after dual-basis projection is a nonzero polynomial).
- **Canonical naming rule:** identification tries I before pairs (all
  scalars), in documented order — needed because degenerate pairs
  exist (Z·Z̄ = qI), so C = qI must read ("q", I), not ("1", Z·Z̄).
- **Falsified-conjecture record (honest):** the tempting structural
  lemmas Σ̄^μ = gΣ^μg and Z̄ = gZg are FALSE (probe 2 falsified them
  before any claim was made; the i-carrying entries do not flip).
  Locked as negative pins — they explain why no family-swap channel
  fired (the swap channel found zero matches).
- **Novelty boundary:** all 30 new statements are evidence class
  symbolic-proof as IDENTITIES; whether any is new to the literature
  (vs. known Fierz/SL(4,C) relations) is deliberately not claimed —
  human judgement, collaborator-facing in report #2 (L6).

## 4. Work items

`lorentz/discovery.py`: all-pairs candidate library, exact symbolic
`full_sweep()` (no seeds — end-to-end exact), canonical identification
order, negative certificates, JSON-able sweep table;
`reports/sweep-lorentz-01.json` (committed, deterministic);
`probes/probe-lorentz-sweep.py` + `probe-lorentz-sweep2.py`;
`tests/test_lorentz_discovery.py` (module-scoped single sweep fixture:
completeness 40/88/128, six Λ-family statements, second-kind and
mixed-pair spot statements, L4-crosswalk consistency (Λ = Z·Z* naming),
canonical-order rule, all-88 negative certificates, falsified-lemma
pins, committed-report reproducibility).

## 5. Acceptance

Full suite green with updated counts; docs-guard re-run after the last
doc edit (L4 rule); adversarial review PASS (same reviewer; special
charges: canonical-order soundness — no ambiguous identification can
slip through; the 30 new statements really are statements, each locked;
falsified-lemma pins honest; no novelty overclaim anywhere); push.
STOP.

**STOP HERE**
