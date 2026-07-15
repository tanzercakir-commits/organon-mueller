# MCP server — how to run (user decision; NOT hosted by default)

The MCP surface is code + tests only. Running or exposing it anywhere is
YOUR decision (critical-decision protocol): the repo never starts it.

## Install & run (stdio)

```bash
pip install -e ".[mcp]"           # optional extra
python -m organon_mueller.mcp_server
```

## Claude Desktop config snippet

```json
{
  "mcpServers": {
    "organon-mueller": {
      "command": "python",
      "args": ["-m", "organon_mueller.mcp_server"]
    }
  }
}
```

## Tools

| tool | input | output |
|---|---|---|
| `decompose_mueller` | real 4x4 Mueller list, symmetry (`type1..type2-3`), variant | weights + component Mueller matrices, or `{"error": reason}` |
| `propose_hypotheses` | `mueller` (reals) or `covariance` ([re,im] pairs) | rank, ordering scores, accepted results, REASONED rejections |
| `guarded_campaign_info` | — | M32 evidence quadruples (candidates; no novelty claims) |
| `generate_report` | mueller + title/date (+`compile_pdf`) | deterministic LaTeX (evidence-labeled blocks) |

## Security contract

Inputs are numbers and enum strings only — no expression text crosses
the boundary, so nothing can reach `sympify`. The serialization layer is
independently hardened (restricted srepr parser, `safe_parse.py`;
injection corpus in `tests/test_security.py`). Errors return reasons,
never tracebacks.
