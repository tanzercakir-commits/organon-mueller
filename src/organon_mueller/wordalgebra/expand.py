"""Express a matrix in the basis: M = sum_nu c_nu B^nu.

Spec 01 covers TRACE-ORTHOGONAL bases (tr(B^i B^j) = 0 for i != j),
which both collaborator briefs use (the Sigma basis has
tr(Sigma^i Sigma^j) = 4 delta). Then the coefficients are exact:

    c_nu = tr(B^nu M) / tr(B^nu B^nu).

A nonzero residual M - sum c_nu B^nu certifies "M does not lie in the
span" (no expansion). A non-trace-orthogonal basis raises a readable
reason (K26) — the Gram-solve generalization is deferred to spec 02
(honest scope: neither current brief needs it).

Backend-agnostic: works on sympy Matrices (the exact proof path) and on
numpy arrays (the numeric screen).
"""
from __future__ import annotations

import numpy as np
import sympy as sp

from .spec import SpecError


def _is_sympy(M) -> bool:
    return isinstance(M, sp.MatrixBase)


def _matmul(A, B):
    # sympy '*' is matrix product; numpy '*' is elementwise, so dispatch
    return A * B if _is_sympy(A) else A @ B


def _trace(M):
    return sp.expand(sp.trace(M)) if _is_sympy(M) else np.trace(M)


def _zeros_like(M):
    return sp.zeros(*M.shape) if _is_sympy(M) else np.zeros(M.shape, complex)


def trace_orthogonal_norms(basis, tol: float = 1e-9):
    """(tr(B^0 B^0), ...) if the basis is trace-orthogonal, else raise.
    Exact for sympy bases; tolerance-based for numeric ones."""
    d = len(basis)
    norms = []
    for i in range(d):
        for j in range(d):
            t = _trace(_matmul(basis[i], basis[j]))
            offdiag_zero = (t == 0) if _is_sympy(basis[0]) else abs(t) < tol
            diag_zero = (t == 0) if _is_sympy(basis[0]) else abs(t) < tol
            if i == j:
                if diag_zero:
                    raise SpecError(
                        f"basis element {i} has zero trace-norm "
                        "tr(B^i B^i) = 0; cannot extract coefficients")
                norms.append(t)
            elif not offdiag_zero:
                raise SpecError(
                    f"basis is not trace-orthogonal (tr(B^{i} B^{j}) != 0); "
                    "spec 01 requires a trace-orthogonal basis (Gram-solve "
                    "generalization is future work)")
    return tuple(norms)


def expand_in_basis(M, basis, norms):
    """Return (coeffs, residual): M = sum_nu coeffs[nu] B^nu + residual.
    A zero residual means M lies in the span (an expansion exists)."""
    d = len(basis)
    coeffs = tuple(_trace(_matmul(basis[n], M)) / norms[n] for n in range(d))
    recon = _zeros_like(M)
    for n in range(d):
        recon = recon + coeffs[n] * basis[n]
    residual = M - recon
    if _is_sympy(M):
        residual = sp.expand(residual)
    return coeffs, residual


def residual_is_zero(residual, tol: float = 1e-9) -> bool:
    if _is_sympy(residual):
        return sp.expand(residual) == sp.zeros(*residual.shape)
    return bool(np.max(np.abs(residual)) < tol)


def coefficient_matrix(word_a, basis, word_b, norms):
    """The coefficient matrix C of the sandwich family: row mu is the
    basis expansion of  word_a . B^mu . word_b, so

        word_a B^mu word_b = sum_nu C[mu][nu] B^nu   (+ residual_mu).

    Returns (C, expands) where C is a list-of-rows of coefficients and
    ``expands`` is True iff every row's residual is zero (the whole
    sandwich family lies in the span)."""
    C, ok = [], True
    for mu in range(len(basis)):
        M = _matmul(_matmul(word_a, basis[mu]), word_b)
        coeffs, residual = expand_in_basis(M, basis, norms)
        C.append(coeffs)
        ok = ok and residual_is_zero(residual)
    return C, ok
