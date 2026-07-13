"""Guarded atoms (stage 9, first half — design: docs/design-note-guarded-atoms.md).

Guards constrain the GENERATORS (interpretation layers), never the axioms
(zero soundness cost, K24 untouched). A `GuardedAtom` subclasses `Atom`,
so the e-graph and the term machinery see a plain atom: `provable(...)`
therefore means "derivable WITHOUT the guard" — exactly the split we want,
because guard-true + unprovable + unguarded-false is the signature of a
genuine Horn-conditional identity (M32).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import sympy as sp

from ..algebra.states import HVector
from ..verify import symbolic_equal, numeric_equal, to_numpy
from .interpret import evaluate
from .symbolic import evaluate_symbolic
from .terms import Atom, Term

__all__ = [
    "GUARD_KEYS",
    "GuardedAtom",
    "guarded_random_hvector",
    "guarded_symbolic_hvector",
    "build_numeric_assignment",
    "build_symbolic_assignment",
    "guarded_numerically_equal",
    "guarded_symbolically_equal",
    "GuardedFinding",
    "run_guarded_campaign",
]

GUARD_KEYS = (
    "hermitian_state",
    "unitary_state",
    "class2_ta",
    "class2_tb",
    "class2_tg",
)


@dataclass(frozen=True)
class GuardedAtom(Atom):
    """An atom whose interpretations are drawn from a constrained class.

    Subclasses Atom deliberately: to_egglog and the axioms treat it as an
    ordinary atom (guards are invisible to proofs)."""

    guard: str = ""

    def render(self) -> str:
        return f"{self.name}{{{self.guard}}}"


# -- constrained generators ---------------------------------------------------

def guarded_random_hvector(rng: np.random.Generator, guard: str) -> HVector:
    def c() -> complex:
        return complex(rng.standard_normal(), rng.standard_normal())

    def r() -> float:
        return float(rng.standard_normal())

    if guard == "hermitian_state":
        params = (r(), r(), r(), r())
    elif guard == "unitary_state":
        params = (r(), 1j * r(), 1j * r(), 1j * r())
    elif guard == "class2_ta":
        params = (c(), c(), 0, 0)
    elif guard == "class2_tb":
        params = (c(), 0, c(), 0)
    elif guard == "class2_tg":
        params = (c(), 0, 0, c())
    else:
        raise ValueError(f"unknown guard: {guard}")
    return HVector(*(sp.sympify(p) for p in params))


def guarded_symbolic_hvector(name: str, guard: str) -> HVector:
    """Generic symbolic representative of the guarded class (K30: constraints
    enter by construction of the parameters, not by assumption injection).

    Faithfulness obligation (stage-8 design note): the parametrization must
    be GENERIC for its class — tested in tests/test_guarded_atoms.py."""
    if guard == "hermitian_state":
        t, a, b, g = sp.symbols(
            f"tau_{name} alpha_{name} beta_{name} gamma_{name}", real=True
        )
        return HVector(t, a, b, g)
    if guard == "unitary_state":
        t, a, b, g = sp.symbols(
            f"tau_{name} ualpha_{name} ubeta_{name} ugamma_{name}", real=True
        )
        return HVector(t, sp.I * a, sp.I * b, sp.I * g)
    if guard == "class2_ta":
        t, a = sp.symbols(f"tau_{name} alpha_{name}", complex=True)
        return HVector(t, a, 0, 0)
    if guard == "class2_tb":
        t, b = sp.symbols(f"tau_{name} beta_{name}", complex=True)
        return HVector(t, 0, b, 0)
    if guard == "class2_tg":
        t, g = sp.symbols(f"tau_{name} gamma_{name}", complex=True)
        return HVector(t, 0, 0, g)
    raise ValueError(f"unknown guard: {guard}")


# -- assignments honoring guards ------------------------------------------------

def build_numeric_assignment(
    guards: dict[str, str | None],
    rng: np.random.Generator,
) -> dict:
    """{atom name -> guard key or None (generic)} -> numeric assignment."""
    from ..verify import random_hvector

    assignment = {}
    for name, guard in guards.items():
        hv = random_hvector(rng) if guard is None else guarded_random_hvector(rng, guard)
        assignment[name] = to_numpy(hv.to_z())
    return assignment


def build_symbolic_assignment(guards: dict[str, str | None]) -> dict:
    assignment = {}
    for name, guard in guards.items():
        hv = (
            HVector.generic(name)
            if guard is None
            else guarded_symbolic_hvector(name, guard)
        )
        assignment[name] = hv.to_z()
    return assignment


def _collect_term_guards(term: Term, out: dict[str, str]) -> None:
    if isinstance(term, GuardedAtom):
        if out.get(term.name, term.guard) != term.guard:
            raise ValueError(
                f"conflicting guards for atom {term.name!r}: "
                f"{out[term.name]} vs {term.guard}"
            )
        out[term.name] = term.guard
    for child in ("left", "right", "arg"):
        if hasattr(term, child):
            _collect_term_guards(getattr(term, child), out)


def _validated_guards(
    a: Term, b: Term, guards: dict[str, str | None]
) -> dict[str, str | None]:
    """Cross-validate the guards dict against the terms' embedded labels
    (stage-9 review: a mislabeled dict must never yield silent Horn
    evidence). Embedded labels missing from the dict are added."""
    embedded: dict[str, str] = {}
    _collect_term_guards(a, embedded)
    _collect_term_guards(b, embedded)
    merged = dict(guards)
    for name, guard in embedded.items():
        if name in merged and merged[name] not in (None, guard):
            raise ValueError(
                f"guards dict says {name}={merged[name]!r} but the term "
                f"carries GuardedAtom({name!r}, {guard!r})"
            )
        merged[name] = guard
    return merged


def guarded_numerically_equal(
    a: Term, b: Term, guards: dict[str, str | None],
    draws: int = 3, seed: int = 20260713,
) -> bool:
    guards = _validated_guards(a, b, guards)
    rng = np.random.default_rng(seed)
    for _ in range(draws):
        assignment = build_numeric_assignment(guards, rng)
        if not numeric_equal(evaluate(a, assignment), evaluate(b, assignment)):
            return False
    return True


def guarded_symbolically_equal(
    a: Term, b: Term, guards: dict[str, str | None]
) -> bool:
    """EXACT proof under the guard (constrained generic parameters)."""
    guards = _validated_guards(a, b, guards)
    assignment = build_symbolic_assignment(guards)
    return symbolic_equal(
        evaluate_symbolic(a, assignment), evaluate_symbolic(b, assignment)
    )


# -- the first guarded campaign ---------------------------------------------------

@dataclass
class GuardedFinding:
    """A Horn-conditional identity candidate with its full evidence (M32)."""

    guards: dict[str, str | None]
    left: Term
    right: Term
    symbolic_guarded: bool
    numeric_guarded: bool
    provable_unguarded: bool
    symbolic_unguarded: bool

    @property
    def is_conditional_identity(self) -> bool:
        """True iff genuinely conditional: exact under the guard, false
        without it, and not derivable by the (guard-blind) axioms."""
        return (
            self.symbolic_guarded
            and self.numeric_guarded
            and not self.provable_unguarded
            and not self.symbolic_unguarded
        )


def run_guarded_campaign() -> list[GuardedFinding]:
    """Stage-9 targets (probe-verified): commutation inside each of the
    class2_ta/tb/tg quaternion planes ({1,i}, {1,j}, {1,k} — every 2D
    subalgebra spanned by 1 and a single unit is commutative); mixed
    guards as the negative control.
    These are KNOWN facts — the point is proving the channel mechanism,
    not novelty (novelty protocol applies unchanged to future outputs)."""
    from .engine import DiscoveryEngine
    from .symbolic import terms_symbolically_equal
    from .terms import Mul

    engine = DiscoveryEngine(atom_names=("a", "b"))
    findings = []
    for guard in ("class2_ta", "class2_tb", "class2_tg"):
        a = GuardedAtom("a", guard=guard)
        b = GuardedAtom("b", guard=guard)
        left, right = Mul(a, b), Mul(b, a)
        findings.append(
            GuardedFinding(
                guards={"a": guard, "b": guard},
                left=left,
                right=right,
                symbolic_guarded=guarded_symbolically_equal(
                    left, right, {"a": guard, "b": guard}
                ),
                numeric_guarded=guarded_numerically_equal(
                    left, right, {"a": guard, "b": guard}
                ),
                provable_unguarded=engine.provable(left, right),
                symbolic_unguarded=terms_symbolically_equal(
                    Mul(Atom("a"), Atom("b")), Mul(Atom("b"), Atom("a")), ("a", "b")
                ),
            )
        )
    return findings
