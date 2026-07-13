"""Stage-01 spike: can egglog's equality saturation host the quaternion
unit algebra (the noncommutative skeleton of the Stokes-Mueller state
formalism)?

Fragment modelled: {1, i, j, k} with negation and noncommutative
multiplication, Hamilton relations as rewrite rules.  Success criterion
(spec stage-01, section 6): saturate and derive i*j*k == -1 plus a
nontrivial equivalence, WITHOUT a commutativity axiom.

Run:  python spikes/egglog_quaternion.py
"""
from __future__ import annotations

from egglog import EGraph, Expr, constant, eq, rewrite, ruleset, vars_


class Q(Expr):
    """Quaternion-unit expressions (noncommutative monoid + negation)."""

    def __mul__(self, other: "Q") -> "Q": ...

    def __neg__(self) -> "Q": ...


ONE = constant("one", Q)
I = constant("i", Q)
J = constant("j", Q)
K = constant("k", Q)

a, b, c = vars_("a b c", Q)

quat = ruleset(
    # associativity (both directions so the e-graph holds all parenthesizations)
    rewrite((a * b) * c).to(a * (b * c)),
    rewrite(a * (b * c)).to((a * b) * c),
    # multiplicative unit
    rewrite(ONE * a).to(a),
    rewrite(a * ONE).to(a),
    # Hamilton relations
    rewrite(I * I).to(-ONE),
    rewrite(J * J).to(-ONE),
    rewrite(K * K).to(-ONE),
    rewrite(I * J).to(K),
    rewrite(J * K).to(I),
    rewrite(K * I).to(J),
    rewrite(J * I).to(-K),
    rewrite(K * J).to(-I),
    rewrite(I * K).to(-J),
    # negation is central
    rewrite((-a) * b).to(-(a * b)),
    rewrite(a * (-b)).to(-(a * b)),
    rewrite(-(-a)).to(a),
)


def main() -> None:
    egraph = EGraph()

    targets = {
        "i*j*k == -1": ((I * J) * K, -ONE),
        "(i*j)*(j*k) == j": ((I * J) * (J * K), J),
        "k*(k*k) == -k": (K * (K * K), -K),
        "(j*i)*k == 1": ((J * I) * K, ONE),
    }
    for lhs, _rhs in targets.values():
        egraph.register(lhs)

    egraph.run(quat.saturate())

    print("egglog quaternion spike results")
    print("-" * 40)
    all_ok = True
    for name, (lhs, rhs) in targets.items():
        try:
            egraph.check(eq(lhs).to(rhs))
            print(f"PASS  {name}")
        except Exception:
            print(f"FAIL  {name}")
            all_ok = False
    print("-" * 40)
    print("SPIKE", "SUCCESS" if all_ok else "FAILURE")


if __name__ == "__main__":
    main()
