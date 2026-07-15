# organon-mueller — Yol Haritası — **FROZEN-22** (ilan: Aşama 2, 2026-07-13)

**22 aşama, 6 faz — DONDURULDU** (Organon v1 geleneği; v1'de frozen-55).
Bu sayı artık değişmez; değişiklik ancak kritik-karar notuyla kullanıcıya
gider. Kuntman/grup geri bildirimi C ve D fazlarının İÇ sırasını
değiştirebilir, aşama sayısını değiştiremez.

```
FAZ A — Zemin (Aşama 0–2)
├── 0  Temsil katmanı + 14 özdeşlik regresyonu            ✅ (36/36)
├── 1  Kütüphane genişletme (21 özdeşlik) + serileştirme
│      + egglog spike (BAŞARILI, hibrit mimari önerisi)    ✅ (50/50)
└── 2  Keşif motoru çekirdeği v0: hibrit egglog+SymPy,        ✅ (56/56)
       enumerasyon+saturasyon+hasat+%100 doğrulama;
       R1-R3 yeniden keşfi, negatif kontroller → FROZEN-22 İLANI

FAZ B — Keşif motoru (Aşama 3–7)                            ✅
├── 3  Terim enumerasyonu + karmaşıklık sınırları           ✅ (M18 yalıtılmış ispatlar)
├── 4  Aday boru hattı: sayısal ön-elek → sembolik ispat    ✅ (M19 sertifikasyon)
├── 5  Geri-kazanım kampanyası: motor I1–I21'i KENDİSİ bulmalı ✅ ({I1,I10,I15})
├── 6  Yeni aday taraması #1 + literatür karşılaştırma disiplini ✅ (fragman tamlığı TEOREM)
└── 7  İterasyon değerlendirmesi (v1 iter geleneği)          ✅ (Sum/Scale; AL ince ayrımı)

FAZ C — Ayrışım türetici (Aşama 8–11)                       ✅
├── 8  Simetri-koşullu ayrışım: AO2016'nın 6 tipinin otomatik türetimi ✅ (Tablo 2 6/6; reshuffle TEOREM)
├── 9  Rank-2 genel çözücü                                  ✅ (Tablo 4 3/3; guarded atoms M32)
├── 10 Rank-3 keşif taraması (yayın-aday yeni sonuç potansiyeli) ✅ (teklik-dışılık bulgusu)
└── 11 İter + Kuntman feedback penceresi #1                 ✅ (paket hazır; köprü v1)

FAZ D — Dipol modülü (Aşama 12–15)                          ✅
├── 12 Coupled-dipole sembolik motor (PRB 98,045410 yeniden türetim) ✅ (Eq. 25 ayrışım TEOREM)
├── 13 γ (optik aktivite) parametresinin yön-genel otomasyonu ✅ (Perrin genel teoremi)
├── 14 N-dimer / ensemble genellemesi (OA-ensemble açık uçları) ✅ (δ=0⇒γ_z≡0; köprü uçtan-uca)
└── 15 İter + feedback penceresi #2                         ✅ (dipol EK; M30×8)

FAZ E — Paketleme (Aşama 16–19)                             ✅ (A19'da)
├── 16 LaTeX/rapor üretici (bulgu → makale malzemesi)       ✅ (kanıt-etiketli, deterministik)
├── 17 MCP server (decompose/propose/discover/report)       ✅ (GATE sertleştirmesi; HOST edilmedi)
├── 18 Web arayüzü — STATİK, hosting'siz (karar değişti: Streamlit yerine ✅ (textContent XSS-güvenli)
│      tek dosya web/index.html; sunucu yüzeyi = saldırı yüzeyi)
└── 19 Dokümantasyon (README/architecture/user-guide)       ✅ (bu aşama)

FAZ F — Kapanış (Aşama 20–22)                               ⏳
├── 20 Yayın-aday sonuçların konsolidasyonu (+guarded-atoms 2. yarı borcu)
├── 21 Dış doğrulama (grup feedback, bağımsız tekrar)
└── 22 v2.0 kapanış değerlendirmesi + retrospektif
```

Durum (Aşama 19): A0–A19 tamamlandı; **286 test yeşil**. Kalan: Faz F
(A20–A22). Not: FROZEN-22 aşama SAYISI değişmez; A18'in "hosted" tanımı
güvenlik gerekçesiyle "statik, hosting'siz"e revize edildi (kapsam
değişikliği, sayı değişikliği değil — retrospektifte gerekçeli).

Süre kalibrasyonu (handoff): sıkı odakta 2–4 ay, part-time 6–12 ay.
Aşama ≈ v1'deki milestone tanesi; her aşama spec → impl → test → rapor
döngüsüyle kapanır.
