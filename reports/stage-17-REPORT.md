# AŞAMA 17 — RAPOR (MCP Server + sympify GATE Sertleştirmesi)

**Tarih**: 2026-07-14 · **Spec**: `specs/stage-17.md` · **Mod**: otonom
**Sonuç**: TAMAMLANDI — 268/268 test yeşil; **STAGE-2 GATE KAPANDI**
(eval'e hiç girmeyen kısıtlı srepr parser); MCP tool yüzeyi + server kodu
(HOST EDİLMEDİ — kritik karar kullanıcıda); güvenlik denetimi BEŞ tur
sonunda PASS.

## 1. Teslim edilenler

- **`safe_parse.py`** — kısıtlı srepr parser: `ast.parse` + BEYAZ-LİSTE
  yürüyüşü; **eval/sympify metin yolunda YOK** (denetçi canary ile
  kanıtladı: 0 sympify-on-string çağrısı). `serialize.hvector_from_dict`
  artık buraya geçer; GATE docstring'i "CLOSED" olarak güncellendi.
- **`mcp_server/`** — SAF tool fonksiyonları (SDK'sız test edilir):
  decompose_mueller / propose_hypotheses / guarded_campaign_info /
  generate_report; girdiler yalnız sayı + enum string (ifade metni sınırı
  hiç geçmez); hatalar `{"error": gerekçe}` (iz sızdırmaz). FastMCP
  sarmalayıcı (`[mcp]` opsiyonel extra); `python -m
  organon_mueller.mcp_server` (stdio) — README-mcp.md.
- **HOST ETME YOK**: sunucu hiçbir yerde başlatılmaz/expose edilmez;
  çalıştırma/paylaşma kararı kullanıcıda (kritik-karar protokolü).

## 2. Güvenlik denetimi — BEŞ tur (güvenlik sınırı, sonuna kadar)

Denetçi kötü-niyetli girdilerle saldırdı; her tur yeni açık, her açık
kapatıldı, aynı denetçi yeniden saldırdı:
- **Tur 1**: anti-eval sağlam AMA 5 açık — D1 (DoS büyüklük), D2 (ham
  MemoryError sızıntısı), D3 (tool tolerans TypeError sızıntısı), D4
  (non-finite geçişi), D5 (regex \n bypass).
- **Tur 2**: D2-D5 kapandı, D1 yarım (exponent sınırlandı ama sonuç
  değil) + regresyon (küçük Float srepr'leri kırıldı).
- **Tur 3**: D1 sonuç-büyüklüğü projeksiyonu + regresyon düzeltildi;
  S1 (Float exponent materialize) + S2 (Mul-fold materialize) kaldı.
- **Tur 4**: S1/S2 fold-öncesi projeksiyonla kapandı; non-integer Pow
  exponent sınıfı (Float/büyük Rational) bulundu.
- **Tur 5**: her exponent tipi + base'e gömülü sayısal atomlar projekte
  edildi → **PASS**. Denetçi kalan tüm yüzeyi (sembolik-base^huge,
  exponent-folding sırası, nested Pow, negatif/I base, conjugate) taradı;
  hiçbiri huge sayı materialize etmiyor/>1s yakmıyor/kod çalıştırmıyor.

Guard'lar: metin ≤64KB, düğüm ≤2000, derinlik ≤64, digit ≤4096, bit
≤16384, exponent ≤10⁶; Symbol regex fullmatch; non-finite ret; Float
exponent yasak; Pow/Mul/Add fold-öncesi büyüklük projeksiyonu. Meşru
kütüphane korpusu (220 ifade) hiçbir şey kaybetmeden roundtrip.

## 3. Sıradaki aşama (otonom devam)

**Aşama 18 — Opsiyonel web UI**: statik HTML+JS demo sayfası (hosting
YOK — aynı kritik-karar kuralı); MCP tool'larının/rapor üretecinin
tarayıcıdan gösterimi. Kapsam kararı spec'te (statik + client-side vs
sunucu bağımlı — güvenlik gerekçesiyle statik öneriliyor).
