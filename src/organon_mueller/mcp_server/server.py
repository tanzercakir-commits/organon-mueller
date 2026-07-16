"""FastMCP wiring (optional extra `mcp`). Run: python -m
organon_mueller.mcp_server  — stdio transport only; NOT hosted anywhere
by default (exposing it is the user's critical decision)."""
from __future__ import annotations

from .tools import (
    tool_decompose_mueller,
    tool_generate_report,
    tool_guarded_campaign_info,
    tool_propose_hypotheses,
)


def build_server():
    """Construct the FastMCP app (import-guarded; smoke-tested without
    running the transport)."""
    from mcp.server.fastmcp import FastMCP

    app = FastMCP(
        "organon-mueller",
        instructions="Stokes-Mueller polarization algebra tools "
                     "(covariance-vector formalism). Numeric inputs only; "
                     "results carry evidence labels and reasons.")

    @app.tool()
    def decompose_mueller(mueller: list, symmetry: str = "type1",
                          variant: str = "auto") -> dict:
        """Two-term symmetric decomposition of a real 4x4 Mueller matrix
        (symmetry: type1|type2|type3|type1-2|type1-3|type2-3)."""
        return tool_decompose_mueller(
            {"mueller": mueller, "symmetry": symmetry, "variant": variant})

    @app.tool()
    def propose_hypotheses(mueller: list | None = None,
                           covariance: list | None = None) -> dict:
        """Try every symmetry hypothesis the rank admits; failures carry
        reasons. covariance entries are [re, im] pairs."""
        payload = {}
        if mueller is not None:
            payload["mueller"] = mueller
        if covariance is not None:
            payload["covariance"] = covariance
        return tool_propose_hypotheses(payload)

    @app.tool()
    def guarded_campaign_info() -> dict:
        """Current guarded-discovery findings (M32 evidence quadruples;
        candidates only, no novelty claims)."""
        return tool_guarded_campaign_info()

    @app.tool()
    def generate_report(mueller: list, symmetry: str = "type1",
                        title: str = "organon-mueller report",
                        date: str = "", compile_pdf: bool = False) -> dict:
        """LaTeX report for a decomposition (evidence-labeled blocks;
        deterministic; optional local PDF compile)."""
        return tool_generate_report(
            {"mueller": mueller, "symmetry": symmetry, "title": title,
             "date": date, "compile_pdf": compile_pdf})

    return app


def main():
    build_server().run()   # stdio


if __name__ == "__main__":
    main()
