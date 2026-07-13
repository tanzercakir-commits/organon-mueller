# AŞAMA 1 — Kütüphane Genişletme + Serileştirme + egglog Spike

**Tarih**: 2026-07-13
**Önceki aşama**: stage-00 (temsil katmanı + 14 özdeşlik, 36/36 yeşil)

---

## 1. Bağlam

Aşama 0 zemini döktü. Bu aşama üç koldan ilerler: (a) özdeşlik kütüphanesi
PRA 95,063819 (koherent süperpozisyon) ve JOSA A 34,80 / Appl. Opt. 55,2543
(simetri sınıfları) özdeşlikleriyle genişler; (b) MCP-hazırlık serileştirme
katmanı (karar M4) yazılır; (c) egglog keşif motoru adayı zaman-kutulu bir
spike ile denenir — Aşama 2 spec'ini bu spike'ın bulguları şekillendirecek.

## 2. Hedefler

1. Yedi yeni özdeşlik (I15–I21), kaynak + koşul metadata'lı, regresyona bağlı.
2. `serialize.py`: HVector JSON round-trip (SymPy srepr tabanlı), kütüphane
   metadata'sının JSON dökümü, LaTeX üretim yardımcıları.
3. egglog spike: kurulum + kuaterniyon birim cebri fragmanının equality
   saturation ile modellenmesi; bulgular `docs/egglog-spike.md`.
4. `docs/ROADMAP.md`: frozen-N taslağı (Aşama 2 sonunda dondurulacak).

## 3. Mimari kararlar

- **M7. Kütüphane büyümesi geriye dönük değişmez**: I1–I14 anahtarları ve
  kontrolleri DONMUŞTUR; yeni özdeşlikler yalnızca eklenir (v1 motor-stabilite
  ilkesinin kütüphane karşılığı).
- **M8. Serileştirme srepr üzerinden**: SymPy ifadeleri `srepr` dizesi olarak
  taşınır (kayıpsız); JSON şeması {"tau": srepr, ...}. `eval` YOK —
  `sympy.parsing.sympy_parser` değil `sympy.sympify(..., strict yok)` yerine
  `sp.parse_expr`? Hayır: srepr geri yüklemesi `sympy.sympify` ile yapılır
  (srepr çıktısı sympify için güvenli kabul edilir; dış girdi doğrulaması MCP
  aşamasının işi, buraya not düşülür).
- **M9. Spike üretim koduna sızmaz**: egglog denemesi `spikes/` altında ayrı
  durur, `src/` bağımlılığı almaz; pyproject'e egglog EKLENMEZ.

## 4. Katı kurallar

- K6. Aşama 0 API imzaları değişmez (yalnızca ekleme).
- K7. Yeni özdeşliklerde de M2 disiplini: sembolik öncelik, sayısalda seed.
- K8. Spike süresi sınırlı; egglog'da tıkanma olursa bulgu olarak yazılır,
  aşama bloke olmaz.

## 5. Teslim

- `src/organon_mueller/identities/known.py`: I15–I21 eklenmiş.
- `src/organon_mueller/serialize.py` + `tests/test_serialize.py`
- `tests/test_fixtures.py`: yapay-QWP süperpozisyon sabitleyicisi.
- `spikes/egglog_quaternion.py` + `docs/egglog-spike.md`
- `docs/ROADMAP.md`
- `reports/stage-01-REPORT.md`, README durum tablosu güncel.

## 6. Doğrulama

| # | Özdeşlik | Kaynak | Koşul | Mod |
|---|---|---|---|---|
| I15 | Z=aZ_a+bZ_b ⇒ M=|a|²M_a+|b|²M_b+(ab*Z_aZ_b*+a*bZ_bZ_a*); çapraz terim gerçel | PRA 95,063819 Eq.(10) | koherent | sembolik |
| I16 | Z_b=e^{iφ}Z_a, a=b=1/√2 ⇒ M=M_a(1+cosφ) | PRA Eq.(25-26) | koherent | sembolik |
| I17 | Kovaryans haritası lineer: H(ΣwᵢMᵢ)=ΣwᵢHᵢ; konveks karışım rank-2 + iz koşulu ihlali | Cloude 1986; Gil | depolarizing | sembolik+sayısal |
| I18 | (1+i)/2·pol_H + (1−i)/2·pol_V süperpozisyonu = QWP durumu, M beklenen | PRA Eq.(15) | koherent | sembolik |
| I19 | (τ,α,0,0) üreteci ⇒ Tip-1 blok-köşegen M simetrisi | JOSA A Eq.(31); AO Eq.(7) | class2_ta | sembolik |
| I20 | (τ,0,β,0) üreteci ⇒ Tip-2 M simetrisi | JOSA A Eq.(31); AO Eq.(8) | class2_tb | sembolik |
| I21 | (τ,0,0,γ) üreteci ⇒ Tip-3 M simetrisi | JOSA A Eq.(31); AO Eq.(9) | class2_tg | sembolik |

Serileştirme: round-trip generic + rastgele sayısal; JSON şema geçerliliği.
Spike kabul: kuaterniyon birim ilişkileri (ij=k, i²=−1, ...) e-graph'ta
sature edilip i·j·k ≡ −1 türetimi gösterilir VEYA engel raporlanır.

## 7. Teslim formatı

Aşama 0 ile birlikte kullanıcının `C:\Projects\organon-mueller` klonuna;
köprü kapalıysa zip + otomatik yeniden deneme.

## 8. Özel uyarılar

1. I15 gerçellik ispatı I10 komütasyonuna dayanır — testte bağımsız expand ile
   doğrula, I10'a çağrı zinciri kurma.
2. Simetri üreteçlerinde "sıfır olmalı" girdileri açıkça listele (pattern
   testi), sadece "eşitlik" değil.
3. srepr→sympify round-trip'inde Float hassasiyeti: `Float(x, precision)`
   korunur; testte tam eşitlik yerine srepr-eşitliği kullan.
4. egglog Python API'si hızlı evriliyor; sürümü spike raporuna yaz.

## 9. Kapsam dışı

- Keşif motorunun kendisi (Aşama 2+, spike bulgularına göre)
- Ayrışım türetici, dipol modülü
- MCP server implementasyonu (yalnızca serileştirme hazırlığı)
- Depolarize H için genel rank-3/4 ayrışımları

**DUR BURAYA**
