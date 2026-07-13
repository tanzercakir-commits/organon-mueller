"""Stage-3 benchmark: pipeline v1.1 across enumeration modes and sizes.

Run:  python spikes/bench_stage3.py
Numbers land in reports/stage-03-REPORT.md (rule K15: always with an
environment note — timings are machine-dependent).
"""
from __future__ import annotations

import time

from organon_mueller.discovery.engine import DiscoveryEngine

CONFIGS = [
    # (atoms, conj_normal, max_size, certify)
    (("a", "b"), False, 7, "none"),   # v0's full-run configuration
    (("a", "b"), True, 7, "none"),
    (("a", "b"), True, 7, "all"),     # stage-4 symbolic certification cost
    (("a", "b"), True, 9, "underivable"),
    (("a", "b", "c"), True, 7, "underivable"),  # stage-4 3-atom scaling
    (("a", "b", "c"), True, 8, "underivable"),
]


def main() -> None:
    print(f"{'atoms':>5s} {'mode':7s} {'size':>4s} {'certify':>11s} {'terms':>6s} "
          f"{'buckets':>7s} {'verified':>8s} {'underiv':>7s} {'demoted':>7s} "
          f"{'refuted':>7s} {'fpcoll':>6s} {'total_s':>8s}")
    for atoms, conj_normal, max_size, certify in CONFIGS:
        start = time.perf_counter()
        result = DiscoveryEngine(
            atom_names=atoms, max_size=max_size,
            conj_normal=conj_normal, certify=certify,
        ).run()
        total = time.perf_counter() - start
        print(
            f"{len(atoms):5d} {'pruned' if conj_normal else 'full':7s} {max_size:4d} "
            f"{certify:>11s} {result.n_terms:6d} {result.n_buckets:7d} "
            f"{len(result.verified):8d} {len(result.underivable):7d} "
            f"{len(result.demoted_by_symbolic):7d} "
            f"{len(result.refuted):7d} {result.fingerprint_collisions:6d} {total:8.2f}"
        )


if __name__ == "__main__":
    main()
