"""Stage-17: STAGE-2 GATE hardening — restricted srepr parser + MCP
input validation. The injection corpus must be REJECTED, never
evaluated (canary side effects checked)."""
import os

import numpy as np
import pytest
import sympy as sp

from organon_mueller.safe_parse import UnsafeExpressionError, safe_parse_srepr
from organon_mueller.serialize import hvector_from_json, hvector_to_json
from organon_mueller.algebra.states import HVector

INJECTIONS = [
    "__import__('os').system('echo pwned')",
    "().__class__.__mro__[1].__subclasses__()",
    "getattr(__import__('os'), 'system')('id')",
    "exec('import os')",
    "eval('1+1')",
    "open('/etc/passwd').read()",
    "lambda: 1",
    "Symbol('x').__class__",
    "Function('f')(Symbol('x'))",                     # unknown call
    "Symbol('x', commutative=False)",                 # kwarg smuggling
    "Symbol('x', real='True')",                       # non-bool assumption
    "Float('1.0', precision=10**9)",                  # kwarg abuse
    "Integer(" + "9" * 5000 + ")",                    # huge literal
    "Symbol('a b')",                                  # bad name
    "Symbol('__dunder__')",                           # leading underscore
    "[1, 2, 3]",                                      # non-expression
    "{'a': 1}",
    "Add(" * 100 + "Integer(1)" + ")" * 100,          # deep nesting
    "import os",                                      # statement
    "Mul(Integer(2), __import__('os'))",              # nested smuggling
]


@pytest.mark.parametrize("payload", INJECTIONS,
                         ids=[f"inj{i}" for i in range(len(INJECTIONS))])
def test_injection_corpus_rejected(payload, tmp_path):
    canary = tmp_path / "canary"
    env_before = dict(os.environ)
    with pytest.raises(UnsafeExpressionError, match="rejected"):
        safe_parse_srepr(payload)
    assert not canary.exists()
    assert dict(os.environ) == env_before


def test_oversized_input_rejected():
    with pytest.raises(UnsafeExpressionError, match="longer"):
        safe_parse_srepr("Integer(1)" + " " * 70000)
    with pytest.raises(UnsafeExpressionError, match="nodes"):
        safe_parse_srepr("Add(" + ", ".join(["Integer(1)"] * 1500) + ")")


def test_non_string_rejected():
    with pytest.raises(UnsafeExpressionError, match="str"):
        safe_parse_srepr(12345)


# -- review round 2: DoS by magnitude, exception contract, regex, non-finite ------

@pytest.mark.parametrize("payload", [
    "Rational('1e9999999')",                          # 33-Mbit literal
    "Rational('1e500000')",
    "Pow(Integer(2), Integer(99999999))",             # exponent bomb
    "Pow(Integer(10), Integer(1000000))",             # base^exp result bomb
    "Pow(Pow(Integer(10), Integer(1000000)), Integer(1000000))",  # tower
    "Mul(" + ", ".join(["Pow(Integer(10), Integer(1000000))"] * 100) + ")",
])
def test_magnitude_dos_rejected_fast(payload):
    """Review D1 (round 2): bound the RESULT magnitude, not the exponent.
    Every bomb rejects by guard in well under a second — no huge number
    is ever materialized."""
    import time

    t0 = time.monotonic()
    with pytest.raises(UnsafeExpressionError):
        safe_parse_srepr(payload)
    assert time.monotonic() - t0 < 1.0


def test_small_floats_still_roundtrip_no_regression():
    """Review round 2 regression guard: srepr emits scientific notation
    for small Floats (Float('1.0e-10')); the magnitude guard must NOT
    reject those — only large exponents."""
    for lit in ("1e-10", "1.0e-10", "2.5e-3", "1e-300", "1.5e-8"):
        f = sp.Float(lit)
        back = safe_parse_srepr(sp.srepr(f))
        assert sp.simplify(back - f) == 0
    with pytest.raises(UnsafeExpressionError, match="exponent"):
        safe_parse_srepr("Float('1.0e9999999', precision=53)")


def test_bare_scientific_float_infinity_rejected():
    for payload in ("1e999", "-1e999", "1e400"):   # review D4 bare-float
        with pytest.raises(UnsafeExpressionError):
            safe_parse_srepr(payload)


@pytest.mark.parametrize("payload", [
    "Float('1e300000')",                              # S1: Float exp bomb
    "Float('1e999999')",
    "Mul(" + ", ".join(["Pow(Integer(10), Integer(4096))"] * 178) + ")",
    "Add(" + ", ".join(["Pow(Integer(10), Integer(4096))"] * 178) + ")",
    # round 4: non-integer / Float exponents on numeric bases, and a
    # numeric coefficient nested in a Mul base
    "Pow(Float('10.0'), Float('1e4096'))",
    "Pow(Integer(10), Float('1e4096'))",
    "Pow(Rational(3, 2), Float('1e4096'))",
    "Pow(Integer(10), Rational(1999999, 2))",
    "Pow(Float('10.0'), Integer(1000000))",
    "Pow(Mul(Integer(3), Symbol('x')), Integer(1000000))",
])
def test_float_and_product_bombs_rejected_before_materializing(payload):
    """Review rounds 3-4 (S1/S2 + non-integer Pow): Float-exponent bombs,
    Mul/Add folds, and non-integer/Float exponents on numeric bases (incl.
    coefficients nested in a Mul base) must be refused by projection
    BEFORE the huge number is ever built (<1s)."""
    import time

    t0 = time.monotonic()
    with pytest.raises(UnsafeExpressionError):
        safe_parse_srepr(payload)
    assert time.monotonic() - t0 < 1.0


def test_legit_powers_still_parse():
    """The projection must NOT reject the powers the library emits."""
    assert safe_parse_srepr("Pow(Symbol('x'), Rational(1, 2))") == \
        sp.sqrt(sp.Symbol("x"))
    assert safe_parse_srepr("Pow(Symbol('x'), Integer(2))") == \
        sp.Symbol("x") ** 2
    assert safe_parse_srepr("Pow(Integer(10), Integer(3))") == sp.Integer(1000)


def test_deep_nesting_reasoned_not_raw_error():
    """Review D2: deep nesting that blows ast.parse must surface as
    UnsafeExpressionError, never a raw MemoryError/RecursionError."""
    with pytest.raises(UnsafeExpressionError):
        safe_parse_srepr("-" * 60000 + "Integer(1)")
    with pytest.raises(UnsafeExpressionError):
        safe_parse_srepr("Add(" * 6000 + "Integer(1)" + ")" * 6000)


def test_non_finite_values_rejected():
    """Review D4: NaN / oo / zoo must never parse into an HVector."""
    for payload in ("Float('nan')", "Float('inf')", "Float('-inf')",
                    "Rational(1, 0)"):
        with pytest.raises(UnsafeExpressionError):
            safe_parse_srepr(payload)


def test_symbol_name_fullmatch_no_newline():
    """Review D5: a trailing newline must not slip through _NAME_RE."""
    with pytest.raises(UnsafeExpressionError):
        safe_parse_srepr("Symbol('x\\n')")
    with pytest.raises(UnsafeExpressionError):
        safe_parse_srepr("Symbol('x\\r')")


def test_tolerance_type_confusion_returns_error_not_traceback():
    """Review D3: bad tolerance types must return {"error": ...}."""
    from organon_mueller.mcp_server import tool_decompose_mueller

    good = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    for bad in (None, [0.5], {}, "0.5", True):
        out = tool_decompose_mueller(
            {"mueller": good, "symmetry": "type1", "rank_tol": bad})
        assert "error" in out and "rank_tol" in out["error"]


# -- the parser must still accept everything WE produce ---------------------------

def test_roundtrip_representative_expression_corpus():
    """Everything this library actually serializes must survive
    srepr -> safe_parse_srepr: generic Z-matrix entries (Symbol/conjugate/
    I/Mul/Add), guarded symbolic generators, numeric scalars."""
    corpus = list(HVector.generic("g").to_z()) \
        + list((HVector.generic("a").to_z() * HVector.generic("b").to_z()))
    try:
        from organon_mueller.discovery.guards import guarded_symbolic_hvector
        for key in ("hermitian_state", "unitary_state", "class2_ta"):
            corpus += list(guarded_symbolic_hvector("x", key).to_z())
    except ImportError:
        pass
    corpus += [sp.Integer(-7), sp.Rational(22, 7), sp.Float("2.5e-3"),
               1 + 2 * sp.I, sp.conjugate(sp.Symbol("w", complex=True)) ** 3]
    count = 0
    for entry in corpus:
        back = safe_parse_srepr(sp.srepr(entry))
        assert sp.simplify(back - entry) == 0
        count += 1
    assert count >= 40


def test_roundtrip_generic_and_numeric_hvectors():
    hv = HVector.generic("q")
    back = hvector_from_json(hvector_to_json(hv))
    assert all(sp.simplify(a - b) == 0 for a, b in
               zip(back.to_column(), hv.to_column()))
    hv2 = HVector(sp.Float("0.25"), sp.Rational(1, 3),
                  2 + 3 * sp.I, -sp.conjugate(sp.Symbol("z", complex=True)))
    back2 = hvector_from_json(hvector_to_json(hv2))
    assert all(sp.simplify(a - b) == 0 for a, b in
               zip(back2.to_column(), hv2.to_column()))


def test_assumptions_survive_roundtrip():
    x = sp.Symbol("x", real=True, positive=True)
    back = safe_parse_srepr(sp.srepr(x))
    assert back.is_real and back.is_positive


# -- MCP tool input validation (K26) ----------------------------------------------

def test_tool_rejects_bad_shapes_and_types():
    from organon_mueller.mcp_server import tool_decompose_mueller

    assert "error" in tool_decompose_mueller({"mueller": [[1, 2], [3, 4]]})
    assert "error" in tool_decompose_mueller(
        {"mueller": [["1"] * 4] * 4})                      # strings
    assert "error" in tool_decompose_mueller(
        {"mueller": [[float("nan")] * 4] * 4})             # non-finite
    assert "error" in tool_decompose_mueller(
        {"mueller": [[True] * 4] * 4})                     # bools
    bad_sym = tool_decompose_mueller(
        {"mueller": [[1, 0, 0, 0]] * 4, "symmetry": "__evil__"})
    assert "error" in bad_sym and "symmetry" in bad_sym["error"]


def test_tool_no_expression_text_path():
    """The MCP boundary accepts numbers only — a payload smuggling an
    expression string anywhere must come back as a reasoned error."""
    from organon_mueller.mcp_server import tool_propose_hypotheses

    out = tool_propose_hypotheses(
        {"covariance": [[["__import__('os')", 0]] * 4] * 4})
    assert "error" in out


def test_tool_happy_path_and_reasons():
    from organon_mueller.mcp_server import (
        tool_decompose_mueller, tool_propose_hypotheses,
    )
    from organon_mueller.decomposition.rank3 import _template_numeric

    rng = np.random.default_rng(20260713)
    x = float(rng.uniform(0.15, 0.85))
    w = np.sqrt(x * (1 - x)) * np.exp(1j * float(rng.uniform(0, 2 * np.pi)))
    h1 = _template_numeric("type1", x, w)
    u = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    u /= np.linalg.norm(u)
    cov = 0.4 * h1 + 0.6 * np.outer(u, u.conj())
    payload = {"covariance": [[[v.real, v.imag] for v in row]
                              for row in cov]}
    out = tool_propose_hypotheses(payload)
    assert out["rank"] == 2
    assert any(a["hypothesis"] == "type1" for a in out["accepted"])
    assert all(r["reason"] for r in out["rejected"])

    from organon_mueller.decomposition.covariance import (
        mueller_from_standard_covariance,
    )
    m = np.array(sp.matrix2numpy(
        mueller_from_standard_covariance(sp.Matrix(cov)).evalf(),
        dtype=complex)).real
    res = tool_decompose_mueller({"mueller": m.tolist(), "symmetry": "type1"})
    assert res.get("kind") == "DecompositionResult"
    assert abs(res["alpha1"] - 0.4) < 1e-6


def test_generate_report_tool_and_guarded_info():
    from organon_mueller.mcp_server import (
        tool_generate_report, tool_guarded_campaign_info,
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
    m = np.array(sp.matrix2numpy(
        mueller_from_standard_covariance(sp.Matrix(cov)).evalf(),
        dtype=complex)).real
    out = tool_generate_report({"mueller": m.tolist(), "date": "2026-07-14",
                                "title": "smoke % _ title"})
    assert "latex" in out and "\\documentclass" in out["latex"]
    assert "never an exactness claim" in out["latex"]

    pytest.importorskip("egglog")
    info = tool_guarded_campaign_info()
    assert len(info["findings"]) == 3
    assert all(f["is_conditional_identity"] for f in info["findings"])
    assert "no" in info["note"] and "novelty" in info["note"]


def test_fastmcp_wiring_smoke():
    mcp = pytest.importorskip("mcp")  # noqa: F841
    from organon_mueller.mcp_server.server import build_server

    app = build_server()
    import anyio

    tools = anyio.run(app.list_tools)
    names = {t.name for t in tools}
    assert names == {"decompose_mueller", "propose_hypotheses",
                     "guarded_campaign_info", "generate_report"}
