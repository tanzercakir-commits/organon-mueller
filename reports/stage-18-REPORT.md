# STAGE 18 — REPORT (Optional Web UI — static, hosting-free)

**Date**: 2026-07-14 · **Spec**: `specs/stage-18.md` · **Mode**: autonomous
**Result**: COMPLETED — 276/276 tests green; `web/index.html` static result
viewer; XSS-focused audit (2 rounds) PASS; NOT HOSTED.

## 1. Deliverables

- **`web/index.html`** — single file, inline CSS+JS, no CDN, NO server.
  The user pastes MCP/CLI tool output (JSON) → decomposition weights,
  component matrices, propose score-table (with justified rejections), report
  LaTeX are rendered safely. Embedded "Load example" (real
  tool output, schema-consistent). The boundary is written honestly: "computation is in the Python
  package; this page is presentation only."
- **Scope decision**: NOT pyodide (honesty + lightness) — presentation layer;
  computation is in the backend. NO hosting (the A17 security line; a server surface =
  attack surface).

## 2. Security

- **XSS boundary**: user/JSON data is printed ONLY via `textContent`
  (`el()` helper); NO `innerHTML`/`insertAdjacentHTML`/`document.write`.
  The reviewer tried 247 payloads (19 fields × 13 vectors): none
  executed a script/opened a dialog/injected a live element.
- **CSP**: `default-src/img-src/connect-src 'none'` → network EGRESS blocked
  (external `<img>`/`fetch` rejected with "csp"); honest note: CSP's job is
  egress, NOT an XSS backstop (textContent is the real boundary — explicit in the document).
- **NO prototype pollution**: `KNOWN = Object.create(null)` + `typeof
  === "function"` guard; `__proto__`/`constructor` keys are
  DISPLAYED as "unrecognized field" (K21), not crashed/silently dropped.
- No `eval`/`Function`/`fetch`/`XMLHttpRequest`.

## 3. Independent audit (2 rounds)

Round 1: **PASS** (security) + 3 robustness defects — D1 (proto-chain
lookup: __proto__ crash / constructor silent swallow, K21 violation), D2
(deep-nested JSON.stringify RangeError → blank page), D3 (CSP unsafe-
inline is not an XSS backstop — informational). Round 2: **PASS** — D1
fixed with `Object.create(null)`, D2 with full-body try/catch + safeStringify;
D3 documented honestly (instead of a script-hash — it would be
fragile in a static file); the non-string note edge was also closed. The reviewer
attacked prototype-chain keys and 500k-depth payloads again — all graceful (≤0.69s),
no pollution, no egress.

## 4. Next stage (autonomous continuation)

**Stage 19 — docs**: user guide + installation + API overview +
architecture (layers: algebra → identities → discovery → decomposition →
dipoles → reporting → mcp_server → web; the verification contract; packaging
three surfaces: package/MCP/web). README the main entry; preparation for Phase F
(A20 consolidation, A21 external verification, A22 v2.0 closure).
