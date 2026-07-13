"""Symmetry-conditioned decomposition of depolarizing Mueller matrices
(Phase C; automation of Kuntman & Arteaga, Appl. Opt. 55, 2543 (2016))."""

from .covariance import (
    SYMMETRY_TEMPLATES,
    TYPE1,
    TYPE2,
    TYPE3,
    mueller_from_standard_covariance,
    standard_covariance_from_mueller,
)
from .derive import DerivedEquations, derive_equations
from .solve import DecompositionError, DecompositionResult, decompose

__all__ = [
    "SYMMETRY_TEMPLATES",
    "TYPE1",
    "TYPE2",
    "TYPE3",
    "mueller_from_standard_covariance",
    "standard_covariance_from_mueller",
    "DerivedEquations",
    "derive_equations",
    "DecompositionError",
    "DecompositionResult",
    "decompose",
]
