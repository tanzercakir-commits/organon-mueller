import sympy as sp

from organon_mueller.algebra.quaternion import BiQuaternion


def _generic(prefix: str) -> BiQuaternion:
    w, x, y, z = sp.symbols(f"w_{prefix} x_{prefix} y_{prefix} z_{prefix}", complex=True)
    return BiQuaternion(w, x, y, z)


def _eq_matrix(a: sp.Matrix, b: sp.Matrix) -> bool:
    return all(e == 0 for e in sp.expand(a - b))


def test_product_matches_matrix_representation():
    """to_matrix is an algebra homomorphism: mat(q1 q2) = mat(q1) mat(q2)."""
    q1, q2 = _generic("a"), _generic("b")
    assert _eq_matrix((q1 * q2).to_matrix(), q1.to_matrix() * q2.to_matrix())


def test_hamilton_conjugate_antihomomorphism():
    q1, q2 = _generic("a"), _generic("b")
    lhs = (q1 * q2).hamilton_conjugate()
    rhs = q2.hamilton_conjugate() * q1.hamilton_conjugate()
    assert lhs.equals(rhs)


def test_hermitian_conjugate_antihomomorphism():
    """(q1 q2)^dag = q2^dag q1^dag (arXiv:1705.07147, Eq. (37))."""
    q1, q2 = _generic("a"), _generic("b")
    lhs = (q1 * q2).hermitian_conjugate()
    rhs = q2.hermitian_conjugate() * q1.hermitian_conjugate()
    assert lhs.equals(rhs)


def test_hermitian_conjugate_matches_matrix_dagger():
    """mat(q^dag) = mat(q)^dagger (conjugate transpose)."""
    q = _generic("a")
    assert _eq_matrix(q.hermitian_conjugate().to_matrix(), q.to_matrix().H)


def test_norm_q_qbar():
    q = _generic("a")
    prod = q * q.hamilton_conjugate()
    norm = q.w**2 + q.x**2 + q.y**2 + q.z**2
    assert sp.expand(prod.w - norm) == 0
    assert sp.expand(prod.x) == 0
    assert sp.expand(prod.y) == 0
    assert sp.expand(prod.z) == 0
