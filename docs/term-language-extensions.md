# Terim Dili Genişletme Gereksinimleri (Aşama 5 çıktısı; Aşama 7'de güncellendi)

Durum (Aşama 7 sonrası): kütüphanenin 21 özdeşliğinden **3'ü tam kazanıldı**
(I1, I10, **I15** — Sum/Scale genişletmesiyle), **2'si yapısal** (I7, I8 —
dilin semantiğinde gömülü), **16'sı** dil dışında. ~~`addition` ve opak
`scalars`~~ **TESLİM EDİLDİ** (Aşama 7): terim toplamı + evrensel-nicelenmiş
katsayılar (M26) dilde; parmak izi ölçek-göreli anahtara geçti.

Satır semantiği: her satır, o özelliği `missing` listesinde **anan**
RECOVERY_TABLE kayıtlarının birleşimidir.

| Öncelik | Özellik | Kilitlediği özdeşlikler | Not |
|---|---|---|---|
| 1 | `interpreted_scalars` (yorumlanan/sabit skaler aritmetiği) | I4, I11, I16, I17, I18 | e^{iφ}, (1+i)/2, 1/det, trig, reel ağırlıklar — SABİT katsayı değerleri. M26 ince ayrımı (stage-7 denetçi bulgusu): tam-sayı-katsayılı özdeşlikler (Amitsur-Levitzki türü) işaretsiz bölmeyle ZATEN ifade edilebilir; bu anahtar değer-düzeyi aritmetik için. |
| 2 | `guarded_atoms` (koşullu atom sınıfları) | I4, I12, I13, I19, I20, I21 | Horn-koşul altyapısına (CONDITIONS) doğal bağlanır: "hermitsel atom", "üniter atom", "(τ,α,0,0) atomu". Faz C ayrışım türetici bunu isteyecek. |
| 3 | `dagger` + `stokes_sort` | I9, I13, I14 | Z^† ayrı unary op; Stokes ayrı sort. S′=ZSZ† ailesi ve H=\|h⟩⟨h\| için. (Denetçi ispatı: dagger mevcut dilde İFADE EDİLEMEZ — derece argümanı.) |
| 4 | `entry_level` (girdi/iz/det ifadeleri) | I3, I5, I6, I12, I13, I14, I17, I19, I20, I21 | Muhtemelen e-graph'a HİÇ girmez; SymPy-tarafı doğrulama/rapor katmanında kalır (keşif = terim düzeyi, betimleme = girdi düzeyi). |
| 5 | `constants` (A, R(θ), özel durumlar) | I2, I11, I18 | Ancak guarded_atoms + interpreted_scalars sonrası anlamlı. |

Önerilen sıra: **2** (Faz C girişiyle birlikte — ayrışım türetici koşullu
sınıflar istiyor), sonra ihtiyaca göre 1/3-5. M22 gereği her genişleme
sonrası kampanya yeniden koşulur ve kazanım sayısı yalnız artabilir.

Bilinen erişilebilirlik notu: AL-türü toplam-özdeşlikleri (S₄=0'ın işaretsiz
bölünmüş formu ~boyut 95, 4 atom) ifade edilebilir ama mevcut enumerasyon
sınırlarının (max_sums=1, boyut ≤~11) çok ötesinde — hedefli (enumerasyonsuz)
doğrulama her zaman mümkün: üç katman doğrudan çift üzerinde çalışır.
