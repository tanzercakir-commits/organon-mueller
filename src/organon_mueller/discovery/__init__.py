"""Discovery engine (stage 2+): hybrid equality saturation + SymPy verification.

Requires the optional dependency set:  pip install organon-mueller[discovery]
"""
from .terms import Atom, Conj, Mul, Term, enumerate_terms

try:  # egglog is optional (decision M13)
    from .engine import DiscoveryEngine, DiscoveryResult

    HAS_EGGLOG = True
except ImportError:  # pragma: no cover - exercised only without the extra
    HAS_EGGLOG = False

__all__ = [
    "Atom",
    "Conj",
    "Mul",
    "Term",
    "enumerate_terms",
    "HAS_EGGLOG",
]

if HAS_EGGLOG:
    __all__ += ["DiscoveryEngine", "DiscoveryResult"]
