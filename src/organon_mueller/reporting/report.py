"""Deterministic LaTeX report builder (stage 16).

Evidence-class discipline (stage-15 lesson institutionalized): every
block carries an evidence label tied to the VERIFICATION.md layers, and
the template VERBS follow the label — "proven" appears only under
`symbolic-proof`; `numeric-deterministic` says "verified numerically";
`candidate` makes NO claim and carries the novelty-protocol footnote.

Determinism contract (tested): identical inputs produce byte-identical
LaTeX; no \\today, no timestamps (dates are explicit parameters); floats
rounded to a fixed precision, with sub-threshold magnitudes falling back
to deterministic scientific notation (never printed as an exact 0).

Security (STAGE-2 GATE alignment, ahead of the A17 MCP surface): this
module only WRITES LaTeX from the library's own result objects — it
never sympifies external input; free text is LaTeX-escaped; pdflatex is
invoked with -no-shell-escape.
"""
from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

__all__ = [
    "EVIDENCE_LABELS",
    "Report",
    "ReportBlock",
    "decomposition_section",
    "propose_section",
    "guarded_finding_section",
    "dipole_section",
    "compile_pdf",
    "build_demo_report",
]

#: evidence label -> (VERIFICATION.md anchor, verb phrase used in text)
EVIDENCE_LABELS = {
    "symbolic-proof": ("layer 1 (exact symbolic)", "proven symbolically"),
    "numeric-deterministic": ("layer 2 (seeded numeric)",
                              "verified numerically (deterministic seeds)"),
    "candidate": ("novelty channel (no claim)",
                  "reported as a CANDIDATE (no novelty or physics claim)"),
}

_PRECISION = 6

_ESCAPES = {
    "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
    "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
}


def latex_escape(text: str) -> str:
    """Escape free text for LaTeX (titles, failure reasons, ...)."""
    return "".join(_ESCAPES.get(ch, ch) for ch in str(text))


def _sci(v: float) -> str:
    """Deterministic scientific notation for sub-threshold magnitudes
    (review D1: a machine-precision residual must NEVER print as an
    exactness claim — 6.7e-16 is not 0)."""
    mant, exp = f"{v:.1e}".split("e")
    # \ensuremath: valid in BOTH text cells (tabular) and math contexts
    return f"\\ensuremath{{{mant} \\times 10^{{{int(exp)}}}}}"


def _fmt_real(v: float) -> str:
    if v != v or v in (float("inf"), float("-inf")):
        raise ValueError(f"non-finite value in report: {v} (K26)")
    if v != 0 and abs(v) < 10 ** (-_PRECISION):
        return _sci(v)
    r = round(v, _PRECISION)
    r = 0.0 if r == 0 else r  # normalize -0.0
    return f"{r:.{_PRECISION}f}".rstrip("0").rstrip(".") or "0"


def _fmt(x) -> str:
    """Deterministic scalar formatting; sub-1e-6 magnitudes fall back to
    scientific notation (evidence honesty); non-finite raises."""
    c = complex(x)
    if c.imag == 0 or (abs(c.imag) < 10 ** (-_PRECISION)
                       and abs(c.real) >= 10 ** (-_PRECISION)):
        # drop numerically-negligible imag ONLY next to a normal real
        return _fmt_real(c.real)
    re_s, im_s = _fmt_real(c.real), _fmt_real(abs(c.imag))
    sign = "+" if c.imag > 0 else "-"
    return f"\\ensuremath{{{re_s} {sign} {im_s}\\,\\mathrm{{i}}}}"


def _matrix_latex(m) -> str:
    m = np.asarray(m)
    rows = [" & ".join(_fmt(v) for v in row) for row in m]
    body = " \\\\\n".join(rows)
    return "\\begin{pmatrix}\n" + body + "\n\\end{pmatrix}"


@dataclass(frozen=True)
class ReportBlock:
    title: str
    evidence: str                    # key of EVIDENCE_LABELS
    source: str                      # paper reference (free text)
    body: str                        # LaTeX body (already escaped/valid)
    reproduction: str = ""           # seeds etc. (free text)

    def __post_init__(self):
        if self.evidence not in EVIDENCE_LABELS:
            raise ValueError(
                f"unknown evidence label {self.evidence!r}; allowed: "
                f"{sorted(EVIDENCE_LABELS)} (labels are TIED to "
                "VERIFICATION.md layers — no free-form claims)")

    def to_latex(self) -> str:
        anchor, verb = EVIDENCE_LABELS[self.evidence]
        lines = [
            f"\\subsection*{{{latex_escape(self.title)}}}",
            f"\\textit{{Evidence: {latex_escape(self.evidence)} "
            f"({latex_escape(anchor)}) --- {latex_escape(verb)}.}}\\\\",
            f"\\textit{{Source: {latex_escape(self.source)}}}\\\\",
        ]
        if self.reproduction:
            lines.append(
                f"\\textit{{Reproduction: {latex_escape(self.reproduction)}}}\\\\")
        lines.append(self.body)
        return "\n".join(lines)


_PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[margin=2.5cm]{geometry}
\usepackage{amsmath,amssymb}
\usepackage[T1]{fontenc}
\setcounter{secnumdepth}{0}
"""

_FOOTNOTE = (
    "\\vspace{1em}\\noindent\\rule{\\linewidth}{0.4pt}\\\\"
    "\\textit{Rounding convention: values are rounded to 6 decimals; "
    "magnitudes below $10^{-6}$ are shown in scientific notation --- a "
    "printed small number is a measured residual, never an exactness "
    "claim.}\\\\"
    "\\textit{Interpretation boundary: whether any result above is "
    "physically interesting or new is deliberately NOT claimed here --- "
    "that judgement is reserved for human experts (novelty protocol, "
    "final step). Verification layers: see docs/VERIFICATION.md.}"
)


@dataclass
class Report:
    title: str
    date: str = ""                   # EXPLICIT; never \today (determinism)
    blocks: list = field(default_factory=list)

    def add(self, block: ReportBlock) -> "Report":
        self.blocks.append(block)
        return self

    def to_latex(self) -> str:
        head = [_PREAMBLE,
                f"\\title{{{latex_escape(self.title)}}}",
                f"\\date{{{latex_escape(self.date)}}}",
                "\\author{organon-mueller (automated report)}",
                "\\begin{document}\\maketitle"]
        body = [b.to_latex() for b in self.blocks]
        return "\n".join(head + body + [_FOOTNOTE, "\\end{document}"]) + "\n"


# ---------------------------------------------------------------- sections

def decomposition_section(result, title: str | None = None) -> ReportBlock:
    """Fundamental / composite / rank-3 decomposition results. All are
    NUMERIC solver outputs -> evidence is numeric-deterministic (the
    underlying equation DERIVATIONS are symbolically proven in the test
    suite; the numbers here are solver evaluations)."""
    cls = type(result).__name__
    if cls == "DecompositionResult":
        label = f"two-term, symmetry {result.symmetry} (variant {result.variant})"
        alphas = [("\\alpha_1", result.alpha1), ("\\alpha_2", 1 - result.alpha1)]
        mats = [("M_1", result.m1), ("M_2", result.m2)]
        src = "Kuntman & Arteaga, Appl. Opt. 55, 2543 (2016), Tables 1-2"
    elif cls == "CompositeResult":
        label = f"two-term, composite symmetry {result.symmetry}"
        alphas = [("\\alpha_1", result.alpha1), ("\\alpha_2", 1 - result.alpha1)]
        mats = [("M_1", result.m1), ("M_2", result.m2)]
        src = "Kuntman & Arteaga, Appl. Opt. 55, 2543 (2016), Tables 3-4"
    elif cls == "Rank3Result":
        label = f"three-term, pair {'+'.join(result.pair)}"
        alphas = list(zip(("\\alpha_A", "\\alpha_B", "\\alpha_G"),
                          result.alphas))
        mats = [(f"M_{i+1}", m) for i, m in enumerate(result.m_components)]
        src = ("beyond-paper zone (M34 framework); "
               "cf. Appl. Opt. 55, 2543 (2016)")
    else:
        raise ValueError(f"unsupported result type: {cls}")

    parts = [f"Decomposition: {latex_escape(label)}.\\\\",
             "Weights: " + ", ".join(
                 f"${nm} = {_fmt(v)}$" for nm, v in alphas)  # nm: our own
             + ".\\\\"]                                      # math literals
    for nm, m in mats:
        parts.append(f"\\[ {nm} = {_matrix_latex(m)} \\]")
    if cls == "Rank3Result":
        if result.consistency_residual is not None:
            parts.append(
                f"Consistency residual (K32): "
                f"${_fmt(result.consistency_residual)}$.")
        parts.append(
            "\\textit{Note: a rank-3 result is A decomposition consistent "
            "with the requested pair, not THE decomposition (verified "
            "non-uniqueness across pair hypotheses).}")
    return ReportBlock(
        title=title or f"Decomposition ({label})",
        evidence="numeric-deterministic",
        source=src,
        body="\n".join(parts),
        reproduction="deterministic solver; tolerances as passed at the "
                     "call site (not recorded in result objects)",
    )


def propose_section(report, title: str = "Hypothesis map") -> ReportBlock:
    """ProposeReport -> score-ordered outcome table (K21: failures carry
    reasons; scores order, never eliminate)."""
    rows = []
    scores = report.scores or {}
    succ = {label for label, _ in report.successes}
    for label, _ in report.successes:
        rows.append((label, scores.get(label), "accepted", ""))
    for label, reason in report.failures:
        rows.append((label, scores.get(label), "rejected", reason))
    rows.sort(key=lambda r: (-(r[1] if r[1] is not None else -1), r[0]))
    lines = ["\\begin{tabular}{llll}",
             "hypothesis & score & outcome & reason \\\\ \\hline"]
    for label, score, outcome, reason in rows:
        s = _fmt(score) if score is not None else "--"
        lines.append(f"{latex_escape(label)} & {s} & {outcome} & "
                     f"{latex_escape(reason[:90])} \\\\")
    lines.append("\\end{tabular}\\\\")
    lines.append("\\textit{Scores are a denominator-health ORDERING "
                 "heuristic, not evidence; acceptance is decided solely "
                 "by the exact solvers. Every hypothesis the rank admits "
                 "was attempted.}")
    return ReportBlock(
        title=f"{title} (rank {report.rank}; "
              f"{len(succ)} accepted / {len(report.failures)} rejected)",
        evidence="numeric-deterministic",
        source="bridge v1 (stage 10-11); AO2016 numerical-health advice",
        body="\n".join(lines),
    )


def guarded_finding_section(finding, title: str | None = None) -> ReportBlock:
    """GuardedFinding -> the M32 four-part evidence table; candidate
    language, no claim."""
    guards = ", ".join(f"{k}:{v}" for k, v in sorted(finding.guards.items()))
    yn = lambda b: "yes" if b else "no"  # noqa: E731
    rows = [
        ("exact symbolic under guard", yn(finding.symbolic_guarded)),
        ("numeric under guard (seeded)", yn(finding.numeric_guarded)),
        ("derivable WITHOUT guard (e-graph)", yn(finding.provable_unguarded)),
        ("symbolically true WITHOUT guard", yn(finding.symbolic_unguarded)),
    ]
    lines = [
        f"Pair: ${latex_escape(finding.left.render())} \\equiv "
        f"{latex_escape(finding.right.render())}$ under guards "
        f"\\texttt{{{latex_escape(guards)}}}.\\\\",
        "\\begin{tabular}{ll}", "check & result \\\\ \\hline"]
    lines += [f"{latex_escape(k)} & {v} \\\\" for k, v in rows]
    lines.append("\\end{tabular}\\\\")
    verdict = ("conditional identity (Horn form: guards imply equality; "
               "false without the guards)"
               if finding.is_conditional_identity else
               "NOT a conditional identity under the M32 criteria")
    lines.append(f"M32 verdict: {latex_escape(verdict)}.")
    return ReportBlock(
        title=title or "Guarded (Horn-conditional) finding",
        evidence="candidate",
        source="discovery engine, guarded campaign (M32); "
               "JOSA A 34, 80 (2017) term language",
        body="\n".join(lines),
        reproduction="numeric seed 20260713 (3 draws); engine isolated "
                     "pair-proof graphs (M18)",
    )


def dipole_section(gamma_map: dict, ensemble: dict,
                   title: str = "Coupled-dipole optical activity") -> ReportBlock:
    """gamma-map values + ensemble statistics (from demo/ensemble_gamma
    outputs)."""
    lines = [
        "Forward-scattering gamma map (theorem: "
        "$h_4 = i e_1 \\alpha_1 \\alpha_2 \\Delta_1 (1 - e_2^2)/(2N)$):\\\\",
        f"co-planar ($e_2 = 1$): $|\\gamma| = {_fmt(gamma_map['coplanar'])}$ "
        "(gamma-blind); ",
        f"out-of-plane: $|\\gamma| = {_fmt(gamma_map['offplane'])}$.\\\\",
        "Ensemble statistics over random rigid orthogonal dimers:\\\\",
        "\\begin{tabular}{lll}",
        "configuration & statistic & value \\\\ \\hline",
        f"chiral, coupled & $|\\overline{{\\gamma_z}}|$ & "
        f"{_fmt(ensemble['chiral_mean_abs'])} \\\\",
        f"achiral, coupled & $|\\overline{{\\gamma_z}}|$ & "
        f"{_fmt(ensemble['achiral_mean_abs'])} \\\\",
        f"chiral, uncoupled & $\\overline{{|\\gamma_z|}}$ (pointwise) & "
        f"{_fmt(ensemble['uncoupled_pointwise'])} \\\\",
        "\\end{tabular}",
    ]
    return ReportBlock(
        title=title,
        evidence="numeric-deterministic",
        source="PRB 98, 045410 (2018); Symmetry 12, 1790 (2020); "
               "OA-in-ensemble preprint",
        body="\n".join(lines),
        reproduction="seed 20260713; deterministic orientation sampling",
    )


# ---------------------------------------------------------------- pdf

def compile_pdf(tex_path, out_dir=None) -> Path:
    """Compile with pdflatex (nonstopmode, -no-shell-escape). Raises with
    the log tail on failure. Requires pdflatex on PATH."""
    tex_path = Path(tex_path)
    out_dir = Path(out_dir) if out_dir else tex_path.parent
    if shutil.which("pdflatex") is None:
        raise RuntimeError("pdflatex not found on PATH")
    proc = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-no-shell-escape",
         "-output-directory", str(out_dir), str(tex_path)],
        capture_output=True, text=True, timeout=120,
        encoding="utf-8", errors="replace")   # log bytes must never crash us
    pdf = out_dir / (tex_path.stem + ".pdf")
    if proc.returncode != 0 or not pdf.exists():
        tail = "\n".join(proc.stdout.splitlines()[-25:])
        raise RuntimeError(f"pdflatex failed (rc={proc.returncode}):\n{tail}")
    return pdf


# ---------------------------------------------------------------- scenario

def build_demo_report(results: dict | None = None,
                      date: str = "2026-07-14") -> Report:
    """First real scenario: the demo results as a report. Deterministic
    for a fixed `results` dict; if None, runs the canonical demo
    (examples/demo.py) to obtain them."""
    if results is None:
        import importlib.util

        demo_path = (Path(__file__).resolve().parents[3]
                     / "examples" / "demo.py")
        spec = importlib.util.spec_from_file_location("organon_demo",
                                                      demo_path)
        demo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(demo)
        results = demo.main()

    rep = Report(title="organon-mueller --- sample automated report",
                 date=date)
    s6 = results["section6"]
    body = (
        f"Recovered $\\alpha_1 = {_fmt(s6['alpha1'])}$ (paper: 0.3); "
        f"$\\max|M_1 - M_1^{{paper}}| = {_fmt(s6['m1_max_err'])}$, "
        f"$\\max|M_2 - M_2^{{paper}}| = {_fmt(s6['m2_max_err'])}$ "
        "(4-decimal print noise).")
    rep.add(ReportBlock(
        title="AO2016 Section-6 example (derived equations)",
        evidence="numeric-deterministic",
        source="Kuntman & Arteaga, Appl. Opt. 55, 2543 (2016), Sec. 6",
        body=body,
        reproduction="variant a pinned; loose tolerances for 4-decimal "
                     "print data"))
    r3 = results["rank3_candidate_zone"]
    rep.add(ReportBlock(
        title="Rank-3 three-term synthetic recovery",
        evidence="candidate",
        source="beyond-paper zone (M34); cf. AO2016",
        body=(f"True weights {tuple(round(a, 6) for a in r3['alphas_true'])} "
              f"recovered to "
              f"$\\max|\\Delta\\alpha| = {_fmt(max(abs(a - b) for a, b in zip(r3['alphas_true'], r3['alphas_recovered'])))}$; "
              f"worst component error ${_fmt(r3['component_max_err'])}$."),
        reproduction="seed 20260713"))
    dp = results["dipoles"]
    rep.add(dipole_section(dp["gamma_map"], dp["ensemble"]))
    return rep
