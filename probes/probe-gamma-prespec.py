"""Stage-13 PRE-SPEC probe: Symmetry 12,1790 (2020) general geometry.

Setup (paper App. A): dipole 1 VERTICAL (y) at origin; dipole 2 at angle
theta in xy, positioned at r = d*u, u = (C1C2, S1, C1S2). Plane wave +z.
e1 = e^{ikd} (dipole-dipole path), e2 = e^{ik r_z} (z-offset drive phase).
delta1_s = k^2(A + S1^2 B), delta2_s = k^2(C1C2S1B)  [SYMMETRY defs!]
Coupling matrix on xy components: M = e1 k^2 (A I + B w w^T), w=(C1C2,S1).

Q1: which far-field bookkeeping reproduces Eq. A11's J (forward z)?
Q2: scalar reduction (dipole1 along y, dipole2 along n(theta)) == full 2x2.
Q3: Case A/B: JA = g[[0,0],[mu,1]], JB = g[[0,-mu],[0,1]], JB == R(JA).
Q4: Perrin general identity: amp_B == amp_A for ANY J (sigma-transpose).
Q5: forward gamma component ~ e1 a1 a2 Delta1 (1 - e2^2)/2 (from A11).
"""
import numpy as np

rng = np.random.default_rng(20260713)
rc = lambda: complex(rng.standard_normal(), rng.standard_normal()) * 0.3
SIG = np.diag([1.0, -1.0])


def recip(J):
    return SIG @ J.T @ SIG


for trial in range(5):
    th = rng.uniform(0, 2 * np.pi)         # theta (dipole 2)
    f1, f2 = rng.uniform(0, 2 * np.pi, 2)  # phi1, phi2 (geometry)
    a1, a2, A, B = rc(), rc(), rc(), rc()
    k2 = 1.0  # absorb k^2 into A, B
    e1 = np.exp(1j * rng.uniform(0, 2 * np.pi))
    e2 = np.exp(1j * rng.uniform(0, 2 * np.pi))
    C1, S1, C2, S2 = np.cos(f1), np.sin(f1), np.cos(f2), np.sin(f2)
    a_, b_, c_ = np.cos(th) ** 2, np.cos(th) * np.sin(th), np.sin(th) ** 2
    J1 = np.array([[0, 0], [0, 1.0]])
    J2 = np.array([[a_, b_], [b_, c_]])
    w = np.array([C1 * C2, S1])
    M = e1 * k2 * (A * np.eye(2) + B * np.outer(w, w))

    d1s = k2 * (A + S1 ** 2 * B)
    d2s = k2 * (C1 * C2 * S1 * B)
    D1 = b_ * d1s + a_ * d2s
    D2 = c_ * d1s + b_ * d2s
    N = 1 - e1 ** 2 * a1 * a2 * (2 * b_ * d1s * d2s + c_ * d1s ** 2 + a_ * d2s ** 2)
    J_A11 = (1 / N) * (e2 * a1 * J1 + e2 * a2 * J2
                       + e1 * a1 * a2 * np.array(
                           [[0, D1], [e2 ** 2 * D1, (1 + e2 ** 2) * D2]]))

    # direct solve: p1 = a1 J1 (E0 + M p2); p2 = a2 J2 (e2 E0 + M p1)
    # (eps=1). Far field weights: try candidates.
    Tdir = {}
    for name, (w1f, w2f) in {
        "p1 + p2": (1, 1),
        "p1 + p2/e2": (1, 1 / e2),
        "e2 p1 + p2": (e2, 1),
        "e2(p1 + p2/e2)": (e2, 1),
    }.items():
        cols = []
        for E0 in (np.array([1, 0]), np.array([0, 1])):
            big = np.eye(4, dtype=complex)
            big[:2, 2:] = -a1 * J1 @ M
            big[2:, :2] = -a2 * J2 @ M
            rhs = np.concatenate([a1 * J1 @ E0, e2 * a2 * J2 @ E0])
            p = np.linalg.solve(big, rhs)
            cols.append(w1f * p[:2] + w2f * p[2:])
        Tdir[name] = np.column_stack(cols)
    best = min(Tdir, key=lambda n: np.max(np.abs(Tdir[n] - J_A11)))
    err = np.max(np.abs(Tdir[best] - J_A11))
    if trial < 2 or err > 1e-10:
        print(f"Q1 trial {trial}: best bookkeeping = '{best}' err={err:.2e}")

    # Q2 scalar reduction: p1 = P1 y_hat, p2 = P2 n(theta)
    n2 = np.array([np.cos(th), np.sin(th)])
    c12 = np.array([0, 1.0]) @ M @ n2     # coupling 2 -> 1
    c21 = n2 @ M @ np.array([0, 1.0])     # coupling 1 -> 2 (symmetric M)
    for E0 in (np.array([0.3 - 0.2j, 0.7 + 0.1j]),):
        E1d, E2d = np.array([0, 1.0]) @ E0, e2 * (n2 @ E0)
        den = 1 - a1 * a2 * c12 * c21
        P1 = a1 * (E1d + a2 * c12 * E2d) / den
        P2 = a2 * (E2d + a1 * c21 * E1d) / den
        big = np.eye(4, dtype=complex)
        big[:2, 2:] = -a1 * J1 @ M
        big[2:, :2] = -a2 * J2 @ M
        rhs = np.concatenate([a1 * J1 @ E0, e2 * a2 * J2 @ E0])
        p = np.linalg.solve(big, rhs)
        errs = max(np.max(np.abs(P1 * np.array([0, 1.0]) - p[:2])),
                   np.max(np.abs(P2 * n2 - p[2:])))
        if errs > 1e-10:
            print(f"Q2 FAIL trial {trial}: {errs:.2e}")

print("Q1/Q2 done")

# Q3: Case A/B (phi1=-45, phi2=0, theta=0, e2=1, in plane)
f1, f2, th = -np.pi / 4, 0.0, 0.0
C1, S1, C2 = np.cos(f1), np.sin(f1), np.cos(f2)
for trial in range(3):
    al, A, B = rc(), rc(), rc()
    e1 = np.exp(1j * rng.uniform(0, 2 * np.pi))
    delta = -B / 2  # k2=1
    mu = e1 * al * delta
    w = np.array([C1 * C2, S1])
    M = e1 * (A * np.eye(2) + B * np.outer(w, w))
    n1, n2v = np.array([0, 1.0]), np.array([1.0, 0])
    c = n1 @ M @ n2v
    assert abs(c - e1 * delta) < 1e-12  # coupling == e1*delta
    den = 1 - al ** 2 * c ** 2
    g = al / den  # eps=F=1
    # Case A: drive (E0x, E0y) along +z (both in plane, in phase);
    # detect +x: only p_y radiates; local frame: E_H'(from -z)=0, E_V=p1y
    JA = np.zeros((2, 2), dtype=complex)
    for col, E0 in enumerate((np.array([1.0, 0]), np.array([0, 1.0]))):
        E1d, E2d = n1 @ E0, n2v @ E0
        P1 = al * (E1d + al * c * E2d) / den
        JA[1, col] = P1
    JA_paper = g * np.array([[0, 0], [mu, 1]])
    okA = np.max(np.abs(JA - JA_paper)) < 1e-10
    # Case B: drive from -x, V=y drives dipole1 only, H=z drives none;
    # detect -z: transverse (x,y), local frame H' = -x (sign flip), V = y
    JB = np.zeros((2, 2), dtype=complex)
    for col, EHV in enumerate((("H",), ("V",))):
        if EHV[0] == "H":
            continue  # z-polarized: no drive
        E1d, E2d = 1.0, 0.0  # V drives dipole1 directly, dipole2 not (th=0)
        P1 = al * E1d / den
        P2 = al * (al * c * E1d) / den
        JB[0, col] = -P2  # H' = -x component
        JB[1, col] = P1
    JB_paper = g * np.array([[0, -mu], [0, 1]])
    okB = np.max(np.abs(JB - JB_paper)) < 1e-10
    okR = np.max(np.abs(recip(JA) - JB)) < 1e-10
    if not (okA and okB and okR):
        print(f"Q3 trial {trial}: A={okA} B={okB} R={okR}")
print("Q3 done")

# Q4: Perrin general: amp_A = v^dag J u ; amp_B = (sig u*)^dag R(J) (sig v*)
for trial in range(5):
    J = np.array([[rc(), rc()], [rc(), rc()]])
    u = np.array([rc(), rc()]); u /= np.linalg.norm(u)
    v = np.array([rc(), rc()]); v /= np.linalg.norm(v)
    ampA = np.conj(v) @ J @ u
    ampB = np.conj(SIG @ np.conj(u)) @ recip(J) @ (SIG @ np.conj(v))
    if abs(ampA - ampB) > 1e-12:
        print(f"Q4 FAIL: {ampA} vs {ampB}")
print("Q4 done")

# Q5: forward gamma from A11: h4 = i(J01-J10)/2 = i e1 a1 a2 D1 (1-e2^2)/(2N)
th, f1, f2 = 0.9, 0.7, 0.3
a1, a2, A, B = rc(), rc(), rc(), rc()
e1 = np.exp(1j * 0.8); e2 = np.exp(1j * 0.5)
C1, S1, C2 = np.cos(f1), np.sin(f1), np.cos(f2)
a_, b_, c_ = np.cos(th) ** 2, np.cos(th) * np.sin(th), np.sin(th) ** 2
d1s, d2s = A + S1 ** 2 * B, C1 * C2 * S1 * B
D1 = b_ * d1s + a_ * d2s
N = 1 - e1 ** 2 * a1 * a2 * (2 * b_ * d1s * d2s + c_ * d1s ** 2 + a_ * d2s ** 2)
J = (1 / N) * (e2 * a1 * np.array([[0, 0], [0, 1.0]])
               + e2 * a2 * np.array([[a_, b_], [b_, c_]])
               + e1 * a1 * a2 * np.array([[0, D1],
                                          [e2 ** 2 * D1, (1 + e2 ** 2) * (c_ * d1s + b_ * d2s)]]))
h4 = 1j * (J[0, 1] - J[1, 0]) / 2
pred = 1j * e1 * a1 * a2 * D1 * (1 - e2 ** 2) / (2 * N)
print("Q5 gamma:", np.isclose(h4, pred), "| zero at e2=1:",
      np.isclose((1 - 1 ** 2), 0))
