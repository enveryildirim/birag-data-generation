# R1 — RAG soru envanteri: dış bilgi gerektiren sorular

**Betik:** `scripts/analiz/2026-09-15-rag-soru-envanteri.py` · **Tarih:** 2026-09-15

| girdi | dosya | SHA256 (ilk 16) | çıkarılan |
|---|---|---|---|
| tohum | `data/seeds.jsonl` | `0631c02ec7510af3` | 2240 tur · 1428 soru |
| korpus v3 | `data/candidates/v3-kumulatif.jsonl` | `5867e31fc49e3dbf` | 154 tur · 87 soru |
| korpus v4 | `data/candidates/v4-parti1.jsonl` | `ea596190dd998935` | 67 tur · 20 soru |
| uzman örneklemi | `data/candidates/expert-70.jsonl` | `ee61043de8d38187` | 84 tur · 31 soru |
| cetvel dev | `evals/golden.dev.jsonl` | `1396c6713e9b2b5d` | 62 tur · 44 soru |
| cetvel test | `evals/golden.test.jsonl` | `2608b58a989f9df1` | 68 tur · 32 soru |
| cetvel locked | `evals/golden.locked.jsonl` | `e8f330c4479d2a88` | 68 tur · 37 soru |
| eksen 4 bağlam | `evals/context_fidelity.jsonl` | `5ec01b50983bb397` | 20 tur · 22 soru |

---

## 1. Neden bu envanter

K73'ün hatası pasajları **soruya değil senaryoya** göre yazmaktı: dokuz pasajın
sekizinde pasajdan cevaba tek bir içerik sözcüğü geçmedi. Belge toplamaya
sorudan başlanmazsa aynı hata büyük ölçekte tekrarlanır.

## 2. İki elek

Taranan kullanıcı turu **2763** · çıkarılan soru cümlesi **1701**.

| elek | ne arıyor | eşleşme | eşsiz soru |
|---|---|---|---|
| **geniş** | kategori sözcüğü (jenerik dahil: *para, test, sıra, merkez*) | 115 | **104** |
| **dar** | kurum/mevzuat/yordam terimi **ve** cümlenin soru olması | 45 | **38** |

| kategori | geniş | dar |
|---|---|---|
| başvuru / erişim | 29 | 17 |
| gizlilik / kayıt | 16 | 4 |
| hukuki yordam | 8 | 6 |
| kurum haritası | 25 | 16 |
| uygunluk / hak | 37 | 2 |
| — eşleşmeyen — | 1590 | 1224 |

⚠️ **Geniş elek okunamaz durumda.** Örneklerine bakıldığında eşleşmelerin çoğu
yanlış pozitif: *"sıra sana mı gelsin"* (başvuru sırası değil, aile sitemi),
*"o parayı nereden bulayım"* (ücret sorusu değil), *"iyi anne mi olduğumu test
ediyormuş gibi"* (idrar testi değil). Türkçe serbest metinde tek sözcüklü kapı
yine tavana vurdu — bu desenin projede kaçıncı örneği olduğu `T22`'de izleniyor.
**Aşağıdaki okuma DAR elekten yapılıyor.**

## 3. Dar elek — örnekler

### başvuru / erişim (17)

- *Kampüsün psikolojik danışma merkezi var, randevu almayı düşünüyorum ama bunu hak edecek kadar 'ciddi' bir durumum var mı, bilmiyorum.* — `tohum`
- *Bu benim sosyalim, başka nereye gideceğim?* — `tohum`
- *Şimdi randevu alacağım ama bir taraftan da 'bunu kendim için mi yapıyorum yoksa boşanmamak için mi?' diye düşünüyorum.* — `tohum`
- *Aile hekimine gitmeyi düşündüm ama oraya 'içki yüzünden' diye nasıl giderim?* — `tohum`
- *Daha erken bir randevu için bir yol var mı, yoksa biz ailecek baba haplara ulaşmasın diye mi uğraşacağız?* — `tohum`
- *Orası uyuşturucu kullananların yeri değil mi, ben oraya nasıl giderim, mahallede duyulsa.* — `tohum`
- *Sabah kızım 'anne geriatri randevusu alalım mı' dedi, ben de 'al' dedim ama içim hâlâ ürperiyor.* — `tohum`
- *Sponsorum iki haftadır sessizdi, az önce yazdı: 'Buradayım, AMATEM randevusunu aldın mı?' diye.* — `tohum`

### gizlilik / kayıt (4)

- *Bir şey soracağım, siz aileme söylemezsiniz değil mi bunu?* — `tohum`
- *Söylemezsem rapordaki hatanın sebebi havada kalacak, söylersem dosyama işlenir mi bilmiyorum.* — `tohum`
- *Acaba bunu yazdığımda kayıt aileme gider mi, ya da KPSS sonrası işe girersem sicilime düşer mi.* — `tohum`
- *Acaba bunu yazdığımda kayıt aileme gider mi, ya da ileride işe girersem sicilime düşer mi?* — `uzman örneklemi`

### hukuki yordam (6)

- *Bu test pozitif çıkarsa işim de denetimli serbestlik dosyam da çok kötü etkilenir, anlıyor musun?* — `tohum`
- *Avukata gidilecek bir şey mi bu?* — `tohum`
- *Mahkeme bittiğinde içeri girer miyim bilmiyorum.* — `tohum`
- *Mahkemeye gidiyorum, buraya geliyorum, daha ne istiyor?* — `tohum`
- *İcra için avukatla yarın görüşme ayarladım, eşim 'gel ben de geleyim' dedi, kabul ettim ama her şeyi anlatacak mıyım bilmiyorum.* — `tohum`

### kurum haritası (16)

- *Aile hekimine gideyim mi acaba.* — `tohum`
- *Bir daha AMATEM'e gitsem yine boş çıkar mı?* — `tohum`
- *Bana AMATEM diyorlar, niye gideyim ki, kim için?* — `tohum`
- *Sen de mi başladın AMATEM AMATEM diye.* — `tohum`
- *Şimdi 112'yi mi arasam, sabah aile hekimine mi gitsem bilemedim, çocuklar uzakta.* — `tohum`
- *Aile hekimine gitmeyi düşündüm ama oraya 'içki yüzünden' diye nasıl giderim?* — `tohum`
- *Aklımdan geçen şey şu: aile hekimine gidip eski reçeteyi sadece birkaç gece için yenilesem ne olur?* — `tohum`
- *Aile hekimini arayıp tekrar yazdırsam mantıksız bir tercih mi sence?* — `tohum`

### uygunluk / hak (2)

- *Kurumsal sigortamız davranışsal sağlık notlarını görüyor mu, görmüyor mu hâlâ anlayamadım.* — `tohum`
- *Açık olursam sigortamın işten ayrılma ya da yenileme sürecinde kullanılır mı?* — `tohum`

## 4. Bulgu — korpusumuz bu soruları neredeyse hiç sormuyor

1701 soru cümlesinin **38**'i dış bilgi gerektiriyor.
Bu, K73'ün bağlam dilimi bulgusuyla aynı yöne işaret ediyor: dokuz bağlamlı
kaydın **altısında** *"kullanıcı zaten soru sormamış"*tı. Ayrıca `plan.md` §6
karışımın **%75'inin** doküman gerektirmediğini zaten söylüyor.

**Sonuç, toplama planını değiştiriyor:** hedef belge listesi korpusumuzdan
**türetilemez**, çünkü korpusumuz o soruları sormuyor. İki kaynağı ayırmak gerek:

| Ne | Nereden gelir | Durum |
|---|---|---|
| Kullanıcı **fiilen** ne soruyor | İP5 pilotu | ⛔ yok — gerçek kullanım verisi yok |
| Kullanıcı **ne sorabilir** | kurumsal harita (`arastirma-notlari` §K) | ✅ elimizde |

Yani R2 kaynak haritası **kapsam** üstüne kurulur (kurumun cevapladığı soru
kümesi), **talep** üstüne değil. Bu bir varsayımdır ve varsayım olduğu yazılı kalır.

## 5. Türkiye geçerlilik denetimi — aranacak belgesi OLMAYAN sorular

Hedef soru listesine giren her satır önce şu denetimden geçmeli: *bu sorunun
Türkiye'de kurumsal bir karşılığı var mı?* Yoksa belge aranmaz — doğru model
davranışı §7a'nın `yetersiz` dalıdır.

`data/seeds.jsonl` (2240 tohum) ABD sistemi çerçevesi için tarandı:

| işaret | tohum | örnek |
|---|---|---|
| AA sponsoru | **14** | …Bir terapistle görüşmeyi de düşünüyorum ama internette AA toplantılarına da baktım. Sadece 'benim durumum o kadar ağır değil, oraya gid… |
| EAP / çalışan destek | **1** | …Yarın kurumsal psikologla görüşeceğim, EAP üzerinden. Reçetemi söylesem mi söylemesem mi tam karar veremedim. Söylemezs… |
| işveren sigortası | **1** | …Bir saat sonra kurumsal psikologla görüşeceğim. Kurumsal sigortamız davranışsal sağlık notlarını görüyor mu, görmüyor mu hâlâ an… |

**16 eşleşme / 2240 tohum (%0.7).**
Dar bir artefakt — korpus geneli ABD çerçeveli DEĞİL. Ama dar elekten çıkan dört
`gizlilik/kayıt` sorusundan **biri** buradan geliyor (*"kurumsal sigortamız
davranışsal sağlık notlarını görüyor mu"*), yani hedef listesi denetimsiz
kullanılamaz. `docs/rag-kaynak-haritasi.md` §1'de S4 bu gerekçeyle elendi.

## 6. Sınırlar

1. **Anahtar kelime vekili** — kapı değil, envanter. Geniş/dar farkı yanlış
   pozitif payını görünür kılmak için basılıyor.
2. Dar elek **yanlış negatif** verir: soru ekisiz, terimsiz sorulan bilgi
   ihtiyacı (*"oraya gitsem ne olur"*) kaçar. Alt sınır ölçüyor, üst sınır değil.
3. ⛔ **Girdilerin tamamı sentetik.** Gerçek BıRAG kullanım verisi yok
   (`PROJECT_MEMORY.md` açık soru). Envanter *"kullanıcılar bunu soruyor"*u değil,
   ***"biz bunu soruyor varsaydık"***ı ölçer.
