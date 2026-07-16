"""organon-mueller: automated identity discovery for the Stokes-Mueller
formalism of polarization optics. Successor to Organon v1."""

from .algebra.quaternion import BiQuaternion
from .algebra.states import (
    HVector,
    covariance_from_mueller,
    hvector_from_covariance,
    hvector_from_jones,
    hvector_from_quaternion,
    mueller_from_covariance,
    mueller_from_jones,
    mueller_rotation,
    rotator_quaternion,
    stokes_from_quaternion,
    stokes_matrix,
    stokes_quaternion,
    z_from_jones,
    zstar_from_jones,
)
from .identities.known import KNOWN_IDENTITIES, Identity, verify_all

__version__ = "1.1.1"

__all__ = [
    "BiQuaternion",
    "HVector",
    "Identity",
    "KNOWN_IDENTITIES",
    "verify_all",
    "covariance_from_mueller",
    "hvector_from_covariance",
    "hvector_from_jones",
    "hvector_from_quaternion",
    "mueller_from_covariance",
    "mueller_from_jones",
    "mueller_rotation",
    "rotator_quaternion",
    "stokes_from_quaternion",
    "stokes_matrix",
    "stokes_quaternion",
    "z_from_jones",
    "zstar_from_jones",
]
