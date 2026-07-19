"""wordalgebra phase 2: basis expansion / coefficient extraction."""
import numpy as np
import pytest
import sympy as sp

from organon_mueller.lorentz.core import SIGMA
from organon_mueller.wordalgebra import (
    SpecError,
    coefficient_matrix,
    expand_in_basis,
    residual_is_zero,
    trace_orthogonal_norms,
)

A = sp.symbols("a0 a1 a2 a3", complex=True)
BASIS = tuple(SIGMA)


def _Z(a):
    return sum((a[m] * SIGMA[m] for m in range(4)), sp.zeros(4))


def test_sigma_is_trace_orthogonal_with_norm_four():
    assert trace_orthogonal_norms(BASIS) == (4, 4, 4, 4)


def test_expand_a_basis_element_is_a_unit_coefficient():
    norms = trace_orthogonal_norms(BASIS)
    coeffs, residual = expand_in_basis(SIGMA[2], BASIS, norms)
    assert [sp.simplify(c) for c in coeffs] == [0, 0, 1, 0]
    assert residual_is_zero(residual)


def test_expand_Z_recovers_alpha():
    norms = trace_orthogonal_norms(BASIS)
    coeffs, residual = expand_in_basis(_Z(A), BASIS, norms)
    assert [sp.simplify(c - A[m]) for m, c in enumerate(coeffs)] == [0, 0, 0, 0]
    assert residual_is_zero(residual)


def test_coefficient_matrix_of_a_sandwich_that_expands():
    """Z^dagger Sigma^mu Z expands in the basis (its coefficient matrix is
    the Lambda of the collaborator's Task 1) — here we only assert it
    EXPANDS and C is 4x4; identifying C is the solver's job."""
    norms = trace_orthogonal_norms(BASIS)
    Z = _Z(A)
    C, expands = coefficient_matrix(Z.conjugate().T, BASIS, Z, norms)
    assert expands
    assert len(C) == 4 and all(len(row) == 4 for row in C)


def test_no_expansion_is_detected():
    """A matrix outside the span of the (Hermitian) Sigma basis — e.g. a
    non-symmetric real matrix with a nonzero (0,1)-(1,0) antisymmetric
    part that the basis cannot represent — has a nonzero residual."""
    norms = trace_orthogonal_norms(BASIS)
    M = sp.Matrix([[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    _, residual = expand_in_basis(M, BASIS, norms)
    assert not residual_is_zero(residual)


def test_numeric_backend_agrees():
    norms = trace_orthogonal_norms(tuple(np.array(s, dtype=complex)
                                         for s in SIGMA))
    assert all(abs(n - 4) < 1e-9 for n in norms)
    a = np.array([1.1, 0.3j, -0.2, 0.5], dtype=complex)
    SN = [np.array(s, dtype=complex) for s in SIGMA]
    Z = sum(a[m] * SN[m] for m in range(4))
    coeffs, residual = expand_in_basis(Z, SN, norms)
    assert all(abs(coeffs[m] - a[m]) < 1e-9 for m in range(4))
    assert residual_is_zero(residual)


def test_non_trace_orthogonal_basis_is_rejected():
    bad = (sp.eye(2), sp.Matrix([[1, 1], [0, 0]]))   # tr(B0 B1) = 1 != 0
    with pytest.raises(SpecError, match="not trace-orthogonal"):
        trace_orthogonal_norms(bad)
