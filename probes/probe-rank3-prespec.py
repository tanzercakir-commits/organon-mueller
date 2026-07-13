"""Stage-10 PRE-SPEC numeric probe (stage-9 lesson: probe before spec).

Question 1: pairs {type1,type2} and {type1,type3} — does the sequential
peel work? (B-component solved from center/edge minors that never touch
type-1's corner support; subtract; delegate residual to the stage-8
rank-2 solver.)

Question 2: pair {type2,type3} — identifiable at all? (supports fully
overlap; center minor goes quadratic). Multi-start least-squares: do all
zero-residual solutions agree on the symmetric parts?
"""
import numpy as np

import sys
sys.path.insert(0, "/home/claude/organon-mueller/src")

import sympy as sp
from organon_mueller.decomposition.covariance import SYMMETRY_TEMPLATES
from organon_mueller.decomposition.solve import decompose

rng = np.random.default_rng(20260713)


def tpl(sym, x, w):
    template, _ = SYMMETRY_TEMPLATES[sym]
    xs, ws = sp.symbols("xs", positive=True), sp.symbols("ws", complex=True)
    m = template(xs, ws).subs({xs: sp.Float(x, 30), ws: sp.sympify(complex(w))})
    return np.array(sp.matrix2numpy(sp.Matrix(m).evalf(), dtype=complex))


def rand_sym_pure(sym):
    total = 1.0 if sym == "type1" else 0.5
    x = float(rng.uniform(0.15, total - 0.15))
    xbar = total - x
    w = np.sqrt(x * xbar) * np.exp(1j * float(rng.uniform(0, 2 * np.pi)))
    return tpl(sym, x, w), x, w


def rand_pure():
    u = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    u /= np.linalg.norm(u)
    return np.outer(u, u.conj()), u


# ---------------------------------------------------------------- Q1: {1,B}
def peel_and_delegate(H, bsym):
    """Solve B-component (type2/3) from minors avoiding corners, subtract,
    delegate to stage-8 solver for type1 + generic pure."""
    h = H
    if bsym == "type2":
        den_c = h[1, 1] + h[2, 2] - h[1, 2] - h[2, 1]
        xB = (h[1, 1] * h[2, 2] - h[1, 2] * h[2, 1]) / den_c          # a2*Kbar
        den_w = h[1, 1] - h[1, 2]
        wB = (h[0, 2] * (h[1, 1] - xB) - h[0, 1] * (h[1, 2] - xB)) / den_w
    else:  # type3: center [[e~, -e~],[-e~, e~]], edges (0,1)=v, (0,2)=-v
        den_c = h[1, 1] + h[2, 2] + h[1, 2] + h[2, 1]
        xB = (h[1, 1] * h[2, 2] - h[1, 2] * h[2, 1]) / den_c          # a2*Ebar
        den_w = h[1, 1] + h[1, 2]
        wB = (h[0, 1] * (h[1, 2] + xB) - h[0, 2] * (h[1, 1] - xB)) / den_w
    assert abs(xB.imag) < 1e-9, f"xB not real: {xB}"
    xB = xB.real
    kB = (wB * np.conj(wB)).real / xB
    alphaB = 2 * (xB + kB)
    TB = tpl(bsym, kB, wB)  # template takes (corner primary k, edge w)
    Hres = (H - TB) / (1 - alphaB)
    r = decompose(covariance=Hres, symmetry="type1")
    return dict(xB=xB, wB=wB, kB=kB, alphaB=alphaB,
                alphaA=r.alpha1 * (1 - alphaB), hA=r.h1,
                alphaG=(1 - r.alpha1) * (1 - alphaB), hG=r.h2)


print("=" * 70)
for bsym in ("type2", "type3"):
    print(f"Q1  pair {{type1, {bsym}}}: sequential peel")
    ok = True
    for trial in range(5):
        hA, xA, wA = rand_sym_pure("type1")
        hB, xB_true, wB_true = rand_sym_pure(bsym)
        hG, u = rand_pure()
        aA, aB = float(rng.uniform(0.2, 0.4)), float(rng.uniform(0.2, 0.4))
        aG = 1 - aA - aB
        H = aA * hA + aB * hB + aG * hG
        try:
            out = peel_and_delegate(H, bsym)
        except Exception as e:
            print(f"  trial {trial}: FAIL: {e}")
            ok = False
            continue
        # template stores corner primary = K (outer); true corner = xB_true
        errs = [
            abs(out["alphaB"] - aB),
            abs(out["kB"] - aB * xB_true),
            abs(out["wB"] - aB * wB_true),
            abs(out["alphaA"] - aA),
            np.max(np.abs(out["hA"] - hA)),
            np.max(np.abs(out["hG"] - hG)),
        ]
        if max(errs) > 1e-7:
            print(f"  trial {trial}: RECOVERY DRIFT {max(errs):.2e}")
            ok = False
    print(f"  -> {'EXACT (5/5)' if ok else 'PROBLEM'}")

# wrong-pair honesty: {1,3} solver on {1,2} data must FAIL a guard
print("Q1b cross-pair guard: type3-peel on {type1,type2} data")
hA, *_ = rand_sym_pure("type1")
hB, *_ = rand_sym_pure("type2")
hG, _ = rand_pure()
H = 0.3 * hA + 0.4 * hB + 0.3 * hG
try:
    out = peel_and_delegate(H, "type3")
    print(f"  !! silently returned alphaB={out['alphaB']:.4f} "
          f"alphaA={out['alphaA']:.4f}  <- must be caught by residual guards")
except Exception as e:
    print(f"  raised as desired: {type(e).__name__}: {str(e)[:80]}")

# ---------------------------------------------------------------- Q2: {2,3}
print("=" * 70)
print("Q2  pair {type2, type3}: identifiability via multi-start LSQ")
from scipy.optimize import least_squares

hB2, x2t, w2t = rand_sym_pure("type2")
hB3, x3t, w3t = rand_sym_pure("type3")
hG, u = rand_pure()
a2, a3 = 0.35, 0.3
aG = 1 - a2 - a3
H = a2 * hB2 + a3 * hB3 + aG * hG


def unpack(p):
    k2, wr2, wi2, e3, vr3, vi3 = p[:6]
    c = p[6:14].reshape(4, 2) @ np.array([1, 1j])
    T2 = tpl("type2", abs(k2) + 1e-12, wr2 + 1j * wi2)
    T3 = tpl("type3", abs(e3) + 1e-12, vr3 + 1j * vi3)
    return T2, T3, np.outer(c, c.conj())


def resid(p):
    T2, T3, G = unpack(p)
    d = H - T2 - T3 - G
    return np.concatenate([d.real.ravel(), d.imag.ravel()])


sols = []
for start in range(12):
    p0 = rng.uniform(0.05, 0.6, 14)
    p0[6:] = rng.standard_normal(8) * 0.5
    r = least_squares(resid, p0, method="lm", max_nfev=20000)
    if r.cost < 1e-18:
        T2, T3, G = unpack(r.x)
        sols.append((T2, T3, G, r.cost))
print(f"  zero-residual solutions found: {len(sols)}/12")
if sols:
    ref2, ref3 = sols[0][0], sols[0][1]
    dev2 = max(np.max(np.abs(s[0] - ref2)) for s in sols)
    dev3 = max(np.max(np.abs(s[1] - ref3)) for s in sols)
    tru2 = np.max(np.abs(ref2 - a2 * hB2))
    tru3 = np.max(np.abs(ref3 - a3 * hB3))
    print(f"  spread across solutions: T2 {dev2:.2e}  T3 {dev3:.2e}")
    print(f"  distance to TRUTH:       T2 {tru2:.2e}  T3 {tru3:.2e}")
    print("  -> IDENTIFIABLE" if max(dev2, dev3, tru2, tru3) < 1e-6
          else "  -> NON-UNIQUE or biased (guard out / needs exact theory)")
