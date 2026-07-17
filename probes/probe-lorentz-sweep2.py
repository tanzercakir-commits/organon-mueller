"""L5 probe, part 2: finish the hunt for the 20 still-unidentified
coefficient matrices.

New machinery tried here:
- structural lemma CANDIDATES: Sigma-bar^mu = g Sigma^mu g and
  Zbar = g Z g (checked first),
- FAMILY-SWAP channel: C = s·g·B in the mid family would be the same
  fact as "the sandwich lands in the OTHER family with coefficient
  s·B" — IF the lemma above held,
- all-pairs candidate library: every ordered product of two letters
  (64), plus I and g, each tried as B in C = s·B and C = s·(gB).

OUTCOME (recorded after the run — reviewer finding, L5): both lemma
candidates are FALSE (the i-carrying entries of Sigma^1/Sigma^3 do not
flip under g-conjugation) and the swap channel found ZERO matches; the
channel was therefore NOT adopted into discovery.py. What survived is
the all-pairs library: 20/20 identified, closing the space at 40
identities / 88 negatives. See discovery.py's falsified-conjecture
record and tests/test_lorentz_discovery.py::
test_falsified_conjecture_pins.

Run: python probes/probe-lorentz-sweep2.py
"""
import sympy as sp

from organon_mueller.lorentz import METRIC, SIGMA, SIGMA_BAR
from organon_mueller.lorentz.terms import (
    KNOWN_TEN, NAMES, classify_all, letter_matrices,
)

A = sp.symbols("s0 s1 s2 s3", complex=True)


def zero(m):
    return sp.expand(m) == sp.zeros(4)


def main():
    L = letter_matrices(A)
    g = sp.Matrix(METRIC)

    # structural lemmas first
    lem_sig = all(zero(sp.Matrix(SIGMA_BAR[m]) - g * sp.Matrix(SIGMA[m])
                       * g) for m in range(4))
    lem_z = zero(L["Zb"] - g * L["Z"] * g)
    print(f"lemma Sigma-bar = g Sigma g : {lem_sig}")
    print(f"lemma Zbar     = g Z g      : {lem_z}")

    cls = classify_all()
    unmatched = sorted(k for k, (kind, _) in cls.items()
                       if kind == "expansion-unmatched")

    q = A[0]**2 - A[1]**2 - A[2]**2 - A[3]**2
    scalars = {"1": sp.Integer(1), "q": q, "qbar": sp.conjugate(q),
               "qqbar": sp.expand(q * sp.conjugate(q))}
    pairs = {"I": sp.eye(4), "g": g}
    for xn in NAMES:
        for yn in NAMES:
            pairs[f"{xn}.{yn}"] = sp.expand(L[xn] * L[yn])

    def extract_C(x, mid, y):
        fam = SIGMA if mid == "S" else SIGMA_BAR
        return sp.Matrix(4, 4, lambda m, n: sp.expand(
            sp.trace(sp.Matrix(fam[n]) * L[x] * sp.Matrix(fam[m])
                     * L[y]) / 4))

    already = {("Z", "S", "Z"), ("Z", "Sb", "Z"),
               ("Zb", "S", "Zb"), ("Zb", "Sb", "Zb")}
    hits, misses = {}, []
    for k in unmatched:
        if k in already:
            continue
        x, mid, y = k
        C = extract_C(x, mid, y)
        found = None
        for s_name, s in scalars.items():
            for b_name, B in pairs.items():
                sB = sp.expand(s * B)
                if zero(C - sB):
                    found = (s_name, b_name, "same")
                    break
                if zero(C - sp.expand(g * sB)):
                    found = (s_name, b_name, "SWAP")
                    break
            if found:
                break
        if found:
            hits[k] = found
        else:
            misses.append(k)

    print(f"identified now: {len(hits)}/20; still dark: {len(misses)}")
    for k, v in sorted(hits.items()):
        print(f"  {k} -> {v}")
    for k in misses:
        print(f"  DARK {k}")


if __name__ == "__main__":
    main()
