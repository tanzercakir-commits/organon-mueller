"""Milestone UI-2: file loading + batch decomposition.

Deliberately NOT gradio-gated: ``ui/loaders.py`` and the file callbacks
in ``ui/app.py`` import no gradio (the module-level app imports are
stdlib-only), so this parse surface stays tested even on environments
without the ``ui`` extra. The parser is the project's second text-parse
surface (after safe_parse.py) — the hostile-input tests here are the
point, not an afterthought.
"""
import pathlib

import pytest

from organon_mueller.ui import loaders
from organon_mueller.ui.app import batch_cb, load_file_cb, synthetic_type1

IDENT16 = ["1", "0", "0", "0", "0", "1", "0", "0",
           "0", "0", "1", "0", "0", "0", "0", "1"]


def _flat_synth():
    return [str(v) for row in synthetic_type1() for v in row]


def _write(tmp_path, name, text):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


# -- parser: accepted shapes -------------------------------------------------------

def test_single_4x4_with_header_comma(tmp_path):
    p = _write(tmp_path, "m.csv",
               "c0,c1,c2,c3\n1,0,0,0\n0,1,0,0\n0,0,1,0\n0,0,0,1\n")
    r = loaders.parse_matrix_file(p)
    assert r["kind"] == "single" and r["matrix"][2][2] == 1.0


def test_single_4x4_whitespace_no_header(tmp_path):
    p = _write(tmp_path, "m.txt", "1 0 0 0\n0 1 0 0\n0 0 1 0\n0 0 0 1\n")
    assert loaders.parse_matrix_file(p)["kind"] == "single"


def test_batch_16_columns_row_labels(tmp_path):
    p = _write(tmp_path, "b.csv",
               ",".join(IDENT16) + "\n" + ",".join(IDENT16) + "\n")
    r = loaders.parse_matrix_file(p)
    assert r["kind"] == "batch" and r["labels"] == ["1", "2"]
    assert r["matrices"][0][3][3] == 1.0


def test_batch_17_columns_label_semicolon_and_comments(tmp_path):
    body = ("# comment line\n"
            "wl;" + ";".join(f"m{k}" for k in range(16)) + "\n"
            "500;" + ";".join(IDENT16) + "\n"
            "\n"
            "550;" + ";".join(IDENT16) + "\n")
    r = loaders.parse_matrix_file(_write(tmp_path, "b.csv", body))
    assert r["labels"] == ["500", "550"] and len(r["matrices"]) == 2


def test_batch_17_nonnumeric_label_without_header_is_data(tmp_path):
    """Width-aware header rule: a non-numeric LABEL must not eat the
    first data row (only the 16 matrix cells decide header-ness)."""
    body = ("sampleA," + ",".join(IDENT16) + "\n"
            "sampleB," + ",".join(IDENT16) + "\n")
    r = loaders.parse_matrix_file(_write(tmp_path, "b.csv", body))
    assert r["labels"] == ["sampleA", "sampleB"]
    assert len(r["matrices"]) == 2


def test_bom_and_tab_delimiter(tmp_path):
    p = tmp_path / "m.tsv"
    p.write_bytes("﻿1\t0\t0\t0\n0\t1\t0\t0\n0\t0\t1\t0\n0\t0\t0\t1\n"
                  .encode("utf-8"))
    assert loaders.parse_matrix_file(p)["kind"] == "single"


def test_long_label_truncated(tmp_path):
    long = "L" * 500
    body = long + "," + ",".join(IDENT16) + "\n"
    r = loaders.parse_matrix_file(_write(tmp_path, "b.csv", body))
    assert len(r["labels"][0]) == loaders.MAX_LABEL_CHARS


# -- parser: hostile inputs (K26 readable reasons, never a crash) ------------------

@pytest.mark.parametrize("body,frag", [
    ("", "empty"),
    ("# only\n\n# comments\n", "no data lines"),
    ("h1,h2,h3,h4\n", "only a header"),
    ("1,2,3\n1,2,3\n1,2,3\n1,2,3\n", "delimiter/column count"),
    ("1,2,3,4,5\n" * 4, "unsupported column count 5"),
    ("1,2,3,4\n" * 3, "exactly 4 data rows"),
    ("1,2,3,4\n1,2,x,4\n1,2,3,4\n1,2,3,4\n", "[row 2][col 3]"),
    ("1,2,3,nan\n" + "1,2,3,4\n" * 3, "not finite"),
    ("1,2,3,inf\n" + "1,2,3,4\n" * 3, "not finite"),
    ("1,2,3,4\n1,2,3,4,5\n1,2,3,4\n1,2,3,4\n", "delimiter/column count"),
], ids=["empty", "comments-only", "header-only", "3cols", "5cols",
        "3rows", "bad-cell", "nan", "inf", "ragged"])
def test_parser_rejects_with_reason(tmp_path, body, frag):
    p = _write(tmp_path, "bad.csv", body)
    with pytest.raises(ValueError) as e:
        loaders.parse_matrix_file(p)
    assert frag in str(e.value)


def test_binary_file_rejected(tmp_path):
    p = tmp_path / "img.csv"
    p.write_bytes(b"\x89PNG\r\n\x1a\n" + bytes(range(256)))
    with pytest.raises(ValueError, match="UTF-8"):
        loaders.parse_matrix_file(p)


def test_oversize_file_rejected(tmp_path):
    p = tmp_path / "big.csv"
    p.write_bytes(b"1" * (loaders.MAX_FILE_BYTES + 1))
    with pytest.raises(ValueError, match="too large"):
        loaders.parse_matrix_file(p)


def test_row_cap_enforced(tmp_path, monkeypatch):
    monkeypatch.setattr(loaders, "MAX_MATRICES", 3)
    body = "\n".join(",".join(IDENT16) for _ in range(4))
    with pytest.raises(ValueError, match="too many rows"):
        loaders.parse_matrix_file(_write(tmp_path, "b.csv", body))


def test_line_length_cap(tmp_path):
    body = "1," * 40000 + "1\n"
    with pytest.raises(ValueError, match="longer than"):
        loaders.parse_matrix_file(_write(tmp_path, "b.csv", body))


def test_missing_file_rejected(tmp_path):
    with pytest.raises(ValueError, match="not found"):
        loaders.parse_matrix_file(tmp_path / "nope.csv")


# -- callbacks ---------------------------------------------------------------------

def test_load_file_cb_single_into_grid(tmp_path):
    p = _write(tmp_path, "m.csv", "\n".join(
        ",".join(str(v) for v in row) for row in synthetic_type1()))
    grid, status = load_file_cb(str(p), 1)
    assert not status.startswith("Error:")
    assert grid == synthetic_type1()


def test_load_file_cb_batch_row_and_bounds(tmp_path):
    body = ("500," + ",".join(_flat_synth()) + "\n"
            "550," + ",".join(IDENT16) + "\n")
    p = _write(tmp_path, "b.csv", body)
    grid, status = load_file_cb(str(p), 2)
    assert "row 2" in status and grid[0][0] == 1.0 and grid[0][1] == 0.0
    _, bad = load_file_cb(str(p), 99)
    assert bad.startswith("Error:") and "between 1 and 2" in bad
    _, none_file = load_file_cb(None, 1)
    assert none_file.startswith("Error:")


def test_batch_cb_mixed_results_and_csv(tmp_path):
    body = ("500," + ",".join(_flat_synth()) + "\n"
            "550," + ",".join(IDENT16) + "\n"     # rank-1 -> honest failure
            "600," + ",".join(_flat_synth()) + "\n")
    p = _write(tmp_path, "b.csv", body)
    summary, rows, csv_path = batch_cb(str(p), "type1", "auto",
                                       1e-9, 1e-6, 1e-6)
    assert "3 matrices — 2 decomposed, 1 failed" in summary
    by_label = {r[0]: r for r in rows}
    assert by_label["500"][1] == "ok"
    assert abs(float(by_label["500"][2]) - 0.35) < 1e-6
    assert by_label["550"][1] == "failed" and "rank" in by_label["550"][2]
    text = pathlib.Path(csv_path).read_text(encoding="utf-8").splitlines()
    assert text[0] == "label,status,alpha1_or_reason"
    assert len(text) == 4


def test_batch_cb_error_paths(tmp_path):
    summary, rows, csv_path = batch_cb(None, "type1", "auto",
                                       None, None, None)
    assert summary.startswith("Error:") and rows == [] and csv_path is None
    p = _write(tmp_path, "bad.csv", "1,2,3\n")
    summary, rows, csv_path = batch_cb(str(p), "type1", "auto",
                                       None, None, None)
    assert summary.startswith("Error:") and csv_path is None


def test_batch_csv_neutralizes_formula_injection(tmp_path):
    """A label like '=HYPERLINK(...)' must not survive into the results
    CSV as a live spreadsheet formula (guard sits INSIDE the quotes)."""
    body = ("=HYPERLINK(1)," + ",".join(IDENT16) + "\n"
            "+cmd," + ",".join(IDENT16) + "\n")
    p = _write(tmp_path, "b.csv", body)
    _, _, csv_path = batch_cb(str(p), "type1", "auto", None, None, None)
    lines = pathlib.Path(csv_path).read_text(encoding="utf-8").splitlines()[1:]
    assert lines[0].startswith("\"'=") and lines[1].startswith("\"'+")


# -- review UI-2 findings, locked --------------------------------------------------

def test_empty_cell_never_shifts_columns(tmp_path):
    """Review finding 1 (MODERATE): a consistently blank column must be a
    readable ERROR, never a silent reinterpretation as a narrower format
    with shifted (wrong) matrices."""
    # 17-col labeled file whose last numeric column is always empty
    body = ("450," + ",".join(IDENT16[:15]) + ",\n"
            "500," + ",".join(IDENT16[:15]) + ",\n")
    with pytest.raises(ValueError, match="empty"):
        loaders.parse_matrix_file(_write(tmp_path, "b.csv", body))
    # inner empty cell
    with pytest.raises(ValueError, match=r"\[row 1\]\[col 2\].*empty"):
        loaders.parse_matrix_file(_write(
            tmp_path, "m.csv", "1,,2,3\n" + "1,2,3,4\n" * 3))
    # trailing comma on a 4-col row -> 5 cells, strict rejection
    with pytest.raises(ValueError):
        loaders.parse_matrix_file(_write(
            tmp_path, "t.csv", "1,2,3,4,\n" * 4))


def test_empty_label_rejected(tmp_path):
    body = ("," + ",".join(IDENT16) + "\n")
    with pytest.raises(ValueError, match="label cell in row 1 is empty"):
        loaders.parse_matrix_file(_write(tmp_path, "b.csv", body))


def test_header_skip_is_visible(tmp_path):
    """Review finding 3: a stripped header line must be REPORTED, so a
    typo'd first data row cannot vanish silently."""
    body = ("wl," + ",".join(f"m{k}" for k in range(16)) + "\n"
            "500," + ",".join(IDENT16) + "\n")
    p = _write(tmp_path, "b.csv", body)
    parsed = loaders.parse_matrix_file(p)
    assert parsed["header_skipped"] is True
    _, status = load_file_cb(str(p), 1)
    assert "skipped 1 header line" in status
    summary, _, _ = batch_cb(str(p), "type1", "auto", None, None, None)
    assert "Skipped 1 header line." in summary
    # and NO false notice without a header
    p2 = _write(tmp_path, "b2.csv", "500," + ",".join(IDENT16) + "\n")
    assert loaders.parse_matrix_file(p2)["header_skipped"] is False


def test_unreadable_file_gives_reason(tmp_path, monkeypatch):
    """Review finding 4: OSError (permissions/races) must surface as a
    readable reason, not a traceback."""
    p = _write(tmp_path, "m.csv", "1,2,3,4\n" * 4)

    def boom(self):
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(pathlib.Path, "read_bytes", boom)
    with pytest.raises(ValueError, match="cannot read file"):
        loaders.parse_matrix_file(p)


def test_batch_csv_quotes_comma_bearing_labels(tmp_path):
    """Review finding 2: a tab-delimited file may carry commas INSIDE the
    label — the results CSV must stay structurally valid (quoted)."""
    import csv as _csv

    body = ("a,b\t" + "\t".join(IDENT16) + "\n")
    p = _write(tmp_path, "b.tsv", body)
    _, _, csv_path = batch_cb(str(p), "type1", "auto", None, None, None)
    with open(csv_path, newline="", encoding="utf-8") as fh:
        rows = list(_csv.reader(fh))
    assert rows[0] == ["label", "status", "alpha1_or_reason"]
    assert len(rows[1]) == 3 and rows[1][0] == "a,b"


def test_organon_ui_without_gradio_gives_readable_message():
    """User field report (2026-07-16): the organon-ui console script is
    installed even WITHOUT the [ui] extra, and used to die with a raw
    ModuleNotFoundError traceback (K26 breach). It must print ONE
    readable line telling the user the fix."""
    import subprocess
    import sys

    code = (
        "import sys; sys.modules['gradio'] = None\n"
        "from organon_mueller.ui.app import main\n"
        "try:\n"
        "    main(argv=['--no-browser'])\n"
        "except SystemExit as e:\n"
        "    msg = str(e)\n"
        "    assert 'organon-mueller[ui]' in msg, msg\n"
        "    assert 'Traceback' not in msg\n"
        "    print('OK')\n"
        "else:\n"
        "    raise AssertionError('expected SystemExit')\n"
    )
    out = subprocess.run([sys.executable, "-c", code],
                         capture_output=True, text=True, timeout=120,
                         encoding="utf-8", errors="replace")
    assert out.returncode == 0 and "OK" in out.stdout, (
        out.stdout + out.stderr)
    assert "ModuleNotFoundError" not in out.stderr


def test_typo_in_first_row_names_the_cell(tmp_path):
    """User field diagnosis (2026-07-16): a data row with ONE typo'd cell
    ('1,abc,3,4') used to be absorbed as a 'header' and surfaced as a
    confusing row-count error. Header rule is now 'no must-numeric cell
    parses as a number' — a single numeric cell makes the row DATA, so
    the user gets the exact cell named, same as anywhere else."""
    body = "1,abc,3,4\n1,2,3,4\n1,2,3,4\n1,2,3,4\n"
    with pytest.raises(ValueError) as e:
        loaders.parse_matrix_file(_write(tmp_path, "m.csv", body))
    msg = str(e.value)
    assert "[row 1][col 2]" in msg and "'abc'" in msg
    # the neighbour's example: three numbers + one typo = data, not header
    body2 = ("abc,0.0,0.0,0.0\n" + "1,2,3,4\n" * 3)
    with pytest.raises(ValueError, match=r"\[row 1\]\[col 1\]"):
        loaders.parse_matrix_file(_write(tmp_path, "m3.csv", body2))
    # a GENUINE header (all cells non-numeric) over too few rows gets the
    # explanatory hint on the row-count message
    with pytest.raises(ValueError) as e3:
        loaders.parse_matrix_file(_write(
            tmp_path, "m4.csv", "c0,c1,c2,c3\n" + "1,2,3,4\n" * 3))
    assert ("found 3 rows" in str(e3.value)
            and "first line was treated as a header" in str(e3.value))
    # ...and a genuinely short file (no header involved) stays hint-free
    with pytest.raises(ValueError) as e2:
        loaders.parse_matrix_file(_write(
            tmp_path, "m2.csv", "1,2,3,4\n" * 3))
    assert "treated as a header" not in str(e2.value)


def test_none_and_odd_path_types_give_reason():
    """Field note (2026-07-16): parse_matrix_file(None) raised TypeError.
    Unreachable from the UI (callbacks guard falsy paths), but a direct
    caller must still get a readable reason — defence in depth."""
    for bad in (None, 123, 1.5, ["x"], {"p": 1}):
        with pytest.raises(ValueError, match="no file provided"):
            loaders.parse_matrix_file(bad)
