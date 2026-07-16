# MILESTONE UI-2 — File Loading & Batch Decomposition (v1.1.0)

**Date**: 2026-07-16 · **Mode**: interactive (user-directed) · **Language**:
English

## 1. Goal

General-audience gap identified after the v1.0.0 release: real
polarimetric data arrives as FILES (a measured spectrum is hundreds of
Mueller matrices in one CSV), while the v1.0 interface only offers
cell-by-cell entry. Add: (a) load a single 4×4 matrix from a file into
the editable grid, and (b) batch-decompose a whole file (one matrix per
row) with a downloadable results table. Version bumps to **1.1.0**
(backward-compatible feature); the release will also be the first
exercise of the automatic publish path (GitHub Release → publish.yml →
PyPI).

## 2. Supported file formats (v1.1 — documented, strict)

Text files (`.csv`, `.tsv`, `.txt`), UTF-8, decimal POINT only.
Delimiters: comma, semicolon, tab, or whitespace (auto-detected; must be
consistent within the file). Blank lines and `#`-comment lines ignored.
An optional single header line (any non-numeric token) is skipped.

- **Single matrix**: exactly 4 data rows × 4 numeric columns → loads
  into the editor grid.
- **Batch (wide format)**: N data rows ×
  - **16 numeric columns** = m00…m33 (row-major), labels = row numbers; or
  - **17 columns** = a leading label column (e.g. wavelength; kept as an
    opaque string) + the 16 matrix entries.

Anything else is rejected with a reason (K26): wrong column count,
non-numeric cell (reported with row/column), non-finite values, mixed
delimiters, empty file. Caps: file ≤ 5 MB, ≤ 10,000 matrices, line
length ≤ 64 KiB — all rejected with readable reasons, never a crash.

## 3. Security posture (a NEW parse path — the review focus)

This milestone deliberately adds the project's second text-parse surface
(after safe_parse.py). Contract:

- The parser (`ui/loaders.py`) is **gradio-free** and **strictly
  numeric**: split lines → split cells → `float()` every cell. No eval,
  no pandas/CSV-module dialect magic, no dynamic dispatch on content.
  The only non-numeric data ever retained is the optional batch label,
  kept as an inert display string (length-capped).
- Defence in depth unchanged: every matrix still goes through
  `tool_decompose_mueller`, which revalidates shape/type/finiteness
  independently. The parser feeding it garbage can only produce a
  readable error, never reach the solvers un-checked.
- DoS caps as above; the upload is a local file on the user's own
  machine (the app still binds 127.0.0.1 only, share=False), but the
  parser treats it as untrusted anyway.

## 4. Work items

1. `src/organon_mueller/ui/loaders.py` — `parse_matrix_file(path)` →
   `{"kind": "single", "matrix": ...}` or `{"kind": "batch", "labels":
   [...], "matrices": [...]}`; module-level caps; ValueError with
   readable reasons.
2. `app.py` — new **"File / batch"** tab: file picker + format help;
   "Load into editor" (single file, or batch row N via a row selector);
   "Decompose all rows" → per-row `tool_decompose_mueller` with the
   shared symmetry/variant/tolerance controls → summary line (n ok / n
   failed), results table (label, status, α₁ or reason), and a results
   CSV download (written via the process-lifetime temp dir). Parsed
   batches are held in a `gr.State` so row-loading does not re-read the
   file. All copy English, in `STRINGS`.
3. `pyproject.toml` version → 1.1.0; README quickstart/feature mention;
   `docs/README-ui.md` file-format section; count claims bumped.
4. Tests: parser unit tests gradio-free (formats, header/label
   detection, delimiter variants, hostile inputs: oversize file, row
   cap, bad cell with row/col in the message, NaN/Inf, 4×5, empty,
   binary garbage); callback tests (single load, row load, batch with
   mixed ok/failing rows, results CSV contents); English-copy guard
   still passes.

## 5. Acceptance

Full suite green with updated count claims; adversarial review PASS with
explicit sign-off on the new parse path (numbers-only, capped, K26, no
eval/exec/import surface, boundary intact); no gated action (push waits
for the user's new fine-grained PAT; the PyPI release of 1.1.0 is the
user's — publish.yml fires only on THEIR GitHub Release).

## 6. Deltas discovered during implementation/review

- §4.2 planned a `gr.State` to avoid re-reading the file; the delivered
  callbacks re-parse per click instead — simpler, and bounded by the
  parser caps (5 MB / 10k rows), so the state object was dropped.
- Review findings (first pass FAIL, all fixed): empty cells are now KEPT
  by the splitter and rejected per-cell with row/col — silently dropping
  them let a consistently blank column reparse as a narrower format and
  produce shifted, wrong matrices with no error; results-CSV labels are
  quoted+escaped (comma-bearing labels from tab-delimited input);
  a stripped header line is reported in the status ("skipped 1 header
  line"), never silent; OSError on the file surfaces as a readable
  reason. Locked by dedicated tests.
- v1.1.1 field diagnoses (Windows/VSCode session testing the released
  1.1.0): stale ``__version__`` ("0.0.1") synced to pyproject and locked
  by a text-level equality guard; the header rule tightened to "a line
  is a header only if NO must-numeric cell parses as a number" — one
  numeric cell is data evidence, so a typo'd data row reports its exact
  cell instead of being absorbed as a header (independently verified
  against the full suite before adoption).

**STOP HERE**
