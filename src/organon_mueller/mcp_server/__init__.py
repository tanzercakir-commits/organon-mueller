"""MCP surface (stage 17). Pure tool functions live in `tools` (testable
without the SDK); `server` wires them to FastMCP. NOT hosted anywhere by
default — running/exposing it is the user's decision (critical-decision
protocol)."""
from .tools import (
    tool_decompose_mueller,
    tool_generate_report,
    tool_guarded_campaign_info,
    tool_propose_hypotheses,
)

__all__ = [
    "tool_decompose_mueller",
    "tool_propose_hypotheses",
    "tool_guarded_campaign_info",
    "tool_generate_report",
]
