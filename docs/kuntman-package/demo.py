"""Runnable demo for feedback window #1 (Kuntman-Arteaga group).

Three self-contained demonstrations:
  1. the AO2016 Section-6 example, decomposed by the DERIVED equations
  2. a rank-3 synthetic three-term mixture, recovered exactly (candidate
     zone -- no physics claim)
  3. the hypothesis bridge: every symmetry hypothesis attempted, ordered
     by a cheap structure score, failures carrying their reasons

Run:  python docs/kuntman-package/demo.py
"""
import numpy as np

# AO2016 Section 6 (print precision) ------------------------------------
M1_PAPER = np.array(
    [[1, 0, 0, 0.1489], [0, 0.9108, 0.3851, 0],
     [0, -0.3851, 0.9108, 0], [0.1489, 0, 0, 1]]
)
M2_PAPER = np.array(
    [[1, 0.0544, 0.6124, 0.2719], [0.2502, 0.7064, 0.2447, 0.2273],
     [0.6124, -0.2146, 0.8118, 0.4669], [-0.1196, -0.0768, -0.4519, 0.5935]]
)


def demo_section6() -> dict:
    from organon_mueller.decomposition import decompose

    mix = 0.3 * M1_PAPER + 0.7 * M2_PAPER
    # variant pinned to "a": on this example the auto (denominator-health)
    # mode picks 3b, which is numerically healthy but ~3e-4 less accurate
    # on 4-decimal print data — a nice in-repo example of health != accuracy
    r = decompose(mueller=mix, symmetry="type3", variant="a",
                  rank_tol=1e-4, psd_tol=1e-3, rank1_tol=1e-2)
    return {
        "alpha1": r.alpha1,
        "alpha1_paper": 0.3,
        "m1_max_err": float(np.max(np.abs(r.m1 - M1_PAPER))),
        "m2_max_err": float(np.max(np.abs(r.m2 - M2_PAPER))),
    }


def demo_rank3() -> dict:
    from organon_mueller.decomposition.rank3 import (
        PAIR_13, _template_numeric, decompose_rank3,
    )

    rng = np.random.default_rng(20260713)
    x = float(rng.uniform(0.15, 0.85))
    w1 = np.sqrt(x * (1 - x)) * np.exp(1j * float(rng.uniform(0, 2 * np.pi)))
    h_a = _template_numeric("type1", x, w1)
    e = float(rng.uniform(0.15, 0.35))
    v = np.sqrt(e * (0.5 - e)) * np.exp(1j * float(rng.uniform(0, 2 * np.pi)))
    h_b = _template_numeric("type3", e, v)
    u = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    u /= np.linalg.norm(u)
    h_g = np.outer(u, u.conj())
    alphas = (0.3, 0.35, 0.35)
    cov = sum(a * h for a, h in zip(alphas, (h_a, h_b, h_g)))

    r = decompose_rank3(cov, PAIR_13)
    return {
        "alphas_true": alphas,
        "alphas_recovered": tuple(float(a) for a in r.alphas),
        "component_max_err": float(max(
            np.max(np.abs(r.h_components[i] - h))
            for i, h in enumerate((h_a, h_b, h_g)))),
    }


def demo_bridge() -> dict:
    from organon_mueller.decomposition.rank3 import (
        PAIR_12, _template_numeric, propose_decompositions,
    )

    rng = np.random.default_rng(424242)
    x = float(rng.uniform(0.15, 0.85))
    w1 = np.sqrt(x * (1 - x)) * np.exp(1j * float(rng.uniform(0, 2 * np.pi)))
    h_a = _template_numeric("type1", x, w1)
    k = float(rng.uniform(0.15, 0.35))
    n = np.sqrt(k * (0.5 - k)) * np.exp(1j * float(rng.uniform(0, 2 * np.pi)))
    h_b = _template_numeric("type2", k, n)
    u = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    u /= np.linalg.norm(u)
    cov = 0.3 * h_a + 0.35 * h_b + 0.35 * np.outer(u, u.conj())

    report = propose_decompositions(cov)
    return {
        "rank": report.rank,
        "successes": [label for label, _ in report.successes],
        "scores": {k_: float(v) for k_, v in (report.scores or {}).items()},
        "failures": {label: reason[:100] for label, reason in report.failures},
    }


def main() -> dict:
    return {
        "section6": demo_section6(),
        "rank3_candidate_zone": demo_rank3(),
        "bridge": demo_bridge(),
    }


if __name__ == "__main__":
    results = main()

    s6 = results["section6"]
    print("=" * 72)
    print("1) AO2016 Section 6 (DERIVED equations, not transcribed)")
    print(f"   alpha1 = {s6['alpha1']:.4f}   (paper: {s6['alpha1_paper']})")
    print(f"   |M1 - paper| = {s6['m1_max_err']:.2e}   "
          f"|M2 - paper| = {s6['m2_max_err']:.2e}  (4-decimal print noise)")

    r3 = results["rank3_candidate_zone"]
    print("=" * 72)
    print("2) rank-3 three-term mixture (CANDIDATE zone -- no claims)")
    print(f"   true alphas      = {tuple(round(a, 6) for a in r3['alphas_true'])}")
    print(f"   recovered alphas = "
          f"{tuple(round(a, 6) for a in r3['alphas_recovered'])}")
    print(f"   worst component error = {r3['component_max_err']:.2e}")

    br = results["bridge"]
    print("=" * 72)
    print("3) hypothesis bridge (score-ordered; failures carry reasons)")
    print("   score = min |guard denominator| on the data: a numerical-")
    print("   health ORDERING heuristic only — acceptance is decided by")
    print("   the exact solvers (a rejected hypothesis may outscore an")
    print("   accepted one, as below)")
    print(f"   rank = {br['rank']}; accepted hypotheses: {br['successes']}")
    for label, score in sorted(br["scores"].items(),
                               key=lambda kv: -kv[1]):
        mark = "ACCEPTED" if label in br["successes"] else "rejected"
        print(f"   {label:14s} score={score:9.3e}  {mark}")
    print("=" * 72)
    print("Interpretation of any of the above is deliberately left to the")
    print("group (novelty protocol step 5 is human); see README-en.md.")
