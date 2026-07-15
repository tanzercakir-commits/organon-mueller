# STAGE 17 — MCP Server + sympify GATE Hardening (Phase E 2/4)

**Date**: 2026-07-14 · **Mode**: autonomous · **Probe**: no mechanism; environment
probe done (mcp SDK 1.28.1 on pip; pdflatex available).

## 1. SECURITY FIRST — restricted srepr parser (`safe_parse.py`)

**Why sympify(evaluate=False)+whitelist is NOT ENOUGH** (the auditor will prove it):
sympify enters the Python `eval` path under all conditions; even if `global_dict`
is restricted, attribute-access chains from within a string and `__import__` derivatives
have historically produced escapes; the security boundary must be "never entering eval at all".

**Solution**: the srepr text is converted to an AST with Python `ast.parse`, and the AST
is built DIRECTLY into sympy objects by a WHITE-LIST walk (NO eval/sympify):
- Nodes: Expression, Call, Name, Constant(str|int|float|bool), USub.
- Call names: Symbol, Integer, Float, Rational, Add, Mul, Pow,
  conjugate. Bare names: I. NO other name (Function, exp, ...
  → rejection).
- Symbol name regex: `^[A-Za-z][A-Za-z0-9_]{0,63}$`; kwargs only
  boolean-valued allowed assumptions {real, positive, negative, complex,
  imaginary, integer} + `precision`(int) for Float.
- DoS guards: text ≤ 65536 characters; AST node count ≤ 2000;
  depth ≤ 64; numeric literal ≤ 4096 digits.
- `UnsafeExpressionError(reason)` — no silent rejection (K26).
- `hvector_from_dict` SWITCHES to this parser (the GATE closes; the docstring
  is updated); roundtrip: all 21 identities in the library +
  random HVectors srepr→parse→equal (tests).
- `tests/test_security.py`: injection corpus (__import__, os.system,
  exec/eval, attribute chain `().__class__...`, lambda, getattr, unknown
  function, kwarg smuggling, 10k-deep expression, 10^6-digit number) —
  all UnsafeExpressionError; no payload is evaluated (canary:
  no os.environ/file-system side effect).

## 2. MCP server (CODE + TEST; NO HOSTING — critical decision with the user)

- `mcp_server/tools.py` — PURE functions (tested without the SDK):
  `tool_decompose_mueller(payload)` (4×4 REAL float matrix; schema+finiteness
  +dimension — K26; symmetry param: fundamental/composite/"propose"),
  `tool_propose_hypotheses(payload)` (accepts covariance [re,im] pairs),
  `tool_guarded_campaign_info()` (current campaign findings with the M32
  table), `tool_generate_report(payload)` (LaTeX string from the previous
  tool's outputs; without sympify — only our own objects).
  Error responses: {"error": rationale} (does not leak exceptions, traceable).
- `mcp_server/server.py` — FastMCP wrapper (`mcp` optional extra;
  pyproject `[project.optional-dependencies] mcp`); test importorskip.
  Running: `python -m organon_mueller.mcp_server` (stdio) — in the README;
  hosting/expose decision WITH THE USER.
- Inputs NEVER go to sympify (number lists + enum strings);
  no free-text input.

## 3. Acceptance

test_security.py injection corpus (≥10 payloads) all rejected + roundtrip
21/21; hvector_from_dict now in the safe parser (existing behavior tests
stay green); tool schema/K26 guard tests (bad dimension, NaN, string
smuggling); FastMCP registration smoke (skipif no mcp); README-mcp; 215 existing
tests green; security-focused audit PASS.

**STOP HERE**
