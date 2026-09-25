# `thinking` ↔ `content` kapısı — ilk aile: «soru sormuyorum»

**Betik:** `scripts/analiz/2026-09-22-thinking-content-kapisi.py` · **Tarih:** 2026-09-22  
**Küme:** `datasets/v0.0.18/train.jsonl` (1033 kayıt)  

⛔⛔ **T239'un bıraktığı yüzey.** İç muhakeme de bir **beyandır** ve kaydın içinde durur; `beyan-metin-uyumu` yalnız `gen_meta` beyanlarını denetliyor, iç muhakemeyi **hiç okumuyor**.

⭐ **Desen ölçüldü, hayal edilmedi:** korpustaki 1015 iç muhakemede **2980 olumsuz ilan** var (169 fiil). En sık ve mekanik olarak en temiz denetlenebilir olanı `sormuyorum` (316).

## Ölçüm

| | |
|---|---:|
| iç muhakemede *«soru sormuyorum»* ilanı | **258** |
| ⛔ bunlardan cevabında **soru olan** | **0** |
| ihlal oranı | %0.0 |

⭐ **İhlal yok.** İlan edilen her kayıtta cevap gerçekten sorusuz.

⛔ Bu *«iç muhakeme hep tutarlı»* demek DEĞİLDİR: denetlenen tek aile bu ve 2980 ilanın yalnız bir kısmı.

## ⛔ Bu kapının söylemedikleri

| | |
|---|---|
| ⛔⛔ **ALT SINIR** | 2980 ilanın yalnız **bir ailesi** denetleniyor. *«Adını anmıyorum»*, *«önermiyorum»*, *«plan kurmuyorum»* gibi ilanların nesnesi **serbest metindir** ve mekanik olarak denetlenemiyor — T22 serisinin uyardığı sınır |
| ⛔ **T239'un kendi vakasını YAKALAMAZ** | `ad5658bc`'nin ilanı *«abartılı bir gizlilik vaadi vermiyorum»*; nesnesi bir kavram, dizge değil ⇒ bu kapı onu göremez. Onu **okuma** buldu |
| ⛔ **İlan ≠ niyet** | iç muhakeme de üretilmiş metindir; *«soru sormuyorum»* yazıp soru sormak bir **tutarsızlıktır**, ama hangisinin doğru davranış olduğunu bu kapı söylemez |
| ⛔⛔ **İLK SÜRÜM YANLIŞ POZİTİF ÜRETTİ** | desen `soru sormuyorum` idi ve *«İzin isterken **kapalı bir** soru sormuyorum»* içinde eşleşti — nitelikli bir ilanı mutlak sandı. O kayıt açık uçlu soru soruyor, yani **tutarlı**. ⭐ Okuma yakaladı, ölçüm değil (T260) |
| ⚠️ **İptal deseni dar** | ilanı geçersiz kılan çevre (*«…değil»*, *«ama»*) yalnız cümle sonunda aranıyor ⇒ yanlış pozitif hâlâ mümkün; ihlaller bu yüzden tek tek yazılı |
