# STAGE 20 — Consolidation + English Language Transition (Phase F opening)

**Date**: 2026-07-14 · **Mode**: autonomous · **Language**: English (new
standing directive — see §3)

## 1. Guarded-atoms second half (deferred debt from A16)

**Pre-implementation probe (mandatory, stage-9 lesson) — DONE**
(`probes/probe-guarded-hermitian-unitary.py`, seed 20260713): scanned all
size-≤4 Mul/Conj term pairs over two guarded atoms for a genuine
Horn-conditional signature (guard-true symbolic+numeric AND
unguarded-false AND guard-blind-unprovable).

**Result: NONE** in both the `hermitian_state` and `unitary_state`
classes (the `class2` control correctly reproduces the known commutation
finding). This is the expected, theory-consistent outcome: a hermitian
state (`|h⟩` real) or unitary state (`|h⟩` = τ real + imaginary vector
part) constrains the covariance-vector COMPONENTS, but the
distinguishing algebraic facts of a hermitian/unitary MATRIX
(`Z = Z†`, `Z Z† = I`) are *dagger* properties — and stage-7 proved the
transpose/dagger is inexpressible in this elementwise-conjugation term
language. No dagger property can therefore surface as a term identity.

**Decision: close the debt as a documented NEGATIVE result** (K21
spirit: an empty channel is a first-class result). Add to
`docs/design-note-guarded-atoms.md` and lock it with a regression test
(`test_no_reachable_horn_identity_in_hermitian_unitary`) so any future
change that *appears* to produce one is flagged (it would signal an
unsound generator or a language extension that reaches dagger).

## 2. Consolidation document — `docs/candidate-findings.md` (English)

A single place collecting the publication-*candidate* outputs, each with
its evidence class, and NO novelty/physics claim (novelty-protocol step 5
is human): rank-3 non-uniqueness; the guarded Horn-conditional
identities (class2 planes); the eight M30 print diagnoses; the
fragment-completeness theorem; the reshuffle theorem; the general Perrin
reciprocity theorem; δ=0 ⇒ γ_z ≡ 0. Raw material for the Kuntman package
and any future write-up.

## 3. English language transition — batch 1

Standing directive (user, 2026-07-14): the project language is English.
Translate ALL Turkish documentation to English — `docs/*.md` (12, EXCEPT
`kuntman-package/*-tr.md`, kept as a deliberate Turkish deliverable),
`specs/*.md` (20), `reports/*.md` (20). Every artifact produced from now
on is written in English (this spec included).

Fidelity rules: technical terms, decision codes (M28, K26, I1, …),
equation references, numbers, seeds, file paths, and code blocks are kept
VERBATIM; only prose is translated; NO summarizing/abbreviation — the
translation must preserve the original meaning exactly. Use parallel
subagents (each a batch of ~5-8 files). If not all 52 files fit in this
stage, carry the remainder to A21 (record which files remain in the
report and the next trigger). `test_docs.py` link/number/command
assertions must still pass after translation.

## 4. Acceptance

Guarded debt closed (negative-result note + regression test); no code
behavior change (guarded campaign still 3 findings). `candidate-findings.md`
fact-checked against the repo. Translated files preserve meaning
(reviewer fidelity spot-check on a sample); `test_docs.py` green; full
suite green (≥ 286, minus none).

**STOP HERE**
