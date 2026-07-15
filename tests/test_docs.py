"""Stage-19: documentation must not drift from the repo (A15 lesson:
every claim/command/number/link is checked against reality)."""
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _read(rel):
    return (ROOT / rel).read_text()


# -- links resolve ----------------------------------------------------------------

@pytest.mark.parametrize("doc", [
    "README.md", "docs/architecture.md", "docs/user-guide.md",
])
def test_relative_links_resolve(doc):
    src = _read(doc)
    base = (ROOT / doc).parent
    for target in re.findall(r"\]\((?!https?://)([^)#]+)", src):
        target = target.strip()
        if target.startswith("/"):
            continue
        assert (base / target).exists(), f"{doc}: broken link -> {target}"


# -- python snippets in README are importable / valid -----------------------------

def test_readme_python_imports_resolve():
    """Every `from organon_mueller...` / `import organon_mueller...` line in
    the README must actually import."""
    import importlib

    src = _read("README.md")
    mods = set()
    for m in re.findall(r"^\s*from (organon_mueller[\w.]*) import", src, re.M):
        mods.add(m)
    for m in re.findall(r"^\s*import (organon_mueller[\w.]*)", src, re.M):
        mods.add(m)
    assert "organon_mueller.decomposition" in mods   # sanity: we found some
    for mod in mods:
        importlib.import_module(mod)


def test_readme_symbols_exist():
    """Named API in the README quickstart actually exists."""
    from organon_mueller import HVector

    h = HVector.generic("a")
    for attr in ("to_mueller", "to_z", "to_quaternion"):
        assert hasattr(h, attr), attr
    from organon_mueller.decomposition import decompose  # noqa: F401
    from organon_mueller.decomposition.rank3 import (  # noqa: F401
        propose_decompositions,
    )
    from organon_mueller.reporting import (  # noqa: F401
        Report, decomposition_section,
    )


# -- numeric claims match reality -------------------------------------------------

def test_stated_test_count_matches_collection():
    """README/ROADMAP advertise a test count — assert the real collected count
    equals the number the docs advertise (catches doc drift)."""
    import subprocess
    import sys

    out = subprocess.run(
        [sys.executable, "-m", "pytest", "--co", "-q"],
        cwd=ROOT, capture_output=True, text=True, timeout=300)
    # sum the per-file "path: N" tallies pytest prints in -q collect mode
    counts = [int(n) for n in re.findall(r":\s*(\d+)\s*$", out.stdout, re.M)]
    total = sum(counts)
    assert total > 0, out.stdout[-500:]

    for doc in ("README.md", "docs/ROADMAP.md"):
        for claimed in re.findall(r"(\d+)\s+test", _read(doc)):
            assert int(claimed) == total, (
                f"{doc} claims {claimed} tests but collection has {total}")


def test_known_identity_count_claim():
    """README says '21 entries' / '21 identities' — must match the library."""
    from organon_mueller.identities.known import KNOWN_IDENTITIES

    n = len(KNOWN_IDENTITIES)
    for claimed in re.findall(r"(\d+)\s+(?:identit|entr)", _read("README.md")):
        assert int(claimed) == n, f"README claims {claimed}, library has {n}"


def test_mcp_run_command_is_real():
    """The `python -m organon_mueller.mcp_server` entry point exists."""
    assert (ROOT / "src" / "organon_mueller" / "mcp_server"
            / "__main__.py").exists()
    # the literal run command lives where users act on it (the guide + the
    # mcp readme); the top-level README delegates via a link
    for doc in ("docs/user-guide.md", "docs/README-mcp.md"):
        assert "python -m organon_mueller.mcp_server" in _read(doc)


def test_no_stale_stage2_status_in_readme():
    """A15 verb-discipline for the outward face: the README must not still
    advertise the old 'Stage 2' status now that A0-A19 are done."""
    src = _read("README.md")
    assert "Stage 2" not in src and "**Stage 2**" not in src
    assert "experimental research software" in src.lower()
    assert "no licence" in src.lower() or "no license" in src.lower()


def test_pyproject_extras_match_readme():
    """README install commands reference extras that pyproject defines."""
    pyproject = _read("pyproject.toml")
    for extra in ("test", "discovery", "mcp"):
        assert re.search(rf"^{extra}\s*=", pyproject, re.M), extra
        assert f'[{extra}' in _read("README.md") or f",{extra}" in _read(
            "README.md") or f'"{extra}' in _read("README.md")
