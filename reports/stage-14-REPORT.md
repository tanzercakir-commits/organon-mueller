# AŞAMA 14 — RAPOR (N-Dimer / Ensemble Genellemesi, Faz D 3/4)

**Tarih**: 2026-07-13 · **Spec**: `specs/stage-14.md` · **Mod**: otonom
**Sonuç**: TAMAMLANDI — 203/203 test yeşil; **OA-in-ensemble preprint'inin
3D formalizmi türetildi ve çapalandı; İKİ yeni baskı teşhisi (M30 #5-#6)
denetçi tarafından PDF'e karşı teyit edildi; depolarizasyon köprüsü —
dipol fiziği → ayrışım katmanı — İLK uçtan-uca test.**

## 1. Teslim edilenler (`dipoles/ensemble.py`)

- 3D rank-1 skaler indirgeme (M28) — denetçi 6×6 tam çözümle teyit etti;
  δ = (n·m)A + (n·u)(m·u)B; anchors: Eqs. 21-24, 26-29 (ileri Jones),
  Eq. 31 γ_z, Eq. 33 + 34-35 γ_x ayrımı (γx1 kuplajsız limitte hayatta —
  metasurface noktası; makalenin "α ve δ'ya bağlı değil" ifadesinin
  dürüst hali test yorumunda), DÜZELTİLMİŞ Eq. 9 γ₋z.
- **δ=0 ⇒ γ_z ≡ 0 sembolik teorem** (ileri saçılımda kuplajsız kiral
  dimerlerde OA yok — makalenin merkez iddiası).
- Kiralite yüklemi (m×n·r); rijit-dimer δ rotasyon-değişmezliği
  (ensemble sabitliğinin gerekçesi — denetçi 1.6e-16 ile teyit).
- Ensemble istatistikleri (tohumlu, deterministik): kiral+kuplajlı
  Σγ_z ≠ 0; akiral Σγ_z ~ 0 ama Σ|γ_z| ≠ 0 (ideal-olmayan ensemble OA);
  kuplajsız noktasal 0. Eşikler denetçi alt-tohum istatistiğiyle
  genişletildi (numpy akış-kararlılığı garantisizliği notuyla).
- **Depolarizasyon köprüsü**: `ensemble_covariance` = ⟨|h⟩⟨h|⟩ iz-1;
  2-oryantasyon karışımı rank-2 PSD → `propose_decompositions` GEREKÇELİ
  rapor (3 bileşik başarı + 3 gerekçeli ret — K21).

## 2. M30 serisi (bu aşama: #5-#8)

- **#5 Eq. 31**: parantez (n_xm_y−m_xn_y) doğru cebir = **(n×m)_z**;
  etiket "(m×n)_z" işaret-ters (probe + denetçi sembolik).
- **#6 Eq. 9**: önek −2iεαµ basılı; µ = εα/(1−(αδ)²) zaten εα içerir —
  türetilen doğru önek **−2iµ** (εα çift sayımı).
- **#7 Eq. 30**: "i(J₁₂−J₁₂)" — ikincisi J₂₁ olmalı (bariz dizgi).
- **#8 Eq. 32**: fazlarda k düşmüş (e^{ir_x/2} → e^{ikr_x/2}).

## 3. Bağımsız denetim

Verdict: **PASS** (1 MINOR + 2 önemsiz — giderildi: ensemble eşikleri,
kullanılmayan import, boş-örneklem guard'ı; d=|r| vs makale-d notu).
Denetçi: 6×6 tam 3D çözüm ↔ skaler indirgeme (3.3e-16); PDF'ten anchor
doğrulaması; çerçeve el-yönü tutarlılığı (stage-13 ile); Haar-uniform
örnekleme kontrolü; köprü kovaryansını bağımsız yeniden inşa (fark 0.0).

## 4. Sıradaki aşama (otonom devam — Faz D kapanışı)

**Aşama 15 — İter + feedback penceresi #2**: Faz D retrospektifi
(M35-M37, K33 taraması, borçlar); Kuntman paketine dipol eki (PRB +
Symmetry + ensemble bulguları, M30 #3-#8 teşhisleri — GÖNDERİM yine
kullanıcıda); Faz E hazırlığı (LaTeX rapor üreteci + MCP server —
sympify güvenlik kapısı).
