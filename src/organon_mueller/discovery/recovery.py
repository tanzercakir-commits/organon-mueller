"""Recovery campaign (stage 5, decision M22): can the engine rediscover,
on its own, the hand-coded identity library I1-I21 — or, where it cannot,
WHY exactly?

Every library identity is mapped to one of three statuses:

* ``translatable``: it has a faithful expression as term-language pairs
  (atoms + Mul + Conj over generic Z matrices).  The campaign proves each
  pair through all three layers (e-graph proof, numeric, symbolic-exact;
  rule K20).
* ``structural``: its content IS the term language itself (e.g. the
  quaternion/Z product isomorphism is what Mul means) — nothing to
  rediscover, nothing missing.
* ``untranslatable``: it needs features the language does not have; the
  missing features are named explicitly (rule K19) and aggregate into the
  extension requirements list (docs/term-language-extensions.md).

The table is wired to tests: as the language grows, entries may move to
``translatable`` and the recovered count may only increase (M22).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .engine import DiscoveryEngine
from .interpret import terms_numerically_equal
from .symbolic import terms_symbolically_equal
from .terms import Atom, Conj, Mul, Scale, ScalarAtom, ScalarConj, Sum, Term

__all__ = [
    "RecoveryEntry",
    "RECOVERY_TABLE",
    "MISSING_FEATURES",
    "run_recovery_campaign",
]

_A, _B = Atom("a"), Atom("b")
_P, _Q = ScalarAtom("p"), ScalarAtom("q")
_CP, _CQ = ScalarConj(_P), ScalarConj(_Q)

#: registered vocabulary of missing features (K19: an untranslatable entry
#: must cite keys from here). Stage 7 delivered `addition` and OPAQUE
#: `scalars` (Sum/Scale, universally-quantified coefficients — M26);
#: what remains missing for fixed-coefficient identities is INTERPRETED
#: scalar arithmetic.
MISSING_FEATURES = {
    "interpreted_scalars": "yorumlanan/sabit skaler aritmetigi "
                           "(e^{i phi}, (1+i)/2, +-1, 1/det, trig, reel agirliklar)",
    "dagger": "eslenik-devrik (transpoze/bra-ket; S' = Z S Z^dagger, H = |h><h|)",
    "stokes_sort": "ayri Stokes sort'u (vektor/matris s, S)",
    "entry_level": "matris girdisi/iz/det duzeyinde ifadeler (M00, tr, det, simetri desenleri)",
    "constants": "sabit yapilar (A matrisi, Kronecker, R(theta), ozel durumlar)",
    "guarded_atoms": "kosullu atom siniflari (parametreleri kisitli durumlar: hermitsel, uniter, tau=0)",
}

# I15 structural forms (stage 7): superposition, its Mueller expansion in
# nested-Scale form (scalar products are never formed — M10/K23), and the
# cross term whose conj-symmetry IS the paper's "real cross term".
_SUP = Sum(Scale(_P, _A), Scale(_Q, _B))
_T_AA = Scale(_P, Scale(_CP, Mul(_A, Conj(_A))))
_T_AB = Scale(_P, Scale(_CQ, Mul(_A, Conj(_B))))
_T_BA = Scale(_Q, Scale(_CP, Mul(_B, Conj(_A))))
_T_BB = Scale(_Q, Scale(_CQ, Mul(_B, Conj(_B))))
_I15_LHS = Mul(_SUP, Conj(_SUP))
_I15_RHS = Sum(Sum(_T_AA, _T_AB), Sum(_T_BA, _T_BB))
_I15_CROSS = Sum(_T_AB, _T_BA)


@dataclass(frozen=True)
class RecoveryEntry:
    identity_key: str
    status: str  # "translatable" | "structural" | "untranslatable"
    pairs: tuple = ()  # ((Term, Term), ...) when translatable
    missing: tuple = ()  # feature keys when untranslatable
    note: str = ""


def _p(left: Term, right: Term) -> tuple:
    return (left, right)


RECOVERY_TABLE: tuple[RecoveryEntry, ...] = (
    RecoveryEntry(
        "I1", "translatable",
        pairs=(
            _p(Mul(_A, Conj(_A)), Mul(Conj(_A), _A)),          # Z Z* = Z* Z
            _p(Mul(_A, Conj(_A)), Conj(Mul(_A, Conj(_A)))),     # M is real: M = conj(M)
        ),
        note="M = ZZ* carpim yarisi + gerceklik t = conj(t) formunda",
    ),
    RecoveryEntry(
        "I2", "untranslatable", missing=("constants",),
        note="A matrisi ve Kronecker carpimi dilde yok",
    ),
    RecoveryEntry(
        "I3", "untranslatable", missing=("entry_level",),
        note="det dilde yok",
    ),
    RecoveryEntry(
        "I4", "untranslatable", missing=("guarded_atoms", "interpreted_scalars"),
        note="isaret-cevrilmis atom (parametre duzeyi islem) ve 1/det olcegi yok",
    ),
    RecoveryEntry(
        "I5", "untranslatable", missing=("entry_level",),
        note="<h|h> ic carpimi ve M00 girdisi dilde yok",
    ),
    RecoveryEntry(
        "I6", "untranslatable", missing=("entry_level",),
        note="iz (trace) dilde yok",
    ),
    RecoveryEntry(
        "I7", "structural",
        note="h2 h1 <-> Z2|h1>: kuaterniyon carpimi = dilin Mul'u (izomorfizm dilin semantigi)",
    ),
    RecoveryEntry(
        "I8", "structural",
        note="Z = kuaterniyonun matris temsili: atom semantiginin tanimi",
    ),
    RecoveryEntry(
        "I9", "untranslatable", missing=("stokes_sort", "dagger"),
        note="Stokes sort'u ve Z^dagger gerekli",
    ),
    RecoveryEntry(
        "I10", "translatable",
        pairs=(
            _p(Mul(_A, Conj(_B)), Mul(Conj(_B), _A)),           # commutation
            _p(
                Mul(Mul(_A, _B), Conj(Mul(_A, _B))),             # M(Z2 Z1) = M2 M1
                Mul(Mul(_A, Conj(_A)), Mul(_B, Conj(_B))),
            ),
        ),
        note="komutasyon aksiyom-duzeyinde; seri Mueller yasasi TURETILIR",
    ),
    RecoveryEntry(
        "I11", "untranslatable", missing=("constants", "interpreted_scalars"),
        note="R(theta) sabiti ve trigonometrik skalerler yok",
    ),
    RecoveryEntry(
        "I12", "untranslatable", missing=("guarded_atoms", "entry_level"),
        note="hermitsel-durum kisiti (reel parametre) ve M = M^T girdi deseni",
    ),
    RecoveryEntry(
        "I13", "untranslatable", missing=("guarded_atoms", "dagger", "entry_level"),
        note="uniter-durum kisiti ve M M^T carpimi",
    ),
    RecoveryEntry(
        "I14", "untranslatable", missing=("dagger", "entry_level"),
        note="H = |h><h| dis carpimi ve iz formulu",
    ),
    RecoveryEntry(
        "I15", "translatable",
        pairs=(
            _p(_I15_LHS, _I15_RHS),          # 4-term expansion, nested-Scale form
            _p(_I15_CROSS, Conj(_I15_CROSS)),  # cross-term reality (M26: all coefficients)
        ),
        note="Asama 7 Sum/Scale ile kazanildi: acilim + capraz-terim gercelligi, "
             "opak (evrensel-nicelenmis) katsayilarla — makalenin Eq.(10)'u da "
             "keyfi a,b icin kurulur, birebir sadik ceviri",
    ),
    RecoveryEntry(
        "I16", "untranslatable", missing=("interpreted_scalars",),
        note="iskelet (Sum/Scale) artik dilde; ama e^{i phi} SABIT birim-modul "
             "skaleri ve 1+cos(phi) aritmetigi yorumlanan skaler ister (M26)",
    ),
    RecoveryEntry(
        "I17", "untranslatable", missing=("interpreted_scalars", "entry_level"),
        note="konveks karisim REEL agirliklar (w1+w2=1) + kovaryans haritasi ister",
    ),
    RecoveryEntry(
        "I18", "untranslatable", missing=("interpreted_scalars", "constants"),
        note="ozel polarizor durumlari ve (1+i)/2 SABIT katsayilari",
    ),
    RecoveryEntry(
        "I19", "untranslatable", missing=("guarded_atoms", "entry_level"),
        note="(tau, alpha, 0, 0) kisitli atom + girdi-deseni simetrisi",
    ),
    RecoveryEntry(
        "I20", "untranslatable", missing=("guarded_atoms", "entry_level"),
        note="(tau, 0, beta, 0) kisitli atom + girdi-deseni simetrisi",
    ),
    RecoveryEntry(
        "I21", "untranslatable", missing=("guarded_atoms", "entry_level"),
        note="(tau, 0, 0, gamma) kisitli atom + girdi-deseni simetrisi",
    ),
)


@dataclass
class CampaignResult:
    recovered: list[str] = field(default_factory=list)
    structural: list[str] = field(default_factory=list)
    untranslatable: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)

    @property
    def complete(self) -> bool:
        """Every translatable identity fully recovered (K20)."""
        return not self.failures


def run_recovery_campaign(engine: DiscoveryEngine | None = None) -> CampaignResult:
    """Prove every translatable pair through all three layers (K20)."""
    engine = engine or DiscoveryEngine(
        atom_names=("a", "b"), scalar_names=("p", "q")
    )
    result = CampaignResult()
    for entry in RECOVERY_TABLE:
        if entry.status == "structural":
            result.structural.append(entry.identity_key)
            continue
        if entry.status == "untranslatable":
            result.untranslatable.append(entry.identity_key)
            continue
        if entry.status != "translatable":  # M20-style runtime guard
            raise ValueError(
                f"unknown recovery status {entry.status!r} for {entry.identity_key}"
            )
        ok = True
        for left, right in entry.pairs:
            layers = {
                "proof": engine.provable(left, right),
                "numeric": terms_numerically_equal(
                    left, right, engine.atom_names,
                    scalar_names=engine.scalar_names,
                ),
                "symbolic": terms_symbolically_equal(
                    left, right, engine.atom_names,
                    scalar_names=engine.scalar_names,
                ),
            }
            if not all(layers.values()):
                ok = False
                failed = ",".join(k for k, v in layers.items() if not v)
                result.failures.append(
                    f"{entry.identity_key} [{failed}]: "
                    f"{left.render()} == {right.render()}"
                )
        if ok:
            result.recovered.append(entry.identity_key)
    return result
