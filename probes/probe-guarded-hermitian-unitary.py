"""Stage-20 PRE-SPEC probe: are there ENUMERATION-REACHABLE Horn-conditional
identities in the hermitian / unitary guarded classes?

M32 signature of a genuine guarded finding: guard-true (symbolic-exact +
numeric) AND unprovable by the guard-blind axioms AND FALSE without the
guard. We scan small Mul/Conj terms over two guarded atoms a, b.

Stage-9 warning kept front of mind: elementwise conj != dagger. A
hermitian STATE here means the covariance vector |h> = (tau,alpha,beta,
gamma) has REAL components (H = Z is a hermitian Mueller-generator); a
unitary state has tau real, vector part imaginary. These are constraints
on the |h> components, NOT on Z being a unitary/hermitian MATRIX.
"""
import sys
sys.path.insert(0, "/home/claude/organon-mueller/src")

import numpy as np
import sympy as sp

from organon_mueller.discovery.guards import (
    guarded_symbolic_hvector, guarded_random_hvector,
)
from organon_mueller.discovery.terms import Atom, Mul, Conj
from organon_mueller.discovery.interpret import evaluate
from organon_mueller.discovery.symbolic import evaluate_symbolic
from organon_mueller.verify import symbolic_equal, numeric_equal, to_numpy


def sym_assign(guard):
    return {"a": guarded_symbolic_hvector("a", guard).to_z(),
            "b": guarded_symbolic_hvector("b", guard).to_z()}


def num_assign(guard, rng):
    return {"a": to_numpy(guarded_random_hvector(rng, guard).to_z()),
            "b": to_numpy(guarded_random_hvector(rng, guard).to_z())}


def guard_sym_eq(t1, t2, guard):
    A = sym_assign(guard)
    return symbolic_equal(evaluate_symbolic(t1, A), evaluate_symbolic(t2, A))


def guard_num_eq(t1, t2, guard, draws=4):
    rng = np.random.default_rng(20260713)
    for _ in range(draws):
        A = num_assign(guard, rng)
        if not numeric_equal(evaluate(t1, A), evaluate(t2, A)):
            return False
    return True


def unguard_sym_eq(t1, t2):
    A = {"a": HVgen("a"), "b": HVgen("b")}
    return symbolic_equal(evaluate_symbolic(t1, A), evaluate_symbolic(t2, A))


def HVgen(name):
    from organon_mueller.algebra.states import HVector
    return HVector.generic(name).to_z()


# candidate term pairs over atoms a, b (size <= 3), Conj included
a, b = Atom("a"), Atom("b")
ca, cb = Conj(a), Conj(b)
terms = [a, b, ca, cb, Mul(a, b), Mul(b, a), Mul(a, ca), Mul(ca, a),
         Mul(a, cb), Mul(b, ca), Mul(a, a), Mul(ca, cb), Mul(cb, ca),
         Mul(Mul(a, b), a), Mul(a, Mul(b, a))]

for guard in ("hermitian_state", "unitary_state"):
    print("=" * 66)
    print(f"guard = {guard}")
    hits = []
    for i in range(len(terms)):
        for j in range(i + 1, len(terms)):
            t1, t2 = terms[i], terms[j]
            # want: guard-true but unguarded-FALSE (genuinely conditional)
            if unguard_sym_eq(t1, t2):
                continue  # unconditional identity, not interesting here
            if guard_sym_eq(t1, t2, guard) and guard_num_eq(t1, t2, guard):
                hits.append((t1.render(), t2.render()))
    if hits:
        print(f"  {len(hits)} guarded-only equalities found:")
        for h in hits[:20]:
            print("   ", h[0], "==", h[1])
    else:
        print("  NONE — no guarded-only equality among size<=3 Mul/Conj terms")

# sanity: the class2 planes DO produce commutation (known positive control)
print("=" * 66)
for guard in ("class2_ta",):
    ok = guard_sym_eq(Mul(a, b), Mul(b, a), guard) and \
        not unguard_sym_eq(Mul(a, b), Mul(b, a))
    print(f"control {guard}: a*b==b*a guarded-only ->", ok)
