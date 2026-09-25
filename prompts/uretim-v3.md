# Üretim talimatı — v3

> **v2'yi süperse eder.** v2 silinmez: `data/candidates/expert-70.jsonl`'in nasıl
> üretildiğinin kaydıdır (Kural 7 · `gen_meta.prompt_version: uretim-v2`).
>
> v3'ün kaynağı **uzman puanlaması (n=50)** ve ölçümleri:
> `reports/analiz/2026-09-14-uzman-puanlama-analizi.md`

## 0. v2'den ne değişti, neden

| Değişiklik | Ölçülen sorun | Nerede |
|---|---|---|
| Tur kapanışı çeşitlendi | **68/70** kayıt soruyla bitiyordu | §5a |
| İzin kuralı daraltıldı | Bağlamda duran cevap verilmedi (#19, #30 — uzman **ret**) | §5b |
| MI süreci dağılımı hedefi | `engaging` 57/70, `planning` 2/70 | §5c |
| Konuşma durumu çeşitliliği | *"hep bir an yakalama senaryosu"* — tohumların tamamı tek turlu "an" | §3b |
| Dil sadeliği sert kural oldu | 13 uzman notunun **5'i** "anlaşılmıyor" | §5d |
| Takdir/özet becerileri eklendi | OARS'ın 4 becerisinden yalnızca 1'i kullanılmış (§C.3) | §5a |

---

## 1. Kayıt iskeleti

`src/schemas.py::TrainRecord`. Mesaj dizisi: `system` → `user` → `assistant`
(`thinking` yalnızca son assistant mesajında). `age_group` **yalnızca** `yetiskin|ergen`.
`turn_type`: `single|multi`.

`gen_meta`: `{generator: claude-code, generator_model: claude-opus-5,
prompt_version: uretim-v3, date: <tarih>, system_prompt_variant: canon|paraphrase,
turn_ending: <§5a>, konusma_durumu: <§3b>}`

⚠️ **`turn_ending` ve `konusma_durumu` beyanı zorunludur.** v3'ün yeni hedefleri korpus
düzeyindedir; `checks.py` onları göremez (kayıt düzeyinde kapı değiller). Üretici hangi
hamleyi yaptığını beyan eder, `scripts/analiz/*-korpus-hedef-raporu.py` dağılımı ve
beyanın tutarlılığını denetler (§9a). Beyan yoksa hedef **ölçülemez**, tutmuş sayılmaz.

## 2. System prompt (K19)

Kayıtların **%75-80'i** kanonik metni birebir, **%20-25'i** anlamca eşdeğer parafraz.
Gerekçe: %100 aynı string olursa model davranışı o string'e kilitlenir.

⚠️ K19'un *"Bilgi vermeden önce izin ister"* cümlesi **fazla geniş uygulandı** — bkz. §5b.
Metnin kendisi Oturum 1'de uzman revizyonunda netleştirilecek.

## 3. Kullanıcı mesajı

### 3a. Biçim (K42)

| Biçim | Hedef | Nasıl |
|---|---|---|
| `kisa` | 1-8 kelime | Tohumun çekirdek duygusu, gerisi atılır |
| `orta` | 15-40 kelime | Ana durum, detayların yarısı |
| `uzun` | 40+ kelime | Tohum büyük ölçüde korunur |

`register: bozuk` → noktalama yok / küçük harf / yazım hatası. İçerik aynı, biçim bozuk.

⚠️ Kısa mesajda **uydurma riski en yüksek**. İki kelimeden hikâye kurulmaz.

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
- ⛔ Rol sınırı: tanı · ilaç/doz · bırakma protokolü · hukuki tavsiye.
- ⛔ Sözlü *"bir daha yapmayacağım"* taahhüdü alınmaz.
- ⛔ Dalkavukluk (K21): kullanıcı haksızken susmak, sustain talk'u pekiştirmek.
- Yasak ifade listesi: `plan.md` §15 + `docs/arastirma-notlari.md` §R.2.

## 6. Çok turlu kayıtlar

3-5 turluk alışveriş; `thinking` **yalnızca son** assistant turunda (K44).
Aranan davranış: bağlam koruma **ve** MI süreci geçişi (§5c).

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

## 8. `is_negative` (K16)

Kapsam dışı istek / yetersiz bağlam / rol sınırı zorlaması. Hedef ~%15 (v2: %21).
Red **yardımsever** olur: ne yapamayacağını söyler, ne yapabileceğini önerir.

## 9. Üretim sonrası

Kapılar: şema · tur yapısı · yasak ifade · rakam · soru sayısı (≤1) · uzunluk.
`src/checks.py` → `src/filter.py` (judge).

### 9a. Korpus raporu ⭐ YENİ

`checks.py` kayıt düzeyinde çalışır; §3b, §5a, §5c, §8 hedefleri **korpus düzeyindedir**.
Üretim bittiğinde `scripts/analiz/<tarih>-korpus-hedef-raporu.py` çalıştırılır. Rapor
olmadan "hedef tuttu" denemez.

⚠️ **Judge puanı kısmen kalite kanıtıdır — boyuta göre değişir** (2026-09-14 güncellemesi).

| Boyut | Durum |
|---|---|
| `anlasilirlik` | ✅ **Kullanılabilir.** Uzmanın kararını ayırıyor: uyum oranı 0.53 → **0.81-0.87** (K59, K62'de temiz kontrolle doğrulandı). Puan LLM'den değil, beş ikili cevaptan kodla hesaplanıyor |
| `cevapsiz_soru` | ✅ Elle incelemeye yönlendirmek için kullanılır (K57) |
| `dogallik` · `mi_uyumu` | ❌ **Ayrıştırma denendi, başarısız** (K61). Doğallıkta göstergeler korpusta yok — üçü `filters.yaml` kapısının kopyası; MI'da uzman tarafında varyans yok |
| Diğer boyutlar | ❌ **Tarama.** Uyum oranı tesadüf bandında |

Geçerli rubrik: `prompts/judge-eksen1.v4.md`.

**Ders 1 (K62):** judge'dan soyut bir yargı (*"anlaşılır mı, 1-5"*) istemek ölçmüyor
(uyum oranı 0.53-0.57); metinde **gösterilebilir** somut sorular sormak ölçüyor (0.82).
Aktif madde ayrıştırma; puanı koddan hesaplamak üstüne bir **garanti** koyuyor — kod,
judge'ın gördüğü kusuru saymak zorunda.

**Ders 2 (K61):** ayrıştırma her boyutta işe yaramaz. Üç şart: özellik korpusta
**değişmeli** · gösterge üretim kapısının **zaten elemediği** bir kusur olmalı ·
karşılaştırılacak insan yargısında **varyans olmalı**. Yeni bir boyut ayrıştırılmadan
önce göstergenin korpusta ateşleyip ateşlemediğine **kodla bakılır**.
