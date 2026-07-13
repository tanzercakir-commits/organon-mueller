# AŞAMA 0 — Repo İskeleti + Temsil Katmanı + Bilinen-Özdeşlik Regresyon Çekirdeği

**Tarih**: 2026-07-13
**Proje**: organon-mueller (Organon_V2)
**Önceki aşama**: — (ilk aşama)

---

## 1. Bağlam

Organon v1 (FOL tabanlı fizik akıl yürütme sistemi, frozen-55, `v1.0`) kapandı. v2'nin
sub-problem'i: **Stokes-Mueller polarizasyon formalizminde otomatik özdeşlik keşfi**
(automated identity discovery). Domain referansları: Kuntman ve ark. 2016–2020 yayınları
(JOSA A 34,80; PRA 95,063819; PRB 98,045410; Applied Optics 55,2543; JOSA A kuaterniyon).

v2'nin mantık çerçevesi: FOL'un **denklemsel fragmanı** (equational logic, Birkhoff
kuralları) + **Horn-koşullu kurallar** (P(x) → t₁ = t₂). Keşif motoru (egglog) sonraki
aşamalarda; bu aşama motorun üstünde koşacağı zemini döker.

## 2. Hedefler

1. Repo iskeleti: `specs/`, `reports/`, `src/organon_mueller/`, `tests/`, CI.
2. **Temsil katmanı**: altı izomorf temsil — Jones J (2×2), Mueller M (4×4),
   kovaryans matrisi H (4×4 Hermitian), kovaryans vektörü |h⟩ = (τ,α,β,γ)ᵀ,
   Z matrisi (4×4), h bikuaterniyonu — ve aralarındaki dönüşümler.
3. **Bilinen-özdeşlik kütüphanesi (çekirdek)**: literatürdeki temel özdeşlikler,
   kaynak + yan koşul (guard) metadata'sıyla kayıtlı.
4. **Regresyon testleri**: her bilinen özdeşlik sembolik (SymPy) ve/veya sayısal
   (NumPy rastgele örneklem) olarak doğrulanır. Hedef: bilineni %100 kurtarma.
5. CI: GitHub Actions, her push'ta pytest.

## 3. Mimari kararlar

- **M1. Kaynak temsil |h⟩**: içsel durum (τ,α,β,γ) dörtlüsüdür; diğer beş temsil
  bundan üretilir. Gerekçe: rank-1 H ↔ |h⟩ birebir; Z, J, h hepsi aynı parametrelerle
  lineer.
- **M2. Çifte doğrulama**: her özdeşlik önce sembolik denenir; sembolik maliyetliyse
  sayısal örneklem (N≥50 rastgele karmaşık parametre, tol=1e-9) kabul edilir. Hangi
  modda doğrulandığı identity kaydında tutulur.
- **M3. Yan koşullar birinci sınıf**: her özdeşlik `conditions` alanı taşır
  (örn. `nondepolarizing`, `tau_real`, `unitary`). Horn-koşullu kural altyapısının
  tohumudur.
- **M4. API durumsuz ve serileştirilebilir**: fonksiyonel çekirdek; girdi/çıktılar
  SymPy ifadeleri/matrisleri. İleride MCP server sarmalaması için JSON köprüsü
  sonraki aşamalarda.
- **M5. Konvansiyonlar Kuntman-Arteaga makalelerine sabitlenir**: Pauli sırası
  (σ0,σ1,σ2,σ3), A matrisi, Z'nin açık formu, kuaterniyon işaretleri JOSA A 34,80
  ve arXiv:1705.07147'deki gibi. Farklı konvansiyonlu literatür (Gil vb.) dönüşümle
  eşlenir, çekirdek değişmez.
- **M6. egglog bu aşamada YOK**: keşif motoru Aşama 2+ (önce spike). Bu aşama
  yalnızca zemin.

## 4. Katı kurallar

- K1. Test edilmemiş hiçbir dönüşüm/özdeşlik `main`'e girmez.
- K2. Sayısal testlerde sabit tohum (seed) — CI deterministik olmalı.
- K3. `src/organon_mueller` içinde print/side-effect yok; saf fonksiyonlar.
- K4. Python ≥3.10; bağımlılık: sympy, numpy (test: pytest). Başka bağımlılık eklenmez.
- K5. Dosya/dizin adları bu spec'teki gibi; runner-dokunulmazlığı ilkesi burada
  "temsil katmanı API'si dokunulmaz" olarak devam eder (Aşama 1+'da imzalar değişmez,
  yalnızca eklenir).

## 5. Teslim

```
organon-mueller/
├── README.md                       (proje tanıtımı, v1 bağı, durum)
├── pyproject.toml                  (src-layout, pip install -e ".[test]")
├── .gitignore
├── .github/workflows/ci.yml        (pytest, py3.11 + py3.12)
├── specs/stage-00.md               (bu dosya)
├── reports/stage-00-REPORT.md
├── src/organon_mueller/
│   ├── __init__.py                 (sürüm + üst düzey API dışa aktarımı)
│   ├── algebra/
│   │   ├── __init__.py
│   │   ├── basis.py                (Pauli, A, Πij, kuaterniyon baz matrisleri 1,I,J,K)
│   │   ├── quaternion.py           (BiQuaternion: Hamilton çarpımı, bar/†, matris temsili)
│   │   └── states.py               (HVector + tüm dönüşümler + Stokes yardımcıları)
│   ├── conditions.py               (yüklemler: nondepolarizing, hermitian_state, unitary_state)
│   ├── verify.py                   (sembolik/sayısal doğrulama yardımcıları, örnekleyici)
│   └── identities/
│       ├── __init__.py
│       └── known.py                (Identity kaydı + KNOWN_IDENTITIES kütüphanesi)
└── tests/
    ├── test_basis.py
    ├── test_quaternion.py
    ├── test_isomorphisms.py
    ├── test_known_identities.py
    └── test_conditions.py
```

## 6. Doğrulama (bu aşamanın "bilineni kurtarma" listesi)

| # | Özdeşlik | Kaynak | Koşul | Mod |
|---|---|---|---|---|
| I1 | M = ZZ\* = Z\*Z | JOSA A 34,80 Eq.(34) | nondepolarizing | sembolik |
| I2 | M = A(J⊗J\*)A⁻¹ ile I1 tutarlı | standart + Eq.(35) | — | sembolik |
| I3 | det Z = (τ²−α²−β²−γ²)² | JOSA A 34,80 Eq.(48) | — | sembolik |
| I4 | Z⁻¹ açık formu (işaret çevirme) | Eq.(50) | det≠0 | sembolik |
| I5 | ⟨h|h⟩ = M₀₀ | Eq.(17) | — | sembolik |
| I6 | tr(MᵀM) = 4M₀₀² | Gil-Bernabeu | nondepolarizing | sayısal |
| I7 | h₂h₁ ↔ Z₂|h₁⟩ (kuaterniyon çarpımı) | arXiv:1705.07147 Eq.(21-23) | — | sembolik |
| I8 | Z = τ1+iαI+iβJ+iγK (matris temsili = Z) | Eq.(13) | — | sembolik |
| I9 | s′ = hsh† ↔ |s′⟩ = M|s⟩ ve S′ = ZSZ† | Eq.(10),(26) | — | sayısal |
| I10 | Z_iZ_j\* = Z_j\*Z_i (komütasyon) → M(Z₂Z₁)=M₂M₁ | JOSA A 34,80 Eq.(38) | — | sembolik+sayısal |
| I11 | Rotasyon: |h(θ)⟩=R(θ)|h⟩, h(θ)=rhr†, M(θ)=R(θ)MR(−θ) | Eq.(30-34) | — | sayısal |
| I12 | Hermitsel durum: τ,α,β,γ ∈ ℝ ⇒ M = Mᵀ | Eq.(46),(53) | hermitian_state | sayısal |
| I13 | Üniter durum: τ∈ℝ, α,β,γ∈iℝ ⇒ MMᵀ = M₀₀²·I | Eq.(54-56) | unitary_state | sayısal |
| I14 | Rank(H)=1 ⇔ nondepolarize; H=|h⟩⟨h|; Mij=tr(ΠijH) | Cloude/Gil | — | sayısal |

Kabul ölçütü: 14/14 doğrulanır; pytest tamamı yeşil; CI dosyası sözdizimsel geçerli.

## 7. Teslim formatı

Dosyalar kullanıcının `C:\Projects\organon-mueller` klonuna yazılır +
`reports/stage-00-REPORT.md` sonuç raporu + önerilen commit mesajı. Push kullanıcıda.

## 8. Özel uyarılar

1. SymPy'da karmaşık eşlenik: parametreler `sympy.symbols(..., complex=True)` ile;
   `conjugate()` kullan, `.T` yerine `.H`'ye dikkat (H = conjugate transpose).
2. Kuaterniyon Hermitsel eşleniği h† = τ\*1+iα\*i+iβ\*j+iγ\*k — bileşen bazında
   naif `conjugate` DEĞİL (bkz. bikuaterniyon: h† = conj(bar(h)) bileşenleri).
3. Sayısal rank testi: eşik 1e-9·λ_max; mutlak eşik kullanma.
4. R(θ) 2θ'lıdır (Mueller uzayı); kuaterniyon rotator r = cosθ·1 + sinθ·k
   (arXiv Eq.(33)) — θ/2 karışıklığına dikkat.
5. Windows klonu: dosyalar LF ile yazılır; .gitignore'a `__pycache__`, `.pytest_cache`,
   `*.egg-info`, `.venv` eklenir.

## 9. Kapsam dışı

- egglog / keşif motoru (Aşama 2+, önce spike)
- Ayrışım türetici, dipol modülü (Aşama 3+)
- MCP server / web UI / LaTeX rapor üretici (paketleme aşamaları)
- LICENSE seçimi (kullanıcı kararı — repo private, aciliyet yok)
- Depolarize M için genel rank-2/3/4 işlemleri (yalnızca yüklem düzeyi var)

**DUR BURAYA** — bu spec dışına çıkma; belirsizlikte REPORT'a "açık soru" yaz.
