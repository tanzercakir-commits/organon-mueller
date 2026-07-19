"""wordalgebra — a general matrix word-algebra identity solver.

A collaborator's brief ("do these A Sigma B products equal Sigma?")
becomes a :class:`BriefSpec` fed to :func:`solve`, rather than bespoke
hand-written code. Framing-neutral: the basis, generator, operations and
constraint are all inputs — no Sigma-bar/Lambda/Mueller is assumed.

See ``specs/wordalgebra-01.md`` for the design and the backward-
validation targets (it must re-solve TANZER_1 and TANZER_2 from a spec
alone).
"""
from .alphabet import alphabet_labels, build_alphabet
from .expand import (
    coefficient_matrix,
    expand_in_basis,
    residual_is_zero,
    trace_orthogonal_norms,
)
from .solve import Cell, SolveResult, solve
from .spec import ALLOWED_OPS, BriefSpec, SpecError

__all__ = [
    "BriefSpec", "SpecError", "ALLOWED_OPS",
    "build_alphabet", "alphabet_labels",
    "trace_orthogonal_norms", "expand_in_basis", "residual_is_zero",
    "coefficient_matrix",
    "solve", "SolveResult", "Cell",
]
