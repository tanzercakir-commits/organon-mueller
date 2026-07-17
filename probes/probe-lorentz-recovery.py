"""L4 pre-implementation probe (FROZEN-7): validate the sandwich
enumeration + trace-extraction classification that the self-recovery
gate will run.

Space: X · mid^mu · Y, X and Y over the 8-letter alphabet
{Z, Z*, Z^T, Zdag} x {plain, bar}, mid in {Sigma, Sigma-bar} — 128
sandwiches, NUMERIC ONLY here (two fixed seeds, genuinely complex
alpha). The classifier:

  1. extract C[m,n] = tr(DUAL^n · X mid^m Y)/4 in the mid family's own
     dual basis (trace-orthogonality),
  2. reconstruct and demand the expansion is exact (residual < tol),
  3. match C against s·B, s in {1, q, qbar, q qbar},
     B in {I, Lam, Lam^T, Lambar, Lambar^T}  (aliases via the L2 bonus
     theorem: Lambar = g Lam^T g, Lambar^T = g Lam g — the g-conjugates
     are not separate bases).

Expectation: the ten known identities (LT1–LT10) fall out with their
exact classes; anything extra is counted for L5 (no claims here).

Run: python probes/probe-lorentz-recovery.py
"""
import numpy as np
import sympy as sp

from organon_mueller.lorentz import SIGMA, SIGMA_BAR

SIG = [np.array(m, dtype=complex) for m in SIGMA]
SIGB = [np.array(m, dtype=complex) for m in SIGMA_BAR]
NAMES = ["Z", "Zc", "Zt", "Zd", "Zb", "Zbc", "Zbt", "Zbd"]
KNOWN = {
    ("Zd", "S", "Z"): ("1", "Lam"),
    ("Zc", "S", "Zbc"): ("qbar", "I"),
    ("Zbc", "S", "Zc"): ("qbar", "I"),
    ("Zt", "S", "Zbt"): ("q", "I"),
    ("Zbt", "S", "Zt"): ("q", "I"),
    ("Z", "Sb", "Zd"): ("1", "Lambar"),
    ("Zc", "Sb", "Zbc"): ("qbar", "I"),
    ("Zbc", "Sb", "Zc"): ("qbar", "I"),
    ("Zt", "Sb", "Zbt"): ("q", "I"),
    ("Zbt", "Sb", "Zt"): ("q", "I"),
}
TOL = 1e-9


def letters(a):
    z = sum(a[m] * SIG[m] for m in range(4))
    zb = sum(a[m] * SIGB[m] for m in range(4))
    return dict(zip(NAMES, [z, z.conj(), z.T, z.conj().T,
                            zb, zb.conj(), zb.T, zb.conj().T]))


def classify(a):
    L = letters(a)
    q = a[0]**2 - a[1]**2 - a[2]**2 - a[3]**2
    lam = L["Z"] @ L["Zc"]
    lamb = L["Zb"] @ L["Zbc"]
    bases = [("I", np.eye(4, dtype=complex)), ("Lam", lam),
             ("LamT", lam.T), ("Lambar", lamb), ("LambarT", lamb.T)]
    scalars = [("1", 1.0 + 0j), ("q", q), ("qbar", np.conj(q)),
               ("qqbar", q * np.conj(q))]
    # sanity: the 20 candidates must be pairwise distinct at this alpha
    cand = [s * B for _, s in scalars for _, B in bases]
    for i in range(len(cand)):
        for j in range(i + 1, len(cand)):
            assert np.linalg.norm(cand[i] - cand[j]) > 1e-6, "collision"

    out = {}
    for mid_name, fam, dual in (("S", SIG, SIG), ("Sb", SIGB, SIGB)):
        for xn in NAMES:
            for yn in NAMES:
                M = [L[xn] @ fam[m] @ L[yn] for m in range(4)]
                C = np.array([[np.trace(dual[n] @ M[m]) / 4
                               for n in range(4)] for m in range(4)])
                R = [sum(C[m, n] * fam[n] for n in range(4))
                     for m in range(4)]
                if max(np.linalg.norm(M[m] - R[m]) for m in range(4)) \
                        > TOL * 100:
                    out[(xn, mid_name, yn)] = ("no-expansion", None)
                    continue
                hit = None
                for sn, s in scalars:
                    for bn, B in bases:
                        if np.linalg.norm(C - s * B) <= TOL * 100:
                            hit = (sn, bn)
                            break
                    if hit:
                        break
                out[(xn, mid_name, yn)] = ("match", hit) if hit \
                    else ("expansion-unmatched", None)
    return out


def main():
    results = []
    for seed in (20260716, 20260717):
        rng = np.random.default_rng(seed)
        a = rng.normal(size=4) + 1j * rng.normal(size=4)
        assert abs(a[0]**2 - a[1]**2 - a[2]**2 - a[3]**2) > 0.1
        results.append(classify(a))
    agree = results[0] == results[1]

    kinds = {}
    for k, (kind, _) in results[0].items():
        kinds[kind] = kinds.get(kind, 0) + 1
    matches = {k: v for k, (kind, v) in results[0].items()
               if kind == "match"}

    print(f"seeds agree          : {agree}")
    print(f"class counts         : {kinds}")
    print(f"total matches        : {len(matches)}")
    known_ok = all(matches.get(k) == v for k, v in KNOWN.items())
    print(f"all 10 knowns found  : {known_ok}")
    for k, v in KNOWN.items():
        got = matches.get(k)
        flag = "OK " if got == v else "MISS"
        print(f"  {flag} {k}: want {v}, got {got}")
    extra = sorted(k for k in matches if k not in KNOWN)
    print(f"extra matches (L5)   : {len(extra)}")
    for k in extra:
        print(f"      {k}: {matches[k]}")


if __name__ == "__main__":
    main()
