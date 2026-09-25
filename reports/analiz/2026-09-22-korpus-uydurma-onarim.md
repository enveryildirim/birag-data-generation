# Kapıdan düşen eski kopyalar kanonik metinle tazelendi

**Betik:** `scripts/analiz/2026-09-22-korpus-uydurma-onarim.py` · **Tarih:** 2026-09-22  
**Kanonik kaynak:** `data/judged/v0.0.18.jsonl` (ana hat)  
**Tazelenen satır:** 10 · **kayıt:** 2 · **dosya:** 10  

## ⛔⛔⛔ T266'nın bir hükmü GERİ ALINDI

T266'da *«kapı korpusta iki YENİ uydurma buldu, daha önce bilinmiyordu»* yazmıştım. **Yanlış.** Ölçüldü: `data/judged/v0.0.8` … `v0.0.20` girdilerinin **hepsi** ve `datasets/v0.0.8` … `v0.0.20` train dosyalarının **hepsi** bu kayıtlar için **temiz metni** taşıyor. Sonraki parti sürümleri (`v5-parti4.v3`+, `v5-parti7.v4`+) düzeltmeyi **zaten yapmış**.

➡️ **Gerçek bulgu daha küçük ama gerçek:** kapı yeni bir kusur değil, **düzeltmenin geriye taşınmadığı eski kopyaları** buldu. Aynı kaydın depoda hem kusurlu hem düzeltilmiş hâli duruyor ve **hangisini okuduğun dosyaya bağlı**.

⭐ Bu yüzden onarım metni **uydurulmadı**: kanonik hâl ana hat derleme girdisinden birebir taşındı.

## Tazelenen satırlar

| dosya | id | eski ilk satır |
|---|---|---|
| `v5-parti4.blok2.jsonl` | `40a4d66151` | Bahane sözcüğünü sen seçtin. "İş çıkışı" dediğin şeye hafta … |
| `v5-parti4.jsonl` | `40a4d66151` | Bahane sözcüğünü sen seçtin. "İş çıkışı" dediğin şeye hafta … |
| `v5-parti4.v2.arinmis.jsonl` | `40a4d66151` | Bahane sözcüğünü sen seçtin. "İş çıkışı" dediğin şeye hafta … |
| `v5-parti4.v2.jsonl` | `40a4d66151` | Bahane sözcüğünü sen seçtin. "İş çıkışı" dediğin şeye hafta … |
| `v5-parti7.arinmis.jsonl` | `3f37970550` | Doktorun söylemiş, sen yatamam diyorsun. İkisi de duruyor.… |
| `v5-parti7.blok2.jsonl` | `3f37970550` | Doktorun söylemiş, sen yatamam diyorsun. İkisi de duruyor.… |
| `v5-parti7.jsonl` | `3f37970550` | Doktorun söylemiş, sen yatamam diyorsun. İkisi de duruyor.… |
| `v5-parti7.v3.jsonl` | `3f37970550` | Doktorun söylemiş, sen yatamam diyorsun. İkisi de duruyor.… |
| `v5-parti4.arinmis.v9.jsonl` | `40a4d66151` | Bahane sözcüğünü sen seçtin. "İş çıkışı" dediğin şeye hafta … |
| `v5-parti7.arinmis.v9.jsonl` | `3f37970550` | Doktorun söylemiş, sen yatamam diyorsun. İkisi de duruyor.… |

## Kapı artık ne tutuyor

⭐ Taranan dosyalarda **hiçbir satır** tutulmuyor.

## ⛔ Bunun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Yargı eski metne ait** | tazelenen satırların `judge` alanına `_metin_tazelendi` işareti kondu; yargı **silinmedi** çünkü `judge: null` kaydı derlemeden eler (T121). Ama not: kanonik metin **zaten ana hatta yargılanmış** metindir ⇒ `v0.0.18` girdisindeki yargı ona aittir |
| ⛔ **`datasets/` dokunulmadı** | Kural 7 — ve zaten temizdi |
| ⛔ **Kapı dar** | `yansitma_ok` yalnız alıntıyla atfa bakar (kesinlik %100, duyarlılık %1) ⇒ eski kopyalarda **alıntısız** parafraz uydurması olabilir, bu tarama onu göstermez |
| ⛔ **Eski kopyalar neden duruyor** | `data/candidates/` altında aynı kaydın parti sürümleri yan yana duruyor ve hangisinin güncel olduğunu söyleyen bir alan **yok**. Bu tazeleme o sorunu **çözmez**, yalnız bir örneğini kapatır |
