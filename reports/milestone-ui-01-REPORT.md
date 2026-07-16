# MILESTONE UI-1 — REPORT (Local Web Interface — post-v2-closure)

**Date**: 2026-07-16 · **Spec**: `specs/milestone-ui-01.md` · **Mode**:
interactive (user-directed) · **Result**: COMPLETED — `organon-ui` ships;
**305 tests green** (288 + 17 new); adversarial review **PASS** (7
minor/doc findings, all fixed and re-confirmed by the same reviewer).

## 1. What shipped

- `src/organon_mueller/ui/app.py` — a Gradio front end over the hardened
  numeric-only tool layer: an editable 4×4 Mueller-matrix grid with three
  example loaders (identity; an exact synthetic type-1 mixture that
  decomposes under the DEFAULT tolerances to α₁ = 0.35; the AO2016 §6
  print-precision mixture, which also sets the demo's documented
  tolerance preset), and three tabs — Decompose, Propose hypotheses, and
  LaTeX report (.tex download). All copy is English (user decision:
  international audience). Install: `pip install -e ".[test,ui]"`; run:
  `organon-ui`.
- `tool_generate_report` gained the same validated tolerance passthrough
  as `tool_decompose_mueller` (print-precision data was unreportable
  without it), locked by a new security test.
- Version renumbered to **1.0.0** (user decision, 2026-07-16:
  organon-mueller is a separate project from Organon v1, so its semver
  starts at 1.x; "Organon v2" stays as the program-generation name).
  `docs/v1.0-tag-proposal.md` supersedes the v2.0 proposal; the Stage 22
  spec/report are kept unchanged as historical records.

## 2. Security posture (verified, not just documented)

The interface binds to **127.0.0.1 only** and `share=False` is a
constant, not a parameter — `launch_kwargs()` exposes only port and
browser-open. The reviewer verified this at the kernel level
(`/proc/net/tcp`: the only listener is `0100007F` = 127.0.0.1), attacked
it with hostile `GRADIO_SERVER_NAME=0.0.0.0` / `GRADIO_SHARE=true`
environment variables (the explicit constants win), and confirmed zero
listeners remain after close. The UI adds no parse path: every
computation goes through the numeric-only tool functions, and 60+ hostile
callback inputs plus live-HTTP attacks all returned readable
`Error: ...` reasons (K26) — zero tracebacks.

## 3. A bug the tests could not see — and the test that now can

Injected-launch tests capture the kwargs `main()` would pass, but cannot
know whether the REAL `Blocks.launch` accepts them. Live launch revealed
gradio 6 removed `show_api` — `organon-ui` would have crashed at startup.
Fixed, and locked by
`test_launch_kwargs_all_exist_in_real_launch_signature`, which validates
every launch kwarg against the installed gradio's actual signature. The
spec records this and the `gradio>=6.0` pin as implementation deltas
(spec §5).

## 4. Independent audit

Verdict: **PASS** (first pass), then all seven MINOR/DOC findings fixed
and re-confirmed by the same reviewer (findings 5–6 re-tested
empirically, not just read): spec staleness ×2 (recorded as spec deltas),
README surface-count heading, the `ui` extra added to the pyproject↔README
guard, a per-click temp-dir leak (now one process-lifetime directory,
auto-cleaned at exit), `np.linalg.LinAlgError` added to the tool-layer
except tuples (it subclasses ValueError only on numpy ≥ 2), and a
boundary comment on numeric-string tolerance coercion. The reviewer also
independently reconstructed both worked examples (the synthetic matrix
byte-matches its seed recipe; AO2016 α₁ to 4e-5 of print) and ran the
full suite bare: 305 passed, exit 0.

## 5. Status and boundaries

A0–A22 + UI-1 complete; 305 tests green; CI installs the `ui` extra on
all three matrix cells. Nothing is hosted: the app is code + tests, and
every launch during development/review was transient and loopback-only.
Gated user decisions unchanged and untaken: the `v1.0.0` tag (proposal
ready), Kuntman package submission, egglog upstream, MCP hosting, any
exposure beyond localhost, licence.
