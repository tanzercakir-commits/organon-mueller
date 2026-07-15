# AŞAMA 19 — Dokümantasyon (Faz E kapanışı)

**Tarih**: 2026-07-14 · **Mod**: otonom · **Probe**: mekanizma yok.

## 1. Hedefler

1. **README.md** (repo dış yüzü — GitHub sync `/README.md` include):
   ne/durum (deneysel; doğrulanmış vs aday); üç kullanım yüzeyi
   (paket/MCP/web); hızlı başlangıç (çalışan komutlar); doğrulama
   sözleşmesi özeti + docs linkleri; LİSANS notu (yok — kullanıcı kararı,
   açıkça). A15 fiil-disiplini: iddia = kanıt sınıfı.
2. **docs/architecture.md**: katman diyagramı + sorumluluklar + tek-yönlü
   köprüler (M35-M37); M-serisi/K-serisi indeks tablosu (yük taşıyanlar);
   güvenlik sınırı (safe_parse GATE).
3. **docs/user-guide.md**: terminal kullanamayan son kullanıcı; "hangi
   soru → hangi araç"; üç yüzeyin kullanımı; kanıt etiketlerinin okunuşu.
4. Mevcut docs tutarlılık taraması: ROADMAP A0-A19 durum işaretleri;
   A18 "hosted → statik" kapsam-değişikliği notu; kırık link yok.

## 2. Doğruluk (docs = repo gerçeği)

`tests/test_docs.py`: göreli linkler çözülür; README Python snippet'leri
import edilir + sembolleri var; belirtilen test sayısı gerçek toplama
eşit (drift guard); 21 özdeşlik iddiası kütüphaneyle eşleşir; MCP komutu
gerçek entry-point; bayat "Stage 2" durumu yok; pyproject extra'ları
README ile tutarlı.

## 3. Kabul

Üç doküman + ROADMAP güncel; test_docs.py yeşil; her komut/sayı/link
repo gerçeğine uyar (denetçi fact-check PASS şart); 276→286 test.

**DUR BURAYA**
