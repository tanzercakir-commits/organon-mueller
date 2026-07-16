"""Stage-19: documentation must not drift from the repo (A15 lesson:
every claim/command/number/link is checked against reality)."""
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


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

def _full_optional_stack() -> bool:
    """The advertised count only fully materializes when every optional
    dependency is importable: egglog (6 discovery test modules gate on it
    at module level and DON'T collect without it, e.g. on Python 3.10),
    gradio (test_ui.py gates on it at module level — the ui extra), and
    mcp and playwright (function-level gates). On a partial environment
    (typical CI 3.10, or CI without mcp/playwright) collection is a
    subset, so the exact-equality check is only enforced on a full env."""
    import importlib.util

    return all(importlib.util.find_spec(m) is not None
               for m in ("egglog", "mcp", "playwright", "gradio"))


def test_stated_test_count_matches_collection():
    """README/ROADMAP advertise a test count. On a FULL environment assert
    it equals the real collected count (drift guard); on any environment
    assert collection never EXCEEDS the advertised number (so adding tests
    without bumping the docs is always caught)."""
    import subprocess
    import sys

    out = subprocess.run(
        [sys.executable, "-m", "pytest", "--co", "-q"],
        cwd=ROOT, capture_output=True, text=True, timeout=300,
        encoding="utf-8", errors="replace")   # Windows code-page hazard
    # sum the per-file "path: N" tallies pytest prints in -q collect mode
    counts = [int(n) for n in re.findall(r":\s*(\d+)\s*$", out.stdout, re.M)]
    total = sum(counts)
    assert total > 0, out.stdout[-500:]

    claims = []
    for doc in ("README.md", "docs/ROADMAP.md"):
        claims += [int(c) for c in re.findall(r"(\d+)\s+test", _read(doc))]
    assert claims, "no test-count claim found in the docs"
    for claimed in claims:
        # partial environments collect a subset — never more than claimed
        assert total <= claimed, (
            f"collection has {total} tests but docs claim only {claimed} "
            "(add-a-test-without-bumping-docs drift)")
        if _full_optional_stack():
            assert total == claimed, (
                f"full env: docs claim {claimed} but collection has {total}")


def test_known_identity_count_claim():
    """README must STATE the known-identity library size, and it must match
    the library. Non-vacuous: the regex finding nothing is itself a failure —
    otherwise dropping the claim from the README would silently pass (the
    A15 verb/number-discipline applied to a count)."""
    from organon_mueller.identities.known import KNOWN_IDENTITIES

    n = len(KNOWN_IDENTITIES)
    claims = [int(c) for c in
              re.findall(r"(\d+)\s+(?:identit|entr)", _read("README.md"))]
    assert claims, ("README states no known-identity count "
                    "(expected a '21 identities'-style claim to guard)")
    for claimed in claims:
        assert claimed == n, f"README claims {claimed}, library has {n}"


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


def test_license_consistency():
    """MIT chosen by the user (2026-07-16). The LICENSE file, README, and
    pyproject must agree — and the old 'no license' framing must be gone
    (it would now be a false claim)."""
    lic = _read("LICENSE")
    assert lic.startswith("MIT License")
    readme = _read("README.md")
    assert "MIT" in readme and "](LICENSE)" in readme
    assert "no license yet" not in readme.lower()
    assert "no licence" not in readme.lower()
    assert 'license = {text = "MIT"}' in _read("pyproject.toml")


def test_pyproject_extras_match_readme():
    """README install commands reference extras that pyproject defines."""
    pyproject = _read("pyproject.toml")
    for extra in ("test", "discovery", "mcp", "ui"):
        assert re.search(rf"^{extra}\s*=", pyproject, re.M), extra
        assert f'[{extra}' in _read("README.md") or f",{extra}" in _read(
            "README.md") or f'"{extra}' in _read("README.md")


def test_text_io_always_declares_encoding():
    """Cross-platform guard (user field report, VSCode/Windows, 2026-07-16):
    a read_text / write_text call WITHOUT encoding= uses the platform
    default code page — on Windows that crashed the report tab for a title
    containing this project's daily notation (a UnicodeEncodeError leaking
    through, violating K26). Every text I/O in the shipped tree must
    declare encoding explicitly."""
    offenders = []
    for base in ("src", "tests", "examples"):
        for path in (ROOT / base).rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            for m in re.finditer(r"\.(?:read_text|write_text)\(", text):
                # inspect the call's argument span (up to 200 chars is
                # plenty for these call sites)
                span = text[m.end():m.end() + 200]
                depth, arg = 1, []
                for ch in span:
                    if ch == "(":
                        depth += 1
                    elif ch == ")":
                        depth -= 1
                        if depth == 0:
                            break
                    arg.append(ch)
                if "encoding=" not in "".join(arg):
                    line = text[:m.start()].count("\n") + 1
                    offenders.append(f"{path.relative_to(ROOT)}:{line}")
    assert not offenders, (
        "text I/O without explicit encoding= (Windows code-page hazard): "
        + ", ".join(offenders))
