# AŞAMA 8 — Simetri-Koşullu Ayrışım Türetici v0 (FAZ C açılışı)

**Tarih**: 2026-07-13 · **Önceki**: stage-07 (Sum/Scale, Faz B kapanışı)
**Mod**: otonom · **Kaynak**: Kuntman & Arteaga, Appl. Opt. 55, 2543 (2016)
(proje dosyası `decompositionofadepolarizingmm.pdf` — bu aşamada tam okundu)

---

## 1. Bağlam

Faz C hedefi: AO2016'nın ELLE türettiği iki-terimli ayrışım denklemlerini
(rank-2 H = α₁H₁ₛ + α₂H₂; H₁ₛ simetrik, H₂ serbest) motorun kendisinin
rank-1 minor koşullarından ÜRETMESİ — sonra (A9-A10) genelleme ve rank-3
keşif bölgesi.

**Konvansiyon uyarısı (kritik)**: AO2016 kovaryansı STANDART bazda tanımlar:
H = ¼Σ mᵢⱼ(σᵢ⊗σⱼ), mᵢⱼ = tr[(σᵢ⊗σⱼ)H] (Eq. 2-3) — çekirdekteki Π-bazlı
`covariance_from_mueller`'dan FARKLI nesne. Ayrışım modülü kendi
standart-baz dönüşümünü taşır; iki baz karıştırılamaz (testle ayrılır).

## 2. Hedefler

1. **`decomposition/` paketi**:
   - `covariance.py`: standart-baz H↔M dönüşümleri; Tip 1/2/3 H-şablonları
     (Tablo 1) parametre fonksiyonu olarak + şablon→parametre çıkarımı.
   - `derive.py`: **TÜRETİCİ** — jenerik Hermitsel H sembolleri üzerinden
     kalan matrisin (H − α₁H₁ₛ) seçili 2×2 minorlarını kur, SymPy ile çöz,
     kapalı-form denklemleri ÜRET; makalenin Tablo 2 formülleriyle
     (elle girilmiş) SEMBOLİK birebir karşılaştır.
   - `solve.py`: sayısal çözücü — M (veya H) + varsayılan tip → α₁, H₁ₛ,
     H₂, M₁, M₂; uygulanabilirlik guard'ları (rank-2, ilgili determinant
     ≈0 değil, ağırlık ∈ (0,1), eigen-fizikalite) — ihlalde açık hata,
     sessiz sonuç YOK (kullanıcı direktifi: guard'lar).
2. **Kapsam bu aşama**: Tip 1 (iki varyant), Tip 2a/2b, Tip 3a/3b —
   Tablo 2'nin tamamı. Tablo 4 (Tip 1-2/1-3/2-3) → A9.
3. **Kabul**:
   - A: Türetilen denklemler ≡ Tablo 2 (sembolik, tip başına).
   - B: **Makale §6 sayısal örneği birebir**: M₁ (Eq. 16a, tip-3) + M₂
     (16b), α=0.3/0.7 → çözücü α₁E=0.1433, α₁V=0.0289+0.0112i,
     α₁Ē=0.0067, α₁=0.3, H₁ (Eq. 21, 4 ondalık) döndürmeli.
   - C: Sentetik roundtrip: rastgele tip-k saf + rastgele saf, rastgele
     ağırlık → iki bileşen + ağırlık geri kazanılır (3 tip × 2 varyant,
     deterministik tohum).
   - D: Dejenere durum (iki bileşen aynı simetri) guard'ı açık hata verir
     (makale: "overlap makes the decomposition impossible").
   - E: Mevcut 92 test yeşil.
4. **`docs/design-note-guarded-atoms.md`**: koşullu atom sınıfları TASARIMI
   (implementasyon A9+): guard'lar AKSIYOM değil YORUMLAMA katmanına girer
   (kısıtlı üreteçler) — ses maliyeti sıfır; guard'lı-doğru-ama-ispatsız
   çiftler `underivable` kanalına guard etiketiyle düşer = Horn-koşullu
   özdeşlik adayları. K24 gereği aksiyom tarafı denetçi onaysız açılmaz.

## 3. Mimari kararlar

- **M28. Türetici ≠ tablo kopyası**: denklemler minor koşullarından SymPy
  çözümüyle üretilir; elle girilmiş Tablo 2 yalnız KARŞILAŞTIRMA çapası.
- **M29. Standart-baz kovaryans ayrışım modülünde yaşar**; çekirdek Π-bazı
  değişmez (K11).
- **M30. OCR güvenilmezliği**: makale metnindeki üst-çizgi (overbar)
  kayıpları olabilir; nihai hakem = sembolik türetim + §6 sayısal çapa +
  sentetik roundtrip üçlüsü.

## 4. Katı kurallar

K26. Çözücü uygulanamaz durumda istisna fırlatır (sessiz NaN/yanlış sonuç yasak).
K27. Tüm sayısal testler deterministik tohumlu.
K28. Tablo-karşılaştırmada sadeleştirme başarısızlığı = aşama başarısız
(yaklaşık eşitlikle geçiştirme yok; sembolik fark tam sıfır olmalı).

## 5-6. Teslim + Doğrulama

`decomposition/{__init__,covariance,templates,derive,solve}.py` ·
`tests/test_decomposition.py` · tasarım notu · rapor. Kabul A-E.

## 7-9.

Push + rapor + A9 (5 dk). Uyarı: makaledeki H₁ normalizasyonu tr=1;
ağırlık α₁ = tr(α₁H₁ₛ) tip-1'de x+w·w̄/x, tip-2/3'te 2(k+k̄). Kapsam dışı:
Tablo 4 tipleri (A9), rank-3 (A10), deneysel veri işleme, Cloude-kesme.

**DUR BURAYA**
