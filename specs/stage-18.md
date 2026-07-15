# STAGE 18 — Optional Web UI (static; NO HOSTING) (Phase E 3/4)

**Date**: 2026-07-14 · **Mode**: autonomous · **Probe**: no mechanism; environment
probe (playwright + node available → headless render smoke is done).

## 1. Scope DECISION (reasoned)

**STATIC single file `web/index.html`** — inline CSS+JS, no CDN, NO server,
NO hosting (continuation of the A17 security line: server surface = attack
surface; a static file has no attack surface). Consistent with the user's vision ("the end
user cannot use a terminal"): opens in the browser with a double-click.

**Where the computation lives**: numpy/sympy are not in the browser. Option (a) HONEST SCOPE
was chosen (NOT pyodide — ~10MB download + sympy build complexity; it gives the dishonest
impression of a "full browser engine"): the page is a **result
VIEWER** — the user pastes the MCP/CLI tool output (JSON), and the
page renders it safely as tables/matrices. A "Load example" button with embedded
SAMPLE JSON (works without a download). It also shows the report
generator's LaTeX output (if any) in a monospace block.
The boundary is written honestly: "the computation is in the Python package; this page is presentation."

## 2. Security (XSS — A17 spirit)

- User input/JSON CONTENT is printed only via `textContent`;
  `innerHTML` is NEVER USED anywhere with user data (except the fixed skeleton).
  The DOM is built with `createElement`/`textContent`.
- `JSON.parse` try/catch; error message via textContent.
- Numeric fields are filtered through `Number.isFinite`; unexpected keys
  are not silently skipped, they are DISPLAYED as "unrecognized field" (K21 spirit).
- `<meta http-equiv="Content-Security-Policy" content="default-src
  'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'">` —
  no network, only inline; external resources cannot be fetched.
- No `eval`/`Function`/`setTimeout(string)` at all.

## 3. Test (`tests/test_web_ui.py`)

- Structural: file exists; CSP meta; expected element ids (json input,
  render target, example button); NO `innerHTML` user-data pattern
  (source scan: `innerHTML =` only fixed/sanitized); no `eval(`/
  `Function(`.
- Sample JSON schema conformance: the embedded sample is consistent with the MCP tool output schema
  (call the tool and compare the key set).
- **Headless render smoke** (playwright available): open the page, load the example,
  expected text in the render target; **XSS payload test**: put a string like
  `<img src=x onerror=alert(1)>` / `"</script>"` into the JSON →
  SCRIPT does not run in the DOM, it appears as text (textContent proof);
  no error/alert in the console. (skipif no playwright, structural is enough.)

## 4. Acceptance

Static file + CSP; XSS-safe render (the headless payload test does not run script);
sample JSON consistent with the tool schema; boundary-honesty text on the
page; 268 existing tests green; XSS-focused audit PASS.

**STOP HERE**
