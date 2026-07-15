# AŞAMA 17 — MCP Server + sympify GATE Sertleştirmesi (Faz E 2/4)

**Tarih**: 2026-07-14 · **Mod**: otonom · **Probe**: mekanizma yok; ortam
probe'u yapıldı (mcp SDK 1.28.1 pip'te; pdflatex mevcut).

## 1. GÜVENLİK ÖNCE — kısıtlı srepr parser (`safe_parse.py`)

**Neden sympify(evaluate=False)+whitelist YETMEZ** (denetçi kanıtlayacak):
sympify her koşulda Python `eval` yoluna girer; `global_dict` kısıtlansa
bile string içinden nitelik-erişim zincirleri ve `__import__` türevleri
tarihsel olarak kaçış verdi; güvenlik sınırı "eval'e hiç girmemek" olmalı.

**Çözüm**: Python `ast.parse` ile srepr metni AST'ye çevrilir, AST
BEYAZ-LİSTE yürüyüşüyle DOĞRUDAN sympy nesnelerine kurulur (eval/sympify
YOK):
- Düğümler: Expression, Call, Name, Constant(str|int|float|bool), USub.
- Çağrı adları: Symbol, Integer, Float, Rational, Add, Mul, Pow,
  conjugate. Çıplak adlar: I. Başka HİÇBİR ad yok (Function, exp, ...
  → ret).
- Symbol adı regex: `^[A-Za-z][A-Za-z0-9_]{0,63}$`; kwargs yalnız
  bool-değerli izinli varsayımlar {real, positive, negative, complex,
  imaginary, integer} + Float için `precision`(int).
- DoS guard'ları: metin ≤ 65536 karakter; AST düğüm sayısı ≤ 2000;
  derinlik ≤ 64; sayısal literal ≤ 4096 hane.
- `UnsafeExpressionError(reason)` — sessiz ret yok (K26).
- `hvector_from_dict` bu parser'a GEÇER (GATE kapanır; docstring
  güncellenir); roundtrip: kütüphanedeki 21 özdeşliğin tamamı +
  rastgele HVector'ler srepr→parse→eşit (testler).
- `tests/test_security.py`: enjeksiyon korpusu (__import__, os.system,
  exec/eval, nitelik zinciri `().__class__...`, lambda, getattr, bilinmeyen
  fonksiyon, kwarg kaçakçılığı, 10k-derin ifade, 10^6-haneli sayı) —
  hepsi UnsafeExpressionError; hiçbir payload değerlendirilmez (canary:
  os.environ/dosya sistemi yan etkisi yok).

## 2. MCP server (KOD + TEST; HOST ETME YOK — kritik karar kullanıcıda)

- `mcp_server/tools.py` — SAF fonksiyonlar (SDK'sız test edilir):
  `tool_decompose_mueller(payload)` (4×4 REEL float matris; şema+sonluluk
  +boyut — K26; symmetry param: fundamental/composite/"propose"),
  `tool_propose_hypotheses(payload)` (kovaryans [re,im] çiftleri kabul),
  `tool_guarded_campaign_info()` (mevcut kampanya bulguları M32
  tablosuyla), `tool_generate_report(payload)` (bir önceki tool
  çıktılarından LaTeX string; sympify'sız — yalnız kendi nesnelerimiz).
  Hata cevapları: {"error": gerekçe} (istisna sızdırmaz, iz sürülebilir).
- `mcp_server/server.py` — FastMCP sarmalayıcı (`mcp` opsiyonel extra;
  pyproject `[project.optional-dependencies] mcp`); test importorskip.
  Çalıştırma: `python -m organon_mueller.mcp_server` (stdio) — README'de;
  hosting/expose kararı KULLANICIDA.
- Girdiler ASLA sympify'a gitmez (sayı listeleri + enum stringler);
  serbest-metin girdisi yok.

## 3. Kabul

test_security.py enjeksiyon korpusu (≥10 payload) tamamı ret + roundtrip
21/21; hvector_from_dict artık safe parser'da (eski davranış testleri
yeşil kalır); tool şema/K26 guard testleri (kötü boyut, NaN, string
kaçakçılığı); FastMCP kayıt smoke (skipif mcp yok); README-mcp; 215 eski
test yeşil; güvenlik-odaklı denetim PASS.

**DUR BURAYA**
