# STAGE 5 — Recovery Campaign (Phase B)

**Date**: 2026-07-13 · **Previous**: stage-04 (v1.2, symbolic certification)
**Mode**: autonomous

---

## 1. Context

The v1 "recover the known" discipline is being carried to the discovery level: the engine
must re-find ON ITS OWN the subset of the hand-coded I1–I21 library that can be translated
into the term language (atoms + mul + conj; atom = generic Z). The ones that cannot be
translated are not accidental, they are the boundary map of the term language → the
requirements list for post-Phase-B expansion comes from here.

## 2. Goals

1. **`discovery/recovery.py`**: I1–I21 → term-language mapping table
   (`RECOVERY_TABLE`): each record is either translatable (with concrete term pairs) or
   structural (embedded in the language itself) or untranslatable (with missing-property
   keys). Campaign runner: for each translatable pair the triple of
   proof + numerical + symbolic.
2. **Expected mapping** (pre-analysis; the test verifies this):
   - Translatable: **I1** (Z·Z\*=Z\*·Z and M-reality in the t≡conj(t) form),
     **I10** (commutation + serial Mueller law).
   - Structural: **I7/I8** (quaternion↔Z product compatibility = the language's Mul).
   - Untranslatable: I2-I6, I9, I11-I21 → missing property groups:
     (a) addition + scalar coefficient (I15-I17), (b) dagger/bra-ket + Stokes
     (I9, I12-I14), (c) entry/trace/det level (I2, I5, I6, I19-I21),
     (d) restricted/special atoms (I4, I11, I18).
3. **`docs/term-language-extensions.md`**: requirements list, in priority
   order (physics value: addition+scalar first — coherent superposition).
4. Harvest-proof: the I1 pairs appear in the full-7 harvest, the I10 pairs appear in the
   harvests of the existing tests (CI-cheap configurations).
5. **egglog upstream draft issue** (`docs/egglog-upstream-issue-draft.md`):
   English, self-contained repro INDEPENDENT of our package; if possible a record set
   minimized with delta-debug. SUBMISSION is subject to user approval
   (critical-decision); this stage only produces the draft.

## 3. Architectural decisions

- **M22. The campaign is a permanent regression**: RECOVERY_TABLE is bound with a test;
  as the language expands in the future, "untranslatable" records are moved to translatable
  and the campaign rate can ONLY INCREASE (monotone-progress guard).
- **M23. The upstream draft lives inside the repo**, is not counted as submitted;
  the submission record (date/link) is added only after user approval.

## 4. Strict rules

- K19. The "untranslatable" verdict cannot be given WITHOUT a missing-property key.
- K20. In the campaign, each translatable pair must pass all three layers
  (proof + numerical + symbolic); a single failure breaks the stage.

## 5-6. Deliverable + Verification

`discovery/recovery.py` · `tests/test_recovery.py` (table integrity K19,
campaign K20, monotonicity M22 base, harvest-proof) ·
`docs/term-language-extensions.md` · `docs/egglog-upstream-issue-draft.md` ·
report. Whole suite green; campaign output as a table in the report.

## 7-9.

Push + report + Stage 6 planning. Warning: the M-reality pair (t, Conj(t))
is NOT conj-normal — the harvest proof is sought in full (unpruned) mode. Out of
scope: the language expansion itself (input to the Stage 6+ specs), literature
comparison, new sweep.

**STOP HERE**
