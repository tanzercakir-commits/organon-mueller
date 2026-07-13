# Yenilik Protokolü — "Yeni Özdeşlik" Aday Zinciri

Motorun `underivable` kanalı (sayısal doğru + sembolik-kesin ispatlı +
aksiyomlardan türetilemeyen çift) bir **aday** üretir; hiçbir otomatik adım
"yeni özdeşlik bulundu" İDDİASI üretemez. Zincir:

```
underivable çifti (M16/M19: zaten kesin-ispatlı)
 └─ 1. Kanonik sunum: çiftin en küçük temsilcisi + LaTeX (serialize katmanı)
 └─ 2. Kütüphane karşılaştırması: KNOWN_IDENTITIES (I1–I21+) ile yapısal
      eşleme — bilinenin yeniden parametrizasyonu mu? (recovery tablosu
      buradaki ilk filtre)
 └─ 3. Aksiyom-boşluğu analizi: türetilemezlik YENİ matematik mi, yoksa
      aksiyom setinin bilinen-ama-kodlanmamış bir yasası mı? (ikincisiyse
      çıktı "yeni özdeşlik" değil "eksik aksiyom" olarak sınıflanır — o da
      değerli, ama farklı bir şey)
 └─ 4. Literatür kontrol listesi (işaretleme, iddia değil):
      □ Gil, Eur. Phys. J. Appl. Phys. 40, 1 (2007) — polarimetrik cebir derlemesi
      □ Gil, J. Appl. Remote Sens. 8, 081599 (2014) — Mueller cebiri review
      □ Cloude, Optik 75, 26 (1986) — kovaryans/spektral ayrışım
      □ Ossikovski hattı (differential/depolarizing decompositions)
      □ Kuntman korpusu (JOSA A 34,80; PRA 95,063819; PRB 98,045410;
        arXiv:1705.07147; AO 55,2543) — proje PDF'leri
      □ Genel: Aiello-Woerdman lineer cebir notları; Chipman
 └─ 5. UZMAN KAPISI: 1-4'ü geçen aday "literatürde izine rastlanmadı"
      etiketiyle rapora girer; fizik-anlam/yayın-değer hükmü İNSANDA
      (Kuntman/kullanıcı — kritik-karar eşiği: dış temas + fizik yorumu).
```

## Negatif sonuç disiplini (M24)

Boş `underivable` kanalı raporlanabilir bir gözlemdir: "taranan fragman ve
boyutta aksiyom seti ampirik olarak tam." Bu, genişletme önceliklendirmesine
kanıt sağlar (hangi fragman doyduysa oradan derinleşmek yerine dil genişletilir).

## Kayıt

Her tarama `reports/sweep-NN-results.json` artefaktıyla kalıcıdır (K21:
konfig + tohumlar gömülü, deterministik yeniden üretim). Aday çıkarsa bu
protokolün 1-4 çıktıları rapora, 5 kararı kullanıcıya gider.
