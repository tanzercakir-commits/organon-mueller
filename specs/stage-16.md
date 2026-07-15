# AŞAMA 16 — LaTeX Rapor Üreteci (FAZ E açılışı)

**Tarih**: 2026-07-14 · **Mod**: otonom · **Probe notu**: yeni matematiksel
mekanizma YOK → sayısal probe gerekmiyor; ortam probe'u yapıldı
(pdflatex/latexmk/xelatex mevcut → PDF derleme testli, CI'da
skipif-korumalı).

## 1. Hedefler — `reporting/` modülü

1. **Kanıt-sınıfı etiketleri** (A15 dersi kurumsallaşıyor): her rapor
   bloğu `evidence ∈ {symbolic-proof, numeric-deterministic, candidate}`
   taşır; etiketler VERIFICATION.md katman 1/2/novelty-kanalına bağlanır;
   şablon fiilleri etikete göre seçilir ("proven" yalnız symbolic-proof).
2. **Blok üreteçleri** (M28 ruhu: sonuç nesnelerinden, elle metinden
   değil): `decomposition_section` (DecompositionResult / CompositeResult
   / Rank3Result — α'lar, bileşen matrisleri, guard bilgisi),
   `propose_section` (skor-sıralı tablo + GEREKÇELİ retler — K21),
   `guarded_finding_section` (M32 dörtlü kanıt tablosu + aday dili),
   `dipole_section` (γ-haritası değerleri + ensemble istatistikleri).
3. **Determinizm**: aynı girdi → bayt-bayt aynı LaTeX (test); \today ve
   zaman damgası YASAK (tarih açık parametre); sayısal yuvarlama sabit
   (6 hane); tohumlar/tekrar-üretim bilgisi her blokta (K21).
4. **Güvenlik** (A17 MCP hazırlığı): üreteç YALNIZ kendi sonuç
   nesnelerimizden LaTeX YAZAR — dış girdi sympify edilmez (STAGE-2 GATE
   ile uyum); serbest metin (başlıklar, ret gerekçeleri) LaTeX-escape
   edilir; pdflatex `-no-shell-escape` ile çağrılır.
5. **PDF derleme**: `compile_pdf` (nonstopmode, no-shell-escape; hata
   log kuyruğuyla fırlatır); test `skipif(pdflatex yok)` — CI'da dürüst
   opsiyonellik.
6. **İlk senaryo**: `build_kuntman_report()` — demo.main() sonuçlarını
   rapora döker; `docs/kuntman-package/sample-report.tex` ÖRNEK çıktı
   (gönderim değil); PDF derlenebilirliği testte.
7. Şablonda fizik-yorumu İDDİASI yok; novelty adım-5 dipnotu sabit.

## 2. Guarded-atoms 2. yarı — kapsam KARARI (retrospektif borcu)

**A20'ye ERTELENDİ.** Gerekçe: (i) Faz E'nin ihtiyacı novelty-kanal
çıktılarının RAPORLANABİLMESİ — `guarded_finding_section` bunu bu aşamada
teslim ediyor; (ii) unitary/hermitian kampanyaları yeni bilinen-gerçek
üretir (mekanizma ispatı A9'da class2 düzlemleriyle tamamlandı) —
konsolidasyon taramasının (A20) doğal parçası; (iii) araya sıkıştırmak
Faz E'nin dış-yüzey güvenlik odağını (A17 GATE) sulandırır.

## 3. Kabul

Determinizm testi (bayt-bayt); üç ayrışım tipi + propose + guarded +
dipol blokları render; kanıt-etiket eşlemesi zorunlu (bilinmeyen etiket
fırlatır); escape testi; \today/timestamp yasağı testi; Kuntman örnek
raporu üretilir + pdflatex ile derlenir (skipif'li); 204 eski test yeşil.

**DUR BURAYA**
