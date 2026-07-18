"""Milestone UI-3 (FROZEN-7 follow-on): the numeric Lorentz tool.

tool_lorentz_transform builds Λ for a boost/rotation from the engine's
proven definitions, evaluated numerically. The keystone test PINS it to
the symbolic engine (lorentz_matrix ∘ boost_alpha / rotation_alpha) at
unit axes, so the fast numeric path can never drift from the proofs.
Everything is numeric-only and K26 (errors are readable reasons).
"""
import math

import numpy as np
import sympy as sp

from organon_mueller.lorentz import (
    boost_alpha,
    lorentz_matrix,
    rotation_alpha,
)
from organon_mueller.mcp_server.tools import tool_lorentz_transform as T


def _sym_lambda(alpha):
    m = lorentz_matrix(alpha)
    return np.array([[complex(m[i, j]) for j in range(4)]
                     for i in range(4)]).real


def test_boost_is_proper_orthochronous_and_textbook():
    r = T({"kind": "boost", "angle": 1.0, "axis": [1, 0, 0]})
    assert "error" not in r
    lam = r["lambda"]
    assert math.isclose(lam[0][0], math.cosh(1.0), abs_tol=1e-9)
    assert math.isclose(lam[0][1], math.sinh(1.0), abs_tol=1e-9)
    ch = r["checks"]
    assert ch["is_proper_orthochronous_lorentz"]
    assert ch["metric_residual"] < 1e-9
    assert abs(ch["det"] - 1.0) < 1e-9
    assert ch["orthochronous"] and ch["imag_leak"] < 1e-12


def test_rotation_is_the_textbook_spatial_rotation():
    r = T({"kind": "rotation", "angle": math.pi / 2, "axis": [0, 0, 1]})
    lam = np.array(r["lambda"])
    want = np.array([[1, 0, 0, 0], [0, 0, 1, 0],
                     [0, -1, 0, 0], [0, 0, 0, 1]], dtype=float)
    assert np.max(np.abs(lam - want)) < 1e-9
    assert r["checks"]["is_proper_orthochronous_lorentz"]


def test_numeric_tool_is_pinned_to_the_symbolic_engine():
    """KEYSTONE: the numeric Λ equals the symbolic engine's Λ at unit
    axes — boost and rotation — so the tool cannot drift from the proofs."""
    third = sp.Integer(1) / sp.sqrt(3)
    sym_boost = _sym_lambda(boost_alpha(sp.Float(0.7), (third,) * 3))
    num_boost = np.array(T({"kind": "boost", "angle": 0.7,
                            "axis": [1, 1, 1]})["lambda"])
    assert np.max(np.abs(sym_boost - num_boost)) < 1e-9

    zaxis = (sp.Integer(0), sp.Integer(0), sp.Integer(1))
    sym_rot = _sym_lambda(rotation_alpha(sp.Float(1.1), zaxis))
    num_rot = np.array(T({"kind": "rotation", "angle": 1.1,
                          "axis": [0, 0, 2]})["lambda"])   # non-unit input
    assert np.max(np.abs(sym_rot - num_rot)) < 1e-9


def test_axis_is_normalized():
    """A non-unit axis gives the same Λ as its normalized direction."""
    a = T({"kind": "boost", "angle": 0.9, "axis": [0, 3, 0]})
    b = T({"kind": "boost", "angle": 0.9, "axis": [0, 1, 0]})
    assert np.max(np.abs(np.array(a["lambda"])
                         - np.array(b["lambda"]))) < 1e-12
    assert a["axis_unit"] == [0.0, 1.0, 0.0]


def test_lambda_is_real_for_boost_and_rotation():
    for kind, ax in (("boost", [1, 2, 3]), ("rotation", [2, -1, 1])):
        r = T({"kind": kind, "angle": 0.8, "axis": ax})
        assert r["checks"]["imag_leak"] < 1e-12


def test_alpha_carries_the_expected_reality_structure():
    """Boost α is real; rotation α has real time part and imaginary
    spatial part (the work order's parametrization)."""
    b = T({"kind": "boost", "angle": 0.6, "axis": [1, 0, 0]})
    assert all(abs(im) < 1e-12 for _, im in b["alpha"])
    r = T({"kind": "rotation", "angle": 0.6, "axis": [1, 0, 0]})
    assert abs(r["alpha"][0][1]) < 1e-12          # time part real
    assert abs(r["alpha"][1][0]) < 1e-12          # spatial part imaginary
    assert abs(r["alpha"][1][1]) > 1e-6


def test_guard_errors_are_readable_reasons():
    assert "kind" in T({"kind": "warp", "angle": 1,
                        "axis": [1, 0, 0]})["error"]
    assert "angle" in T({"kind": "boost", "angle": "1.0",
                        "axis": [1, 0, 0]})["error"]
    assert "finite" in T({"kind": "boost", "angle": float("inf"),
                         "axis": [1, 0, 0]})["error"]
    assert "non-zero" in T({"kind": "boost", "angle": 1,
                           "axis": [0, 0, 0]})["error"]
    assert "3" in T({"kind": "boost", "angle": 1,
                    "axis": [1, 0]})["error"]
    assert "axis[2]" in T({"kind": "boost", "angle": 1,
                          "axis": [1, 0, "z"]})["error"]


def test_bool_is_not_accepted_as_a_number():
    """Defence in depth: bool is an int subclass; angle=True must be
    rejected, not silently read as 1.0."""
    assert "error" in T({"kind": "boost", "angle": True,
                        "axis": [1, 0, 0]})


def test_huge_boost_angle_is_a_readable_reason_not_a_traceback():
    """A boost rapidity that overflows double precision must return a K26
    reason across the WHOLE overflow-adjacent band — not just past it
    (review UI-3, MAJOR: an earlier fix guarded only the intermediate Λ
    and missed the ≈355–710 band). Three regimes fail cleanly:
      - mid band (~355–710): Λ finite, but the ×1e12 rounding of the
        output and the SQUARED metric/det checks overflow;
      - Λ-overflow band (>710): Λ itself is inf.
    All must yield "too large" with NO leaked RuntimeWarning (asserted
    under warnings-as-errors) and NO served inf matrix. Rotations are
    bounded and never trip it."""
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)   # any leak -> raise
        for bad in (500.0, 690.0, 1420.0, 1e4, -1e4, 1e300):
            r = T({"kind": "boost", "angle": bad, "axis": [1, 0, 0]})
            assert "error" in r and "too large" in r["error"], bad
            assert "lambda" not in r                       # no inf matrix served
        ok = T({"kind": "boost", "angle": 6.0, "axis": [1, 0, 0]})
        assert ok["checks"]["is_proper_orthochronous_lorentz"]
        rot = T({"kind": "rotation", "angle": 1e9, "axis": [0, 0, 1]})
        assert "error" not in rot
    assert all(np.isfinite(x) for row in rot["lambda"] for x in row)
