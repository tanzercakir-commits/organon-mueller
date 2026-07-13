# Tasarım Notu — Terim Diline `addition` + `scalars` (Aşama 7 spec girdisi)

Kaynak gereksinim: `docs/term-language-extensions.md` öncelik 1/1b —
koherent süperpozisyon fiziği (I15–I18) dile girsin.

## Dil genişletmesi

```
t ::= Atom(name) | Mul(t, t) | Conj(t)
    | Sum(t, t)                    # YENİ: terim toplamı
    | Scale(c, t)                  # YENİ: opak skaler katsayı c ile ölçek
c ::= ScalarAtom(name) | ScalarConj(c)   # opak; aritmetiği YOK (M10)
```

- **Hibrit sınır korunur (M10)**: e-graph skaleri OPAK tutar — `c` üzerinde
  hiçbir aritmetik kural yok (toplama/çarpma değerlendirmesi SymPy'da).
  e-graph yalnız YAPISAL yasaları bilir.
- Yorumlama: `ScalarAtom(name)` → SymPy karmaşık sembolü; sayısal katmanda
  rastgele karmaşık skaler (tohum ayrık, K14 genişler).

## Yapısal aksiyomlar (ses sınırı analiziyle — stage-02/03 dersleri)

| Kural | Not |
|---|---|
| Sum komütatif + asosiyatif | matris toplamı ✓ sound |
| Mul, Sum üzerine iki yandan dağılır | ✓ sound |
| Conj(Sum(x,y)) = Sum(Conj(x),Conj(y)) | elementwise ✓ |
| Conj(Scale(c,x)) = Scale(ScalarConj(c), Conj(x)) | ✓ |
| Scale(c, x)·y = Scale(c, x·y) = x·Scale(c, y) | skaler merkezî ✓ |
| Scale iç içe: Scale(c, Scale(d, x)) = Scale(d, Scale(c, x)) | skaler değişmeli ✓ (çarpımını OLUŞTURMADAN sıra-değişimi — opaklık korunur) |
| **YOK**: skaler kısaltma/birleştirme (c+d, c·d) | M10: SymPy tarafında |

Atom-komütasyon kuralı (I10) değişmez; Sum/Scale içeren serbest-değişkenli
komütasyon YOK (stage-03 ses dersi — genel kural unsound olur, türetim
saturasyona bırakılır).

## Patlama yönetimi

- Başlangıçta **Sum en fazla 1 kez, 2 toplamlı** (süperpozisyon çifti
  aZ_a + bZ_b) — enumerasyon boyutu kontrollü; kademeli açılır.
- conj-normal budama Sum/Scale'e genişler: Conj yalnız atom/skaler-atom
  düzeyinde.
- **Parmak izi ölçek-göreli anahtara geçer** (stage-03 uyarısının vadesi):
  opak skalerler rastgele değer alınca mutlak 3-ondalık yuvarlama yetersiz;
  anahtar, matrisin Frobenius normuna bölünmüş girdilerden üretilir
  (+ sıfır-matris özel durumu). Yanlış-ayrılma analizi yeniden yapılır.

## Kabul hedefleri (Aşama 7)

1. I15 açılımı: (aZ_a + bZ_b)·conj(aZ_a + bZ_b) genişlemesinin dört terimli
   yapısal formu motor tarafından türetilir; çapraz terimin gerçelliği
   (yapısal formda conj-simetri) kazanılır.
2. I16 girişim: Scale(e, x) özel durumu — yapısal iskeleti (skaler aritmetiği
   SymPy doğrular).
3. Geri-kazanım kampanyası yeniden koşar; M22 monotonluk: kazanım seti
   {I1, I10} ⊂ yeni set (hedef: + I15 yapısal yarısı; I16-I18 kısmı).
4. Tüm eski testler değişmeden yeşil (K11 API dokunulmazlığı).

## Riskler

- egglog patolojisi yeni düğüm tipleriyle farklı yüzeylerde tekrarlayabilir →
  yalıtılmış-graf modu (M18) zaten koruyor; probe genişletilir.
- Sembolik sertifikasyon maliyeti Sum ile büyür (polinom terim sayısı) —
  certify süreleri yeniden ölçülür; gerekirse "underivable-only" varsayılanı korunur.
