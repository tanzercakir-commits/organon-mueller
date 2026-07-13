"""egglog model of the Z-algebra structural axioms (decision M11).

SOUNDNESS BOUNDARY — read before touching the rules:

* Commutation Za . Zb* = Zb* . Za (library identity I10) is axiomatized at
  the ATOM level only: `atom_i * conj(atom_j) = conj(atom_j) * atom_i`.
  The free-variable version `x * conj(y) = conj(y) * x` would be UNSOUND:
  with x = conj(u) it would force conj(u)*conj(v) = conj(v)*conj(u), i.e.
  commutativity of conjugated Z's, which is false (the Z algebra is a
  noncommutative biquaternion algebra).  Everything the free version could
  soundly derive is reachable from the atom rule plus associativity and
  conj distribution through saturation (verified empirically in the stage-2
  review: compound-word commutations are derived, unsound mixed instances
  stay separate).
* conj is elementwise: it distributes over products PRESERVING order,
  conj(x*y) = conj(x)*conj(y)  ((AB)^* = A^* B^*, not the dagger).
"""
from __future__ import annotations

from egglog import Expr, StringLike, rewrite, ruleset, vars_

from .terms import Atom, Conj, Mul, Scale, ScalarAtom, ScalarConj, Sum, Term

__all__ = ["ZTerm", "STerm", "structural_rules", "to_egglog", "scalar_to_egglog"]


class STerm(Expr):
    """egglog sort for OPAQUE scalars (stage 7, M10/K23): only atoms and
    conjugation — no scalar arithmetic exists on this sort."""

    def __init__(self, name: StringLike) -> None: ...

    def conj(self) -> "STerm": ...


class ZTerm(Expr):
    """egglog expression sort for abstract Z-algebra terms."""

    def __init__(self, name: StringLike) -> None: ...

    def __mul__(self, other: "ZTerm") -> "ZTerm": ...

    def __add__(self, other: "ZTerm") -> "ZTerm": ...

    def conj(self) -> "ZTerm": ...

    def scaled(self, coeff: STerm) -> "ZTerm": ...


def structural_rules(atom_names: tuple[str, ...]):
    """Ruleset: associativity, conj involution/distribution, atom commutation,
    and (stage 7, design-note table ONLY — rule K24) the Sum/Scale axioms.

    Terms without Sum/Scale nodes are unaffected by the added rules (typed
    pattern matching), so pre-stage-7 behavior is unchanged (M27/K11).
    """
    x, y, z = vars_("x y z", ZTerm)
    c, d = vars_("c d", STerm)
    rules = [
        # associativity, both directions
        rewrite((x * y) * z).to(x * (y * z)),
        rewrite(x * (y * z)).to((x * y) * z),
        # conj is an involution
        rewrite(x.conj().conj()).to(x),
        # conj distributes over products, ORDER-PRESERVING (elementwise)
        rewrite((x * y).conj()).to(x.conj() * y.conj()),
        rewrite(x.conj() * y.conj()).to((x * y).conj()),
        # ---- stage 7: Sum/Scale (sound per design-note review) ----
        # matrix addition is commutative and associative
        rewrite(x + y).to(y + x),
        rewrite((x + y) + z).to(x + (y + z)),
        rewrite(x + (y + z)).to((x + y) + z),
        # multiplication distributes over sums, both sides, both directions
        rewrite(x * (y + z)).to(x * y + x * z),
        rewrite(x * y + x * z).to(x * (y + z)),
        rewrite((x + y) * z).to(x * z + y * z),
        rewrite(x * z + y * z).to((x + y) * z),
        # conj distributes over sums (elementwise)
        rewrite((x + y).conj()).to(x.conj() + y.conj()),
        rewrite(x.conj() + y.conj()).to((x + y).conj()),
        # conj of a scaled term conjugates the coefficient
        rewrite(x.scaled(c).conj()).to(x.conj().scaled(c.conj())),
        rewrite(x.conj().scaled(c.conj())).to(x.scaled(c).conj()),
        # scalars are central: c(X)Y = (XY)c = X(cY) — WITHOUT scalar products
        rewrite(x.scaled(c) * y).to((x * y).scaled(c)),
        rewrite((x * y).scaled(c)).to(x.scaled(c) * y),
        rewrite(x * y.scaled(c)).to((x * y).scaled(c)),
        # nested scales commute (encodes scalar commutativity opaquely, K23)
        rewrite(x.scaled(c).scaled(d)).to(x.scaled(d).scaled(c)),
        # scale distributes over sums (added post stage-7 review with auditor
        # soundness verification, per K24 — closes a derivability gap that
        # would otherwise surface as a fake "underivable" for Scale(c, Sum) shapes)
        rewrite((x + y).scaled(c)).to(x.scaled(c) + y.scaled(c)),
        rewrite(x.scaled(c) + y.scaled(c)).to((x + y).scaled(c)),
        # scalar conjugation is an involution (STerm sort)
        rewrite(c.conj().conj()).to(c),
    ]
    # I10 commutation, atoms only (soundness boundary, see module docstring)
    for a_name in atom_names:
        for b_name in atom_names:
            a, b = ZTerm(a_name), ZTerm(b_name)
            rules.append(rewrite(a * b.conj()).to(b.conj() * a))
            rules.append(rewrite(b.conj() * a).to(a * b.conj()))
    return ruleset(*rules)


def scalar_to_egglog(scalar) -> STerm:
    if isinstance(scalar, ScalarAtom):
        return STerm(scalar.name)
    if isinstance(scalar, ScalarConj):
        return scalar_to_egglog(scalar.arg).conj()
    raise TypeError(f"unknown scalar node: {scalar!r}")


def to_egglog(term: Term) -> ZTerm:
    """Translate an abstract Term into the egglog sort."""
    if isinstance(term, Atom):
        return ZTerm(term.name)
    if isinstance(term, Mul):
        return to_egglog(term.left) * to_egglog(term.right)
    if isinstance(term, Conj):
        return to_egglog(term.arg).conj()
    if isinstance(term, Sum):
        return to_egglog(term.left) + to_egglog(term.right)
    if isinstance(term, Scale):
        return to_egglog(term.arg).scaled(scalar_to_egglog(term.coeff))
    raise TypeError(f"unknown term node: {term!r}")
