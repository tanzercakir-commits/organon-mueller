# organon-mueller — Roadmap — **FROZEN-22** (declared: Stage 2, 2026-07-13)

**22 stages, 6 phases — FROZEN** (Organon v1 tradition; frozen-55 in v1).
This number no longer changes; a change only goes to the user via a
critical-decision note. Kuntman/group feedback can change the INTERNAL order of
phases C and D, but cannot change the number of stages.

```
PHASE A — Foundation (Stage 0–2)
├── 0  Representation layer + 14-identity regression        ✅ (36/36)
├── 1  Library extension (21 identities) + serialization
│      + egglog spike (SUCCESSFUL, hybrid architecture proposal)  ✅ (50/50)
└── 2  Discovery engine core v0: hybrid egglog+SymPy,        ✅ (56/56)
       enumeration+saturation+harvest+100% verification;
       R1-R3 rediscovery, negative controls → FROZEN-22 DECLARATION

PHASE B — Discovery engine (Stage 3–7)                      ✅
├── 3  Term enumeration + complexity bounds                 ✅ (M18 isolated proofs)
├── 4  Candidate pipeline: numeric pre-screen → symbolic proof  ✅ (M19 certification)
├── 5  Recovery campaign: the engine must find I1–I21 ITSELF  ✅ ({I1,I10,I15})
├── 6  New candidate sweep #1 + literature-comparison discipline  ✅ (fragment completeness THEOREM)
└── 7  Iteration evaluation (v1 iter tradition)             ✅ (Sum/Scale; AL fine distinction)

PHASE C — Decomposition deriver (Stage 8–11)                ✅
├── 8  Symmetry-conditioned decomposition: automatic derivation of AO2016's 6 types ✅ (Table 2 6/6; reshuffle THEOREM)
├── 9  Rank-2 general solver                                ✅ (Table 4 3/3; guarded atoms M32)
├── 10 Rank-3 discovery sweep (publication-candidate new-result potential) ✅ (non-uniqueness finding)
└── 11 Iter + Kuntman feedback window #1                    ✅ (package ready; bridge v1)

PHASE D — Dipole module (Stage 12–15)                       ✅
├── 12 Coupled-dipole symbolic engine (PRB 98,045410 re-derivation) ✅ (Eq. 25 decomposition THEOREM)
├── 13 direction-general automation of the γ (optical activity) parameter ✅ (Perrin general theorem)
├── 14 N-dimer / ensemble generalization (OA-ensemble open ends) ✅ (δ=0⇒γ_z≡0; bridge end-to-end)
└── 15 Iter + feedback window #2                            ✅ (dipole addition; M30×8)

PHASE E — Packaging (Stage 16–19)                           ✅ (at A19)
├── 16 LaTeX/report generator (finding → paper material)    ✅ (evidence-labeled, deterministic)
├── 17 MCP server (decompose/propose/discover/report)       ✅ (GATE hardening; NOT hosted)
├── 18 Web interface — STATIC, hosting-free (decision changed: instead of Streamlit ✅ (textContent XSS-safe)
│      single file web/index.html; server surface = attack surface)
└── 19 Documentation (README/architecture/user-guide)       ✅ (this stage)

PHASE F — Closure (Stage 20–22)                             ⏳
├── 20 Consolidation of publication-candidate results (+guarded-atoms 2nd-half debt) ✅ (negative-result debt closed; repo English)
├── 21 External verification (group feedback, independent replication) ✅ (288 green; CI ×3; D1/D2 found+fixed)
└── 22 v2.0 closure evaluation + retrospective
```

Status (Stage 21 complete): A0–A21 completed, A22 (v2.0 closure) the only
remaining stage; **288 tests green**, CI green on all three matrix cells.
Note: the FROZEN-22
stage COUNT does not change; A18's "hosted" definition was revised to
"static, hosting-free" for security reasons (a scope change, not a count
change — reasoned in the retrospective).

Time calibration (handoff): 2–4 months in tight focus, 6–12 months part-time.
A stage ≈ one milestone unit in v1; every stage closes with a spec → impl →
test → report cycle.
