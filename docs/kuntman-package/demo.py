"""Feedback-package demo shim.

The canonical, general demo lives at ``examples/demo.py`` (same content:
the AO2016 Section-6 example, rank-3 recovery, the hypothesis bridge, and
the coupled-dipole engine). This shim keeps the feedback package
self-contained: ``python docs/kuntman-package/demo.py`` still runs it.
"""
import importlib.util
import pathlib

_CANONICAL = (pathlib.Path(__file__).resolve().parents[2]
              / "examples" / "demo.py")
_spec = importlib.util.spec_from_file_location("organon_examples_demo",
                                               _CANONICAL)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

main = _mod.main            # smoke-tested entry point (returns the dict)

if __name__ == "__main__":
    _mod._cli()
