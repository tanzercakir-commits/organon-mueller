# AŞAMA 5 — RAPOR

**Tarih**: 2026-07-13 · **Spec**: `specs/stage-05.md` · **Mod**: otonom
**Sonuç**: TAMAMLANDI — 80/80 test yeşil; geri-kazanım kampanyası çalışıyor;
terim dilinin sınır haritası çıktı; egglog upstream taslağı hazır (gönderilmedi).

---

## 1. Geri-kazanım kampanyası sonucu

Motor, elle kodlanmış I1–I21 kütüphanesinin terim diline çevrilebilen alt
kümesini üç katmandan (e-graph ispatı + sayısal + sembolik-kesin, K20)
geçirerek KENDİ başına yeniden buldu:

| Durum | Özdeşlikler | Not |
|---|---|---|
| **Kazanıldı (2)** | I1 (Z·Z\*=Z\*·Z **ve** M-gerçelliği t≡conj(t) formunda), I10 (komütasyon + seri Mueller yasası) | 4/4 çift üç katmandan geçti; harvest-kanıtı testli |
| **Yapısal (2)** | I7, I8 | Dilin semantiğinin tanımı (motor kendi yorumlama fonksiyonunu "keşfedemez") — denetçi bu kategorinin dürüstlüğünü ayrıca savundu; suite'te sembolik ispatları zaten var |
| **Çevrilemez (17)** | kalanlar | Her biri adlandırılmış eksik-özellik anahtarlarıyla (K19) |

Eksik-özellik birleşimi → `docs/term-language-extensions.md` (önceliklendirilmiş):
1) `addition`+`scalars` (koherent süperpozisyon, I15-I18) → **Aşama 6+ ana hedef**;
2) `guarded_atoms` (I4, I12-I13, I19-I21) → Faz C bağlantısı;
3) `dagger`+`stokes_sort` (I9, I13-I14) — denetçi dagger'ın mevcut dilde
   ifade EDİLEMEZLİĞİNİ derece argümanıyla ispatladı;
4) `entry_level` — e-graph'a girmeyecek, SymPy katmanında kalacak;
5) `constants`.
M22 monotonluk guard'ı: dil genişledikçe kazanım seti yalnız BÜYÜYEBİLİR.

## 2. egglog upstream taslağı (M23 — GÖNDERİLMEDİ)

`docs/egglog-upstream-issue-draft.md`: İngilizce, paketten bağımsız,
kendi kendine yeten repro. Delta-debug ile küçültüldü: **tek ground kural +
29 kayıtlı terim** — çocuk sınıflar birleşiyor, sözdizimsel özdeş ebeveynler
birleşmiyor (kongruans ihlali); kayıt SIRASINA bağlı (çift önce kaydedilirse
geçiyor); seminaive/ek-iterasyon etkisiz. Denetçi taslak kodunu birebir
çalıştırıp tüm kontrol tablosunu ve 29 terimin **1-minimalliğini** (her tekil
çıkarma hatayı yok ediyor) doğruladı. Gönderim kullanıcı onayı bekliyor.

## 3. Bağımsız denetim

Verdict: **PASS** (iki doküman-satırı düzeltmesi şartıyla — yapıldı).
Denetçi 21 kaydın her birinin hükmünü tek tek sorguladı: I1-gerçellik
çevirisinin sadakati (elementwise conj ⇔ gerçeklik), I7/I8'in "yapısal"
kategorisinin meşruiyeti, dagger'ın ifade edilemezliği (derece-homojenlik
argümanı) ve kısmi-gölge taraması (I15 çapraz-terimi = I10'a eşdeğer, zaten
kazanılmış). Uygulanan öneriler: genişletme tablosu birleşim-semantiğine
düzeltildi (I18/I2 satır hataları), kampanyaya bilinmeyen-durum guard'ı +
katman-bazlı hata kaydı eklendi, patoloji↔taslak çapraz referansı ve I15
kısmi-gölge notu işlendi.

## 4. Sıradaki aşama (otonom devam; kullanıcı direktifi: aralık 5 dk)

**Aşama 6 — Yeni-aday taraması #1 + literatür karşılaştırma disiplini**:
mevcut dil fragmanında (2-3 atom, derin boyut) sistematik tarama; `underivable`
kanalı boş çıkarsa (aksiyomlar tam görünüyor) bu KENDİSİ raporlanabilir bir
tamlık gözlemi; paralelde `addition`+`scalars` genişletmesinin tasarım notu
(Aşama 7 spec girdisi). "Yeni" iddiası için literatür karşılaştırma şablonu.
