"""Local web interface (milestone UI-1).

A thin Gradio layer over the hardened numeric-only tool functions
(``mcp_server/tools.py``). Binds to 127.0.0.1 only; ``share=False`` is
hard-coded — nothing is hosted or exposed (Stage 18 posture). Requires
the ``ui`` extra: ``pip install "organon-mueller[ui]"``.
"""
