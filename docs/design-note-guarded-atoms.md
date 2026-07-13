# Tasarım Notu — Koşullu Atom Sınıfları (guarded_atoms; implementasyon A9+)

Kaynak gereksinim: `docs/term-language-extensions.md` öncelik 2 — I4, I12,
I13, I19-I21 ailesi ve Faz C ayrışım türeticisinin keşif tarafı bağlantısı.

## İlke: guard'lar AKSIYOM değil, YORUMLAMA katmanına girer

Stage-2/3/7 ses derslerinin doğrudan sonucu: her yeni e-graph kuralı bir
unsound-birleşme riskidir ve K24 süreci ister. Guard'lı atomlar için buna
GEREK YOK — kısıt, atomun ÜRETECİNE konur:

```
GuardedAtom(name, guard)   guard ∈ CONDITIONS anahtarları
                           (hermitian_state, unitary_state, class2_ta, ...)
yorumlama (sayısal):  kısıtlı rastgele HVector (örn. hermitsel: reel parametreler)
yorumlama (sembolik): kısıtlı jenerik parametreler (örn. tau reel, alpha reel, ...)
e-graph:              atom gibi — HİÇBİR ek kural yok
```

## Keşif semantiği (asıl kazanç)

Guard'lı atomlarla bir çift üç katmandan geçtiğinde anlamı:
"guard koşulu ALTINDA özdeşlik" — yani Horn-koşullu özdeşlik:
`hermitian(a) → t₁(a) = t₂(a)`.

- e-graph guard'ları bilmediğinden bu çiftler tipik olarak İSPATSIZ kalır →
  `underivable` kanalına **guard etiketiyle** düşerler = tam da aradığımız
  koşullu-özdeşlik ADAYLARI. (Kanal bugüne dek boş — ilk adaylar buradan
  bekleniyor; novelty-protocol zinciri değişmeden uygulanır.)
- Sembolik katman guard'ı kısıtlı parametrelerle otomatik uygular (kesin
  ispat "koşul altında" olur); sayısal katman kısıtlı örneklemle.
- İsteğe bağlı ileri adım (ayrı K24 turu): sık doğrulanan guard'lı denklik
  ailelerini guard-özgü GROUND kurallara derlemek (örn. hermitsel a için
  a·conj(a) ilişkileri) — ancak denetçi ses onayıyla.

## Ayrışım köprüsü (Faz C)

AO2016 Tip 1/2/3 saf durumları = guard'lı atom sınıflarının kovaryans
yüzü. A9+ hedefi: `class2_*` guard'lı atomlarla keşif taraması, ayrışım
türeticinin simetri şablonlarını keşif tarafından da görünür kılar
(örn. tip-1 atomlu çiftlerde M-simetri desenleri underivable adayı olarak
kendiliğinden çıkmalı — I19-I21'in keşif-yüzü).

## Parmak izi ve tohumlar

Guard'lı üreteçler ayrı tohum uzayı kullanır (K14 genişler); kova anahtarı
değişmez (ölçek-göreli). Guard başına örneklem yeterliliği (dejenere
alt-uzaylarda yanlış-pozitif riski: örn. tau=0 sınıfında bazı ifadeler özdeş
görünebilir) → sembolik-kesin katman zorunlu kalır (M19 aynen).

## İleriye dönük yükümlülükler (stage-8 denetçi eki)

1. **Üreteç sadakati**: her guard'ın sembolik parametrizasyonu kendi sınıfı
   için JENERİK ve sadık olmalı — aksi halde "guard → özdeşlik" hükmünün
   kapsamı fazla-iddia olur. (Bugünkü bölmesiz dilde jenerik-doğru ⇒
   tüm-sınıf-doğru: polinom özdeşlik teoremi; τ=0 gibi ölçü-sıfır katmanlar
   dahil.)
2. **Payda yükümlülüğü**: `interpreted_scalars` (1/det tarzı değerler)
   geldiğinde sympy sadeleştirmesinin sessiz ≠0 varsayımları, sertifikalı
   Horn-özdeşliklere EK guard bileşeni olarak yazılmalı (CONDITIONS'taki
   `det_nonzero` anahtarı tam bunun için).

## Kabul taslağı (A9 spec'ine girdi)

1. GuardedAtom düğümü + kısıtlı üreteçler (hermitsel, üniter, class2_ta/tb/tg).
2. Kampanya: I12/I13'ün guard'lı-çift karşılıkları üç katmandan geçer
   (e-graph ispatı yerine "guard altında sembolik-kesin" ölçütüyle —
   sınıflandırma şeması bu ayrımı raporlar).
3. Tarama: 2 guard'lı atom konfigürasyonunda underivable kanalının İLK
   dolu çıktısı beklenir; novelty-protocol'e akar, İDDİA üretilmez.
