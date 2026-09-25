# İnceleme kuyruğu — kapıların konuşup da kimsenin dinlemediği yer

**Betik:** `scripts/analiz/2026-09-18-inceleme-kuyrugu.py` (yazıldı 2026-09-18) · **koşu tarihi:** 2026-09-19  
**Girdi:** `datasets/v0.0.9/train.jsonl` · SHA256-16 `667ec2c580cb7b59` · **571** kayıt

⛔⛔ **`checks.py` birkaç sinyali bilerek sert kapı yapmıyor** ve her birinin yanında
aynı cümle yazılı: *«inceleme kuyruğuna gider»*. Ama kuyruğu **okuyan bir şey**
**yoktu**; en eskisi **2026-09-12**'den beri bekliyor.

➡️⭐⭐ *Okunmayan bir sinyal, sinyal değildir. Bir kapıyı «rapor eden» yapmak, onu
susturmakla aynı şeydir — kuyruğu okuyan bir şey yazılmadıkça.*

## Özet — **16 vuruş / 16 kayıt**

| sinyal | vuruş | ⛔ asistanın kendi cümlesi | ne için kuyrukta |
|---|---:|---:|---|
| `klinik_ad_izi` | **6** | 0 | T150: bir ad iddia değildir; iddia yüklem gerektirir |
| `yansitma_soru_orani` | **4** | 0 | K40: 20 kayıtlık ilk üretimde 17'si YALNIZ bunun yüzünden elenmişti · ⚠️ 1 kapsam dışı |
| `rol_siniri` | **3** | 0 | *«ben teşhis koyamam», «doz öneremem»* — model DOĞRU reddederken de geçer |
| `sayi_adayi` | **2** | 1 | *«yıl gibi yanlış pozitifler olabilir»* (`checks.py:100`) |
| `zararli_normallestirme` | **1** | 0 | zararlı normalleştirme — aktarım ile onay ayrılmalı |

⭐ *«Asistanın kendi cümlesi»* sütunu ayrı duruyor çünkü bu oturumun
tekrarlanan dersi: bir ifade **kullanıcının sözünü aktarırken** de geçebilir ve
o zaman ihlal değildir (T62 aynalama). Kuyruğu okurken önce o sütuna bakılır.

## `klinik_ad_izi` (6)

| kayıt | öge | cümle | yer |
|---|---|---|---|
| `c977b4d0ea` | `tanI` | Programa katılmak için konulmuş bir tanı aranmaz; başvuru kişinin kendi isteğiyle yapılır. Program sekiz haftalık görüşmelerden ol | bağlam pasajı · `dijital iyi oluş programı tanıtım metni` |
| `f795a1bc8b` | `tedavI` | Gündüz tedavi ünitelerinde geceleme yapılmaz; ünite kapanış saatinde kapanır. Yatışlı servislerde refakatçi kalabilir ve refakatçi | bağlam pasajı · `hastane refakatçi düzeni metni` |
| `02e4d2e3d8` | `tanI` | Araç bir tarama aracıdır ve tanı koymaz. Sonuç, kişinin son on iki aya ilişkin kendi yanıtlarından üretilir. Yanıtlar oturum kapan | bağlam pasajı · `öz değerlendirme aracı kullanım notu` |
| `27e8728cd5` | `tanI` | Araç tanı koymaz; sonuç kişinin kendi yanıtlarından üretilir. Yanıtlar kaydedilmez ve üçüncü kişilerle paylaşılmaz. | bağlam pasajı · `çevrim içi öz değerlendirme aracı kullanım notu` |
| `f91237779b` | `tanI` | Araç tanı koymaz. Sonuç kişinin son on iki aya ilişkin kendi yanıtlarından üretilir ve yalnızca kişinin kendisine gösterilir. | bağlam pasajı · `öz değerlendirme aracı kullanım notu` |
| `182a334d93` | `Ilaçlar` | Nöbetçi eczaneler gece boyunca açıktır. Reçeteli ilaçlar için reçete aranır; reçetesiz danışma için bir belge gerekmez. | bağlam pasajı · `nöbetçi eczane hizmet notu` |

## `yansitma_soru_orani` (4)

| kayıt | öge | cümle | yer |
|---|---|---|---|
| `0d95d9459f` | `oran 1.0` | İstediğin şey hesap değilmiş, bir cümleymiş: güvendiğini duymak.  O cümleyi duymanı yakınlaştıracak ilk şey ne olurdu? | — |
| `c978e37621` | `oran 1.0` | Yıllardır bilen tek kişi sensin ve bu hafta ilk kez birinin görebileceğini düşündün.  Görülmek neden şimdi ağırlaştı? | — |
| `0709175b76` | `oran 0.0` | Aldığınız eğitimden ne kadar memnunsunuz? | ⚠️ **replay — persona kapıları kapsam dışı** |
| `c1b1687028` | `oran 1.0` | "Çıkış göremiyorum" dedin ve bunu hafife almayacağım.  Şunu doğrudan sormam gerekiyor: kendine zarar vermeyi düşündüğün bir an old | — |

## `rol_siniri` (3)

| kayıt | öge | cümle | yer |
|---|---|---|---|
| `fb634d744d` | `doz` | Bunu bilmesi gereken kişi, dozu azaltan hekim. | ⚠️ **kullanıcı da yazmış** |
| `dcbfd63a3e` | `doz` | Dozun yüksek olup olmadığını, başka bir şeyle etkileşip etkileşmediğini ben söyleyemem. | ⚠️ **kullanıcı da yazmış** |
| `16550563dc` | `doz` | Ama şunu söyleyeceğim: dozu kendin artırmış olabileceğini yazdın. | ⚠️ **kullanıcı da yazmış** |

## `sayi_adayi` (2)

| kayıt | öge | cümle | yer |
|---|---|---|---|
| `08f589bc4c` | `1919` | Versailles Antlaşması, Birinci Dünya Savaşı'nın sonunda 1919'da imzalandı ve İkinci Dünya Savaşı'nın önemli bir nedeni olarak görü | ⛔ asistanın kendi cümlesi |
| `d83c64b236` | `6900` | The AMD Radeon RX 6900XTX has 80 compute units (CUs). | ⚠️ **kullanıcı da yazmış** |

## `zararli_normallestirme` (1)

| kayıt | öge | cümle | yer |
|---|---|---|---|
| `43e6092f6a` | `herkes yapıyor` | Ama "herkes yapıyor" cümlesini bir kenara koyuyorum: kaç kişinin ne yaptığı, senin ne kadar içtiğin hakkında bir şey söylemiyor. | ⚠️ **kullanıcı da yazmış** · ⚠️ **tırnak içinde** |

## ⭐ Elle okuma kararları (2026-09-18, `v0.0.9`)

⭐ **On altı vuruşun on altısı da belgelenmiş yanlış pozitif sınıflarından;**
kuyrukta **gerçek ihlal yok**. Ama kuyruk yine de işe yaradı: okunur okunmaz
üretim filtresinde bir kusur ortaya çıkardı (aşağıya bakınız).

| sinyal | karar |
|---|---|
| `klinik_ad_izi` (6) | ✅ altısı da yordam/uygunluk/gizlilik cümlesi — üçü tam tersini söylüyor: *«Araç tanı koymaz»* (T150) |
| `yansitma_soru_orani` (4) | ✅ ikisi K40'ın tarif ettiği doğru MI kalıbı (bileşik yansıtma + tek soru), biri kriz sondası (*«kendine zarar vermeyi düşündüğün bir an oldu mu»* — doğrudan sorulması GEREKEN), biri replay ⇒ kapsam dışı |
| `rol_siniri` (3) | ✅ üçü de *«doz»*; ikisi doğru reddin içinde (*«ben söyleyemem»*), biri kullanıcının kendi sözünün yansıtması |
| `sayi_adayi` (2) | ✅ ikisi de replay: *«Versailles… 1919»* ve *«RX 6900XTX»* |
| `zararli_normallestirme` (1) | ✅ *«herkes yapıyor»* tırnak içinde ve açıkça REDDEDİLİYOR: *«…cümlesini bir kenara koyuyorum»* |

### ⛔⛔ Kuyruk okunur okunmaz bir üretim kusuru buldu

`bos_guvence` altındaki tek satır bir boş güvence **değildi**: *«…sayıyı yine de
merak ETMEK bunları geçersiz kılmıyor»*. Düz alt dizge araması, *«merak etme»*
olumsuz emrini *«merak etmek»* mastarının içinde buluyordu. Bütün korpuslarda
bu kategorinin **16 vuruşunun 16'sı** aynı kusurdandı ⇒ düzeltildi
(`2026-09-18-yasak-ifade-eki.md`), kategori **16 → 0**.

➡️⭐⭐ *Kuyruğun değeri içindekiler değildi — okunması oldu. Bir sinyali okumak,
sinyali üreten aracı da denetlemektir.*

## ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔ **Karar vermiyor** | her satır ELLE okunmalı; betik yalnız listeyi üretir |
| ⛔ **Sözlüğe bağlı** | yumuşak kategoriler `configs/filters.yaml`'daki ifade listesinden geliyor ⇒ listede olmayan bir ihlal kuyruğa da girmez |
| ⚠️ **«Kullanıcı da yazmış» muaf DEĞİL** | aynalamak meşru olabilir ama ONAYLAMAK değildir; sütun bir muafiyet değil, okuma sırası |
| ⛔ **Tek set** | varsayılan olarak yalnız en yeni sürüm okunuyor |
