# Verification Contract

This project is being run in autonomous mode (2026-07-13 mandate). The user's
trust anchor is the layers in this document: **no mathematical claim can enter
the repo without passing through these layers.** Any change that weakens any
layer is a "critical decision" and requires user approval.

## Layers

1. **Symbolic-exact verification (SymPy)** — polynomial identities are proven
   with an `expand`-based EXACT zero test (not approximate). Source:
   `verify.symbolic_zero/symbolic_equal`.
2. **Deterministic numeric verification (NumPy)** — everything for which
   symbolic is costly is tested with fixed-seed (seed=20260713) random complex
   samples, with scale-relative tolerance. Reproducible in CI.
3. **Known-identity regression** — every identity in the library (currently 21)
   carries source-paper reference + side-condition (Horn guard) metadata and is
   re-proven on every push. The library only GROWS (I-keys frozen, decision
   M7). Tautological test legs are explicitly marked; only load-bearing legs
   enter the "recovered" count.
4. **Discovery engine contract (K9/K10)** — the engine (egglog equality
   saturation) is NOT a verifier ON ITS OWN: every candidate pair proposed by
   the e-graph is tested with an engine-independent SymPy/NumPy interpretation.
   A candidate that cannot be verified is not silently discarded; it surfaces as
   `refuted` and BREAKS the build (unsound axiom signal). Negative controls
   (e.g. saturation "not inventing" commutativity) are permanent tests. The
   soundness boundaries are written with rationale in the
   `discovery/axioms.py` docstring.
5. **Independent adversarial audit** — at every stage, a separate auditor agent
   that did not write the implementation audits the code and the mathematics by
   re-deriving them through routes independent of the source papers; no push
   happens without a PASS. Findings are recorded into the stage reports
   (`reports/`).
6. **CI matrix** — GitHub Actions, Python 3.10/3.11/3.12, full regression on
   every push. Red CI = the stage has not been closed.

## Phase C additions (stage 8–11; addition ONLY — no layer was weakened)

- **Pre-spec numeric probe**: campaign/sweep targets and derivation
  mechanisms pass through a numeric probe BEFORE being written into the spec
  (two gains recorded: A9 wrong-unitary target — as a spec-09 retraction note;
  A10 type-3 sign error — with a probe file). From A10 onward, probe files are
  stored under `probes/`.
- **Runtime invariant guards**: on every call, the solvers check the trace-1
  convention, input finiteness, the rank precondition, denominator/domain
  conditions, and the PSD/rank-1 physicality of the output components; a
  violation throws a reasoned `DecompositionError` (K26: no silent
  plausible-but-wrong output). Its counterpart on the discovery side is
  `check_invariants → DiscoveryInvariantError`.
- **M34 — the region without a paper-anchor**: when K28's "one-to-one with the
  printed table" anchor is not available, a three-layer substitute is
  MANDATORY: (i) the probe-verified hand derivation is fixed in the spec, (ii)
  the deriver output is tested symbolically one-to-one against those hand
  formulas, (iii) an independent auditor re-derives the mathematics from
  scratch. The language of the results is "candidate"; the physics
  interpretation is left to the human.
- **Over-determination guards (K32 type)**: if a solution path contains more
  independent equations than unknowns, the residual equation(s) turn into a
  MANDATORY consistency check at runtime; data that cannot pass is rejected
  with a reasoned error (silent patching forbidden).
- **Post-acceptance verification**: if a hypothesis is accepted unexpectedly
  (e.g. non-uniqueness: the same data can carry multiple valid decompositions)
  the acceptance is NOT automatically counted as an error; reconstruction +
  component purity are additionally verified and explicitly labeled in the
  artifact (`accepted_alternative_verified`). An acceptance that cannot be
  verified is a bug.

## Phase D additions (stage 12–15; addition ONLY)

- **K33 — PDF-based anchor discipline**: every anchor taken from the paper
  text carries an equation number; if the printed value conflicts with the
  derived one, an M30 print-note is filed (cumulative table:
  docs/phase-d-retrospective.md — eight diagnoses, all independent-auditor
  confirmed). Namesake-different-object warnings (e.g. the δ₁/δ₂ of two
  papers) are recorded into the naming.
- **Multi-paper cross-sentinels (M36 type)**: two independent modules must
  give the SAME result for the same physical configuration (Symmetry-general ↔
  PRB; paper Eq. 29 ↔ JOSA A HVector) — permanent tests.
- **Reduction-exactness proofs**: every dimension-reducing solution path
  (2×2 xy-block, rank-1 scalar) is verified in the audit against the FULL
  system (3D dyadic 6×6); the ruling "exact, not approximate" is put on
  record.

## Limits (honesty)

- Numeric verification (layer 2/4) is not a proof; it is evidence of
  "equality on a random set of points". Its practical confidence is high for
  polynomial-type identities; new-candidate identities MUST be passed through
  layer 1 (symbolic-exact) before turning into a publication claim (Phase B
  pipeline rule).
- Defense against convention errors: expected-value fixtures hand-fixed from
  the literature (`tests/test_fixtures.py`) — to catch correlated errors that
  route-to-route tests could hide.
- The physics INTERPRETATION (which identity is interesting, which is
  publication-worthy) is outside this system; it requires Kuntman/group
  feedback (Phase C/D windows).
