# STAGE 2 — Discovery Engine Core v0 (Hybrid egglog + SymPy) + FROZEN-N

**Date**: 2026-07-13
**Previous stage**: stage-01 (21 identities, serialization, egglog spike SUCCESSFUL)
**Note**: From this stage on the project runs in autonomous mode (user mandate,
2026-07-13): outside the critical-decision threshold, all decisions are justified within
the spec+report; the trust anchor is the verification system (docs/VERIFICATION.md).

---

## 1. Context

The spike showed that the non-commutative skeleton of the quaternion/Z algebra can be
saturated in egglog. This stage turns the proposal into architecture: **hybrid engine** —
egglog produces term-structure equivalence (equality saturation), SymPy/NumPy independently
verifies each candidate. The engine's FIRST job is not to find something new but to
**re-find the known on its own** (the v1 "recover the known" discipline, at the discovery
level).

## 2. Goals

1. `discovery/` package: term language, egglog axiom model, enumeration,
   e-class harvesting, SymPy interpreter + verification pipeline.
2. Acceptance (rediscovery): the engine, over atoms {a,b} and ops {mul, conj}, must find
   the following ITSELF (correction: the sizes of the R3 terms are 8 and 9 — the "size 7"
   in the first draft was an arithmetic error; the acceptance saturation runs over the size 9
   enumeration, for harvest/CI economy the full-pipeline test stays at size 7):
   - R1: conj(conj(a)) ≡ a
   - R2: a·conj(b) ≡ conj(b)·a  (I10 commutation)
   - R3: (a·b)·conj(a·b) ≡ (a·conj(a))·(b·conj(b))  (serial Mueller product, consequence of I10)
3. Negative controls: a·b ≢ b·a and conj(a)·conj(b) ≢ conj(b)·conj(a) must stay SEPARATE
   in the e-graph (saturation must not invent commutativity).
4. EVERY generated candidate pair must be verified by numerical SymPy interpretation; the
   verification rate must be 100% (otherwise engine error → stage fails).
5. `docs/VERIFICATION.md` (trust contract) + ROADMAP frozen-N declaration.

## 3. Architectural decisions

- **M10. Hybrid boundary**: egglog is STRUCTURE only (atoms abstract, no coefficients); the
  parameter level is entirely in SymPy. egglog is never the sole verifier.
- **M11. Soundness rules**: commutation ONLY at the atom level
  (a·conj(b) = conj(b)·a, a,b atoms). General x·conj(y)=conj(y)·x is NOT A RULE —
  since conj-conj pairs are non-commutative it would be unsound; what is derivable follows
  from associativity + the atom rule via saturation. conj distribution PRESERVING order:
  conj(x·y) = conj(x)·conj(y) (element-wise conjugate, not transpose).
- **M12. Candidate definition**: syntactically different term pairs that fall into the same
  e-class; harvest by `extract` grouping (representative string as key).
- **M13. egglog `[discovery]` extra**: the base setup works without egglog; discovery tests
  are skipped with `pytest.importorskip`. CI installs including discovery.
- **M14. FROZEN-N = 22**: the 6 phases / 22 stages in the ROADMAP freeze with this stage.
  A change only goes to the user with a critical-decision note.

## 4. Strict rules

- K9. The engine cannot say "I discovered" → no unverified pair can be reported.
- K10. A candidate that fails verification = test error (silent elimination FORBIDDEN; it is
  the signal of an unsound axiom).
- K11. Stage 0-1 APIs are immutable.
- K12. Enumeration is deterministic (ordered generation, no seeded sampling).

## 5. Deliverable

```
src/organon_mueller/discovery/
├── __init__.py          (graceful ImportError in the absence of egglog)
├── terms.py             (Atom/Mul/Conj, size, deterministic enumeration)
├── axioms.py            (egglog model: ZTerm, rule set — M11 boundaries)
├── interpret.py         (term → SymPy/NumPy Z-matrix value; numerical equivalence)
└── engine.py            (saturate → e-class harvest → verify → DiscoveryResult)
tests/test_discovery.py  (acceptance R1-R3, negative controls, 100% verification)
docs/VERIFICATION.md
docs/ROADMAP.md          (frozen-22 declaration)
specs/stage-02.md, reports/stage-02-REPORT.md
pyproject.toml           ([discovery] extra; CI ".[test,discovery]")
```

## 6. Verification

- R1/R2/R3 via e-graph `check`; negative controls via check-failure.
- All harvested pairs: 3 independent random Z-assignments × numerical comparison.
- Full suite green (both with and without egglog installed).
- Independent (adversarial) auditor PASS.

## 7. Delivery format

Push directly to `main` with PAT (on top of 5cf0bb9) + report + short summary to the user.

## 8. Special warnings

1. (AB)* = A*B* — the element-wise conjugate PRESERVES ORDER; do not confuse it with (AB)^T/†.
2. Do NOT WRITE the atom-commutation rule with free variables x,y (unsound, see M11).
3. The extract representative may not be deterministic — do the grouping within the same
   EGraph object, do not compare across sessions.
4. Measured costs (this environment): size 7 → 570 terms; size 9 → 5698 terms,
   saturation 0.15 s, extract ~21 s (bottleneck is extract; check is cheap). Acceptance
   tests are check-based (size 9), the harvest test is size 7.

## 9. Out of scope

- Scalar/complex-coefficient terms (in Phase B, preserving the hybrid boundary)
- Canonical-form extraction cost function tuning
- New-candidate literature comparison (Stage 6)
- MCP/UI

**STOP HERE**
