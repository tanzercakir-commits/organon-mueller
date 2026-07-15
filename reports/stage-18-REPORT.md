# AŞAMA 18 — RAPOR (Opsiyonel Web UI — statik, hosting'siz)

**Tarih**: 2026-07-14 · **Spec**: `specs/stage-18.md` · **Mod**: otonom
**Sonuç**: TAMAMLANDI — 276/276 test yeşil; `web/index.html` statik sonuç
görüntüleyici; XSS-odaklı denetim (2 tur) PASS; HOST EDİLMEDİ.

## 1. Teslim edilenler

- **`web/index.html`** — tek dosya, inline CSS+JS, CDN'siz, sunucu YOK.
  Kullanıcı MCP/CLI tool çıktısını (JSON) yapıştırır → ayrışım ağırlıkları,
  bileşen matrisleri, propose skor-tablosu (gerekçeli retlerle), rapor
  LaTeX'i güvenli biçimde render edilir. Gömülü "Load example" (gerçek
  tool çıktısı, şema-tutarlı). Sınır dürüstçe yazılı: "hesap Python
  paketinde; bu sayfa yalnız sunum."
- **Kapsam kararı**: pyodide DEĞİL (dürüstlük + hafiflik) — sunum katmanı;
  hesap backend'de. Hosting YOK (A17 güvenlik çizgisi; sunucu yüzeyi =
  saldırı yüzeyi).

## 2. Güvenlik

- **XSS sınırı**: kullanıcı/JSON verisi YALNIZCA `textContent` ile basılır
  (`el()` yardımcısı); `innerHTML`/`insertAdjacentHTML`/`document.write`
  YOK. Denetçi 247 payload (19 alan × 13 vektör) denedi: hiçbiri script
  çalıştırmadı/dialog açmadı/canlı eleman enjekte etmedi.
- **CSP**: `default-src/img-src/connect-src 'none'` → ağ EGRESS engelli
  (dış `<img>`/`fetch` "csp" ile reddediliyor); dürüst not: CSP'nin işi
  egress, XSS backstop DEĞİL (textContent asıl sınır — belgede açık).
- **Prototype pollution YOK**: `KNOWN = Object.create(null)` + `typeof
  === "function"` guard; `__proto__`/`constructor` anahtarları
  "unrecognized field" olarak GÖSTERİLİR (K21), çökmez/sessizce atılmaz.
- `eval`/`Function`/`fetch`/`XMLHttpRequest` YOK.

## 3. Bağımsız denetim (2 tur)

Tur 1: **PASS** (güvenlik) + 3 robustluk kusuru — D1 (proto-zincir
lookup: __proto__ çökme / constructor sessiz yutma, K21 ihlali), D2
(derin-nested JSON.stringify RangeError → boş sayfa), D3 (CSP unsafe-
inline XSS backstop değil — bilgilendirme). Tur 2: **PASS** — D1
`Object.create(null)` ile, D2 tam gövde try/catch + safeStringify ile
kapandı; D3 dürüstçe belgelendi (script-hash yerine — statik dosyada
kırılgan olurdu); string-olmayan note kenarı da kapatıldı. Denetçi
prototype-zincir anahtarlarını, 500k-derinlikli payload'ları yeniden
saldırdı — hepsi zarif (≤0.69s), pollution yok, egress yok.

## 4. Sıradaki aşama (otonom devam)

**Aşama 19 — docs**: kullanıcı kılavuzu + kurulum + API genel bakışı +
mimari (katmanlar: algebra → identities → discovery → decomposition →
dipoles → reporting → mcp_server → web; doğrulama sözleşmesi; paketleme
üç yüzey: paket/MCP/web). README ana giriş; Faz F'ye (A20 konsolidasyon,
A21 dış doğrulama, A22 v2.0 kapanış) hazırlık.
