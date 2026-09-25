# Yayımlanmış raporlar kendi betikleriyle yeniden üretilebiliyor mu

*2026-09-16 · betik `scripts/analiz/2026-09-16-rapor-yeniden-uretilebilirlik.py`*
*her betik koşuldu, çıktısı yayımlanan dosyayla karşılaştırıldı, sonra
çalışma ağacı **geri alındı**; betik temiz olmayan bir ağaçta başlamaz*

## Neden

Kural 7 her raporun betiğini adıyla taşımasını istiyor ve bu kural tutuldu.
Ama **tutulup tutulmadığı hiç sınanmamıştı**: bir betiğin bugün hâlâ o raporu
ürettiği ölçülmedi. ⛔ 2026-09-16'da tarih dönünce açık kendiliğinden görüldü —
48 betik rapor adını ya da tarih satırını `date.today()`'den kuruyordu ve
hiçbiri ertesi gün kendi yayımlanmış raporunu yeniden üretemiyordu.

⚠️ **Bu raporun ilk sürümü (aynı gün, commit `8314fbf`) kendi bulgusunu
yanlış sınıflandırdı.** O koşuda 29 betik yamalanmıştı ve 21 rapor *«kaydı»*
(girdi kaymış) diye işaretlendi. Yamanın eksik olduğu sonradan görüldü:
raporuna tarih yazan **19 betik daha** vardı. Onlar da sabitlenince *«kaydı»*
sayısı **21'den 3'e** düştü. ➡️ *Bir sınıflandırma, sınıflandırdığı kusurun
kendisi tam onarılmadan okunursa en kalabalık kutu «sebebi bilinmiyor»
kutusudur.* Bu yüzden sınama **onarımdan sonra yeniden koşuldu**.

## Sonuç

| | sayı |
|---|---:|
| ✅ aynı | **95** |
| ⏭️ model | **4** |
| ⛔ hata | **1** |
| ⛔ kaydı | **2** |
| ⛔ mühür | **2** |
| **toplam** | **104** |

⚠️ Ayrıca **0** rapor hiçbir betik adı taşımıyor ve bu sınamaya hiç giremiyor — Kural 7 onlarda **zaten** karşılanmamış.

## Betik betik

| Betik | rapor | sonuç | not |
|---|---|---|---|
| `2026-09-12-judge-karsilastirma.py` | `2026-09-12-judge-karsilastirma.md` | ✅ aynı |  |
| `2026-09-12-kullanici-mesaji-bicimi.py` | `2026-09-12-kullanici-mesaji-bicimi.md` | ✅ aynı |  |
| `2026-09-12-prompt-dili-ablasyonu.py` | `2026-09-12-prompt-dili-ablasyonu.md` | ⏭️ model | model çağırıyor — koşulmadı |
| `2026-09-12-thinking-dili-raporu.py` | `2026-09-12-thinking-dili-ogrenilebilirlik.md` | ✅ aynı |  |
| `2026-09-12-turkce-ifade-bankasi.py` | `2026-09-12-turkce-ifade-bankasi.md` | ✅ aynı |  |
| `2026-09-12-turkce-register-sondasi.py` | `2026-09-12-turkce-register-sondasi.md` | ⏭️ model | model çağırıyor — koşulmadı |
| `2026-09-12-uctan-uca-eval.py` | `2026-09-12-uctan-uca-eval.md` | ✅ aynı |  |
| `2026-09-14-baglam-dilimi-envanteri.py` | `2026-09-14-baglam-dilimi-envanteri.md` | ✅ aynı |  |
| `2026-09-14-dilim-kapsama-raporu.py` | `2026-09-14-dilim-kapsama.md` | ✅ aynı |  |
| `2026-09-14-golden-bolme.py` | `2026-09-14-golden-bolme.md` | ⛔ mühür | mühürlü girdiyi yeniden yazmaya çalıştı (K31 kapısı durdurdu) |
| `2026-09-14-golden-dev.py` | `2026-09-14-golden-dev.md` | ⛔ kaydı | iki koşu birbiriyle aynı, yayımlanan dosyadan farklı · ✅ ilan edilen SHA 1 girdide hâlâ tutuyor — sapma başka sebepten |
| `2026-09-14-golden-kosu-raporu.py` | `2026-09-14-golden-kosu-baseline.md` | ✅ aynı |  |
| `2026-09-14-gosterge-secimi.py` | `2026-09-14-gosterge-secimi.md` | ✅ aynı |  |
| `2026-09-14-judge-v2-karsilastirma.py` | `2026-09-14-judge-v2-karsilastirma.md` | ✅ aynı |  |
| `2026-09-14-judge-v3-kanit-puan.py` | `2026-09-14-judge-v3-kanit-puan.md` | ✅ aynı |  |
| `2026-09-14-judge-v4-derinlik.py` | `2026-09-14-judge-v4-derinlik.md` | ✅ aynı |  |
| `2026-09-14-judge-v4-karsilastirma.py` | `2026-09-14-judge-v4-havuzlanmis.md`, `2026-09-14-judge-v4-parti1-parti2.md`, `2026-09-14-judge-v4-parti2-parti3.md`, `2026-09-14-judge-v4-v3parti1.md`, `2026-09-14-judge-v4-v3parti2.md`, `2026-09-14-judge-v4-v3parti3.md` | ✅ aynı |  |
| `2026-09-14-judge-v4-uc-boyut.py` | `2026-09-14-judge-v4-uc-boyut.md` | ✅ aynı |  |
| `2026-09-14-korpus-hedef-raporu.py` | `2026-09-14-korpus-hedef-expert70.md`, `2026-09-14-korpus-hedef-v3-kumulatif.md`, `2026-09-14-korpus-hedef-v3-parti1.md`, `2026-09-14-korpus-hedef-v3-parti2.md` | ✅ aynı |  |
| `2026-09-14-kriz-filtresi-bedensel-acik.py` | `2026-09-14-kriz-filtresi-bedensel-acik.md` | ✅ aynı |  |
| `2026-09-14-replay-ornekleme.py` | `2026-09-14-replay-ornekleme.md` | ✅ aynı |  |
| `2026-09-14-replay-turkce-kalitesi.py` | `2026-09-14-replay-turkce-kalitesi.md` | ⏭️ model | model çağırıyor — koşulmadı |
| `2026-09-14-uzman-ornekleme.py` | `2026-09-14-uzman-ornekleme.md` | ⛔ mühür | mühürlü girdiyi yeniden yazmaya çalıştı (K31 kapısı durdurdu) |
| `2026-09-14-uzman-puanlama-analizi.py` | `2026-09-14-uzman-puanlama-analizi.md` | ✅ aynı |  |
| `2026-09-14-uzman70-bilesim.py` | `2026-09-14-uzman70-bilesim.md` | ✅ aynı |  |
| `2026-09-14-v3-ornekleme.py` | `2026-09-14-v3-ornekleme.md` | ✅ aynı |  |
| `2026-09-14-v3-parti2-baglam-plani.py` | `2026-09-14-v3-parti2-baglam-plani.md` | ✅ aynı |  |
| `2026-09-14-v3-parti2-plani.py` | `2026-09-14-v3-parti2-plani.md` | ✅ aynı |  |
| `2026-09-14-v3-parti3-plani.py` | `2026-09-14-v3-parti3-plani.md` | ✅ aynı |  |
| `2026-09-15-context-fidelity.py` | `2026-09-15-context-fidelity.md` | ✅ aynı |  |
| `2026-09-15-eksen-baseline.py` | `2026-09-15-eksen-baseline.md` | ✅ aynı |  |
| `2026-09-15-eksen2-judge-ayiklama.py` | `2026-09-15-eksen2-judge-ayiklama.md` | ✅ aynı |  |
| `2026-09-15-eksen2-judge-plan.py` | `2026-09-15-eksen2-judge-tasarim.md` | ✅ aynı |  |
| `2026-09-15-eksen2-judge-raporu.py` | `2026-09-15-eksen2-judge.md` | ✅ aynı |  |
| `2026-09-15-eksen4-sentetik-vs-gercek.py` | `2026-09-15-eksen4-sentetik-vs-gercek.md` | ✅ aynı |  |
| `2026-09-15-f4-kapsam-raporu.py` | `2026-09-15-f4-lora-kapsam-taramasi.md` | ✅ aynı |  |
| `2026-09-15-f4b-kapsam-raporu.py` | `2026-09-15-f4b-lora-kapsam-taramasi-2.md` | ✅ aynı |  |
| `2026-09-15-f4c-doz-raporu.py` | `2026-09-15-doz-yanit-egrisi.md` | ✅ aynı |  |
| `2026-09-15-forgetting-smoke.py` | `2026-09-15-forgetting-smoke.md` | ✅ aynı |  |
| `2026-09-15-gecikme-taban.py` | `2026-09-15-gecikme-taban.md` | ✅ aynı |  |
| `2026-09-15-geriye-donuk-eslesme.py` | `2026-09-15-geriye-donuk-eslesme.md` | ✅ aynı |  |
| `2026-09-15-golden-iddia-dayanikliligi.py` | `2026-09-15-golden-iddia-dayanikliligi.md` | ✅ aynı |  |
| `2026-09-15-golden-locked.py` | `2026-09-15-golden-locked.md` | ✅ aynı |  |
| `2026-09-15-golden-test.py` | `2026-09-15-golden-test.md` | ✅ aynı |  |
| `2026-09-15-judge-claude-sapmasi.py` | `2026-09-15-judge-claude-sapmasi-sonnet.md`, `2026-09-15-judge-claude-sapmasi.md` | ✅ aynı |  |
| `2026-09-15-judge-rubrik-korluk.py` | `2026-09-15-judge-v5-korluk.md`, `2026-09-15-judge-v6-korluk.md`, `2026-09-15-judge-v7-korluk.md` | ✅ aynı |  |
| `2026-09-15-judge-tekrar-test.py` | `2026-09-15-judge-tekrar-test.md` | ⛔ hata |    yeniden türetilemez — yayımlanmış hâli tek kayıttır (Kural 7). |
| `2026-09-15-judge-v7-etki.py` | `2026-09-15-judge-v7-etki.md` | ✅ aynı |  |
| `2026-09-15-judge-v7-uzman.py` | `2026-09-15-judge-v7-uzman.md` | ✅ aynı |  |
| `2026-09-15-k-gecis-toplama.py` | `2026-09-15-k-gecis-toplama.md` | ✅ aynı |  |
| `2026-09-15-klinik-iddia-kapisi-gercek-metin.py` | `2026-09-15-klinik-iddia-kapisi-gercek-metin.md` | ✅ aynı |  |
| `2026-09-15-korpus-v4-v6.py` | `2026-09-15-korpus-v4-v6.md` | ✅ aynı |  |
| `2026-09-15-korpus-v6-isaret-ayiklamasi.py` | `2026-09-15-korpus-v6-isaret-ayiklamasi.md` | ✅ aynı |  |
| `2026-09-15-korpus-v6-v7.py` | `2026-09-15-korpus-v6-v7.md` | ✅ aynı |  |
| `2026-09-15-korpus-v9-plan.py` | `2026-09-15-korpus-v9-tasarim.md` | ✅ aynı |  |
| `2026-09-15-korpus-v9-raporu.py` | `2026-09-15-korpus-v9-kosusu.md` | ✅ aynı |  |
| `2026-09-15-locked-baseline.py` | `2026-09-15-locked-baseline.md` | ✅ aynı |  |
| `2026-09-15-olu-desen-taramasi.py` | `2026-09-15-normalizasyon-olu-desen.md` | ✅ aynı |  |
| `2026-09-15-rag-a-katmani-chunk.py` | `2026-09-15-rag-a-katmani-pilot.md` | ✅ aynı |  |
| `2026-09-15-rag-mevcut-korpus-envanteri.py` | `2026-09-15-rag-mevcut-korpus-envanteri.md` | ✅ aynı |  |
| `2026-09-15-rag-soru-envanteri.py` | `2026-09-15-rag-soru-envanteri.md` | ✅ aynı |  |
| `2026-09-15-safety-crisis-ikinci-set-plan.py` | `2026-09-15-safety-crisis-ikinci-set-tasarim.md` | ✅ aynı |  |
| `2026-09-15-safety-crisis-ikinci-set-raporu.py` | `2026-09-15-safety-crisis-ikinci-set.md` | ✅ aynı |  |
| `2026-09-15-safety-crisis.py` | `2026-09-15-safety-crisis.md` | ✅ aynı |  |
| `2026-09-15-sycophancy.py` | `2026-09-15-sycophancy.md` | ✅ aynı |  |
| `2026-09-15-v7-gerekce.py` | `2026-09-15-v7-gerekce.md` | ⛔ kaydı | iki koşu birbiriyle aynı, yayımlanan dosyadan farklı · ✅ ilan edilen SHA 1 girdide hâlâ tutuyor — sapma başka sebepten |
| `2026-09-15-v7-kontrol-kosusu.py` | `2026-09-15-v7-kontrol-kosusu.md` | ✅ aynı |  |
| `2026-09-15-v7-turetme-sinamasi.py` | `2026-09-15-v7-turetme-sinamasi.md` | ✅ aynı |  |
| `2026-09-15-v8-kosu-plan.py` | `2026-09-15-v8-kosu-tasarim.md` | ✅ aynı |  |
| `2026-09-15-v8-raporu.py` | `2026-09-15-judge-v8-kosusu.md` | ✅ aynı |  |
| `2026-09-15-v8-turetme-sinamasi.py` | `2026-09-15-v8-turetme-sinamasi.md` | ✅ aynı |  |
| `2026-09-15-v9-kanit-denetimi.py` | `2026-09-15-v9-kanit-denetimi.md` | ✅ aynı |  |
| `2026-09-15-v9-kapi-denetimi.py` | `2026-09-15-v9-kapi-defteri.md` | ✅ aynı |  |
| `2026-09-15-v9-kosu-plan.py` | `2026-09-15-v9-kosu-tasarim.md` | ✅ aynı |  |
| `2026-09-15-v9-raporu.py` | `2026-09-15-judge-v9-kosusu.md` | ✅ aynı |  |
| `2026-09-15-v9-turetme-sinamasi.py` | `2026-09-15-v9-turetme-sinamasi.md` | ✅ aynı |  |
| `2026-09-15-vahsi-dilim-kaynak-taramasi.py` | `2026-09-15-vahsi-dilim-kaynak-taramasi.md` | ✅ aynı |  |
| `2026-09-16-alinti-nrm-sinamasi.py` | `2026-09-16-alinti-nrm-sinamasi.md` | ✅ aynı |  |
| `2026-09-16-buyuk-harf-kapisi.py` | `2026-09-16-buyuk-harf-kapisi.md` | ✅ aynı |  |
| `2026-09-16-dejenerasyon-ikinci-okuma.py` | `2026-09-16-dejenerasyon-ikinci-okuma.md` | ✅ aynı |  |
| `2026-09-16-dejenerasyon-kapisi.py` | `2026-09-16-dejenerasyon-kapisi.md` | ✅ aynı |  |
| `2026-09-16-faz4-kapanis-listesi.py` | `2026-09-16-faz4-kapanis-listesi.md` | ✅ aynı |  |
| `2026-09-16-golden-rubrik-kapsama.py` | `2026-09-16-golden-rubrik-kapsama.md` | ✅ aynı |  |
| `2026-09-16-ham-meta-hasari.py` | `2026-09-16-ham-meta-hasari.md` | ✅ aynı |  |
| `2026-09-16-ic-muhakeme-sizintisi.py` | `2026-09-16-ic-muhakeme-sizintisi.md` | ✅ aynı |  |
| `2026-09-16-ilan-edilen-sha-denetimi.py` | `2026-09-16-ilan-edilen-sha-denetimi.md` | ✅ aynı |  |
| `2026-09-16-istek-arsivle.py` | `2026-09-16-istek-arsivle.md` | ✅ aynı |  |
| `2026-09-16-judge-kapsama-kalibrasyonu.py` | `2026-09-16-judge-kapsama-kalibrasyonu.md` | ✅ aynı |  |
| `2026-09-16-k46-metrikleri.py` | `2026-09-16-k46-metrikleri.md` | ✅ aynı |  |
| `2026-09-16-kalan-lower-satirlari.py` | `2026-09-16-kalan-lower-satirlari.md` | ✅ aynı |  |
| `2026-09-16-katki-defteri-denetimi.py` | `2026-09-16-katki-defteri-denetimi.md` | ✅ aynı |  |
| `2026-09-16-kayma-kapanis.py` | `2026-09-16-kayma-kapanis.md` | ✅ aynı |  |
| `2026-09-16-kosu-kaydi-denetimi.py` | `2026-09-16-kosu-kaydi-denetimi.md` | ✅ aynı |  |
| `2026-09-16-lora-kapsam-onkontrolu.py` | `2026-09-16-lora-kapsam-onkontrolu.md` | ⏭️ model | model çağırıyor — koşulmadı |
| `2026-09-16-lower-denetimi.py` | `2026-09-16-lower-denetimi.md` | ✅ aynı |  |
| `2026-09-16-muafiyet-kapisi-gucu.py` | `2026-09-16-muafiyet-kapisi-gucu.md` | ✅ aynı |  |
| `2026-09-16-normalize-kanonlastirma.py` | `2026-09-16-normalize-kanonlastirma.md` | ✅ aynı |  |
| `2026-09-16-okunmayan-alan-denetimi.py` | `2026-09-16-okunmayan-alan-denetimi.md` | ✅ aynı |  |
| `2026-09-16-rapor-serh-denetimi.py` | `2026-09-16-rapor-serh-denetimi.md` | ✅ aynı |  |
| `2026-09-16-rol-siniri-ablasyonu.py` | `2026-09-16-rol-siniri-ablasyonu.md` | ✅ aynı |  |
| `2026-09-16-sizinti-sebebi.py` | `2026-09-16-sizinti-sebebi.md` | ✅ aynı |  |
| `2026-09-16-tez-plani-turetme.py` | `2026-09-16-tez-plani-turetme.md` | ✅ aynı |  |
| `2026-09-16-tohum-alani-tuketimi.py` | `2026-09-16-tohum-alani-tuketimi.md` | ✅ aynı |  |
| `2026-09-16-yonlendirme-olcutu-duyarliligi.py` | `2026-09-16-yonlendirme-olcutu-duyarliligi.md` | ✅ aynı |  |

## Sınıfların anlamı

| sınıf | ne demek | ne yapılmalı |
|---|---|---|
| ✅ **aynı** | betik bugün de aynı dosyayı üretiyor | — |
| ⚠️ **sıralama** | sayılar aynı, **satır sırası** farklı: bir yerde belirsiz tie-break var (`sorted(set(...))`) | ikincil anahtar eklenmeli; sayıları etkilemez ama *«yeniden üretilebilir»* iddiasını zayıflatır |
| ⛔ **kaydı** | iki koşu **birbiriyle aynı**, yayımlanan dosyadan farklı: girdi ya da kod değişmiş | ⛔ yayımlanan sayı artık betiğin ürettiği sayı değil — rapor ya yenilenmeli ya girdisi sabitlenmeli |
| ⛔ **kararsız** | aynı girdiyle **iki koşu birbirinden farklı**: betiğin içinde tohumsuz rastgelelik ya da belirsiz sıra var | ⛔ en ağır sınıf — rapor **hiçbir zaman** yeniden üretilemez; tohum sabitlenmeli |
| ⛔ **mühür** | betik bir eval seti **üretiyor** ve mühürlü dosyayı yeniden yazmaya çalıştı (K31 kapısı durdurdu) | üretici ile raporlayıcı **ayrılmalı**: rapor, seti yeniden üretmeden yazılabilmeli |
| ⛔ **argüman** | betik komut satırı argümanı istiyor ve **rapor onu kaydetmemiş** | çağrı satırı raporun başına yazılmalı |
| ⛔ **hata** | bugün hiç koşmuyor | girdisi silinmiş olabilir (Kural 8) |
| ⏭️ **model** | betik bir modeli çağırıyor; koşulmadı | yeniden üretilebilirliği zaten modele bağlı (K97) — ayrı bir soru |
| ⏱️ **zaman aşımı** | sınama penceresine sığmadı | elle koşulmalı |

⛔ **Bu tablo bir kusur listesi değil, bir ÖLÇÜM.** Bir raporun bugün yeniden
üretilememesi onun yanlış olduğu anlamına gelmez; *«yeniden üretilebilir»*
iddiasının **sınanmamış** olduğu anlamına gelir — ve artık sınanıyor.

## ⛔ Bu sınamanın ölçmediği

- **Raporun doğruluğu.** Ölçülen tek şey betik→dosya kararlılığı.
- **Betiğin girdisini nereden aldığı.** Scratchpad'e bağlı betikler oturum
  silinince *«hata»* sınıfına düşer; bu Kural 8'in bilinen bedeli.
- **`runs/` altındaki koşular.** Onlar yeniden üretilmez, saklanır (Kural 7).
