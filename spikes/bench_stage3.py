"""Stage-3 benchmark: pipeline v1.1 across enumeration modes and sizes.

Run:  python spikes/bench_stage3.py
Numbers land in reports/stage-03-REPORT.md (rule K15: always with an
environment note — timings are machine-dependent).
"""
from __future__ import annotations

import time

from organon_mueller.discovery.engine import DiscoveryEngine

CONFIGS = [
    (False, 7),   # v0's full-run configuration, for comparison
    (True, 7),
    (True, 9),
]


def main() -> None:
    print(f"{'mode':7s} {'size':>4s} {'terms':>6s} {'buckets':>7s} "
          f"{'verified':>8s} {'underiv':>7s} {'refuted':>7s} {'fpcoll':>6s} "
          f"{'harvest_s':>9s} {'total_s':>8s}")
    for conj_normal, max_size in CONFIGS:
        start = time.perf_counter()
        result = DiscoveryEngine(
            atom_names=("a", "b"), max_size=max_size, conj_normal=conj_normal
        ).run()
        total = time.perf_counter() - start
        print(
            f"{'pruned' if conj_normal else 'full':7s} {max_size:4d} "
            f"{result.n_terms:6d} {result.n_buckets:7d} "
            f"{len(result.verified):8d} {len(result.underivable):7d} "
            f"{len(result.refuted):7d} {result.fingerprint_collisions:6d} "
            f"{result.harvest_seconds:9.2f} {total:8.2f}"
        )


if __name__ == "__main__":
    main()
