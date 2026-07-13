"""Hard-coded literature fixtures: external anchors for the conventions.

Reviewer finding (stage 0): route-vs-route checks could hide a correlated
convention error.  These fixtures pin concrete, textbook Mueller/Z entries.
"""
import sympy as sp

from organon_mueller.algebra.states import (
    HVector,
    hvector_from_covariance,
    hvector_from_jones,
    mueller_rotation,
)
from organon_mueller.verify import symbolic_equal

_i = sp.I
_half = sp.Rational(1, 2)


def test_horizontal_polarizer():
    """J = diag(1, 0)  ->  M = 1/2 [[1,1,0,0],[1,1,0,0],[0,0,0,0],[0,0,0,0]]."""
    h = hvector_from_jones(sp.Matrix([[1, 0], [0, 0]]))
    assert (h.tau, h.alpha, h.beta, h.gamma) == (_half, _half, 0, 0)
    expected = _half * sp.Matrix(
        [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    )
    assert symbolic_equal(h.to_mueller(), expected)


def test_vertical_polarizer():
    """J = diag(0, 1)  ->  M = 1/2 [[1,-1,0,0],[-1,1,0,0],[0,0,0,0],[0,0,0,0]]."""
    h = hvector_from_jones(sp.Matrix([[0, 0], [0, 1]]))
    expected = _half * sp.Matrix(
        [[1, -1, 0, 0], [-1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    )
    assert symbolic_equal(h.to_mueller(), expected)


def test_quarter_wave_plate():
    """J = diag(1, i) (fast axis horizontal, 90 deg retardance).

    Expected M = [[1,0,0,0],[0,1,0,0],[0,0,0,-1],[0,0,1,0]], hand-derived
    from M_ij = (1/2) tr(sigma_i J sigma_j J^dagger).
    """
    h = hvector_from_jones(sp.Matrix([[1, 0], [0, _i]]))
    expected = sp.Matrix(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, -1], [0, 0, 1, 0]]
    )
    assert symbolic_equal(h.to_mueller(), expected)


def test_rotator_state_gives_rotation_mueller():
    """|r(theta)> = (cos t, 0, 0, -i sin t) generates M = R(theta) (Eq. (32)-(33))."""
    theta = sp.symbols("theta", real=True)
    h = HVector(sp.cos(theta), 0, 0, -_i * sp.sin(theta))
    diff = sp.expand_trig(sp.expand(h.to_mueller() - mueller_rotation(theta)))
    assert all(sp.simplify(e) == 0 for e in diff)


def test_hvector_from_covariance_rejects_tau_zero():
    """Silent zero-state regression guard (reviewer defect #1)."""
    import pytest

    h = HVector(0, 0, 0, 1)  # ideal half-wave-plate-type state, tau = 0
    with pytest.raises(ValueError):
        hvector_from_covariance(h.to_covariance_matrix())
