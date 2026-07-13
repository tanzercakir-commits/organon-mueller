"""Rank-3 three-term decomposition (stage 10 — BEYOND the AO2016 tables):

    H = alpha_A * H_A  +  alpha_B * H_B  +  alpha_G * |u><u|

with H_A, H_B pure components of two DIFFERENT fundamental symmetry types
(Table 1) and |u><u| a generic pure. This zone has no paper table to
anchor against (M34): the derivations below were fixed by a
pre-implementation numeric probe (spec-10 section 0), the deriver must
reproduce those hand formulas symbolically, and the adversarial reviewer
re-derives independently. NO novelty/physics claim is made here — the
results are reported as candidates (novelty protocol, step 5 is human).

Mechanism (M33 — one-way layering, stage-8/9 machinery untouched):

* pairs {type1, type2} and {type1, type3} — SEQUENTIAL PEEL: type-1's
  support is only the four corners, so the other component's center
  parameter comes LINEARLY from the center minor of the rank-1 remainder
  and its edge parameter from an edge minor; subtract, rescale, and
  DELEGATE the corner-only residual to the stage-8 rank-2 solver (which
  contributes all of its own guards).
* pair {type2, type3} — COMBINATION VARIABLES: the supports overlap
  completely, but the sum T2+T3 is the 7-parameter Hermitian pattern in
  (sigma, p, m, s, d) = (k2+e3, w2+v3, w2-v3, kbar2+ebar3, kbar2-ebar3),
  and the corner/edge/center minors are LINEAR in these, solved in that
  order. Reconstruction recovers the individual parameters through the
  rank-1 relations, and the OVERDETERMINATION k2 + e3 = sigma becomes a
  mandatory consistency guard (K32): data that does not really have this
  structure is rejected, never silently patched. (Review census note: on
  random wrong data the REALNESS checks on s and d do most of the
  rejection work — each is one complex equation for one real unknown, so
  they are overdeterminations too; K32 catches the thinner stratum where
  s and d come out real anyway, e.g. all-real covariances.)

Guards (K26/K29/K31): every derived minor carries order-aware structural
guards (linear + conj-free in its target, untouched by not-yet-solved
symbols); the numeric path guards trace-1, rank==3, denominators
(missing-anisotropy conditions on the GENERIC pure — e.g. the corner
denominator is alpha_G*|u0-u3|^2), parameter domains, and PSD/rank-1 of
every recovered component.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np
import sympy as sp

from .covariance import (
    SYMMETRY_TEMPLATES,
    mueller_from_standard_covariance,
)
from .derive import generic_hermitian
from .solve import DecompositionError, decompose

__all__ = [
    "RANK3_PAIRS",
    "derive_rank3",
    "decompose_rank3",
    "Rank3Derived",
    "Rank3Result",
    "propose_decompositions",
    "ProposeReport",
    "sweep_rank3",
]

PAIR_12 = ("type1", "type2")
PAIR_13 = ("type1", "type3")
PAIR_23 = ("type2", "type3")
RANK3_PAIRS = (PAIR_12, PAIR_13, PAIR_23)

_TOL = 1e-9
_DENOM_TOL = 1e-8


def _minor(matrix: sp.Matrix, rows, cols) -> sp.Expr:
    return sp.expand(matrix.extract(list(rows), list(cols)).det())


def _forbid(expr: sp.Expr, probes, label: str, pair: str) -> None:
    """K31 structural guard: a minor touching a forbidden symbol raises."""
    for probe in probes:
        if expr.has(probe):
            raise ValueError(f"{pair}: {label} touches {probe} (K31)")


def _solve_unique(eq: sp.Expr, target: sp.Symbol, label: str, pair: str) -> sp.Expr:
    if sp.degree(sp.Poly(eq, target)) != 1:
        raise ValueError(f"{pair}: {label} not linear in {target} (K31)")
    sols = sp.solve(eq, target)
    if len(sols) != 1:
        raise ValueError(f"{pair}: {label} not uniquely solvable")
    return sp.simplify(sols[0])


@dataclass(frozen=True)
class Rank3Derived:
    pair: tuple[str, str]
    kind: str                      # "peel_delegate" | "combo"
    exprs: tuple                   # ordered (name, expr) pairs
    hermitian: sp.Matrix


@lru_cache(maxsize=None)
def derive_rank3(pair: tuple[str, str]) -> Rank3Derived:
    """Derive the sequential solution symbolically (M28: never hand-copied
    into the solver — the solver only evaluates what is derived here)."""
    if pair not in RANK3_PAIRS:
        raise ValueError(f"unknown rank-3 pair: {pair}")
    hmat = generic_hermitian()
    name = "+".join(pair)

    if pair in (PAIR_12, PAIR_13):
        bsym = pair[1]
        # full remainder including a symbolic type-1 part, so the guards
        # PROVE the selected minors never touch the unsolved component
        xa = sp.symbols("xA_r3", positive=True)
        wa = sp.symbols("wA_r3", complex=True)
        t1_template, _ = SYMMETRY_TEMPLATES["type1"]
        c = sp.symbols("cB_r3", positive=True)   # scaled CENTER of B
        w = sp.symbols("wB_r3", complex=True)    # scaled edge of B
        b_template, _ = SYMMETRY_TEMPLATES[bsym]
        remainder = hmat - t1_template(xa, wa) - b_template(c, w, primary="center")
        other = (xa, wa, sp.conjugate(wa))

        eq_c = _minor(remainder, (1, 2), (1, 2))
        _forbid(eq_c, other + (w, sp.conjugate(w)), "center minor", name)
        c_expr = _solve_unique(eq_c, c, "center minor", name)

        eq_w = _minor(remainder, (0, 1), (1, 2))
        _forbid(eq_w, other + (sp.conjugate(w),), "edge minor", name)
        w_expr = sp.simplify(_solve_unique(eq_w, w, "edge minor", name).subs(c, c_expr))

        return Rank3Derived(pair, "peel_delegate",
                            (("center", c_expr), ("edge", w_expr)), hmat)

    # PAIR_23: combination variables on the summed pattern
    sg, s_, d_ = sp.symbols("sigma_r3 s_r3 d_r3", real=True)
    p, m = sp.symbols("p_r3 m_r3", complex=True)
    cp, cm = sp.conjugate(p), sp.conjugate(m)
    t23 = sp.Matrix([
        [sg, p,  m,  sg],
        [cp, s_, d_, cp],
        [cm, d_, s_, cm],
        [sg, p,  m,  sg],
    ])
    remainder = hmat - t23
    solved: dict[sp.Symbol, sp.Expr] = {}

    plan = (
        ("sigma", sg, ((0, 3), (0, 3)), (p, m, s_, d_, cp, cm)),
        ("p",     p,  ((0, 3), (0, 1)), (m, s_, d_, cp, cm)),
        ("m",     m,  ((0, 3), (0, 2)), (p, s_, d_, cp, cm)),
        ("s",     s_, ((0, 1), (1, 3)), (m, d_, cm)),
        ("d",     d_, ((0, 1), (2, 3)), (p, s_, cp)),
    )
    exprs = []
    for label, target, (rows, cols), forbidden in plan:
        eq = _minor(remainder, rows, cols)
        # order-aware guard: substitute what is already solved, THEN no
        # other unknown may remain (K31)
        eq = sp.expand(eq.subs(solved))
        _forbid(eq, forbidden, f"{label} minor", name)
        expr = _solve_unique(eq, target, f"{label} minor", name)
        solved[target] = expr
        solved[sp.conjugate(target)] = sp.conjugate(expr)
        exprs.append((label, expr))
    return Rank3Derived(pair, "combo", tuple(exprs), hmat)


# ---------------------------------------------------------------- numeric

@dataclass
class Rank3Result:
    pair: tuple[str, str]
    alphas: tuple[float, float, float]        # (alpha_A, alpha_B, alpha_G)
    h_components: tuple[np.ndarray, np.ndarray, np.ndarray]  # trace-1 each
    m_components: tuple[np.ndarray, np.ndarray, np.ndarray]
    consistency_residual: float | None = None  # {2,3} only (K32)


def _subs_map(hermitian: sp.Matrix, cov: np.ndarray) -> dict:
    mapping = {}
    for i in range(4):
        mapping[hermitian[i, i]] = complex(cov[i, i]).real
        for j in range(i + 1, 4):
            mapping[hermitian[i, j]] = complex(cov[i, j])
    return mapping


def _eval_guarded(expr: sp.Expr, mapping: dict, what: str, pair_name: str) -> complex:
    _, den = sp.fraction(sp.together(expr))
    if abs(complex(sp.N(den.subs(mapping)))) < _DENOM_TOL:
        raise DecompositionError(
            f"{pair_name}: {what}-denominator ~ 0 (the generic pure does not "
            "carry the missing anisotropy, or symmetries overlap)"
        )
    return complex(sp.N(expr.subs(mapping)))


def _require_real(value: complex, what: str, pair_name: str) -> float:
    if abs(value.imag) > 1e-6 * (1 + abs(value)):
        raise DecompositionError(f"{pair_name}: {what} not real ({value})")
    return value.real


def _require_positive(value: float, what: str, pair_name: str) -> float:
    if value <= _TOL:
        raise DecompositionError(f"{pair_name}: {what} <= 0 ({value})")
    return value


def _template_numeric(sym: str, x: float, edge: complex,
                      primary: str = "outer") -> np.ndarray:
    """Evaluate a Table-1 template numerically. Substitution happens on the
    SYMBOLIC template so the dependent parameter is formed before numbers
    enter (review defect 2: substituting corner=0 into an outer-primary
    template collapses 0*conj(0)/x to a zero matrix — always pass the
    NONZERO parameter as `x` with the matching `primary`)."""
    template, _ = SYMMETRY_TEMPLATES[sym]
    xs = sp.symbols("xs", positive=True)
    ws = sp.symbols("ws", complex=True)
    mat = template(xs, ws, primary=primary).subs({xs: x, ws: sp.sympify(edge)})
    return np.array(sp.matrix2numpy(sp.Matrix(mat).evalf(), dtype=complex))


def _pure_guards(h: np.ndarray, label: str, pair_name: str,
                 psd_tol: float, rank1_tol: float) -> None:
    eig = np.linalg.eigvalsh(h)
    if eig[-1] < _TOL:  # review: the zero matrix must not pass as "rank 1"
        raise DecompositionError(f"{pair_name}: {label} is (near-)zero")
    if eig.min() < -psd_tol:
        raise DecompositionError(
            f"{pair_name}: {label} not PSD (min eig {eig.min():.2e})"
        )
    if eig[-2] > rank1_tol * max(eig[-1], 1e-300):
        raise DecompositionError(
            f"{pair_name}: {label} not rank 1 (second eig {eig[-2]:.2e})"
        )


def decompose_rank3(
    covariance: np.ndarray,
    pair: tuple[str, str],
    rank_tol: float = 1e-9,
    psd_tol: float = 1e-6,
    rank1_tol: float = 1e-6,
    consistency_tol: float = 1e-6,
) -> Rank3Result:
    """Three-term decomposition for the given symmetric-type pair.

    NON-UNIQUENESS (stage-10 finding, generalizing the stage-9 review
    note): a rank-3 covariance can admit VALID decompositions under more
    than one pair hypothesis (verified example: two type-2 pures +
    generic re-splits exactly as type1+type2+generic). The result is
    therefore *a* decomposition consistent with the requested pair, not
    *the* decomposition; selecting among physically valid alternatives
    is a physics question outside this solver (novelty protocol step 5).
    Use `propose_decompositions` to see every hypothesis that passes."""
    if pair not in RANK3_PAIRS:
        raise ValueError(f"unknown rank-3 pair: {pair} (same-type pairs are "
                         "degenerate by construction; order is (A, B))")
    name = "+".join(pair)
    cov = np.asarray(covariance, dtype=complex)
    if not np.all(np.isfinite(cov.real)) or not np.all(np.isfinite(cov.imag)):
        raise DecompositionError("covariance contains non-finite entries")
    cov = (cov + cov.conj().T) / 2

    trace = float(np.trace(cov).real)
    if abs(trace - 1.0) > 1e-6:
        raise DecompositionError(
            f"covariance trace is {trace:.6f}; normalize to m00 = 1 "
            "(trace-1 convention, AO2016)"
        )
    eig = np.linalg.eigvalsh(cov)
    lam_max = float(np.max(np.abs(eig)))
    rank = int(np.sum(np.abs(eig) > rank_tol * lam_max))
    if rank != 3:
        raise DecompositionError(
            f"covariance rank is {rank} (rank_tol={rank_tol}), "
            "three-term decomposition needs rank 3"
        )

    derived = derive_rank3(pair)
    mapping = _subs_map(derived.hermitian, cov)

    if derived.kind == "peel_delegate":
        bsym = pair[1]
        c = _require_positive(
            _require_real(
                _eval_guarded(dict(derived.exprs)["center"], mapping, "center", name),
                "center parameter", name),
            "center parameter", name)
        w = _eval_guarded(dict(derived.exprs)["edge"], mapping, "edge", name)
        corner = float((w * np.conj(w)).real / c)
        alpha_b = 2 * (c + corner)
        if not (_TOL < alpha_b < 1 - _TOL):
            raise DecompositionError(f"{name}: alpha_B out of (0,1): {alpha_b}")
        # build from the guarded-positive CENTER (review defect 2: an
        # outer-primary build with corner == 0 — legitimate center-only
        # pures, e.g. edge w = 0 — collapses to the zero matrix)
        t_b = _template_numeric(bsym, c, w, primary="center")

        residual = (cov - t_b) / (1 - alpha_b)
        residual = (residual + residual.conj().T) / 2
        # DELEGATE: the stage-8 solver contributes its own guard set
        try:
            r2 = decompose(covariance=residual, symmetry="type1",
                           rank_tol=rank_tol, psd_tol=psd_tol,
                           rank1_tol=rank1_tol)
        except DecompositionError as exc:
            raise DecompositionError(
                f"{name}: delegated type-1 stage failed: {exc}"
            ) from exc
        alpha_a = r2.alpha1 * (1 - alpha_b)
        alpha_g = (1 - r2.alpha1) * (1 - alpha_b)
        h_a, h_g = r2.h1, r2.h2
        h_b = t_b / alpha_b
        _pure_guards(h_b, "recovered H_B", name, psd_tol, rank1_tol)
        result = Rank3Result(
            pair=pair,
            alphas=(alpha_a, alpha_b, alpha_g),
            h_components=(h_a, h_b, h_g),
            m_components=tuple(_to_mueller(h) for h in (h_a, h_b, h_g)),
        )
        return result

    # combo path ({type2, type3})
    values = {}
    for label, expr in derived.exprs:
        values[label] = _eval_guarded(expr, mapping, label, name)
    sigma = _require_real(values["sigma"], "sigma", name)
    s_val = _require_real(values["s"], "s", name)
    d_val = _require_real(values["d"], "d", name)
    w2 = (values["p"] + values["m"]) / 2
    v3 = (values["p"] - values["m"]) / 2
    kbar2 = _require_positive((s_val + d_val) / 2, "kbar2 (type-2 center)", name)
    ebar3 = _require_positive((s_val - d_val) / 2, "ebar3 (type-3 center)", name)
    k2 = _require_positive(float((w2 * np.conj(w2)).real) / kbar2,
                           "k2 (type-2 corner)", name)
    e3 = _require_positive(float((v3 * np.conj(v3)).real) / ebar3,
                           "e3 (type-3 corner)", name)

    # K32: the overdetermination k2 + e3 = sigma is a mandatory check
    residual_sigma = abs(k2 + e3 - sigma) / (1 + abs(sigma))
    if residual_sigma > consistency_tol:
        raise DecompositionError(
            f"{name}: consistency guard failed |k2+e3-sigma| = "
            f"{residual_sigma:.2e} (data does not carry the type2+type3 "
            "structure; no silent patching — K32)"
        )

    alpha_2 = 2 * (k2 + kbar2)
    alpha_3 = 2 * (e3 + ebar3)
    alpha_g = 1 - alpha_2 - alpha_3
    for label, val in (("alpha_A(type2)", alpha_2), ("alpha_B(type3)", alpha_3),
                       ("alpha_G", alpha_g)):
        if not (_TOL < val < 1 - _TOL):
            raise DecompositionError(f"{name}: {label} out of (0,1): {val}")

    t2 = _template_numeric("type2", k2, w2)
    t3 = _template_numeric("type3", e3, v3)
    h_2, h_3 = t2 / alpha_2, t3 / alpha_3
    h_g = (cov - t2 - t3) / alpha_g
    h_g = (h_g + h_g.conj().T) / 2
    _pure_guards(h_2, "recovered H_A (type2)", name, psd_tol, rank1_tol)
    _pure_guards(h_3, "recovered H_B (type3)", name, psd_tol, rank1_tol)
    _pure_guards(h_g, "residual generic pure", name, psd_tol, rank1_tol)
    return Rank3Result(
        pair=pair,
        alphas=(alpha_2, alpha_3, alpha_g),
        h_components=(h_2, h_3, h_g),
        m_components=tuple(_to_mueller(h) for h in (h_2, h_3, h_g)),
        consistency_residual=residual_sigma,
    )


def _to_mueller(h: np.ndarray) -> np.ndarray:
    return np.array(
        sp.matrix2numpy(
            mueller_from_standard_covariance(sp.Matrix(h)).evalf(), dtype=complex
        )
    ).real


# ---------------------------- bridge (v0: spec-10 goal 2; v1 scores: A11)

@dataclass
class ProposeReport:
    """Every attempt is recorded — successes with results, failures with
    reasons (K21 spirit: nothing is silently dropped). `scores` (bridge
    v1, stage 11) carries the cheap structure score per attempted
    hypothesis: min |denominator| of its derived expressions on this
    data — the paper's "larger denominator = numerically healthier"
    advice generalized. Scores ORDER the attempts and the returned
    successes; they never eliminate anything."""
    rank: int
    successes: list          # [(label, result)] — best score first
    failures: list           # [(label, reason)]
    scores: dict | None = None  # {label: float}


def _min_abs_denominator(exprs, hermitian: sp.Matrix, cov: np.ndarray) -> float:
    """Cheap health score: the smallest |denominator| among the derived
    expressions of a hypothesis, evaluated on the data."""
    mapping = _subs_map(hermitian, cov)
    vals = []
    for expr in exprs:
        _, den = sp.fraction(sp.together(expr))
        try:
            vals.append(abs(complex(sp.N(den.subs(mapping)))))
        except (TypeError, ValueError):  # non-numeric residue: score 0
            vals.append(0.0)
    return min(vals) if vals else float("inf")


def _hypothesis_score(label: str, cov: np.ndarray) -> float:
    """Structure score for a rank-2 symmetry or rank-3 pair label."""
    from .composite import COMPOSITE_TYPES, derive_composite

    if label in ("type1", "type2", "type3"):
        # best variant's health (auto mode will pick it anyway); use the
        # lru-cached deriver from solve (review: derive.py is uncached)
        from .solve import _derived

        best = 0.0
        for variant in ("a", "b"):
            eq = _derived(label, variant)
            best = max(best, _min_abs_denominator(
                (eq.x_expr, eq.w_expr), eq.hermitian, cov))
        return best
    if label in COMPOSITE_TYPES:
        d = derive_composite(label)
        return _min_abs_denominator(
            (d.x_expr, d.g_expr, d.h_expr), d.hermitian, cov)
    pair = tuple(label.split("+"))
    d = derive_rank3(pair)
    return _min_abs_denominator(
        [expr for _, expr in d.exprs], d.hermitian, cov)


def propose_decompositions(
    covariance: np.ndarray,
    rank_tol: float = 1e-9,
    psd_tol: float = 1e-6,
    rank1_tol: float = 1e-6,
) -> ProposeReport:
    """Bridge v1: given a covariance, score every symmetry class the rank
    admits (denominator health — see ProposeReport), attempt ALL of them
    in score order, and report the full outcome map. Scoring orders, it
    never eliminates; acceptance is decided solely by the exact solvers."""
    from .composite import COMPOSITE_TYPES, decompose_composite

    cov = np.asarray(covariance, dtype=complex)
    if not np.all(np.isfinite(cov.real)) or not np.all(np.isfinite(cov.imag)):
        return ProposeReport(rank=-1, successes=[], failures=[
            ("input", "covariance contains non-finite entries")], scores={})
    cov = (cov + cov.conj().T) / 2
    eig = np.linalg.eigvalsh(cov)
    lam_max = float(np.max(np.abs(eig)))
    rank = int(np.sum(np.abs(eig) > rank_tol * lam_max))

    caught = (DecompositionError, ValueError, np.linalg.LinAlgError)
    if rank == 2:
        labels = ["type1", "type2", "type3", *COMPOSITE_TYPES]
    elif rank == 3:
        labels = ["+".join(pair) for pair in RANK3_PAIRS]
    else:
        return ProposeReport(rank=rank, successes=[], failures=[(
            "rank",
            f"rank {rank}: no symmetry-conditioned path implemented "
            "(1 = already pure, 4 = full-rank needs different machinery)",
        )], scores={})

    # bridge v1: score every hypothesis first, attempt in score order
    scores = {}
    for label in labels:
        try:
            scores[label] = _hypothesis_score(label, cov)
        except caught:
            scores[label] = 0.0
    ordered = sorted(labels, key=lambda lb: scores[lb], reverse=True)

    def _attempt(label):
        if label in ("type1", "type2", "type3"):
            return decompose(covariance=cov, symmetry=label,
                             rank_tol=rank_tol, psd_tol=psd_tol,
                             rank1_tol=rank1_tol)
        if label in COMPOSITE_TYPES:
            return decompose_composite(cov, label, rank_tol=rank_tol,
                                       psd_tol=psd_tol, rank1_tol=rank1_tol)
        return decompose_rank3(cov, tuple(label.split("+")),
                               rank_tol=rank_tol, psd_tol=psd_tol,
                               rank1_tol=rank1_tol)

    successes, failures = [], []
    for label in ordered:
        try:
            successes.append((label, _attempt(label)))
        except caught as exc:
            failures.append((label, str(exc)))
    return ProposeReport(rank=rank, successes=successes,
                         failures=failures, scores=scores)


# ------------------------------------------------- sweep (K21 artifact)

def sweep_rank3(seed: int = 20260713, trials_per_pair: int = 4) -> dict:
    """Deterministic synthetic sweep over the three pairs + negative
    controls; returns a JSON-able dict (reports/sweep-03-rank3.json)."""
    rng = np.random.default_rng(seed)

    def sym_pure(sym):
        total = 1.0 if sym == "type1" else 0.5
        x = float(rng.uniform(0.15, total - 0.15))
        w = np.sqrt(x * (total - x)) * np.exp(1j * float(rng.uniform(0, 2 * np.pi)))
        return _template_numeric(sym, x, w)

    def gen_pure():
        u = rng.standard_normal(4) + 1j * rng.standard_normal(4)
        u /= np.linalg.norm(u)
        return np.outer(u, u.conj())

    entries = []
    for pair in RANK3_PAIRS:
        for trial in range(trials_per_pair):
            h_a, h_b, h_g = sym_pure(pair[0]), sym_pure(pair[1]), gen_pure()
            a_a = float(rng.uniform(0.2, 0.4))
            a_b = float(rng.uniform(0.2, 0.4))
            a_g = 1 - a_a - a_b
            cov = a_a * h_a + a_b * h_b + a_g * h_g
            entry = {"pair": "+".join(pair), "trial": trial,
                     "alphas_true": [a_a, a_b, a_g]}
            try:
                r = decompose_rank3(cov, pair)
                entry["status"] = "recovered"
                entry["alpha_error"] = float(max(
                    abs(r.alphas[i] - t) for i, t in
                    enumerate((a_a, a_b, a_g))))
                entry["component_error"] = float(max(
                    np.max(np.abs(r.h_components[i] - h))
                    for i, h in enumerate((h_a, h_b, h_g))))
                if r.consistency_residual is not None:
                    entry["consistency_residual"] = r.consistency_residual
            except DecompositionError as exc:
                entry["status"] = "rejected"
                entry["reason"] = str(exc)
            entries.append(entry)

    # negative/alternative controls. IMPORTANT (stage-10 finding): rank-3
    # decompositions are NOT unique across pair hypotheses — e.g. data
    # built as two type-2 pures + generic ALSO admits an exact
    # type1+type2+generic split. An acceptance here is therefore not
    # automatically a bug: it must be VERIFIED (exact reconstruction +
    # purity of every component); only a verification failure is a bug.
    for control in ("rank2_type1", "same_pair_data"):
        if control == "rank2_type1":
            cov = 0.4 * sym_pure("type1") + 0.6 * gen_pure()
        else:
            cov = (0.3 * sym_pure("type2") + 0.3 * sym_pure("type2")
                   + 0.4 * gen_pure())
        for pair in RANK3_PAIRS:
            entry = {"pair": "+".join(pair), "control": control}
            try:
                r = decompose_rank3(cov, pair)
            except DecompositionError as exc:
                entry["status"] = "rejected"
                entry["reason"] = str(exc)[:160]
            else:
                recon = sum(a * h for a, h in zip(r.alphas, r.h_components))
                recon_err = float(np.max(np.abs(recon - cov)))
                purity = float(max(
                    np.linalg.eigvalsh(h)[-2] / np.linalg.eigvalsh(h)[-1]
                    for h in r.h_components))
                if recon_err < 1e-10 and purity < 1e-8:
                    entry["status"] = "accepted_alternative_verified"
                    entry["reconstruction_error"] = recon_err
                    entry["max_purity_defect"] = purity
                    entry["alphas"] = [float(a) for a in r.alphas]
                else:
                    entry["status"] = "INVALID (accepted but failed "
                    entry["status"] += "verification — bug)"
                    entry["reconstruction_error"] = recon_err
                    entry["max_purity_defect"] = purity
            entries.append(entry)

    return {
        "sweep": "rank3-01",
        "seed": seed,
        "trials_per_pair": trials_per_pair,
        "note": ("beyond-paper zone (M34): recoveries are mechanism "
                 "verifications on synthetic data; NO physics/novelty claim "
                 "— candidates only (novelty protocol step 5 is human)"),
        "entries": entries,
    }
