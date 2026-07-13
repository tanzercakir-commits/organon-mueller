"""Reproduction probe for the egglog 13.2.0 large-graph pathology
(docs/egglog-large-graph-pathology.md). Rerun after every egglog upgrade:
if all four lines print the expected values, the pathology is gone and the
engine could return to a shared-graph design (decision M18 revisit).

Expected output on egglog 13.2.0:
    isolated  : mid==rhs  -> True   (correct)
    large     : mid==rhs  -> False  (pathology: unprovable in shared graph)
    extract(rhs) contains 'b' -> False (pathology: wrong class)
"""
from __future__ import annotations

from egglog import EGraph, eq

from organon_mueller.discovery.axioms import structural_rules, to_egglog
from organon_mueller.discovery.terms import Atom, Conj, Mul, enumerate_terms

A, B = Atom("a"), Atom("b")
RULES = structural_rules(("a", "b"))
MID = Mul(B, Mul(A, Conj(A)))   # b*(a*conj(a))
RHS = Mul(B, Mul(Conj(A), A))   # b*(conj(a)*a)


def check(egraph: EGraph, left, right) -> bool:
    try:
        egraph.check(eq(to_egglog(left)).to(to_egglog(right)))
        return True
    except Exception:
        return False


def main() -> None:
    iso = EGraph()
    iso.register(to_egglog(MID))
    iso.register(to_egglog(RHS))
    iso.run(RULES.saturate())
    print("isolated  : mid==rhs  ->", check(iso, MID, RHS))

    big = EGraph()
    for t in enumerate_terms(("a", "b"), 9, conj_normal=True):
        big.register(to_egglog(t))
    big.run(RULES.saturate())
    print("large     : mid==rhs  ->", check(big, MID, RHS))
    rep = str(big.extract(to_egglog(RHS)))
    print("extract(rhs) contains 'b' ->", '"b"' in rep, "| rep:", rep)


if __name__ == "__main__":
    main()
