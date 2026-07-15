"""Stage-18: static web viewer — structural + XSS-safety tests."""
import json
import pathlib
import re

import numpy as np
import pytest
import sympy as sp

ROOT = pathlib.Path(__file__).resolve().parent.parent
HTML = ROOT / "web" / "index.html"


def _html():
    return HTML.read_text()


# -- structural -------------------------------------------------------------------

def test_page_exists_and_core_elements():
    src = _html()
    for token in ('id="json-input"', 'id="render-btn"', 'id="example-btn"',
                  'id="output"', 'id="example-data"'):
        assert token in src, token
    assert "Content-Security-Policy" in src
    assert "default-src 'none'" in src


def test_no_network_or_dynamic_code():
    src = _html()
    # no eval / Function / string-timers / remote resources
    assert "eval(" not in src
    assert re.search(r"\bnew Function\b", src) is None
    assert "http://" not in src and "https://" not in src.replace(
        'http-equiv', '')  # CSP attr is not a URL
    assert "fetch(" not in src and "XMLHttpRequest" not in src


def test_user_data_never_via_innerhtml():
    """The only mutations of user/JSON data go through textContent (el()
    helper) — no `innerHTML =` anywhere (XSS boundary)."""
    src = _html()
    # ignore comments/prose; check only executable lines for HTML sinks
    code_lines = [ln for ln in src.splitlines()
                  if "//" not in ln and "<!--" not in ln and "---" not in ln]
    code = "\n".join(code_lines)
    for sink in ("innerHTML", "insertAdjacentHTML", "document.write",
                 "outerHTML"):
        assert sink not in code, f"HTML sink {sink} in executable code"
    # the safe helper is present and uses textContent
    assert "e.textContent = String(text)" in src


# -- example JSON is schema-consistent with the real tools ------------------------

def test_embedded_example_matches_tool_schema():
    src = _html()
    m = re.search(r'id="example-data"[^>]*>(.*?)</script>', src, re.S)
    assert m, "example-data script block not found"
    example = json.loads(m.group(1))
    assert "decompose_mueller" in example and "propose_hypotheses" in example

    from organon_mueller.mcp_server import (
        tool_decompose_mueller, tool_propose_hypotheses,
    )
    from organon_mueller.decomposition.rank3 import _template_numeric
    from organon_mueller.decomposition.covariance import (
        mueller_from_standard_covariance,
    )

    rng = np.random.default_rng(20260713)
    x = float(rng.uniform(0.15, 0.85))
    w = np.sqrt(x * (1 - x)) * np.exp(1j * float(rng.uniform(0, 2 * np.pi)))
    h1 = _template_numeric("type1", x, w)
    u = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    u /= np.linalg.norm(u)
    cov = 0.4 * h1 + 0.6 * np.outer(u, u.conj())
    m_arr = np.array(sp.matrix2numpy(
        mueller_from_standard_covariance(sp.Matrix(cov)).evalf(),
        dtype=complex)).real
    real_dec = tool_decompose_mueller(
        {"mueller": m_arr.tolist(), "symmetry": "type1"})
    # embedded example carries the SAME keys the live tool produces
    assert set(example["decompose_mueller"]) >= {"kind", "symmetry", "alpha1",
                                                 "m1", "m2"}
    assert set(real_dec) >= set(example["decompose_mueller"]) - {"note"}
    prop = example["propose_hypotheses"]
    assert set(prop) >= {"rank", "scores", "accepted", "rejected", "note"}


# -- headless render + XSS payload (playwright optional) --------------------------

def _render_with_playwright(json_text):
    from playwright.sync_api import sync_playwright

    errors = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.on("console", lambda msg: errors.append(msg.text)
                if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        dialogs = []
        page.on("dialog", lambda d: (dialogs.append(d.message), d.dismiss()))
        page.goto(HTML.as_uri())
        page.fill("#json-input", json_text)
        page.click("#render-btn")
        page.wait_for_timeout(200)
        out_text = page.inner_text("#output")
        html_out = page.inner_html("#output")
        browser.close()
    return out_text, html_out, errors, dialogs


def test_headless_example_renders():
    pytest.importorskip("playwright")
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
        import subprocess
        subprocess.run(["playwright", "install", "chromium"],
                       capture_output=True, timeout=180)
    except Exception:
        pytest.skip("playwright chromium unavailable")
    src = _html()
    example = re.search(r'id="example-data"[^>]*>(.*?)</script>', src, re.S).group(1)
    try:
        out_text, _, errors, dialogs = _render_with_playwright(example.strip())
    except Exception as exc:
        pytest.skip(f"headless browser unavailable: {exc}")
    assert "decomposition" in out_text.lower()
    assert "type1" in out_text
    assert not errors and not dialogs


def test_headless_xss_payload_is_inert():
    """A JSON string carrying an XSS payload must render as TEXT — no
    script execution, no dialog, no injected <img>/<script> element."""
    pytest.importorskip("playwright")
    try:
        import subprocess
        subprocess.run(["playwright", "install", "chromium"],
                       capture_output=True, timeout=180)
    except Exception:
        pytest.skip("playwright chromium unavailable")
    payload = json.dumps({
        "propose_hypotheses": {
            "rank": 2, "scores": {}, "accepted": [],
            "rejected": [{"hypothesis": "<img src=x onerror=alert(1)>",
                          "reason": "</script><script>alert(2)</script>"}],
            "note": "<b>not bold</b>",
        }})
    try:
        out_text, html_out, errors, dialogs = _render_with_playwright(payload)
    except Exception as exc:
        pytest.skip(f"headless browser unavailable: {exc}")
    assert not dialogs, "XSS executed a dialog!"
    assert not errors
    # the payload appears as literal text (escaped by the DOM)...
    assert "<img" in out_text or "onerror" in out_text
    # ...and NOT as a live element or unescaped markup
    assert "<img" not in html_out.lower()
    assert "<script" not in html_out.lower()
    assert "&lt;img" in html_out.lower() or "&lt;b&gt;" in html_out.lower()


def test_headless_prototype_keys_shown_not_dropped():
    """Review D1: a field named __proto__/constructor must be SHOWN as an
    unrecognized field (K21), not crash render or get silently swallowed."""
    pytest.importorskip("playwright")
    try:
        import subprocess
        subprocess.run(["playwright", "install", "chromium"],
                       capture_output=True, timeout=180)
    except Exception:
        pytest.skip("playwright chromium unavailable")
    payload = ('{"decompose_mueller":{"kind":"DecompositionResult",'
               '"symmetry":"type1","alpha1":0.4,"m1":[[1]],"m2":[[1]]},'
               '"constructor":{"x":1},"__proto__":{"y":2}}')
    try:
        out_text, html_out, errors, dialogs = _render_with_playwright(payload)
    except Exception as exc:
        pytest.skip(f"headless browser unavailable: {exc}")
    assert not errors and not dialogs           # no crash
    low = out_text.lower()                       # .label is CSS-uppercased
    assert "type1" in low                        # the real field still renders
    assert "unrecognized field" in low           # proto keys shown, not dropped
    assert "constructor" in low


def test_headless_deep_nesting_graceful():
    """Review D2: a deeply-nested unrecognized field must not blank the
    page with an uncaught RangeError."""
    pytest.importorskip("playwright")
    try:
        import subprocess
        subprocess.run(["playwright", "install", "chromium"],
                       capture_output=True, timeout=180)
    except Exception:
        pytest.skip("playwright chromium unavailable")
    deep = "[" * 4000 + "]" * 4000
    payload = '{"weird":' + deep + '}'
    try:
        out_text, html_out, errors, dialogs = _render_with_playwright(payload)
    except Exception as exc:
        pytest.skip(f"headless browser unavailable: {exc}")
    assert not dialogs
    low = out_text.lower()
    # either it stringifies, or it shows a graceful message — never blank+crash
    assert ("unrecognized field" in low
            or "unrenderable" in low or "could not render" in low)
