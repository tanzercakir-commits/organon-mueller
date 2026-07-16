"""File loading for the local UI (milestone UI-2) — a deliberately
STRICT, gradio-free, numbers-only parser.

Security contract (this is the project's second text-parse surface,
after safe_parse.py — see specs/milestone-ui-02.md §3):

- Every retained value is produced by ``float()`` on a single cell and
  checked finite; the ONLY non-numeric data kept is the optional batch
  label column, stored as an inert, length-capped display string.
- No eval/exec, no csv-module dialects, no pandas — line/cell splitting
  and ``float()`` only, so the attack surface is enumerable by eye.
- DoS caps: file size, matrix count, line length. Everything rejected
  carries a readable reason (K26), never a traceback.
- Defence in depth: whatever this module outputs is re-validated by
  ``tool_decompose_mueller`` before any solver runs.

Accepted shapes (documented in docs/README-ui.md):
- single: exactly 4 data rows x 4 numeric columns  -> one 4x4 matrix
- batch:  N data rows x 16 numeric columns (m00..m33 row-major), or
          N data rows x 17 columns (leading label column + 16 entries)
"""
from __future__ import annotations

from pathlib import Path

MAX_FILE_BYTES = 5 * 1024 * 1024      # 5 MB
MAX_MATRICES = 10_000
MAX_LINE_CHARS = 65_536
MAX_LABEL_CHARS = 64

_DELIMITERS = (",", ";", "\t", None)   # None = any whitespace


def _err(msg: str) -> ValueError:
    return ValueError(msg)


def _read_text(path) -> str:
    p = Path(path)
    try:
        if not p.is_file():
            raise _err("file not found")
        size = p.stat().st_size
        if size == 0:
            raise _err("file is empty")
        if size > MAX_FILE_BYTES:
            raise _err(f"file too large ({size} bytes; limit "
                       f"{MAX_FILE_BYTES} = 5 MB)")
        raw = p.read_bytes()
    except OSError as exc:            # permissions, races, ... (review 4)
        raise _err(f"cannot read file: {exc.strerror or exc}") from None
    try:
        text = raw.decode("utf-8-sig")              # tolerates a BOM
    except UnicodeDecodeError:
        raise _err("file is not UTF-8 text (is it binary or another "
                   "encoding?)") from None
    return text


def _data_lines(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        if len(raw) > MAX_LINE_CHARS:
            raise _err(f"line longer than {MAX_LINE_CHARS} characters")
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    if not lines:
        raise _err("no data lines found (only blanks/comments)")
    return lines


def _split(line: str, delim) -> list[str]:
    """Split ONE line. Empty cells are KEPT for explicit delimiters
    (review UI-2 finding 1: silently dropping them let a file with a
    consistently blank column reparse as a narrower format and produce
    SHIFTED, wrong matrices with no error — the one failure mode a
    scientific loader must not have). Whitespace mode cannot produce
    empties. Empty cells are then rejected per-cell with row/col."""
    if delim is None:
        return line.split()
    return [c.strip() for c in line.split(delim)]


def _pick_delimiter(lines: list[str]) -> object:
    """First delimiter that gives a CONSISTENT column count >= 4 on every
    line. Deterministic preference order: ',', ';', tab, whitespace."""
    for delim in _DELIMITERS:
        counts = {len(_split(ln, delim)) for ln in lines}
        if len(counts) == 1 and counts.pop() >= 4:
            return delim
    raise _err("could not detect a consistent delimiter/column count "
               "(expected 4, 16 or 17 columns on every line; delimiters: "
               "comma, semicolon, tab or whitespace; decimal POINT only)")


def _cell_float(cell: str, row: int, col: int) -> float:
    if cell == "":
        raise _err(f"cell [row {row}][col {col}] is empty (strict mode: "
                   "no blank cells, no trailing delimiters)")
    try:
        v = float(cell)
    except ValueError:
        raise _err(f"cell [row {row}][col {col}] is not a number: "
                   f"{cell[:40]!r} (decimal POINT only; no units)") from None
    if v != v or v in (float("inf"), float("-inf")):
        raise _err(f"cell [row {row}][col {col}] is not finite ({cell[:40]})")
    return v


def _is_header(cells: list[str]) -> bool:
    """A single leading header line — width-aware: in the 17-column
    (label + 16) format the label cell may legitimately be non-numeric
    (a sample name), so only the cells that MUST be numeric are tested.

    Rule (field diagnosis, 2026-07-16): a line is a header only if NONE
    of its must-numeric cells parses as a number. Seeing even one
    numeric cell is data evidence — real headers carry no numbers — so a
    data row with a single typo ('1,abc,3,4') is treated as DATA and the
    strict per-cell check names the exact cell, instead of the row being
    absorbed as a 'header' and surfacing as a confusing row-count error.
    An EMPTY cell is likewise never header evidence (same rationale:
    '1,,2,3' must report the precise cell)."""
    numeric_cells = cells[1:] if len(cells) == 17 else cells
    for c in numeric_cells:
        if c == "":
            return False              # data: precise empty-cell report
        try:
            float(c)
            return False              # a numeric cell = data evidence
        except ValueError:
            continue
    return True                       # all non-empty and non-numeric


def parse_matrix_file(path) -> dict:
    """Parse a Mueller-matrix text file.

    Returns {"kind": "single", "matrix": 4x4 floats}
         or {"kind": "batch", "labels": [str], "matrices": [4x4 floats]}.
    Raises ValueError with a readable reason on ANY deviation.
    """
    lines = _data_lines(_read_text(path))
    delim = _pick_delimiter(lines)
    rows = [_split(ln, delim) for ln in lines]

    header_skipped = False
    if _is_header(rows[0]):
        # visible, never silent (review UI-2 finding 3): the callbacks
        # surface header_skipped so a typo'd first DATA row that gets
        # classified as a header is noticeable, not vanished.
        header_skipped = True
        rows = rows[1:]
        if not rows:
            raise _err("only a header line found — no data rows")
        # header must not hide a second, inconsistent width
        if len(rows[0]) not in (4, 16, 17) or any(
                len(r) != len(rows[0]) for r in rows):
            raise _err("inconsistent column count after the header")

    width = len(rows[0])
    if any(len(r) != width for r in rows):
        raise _err("rows have differing column counts")

    if width == 4:
        if len(rows) != 4:
            hint = ""
            if header_skipped:
                # user field report (2026-07-16): a TYPO in the first data
                # row makes it look like a header, and a bare row-count
                # message sends the user hunting in the wrong place
                hint = (" Note: the first line was treated as a header "
                        "because it contains a non-numeric cell — if it "
                        "was meant to be data, fix that cell instead.")
            raise _err(f"a 4-column file must have exactly 4 data rows "
                       f"(one 4x4 matrix); found {len(rows)} rows. For a "
                       "batch, use 16 columns per row (m00..m33) or 17 "
                       "(label + 16)." + hint)
        matrix = [[_cell_float(c, i + 1, j + 1)
                   for j, c in enumerate(row)] for i, row in enumerate(rows)]
        return {"kind": "single", "matrix": matrix,
                "header_skipped": header_skipped}

    if width in (16, 17):
        if len(rows) > MAX_MATRICES:
            raise _err(f"too many rows ({len(rows)}; limit {MAX_MATRICES})")
        labeled = width == 17
        labels, matrices = [], []
        for i, row in enumerate(rows, start=1):
            if labeled:
                if row[0] == "":
                    raise _err(f"label cell in row {i} is empty")
                labels.append(row[0][:MAX_LABEL_CHARS])
                cells = row[1:]
            else:
                labels.append(str(i))
                cells = row
            flat = [_cell_float(c, i, j + (2 if labeled else 1))
                    for j, c in enumerate(cells)]
            matrices.append([flat[k * 4:(k + 1) * 4] for k in range(4)])
        return {"kind": "batch", "labels": labels, "matrices": matrices,
                "header_skipped": header_skipped}

    raise _err(f"unsupported column count {width} (expected 4 for a "
               "single matrix, 16 for m00..m33 rows, or 17 for "
               "label + m00..m33)")
