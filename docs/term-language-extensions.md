# Terim Dili Genişletme Gereksinimleri (Aşama 5 çıktısı)

Geri-kazanım kampanyası (bkz. `discovery/recovery.py`, `reports/stage-05-REPORT.md`)
kütüphanenin 21 özdeşliğinden **2'sinin tam** (I1, I10), **2'sinin yapısal**
(I7, I8 — dilin semantiğinde gömülü) kazanıldığını, **17'sinin** ise dilin
dışında kaldığını gösterdi. Eksik özellikler, sıklık ve fizik değerine göre:

Satır semantiği: her satır, o özelliği `missing` listesinde **anan** kayıtların
birleşimidir (RECOVERY_TABLE ile birebir; testle bağlı).

| Öncelik | Özellik | Kilitlediği özdeşlikler | Not |
|---|---|---|---|
| 1 | `addition` (terim toplamı) | I15, I16, I17, I18 | Koherent süperpozisyon fiziğinin tamamı. Hibrit sınır (M10) gereği skaler aritmetik SymPy'da kalır; e-graph tarafında biçimsel + düğümü. |
| 1b | `scalars` (karmaşık katsayılar) | I4, I11, I15, I16, I17, I18 | Addition ile birlikte gelir; ayrıca I4 (1/det ölçeği) ve I11 (trig) tek başına skaler ister. Parmak izi anahtarı ölçek-göreliye geçmeli (stage-03 uyarısı). |
| 2 | `guarded_atoms` (koşullu atom sınıfları) | I4, I12, I13, I19, I20, I21 | Horn-koşul altyapısına (CONDITIONS) doğal bağlanır: "hermitsel atom", "üniter atom", "(τ,α,0,0) atomu". Keşif uzayını simetri sınıflarına açar. |
| 3 | `dagger` + `stokes_sort` | I9, I13, I14 | Z^† ayrı unary op; Stokes ayrı sort. S′=ZSZ† ailesi ve H=\|h⟩⟨h\| için. (Denetçi ispatı: dagger mevcut dilde İFADE EDİLEMEZ — derece argümanı.) |
| 4 | `entry_level` (girdi/iz/det ifadeleri) | I3, I5, I6, I12, I13, I14, I17, I19, I20, I21 | Muhtemelen e-graph'a HİÇ girmez; SymPy-tarafı doğrulama/rapor katmanında kalır (keşif = terim düzeyi, betimleme = girdi düzeyi). |
| 5 | `constants` (A, R(θ), özel durumlar) | I2, I11, I18 | Ancak guarded_atoms + scalars sonrası anlamlı. |

Önerilen sıra (Faz B kalanı + Faz C girişi): önce **1** (Aşama 6'da tarama
yeni-aday hedefi de süperpozisyon cebiri olabilir), sonra **2** (Faz C
ayrışım türetici zaten koşullu sınıflar istiyor), **3-5** ihtiyaç düştükçe.
M22 gereği her genişleme sonrası kampanya yeniden koşulur ve kazanım sayısı
yalnız artabilir.
