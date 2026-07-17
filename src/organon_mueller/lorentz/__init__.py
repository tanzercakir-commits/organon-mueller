"""Lorentz face of the Z-matrix algebra (FROZEN-7 milestone series).

The Σ^μ basis of the collaborator's work order coincides exactly with
this engine's Z-matrix basis — Λ = ZZ* on this face is M = ZZ* on the
polarization face. See ``core`` for the theorems and convention notes.
"""
from .core import (
    METRIC,
    SIGMA,
    SIGMA_BAR,
    boost_alpha,
    lorentz_matrix,
    minkowski_square,
    rotation_alpha,
    z_bar_matrix,
    z_inverse,
    z_matrix,
)
from .identities import (
    LORENTZ_TASK1,
    LORENTZ_TASK2,
    LorentzIdentity,
    bonus_lambda_zbar_theorem,
    spec_form_holds,
    spec_form_holds_bar,
    verify_task1,
    verify_task2,
)
from .discovery import (
    full_sweep,
    sweep_report,
)
from .terms import (
    KNOWN_TEN,
    certify,
    classify_all,
    letter_matrices,
    recovery_gate,
)

__all__ = [
    "METRIC", "SIGMA", "SIGMA_BAR",
    "boost_alpha", "lorentz_matrix", "minkowski_square", "rotation_alpha",
    "z_bar_matrix", "z_inverse", "z_matrix",
    "LORENTZ_TASK1", "LORENTZ_TASK2", "LorentzIdentity",
    "bonus_lambda_zbar_theorem", "spec_form_holds", "spec_form_holds_bar",
    "verify_task1", "verify_task2",
    "KNOWN_TEN", "certify", "classify_all", "letter_matrices",
    "recovery_gate",
    "full_sweep", "sweep_report",
]
