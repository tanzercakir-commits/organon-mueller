# AŞAMA 13 — RAPOR (γ Yön-Genel Otomasyonu, Faz D 2/4)

**Tarih**: 2026-07-13 · **Spec**: `specs/stage-13.md` · **Mod**: otonom
**Sonuç**: TAMAMLANDI — 192/192 test yeşil; **Symmetry 12, 1790 (2020)
App. A genel geometrisi türetildi (Eq. A11 sembolik birebir), Perrin
karşılıklılık teoremi HER J için sembolik ispatlandı, γ'nın yön/faz
haritası teorem düzeyinde kapandı.**

## 1. Teslim edilenler (`dipoles/general.py`)

- **Genel çözüm**: skaler-indirgemeli kuple sistem (M28) → `forward_jones
  _general` == **Eq. A11 (elle-girilmiş çapa, K28)**; A12 özel durumu;
  probe faz-muhasebesini çözdü: T = e₂p₁+p₂ (denetçi fiziksel yol
  fazlarıyla teyit etti: makalenin A11'i global e₂ taşıyor — docstring'de).
- **Karşılıklılık**: R(J) = σJᵀσ (Eq. 1 deseni + involüsyon); türetilmiş
  JA = g[[0,0],[µ,1]], JB = g[[0,−µ],[0,1]] çapaları; **JB == R(JA)
  teoremi** (iki taraf bağımsız türetilerek — inşa gereği değil).
- **Perrin teoremi (genel, sembolik)**: amp_B = (σu*)†R(J)(σv*) == v†Ju
  → I_B = I_A, HER J için; makalenin Eq. 8-13 eliptik-polarizör özel
  durumu ayrıca çapalı (I_B = (|x|²+|y|²)·I_A — Eq. 13 birebir).
- **γ-haritası teoremi**: h₄ = i·e₁α₁α₂Δ₁(1−e₂²)/(2N); sıfır kümesi TAM
  (denetçi doğruladı): kuplaj yok ∨ Δ₁=0 (θ=±π/2 kuplajlı-ama-kör dal
  test edildi) ∨ e₂²=1 (eş-düzlem / λ/2 ofsetleri ileri-yönde γ-kör).
  90° yönde h₄(JA) = −igµ/2 ≠ 0 (asimetrik saçılım imzası — bilinen
  gerçek, yenilik iddiası yok).
- **K33 adlandırma uyarısı**: Symmetry-makalesi δ₁ₛ/δ₂ₛ ≠ PRB δ₁/δ₂
  (adaş, farklı nesneler) — modülde `_s` soneki + docstring.
- **M36 sentineli**: φ₁=−π/2, e₁=e₂=1 konfigürasyonunda genel çözücü ==
  stage-12 PRB ayrışımı (δ₁=A, δ₂=A+B eşlemesiyle); u→−u değişmezliği
  denetçi teyitli.

## 2. Bağımsız denetim

Verdict: **PASS** (2 LOW + 1 kozmetik — hepsi giderildi: A11 çapası
tümüyle elle-yazılı hale getirildi + symmetry_deltas ayrı teste alındı;
sayısal katmanda kompleks açı sessiz-kırpılması yerine açık ret;
kullanılmayan unpack temizliği; θ=π/2 kuplajlı-kör dal testi). Denetçi:
tam 3D dyadic Green 6×6 çözümüyle xy-blok indirgemesinin KESİN olduğunu
ispatladı (rank-1 düzlem-içi projektörler (û·p)û'nun z-bileşenini yok
ediyor); A11'i PDF'ten kendisi yazıp birebir buldu; JA/JB'yi ham 3D
ışımadan yeniden türetti; Perrin σ-kimliğini ve γ sıfır-kümesinin
tamlığını doğruladı.

## 3. Sıradaki aşama (otonom devam)

**Aşama 14 — N-dimer / ensemble genellemesi**: spec öncesi proje dosyası
OAinanenseble.pdf okunacak; N kuple dipolün skaler-indirgeme yapısının
genelleşmesi + ensemble ortalamasının kovaryans/Mueller karşılığı
(depolarizasyon köprüsü — ayrışım katmanıyla ilk fiziksel bağlantı adayı).
