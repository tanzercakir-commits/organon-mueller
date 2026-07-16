# MILESTONE UI-2 — REPORT (File Loading & Batch Decomposition — v1.1.0)

**Date**: 2026-07-16 · **Spec**: `specs/milestone-ui-02.md` · **Mode**:
interactive (user-directed) · **Result**: COMPLETED — **342 tests green**;
adversarial review FAIL → all findings fixed → **PASS** with explicit
sign-off on the new parse path; three user field reports (Windows/VSCode)
fixed and locked in the same milestone.

## 1. What shipped

- `ui/loaders.py` — the project's second text-parse surface, deliberately
  strict: `.csv/.tsv/.txt`, single 4×4 or wide batch (16 cols = m00…m33
  row-major; 17 = label + 16), delimiter auto-detection (consistent
  comma/semicolon/tab/whitespace), optional single header (width-aware),
  `#` comments, BOM; caps 5 MB / 10,000 matrices / 64 KiB line / 64-char
  labels; everything `float()`ed and finite-checked; K26 readable reasons
  throughout.
- "File / batch" UI tab: load a file (or one batch row) into the shared
  editor; decompose all rows through the hardened `tool_decompose_mueller`
  boundary (defence in depth unchanged); per-row α₁ or failure reason;
  results table + downloadable CSV (labels quoted AND
  formula-injection-neutralized).
- When several hypotheses are exact at once, the propose view now says
  so explicitly (*a* decomposition, not *the* decomposition — verified
  non-uniqueness; the physical choice is a human judgement) — added from
  a live field observation.

## 2. Review: FAIL → fixed → PASS

First pass returned one MODERATE + three MINOR findings. The MODERATE
was the important one: the splitter silently dropped empty cells, so a
file with a consistently blank column reparsed as a narrower format and
produced **shifted, wrong matrices with no error** — the one failure mode
a scientific batch loader must not have. Fixed by keeping empty cells and
rejecting them per-cell with row/col (plus: empty labels rejected; an
empty cell never counts as header evidence). Also fixed: results-CSV
label quoting (comma-bearing labels from tab-delimited input), visible
"skipped 1 header line" notices (a stripped header is never silent), and
OSError surfacing as a readable reason. The re-verification confirmed the
original exploit now fails closed, CSV structure is valid under
`csv.reader`, and no regressions.

## 3. Field reports (Windows/VSCode session), all fixed here

1. **Report tab crashed on a Greek title** (`UnicodeEncodeError` via the
   platform code page — and α, β, λ are this project's daily notation):
   every text write now declares UTF-8.
2. **The suite failed en masse on Windows** (encoding-less `read_text` in
   test helpers): repo-wide sweep — every `read_text`/`write_text` in
   src/tests/examples declares `encoding="utf-8"`; three `subprocess.run`
   text-mode calls got `encoding="utf-8", errors="replace"`. Locked by a
   STATIC guard (`test_text_io_always_declares_encoding`, which scans the
   tree — it caught its own docstring during development) and a dynamic
   sweep (`PYTHONWARNDEFAULTENCODING=1`: zero EncodingWarnings from our
   files), plus a functional Greek-title round-trip test. CI gained a
   **windows-latest cell** so the discipline stays honest cross-platform.
3. **`organon-ui` without the `[ui]` extra died with a raw traceback**
   (the console script installs regardless): now one readable line —
   `organon-ui: the web-interface extra is not installed. Fix: pip
   install "organon-mueller[ui]"` — locked by a subprocess test.

## 4. Status

Version **1.1.0** (metadata set; PyPI release happens only when the user
publishes the GitHub Release — publish.yml then uploads automatically,
its first automatic run). 342 tests green; claims updated; no gated
action taken.
