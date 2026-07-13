# AŞAMA 6 — Yeni-Aday Taraması #1 + Yenilik Protokolü (Faz B)

**Tarih**: 2026-07-13 · **Önceki**: stage-05 (geri-kazanım, sınır haritası)
**Mod**: otonom

---

## 1. Bağlam

Motor artık bilineni kurtarıyor; sıra ilk sistematik YENİ-aday taramasında.
Mevcut fragman (atomlar+mul+conj) dar; bu taramanın iki meşru sonucu var:
(a) underivable adaylar çıkar → yenilik protokolüne girer; (b) kanal boş
çıkar → "bu fragman için aksiyom seti ampirik olarak TAM görünüyor" gözlemi
— bu da raporlanabilir bir sonuçtur (negatif sonuç disiplini). "Yeni" iddiası
hiçbir zaman otomatik üretilmez; karşılaştırma yalnız ADAY işaretler.

## 2. Hedefler

1. **`discovery/sweep.py`**: konfigürasyonlu tarama kampanyası —
   `SweepConfig(atom_names, max_size, conj_normal, certify)` →
   `SweepOutcome` (sayılar + underivable render çiftleri + süreler);
   JSON serileştirme (kalıcı kanıt artefaktı `reports/sweep-01-results.json`).
2. **Tarama #1 kapsamı** (ölçülen boyutlara göre; K15 ortam notuyla):
   2-atom pruned-10 (4036 terim) + 3-atom pruned-9 (8331 terim);
   süre bütçesi izin verirse 2-atom pruned-11 (11284) denemesi zaman-kutulu.
3. **`docs/novelty-protocol.md`**: underivable → aday → iddia zinciri:
   kesin sembolik ispat (zaten M19) → kanonik sunum → kütüphane
   karşılaştırması → literatür kontrol listesi (Gil 2007/2014, Cloude 1986,
   Ossikovski hattı, Kuntman korpusu) → uzman (Kuntman) kapısı. Protokol
   İDDİA üretmez; fizik-yorum eşiği (kritik-karar) korunur.
4. **`docs/design-note-addition-scalars.md`**: Aşama 7 spec girdisi —
   Sum düğümü + opak skaler katsayılar (hibrit sınır M10: skaler aritmetik
   SymPy'da; e-graph'ta yapısal aksiyomlar), parmak izinin ölçek-göreli
   anahtara geçişi, enumerasyon patlaması yönetimi (başlangıçta 2-toplamlı),
   kabul hedefleri (I15 açılımı, I16 girişim).

## 3. Mimari kararlar

- **M24. Negatif sonuç birinci sınıftır**: boş underivable kanalı
  "başarısızlık" değil, fragman-tamlık gözlemi olarak JSON artefaktı +
  raporla kayda geçer.
- **M25. Tarama artefaktları repoda**: her tarama kampanyasının özeti
  `reports/sweep-NN-results.json` (deterministik, tekrar üretilebilir
  konfigürasyonla).

## 4. Katı kurallar

- K21. Tarama konfigürasyonları ve tohumlar artefakta gömülür (yeniden
  üretilebilirlik).
- K22. CI testleri küçük konfigürasyonla sınırlı (tam tarama CI'da koşmaz);
  tam tarama sonuçları artefakttan doğrulanır.

## 5-6. Teslim + Doğrulama

`discovery/sweep.py` · `tests/test_sweep.py` (küçük konfig, determinizm,
JSON round-trip, alan bütünlüğü) · `reports/sweep-01-results.json` ·
`docs/novelty-protocol.md` · `docs/design-note-addition-scalars.md` · rapor.
Suite yeşil; tarama sonuçları raporda tablo.

## 7-9.

Push + rapor + Aşama 7 (5 dk). Uyarı: derin boyutlarda per-pair ispat süresi
terim boyutuyla büyür — bütçe konfigler ARASINDA denetlenir (başlayan konfig
tamamlanır, aşabilir; orta-koşu kesme yok); bütçe bitince kalan konfigler
`skipped_budget` + null gözlem alanlarıyla kaydedilir. Kapsam dışı:
genişletmenin implementasyonu (Aşama 7), Lean, MCP.

**DUR BURAYA**
