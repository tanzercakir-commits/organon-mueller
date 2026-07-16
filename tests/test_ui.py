"""Milestone UI-1: the local web interface.

Module-gated on gradio (same pattern as the egglog-gated discovery
modules): without the ``ui`` extra this file does not collect, and the
doc-count drift guard accounts for it via _full_optional_stack.

The security-relevant assertions are the point here: the launch kwargs
must pin 127.0.0.1 and share=False (Stage 18 posture — no hosted
surface), and every failure must surface as a readable reason (K26),
never a traceback.
"""
import json

import pytest

gr = pytest.importorskip("gradio")

from organon_mueller.ui import app as ui  # noqa: E402


# -- app assembly ------------------------------------------------------------------

def test_build_app_returns_blocks():
    app = ui.build_app()
    assert isinstance(app, gr.Blocks)


# -- security posture (the load-bearing tests) -------------------------------------

def test_launch_binds_loopback_only_and_never_shares():
    """main() must launch with server_name=127.0.0.1 and share=False —
    asserted on the EXACT kwargs passed to launch, via injection (no
    socket is opened)."""
    captured = {}

    def fake_launch(app, kwargs):
        captured["app"] = app
        captured["kwargs"] = kwargs

    ui.main(argv=["--port", "7999", "--no-browser"], _launch=fake_launch)
    kw = captured["kwargs"]
    assert kw["server_name"] == "127.0.0.1"
    assert kw["share"] is False
    assert kw["server_port"] == 7999
    assert kw["inbrowser"] is False
    assert isinstance(captured["app"], gr.Blocks)


def test_launch_kwargs_all_exist_in_real_launch_signature():
    """Injected-launch tests can't catch a kwarg the REAL Blocks.launch
    rejects (found live: gradio 6 removed show_api and organon-ui would
    have crashed at startup). Every launch_kwargs key must exist in the
    installed gradio's launch signature."""
    import inspect

    real = set(inspect.signature(gr.Blocks.launch).parameters)
    unknown = set(ui.launch_kwargs()) - real
    assert not unknown, f"launch_kwargs not accepted by Blocks.launch: {unknown}"


def test_security_constants_are_pinned():
    """The posture is constants, not parameters: launch_kwargs exposes no
    way to change the bind address or enable sharing."""
    import inspect

    assert ui.HOST == "127.0.0.1"
    assert ui.SHARE is False
    params = inspect.signature(ui.launch_kwargs).parameters
    assert set(params) == {"port", "open_browser"}      # nothing else
    kw = ui.launch_kwargs()
    assert kw["server_name"] == "127.0.0.1" and kw["share"] is False


# -- decompose callback ------------------------------------------------------------

def test_decompose_cb_synthetic_type1_default_tolerances():
    s, m1, m2, det = ui.decompose_cb(
        ui.synthetic_type1(), "type1", "auto", 1e-9, 1e-6, 1e-6)
    assert not s.startswith(ui.STRINGS["err_prefix"])
    payload = json.loads(det)
    assert abs(payload["alpha1"] - 0.35) < 1e-6
    assert len(m1) == 4 and all(len(r) == 4 for r in m1)
    assert len(m2) == 4 and all(len(r) == 4 for r in m2)


def test_decompose_cb_ao2016_preset_reproduces_paper_alpha():
    p = ui.AO2016_PRESET
    s, m1, m2, det = ui.decompose_cb(
        ui.ao2016_mixture(), p["symmetry"], p["variant"],
        p["rank_tol"], p["psd_tol"], p["rank1_tol"])
    assert not s.startswith(ui.STRINGS["err_prefix"])
    assert abs(json.loads(det)["alpha1"] - 0.3) < 1e-3   # print precision


def test_decompose_cb_bad_shape_returns_reason_not_traceback():
    s, m1, m2, det = ui.decompose_cb(
        [[1, 2, 3]] * 3, "type1", "auto", None, None, None)
    assert s.startswith(ui.STRINGS["err_prefix"]) and "4x4" in s
    assert det == "{}"


def test_decompose_cb_non_decomposable_returns_reason():
    """A pure (rank-1) matrix has nothing to split — the solver's K26
    reason must surface in the UI string."""
    s, *_ = ui.decompose_cb(
        ui.identity_matrix(), "type1", "auto", None, None, None)
    assert s.startswith(ui.STRINGS["err_prefix"]) and "rank" in s


def test_decompose_cb_bad_cell_types():
    bad = ui.identity_matrix()
    bad[2][3] = "not-a-number"
    s, *_ = ui.decompose_cb(bad, "type1", "auto", None, None, None)
    assert s.startswith(ui.STRINGS["err_prefix"]) and "[2][3]" in s
    bad[2][3] = None
    s2, *_ = ui.decompose_cb(bad, "type1", "auto", None, None, None)
    assert s2.startswith(ui.STRINGS["err_prefix"]) and "[2][3]" in s2


# -- propose callback --------------------------------------------------------------

def test_propose_cb_exact_rank2_accepts_type1():
    md, js = ui.propose_cb(ui.synthetic_type1())
    payload = json.loads(js)
    assert payload["rank"] == 2
    assert any(a["hypothesis"].startswith("type1")
               for a in payload["accepted"])
    # the honesty note travels into the UI verbatim
    assert "ordering heuristic" in md


def test_propose_cb_error_path():
    md, js = ui.propose_cb(None)
    assert md.startswith(ui.STRINGS["err_prefix"])
    assert js == "{}"


# -- report callback ---------------------------------------------------------------

def test_report_cb_emits_latex_and_tex_file(tmp_path):
    tex, path, status = ui.report_cb(
        ui.synthetic_type1(), "type1", "auto", "UI test report")
    assert not status.startswith(ui.STRINGS["err_prefix"])
    assert "\\documentclass" in tex and "UI test report" in tex
    assert str(path).endswith(".tex")
    from pathlib import Path
    assert Path(path).read_text() == tex


def test_report_cb_passes_tolerances_for_print_precision_data():
    """Without the tolerance passthrough the AO2016 print-precision data
    cannot be reported at all — regression for the UI-1 tools.py change."""
    p = ui.AO2016_PRESET
    tex, path, status = ui.report_cb(
        ui.ao2016_mixture(), p["symmetry"], p["variant"], "AO2016",
        p["rank_tol"], p["psd_tol"], p["rank1_tol"])
    assert not status.startswith(ui.STRINGS["err_prefix"])
    assert "\\documentclass" in tex


def test_report_cb_error_path():
    tex, path, status = ui.report_cb(
        ui.identity_matrix(), "type1", "auto", "x")
    assert status.startswith(ui.STRINGS["err_prefix"])
    assert tex == "" and path is None


# -- language & copy discipline ----------------------------------------------------

def test_ui_copy_is_english_only():
    """User decision (2026-07-16): the interface language is English —
    international audience expected. Guard: no Turkish-specific letters
    in any UI string."""
    turkish = set("çÇğĞıİöÖşŞüÜ")
    for key, text in ui.STRINGS.items():
        assert not (set(text) & turkish), f"non-English copy in {key!r}"


def test_ui_footer_keeps_evidence_discipline():
    """The A15 verb-discipline extends to the UI: the footer must carry
    the evidence-class framing, the no-claim note, and the score caveat."""
    footer = ui.STRINGS["footer"]
    assert "numeric-deterministic" in footer
    assert "candidate" in footer
    assert "novelty" in footer
    assert "ordering heuristic" in footer
    assert "127.0.0.1" in footer
