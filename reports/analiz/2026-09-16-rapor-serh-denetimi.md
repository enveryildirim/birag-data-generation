# Rapor şerh denetimi — T63 ve T68 artık sınanıyor

**Betik:** `scripts/analiz/2026-09-16-rapor-serh-denetimi.py` · **Tarih:** 2026-09-16  
**Girdi:** `reports/analiz/*.md` — **123** rapor  
**Girdi:** `prompts/judge-eksen1.v9.md` SHA256 `4b78260a96d78311` (bayrak adları buradan)  
**Girdi:** `configs/training/f4*.yaml` — **21** config (kol adları buradan)  
**Kesme tarihi:** `2026-09-16` — kural bu günden itibaren borç doğurur (Kural 7)

---

## Neden

T63 ve T68 birer **yazım kuralı** bırakmıştı ve ikisi de yalnızca `plan.md`'ye
yazılmıştı. ⛔ Aynı oturumda T70 bunun bedelini ölçtü: `samples.md` **iki ayrı**
**yerde** ilan edilmiş, **24 koşunun hiçbirinde** üretilmemişti — çünkü ilanı
sınayan bir şey yoktu. ➡️ *Bir yazım kuralı, denetlenmediği sürece bir kural*
*değil bir dilektir.* Burada ikisi de **tetikleyici + uyum** çiftine çevriliyor.

| | Tetikleyici | Uyum |
|---|---|---|
| **Ş1** (T68) | rapor bir sert kapı bayrağını **sayıyla** bildiriyor | *«üst sınır»* şerhi var |
| **Ş2** (T63) | rapor **≥3 kolu** adlandırıp bir **sıra** kuruyor | *«ters çift»* sayısı var |

⛔ Listeler elle yazılmıyor: **5 bayrak** rubrikten (`bos_guvence`, `klinik_guvenlik_ihlali`, `kurum_yordam_ihlali`, `rol_siniri_ihlali`, `tuzak_ihlali`), **6 kol** config'lerin `ad:` alanından (`A-dar`, `A-dar-280adim`, `B-derin`, `C-dikkat`, `D-tam`, `E-genis`).

---

## 1. Ş1 (T68) — sert kapı sayısı bildiren rapor *«üst sınır»* diyor mu

Güvenlik judge'ları **tek yönlü tedbirli sapma** gösteriyor ve bizim asimetrimiz bu sapmayı azaltmıyor, **aynı yöne ekliyor** (T68). ⇒ Bildirdiğimiz ihlal sayıları **üst sınırdır** ve bu her sayının yanında yazılı olmalı.

| | rapor |
|---|---:|
| ⛔ **borçlu** (kesme sonrası, şerh yok) | **0** |
| ✅ uyan | 3 |
| ⚪ kesme öncesi (değiştirilmez, Kural 7) | 31 |

✅ **Uyanlar:** `2026-09-16-ic-muhakeme-sizintisi.md`, `2026-09-16-parti2-judge-v9.md`, `2026-09-16-rol-siniri-ablasyonu.md`

⚪ **Kesme öncesi 31 rapor** tetikliyor; 1'inde şerh **rastlantıyla** var. Şerhsiz olanlar bir kusur **değil**: kural o gün yoktu ve geçmiş rapor değiştirilmez (Kural 7). ⚠️ Ama tezde bu raporlardan sayı alınırken şerh **oradan değil buradan** okunmalı:

`2026-09-14-golden-dev.md`, `2026-09-14-golden-kosu-baseline.md`, `2026-09-14-gosterge-secimi.md`, `2026-09-14-judge-v4-havuzlanmis.md`, `2026-09-14-judge-v4-parti1-parti2.md`, `2026-09-14-judge-v4-parti2-parti3.md`, `2026-09-14-judge-v4-uc-boyut.md`, `2026-09-14-judge-v4-v3parti1.md`, `2026-09-14-judge-v4-v3parti2.md`, `2026-09-14-judge-v4-v3parti3.md`, `2026-09-15-geriye-donuk-eslesme.md`, `2026-09-15-golden-iddia-dayanikliligi.md`, `2026-09-15-judge-claude-sapmasi-sonnet.md`, `2026-09-15-judge-claude-sapmasi.md`, `2026-09-15-judge-tekrar-test.md`, `2026-09-15-judge-v5-korluk.md`, `2026-09-15-judge-v6-korluk.md`, `2026-09-15-judge-v7-korluk.md`, `2026-09-15-judge-v7-uzman.md`, `2026-09-15-judge-v9-kosusu.md`, `2026-09-15-k-gecis-toplama.md`, `2026-09-15-korpus-v4-v6.md`, `2026-09-15-korpus-v6-isaret-ayiklamasi.md`, `2026-09-15-korpus-v6-v7.md`, `2026-09-15-korpus-v9-kosusu.md`, `2026-09-15-locked-baseline.md`, `2026-09-15-v7-kontrol-kosusu.md`, `2026-09-15-v8-kosu-tasarim.md`, `2026-09-15-v8-turetme-sinamasi.md`, `2026-09-15-v9-kosu-tasarim.md`, `2026-09-15-v9-turetme-sinamasi.md`

## 2. Ş2 (T63) — kol sırası kuran rapor **ters çift** sayısı veriyor mu

Eşitliğin sık olduğu 6 kolluk bir kümede sıra numarası **eşitlik bozucu ada** duyarlıdır; ilk hesap *«4 kolun sırası değişti»* dedi, doğru sayı **1**'di. ⇒ Sıra yazılacaksa yanında **kesin ters dönen çift** sayısı olmalı.

| | rapor |
|---|---:|
| ⛔ **borçlu** (kesme sonrası, şerh yok) | **0** |
| ✅ uyan | 1 |
| ⚪ kesme öncesi (değiştirilmez, Kural 7) | 8 |

✅ **Uyanlar:** `2026-09-16-judge-kapsama-kalibrasyonu.md`

⚪ **Kesme öncesi 8 rapor** tetikliyor; 0'inde şerh **rastlantıyla** var. Şerhsiz olanlar bir kusur **değil**: kural o gün yoktu ve geçmiş rapor değiştirilmez (Kural 7). ⚠️ Ama tezde bu raporlardan sayı alınırken şerh **oradan değil buradan** okunmalı:

`2026-09-15-eksen2-judge-tasarim.md`, `2026-09-15-eksen2-judge.md`, `2026-09-15-f4-lora-kapsam-taramasi.md`, `2026-09-15-judge-v8-kosusu.md`, `2026-09-15-judge-v9-kosusu.md`, `2026-09-15-safety-crisis-ikinci-set.md`, `2026-09-15-v8-kosu-tasarim.md`, `2026-09-15-v9-kosu-tasarim.md`

## ⛔ Bu denetimin söylemedikleri

| | |
|---|---|
| ⛔ Şerhin **doğru yerde** olduğu | dizge aranıyor, konumu değil: raporun sonunda tek cümle de sayılır. ⚠️ İnsan okuması gerekli |
| ⛔ Tetikleyicinin **tam** olduğu | bayrağı sayıyla bildirmenin tek biçimi tablo değil; düzyazıyla verilen bir sayı görünmez |
| ⚠️ Ş2 bugün **neredeyse boş çalışıyor** | kesme sonrası tek tetikleyen rapor var ve o zaten uyuyor. Kuralın değeri ilk ihlalde ortaya çıkacak — ⭐ *boş çalışan bir denetim, yokluğu ölçülemeyen bir denetimden farklıdır* |
| ⛔ Kendi raporu ve 4 denetim raporu | kapsam dışı (aşağıda), çünkü bayrak adlarını **sayarak değil alıntılayarak** taşıyorlar |

**Kapsam dışı bırakılanlar — gerekçesiyle:**

· `2026-09-16-ilan-edilen-sha-denetimi.md` — SHA sayar, bayrak saymaz  
· `2026-09-16-katki-defteri-denetimi.md` — katkı sayar, bayrak saymaz  
· `2026-09-16-rapor-serh-denetimi.md` — denetimin kendisi (yapısal, T64'ün sınıfı)  
· `2026-09-16-rapor-yeniden-uretilebilirlik.md` — betik adı sayar, bayrak saymaz  
· `2026-09-16-tez-plani-turetme.md` — artefakt sayar, bayrak saymaz  

