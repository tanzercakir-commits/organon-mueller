# AŞAMA 12 — Coupled-Dipole Sembolik Motor (FAZ D açılışı)

**Tarih**: 2026-07-13 · **Kaynak**: PRB 98, 045410 (proje PDF'i okundu; Symmetry
12, 1790 (2020) coupled-oscillator eki de okundu — onun e₁/e₂ gecikmeli
geometrisi ve 90° saçılım/karşılıklılık A13 kapsamına) · **Mod**: otonom

## 0. İmplementasyon-öncesi probe (ZORUNLU — yapıldı, probes/'a kopyalanacak)

`scratch/probe_dipoles.py` (tohum 20260713), 6 rastgele kompleks
parametre denemesi:
- **Q1 ✓** 4×4 doğrudan çözüm == kapalı formlar (Eq. 14-17) == ayrışım
  T = γ[α₁J₁+α₂J₂+α₁α₂ΛJ_int] (Eq. 25), ~1e-12.
- **Q2 ✓** det(A) == λ₁λ₂(λ₁λ₂−Λ²) (Eq. 42 yapısı).
- **Q3 ✓** hibrit frekanslar: kuartik kökleri == Eq. 45 kapalı formu;
  özdeş dipoller ω₀√(1±ηΛ) (Eq. 46).
- **Q4 ✓** hibrit baz özdeşliği |t⟩ = ν₊|h₊⟩+ν₋|h₋⟩ ve g₁=g₂ iken
  ⟨h₊|h₋⟩=0 (her φ çiftinde — genel teorem adayı).
- **Q5 ✓** Eq. 70 tersine çözümü (φ₁=90°, φ₂=135°).
- **Q6 — BASKI-FAKTÖRÜ NOTU (M30)**: Eq. 37'nin bileşenleri, makalenin
  KENDİ Eq. 29 (½'li) konvansiyonuna göre 2 kat ölçekli basılı; ½'li
  tutarlı değer h₄ = −(i/2)sin(φ₁−φ₂)(1−e^{iχ}). Yön iddiaları (χ=0 veya
  φ₁=φ₂ → 0; χ=π → salt 4. bileşen) etkilenmiyor — çapa ½'li formda,
  gerekçe testte.

## 1. Hedefler

1. `dipoles/dimer.py`: projektör Jones J(φ); Λ = C₁C₂δ₁+S₁S₂δ₂; 4×4
   kuple sistemin SymPy kurulumu ve çözümü (**M28: T doğrudan sistemden
   türetilir**); ayrışım teoremi T == γ[α₁J₁+α₂J₂+α₁α₂ΛJ_int] sembolik
   KESİN (K28 çapası Eq. 25-27); kovaryans köprüsü `jones_to_hvector`
   (paper Eq. 29 == JOSA A HVector — sentinel test); |h⟩₁/|h⟩₂/|h⟩_int
   çapaları (Eq. 31-32); seri kombinasyon Eq. 33 (4. bileşen i·sin(φ₁−φ₂)
   — kiralite seri dizilimden); dephased J'_int (Eq. 36) + h₄ çapası
   (½'li, M30 notu) — **A13 γ-otomasyonunun zemini**; özel durumlar
   Ta/Tb (Eq. 53-54) çapaları; Λ=0 dejenerasyonu (0°,90°) vs Λ≠0
   (−45°,45°) sentineli.
2. `dipoles/hybrid.py`: Lorentzian α(ω); det yapı TEOREMİ (Eq. 42,
   sembolik); ω± türetimi == Eq. 45/46 (K28); ν±, hibrit baz |h±⟩
   (Eq. 63-64); **genel teoremler (sembolik)**: |t⟩ = ν₊|h₊⟩+ν₋|h₋⟩ her
   (g₁,g₂,g_int,φ₁,φ₂) için; g₁=g₂ ⇒ ⟨h₊|h₋⟩=0 her (φ₁,φ₂) için
   (|h₁+h₂|² = 1+cos²Δφ = |h_int|² kimliğinden); genel katsayı çözümü
   `decomposition_coefficients` (3×3 lineer; tekillik guard'ı — φ₁=φ₂
   bağımlı vektörler) + Eq. 70 özel-durum çapası; I = I⁺+I⁻ (g₁=g₂).
3. Sayısal katman: deterministik rastgele-parametre eşitlik testleri;
   K26 guard'ları (rezonans paydası |1−α₁α₂Λ²|, katsayı-çözümü tekilliği,
   sonlu girdi).

## 2. Kararlar

- **M35**: Dipol modülü ayrışım/keşif katmanlarına DOKUNMAZ; köprü tek
  yönlü (dipoles → algebra.HVector). Symmetry-2020 geometrisi
  (gecikme fazları, 90° saçılım, JA/JB karşılıklılık dönüşümü Eq. 1)
  A13'te; χ-dephasing mekanizması oradaki γ-üretiminin çekirdeği.
- **K33**: PDF-okuma tabanlı her çapa, denklem numarası + varsa
  baskı-faktörü/artefakt notuyla girilir (M30 disiplini sürer).

## 3. Kabul

Ayrışım teoremi sembolik kesin; det teoremi; ω± çapası; hibrit baz
özdeşliği + ortogonallik genel teorem; Eq. 31-33 çapaları; Eq. 70;
Ta/Tb; Λ sentinelleri; dephased h₄ (½ notuyla); konvansiyon sentineli
(Eq. 29 == HVector); sayısal eşitlikler tohumlu; K26 guard'ları; 156
eski test yeşil.

**DUR BURAYA**
