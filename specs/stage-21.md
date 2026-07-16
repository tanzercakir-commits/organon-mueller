# STAGE 21 — External Validation (Phase F)

**Date**: 2026-07-15 · **Mode**: autonomous · **Language**: English

## 1. Goal

Validate the frozen artifact from the outside. Three questions, none of
which may be answered by re-running our own happy path: (a) does the trust
anchor — tests + CI — actually hold across the *full* support matrix, not
just the one interpreter this box happens to run; (b) is the outward-facing
Kuntman feedback package internally consistent and honest; (c) do the
headline results reproduce when a second party re-derives them from
scratch.

## 2. Work items

### 2.1 CI / drift-guard realism across the 3-version matrix

- `.github/workflows/ci.yml`: matrix `["3.10", "3.11", "3.12"]`,
  `pip install -e ".[test,discovery,mcp]"`, bare `pytest`. `discovery`
  (egglog) installs only on ≥ 3.11 via its marker; `playwright` (web UI)
  and `pdflatex` (PDF compile) are intentionally NOT installed — those
  tests self-skip, so the matrix stays fast and the skips are honest
  optionality.
- The doc-count drift guard (`test_stated_test_count_matches_collection`)
  must be environment-robust: on a FULL optional stack (egglog + mcp +
  playwright importable) assert the collected count EQUALS the advertised
  number; on a partial environment (typical 3.10, or CI without
  mcp/playwright) assert collection never EXCEEDS the claim — so adding a
  test without bumping the docs is still caught everywhere.
- The MCP tool `tool_guarded_campaign_info` must degrade gracefully
  without egglog: egglog is imported lazily inside `engine.py` at module
  load, so a bare `ModuleNotFoundError` can surface at the CALL, not just
  the import. Wrap both and return `{"error": ...}` (K26: a reason, never
  a leaked traceback). Lock with a subprocess regression test that blocks
  egglog and asserts the graceful error.

### 2.2 Kuntman package outward-readiness review

Final consistency pass over `docs/kuntman-package/` (README-en/tr,
ADDENDUM-dipoles-en/tr, demo.py, sample-report.tex) together with the
top-level README and `docs/candidate-findings.md`: no internal
contradiction, every mathematical claim carries its evidence class
(verified / candidate), and every gated item (package submission, egglog
upstream draft, MCP hosting, web exposure) stays explicitly the user's
decision.

### 2.3 Independent reproduction of the headline results

An adversarial reviewer re-derives the headline theorems from scratch —
the covariance reshuffle, fragment-completeness, general Perrin
reciprocity, δ=0 ⇒ γ_z ≡ 0, and {2,3} rank-3 uniqueness — with a
from-scratch implementation, and must MATCH the repository's results.

## 3. Acceptance

- Full suite green; CI green on all three cells (3.10 collects the
  non-egglog subset, 3.11/3.12 collect the full suite).
- Package internally consistent: no "planned / next-phase" language for
  work already delivered; every adversarial finding fixed and
  re-verified to PASS by the SAME reviewer (FAIL → fix → re-verify with
  the same reviewer — the standing discipline).
- Independent theorem reproduction all MATCH.
- No novelty/physics claim added (novelty-protocol step 5 stays human);
  submission / hosting / version-tagging remain user decisions.

**STOP HERE**
