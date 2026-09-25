# Korpus koşusu (v8 + v9) — TASARIM *(koşudan ÖNCE yazıldı)*

*2026-09-15 · betik `scripts/analiz/2026-09-15-korpus-v9-plan.py`*
*korpus `data/candidates/v3-kumulatif.jsonl` SHA256 `5867e31fc49e3dbf` · 104 kayıt*
*rubrikler: v7 `2cfd542fc671c64d` · v8 `bfc1e242a21a7043` · v9 `4b78260a96d78311`*

## Soru

v8 ve v9 üretim hattının varsayılanı (K118/K120) ama ikisi de yalnızca **Eksen
2'de** (20 kriz öğesi) ölçüldü. Hattın işlediği şey korpus. İki soru:
**(1)** v9 korpus kararlarını değiştiriyor mu — yani hangi kaydın eğitime gireceğini?
**(2)** v9'un Eksen 2'de **hiç uyarılamayan** iki parçası burada uyarılıyor mu?

## ⭐ Korpusun ölçebildiği, Eksen 2'nin ölçemediği

| yol | Eksen 2 | korpus |
|---|---:|---:|
| `context` (bağlam belgesi) taşıyan kayıt | **0**/114 | **10**/104 |
| çok turlu kayıt (1'den fazla BıRAG turu) | **0**/114 | **32**/104 |

⭐ v9'un iki mekanizması **yalnızca** bu iki yolda uyarılabilir: bağlam kaçışının
alıntı **doğrulaması** ve dayanağın **hangi tura ait olduğunun** kodca bulunması.
Eksen 2'de kod kapısının 0 kez ateşlemesi (T46) kısmen bunun sonucuydu.

## Küme ve aşamalar

| Aşama | Ne | k |
|---|---|---|
| 1a | 104 kayıt, **v8** rubriğiyle, kör | 1 |
| 1b | 104 kayıt, **v9** rubriğiyle, kör | 1 |
| 2 | tohumla çekilmiş **24** kayıt, v9 ile 2 ek geçiş | 3 |

⛔ **v8 DE koşuluyor** çünkü korpusta hiç koşmadı. Yalnızca v9 koşulsaydı v7→v9
farkı iki sürümü birden taşır ve hiçbir kaleme atfedilemezdi.
⚠️ v8'e ayrı gürültü tabanı **koşulmuyor** — köprü rolünde. Bunun bedeli:
**v8'e ait farklar tek tek okunamaz.**

### Kuyruk kimliği — dosya değil KOD doğrulandı

v7 korpus koşusunun iş dosyaları Kural 8 gereği silinmiş. Yerine commit `0b3c43f` ile kod kimliği doğrulandı:

| işlev | v7 commit'i ile aynı |
|---|:--:|
| `_render_conversation` | ✅ |
| `_last_assistant` | ✅ |
| `prompt_kur` | ✅ |

➡️ Üretilen konuşma kuyruğu v7'nin kuyruğuyla **aynı olmak zorunda**; kimlik
dosya karşılaştırmasıyla değil **kod karşılaştırmasıyla** kuruluyor.

### Yansız kontrol kümesi — tohum `20260915`, 24 kayıt

Ayrışmadan **bağımsız** çekildi; ayrışan kayıtlarla kesişmesi beklenen ve
istenen bir durumdur. Çekilen kimlikler (ilk 8 hane):

> `0d95d945` · `0fd4ea08` · `16c95f92` · `1cf213a5` · `28f93b83` · `2ee68a30` · `3517c2b8` · `48c49e21` · `4a8af146` · `4d3ca8e3` · `52545776` · `54e51a55` · `5d24f424` · `61591116` · `69776ab9` · `7a2be624` · `83e6e632` · `afeb9133` · `b16775d1` · `cb0b36a9` · `db79f395` · `dec0afd1` · `dfe09cff` · `f3c15ff6`

## Karar ölçütü *(T24 — önceden yazıldı, sonradan gevşetilmez)*

- **Ö1.** ⭐ **KORPUSUN VARLIK SEBEBİ: iki yol ilk kez uyarılıyor.** (a) `context` taşıyan 10 kayıtta bağlam kaçışının **doğrulaması**, (b) çok turlu 32 kayıtta dayanağın **hangi tura** ait olduğunun kodca bulunması. Her ikisinin kaç kez uyarıldığı raporlanır. ⛔ **Sıfır çıkarsa v9'un o parçaları hâlâ sınanmamıştır ve öyle yazılır** — Eksen 2 koşusunda kod kapısının 0 kez ateşlemesi (T46) tam olarak bu sebeple bir eksiklik olarak kaydedilmişti.
- **Ö2.** **Her değişen karar atfedilebilmeli.** v7→v8 ve v8→v9 ayrı ayrı okunur; v9'un makine-okunur izleri (`alinti_dogrulanmadi` · `teselli_dayanak_dogrulandi` · `alinti_dogrulama`) ve alan değerleri kullanılır. Atfedilemeyen değişim gürültüdür ve gürültü bandıyla karşılaştırılır.
- **Ö3.** ⛔ **Gürültü tabanı.** v7'nin korpusta **üç geçişi** var (K106), yani v7'nin tabanı zaten ölçülü. v9 için taban, tohum `20260915` ile çekilen **24 rastgele kayıt** × 2 ek geçişle ölçülür; tohum ve büyüklük burada, koşudan önce yazılıdır. ⚠️ v8'e ayrı taban koşulmaz — v8 bu koşuda **köprü**, kendi başına bir iddia taşımıyor. Bu, v8'e ait farkların tek tek okunamayacağı anlamına gelir ve raporda öyle yazılır.
- **Ö4.** ⭐ **ÜRETİM SONUCU ölçülür.** v9 hattın varsayılanı (K120): korpus kayıtlarının **bayrakları** (`rol_siniri_ihlali` · `klinik_guvenlik_ihlali` · `bos_guvence` · `tuzak_suclama` · `tuzak_etiketleme`) ve **hesaplanan üç puanı** v7'ye göre nasıl değişiyor. Bu sayı doğrudan hangi kaydın eğitime gireceğini etkiler.
- **Ö5.** ⛔ **Doğrulayıcının kendi hata oranı yine ölçülür.** Eksen 2'de 0 çıktı ama orada bağlam belgesi yoktu. Korpusta `rol_baglam_alintisi` bir **belgeden** alıntı ister; belge metniyle eşleşme, konuşma metniyle eşleşmeden daha kırılgandır. `alinti_dogrulanmadi` kayıtlarının tamamı dökülür ve elle okunur.
- **Ö6.** **Maliyet:** bozuk JSON, eksik alan, kaldırılan alanı yine de yazan kayıt.
- **Ö7.** **Dokunulmayan boyutlar kaymamalı.** v9 F1/F3/F4/F5'e ve Bölüm A-E'ye dokunmadı; `anlasilirlik_holistik` · `dogallik_holistik` · `mi_uyumu_holistik` · `duygusal_tepki` · `yorumlama` · `kesif` ortalamaları raporlanır. ⚠️ Beklenti yazılmıyor: v7'nin kendi kontrol koşusu bu boyutlarda rubrik etkisinden BÜYÜK kayma üretmişti (K61), yani buradaki kayma **rubriğe delil değildir** — yalnızca gürültünün büyüklüğünü hatırlatır.

## Elenen alternatifler *(Kural 7)*

| Alternatif | Neden değil |
|---|---|
| Yalnızca v9'u koşmak | ⛔ v8 korpusta hiç koşmadı; v7→v9 farkı **iki sürümü birden** taşır ve hiçbir kaleme atfedilemez. Tam da bu projenin sürekli eleştirdiği türden bir sayı olurdu. |
| v8'e de gürültü tabanı koşmak | ⛔ v8 bu koşuda köprü; kendi başına bir iddiası yok. 24×2 ek iş, okunmayacak bir sayı için harcanırdı. ⚠️ Bedeli açık: v8'e ait farklar tek tek okunamaz. |
| İş dosyalarını v7'nin dizinlerinden kopyalamak | ⛔ O dosyalar Kural 8 gereği silinmiş. Yerine **daha güçlü** bir kanıt kullanılıyor: iş kurucusu (`prompt_kur`) ve render (`_render_conversation`, `_last_assistant`) commit `0b3c43f` ile **birebir aynı** — yani üretilen kuyruk v7'nin kuyruğuyla aynı olmak zorunda. Kimlik dosyadan değil **koddan** doğrulanıyor. |
| Korpusu yeniden ÜRETMEK | ⛔ Puanlanan metin değişmemeli; ölçülen şey rubrik. |
| Eksen 2'nin hakemlik kümesini korpusa taşımak | ⛔ Farklı nüfus. Korpusun kendi rastgele kümesi tohumla çekiliyor. |

## Bu koşunun ölçmeyeceği

- **Judge ailesi sapması (K45).** Korpusu Claude yazdı, judge da Claude ailesi —
  bilinen ve ölçülmüş bir sapma (+6/+11 puan). Karşılaştırma yine temiz (v7 de
  aynı aile) ama mutlak puanlar bu sapmayı taşıyor.
- **Uzman uyumu.** K27 örneklemi gerekir.
- **Kriz davranışı.** Korpusta kriz kaydı yok (Kural 3); F2/F7 burada zayıf uyarılır.
- **v8'e ait farkların tek tek okunması** — v8'in kendi tabanı ölçülmüyor.
