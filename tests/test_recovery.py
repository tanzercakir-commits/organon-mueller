"""Stage-5: the recovery campaign — the engine rediscovers the translatable
subset of the hand-coded library, and the untranslatable rest is explained
by named missing features (K19/K20/M22)."""
import pytest

pytest.importorskip("egglog")

from organon_mueller.discovery.engine import DiscoveryEngine  # noqa: E402
from organon_mueller.discovery.recovery import (  # noqa: E402
    MISSING_FEATURES,
    RECOVERY_TABLE,
    run_recovery_campaign,
)
from organon_mueller.discovery.terms import Atom, Conj, Mul  # noqa: E402
from organon_mueller.identities.known import KNOWN_IDENTITIES  # noqa: E402


def test_table_covers_library_exactly():
    table_keys = [e.identity_key for e in RECOVERY_TABLE]
    assert table_keys == [i.key for i in KNOWN_IDENTITIES]


def test_table_integrity_k19():
    for entry in RECOVERY_TABLE:
        assert entry.status in {"translatable", "structural", "untranslatable"}
        if entry.status == "translatable":
            assert entry.pairs and not entry.missing
        elif entry.status == "untranslatable":
            # K19: verdict requires named missing features from the vocabulary
            assert entry.missing, f"{entry.identity_key} missing features unnamed"
            assert all(k in MISSING_FEATURES for k in entry.missing)
        else:
            assert not entry.pairs and not entry.missing
        assert entry.note


def test_campaign_recovers_all_translatable():
    result = run_recovery_campaign()
    assert result.complete, f"campaign failures: {result.failures}"
    assert result.recovered == ["I1", "I10", "I15"]  # I15 joined at stage 7
    assert result.structural == ["I7", "I8"]
    assert len(result.untranslatable) == 16


def test_m22_monotonicity_floor():
    """M22: the recovered set may only grow. Floor raised at stage 7
    (Sum/Scale delivered I15); raise again on future extensions, never lower."""
    result = run_recovery_campaign()
    assert set(result.recovered) >= {"I1", "I10", "I15"}


def test_mueller_reality_pair_in_full_harvest():
    """Harvest evidence for I1's reality half: t and conj(t) share a class
    in the FULL (unpruned) size-7 run — spec note: not conj-normal."""
    result = DiscoveryEngine(atom_names=("a", "b"), max_size=7).run()
    a = Atom("a")
    t = Mul(a, Conj(a))
    target = frozenset((t, Conj(t)))
    harvested = {frozenset((p.left, p.right)) for p in result.verified}
    assert target in harvested
