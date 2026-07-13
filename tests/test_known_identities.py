"""Stage-00 acceptance: recover every known identity in the library."""
import pytest

from organon_mueller.identities.known import KNOWN_IDENTITIES


@pytest.mark.parametrize(
    "identity", KNOWN_IDENTITIES, ids=[i.key for i in KNOWN_IDENTITIES]
)
def test_known_identity(identity):
    assert identity.check(), f"{identity.key} failed: {identity.statement}"


def test_library_metadata_complete():
    from organon_mueller.conditions import CONDITIONS

    for identity in KNOWN_IDENTITIES:
        assert identity.statement
        assert identity.source
        assert identity.mode in {"symbolic", "numeric", "symbolic+numeric"}
        for key in identity.conditions:
            assert key in CONDITIONS, f"unregistered condition key: {key}"
