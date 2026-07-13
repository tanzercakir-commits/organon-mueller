# AŞAMA 9 — Rank-2 Genel: Bileşik Simetriler + Guarded Atoms (Faz C)

**Tarih**: 2026-07-13 · **Önceki**: stage-08 (Tip 1/2/3 türetici) · **Mod**: otonom

---

## 1. Hedefler

### (a) Bileşik tipler (AO2016 Tablo 3-4): 1-2, 1-3, 2-3
1. `decomposition/composite.py`: üç-parametreli şablonlar (Tablo 3 —
   birincil {x, g, h}: 1-2/1-3'te x=α₁B merkez + G, H; 2-3'te x=α₁A köşe +
   G\*, H\*; bağımlılar rank-1 ilişkilerinden: AB=GG\*, GH\*=MB, BC=HH\* /
   2-3: AB=GG\*, HG\*=AY, AC=HH\*), sıralı minor çözümü (her minor kendi
   bilinmeyeninde lineer + conj-içermez; yapısal guard'lar stage-08 gibi),
   Tablo-4 çapa karşılaştırması (K28 tam sembolik sıfır), sayısal çözücü
   `decompose_composite` (K26 guard'ları + α₁ = iz formülü: 1-2/1-3:
   A+2B+C; 2-3: 2A+B+C ölçekli).
2. Sentetik roundtrip: tip-özel saf H'ler rank-1 |u⟩⟨u| vektöründen
   (1-2: u=(u₀,u₁,u₁,u₃); 1-3: u=(u₀,u₁,−u₁,u₃); 2-3: u=(u₀,u₁,u₂,u₀)) +
   jenerik saf; deterministik tohum; kesin geri kazanım.
3. Dejenere guard: eksik-tip anizotropi yoksa (makale şartı) açık hata.

### (b) guarded_atoms — ilk yarı (tasarım notuna göre; aksiyoma DOKUNMADAN)
4. `discovery/guards.py`: `GuardedAtom(name, guard)` düğümü (guard ∈
   GUARD_KEYS — CONDITIONS sözlüğünü class2_ta/tb/tg ile GENİŞLETEN kendi
   kelime dağarcığı; hermitian/unitary anahtarları CONDITIONS ile ortak) +
   kısıtlı üreteçler:
   - sayısal: hermitian → reel parametreler; unitary → τ reel, α,β,γ sanal;
     class2_ta/tb/tg → (τ,α,0,0)/(τ,0,β,0)/(τ,0,0,γ).
   - sembolik: aynı kısıtlarla jenerik semboller (K17 bağımsızlık sürer).
5. **Üreteç sadakati testi** (stage-08 yükümlülük 1): sembolik üreteç
   sınıfın jenerik temsilcisi (serbest sembol sayısı/deseni + sayısal
   üretecin CONDITIONS yüklemlerini sağlaması).
6. **Guard'lı kampanya** (`run_guarded_campaign`): ilk Horn-koşullu özdeşlik
   adayları. **DÜZELTME (implementasyon öncesi sayısal probe)**: ilk
   taslaktaki `unitary(a) → (a·conj(a))·b ≡ b·(a·conj(a))` hedefi YANLIŞTI —
   elementwise conj ≠ dagger karıştırması (hh†=1 kuaterniyon-Hermitsel
   eşlenik gerektirir; ZZ\* retarder Mueller'idir, skaler değil). Probe ile
   elendi; ders kayıtlı. Doğrulanmış hedefler:
   - G1: `class2_ta(a) ∧ class2_ta(b) → a·b ≡ b·a` ({1,i} kuaterniyon
     düzlemi değişmeli — probe ✓)
   - G2: `class2_tg(a) ∧ class2_tg(b) → a·b ≡ b·a` ({1,k} düzlemi — probe ✓)
   - G3 (denetim sonrası eklendi, öneri 2): `class2_tb(a) ∧ class2_tb(b) →
     a·b ≡ b·a` ({1,j} düzlemi) — üç düzlemin tam simetrisi için
   - N1 (negatif): `class2_ta(a) ∧ class2_tg(b)` karışımı DEĞİŞMEZ (probe ✓)
   Ölçüt: guard altında sembolik-KESİN + guard'lı sayısal ✓; e-graph
   İSPATSIZ; guard'sız sembolik YANLIŞ (M32) → `underivable` kanalının İLK
   dolu çıktısı, guard etiketiyle; novelty-protocol'e işaretlenir, İDDİA yok
   (bunlar bilinen gerçekler — amaç kanal mekanizmasının kanıtı; rapora
   böyle yazılır). unitary/hermitian guard'lar bu aşamada üreteç+sadakat
   testiyle sınırlı (özdeşlik iddiası yok — dürüst kapsam).

## 2. Mimari kararlar

- **M31. Bileşik çözücü ayrı modülde**; stage-08 fundamental yolu değişmez.
- **M32. Guard'lı hüküm formatı**: (guard-konjonksiyonu, çift, katman
  sonuçları) üçlüsü; guard'sız-yanlış kontrolü ZORUNLU (aksi halde koşulsuz
  özdeşliktir, guard etiketi yanıltıcı olur).

## 3. Katı kurallar

K29. Bileşik minor seçimleri de yapısal guard'lı (x-minoru g/h'ye dokunamaz
vb.); ihlal fırlatır. K30. Guard'lı sembolik değerlendirme kısıt-parametreli
jenerik sembollerle (varsayım enjeksiyonu değil — substitüsyonla).

## 4-6. Teslim + Doğrulama

composite.py + guards.py + iki test dosyası + rapor (A10 zemini: rank-3'te
kalan = H − α₁H₁ₛ − α₂H₂ₛ rank-1 koşulları — minör mekanizması hazır).
Kabul: Tablo-4 3/3 sembolik birebir; roundtrip 3 tip kesin; G1-G2 dört
kontrol (guard'lı sembolik ✓, guard'lı sayısal ✓, ispat ✗, guard'sız
sembolik ✗); 110 eski test yeşil.

**DUR BURAYA**
