# Faz C Retrospektifi (A8–A11) — stage-11

v1 iter geleneği; Faz B retrospektifi stage-07 raporundaydı, Faz C'ninki
bağımsız doküman (ayrışım katmanı kalıcı bir alt-sistem haline geldi).

## 1. Ne kuruldu

`decomposition/` paketi dört adımda: türetici (A8: Tablo 2, 6/6 sembolik
birebir) → bileşik tipler (A9: Tablo 4, 3/3) → rank-3 (A10: makale-ötesi,
M34 çerçevesi) → köprü + skorlar (A10-11). Yanında guarded-atoms ilk
yarısı (A9) `underivable` kanalının ilk dolu çıktısını verdi.

## 2. Karar/kural tutarlılık taraması (M28–M34, K26–K32)

- **M28 (denklemler türetilir, kopyalanmaz)** — üç aşamada da korundu;
  rank-3'te anchor'ın kendisi yokken bile türetim disiplini değişmedi.
- **M29 (baz ayrımı)** / **M30 (OCR güvenilmezliği — üst-çizgi kayıpları
  çapa girişlerinde gerekçeyle belgelenir)** / **M31 (bileşik ayrı
  modül)** / **M33 (tek yönlü katmanlama)** — dosya yapısı bu sınırlara
  birebir uyuyor; rank3 yalnız solve'un PUBLIC decompose'unu çağırıyor;
  M30 disiplini Tablo-2/4 çapa notlarında ve iki baskı-hatası teşhisinde
  işledi.
- **M32 (Horn hüküm formatı)** — dörtlü kanıt kaydı `GuardedFinding`'te;
  guard'sız-yanlış kontrolü zorunlu ve test ediliyor.
- **M34 (makale-çapası ikamesi)** — üç katman (probe'lu el türetimi +
  türetici birebirliği + bağımsız denetçi türetimi) A10'da tam işledi;
  denetçi beş formülü ve payda yorumlarını bağımsız doğruladı.
- **K26 (sessiz yanlış yok)** — iz-1, sonluluk, payda, alan, PSD/rank-1,
  tutarlılık (K32) guard'ları üç çözücüde; "yanlış SEBEPLE ret" bile
  kusur sayıldı ve düzeltildi (merkez-only sınır ailesi).
- **K28 çapa disiplini** — Tablo 2/4 çapaları elle girilip AYRI test
  dosyalarında; rank-3'te bilinçli olarak K28 yerine M34.
- **K27 (deterministik tohumlar)** — tüm sweep/kampanya/roundtrip
  testleri sabit tohumlu (20260713, 424242; K32 ailesi 0); artefaktlar
  tohumları taşıyor (K21 ile birlikte).
- **K29/K31 (yapısal minor guard'ları)** — türetim zamanı fırlatır;
  çözüm-sırası duyarlılığı (K31) rank-3'ün yeni katkısı.
- **K30 (kısıt-inşayla, varsayım-enjeksiyonsuz)** — guarded üreteçler
  parametrizasyonla kısıtlanıyor; sympy assumption enjeksiyonu yok;
  sadakat meta-testi (stage-11) bunu yapısallaştırdı.
- **K32 (fazladan-belirlenim zorunlu kontrol)** — denetçinin MAJOR'ı
  üzerine kendi regresyon testine kavuştu (tüm-reel aile, tohum 0).

## 3. Teknik borç envanteri

| Borç | Durum | Gerekçe/pencere |
|---|---|---|
| rank-3 a/b minor varyantları (M33 notu) | ERTELENDİ | varyant paydaları yalnız ölçü-sıfır dejenerasyonlarda ayrışıyor (u₁=0 vs u₂=0); gürültülü gerçek veri bu noktalara oturmaz; deneysel veri geldiğinde açılır |
| köprü v1 ön-sıralama | KAPANDI (stage-11) | `ProposeReport.scores`, payda-sağlığı skoru; yalnız sıralar |
| guard-üreteç sadakati (tasarım-notu Y1) | YAPISALLAŞTI (stage-11) | GUARD_KEYS↔üreteç meta-testi; yeni anahtar üreteçsiz giremez |
| interpreted_scalars payda yan-koşulları (Y2) | KOŞULLU BORÇ | özellik dilde yok (K19); dile girdiği aşamada zorunlu kabul maddesi |
| guarded-atoms 2. yarı (unitary/hermitian kampanyaları) | AÇIK | Faz D-E arasına; şu an üreteç+sadakat testiyle sınırlı (dürüst kapsam) |
| stage-10 denetçi önerileri | KAPANDI (stage-10) | primary="center" inşa, sonluluk, K32/u₀=u₃/çapraz-çift testleri, sıfır-matris guard'ı |

## 4. Dersler

1. **Probe-before-spec iki kez kazandırdı**: yanlış unitary hedefi (A9)
   koda değmeden elendi; tip-3 kenar işaret hatası (A10) spec'e girmeden
   yakalandı. Kural artık yürütme zincirinin parçası.
2. **pytest'i pipe'lama kuralı bir kez ihlal edildi** (A10 içinde, tail
   ile) — çıktı exit'i maskeledi; aynı turda fark edilip bare tekrar
   koşuldu. Kural hatırlatıcısı proje dokümanında kalıyor.
3. **"Negatif kontrol reddedilmeli" varsayımı yanlıştı**: rank-3'te
   kabul edilen alternatif GEÇERLİ çıktı (teklik-dışılık). Doğru çerçeve
   "kabul → doğrula": sweep artık kabul edilen alternatifleri ayrıca
   doğruluyor. Ders: dürüstlük, reddetmekte değil doğrulamakta.
4. **Denetçi katmanı teorem üretiyor**: reshuffle özdeşliği (A8), {2,3}
   hipotez-içi teklik ispatı (A10) denetimden çıktı — katman 5 yalnız
   hata bulmuyor, matematiği güçlendiriyor.

## 5. Faz D'ye devir

Coupled-dipole modülü (A12-15) için hazır zemin: HVector/kuaterniyon
temsilleri, keşif motoru + guarded atoms (dimer simetrileri doğal guard
adayları), ayrışım çözücüleri (dimer kovaryanslarının tip analizi),
novelty protokolü. Kuntman paketi feedback'i Faz D iç sırasını
değiştirebilir (FROZEN-22 gereği sayı/kapsam değişmez).
