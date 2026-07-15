# STAGE 19 — Documentation (Phase E closure)

**Date**: 2026-07-14 · **Mode**: autonomous · **Probe**: no mechanism.

## 1. Goals

1. **README.md** (repo external face — GitHub sync `/README.md` include):
   what/status (experimental; verified vs candidate); three usage surfaces
   (package/MCP/web); quick start (working commands); verification
   contract summary + docs links; LICENSE note (none — user decision,
   explicitly). A15 verb-discipline: claim = evidence class.
2. **docs/architecture.md**: layer diagram + responsibilities + one-way
   bridges (M35-M37); M-series/K-series index table (the load-bearing ones);
   security boundary (safe_parse GATE).
3. **docs/user-guide.md**: end user who cannot use a terminal; "which
   question → which tool"; usage of the three surfaces; how to read the evidence labels.
4. Existing docs consistency scan: ROADMAP A0-A19 status markers;
   A18 "hosted → static" scope-change note; no broken links.

## 2. Correctness (docs = repo truth)

`tests/test_docs.py`: relative links resolve; README Python snippets
are imported + their symbols exist; the stated test count equals the real total
(drift guard); the 21 identity claims match the library; MCP command is a
real entry-point; no stale "Stage 2" status; pyproject extras consistent with the
README.

## 3. Acceptance

Three documents + ROADMAP up to date; test_docs.py green; every command/number/link
matches repo truth (auditor fact-check PASS required); 276→286 tests.

**STOP HERE**
