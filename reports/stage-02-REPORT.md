# AŞAMA 2 — RAPOR

**Tarih**: 2026-07-13
**Spec**: `specs/stage-02.md`
**Sonuç**: TAMAMLANDI — 56/56 test yeşil; motor bilinen yapıyı kendi başına
yeniden keşfetti; hasat edilen adayların %100'ü bağımsız doğrulamadan geçti;
**FROZEN-22 ilan edildi**.
**Mod**: Bu aşamadan itibaren otonom yürütme (kullanıcı mandası 2026-07-13);
güven çıpası `docs/VERIFICATION.md`.

---

## 1. Teslim edilenler

- **`discovery/` paketi (hibrit motor v0)**:
  - `terms.py`: soyut terim dili (Atom/Mul/Conj), deterministik enumerasyon.
  - `axioms.py`: egglog kural seti — asosiyatiflik (çift yön), conj involüsyon,
    **sıra-koruyan** conj dağılımı ((AB)\*=A\*B\*), I10 komütasyonu **yalnız
    atom düzeyinde** (ses/soundness sınırı; serbest-değişkenli hali unsound —
    gerekçe modül docstring'inde, sayısal karşı-örnekle).
  - `interpret.py`: terim → somut Z-matris değeri (SymPy/NumPy); motordan
    bağımsız sayısal denklik testi.
  - `engine.py`: enumerate → saturate → hasat (extract-gruplama + check-teyit)
    → doğrula boru hattı; `DiscoveryResult(sound, verified, refuted,
    extraction_collisions, ...)`. K9/K10: doğrulanamayan aday sessizce elenmez,
    build'i kırar.
- `docs/VERIFICATION.md`: 6 katmanlı doğrulama sözleşmesi + dürüst sınırlar.
- `docs/ROADMAP.md`: **FROZEN-22** (6 faz, 22 aşama — artık değişmez).
- pyproject `[discovery]` extra'sı (egglog>=13); CI `.[test,discovery]`.

## 2. Doğrulama sonuçları

- Suite: **56/56 yeşil** (~32 sn; egglog'suz kurulumda discovery testleri
  düzgün atlanıyor).
- **Yeniden keşif kabulü** (boyut-9 saturasyon, 5698 terim, 0.15 sn):
  R1 conj-involüsyon ✅ · R2 a·conj(b)≡conj(b)·a ✅ · R3 seri Mueller çarpımı
  (a·b)·conj(a·b) ≡ (a·conj(a))·(b·conj(b)) ✅
- **Negatif kontroller**: a·b ≢ b·a ✅ · conj(a)·conj(b) ≢ conj(b)·conj(a) ✅
  (saturasyon komütatiflik "icat etmiyor"; her ikisi sayısal olarak da gerçekten eşitsiz)
- **Tam hasat** (boyut 7): 570 terim → 64 e-sınıf → **506 aday çift, 506/506
  doğrulandı, 0 çürütüldü, 0 extraction çakışması**.

## 3. Bağımsız denetim

Verdict: **PASS**. Denetçi farklı tohumla (seed 7): ses sınırını iki yönde
sayısal olarak teyit etti (serbest kural 20/20 çürüdü; atom kuralı 20/20
geçti), 506 çifti yeniden doğruladı (0 hata), 64 sınıf çapasının ikili
FARKLILIĞINI da doğruladı (motor ne fazla birleştiriyor ne — bu boyutta —
eksik birleştiriyor). Üç önerisi uygulandı:

| Öneri | Aksiyon |
|---|---|
| `equivalent` genel Exception yutuyordu | ✅ yalnız `EggSmolError` yakalanıyor; operasyonel hata artık "eşit değil" maskesi takamaz |
| Defensive-split görünmezdi | ✅ `extraction_collisions` sayacı + testte sıfır garantisi |
| axioms docstring türetilebilirlik ifadesi eksikti | ✅ "assoc + conj dağılımı" olarak düzeltildi |

## 4. Kararlar

1. **FROZEN-22** ilanı (karar M14) — değişiklik ancak kritik-karar notuyla.
2. Hibrit sınır (M10) kalıcı mimari ilke: egglog asla tek doğrulayıcı olmaz.
3. Tamlık (completeness) kaybı bilinçli tercih: motor eksik bulabilir ama
   yanlış bulamaz — spec yalnız ses garantisi veriyor.
4. Düzeltme kaydı: spec'in ilk taslağındaki boyut aritmetiği hatası (R3
   terimleri 8/9, "7" değil) spec içinde açıkça düzeltildi.

## 5. Sıradaki aşama (otonom devam)

**Aşama 3 — Terim enumerasyonu + karmaşıklık sınırları (Faz B)**: atom sayısı
ve boyut ölçekleme stratejisi, extract darboğazının (21 sn @ boyut 9)
optimizasyonu, skaler yer tutucular için tasarım notu.
