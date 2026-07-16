"""Runnable demonstration of the engine's main capabilities.

Three self-contained demonstrations:
  1. the AO2016 Section-6 example, decomposed by the DERIVED equations
  2. a rank-3 synthetic three-term mixture, recovered exactly (candidate
     zone -- no physics claim)
  3. the hypothesis bridge: every symmetry hypothesis attempted, ordered
     by a cheap structure score, failures carrying their reasons

Run:  python examples/demo.py
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


def demo_dipoles() -> dict:
    """Section 4 (addendum): coupled-dipole engine — PRB decomposition
    equality (numeric, seeded), the forward gamma map, and the ensemble
    triple (chiral/achiral/uncoupled)."""
    from organon_mueller.dipoles.dimer import (
        scattering_matrix_decomposed, scattering_matrix_direct,
    )
    from organon_mueller.dipoles.ensemble import ensemble_gamma
    from organon_mueller.dipoles.general import forward_gamma_general
    import sympy as sp

    rng = np.random.default_rng(20260713)
    phi1, phi2 = rng.uniform(0, 2 * np.pi, 2)
    a1, a2, d1, d2 = (complex(x, y) * 0.3 for x, y in
                      rng.standard_normal((4, 2)))
    # genuinely the DIRECT coupled 4x4 solve vs the three-term form
    # (the full symbolic theorem lives in tests/test_dipoles.py)
    direct = scattering_matrix_direct(
        sp.Float(phi1), sp.Float(phi2), a1, a2, d1, d2)
    dec = scattering_matrix_decomposed(
        sp.Float(phi1), sp.Float(phi2), a1, a2, d1, d2)
    decomposition_err = float(np.max(np.abs(
        np.array(sp.matrix2numpy((direct - dec).evalf(), dtype=complex)))))

    # gamma map (stage-13 theorem): co-planar e2 = 1 is gamma-blind,
    # out-of-plane e2 != 1 is not
    args = (0.7, 0.4, 0.3, a1, a2, d1, d2, sp.exp(sp.I * 0.8))
    gamma_coplanar = complex(forward_gamma_general(*args, 1).evalf())
    gamma_offplane = complex(forward_gamma_general(
        *args, sp.exp(sp.I * 0.5)).evalf())

    chiral = ensemble_gamma(chiral=True, n_samples=400)
    achiral = ensemble_gamma(chiral=False, n_samples=400)
    uncoupled = ensemble_gamma(chiral=True, n_samples=50,
                               a_coef=0.0, b_coef=0.0)
    return {
        "decomposition_eq25_err": decomposition_err,
        "gamma_map": {"coplanar": abs(gamma_coplanar),
                      "offplane": abs(gamma_offplane)},
        "ensemble": {
            "chiral_mean_abs": abs(chiral["mean_gamma"]),
            "achiral_mean_abs": abs(achiral["mean_gamma"]),
            "uncoupled_pointwise": uncoupled["mean_abs_gamma"],
        },
    }


def main() -> dict:
    return {
        "section6": demo_section6(),
        "rank3_candidate_zone": demo_rank3(),
        "bridge": demo_bridge(),
        "dipoles": demo_dipoles(),
    }


def _cli() -> None:
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
    dp = results["dipoles"]
    print("=" * 72)
    print("4) coupled-dipole engine (addendum; PRB 98,045410 + ensemble)")
    print(f"   Eq. 25: direct 4x4 coupled solve vs three-term form: "
          f"{dp['decomposition_eq25_err']:.2e}")
    gm = dp["gamma_map"]
    print(f"   gamma map: co-planar |gamma| = {gm['coplanar']:.1e} (blind), "
          f"out-of-plane |gamma| = {gm['offplane']:.3e}")
    en = dp["ensemble"]
    print(f"   ensemble |mean gamma_z|: chiral+coupled {en['chiral_mean_abs']:.3e}"
          f"  achiral {en['achiral_mean_abs']:.3e}"
          f"  uncoupled(pointwise) {en['uncoupled_pointwise']:.1e}")
    print("=" * 72)
    print("Interpretation of any of the above is deliberately left to")
    print("domain experts (novelty protocol step 5 is human); see")
    print("docs/novelty-protocol.md and docs/candidate-findings.md.")


if __name__ == "__main__":
    _cli()
