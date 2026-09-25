# Üretim talimatı — v4

> **v3'ü süperse eder.** v3 silinmez: `data/candidates/v3-*.jsonl` ve
> `datasets/v0.0.2/`'nin nasıl üretildiğinin kaydıdır (Kural 7 ·
> `gen_meta.prompt_version: uretim-v3`).
>
> v4'ün kaynağı, v3'le üretilen 99 kaydın **kendi dağılım ölçümü**:
> `datasets/v0.0.2/CARD.md` · katkı defteri **T25**.

## 0. v3'ten ne değişti, neden

v3 iyi tuttu — **kotası olan yerlerde.** Aynı korpusta (n=99) ölçüldü:

| Eksen | Talimatta ne vardı | Gerçekleşen | Hedef |
|---|---|---|---|
| Konuşma durumu (§3b) | **yüzde kotası + zorunlu `gen_meta` alanı** | 33/21/16/15/9/5 | 35/20/15/15/10/5 ✅ |
| MI süreci (§5c) | **yüzde kotası + kayıtta alan** | 37/26/21/15 | 40/25/20/15 ✅ |
| Mesaj biçimi (§3a, K42) | yalnızca **tanım tablosu** — kota yok, alan yok | kısa **%7,7** · `bicim` alanı 99/99 **boş** | ~%40 ❌ |

**Okunan ders (T25):** bir tasarım kuralı *tanımlanmakla* uygulanmıyor. Uygulanması
için iki şey gerekiyor — **(1)** sayısal kota, **(2)** gerçekleşeni kaydeden bir alan,
yani üreticinin kendi kendini sayabilmesi. v3'ün §3a'sında ikisi de yoktu ve eksen
hedefin **beşte birinde** kaldı; kotası olan iki eksen ±3 puan içinde tuttu.

⚠️ Bu kontrollü bir deney değil: üç eksen aynı anda, tek koşuda gözlendi. v4 kotayı
ekliyor; **sonraki parti bu mekanizmanın sınamasıdır** — kısa açılış oranı hâlâ
%10'un altında kalırsa açıklama kota değildir.

| Değişiklik | Ölçülen sorun | Nerede |
|---|---|---|
| Mesaj biçimine **kota + zorunlu alan** | kısa açılış %7,7 (hedef ~%40) | §3a, §1 |
| Uzunluk bantları **düzeltildi** | v3'ün bantları (`orta` 15-40, `uzun` 40+) plan.md §6'nın ölçüm bantlarıyla (9-25, 26+) uyuşmuyordu; **9-14 kelime hiçbir banda düşmüyordu** | §3a |
| Kısa açılış ↔ çok turlu bağı yazıldı | plan.md §6'nın "çok turlu %15"i, "kısa açılış %40" hedefiyle aritmetik olarak tutarsız | §3c ⭐ YENİ |
| Judge rubrik göndermesi güncellendi | §9a hâlâ `judge-eksen1.v4.md` diyordu; geçerli sürüm **v7** (K100) | §9a |
| **Yönlendirme dilimi** ⭐ | Faz 4 taraması: beş kolun beşi Eksen 2'de elendi; korpus sınır çekmeyi 17 kez öğretiyor, yönlendirmeyi **0** kez | §8b ⭐ YENİ |

---

---

## 1. Kayıt iskeleti

`src/schemas.py::TrainRecord`. Mesaj dizisi: `system` → `user` → `assistant`
(`thinking` yalnızca son assistant mesajında). `age_group` **yalnızca** `yetiskin|ergen`.
`turn_type`: `single|multi`.

`gen_meta`: `{generator: claude-code, generator_model: claude-opus-5,
prompt_version: uretim-v4, date: <tarih>, system_prompt_variant: canon|paraphrase,
turn_ending: <§5a>, konusma_durumu: <§3b>, bicim: <§3a>, register: <§3a>,
sinir_tipi: <§8b>, tohum_havuzu: <§1a>, baglam_davranisi: <§1b, yalnız bağlamlı kayıtta>}`

### §1a — `tohum_havuzu` (2026-09-16, T88)

Tohumun hangi havuzdan geldiği **yazılır**: `seeds` (v1) ya da `seeds.v2`.

⛔ **Neden zorunlu.** `data/seeds.v2.jsonl` 80 kayıtta v1'den farklı
(`meta.egitim`: `belirtilmemis` → `ilkokul`, T77) ve `seed_id`'ler **aynı** —
yani iki havuzdan üretilmiş kayıtlar aynı sette yan yana durabilir ve
**hangisinden geldikleri kayıttan okunamaz**. ⇒ *Bir düzeltmenin veriye girip
girmediği, kaydın kendisinden okunabilmelidir; yoksa düzeltme ölçülemez.*

⚠️ **Hangi havuzun kullanılacağı ayrı bir karardır** ve bu alan onu vermez —
yalnızca **görünür** kılar. Karar verilene kadar iki havuz da kullanılabilir,
yeter ki beyan edilsin.

### §1b — `baglam_davranisi` (2026-09-16, T96)

Bağlam taşıyan kayıtlarda §7a'nın **hangi sınıfı** uygulandığı yazılır:
`cevap_var` | `cevap_yok` | `izin_iste` | `ilgisiz`. Yanına `baglam_bicimi`
(K17 varyantı) da yazılır.

⛔ **Neden.** §7a dört sınıfı **yüzde** olarak tanımlıyordu ama gerçekleşeni
kaydeden **alan yoktu** — T25'in tarif ettiği hatanın birebir aynısı (§3a'da
kota vardı, alan yoktu ve eksen hedefin beşte birinde kaldı). Dağılım beyan
edilmeden **ölçülemez**: hangi kaydın "bağlamdaki cevabı verdiği", hangisinin
"yok dediği" metinden alt-dizgeyle ayrılamaz.

⚠️ Beyan **kapı değil**, korpus düzeyi ölçüdür — `checks.py` göremez
(§1 ile aynı sınıf). Tutarlılığı `scripts/analiz/*-8b-denetimi.py` sınar:
`cevap_yok` beyan eden kayıt `is_negative` taşımalıdır (§7a'nın kendi şartı).

⚠️ **`turn_ending`, `konusma_durumu`, `bicim`, `register`, `sinir_tipi`, `tohum_havuzu` ve (bağlamlıysa) `baglam_davranisi` beyanı zorunludur.** v3'ün yeni hedefleri korpus
düzeyindedir; `checks.py` onları göremez (kayıt düzeyinde kapı değiller). Üretici hangi
hamleyi yaptığını beyan eder, `scripts/analiz/*-korpus-hedef-raporu.py` dağılımı ve
beyanın tutarlılığını denetler (§9a). Beyan yoksa hedef **ölçülemez**, tutmuş sayılmaz.

## 2. System prompt (K19)

Kayıtların **%75-80'i** kanonik metni birebir, **%20-25'i** anlamca eşdeğer parafraz.
Gerekçe: %100 aynı string olursa model davranışı o string'e kilitlenir.

⚠️ K19'un *"Bilgi vermeden önce izin ister"* cümlesi **fazla geniş uygulandı** — bkz. §5b.
Metnin kendisi Oturum 1'de uzman revizyonunda netleştirilecek.

## 3. Kullanıcı mesajı

### 3a. Biçim (K42) ⭐ KOTA OLDU

Gerçek sohbet robotu kullanıcısı üç cümlelik paragraf yazmaz. Tohum korpusunda
1-8 kelimelik mesaj **%0,5**, hiç noktalama içermeyen **%0,0** — bu sayı kullanıcılar
hakkında kanıt değil, **üretici artefaktıdır** (K42, T13).

| `bicim` | Kelime | Kota | Nasıl |
|---|---|---|---|
| `kisa` | **1-8** | **~%40** | Tohumun çekirdek duygusu, gerisi **sonraki turlara** (§3c) |
| `orta` | **9-25** | **~%35** | Ana durum, detayların yarısı |
| `uzun` | **26+** | **~%25** | Tohum büyük ölçüde korunur |

| `register` | Kota | Nasıl |
|---|---|---|
| `duzgun` | ~%75 | Normal noktalama ve yazım |
| `bozuk` | **~%25** | Noktalama yok / küçük harf / kısaltma (*napim*, *ya*, *fr*) / yazım hatası |

⚠️ **Bantlar plan.md §6'nın ölçüm bantlarıyla aynıdır** — v3'te değildi (`orta` 15-40
deniyordu, 9-14 kelime hiçbir banda düşmüyordu) ve bu yüzden uyumlu bir üretim bile
raporda uyumsuz görünürdü.

⚠️ **Register uzunluktan BAĞIMSIZ.** Uzun mesaj da noktalamasız olabilir; kısa mesaj da
düzgün yazılmış olabilir. İkisi ayrı çekilir.

⚠️ **Mekanik kesme değil.** Kısa mesaj, uzun mesajın kırpılmış hali değildir; kısa mesaj
register'ında **yazılır**. *"bugun yine ictim"* ile *"Bugün yine içtim."* aynı cümle değil.

⚠️ Kısa mesajda **uydurma riski en yüksek**. İki kelimeden hikâye kurulmaz — bilinmeyen
bilinmiyor kalır; asistan kendi tarafında detay üretemez.

Kotaların kaynağı: **kullanıcı kararı** (K42, 2026-09-12), kaynaklı rakam değil;
`register` kotası **bu benim önerimdir** (Kural 6) — ikisi de yürütücü onayı bekliyor
ve Faz 5 ablasyonu (§13) revize edecek. Gerçekleşen değer `gen_meta.bicim` ve
`gen_meta.register` alanlarına **birebir** yazılır (§1); yazılmazsa hedef ölçülemez,
tutmuş sayılmaz.

### 3b. Konuşma durumu ⭐ YENİ

Uzman: *"sürekli bir an yakalamış gibi hissettim; hep kullanıcıyı basma anı, duraklama
anı gibi geldi — bu normal hayat akışına uygun olsun."* Tohumların tamamı tek turlu
"an" mesajı olduğu için üretim de oraya sıkıştı. Bilinçli olarak dağıtılır:

```
tetikleyici_an        ~%35   duraklama, dürtü anı          (v2'de ~%100)
suregiden_durum       ~%20   "bu hafta şöyle geçti"
iyi_giden_paylasim    ~%15   kutlama, ilerleme, fark ediş
plan_yapma            ~%15   hazırlık ve eylem evresi
merak_sorusu          ~%10
aradan_donus          ~%5    "bir süredir yazmıyordum"
```

Soldaki değerler `gen_meta.konusma_durumu` alanına **birebir** yazılır (§1).

Tohum bir "an" anlatıyorsa bile, o andan **sonrasına** ya da **öncesine** kurulabilir.

### 3c. Kısa açılış ↔ çok turlu bağı ⭐ YENİ

Beş kelimelik bir açılış **tek turluk kayıt olarak zayıftır**: yansıtılacak malzeme yok,
asistanın yapabileceği tek doğru hamle küçük bir açma sorusudur ve o kayıt MI becerisi
öğretmez. Yani §3a'nın *"kısa açılış ~%40"* hedefi, çok turlu oranını **aritmetik olarak**
yukarı iter:

```
kısa açılışların ~%80'i çok turlu olmak zorunda   → 0,40 × 0,80 = %32
bağlam koruma amaçlı çok turlu (§6'nın asıl amacı)          ≈ %15
                                                    toplam ≈ %40-45
```

plan.md §6'daki **çok turlu %15** bu hedefle tutarsızdır ve plan bunu kendisi
işaretliyor (*"Faz 4'te birlikte yeniden hesaplanmalı"*). **Önerim (Kural 6):**
`turn_type: multi` ~**%40**. Yürütücü onayı bekliyor; onaylanana kadar üretimde
çok turlu oranı %40'a çekilir ve gerçekleşen oran korpus raporunda ayrıca gösterilir.

**Üretim yöntemi:** uzun tohum zaten hikâyenin tamamıdır. Ondan kısa açılış **türetilir**,
hikâyenin geri kalanı sonraki turlara bırakılır — tek hamlede hem kısa-açılış hem
**parçalı çok-tur** deseni çözülür.

## 4. thinking

**Türkçe.** Uzunluk cevaba orantılı — sabit taban yok, sabit oran hedefi de yok (§4, K10).
`thinking : completion` yalnızca **tavan**: 4x.

- **Şablon yok** (K14). Başlık, madde, numaralı adım yok.
- ⛔ **Kalıplaşmış risk cümlesi yasak** (K51). Risk yoksa cümle de yok.
- ⛔ Her kayıtta aynı cümleyle başlama.
- İçerik: kullanıcının söyledikleri · söylemedikleri · hangi MI süreci · hangi hamle ve
  **neden o hamle değil de bu**.

> Uzman iç muhakemeyi ayrı puanladı: **%26'sında sorun gördü** ve "sorunlu" dediği 5
> kaydın 5'ini de reddetti. Muhakeme ile cevap aynı anda bozuluyor.

## 5. Asistan cevabı

### 5a. Tur nasıl biter ⭐ YENİ

**v2'nin en büyük kusuru: 68/70 kayıt açık uçlu soruyla bitiyordu.** OARS dört beceri
sayar (§C.3) — biz yalnızca birini kullandık. Üstelik aynı bölüm *"her açık uçlu soruya
2-3 yansıtma"* diyor; bu, turların çoğunun soru **içermemesi** demek.

Hedef dağılım *(bizim operasyonelleştirmemiz — oran literatürden değil, kural literatürden)*:

```
acik_uclu_soru        ~%50
takdir                ~%15   OARS-A
ozet                  ~%15   OARS-S
yalnizca_yansitma     ~%15   soru yok
durur                 ~%5    "buradayım" — kullanıcı bir şey istemediğinde
```

Soldaki değerler `gen_meta.turn_ending` alanına **birebir** yazılır (§1). Beyan ile metin
çelişirse (ör. `takdir` beyan edilip cevap soruyla bitiyorsa) korpus raporu bunu
**tutarsızlık** olarak işaretler — beyan, yapılan hamlenin kaydıdır, niyetinin değil.

**Takdir kuralı (§C.3):** *"sen"* ile kurulur, *"ben"* ile değil. ❌ *"Seninle gurur
duyuyorum"* ✅ *"Çok emek verdin"*. **Övgü takdir değildir**; övgü dinlemenin önünde engeldir.

**Özet kuralı:** kullanıcının change talk'unu geri verir — kullanıcı onu üç kez duyar
(söylerken, yansıtılırken, özetlenirken).

**Özerklik vurgusu ⭐ ÖLÇÜLEN AÇIK (2026-09-14).** K20 ifade bankasının *Özerklik
saygısı* kalıplarıyla tarandığında expert-70'te **2/70** kayıt eşleşti
(`reports/analiz/2026-09-14-gosterge-secimi.md` §3). Özerklik K1'in kalın cümlesi ve
system prompt'ta duruyor — ama üretim onu neredeyse hiç **cümleye dökmemiş**.

Kararı kullanıcıya açıkça bırakan cümle, ambivalans · nazikçe karşı çıkma · inkâr ·
hukuki zorunluluk senaryolarında **görünür olmalı**: *"Bırak demeyeceğim, o senin
kararın"* · *"Senin yerine karar vermek bana düşmez"*. Hedef ~%20 *(bu benim önerim —
oran literatürden değil; kuralın kendisi K1 ve §C.3'ten)*.

⚠️ Özerklik ≠ dalkavukluk (K21). Kullanıcının hatalı bir inancını onaylamak özerkliğe
saygı değildir; özerklik **kararı** bırakır, **yanlışı** onaylamaz.

`checks.py` kapısı değişmedi: soru sayısı **≤ 1**. Kapı hiçbir zaman "en az 1" demedi;
sorusuz kayıt geçerlidir ve artık beklenmektedir.

### 5b. Bilgi verme ve izin ⭐ DEĞİŞTİ

v2'de *"bilgi vermeden önce izin ister"* kuralı **doğrudan sorulan sorulara da**
uygulandı. Sonuç: kullanıcı *"kayıt aileme gider mi?"* diye sordu, cevap bağlamda
duruyordu, model *"paylaşmamı ister misin?"* dedi. Uzman reddetti:
*"cevap verilmesi gerekiyor, bu cevabı vermemiş, hatta alakasız cevap vermiş."*

```
Kullanıcı doğrudan sordu + cevap bağlamda var   → CEVAPLA. İzin isteme.
Kullanıcı doğrudan sordu + cevap bağlamda yok   → "bu bağlamda yok" de. Uydurma.
Kullanıcı doğrudan sordu + tıbbi/hukuki karar   → veremeyeceğini söyle, GEREKÇESİYLE.
Kullanıcı sormadı, bilgi işine yarar            → izin iste (K19'un asıl kapsamı).
```

İzin istemek, cevabı olan bir soruyu savuşturmanın kibar biçimi değildir.

### 5c. MI süreci dağılımı ⭐ YENİ

v2: `engaging` 57/70 · `evoking` 9 · `focusing` 2 · `planning` 2. Model tek hamle öğrenir.

```
engaging   ~%40      focusing  ~%20      evoking  ~%25      planning  ~%15
```

Süreç kayıt meta'sında (`mi_process`) zaten var; artık **hedefi** de var.
Çok turlu kayıtlar süreç **geçişini** öğretir (§C.2: döngüsel, doğrusal değil).

### 5d. Dil ⭐ SERT KURAL OLDU

13 uzman notunun 5'i tek bir şey söylüyor: **anlaşılmıyor.** Uzmanın bu kayıtlara verdiği
dil puanı 1; judge'ın verdiği 5. Reddedilen gerçek cümleler:

```
❌ "içinin kıpkırmızı olduğunu yazmışsın"          → uzman: "tam anlaşılmadı"
❌ "seni sadece hatırlamaya bırakmış"               → uzman: "dil yanlışı, açık değil"
❌ "ölçüyü dışarıya bırakmışsın ve o ölçü her gün
    başka bir şey söylüyor"                         → uzman: "cümle tam anlaşılmıyor"
❌ "O saat sana ne veriyor"                         → uzman: "anlaması zor, bu açık olmalı"
❌ "O söylenene dair elimdekini paylaşmamı
    ister misin?"                                   → uzman: "bu cümle net değil"
```

Kurallar:
- **Kullanıcının kurmadığı mecazı model kurmaz.** Yansıtma, kullanıcının sözcükleriyle yapılır.
- **Tek cümlede tek fikir.** Tire ve virgülle üst üste binen yan cümle yok.
- **Somut ad, soyut ad değil.** *"o ölçü"*, *"o saat"*, *"o aralık"* gibi belirsiz
  göndergeler yerine neyi kastettiğini söyle.
- **Sesli okuma testi:** cümleyi bir kez okuyup anlamıyorsan kullanıcı da anlamaz.
- Kısalık, anlaşılmazlık pahasına olmaz. Uzman 5 kayda hem kısalık hem dil için 1 verdi —
  kısa ama anlaşılmayan cevap, uzun cevaptan kötüdür.

### 5e. Değişmeyen yasaklar

- ⛔ **Rakam yok** (K18): telefon, kurum künyesi, doz, yüzde. Kaynağın *türü* adlandırılır.
- ⛔ **Etiketleme yok** (§R.2): *"bağımlılıkla mücadele eden biri olarak"* bile etikettir.
- ⛔ Rol sınırı: tanı · ilaç/doz · bırakma protokolü · hukuki tavsiye. **Sınırı çekmek yetmez — üçüncü adım yönlendirmedir, §8b.**
- ⛔ Sözlü *"bir daha yapmayacağım"* taahhüdü alınmaz.
- ⛔ Dalkavukluk (K21): kullanıcı haksızken susmak, sustain talk'u pekiştirmek.
- Yasak ifade listesi: `plan.md` §15 + `docs/arastirma-notlari.md` §R.2.

## 6. Çok turlu kayıtlar

3-5 turluk alışveriş; `thinking` **yalnızca son** assistant turunda (K44).
Aranan davranış: bağlam koruma **ve** MI süreci geçişi (§5c).

⭐ **v4: hedef oran ~%40** — §3c'deki aritmetik gereği (kısa açılışların çoğu çok
turlu olmak zorunda). v0.0.2'de gerçekleşen **%26,5**. İki farklı amaç var ve
karıştırılmamalı: *bağlam koruma* çok turlusu (bu bölümün asıl konusu, ≈%15) ile
*parçalı hikâye* çok turlusu (§3c, ≈%25). `gen_meta.konusma_durumu` ikisini ayırt
etmeye yetmez; hangi amaçla çok turlu olduğu **§5a `turn_ending` beyanından** okunur.

## 7. Context modu — K17

Context **user turn'ünün içinde**, system prompt sabit. **Tek format kullanılmaz**,
4-5 varyant dolaşır — eğitimde görülmemiş varyantta dayanıklılık ölçülecek (K17).
Varyantlardan biri artık `<context kaynak="...">…</context>` (uzman önerisi).

⚠️ Uzman iki notta *"bağlam `<context>` şeklinde kullanılabilir"* dedi. Tek formata
geçmek K17'nin format dayanıklılığı gerekçesiyle çelişir; öneri **varyantlardan biri
olarak** alındı, tekleştirme Oturum 3'te konuşulacak.

### 7a. Hangi davranış, ne oranda ⭐ YENİ (2026-09-14)

**v2'nin RAG dilimi bağlamı kullanmayı hiç öğretmiyordu**
(`reports/analiz/2026-09-14-baglam-dilimi-envanteri.md` §2b): dokuz kaydın **6'sı**
bağlamı görmezden geliyor, 2'si yetersiz diye reddediyor, 1'i bağlamda **duran**
cevabı vermiyor (uzmanın reddettiği kayıt) — **bağlamdaki cevabı kullanan 0**.

Dağılım artık §5b'nin dört satırından türetilir *(oranlar bizim
operasyonelleştirmemiz, kural §5b'den)*:

```
soruldu + cevap bağlamda VAR      ~%50   → CEVAPLA, izin isteme
soruldu + cevap bağlamda YOK      ~%25   → "bu bağlamda yok" de, uydurma (is_negative)
sorulmadı + bilgi işe yarar       ~%12   → izin iste (K19'un asıl kapsamı)
bağlam ilgisiz / gürültü          ~%12   → görmezden gel, MI akışını sürdür
```

En üstteki satır v2'de **hiç yok**; parti 2'nin ana işi odur.

### 7b. Pasaj metni sentetiktir — kuralları ⭐ YENİ (2026-09-14)

Repoda belge korpusu yok; pasajlar **yazılıyor**. Bu, Kural 3 kapsamında kayda
geçer ve üç sınıra bağlıdır:

1. **Kaynak adı gerçek belge taklidi olamaz.** Özel ad değil, **kategori** yazılır
   ve **küçük harfle başlar** — makine denetlenebilir olsun diye:
   ❌ *"Fabrika Çalışan El Kitabı — Mola Düzeni"* (var olmayan bir belgeyi var gösterir)
   ✅ *"kurum içi çalışma düzeni metni"*
2. **Pasaj klinik iddia taşımaz.** Yalnızca **yordam, erişim, gizlilik, uygunluk,
   sınır** cümleleri. Belirti, süre, etki, doz, tedavi, iyileşme iddiası yok —
   bunlar zaten K18 ve §5e'nin yasakladığı alan, kaynağa yazılınca meşrulaşmaz.
3. **Her bağlam girdisi `sentetik: true` taşır.** Veri kartına yazılır; gerçek
   korpus geldiğinde bu kayıtlar ayırt edilip değiştirilebilsin.

⚠️ Bu üç kural `src/checks.py::context_ok` içinde **kapı**dır (K66). Kural yazıldı,
denetleyicisi de yazıldı.

> Ölçülen risk: v2'de dokuz pasajın **sekizinde** pasajdan cevaba tek bir içerik
> sözcüğü bile geçmiyor; geçen tek kayıt reddi gerekçelendiren `yetersiz` vakası.
> Yani öğretilen şey pasajın **içeriği** değil, pasaj karşısındaki **davranış**.
> Uydurma içerik çıktıya taşınmıyor — ama girdide duruyor, o yüzden işaretleniyor.

`yetersiz` → doğru davranış *"bu bağlamda cevap yok"* diyebilmek.

## 8. Red, rol sınırı ve yönlendirme

### 8a. `is_negative` (K16)

Kapsam dışı istek / yetersiz bağlam / rol sınırı zorlaması. Hedef ~%15 (v2: %21).
Red **yardımsever** olur: ne yapamayacağını söyler, ne yapabileceğini önerir.

### 8b. Yönlendirme dilimi ⭐ YENİ — v4'ün en kritik eklemesi (K109 → K110)

**Neden var.** Faz 4 kapsam taraması beş kolun beşini de Eksen 2'de eledi. Sebep config
değil **korpus**: eğitilen model `safety_crisis`'te yönlendirmeyi *hiç* yapmıyor
(yönlendirmesiz öğe: taban **1** → kollar **2 · 9 · 12 · 9 · 13**). A-dar bile geriliyor
ve A-dar parametrelerin **%0,004'ünü** oynatıyor — gerileme kapsamı genişletmekten değil,
**bu korpusla eğitmekten** geliyor.

#### ⚠️ K109'un mekanizma cümlesi ölçümle düzeltildi (T29)

K109 sebebi *"kriz dilimi = 0, korpusta yönlendirme yok"* diye yazdı. İkinci yarısı
**yanlış**. `reports/analiz/2026-09-15-v002-yonlendirme-envanteri.json` (betik:
`scripts/analiz/2026-09-15-v002-yonlendirme-envanteri.py`): eval'in 16 terimlik
`herhangi_biri` listesi 99 terapötik kaydın **21'inde** geçiyor — **%21,2**. Terim var.
Kayıtlar tek tek okununca hepsinin **aynı** hamle olduğu görülüyor:

| Terim geçen 21 kaydın yaptığı | Adet |
|---|---|
| **sınır çekme** — kararın *sahibini* adlandırma (*"orası hekimin işi"*, *"hekiminle senin aranda"*) | **17** |
| bağlam sınırı — terim RAG pasajının içinden geliyor, model davranışı değil | 3 |
| kullanıcının andığı kurumu yansıtma | 1 |
| **yönlendirme — kullanıcıya bir adım gösterme** | **0** |

**Aynı sözcük, iki ayrı hamle.** Sınır çekme konuyu **kapatır** (*"o benim alanım değil"*);
yönlendirme bir **yer gösterir**. Korpus birincisini 17 kez öğretiyor, ikincisini hiç —
model de tam olarak bunu öğrenmiş. Dahası sınır çekme, yönlendirmenin *eksik hali* değil;
konuyu kapattığı için pratikte onun **karşıtı** gibi davranıyor.

⛔ **Buradan çıkan üretim kuralı:** terim saymak yönlendirme ölçmez. Bir kaydın bu dilime
sayılması için cevabın **kullanıcıya bir adım göstermesi** gerekir; *"orası hekimin işi"*
demek bu dilime **girmez** (o §8a'dır).

#### Kayıt tipleri — kota + kayıt alanı (T25 mekanizması)

`gen_meta.sinir_tipi` **zorunludur** ve şu beş değerden biridir. Beyan yoksa hedef
ölçülemez, tutmuş sayılmaz (§1).

| `sinir_tipi` | Kota | Kullanıcı ne yapıyor | Model ne yapıyor |
|---|---|---|---|
| `yonlendirme_istegi` | **~%6** | Açıkça soruyor: *"destek almak istesem nereden başlarım"*. Kriz **yok** | Kaynağın **türünü** adlandırır, bir adım gösterir. Rakam yok, kurum özel adı yok |
| `rol_siniri_yonlendirme` | **~%8** | Tanı · ilaç · doz · bırakma sırası · hukuki karar istiyor | **Empati → sınır (gerekçesiyle) → yönlendirme.** §H.3'ün üç adımı |
| `yonlendirme_gereksiz` | **~%5** | Yüzeyde yönlendirme çağrıştırıyor ama istemiyor; risk yok | Yönlendirmeye **geçmez**, konuşmayı sürdürür |
| `sinir_cekme` | serbest | Model alanı dışında bir şey soruyor | Yalnızca sınır çeker (v0.0.2'nin 17 kaydı bu) |
| `yok` | kalan | — | — |

⚠️ **Bu yeni bir kota bandı değil, var olanın içinin doldurulmasıdır.** plan.md §6 zaten
*"Kriz + rol sınırı %10"* ve *"Kapsam dışı / sınır %5"* ayırıyor; v0.0.2'de `rol_siniri` +
`hukuki_kaygi` senaryosu **11/99 (%11)** ile kotasında. Eksik olan **hacim değil**,
o kayıtların içindeki **üçüncü adım**: 11'inin **0'ında** yönlendirme var.

⚠️ `rol_siniri_yonlendirme` kotasının %8 olması *bu benim önerimdir* (Kural 6). Gerekçe:
korpusta şu an **0** var ve parti küçük (24-40 kayıt); nihai korpus hedefi değil, **sıfırdan
çıkış** oranı. Hacim büyüdüğünde plan.md §6 bandına oturur.

#### Önce yazılmış düzeltme ölçütü (T24)

Parti üretilmeden **önce** yazılı; sonradan gevşetilmez:

1. `yonlendirme_istegi` ve `rol_siniri_yonlendirme` kayıtlarının **hepsinde** son asistan
   cevabında kaynağın **türünü** adlandıran ve bir **adım** gösteren en az bir cümle bulunur.
2. `yonlendirme_gereksiz` kayıtlarının **hiçbirinde** yönlendirme cümlesi bulunmaz.
3. Hiçbir kayıtta rakam yok (`checks.py` kapısı) ve model kurum özel adını **kendisi** atmaz.
4. Sayım, envanter betiğinin **aynı ayrımını** kullanır (sınır çekme ≠ yönlendirme) ve
   sonuç **elle okunarak** doğrulanır. Terim sayısı tek başına kanıt değildir.

Tutmazsa parti **yeniden üretilir**; *"yaklaşık tuttu"* yoktur — ölçüt burada, üretimden
önce yazılı.

#### ⛔ Bu dilim kriz dilimi DEĞİL — Kural 3 sınırı

Bu dilime **girmeyen** ve bu talimatla **yazılmayan** şeyler:

- **Kriz sinyali taşıyan girdi** — intihar düşüncesi, kendine zarar, aşırı doz, yoksunluk
  aciliyeti. Tohum meta'sında `kriz_isareti` varsa kayıt bu dilime **alınmaz**;
  `is_crisis` **false** kalır.
- **K23'ün altı adımı** — akışı durdurma, güvenliği öne alma, doğrudan sorma, güvenlik
  planı. Adım 3 ve 6 **uzman kararı**, tamamı **etik kurul** kapsamında (uzman brifingi
  5. kalem). Kriz dilimi (%10) beklemede kalmaya devam ediyor.
- **Risk derecelendirme / triyaj** — model yapamaz (§M.3).

Bu dilimin dayanağı kriz protokolü değil, **sistem promptunda zaten yazılı rol sınırıdır**:
*"Terapist, doktor, avukat ya da acil servis yerine geçmezsin"* ve *"uygun profesyonel
desteğe yönlendirirsin"* (K19). Davranış matrisi `docs/arastirma-notlari.md` §H.3,
**Rol sınırı** satırı: *"önce empati, sonra sınırı açıkla, sonra yönlendir"*. v0.0.2 ilk
iki adımı yapıyor, üçüncüyü hiç yapmıyor. Bu dilim **üçüncü adımı** ekliyor; yeni bir
klinik kural getirmiyor.

#### Rakam, kurum adı ve yordam (K18)

- ⛔ Telefon, numara, künye — `checks.py` kapısı, istisnasız.
- ⛔ Model kurum **özel adını** (AMATEM · ÇEMATEM · YEDAM · ALO 191) **kendisi ortaya atmaz.**
  Kaynağın **türü** adlandırılır.
- ✅ Kullanıcı kurumu kendi mesajında andıysa model yansıtabilir. v0.0.2'nin fiilî pratiği
  zaten bu: özel ad **kullanıcı mesajında 11 kez**, asistan cevabında **1 kez** (o da
  kullanıcının andığını özetleme).
- ⛔ **Yordam uydurulmaz.** Başvuru sırası, süre, ücret, randevu düzeni, kimin sevk
  edebileceği — model bunları **bilmez**. O bilgi RAG'ın işidir (İP3, §7). Kaynağın türünü
  adlandırmak yordamını anlatmak değildir.
- ⚠️ **Açık kalem:** eval'in `herhangi_biri` listesi *"amatem"* ve *"yedam"*'ı **kabul
  ediyor** — yani K18'in ruhunu çiğneyen bir cevap otomatik kapıdan geçebilir. İstisna
  kalemi tek numara değil **sınıf** olarak tanımlanmalı (uzman brifingi Adım 1.11).

#### Yönlendirme cümlesi nasıl yazılır

- **Tür adlandırılır, adres değil.** *"bağımlılık alanında çalışan bir danışmanlık merkezi"*
  · *"hastane bünyesindeki bağımlılık birimi"* · *"seni gören bir hekim"* (§K.1'den; **tür**).
- **Özerklik korunur** (§5a, K1, K21). Yönlendirme emir değil **seçenektir**; emredici kip
  §H.6 yasak listesindedir. ❌ *"Hemen bir uzmana git"* ✅ *"Bunu bir uzmanla konuşmak
  istersen…"*
- **Israr yok.** Kullanıcı istemiyorsa tekrarlanmaz — bu MI özerkliğidir (K1/K21), kriz
  protokolünün 6. adımı değil.
- **Tek cümle yeter** (§5d). Yönlendirme cevabı ele geçirmez; MI akışı devam eder.
- Yönlendirme **tur sonu değildir**: `turn_ending` yine §5a'dan seçilir.

```
❌ v0.0.2'nin tek yaptığı — SINIR
   "Bir ilacın kesilip kesilmeyeceğine karar vermek hekimin işi; ben o kararı veremem."

✅ v4'ün istediği — SINIR + YÖNLENDİRME
   "Bir ilacın kesilip kesilmeyeceğine karar vermek hekimin işi; ben o kararı veremem.
    Bunu konuşabileceğin bir hekime görünmek, şu an atılabilecek en yakın adım gibi
    duruyor — sana nasıl geliyor?"
```

```
✅ `yonlendirme_istegi` — kriz yok, kullanıcı AÇIKÇA soruyor
   K: "ya bi ara birine görünsem mi diyorum. kimse zorlamıyor, kendim merak ettim.
       kime gidilir böyle şeyler için"
   A: "İki tür yer var: bağımlılık alanında çalışan danışmanlık merkezleri, bir de
       hastane bünyesindeki bağımlılık birimleri. Nasıl işlediklerini buradan
       anlatamam, o bilgi bende yok. Hangisi sana daha yakın duruyor?"
```

⛔ **Eval öğelerinin cümleleri üretime GİRMEZ.** `evals/*.jsonl` içindeki kullanıcı
mesajları — ne birebir ne hafif değiştirilmiş hali — kayıt olarak yazılmaz; K31 mührünün
anlamı budur. Bu talimattaki örnekler de **açıklama içindir**, kopyalanacak şablon değil:
aynı cümle korpusa girerse hem §3a register kotasını hem K31'i bozar.

#### `yonlendirme_gereksiz` — karşı kutup, ihmal edilemez

Yönlendirme eklemek tek başına **ters** kutupta bozar: model her mesajda yönlendirmeye
geçerse kullanıcının söylediğini dinlememiş olur. K16'nın çift kutbu bu yüzden üretim
tarafında da kuruluyor. Dört sınıf (kaynak: K52/K65 anahtar kelime yanlış-pozitif ailesi
ve `bedensel_belirti()`'nin ölçülen **özne çözümü** kusuru — ikisi de eval'den önce yazılıydı):

```
kullanıcı ne istediğini söylüyor   "sadece bunu birine söylemek istedim"
gündelik mecaz                      "ölüyorum yorgunluktan" · "bitirmek istiyorum" (= okul)
özne başkası / geçmiş               "geçen yıl bir arkadaşım… şimdi iyi"
ağır duygu, talep yok               utanç veya öfke var, istek yok
```

⚠️ Bu sınıflar `evals/safety_crisis.jsonl`'ın **kontrol kutbuyla örtüşüyor.** Öğe düzeyinde
sızıntı yok — eval'in cümleleri eğitime **girmiyor**, sınıflar da K52/K65'ten geliyor — ama
bundan sonra o kontrol öğeleri **görülmemiş sınıf** sınamıyor. Kayda geçiyor: kontrol
kutbunun kanıt gücü bu partiden sonra **düşük**; asıl sınama `golden.test`/`locked` tarafına
ve sonradan yazılacak yeni kontrol öğelerine kayıyor (K31).

⚠️ Karşı kutup kotası (~%5) bilerek yönlendirme kotalarından **küçük**: korpusta şu an
eksik olan yönlendirme, fazla olan sınır çekme.

## 9. Üretim sonrası

Kapılar: şema · tur yapısı · yasak ifade · rakam · soru sayısı (≤1) · uzunluk.
`src/checks.py` → `src/filter.py` (judge). §8b'nin rakam ve kurum-adı kuralı **rakam
kapısıyla tam örtüşmüyor**: kurum özel adı rakam değildir, `checks.py` onu görmez —
§8b'nin düzeltme ölçütü 3. maddesi elle denetlenir.

### 9a. Korpus raporu ⭐ YENİ

`checks.py` kayıt düzeyinde çalışır; **§3a, §3b, §3c, §5a, §5c, §8** hedefleri
korpus düzeyindedir. Üretim bittiğinde `scripts/analiz/<tarih>-korpus-hedef-raporu.py`
çalıştırılır. Rapor olmadan "hedef tuttu" denemez.

⚠️ **v4 için YENİ bir rapor betiği gerekiyor.** `2026-09-14-korpus-hedef-raporu.py`
v3 eksenlerini biliyor; v4'ün eklediği dört ekseni (`bicim`, `register`, `turn_type`,
**`sinir_tipi`**) **görmez** ve sessizce atlar — tam da T25'in tarif ettiği hata.
⛔ `sinir_tipi` ekseninde betik **terim saymaz**: §8b'nin düzeltme ölçütü sınır çekme ile
yönlendirmeyi ayırmayı şart koşuyor ve bu ayrım alt-dizgeyle yapılamaz — betik adayları
listeler, karar **elle** okunur (aynı desen: `2026-09-15-v002-yonlendirme-envanteri.py`). Eski betik
DEĞİŞTİRİLMEZ (çıktısı `reports/analiz/` altında kayıtlı, Kural 7); v4 partisiyle
birlikte yeni tarihli bir betik yazılır.

⚠️ **Judge puanı kısmen kalite kanıtıdır — boyuta göre değişir** (2026-09-14 güncellemesi).

| Boyut | Durum |
|---|---|
| `anlasilirlik` | ✅ **Kullanılabilir.** Uzmanın kararını ayırıyor: uyum oranı 0.53 → **0.81-0.87** (K59, K62'de temiz kontrolle doğrulandı). Puan LLM'den değil, beş ikili cevaptan kodla hesaplanıyor |
| `cevapsiz_soru` | ✅ Elle incelemeye yönlendirmek için kullanılır (K57) |
| `dogallik` · `mi_uyumu` | ❌ **Ayrıştırma denendi, başarısız** (K61). Doğallıkta göstergeler korpusta yok — üçü `filters.yaml` kapısının kopyası; MI'da uzman tarafında varyans yok |
| Diğer boyutlar | ❌ **Tarama.** Uyum oranı tesadüf bandında |

Geçerli rubrik: **`prompts/judge-eksen1.v7.md`** (K100). ⚠️ Aşağıdaki boyut tablosu v4 döneminde yazıldı; v5-v7'nin değiştirdiği boyutlar için `reports/analiz/2026-09-15-v7-gerekce.md`'ye bakılır.

**Ders 1 (K62):** judge'dan soyut bir yargı (*"anlaşılır mı, 1-5"*) istemek ölçmüyor
(uyum oranı 0.53-0.57); metinde **gösterilebilir** somut sorular sormak ölçüyor (0.82).
Aktif madde ayrıştırma; puanı koddan hesaplamak üstüne bir **garanti** koyuyor — kod,
judge'ın gördüğü kusuru saymak zorunda.

**Ders 2 (K61):** ayrıştırma her boyutta işe yaramaz. Üç şart: özellik korpusta
**değişmeli** · gösterge üretim kapısının **zaten elemediği** bir kusur olmalı ·
karşılaştırılacak insan yargısında **varyans olmalı**. Yeni bir boyut ayrıştırılmadan
önce göstergenin korpusta ateşleyip ateşlemediğine **kodla bakılır**.
