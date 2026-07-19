"""wordalgebra phase 3+4: the solver core, and the TANZER_2 backward-
validation — the general engine must reproduce the hand-derived answer
from a spec alone.
"""
import numpy as np
import pytest
import sympy as sp

from organon_mueller.lorentz.core import SIGMA
from organon_mueller.wordalgebra import solve
from organon_mueller.wordalgebra.briefs import tanzer2_spec

#: the hand-derived TANZER_2 answer (studies/tanzer2, on its own branch)
TANZER2_IDENTITIES = {
    ("Z*", "(Z^-1)*"), ("(Z^-1)*", "Z*"),
    ("Z^T", "(Z^-1)^T"), ("(Z^-1)^T", "Z^T"),
}
_MODULE_RESULT = None


def _result():
    global _MODULE_RESULT
    if _MODULE_RESULT is None:
        _MODULE_RESULT = solve(tanzer2_spec())
    return _MODULE_RESULT


# -- backward validation: TANZER_2 reproduced from a spec -------------------

def test_tanzer2_identities_reproduced_exactly():
    r = _result()
    assert set(r.identities()) == TANZER2_IDENTITIES
    assert len(r.identities()) == 4


def test_tanzer2_full_table_is_8x8():
    r = _result()
    assert len(r.cells) == 64
    assert len(r.alphabet) == 8


def test_lambda_type_sandwich_is_a_matrix_not_an_identity():
    """Z^dagger Sigma Z expands (it is the Lambda-type of Task 1) but its
    coefficient is a genuine matrix, so it is NOT an identity = Sigma."""
    c = _result().cells[("Zdag", "Z")]
    assert c.expands and c.kind == "matrix" and not c.holds


def test_the_four_are_scalar_multiples_that_become_one_on_the_constraint():
    """Each identity's sandwich is s*Sigma with s in {alpha.alpha,
    conj(alpha.alpha)} — not identically 1, but 1 on the constraint (the
    ideal reduction decides this, not sampling)."""
    r = _result()
    for a, b in TANZER2_IDENTITIES:
        c = r.cells[(a, b)]
        assert c.kind == "scalar" and c.holds
        assert sp.expand(c.scalar - 1) != 0        # genuinely conditional


def test_numeric_cross_check_on_the_constraint_surface():
    """Independent of the solver's symbolic path: at a random point on
    alpha.alpha = 1, exactly the four identities hold numerically."""
    rng = np.random.default_rng(20260718)
    a1, a2, a3 = (rng.normal() + 1j * rng.normal() for _ in range(3))
    a0 = np.sqrt(1 + a1**2 + a2**2 + a3**2)
    a = np.array([a0, a1, a2, a3], dtype=complex)
    SN = [np.array(s, dtype=complex) for s in SIGMA]
    Z = sum(a[m] * SN[m] for m in range(4))
    Zi = a[0]*SN[0] - a[1]*SN[1] - a[2]*SN[2] - a[3]*SN[3]
    S = {"Z": Z, "Z*": Z.conj(), "Z^T": Z.T, "Zdag": Z.conj().T,
         "Z^-1": Zi, "(Z^-1)*": Zi.conj(), "(Z^-1)^T": Zi.T,
         "(Z^-1)dag": Zi.conj().T}
    holds = set()
    for an in S:
        for bn in S:
            if all(np.max(np.abs(S[an] @ SN[m] @ S[bn] - SN[m])) < 1e-9
                   for m in range(4)):
                holds.add((an, bn))
    assert holds == TANZER2_IDENTITIES


# -- solver mechanics -------------------------------------------------------

def test_query_guard():
    with pytest.raises(ValueError, match="query"):
        solve(tanzer2_spec(), query="whatever")


def test_unconstrained_scalar_must_be_identically_one():
    """With no constraint, a scalar sandwich holds only if s == 1
    identically (nothing to reduce against)."""
    from organon_mueller.wordalgebra.briefs import _generator, _inverse
    from organon_mueller.wordalgebra import BriefSpec
    spec = BriefSpec("free", tuple(SIGMA), _generator, _inverse, 4,
                     operations=("id", "conj", "T", "dagger", "inv"),
                     constraint=None)
    r = solve(spec)
    # off the constraint the q-scaled sandwiches are NOT identities
    assert r.identities() == []
