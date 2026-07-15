# STAGE 17 — REPORT (MCP Server + sympify GATE Hardening)

**Date**: 2026-07-14 · **Spec**: `specs/stage-17.md` · **Mode**: autonomous
**Result**: COMPLETED — 268/268 tests green; **STAGE-2 GATE CLOSED**
(restricted srepr parser that never enters eval); MCP tool surface + server code
(NOT HOSTED — critical decision with the user); security audit PASS after FIVE rounds.

## 1. Deliverables

- **`safe_parse.py`** — restricted srepr parser: `ast.parse` + WHITE-LIST
  walk; **NO eval/sympify on the text path** (reviewer proved with a canary:
  0 sympify-on-string calls). `serialize.hvector_from_dict`
  now passes through here; the GATE docstring was updated to "CLOSED".
- **`mcp_server/`** — PURE tool functions (tested without the SDK):
  decompose_mueller / propose_hypotheses / guarded_campaign_info /
  generate_report; inputs are only numbers + enum strings (the expression-text boundary
  is never crossed); errors are `{"error": reason}` (no trace leak). FastMCP
  wrapper (`[mcp]` optional extra); `python -m
  organon_mueller.mcp_server` (stdio) — README-mcp.md.
- **NO HOSTING**: the server is not started/exposed anywhere;
  the run/share decision is with the user (critical-decision protocol).

## 2. Security audit — FIVE rounds (security boundary, to the end)

The reviewer attacked with malicious inputs; each round a new hole, each hole
closed, the same reviewer attacked again:
- **Round 1**: anti-eval sound BUT 5 holes — D1 (DoS magnitude), D2 (raw
  MemoryError leak), D3 (tool tolerance TypeError leak), D4 (non-finite passthrough),
  D5 (regex \n bypass).
- **Round 2**: D2-D5 closed, D1 half (exponent bounded but not the result)
  + regression (small Float sreprs broke).
- **Round 3**: D1 result-magnitude projection + regression fixed;
  S1 (Float exponent materialize) + S2 (Mul-fold materialize) remained.
- **Round 4**: S1/S2 closed with pre-fold projection; a non-integer Pow
  exponent class (Float/large Rational) was found.
- **Round 5**: every exponent type + numeric atoms embedded in the base were
  projected → **PASS**. The reviewer swept the entire remaining surface (symbolic-base^huge,
  exponent-folding order, nested Pow, negative/I base, conjugate);
  none materialize a huge number/burn >1s/execute code.

Guards: text ≤64KB, nodes ≤2000, depth ≤64, digits ≤4096, bits
≤16384, exponent ≤10⁶; Symbol regex fullmatch; non-finite rejected; Float
exponent forbidden; Pow/Mul/Add pre-fold magnitude projection. The legitimate
library corpus (220 expressions) roundtrips losing nothing.

## 3. Next stage (autonomous continuation)

**Stage 18 — Optional web UI**: static HTML+JS demo page (NO hosting
— the same critical-decision rule); browser display of the MCP tools/report generator.
Scope decision in the spec (static + client-side vs
server-dependent — static is recommended for security reasons).
