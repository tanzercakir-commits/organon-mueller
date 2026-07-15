# Term-Language Extension Requirements (Stage 5 output; updated at Stage 7)

Status (after Stage 7): of the library's 21 identities, **3 are fully
recovered** (I1, I10, **I15** — via the Sum/Scale extension), **2 are
structural** (I7, I8 — embedded in the semantics of the language), **16** are
outside the language. ~~`addition` and opaque `scalars`~~ **DELIVERED**
(Stage 7): term summation + universally-quantified coefficients (M26) are in
the language; the fingerprint switched to a scale-relative key.

Row semantics: each row is the union of the RECOVERY_TABLE records that
**mention** that feature in their `missing` list.

| Priority | Feature | Identities it locks | Note |
|---|---|---|---|
| 1 | `interpreted_scalars` (interpreted/constant scalar arithmetic) | I4, I11, I16, I17, I18 | e^{iφ}, (1+i)/2, 1/det, trig, real weights — CONSTANT coefficient values. M26 fine distinction (stage-7 auditor finding): integer-coefficient identities (Amitsur-Levitzki type) can ALREADY be expressed with unsigned division; this key is for value-level arithmetic. |
| 2 | `guarded_atoms` (conditional atom classes) | I4, I12, I13, I19, I20, I21 | Binds naturally to the Horn-condition infrastructure (CONDITIONS): "Hermitian atom", "unitary atom", "(τ,α,0,0) atom". The Phase C decomposition deriver will request this. |
| 3 | `dagger` + `stokes_sort` | I9, I13, I14 | Z^† a separate unary op; Stokes a separate sort. For the S′=ZSZ† family and H=\|h⟩⟨h\|. (Auditor proof: dagger CANNOT BE EXPRESSED in the current language — degree argument.) |
| 4 | `entry_level` (entry/trace/det expressions) | I3, I5, I6, I12, I13, I14, I17, I19, I20, I21 | Probably NEVER enters the e-graph; stays in the SymPy-side verification/report layer (discovery = term level, description = entry level). |
| 5 | `constants` (A, R(θ), special cases) | I2, I11, I18 | Only meaningful after guarded_atoms + interpreted_scalars. |

Recommended order: **2** (together with the Phase C entry — the decomposition
deriver wants conditional classes), then 1/3-5 as needed. Per M22, after every
extension the campaign is re-run and the recovery count can only increase.

Known reachability note: AL-type sum-identities (the unsigned divided form of
S₄=0, ~size 95, 4 atoms) are expressible but far beyond the current enumeration
limits (max_sums=1, size ≤~11) — targeted (enumeration-free) verification is
always possible: the three layers operate directly on the pair.
