# egglog Spike Bulguları (Aşama 1)

**Tarih**: 2026-07-13 · **egglog-python**: 13.2.0 · **Sonuç**: BAŞARILI

## Ne denendi

Stokes-Mueller formalizminin komütatif olmayan iskeleti — kuaterniyon birim
cebri {1, i, j, k} + negasyon — egglog e-graph'ında rewrite kurallarıyla
modellendi (`spikes/egglog_quaternion.py`). Komütatiflik aksiyomu bilinçli
olarak VERİLMEDİ; Hamilton ilişkileri (i²=j²=k²=−1, ij=k, ji=−k, ...) +
çift yönlü asosiyatiflik + negasyonun merkezîliği kural olarak girildi.

Saturasyon sonrası dört denklik `check` ile doğrulandı:

| Sorgu | Sonuç |
|---|---|
| i·j·k ≡ −1 | PASS |
| (i·j)·(j·k) ≡ j | PASS |
| k·(k·k) ≡ −k | PASS |
| (j·i)·k ≡ 1 | PASS |

## Bulgular

1. **Komütatif olmayan çarpım doğal**: kural vermeyerek elde ediliyor; e-graph
   tüm parantezlemeleri tek eşdeğerlik sınıfında tutuyor. v2'nin Z-matris /
   kuaterniyon çarpımları için temel engel YOK.
2. **Skaler (karmaşık) katsayılar henüz modellenmedi** — asıl açık soru bu.
   İki seçenek: (a) katsayıları rasyonel çiftler (re, im) olarak egglog'a
   gömmek, (b) **hibrit mimari**: egglog yalnızca terim-yapısı denkliği
   (structural equivalence) için, katsayı aritmetiği ve doğrulama SymPy'da.
   **Öneri: (b) hibrit** — float/karmaşık tamlık riskini e-graph'a taşımaz,
   Aşama 0-1'in SymPy doğrulama boru hattını aynen kullanır.
3. **API notları**: `vars_("a b c", Q)` tek çağrıda; tek isimli `vars_`
   üreteç döndürüyor (tuzak). Kural planlaması `ruleset(...)` +
   `egraph.run(rs.saturate())`; denklik testi `egraph.check(eq(l).to(r))`.
4. **Ölçek**: bu fragman milisaniyelerde sature oluyor. Gerçek keşif yükü
   (terim enumerasyonu × kanonik form) Aşama 2'nin ölçüm konusu.

## Aşama 2'ye girdiler

- Hibrit mimari kabul edilirse: egglog tarafında soyut terim cebri
  (Z-çarpımı, eşlenik `conj` unary, `mueller(z) = z * conj(z)` gömmesi),
  SymPy tarafında parametre-düzeyi verifikasyon.
- Kanonik form üretimi için extraction (en küçük terim) denenmeli.
- Aday özdeşlik = saturasyon sonrası aynı e-sınıfa düşen, sözdizimsel olarak
  farklı terim çiftleri; karmaşıklık sınırı enumerasyonda uygulanır.
- egglog pyproject bağımlılığı OLMADI (karar M9); Aşama 2'de `discovery`
  extra'sı olarak eklenebilir: `pip install organon-mueller[discovery]`.
