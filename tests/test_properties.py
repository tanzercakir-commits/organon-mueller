"""Stage-4 property-based tests (hypothesis, derandomized for CI — K2/K18).

These encode the CONTRACTS between layers, not examples:
  P1  provable(t1, t2)            =>  numerically equal   (axiom soundness)
  P2  symbolically equal (exact)  =>  numerically equal   (layer coherence)
  P3  enumeration is deterministic and duplicate-free for random configs
"""
import pytest

pytest.importorskip("egglog")
from hypothesis import HealthCheck, given, settings  # noqa: E402
from hypothesis import strategies as st  # noqa: E402

from organon_mueller.discovery.engine import DiscoveryEngine  # noqa: E402
from organon_mueller.discovery.interpret import terms_numerically_equal  # noqa: E402
from organon_mueller.discovery.symbolic import terms_symbolically_equal  # noqa: E402
from organon_mueller.discovery.terms import enumerate_terms  # noqa: E402

ATOMS = ("a", "b")
POOL = enumerate_terms(ATOMS, 5)  # 66 terms: rich but cheap
_ENGINE = DiscoveryEngine(atom_names=ATOMS)

SETTINGS = settings(
    max_examples=30,
    derandomize=True,  # K2: CI must be deterministic
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)

def _sound_variants(t):
    """Terms equal to t by construction (sound structural transformations)."""
    from organon_mueller.discovery.terms import Conj as C, Mul as M

    variants = [C(C(t))]
    if isinstance(t, M):
        variants.append(C(M(C(t.left), C(t.right))))  # t == conj(conj(l)*conj(r))
        if isinstance(t.left, M):  # reassociation
            variants.append(M(t.left.left, M(t.left.right, t.right)))
    if isinstance(t, C) and isinstance(t.arg, M):  # conj distribution
        variants.append(M(C(t.arg.left), C(t.arg.right)))
    return variants


# uniform pairs rarely satisfy the antecedents (stage-4 review: measured
# ~4.6%), so mix in constructed-equal pairs to guarantee nontrivial hits
# on every derandomized run
uniform_pair = st.tuples(st.sampled_from(POOL), st.sampled_from(POOL))
equal_pair = st.sampled_from(POOL).flatmap(
    lambda t: st.sampled_from(_sound_variants(t)).map(lambda v: (t, v))
)
pair = st.one_of(uniform_pair, equal_pair)


@SETTINGS
@given(pair)
def test_p1_provable_implies_numeric(tp):
    t1, t2 = tp
    if _ENGINE.provable(t1, t2):
        assert terms_numerically_equal(t1, t2, ATOMS)


@SETTINGS
@given(pair)
def test_p2_symbolic_implies_numeric(tp):
    t1, t2 = tp
    if terms_symbolically_equal(t1, t2, ATOMS):
        assert terms_numerically_equal(t1, t2, ATOMS)


@SETTINGS
@given(
    st.integers(min_value=1, max_value=6),
    st.sampled_from([("a",), ("a", "b"), ("a", "b", "c")]),
    st.booleans(),
)
def test_p3_enumeration_deterministic_no_duplicates(max_size, atoms, pruned):
    first = enumerate_terms(atoms, max_size, conj_normal=pruned)
    second = enumerate_terms(atoms, max_size, conj_normal=pruned)
    assert first == second
    assert len(first) == len(set(first))
    assert all(t.size() <= max_size for t in first)
