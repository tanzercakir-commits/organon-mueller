# STAGE 9 — Rank-2 General: Composite Symmetries + Guarded Atoms (Phase C)

**Date**: 2026-07-13 · **Previous**: stage-08 (Type 1/2/3 deriver) · **Mode**: autonomous

---

## 1. Goals

### (a) Composite types (AO2016 Table 3-4): 1-2, 1-3, 2-3
1. `decomposition/composite.py`: three-parameter templates (Table 3 —
   primaries {x, g, h}: in 1-2/1-3 x=α₁B center + G, H; in 2-3 x=α₁A corner +
   G\*, H\*; dependents from rank-1 relations: AB=GG\*, GH\*=MB, BC=HH\* /
   2-3: AB=GG\*, HG\*=AY, AC=HH\*), sequential minor solution (each minor linear
   in its own unknown + conj-free; structural guards like stage-08),
   Table-4 anchor comparison (K28 full symbolic zero), numeric solver
   `decompose_composite` (K26 guards + α₁ = trace formula: 1-2/1-3:
   A+2B+C; 2-3: 2A+B+C scaled).
2. Synthetic roundtrip: type-specific pure H's from a rank-1 |u⟩⟨u| vector
   (1-2: u=(u₀,u₁,u₁,u₃); 1-3: u=(u₀,u₁,−u₁,u₃); 2-3: u=(u₀,u₁,u₂,u₀)) +
   generic pure; deterministic seed; exact recovery.
3. Degenerate guard: if the missing-type anisotropy is absent (paper condition), explicit error.

### (b) guarded_atoms — first half (per the design note; WITHOUT TOUCHING the axiom)
4. `discovery/guards.py`: `GuardedAtom(name, guard)` node (guard ∈
   GUARD_KEYS — its own vocabulary that EXTENDS the CONDITIONS dictionary with
   class2_ta/tb/tg; hermitian/unitary keys shared with CONDITIONS) +
   constrained generators:
   - numeric: hermitian → real parameters; unitary → τ real, α,β,γ imaginary;
     class2_ta/tb/tg → (τ,α,0,0)/(τ,0,β,0)/(τ,0,0,γ).
   - symbolic: generic symbols with the same constraints (K17 independence continues).
5. **Generator fidelity test** (stage-08 obligation 1): the symbolic generator is
   the generic representative of the class (number/pattern of free symbols + the numeric
   generator satisfying the CONDITIONS predicates).
6. **Guarded campaign** (`run_guarded_campaign`): the first Horn-conditional identity
   candidates. **CORRECTION (pre-implementation numeric probe)**: the first
   draft's target `unitary(a) → (a·conj(a))·b ≡ b·(a·conj(a))` was WRONG —
   an elementwise conj ≠ dagger confusion (hh†=1 requires a quaternion-Hermitian
   conjugate; ZZ\* is a retarder Mueller, not a scalar). Eliminated by probe; lesson
   recorded. Verified targets:
   - G1: `class2_ta(a) ∧ class2_ta(b) → a·b ≡ b·a` (the {1,i} quaternion
     plane is commutative — probe ✓)
   - G2: `class2_tg(a) ∧ class2_tg(b) → a·b ≡ b·a` (the {1,k} plane — probe ✓)
   - G3 (added after audit, suggestion 2): `class2_tb(a) ∧ class2_tb(b) →
     a·b ≡ b·a` (the {1,j} plane) — for full symmetry of the three planes
   - N1 (negative): a mixture `class2_ta(a) ∧ class2_tg(b)` does NOT COMMUTE (probe ✓)
   Criterion: under the guard symbolic-EXACT + guarded numeric ✓; e-graph
   UNPROVEN; guard-free symbolic WRONG (M32) → the FIRST filled output of the
   `underivable` channel, with a guard tag; flagged to the novelty-protocol, no CLAIM
   (these are known facts — the aim is proof of the channel mechanism; written that way
   in the report). unitary/hermitian guards are limited in this stage to generator+fidelity
   test (no identity claim — honest scope).

## 2. Architectural decisions

- **M31. The composite solver is in a separate module**; the stage-08 fundamental path is unchanged.
- **M32. Guarded-verdict format**: a triple (guard-conjunction, pair, layer
  results); the guard-free-wrong check is MANDATORY (otherwise it is an unconditional
  identity, and the guard tag would be misleading).

## 3. Strict rules

K29. Composite minor selections are also structurally guarded (the x-minor cannot touch g/h,
etc.); violation throws. K30. Guarded symbolic evaluation is with constraint-parameterized
generic symbols (not assumption injection — by substitution).

## 4-6. Delivery + Verification

composite.py + guards.py + two test files + report (A10 groundwork: in rank-3 the
residual = H − α₁H₁ₛ − α₂H₂ₛ rank-1 conditions — the minor mechanism is ready).
Acceptance: Table-4 3/3 symbolic one-to-one; roundtrip 3 types exact; G1-G2 four
checks (guarded symbolic ✓, guarded numeric ✓, proof ✗, guard-free
symbolic ✗); 110 old tests green.

**STOP HERE**
