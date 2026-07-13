# AŞAMA 7 — Dil Genişletmesi: Sum + Scale — ve Faz B İterasyon Değerlendirmesi

**Tarih**: 2026-07-13 · **Önceki**: stage-06 (tarama #1, tamlık teoremi)
**Mod**: otonom · **Girdi**: `docs/design-note-addition-scalars.md` (denetçi ses-onaylı)

---

## 1. Bağlam

Mul/Conj fragmanı ispatlanabilir biçimde TAM (stage-06). Yeni matematik
ihtimali ancak dil genişleyince doğar. Bu aşama tasarım notunu uygular ve
FROZEN-22'nin A7'si (iterasyon değerlendirmesi) ile birleşik yürür
(stage-06 raporu §5'te ilan edildi).

## 2. Hedefler

1. **Terim dili**: `Sum(t,t)`, `Scale(c,t)`, `ScalarAtom(name)`,
   `ScalarConj(c)` düğümleri; boyutlar (Sum/Scale +1; ScalarAtom 1;
   ScalarConj +1); genişletilmiş conj-normal (Conj yalnız Atom'da,
   ScalarConj yalnız ScalarAtom'da).
2. **Aksiyomlar** (yalnız tasarım notundaki ses-onaylı tablo): Sum
   komütatif+asosiyatif; Mul'un Sum üzerine iki yanlı dağılımı (çift yön);
   Conj-Sum dağılımı; Conj-Scale eşlenik kuralı; Scale merkezîliği (iki yan);
   iç içe Scale takası (skaler çarpım OLUŞTURMADAN — opaklık M10);
   skaler-conj involüsyonu. Serbest-değişkenli YENİ komütasyon YOK.
3. **Katmanlar**: interpret (skaler→rastgele karmaşık), symbolic
   (skaler→bağımsız jenerik sembol, K17 genişler), fingerprint
   **ölçek-göreli** (Frobenius normuna bölünmüş girdiler; ‖M‖≈0 → "ZERO"
   özel anahtarı; oransal-farklı terimlerin çakışması BEKLENİR ve aşağı
   katmanlar eler — M15 değişmez).
4. **Enumerasyon** `enumerate_extended(atoms, scalars, max_size,
   max_sums=1, max_scale_depth=1)` — patlama sınırları spec'li; K12
   determinizm korunur. Eski `enumerate_terms` DEĞİŞMEZ (K11).
5. **Kabul (tasarım notu §Kabul)**:
   - A: I15 açılımı — (aZ_a+bZ_b)·conj(aZ_a+bZ_b) dört-terimli iç-içe-Scale
     formuna İSPATLA eşit (provable) + sembolik-kesin + sayısal.
   - B: I15 çapraz-terim gerçelliği — yapısal formda t ≡ conj(t) İSPATLI.
   - C: Geri-kazanım kampanyası: I15 → translatable; sonuç kümesi
     {I1, I10, I15} (M22 monotonluk); I16/I18 "interpreted_scalars" yeni
     eksik-özellik anahtarına taşınır (opak skaler evrensel-nicelenmiş
     özdeşlikler için DOĞRU; sabit-katsayılılar için yetersiz — dürüst ayrım).
   - D: K11 (eski dil/API) korunur — eski enumerasyon sayıları sabit
     (sentinel testli); recovery tablo testleri M22 gereği YÜKSELTİLİR
     (kazanım seti büyür), bu K11 ihlali değildir.
   - E: Mini-harvest (2 atom + 2 skaler, sınırlı boyut) uçtan uca koşar;
     refuted=0; underivable çıkarsa novelty-protocol zinciri (İDDİA YOK).
6. **Faz B iter retrospektifi** (rapor bölümü): A3-A7 dersleri, metrikler,
   Faz C'ye devreden riskler.

## 3. Mimari kararlar

- **M26. Opak skaler semantiği = evrensel nicelenme** (denetçi düzeltmesiyle):
  dildeki skalerli bir özdeşlik "TÜM karmaşık katsayılar için" okunur (I15 tam
  bu). Sabit KATSAYI DEĞERLERİ (e^{iφ}, (1+i)/2) `interpreted_scalars` ister.
  Amitsur-Levitzki için İNCE AYRIM (stage-7 denetçi bulgusu D1): ±1'li FORM
  yorumlanan skaler ister, ama özdeşliğin KENDİSİ işaretsiz ifade edilebilir —
  S₄=0 ⟺ (çift permütasyon toplamı) = (tek permütasyon toplamı), yalnız
  Sum+Mul ile, 4 atom, boyut ~95. Yani AL-türü eksik-tamlık bu dilde
  PRENSİPTE ifade edilebilir; mevcut enumerasyon sınırlarının (max_sums=1,
  boyut ≤~11) ERİŞEMEYECEĞİ kadar büyük. Stage-06 beklentisi ifade-gücü
  anlamında doğruydu; erişilebilirlik ayrı konu.
- **M27. Tek kural seti**: Sum/Scale kuralları structural_rules'a eklenir;
  eski terimler yeni kurallardan etkilenmez (tip bazlı eşleşme), motor tek
  provable yolu korur (M18 yalıtım aynen).

## 4. Katı kurallar

K23. Skaler aritmetik düğümü (c+d, c·d) e-graph'a GİRMEZ (M10).
K24. Yeni kural eklemek = ses analizi + denetçi onayı (bu spec'teki tablo dışına çıkma).
K25. Kampanya/harvest yeniden-üretim girdileri artefakt/rapora gömülür (K21 devam).

## 5-6. Teslim + Doğrulama

terms/axioms/interpret/symbolic/fingerprint/engine/recovery güncellemeleri ·
`tests/test_extended_language.py` · recovery testleri güncel · mini-harvest
sonucu raporda · Faz B retrospektif bölümü · rapor. Suite: 84 eski + yeniler yeşil.

## 7-9.

Push + rapor + Aşama 8 (5 dk; Faz C: ayrışım türetici başlangıcı). Uyarılar:
ölçek-göreli anahtarda -0.0 normalizasyonu KORUNUR; Scale'li çiftlerde
sembolik sertifikasyon maliyeti ölçülür. Kapsam dışı: interpreted_scalars,
Sum>1/derin Scale enumerasyonu, tarama #2 tam kampanyası, AL-türü arayış.

**DUR BURAYA**
