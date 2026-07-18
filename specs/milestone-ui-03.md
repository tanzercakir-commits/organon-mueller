# MILESTONE UI-3 — Lorentz transform tab (v1.3.0)

**Date**: 2026-07-18 · **Mode**: stage-gated interactive · **Language**:
English UI · **Isolation**: developed on branch `feature/lorentz-ui`
(main untouched until a reviewed PR merge)

## 1. Goal

Give the local interface a small, numeric interactive surface for the
Lorentz face: pick boost or rotation, enter the parameter and axis, get
Λ back with an honest validity badge. The 40-identity table and the
sweep stay reference material (`reports/`), not UI.

## 2. Decisions locked up front (anti-assumption)

- **Access surface: UI + MCP** — the tool is exposed both from the web
  UI and the MCP server (`server.py` `@app.tool()` + `mcp/__init__`
  re-export + the `test_fastmcp_wiring_smoke` exact-set updated to the
  5-name set). No half-wired function.
- **Version: 1.3.0 (minor)** — a new public function
  (`tool_lorentz_transform`) plus a new UI/MCP surface is new
  backward-compatible functionality; strict semver ⇒ minor.
- **Scope: minimal** — boost/rotation → Λ + validity badge + the
  computed α. No composition, no Z display (possible later).

## 3. Design

- **Tool** (`tool_lorentz_transform`, numeric-only, K26): axis
  NORMALIZED; Λ = ZZ* over the Σ basis from α = (cosh(φ/2),
  sinh(φ/2)·n̂) / (cos(θ/2), i·sin(θ/2)·n̂), evaluated numerically. A
  test PINS it to the symbolic engine at unit axes.
- **Overflow, handled from the start**: the hyperbolics use numpy (an
  out-of-range boost rapidity overflows to inf, it does NOT raise
  `OverflowError` — which is an `ArithmeticError`, not a `ValueError`,
  and would escape the K26 `except ValueError` guard). A single
  finiteness check on Λ turns both the overflow band and the inf/nan
  band into one readable reason. (This gap — a valid-but-extreme INPUT
  RANGE surfacing a downstream overflow that the error taxonomy didn't
  cover — is the lesson worth carrying: guarding input *form* does not
  cover input *range* effects.)
- **Validity badge** (physics-meaningful, not circular): ΛᵀgΛ = g
  residual, det Λ = +1, Λ₀₀ ≥ 1, imaginary-leak; "proper orthochronous
  Lorentz transformation" asserted only when all four pass. The
  Task-1/2 identities are NOT re-checked per input (they hold for every
  boost/rotation by construction — the symbolic-engine pin is the
  guardrail instead).
- **UI** (thin, no new parse path): a "Lorentz transform" tab — Radio
  (boost/rotation), `gr.Number` angle + 3 axis Numbers, a compute
  button; outputs α (Markdown), Λ (Dataframe), badge (Markdown). α
  NEVER enters as text.

## 4. Security posture (unchanged)

127.0.0.1 + share=False constants intact; no new file/parse surface;
the tool re-validates independently of the UI grid.

## 5. Acceptance

Tool + UI tests (validity for boost & rotation, the symbolic-engine
pin, axis normalization, all K26 guards incl. the overflow band,
English copy, real-Λ); the MCP exact-set test updated and green; full
suite green with updated counts; docs-guard re-run after the last doc
edit; adversarial review PASS; version 1.3.0 + tag proposal (tag +
Release remain USER actions). Merge to main only via a reviewed PR.

**STOP HERE**
