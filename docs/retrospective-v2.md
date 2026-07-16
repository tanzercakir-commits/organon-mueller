# Organon v2 (organon-mueller) — Project Retrospective (v2.0 closure)

**Date**: 2026-07-16 · **Scope**: the FROZEN-22 roadmap (stages A0–A22) ·
**State at writing**: A0–A21 complete, 288 tests green, CI green on the
three-version matrix. This document is the Stage 22 deliverable that
closes v2; it is documentation and assessment only — no code behaviour
changed in this stage.

## What v2 set out to be

Organon began, in v1, as a First-Order-Logic reasoning experiment that
started from concrete science rules and worked toward abstract concepts,
under a frozen stage count (frozen-55 there). v2 narrowed the substrate to
one well-characterised algebra — the Stokes–Mueller polarization algebra of
the Kuntman–Arteaga papers — and asked a sharper question: can a machine,
held to exact proof, both *rediscover* the known algebra and *derive*
(rather than transcribe) the published decompositions, and then push a
little past the printed tables without ever making a claim it cannot back?

The organising commitment was never the cleverness of any single result.
It was the trust anchor: **tests and runtime guards**. Every stage had to
close with green tests and an independent adversarial review, or it did not
close. That discipline, not any individual theorem, is what a reader should
take away from v2.

## The verification discipline (the through-line)

Every one of the 22 stages ran the same cycle: a written spec, a numeric
probe first whenever a new mechanism was in play, an implementation, tests,
an independent adversarial review by an agent that did not write the code
and re-derived the mathematics from scratch, and only then a push and a
report. The review verdict was binary; a FAIL was fixed and re-verified by
the *same* reviewer before the stage was allowed to close.

Three rules gave that cycle its teeth. First, the hybrid boundary (M10):
the equality-saturation engine (egglog) is never the sole verifier — every
candidate is certified independently by exact SymPy proof, so a bug in the
saturation layer can only ever cost a missed discovery, never admit a false
one. Second, the hard fuse (K9/K10): a candidate that cannot be verified is
not silently dropped, it breaks the build; the user's own framing was that
the tests are the only thing that saves us, so nothing is allowed to pass
quietly. Third, the evidence-class labels. Every outward statement is tagged
`symbolic-proof`, `numeric-deterministic`, or `candidate`, and the verb has
to match the label — "numerically verified" is not "symbolically proven".
That last rule (the "A15 verb-discipline") was learned the hard way in
Stage 15, when an outward-facing addendum called a result "symbolic" that
was at that point only numeric; the fix was permanent, both in the document
and as a lesson applied to every artifact afterward.

## Phase A — Foundation (A0–A2)

A0 built the representation layer: six isomorphic views of a polarization
state — Jones matrix, Mueller matrix, covariance matrix, covariance vector
|h⟩ = (τ, α, β, γ), Z-matrix, and biquaternion — with all conversions and a
symbolically-proven homomorphism between the biquaternion and 4×4 routes,
and recovered the first fourteen known identities as a regression seed. A1
extended the seed library to twenty-one identities (adding the
coherent-superposition and Type-1/2/3 symmetry relations) and ran a
successful egglog spike, which produced the hybrid-architecture proposal.
A2 built the discovery engine core — enumerate, saturate, harvest, verify —
rediscovered the seed relations, harvested a first sweep at 100% independent
verification, wrote the six-layer `docs/VERIFICATION.md` contract, and, on
that foundation, declared **FROZEN-22**: twenty-two stages, six phases, a
number that would not change again. (The name follows v1's frozen-55
convention — it indexes the roadmap by its final stage rather than counting
slots; the stages are enumerated A0 through A22, with A0 the zero-indexed
foundation layer, so "twenty-two" is the terminal index and the phase tree
below lists the full A0–A22 enumeration.)

## Phase B — Discovery engine (A3–A7)

A3 reversed the enumeration flow (fingerprint buckets suggest, an isolated
two-term e-graph proves) and, in doing so, hit and contained a real
large-graph pathology in egglog 13.2.0 — caught precisely because M10 never
trusted the engine alone (M18). A4 made exact `expand`-based symbolic proof
the binding certification layer (M19), so a numeric-only result can never
enter the finding channel. A5 turned the engine on itself: it had to
re-discover the seed identities unaided, recovered a subset, and named every
identity it *couldn't* reach with an explicit missing-property key — which
led to the **dagger-inexpressibility** argument, the proof that transpose /
dagger is not expressible in an elementwise-conjugation term language. A6's
first broad sweep returned an empty novelty channel, and rather than shrug
that off, elevated it to the **fragment-completeness theorem** (the term
language realises a trace monoid whose structure explains exactly which
classical identities can and cannot appear). A7 added opaque-scalar Sum and
Scale nodes and closed the phase with the Amitsur–Levitzki fine distinction
(expressible in principle, unreachable by the bounded enumeration).

## Phase C — Decomposition deriver (A8–A11)

A8 derived — not copied — all six variants of the AO2016 symmetry-conditioned
decomposition table from ordered rank-1 minor conditions, matched the printed
table to exact symbolic zero, reproduced the paper's numeric example, and
proved the **reshuffle theorem** establishing that the paper's covariance is
exactly the standard Cloude/Gil covariance. It also diagnosed two suspected
print artifacts in the source paper (an Eq. 17 imaginary part and an Eq. 21
entry), offered to the group as candidates for confirmation, never as
corrections asserted. A9 built the rank-2 general (composite-type) solver
and produced the first guarded-atom output — three Horn-conditional
identities carrying the four-part M32 evidence record (guarded-symbolic,
guarded-numeric, e-graph-unreachable, unguarded-false). A10 pushed into the
rank-3 three-term region, derived three type-pair decompositions verbatim,
and surfaced a genuine **non-uniqueness** observation (a covariance that
admits two different exact three-term splits), with an in-hypothesis
uniqueness proof for the {2,3} pair — labelled candidate, with the physical
selection question explicitly handed to the group. A11 assembled the first
Kuntman feedback package and the discovery→decomposition bridge, and closed
the phase with an honest ledger of deferred debts.

## Phase D — Dipole module (A12–A15)

A12 re-derived the coupled-dipole scattering results of PRB 98, 045410 as
theorems: the Eq. 25 three-term decomposition and the coupling determinant
identity, with the optical-activity parameter automated. A13 generalised the
optical-activity treatment to arbitrary propagation direction and proved a
general **Perrin reciprocity theorem** (for every Jones matrix, the
reciprocal geometry reproduces the transpose-conjugated response), with a
complete zero-set for the γ map. A14 generalised to N-dimer ensembles and
proved the forward result that a coupling-free chiral ensemble carries no
optical activity (δ = 0 ⇒ γ_z ≡ 0), and closed the first end-to-end bridge
from an ensemble covariance back through the decomposition layer. A15
delivered the bilingual dipole addendum and the phase retrospective — and is
where the verb-discipline lesson was learned and made permanent.

## Phase E — Packaging (A16–A19)

A16 built the deterministic, byte-identical LaTeX report generator and
institutionalised the evidence-class label as a first-class field of every
reported block. A17 built the MCP server surface and, with it, closed the
long-standing Stage-2 security gate: a restricted srepr parser
(`safe_parse.py`) that never routes text through `eval` or `sympify`,
hardened across five successive adversarial review rounds. A18 is the first
of the two reasoned scope revisions (below): the planned hosted Streamlit UI
became a single static, hosting-free `web/index.html`, XSS-safe by
construction. A19 rewrote the outward documentation — README, architecture
map, user guide — and added the ten `tests/test_docs.py` drift guards that
hold the documentation to the code.

## Phase F — Closure (A20–A22)

A20 closed the last deferred debt as an honest negative result (below),
consolidated the beyond-literature outputs into a single evidence-labelled
inventory (`docs/candidate-findings.md`), and carried out the second scope
revision: the English project-language transition. A21 validated the frozen
artifact from the outside — confirming CI green across the three-version
matrix, reproducing the five headline theorems from scratch through an
independent reviewer, and giving the Kuntman package a final consistency
pass (which caught and fixed a self-contradiction and a vacuous test before
they could reach anyone). A22 — this stage — is the retrospective, the
completion assessment, the version-tag proposal, and the future-work list.

## Two reasoned scope revisions (the count never changed)

The FROZEN-22 declaration fixed the *number* of stages, not every internal
detail. Two scope revisions happened, and neither touched the count:

The first is A18. The roadmap records it in its own words: the stage count
does not change, but A18's "hosted" definition was revised to "static,
hosting-free" for security reasons — a scope change, not a count change. The
reasoning is that a server is an attack surface; a single static file that
renders results a reader already has, with no network egress, removes that
surface entirely while still delivering the "read results in a browser"
goal.

The second is the English project-language transition (A20), on the user's
standing directive of 2026-07-14 that the project language is English. All
repository documentation was translated in place, with decision codes,
equation references, numbers, seeds, paths, and code kept verbatim; the
`docs/kuntman-package/*-tr.md` files were kept deliberately as a bilingual
deliverable for the group. Every artifact produced afterward, this
retrospective included, is written in English.

Both are recorded so that a future reader sees the freeze was honoured in
substance: the number was invariant, and each revision to scope was reasoned
in writing rather than quietly absorbed.

## The one negative result

The guarded-atoms channel had a second half that was deferred through
several stages (opened in A9, carried A11 → A15 → A16, scheduled into A20).
It was closed in A20 not by manufacturing a result but by proving there
isn't one to find. A probe scanned every small Mul/Conj term pair over the
hermitian-state and unitary-state guarded generators and found no
enumeration-reachable Horn-conditional identity; the reviewer re-scanned
from scratch to size six (188 terms) and still found none, and separately
proved the generators faithful (a hermitian state really gives Z = Z†, a
unitary state really gives Z Z† ∝ I). This is exactly what the theory
predicts: hermitian and unitary are *dagger* properties of the matrix, and
A5/A7 already proved dagger is inexpressible in this term language, so no
such property can ever surface as a term identity. The empty channel is
recorded as a first-class result (K21) and locked by a regression test, so
that any future change which *appears* to produce one is flagged as a bug in
a generator or an unsound language extension.

## FROZEN-22 completion assessment

All twenty-two stages closed against their roadmap lines. The suite grew
monotonically from 36 tests at A0 to 288 at A21, every increment gated by an
independent review; the only deferred acceptance debt (guarded-atoms second
half) was discharged in A20. No stage was skipped, merged, or split; the
count stayed at 22 throughout.

| Stage | Phase | Delivered | Status |
|---|---|---|---|
| A0 | A | 6-representation algebra + 14-identity seed; biquaternion homomorphism proof | ✅ |
| A1 | A | 21-identity library + serialization; successful egglog spike | ✅ |
| A2 | A | discovery engine core (enumerate/saturate/harvest/verify); VERIFICATION.md; **FROZEN-22 declared** | ✅ |
| A3 | B | reversed enumeration + isolated two-term proof (M18); egglog pathology contained | ✅ |
| A4 | B | exact symbolic-proof certification layer (M19) | ✅ |
| A5 | B | self-recovery campaign; dagger-inexpressibility argument | ✅ |
| A6 | B | sweep #1 → fragment-completeness theorem; novelty protocol | ✅ |
| A7 | B | Sum/Scale opaque scalars; Amitsur–Levitzki fine distinction | ✅ |
| A8 | C | AO2016 six variants derived from minors; reshuffle theorem; two print-artifact diagnoses | ✅ |
| A9 | C | rank-2 composite solver (Table 4 3/3); guarded atoms + M32 quadruple | ✅ |
| A10 | C | rank-3 three-term region; non-uniqueness finding; {2,3} uniqueness proof | ✅ |
| A11 | C | Kuntman package #1; discovery→decomposition bridge v1 | ✅ |
| A12 | D | coupled-dipole engine; Eq. 25 decomposition theorem | ✅ |
| A13 | D | direction-general optical activity; general Perrin reciprocity theorem | ✅ |
| A14 | D | N-dimer/ensemble; δ=0 ⇒ γ_z ≡ 0 theorem; end-to-end bridge | ✅ |
| A15 | D | dipole addendum; phase-D retrospective; verb-discipline lesson | ✅ |
| A16 | E | deterministic evidence-labelled LaTeX report generator | ✅ |
| A17 | E | MCP server; restricted srepr parser (Stage-2 gate closed, 5 review rounds) | ✅ |
| A18 | E | static hosting-free web viewer (**scope revision**, XSS-safe) | ✅ |
| A19 | E | README/architecture/user-guide; 10 doc-drift guards | ✅ |
| A20 | F | guarded-atoms negative result; candidate-findings inventory; **English transition** | ✅ |
| A21 | F | external validation; CI green ×3; independent theorem reproduction | ✅ |
| A22 | F | v2.0 closure: this retrospective, completion assessment, tag proposal, future work | ✅ |

## Open ends / future work

None of the following is a commitment; they are the honest edges of the
frozen artifact.

The freeze permits the internal order of phases C and D to change in
response to Kuntman-group feedback (the order may move, the count may not) —
so the natural next input is the group's answers to the package questions,
which could reprioritise the rank-3 non-uniqueness work or the dipole
extensions. On the mathematics, the OA-in-ensemble direction has open
generalisations beyond the forward δ=0 ⇒ γ_z ≡ 0 result, and the rank-3
region still has the physical-selection question (which of several exact
decompositions is the physical one) that is deliberately left to domain
experts. On the engine, the egglog large-graph pathology contained in A3 is
the subject of an upstream issue draft that has been written but not
submitted. And the four outward-facing actions — sending the Kuntman
feedback package, filing the egglog upstream issue, hosting the MCP server,
and exposing the web viewer — remain open by design, because they are the
user's to take, not the engine's.

## Trust boundary at closure

v2 closes with everything that is internal to the repository complete and
verified, and everything that reaches outside the repository reserved for a
human. Concretely, the following are *not* done and are not the assistant's
to do: submitting or sending the Kuntman package, filing the egglog upstream
issue, hosting or exposing the MCP server or web viewer, applying the v2.0
version tag, and — most importantly — making any claim that a candidate
result is physically new or interesting. That last one is step 5 of the
written novelty protocol, and it is reserved for people. The engine's job
was to make every such judgement *safe to make* by getting the mathematics
exactly right and labelling it honestly; the judgement itself stays with the
Kuntman–Arteaga group and the user.
