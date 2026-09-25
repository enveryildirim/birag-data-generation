# 27 alıntısız *«aynı cümlede»* iddiası — elle okundu

**Betik:** `scripts/analiz/2026-09-18-ayni-cumlede-elle-okuma.py` · **Tarih:** 2026-09-18  
**Girdi:** `datasets/v0.0.9/train.jsonl` · SHA256-16 `667ec2c580cb7b59`

⛔⛔ **T140'ın açık kalemi kapandı — ve T140 haklı çıktı.** Yapısal atıf kapısı
yalnız **≥2 alıntı** taşıyan iddiaları otomatik sınayabiliyor; ötekiler *«elle
okunacak»* yığınına düşüyor ve o yığın hiç okunmamıştı.

| | |
|---|---:|
| kapının OTOMATİK sınadığı ihlal | **0** |
| elle okunacak iddia | **27** |
| ⛔ **elle okununca YANLIŞ çıkan** | **7** (%26) |

➡️⭐⭐ *Kapının otomatik sınayabildiği kısım temiz; kusurun tamamı kapının
ULAŞAMADIĞI yerde birikmiş. Bir kapının «0 ihlal» demesi, kapının BAKABİLDİĞİ
yerde 0 ihlal olduğu demektir.*

## 1. ⛔ Yanlış çıkan iddialar

Hepsi aynı biçimde yanlış: iddia *«aynı CÜMLEDE»* diyor, oysa iki öge
kullanıcının **aynı mesajındaki AYRI cümlelerinde** duruyor.

| # | iddia | neden yanlış |
|---:|---|---|
| 41 | Öğle arası çıkıp yaktığını da aynı cümlede söyledin. | *«İnhaleri aldım, kullanmayı da öğrendim.»* ve *«Ama öğle arası çıkıp yine yaktım.»* — **iki ayrı cümle** |
| 60 | Üst kattaki oğlundan da aynı cümlede söz ettin. | *«Ben de aynı koltuğa oturmuşum gibi hissettim.»* ve *«Üst katta oğlum uyuyor.»* — **iki ayrı cümle** |
| 23 | Kahvaltı etmediğini ve iki tane içtiğini aynı cümlede yazdın. | iki ayrı cümle ⛔ **ve ikinci kusur:** *«iki tane»* kullanıcının sözü değil, *«bir tane… sonra bir tane daha»*dan çıkarılmış bir SAYIM |
| 35 | Ama ikisini aynı cümlede tutabilmek zaten bir şey. | *«Hayatımın değişmesi gerektiğini biliyorum…»* ve *«Ama oyunu bırakmak istemiyorum…»* — **iki ayrı cümle** |
| 16 | İki şeyi aynı cümlede söyledin: hesabı yapmaya korkuyorsun ve onsuz yol gitmiyor. | *«…hesabını yapmaya bile korkuyorum.»* ve *«Ama bu kahve bu sigara olmadan da yol gitmiyor…»* — **iki ayrı cümle** |
| 20 | Bir şeye de katılmıyorum: "net kazanmışım" diyorsun ama aynı cümlede tam rakamı eşinin bilmediğini s | ⭐ *«…net kazanmışım.»* ve *«Bunu kimseye anlatmıyorum, eşim bile bilmiyor…»* — iki ayrı cümle. **Tek alıntı taşıdığı için kapı sınayamadı** |
| 27 | Üç haftadır uyuyamadığını da aynı cümlede söylüyorsun — yani dalmak çözülmüş, uyumak çözülmemiş. | *«son üç haftadır uyuyamıyorum.»* ve *«…gerçekten işe yarıyor.»* — **iki ayrı cümle** |

⭐ **Düzeltme mekanik ve aynı:** *«aynı cümlede»* → *«aynı mesajda»*. İki öge
gerçekten aynı mesajda; yanlış olan tek şey iddianın **düzeyi**.

⛔⛔ **Biri tam olarak daha önce iki kez düzeltilmiş kusur.** `#20`in iddiası bir
alıntı taşıyor (*«net kazanmışım»*) ama **tek** alıntı taşıdığı için kapı onu
sınayamadı; aynı kusur `v5-parti8 #13` ve `#15`te İKİ alıntılı olduğu için
yakalanmıştı. ➡️ *Kapının eşiği (≥2 alıntı) kusurun kendisiyle ilgisiz, yalnız
kapının GÖRME koşuluyla ilgili — ve kusur eşiğin altında da aynı sıklıkta var.*

## 2. ⭐ Doğru çıkan iddialar

**20** iddia doğrulandı; kullanıcının tek bir cümlesi iki ögeyi birden taşıyor. Örnekler:

| # | iddia | kullanıcının cümlesi |
|---:|---|---|
| 33 | Haklı olabileceklerini söylüyorsun ve aynı cümlede bunu kabul etmenin zor olduğu | *«ailem haklı olabilir oyun konusunda ama bunu kabul etmek çok zor.»* |
| 13 | Bırakamadığını da aynı cümlede söyledin. | *«Ama ağrım vardı, doktor verdi, ben de aldım.»* |
| 47 | İkisini aynı cümlede tutmuşsun, birini öbürüyle silmemişsin. | *«Kızıma yapıyorum bunu biliyorum ama elim gidiyor pakete.»* |
| 53 | Suçluluk ve kızgınlığı aynı cümlede söyledin. | *«Suçlu hissediyorum ama aynı zamanda çok da kızgınım.»* |
| 33 | İki şeyi aynı cümlede söyledin: alındığını ve onun abarttığını. | *«ailem haklı olabilir oyun konusunda ama bunu kabul etmek çok zor.»* |

## 3. ⭐ Şablon bağlantısı (T139)

T139: *«her yeni kural, bir sonraki şablonun tohumu»*. Bu kalıp da bir kuralın
(T104 yapısal atıf) ürünü — sürümler boyunca nasıl büyümüş:

⚠️ Sayım **yalnız asistan cevabında** — `thinking` ve `judge` alanları hariç.
⛔ İlk ölçümüm ham JSONL satırında aramıştı ve *«aynı cümlede»*yi 97 kayıtta
buluyordu; asistan cevabındaki gerçek sayı **çok daha az**. ➡️ *Bir JSONL satırı
metin değil KAYITTIR ve kaydın çoğu modele hiç gitmez.*

| sürüm | kayıt | *«aynı cümlede»* | *«aynı mesajda»* |
|---|---:|---:|---:|
| `v0.0.1` | 20 | 0 | 0 |
| `v0.0.2` | 117 | 1 | 0 |
| `v0.0.3` | 155 | 1 | 0 |
| `v0.0.4` | 155 | 1 | 0 |
| `v0.0.5` | 155 | 1 | 0 |
| `v0.0.6` | 214 | 5 | 0 |
| `v0.0.7` | 272 | 8 | 0 |
| `v0.0.8` | 571 | 31 | 11 |
| `v0.0.9` | 571 | 29 | 13 |

⚠️ *«aynı mesajda»* sayısının artışı T140'ın düzeltmelerinden geliyor — yani
kuralın kendisi de yeni bir kalıp doğuruyor. ⛔ Şablonlaşmayı yakalayan bir kapı
hâlâ yok (T139'un açık kalemi).

## ⛔ Bu okumanın söylemedikleri

| | |
|---|---|
| ⛔ **Düzeltme UYGULANMADI** | `datasets/v0.0.9` IMMUTABLE (Kural 4); yedi kayıt sette **duruyor** ve düzeltme bir sonraki derlemeye kalıyor |
| ⛔ **Kararlar elle verildi** (K30) | ölçüt yazılı — *«aynı cümlede»* diyen bir iddia için kullanıcının TEK cümlesi iki ögeyi taşımalı — ama hüküm benim |
| ⛔ **Yalnız bu set okundu** | aday dosyalardaki aynı kalıp taranmadı |
| ⚠️ **Kapı hâlâ ulaşamıyor** | ≥2 alıntı eşiği duruyor; bu okuma kapıyı güçlendirmedi, yalnız onun göremediği yeri bir kez okudu |
