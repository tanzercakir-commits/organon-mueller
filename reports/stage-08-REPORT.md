# AŞAMA 8 — RAPOR (Faz C açılışı: Simetri-Koşullu Ayrışım Türetici v0)

**Tarih**: 2026-07-13 · **Spec**: `specs/stage-08.md` · **Mod**: otonom
**Sonuç**: TAMAMLANDI — 110/110 test yeşil; **motor, AO2016 Tablo 2'nin
altı denklem setinin tamamını rank-1 minor koşullarından KENDİSİ türetti ve
makaleyle sembolik birebir eşleşti**; makale §6 sayısal örneği baskı
hassasiyetinde yeniden üretildi.

---

## 1. Teslim edilenler (`decomposition/` paketi)

- **`covariance.py`**: AO2016-konvansiyonlu kovaryans H↔M + Tip 1/2/3
  şablonları (Tablo 1, primary outer/center parametrizasyonu).
  **Konvansiyon bulgusu → TEOREM**: makalenin Eq. (2)'si harfiyen kron
  olarak okununca PSD-olmayan bir kuzen çıkıyor; gerçek H bunun indeks
  reshuffle'ı, ve denetçi R(σᵢ⊗σⱼ)=σᵢ⊗σⱼ\* özdeşliğini İSPATLADI — yani
  makalenin H'si standart Cloude/Gil kovaryansı (baskıda eşlenik düşmüş).
- **`derive.py` (M28)**: denklemler tablodan KOPYALANMAZ — jenerik Hermitsel
  H üzerinde kalanın (H − α₁H₁ₛ) seçili 2×2 minorları SymPy ile çözülür;
  yapısal guard'lar (x-minoru w'ye dokunamaz; w-minoru conj-içermez) ihlalde
  fırlatır. Altı varyantın altısı da elle girilmiş Tablo-2 çapalarıyla
  **tam sembolik sıfır** farkla eşleşti (K28).
- **`solve.py`**: sayısal çözücü — rank-2/payda/α₁∈(0,1)/PSD/rank-1
  guard'ları (K26: sessiz yanlış sonuç yok); `variant="auto"` makalenin
  sayısal tavsiyesiyle (büyük |payda| önce) sıralar; tolerans parametreleri
  (kesin veri: katı varsayılan; 4-ondalık literatür verisi: gevşek).

## 2. Doğrulama sonuçları

- **A**: 6/6 varyant sembolik birebir (2b/3b "overbar" okuması denetçinin
  bağımsız türetimi + makalenin kendi Eq. (20) etiketiyle teyitli; 3a
  eşlenik-taraflı — anchor yorumları test dosyasında belgeli).
- **B (makale §6 çapası)**: α₁=0.3000; α₁E=0.1433; α₁V=0.0289+0.0112i;
  α₁Ē=0.0067; H₁ girdileri 0.4777/0.0962+0.0372i; M₁ ve M₂ ~1e-3'te geri
  kazanıldı (4-ondalık baskı gürültüsü). **İki baskı hatası teşhis edildi**
  (Eq. 17 h03: 0.0161→0.1608; Eq. 21 [1,3]): makalenin KENDİ türetilmiş
  değerleriyle öz-tutarlılık üzerinden — 0.0161 hiçbir tutarlı
  rekonstrüksiyona oturmuyor.
- **C**: sentetik kesin roundtrip 3 tip × 2 varyant (denetçi farklı tohumla
  5×6 tekrar: en kötü hata 1.1e-15).
- **D**: aynı-simetri örtüşmesi ve rank≠2 açık hatayla reddediliyor;
  near-dejenere taramada (ε→1e-8) sessiz çöp yok — ε=1e-4'e dek kesin,
  altında guard mesajla devreye giriyor.
- Baz-ayrımı sentineli: standart ve Π kovaryansları karıştırılamaz (M29).

## 3. Bağımsız denetim

Verdict: **PASS** (3 doküman-düzeyi kusur — düzeltildi: auto-variant
sözleşmesi makale tavsiyesiyle gerçekten implement edildi; konvansiyon
docstring'i "ampirik"ten "ispatlı"ya yükseltildi + baskı-hatası notu;
2b/3b overbar gerekçesi test dosyasına taşındı). Denetçinin kendi
türetimleri: reshuffle teoremi, altı varyantın bağımsız SymPy çözümü,
tam-rasyonel roundtrip'lerde α₁=2/7'nin sembolik kesin geri kazanımı.

## 4. guarded_atoms tasarımı (A9 girdisi)

`docs/design-note-guarded-atoms.md`: guard'lar aksiyoma DEĞİL yorumlama
katmanına girer (ses maliyeti sıfır, K24 dokunulmadı); guard'lı-doğru-ama-
ispatsız çiftler `underivable` kanalına guard etiketiyle düşer = Horn-koşullu
özdeşlik adayları (kanalın İLK dolu çıktısı burada bekleniyor). Denetçi
τ=0 tipi ölçü-sıfır sınıf endişesini kapattı (bölmesiz dilde polinom
özdeşlik teoremi yeter) ve iki ileriye-dönük yükümlülük ekletti (üreteç
sadakati; interpreted_scalars gelince payda yan-koşullarının guard'a
yazılması).

## 5. Sıradaki aşama (otonom devam)

**Aşama 9 — Rank-2 genel çözücü**: Tablo 4 tipleri (1-2, 1-3, 2-3) türetici
kapsamına; guarded_atoms implementasyonunun ilk yarısı (üreteçler +
kampanya bağlantısı); ayrışım-keşif köprüsünün ilk testi.
