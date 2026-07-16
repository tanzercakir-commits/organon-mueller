# Local web interface (`organon-ui`)

An interactive front end for the decomposition engine that runs entirely
on your own machine. No account, no service, no hosting, no cost.

## Install and run

```bash
pip install "organon-mueller[ui]"   # from PyPI (or from a clone: pip install -e ".[test,ui]")
organon-ui                          # opens http://127.0.0.1:7860 in your browser
```

Options: `organon-ui --port 8000` (different port), `organon-ui
--no-browser` (do not auto-open a tab).

## What it does

- **Editable 4×4 Mueller matrix** (spreadsheet-style grid — change any
  cell and re-run instantly). Example loaders: identity, an exact
  synthetic type-1 mixture (decomposes under the default tolerances with
  α₁ = 0.35), and the AO2016 §6 mixture (print-precision data; loading it
  also sets the documented tolerance preset).
- **Decompose** tab: pick a symmetry hypothesis (`type1/2/3`, composites
  `type1-2/1-3/2-3`) and the a/b/auto variant; get α₁ and the two
  component matrices, plus the full JSON details.
- **Propose hypotheses** tab: try every hypothesis the covariance rank
  admits; accepted results and rejected hypotheses each carry their
  reasons. Scores shown are an *ordering heuristic, not evidence* —
  acceptance is decided solely by the exact solvers.
- **File / batch** tab: load matrices from `.csv` / `.tsv` / `.txt`
  files. A 4×4 file loads straight into the editor; a wide-format batch
  file — one matrix per row, 16 columns (m00…m33, row-major) or 17
  columns (leading label such as wavelength + 16 entries) — can be
  decomposed in one go (per-row α₁ or failure reason, downloadable
  results CSV) or sampled row-by-row into the editor. UTF-8, decimal
  point, delimiter comma/semicolon/tab/whitespace, one optional header
  line, `#` comments; limits 5 MB / 10,000 matrices. The file is parsed
  strictly as numbers, locally.
- **LaTeX report** tab: generate the deterministic, evidence-labelled
  report for the current matrix and download the `.tex` source.

## Security posture

- The app binds to **127.0.0.1 only** and `share=False` is hard-coded —
  no tunnel, no public link, nothing ever leaves your machine. This is
  the Stage 18 posture (no hosted surface): the only listener is loopback
  on your own computer, reachable from that computer alone.
- The interface is a thin layer over the hardened numeric-only tool
  functions (`mcp_server/tools.py`): inputs are numbers and enum strings;
  no expression text crosses the boundary; every failure returns a
  readable reason, never a traceback.
- PDF compilation is deliberately not wired into the UI; the report tab
  serves the `.tex` source (compile it yourself if you have LaTeX).

## Evidence discipline

Numbers displayed in the interface are evidence class
*numeric-deterministic*; the symbolic proofs live in the test suite (see
`VERIFICATION.md`). Outputs beyond the published tables are *candidates* —
no novelty or physics claim is made; that judgement is reserved for human
experts (`novelty-protocol.md`, step 5).
