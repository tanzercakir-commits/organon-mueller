"""L1 pre-implementation probe (FROZEN-7): the five Task-1 identities.

Findings (all subsequently locked in tests/test_lorentz_task1.py):

1. GUARD-FREE THEOREMS for generic complex alpha (q = alpha.alpha):
   LT1: Zdag S^mu Z = Lambda^mu_nu S^nu (Lambda = ZZ*, ROW convention;
        the column form FAILS -> the index convention is pinned)
   LT2: Z*  S^mu Zbar*  = conj(q) S^mu
   LT3: Zbar* S^mu Z*   = conj(q) S^mu
   LT4: Z^T S^mu Zbar^T = q S^mu
   LT5: Zbar^T S^mu Z^T = q S^mu
   chain: Lambda(Z) . Lambda(Zbar) = q conj(q) I
2. On the guard q = 1 (boosts AND rotations both satisfy it) the spec's
   five identities hold EXACTLY AS WRITTEN — no sign flip needed under
   the L0 parametrization conventions. The first symbolic attempt on the
   spec form returned False for boost/rotation: that was a SIMPLIFICATION
   weakness with half-angle hyperbolics, not mathematics — rewriting in
   exponentials proves zero exactly (numeric agreement confirmed first).
3. Conjugation lemma (explains the spec's sign warning):
   Z(alpha)* = Z(alpha*)^T (guard-free; Sigma* = Sigma^T). At the
   PARAMETER level conjugation reverses rotations
   (rotation_alpha(theta)* = rotation_alpha(-theta)) and fixes boosts.
   HISTORICAL NOTE: this probe's first draft stated the matrix-level
   claim WITHOUT the transpose — that phrasing is FALSE (Sigma^1/Sigma^3
   are not symmetric) and was caught by the L1 test suite; the corrected
   statement above is what tests/test_lorentz_task1.py locks.

Run: python probes/probe-lorentz-task1.py
"""
import sympy as sp

from organon_mueller.lorentz import (
    SIGMA, boost_alpha, rotation_alpha, z_bar_matrix, z_matrix,
)

A = sp.symbols("a0 a1 a2 a3", complex=True)


def zero(m):
    return sp.expand(m) == sp.zeros(4)


def main() -> dict:
    Z, Zb = z_matrix(A), z_bar_matrix(A)
    q = A[0]**2 - A[1]**2 - A[2]**2 - A[3]**2
    qc = sp.conjugate(q)
    Zd, lam = Z.conjugate().T, sp.expand(Z * Z.conjugate())

    def row(m):
        return sum((lam[m, n] * SIGMA[n] for n in range(4)), sp.zeros(4))

    def col(m):
        return sum((lam[n, m] * SIGMA[n] for n in range(4)), sp.zeros(4))

    out = {
        "LT1_row": all(zero(Zd * SIGMA[m] * Z - row(m)) for m in range(4)),
        "LT1_col_fails": not all(zero(Zd * SIGMA[m] * Z - col(m))
                                 for m in range(4)),
        "LT2": all(zero(Z.conjugate() * SIGMA[m] * Zb.conjugate()
                        - qc * SIGMA[m]) for m in range(4)),
        "LT3": all(zero(Zb.conjugate() * SIGMA[m] * Z.conjugate()
                        - qc * SIGMA[m]) for m in range(4)),
        "LT4": all(zero(Z.T * SIGMA[m] * Zb.T - q * SIGMA[m])
                   for m in range(4)),
        "LT5": all(zero(Zb.T * SIGMA[m] * Z.T - q * SIGMA[m])
                   for m in range(4)),
        "chain": zero(sp.expand((Z * Z.conjugate()) * (Zb * Zb.conjugate()))
                      - q * qc * sp.eye(4)),
    }

    # spec forms on the guard, boost + rotation, exp-rewrite proof
    for name, al in (("boost", boost_alpha(sp.Symbol("phi", real=True))),
                     ("rot", rotation_alpha(sp.Symbol("theta", real=True)))):
        Zc, Zi = z_matrix(al), z_bar_matrix(al)      # guard: Z^-1 = Zbar
        Lc = sp.expand(Zc * Zc.conjugate())
        forms = {
            "I1": lambda m: sum((Lc[m, n] * (Zi.conjugate().T) * SIGMA[n]
                                 * Zi for n in range(4)), sp.zeros(4)),
            "I2": lambda m: Zc.conjugate() * SIGMA[m] * Zi.conjugate(),
            "I3": lambda m: Zi.conjugate() * SIGMA[m] * Zc.conjugate(),
            "I4": lambda m: Zc.T * SIGMA[m] * Zi.T,
            "I5": lambda m: Zi.T * SIGMA[m] * Zc.T,
        }
        for lab, f in forms.items():
            out[f"{name}_{lab}"] = all(
                sp.simplify(sp.expand((f(m) - SIGMA[m]).rewrite(sp.exp)))
                == sp.zeros(4) for m in range(4))
    return out


if __name__ == "__main__":
    for k, v in main().items():
        print(f"{k:16s}: {v}")
