# AŞAMA 2 — Keşif Motoru Çekirdeği v0 (Hibrit egglog + SymPy) + FROZEN-N

**Tarih**: 2026-07-13
**Önceki aşama**: stage-01 (21 özdeşlik, serileştirme, egglog spike BAŞARILI)
**Not**: Bu aşamadan itibaren proje otonom modda yürür (kullanıcı mandası,
2026-07-13): kritik-karar eşiği dışında tüm kararlar spec+rapor içinde
gerekçelendirilir; güven çıpası doğrulama sistemidir (docs/VERIFICATION.md).

---

## 1. Bağlam

Spike, kuaterniyon/Z cebrinin komütatif olmayan iskeletinin egglog'da sature
edilebildiğini gösterdi. Bu aşama öneriyi mimariye çevirir: **hibrit motor** —
egglog terim-yapısı denkliği (equality saturation) üretir, SymPy/NumPy her
adayı bağımsız doğrular. Motorun İLK işi yeni şey bulmak değil, **bilineni
kendi başına yeniden bulmaktır** (v1 "bilineni kurtar" disiplini, keşif
düzeyinde).

## 2. Hedefler

1. `discovery/` paketi: terim dili, egglog aksiyom modeli, enumerasyon,
   e-sınıf hasadı, SymPy yorumlayıcı + doğrulama boru hattı.
2. Kabul (yeniden keşif): motor, atomlar {a,b} ve ops {mul, conj} üzerinde
   şunları KENDİSİ bulmalı (düzeltme: R3 terimlerinin boyutları 8 ve 9 —
   ilk taslaktaki "boyut 7" aritmetik hatasıydı; kabul saturasyonu boyut 9
   enumerasyonu üzerinde koşar, hasat/CI ekonomisi için tam-boru-hattı testi
   boyut 7'de kalır):
   - R1: conj(conj(a)) ≡ a
   - R2: a·conj(b) ≡ conj(b)·a  (I10 komütasyonu)
   - R3: (a·b)·conj(a·b) ≡ (a·conj(a))·(b·conj(b))  (seri Mueller çarpımı, I10 sonucu)
3. Negatif kontroller: a·b ≢ b·a ve conj(a)·conj(b) ≢ conj(b)·conj(a)
   e-graph'ta AYRI kalmalı (saturasyon komütatiflik icat etmemeli).
4. Üretilen HER aday çift SymPy sayısal yorumlamayla doğrulanmalı; doğrulama
   oranı %100 olmalı (aksi motor hatası → aşama başarısız).
5. `docs/VERIFICATION.md` (güven sözleşmesi) + ROADMAP frozen-N ilanı.

## 3. Mimari kararlar

- **M10. Hibrit sınır**: egglog yalnız YAPI (atomlar soyut, katsayı yok);
  parametre düzeyi tamamen SymPy'da. egglog hiçbir zaman tek doğrulayıcı değil.
- **M11. Ses (soundness) kuralları**: komütasyon SADECE atom düzeyinde
  (a·conj(b) = conj(b)·a, a,b atom). Genel x·conj(y)=conj(y)·x KURAL DEĞİL —
  conj-conj çiftleri komütatif olmadığından unsound olur; türetilebilenler
  asosiyatiflik + atom kuralından saturasyonla çıkar. conj dağılımı sıra
  KORUYARAK: conj(x·y) = conj(x)·conj(y) (elementwise eşlenik, transpoze değil).
- **M12. Aday tanımı**: aynı e-sınıfta düşen, sözdizimsel olarak farklı terim
  çiftleri; hasat `extract` gruplamasıyla (temsilci dizgisi anahtar).
- **M13. egglog `[discovery]` extra'sı**: temel kurulum egglog'suz çalışır;
  discovery testleri `pytest.importorskip` ile atlanır. CI discovery dahil kurar.
- **M14. FROZEN-N = 22**: ROADMAP'teki 6 faz / 22 aşama bu aşamayla donar.
  Değişiklik ancak kritik-karar notuyla kullanıcıya gider.

## 4. Katı kurallar

- K9. Motor "keşfettim" diyemez → doğrulanmamış hiçbir çift raporlanamaz.
- K10. Doğrulama başarısız aday = test hatası (sessiz eleme YASAK; unsound
  aksiyom sinyalidir).
- K11. Aşama 0-1 API'leri dokunulmaz.
- K12. Enumerasyon deterministik (sıralı üretim, seed'li örnekleme yok).

## 5. Teslim

```
src/organon_mueller/discovery/
├── __init__.py          (egglog yokluğunda nazik ImportError)
├── terms.py             (Atom/Mul/Conj, boyut, deterministik enumerasyon)
├── axioms.py            (egglog modeli: ZTerm, kural seti — M11 sınırları)
├── interpret.py         (terim → SymPy/NumPy Z-matris değeri; sayısal denklik)
└── engine.py            (saturate → e-sınıf hasadı → doğrulama → DiscoveryResult)
tests/test_discovery.py  (kabul R1-R3, negatif kontroller, %100 doğrulama)
docs/VERIFICATION.md
docs/ROADMAP.md          (frozen-22 ilanı)
specs/stage-02.md, reports/stage-02-REPORT.md
pyproject.toml           ([discovery] extra; CI ".[test,discovery]")
```

## 6. Doğrulama

- R1/R2/R3 e-graph `check` ile; negatif kontroller check-başarısızlığı ile.
- Hasat edilen tüm çiftler: 3 bağımsız rastgele Z-ataması × sayısal karşılaştırma.
- Tam suite yeşil (egglog'lu ve egglog'suz kurulumda).
- Bağımsız denetçi (adversarial) PASS.

## 7. Teslim formatı

PAT ile doğrudan `main`'e push (5cf0bb9 üstüne) + rapor + kullanıcıya kısa özet.

## 8. Özel uyarılar

1. (AB)* = A*B* — elementwise eşlenik SIRA KORUR; (AB)^T/† ile karıştırma.
2. Atom-komütasyon kuralını x,y serbest değişkenli YAZMA (unsound, bkz. M11).
3. extract temsilcisi deterministik olmayabilir — gruplamayı aynı EGraph
   nesnesi içinde yap, oturumlar arası karşılaştırma yapma.
4. Ölçülen maliyetler (bu ortam): boyut 7 → 570 terim; boyut 9 → 5698 terim,
   saturasyon 0.15 sn, extract ~21 sn (darboğaz extract; check ucuz). Kabul
   testleri check-tabanlı (boyut 9), hasat testi boyut 7.

## 9. Kapsam dışı

- Skaler/karmaşık katsayılı terimler (Faz B'de, hibrit sınır korunarak)
- Kanonik form extraction maliyet fonksiyonu ayarı
- Yeni-aday literatür karşılaştırması (Aşama 6)
- MCP/UI

**DUR BURAYA**
