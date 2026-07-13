# AŞAMA 10 — RAPOR (Faz C: Rank-3 Üç-Terimli Ayrışım + Keşif Köprüsü)

**Tarih**: 2026-07-13 · **Spec**: `specs/stage-10.md` · **Mod**: otonom
**Sonuç**: TAMAMLANDI — 149/149 test yeşil; **makale-ötesi bölgede ilk
sonuçlar**: üç çift için rank-3 ayrışım türetildi (probe-doğrulamalı el
formülleriyle sembolik birebir + denetçinin bağımsız türetimleriyle
birebir), **teklik-dışılık bulgusu** kapalı formda doğrulandı, keşif→minor
köprüsü v0 çalışıyor.

---

## 1. Teslim edilenler

- **`decomposition/rank3.py`**: `H = α_A·H_A + α_B·H_B + α_G·|u⟩⟨u|`.
  - {1,2} ve {1,3}: SIRALI PEEL — tip-1'in desteği yalnız köşeler; B'nin
    merkez parametresi merkez minöründen, kenarı kenar minöründen LİNEER
    çözülür (yapısal guard: seçili minörler çözülmemiş bileşene DEĞEMEZ —
    K31); B çıkarılır, kalan stage-8 çözücüsüne DELEGE edilir (onun tüm
    guard'ları miras — M33 tek yönlü katmanlama).
  - {2,3}: destekler tam örtüşür → KOMBİNASYON DEĞİŞKENLERİ (σ,p,m,s,d);
    beş minör SIRAYLA lineer; geri-inşadan sonra **k₂+e₃=σ fazladan
    belirlenimi ZORUNLU tutarlılık guard'ı (K32)**.
  - `propose_decompositions` (köprü v0): rank'e göre tüm hipotezleri
    dener; başarısızlıklar GEREKÇELİ (K21 — sessiz eleme yok).
  - `sweep_rank3` → `reports/sweep-03-rank3.json`: 12/12 sentetik geri
    kazanım (en kötü α hatası 2.4e-15), negatif kontroller gerekçeli.
- **`probes/probe-rank3-prespec.py`**: spec-öncesi probe repoya alındı
  (spec §0'ın kanıtı; tip-3 kenar formülündeki işaret hatasını probe
  yakaladı — mekanizma yine çalıştı).

## 2. Ana bulgu: TEKLİK-DIŞILIK (aday gözlem — iddia değil)

İki tip-2 saf + jenerik olarak KURULAN veri, {1,2} hipotezi altında da
KESİN geçerli bir ayrışım verdi (rekonstrüksiyon 3e-17; tüm bileşenler
saf/PSD). Denetçi kapalı formunu çıkardı: T₁(P=W=P̄=δ/K̄)+T₂′, δ=KK̄−|W|²,
α₁=2δ/K̄ — kod çıktısıyla 1e-16'da eşleşti. **Sonuç çerçevesi**: rank-3'te
çözüm "*bir* ayrışımdır, *tek* ayrışım değil"; sweep artefaktı kabul edilen
alternatifleri AYRICA doğrular (`accepted_alternative_verified`), fizik
seçimi insana/novelty-protokolüne kalır. Öte yandan denetçi {2,3} için
tekliği HİPOTEZ-İÇİ analitik ispata yükseltti: beş formül yalnız H'ye
bağlı → geçerli her {2,3}+jenerik ayrışımı zorlanmış (tek).

## 3. Bağımsız denetim

Verdict: **PASS** (1 MAJOR + 3 MINOR + 1 DOC — hepsi giderildi):
- MAJOR: K32 guard'ının test kapsamı yoktu → tüm-REEL kovaryans ailesi
  (s,d kendiliğinden reel → realness guard'ları geçer) ile deterministik
  regresyon testi eklendi (tohum 0, |k₂+e₃−σ|=2.8e-02 ile fırlatıyor).
- MINOR: merkez-only saf (kenar w=0, meşru Tablo-1 noktası) dış-birincil
  şablon inşasında sıfır matrise çöküyordu → inşa guard'lı-pozitif
  MERKEZ birincille yapılıyor; sınır ailesi artık KESİN çözülüyor (test).
- MINOR: NaN, |iz−1| karşılaştırmalarından sızıp eigvalsh'ta ham çöküş
  veriyordu → üç çözücüye de sonluluk guard'ı; köprü artık gerekçeli
  rapor döndürüyor (test).
- MINOR: çapraz-çift dürüstlüğü 3×2 tam yön matrisine, u₀=u₃ dejenerasyonu
  spec kabulüne uygun teste genişletildi.
- DOC: {2,3}'te asıl eleme yükünü s/d REELLİK kontrollerinin taşıdığı
  (her biri kendi başına bir fazladan belirlenim; K32 daha ince stratumda
  devrede) modül docstring'ine işlendi.
- Denetçinin bağımsız türetimleri: beş {2,3} formülü, iki peel çifti,
  payda≡eksik-anizotropi yorumları ({1,2}: α_G|u₁−u₂|²; {1,3}:
  α_G|u₁+u₂|²; {2,3}: α_G|u₀−u₃|² — ara tekil çarpanlar sembolik
  sadeleşiyor) — HEPSİ birebir eşleşti.

## 4. M34 dürüstlük çerçevesi (kayıt)

Bu bölgede makale çapası YOK; K28'in yerine üç katman kondu: probe'lu el
türetimi (spec §0) + türetici-el sembolik birebirliği (testler) + denetçi
bağımsız türetimi. Yenilik/fizik İDDİASI yapılmadı — sweep notu ve rapor
"aday" der; novelty-protocol 5. adım (insan) değişmedi.

## 5. Sıradaki aşama (otonom devam)

**Aşama 11 — İter + Kuntman feedback penceresi #1** (FROZEN-22, Faz C
kapanışı): Faz C retrospektifi; birikmiş yükümlülükler (rank-3 a/b minor
varyantları, köprü v1 parmak-izi ön-sıralaması, guarded-atoms ikinci yarı
yükümlülükleri); Kuntman'a sunulabilir Türkçe/İngilizce özet paketi
HAZIRLANIR (dış temas YOK — paylaşım kararı kritik-karar protokolüyle
kullanıcıda).
