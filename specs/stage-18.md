# AŞAMA 18 — Opsiyonel Web UI (statik; HOST ETME YOK) (Faz E 3/4)

**Tarih**: 2026-07-14 · **Mod**: otonom · **Probe**: mekanizma yok; ortam
probe'u (playwright + node mevcut → headless render smoke yapılır).

## 1. Kapsam KARARI (gerekçeli)

**STATİK tek dosya `web/index.html`** — inline CSS+JS, CDN'siz, sunucu
YOK, hosting YOK (A17 güvenlik çizgisinin devamı: sunucu yüzeyi = saldırı
yüzeyi; statik dosyanın saldırı yüzeyi yok). Kullanıcı vizyonu ("son
kullanıcı terminal kullanamaz") ile uyumlu: çift-tıkla tarayıcıda açılır.

**Hesap nerede**: numpy/sympy tarayıcıda yok. Seçenek (a) DÜRÜST KAPSAM
seçildi (pyodide DEĞİL — ~10MB indirme + sympy build karmaşası; dürüst
olmayan "tam tarayıcı motoru" izlenimi verir): sayfa bir **sonuç
GÖRÜNTÜLEYİCİ** — kullanıcı MCP/CLI tool çıktısını (JSON) yapıştırır,
sayfa güvenli biçimde tablolar/matrisler olarak render eder. Gömülü
ÖRNEK JSON ile "Load example" düğmesi (indirmeden çalışır). Rapor
üretecinin LaTeX çıktısını da (varsa) monospace blokta gösterir.
Sınır dürüstçe yazılır: "hesap Python paketinde; bu sayfa sunumdur."

## 2. Güvenlik (XSS — A17 ruhu)

- Kullanıcı girdisi/JSON İÇERİĞİ yalnızca `textContent` ile basılır;
  `innerHTML` HİÇBİR yerde kullanıcı verisiyle KULLANILMAZ (sabit iskelet
  hariç). DOM `createElement`/`textContent` ile kurulur.
- `JSON.parse` try/catch; hata mesajı textContent.
- Sayısal alanlar `Number.isFinite` süzülür; beklenmeyen anahtarlar
  sessiz atlanmaz, "unrecognized field" olarak GÖSTERİLİR (K21 ruhu).
- `<meta http-equiv="Content-Security-Policy" content="default-src
  'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'">` —
  ağ yok, yalnız inline; dış kaynak çekilemez.
- Hiçbir `eval`/`Function`/`setTimeout(string)` yok.

## 3. Test (`tests/test_web_ui.py`)

- Yapısal: dosya var; CSP meta; beklenen element id'leri (json girişi,
  render hedefi, örnek düğmesi); `innerHTML` kullanıcı-veri deseni YOK
  (kaynak taraması: `innerHTML =` yalnız sabit/temizlenmiş); `eval(`/
  `Function(` yok.
- Örnek JSON şema uyumu: gömülü örnek, MCP tool çıktı şemasıyla tutarlı
  (tool'u çağırıp anahtar kümesini karşılaştır).
- **Headless render smoke** (playwright mevcut): sayfayı aç, örnek yükle,
  render hedefinde beklenen metin; **XSS payload testi**: JSON'a
  `<img src=x onerror=alert(1)>` / `"</script>"` benzeri string koy →
  DOM'da SCRIPT çalışmaz, metin olarak görünür (textContent kanıtı);
  console'da hata/alert yok. (skipif playwright yoksa yapısal yeter.)

## 4. Kabul

Statik dosya + CSP; XSS-güvenli render (headless payload testi script
çalıştırmıyor); örnek JSON tool şemasıyla uyumlu; sınır-dürüstlük metni
sayfada; 268 eski test yeşil; XSS-odaklı denetim PASS.

**DUR BURAYA**
