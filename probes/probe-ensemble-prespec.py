"""Stage-14 PRE-SPEC probe: OA-in-ensemble paper (Kuntman & Kuntman).

Setup: 3D rank-1 dipoles m, n (unit vectors); u = r/D; delta = (n.m)A +
(n.u)(m.u)B (k^2 absorbed); mu = eps*alpha/(1-(alpha*delta)^2); drives
e^{-+ik rz/2} (n behind m); forward far-field phases e^{+-ik rz/2}.

Q1: scalar-reduced solve == paper Eqs. 21-24 (Pnx, Pmx, Pny, Pmy).
Q2: forward Jones == Eqs. 26-29; gamma_z == -2 mu alpha delta
    (n x m)_z sin(k rz)  [paper prints (m x n)_z — check labeling].
Q3: x-scattering Jones via Eq. 32 frame (x'=-z, y'=y, phases rx) ->
    gamma_x == Eq. 33 (two-term split Eqs. 34-35).
Q4: backscattering via Eq. 8 -> gamma_-z vs Eq. 9 (SUSPECT: eps*alpha*mu
    double-counts eps*alpha since mu = eps*alpha/(...)).
Q5: ensemble sums (seeded): achiral -> sum gamma_z ~ 0; chiral coupled ->
    != 0; delta=0 -> gamma_z = 0 pointwise.
"""
import numpy as np

rng = np.random.default_rng(20260713)
rc = lambda: complex(rng.standard_normal(), rng.standard_normal()) * 0.3
EPS = 1.0


def solve_dimer3d(m, n, rz, alpha, delta, Ex, Ey, k=1.0):
    """Scalar reduction: Pn = Qn * n, Pm = Qm * m (amplitudes along axes)."""
    en = np.exp(-1j * k * rz / 2) * (n[0] * Ex + n[1] * Ey)
    em = np.exp(+1j * k * rz / 2) * (m[0] * Ex + m[1] * Ey)
    mu = EPS * alpha / (1 - (alpha * delta) ** 2)
    qn = mu * (en + em * alpha * delta)
    qm = mu * (em + en * alpha * delta)
    return qn, qm


def jones_dir(m, n, rz, rx, alpha, delta, direction, k=1.0):
    """2x2 Jones for detection along +z, +x or -z (paper frames)."""
    cols = []
    for Ex, Ey in ((1, 0), (0, 1)):
        qn, qm = solve_dimer3d(m, n, rz, alpha, delta, Ex, Ey, k)
        pn, pm = qn * np.asarray(m * 0 + n, dtype=complex), qm * np.asarray(m, dtype=complex)
        if direction == "+z":
            fn, fm = np.exp(1j * k * rz / 2), np.exp(-1j * k * rz / 2)
            cols.append((fn * pn[:2] + fm * pm[:2]))
        elif direction == "+x":
            fn, fm = np.exp(1j * k * rx / 2), np.exp(-1j * k * rx / 2)
            # x' = -z, y' = y
            ex = -(fn * pn[2] + fm * pm[2])
            ey = fn * pn[1] + fm * pm[1]
            cols.append(np.array([ex, ey]))
        else:  # -z backscatter: x' = -x, y' = y (Eq. 8)
            fn, fm = np.exp(-1j * k * rz / 2), np.exp(+1j * k * rz / 2)
            ex = -(fn * pn[0] + fm * pm[0])
            ey = fn * pn[1] + fm * pm[1]
            cols.append(np.array([ex, ey]))
    return np.column_stack(cols)


def gam(J):
    return 1j * (J[0, 1] - J[1, 0])


def rand_unit():
    v = rng.standard_normal(3)
    return v / np.linalg.norm(v)


ok12 = True
for t in range(6):
    m, n = rand_unit(), rand_unit()
    rz, rx = rng.uniform(-2, 2), rng.uniform(-2, 2)
    alpha, delta = rc(), rc()
    mu = EPS * alpha / (1 - (alpha * delta) ** 2)
    # Q1: paper Eqs. 21-24
    for Ex, Ey in ((1, 0), (0, 1), (0.3 - 0.2j, 0.7 + 0.1j)):
        qn, qm = solve_dimer3d(m, n, rz, alpha, delta, Ex, Ey)
        e_m, e_p = np.exp(-1j * rz / 2), np.exp(1j * rz / 2)
        pnx = mu * n[0] * ((e_m * n[0] + e_p * m[0] * alpha * delta) * Ex
                           + (e_m * n[1] + e_p * m[1] * alpha * delta) * Ey)
        pmx = mu * m[0] * ((e_p * m[0] + e_m * n[0] * alpha * delta) * Ex
                           + (e_p * m[1] + e_m * n[1] * alpha * delta) * Ey)
        if abs(qn * n[0] - pnx) + abs(qm * m[0] - pmx) > 1e-12:
            ok12 = False
    # Q2: forward Jones Eqs. 26-29 + gamma_z
    J = jones_dir(m, n, rz, rx, alpha, delta, "+z")
    ad = alpha * delta
    J11 = mu * (n[0] ** 2 + m[0] ** 2 + 2 * n[0] * m[0] * np.cos(rz) * ad)
    J12 = mu * (n[0] * n[1] + m[0] * m[1]
                + n[0] * m[1] * np.exp(1j * rz) * ad
                + m[0] * n[1] * np.exp(-1j * rz) * ad)
    J21 = mu * (n[0] * n[1] + m[0] * m[1]
                + n[0] * m[1] * np.exp(-1j * rz) * ad
                + m[0] * n[1] * np.exp(1j * rz) * ad)
    J22 = mu * (n[1] ** 2 + m[1] ** 2 + 2 * n[1] * m[1] * np.cos(rz) * ad)
    if np.max(np.abs(J - np.array([[J11, J12], [J21, J22]]))) > 1e-12:
        ok12 = False
    gz = gam(J)
    nxm_z = n[0] * m[1] - m[0] * n[1]          # (n x m)_z
    mxn_z = m[0] * n[1] - n[0] * m[1]          # (m x n)_z
    pred_nxm = -2 * mu * ad * nxm_z * np.sin(rz)
    pred_mxn = -2 * mu * ad * mxn_z * np.sin(rz)
    if abs(gz - pred_nxm) > 1e-12:
        ok12 = False
    if t == 0:
        print("Q2 gamma_z labeling: (n x m)_z err",
              abs(gz - pred_nxm), "| (m x n)_z err", abs(gz - pred_mxn))
print("Q1+Q2:", "OK" if ok12 else "PROBLEM")

# Q3: gamma_x vs Eq. 33
ok3 = True
for t in range(5):
    m, n = rand_unit(), rand_unit()
    rz, rx = rng.uniform(-2, 2), rng.uniform(-2, 2)
    alpha, delta = rc(), rc()
    mu = EPS * alpha / (1 - (alpha * delta) ** 2)
    J = jones_dir(m, n, rz, rx, alpha, delta, "+x")
    gx = gam(J)
    ad = alpha * delta
    g1 = -1j * mu * (n[1] * (n[0] + n[2]) * np.exp(-1j * (rz - rx) / 2)
                     + m[1] * (m[0] + m[2]) * np.exp(1j * (rz - rx) / 2))
    g2 = -1j * mu * ad * ((n[2] * m[1] + n[1] * m[0]) * np.exp(1j * (rz + rx) / 2)
                          + (m[2] * n[1] + m[1] * n[0]) * np.exp(-1j * (rz + rx) / 2))
    if abs(gx - (g1 + g2)) > 1e-12:
        ok3 = False
        if t < 2:
            print(f"Q3 t{t}: gx={gx:.6f} vs eq33={(g1+g2):.6f} "
                  f"diff={abs(gx-(g1+g2)):.2e}")
print("Q3 (Eq. 33):", "OK" if ok3 else "MISMATCH — investigate")

# Q4: backscatter gamma vs Eq. 9
ok4a = ok4b = True
for t in range(5):
    m, n = rand_unit(), rand_unit()
    rz = rng.uniform(-2, 2)
    alpha, delta = rc(), rc()
    mu = EPS * alpha / (1 - (alpha * delta) ** 2)
    J = jones_dir(m, n, rz, 0.0, alpha, delta, "-z")
    gmz = gam(J)
    ad = alpha * delta
    core = (n[0] * n[1] * np.exp(-1j * rz) + m[0] * m[1] * np.exp(1j * rz)
            + (n[0] * m[1] + m[0] * n[1]) * ad)
    eq9 = -2j * EPS * alpha * mu * core            # as printed
    alt = -2j * mu * core                          # without extra eps*alpha
    if abs(gmz - eq9) > 1e-12:
        ok4a = False
    if abs(gmz - alt) > 1e-12:
        ok4b = False
print(f"Q4 backscatter: printed Eq.9 match={ok4a} | mu-only match={ok4b}")

# Q5: ensemble sums (orthogonal dimers, Fig. 2 geometry)
def ortho_pair():
    u, v = rand_unit(), rand_unit()
    z = np.cross(u, v); z /= np.linalg.norm(z)
    e1 = u / np.linalg.norm(u)
    e2 = np.cross(z, e1)
    mm = (e1 + e2) / np.sqrt(2)
    nn = (e1 - e2) / np.sqrt(2)
    return mm, nn, z


alpha = 0.4 + 0.2j
for tag, chiral, delta in (("achiral+coupled", False, 0.3 + 0.1j),
                           ("chiral+coupled", True, 0.3 + 0.1j),
                           ("chiral+uncoupled", True, 0.0)):
    tot, tota = 0, 0
    for _ in range(4000):
        mm, nn, z = ortho_pair()
        d = 1.3
        r = d * (mm - nn + (z if chiral else 0)) / np.sqrt(3 if chiral else 2)
        rz = r[2]
        J = jones_dir(mm, nn, rz, r[0], alpha, delta, "+z")
        g = gam(J)
        tot += g; tota += abs(g)
    print(f"Q5 {tag}: |sum g|/N={abs(tot)/4000:.2e}  sum|g|/N={tota/4000:.3e}")
