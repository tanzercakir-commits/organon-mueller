"""Concrete brief instances — the collaborator's problems encoded as
:class:`BriefSpec` DATA, fed to the general solver. This is the payoff:
a brief is a spec, not new code.

The Sigma basis is taken from ``lorentz.core.SIGMA`` (its equality to the
collaborator's Sigma is already an engine theorem); nothing else of the
old framing is carried in.
"""
from __future__ import annotations

import sympy as sp

from ..lorentz.core import SIGMA
from .spec import BriefSpec


def _generator(a):
    return sum((a[m] * SIGMA[m] for m in range(4)), sp.zeros(4))


def _inverse(a):
    # the collaborator's Z^{-1}: the sign-flipped spatial combination
    # (his definition; the true inverse on the constraint alpha.alpha = 1)
    return a[0] * SIGMA[0] - a[1] * SIGMA[1] - a[2] * SIGMA[2] - a[3] * SIGMA[3]


def tanzer2_spec() -> BriefSpec:
    """TANZER_2: the narrowed brief — which A Sigma^mu B equal Sigma^mu,
    over S = {Z, Z^-1, Zdag, Z*, Z^T, (Z^-1)dag, (Z^-1)*, (Z^-1)^T}, on
    det(Z)=1 i.e. alpha.alpha = 1."""
    return BriefSpec(
        name="TANZER_2",
        basis=tuple(SIGMA),
        generator=_generator,
        inverse=_inverse,
        n_params=4,
        operations=("id", "conj", "T", "dagger", "inv"),
        constraint=lambda p: p[0]**2 - p[1]**2 - p[2]**2 - p[3]**2 - 1,
    )
