"""Coupled-dipole symbolic engine (Phase D; PRB 98, 045410)."""
from .dimer import (
    coupling_lambda,
    dephased_interaction_jones,
    interaction_jones,
    jones_projector,
    jones_to_hvector,
    scattering_matrix_decomposed,
    scattering_matrix_direct,
    scattering_matrix_numeric,
)
from .hybrid import (
    coupled_system_matrix,
    decomposition_coefficients,
    hybrid_basis,
    hybrid_frequencies,
    lorentzian,
)

__all__ = [
    "jones_projector",
    "interaction_jones",
    "dephased_interaction_jones",
    "coupling_lambda",
    "scattering_matrix_direct",
    "scattering_matrix_decomposed",
    "scattering_matrix_numeric",
    "jones_to_hvector",
    "coupled_system_matrix",
    "lorentzian",
    "hybrid_frequencies",
    "hybrid_basis",
    "decomposition_coefficients",
]
