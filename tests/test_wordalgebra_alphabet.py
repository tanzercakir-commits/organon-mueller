"""wordalgebra phase 1: BriefSpec validation + alphabet construction."""
import numpy as np
import pytest
import sympy as sp

from organon_mueller.lorentz.core import SIGMA
from organon_mueller.wordalgebra import (
    BriefSpec,
    SpecError,
    alphabet_labels,
    build_alphabet,
)


def _tanzer_generator(a):
    return sum((a[m] * SIGMA[m] for m in range(4)), sp.zeros(4))


def _tanzer_inverse(a):
    return a[0] * SIGMA[0] - a[1] * SIGMA[1] - a[2] * SIGMA[2] - a[3] * SIGMA[3]


def _tanzer_spec(operations=("id", "conj", "T", "dagger", "inv")):
    a = sp.symbols("a0 a1 a2 a3", complex=True)
    return BriefSpec(
        name="tanzer",
        basis=tuple(SIGMA),
        generator=_tanzer_generator,
        inverse=_tanzer_inverse,
        n_params=4,
        operations=operations,
        constraint=lambda p: p[0]**2 - p[1]**2 - p[2]**2 - p[3]**2 - 1,
    )


# -- alphabet ---------------------------------------------------------------

def test_full_alphabet_is_the_collaborators_eight_letters():
    a = sp.symbols("a0 a1 a2 a3", complex=True)
    Z, Zi = _tanzer_generator(a), _tanzer_inverse(a)
    alpha = build_alphabet(Z, Zi, ("id", "conj", "T", "dagger", "inv"))
    assert list(alpha) == ["Z", "Z*", "Z^T", "Zdag",
                           "Z^-1", "(Z^-1)*", "(Z^-1)^T", "(Z^-1)dag"]
    # the letters are the advertised operations, exactly
    assert sp.expand(alpha["Z*"] - Z.conjugate()) == sp.zeros(4)
    assert sp.expand(alpha["Z^T"] - Z.T) == sp.zeros(4)
    assert sp.expand(alpha["Zdag"] - Z.conjugate().T) == sp.zeros(4)
    assert sp.expand(alpha["(Z^-1)*"] - Zi.conjugate()) == sp.zeros(4)
    assert sp.expand(alpha["(Z^-1)dag"] - Zi.conjugate().T) == sp.zeros(4)


def test_alphabet_labels_match_build_order():
    ops = ("id", "conj", "T", "dagger", "inv")
    a = sp.symbols("a0 a1 a2 a3", complex=True)
    alpha = build_alphabet(_tanzer_generator(a), _tanzer_inverse(a), ops)
    assert alphabet_labels(ops) == list(alpha)


def test_operations_subset_shrinks_the_alphabet():
    # no inverse root, no transpose -> only Z, Z*, Zdag
    labels = alphabet_labels(("id", "conj", "dagger"))
    assert labels == ["Z", "Z*", "Zdag"]


def test_builder_works_numerically_too():
    """Same builder must serve the numeric screen (numpy arrays)."""
    a = np.array([1.3, 0.2j, 0.1, -0.4], dtype=complex)
    SN = [np.array(s, dtype=complex) for s in SIGMA]
    Z = sum(a[m] * SN[m] for m in range(4))
    Zi = a[0]*SN[0] - a[1]*SN[1] - a[2]*SN[2] - a[3]*SN[3]
    alpha = build_alphabet(Z, Zi, ("id", "conj", "T", "dagger", "inv"))
    assert np.max(np.abs(alpha["Zdag"] - Z.conj().T)) < 1e-12
    assert np.max(np.abs(alpha["(Z^-1)^T"] - Zi.T)) < 1e-12


# -- spec validation (K26) --------------------------------------------------

def test_valid_spec_passes():
    assert _tanzer_spec().validate() is not None


def test_bad_specs_give_readable_reasons():
    with pytest.raises(SpecError, match="non-empty name"):
        BriefSpec("", tuple(SIGMA), _tanzer_generator, _tanzer_inverse, 4
                  ).validate()
    with pytest.raises(SpecError, match="square"):
        BriefSpec("x", (sp.Matrix([[1, 0, 0]]),), _tanzer_generator,
                  _tanzer_inverse, 4).validate()
    with pytest.raises(SpecError, match="n_params"):
        BriefSpec("x", tuple(SIGMA), _tanzer_generator, _tanzer_inverse, 0
                  ).validate()
    with pytest.raises(SpecError, match="unknown operations"):
        _tanzer_spec(operations=("id", "warp")).validate()
    with pytest.raises(SpecError, match="unary op"):
        _tanzer_spec(operations=("inv",)).validate()


def test_spec_helpers():
    s = _tanzer_spec()
    assert s.dim() == 4
    assert s.mids() == tuple(SIGMA)          # default middles = basis
    assert len(s.symbols()) == 4
