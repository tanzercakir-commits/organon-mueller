# FROZEN-7 Retrospective — the Lorentz Face (L0–L6)

**Series**: declared 2026-07-17 from a collaborator's written work
order; closed 2026-07-18. Seven stages, stage-gated interactive
cadence (STOP at every stage end; the user gated continuation).

## What was delivered

| Stage | Delivered | Headline |
|-------|-----------|----------|
| L0 | representation layer | bridge theorem: Σ^μ IS the engine's Z-basis |
| L1 | Task 1 verified | five identities = q=1 corollaries of guard-free theorems; no sign flip; row convention forced |
| L2 | Task 2 solved | five Σ̄ identities found; C = gΛᵀg = Λ(Z̄) forced; two bonus theorems |
| L3 | report #1 delivered | evidence-labeled LaTeX in the work order's own notation (out-of-repo) |
| L4 | term language + gate | self-recovery: 10/10 knowns re-found blindly and certified |
| L5 | discovery sweep | COMPLETENESS: 128 sandwiches decided — 40 identities (30 new) / 88 negative certificates |
| L6 | closure | report #2 (Task-3 answer), consolidation, v1.2.0 proposal |

Tests 368 → 399; every stage closed with the same adversarial reviewer
(independent re-derivation), full bare suite, and a push gated on the
review verdict.

## What worked (keep)

- **Probe-first on every new mechanism.** Both false starts of the
  series (the conjugation lemma's transpose-free first phrasing at L1;
  the Σ̄ = gΣg / Z̄ = gZg conjectures at L5) were caught by probes or
  tests BEFORE anything was claimed — the falsified versions are
  pinned as negative tests with honest records.
- **Self-recovery gate before discovery** (v2 A5 tradition transposed):
  the L5 sweep's credibility rests on L4's registry-blind 10/10.
- **Trace-orthogonality extraction** as the discovery workhorse:
  coefficient matrices are computed, not guessed, then identified
  against candidate libraries with degeneracy-aware canonical naming.
- **Same-reviewer adversarial continuity**: the reviewer's independent
  re-derivations sharpened results twice (the |q|² theorem now locked;
  the degeneracy census behind the canonical-naming audit) and
  corrected its own records when wrong (stale L1 carry-forward,
  documented).
- **Stage-gated cadence with the user** (quota checks between stages)
  — including a mid-series billing disruption absorbed without losing
  work (side-branch checkpoint `l2-wip`, ruled a legitimate practice
  by review, deleted after the reviewed main push).

## What bit us (rules adopted)

- **Docs edited after the last verification run** (L3's ROADMAP
  annotation read by the count-guard regex as a "2 tests" claim) put a
  red CI on an otherwise-green stage. Same failure family as v2's
  governance-docs-lag. RULE: the docs-guard runs after the FINAL doc
  edit of every stage; CI is the backstop, not the discovery point.
  The L4 commit message owns that red CI explicitly.
- **Evidence label ahead of its lock** (L3: two report statements —
  the |q|² sharpening and Cᵀ = gΛg — carried the `symbolic-proof`
  label before a repo test proved them; caught in-review, same stage,
  and locked as a 14th Task-2 test). RULE: nothing is labeled
  `symbolic-proof` until its locking test exists. The evidence class
  is a promise about the test suite, not about a derivation done once
  in a review run.

## Open ends (deliberate, gated)

- The universal pair-product formula: observed 40/40, posed to the
  collaborator as an open question — not claimed.
- Longer words, other middles (Λ as middle, q-rational forms): a
  possible next face, to be directed by collaborator feedback.
- Novelty-to-literature of the 30 new identities: human judgement,
  never the engine's claim.
