# Doğrulama Sözleşmesi / Verification Contract

Bu proje otonom modda yürütülüyor (2026-07-13 mandası). Kullanıcının güven
çıpası bu dokümandaki katmanlardır: **hiçbir matematiksel iddia bu
katmanlardan geçmeden repoya giremez.** Herhangi bir katmanı zayıflatan
değişiklik "kritik karar"dır ve kullanıcı onayı gerektirir.

## Katmanlar

1. **Sembolik-kesin doğrulama (SymPy)** — polinom özdeşlikler `expand`
   tabanlı KESİN sıfır testiyle ispatlanır (yaklaşık değil). Kaynak:
   `verify.symbolic_zero/symbolic_equal`.
2. **Deterministik sayısal doğrulama (NumPy)** — sembolik maliyetli olan her
   şey sabit tohumlu (seed=20260713) rastgele karmaşık örneklemlerle,
   ölçek-göreli toleransla test edilir. CI'da tekrarlanabilir.
3. **Bilinen-özdeşlik regresyonu** — kütüphanedeki her özdeşlik (şu an 21)
   kaynak makale referansı + yan koşul (Horn guard) metadata'sı taşır ve her
   push'ta yeniden ispatlanır. Kütüphane yalnız BÜYÜR (I-anahtarları donmuş,
   karar M7). Totolojik test ayakları açıkça işaretlidir; "kurtarıldı"
   sayımına yalnız yük taşıyan ayaklar girer.
4. **Keşif motoru sözleşmesi (K9/K10)** — motor (egglog equality saturation)
   TEK BAŞINA doğrulayıcı değildir: e-graph'ın önerdiği her aday çift,
   motordan bağımsız SymPy/NumPy yorumlamasıyla test edilir. Doğrulanamayan
   aday sessizce elenmez; `refuted` olarak yüzeye çıkar ve build'i KIRAR
   (unsound aksiyom sinyali). Negatif kontroller (ör. saturasyonun
   komütatiflik "icat etmemesi") kalıcı testlerdir. Ses sınırları
   `discovery/axioms.py` docstring'inde gerekçeliyle yazılıdır.
5. **Bağımsız adversarial denetim** — her aşamada, implementasyonu yazmamış
   ayrı bir denetçi ajan kodu ve matematiği kaynak makalelerden bağımsız
   rotalarla yeniden türeterek denetler; PASS almadan push yapılmaz.
   Bulgular aşama raporlarına işlenir (`reports/`).
6. **CI matrisi** — GitHub Actions, Python 3.10/3.11/3.12, her push'ta tam
   regresyon. Kırmızı CI = aşama kapanmamış demektir.

## Sınırlar (dürüstlük)

- Sayısal doğrulama (katman 2/4) ispat değildir; "rastgele nokta kümesinde
  eşitlik" kanıtıdır. Polinom-tipi özdeşliklerde pratik güveni yüksektir;
  yeni-aday özdeşlikler yayın iddiasına dönüşmeden önce katman 1'den
  (sembolik-kesin) geçirilmek ZORUNDADIR (Faz B boru hattı kuralı).
- Konvansiyon hatalarına karşı savunma: literatürden elle sabitlenmiş
  beklenen-değer fixture'ları (`tests/test_fixtures.py`) — rota-rotaya
  testlerin gizleyebileceği korelasyonlu hataları yakalamak için.
- Fizik YORUMU (hangi özdeşlik ilginç, hangisi yayın-değer) bu sistemin
  dışındadır; Kuntman/grup geri bildirimi gerektirir (Faz C/D pencereleri).
