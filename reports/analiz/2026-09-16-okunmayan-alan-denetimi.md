# Okunmayan alanlar doğru mu — T79'un (b) şıkkı

**Betik:** `scripts/analiz/2026-09-16-okunmayan-alan-denetimi.py` · **Tarih:** 2026-09-16  
**Girdi:** `data/seeds.v2.jsonl` SHA256 `3399f543c8b882c7` — **2240** tohum

---

## Neden

T79: `SeedMeta`'nın 16 alanından **11'ini** boru hattında hiçbir şey okumuyor
⇒ *okunmayan bir alanın yanlış olduğu hiçbir yerde ortaya çıkmaz.* Üç yoldan
**(b)** seçildi: betimleyici olarak kullan ama doğruluğunu **ayrıca denetle**.

⭐ Ölçüt **geri düşme oranı**: ham değer kanonik bir sınıfa çevrilemeyip
`diger`/`belirtilmemis`/`belirsiz`/`None`'a düşüyorsa alan ya kaynakta yok
ya da eşleme kopuk. ⛔ İkisini bu betik **ayıramaz** (T77: üst sınır ≠
gerçek) — ama **bakılacak yeri gösterir**.

⛔⛔ **Geri düşme değeri ALANIN KENDİSİNE bağlıdır ve ilk ölçümüm bunu
kaçırdı:** `"yok"`u her alanda geri düşme saymıştım ve `onceki_tedavi` %69 ile
*«yüksek riskli»* göründü. Oysa orada `yok` = **önceki tedavi yok**, yani
gerçek bir değer; `stres_tipi`'nde ise `normalize()` onu **fallback olarak**
**üretiyor**. ➡️ *Aynı dizge bir alanda VERİ, ötekinde YOKLUK — ve bunu ayıran
şey değerin kendisi değil, onu üreten KODdur.*

---

## Geri düşme oranları

| alan | okunuyor mu | geri düşen | oran | |
|---|---|---:|---:|---|
| `bagimlilik_turu` | ⭐ evet | 0 | %0.0 | ✅ |
| `bagimlilik_alt_turu` | — | 20 | %0.9 | ✅ |
| `senaryo` | ⭐ evet | 531 | %23.7 | ⚠️ |
| `stres_tipi` | — | 1714 | %76.5 | ⛔ **yüksek** |
| `profil` | — | 40 | %1.8 | ✅ |
| `yas_grubu` | ⭐ evet | 0 | %0.0 | ✅ |
| `evre` | — | 0 | %0.0 | ✅ |
| `motivasyon_evresi` | — | 0 | %0.0 | ✅ |
| `motivasyon` | — | 0 | %0.0 | ✅ |
| `risk_seviyesi` | ⭐ evet | 0 | %0.0 | ✅ |
| `siddet_seviyesi` | — | 0 | %0.0 | ✅ |
| `egitim` | — | 0 | %0.0 | ✅ |
| `kullanim_suresi` | — | 0 | %0.0 | ✅ |
| `onceki_tedavi` | — | 80 | %3.6 | ✅ |
| `cinsiyet` | — | 480 | %21.4 | ⚠️ |

⛔ **1 okunmayan alanın geri düşme oranı %40'ın üstünde:** `stres_tipi` (%77).

⭐ **Kalan tek yüksek satır `stres_tipi` ve sebebi T77'de ölçülü:**
`normalize()` zinciri `_exact`'i önce deniyor (374/2240 kayıt) ve `_keyword`'e
ulaşan 1866 kaydın tamamı İngilizce `snake_case`; eşleşmeyen her kayıt
`senaryo != belirsiz` ise **yapıca** `yok` alıyor. ⇒ Oran bir **kopukluk**
değil, zincirin tasarımı. ⚠️ Yine de tezde betimleyici olarak kullanılırsa
*«%76'sı `yok`»* cümlesi **yanıltıcıdır**: o `yok` ölçülmüş bir yokluk değil,
**ölçülememiş** bir alandır.

⚠️ **Yüksek oran kendiliğinden kusur DEĞİL:** `senaryo=belirsiz` %23,7 ve o
**tasarım gereği** (K37: belirsiz bir etiketleme borcu değil, üretim-zamanı
kararı). ⇒ Her yüksek satır **elle** okunmalı; bu betik onları **işaretler**,
hükmetmez.

---

## ⭐ En sık değerler — okunmayan alanlar

· **`bagimlilik_alt_turu`** (24 ayrık) — `sigara` %20, `karma_alkol` %16, `karma_bahis` %8, `benzodiazepin` %7  
· **`stres_tipi`** (14 ayrık) — `yok` %75, `yalnizlik` %3, `akademik_stres` %3, `aile_catismasi` %3  
· **`profil`** (9 ayrık) — `beyaz_yakali` %25, `emekli_yasli` %13, `lise_ergeni` %12, `universite_ogrencisi` %12  
· **`evre`** (7 ayrık) — `tolerans` %46, `birakma_cabasi` %12, `dibe_vurma` %11, `nuksetme` %10  
· **`motivasyon_evresi`** (4 ayrık) — `dusunme` %67, `on_dusunme` %17, `hazirlik` %12, `eylem` %4  
· **`motivasyon`** (5 ayrık) — `ic_motivasyon` %43, `aile_baskisi` %27, `tetikleyici_olay` %21, `duygusal_regulasyon` %5  
· **`siddet_seviyesi`** (3 ayrık) — `orta` %64, `agir` %23, `hafif` %14  
· **`egitim`** (5 ayrık) — `universite` %44, `lise` %39, `ortaokul` %7, `lisansustu` %6  
· **`kullanim_suresi`** (5 ayrık) — `3_10_yil` %46, `1_3_yil` %27, `0_6_ay` %13, `6_ay_1_yil` %10  
· **`onceki_tedavi`** (5 ayrık) — `yok` %69, `profesyonel_destek` %19, `kendi_basina_deneme` %7, `bilinmiyor` %4  
· **`cinsiyet`** (3 ayrık) — `erkek` %47, `kadin` %31, `belirtilmemis` %21  

➡️ *Bir alanın **ayrık değer sayısı** ve **en sık değerinin payı** birlikte*
*okunur: 1-2 ayrık değer taşıyan bir alan ya gerçekten tekdüze ya da eşlemesi*
*çökmüş demektir ve ikisi ayırt edilmelidir.*

## ⛔ Bu denetimin söylemedikleri

| | |
|---|---|
| ⛔ **«Kaynakta yok» ile «eşleme kopuk» ayrılmadı** | ayırmak için ham meta ile alan alan karşılaştırma gerekir; T77 bunu yalnızca `egitim`, `kullanim_suresi` ve `stres_tipi` için yaptı |
| ⛔ **Doğruluk ölçülmedi, GERİ DÜŞME ölçüldü** | geri düşmeyen bir değer de yanlış olabilir (yanlış kova — T76'nın sınıfı) |
| ⚠️ Yüksek oran kusur değil | `senaryo=belirsiz` tasarım gereği (K37) |
| ⛔ `notlar` kapsam dışı | sözlük; alt anahtarları ayrıca taranmadı |

