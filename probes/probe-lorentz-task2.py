"""L2 pre-implementation probe (FROZEN-7): DISCOVER the five Sigma-bar
identities the work order's Task 2 asks for.

Method: the Sigma basis is trace-orthogonal (tr(S^m S^n) = 4 delta —
verified), so the coefficient matrix C of any Sigma-bar expansion is
extracted exactly by traces; C is then IDENTIFIED against candidate
closed forms.

Findings (locked in tests/test_lorentz_task2.py):

1. Lambda-type (LT6): Z Sbar^mu Zdag = C^mu_nu Sbar^nu with
   C = g Lambda^T g = Lambda(Zbar)  — two identifications whose equality
   is itself a BONUS THEOREM: Lambda(Zbar) = g Lambda(Z)^T g, guard-free.
   On the guard (Lambda^T g Lambda = g) C = Lambda^{-1}, giving the
   spec-mirror form  Sbar^mu = Lambda^mu_nu Z Sbar^nu Zdag  — the exact
   dual of Task-1's I1 (the sandwich swaps (Z^-1)dag..Z^-1 <-> Z..Zdag).
   Plain Lambda, Lambda^T, g Lambda g and Lambda(Zbar)^T all FAIL as C
   (negative pins).
2. Sandwich family (LT7-LT10): with Sbar in the middle the SAME scalar
   factors appear as in the Sigma family:
     Z*  Sbar Zbar* = conj(q) Sbar        Zbar* Sbar Z*  = conj(q) Sbar
     Z^T Sbar Zbar^T = q Sbar             Zbar^T Sbar Z^T = q Sbar
   On the guard q = 1 these are the spec-style forms
   Sbar^mu = Z* Sbar^mu (Z^-1)* etc., for boosts AND rotations alike.

Run: python probes/probe-lorentz-task2.py
"""
import sympy as sp

from organon_mueller.lorentz import (
    METRIC, SIGMA, SIGMA_BAR, z_bar_matrix, z_matrix,
)

A = sp.symbols("a0 a1 a2 a3", complex=True)


def zero(m):
    return sp.expand(m) == sp.zeros(4)


def main() -> dict:
    Z, Zb = z_matrix(A), z_bar_matrix(A)
    q = sp.expand(A[0]**2 - A[1]**2 - A[2]**2 - A[3]**2)
    qc = sp.conjugate(q)
    lam = sp.expand(Z * Z.conjugate())
    Zd = Z.conjugate().T

    out = {
        "trace_orthogonal": all(
            sp.trace(SIGMA[i] * SIGMA[j]) == (4 if i == j else 0)
            for i in range(4) for j in range(4)),
        "LT7": all(zero(Z.conjugate() * SIGMA_BAR[m] * Zb.conjugate()
                        - qc * SIGMA_BAR[m]) for m in range(4)),
        "LT8": all(zero(Zb.conjugate() * SIGMA_BAR[m] * Z.conjugate()
                        - qc * SIGMA_BAR[m]) for m in range(4)),
        "LT9": all(zero(Z.T * SIGMA_BAR[m] * Zb.T - q * SIGMA_BAR[m])
                   for m in range(4)),
        "LT10": all(zero(Zb.T * SIGMA_BAR[m] * Z.T - q * SIGMA_BAR[m])
                    for m in range(4)),
    }

    # extract C for the Lambda-type identity and identify it
    X = [sp.expand(Z * SIGMA_BAR[m] * Zd) for m in range(4)]
    C = sp.zeros(4)
    for m in range(4):
        for n in range(4):
            eta = 1 if n == 0 else -1
            C[m, n] = sp.expand(sp.trace(SIGMA[n] * X[m]) / 4 * eta)
    out["LT6_C_eq_gLTg"] = zero(C - METRIC * lam.T * METRIC)
    out["LT6_C_eq_lambda_zbar"] = zero(C - sp.expand(Zb * Zb.conjugate()))
    out["bonus_lambda_zbar_eq_gLTg"] = zero(
        sp.expand(Zb * Zb.conjugate()) - METRIC * lam.T * METRIC)
    out["neg_C_is_not_lambda"] = not zero(C - lam)
    out["neg_C_is_not_lambdaT"] = not zero(C - lam.T)
    out["neg_C_is_not_gLg"] = not zero(C - METRIC * lam * METRIC)
    return out


if __name__ == "__main__":
    for k, v in main().items():
        print(f"{k:26s}: {v}")
