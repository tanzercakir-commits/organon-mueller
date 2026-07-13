# AŞAMA 14 — N-Dimer / Ensemble Genellemesi (Faz D 3/4)

**Tarih**: 2026-07-13 · **Kaynak**: "OA in an ensemble of randomly oriented
chiral and achiral plasmonic dimers" (Kuntman & Kuntman, proje PDF'i) ·
**Mod**: otonom

## 0. Probe (ZORUNLU — yapıldı: probes/probe-ensemble-prespec.py)

- **Q1-Q2 ✓** 3D skaler indirgeme (rank-1 projektörler; sürüş fazları
  e^{∓ikr_z/2}) == Eqs. 21-24; ileri Jones == Eqs. 26-29; γ_z formülü
  doğru AMA **etiket kayması (M30 #5)**: γ_z = −2µαδ·**(n×m)_z**·sin(kr_z)
  — makale "(m×n)_z" yazıyor ((n×m)_z hatası 2.7e-17, (m×n)_z 2.2e-2).
- **Q3 ✓** γ_x == Eq. 33 birebir (x′=−z, y′=y çerçevesi + r_x fazları);
  iki-terim ayrımı (γx1 kuplajdan bağımsız — metasurface noktası) ✓.
- **Q4 — M30 #6**: Eq. 9'un basılı öneki −2iεαµ YANLIŞ (µ = εα/(1−(αδ)²)
  zaten εα içerir); türetilen doğru önek **−2iµ** (sayısal: printed=False,
  mu-only=True). Köşeli parantez içeriği doğru.
- **Q5 ✓** ensemble iddiaları (4000 örnek, tohumlu): akiral Σγ_z/N ~ 3e-4
  (≈1/√N gürültüsü), kiral+kuplajlı 2.6e-2 ≠ 0, kuplajsız γ_z ≡ 0
  noktasal (1e-19). Rijit dimerde δ rotasyon-değişmezi (iç çarpımlar
  korunur) — makalenin "µ,α,δ oryantasyona bağlı değil" notunun gerekçesi.
- **K33**: makalenin γ'sı = i(J₁₂−J₂₁) = 2×HVector.gamma (½'siz).

## 1. Hedefler — `dipoles/ensemble.py`

1. `coupling_delta_3d(m,n,u,A,B)` = (n·m)A + (n·u)(m·u)B (M28, Green).
2. Sembolik türetimler + K28 çapaları: `forward_jones_3d` (Eqs. 26-29),
   `gamma_z_3d` (Eq. 31, (n×m)_z etiket notu), `transverse_jones_3d` →
   γ_x (Eq. 33 + 34-35 ayrımı), `backscatter_jones_3d` → γ₋z (DÜZELTİLMİŞ
   önekle; M30 #6 notu). δ=0 ⇒ γ_z ≡ 0 sembolik teorem.
3. `is_chiral(m,n,r)` (m×n·r ≠ 0) + sayısal katman `jones_3d_numeric`
   (K26: sonluluk + rezonans guard'ı |1−(αδ)²|).
4. `ensemble_gamma(direction, chiral, d, ...)`: tohumlu deterministik
   ortogonal-dimer ensembles (Fig. 2 geometrisi r = d(m−n+z)/√3, akiral
   Z=0) — Q5 iddiaları test olarak.
5. **Depolarizasyon köprüsü (İLK uçtan-uca)**: `ensemble_covariance` =
   ⟨|h⟩⟨h|⟩ (bizim ½'li HVector'le), iz-normalize → rank>1 PSD; iki-
   oryantasyon karışımı rank-2 → `propose_decompositions`'a beslenir
   (K21: sonuç GEREKÇELİ — başarı şart değil, kompozisyon ve guard'ların
   çalışması şart).

## 2. Karar

**M37**: ensemble modülü dimer/general modüllerine dokunmaz; γ tanımı
makale konvansiyonunda (2×h₄) `gamma_paper` adıyla — HVector.gamma ile
karışmaz (K33).

## 3. Kabul

Eqs. 21-24/26-29/31/33 çapaları sembolik; Eq. 9 düzeltilmiş-önek çapası
(M30 #6 gerekçeli); δ=0 teoremi; kiralite yüklemi; ensemble Q5 üçlüsü
(tohumlu, N=800 CI-hızlı); köprü testi (rank-2 PSD iz-1 + gerekçeli
propose raporu); K26 guard'ları; 192 eski test yeşil.

**DUR BURAYA**
