# Üretim kapısının muafiyetleri — `run_checks` neyi bağışlıyor?

**Betik:** `scripts/analiz/2026-09-18-uretim-kapisi-muafiyetleri.py` · **Tarih:** 2026-09-18

⛔⛔ **Bu kapı ötekilerden başka.** T141/T144'te sayılan sekiz kapı ANALİZ aracı:
bulgu üretir, kimseyi elemezler. `run_checks` ise `build.py`'nin elemesini
belirler ⇒ **`datasets/` içine neyin gireceğine o karar veriyor.**

⭐⭐ **Yöntem:** muafiyetin bedeli için ikinci bir karar kuralı YAZILMADI (K97).
Kaydın kopyasında muafiyetin koşulu çevrildi ve `run_checks` **olduğu gibi**
yeniden çağrıldı. ➡️ *Bir muafiyetin bedeli, kuralı yeniden yazarak değil,
koşulu çevirip aynı kuralı yeniden koşarak ölçülür.*

⭐ Yayımlanmış setler zaten kapıdan geçmiş kayıtlardan oluşuyor ⇒ **net bağış**,
*«bu sette olup da muafiyet olmasa OLMAYACAK kayıt»* sayısıdır.

## 1. ⭐ Toplam

| muafiyet | kapsamdaki kayıt | net bağış (ham) | ⛔ **net (tekil kayıt)** | ne için |
|---|---:|---:|---:|---|
| `replay_persona_muafiyeti` | 216 | 12 | **1** | §9 çeşitlilik: replay dilimine MI/persona kapıları uygulanmaz (kısa yanıt, farklı prompt, İngilizce tasarım gereği) |
| `uretim_v2_baglam_muafiyeti` | 4848 | 9 | **9** | §7b kapısı 2026-09-14'te yazıldı; `expert-70` (uretim-v2) ondan önce üretildi ve geriye dönük düzeltilmiyor (SHA256 üç raporda kayıtlı) |

⛔ **Ham sayı sürüm sayısınca şişer:** aynı kayıt `v5-parti5.jsonl`, `.v3`, `.v4`, `.v5`, `.arinmis`, `.blok1` dosyalarının hepsinde duruyor. ➡️ *Bir korpusta «kaç kayıt» sorusunun cevabı dosya satırlarını toplamak değildir.* ⇒ Karar için okunacak sütun **tekil kayıt**.

⚠️ *«Net bağış»* **kusur sayısı değildir**: muafiyetlerin ikisi de ilan
edilmiş ve gerekçeli. Ölçülen şey, gerekçenin **bedeli** — o gerekçe olmasa
veri setinde olmayacak kayıt sayısı.

## 2. Dosya dosya

| dosya | SHA256-16 | kayıt | geçen | replay muaf (net) | v2 muaf (net) |
|---|---|---:|---:|---:|---:|
| `data/candidates/expert-70.jsonl` | `ee61043de8d38187` | 70 | 68 | 0 (0) | 68 (9) |
| `data/candidates/replay-v1.jsonl` | `d543e8c66edbb855` | 18 | 18 | 18 (1) | 18 (0) |
| `data/candidates/v0.0.1.jsonl` | `416cb3499e007843` | 20 | 20 | 0 (0) | 20 (0) |
| `data/candidates/v0.0.4-doz10.jsonl` | `d0159f7b014f8ef4` | 155 | 155 | 18 (1) | 56 (0) |
| `data/candidates/v0.0.5-doz25.jsonl` | `f36387f857f43b78` | 155 | 155 | 18 (1) | 56 (0) |
| `data/candidates/v4-parti1.jsonl` | `ea596190dd998935` | 40 | 40 | 0 (0) | 40 (0) |
| `data/candidates/v4-parti1.v8.jsonl` | `9bf6ea1e6bbaf4c4` | 40 | 40 | 0 (0) | 40 (0) |
| `data/candidates/v4-parti2.jsonl` | `4154385d9d39d244` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v4-parti2.v2.jsonl` | `2867eb01834e3e41` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v4-parti2.v3.jsonl` | `36c99c2aa3934c00` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti3.jsonl` | `746e25e983550681` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti3.v2.jsonl` | `18ab94595be21076` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti3.v3.jsonl` | `20d8fd0443be60bb` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti3.v4.jsonl` | `435f29c3d0a11a69` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti3.v5.jsonl` | `0843ed1d09fb5ccd` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti3.v6.jsonl` | `f872e29c59cc2703` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti3.v7.jsonl` | `f297eb548e3c7ce8` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti4.blok1.jsonl` | `ddfbcf1026c86232` | 15 | 15 | 0 (0) | 15 (0) |
| `data/candidates/v5-parti4.blok2.jsonl` | `f0578e7159830853` | 13 | 13 | 0 (0) | 13 (0) |
| `data/candidates/v5-parti4.blok3a.jsonl` | `e638c551c8bf078f` | 16 | 16 | 0 (0) | 16 (0) |
| `data/candidates/v5-parti4.blok3b.jsonl` | `32748645a141bc58` | 16 | 16 | 0 (0) | 16 (0) |
| `data/candidates/v5-parti4.jsonl` | `8f10f3414c02b5ef` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti4.v2.arinmis.jsonl` | `0384d3a7afc90df5` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti4.v2.jsonl` | `f9591e84aa45eeed` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti4.v3.jsonl` | `917a60679a47396e` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti4.v4.jsonl` | `09e1e240e4df79b6` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti4.v5.jsonl` | `92215eb54511b6aa` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti5.arinmis.jsonl` | `0d507c03920335bb` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti5.blok1.jsonl` | `3f7bdc0d9805f47e` | 15 | 15 | 0 (0) | 15 (0) |
| `data/candidates/v5-parti5.blok2.jsonl` | `7eb905497b0ef197` | 13 | 13 | 0 (0) | 13 (0) |
| `data/candidates/v5-parti5.blok3a.jsonl` | `7201490d44844ed0` | 16 | 16 | 0 (0) | 16 (0) |
| `data/candidates/v5-parti5.blok3b.jsonl` | `016ff90810fcc70d` | 16 | 16 | 0 (0) | 16 (0) |
| `data/candidates/v5-parti5.jsonl` | `8c5bf9a18982624a` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti5.v3.jsonl` | `88c3ca92e83b9524` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti5.v4.jsonl` | `a1751f2c595e6058` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti5.v5.jsonl` | `a1e0d9b9988b04d8` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti6.arinmis.jsonl` | `a22425efaede4f65` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti6.blok1.jsonl` | `f40bf648478c6a8b` | 15 | 15 | 0 (0) | 15 (0) |
| `data/candidates/v5-parti6.blok2.jsonl` | `b5000f918d9a1624` | 13 | 13 | 0 (0) | 13 (0) |
| `data/candidates/v5-parti6.blok3a.jsonl` | `bb13601a9444aa36` | 16 | 16 | 0 (0) | 16 (0) |
| `data/candidates/v5-parti6.blok3b.jsonl` | `397aa33260b4ef28` | 16 | 16 | 0 (0) | 16 (0) |
| `data/candidates/v5-parti6.jsonl` | `b8b351bfbada9e2b` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti6.v3.jsonl` | `ed9ece2dc20557e8` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti6.v4.jsonl` | `47daf856d6da4825` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti6.v5.jsonl` | `25acf8e97de4915d` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti6.v6.jsonl` | `e5dfcc5f0279e94c` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti7.arinmis.jsonl` | `4b9cccb2cd74b616` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti7.blok1.jsonl` | `2a3d3b69e7ede41b` | 15 | 15 | 0 (0) | 15 (0) |
| `data/candidates/v5-parti7.blok2.jsonl` | `eda07d9eba9f9ae8` | 14 | 14 | 0 (0) | 14 (0) |
| `data/candidates/v5-parti7.blok3a.jsonl` | `2042d74d7d4d4446` | 16 | 16 | 0 (0) | 16 (0) |
| `data/candidates/v5-parti7.blok3b.jsonl` | `30bbb9ac049e055d` | 15 | 15 | 0 (0) | 15 (0) |
| `data/candidates/v5-parti7.jsonl` | `317f23d17f855435` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti7.v3.jsonl` | `1888b35bf23b51c0` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti7.v4.jsonl` | `9583543b016daa88` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti7.v5.jsonl` | `008368c9eaa169de` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti7.v6.jsonl` | `d407c2be24702a9c` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti8.arinmis.jsonl` | `abf553ba7f938eba` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti8.blok1.jsonl` | `59976be748d09c31` | 15 | 15 | 0 (0) | 15 (0) |
| `data/candidates/v5-parti8.blok2.jsonl` | `9867870ddb5777bc` | 12 | 12 | 0 (0) | 12 (0) |
| `data/candidates/v5-parti8.blok3a.jsonl` | `07a4e722e2d1bb8b` | 17 | 17 | 0 (0) | 17 (0) |
| `data/candidates/v5-parti8.blok3b.jsonl` | `38795cd5f4da9514` | 16 | 16 | 0 (0) | 16 (0) |
| `data/candidates/v5-parti8.jsonl` | `ad4276805d3f07c3` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti8.v3.jsonl` | `b136c76562a9d18d` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti8.v4.jsonl` | `0699605a7a64d3c2` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti8.v5.jsonl` | `0fd9e2d13a2e70e4` | 60 | 60 | 0 (0) | 60 (0) |
| `data/candidates/v5-parti8.v6.jsonl` | `53160d3befe5e442` | 60 | 60 | 0 (0) | 60 (0) |
| `datasets/v0.0.1/train.jsonl` | `cff23210d80ebd81` | 20 | 20 | 0 (0) | 20 (0) |
| `datasets/v0.0.10/train.jsonl` | `0e196e88815defea` | 571 | 571 | 18 (1) | 472 (0) |
| `datasets/v0.0.2/train.jsonl` | `b78103aecb627e63` | 117 | 117 | 18 (1) | 18 (0) |
| `datasets/v0.0.3/train.jsonl` | `b50f7588e085f212` | 155 | 155 | 18 (1) | 56 (0) |
| `datasets/v0.0.4/train.jsonl` | `8c15ee2349e45124` | 155 | 155 | 18 (1) | 56 (0) |
| `datasets/v0.0.5/train.jsonl` | `d8e465c50bea4fca` | 155 | 155 | 18 (1) | 56 (0) |
| `datasets/v0.0.6/train.jsonl` | `20164ce4cbd853e8` | 214 | 214 | 18 (1) | 115 (0) |
| `datasets/v0.0.7/train.jsonl` | `f7b5f27fdc7e2c6a` | 272 | 272 | 18 (1) | 173 (0) |
| `datasets/v0.0.8/train.jsonl` | `5d605d7c7d7e9890` | 571 | 571 | 18 (1) | 472 (0) |
| `datasets/v0.0.9/train.jsonl` | `667ec2c580cb7b59` | 571 | 571 | 18 (1) | 472 (0) |

## 3. ⛔ Muafiyet olmasa ne düşerdi — örnekler

### `replay_persona_muafiyeti` — 12 kayıt

| kayıt | muafiyet olmasa düşme sebebi |
|---|---|
| `1a401482baca` | uzunluk (completion uzunluk 5 sınır dışı (10-2000)) |
| `1a401482baca` | uzunluk (completion uzunluk 5 sınır dışı (10-2000)) |
| `1a401482baca` | uzunluk (completion uzunluk 5 sınır dışı (10-2000)) |
| `1a401482baca` | uzunluk (completion uzunluk 5 sınır dışı (10-2000)) |
| `1a401482baca` | uzunluk (completion uzunluk 5 sınır dışı (10-2000)) |
| `1a401482baca` | uzunluk (completion uzunluk 5 sınır dışı (10-2000)) |
| `1a401482baca` | uzunluk (completion uzunluk 5 sınır dışı (10-2000)) |
| `1a401482baca` | uzunluk (completion uzunluk 5 sınır dışı (10-2000)) |
| `1a401482baca` | uzunluk (completion uzunluk 5 sınır dışı (10-2000)) |
| `1a401482baca` | uzunluk (completion uzunluk 5 sınır dışı (10-2000)) |
| `1a401482baca` | uzunluk (completion uzunluk 5 sınır dışı (10-2000)) |
| `1a401482baca` | uzunluk (completion uzunluk 5 sınır dışı (10-2000)) |

### `uretim_v2_baglam_muafiyeti` — 9 kayıt

| kayıt | muafiyet olmasa düşme sebebi |
|---|---|
| `b04849308b60` | uzunluk (None) · soru sayısı None · thinking dili None · bağlam (context[1] `sentetik` bayrağı yok (§7b-3)) · replay system prompt |
| `1df90d599761` | uzunluk (None) · soru sayısı None · thinking dili None · bağlam (context[1] `sentetik` bayrağı yok (§7b-3)) · replay system prompt |
| `4469c20d49de` | uzunluk (None) · soru sayısı None · thinking dili None · bağlam (context[1] `sentetik` bayrağı yok (§7b-3)) · replay system prompt |

## 4. ⛔⛔ SERT KAPI KENDİ KENDİNE KAPANMIŞTI — ve aynı gün düzeltildi

⭐ **Durum:** kusur bulundu, iki parçalı düzeltme yazıldı ve ölçüldü (`reports/analiz/2026-09-18-7b-kapi-duzeltmesi.md`): desen denkliği 25454/25454, regresyon 12/12, **kararı dönen kayıt 0**. Aşağıdaki anlatı kusurun BULUNDUĞU ândaki durumu tarif eder; tablodaki *«açık/kapalı»* sütunu ise kapının **şu anki** koşulunu `checks.uretim_surumu`'ye sorarak yazılır.

`run_checks` §7b'yi sert kapı yapan koşulu şöyle kuruyor:

```python
v3_ve_sonrasi = str(...prompt_version).startswith("uretim-v3")
```

⛔⛔ **Değişkenin adı `v3_ve_sonrasi`, yorumu *«uretim-v3 ve sonrası»*, ama kodu
yalnız v3'ü tutuyor.** Üretim v4'e, sonra v5'e geçince kapı **kendiliğinden
kapandı** ve bunu kimse görmedi: kapının kapanması bir hata vermez, yalnız
eleme yapmamaya başlar.

| prompt_version | kayıt | §7b sert kapı |
|---|---:|---|
| `uretim-v5` | 3589 | ✅ açık |
| `uretim-v3` | 1337 | ✅ açık |
| `uretim-v4` | 935 | ✅ açık |
| `—` | 242 | ⛔ kapalı |
| `uretim-v2` | 70 | ⛔ kapalı |
| `dikey-dilim-v1` | 40 | ⛔ kapalı |

➡️ Kusur bulunduğunda kapı **4876** kayıtta kapalıydı.

### ⭐⭐ Ama bedeli ölçülünce işaret TERS çıktı

v4/v5 adaylarında §7b-2'ye takılan **benzersiz pasaj: 6** — ve
**6'sı aynı cümlede olumsuzlama taşıyor**, yani feragat cümlesi:

| vuruş | cümle | feragat mi? |
|---|---|---|
| `tanı` | Programa katılmak için konulmuş bir tanı aranmaz; başvuru kişinin kendi isteğiyle yapılır. | ⭐ evet |
| `tedavi` | Gündüz tedavi ünitelerinde geceleme yapılmaz; ünite kapanış saatinde kapanır. | ⭐ evet |
| `tanı` | Araç bir tarama aracıdır ve tanı koymaz. | ⭐ evet |
| `tanı` | Araç tanı koymaz; sonuç kişinin kendi yanıtlarından üretilir. | ⭐ evet |
| `tanı` | Araç tanı koymaz. | ⭐ evet |
| `ilaçlar` | Reçeteli ilaçlar için reçete aranır; reçetesiz danışma için bir belge gerekmez. | ⭐ evet |

⭐⭐ **Gerçek ihlal: 0.** Kapı açık olsaydı bu pasajların hepsini elerdi — üçü tam tersini söylüyor: *«Araç tanı koymaz»*. ➡️⭐⭐⭐ *Hatalı kod, kazara doğru sonucu üretmiş: sürüm koşulu YANLIŞ ama kapının kendisi de yanlış olduğu için kapalı olması veriyi korudu. «Doğru sonuç, doğru kural demek değildir» bu kez ters yönden geçerli.*

⚠️ **İddia dar tutulmalı:** *«gerçek ihlal 0»* demek, **bu kelime tarayıcısının**
başka bir şey bulmadığı demektir. Kapı kapalıyken üretilen bir korpusta üretici
bu kuraldan geri bildirim de almadı ⇒ *«korpus §7b açısından temiz»* DEĞİL,
*«kapının kendi ölçütüyle görünen bir şey yok»*.

### ⭐ Önerilen düzeltme ÇİFT parçalı — tek parçası zarar verir

| parça | ölçülen etki |
|---|---|
| (a) sürüm koşulu *«v3 ve sonrası»* olsun | tek başına: 6 doğru kayıt **yanlışlıkla düşer**, 0 ihlal yakalanır |
| (b) `KLINIK_IDDIA` aynı cümledeki olumsuzlamayı görsün | 6/6 yanlış pozitif kalkar |
| (a) + (b) birlikte | kapı açılır, bilinen yanlış pozitif sınıfı kapanır, kayıp kayıt 0 |

⛔⛔ **Değişiklik YAPILMADI.** `src/checks.py` `build.py`'nin elemesini belirler ⇒
sert kapıyı açmak bir sonraki bütün derlemeleri etkiler ve (b) yeni bir sezgi
getirir; sezginin kendi regresyon sınaması yazılmadan üretime girmemeli.

## 5. ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔ **§7b kapısı 4070 kayıtta kapalıydı** | düzeltilmedi; çift parçalı öneri ölçüldü ve yazıldı (§4) |
| ⛔ **Yalnız iki muafiyet ölçüldü** | `run_checks` başka kararlar da veriyor (`rol_siniri` ve `yansitma_soru_orani` SERT KAPI DEĞİL, inceleme kuyruğuna gider) ⇒ bunlar bir muafiyet değil **tasarım**, ama bedelleri de ölçülmedi |
| ⛔ **`thinking_dili` None muafiyeti** | thinking'i olmayan kayıtta dil kapısı hiç çalışmıyor; koşulu çevirmek anlamsız (dil yok) ⇒ sayılmadı |
| ⚠️ **Koşul çevirmek yan etki yaratır** | `replay=False` yapmak `replay_ok`'u da etkiler; ölçülen şey *«BıRAG kaydı olsaydı geçer miydi»*, muafiyetin tek başına etkisi değil |
| ⭐ Hata yok | 0 kayıt `run_checks` sırasında hata verdi |
