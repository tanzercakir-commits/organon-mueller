"""Stage-16: deterministic LaTeX report generator."""
import shutil

import numpy as np
import pytest
import sympy as sp

from organon_mueller.reporting import (
    EVIDENCE_LABELS,
    Report,
    ReportBlock,
    compile_pdf,
    decomposition_section,
    dipole_section,
    guarded_finding_section,
    propose_section,
)
from organon_mueller.reporting.report import latex_escape

RNG_SEED = 20260713


def _rank2_cov():
    from organon_mueller.decomposition.rank3 import _template_numeric

    rng = np.random.default_rng(RNG_SEED)
    x = float(rng.uniform(0.15, 0.85))
    w = np.sqrt(x * (1 - x)) * np.exp(1j * float(rng.uniform(0, 2 * np.pi)))
    h1 = _template_numeric("type1", x, w)
    u = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    u /= np.linalg.norm(u)
    return 0.4 * h1 + 0.6 * np.outer(u, u.conj())


# -- evidence discipline ---------------------------------------------------------

def test_unknown_evidence_label_raises():
    with pytest.raises(ValueError, match="evidence"):
        ReportBlock(title="x", evidence="proven-forever", source="s", body="b")


def test_verbs_follow_evidence_class():
    tex = ReportBlock(title="t", evidence="numeric-deterministic",
                      source="s", body="b").to_latex()
    assert "verified numerically" in tex and "proven symbolically" not in tex
    tex = ReportBlock(title="t", evidence="candidate",
                      source="s", body="b").to_latex()
    assert "CANDIDATE" in tex and "claim" in tex


def test_subthreshold_magnitudes_scientific_not_zero():
    """Review D1: machine-precision residuals must never print as "0"
    (an exactness claim). Sub-1e-6 magnitudes render scientifically."""
    from organon_mueller.reporting.report import _fmt

    assert "10^{-16}" in _fmt(6.66e-16)
    assert _fmt(0) == "0" and _fmt(0.25) == "0.25"
    assert "10^{-18}" in _fmt(9.09e-18)
    with pytest.raises(ValueError, match="non-finite"):
        _fmt(float("nan"))
    tex = dipole_section({"coplanar": 1.3e-17, "offplane": 4.6e-3},
                         {"chiral_mean_abs": 1.1e-2,
                          "achiral_mean_abs": 6.3e-6,
                          "uncoupled_pointwise": 9e-18}).to_latex()
    assert "10^{-17}" in tex and "10^{-18}" in tex


def test_escape():
    s = latex_escape("50% of a_b & {c} #1 ~x^2 $5")
    for raw in ("50\\%", "a\\_b", "\\&", "\\{c\\}", "\\#1"):
        assert raw in s


# -- determinism -----------------------------------------------------------------

def test_report_deterministic_and_timestamp_free():
    from organon_mueller.decomposition import decompose

    r = decompose(covariance=_rank2_cov(), symmetry="type1")
    def build():
        return (Report(title="det-test", date="2026-07-14")
                .add(decomposition_section(r)).to_latex())
    a, b = build(), build()
    assert a == b                       # byte-identical
    assert "\\today" not in a
    assert "2026-07-14" in a


# -- sections --------------------------------------------------------------------

def test_all_three_decomposition_types_render():
    from organon_mueller.decomposition import decompose
    from organon_mueller.decomposition.composite import decompose_composite
    from organon_mueller.decomposition.rank3 import (
        PAIR_13, _template_numeric, decompose_rank3,
    )

    tex1 = decomposition_section(
        decompose(covariance=_rank2_cov(), symmetry="type1")).to_latex()
    assert "\\alpha_1" in tex1 and "pmatrix" in tex1

    rng = np.random.default_rng(RNG_SEED)

    def pure(sym):
        total = 1.0 if sym == "type1" else 0.5
        x = float(rng.uniform(0.15, total - 0.15))
        w = np.sqrt(x * (total - x)) * np.exp(1j * float(rng.uniform(0, 2 * np.pi)))
        return _template_numeric(sym, x, w)

    def gen():
        u = rng.standard_normal(4) + 1j * rng.standard_normal(4)
        u /= np.linalg.norm(u)
        return np.outer(u, u.conj())

    # composite 1-2 mixture
    u1 = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    u1[2] = u1[1]
    u1 /= np.linalg.norm(u1)
    cov = 0.4 * np.outer(u1, u1.conj()) + 0.6 * gen()
    r2 = decompose_composite(cov, "type1-2")
    tex2 = decomposition_section(r2).to_latex()
    assert "type1-2" in tex2

    cov3 = 0.3 * pure("type1") + 0.35 * pure("type3") + 0.35 * gen()
    r3 = decompose_rank3(cov3, PAIR_13)
    tex3 = decomposition_section(r3).to_latex()
    assert "type1+type3" in tex3
    assert "A decomposition" in tex3    # non-uniqueness note


def test_propose_section_reasons_and_framing():
    from organon_mueller.decomposition.rank3 import propose_decompositions

    rep = propose_decompositions(_rank2_cov())
    tex = propose_section(rep).to_latex()
    assert "hypothesis & score & outcome" in tex
    assert "ORDERING heuristic" in tex           # score != truth framing
    assert tex.count("rejected") >= 1            # reasons present


def test_guarded_finding_section_candidate_language():
    pytest.importorskip("egglog")
    from organon_mueller.discovery.guards import run_guarded_campaign

    finding = run_guarded_campaign()[0]
    tex = guarded_finding_section(finding).to_latex()
    assert "CANDIDATE" in tex
    assert "conditional identity" in tex
    assert tex.count("yes") >= 2 and tex.count("no") >= 2  # M32 quadruple
    assert "20260713" in tex                     # reproduction seed


def test_dipole_section_renders():
    tex = dipole_section({"coplanar": 1.3e-17, "offplane": 4.6e-3},
                         {"chiral_mean_abs": 1.1e-2,
                          "achiral_mean_abs": 6.3e-6,
                          "uncoupled_pointwise": 9e-18}).to_latex()
    assert "gamma-blind" in tex and "chiral, coupled" in tex


# -- full document + pdf -----------------------------------------------------------

def test_full_document_structure_and_footnote():
    from organon_mueller.decomposition import decompose

    rep = Report(title="doc", date="2026-07-14").add(
        decomposition_section(decompose(covariance=_rank2_cov(),
                                        symmetry="type1")))
    tex = rep.to_latex()
    assert tex.startswith("\\documentclass")
    assert tex.rstrip().endswith("\\end{document}")
    assert "novelty protocol" in tex             # interpretation boundary
    assert "never an exactness claim" in tex     # rounding convention (D1)
    assert "reserved for human experts" in tex


@pytest.mark.skipif(shutil.which("pdflatex") is None,
                    reason="pdflatex not available (CI-optional)")
def test_demo_sample_report_compiles(tmp_path):
    from organon_mueller.reporting import build_demo_report

    rep = build_demo_report()
    tex = rep.to_latex()
    assert tex == build_demo_report().to_latex()   # deterministic
    p = tmp_path / "sample-report.tex"
    p.write_text(tex)
    pdf = compile_pdf(p, tmp_path)
    assert pdf.exists() and pdf.stat().st_size > 1000
