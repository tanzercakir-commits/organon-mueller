"""Build the labelled alphabet of a brief from its generator and inverse.

From the two roots Z and Z^{-1} and the unary operations
{id, conj (*), T, dagger}, produce the letters
  Z, Z*, Z^T, Zdag, Z^-1, (Z^-1)*, (Z^-1)^T, (Z^-1)dag
(the collaborator's set S, when all ops and the inverse are enabled).

Works on sympy Matrices OR numpy arrays — .conjugate()/.T (sympy) and
.conj()/.T (numpy) are both supported, so the same builder serves the
symbolic proof path and the numeric screen.
"""
from __future__ import annotations

#: unary ops as (matrix -> matrix); tries sympy's API then numpy's
_UNARY = {
    "id": lambda M: M,
    "conj": lambda M: M.conjugate() if hasattr(M, "conjugate") else M.conj(),
    "T": lambda M: M.T,
    "dagger": lambda M: (M.conjugate() if hasattr(M, "conjugate")
                         else M.conj()).T,
}
_SUFFIX = {"id": "", "conj": "*", "T": "^T", "dagger": "dag"}
_UNARY_ORDER = ("id", "conj", "T", "dagger")


def _label(root_name: str, op: str) -> str:
    suf = _SUFFIX[op]
    if not suf:
        return root_name
    if root_name == "Z":
        return f"Z{suf}"
    return f"({root_name}){suf}"          # (Z^-1)*, (Z^-1)^T, (Z^-1)dag


def build_alphabet(Z, Zinv, operations) -> dict:
    """Return an ordered dict {label: matrix}. Roots: always Z; plus
    Z^-1 iff 'inv' in operations. Unary ops applied to each root in the
    fixed order id, conj, T, dagger (whichever are enabled)."""
    unary = [o for o in _UNARY_ORDER if o in operations]
    roots = [("Z", Z)]
    if "inv" in operations:
        roots.append(("Z^-1", Zinv))
    out = {}
    for rname, rmat in roots:
        for op in unary:
            out[_label(rname, op)] = _UNARY[op](rmat)
    return out


def alphabet_labels(operations) -> list:
    """The labels build_alphabet will produce, in order (no matrices) —
    handy for tests and report headers."""
    unary = [o for o in _UNARY_ORDER if o in operations]
    roots = ["Z"] + (["Z^-1"] if "inv" in operations else [])
    return [_label(r, o) for r in roots for o in unary]
