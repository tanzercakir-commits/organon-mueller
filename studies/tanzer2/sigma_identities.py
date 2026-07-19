"""TANZER_2 — the narrowed Sigma-conjugation study (self-contained).

The collaborator's second, deliberately narrower brief. His frame,
nothing added — no Lambda, no Sigma-bar, no Mueller:

  Sigma^mu (his 4x4 Pauli generalization); Z = alpha_mu Sigma^mu on the
  constraint  alpha.alpha = alpha_0^2 - alpha_1^2 - alpha_2^2 - alpha_3^2 = 1;
  Z^{-1} = alpha_0 Sigma^0 - alpha_1 Sigma^1 - alpha_2 Sigma^2 - alpha_3 Sigma^3;
  the 8-element set
    S = { Z, Z^-1, Zdag, Z*, Z^T, (Z^-1)dag, (Z^-1)*, (Z^-1)^T }.

  Task 1: verify four given identities  Sigma^mu = A Sigma^mu B.
  Task 2: for every (A, B) in S x S, does  Sigma^mu = A Sigma^mu B  hold?

RESULT (proven below): exactly the four given identities hold; there are
NO further identities of this form in S. The reason is one structural
lemma, not enumeration:

  LEMMA  [ (Sigma^mu)^T , Sigma^nu ] = 0   for all mu, nu.

Since Sigma is Hermitian ((Sigma^mu)^* = (Sigma^mu)^T), the four
"transpose-built" elements { Z*, Z^T, (Z^-1)*, (Z^-1)^T } commute with
every Sigma^mu; the four "Sigma-built" elements { Z, Z^-1, Zdag,
(Z^-1)dag } do not. Then:

  - mu = 0 (Sigma^0 = I) forces  A B = I,  i.e.  B = A^{-1}
    (each element's inverse is in S, so 8 candidate pairs survive);
  - mu = 1,2,3 force A to commute with the Sigma^k
    (only the 4 transpose-built elements do).

=> exactly the 4 transpose-built pairs (A, A^{-1}) satisfy the identity,
and those are precisely the four given ones.

Precision note (honest): det(Z) = (alpha.alpha)^2, NOT alpha.alpha, so
"det(Z) = 1" means alpha.alpha = +/-1; the intended alpha.alpha = 1 is
the branch on which Z^{-1} above is the true two-sided inverse
(Z Z^{-1} = (alpha.alpha) I).
"""
import numpy as np
import sympy as sp

# --- his Sigma matrices (verbatim from TANZER_2.tex) -----------------------
S0 = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
S1 = sp.Matrix([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, -sp.I], [0, 0, sp.I, 0]])
S2 = sp.Matrix([[0, 0, 1, 0], [0, 0, 0, sp.I], [1, 0, 0, 0], [0, -sp.I, 0, 0]])
S3 = sp.Matrix([[0, 0, 0, 1], [0, 0, -sp.I, 0], [0, sp.I, 0, 0], [1, 0, 0, 0]])
SIGMA = [S0, S1, S2, S3]

#: his set S, in his order
NAMES = ["Z", "Z^-1", "Zdag", "Z*", "Z^T",
         "(Z^-1)dag", "(Z^-1)*", "(Z^-1)^T"]


def _zero(m):
    return sp.expand(m) == sp.zeros(4)


def z_and_zinv(a):
    Z = sum((a[m] * SIGMA[m] for m in range(4)), sp.zeros(4))
    Zi = a[0] * S0 - a[1] * S1 - a[2] * S2 - a[3] * S3
    return Z, Zi


def set_S(a):
    """The 8 elements of S built by his definitions from Z(a), Z^-1(a)."""
    Z, Zi = z_and_zinv(a)
    return {
        "Z": Z, "Z^-1": Zi, "Zdag": Z.conjugate().T, "Z*": Z.conjugate(),
        "Z^T": Z.T, "(Z^-1)dag": Zi.conjugate().T,
        "(Z^-1)*": Zi.conjugate(), "(Z^-1)^T": Zi.T,
    }


# --- the structural facts (exact, symbolic; generic complex alpha) ---------

def sigma_is_hermitian():
    return all(_zero(SIGMA[m].conjugate() - SIGMA[m].T) for m in range(4))


def commutation_lemma():
    """[ (Sigma^mu)^T , Sigma^nu ] = 0 for all mu, nu."""
    return all(_zero(SIGMA[m].T * SIGMA[n] - SIGMA[n] * SIGMA[m].T)
               for m in range(4) for n in range(4))


def det_Z_is_alpha_squared():
    a = sp.symbols("a0 a1 a2 a3", complex=True)
    Z, _ = z_and_zinv(a)
    q = a[0]**2 - a[1]**2 - a[2]**2 - a[3]**2
    return sp.expand(Z.det() - q**2) == 0


def commuting_elements():
    """Which of the 8 elements commute with every Sigma^mu (exact)."""
    a = sp.symbols("a0 a1 a2 a3", complex=True)
    S = set_S(a)
    return {n: all(_zero(M * SIGMA[k] - SIGMA[k] * M) for k in range(4))
            for n, M in S.items()}


# --- the 64-trial table on the constraint surface --------------------------

_SN = [np.array(s, dtype=complex) for s in SIGMA]


def _alpha_on_constraint(rng):
    a1, a2, a3 = (rng.normal() + 1j * rng.normal() for _ in range(3))
    a0 = np.sqrt(1 + a1**2 + a2**2 + a3**2)   # a0^2 - a1^2 - a2^2 - a3^2 = 1
    return np.array([a0, a1, a2, a3], dtype=complex)


def _set_S_numeric(a):
    Z = sum(a[m] * _SN[m] for m in range(4))
    Zi = a[0] * _SN[0] - a[1] * _SN[1] - a[2] * _SN[2] - a[3] * _SN[3]
    return {"Z": Z, "Z^-1": Zi, "Zdag": Z.conj().T, "Z*": Z.conj(),
            "Z^T": Z.T, "(Z^-1)dag": Zi.conj().T,
            "(Z^-1)*": Zi.conj(), "(Z^-1)^T": Zi.T}


def table(seeds=(20260718, 20260719), tol=1e-9):
    """The 8x8 identity table: True iff Sigma^mu = A Sigma^mu B holds for
    all mu, checked at two independent points on the constraint surface
    (a coincidence would have to survive both)."""
    runs = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        a = _alpha_on_constraint(rng)
        Z = sum(a[m] * _SN[m] for m in range(4))
        Zi = a[0] * _SN[0] - a[1] * _SN[1] - a[2] * _SN[2] - a[3] * _SN[3]
        assert abs(np.linalg.det(Z) - 1) < 1e-8
        assert np.max(np.abs(Z @ Zi - np.eye(4))) < 1e-8
        S = _set_S_numeric(a)
        runs.append({(an, bn): all(
            np.max(np.abs(S[an] @ _SN[m] @ S[bn] - _SN[m])) < tol
            for m in range(4)) for an in NAMES for bn in NAMES})
    return {k: (runs[0][k] and runs[1][k]) for k in runs[0]}


#: his four Task-1 identities as (A, B) pairs
TASK1 = [("Z*", "(Z^-1)*"), ("(Z^-1)*", "Z*"),
         ("Z^T", "(Z^-1)^T"), ("(Z^-1)^T", "Z^T")]


#: LaTeX labels for the 8 elements, in NAMES order
_LATEX = {
    "Z": "$Z$", "Z^-1": "$Z^{-1}$", "Zdag": "$Z^{\\dagger}$",
    "Z*": "$Z^{*}$", "Z^T": "$Z^{T}$",
    "(Z^-1)dag": "$(Z^{-1})^{\\dagger}$", "(Z^-1)*": "$(Z^{-1})^{*}$",
    "(Z^-1)^T": "$(Z^{-1})^{T}$",
}


def latex_table_body():
    """Emit the 8x8 table body (one row per A) from the COMPUTED table, so
    the report's checkmarks cannot drift from the result (L3 lesson:
    generate tables, never hand-transcribe)."""
    t = table()
    lines = []
    for an in NAMES:
        cells = ["$\\checkmark$" if t[(an, bn)] else "" for bn in NAMES]
        lines.append(f"{_LATEX[an]:>20} & " + " & ".join(cells) + "\\\\")
    return "\n".join(lines)


def summary():
    t = table()
    yes = sorted(k for k, v in t.items() if v)
    return {
        "sigma_hermitian": sigma_is_hermitian(),
        "commutation_lemma": commutation_lemma(),
        "det_Z_is_alpha_squared": det_Z_is_alpha_squared(),
        "commuting": commuting_elements(),
        "identities": yes,
        "task1_all_hold": all(t[p] for p in TASK1),
        "count": len(yes),
        "only_task1": set(yes) == set(TASK1),
    }


if __name__ == "__main__":
    s = summary()
    print("Sigma Hermitian          :", s["sigma_hermitian"])
    print("Lemma [Sig^T, Sig] = 0   :", s["commutation_lemma"])
    print("det(Z) = (alpha.alpha)^2 :", s["det_Z_is_alpha_squared"])
    print("\nWhich elements commute with every Sigma:")
    for n, ok in s["commuting"].items():
        print(f"  {n:>10}: {ok}")
    print(f"\nTask 1 — all four hold   : {s['task1_all_hold']}")
    print(f"Task 2 — identities in S : {s['count']} / 64")
    for A, B in s["identities"]:
        print(f"    Sigma^mu = {A} Sigma^mu {B}")
    print(f"exactly the four given   : {s['only_task1']}")
