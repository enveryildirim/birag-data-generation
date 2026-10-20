# Ölçek-5k — yükselen kalıplar ve kriz yönlendirmesi (v0.1.1 kıyaslı)

- Betik: `scripts/analiz/2026-10-20-olcek5k-kalip-kriz.py` · tarih 2026-10-20
- Koşu durumu (betik çalıştığında): ölçek-5k A 75/200 parça (1875 kayıt) · C 0/200 parça (0 kayıt)
- Kalıplar `2026-10-20-taban-vs-ince-basit-inceleme.py` ile aynı, tr_sadelestir edilmiş metinde; sayım asistan TURU başına.
- Risk sinyali: `KRIZ_ANAHTAR` ∪ `DOLAYLI` (üretim süzgeçleri, elle yazılmış ⇒ ALT SINIR).
- Girdiler (SHA256-16):

  - `datasets/v0.1.1/train.jsonl` `f8fcaa1e96603cb2`
  - `data/candidates/haiku-pilot.blok1.jsonl` `6cd4ace9ab8ca855`
  - `data/candidates/haiku-pilot.blok2.jsonl` `793a2cf9c3c097e0`
  - `data/candidates/haiku-pilot.blok3.jsonl` `6871caf6e19b3082`
  - `data/candidates/olcek5k-kalibrasyon/kayit/parca001.B.jsonl` `bc3449af3ebba630`
  - `data/candidates/olcek5k-kalibrasyon/kayit/parca002.B.jsonl` `00b9ab5a84717635`
  - `data/candidates/olcek5k-kalibrasyon/kayit/parca001.C.jsonl` `4ac9bfd9e48e08e0`
  - `data/candidates/olcek5k-kalibrasyon/kayit/parca002.C.jsonl` `1658a1b5994dc03e`
  - `data/candidates/olcek5k/A/parca001.jsonl` `62fe2e7b2cd08aa1`
  - `data/candidates/olcek5k/A/parca002.jsonl` `ac60e72e4698e6db`
  - `data/candidates/olcek5k/A/parca003.jsonl` `265dd15a7dde520b`
  - `data/candidates/olcek5k/A/parca004.jsonl` `546e7ed16073812d`
  - `data/candidates/olcek5k/A/parca005.jsonl` `92bbd5a6f67d40cc`
  - `data/candidates/olcek5k/A/parca006.jsonl` `365d0d7d351c108d`
  - `data/candidates/olcek5k/A/parca007.jsonl` `75785fd78796e254`
  - `data/candidates/olcek5k/A/parca008.jsonl` `9224d615e67db210`
  - `data/candidates/olcek5k/A/parca009.jsonl` `1870b8bd257ee11b`
  - `data/candidates/olcek5k/A/parca010.jsonl` `c080268dd091c316`
  - `data/candidates/olcek5k/A/parca011.jsonl` `1094a4e963169303`
  - `data/candidates/olcek5k/A/parca012.jsonl` `ff4a19ca1faa400b`
  - `data/candidates/olcek5k/A/parca013.jsonl` `17ee9c3ca5a6682f`
  - `data/candidates/olcek5k/A/parca014.jsonl` `76848b80272956ea`
  - `data/candidates/olcek5k/A/parca015.jsonl` `cf80881b87c821b1`
  - `data/candidates/olcek5k/A/parca016.jsonl` `9060fb693e3f8191`
  - `data/candidates/olcek5k/A/parca017.jsonl` `5f31413c73018a05`
  - `data/candidates/olcek5k/A/parca018.jsonl` `7cb1c466333c5bf6`
  - `data/candidates/olcek5k/A/parca019.jsonl` `849e47624e590c23`
  - `data/candidates/olcek5k/A/parca020.jsonl` `360311d9c4ef9f71`
  - `data/candidates/olcek5k/A/parca021.jsonl` `437b718ddab80378`
  - `data/candidates/olcek5k/A/parca022.jsonl` `78c3fd9b68a108f7`
  - `data/candidates/olcek5k/A/parca023.jsonl` `e88408c3761977a9`
  - `data/candidates/olcek5k/A/parca024.jsonl` `3745419a183310db`
  - `data/candidates/olcek5k/A/parca025.jsonl` `b4fa8e30a5f13aa8`
  - `data/candidates/olcek5k/A/parca026.jsonl` `53b6ea9744f805a1`
  - `data/candidates/olcek5k/A/parca027.jsonl` `f77b7e50c367331f`
  - `data/candidates/olcek5k/A/parca028.jsonl` `053f273182f30ecd`
  - `data/candidates/olcek5k/A/parca029.jsonl` `9344623ffe4e06aa`
  - `data/candidates/olcek5k/A/parca030.jsonl` `82b87133585dbd43`
  - `data/candidates/olcek5k/A/parca031.jsonl` `befd2fcc65ae9b53`
  - `data/candidates/olcek5k/A/parca032.jsonl` `2a2f1d6a97d5234f`
  - `data/candidates/olcek5k/A/parca033.jsonl` `648691f2ef86a027`
  - `data/candidates/olcek5k/A/parca034.jsonl` `de1a8e3e66d4d8bf`
  - `data/candidates/olcek5k/A/parca035.jsonl` `1ee842e763cbe1f6`
  - `data/candidates/olcek5k/A/parca036.jsonl` `0ba09b2293a2b266`
  - `data/candidates/olcek5k/A/parca037.jsonl` `8dbd2f4178c83ae0`
  - `data/candidates/olcek5k/A/parca038.jsonl` `b98ebeabcf8bd22f`
  - `data/candidates/olcek5k/A/parca039.jsonl` `5e5136f722cdcdc1`
  - `data/candidates/olcek5k/A/parca040.jsonl` `a3131a6ef0f0a7de`
  - `data/candidates/olcek5k/A/parca041.jsonl` `bd6d5907329f712e`
  - `data/candidates/olcek5k/A/parca042.jsonl` `10b3a1ee9e7a4dc5`
  - `data/candidates/olcek5k/A/parca043.jsonl` `6cb2b31fdcbe73a9`
  - `data/candidates/olcek5k/A/parca044.jsonl` `c84f470bf174b9ac`
  - `data/candidates/olcek5k/A/parca045.jsonl` `23db01276a023856`
  - `data/candidates/olcek5k/A/parca046.jsonl` `b6a664e3395cca56`
  - `data/candidates/olcek5k/A/parca047.jsonl` `d49a2787c6f5f851`
  - `data/candidates/olcek5k/A/parca048.jsonl` `fb24b0fd4e966c24`
  - `data/candidates/olcek5k/A/parca049.jsonl` `268839a3d78c25cf`
  - `data/candidates/olcek5k/A/parca050.jsonl` `8e13857fb51299e6`
  - `data/candidates/olcek5k/A/parca051.jsonl` `89f144429a35fff5`
  - `data/candidates/olcek5k/A/parca052.jsonl` `f685f27d4b3a12fd`
  - `data/candidates/olcek5k/A/parca053.jsonl` `91f75fb150838f1f`
  - `data/candidates/olcek5k/A/parca054.jsonl` `ed34b7d4bd77f2a4`
  - `data/candidates/olcek5k/A/parca055.jsonl` `f82d52a6a27cbd1d`
  - `data/candidates/olcek5k/A/parca056.jsonl` `21928674646a18a4`
  - `data/candidates/olcek5k/A/parca057.jsonl` `fdf0f58c0b1eaf69`
  - `data/candidates/olcek5k/A/parca058.jsonl` `02da5dd3de06e9fc`
  - `data/candidates/olcek5k/A/parca059.jsonl` `3de02d9558842a99`
  - `data/candidates/olcek5k/A/parca060.jsonl` `41add90259d76baf`
  - `data/candidates/olcek5k/A/parca061.jsonl` `99d622c8a367eb77`
  - `data/candidates/olcek5k/A/parca062.jsonl` `4256b9952af256ef`
  - `data/candidates/olcek5k/A/parca063.jsonl` `bfc0b1561c307928`
  - `data/candidates/olcek5k/A/parca064.jsonl` `a800ad7f661f8c0a`
  - `data/candidates/olcek5k/A/parca065.jsonl` `3ebe896b374e368b`
  - `data/candidates/olcek5k/A/parca066.jsonl` `41d4ee208fd29cfe`
  - `data/candidates/olcek5k/A/parca067.jsonl` `e89ffecfc3f6ec8e`
  - `data/candidates/olcek5k/A/parca068.jsonl` `db53cb3cf0fd3c30`
  - `data/candidates/olcek5k/A/parca069.jsonl` `6e626e4d5a209d2d`
  - `data/candidates/olcek5k/A/parca070.jsonl` `0c0e0adface37be5`
  - `data/candidates/olcek5k/A/parca071.jsonl` `679fd70b5852ea90`
  - `data/candidates/olcek5k/A/parca072.jsonl` `9f2a93eb97950ee0`
  - `data/candidates/olcek5k/A/parca073.jsonl` `a3b115c2bdf8e046`
  - `data/candidates/olcek5k/A/parca074.jsonl` `e7820cf71e98b154`
  - `data/candidates/olcek5k/A/parca075.jsonl` `ddadd95569003a77`
  - `data/plan/olcek5k.jsonl` `922926a97588363c`
  - `birag-degerlendirme/ince/cok_turlu.jsonl` `762b5aa76bbbaeba`
  - `birag-degerlendirme/ince/context_fidelity.jsonl` `8a74a742c15b9c55`
  - `birag-degerlendirme/ince/context_fidelity.ortusmez.jsonl` `a8653aa266b6a387`
  - `birag-degerlendirme/ince/context_fidelity.real.jsonl` `0114cd1285ad7b2f`
  - `birag-degerlendirme/ince/forgetting_smoke.jsonl` `b728806bf9dff4d7`
  - `birag-degerlendirme/ince/golden.dev.jsonl` `5661f7895eb832ad`
  - `birag-degerlendirme/ince/golden.test.jsonl` `b4b8173c571c68db`
  - `birag-degerlendirme/ince/safety_crisis.jsonl` `e81b3c57951b512e`
  - `birag-degerlendirme/ince/sycophancy.jsonl` `4248a7bf0c4029e7`

## 1. Asistan turlarında kalıp oranları

| kaynak | asistan turu | «…yazdın / söyledin / dedin» | «söyleyemem / bilemem / bilmiyorum» | «katılmıyorum» | «benim işim değil» | soruyla biten | acil hat/servis (adet) | profesyonele işaret |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| v0.1.1 | 1654 | %21.4 | %19.2 | %5.7 | %1.9 | %54.7 | 10 | %12.3 |
| Haiku pilotu (son) | 78 | %6.4 | %19.2 | %0.0 | %0.0 | %38.5 | 2 | %20.5 |
| kalibrasyon B (Haiku) | 72 | %0.0 | %15.3 | %0.0 | %0.0 | %70.8 | 0 | %26.4 |
| kalibrasyon C (Sonnet sonrası) | 71 | %0.0 | %19.7 | %0.0 | %0.0 | %73.2 | 0 | %28.2 |
| ölçek-5k C | 0 | — | — | — | — | — | — | — |
| başvuru: ince model çıktısı | 226 | %34.1 | %30.1 | %4.4 | %8.0 | %44.7 | 3 | %9.7 |

Acil = `\b112\b|\b182\b|\b183\b|kriz hatt|kriz merkez|acil serv` · profesyonel = `hekim|doktor|uzman|profesyonel|amatem|cematem|hastane|psikiyatr`.
⚠️ Elle okundu (2026-10-20): v0.1.1'deki 10 ve Haiku pilotundaki 2 «acil» eşleşmesinin hepsi bedensel aciliyet için «acil servis» (randevu beklemeden bakılacak yer); intihar/kendine zarar bağlamında acil yönlendirme yok.

## 2. Kriz kapsamı

- Plan (`data/plan/olcek5k.jsonl`, 5000 satır) tohum senaryoları: ambivalans 1915 · belirsiz 1213 · rol_siniri 1070 · nazikce_karsi_cikma 731 · inkar 48 · discord 23
- Plan tohum metinlerinde risk sinyali: 0 (plan betiği kriz tohumlarını ve iki süzgeçten birine takılanları eliyor)
- `is_crisis` doğru olan kayıt: v0.1.1 0 · Haiku pilotu (son) 0 · kalibrasyon B (Haiku) 0 · kalibrasyon C (Sonnet sonrası) 0

## 3. Kullanıcı turunda risk sinyali → sonraki asistan turu

| kaynak | kayıt | risk sinyalli kullanıcı turu | ardından asistan turu olan | acil yönlendirme | profesyonele işaret |
|---|---:|---:|---:|---:|---:|
| v0.1.1 | 1058 | 0 | 0 | 0 | 0 |
| Haiku pilotu (son) | 55 | 0 | 0 | 0 | 0 |
| kalibrasyon B (Haiku) | 50 | 0 | 0 | 0 | 0 |
| kalibrasyon C (Sonnet sonrası) | 49 | 0 | 0 | 0 | 0 |
| ölçek-5k A (yalnız kullanıcı tarafı) | 1875 | 0 | 0 | 0 | 0 |

Örnekler (kaynak başına en çok 12):

| kaynak | kayıt | kullanıcı turu | sonraki asistan turu |
|---|---|---|---|
