# Ek — coupled-dipole motoru (geri bildirim paketi #1, bölüm 2)

*Ana README ile aynı etiketleme: **doğrulanmış** = yayınlarınızdaki
denklem/tablolara karşı makine kontrollü; **aday** = onların ötesi,
iddiasız. Yorum sizindir (novelty protokolü, son adım insanda).*

## PRB 98, 045410 (2018)'e karşı doğrulananlar

- **Üç-terimli ayrışım (Eq. 25) teorem olarak**: kuple 4×4 dipol sistemi
  sembolik çözülüyor ve T = γ[α₁J₁ + α₂J₂ + α₁α₂ΛJ_int] eşitliği KESİN
  ispatlanıyor — ayrışım *varsayılmıyor, türetiliyor*. Kapalı formlar
  (14)-(17), Eq. (42)'nin arkasındaki det(A) = λ₁λ₂(λ₁λ₂−Λ²) yapısı,
  hibrit frekanslar (45)-(46), hibrit-baz özdeşliği |t⟩ = ν₊|h₊⟩+ν₋|h₋⟩
  ve g₁=g₂ ortogonalliği (baz tanımı 61-64; ortogonallik ifadesi 73-74
  civarı) sembolik olarak (kalıcı testlerle) yeniden üretildi;
  (90°,135°) için Eq. (70) tersine çözümü birebir.
- **Kovaryans-vektör konvansiyonunuz (Eq. 29) bizim JOSA A 34, 80
  konvansiyonumuzla birebir aynı** — iki yönlü sentinel testli; dimer
  fiziği kovaryans/Mueller makinesine doğrudan akıyor.
- Faz-farklı dedektör mekanizması (35-37): yalnız etkileşim terimi
  dördüncü (sirküler) bileşen kazanıyor; χ=0 veya paralel dipollerde
  sıfır, χ=π'de salt sirküler.

## Symmetry 12, 1790 (2020)'ye karşı doğrulananlar

- Genel-geometri Jones (Eq. A11) kuple sistemden yeniden türetildi
  (uzak-alan muhasebesi çözüldü: A11, T = e₂p₁+p₂'ye karşılık geliyor —
  global bir e₂ soğurulmuş); özel durum (A12/Eq. 3-4) kesin. 90°
  matrisleri J_A = g[[0,0],[µ,1]], J_B = g[[0,−µ],[0,1]] ışıma
  projeksiyonundan türetildi ve J_B = R(J_A) sağlanıyor.
- **Perrin karşılıklılığı genel sembolik teorem olarak**: R(J) = σJᵀσ
  (Eq. 1'iniz) ile amp_B = (σu*)†R(J)(σv*) = v†Ju — HER Jones matrisi
  için; (8)-(13) kurgunuz özel durum olarak çıkıyor (I_B =
  (|x|²+|y|²)·I_A, Eq. 13'ünüz).

## OA-in-ensemble preprint'ine karşı doğrulananlar

- 3D rank-1 skaler indirgeme (Eqs. 16-24), tam 3D dyadic 6×6 çözüme
  karşı ~3e-16 hassasiyetle doğrulandı (düzlemsel xy-blok analoğu ayrıca
  denetimde sembolik olarak kesin ispatlandı); ileri Jones
  (26)-(29); γ_z (31); γ_x ve ayrımı (33)-(35), γ_x1'in kuplajsız
  limitte hayatta kalması (metasurface gözlemi) dahil.
- **δ = 0 ⇒ γ_z ≡ 0 (her oryantasyonda), sembolik teorem olarak**
  (ileri-saçılım merkez ifadeniz); ensemble istatistikleri
  (kiral+kuplajlı Σγ_z ≠ 0; akiral Σγ_z = 0 ama Σ|γ_z| ≠ 0; kuplajsız
  noktasal sıfır) deterministik örneklemeyle yeniden üretildi.
- Köprü (aday bölge): sonlu oryantasyon karışımlarının ⟨|h⟩⟨h|⟩
  kovaryansları, simetri-koşullu ayrışım çözücülerimize uçtan-uca akıyor.

## Muhtemel baskı artefaktları — teyidinizi rica ederiz

*(Hiçbiri fiziksel bir sonucu etkilemiyor; her biri makalelerin KENDİ iç
denklemleriyle çapraz kontrolle bulundu ve bağımsız bir denetçi
tarafından ayrıca türetilerek doğrulandı.)*

| # | Makale | Yer | Not |
|---|---|---|---|
| 1 | PRB 98, 045410 | Eq. (37), s. 045410-4 | makalenin kendi Eq. (29) ½-konvansiyonuna göre 2× ölçekli basılı (χ=0'da Eq. (32)'ye inmeli) |
| 2 | PRB 98, 045410 | Eq. (39), s. 045410-5 | pay ηᵢωᵢ basılı; kendi (44)-(45) denklemleriniz ηᵢωᵢ² gerektiriyor |
| 3 | ensemble preprint | Eq. (31), Ek | parantez (n_xm_y − m_xn_y) doğru ve (n×m)_z'ye eşit; etiket "(m×n)_z" basılı |
| 4 | ensemble preprint | Eq. (9), ana metin | önek −2iεαµ basılı; µ = εα/(1−(αδ)²) zaten εα içerdiğinden türetilen önek −2iµ |
| 5 | ensemble preprint | Eq. (30), Ek | "i(J₁₂ − J₁₂)" basılı — ikinci indis J₂₁ olmalı |
| 6 | ensemble preprint | Eq. (32), Ek | yol fazları e^{ir_x/2} basılı; k düşmüş |

(Appl. Opt. 55, 2543'teki iki teşhis — Eq. 17 h₀₃ ve Eq. 21 [1,3] —
ana README'de.)

## Deneyin

```bash
python docs/kuntman-package/demo.py   # bölüm 4 = dipol motoru
```
