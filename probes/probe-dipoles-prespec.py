"""Stage-12 PRE-SPEC numeric probe: PRB 98,045410 mechanism checks.

Q1: direct 4x4 solve of the coupled-dipole system (Eq. 41) == the paper's
    closed forms (14-17) == the decomposition T = gamma[a1 J1 + a2 J2 +
    a1 a2 Lam Jint] (Eq. 25), for random complex parameters.
Q2: det(A) == lam1*lam2*(lam1*lam2 - Lam^2) (Eq. 42 structure).
Q3: hybrid frequencies (45): quartic roots match the closed form.
Q4: hybrid-basis identity t = nu+ h+ + nu- h- and <h+|h-> = 0 when g1=g2.
Q5: Eq. 70 inversion (phi1=90, phi2=135).
Q6: dephased J'int covariance 4th component vs the paper's PRINTED Eq. 37.
    ARCHIVAL NOTE: Q6 prints False BY DESIGN — that False *is* the M30(a)
    discovery: printed Eq. 37 is 2x the paper's own Eq. 29 half-convention;
    the consistent value is -(i/2) sin(phi1-phi2)(1-e^{i chi}), anchored in
    tests/test_dipoles.py.
"""
import numpy as np

rng = np.random.default_rng(20260713)
rc = lambda: complex(rng.standard_normal(), rng.standard_normal()) * 0.3


def jones(phi):
    C, S = np.cos(phi), np.sin(phi)
    return np.array([[C * C, C * S], [C * S, S * S]])


def hvec(J):
    return 0.5 * np.array([J[0, 0] + J[1, 1], J[0, 0] - J[1, 1],
                           J[0, 1] + J[1, 0], 1j * (J[0, 1] - J[1, 0])])


ok = True
for trial in range(6):
    phi1, phi2 = rng.uniform(0, 2 * np.pi, 2)
    a1, a2, d1, d2 = rc(), rc(), rc(), rc()
    eps, beta = 1.0, 1.0  # overall factors, keep 1 for the probe
    C1, S1, C2, S2 = np.cos(phi1), np.sin(phi1), np.cos(phi2), np.sin(phi2)
    aa1, bb1, cc1 = C1 * C1, C1 * S1, S1 * S1
    aa2, bb2, cc2 = C2 * C2, C2 * S2, S2 * S2
    lam1, lam2 = 1 / a1, 1 / a2
    Lam = C1 * C2 * d1 + S1 * S2 * d2

    # 4x4 system (Eq. 41): A P = E_drive; drive = eps * (a_i, b_i / b_i, c_i) E0
    A = np.array([
        [lam1, 0, -d1 * aa1, -d2 * bb1],
        [0, lam1, -d1 * bb1, -d2 * cc1],
        [-d1 * aa2, -d2 * bb2, lam2, 0],
        [-d1 * bb2, -d2 * cc2, 0, lam2],
    ])
    # Q2: det structure
    det_lhs = np.linalg.det(A)
    det_rhs = lam1 * lam2 * (lam1 * lam2 - Lam ** 2)
    if abs(det_lhs - det_rhs) > 1e-10 * (1 + abs(det_rhs)):
        print(f"Q2 FAIL trial {trial}: det {det_lhs} vs {det_rhs}")
        ok = False

    T = np.zeros((2, 2), dtype=complex)
    for col, E0 in enumerate((np.array([1, 0]), np.array([0, 1]))):
        # note the drive on dipole i is eps * J_i E0 scaled by... Eq 38 RHS:
        # eps*alpha_i*(a_i E0x + b_i E0y, ...) but A has lam=1/alpha ->
        # RHS of A P = E is eps*(J_i E0) rows (alpha cancels into lam)
        E = np.concatenate([eps * jones(phi1) @ E0, eps * jones(phi2) @ E0])
        P = np.linalg.solve(A, E)
        Escat = beta * (P[:2] + P[2:])
        T[:, col] = Escat
        # Q1b: closed forms (14-17)
        E1 = C1 * E0[0] + S1 * E0[1]
        E2 = C2 * E0[0] + S2 * E0[1]
        den = 1 - a1 * a2 * Lam ** 2
        p1 = eps * a1 * np.array([C1, S1]) * (E1 + a2 * Lam * E2) / den
        p2 = eps * a2 * np.array([C2, S2]) * (E2 + a1 * Lam * E1) / den
        if max(np.max(np.abs(p1 - P[:2])), np.max(np.abs(p2 - P[2:]))) > 1e-10:
            print(f"Q1b FAIL trial {trial}: closed forms mismatch")
            ok = False

    # Q1: decomposition (25)
    gamma = eps * beta / (1 - a1 * a2 * Lam ** 2)
    Jint = np.array([[2 * C1 * C2, C1 * S2 + C2 * S1],
                     [C1 * S2 + C2 * S1, 2 * S1 * S2]])
    T_dec = gamma * (a1 * jones(phi1) + a2 * jones(phi2) + a1 * a2 * Lam * Jint)
    if np.max(np.abs(T - T_dec)) > 1e-10:
        print(f"Q1 FAIL trial {trial}: {np.max(np.abs(T - T_dec)):.2e}")
        ok = False

    # Q4: hybrid basis identity
    g1, g2, gint = gamma * a1, gamma * a2, gamma * a1 * a2 * Lam
    sq = np.sqrt(g1 * g2)
    nup, num = sq + gint, sq - gint
    h1, h2 = hvec(jones(phi1)), hvec(jones(phi2))
    hint = hvec(Jint)
    hp = (g1 * h1 + g2 * h2) / (2 * sq) + hint / 2
    hm = (g1 * h1 + g2 * h2) / (2 * sq) - hint / 2
    t = hvec(T)
    if np.max(np.abs(nup * hp + num * hm - t)) > 1e-10:
        print(f"Q4 FAIL trial {trial}: hybrid identity")
        ok = False
    # orthogonality when g1 == g2 (geometric basis, Eq. 64)
    hp0, hm0 = (h1 + h2) / 2 + hint / 2, (h1 + h2) / 2 - hint / 2
    if abs(np.vdot(hp0, hm0)) > 1e-10:
        print(f"Q4b FAIL trial {trial}: <h+|h-> = {np.vdot(hp0, hm0)}")
        ok = False

print("Q1/Q1b/Q2/Q4:", "OK (6 trials)" if ok else "PROBLEM")

# Q3: hybrid frequencies (Eq. 45), no damping
w1, w2, eta1, eta2 = 1.3, 1.7, 0.21, 0.34
phi1, phi2 = 0.4, 1.1
d1, d2 = 0.15, -0.08  # real for the no-damping analysis
Lam = np.cos(phi1) * np.cos(phi2) * d1 + np.sin(phi1) * np.sin(phi2) * d2
# lam1*lam2 = Lam^2 with lam_i = (w_i^2 - w^2)/(eta_i w_i^2)
# -> (w1^2-w^2)(w2^2-w^2) = eta1 eta2 w1^2 w2^2 Lam^2 : quadratic in w^2
coef = [1, -(w1 ** 2 + w2 ** 2),
        w1 ** 2 * w2 ** 2 * (1 - eta1 * eta2 * Lam ** 2)]
roots = np.roots(coef)
wpm_paper = np.sqrt((w1 ** 2 + w2 ** 2 + np.array([1, -1]) * np.sqrt(
    (w1 ** 2 - w2 ** 2) ** 2 + 4 * w1 ** 2 * w2 ** 2 * eta1 * eta2 * Lam ** 2)) / 2)
print("Q3 roots:", np.sort(np.sqrt(roots.real)), "paper:", np.sort(wpm_paper))

# identical dipoles: w0 sqrt(1 +- eta Lam)
w0, eta = 1.5, 0.3
coef = [1, -2 * w0 ** 2, w0 ** 4 * (1 - eta ** 2 * Lam ** 2)]
roots = np.sort(np.sqrt(np.roots(coef).real))
paper = np.sort(w0 * np.sqrt(1 + np.array([1, -1]) * eta * Lam))
print("Q3b identical:", roots, "paper:", paper, "match:",
      np.allclose(roots, paper))

# Q5: Eq. 70 inversion at phi1=90deg, phi2=135deg
phi1, phi2 = np.pi / 2, 3 * np.pi / 4
g1t, g2t, gintt = rc(), rc(), rc()
h1, h2 = hvec(jones(phi1)), hvec(jones(phi2))
C1, S1, C2, S2 = np.cos(phi1), np.sin(phi1), np.cos(phi2), np.sin(phi2)
Jint = np.array([[2 * C1 * C2, C1 * S2 + C2 * S1],
                 [C1 * S2 + C2 * S1, 2 * S1 * S2]])
hint = hvec(Jint)
t = g1t * h1 + g2t * h2 + gintt * hint
h0v, h1v, h2v = t[0], t[1], t[2]
g1r = 2 * (h0v + h2v)
g2r = 2 * (h0v + h1v)
gintr = -np.sqrt(2) * (h0v + h1v + h2v)
print("Q5 inversion:", np.allclose([g1r, g2r, gintr], [g1t, g2t, gintt]))

# Q6: dephased interaction h-vector 4th component
chi = 0.7
phi1, phi2 = 0.3, 1.2
C1, S1, C2, S2 = np.cos(phi1), np.sin(phi1), np.cos(phi2), np.sin(phi2)
e = np.exp(1j * chi)
Jp = np.array([[C1 * C2 * (1 + e), C1 * S2 + C2 * S1 * e],
               [C1 * S2 * e + C2 * S1, S1 * S2 * (1 + e)]])
h4 = hvec(Jp)[3]
paper4 = -1j * np.sin(phi1 - phi2) * (1 - e)
print("Q6 4th comp:", np.isclose(h4, paper4),
      "| zero at chi=0:", np.isclose(hvec(np.array(
          [[2*C1*C2, C1*S2+C2*S1], [C1*S2+C2*S1, 2*S1*S2]]))[3], 0))
