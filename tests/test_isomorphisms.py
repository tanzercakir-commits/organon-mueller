import numpy as np
import sympy as sp

from organon_mueller.algebra.states import (
    HVector,
    covariance_from_mueller,
    hvector_from_covariance,
    hvector_from_jones,
    hvector_from_quaternion,
    z_from_jones,
)
from organon_mueller.verify import (
    numeric_equal,
    random_hvector,
    sample_check,
    symbolic_equal,
    to_numpy,
)


def _eq_hvec(a: HVector, b: HVector) -> bool:
    return all(
        sp.expand(x - y) == 0
        for x, y in (
            (a.tau, b.tau),
            (a.alpha, b.alpha),
            (a.beta, b.beta),
            (a.gamma, b.gamma),
        )
    )


def test_jones_roundtrip():
    h = HVector.generic("a")
    assert _eq_hvec(hvector_from_jones(h.to_jones()), h)


def test_quaternion_roundtrip():
    h = HVector.generic("a")
    assert _eq_hvec(hvector_from_quaternion(h.to_quaternion()), h)


def test_z_from_jones_matches_explicit_z():
    h = HVector.generic("a")
    assert symbolic_equal(z_from_jones(h.to_jones()), h.to_z())


def test_covariance_roundtrip_numeric():
    def one(rng: np.random.Generator) -> bool:
        h = random_hvector(rng)
        cov = covariance_from_mueller(h.to_mueller())
        h_rec = hvector_from_covariance(cov)
        # recovery is up to a global phase; compare rank-1 projectors
        return numeric_equal(
            to_numpy(h_rec.to_covariance_matrix()),
            to_numpy(h.to_covariance_matrix()),
        )

    assert sample_check(one, samples=25)
