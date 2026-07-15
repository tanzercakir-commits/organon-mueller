# User guide

This guide is task-oriented and assumes no command-line fluency. The maths
lives in a Python package; you reach it through one of three surfaces.

## Which surface do I want?

- **I want to read results in a browser, no terminal** → the static web viewer
  (`web/index.html`). Someone runs a tool for you (or you use the MCP surface
  below), and you paste the JSON output into the page.
- **I use an AI assistant that speaks MCP** → the MCP server. It exposes the
  decomposition, hypothesis, discovery-info, and report tools.
- **I write Python** → import the package directly.

Nothing here is hosted for you: the MCP server and web page are code you (or a
collaborator) run locally. That is a deliberate security choice.

## Which question → which tool?

| You have… | You want… | Tool |
|---|---|---|
| a depolarizing Mueller matrix | its symmetric + generic components | `decompose_mueller` |
| a Mueller/covariance matrix, unsure of its symmetry | every hypothesis that fits, ranked, with reasons for rejections | `propose_hypotheses` |
| curiosity about the guarded-identity channel | the current Horn-conditional findings (candidates) | `guarded_campaign_info` |
| a result to hand to a colleague | a deterministic, evidence-labelled LaTeX report | `generate_report` |

## Reading a result

Every result carries an **evidence label**:

- **symbolic-proof** — exact (the equation was proved symbolically).
- **numeric-deterministic** — checked at seeded sample points (practical
  certainty for polynomial-type identities, but not a proof).
- **candidate** — beyond the published results; **no** novelty or physics
  claim is made. Deciding whether a candidate is interesting or new is a human
  judgement (the novelty protocol's final step).

A rank-3 decomposition is reported as *a* decomposition consistent with the
requested symmetry pair, **not** *the* decomposition — rank-3 results are not
unique across pair hypotheses.

## The web viewer

1. Open `web/index.html` in any browser (double-click; no install, no network).
2. Paste a tool's JSON output into the box, or press **Load example**.
3. Press **Render**. You get the weights, component matrices, the ranked
   hypothesis table (with rejection reasons), and any LaTeX report.

The page performs no computation and sends nothing anywhere; it renders pasted
text safely (as text, never as markup).

## The MCP server

Install and run locally:

```bash
pip install -e ".[mcp]"
python -m organon_mueller.mcp_server      # stdio transport
```

To use it from an assistant, register it (see
[`README-mcp.md`](README-mcp.md) for the config snippet and the full tool
table). Inputs are numbers and enum strings only; on bad input the tools
return `{"error": "<reason>"}` rather than failing opaquely.

## The Python package

```python
import numpy as np
from organon_mueller.decomposition import decompose
from organon_mueller.decomposition.rank3 import propose_decompositions

r = decompose(mueller=my_matrix, symmetry="type1")
print(r.alpha1, r.m1, r.m2)

report = propose_decompositions(my_covariance)   # ranked hypotheses + reasons
```

To generate a LaTeX report:

```python
from organon_mueller.reporting import Report, decomposition_section
tex = Report(title="my report", date="2026-07-14").add(
    decomposition_section(r)).to_latex()
```

## Trust

Read [`VERIFICATION.md`](VERIFICATION.md): it lists exactly what "verified"
means here and where the limits are. The short version: nothing reaches the
main branch without passing symbolic and numeric checks, regression against
the source papers, and an independent adversarial review.
