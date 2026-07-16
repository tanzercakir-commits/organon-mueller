# MILESTONE UI-1 — Local Web Interface (post-v2-closure)

**Date**: 2026-07-16 · **Mode**: interactive (user-directed) · **Language**:
English (project directive; UI copy in English by explicit user decision —
international audience expected)

## 0. Position relative to FROZEN-22

FROZEN-22 is closed (A0–A22); its stage count does not change. This is a
**post-closure milestone** in a new series (UI-1), opened by the user's
distribution decision: the easiest free way to *use* the engine is a local
interface on the user's own machine. It targets the `v1.0.0` release (see
`docs/v1.0-tag-proposal.md`, which also records the user's renumbering
decision: organon-mueller's semver starts at 1.x — "Organon v2" stays as
the program-generation name only).

## 1. Goal

`pip install "organon-mueller[ui]"` → `organon-ui` → a browser opens on
`http://127.0.0.1:7860` with an interactive, English-language interface:
enter/edit a 4×4 Mueller matrix cell by cell, pick a symmetry hypothesis,
and get the decomposition — plus an all-hypotheses proposal view and a
LaTeX report download. Free end to end (Gradio is Apache-2.0; everything
runs locally; no account, no service, no hosting).

## 2. Security posture (extends, does not weaken, Stage 17/18)

- The UI is a THIN layer over the already-hardened numeric-only tool
  functions (`mcp_server/tools.py`): inputs are numbers and enum strings
  only; no expression text ever crosses the boundary; all failures return
  a reason (K26), never a traceback.
- Binds to **127.0.0.1 only**; `share=False` hard-coded (no Gradio tunnel);
  `show_api=False`. Nothing is hosted or exposed — consistent with the
  Stage 18 decision ("a server surface is an attack surface"): the only
  listener is loopback on the user's own machine, reachable from that
  machine alone.
- No PDF compilation in the UI (the optional pdflatex path stays
  CLI/library-only); the report tab offers the `.tex` source for download.

## 3. Work items

1. `src/organon_mueller/ui/app.py` — pure, testable callback functions
   (grid → tool payload → display values) + `build_app()` (Gradio Blocks)
   + `main()` entry point with an injectable launcher (so tests can assert
   the launch kwargs without opening a socket).
   - Shared editable 4×4 matrix (spreadsheet-style grid) with example
     loaders: Identity and the AO2016 §6 mixture (0.3·M1 + 0.7·M2 at print
     precision, with the demo's documented tolerance preset).
   - Tabs: **Decompose** (fundamental + composite symmetries, a/b/auto
     variant, advanced tolerance fields), **Propose hypotheses** (rank +
     accepted/rejected with reasons + the verbatim "scores are an ordering
     heuristic, not evidence" note), **LaTeX report** (title + `.tex`
     download).
   - Footer: evidence-class note (numeric-deterministic display; symbolic
     proofs live in the suite; candidates carry no novelty/physics claim —
     protocol step 5 is human) + "runs entirely on your machine" line.
2. `pyproject.toml`: `[ui]` extra (`gradio>=4.0`), `organon-ui` console
   script, version → **1.0.0** (renumbering decision).
3. `docs/README-ui.md` — install/run/security notes (English).
4. Top-level README: add the local UI as a fourth usage surface +
   quickstart lines.
5. Tests (`tests/test_ui.py`, module-gated on gradio importability, same
   pattern as egglog): build_app smoke; decompose callback reproduces the
   §6 example (α₁ ≈ 0.3000); error paths return readable messages (K26) —
   wrong shape, non-decomposable input; propose callback on an exact
   synthetic rank-2 mixture; report callback emits `\documentclass` and a
   `.tex` file; launch-kwargs test proves `server_name="127.0.0.1"` and
   `share=False`; an English-copy guard over the UI string table.
6. `tests/test_docs.py::_full_optional_stack` gains `gradio`; README/
   ROADMAP test-count claims bumped to the new collected total; `ci.yml`
   installs `.[test,discovery,mcp,ui]` so the UI tests run on all cells.

## 4. Acceptance

Full suite green (old 288 + new UI tests, exact count in the docs);
adversarial review PASS covering: the localhost/share posture actually
enforced in code (not just documented), the numeric-only boundary intact
(UI adds no new parse path), English copy, evidence-class discipline in
the UI text, the version renumbering consistent everywhere it appears,
and doc-count drift guards green. FAIL → fix → re-verify with the SAME
reviewer. No gated action: nothing hosted, no tag applied, no submission.

## 5. Deltas discovered during implementation/review

- §2 listed `show_api=False` in the launch posture; **gradio 6 removed
  that kwarg** (passing it crashes the real launch — found live, since
  injected-launch tests cannot catch it). The delivered posture is
  `server_name=127.0.0.1`, `share=False`, `quiet=True`, and a regression
  test that validates every launch kwarg against the installed gradio's
  real `Blocks.launch` signature. The HTTP endpoint surface this leaves
  on loopback is guarded by the same numeric-only tool layer (verified
  adversarially over live HTTP in review).
- §3.2 said `gradio>=4.0`; the app uses the gradio-6 Dataframe API
  (`column_count`), so pyproject pins **`gradio>=6.0`**.

**STOP HERE**
