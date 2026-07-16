"""Pure MCP tool functions (stage 17) — SDK-independent, fully testable.

Security contract: inputs are NUMBERS and enum strings only — no
expression text ever crosses this boundary, so nothing here can reach
sympify (the restricted parser guards the serialization layer
independently; see safe_parse.py). All validation errors return
{"error": reason} (K26: reasons, never silent failure; no traceback
leakage)."""
from __future__ import annotations

import numpy as np

__all__ = [
    "tool_decompose_mueller",
    "tool_propose_hypotheses",
    "tool_guarded_campaign_info",
    "tool_generate_report",
]

_FUNDAMENTAL = ("type1", "type2", "type3")
_COMPOSITE = ("type1-2", "type1-3", "type2-3")


def _validate_real_matrix(m, name="matrix"):
    if not (isinstance(m, (list, tuple)) and len(m) == 4
            and all(isinstance(r, (list, tuple)) and len(r) == 4 for r in m)):
        raise ValueError(f"{name} must be a 4x4 nested list")
    out = np.empty((4, 4), dtype=float)
    for i, row in enumerate(m):
        for j, v in enumerate(row):
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                raise ValueError(
                    f"{name}[{i}][{j}] must be a real number, got "
                    f"{type(v).__name__}")
            out[i, j] = float(v)
    if not np.all(np.isfinite(out)):
        raise ValueError(f"{name} contains non-finite entries")
    return out


def _validate_complex_matrix(m, name="covariance"):
    """Entries are [re, im] pairs (JSON has no complex type)."""
    if not (isinstance(m, (list, tuple)) and len(m) == 4
            and all(isinstance(r, (list, tuple)) and len(r) == 4 for r in m)):
        raise ValueError(f"{name} must be a 4x4 nested list of [re, im] pairs")
    out = np.empty((4, 4), dtype=complex)
    for i, row in enumerate(m):
        for j, v in enumerate(row):
            if (not isinstance(v, (list, tuple)) or len(v) != 2
                    or any(isinstance(x, bool) or not isinstance(x, (int, float))
                           for x in v)):
                raise ValueError(
                    f"{name}[{i}][{j}] must be a [re, im] pair of numbers")
            out[i, j] = complex(float(v[0]), float(v[1]))
    if not (np.all(np.isfinite(out.real)) and np.all(np.isfinite(out.imag))):
        raise ValueError(f"{name} contains non-finite entries")
    return out


def _result_to_dict(r) -> dict:
    cls = type(r).__name__
    if cls in ("DecompositionResult", "CompositeResult"):
        return {
            "kind": cls, "symmetry": r.symmetry,
            "variant": getattr(r, "variant", None),
            "alpha1": float(r.alpha1),
            "m1": np.asarray(r.m1, dtype=float).round(9).tolist(),
            "m2": np.asarray(r.m2, dtype=float).round(9).tolist(),
        }
    if cls == "Rank3Result":
        return {
            "kind": cls, "pair": list(r.pair),
            "alphas": [float(a) for a in r.alphas],
            "m_components": [np.asarray(m, dtype=float).round(9).tolist()
                             for m in r.m_components],
            "consistency_residual": (None if r.consistency_residual is None
                                     else float(r.consistency_residual)),
            "note": "A decomposition consistent with the pair, not THE "
                    "decomposition (verified non-uniqueness)",
        }
    raise ValueError(f"unsupported result type {cls}")


def tool_decompose_mueller(payload: dict) -> dict:
    """Two-term symmetric decomposition of a REAL 4x4 Mueller matrix.

    payload: {"mueller": [[...4x4 floats...]], "symmetry": "type1"|...|
    "type2-3", optional "variant": "a"|"b"|"auto", optional tolerances}.
    """
    from ..decomposition import DecompositionError, decompose
    from ..decomposition.composite import decompose_composite
    from ..decomposition.covariance import standard_covariance_from_mueller
    import sympy as sp

    try:
        m = _validate_real_matrix(payload.get("mueller"), "mueller")
        symmetry = payload.get("symmetry", "type1")
        tols = {}
        for k in ("rank_tol", "psd_tol", "rank1_tol"):
            if k in payload:
                v = payload[k]
                if isinstance(v, bool) or not isinstance(v, (int, float)):
                    raise ValueError(f"{k} must be a real number in (0, 1)")
                if not (0 < v < 1):
                    raise ValueError(f"{k} must be in (0, 1)")
                tols[k] = float(v)
        if symmetry in _FUNDAMENTAL:
            variant = payload.get("variant", "auto")
            if variant not in ("a", "b", "auto"):
                raise ValueError("variant must be 'a', 'b' or 'auto'")
            r = decompose(mueller=m, symmetry=symmetry, variant=variant,
                          **tols)
        elif symmetry in _COMPOSITE:
            cov = np.array(sp.matrix2numpy(
                standard_covariance_from_mueller(sp.Matrix(m)).evalf(),
                dtype=complex))
            r = decompose_composite(cov, symmetry, **tols)
        else:
            raise ValueError(
                f"symmetry must be one of {_FUNDAMENTAL + _COMPOSITE}")
        return _result_to_dict(r)
    except (ValueError, DecompositionError,
            np.linalg.LinAlgError) as exc:
        # LinAlgError subclasses ValueError only on numpy >= 2.0; listed
        # explicitly so numpy 1.x solver failures also return a reason
        # (review UI-1, finding 6).
        return {"error": str(exc)}


def tool_propose_hypotheses(payload: dict) -> dict:
    """Try every symmetry hypothesis the rank admits (bridge v1).

    payload: {"covariance": [[[re, im] x4] x4]} OR {"mueller": 4x4 reals}.
    """
    from ..decomposition.covariance import standard_covariance_from_mueller
    from ..decomposition.rank3 import propose_decompositions
    import sympy as sp

    try:
        if "covariance" in payload:
            cov = _validate_complex_matrix(payload["covariance"])
        elif "mueller" in payload:
            m = _validate_real_matrix(payload["mueller"], "mueller")
            cov = np.array(sp.matrix2numpy(
                standard_covariance_from_mueller(sp.Matrix(m)).evalf(),
                dtype=complex))
        else:
            raise ValueError("provide 'covariance' ([re,im] pairs) or "
                             "'mueller' (reals)")
        rep = propose_decompositions(cov)
        return {
            "rank": rep.rank,
            "scores": {k: float(v) for k, v in (rep.scores or {}).items()},
            "accepted": [{"hypothesis": lb, **_result_to_dict(r)}
                         for lb, r in rep.successes],
            "rejected": [{"hypothesis": lb, "reason": reason}
                         for lb, reason in rep.failures],
            "note": "scores are an ordering heuristic, not evidence; "
                    "acceptance is decided solely by the exact solvers",
        }
    except (ValueError, np.linalg.LinAlgError) as exc:
        # LinAlgError listed for numpy 1.x — see the note in
        # tool_decompose_mueller (review UI-1, finding 6)
        return {"error": str(exc)}


def tool_guarded_campaign_info() -> dict:
    """Report the current guarded-campaign findings (M32 evidence
    quadruples). Requires the discovery extra (egglog)."""
    try:
        # egglog is imported lazily deep inside run_guarded_campaign
        # (engine.py at module load), so the ImportError can surface at
        # the CALL, not just this import — wrap both (MCP contract: return
        # a reason, never leak a traceback).
        from ..discovery.guards import run_guarded_campaign
        findings = run_guarded_campaign()
    except ImportError:
        return {"error": "discovery extra not installed (pip install "
                         "organon-mueller[discovery], Python >= 3.11)"}
    return {"findings": [
        {
            "left": f.left.render(), "right": f.right.render(),
            "guards": dict(sorted(f.guards.items())),
            "symbolic_guarded": f.symbolic_guarded,
            "numeric_guarded": f.numeric_guarded,
            "provable_unguarded": f.provable_unguarded,
            "symbolic_unguarded": f.symbolic_unguarded,
            "is_conditional_identity": f.is_conditional_identity,
        } for f in findings],
        "note": "candidates/known facts under the M32 criteria — no "
                "novelty claim (protocol step 5 is human)",
        "seed": 20260713}


def tool_generate_report(payload: dict) -> dict:
    """Build a LaTeX report from a decomposition request (runs
    tool_decompose_mueller internally, then renders). payload adds
    optional "title", "date", "compile_pdf": bool (default False), and the
    same optional tolerances as tool_decompose_mueller — validated
    identically (UI-1: print-precision data needs looser tolerances)."""
    from ..decomposition import DecompositionError, decompose
    from ..reporting import Report, compile_pdf, decomposition_section

    try:
        m = _validate_real_matrix(payload.get("mueller"), "mueller")
        symmetry = payload.get("symmetry", "type1")
        if symmetry not in _FUNDAMENTAL:
            raise ValueError(f"report tool supports {_FUNDAMENTAL} here; "
                             "use decompose_mueller for composites")
        variant = payload.get("variant", "auto")
        if variant not in ("a", "b", "auto"):
            raise ValueError("variant must be 'a', 'b' or 'auto'")
        tols = {}
        for k in ("rank_tol", "psd_tol", "rank1_tol"):
            if k in payload:
                v = payload[k]
                if isinstance(v, bool) or not isinstance(v, (int, float)):
                    raise ValueError(f"{k} must be a real number in (0, 1)")
                if not (0 < v < 1):
                    raise ValueError(f"{k} must be in (0, 1)")
                tols[k] = float(v)
        title = str(payload.get("title", "organon-mueller report"))[:200]
        date = str(payload.get("date", ""))[:40]
        r = decompose(mueller=m, symmetry=symmetry, variant=variant, **tols)
        rep = Report(title=title, date=date).add(decomposition_section(r))
        tex = rep.to_latex()
        out = {"latex": tex}
        if payload.get("compile_pdf"):
            import tempfile
            from pathlib import Path

            with tempfile.TemporaryDirectory() as td:
                p = Path(td) / "report.tex"
                p.write_text(tex)
                try:
                    pdf = compile_pdf(p, td)
                    out["pdf_bytes"] = pdf.stat().st_size
                    out["pdf_note"] = ("compiled OK (bytes reported; "
                                       "transfer channel is host-specific)")
                except RuntimeError as exc:
                    out["pdf_error"] = str(exc)[:300]
        return out
    except (ValueError, DecompositionError,
            np.linalg.LinAlgError) as exc:
        # LinAlgError subclasses ValueError only on numpy >= 2.0; listed
        # explicitly so numpy 1.x solver failures also return a reason
        # (review UI-1, finding 6).
        return {"error": str(exc)}
