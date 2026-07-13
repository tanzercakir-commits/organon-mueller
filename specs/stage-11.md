# AŞAMA 11 — İter + Kuntman Feedback Penceresi #1 (Faz C kapanışı)

**Tarih**: 2026-07-13 · **Önceki**: stage-10 (rank-3 + köprü v0) · **Mod**: otonom
**Probe notu**: bu aşamada yeni kampanya/tarama hedefi YOK → spec-öncesi
sayısal probe gerekmiyor (kural yerinde duruyor).

---

## 1. Hedefler

### (a) Faz C retrospektifi
`docs/phase-c-retrospective.md`: A8-A10 kararlarının (M28-M34) ve katı
kuralların (K26-K32) tutarlılık taraması; teknik borç envanteri; dersler
(probe-before-spec'in iki kazanımı; pytest-pipe ihlalinin kendi kendine
yakalanışı; teklik-dışılık bulgusunun çerçevelenmesi).

### (b) Birikmiş yükümlülükler — uygula veya GEREKÇELİ ertele
1. **UYGULA — köprü v1 ön-sıralama**: `propose_decompositions`'a ucuz
   yapı-skoru: hipotezin türetilmiş ifadelerinin payda büyüklüklerinin
   min'i (makalenin "büyük payda = sayısal sağlık" tavsiyesinin
   genellemesi). SADECE SIRALAR — eleme yine kesin çözücülerde ve
   gerekçeli (K21). Skorlar rapora girer (`ProposeReport.scores`).
2. **UYGULA — guard-üreteç sadakati meta-testi**: GUARD_KEYS'e eklenen
   her yeni anahtar, sayısal VE sembolik üreteci olmadan test edilemez
   (tasarım-notu yükümlülük 1'in yapısal hali).
3. **ERTELE — rank-3 a/b minor varyantları** (M33): kanonik set + net
   guard mesajları duruyor. Gerekçe: varyant paydaları yalnız ölçü-sıfır
   dejenerasyonlarda ayrışıyor (ör. u₁=0 vs u₂=0); ölçülmüş/gürültülü
   gerçek veri bu noktalara tam oturmaz, toleranslar mevcut; deneysel
   veri geldiğinde (Kuntman penceresi sonrası) açılır.
4. **ERTELE — interpreted_scalars payda yan-koşulları** (tasarım-notu
   yükümlülük 2): özellik dilde henüz YOK (K19 anahtarı); koşullu borç
   olarak retrospektife kaydedilir.
5. Stage-10 denetçi önerileri: hepsi stage-10 kapanışında uygulandı
   (primary="center" inşa, sonluluk guard'ları, K32/u₀=u₃/çapraz-çift
   testleri, sıfır-matris guard'ı) — retrospektifte doğrulanır.

### (c) Kuntman feedback paketi (dış temas YOK — gönderim kullanıcıda)
`docs/kuntman-package/`: `README-tr.md` + `README-en.md` (ne
otomatikleştirildi: Tablo 1-4 türetimleri; §6 örneği baskı hassasiyetinde
+ 2 baskı-hatası teşhisi; rank-3 ADAY sonuçlar + teklik-dışılık gözlemi;
doğrulama sözleşmesi özeti; geri-bildirim soruları) + `demo.py`
(çalıştırılabilir: §6 ayrışımı, rank-3 roundtrip, köprü skorlarıyla) +
smoke test. Dil: "aday/candidate" — İDDİA YOK; novelty-protocol adım 5
vurgusu her iki dilde.

### (d) VERIFICATION.md güncellemesi
Faz C eklerini katmanlara işle: spec-öncesi probe kuralı; M34 (makale
çapası olmayan bölgede üç-katmanlı ikame); K32-tipi fazladan-belirlenim
guard'ları; çalışma-zamanı invariant guard'ları. Katman zayıflatma YOK
(sadece ekleme — kritik-karar tetiklenmez).

## 2. Kabul

- Köprü skorları: tüm denenen hipotezlerde mevcut + deterministik; doğru
  hipotezin skoru sonlu-pozitif; başarı kümesi skorsuz haliyle AYNI
  (sıralama davranışı değiştirir, sonuç kümesini değiştirmez).
- Meta-test: GUARD_KEYS ↔ üreteçler birebir.
- demo.py smoke testi: §6'da α₁=0.3'ü ~1e-3'te, rank-3 sentetikte kesin
  geri kazanımı doğrular.
- 149 eski test yeşil; retrospektif + paket + VERIFICATION güncel.

**DUR BURAYA**
