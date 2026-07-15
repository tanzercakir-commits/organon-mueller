# Faz D Retrospektifi (A12–A15) — stage-15

## 1. Ne kuruldu

`dipoles/` paketi dört adımda: PRB motoru (A12: Eq. 25 ayrışım TEOREMİ,
ω±, hibrit baz) → yön-genel γ (A13: Symmetry A11, Perrin genel teoremi,
JA/JB+R) → 3D dimer + ensemble (A14: δ=0⇒γ_z≡0 teoremi, ensemble
istatistikleri, depolarizasyon köprüsü) → bu kapanış (A15). Köprü zinciri
tamam: **Green fonksiyonu → kuple dipoller → Jones → HVector → kovaryans
→ ayrışım katmanı** — uçtan-uca test edildi (A14).

## 2. Karar/kural taraması

- **M35 (dipoles → algebra tek yönlü köprü)** ✅ — dipoles yalnız
  HVector'e yazar; keşif/ayrışım katmanlarına dokunmadı.
- **M36 (Symmetry-genel modül PRB modülüne dokunmaz)** ✅ — uyum
  SENTİNELLE kanıtlı (φ₁=−π/2, e₁=e₂=1 konfigürasyonunda iki modül aynı
  J; denetçi u→−u değişmezliğini de doğruladı).
- **M37 (ensemble ayrı modül; γ_paper = 2×HVector.gamma adlandırması)**
  ✅ — K33 adaş-farklı-nesne uyarılarıyla birlikte (Symmetry δ'ları ≠
  PRB δ'ları; paper-γ ≠ h-vektör γ bileşeni).
- **K33 (PDF çapaları denklem no + baskı-notuyla)** ✅ — Faz D'nin altı
  M30 kaydı (#3-#8) bu disiplinin ürünü (#1-2 Faz C/K28 fixture'ları); her çapa test docstring'inde konumlu.

## 3. M30 kümülatif tablosu (sekiz teşhis — hepsi bağımsız teyitli)

| # | Kaynak | Yer | Teşhis |
|---|---|---|---|
| 1 | AO2016 | Eq. 17 | h₀₃ sanal kısmı 0.0161 → türetilenle tutarlı 0.1608 |
| 2 | AO2016 | Eq. 21 [1,3] | benzer rakam artefaktı (−0.0037 → −0.0372) |
| 3 | PRB 98,045410 | Eq. 37 | kendi Eq. 29 ½-konvansiyonuna göre 2× ölçek |
| 4 | PRB 98,045410 | Eq. 39 | pay ηω; kendi Eq. 44-45'i ηω² gerektirir |
| 5 | ensemble preprint | Eq. 31 | parantez doğru; etiket (m×n)_z → (n×m)_z |
| 6 | ensemble preprint | Eq. 9 | önek −2iεαµ → −2iµ (εα çift sayımı) |
| 7 | ensemble preprint | Eq. 30 | "i(J₁₂−J₁₂)" dizgisi (→ J₂₁) |
| 8 | ensemble preprint | Eq. 32 | fazlarda k düşmüş |

Ders: **spec-öncesi sayısal probe** üç türetim aşamasında da (A12 Q6,
A13 Q1 faz muhasebesi, A14 Q4 öneki) konvansiyon/baskı sürprizini koda
girmeden yakaladı; A15 probe'suz (yeni mekanizma yok). #1-2 ise K28-dönemi
fixture disiplininin ürünü (Faz C). Kural yürütme zincirinin kalıcı parçası.

## 4. Borç envanteri

| Borç | Durum | Gerekçe/pencere |
|---|---|---|
| rank-3 a/b minor varyantları | ERTELENMİŞ (A11'den beri) | ölçü-sıfır dejenerasyonlar; deneysel veri gelince |
| guarded-atoms 2. yarı (unitary/hermitian kampanyaları) | AÇIK | Faz E başında kapsam değerlendirmesi — A16 spec'ine not |
| N>2 kuple dipol zinciri | ERTELENDİ | A14 2-dipolü TAM 3D geometri+ensemble ile teslim etti (FROZEN-22 başlığının ensemble yakası); N>2 lineer sistemi mekanik genelleme ama yayın-motivasyonu (hangi N-konfigürasyonlar?) Kuntman penceresi #2 feedback'ine bağlı |
| Fano derinlemesi | ERTELENDİ | PRB'nin kendisi "future work" diyor; motor hazır (ν± makinesi) |
| interpreted_scalars yan-koşulları | KOŞULLU BORÇ (değişmedi) | özellik dilde yok |

## 5. Faz E'ye devir

Paketleme vizyonu (kullanıcı, proje başı): son kullanıcı terminal
KULLANAMAZ → A16 LaTeX rapor üreteci (birinci sınıf çıktı), A17 MCP
server (sympify STAGE-2 GATE güvenlik şartı — serialize.py notu: dış
yüzey açılmadan sertleştirme ZORUNLU), A18 opsiyonel web UI, A19 docs.
Motor + ayrışım + dipol katmanları rapor-üretecinin İÇERİK kaynakları;
Kuntman paketi + eki raporun İLK gerçek kullanım senaryosu.
