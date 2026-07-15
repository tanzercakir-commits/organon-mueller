# DRAFT — egglog upstream issue (NOT SUBMITTED)

> Status: DRAFT. Submission depends on user approval (decision M23).
> Target repo: egglog-python (or core egglog if they redirect us).
> If submitted: date/link to be recorded here.

---

**Title:** Congruence not maintained after saturation: parents of merged
e-classes stay separate (registration-order dependent)

**Versions:** egglog (Python) 13.2.0 · Python 3.11.15 · Linux x86_64

## Summary

With a single ground rewrite and ~29 registered ground terms, saturation
merges two child terms but does **not** merge their syntactically identical
parents — `check` reports `b*(a*conj(a)) != b*(conj(a)*a)` even though
`a*conj(a) == conj(a)*a` checks true in the same e-graph. The behavior is
deterministic, depends on registration **order** (registering the two parent
terms first makes it pass), persists after additional `run` iterations and
re-saturation, and is unaffected by `seminaive=False`. In a larger
registration set (5698 terms, superset of the failing 1476-term set) the same
check passes — derivability is non-monotone in the registered set, which no
rule semantics can produce. We also observed `extract` returning a
representative from a different atom multiset than the queried term
(impossible under content-preserving rules), suggesting the same underlying
congruence/rebuild issue.

## Minimal reproduction (self-contained)

```python
from egglog import EGraph, Expr, StringLike, eq, rewrite, ruleset

class Q(Expr):
    def __init__(self, name: StringLike) -> None: ...
    def __mul__(self, other: "Q") -> "Q": ...
    def conj(self) -> "Q": ...

a, b = Q("a"), Q("b")
ca, cb = a.conj(), b.conj()

TERMS = [
    a, b, ca, cb,
    a*a, a*b, b*a, b*b,
    a*ca, a*cb, b*ca, b*cb, ca*a, ca*b,
    b*(a*a), b*(a*b), b*(b*a), b*(b*b),
    (a*a)*b, (a*b)*b, (b*a)*b, (b*b)*b,
    a*(ca*a), a*(cb*b),
    b*(a*ca), b*(a*cb), b*(b*ca), b*(b*cb),
    b*(ca*a),
]
rules = ruleset(rewrite(a * a.conj()).to(a.conj() * a))

eg = EGraph()
for t in TERMS:
    eg.register(t)
eg.run(rules.saturate())

eg.check(eq(a*ca).to(ca*a))            # passes: children merged
eg.check(eq(b*(a*ca)).to(b*(ca*a)))    # FAILS — congruence violation
```

Expected: after the children `a*conj(a)` and `conj(a)*a` merge, the parent
e-nodes `Mul(b, <class>)` are congruent and must share a class; the second
`check` should pass.

Observed: the second `check` raises. Control experiments (same versions):

| Variant | parent check |
|---|---|
| as above (natural registration order) | **FAILS** |
| register the two parent terms FIRST, then TERMS | passes |
| only the two parent terms registered (isolated) | passes |
| `EGraph(seminaive=False)` | still FAILS |
| extra `eg.run(rules * 30)` after saturation | still FAILS |

The 29-term set is 1-minimal under delta debugging (removing any single
term makes the failure disappear). Originally found on a 1476-term
registration where 9 such pairs were affected; a 5698-term superset does
not exhibit the failure on this pair.

Happy to provide the larger deterministic reproductions if useful.
