"""BriefSpec — the specification of a matrix word-algebra identity
problem, fed to the general solver instead of hand-written code.

A brief is: a fixed BASIS B^0..B^{d-1} (the "middle" family, e.g. the
Sigma matrices); a parametrized GENERATOR Z(alpha) and its inverse
Z^{-1}(alpha) (both supplied as callables — the collaborator's briefs
DEFINE the inverse explicitly, so the spec carries it rather than
guessing); a set of unary OPERATIONS building the alphabet; an optional
polynomial CONSTRAINT on the parameters; and the middles to sandwich.

Everything here is framing-neutral: no Sigma-bar, no Lambda, no Mueller.
Those are values a caller may pass in, never assumptions of the engine.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional, Sequence

import sympy as sp

#: the unary operations the alphabet builder understands, plus the
#: inverse-root inclusion flag "inv"
ALLOWED_OPS = ("id", "conj", "T", "dagger", "inv")


class SpecError(ValueError):
    """A malformed brief — always raised with a readable reason (K26)."""


@dataclass(frozen=True)
class BriefSpec:
    name: str
    basis: tuple                      # sympy Matrices B^0..B^{d-1}
    generator: Callable               # generator(params) -> sympy Matrix Z
    inverse: Callable                 # inverse(params) -> sympy Matrix Z^{-1}
    n_params: int
    operations: tuple = ALLOWED_OPS   # subset of ALLOWED_OPS
    constraint: Optional[Callable] = None   # constraint(params) -> expr, =0 on the surface
    middles: Optional[tuple] = None         # default: the basis itself

    # -- derived helpers ---------------------------------------------------

    def dim(self) -> int:
        return self.basis[0].shape[0]

    def mids(self) -> tuple:
        return self.basis if self.middles is None else self.middles

    def symbols(self, prefix: str = "p") -> tuple:
        """n complex parameter symbols (fresh; caller substitutes)."""
        return sp.symbols(f"{prefix}0:{self.n_params}", complex=True)

    def validate(self) -> "BriefSpec":
        """Structural checks with readable reasons (K26). Returns self so
        specs can be validated inline."""
        if not self.name or not isinstance(self.name, str):
            raise SpecError("spec needs a non-empty name")
        if not self.basis:
            raise SpecError("basis must be a non-empty tuple of matrices")
        shapes = {tuple(B.shape) for B in self.basis}
        if len(shapes) != 1:
            raise SpecError(f"basis matrices must share one shape, got {shapes}")
        r, c = self.basis[0].shape
        if r != c:
            raise SpecError(f"basis matrices must be square, got {r}x{c}")
        if self.n_params < 1:
            raise SpecError("n_params must be >= 1")
        bad = [o for o in self.operations if o not in ALLOWED_OPS]
        if bad:
            raise SpecError(f"unknown operations {bad}; allowed: {ALLOWED_OPS}")
        if not any(o in ("id", "conj", "T", "dagger") for o in self.operations):
            raise SpecError("operations must include at least one unary op "
                            "(id/conj/T/dagger)")
        if self.middles is not None:
            ms = {tuple(M.shape) for M in self.middles}
            if ms != {(r, c)}:
                raise SpecError("middles must match the basis shape")
        # generator / inverse must be callable and produce the right shape
        try:
            p = self.symbols("_v")
            Z = self.generator(p)
            Zi = self.inverse(p)
        except Exception as exc:                       # pragma: no cover
            raise SpecError(f"generator/inverse not callable on params: {exc}")
        if tuple(Z.shape) != (r, c) or tuple(Zi.shape) != (r, c):
            raise SpecError("generator and inverse must return basis-shaped "
                            "matrices")
        return self
