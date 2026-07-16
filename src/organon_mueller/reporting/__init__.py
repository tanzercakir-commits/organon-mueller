"""LaTeX report generation (Phase E; user packaging vision: end users
cannot use terminals — reports are first-class output)."""
from .report import (
    EVIDENCE_LABELS,
    Report,
    ReportBlock,
    build_demo_report,
    compile_pdf,
    decomposition_section,
    dipole_section,
    guarded_finding_section,
    propose_section,
)

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
