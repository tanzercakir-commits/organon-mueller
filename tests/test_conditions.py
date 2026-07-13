import numpy as np

from organon_mueller.algebra.states import covariance_from_mueller
from organon_mueller.conditions import (
    covariance_rank,
    is_hermitian_state,
    is_nondepolarizing_mueller,
    is_unitary_state,
    trace_condition,
)
from organon_mueller.verify import random_hvector, to_numpy

_RNG = np.random.default_rng(20260713)


def _pure_mueller_and_cov():
    h = random_hvector(_RNG)
    m = h.to_mueller()
    return to_numpy(m), to_numpy(covariance_from_mueller(m))


def test_pure_state_is_nondepolarizing():
    m, cov = _pure_mueller_and_cov()
    assert trace_condition(m)
    assert covariance_rank(cov) == 1
    assert is_nondepolarizing_mueller(m, cov)


def test_mixture_is_depolarizing():
    m1, c1 = _pure_mueller_and_cov()
    m2, c2 = _pure_mueller_and_cov()
    m_mix, c_mix = 0.5 * (m1 + m2), 0.5 * (c1 + c2)
    assert covariance_rank(c_mix) == 2
    assert not trace_condition(m_mix)
    assert not is_nondepolarizing_mueller(m_mix, c_mix)


def test_state_predicates():
    assert is_hermitian_state([1.0, 0.3, -0.2, 0.7])
    assert not is_hermitian_state([1.0, 0.3j, -0.2, 0.7])
    assert is_unitary_state([1.0, 0.3j, -0.2j, 0.7j])
    assert not is_unitary_state([1.0, 0.3, -0.2j, 0.7j])
    assert not is_unitary_state([1.0j, 0.3j, -0.2j, 0.7j])
