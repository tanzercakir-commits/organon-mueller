"""L5 pre-implementation probe (FROZEN-7): the discovery sweep over the
128-sandwich space — what the work order's Task 3 asks for, run on the
L4 substrate (gate passed there).

Three questions:
1. The 6 EXTRA matches from L4 — certify symbolically; are they
   corollaries of LT1/LT6 via the conjugation lemma Z(α)* = Z(α*)ᵀ
   (i.e. same-family relatives), or independent?
2. The 24 expansion-unmatched sandwiches — extract their coefficient
   matrices C SYMBOLICALLY and hunt closed forms in an EXTENDED
   quadratic library (the L4 library only knew ZZ* and Z̄Z̄*-type
   bases; the second-kind quadratics ZZᵀ, ZZ†, Z̄Z̄ᵀ, Z̄Z̄†, ZᵀZ,
   Z†Z, ... are the natural new candidates).
3. The 88 no-expansion sandwiches — can the negative be certified
   symbolically (residual after dual-basis projection is nonzero as a
   polynomial), and how expensive is the full negative certification?

Everything printed is probe output — claims are locked only by the L5
tests that follow. Run: python probes/probe-lorentz-sweep.py
"""
import itertools

import numpy as np
import sympy as sp

from organon_mueller.lorentz import SIGMA, SIGMA_BAR
from organon_mueller.lorentz.terms import (
    KNOWN_TEN, NAMES, classify_all, letter_matrices,
)

A = sp.symbols("s0 s1 s2 s3", complex=True)


def zero(m):
    return sp.expand(m) == sp.zeros(4)


def main():
    cls = classify_all()
    matches = {k: v for k, (kind, v) in cls.items() if kind == "match"}
    extras = sorted(k for k in matches if k not in KNOWN_TEN)
    unmatched = sorted(k for k, (kind, _) in cls.items()
                       if kind == "expansion-unmatched")
    noexp = sorted(k for k, (kind, _) in cls.items()
                   if kind == "no-expansion")

    L = letter_matrices(A)
    q = A[0]**2 - A[1]**2 - A[2]**2 - A[3]**2
    lam = sp.expand(L["Z"] * L["Zc"])
    lamb = sp.expand(L["Zb"] * L["Zbc"])
    bases_l4 = {"I": sp.eye(4), "Lam": lam, "LamT": lam.T,
                "Lambar": lamb, "LambarT": lamb.T}
    scalars = {"1": sp.Integer(1), "q": q, "qbar": sp.conjugate(q),
               "qqbar": sp.expand(q * sp.conjugate(q))}

    def fam_of(mid):
        return SIGMA if mid == "S" else SIGMA_BAR

    def extract_C(x, mid, y):
        fam = fam_of(mid)
        return sp.Matrix(4, 4, lambda m, n: sp.expand(
            sp.trace(sp.Matrix(fam[n]) * L[x] * sp.Matrix(fam[m])
                     * L[y]) / 4))

    # -- 1. certify the six extras symbolically --------------------------
    print("== extras: symbolic certification against their L4 classes ==")
    for k in extras:
        s_name, b_name = matches[k]
        x, mid, y = k
        fam = fam_of(mid)
        sB = sp.expand(scalars[s_name] * bases_l4[b_name])
        ok = all(zero(L[x] * fam[m] * L[y]
                      - sum((sB[m, n] * fam[n] for n in range(4)),
                            sp.zeros(4)))
                 for m in range(4))
        print(f"  {k} = ({s_name},{b_name}) : {ok}")

    # -- 2. the 24 unmatched: extract C, hunt in extended library --------
    print("== unmatched: extended-library identification ==")
    second = {
        "ZZt": sp.expand(L["Z"] * L["Zt"]),
        "ZtZ": sp.expand(L["Zt"] * L["Z"]),
        "ZZd": sp.expand(L["Z"] * L["Zd"]),
        "ZdZ": sp.expand(L["Zd"] * L["Z"]),
        "ZbZbt": sp.expand(L["Zb"] * L["Zbt"]),
        "ZbtZb": sp.expand(L["Zbt"] * L["Zb"]),
        "ZbZbd": sp.expand(L["Zb"] * L["Zbd"]),
        "ZbdZb": sp.expand(L["Zbd"] * L["Zb"]),
        "ZcZt": sp.expand(L["Zc"] * L["Zt"]),
        "ZtZc": sp.expand(L["Zt"] * L["Zc"]),
    }
    ext = dict(bases_l4)
    for n, B in second.items():
        ext[n] = B
        ext[n + "_T"] = B.T
    hits, misses = {}, []
    for k in unmatched:
        x, mid, y = k
        C = extract_C(x, mid, y)
        found = None
        for s_name, s in scalars.items():
            for b_name, B in ext.items():
                if zero(C - sp.expand(s * B)):
                    found = (s_name, b_name)
                    break
            if found:
                break
        if found:
            hits[k] = found
            print(f"  {k} -> C = {found}")
        else:
            misses.append(k)
    print(f"  identified: {len(hits)}/24; unidentified: {len(misses)}")
    for k in misses[:4]:
        x, mid, y = k
        C = extract_C(x, mid, y)
        print(f"  UNIDENTIFIED {k}: C[0,:] = {list(C.row(0))}")

    # -- 3. no-expansion negative certificates: cost + sample ------------
    print("== no-expansion: symbolic negative certificates (sample 8) ==")
    import time
    t0 = time.time()
    neg_ok = 0
    for k in noexp[:8]:
        x, mid, y = k
        fam = fam_of(mid)
        C = extract_C(x, mid, y)
        resid_nonzero = any(
            not zero(L[x] * fam[m] * L[y]
                     - sum((C[m, n] * fam[n] for n in range(4)),
                           sp.zeros(4)))
            for m in range(4))
        neg_ok += bool(resid_nonzero)
    print(f"  sample negatives certified: {neg_ok}/8 "
          f"({time.time()-t0:.1f}s for 8 -> est full 88: "
          f"{(time.time()-t0)/8*88:.0f}s)")


if __name__ == "__main__":
    main()
