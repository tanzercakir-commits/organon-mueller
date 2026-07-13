# AŞAMA 10 — Rank-3 Ayrışım + Keşif Köprüsü (Faz C, yayın-aday bölge)

**Tarih**: 2026-07-13 · **Önceki**: stage-09 (bileşik tipler + guarded atoms) ·
**Mod**: otonom

---

## 0. İmplementasyon-öncesi probe (stage-9 dersi — ZORUNLU, yapıldı)

`H = α_A·H_A + α_B·H_B + α_G·|u⟩⟨u|` (iki fundamental-simetrik saf + jenerik
saf; rank 3, iz 1). Probe sonuçları (`probes/probe-rank3-prespec.py`,
tohum 20260713):

- **{tip1, tip2}**: sıralı peel KESİN (5/5 deneme, ~1e-12) — B'nin merkez
  parametresi merkez minöründen LİNEER, kenarı satır-0 kenar minöründen
  LİNEER (ikisi de tip-1'in köşe desteğine değmez); B çıkarılır, kalan
  yeniden ölçeklenip stage-8 rank-2 çözücüsüne DELEGE edilir.
- **{tip1, tip3}**: aynı — işaret-ayarlı minörlerle KESİN (5/5). (Probe'un
  ilk sürümünde kenar formülünde işaret hatası vardı; probe yakaladı,
  düzeltildi — probe mekanizması yine işledi.)
- **{tip2, tip3}**: destekler TAM örtüşüyor; 12/12 çok-başlangıçlı LSQ
  aynı sıfır-artık çözüme (= gerçeğe) yakınsadı → TANIMLANABİLİR.
  Kesin yol: KOMBİNASYON DEĞİŞKENLERİ (σ=k₂+e₃, p=w₂+v₃, m=w₂−v₃,
  s=k̄₂+ē₃, d=k̄₂−ē₃) ile T₂+T₃ toplamı 7-parametreli Hermitsel desen;
  köşe minörü σ'da LİNEER (kareler sadeleşir), p/m/s/d sırayla LİNEER →
  geri-inşa (w₂,v₃,k̄₂,ē₃ → k₂=|w₂|²/k̄₂, e₃=|v₃|²/ē₃) + **tutarlılık
  guard'ı k₂+e₃ = σ** (fazladan belirlenim = K26 fırsatı).

## 1. Hedefler

1. `decomposition/rank3.py`:
   - `derive_rank3(pair)` (M28 sürer): jenerik Hermitsel üzerinde kalanın
     minörleri SymPy ile SIRALI çözülür; yapısal guard'lar (K29 genişler):
     her minör kendi bilinmeyeninde lineer + conj-içermez + HENÜZ
     ÇÖZÜLMEMİŞ diğer bileşen sembollerine değmez; ihlal fırlatır.
     Çiftler: (1,2), (1,3) → (merkez, kenar) + delegasyon; (2,3) →
     (σ,p,m,s,d) + geri-inşa.
   - `decompose_rank3(covariance, pair, ...)`: K26 guard seti — iz-1,
     rank==3, payda~0 (eksik-anizotropi: örn. köşe paydası α_G|u₀−u₃|² —
     jenerik saf eksik anizotropiyi TAŞIMALI, makale temasının rank-3
     genellemesi), birincil reel+pozitif, α'lar ∈(0,1), {2,3} tutarlılık
     guard'ı, kalan saf PSD + rank-1. Delegasyon: {1,B} kalanı yeniden
     ölçekle → stage-8 `decompose` (onun tüm guard'ları miras).
2. `propose_decompositions(cov)` (fingerprint→minor köprüsü v0): rank'e
   göre aday sınıfları DENER (rank 2: fundamental+bileşik; rank 3: üç
   çift), başarıları sonuç+etiketle, başarısızlıkları GEREKÇELİ döndürür
   (sessiz eleme yok — K21 ruhu).
3. Tarama (keşif): deterministik sentetik süpürme (3 çift × tohumlar +
   negatif kontroller) → `reports/sweep-03-rank3.json` (K21 artefakt).

## 2. Mimari kararlar

- **M33**: Rank-3 çözücü stage-8/9 yollarına DOKUNMAZ; delegasyon tek yönlü
  (rank3 → rank2). Varyantlar (a/b minor seçenekleri) bu aşamada YOK —
  kanonik set + net guard mesajları; a/b genişlemesi A11'e not edildi.
- **M34 (K28 uyarlaması — dürüstlük)**: Bu bölge makale-ötesi: Tablo-benzeri
  DIŞ ÇAPA YOK. K28'in "makaleyle birebir" çapası yerine üç katman:
  (i) probe-doğrulanmış el türetimi spec'te sabitlendi (yukarıda),
  (ii) türeticinin çıktısı bu el formülleriyle sembolik karşılaştırılır,
  (iii) bağımsız denetçi kendi türetimini yapar. Fizik-yorumu/yenilik
  İDDİASI YOK — novelty-protocol adım 5 İNSANDA; rapor "aday" der.

## 3. Katı kurallar

K31. Rank-3 minör seçimleri çözüm SIRASINA duyarlı yapısal guard taşır
(çözülmemiş sembole değen minör fırlatır). K32. {2,3} tutarlılık artığı
|k₂+e₃−σ| çözücüde ZORUNLU kontrol — geçemeyen veri reddedilir (sessiz
yamalama yok).

## 4. Kabul

- Türetici 3 çiftte yapısal guard'lardan geçer; el-formülleriyle sembolik
  birebir (M34-ii).
- Roundtrip: 3 çift × 3 deterministik örnek, kesin geri kazanım (test
  toleransları α 1e-8, bileşenler 1e-6; gözlenen hatalar ~1e-15).
- Dejenere guard'lar: aynı-tip çift; kasıtlı u₀=u₃ / u₁=u₂ dejenerasyonları;
  rank≠3; iz≠1; {2,3} tutarlılık ihlali — hepsi GEREKÇELİ hata.
- Çapraz-çift dürüstlüğü: yanlış çift ya guard'da düşer ya delegasyon
  guard'ında — sessiz makul-ama-yanlış YOK.
- `propose_decompositions`: rank-2 sentetikte doğru fundamentali, rank-3
  sentetikte doğru çifti bulur; eleme gerekçeli.
- sweep-03 JSON deterministik; 126 eski test yeşil.

**DUR BURAYA**
