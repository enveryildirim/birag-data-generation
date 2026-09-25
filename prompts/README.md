# Üretim promptları

Faz 2'de ilk şablon eklenir. Her prompt sürümlü olur; hash'i `gen_meta.prompt_hash`
alanına yazılır (§12). Dosya adı kalıbı: `<amac>.v<N>.md`.

## Sürümler

| Amaç | Güncel | Süperse edilenler (silinmez, Kural 7) |
|---|---|---|
| Judge · Eksen 1 | **`judge-eksen1.v9.md`** (K120) | v1 · v2 · v3 · v4 · v5 · v6 · v7 · v8 |
| Üretim | **`uretim-v5.md`** (delta; taban `uretim-v4.md`, K110 §8b) | `uretim-v2.md` · `uretim-v3.md` |
| Yeniden kurma (`v0.1.1`) | **`uretim-v6.md`** (K277; delta, taban v5) — yeni kayıt yazmaz, düşünmeyi yeniden kurar | — |
| Karar korunumu okuması | **`karar-korunumu.v1.md`** (K277) — eski ↔ yeni düşünme | — |
| Türkçe doğallık sondası | `turkce-dogallik-sondasi.v1.md` | — |

⚠️ Judge sürümü `src/filter.py` içindeki `JUDGE_PROMPT_VERSION` ile seçilir
(`BIRAG_JUDGE_SURUM` ortam değişkeni ezer). **Eski kayıtlar yeniden puanlanmaz:**
her kayıt kendi `prompt_version`'ını taşır ve K97 farklı sürümlerin aynı tabloda
karşılaştırılmasını yasaklar.

## ⛔ v8'de bilinen kusur — dosya DÜZELTİLMEZ

`judge-eksen1.v8.md` §F6'nın örnek tablosunda `E-genis`/`sk-020` satırı
*«cümle kullanıcının tırnak içindeki sözcüğünü taşıyor»* diyor ve
`teselli_ozgu_oge` / `teselli_kullanici_alintisi` için *«bekleyebilirsin»*
yazılmasını öğretiyor. **Sözcük o konuşmada hiç geçmiyor** — cevap olmayan bir
turu alıntılamış (`reports/analiz/2026-09-15-v9-kanit-denetimi.md` §1).

⚠️ Dosya **düzeltilmez**: v8 ile koşulmuş bir ölçüm var ve SHA256'sı
(`bfc1e242a21a7043`) o koşunun raporuna yazılı (Kural 7). Düzeltme v9'da yapıldı;
aynı vaka orada **ders vakası** olarak duruyor ve türetme sınaması her koşuda
iddianın çürümediğini yeniden denetliyor.
