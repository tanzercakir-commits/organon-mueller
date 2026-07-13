# AŞAMA 4 — Sembolik-Kesin İspat Katmanı + Runtime Guard'lar (Faz B)

**Tarih**: 2026-07-13 · **Önceki**: stage-03 (v1.1, patoloji bulgusu, M18)
**Mod**: otonom · **Kullanıcı direktifi (2026-07-13)**: "non-determinizme
karşı tek sigorta testler — mümkün olduğunca test ve guard ile çalış."

---

## 1. Bağlam

v1.1'de "doğru" hükmü sayısal örnekleme dayanıyor (katman 2). VERIFICATION.md
katman 1 (sembolik-kesin) keşif tarafına henüz bağlı değil; `underivable`
çiftleri yayın-aday bulgu kanalı olduğundan, o kanala giren her şey KESİN
ispatlı olmalı. Ayrıca kullanıcı direktifi gereği motor sonuç değişmezleri
artık çalışma anında da denetlenmeli.

## 2. Hedefler

1. **`discovery/symbolic.py`**: soyut terim → jenerik parametreli sembolik
   Z-matris değerlendirmesi; `terms_symbolically_equal` (expand tabanlı KESİN).
2. **Motorda sertifikasyon modu** `certify ∈ {"none","underivable","all"}`
   (varsayılan `"underivable"`):
   - `underivable` adayı sembolik ispattan geçemezse → `demoted_by_symbolic`
     (sayısal örneklem tesadüfü; ayrı listede, şeffaf).
   - `certify="all"` iken `verified` çifti sembolik ispattan geçemezse →
     `refuted` (e-graph + sayısalın birlikte yanılması = büyük alarm, build kırar).
3. **Runtime invariant guard'ları**: `DiscoveryResult.check_invariants()` —
   kategoriler ayrık; çakışma=0 iken verified+underivable+refuted+demoted =
   terim−kova; süreler ≥0; motor `run()` sonunda ÇAĞIRIR, ihlal
   `DiscoveryInvariantError` fırlatır (sessiz geçiş yok).
4. **Property-based testler** (hypothesis, `[test]` extra'sına eklenir;
   `derandomize=True` ile CI deterministik — K2 korunur):
   - P1: `provable(t1,t2) ⇒ terms_numerically_equal` (ses sözleşmesi)
   - P2: `terms_symbolically_equal ⇒ terms_numerically_equal` (katman tutarlılığı)
   - P3: enumerate determinism + duplicate-free (rastgele boyut/atomlarda)
5. **3-atom ölçekleme ölçümü**: (a,b,c) pruned boyut 7 (ve süre izin verirse 8)
   tam koşu; sayılar rapora.
6. Patoloji dokümanı "Açık iş" güncellemesi: upstream bildirimi YAPILMAYACAK
   (kullanıcı kararı, 2026-07-13).

## 3. Mimari kararlar

- **M19. Yayın-aday kanal kuralı**: `underivable` çıktısı yalnız
  sembolik-kesin ispat sonrası raporlanabilir (varsayılan certify düzeyi bunu
  garantiler). Sayısal-yalnız doğruluk hiçbir bulgu kanalına tek başına giremez.
- **M20. Guard'lar üretim kodunda**: değişmez denetimi test-yalnız değil,
  motorun kendisinde (kullanıcı direktifinin kod karşılığı).
- **M21. hypothesis yalnız test bağımlılığı**; çekirdek bağımlılıklar değişmez.

## 4. Katı kurallar

- K16. `demoted_by_symbolic` sessizce düşürülmez; sonuçta listelenir.
- K17. Sembolik değerlendirme atom başına AYRI jenerik parametre seti kullanır
  (paylaşım = yanlış özdeşlik ispatı riski).
- K18. Property testleri deterministik profille koşar (derandomize).

## 5. Teslim

`discovery/symbolic.py` · `engine.py` (certify + guard'lar) ·
`tests/test_symbolic.py` · `tests/test_properties.py` · pyproject ([test] +=
hypothesis) · bench güncellemesi (3-atom) · patoloji doc güncellemesi ·
`reports/stage-04-REPORT.md`.

## 6. Doğrulama

- R3 çifti sembolik-kesin ispatla da geçer (katman-1 keşif bağlantısı kanıtı).
- Negatif: a·b vs b·a sembolik olarak da eşit DEĞİL.
- pruned-7 tam koşu `certify="all"` ile: tüm verified sembolik sertifikalı,
  demoted boş; süre rapora.
- pruned-9 varsayılan certify ile önceki sayılar korunur (1348 verified).
- Invariant guard: bilinçli bozulmuş sahte sonuçla `DiscoveryInvariantError`
  testi.
- Tüm suite (hypothesis dahil) yeşil; 3-atom ölçümü raporda.

## 7-9. Teslim formatı / Uyarılar / Kapsam dışı

Push + rapor + Aşama 5 planlaması. Uyarılar: sembolik matmul zinciri 4+
atomda pahalılaşır — certify süreleri ölçülmeden "all" varsayılan yapılmaz;
`conjugate()` elementwise'dır (dagger değil). Kapsam dışı: skaler katsayılı
terim dili, kanonik form, literatür karşılaştırması, Lean.

**DUR BURAYA**
