"""Abstract term language over the Z-algebra (structure only, no scalars).

Grammar:  t ::= Atom(name) | Mul(t, t) | Conj(t)

Semantics (see interpret.py): atoms denote Z matrices of nondepolarizing
states; Mul is matrix multiplication; Conj is the ELEMENTWISE complex
conjugate (order-preserving under products: (AB)* = A* B*).
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

__all__ = ["Term", "Atom", "Mul", "Conj", "enumerate_terms"]


class Term:
    """Base class; subclasses are frozen dataclasses usable as dict keys."""

    def size(self) -> int:
        raise NotImplementedError

    def render(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class Atom(Term):
    name: str

    def size(self) -> int:
        return 1

    def render(self) -> str:
        return self.name


@dataclass(frozen=True)
class Mul(Term):
    left: Term
    right: Term

    def size(self) -> int:
        return 1 + self.left.size() + self.right.size()

    def render(self) -> str:
        return f"({self.left.render()}*{self.right.render()})"


@dataclass(frozen=True)
class Conj(Term):
    arg: Term

    def size(self) -> int:
        return 1 + self.arg.size()

    def render(self) -> str:
        return f"conj({self.arg.render()})"


def enumerate_terms(
    atom_names: tuple[str, ...], max_size: int, conj_normal: bool = False
) -> list[Term]:
    """All terms up to `max_size`, deterministically ordered (rule K12).

    Sizes: atom = 1; Conj adds 1; Mul adds 1 plus both operand sizes.

    With ``conj_normal=True`` (stage 3), Conj is only applied at the atom
    level: forms like conj(conj(x)) and conj(x*y) are pruned from generation.
    Under the structural axioms every term has such a normal form, so
    identity content is preserved UP TO A MAX_SIZE SHIFT: conj-normalizing
    can grow a term (conj of a k-atom product gains k-1 size), so a pruned
    enumeration at a given max_size covers slightly fewer identities than
    the unpruned one at the same bound (stage-3 review note).
    """

    @lru_cache(maxsize=None)
    def of_size(n: int) -> tuple[Term, ...]:
        out: list[Term] = []
        if n == 1:
            out.extend(Atom(name) for name in atom_names)
        if n >= 2:
            if conj_normal:
                if n == 2:
                    out.extend(Conj(Atom(name)) for name in atom_names)
            else:
                out.extend(Conj(t) for t in of_size(n - 1))
        for left_size in range(1, n - 1):
            right_size = n - 1 - left_size
            if right_size < 1:
                continue
            for left in of_size(left_size):
                for right in of_size(right_size):
                    out.append(Mul(left, right))
        return tuple(out)

    result: list[Term] = []
    for n in range(1, max_size + 1):
        result.extend(of_size(n))
    return result
