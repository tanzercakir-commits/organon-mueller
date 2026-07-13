# AŞAMA 12 — RAPOR (FAZ D Açılışı: Coupled-Dipole Sembolik Motor)

**Tarih**: 2026-07-13 · **Spec**: `specs/stage-12.md` · **Mod**: otonom
**Sonuç**: TAMAMLANDI — 179/179 test yeşil; **PRB 98, 045410'un ana
sonuçları sembolik olarak yeniden türetildi ve makaleyle birebir**;
denetçi her türetimi bağımsız yeniden yaptı ve **iki baskı-tutarsızlığı
teşhisimizi de matematiksel olarak DOĞRULADI** (M30 serisi büyüyor).

## 1. Teslim edilenler (`dipoles/` paketi)

- **`dimer.py`**: projektör Jones; Λ = C₁C₂δ₁+S₁S₂δ₂; **ayrışım teoremi
  (Eq. 25)**: 4×4 kuple sistemden TÜRETİLEN T == γ[α₁J₁+α₂J₂+α₁α₂ΛJ_int],
  tam sembolik (M28); kovaryans köprüsü `jones_to_hvector` — makale
  Eq. 29 == JOSA A HVector konvansiyonumuz (çift yönlü sentinel);
  dephased J'_int (**A13 γ-otomasyonunun mekanizması**: h₄ =
  −(i/2)sinΔφ(1−e^{iχ}); χ=0 veya paralel → 0; χ=π → salt sirküler);
  sayısal değerlendirici (K26: sonluluk+rezonans guard'ları).
- **`hybrid.py`**: det TEOREMİ det(A)=λ₁λ₂(λ₁λ₂−Λ²); ω± türetimi ==
  Eq. 45/46; hibrit baz — **iki genel teorem**: |t⟩=ν₊|h₊⟩+ν₋|h₋⟩ (her
  jenerik g,φ) ve g₁=g₂ ⇒ ⟨h₊|h₋⟩=0 (|h₁+h₂|²=|h_int|²=1+cos²Δφ
  kimliğinden); genel açı katsayı çözümü + Eq. 70 çapası; guard'lar
  (tekillik — det=sin³Δφ/2, denetçi türetimi; t₄≠0 span dışı; güçlü
  kuplaj ω₋² < 0; çift kök).

## 2. M30 baskı-tutarsızlıkları (denetçi teyitli)

- **Eq. 37**: makalenin kendi Eq. 29 (½'li) konvansiyonuna göre 2×
  ölçekli basılı (χ=0'da kendi Eq. 32'siyle de çelişiyor). Yön iddiaları
  sağlam. Probe Q6'nın "False" çıktısı bu keşfin kendisi — arşiv notu
  probe dosyasında.
- **Eq. 39 vs Eq. 44**: basılı Lorentzian payı ηω, makalenin Eq. 44'ü
  (ve Eq. 45'in 4ω₁²ω₂²η₁η₂Λ² terimi) ηω² gerektiriyor — Eq.-44-tutarlı
  form implement edildi, `lorentzian`↔Eq.44 bağı test çapalı.
- Eq. 33 seri-ürün h-vektörü cosΔφ/2 faktörüyle basılı (ölçeksiz rapor).
  Kiralite incelmesi: 4. bileşen (i/4)sin2Δφ — paralel VEYA dik (çapraz
  projektörler ürünü yok eder) durumlarında sıfır.

## 3. Bağımsız denetim

Verdict: **PASS** (4 MINOR + 2 DOC — hepsi giderildi): açı sonluluk
guard'ı; t₄≠0 sessiz bilgi kaybı → açık ret (K26); güçlü-kuplaj sanal
frekans + çift-kök davranışı; I=I⁺+I⁻ ve lorentzian tutarlılık testleri;
probe arşiv notu; kiralite ifade düzeltmesi. Denetçinin bağımsız
türetimleri: Green geometrisinden K=diag(δ₁,δ₂) (B-terimi û'da çift —
işaret bağımsız); Eq. 25 sıfırdan (projektör skaler indirgemesi);
det teoremi; ω±; Eq. 33 faktörü; iki M30 teşhisi; Eq. 70; tekillik
guard'ının TAMLIĞI (φ₁=φ₂ mod π tek tekil konfigürasyon).

## 4. Sıradaki aşama (otonom devam)

**Aşama 13 — γ (optik aktivite) yön-genel otomasyonu**: dephased-χ
mekanizması + Symmetry 12, 1790 (2020) geometrisi (e₁/e₂ gecikme fazları,
90° saçılım JA/JB, Eq. 1 karşılıklılık dönüşümü); hedef: keyfi
gözlem yönü için γ(χ,φ₁,φ₂) haritası ve karşılıklılık testleri (M35
köprüsüyle keşif motoruna guard'lı-atom bağlantısı adayı).
