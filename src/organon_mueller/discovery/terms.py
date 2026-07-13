"""Abstract term language over the Z-algebra (structure only, no scalars).

Grammar:  t ::= Atom(name) | Mul(t, t) | Conj(t)

Semantics (see interpret.py): atoms denote Z matrices of nondepolarizing
states; Mul is matrix multiplication; Conj is the ELEMENTWISE complex
conjugate (order-preserving under products: (AB)* = A* B*).
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

__all__ = [
    "Term",
    "Atom",
    "Mul",
    "Conj",
    "Scalar",
    "ScalarAtom",
    "ScalarConj",
    "Sum",
    "Scale",
    "enumerate_terms",
    "enumerate_extended",
]


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


# -- stage 7: scalars, sums, scaling -----------------------------------------

class Scalar:
    """Opaque scalar expressions (decision M10/M26): NO arithmetic nodes —
    a scalar is an atom or a conjugated atom; products/sums of scalars are
    never formed (nesting Scale replaces scalar products)."""

    def size(self) -> int:
        raise NotImplementedError

    def render(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class ScalarAtom(Scalar):
    name: str

    def size(self) -> int:
        return 1

    def render(self) -> str:
        return self.name


@dataclass(frozen=True)
class ScalarConj(Scalar):
    arg: Scalar

    def size(self) -> int:
        return 1 + self.arg.size()

    def render(self) -> str:
        return f"conj({self.arg.render()})"


@dataclass(frozen=True)
class Sum(Term):
    left: Term
    right: Term

    def size(self) -> int:
        return 1 + self.left.size() + self.right.size()

    def render(self) -> str:
        return f"({self.left.render()}+{self.right.render()})"


@dataclass(frozen=True)
class Scale(Term):
    coeff: Scalar
    arg: Term

    def size(self) -> int:
        return 1 + self.coeff.size() + self.arg.size()

    def render(self) -> str:
        return f"[{self.coeff.render()}]{self.arg.render()}"


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


def enumerate_extended(
    atom_names: tuple[str, ...],
    scalar_names: tuple[str, ...],
    max_size: int,
    max_sums: int = 1,
    max_scale_depth: int = 1,
) -> list[Term]:
    """Deterministic enumeration of the EXTENDED language (stage 7),
    with explosion controls:

    * conj-normal throughout (Conj on atoms, ScalarConj on scalar atoms);
    * Scale nesting bounded by ``max_scale_depth`` (nested Scale encodes
      scalar products without forming them, M10);
    * at most ``max_sums`` Sum nodes, and Sums only combine sum-free terms
      (superpositions of monomials — the physically central shape).
      Only ``max_sums=1`` is implemented; larger values raise instead of
      silently degrading (stage-7 review: honest knobs).
    """
    if max_sums > 1:
        raise NotImplementedError(
            "stage-7 enumeration bound: max_sums=1 (larger values are a "
            "future extension, not a silent no-op)"
        )
    scalars: list[Scalar] = []
    for name in scalar_names:
        scalars.append(ScalarAtom(name))
        scalars.append(ScalarConj(ScalarAtom(name)))

    @lru_cache(maxsize=None)
    def sumfree(n: int, depth: int) -> tuple[Term, ...]:
        """Sum-free terms of exact size n with Scale depth <= depth."""
        out: list[Term] = []
        if n == 1:
            out.extend(Atom(name) for name in atom_names)
        if n == 2:
            out.extend(Conj(Atom(name)) for name in atom_names)
        for left_size in range(1, n - 1):
            right_size = n - 1 - left_size
            if right_size < 1:
                continue
            for left in sumfree(left_size, depth):
                for right in sumfree(right_size, depth):
                    out.append(Mul(left, right))
        if depth >= 1:
            for s in scalars:
                inner = n - 1 - s.size()
                if inner >= 1:
                    out.extend(
                        Scale(s, t) for t in sumfree(inner, depth - 1)
                    )
        return tuple(out)

    result: list[Term] = []
    for n in range(1, max_size + 1):
        result.extend(sumfree(n, max_scale_depth))
    if max_sums >= 1:
        for n in range(3, max_size + 1):
            for left_size in range(1, n - 1):
                right_size = n - 1 - left_size
                if right_size < 1:
                    continue
                for left in sumfree(left_size, max_scale_depth):
                    for right in sumfree(right_size, max_scale_depth):
                        result.append(Sum(left, right))
    return result
