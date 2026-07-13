# AŞAMA 3 — RAPOR

**Tarih**: 2026-07-13 · **Spec**: `specs/stage-03.md` · **Mod**: otonom
**Sonuç**: TAMAMLANDI — 65/65 test yeşil; boru hattı v1.1; **önemli
güvenilirlik bulgusu yakalandı ve etrafından dolaşıldı** (aşağıda).

---

## 1. Teslim edilenler

- **Boru hattı v1.1 (tersine akış)**: sayısal parmak izi kovalar aday ÖNERİR
  (`fingerprint.py`, kaba 3-ondalık anahtar, doğrulamadan bağımsız tohum) →
  her aday çift **yalıtılmış iki-terimli e-graph'ta** İSPATLANIR → bağımsız
  çok-tohumlu sayısal doğrulama karar verir. Yeni sınıf: **`underivable`** —
  sayısal doğru ama aksiyomlardan türetilemeyen çift (yenilik/eksik-aksiyom
  sinyali; Aşama 5-6'nın girdisi).
- **conj-normal budanmış enumerasyon** (`terms.py`): Conj yalnız atom
  seviyesinde; boyut 9'da 5698 → 1476 terim. (İçerik max_size kayması payıyla
  korunur — docstring'de dürüst kayıt.)
- Çakışma-gölgeleme kapaması: parmak izi çakışması yaşayan kova artıkları
  kendi aralarında yeniden incelenir (tamlık kaybı kapatıldı).
- `spikes/bench_stage3.py`, `spikes/egglog_pathology_probe.py`,
  `docs/egglog-large-graph-pathology.md`.

## 2. GÜVENİLİRLİK BULGUSU — egglog 13.2.0 büyük-graf patolojisi

Paylaşılan tek e-graph üzerinde (1476 terim) saturasyon **tutarsız** çıktı:
yalıtımda ispatlanan 9 çift büyük grafta "ispatlanamaz" göründü; `extract`
bir terimi **farklı atom-çokkümesindeki** bir sınıfa düşürdü (aksiyomların
hiçbiri çokkümeyi değiştiremez — imkânsız temsilci). Denetçi üç bağımsız
argümanla kök nedeni kütüphaneye sabitledi (monotonluk ihlali, kongruans
ihlali, çokküme değişmezi) ve tüm sayıları yeniden üretti.

**Sistem tasarımı gereği yakalandı**: e-graph hiçbir zaman tek doğrulayıcı
değildi (M10); sahte-underivable çiftler sayısal katmanda "doğru ama
ispatsız" görününce alarm verdi. **Çözüm (M18)**: paylaşılan graf kaldırıldı;
her çift taze iki-terimli grafta ispatlanıyor. Bilinçli takas: hız yerine
güvenilirlik. Upstream'e hata bildirimi dış temas olduğundan kullanıcı
onayına bırakıldı (kritik-karar listesi).

## 3. Ölçümler (bu sandbox; K15)

| mod | boyut | terim | kova | verified | underivable | refuted | çakışma | süre |
|---|---|---|---|---|---|---|---|---|
| full | 7 | 570 | 64 | 506 | 0 | 0 | 0 | ~10 sn |
| pruned | 7 | 212 | 56 | 156 | 0 | 0 | 0 | ~3 sn |
| pruned | 9 | 1476 | 128 | **1348** | **0** | **0** | 0 | ~30 sn |

İç tutarlılık değişmezi testte: çakışma=0 iken verified = terim − kova.

## 4. Bağımsız denetim

Verdict: **PASS**. Patoloji problarını yeniden üretti; kural-kural çokküme
korunumunu bağımsız doğruladı; parmak izinin −0.0 normalizasyonunu ve
yanlış-ayrılma mesafesini ölçtü (en yakın sınır 1.3e-7 — 1e-12 titremeden 5
kademe uzak). Üç önerisi uygulandı: çakışma-gölgeleme kapaması, patoloji
ailesi regresyonu (6 çift) + verified=terim−kova değişmezi, docstring/K14/spec
düzeltmeleri.

## 5. Sıradaki aşama (otonom devam)

**Aşama 4 — Aday boru hattı: sayısal ön-elek → sembolik ispat**: underivable
çiftleri için SymPy **sembolik-kesin** doğrulama katmanı (rastgele örneklem
yerine tam ispat, VERIFICATION.md katman-1'in keşif tarafına bağlanması) +
atom sayısı ölçekleme (3 atom) denemesi.
