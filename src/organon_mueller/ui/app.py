"""organon-ui — local web interface (milestone UI-1).

Design contract:

- THIN layer: every computation goes through the already-hardened,
  numeric-only tool functions in ``..mcp_server.tools`` (numbers and enum
  strings only; failures return a reason, never a traceback — K26). The
  UI adds NO new parse path.
- LOCAL only: ``HOST = "127.0.0.1"`` and ``share=False`` are hard-coded
  in :func:`launch_kwargs`; the only listener is loopback on the user's
  own machine (Stage 18 posture: no hosted surface).
- TESTABLE: callbacks are pure functions over plain lists; ``main()``
  takes an injectable ``_launch`` so tests assert the exact launch
  kwargs without opening a socket.
- ENGLISH copy only (user decision, 2026-07-16): every user-facing
  string lives in :data:`STRINGS` so a test can enforce the language.
"""
from __future__ import annotations

import argparse
import itertools
import json
import tempfile
from pathlib import Path

# --------------------------------------------------------------------------
# security posture (hard-coded; tests assert these reach launch verbatim)
# --------------------------------------------------------------------------
HOST = "127.0.0.1"
SHARE = False          # never a Gradio tunnel
DEFAULT_PORT = 7860

_SYMMETRIES = ("type1", "type2", "type3", "type1-2", "type1-3", "type2-3")
_VARIANTS = ("auto", "a", "b")

# --------------------------------------------------------------------------
# UI copy — English only (single source so tests can enforce it)
# --------------------------------------------------------------------------
STRINGS = {
    "title": "organon-mueller — local interface",
    "intro": (
        "Interactive front end for the Stokes–Mueller decomposition "
        "engine. Enter or edit the 4×4 Mueller matrix below (cells are "
        "editable), then use the tabs. Everything runs **locally on your "
        "machine** (127.0.0.1) — nothing is uploaded anywhere."
    ),
    "matrix_label": "Mueller matrix M (4×4, real; edit cells directly)",
    "ex_identity": "Load: identity",
    "ex_synth": "Load: exact type1 mixture (default tolerances)",
    "ex_synth_note": (
        "Exact synthetic mixture loaded (0.35 · type1 pure + 0.65 · "
        "generic pure, seed 20260716). Decomposes under the DEFAULT "
        "tolerances with symmetry type1 — expect α₁ = 0.35."
    ),
    "ex_ao2016": "Load: AO2016 §6 mixture (0.3·M1 + 0.7·M2)",
    "ex_ao2016_note": (
        "AO2016 §6 preset loaded (print-precision data). Tolerances set "
        "to the demo preset (rank 1e-4, PSD 1e-3, rank-1 1e-2) and "
        "symmetry to type3, variant a — the paper's §6 configuration."
    ),
    "tab_decompose": "Decompose",
    "tab_propose": "Propose hypotheses",
    "tab_report": "LaTeX report",
    "tab_file": "File / batch",
    "file_help": (
        "Load Mueller matrices from a text file (`.csv`, `.tsv`, `.txt`; "
        "UTF-8, decimal point, delimiter comma/semicolon/tab/whitespace, "
        "optional single header line, `#` comments ignored).\n\n"
        "- **Single matrix**: 4 rows × 4 columns → use *Load into "
        "editor*.\n"
        "- **Batch**: one matrix per row — 16 columns (m00…m33, "
        "row-major) or 17 columns (leading label such as wavelength + "
        "16 entries). *Decompose all rows* runs the symmetry/variant/"
        "tolerance settings above on every row; *Load into editor* "
        "brings one chosen row into the grid for hands-on work.\n\n"
        "Limits: 5 MB, 10,000 matrices. The file is parsed strictly as "
        "numbers on your machine; nothing is uploaded anywhere."
    ),
    "file_label": "Matrix file (.csv / .tsv / .txt)",
    "row_label": "Batch row to load (1-based)",
    "btn_load_file": "Load into editor",
    "btn_batch": "Decompose all rows",
    "batch_results_label": "Batch results",
    "batch_csv_label": "Download results (.csv)",
    "symmetry_label": "Symmetry hypothesis",
    "variant_label": "Variant (a/b equation sets; auto = denominator health)",
    "advanced": "Advanced tolerances",
    "rank_tol": "rank_tol (effective-rank threshold)",
    "psd_tol": "psd_tol (positive-semidefiniteness slack)",
    "rank1_tol": "rank1_tol (rank-1 residual threshold)",
    "btn_decompose": "Decompose",
    "btn_propose": "Try every hypothesis",
    "propose_nonunique_note": (
        "**Several hypotheses are exact at once.** That is expected, not "
        "an error: composite types subsume fundamental ones, and a "
        "decomposition is generally *a* decomposition, not *the* "
        "decomposition (verified non-uniqueness — see "
        "`docs/candidate-findings.md`). Selecting the physically "
        "meaningful one is a domain judgement the engine deliberately "
        "does not make."
    ),
    "btn_report": "Generate LaTeX",
    "m1_label": "Component M1 (symmetric part, α₁·M1)",
    "m2_label": "Component M2 (remainder)",
    "details_label": "Details (JSON)",
    "propose_label": "Result",
    "report_title_label": "Report title",
    "latex_label": "LaTeX source",
    "download_label": "Download .tex",
    "tab_lorentz": "Lorentz transform",
    "lorentz_help": (
        "The Lorentz face of the engine (`organon_mueller.lorentz`): pick "
        "a **boost** or a **rotation**, enter the parameter and an axis, "
        "and read off the Lorentz matrix Λ = ZZ*. The axis is normalized "
        "for you; only numbers are entered (the covariance parameters α "
        "are computed, never typed). The 40 proven identities and the full "
        "sweep are reference material — see `reports/sweep-lorentz-01.json`."
    ),
    "lorentz_kind_label": "Transformation",
    "lorentz_angle_label": (
        "Parameter — rapidity φ (boost) or angle θ (rotation), in radians"
    ),
    "lorentz_axis_help": "Axis n (any non-zero vector; normalized for you)",
    "btn_lorentz": "Compute Λ",
    "lorentz_alpha_label": "Covariance parameters (computed)",
    "lorentz_matrix_label": "Lorentz matrix Λ (4×4, real)",
    "lorentz_badge_label": "Validity",
    "footer": (
        "**Evidence discipline.** Numbers shown here are evidence class "
        "*numeric-deterministic*; the symbolic proofs live in the test "
        "suite (see `docs/VERIFICATION.md`). Outputs beyond the published "
        "tables are *candidates* — no novelty or physics claim is made; "
        "that judgement is reserved for human experts "
        "(`docs/novelty-protocol.md`, step 5). Hypothesis *scores* are an "
        "ordering heuristic, not evidence; acceptance is decided solely "
        "by the exact solvers. This app binds to 127.0.0.1 and never "
        "creates a public link."
    ),
    "err_prefix": "Error: ",
}

# AO2016 Section 6 component matrices at print precision (same data as
# examples/demo.py; the mixture is 0.3*M1 + 0.7*M2).
_M1_PAPER = [
    [1.0, 0.0, 0.0, 0.1489],
    [0.0, 0.9108, 0.3851, 0.0],
    [0.0, -0.3851, 0.9108, 0.0],
    [0.1489, 0.0, 0.0, 1.0],
]
_M2_PAPER = [
    [1.0, 0.0544, 0.6124, 0.2719],
    [0.2502, 0.7064, 0.2447, 0.2273],
    [0.6124, -0.2146, 0.8118, 0.4669],
    [-0.1196, -0.0768, -0.4519, 0.5935],
]
# demo.py preset for print-precision data (documented there: health != accuracy)
AO2016_PRESET = {"symmetry": "type3", "variant": "a",
                 "rank_tol": 1e-4, "psd_tol": 1e-3, "rank1_tol": 1e-2}

# Exact synthetic two-term mixture: 0.35 * (type1 pure, x=0.42, w=|w|e^{0.7i})
# + 0.65 * generic pure (seed 20260716), rounded at 1e-12 (well inside the
# default tolerances). decompose(symmetry="type1") on DEFAULT tolerances
# recovers alpha1 = 0.35 — a clean first-run example.
SYNTHETIC_TYPE1 = [
    [1.0, -0.119053107844, -0.370818722287, -0.120455781008],
    [0.179735764917, 0.661694060772, -0.473703504039, 0.023050796426],
    [-0.107366637711, -0.072411201633, 0.295400357743, 0.743936714628],
    [0.298149071156, -0.409984524562, -0.645240415593, 0.171162044055],
]


def identity_matrix() -> list[list[float]]:
    return [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]


def synthetic_type1() -> list[list[float]]:
    return [row[:] for row in SYNTHETIC_TYPE1]


def ao2016_mixture() -> list[list[float]]:
    return [[round(0.3 * _M1_PAPER[i][j] + 0.7 * _M2_PAPER[i][j], 6)
             for j in range(4)] for i in range(4)]


# --------------------------------------------------------------------------
# grid handling (Dataframe value -> plain 4x4 float list; K26 on failure)
# --------------------------------------------------------------------------

def _grid_to_matrix(grid) -> list[list[float]]:
    """Normalize a Gradio Dataframe value (pandas DataFrame, numpy array,
    or nested list) to a 4x4 nested list of floats. Raises ValueError with
    a readable reason on anything else — the tool layer re-validates
    independently (defence in depth)."""
    if grid is None:
        raise ValueError("matrix is empty — enter a 4x4 Mueller matrix")
    values = getattr(grid, "values", grid)          # pandas -> ndarray
    tolist = getattr(values, "tolist", None)
    rows = tolist() if callable(tolist) else values
    if not (isinstance(rows, (list, tuple)) and len(rows) == 4
            and all(isinstance(r, (list, tuple)) and len(r) == 4
                    for r in rows)):
        raise ValueError("matrix must be exactly 4x4")
    out: list[list[float]] = []
    for i, row in enumerate(rows):
        new_row: list[float] = []
        for j, v in enumerate(row):
            if v is None or (isinstance(v, str) and not v.strip()):
                raise ValueError(f"cell [{i}][{j}] is empty")
            try:
                new_row.append(float(v))
            except (TypeError, ValueError):
                raise ValueError(
                    f"cell [{i}][{j}] is not a number: {v!r}") from None
        out.append(new_row)
    return out


def _tols(rank_tol, psd_tol, rank1_tol) -> dict:
    """Pass tolerances through as plain floats; the tool layer enforces
    the (0, 1) range and returns its own reasons. Note: a numeric STRING
    ("0.5") is float()ed here — gr.Number only ever delivers float/None,
    so this arises only for direct module callers, and the boundary still
    receives numbers only (review UI-1, finding 7)."""
    out = {}
    for key, val in (("rank_tol", rank_tol), ("psd_tol", psd_tol),
                     ("rank1_tol", rank1_tol)):
        if val is None or val == "":
            continue
        try:
            out[key] = float(val)
        except (TypeError, ValueError):
            out[key] = val          # let the tool layer report the reason
    return out


def _err(msg: str) -> str:
    return STRINGS["err_prefix"] + str(msg)


# --------------------------------------------------------------------------
# callbacks (pure; UI-independent; every failure is a readable string)
# --------------------------------------------------------------------------

def decompose_cb(grid, symmetry, variant, rank_tol, psd_tol, rank1_tol):
    """-> (summary_markdown, m1_grid, m2_grid, details_json_str)"""
    from ..mcp_server.tools import tool_decompose_mueller

    empty = [[0.0] * 4 for _ in range(4)]
    try:
        matrix = _grid_to_matrix(grid)
    except ValueError as exc:
        return _err(exc), empty, empty, "{}"
    payload = {"mueller": matrix, "symmetry": symmetry, "variant": variant,
               **_tols(rank_tol, psd_tol, rank1_tol)}
    if symmetry not in ("type1", "type2", "type3"):
        payload.pop("variant", None)        # composites take no variant
    result = tool_decompose_mueller(payload)
    if "error" in result:
        return _err(result["error"]), empty, empty, "{}"
    summary = (f"**{result['kind']}** — symmetry `{result['symmetry']}`"
               + (f", variant `{result['variant']}`"
                  if result.get("variant") else "")
               + f" · α₁ = {result['alpha1']:.6g}")
    return (summary, result["m1"], result["m2"],
            json.dumps(result, indent=2))


def propose_cb(grid):
    """-> (markdown_summary, details_json_str)"""
    from ..mcp_server.tools import tool_propose_hypotheses

    try:
        matrix = _grid_to_matrix(grid)
    except ValueError as exc:
        return _err(exc), "{}"
    result = tool_propose_hypotheses({"mueller": matrix})
    if "error" in result:
        return _err(result["error"]), "{}"
    lines = [f"**Covariance rank: {result['rank']}**", ""]
    if result["accepted"]:
        lines.append("Accepted (by the exact solvers):")
        lines += [f"- `{a['hypothesis']}` — α₁ = {a['alpha1']:.6g}"
                  if "alpha1" in a else f"- `{a['hypothesis']}`"
                  for a in result["accepted"]]
    else:
        lines.append("Accepted: none.")
    if result["rejected"]:
        lines.append("")
        lines.append("Rejected (with reasons):")
        lines += [f"- `{r['hypothesis']}`: {r['reason']}"
                  for r in result["rejected"]]
    if len(result["accepted"]) > 1:
        # field observation (2026-07-16): several exact hypotheses at once
        # prompts "which one is right?" — answer it where it happens
        lines += ["", STRINGS["propose_nonunique_note"]]
    lines += ["", f"*{result['note']}*"]
    return "\n".join(lines), json.dumps(result, indent=2)


# one process-lifetime temp dir (auto-cleaned at interpreter exit), a
# fresh file name per click — review UI-1 finding 5: no per-click dir leak
_REPORT_TMP = None
_REPORT_SEQ = itertools.count(1)


def _new_artifact_path(stem: str, suffix: str) -> Path:
    global _REPORT_TMP
    if _REPORT_TMP is None:
        _REPORT_TMP = tempfile.TemporaryDirectory(prefix="organon_ui_")
    return Path(_REPORT_TMP.name) / f"{stem}-{next(_REPORT_SEQ):04d}{suffix}"


def _new_report_path() -> Path:
    return _new_artifact_path("report", ".tex")


def report_cb(grid, symmetry, variant, title,
              rank_tol=None, psd_tol=None, rank1_tol=None):
    """-> (latex_source, tex_file_path_or_None, status_markdown)"""
    from ..mcp_server.tools import tool_generate_report

    try:
        matrix = _grid_to_matrix(grid)
    except ValueError as exc:
        return "", None, _err(exc)
    payload = {"mueller": matrix, "symmetry": symmetry, "variant": variant,
               "title": (title or "organon-mueller report"),
               **_tols(rank_tol, psd_tol, rank1_tol)}
    result = tool_generate_report(payload)
    if "error" in result:
        return "", None, _err(result["error"])
    tex = result["latex"]
    path = _new_report_path()
    path.write_text(tex, encoding="utf-8")
    return tex, str(path), "Report generated (evidence-labelled LaTeX)."


# -- file loading / batch (milestone UI-2) ----------------------------------

def _csv_safe(label: str) -> str:
    """Neutralize spreadsheet formula injection in a display label written
    to the results CSV (a label like '=HYPERLINK(...)' must not execute
    when the CSV is opened in a spreadsheet app)."""
    return ("'" + label) if label[:1] in ("=", "+", "-", "@") else label


def load_file_cb(file_path, row):
    """-> (grid_matrix, status_markdown). Loads a single-matrix file, or
    the chosen row of a batch file, into the editor grid."""
    from .loaders import parse_matrix_file

    keep = [[0.0] * 4 for _ in range(4)]
    if not file_path:
        return keep, _err("no file selected")
    try:
        parsed = parse_matrix_file(file_path)
    except ValueError as exc:
        return keep, _err(exc)
    head_note = (" (skipped 1 header line)"
                 if parsed.get("header_skipped") else "")
    if parsed["kind"] == "single":
        return (parsed["matrix"],
                "Loaded the 4×4 matrix into the editor." + head_note)
    n = len(parsed["matrices"])
    try:
        idx = int(row)
    except (TypeError, ValueError):
        return keep, _err("row must be a number")
    if not (1 <= idx <= n):
        return keep, _err(f"row must be between 1 and {n} "
                          "(the file has that many matrices)")
    label = parsed["labels"][idx - 1]
    return (parsed["matrices"][idx - 1],
            f"Batch file with {n} matrices — loaded row {idx} "
            f"(label `{label}`) into the editor." + head_note)


def batch_cb(file_path, symmetry, variant, rank_tol, psd_tol, rank1_tol):
    """-> (summary_markdown, results_rows, csv_path_or_None). Decomposes
    every matrix in the file through the hardened tool layer."""
    from ..mcp_server.tools import tool_decompose_mueller

    if not file_path:
        return _err("no file selected"), [], None
    from .loaders import parse_matrix_file
    try:
        parsed = parse_matrix_file(file_path)
    except ValueError as exc:
        return _err(exc), [], None
    if parsed["kind"] == "single":
        labels, matrices = ["1"], [parsed["matrix"]]
    else:
        labels, matrices = parsed["labels"], parsed["matrices"]

    payload_base = {"symmetry": symmetry,
                    **_tols(rank_tol, psd_tol, rank1_tol)}
    if symmetry in ("type1", "type2", "type3"):
        payload_base["variant"] = variant

    rows, ok = [], 0
    for label, matrix in zip(labels, matrices):
        result = tool_decompose_mueller({"mueller": matrix, **payload_base})
        if "error" in result:
            rows.append([label, "failed", result["error"]])
        else:
            ok += 1
            rows.append([label, "ok", f"{result['alpha1']:.9g}"])

    csv_path = _new_artifact_path("batch-results", ".csv")
    lines = ["label,status,alpha1_or_reason"]
    for label, status, detail in rows:
        # labels AND details are quoted+escaped (review UI-2 finding 2: a
        # comma-bearing label from a tab-delimited file must not corrupt
        # the CSV structure); the formula-injection guard sits inside the
        # quotes.
        label_q = '"' + _csv_safe(str(label)).replace('"', '""') + '"'
        detail_q = '"' + str(detail).replace('"', '""') + '"'
        lines.append(f"{label_q},{status},{detail_q}")
    csv_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    head_note = (" Skipped 1 header line."
                 if parsed.get("header_skipped") else "")
    summary = (f"**{len(rows)} matrices — {ok} decomposed, "
               f"{len(rows) - ok} failed** (symmetry `{symmetry}`"
               + (f", variant `{variant}`"
                  if "variant" in payload_base else "") + ")."
               + head_note + " "
               "Failures carry their reasons; scores/health are not "
               "evidence — acceptance is decided by the exact solvers.")
    return summary, rows, str(csv_path)


# -- Lorentz transform (milestone UI-3) -------------------------------------

def _fmt_complex(pair) -> str:
    re, im = pair
    if abs(im) < 1e-12:
        return f"{re:.6g}"
    sign = "+" if im >= 0 else "−"
    return f"{re:.6g} {sign} {abs(im):.6g}i"


def lorentz_cb(kind, angle, nx, ny, nz):
    """-> (alpha_markdown, lambda_grid, validity_markdown). Thin wrapper
    over tool_lorentz_transform; every failure is a readable string."""
    from ..mcp_server.tools import tool_lorentz_transform

    empty = [[0.0] * 4 for _ in range(4)]
    result = tool_lorentz_transform(
        {"kind": kind, "angle": angle, "axis": [nx, ny, nz]})
    if "error" in result:
        return _err(result["error"]), empty, ""

    nhat = result["axis_unit"]
    alpha_md = (
        "**α** = ("
        + ", ".join(_fmt_complex(a) for a in result["alpha"]) + ")"
        + "  ·  n̂ = ("
        + ", ".join(f"{x:.4g}" for x in nhat) + ")")

    ch = result["checks"]
    ok = ch["is_proper_orthochronous_lorentz"]
    head = ("**Proper orthochronous Lorentz transformation** — all checks "
            "pass." if ok else
            "**Not a proper orthochronous Lorentz transformation** — see "
            "the residuals below.")
    body = (
        f"\n\n- metric ΛᵀgΛ = g — residual `{ch['metric_residual']:.2e}`"
        f"\n- det Λ = `{ch['det']:.6f}` (expected +1)"
        f"\n- orthochronous (Λ₀₀ ≥ 1) — {'yes' if ch['orthochronous'] else 'no'}"
        f"\n- imaginary part of Λ — `{ch['imag_leak']:.2e}` (expected ~0)")
    return alpha_md, result["lambda"], head + body


# --------------------------------------------------------------------------
# app assembly
# --------------------------------------------------------------------------

def build_app():
    """Build (but do not launch) the Gradio Blocks app."""
    import gradio as gr

    with gr.Blocks(title=STRINGS["title"]) as app:
        gr.Markdown(f"# {STRINGS['title']}\n\n{STRINGS['intro']}")

        matrix = gr.Dataframe(
            value=synthetic_type1(), headers=["c0", "c1", "c2", "c3"],
            datatype="number", row_count=4, column_count=4,
            interactive=True, type="array",
            label=STRINGS["matrix_label"])
        with gr.Row():
            ex_id = gr.Button(STRINGS["ex_identity"], size="sm")
            ex_sy = gr.Button(STRINGS["ex_synth"], size="sm")
            ex_ao = gr.Button(STRINGS["ex_ao2016"], size="sm")

        symmetry = gr.Dropdown(choices=list(_SYMMETRIES), value="type1",
                               label=STRINGS["symmetry_label"])
        variant = gr.Radio(choices=list(_VARIANTS), value="auto",
                           label=STRINGS["variant_label"])
        with gr.Accordion(STRINGS["advanced"], open=False):
            rank_tol = gr.Number(value=1e-9, label=STRINGS["rank_tol"])
            psd_tol = gr.Number(value=1e-6, label=STRINGS["psd_tol"])
            rank1_tol = gr.Number(value=1e-6, label=STRINGS["rank1_tol"])

        preset_note = gr.Markdown("")
        ex_id.click(
            lambda: (identity_matrix(), ""),
            outputs=[matrix, preset_note])
        ex_sy.click(
            lambda: (synthetic_type1(), "type1", "auto", 1e-9, 1e-6, 1e-6,
                     STRINGS["ex_synth_note"]),
            outputs=[matrix, symmetry, variant, rank_tol, psd_tol,
                     rank1_tol, preset_note])
        ex_ao.click(
            lambda: (ao2016_mixture(), AO2016_PRESET["symmetry"],
                     AO2016_PRESET["variant"], AO2016_PRESET["rank_tol"],
                     AO2016_PRESET["psd_tol"], AO2016_PRESET["rank1_tol"],
                     STRINGS["ex_ao2016_note"]),
            outputs=[matrix, symmetry, variant, rank_tol, psd_tol,
                     rank1_tol, preset_note])

        with gr.Tab(STRINGS["tab_decompose"]):
            btn_d = gr.Button(STRINGS["btn_decompose"], variant="primary")
            summary = gr.Markdown("")
            with gr.Row():
                m1_out = gr.Dataframe(label=STRINGS["m1_label"],
                                      interactive=False, type="array")
                m2_out = gr.Dataframe(label=STRINGS["m2_label"],
                                      interactive=False, type="array")
            details = gr.Code(label=STRINGS["details_label"],
                              language="json")
            btn_d.click(decompose_cb,
                        inputs=[matrix, symmetry, variant,
                                rank_tol, psd_tol, rank1_tol],
                        outputs=[summary, m1_out, m2_out, details])

        with gr.Tab(STRINGS["tab_propose"]):
            btn_p = gr.Button(STRINGS["btn_propose"], variant="primary")
            propose_md = gr.Markdown(label=STRINGS["propose_label"])
            propose_json = gr.Code(label=STRINGS["details_label"],
                                   language="json")
            btn_p.click(propose_cb, inputs=[matrix],
                        outputs=[propose_md, propose_json])

        with gr.Tab(STRINGS["tab_file"]):
            gr.Markdown(STRINGS["file_help"])
            file_in = gr.File(label=STRINGS["file_label"],
                              file_types=[".csv", ".tsv", ".txt"],
                              type="filepath")
            with gr.Row():
                row_num = gr.Number(value=1, precision=0,
                                    label=STRINGS["row_label"])
                btn_load = gr.Button(STRINGS["btn_load_file"])
                btn_batch = gr.Button(STRINGS["btn_batch"],
                                      variant="primary")
            file_status = gr.Markdown("")
            batch_summary = gr.Markdown("")
            batch_table = gr.Dataframe(
                headers=["label", "status", "alpha1 / reason"],
                interactive=False, type="array",
                label=STRINGS["batch_results_label"])
            batch_csv = gr.File(label=STRINGS["batch_csv_label"])
            btn_load.click(load_file_cb, inputs=[file_in, row_num],
                           outputs=[matrix, file_status])
            btn_batch.click(batch_cb,
                            inputs=[file_in, symmetry, variant,
                                    rank_tol, psd_tol, rank1_tol],
                            outputs=[batch_summary, batch_table,
                                     batch_csv])

        with gr.Tab(STRINGS["tab_report"]):
            title_box = gr.Textbox(value="organon-mueller report",
                                   label=STRINGS["report_title_label"])
            btn_r = gr.Button(STRINGS["btn_report"], variant="primary")
            report_status = gr.Markdown("")
            latex_out = gr.Code(label=STRINGS["latex_label"],
                                language="latex")
            tex_file = gr.File(label=STRINGS["download_label"])
            btn_r.click(report_cb,
                        inputs=[matrix, symmetry, variant, title_box,
                                rank_tol, psd_tol, rank1_tol],
                        outputs=[latex_out, tex_file, report_status])

        with gr.Tab(STRINGS["tab_lorentz"]):
            gr.Markdown(STRINGS["lorentz_help"])
            lor_kind = gr.Radio(choices=["boost", "rotation"],
                                value="boost",
                                label=STRINGS["lorentz_kind_label"])
            lor_angle = gr.Number(value=0.5,
                                  label=STRINGS["lorentz_angle_label"])
            gr.Markdown(STRINGS["lorentz_axis_help"])
            with gr.Row():
                lor_nx = gr.Number(value=1.0, label="nx")
                lor_ny = gr.Number(value=0.0, label="ny")
                lor_nz = gr.Number(value=0.0, label="nz")
            btn_lor = gr.Button(STRINGS["btn_lorentz"], variant="primary")
            lor_alpha = gr.Markdown(label=STRINGS["lorentz_alpha_label"])
            lor_matrix = gr.Dataframe(label=STRINGS["lorentz_matrix_label"],
                                      interactive=False, type="array")
            lor_badge = gr.Markdown(label=STRINGS["lorentz_badge_label"])
            btn_lor.click(lorentz_cb,
                          inputs=[lor_kind, lor_angle,
                                  lor_nx, lor_ny, lor_nz],
                          outputs=[lor_alpha, lor_matrix, lor_badge])

        gr.Markdown(STRINGS["footer"])
    return app


def launch_kwargs(port: int = DEFAULT_PORT,
                  open_browser: bool = True) -> dict:
    """The exact kwargs passed to Blocks.launch. Security-relevant values
    are NOT parameters — 127.0.0.1 and share=False are constants. Every
    key here must exist in gradio-6 Blocks.launch (regression-tested
    against the real signature: an unknown key would crash organon-ui at
    startup, which injected-launch tests alone cannot catch)."""
    return {
        "server_name": HOST,
        "server_port": port,
        "share": SHARE,
        "inbrowser": open_browser,
        "quiet": True,
    }


def main(argv=None, _launch=None):
    """Console entry point (``organon-ui``). ``_launch(app, kwargs)`` is
    injectable for tests; the default launches Gradio."""
    parser = argparse.ArgumentParser(
        prog="organon-ui",
        description="Local web interface for organon-mueller "
                    "(binds to 127.0.0.1 only; nothing is uploaded).")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--no-browser", action="store_true",
                        help="do not open a browser tab automatically")
    args = parser.parse_args(argv)

    try:
        app = build_app()
    except ImportError as exc:
        # The console script is installed even WITHOUT the ui extra (user
        # field report, 2026-07-16): a bare ModuleNotFoundError traceback
        # here would violate K26 — one readable line instead.
        if getattr(exc, "name", None) == "gradio":
            raise SystemExit(
                "organon-ui: the web-interface extra is not installed.\n"
                'Fix:  pip install "organon-mueller[ui]"') from None
        raise
    kwargs = launch_kwargs(port=args.port, open_browser=not args.no_browser)
    if _launch is not None:
        return _launch(app, kwargs)
    app.launch(**kwargs)


if __name__ == "__main__":
    main()
