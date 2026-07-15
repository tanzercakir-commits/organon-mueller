# Candidate findings — consolidation

This document collects, in one place, the outputs of the engine that go
**beyond** re-verifying the published literature. Each carries its
**evidence class**. **No novelty or physics claim is made here**: whether
any of these is interesting, new, or publishable is a human judgement —
the final step of [`novelty-protocol.md`](novelty-protocol.md). The
material is raw input for the Kuntman feedback package and any future
write-up.

Evidence classes (tied to [`VERIFICATION.md`](VERIFICATION.md)):
**symbolic-proof** (exact), **numeric-deterministic** (seeded sampling),
**candidate** (beyond the papers; no claim).

## 1. Verified results (machine-checked against the papers)

These re-derive published results and are recorded as confidence anchors,
not as new findings.

| Result | Evidence | Source |
|---|---|---|
| Six-representation isomorphisms + conversions | symbolic-proof | JOSA A 34, 80; PRA 95, 063819 |
| Fundamental decomposition, Table 2, all six variants | symbolic-proof (exact zero) | AO 55, 2543 |
| Composite types, Table 4, all three | symbolic-proof | AO 55, 2543 |
| Section-6 numeric example | numeric-deterministic (print precision) | AO 55, 2543 §6 |
| Coupled-dipole three-term decomposition (Eq. 25) | symbolic-proof (theorem) | PRB 98, 045410 |
| Hybrid frequencies ω±, hybrid basis | symbolic-proof | PRB 98, 045410 |
| General-geometry Jones (Eq. A11) | symbolic-proof | Symmetry 12, 1790 |
| 3D rank-1 reduction, γ_z / γ_x / γ_−z | symbolic-proof (+6×6 numeric check) | OA-in-ensemble preprint |

## 2. Theorems that arose during verification

- **Reshuffle theorem** (symbolic-proof): R(σᵢ⊗σⱼ) = σᵢ⊗σⱼ*, i.e. the
  AO2016 covariance H is exactly the standard Cloude/Gil covariance;
  Eq. (2) read literally (no conjugate) gives a non-PSD cousin.
- **Fragment-completeness theorem** (symbolic-proof): the axiom set is
  empirically complete for the swept Mul/Conj fragment (sweeps #1/#2
  found zero underivable pairs over 22,560 + 924 pairs).
- **General Perrin reciprocity** (symbolic-proof): with R(J) = σJᵀσ,
  amp_B = (σu*)†R(J)(σv*) = v†Ju for ANY Jones matrix — the paper's
  Eqs. (8)-(13) construction is the special case.
- **δ = 0 ⇒ γ_z ≡ 0** (symbolic-proof): no forward-scattering optical
  activity without coupling, for every orientation.
- **{2,3} within-hypothesis uniqueness** (symbolic-proof, reviewer):
  the rank-3 {type2,type3} decomposition is unique given the pair
  hypothesis.
- **Dagger inexpressibility** (symbolic-proof): transpose/dagger cannot
  be expressed in the elementwise-conjugation term language; this bounds
  what the discovery engine can find and explains the empty guarded
  hermitian/unitary channel (below).

## 3. Candidate observations (beyond the papers — NO claim)

- **Rank-3 non-uniqueness** (candidate; closed form verified to 1e-16):
  a rank-3 covariance can admit valid decompositions under more than one
  symmetry-pair hypothesis (verified example: two type-2 pures + generic
  also splits exactly as type1 + type2 + generic). A rank-3 result is
  therefore *a* decomposition consistent with the requested pair, not
  *the* decomposition. Selecting the physical one is outside the solver.
- **Guarded Horn-conditional identities** (candidate; M32 four-part
  evidence): commutation inside each class-2 quaternion plane
  (class2_ta/tb/tg) — true under the guard, false without it, not
  derivable by the guard-blind axioms. These are known facts (the {1,q}
  planes are commutative); recorded as the mechanism proof of the
  underivable channel, not as new identities.
- **Empty hermitian/unitary guarded channel** (numeric + theory): no
  enumeration-reachable Horn identity exists in these classes (stage-20
  probe; consistent with dagger inexpressibility). A first-class negative
  result.

## 4. Print-artifact diagnoses (M30 series — eight, all reviewer-confirmed)

Each was found by cross-checking a paper's own internal equations and
independently re-derived; **none affects a physical conclusion**. See
[`phase-d-retrospective.md`](phase-d-retrospective.md) for the table.
Summary: AO2016 Eq. 17 (h₀₃) and Eq. 21 [1,3]; PRB 98,045410 Eq. 37
(2× scale vs its own Eq. 29) and Eq. 39 (η ω vs the Eq.-44-required
η ω²); OA-in-ensemble preprint Eq. 31 (label (n×m)_z), Eq. 9 (prefactor
−2iµ), Eq. 30 (J₁₂−J₁₂ typo), Eq. 32 (dropped k). We would value the
authors' confirmation of these.

## 5. What is NOT here

No physical interpretation, no significance ranking, no publication
recommendation — those require the domain experts (Kuntman–Arteaga
group). This document is deliberately a labelled inventory, nothing more.
