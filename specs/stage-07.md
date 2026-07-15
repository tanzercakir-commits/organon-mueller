# STAGE 7 — Language Extension: Sum + Scale — and Phase B Iteration Evaluation

**Date**: 2026-07-13 · **Previous**: stage-06 (sweep #1, completeness theorem)
**Mode**: autonomous · **Input**: `docs/design-note-addition-scalars.md` (auditor soundness-approved)

---

## 1. Context

The Mul/Conj fragment is provably COMPLETE (stage-06). New math
possibility arises only once the language is extended. This stage implements the design note and
runs jointly with A7 of FROZEN-22 (iteration evaluation)
(announced in stage-06 report §5).

## 2. Goals

1. **Term language**: `Sum(t,t)`, `Scale(c,t)`, `ScalarAtom(name)`,
   `ScalarConj(c)` nodes; sizes (Sum/Scale +1; ScalarAtom 1;
   ScalarConj +1); extended conj-normal (Conj only on Atom,
   ScalarConj only on ScalarAtom).
2. **Axioms** (only the soundness-approved table in the design note): Sum
   commutative+associative; two-sided distribution of Mul over Sum (both directions);
   Conj-Sum distribution; Conj-Scale conjugate rule; Scale centrality (two sides);
   nested Scale swap (WITHOUT FORMING a scalar product — opacity M10);
   scalar-conj involution. NO NEW free-variable commutation.
3. **Layers**: interpret (scalar→random complex), symbolic
   (scalar→independent generic symbol, K17 extends), fingerprint
   **scale-relative** (inputs divided by Frobenius norm; ‖M‖≈0 → "ZERO"
   special key; collision of proportionally-different terms is EXPECTED and lower
   layers filter it out — M15 unchanged).
4. **Enumeration** `enumerate_extended(atoms, scalars, max_size,
   max_sums=1, max_scale_depth=1)` — explosion limits spec'd; K12
   determinism preserved. Old `enumerate_terms` UNCHANGED (K11).
5. **Acceptance (design note §Acceptance)**:
   - A: I15 expansion — (aZ_a+bZ_b)·conj(aZ_a+bZ_b) PROVABLY equal to the four-term nested-Scale
     form (provable) + symbolic-exact + numeric.
   - B: I15 cross-term reality — t ≡ conj(t) PROVEN in structural form.
   - C: Recovery campaign: I15 → translatable; result set
     {I1, I10, I15} (M22 monotonicity); I16/I18 moved to the new "interpreted_scalars"
     missing-feature key (CORRECT for opaque scalar universally-quantified
     identities; insufficient for fixed-coefficient ones — honest distinction).
   - D: K11 (old language/API) preserved — old enumeration counts fixed
     (sentinel tested); recovery table tests are RAISED per M22
     (recovery set grows), this is not a K11 violation.
   - E: Mini-harvest (2 atoms + 2 scalars, limited size) runs end-to-end;
     refuted=0; if underivable appears, the novelty-protocol chain (NO CLAIM).
6. **Phase B iter retrospective** (report section): A3-A7 lessons, metrics,
   risks carried over to Phase C.

## 3. Architectural decisions

- **M26. Opaque scalar semantics = universal quantification** (with auditor correction):
  an identity with a scalar in the language reads "for ALL complex coefficients" (I15 is exactly
  this). Constant COEFFICIENT VALUES (e^{iφ}, (1+i)/2) require `interpreted_scalars`.
  A FINE DISTINCTION for Amitsur-Levitzki (stage-7 auditor finding D1): the FORM with ±1
  requires an interpreted scalar, but the identity ITSELF can be expressed sign-free —
  S₄=0 ⟺ (sum of even permutations) = (sum of odd permutations), with only
  Sum+Mul, 4 atoms, size ~95. So an AL-type incompleteness is IN PRINCIPLE expressible
  in this language; it is just too large for the current enumeration limits (max_sums=1,
  size ≤~11) to REACH. The stage-06 expectation was correct in terms of expressive
  power; reachability is a separate matter.
- **M27. Single rule set**: Sum/Scale rules are added to structural_rules;
  old terms are unaffected by the new rules (type-based matching), the engine keeps a single
  provable path (M18 isolation as-is).

## 4. Strict rules

K23. A scalar arithmetic node (c+d, c·d) does NOT ENTER the e-graph (M10).
K24. Adding a new rule = soundness analysis + auditor approval (going outside the table in this spec).
K25. Campaign/harvest reproduction inputs are embedded in the artifact/report (K21 continues).

## 5-6. Delivery + Verification

terms/axioms/interpret/symbolic/fingerprint/engine/recovery updates ·
`tests/test_extended_language.py` · recovery tests current · mini-harvest
result in report · Phase B retrospective section · report. Suite: 84 old + new ones green.

## 7-9.

Push + report + Stage 8 (5 min; Phase C: start of decomposition deriver). Warnings:
-0.0 normalization in the scale-relative key is PRESERVED; symbolic certification cost
is measured for Scale'd pairs. Out of scope: interpreted_scalars,
Sum>1/deep Scale enumeration, full campaign of sweep #2, AL-type search.

**STOP HERE**
