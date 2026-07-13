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

from .terms import Atom, Conj, Mul, Term

__all__ = ["ZTerm", "structural_rules", "to_egglog"]


class ZTerm(Expr):
    """egglog expression sort for abstract Z-algebra terms."""

    def __init__(self, name: StringLike) -> None: ...

    def __mul__(self, other: "ZTerm") -> "ZTerm": ...

    def conj(self) -> "ZTerm": ...


def structural_rules(atom_names: tuple[str, ...]):
    """Ruleset: associativity, conj involution/distribution, atom commutation."""
    x, y, z = vars_("x y z", ZTerm)
    rules = [
        # associativity, both directions
        rewrite((x * y) * z).to(x * (y * z)),
        rewrite(x * (y * z)).to((x * y) * z),
        # conj is an involution
        rewrite(x.conj().conj()).to(x),
        # conj distributes over products, ORDER-PRESERVING (elementwise)
        rewrite((x * y).conj()).to(x.conj() * y.conj()),
        rewrite(x.conj() * y.conj()).to((x * y).conj()),
    ]
    # I10 commutation, atoms only (soundness boundary, see module docstring)
    for a_name in atom_names:
        for b_name in atom_names:
            a, b = ZTerm(a_name), ZTerm(b_name)
            rules.append(rewrite(a * b.conj()).to(b.conj() * a))
            rules.append(rewrite(b.conj() * a).to(a * b.conj()))
    return ruleset(*rules)


def to_egglog(term: Term) -> ZTerm:
    """Translate an abstract Term into the egglog sort."""
    if isinstance(term, Atom):
        return ZTerm(term.name)
    if isinstance(term, Mul):
        return to_egglog(term.left) * to_egglog(term.right)
    if isinstance(term, Conj):
        return to_egglog(term.arg).conj()
    raise TypeError(f"unknown term node: {term!r}")
