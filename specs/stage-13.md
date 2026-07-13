# AŞAMA 13 — γ Yön-Genel Otomasyonu (Faz D 2/4)

**Tarih**: 2026-07-13 · **Kaynak**: Symmetry 12, 1790 (2020) App. A +
stage-12 dephased mekanizması · **Mod**: otonom

## 0. Probe (ZORUNLU — yapıldı: probes/probe-gamma-prespec.py, tohum 20260713)

- **Q1 ✓ (faz muhasebesi çözüldü)**: Eq. A11'i üreten uzak-alan ağırlığı
  **T = e₂·p₁ + p₂** (5 denemede ~1e-17) — dipol-2 dedektöre r_z kadar
  yakın; makale tek-parçacık terimlerine e₂ taşıyacak biçimde çarpmış.
- **Q2 ✓** skaler indirgeme (p₁ = P₁ŷ, p₂ = P₂n̂(θ), kuplaj skaleri
  n̂ᵢᵀMn̂ⱼ, M = e₁k²(A·I + B·wwᵀ), w=(C₁C₂,S₁)) == tam 2×2 çözüm.
- **Q3 ✓** JA = g[[0,0],[µ,1]], JB = g[[0,−µ],[0,1]] türetimi: skaler
  sistem + ışıma projeksiyonu (+x'e yalnız p_y ışır; −z yerel çerçevesi
  H′=−x işaret çevrimi) — makaleyle birebir; **JB == R(JA)** ✓.
- **Q4 ✓** Genel Perrin: R(J) = σJᵀσ (σ=diag(1,−1)) ile
  amp_B = (σu*)†R(J)(σv*) == v†Ju = amp_A — HER J için (5 deneme kesin).
- **Q5 ✓** İleri-yön γ: h₄ = i·e₁α₁α₂Δ₁(1−e₂²)/(2N); e₂²=1 (aynı düzlem
  veya λ/2 katları) → 0.

**K33 notu**: Symmetry-makalesi δ₁=k²(A+S₁²B), δ₂=k²(C₁C₂S₁B) tanımları
PRB'nin δ₁=k²A, δ₂=k²(A+B) tanımlarından FARKLIDIR (adaş ama başka
nesneler); modülde `delta1_s/delta2_s` adlandırması + docstring uyarısı.

## 1. Hedefler — `dipoles/general.py`

1. `coupling_matrix(phi1, phi2, A, B, e1)` = e₁(A·I₂ + B·wwᵀ) (M28:
   Green'den, tablodan değil); `symmetry_deltas` (δ₁ₛ, δ₂ₛ, Δ₁, Δ₂
   ifadeleri — K33 adlandırması).
2. `solve_dimer_general(theta, phi1, phi2, alpha1, alpha2, A, B, e1, e2, E0)`
   — skaler indirgemeli sembolik çözüm; `forward_jones_general` (T =
   e₂p₁+p₂ muhasebesi) — **Eq. A11 çapası (K28, sembolik birebir)**;
   özel durum Eq. A12 (φ₁=−45°, θ=φ₂=0: J = g[[1,e₁αδ],[e₁αδ,1]],
   δ=−k²B/2) çapası.
3. `reciprocity_transform(J)` = σJᵀσ; özellikler: involüsyon, Eq. 1
   deseni; `case_A_jones/case_B_jones` (90° saçılım, türetilmiş) —
   JA/JB çapaları + **JB == R(JA) teoremi**.
4. **Perrin teoremi (sembolik, genel)**: her J ve normalize u,v için
   amp_B == amp_A (yukarıdaki σ-kimliği) → I_B = I_A; makalenin
   Eq. 8-13 eliptik-polarizör özel durumu ayrıca çapalanır.
5. **γ-haritası**: `forward_gamma_general` — h₄ = i·e₁α₁α₂Δ₁(1−e₂²)/(2N)
   TEOREM (A11'den türetilen J üzerinden, jones_to_hvector ile); sıfır
   koşulları (Δ₁=0 VEYA e₂²=1 VEYA kuplaj yok) sembolik; 90°-yön
   h₄(JA) = −igµ/2 ≠ 0 kaydı (asimetrik saçılımın γ-imzası).
6. K26 guard'ları: sayısal değerlendiricilerde sonluluk + N~0 rezonans.

## 2. Kararlar

**M36**: Symmetry-geometri modülü stage-12 `dimer.py`'ye DOKUNMAZ (PRB
geometrisi aynı-düzlem özel durumdur; tutarlılık testi: e₂=1, θ ve
w-uyumlu konfigürasyonda iki modül aynı J'yi vermeli — sentinel).

## 3. Kabul

Eq. A11 sembolik birebir; A12 özel durumu; JA/JB + JB==R(JA); genel
Perrin sembolik; Eq. 8-13 çapası; γ-teoremi + sıfır koşulları; PRB-uyum
sentineli; K26 guard'ları; 179 eski test yeşil.

**DUR BURAYA**
