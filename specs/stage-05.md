# AŞAMA 5 — Geri-Kazanım Kampanyası (Faz B)

**Tarih**: 2026-07-13 · **Önceki**: stage-04 (v1.2, sembolik sertifikasyon)
**Mod**: otonom

---

## 1. Bağlam

v1'in "bilineni kurtar" disiplini keşif düzeyine taşınıyor: elle kodlanmış
I1–I21 kütüphanesinin terim diline (atomlar + mul + conj; atom = jenerik Z)
çevrilebilen alt kümesini motor KENDİ BAŞINA yeniden bulmalı. Çevrilemeyenler
tesadüf değil, terim dilinin sınır haritasıdır → Faz B sonrası genişletmenin
gereksinim listesi buradan çıkar.

## 2. Hedefler

1. **`discovery/recovery.py`**: I1–I21 → terim dili eşleme tablosu
   (`RECOVERY_TABLE`): her kayıt ya çevrilebilir (somut terim çiftleriyle) ya
   yapısal (dilin kendisinde gömülü) ya da çevrilemez (eksik özellik
   anahtarlarıyla). Kampanya koşucusu: çevrilebilir her çift için
   ispat + sayısal + sembolik üçlüsü.
2. **Beklenen eşleme** (ön analiz; test bunu doğrular):
   - Çevrilebilir: **I1** (Z·Z\*=Z\*·Z ve M-gerçelliği t≡conj(t) formunda),
     **I10** (komütasyon + seri Mueller yasası).
   - Yapısal: **I7/I8** (kuaterniyon↔Z çarpım uyumu = dilin Mul'ü).
   - Çevrilemez: I2-I6, I9, I11-I21 → eksik özellik grupları:
     (a) toplama + skaler katsayı (I15-I17), (b) dagger/bra-ket + Stokes
     (I9, I12-I14), (c) entry/trace/det düzeyi (I2, I5, I6, I19-I21),
     (d) kısıtlı/özel atomlar (I4, I11, I18).
3. **`docs/term-language-extensions.md`**: gereksinim listesi, öncelik
   sırasıyla (fizik değeri: önce toplama+skaler — koherent süperpozisyon).
4. Harvest-kanıtı: I1 çiftleri full-7 hasadında, I10 çiftleri mevcut
   testlerdeki hasatlarda görünür (CI-ucuz konfigürasyonlar).
5. **egglog upstream taslak issue** (`docs/egglog-upstream-issue-draft.md`):
   İngilizce, paketimizden BAĞIMSIZ kendi kendine yeten repro; mümkünse
   delta-debug ile küçültülmüş kayıt kümesi. GÖNDERİM kullanıcı onayına bağlı
   (kritik-karar); bu aşama yalnız taslağı üretir.

## 3. Mimari kararlar

- **M22. Kampanya kalıcı regresyondur**: RECOVERY_TABLE testle bağlanır;
  gelecekte dil genişledikçe "çevrilemez" kayıtlar çevrilebilire taşınır ve
  kampanya oranı ANCAK ARTABİLİR (monoton ilerleme guard'ı).
- **M23. Upstream taslağı repo içinde yaşar**, gönderilmiş sayılmaz;
  gönderim kaydı (tarih/link) ancak kullanıcı onayından sonra eklenir.

## 4. Katı kurallar

- K19. "Çevrilemez" hükmü eksik-özellik anahtarı OLMADAN verilemez.
- K20. Kampanyada her çevrilebilir çift üç katmandan da geçmeli
  (ispat + sayısal + sembolik); tek başarısızlık aşamayı kırar.

## 5-6. Teslim + Doğrulama

`discovery/recovery.py` · `tests/test_recovery.py` (tablo bütünlüğü K19,
kampanya K20, monotonluk M22 tabanı, harvest-kanıtı) ·
`docs/term-language-extensions.md` · `docs/egglog-upstream-issue-draft.md` ·
rapor. Tüm suite yeşil; kampanya çıktısı raporda tablo olarak.

## 7-9.

Push + rapor + Aşama 6 planlaması. Uyarı: M-gerçelliği çifti (t, Conj(t))
conj-normal DEĞİL — harvest kanıtı full (budanmamış) modda aranır. Kapsam
dışı: dil genişletmesinin kendisi (Aşama 6+ spec'lerine girdi), literatür
karşılaştırması, yeni tarama.

**DUR BURAYA**
