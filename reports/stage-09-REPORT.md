# AŞAMA 9 — RAPOR (Faz C: Bileşik Simetriler + Guarded Atoms İlk Yarı)

**Tarih**: 2026-07-13 · **Spec**: `specs/stage-09.md` · **Mod**: otonom
**Sonuç**: TAMAMLANDI — 126/126 test yeşil; **bileşik tipler (1-2, 1-3, 2-3)
üç-parametreli sıralı minor çözümüyle türetildi ve Tablo 4 ile 3/3 sembolik
birebir eşleşti**; `underivable` kanalının İLK dolu çıktısı üretildi
(üç Horn-koşullu özdeşlik, M32 dörtlü kanıtla).

---

## 1. Teslim edilenler

### (a) `decomposition/composite.py` — bileşik tipler (M31: ayrı modül)
- **Şablonlar (Tablo 3)**: üç birincil {x, g, h} — 1-2/1-3'te merkez
  x=α₁B + α₁G, α₁H; 2-3'te köşe x=α₁A + α₁G\*, α₁H\*; bağımlılar rank-1
  ilişkilerinden (AB=GG\*, GH\*=MB, BC=HH\* / 2-3: AB=GG\*, HG\*=AY, AC=HH\*).
- **Sıralı minor türetimi** (M28 disiplini sürer): x-minoru g/h'siz çözülür,
  sonra g-minoru (lineer, conj(g)'siz, h'siz), sonra h-minoru; her yapısal
  ihlal fırlatır (K29). Tablo-4 çapalarıyla **tam sembolik sıfır** (K28).
- **`decompose_composite`**: K26 guard'ları — rank-2, payda~0 (eksik-tip
  anizotropi/örtüşme), birincil reel+pozitif, α₁∈(0,1), H₂ PSD + rank-1,
  **iz-1 konvansiyon guard'ı** (aşağıda).

### (b) `discovery/guards.py` — guarded atoms (tasarım notunun ilk yarısı)
- `GuardedAtom(name, guard)`: `Atom` alt sınıfı — e-graph ve aksiyomlar
  guard'ı GÖRMEZ (ses maliyeti sıfır, K24 dokunulmadı); `provable()` böylece
  "guard'sız türetilebilir mi" sorusunun kendisi olur.
- Kısıtlı üreteçler (K30: kısıt parametre inşasıyla girer, varsayım
  enjeksiyonu yok): hermitian → 4 reel; unitary → τ reel + sanal vektör;
  class2_ta/tb/tg → (τ,α,0,0)/(τ,0,β,0)/(τ,0,0,γ). Sayısal + sembolik.
- `_validated_guards` (denetim sonrası): guards sözlüğü terimlerdeki gömülü
  etiketlerle çapraz doğrulanır — yanlış etiketlenmiş sözlük sessiz Horn
  kanıtı üretemez, fırlatır.

## 2. Doğrulama sonuçları

- **Tablo 4**: 3/3 tip sembolik birebir (`sp.simplify(fark) == 0`).
- **Roundtrip**: 3 tip × 3 deterministik örnek, kesin geri kazanım
  (α₁ ~1e-8, H'ler ~1e-7; denetçi ~1e-15 gözledi).
- **Guard'lı kampanya (M32 dörtlü kanıt)**: üç bulgu — class2_ta ({1,i}),
  class2_tb ({1,j}, denetim önerisi 2 ile eklendi), class2_tg ({1,k}):
  guard'lı sembolik-KESİN ✓ · guard'lı sayısal ✓ · e-graph ispatı ✗ ·
  guard'sız sembolik ✗ → `is_conditional_identity` üçünde de doğru.
  Karışık guard (ta×tg) negatif kontrolü değişmiyor ✓. **Bunlar bilinen
  gerçekler** (kuaterniyonun {1,q} düzlemleri değişmeli) — amaç kanal
  mekanizmasının ispatıydı, novelty İDDİASI YOKTUR (protokol değişmedi).
- **Dejenere guard'lar**: aynı-simetri karışımı üç bileşik tipte de payda
  çökmesiyle reddediliyor (parametrize test, denetim önerisi 3); rank≠2
  açık hata.
- Eski 110 test + yeni 16 = **126/126 yeşil** (py3.12 lokal; CI matrisi
  push'ta koşacak).

## 3. Spec düzeltmesi — implementasyon ÖNCESİ probe kazancı

İlk taslak hedef `unitary(a) → (a·conj(a))·b ≡ b·(a·conj(a))` sayısal
probe'da YANLIŞ çıktı ve spec'e retraksiyon notuyla işlendi: elementwise
conj ≠ dagger (hh†=1 kuaterniyon-Hermitsel eşlenik ister; ZZ\* bir retarder
Mueller'idir, skaler·I değil — stage-7'nin "dagger dilde ifade edilemez"
teoremiyle tutarlı). Ders: **kampanya hedefleri spec'e yazılmadan önce
sayısal probe zorunlu** — yanlış hedef koda hiç değmeden elendi.

## 4. Bağımsız denetim

Verdict: **PASS** (2 doküman-düzeyi kusur + 3 öneri — hepsi uygulandı):
- D1: composite.py 2-3 şablonundaki karışık y-yorumu düzeltildi
  (Y\* = H\*G/A → ölçekli h·conj(g)/x zinciri açık yazıldı).
- D2: spec'teki "guard ∈ CONDITIONS anahtarları" ifadesi düzeltildi —
  GUARD_KEYS, CONDITIONS'ı class2_ta/tb/tg ile GENİŞLETİR.
- Öneri 1 → **iz-1 konvansiyon guard'ı** hem `decompose_composite`'a hem
  (miras aynı tehlike) stage-8 `decompose`'a eklendi: ölçekli kovaryans
  sessizce ölçekli α₁ döndürürdü (K26 ihlali olurdu).
- Öneri 2 → class2_tb kampanyaya eklendi (üç düzlem tam simetri).
- Öneri 3 → eksik-anizotropi testi üç tipe parametrize edildi.
- Denetçinin guard-sözlüğü endişesi → `_validated_guards` çapraz kontrolü.

Denetçi notu (belgelendi): bir bileşik-simetrik H₁, BAŞKA tipte ikinci
bileşenle karışınca çapraz-tip çözüm de fiziksel olarak geçerli alternatif
bir ayrışım verebilir — teklik iddiası yok, makale de yapmıyor; kullanıcıya
dönen sonuç `symmetry` etiketini açık taşıyor.

## 5. A10 zemini (rank-3'e köprü)

Rank-3 için kalan nesne H − α₁H₁ₛ − α₂H₂ₛ; iki simetrik bileşenin
minorları SIRALI çözülebilir (bu aşamanın üç-bilinmeyenli sıralı mekanizması
birebir genelleşir). Fingerprint→minor köprüsü: keşif motorunun bucket'ları
aday simetri sınıfını önerir, minor makinesi kesin çözer. **Aşama 10 =
rank-3 keşif taraması** — yayın-adayı bölge (Kuntman-Arteaga rank-3'ü
sistematik taramadı); novelty protokolü 5. adım (insan onayı) geçerli.

## 6. Sıradaki aşama (otonom devam)

**Aşama 10 — Rank-3 ayrışım + keşif taraması**: üç-terimli ayrışım
(2 simetrik + 1 jenerik saf), sıralı minor genelleştirmesi, sentetik
roundtrip'ler, dejenere guard'lar; keşif motoruyla ilk köprü (fingerprint
bucket'larından simetri adayı önerme).
