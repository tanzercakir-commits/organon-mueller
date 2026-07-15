# AŞAMA 16 — RAPOR (FAZ E Açılışı: LaTeX Rapor Üreteci)

**Tarih**: 2026-07-14 · **Spec**: `specs/stage-16.md` · **Mod**: otonom
**Sonuç**: TAMAMLANDI — 215/215 test yeşil; `reporting/` modülü + Kuntman
paketine örnek rapor (`sample-report.tex`, pdflatex ile derleniyor).

## 1. Teslim edilenler

- **Kanıt-sınıfı disiplini kurumsallaştı**: her blok `evidence ∈
  {symbolic-proof, numeric-deterministic, candidate}` (VERIFICATION.md
  katmanlarına bağlı); şablon FİİLLERİ etikete göre ("proven" yalnız
  symbolic-proof); bilinmeyen etiket fırlatır.
- **Blok üreteçleri**: üç ayrışım tipi (+rank-3 teklik-dışılık notu her
  sonuçta), skor-sıralı hipotez tablosu (gerekçeli retler, "skor sıralar
  kabul etmez" çerçevesi), M32 dörtlü-kanıt tablosu (aday dili), dipol
  γ-haritası + ensemble istatistikleri (satır-başına istatistik etiketi).
- **Determinizm**: bayt-bayt aynı çıktı (süreçler-arası sha256 teyitli);
  \today/timestamp yasak (testli); sabit yuvarlama + **alt-eşik büyüklük
  bilimsel gösterim** kuralı.
- **Güvenlik** (A17 hazırlığı): yalnız kendi sonuç nesnelerimizden LaTeX;
  serbest metin escape'li (enjeksiyon probe'ları: \input, \write18, $(rm)
  — hepsi etkisiz, denetçi doğruladı); pdflatex -no-shell-escape.

## 2. Bağımsız denetim — yine iki tur

İlk verdict **FAIL (koşullu)**, D1 MAJOR: `_fmt` 6.7e-16'yı "0" basıyordu
— makine-hassasiyeti artığını KESİNLİK iddiasına çeviren, tam da bu
aşamanın kurumsallaştırdığı sözleşmenin ihlali (A15 dersinin ayna hali).
Düzeltme: alt-eşik büyüklükler deterministik bilimsel gösterime düşer
(\ensuremath sarmalı — metin/matematik iki modda geçerli); NaN/Inf
fırlatır (K26); sabit yuvarlama-kuralı cümlesi her raporun dipnotunda.
+ D2 (tolerans iddiası inceltildi), D3 (istatistik etiketi satır-başına),
D4 (gerçek matematik \alpha, \mathrm{i}), süreç-dili sızıntısı temizliği.
Yeniden doğrulama: **PASS** (enjeksiyon/derleme/determinizm probe'ları
dahil). Örnek rapor artık artıkları dürüst basıyor (6.7×10⁻¹⁶ vb.).

## 3. Kapsam kararı (kayıt)

Guarded-atoms 2. yarı **A20'ye ertelendi** (spec §2 gerekçeli): Faz E'nin
ihtiyacı novelty-kanalının RAPORLANABİLMESİ — `guarded_finding_section`
bunu teslim etti; yeni kampanyalar konsolidasyon taramasının işi.

## 4. Sıradaki aşama (otonom devam)

**Aşama 17 — MCP server**: ÖNCE serialize.py sympify STAGE-2 GATE
güvenlik sertleştirmesi (dış girdi hiçbir koşulda ham sympify'a gitmez);
dış yüzey ancak ondan sonra. Rapor üreteci sunucunun ana çıktı kanalı.
