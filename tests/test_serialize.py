import json

import numpy as np
import pytest
import sympy as sp

from organon_mueller.algebra.states import HVector
from organon_mueller.identities.known import KNOWN_IDENTITIES
from organon_mueller.serialize import (
    hvector_from_dict,
    hvector_from_json,
    hvector_to_json,
    hvector_to_latex,
    library_to_json,
    matrix_to_latex,
)
from organon_mueller.verify import random_hvector


def _srepr_equal(a: HVector, b: HVector) -> bool:
    return all(
        sp.srepr(getattr(a, f)) == sp.srepr(getattr(b, f))
        for f in ("tau", "alpha", "beta", "gamma")
    )


def test_roundtrip_generic_symbols():
    h = HVector.generic("a")
    assert _srepr_equal(hvector_from_json(hvector_to_json(h)), h)


def test_roundtrip_numeric():
    rng = np.random.default_rng(20260713)
    for _ in range(10):
        h = random_hvector(rng)
        assert _srepr_equal(hvector_from_json(hvector_to_json(h)), h)


def test_roundtrip_exact_rationals():
    h = HVector(sp.Rational(1, 2), sp.sqrt(2) / 2, 0, sp.I / 3)
    assert _srepr_equal(hvector_from_json(hvector_to_json(h)), h)


def test_missing_field_raises():
    with pytest.raises(ValueError):
        hvector_from_dict({"tau": "Integer(1)"})


def test_library_export_schema():
    entries = json.loads(library_to_json())
    assert len(entries) == len(KNOWN_IDENTITIES)
    keys = [e["key"] for e in entries]
    assert keys == [i.key for i in KNOWN_IDENTITIES]
    for e in entries:
        assert set(e) == {"key", "statement", "source", "conditions", "mode"}


def test_latex_output():
    h = HVector.generic("a")
    tex_vec = hvector_to_latex(h)
    assert tex_vec.startswith("\\left[") or "matrix" in tex_vec
    assert "\\tau" in tex_vec
    tex_m = matrix_to_latex(h.to_z())
    assert "\\alpha" in tex_m and "i" in tex_m
