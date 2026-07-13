# AŞAMA 4 — RAPOR

**Tarih**: 2026-07-13 · **Spec**: `specs/stage-04.md` · **Mod**: otonom
**Sonuç**: TAMAMLANDI — 75/75 test yeşil; sembolik-kesin katman keşfe bağlandı;
runtime guard'lar üretim kodunda (kullanıcı direktifinin kod karşılığı).

---

## 1. Teslim edilenler

- **`discovery/symbolic.py` (katman-1 keşif bağlantısı, M19)**: soyut terim →
  atom başına bağımsız jenerik parametreli sembolik Z-matris; `expand` tabanlı
  **KESİN** eşitlik ispatı (örneklem değil teorem). Denetçi, prosedürün bu
  terim dili için hem sound hem complete olduğunu ispatladı (z/z̄
  polarizasyon argümanı) ve 66-terimlik havuzda ispat≡sembolik katmanların
  birebir örtüştüğünü (68/68 çift) doğruladı.
- **Sertifikasyon modları** `certify ∈ {none, underivable, all}` (varsayılan
  `underivable`): yayın-aday `underivable` kanalına giren her çift artık
  kesin ispatlı; geçemeyen `demoted_by_symbolic`'e düşer (K16, şeffaf).
  `certify="all"`: verified çiftleri de sertifikalanır. Yeni kurtarma yolu:
  ispatlı + sembolik-doğru + sayısal-yanlış → sayısal katman yanlış-negatifi
  (jitter) olarak verified'a alınır ve sayaçlanır (yanıltıcı alarm önlenir).
- **Runtime invariant guard'ları (M20)**: `DiscoveryResult.check_invariants()`
  motor tarafından her koşu sonunda çağrılır — kategori ayrıklığı, çift
  muhasebesi (çakışmalı durumda bile kayıp-çift denetimi), NaN/negatif sayaç,
  dejenere çift. Bilinçli bozulmuş sonuçla guard'ın gerçekten ateşlediği
  testli. Atom adı tekilliği kurucuda doğrulanıyor.
- **Property-based testler (hypothesis, derandomize — K2/K18)**: P1
  ispat⇒sayısal (ses sözleşmesi), P2 sembolik⇒sayısal (katman tutarlılığı),
  P3 enumerasyon determinizmi. Denetçi ilk sürümde antecedent'lerin neredeyse
  hiç ateşlemediğini ölçtü (%4.6 taban oranı) → kurulmuş-eşit-çift üreteci
  eklendi; şimdi her deterministik koşuda **13/30 nontrivial isabet**.
- **3-atom ölçekleme** (bu sandbox): pruned-7 → 825 terim / 630 verified /
  18.5 sn; pruned-8 → 2499 / 2196 / 68 sn; tümü 0 underivable/demoted/refuted.
  2-atom pruned-7 `certify="all"`: 156/156 sertifikalı, ~13 sn.
- Patoloji dokümanı güncellendi: kullanıcı kararı (upstream bildirimi yok) +
  **elenen hipotezler** — bellek yönetimi (kanıt deseni uyumsuz) ve
  `seminaive` bayrağı (iki ayarda da aynı davranış; kullanıcı sorusu üzerine
  test edildi).

## 2. Bağımsız denetim

Verdict: **PASS**. Sembolik katmanın ispat-değeri formel olarak gerekçelendi;
sınıflandırma yolları ve çakışma-kuyruğu hedefli bozma denemelerine dayandı
(5-terimli kova, 4-tur kaskadda her çift tam bir kez incelendi); tüm
benchmark sayıları bağımsız yeniden üretildi. Üç önerisi de uygulandı:
property-test üreteci, sayısal-yanlış-negatif kurtarma yolu, guard
sıkılaştırması (+ docstring güncellemeleri).

## 3. Kararlar

- M19 gereği "yeni özdeşlik" iddiası taşıyabilecek her çıktı bundan böyle
  kesin ispat katmanından geçer; sayısal-yalnız hiçbir sonuç bulgu kanalına
  giremez.
- 3-atom ölçekleme pruned-8'de 68 sn — Faz B ilerisi için kabul edilebilir;
  daha derin taramalar (Aşama 6) kova-paralelleştirme adayı (not düşüldü).

## 4. Sıradaki aşama (otonom devam)

**Aşama 5 — Geri-kazanım kampanyası**: motor, kütüphanedeki I1–I21'in terim
diline çevrilebilen alt kümesini KENDİ başına yeniden bulmalı; çevrilemeyenler
(skaler katsayı/Stokes gerektirenler) açıkça listelenir → Faz B sonrası terim
dili genişletmesinin gereksinim listesi bu boşluktan çıkar.
