# organon-mueller — geri bildirim paketi #1 (Kuntman–Arteaga grubu için)

*Durum: deneysel araştırma yazılımı. Aşağıdaki sonuçlar **doğrulanmış**
(yayınlarınızdaki tablo/örneklerle makine kontrollü) ya da **aday**
(yayınlanmış tabloların ötesi — yenilik/fizik İDDİASI yoktur; yorum
bilinçli olarak size bırakılmıştır) olarak etiketlidir.*

## Bu nedir

Yayınlarınızdaki Stokes–Mueller cebirini otomatikleştiren deneysel bir
motor (JOSA A **34**, 80 (2017); Phys. Rev. A **95**, 063819 (2017);
Appl. Opt. **55**, 2543 (2016); coupled-dipole çalışması — PRB **98**,
045410 (2018), Symmetry **12**, 1790 (2020) ve OA-topluluk ön-baskısı —
artık kapsanıyor; bkz. `ADDENDUM-dipoles-tr.md`). İki ayak: **keşif motoru**
(kovaryans-vektörü terim dili üzerinde
equality saturation; her aday kesin sembolik ispatla sertifikalanır) ve
**ayrışım türetici** (AO2016'nın simetri-koşullu ayrışımları rank-1 minor
koşullarından *türetilir* — tablodan kopyalanmaz).

## Yayınlarınıza karşı doğrulananlar

- **Tablo 2 (AO2016), altı varyantın altısı**: motor denklem setlerini
  H − α₁H₁ₛ'nin 2×2 minorlarından türetiyor ve basılı tabloyla sembolik
  birebir (tam sıfır fark) eşleşiyor — a/b varyant yapısı ve "büyük payda
  sayısal olarak sağlıklı" tavsiyesi dahil.
- **§6 sayısal örneği**: baskı hassasiyetinde (α₁ = 0.3000,
  α₁E = 0.1433, α₁V = 0.0289+0.0112i, α₁Ē = 0.0067; iki bileşen Mueller
  matrisi ~1e-3).
- **Bileşik tipler 1-2 / 1-3 / 2-3 (Tablo 3–4)**: üç-parametreli sıralı
  minor türetimi, Tablo 4 ile sembolik birebir; sentetik roundtrip'ler
  kesin.
- **Kovaryans konvansiyonu**: R(σᵢ⊗σⱼ) = σᵢ⊗σⱼ* (indis reshuffle)
  özdeşliğini ispatladık — AO2016'nın H'si tam olarak standart Cloude/Gil
  kovaryansı; Eq. (2) harfiyen (eşleniksiz) okununca PSD-olmayan bir kuzen
  çıkıyor. Başlangıçtaki kafa karışıklığımızı bu çözdü; regresyon
  testi olarak kayıtlı.
- **İki muhtemel baskı hatası** (teyidiniz bizi çok memnun eder):
  Eq. (17)'de h₀₃'ün sanal kısmı 0.0161 basılmış ama makalenin KENDİ
  (18)–(20) denklemleriyle tutarsız; boru hattımız aynı denklemleri
  0.1608 ile birebir yeniden üretiyor. Eq. (21)'in [1,3] girdisinde
  benzer ikinci bir artefakt var.

## Aday bölge (yayınlanmış tabloların ötesi — iddiasız)

- **Rank-3 üç-terimli ayrışımlar** H = α_A H_A + α_B H_B + α_G|u⟩⟨u|
  ({H_A, H_B} iki FARKLI fundamental tip): {1,2} ve {1,3} sıralı
  "peel" ile, {2,3} kombinasyon değişkenleri + zorunlu
  fazladan-belirlenim kontrolüyle çözülüyor. Eksik-anizotropi koşulları
  çift bazında genelleşiyor — guard paydaları: {1,2} için α_G|u₁−u₂|²,
  {1,3} için α_G|u₁+u₂|², {2,3} için α_G|u₀−u₃|².
- **Teklik-dışılık gözlemi**: iki tip-2 saf + jenerik olarak kurulan bir
  kovaryans, tip-1 + tip-2 + jenerik olarak da *kesin* ayrışıyor (kapalı
  form 1e-16'da doğrulandı). Sabit çift hipotezi içinde {2,3} ispatla
  tek. Yani rank-3 sonucu "*bir* ayrışım"dır, "*tek* ayrışım" değil —
  fiziksel olanın seçimi tam da görüşünüze değer vereceğimiz türden bir
  soru.
- **Horn-koşullu özdeşlik kanalı**: guard-kısıtlı üreteçler (ör. üç
  class-2 kuaterniyon düzlemi) "guard altında doğru + guard'sız
  türetilemez" hükümleri dört-parça kanıt kaydıyla üretiyor; şimdilik
  bilinen gerçeklerle (mekanizma ispatı) dolu.
- Demo'daki hipotez "skorları" hakkında not: skor yalnız bir sayısal
  sağlık sezgiseli (verideki en küçük guard paydası) — denemeleri
  SIRALAR; kabul kararını yalnız kesin çözücüler verir ve reddedilen bir
  hipotezin skoru kabul edilenden yüksek olabilir. Tüm aday çıktılar
  yazılı yenilik protokolümüzden (`docs/novelty-protocol.md`) geçer;
  protokolün son adımı — bir şeyin fiziksel olarak ilginç/yeni olup
  olmadığına karar vermek — açıkça insana, yani size ayrılmıştır.

## Doğrulama sözleşmesi (özet)

Hiçbir matematiksel ifade şu katmanlardan geçmeden repoya giremez: kesin
sembolik ispat (SymPy, expand-tabanlı sıfır testi) · deterministik
tohumlu sayısal kontroller · makalelere karşı bilinen-özdeşlik regresyonu
· her keşif adayının motordan bağımsız sertifikasyonu · her aşamada
bağımsız adversarial denetim (denetçi matematiği sıfırdan yeniden
türetir) · 3 sürümlü CI matrisi. Ayrıntı: `docs/VERIFICATION.md`.

## Deneyin

```bash
pip install -e ".[test]"
python docs/kuntman-package/demo.py
```

## Geri bildirimin en çok yarayacağı sorular

1. İki baskı-hatası teşhisi (Eq. 17 / Eq. 21) kayıtlarınızla uyuşuyor mu?
2. Rank-3 üç-terimli bölge programınızla ilgili mi; teklik-dışılık
   davranışı sizce beklenen/bilinen bir şey mi?
3. Konvansiyonlarımız (reshuffle ile standart-baz kovaryans, iz-1
   normalizasyonu, ölçekli-parametre şablonları) günlük kullandıklarınız
   mı?
4. Coupled-dipole modülü (PRB 98, 045410; Symmetry 12, 1790; ve OA-topluluk
   ön-baskısı) teslim edildi — bkz. `ADDENDUM-dipoles-tr.md`. Çıktılarından
   — Eq. (25) üç-terimli saçılma ayrışımı (teorem), genel-yön γ (optik
   aktivite) otomasyonu ve δ=0 ⇒ γ_z ≡ 0 topluluk sonucu — hangisini bir
   sonraki adımda genişletmek en yararlı olur?
