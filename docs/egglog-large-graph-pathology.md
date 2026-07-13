# egglog 13.2.0 Büyük-Graf Patolojisi (Aşama 3 bulgusu)

**Tarih**: 2026-07-13 · **egglog-python**: 13.2.0 · **Durum**: motor v1.1 ile
etrafından dolaşıldı (karar M18); kök neden üstümüzde (kütüphane) — izlenecek.

## Gözlem

Tam enumerasyonun (conj-normal, boyut 9, 1476 terim) TEK paylaşılan e-graph'ta
sature edilmesi tutarsız sonuçlar verdi:

1. `b·(a·conj(a)) == b·(conj(a)·a)` — yalıtılmış iki-terimli grafta İSPATLANIR
   (asosiyatiflik + atom komütasyonu); 1476-terimli grafta `check` BAŞARISIZ,
   ek 30 iterasyon da düzeltmiyor. Çocuk sınıflar (a·conj(a) ≡ conj(a)·a)
   birleşikken ebeveynler ayrı kalıyor — kongruans kapanışına aykırı görünüm.
2. Daha vahimi: `extract(b·(conj(a)·a))` sonucu **b içermeyen** bir temsilci
   (`a·(a·conj(a·a))`) — farklı atom-çokkümesinden bir sınıf. Aksiyomların
   hiçbiri atom çokkümesini değiştiremeyeceğinden bu ya hatalı bir birleşme
   ya da taze-düğüm ekleme/kanonikleştirme hatası.
3. Aynı çiftler 5698-terimli BUDANMAMIŞ grafta doğru çıkabiliyor — davranış
   kayıt kümesine duyarlı, deterministik olarak yeniden üretilebilir
   (`spikes/egglog_pathology_probe.py`).

## Etki ve savunma

- Motor hiçbir zaman e-graph'a tek başına güvenmiyordu (karar M10); nihai söz
  bağımsız çok-tohumlu sayısal doğrulamada. Patoloji tam da bu katman
  sayesinde yakalandı: sahte "underivable" çiftler sayısal olarak doğru ama
  ispatsız görününce alarm verdi.
- **v1.1 (karar M18)**: paylaşılan büyük graf kaldırıldı; her aday çift kendi
  taze iki-terimli e-graph'ında ispatlanıyor. Yalıtılmış modda tüm problarda
  tutarlı davranış; 9/9 takılan çift ispatlandı.

## Elenen hipotezler (2026-07-13, kullanıcı sorusu üzerine)

- **Bellek yönetimi**: hayır — graflar küçük (≈10³ düğüm), hata deterministik
  ve içerik-bağımlı; daha büyük (5698) graf doğruyken daha küçüğü (1476)
  hatalı — bellek baskısı deseniyle uyumsuz.
- **`seminaive` bayrağı**: hayır — `EGraph(seminaive=False)` ile de aynı
  davranış (her iki ayarda test edildi). API'de başka ilgili konfigürasyon
  yüzeyi görünmüyor (`RunConfig` iterasyon/scheduler düzeyi; ek iterasyonlar
  zaten denendi).

## Açık iş

- ~~Upstream'e bildirim~~ — **kullanıcı kararı (2026-07-13): bildirim
  YAPILMAYACAK** ("tek geliştirici benim; biz paketi sunacağız"). Repro ve
  analiz repoda kalıyor; plan değişirse yeniden değerlendirilir.
- egglog sürüm yükseltmelerinde probe script yeniden koşulmalı.
