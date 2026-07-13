"""Serialization and LaTeX output (MCP-readiness, decisions M4/M8).

SymPy expressions travel as `srepr` strings (lossless). Reconstruction uses
`sympy.sympify` on srepr output, which is safe for strings this module
itself produced.

STAGE-2 GATE (security): `sympify` evaluates arbitrary expressions — an
untrusted payload can reach `__import__` through it. Before ANY external
surface (MCP server, web UI) is wired to `hvector_from_dict`, this module
must switch to a restricted parser (whitelisted `global_dict`, no attribute
access) plus a rejection test for injection payloads. Tracked in
docs/ROADMAP.md phase E; do not expose earlier.
"""
from __future__ import annotations

import json

import sympy as sp

from .algebra.states import HVector
from .identities.known import KNOWN_IDENTITIES, Identity

__all__ = [
    "hvector_to_dict",
    "hvector_from_dict",
    "hvector_to_json",
    "hvector_from_json",
    "identity_to_dict",
    "library_to_json",
    "hvector_to_latex",
    "matrix_to_latex",
]

_FIELDS = ("tau", "alpha", "beta", "gamma")


# -- HVector round-trip -------------------------------------------------------

def hvector_to_dict(h: HVector) -> dict:
    return {name: sp.srepr(getattr(h, name)) for name in _FIELDS}


def hvector_from_dict(data: dict) -> HVector:
    missing = [name for name in _FIELDS if name not in data]
    if missing:
        raise ValueError(f"missing HVector fields: {missing}")
    return HVector(*(sp.sympify(data[name]) for name in _FIELDS))


def hvector_to_json(h: HVector) -> str:
    return json.dumps(hvector_to_dict(h), sort_keys=True)


def hvector_from_json(payload: str) -> HVector:
    return hvector_from_dict(json.loads(payload))


# -- identity library export ---------------------------------------------------

def identity_to_dict(identity: Identity) -> dict:
    """Metadata-only export (the check callable is not serializable)."""
    return {
        "key": identity.key,
        "statement": identity.statement,
        "source": identity.source,
        "conditions": list(identity.conditions),
        "mode": identity.mode,
    }


def library_to_json(indent: int | None = 2) -> str:
    """The whole known-identity library as JSON (for MCP tools / reports)."""
    return json.dumps(
        [identity_to_dict(i) for i in KNOWN_IDENTITIES],
        indent=indent,
        sort_keys=False,
    )


# -- LaTeX ---------------------------------------------------------------------

def hvector_to_latex(h: HVector) -> str:
    r"""|h> as a LaTeX column vector \begin{pmatrix}...\end{pmatrix}."""
    return sp.latex(h.to_column())


def matrix_to_latex(m: sp.Matrix) -> str:
    return sp.latex(sp.Matrix(m))
