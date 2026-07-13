# AŞAMA 3 — Enumerasyon Ölçekleme + Hasat Boru Hattı v1 (Faz B)

**Tarih**: 2026-07-13 · **Önceki**: stage-02 (motor v0, FROZEN-22)
**Mod**: otonom (manda 2026-07-13)

---

## 1. Bağlam

v0 hasadının darboğazı `extract` (boyut 9'da ~21 sn; saturasyon 0.15 sn).
Ayrıca v0, e-graph'ın ZATEN ispatladığı denklikleri hasat ediyordu — "sayısal
olarak doğru ama aksiyomlardan türetilemeyen" çiftleri görme yeteneği yoktu.
Oysa Faz B'nin asıl hedefi tam o boşluk: türetilemeyen doğru denklik =
potansiyel yeni özdeşlik / eksik aksiyom sinyali.

## 2. Hedefler

1. **Boru hattı v1 (tersine akış)**: sayısal parmak izi (fingerprint) aday
   ÜRETİR → e-graph türetilebilirliği İSPATLAR → bağımsız çok-tohumlu sayısal
   doğrulama ONAYLAR. Sınıflandırma:
   - `verified`: ispatlı + doğrulanmış
   - `refuted`: ispatlı ama sayısal yanlış (ALARM — unsound aksiyom, build kırar)
   - `underivable`: sayısal doğru ama aksiyomlardan türetilemedi (BULGU —
     yenilik/eksik-aksiyom tohumu; Aşama 5-6'nın girdisi)
   - `fingerprint_collisions`: kaba anahtar çakışması, sayısal elemede düştü (normal)
2. **conj-normal (budanmış) enumerasyon**: Conj yalnız atom seviyesinde —
   conj(conj(x)) ve conj(x·y) formları üretimden çıkar (e-graph fodder'ı
   azalır); özdeşlik içeriği normal formda korunur.
3. **Ölçüm**: boyut 7/8/9, budanmış/budanmamış: terim sayısı, saturasyon,
   hasat süreleri — rapora tablo.
4. Extract tabanlı `_bucket_by_class` v1'de kalkar (`extraction_collisions`
   alanıyla birlikte); check-tabanlı kabul testleri (R1-R3, negatifler) aynen korunur.

## 3. Mimari kararlar

- **M18 (uygulama sırasında eklendi). İspatlar yalıtılmış çift-grafında**:
  paylaşılan büyük e-graph, egglog 13.2.0'da tutarsız check/extract davranışı
  gösterdi (farklı atom-çokkümesine düşen extract temsilcisi; yalıtımda
  ispatlanan çiftin büyük grafta ispatlanamaması — repro:
  `spikes/egglog_pathology_probe.py`, analiz:
  `docs/egglog-large-graph-pathology.md`). v1.1'de her aday çift kendi taze
  iki-terimli grafında sature edilip kontrol edilir; paylaşılan graf kalktı.
  Ses zaten sayısal doğrulamaya dayanıyordu (M10); patolojiyi de o katman
  yakaladı.

- **M15. Parmak izi = aday üreteci, ASLA kanıt**: kaba anahtar (tek sabit
  atama, 3 ondalık yuvarlama) yalnız kovalama içindir. Yanlış-birleşme →
  sonraki katmanlar eler; yanlış-ayrılma (sınır titremesi, ~1e-4'ten yakın
  yuvarlama sınırı) → yalnız tamlık kaybı. Ses garantisi parmak izine hiçbir
  noktada dayanmaz.
- **M16. `underivable` birinci sınıf çıktı**: sessizce yutulmaz, sayılır ve
  raporlanır; `sound` tanımına DAHİL DEĞİL (ses = refuted boş).
- **M17. discovery API'si Faz B boyunca evrilebilir** (v0→v1); Aşama 7'de
  dondurulur. Aşama 0-1 API'leri (K11) değişmez.

## 4. Katı kurallar

- K13. `verified` yalnız ispat+doğrulama kesişimi; `underivable` hiçbir
  sayaçta "keşif" olarak sunulmaz, ayrı raporlanır.
- K14. Parmak izi ataması ve doğrulama tohumları FARKLI (bağımsızlık).
- K15. Benchmark sayıları rapora ölçüldüğü ortam notuyla girer.

## 5. Teslim

- `discovery/fingerprint.py`, `engine.py` v1, `terms.py` (conj_normal parametresi)
- `tests/test_discovery.py` güncel (yeni sınıflandırma + budanmış enumerasyon
  özellik testleri + R3'ün conj-normal karşılığının hasatta çıkması)
- `spikes/bench_stage3.py` + rapor tablosu
- `reports/stage-03-REPORT.md`

## 6. Doğrulama

- R1-R3 testleri (M18 gereği yalıtılmış çift-graflarında) AYNEN yeşil.
- v1 tam koşu (conj-normal, boyut 9): R2 çifti ve R3'ün conj-normal formu
  ((a·b)·(conj(a)·conj(b)) ≡ (a·conj(a))·(b·conj(b))) `verified` içinde.
- `refuted` boş; `underivable` bu fragmanda beklenen: boş (değilse ön-inceleme
  yapılır, bulgu rapora yazılır; boş değilken de aşama geçebilir — K13).
- Hasat: ölçülen (bu ortam, v1.1 yalıtılmış ispatlar) — budanmış boyut 9:
  1476 terim, 128 kova, 1348 verified, 0 underivable/refuted, ~30 sn (tam
  sınıflandırma dahil; v0'ın 21 sn'lik extract'i yalnız gruplamaydı ve
  underivable görüsü yoktu). İlk taslaktaki "<5 sn" hedefi v0 extract'inin
  yerine geçen kovalama içindi; v1.1'de süre ispat çağrılarına gidiyor —
  bilinçli takas: hız yerine güvenilirlik.

## 7-9. Teslim formatı / Uyarılar / Kapsam dışı

Push + rapor + Aşama 4 planlaması. Uyarı: parmak izi anahtarında mutlak
yuvarlama (3 ondalık) magnitude ~10 değerler için yeterli; skaler katsayılar
gelince (Faz B ilerisi) ölçek-göreli anahtara geçilecek. Kapsam dışı: skaler
terimler, kanonik form maliyet fonksiyonu, literatür karşılaştırma.

**DUR BURAYA**
