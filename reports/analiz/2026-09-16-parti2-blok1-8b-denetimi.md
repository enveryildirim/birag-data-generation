# v4-parti2 · Blok 1 — §8b düzeltme ölçütünün denetimi

**Betik:** `scripts/analiz/2026-09-16-parti2-blok1-8b-denetimi.py`
**Girdi:** `data/candidates/v4-parti2.jsonl` · **SHA256:** `4154385d9d39d2449786050081684ad6fd4461b04fa1d73257fae7556dd7bfeb`
**Tarih:** 2026-09-16 · **Kayıt:** 60 (parti tamam)
**SHA256:** `4154385d9d39d2449786050081684ad6fd4461b04fa1d73257fae7556dd7bfeb`

> Ölçüt **üretimden önce** yazıldı (`prompts/uretim-v4.md` §8b, T24) ve burada
> gevşetilmedi. *"Yaklaşık tuttu"* yok.

---

## 1. Ne üretildi

⚠️ **Kapsam aynı gün büyüdü.** Betik önce blok 1 (§8b dilimi, 20 kayıt) için
yazıldı; blok 2 üretilince (kısa açılış bloğu, 18 kayıt) **aynı betiğe** eklendi
ve çıktı yeniden üretildi. Dosya adı ilk kapsamı taşıyor, **atıf kararlılığı için
değiştirilmedi** (T92/T93 bu adı gösteriyor).

v4-parti2'nin **60 kaydının tamamı**: §8b dilimi (**20**), kısa açılış bloğu
(**18**) ve orta+uzun blok (**22**, 6'sı bağlamlı).

⭐ **`yok` beyanı da sınanır.** Yönlendirme içeren bir kayıt `yok` diye beyan
edilirse beyan yanlıştır ve §8b'nin dilim sayımı sessizce bozulur ⇒ `yok`
kayıtları da ölçüt 2'ye tabi tutuldu (40/40 temiz).

| `sinir_tipi` | adet | kayıt no |
|---|---:|---|
| `yonlendirme_istegi` | 5 | 1-5 |
| `rol_siniri_yonlendirme` | 7 | 6-12 |
| `yonlendirme_gereksiz` | 4 | 13-16 |
| `sinir_cekme` | 4 | 17-20 |
| `yok` (blok 2 + 3) | 40 | 21-60 |

Kapılar: `src/checks.py` **60/60 geçti**, yinelenen `id` **0**.
Tek yumuşak bayrak: **#8**'de `rol_siniri: ['doz']` — modelin hekime iletilmesini
önerdiği cümlenin içinde (*"doz azalınca bacaklarım kramp giriyor"*), yani
**doğru reddin içinde geçen kelime** (checks.py'nin `SERT_KATEGORILER` dışı
bırakma gerekçesinin tam olarak tarif ettiği durum).

---

## 2. Ölçüt 1-3 — sonuç

| # | Ölçüt | Sonuç |
|---|---|---|
| 1 | `yonlendirme_istegi` + `rol_siniri_yonlendirme`'nin **hepsinde** tür + adım | **12/12** ✅ |
| 2 | `yonlendirme_gereksiz`'in **hiçbirinde** yönlendirme yok | **4/4** ✅ |
| 3 | Rakam yok · model kurum **özel adını** kendisi atmıyor | **0 rakam · 0 özel ad** ✅ |
| 4 | Sayım envanterin ayrımını kullanır, karar **elle** okunur | ✅ — §3 |

Elle okuma `ELLE` sözlüğünde **cümle numarasıyla** yazılı; betik numarayı
doğrulayıp cümleyi rapora basıyor, yani numara boşa yazılamıyor.

⚠️ **İki sınırda kalem, kabul edildi ve gerekçesi yazıldı:**

- **#4** — kaynağın türünü (*"psikolojik danışma merkezi"*) **kullanıcı andı**;
  model yansıttı ve **adımı** o ekledi. §8b'nin izin verdiği durum (kullanıcının
  andığı kaynağı yansıtma), ama ölçüt 1 açısından *modelin kendi yönlendirmesi*
  sayılması sınırda.
- **#15** — `yonlendirme_gereksiz` olduğu hâlde cevapta **terapist anılıyor**.
  Model bir yer **önermiyor**: kullanıcının kendi kurduğu düzeni yansıtıyor.
  Yeni kaynak yok, adım yok ⇒ ölçüt 2 ihlali değil.

---

## 3. ⭐⭐ Ölçüt 4'ün ölçtüğü asıl şey — terim listesi bu partiyi GÖREMİYOR

Sayım, `2026-09-15-v002-yonlendirme-envanteri.py`'nin 16 terimlik listesini
**import ederek** yaptı (kopyalamadan; tek fark katlama — orası düz `.lower()`,
burası `tr_fold`, ki **daha kapsayıcıdır**).

| | adet | kayıt no |
|---|---:|---|
| terim geçen (eval listesi) | 14 | — |
| **elle okunmuş yönlendirme** | **12** | 1-12 |
| ⛔ terim var, yönlendirme YOK | **5** | **30, 32, 43, 50, 59** |
| ⛔ **yönlendirme var, terim YOK** | **3** | **4, 5, 11** |

⭐⭐ **Repoda İKİ liste var ve ikisi de aynı şeyi ölçüyor.** Betik ikisini de
**import ediyor**, kopyalamıyor:

| liste | terim | kesinlik | duyarlılık | kaçırdığı |
|---|---:|---:|---:|---|
| **eval** — `safety_crisis` `herhangi_biri` (Faz 5'te PUANI bu belirler) | 16 | %64 | **%75** | 4, 5, 11 |
| **rapor** — `2026-09-15-v4-korpus-hedef-raporu.py` (üretim tarafı) | 21 | %71 | **%100** | — |

Aradaki **beş terim**: `danışmanlık` · `merkez` · `birim` · `avukat` ·
`müdürlük` — yani tam olarak **kurum kategorisi** sözcükleri, §8b'nin yazılmasını
şart koştuğu biçim.

⛔⛔ **Boşluk üretim tarafında zaten kapatılmış, eval tarafında kapatılmamış.**
Yani kendi raporumuz *"yönlendirme dilimi tuttu"* diyecek (%100 duyarlılık),
Faz 5'i puanlayacak eval ise dörtte birini **görmeyecek** (%75).

⭐ **Kesinlik ise liste genişleterek kapanmıyor:** iki listenin de **5 yanlış
pozitifi aynı sınıf** — `#30`/`#32` kullanıcının kendi doktorunu yansıtıyor,
`#43`/`#50`/`#59` kullanıcının SORDUĞU bir pasajı aktarıyor. Hepsinde eksik olan
şey sözcük değil, **kimin inisiyatifi** olduğu. Alt-dizge bunu göremez.

⛔⛔ **Aynı 60 kayıtta İKİ YÖN de ölçüldü.** 2026-09-15'te yalnız bir yön
görülmüştü (*yanlış pozitif*: terim 21 kayıtta, yönlendirme 0). Burada ikisi
birden var:

- **Yanlış negatif (3):** gerçek yönlendirme, listede hiç terim yok.
- **Yanlış pozitif (5):** `#30`/`#32` kullanıcının **kendi doktorunu**
  yansıtıyor; `#43`/`#50`/`#59` kullanıcının **sorduğu** bir pasajı aktarıyor
  (2026-09-15 envanterinin `baglam_siniri` sınıfı). Hiçbirinde model kendi
  inisiyatifiyle kaynak önermiyor.

➡️ Yani liste **hem fazla hem az sayıyor** ve iki hata birbirini gizliyor:
toplam terim sayısı (14) toplam yönlendirmeye (12) yakın durduğu için **ölçüt
tutmuş gibi görünür**.

Sebep okunabiliyor: liste **meslek adları** (*hekim, doktor, uzman, profesyonel*)
ve **hat** adları (*destek hattı, danışma hattı*) içeriyor; §8b'nin istediği
biçim ise **kurum kategorisi** — *"bağımlılık alanında çalışan danışmanlık
merkezleri"*, *"hastanelerin bağımlılık birimleri"*, *"psikolojik danışma
merkezi"*, *"bir avukat"*. Bunların hiçbiri listede yok.

➡️ **Faz 5 için doğrudan sonuç:** §8b'yi doğuran eval, §8b'nin ürettiği
davranışın dörtte birini **ölçemez**. Eğitim gerçek davranışı düzeltse bile
metrik kıpırdamayabilir — ve bu, eğitimin başarısızlığı olarak okunur.

⚠️ **Yön uyarısı:** bu sayı *bizim* yazımımıza da bağlı — kurum özel adlarından
kaçınmak (K18) doğrudan liste dışı bir söz dağarcığına itiyor. Yani bulgu
"liste kötü" değil, **"liste ile üretim kuralı aynı şeyi tarif etmiyor"**.

---

## 4. Şablonlaşma — K14 gereği eklendi, ölçütte yoktu

Yönlendirme dilimini eklerken en kolay hata, korpusa **17 kez tekrarlanan sınır
çekmenin** yerine **N kez tekrarlanan tek bir yönlendirme cümlesi** koymaktır:
hamle değil **dizge** öğretilir.

| ölçüm | ilk yazım | düzeltme sonrası |
|---|---:|---:|
| birden fazla kayıtta geçen 6-gram (son cevap) | **21** | **5** |
| en yüksek tekrar | **4x** (#1,2,3,11) | **2x** |
| birden fazla kayıtta geçen 6-gram (thinking) | 1 | **0** (blok 1) · **1** (38 kayıtta, 2x) |

Sayılar **blok 1'in** ilk ve düzeltilmiş hâlidir. 38 kayıtta ölçüm: cevapta
**5** tekrarlı 6-gram (en çok **2x**), thinking'de **1** (2x).

İlk yazımda #1, #2 ve #3 aynı 11 kelimelik yönlendirme cümlesini paylaşıyordu.
Beş cümle yeniden yazıldı (farklı kaynak türü çiftleri, adım kullanıcının kendi
cümlesine bağlandı). Betik artık **3+ tekrarı hata** sayıyor.

---

## 5. ⭐ Blok 2'nin kendi yükü — §5a ve §3c

Blok 2 (kısa açılış bloğu, 18 kayıt) §8b dilimine girmiyor; ölçtüğü şey başka.

**§5a — turların çoğu soru İÇERMEMELİ.** v2'nin en büyük kusuru 70 kaydın
**68'inin** açık uçlu soruyla bitmesiydi. Blok 2'de **18 kaydın 13'ü soruyla
bitmiyor**: `takdir` 5 · `ozet` 4 · `yalnizca_yansitma` 2 · `durur` 2.
38 kayıtlık birikimde açık uçlu soru payı **%53** (parti hedefi ~%50).

**§3c çarpışması — ölçütte yoktu, blok 2 yazılırken görüldü.**

§3c açıkça yazıyor: *"Beş kelimelik bir açılış tek turluk kayıt olarak zayıftır:
yansıtılacak malzeme yok."* Izgara `bicim` ile `turn_type`'ı **bağımsız** çekiyor
(§3a'nın kendi kuralı, register için de aynısı) ⇒ bu hücre yine de doluyor:
**60 satırın 5'i** kısa + tek tur (`#7, #8, #9, #37, #38`).

⭐ Ölçülünce zayıflık koşulunun *kısa + tek tur* olmadığı görüldü — **üçüncü,
ızgarada hiç çekilmeyen bir değişkene** bağlı: kısa mesaj **cevaplanabilir bir
talep** taşıyor mu.

| kayıt | ilk mesaj talep taşıyor mu | `turn_ending` |
|---|---|---|
| #7, #8, #9 | ✅ (rol sınırı soruları) | soru · yansıtma · soru |
| #37, #38 | ❌ | **ozet** · **takdir** |

⛔⛔ **Talep taşımayan ikisi, ızgaradan sorusuz bitiş çekti — tesadüfen.**
`#37` `acik_uclu_soru` çekseydi, neredeyse boş bir mesaja soru sormak zorunda
kalırdım. ➡️ *Izgaranın kota denetimi her ekseni ayrı ayrı doğru bulur ve
eksenlerin KESİŞİMİNDE talimatın kendi yasakladığı hücreyi göremez.*

Denetim artık bu hücreyi kapı olarak tutuyor: **talep yok + açık uçlu soru = hata.**

---

## 6. ⭐ Blok 3 — bağlam dilimi ve ızgara-tohum çarpışması

### 6a. §7 bağlam dilimi (6 kayıt)

Partinin RAG dilimi bu blokta. **§7a beyanı artık bir ALAN** — `gen_meta.baglam_davranisi`
(§1b, T96): §7a dört sınıfı yüzde olarak tanımlıyordu ama gerçekleşeni kaydeden
alan yoktu, yani T25'in hatasının birebir tekrarı.

| §7a sınıfı | hedef | gerçekleşen (n=6) | kayıt |
|---|---:|---:|---|
| `cevap_var` — soruldu, cevap pasajda → **CEVAPLA** | ~%50 | 3 (%50) | 43, 55, 59 |
| `cevap_yok` — soruldu, cevap pasajda yok → *"yok"* de | ~%25 | 1 (%17) | 50 |
| `izin_iste` — sorulmadı, bilgi işe yarar | ~%12 | 1 (%17) | 40 |
| `ilgisiz` — gürültü → görmezden gel | ~%12 | 1 (%17) | 52 |

⚠️ **n=6'da hedef dağılımı tam tutturulamaz**; 3/1/1/1 en yakın tam sayı bölüşümü.
⭐ `cevap_var` satırı **v2'de sıfırdı** (dokuz pasajın hiçbirinde bağlamdaki cevap
kullanılmamıştı) — partinin bağlam tarafındaki asıl işi buydu.

**K17 biçim çeşitliliği:** beş varyantın beşi de dolaşıyor (`v1`-`v5`); `v5`
(`{bağlam kaynağı: …}`) bu partide yeni. Tek formata geçilmedi.

**§7b kapısı:** altı pasajın altısı `sentetik: true`, kaynak adları küçük harfle
başlayan **kategori** adları, klinik iddia taşımıyor — `checks.py::context_ok`
60/60 geçti.

⛔ `cevap_yok` kaydı (`#50`) `is_negative` taşıyor; denetim bunu **kapı** olarak
tutuyor (§7a'nın kendi şartı: *"uydurma (is_negative)"*).

### 6b. ⛔ Izgara ile tohum çarpışması — 4 satırda tohum kazandı

Blok 3 yazılırken görüldü: ızgaranın `motivasyon` sütunu tohumların kendi
meta'sıyla **60 satırın 23'ünde** çelişiyor.

| sınıf | adet | ne oluyor | karar |
|---|---:|---|---|
| tam uyum | 37 | — | — |
| ⚠️ **düzleştirme** | 19 | tohum daha özgül, ızgara `ic`e çekmiş (`aile_baskisi → ic` 18) | ızgara korunur, tohum değeri `gen_meta.motivasyon_tohum`'a yazılır |
| ⛔ **uydurma** | 4 | ızgara tohumda **olmayan** bir durum iddia ediyor | **tohum kazanır**, sapma `gen_meta.izgara_sapmasi`'na yazılır |

⛔⛔ **Ayrım kritik:** düzleştirme bilgi **kaybıdır** ve alan yazılınca geri
alınabilir; uydurma bilgi **üretimidir** ve geri alınamaz — korpusa tohumu
olmayan bir vaka girer.

Dört uydurma satırı ve kanıtları (betik tohumun **kendi notunu** okuyor, varsaymıyor):

| kayıt | ızgara | tohum | düzeltme | tohumun kendi notu |
|---|---|---|---|---|
| #44 | `yasal_zorunluluk` | `ic_motivasyon` | `ic` | — |
| #46 | `aile_baskisi` | `yasal_zorunluluk` | `yasal_zorunluluk` | *"okul yönlendirmesi"* |
| #57 | `yasal_zorunluluk` | `ic_motivasyon` | `ic` | — |
| #59 | `yasal_zorunluluk` | `tetikleyici_olay` | `ic` | — |

⭐ `#46` ters yönde: ızgara **hukuki/kurumsal** bir zorunluluğu silmişti. Tohumun
`notlar.motivasyon_notu` alanı *"okul yönlendirmesi"* diyor ve tohum metni de
(*"Okul müdürü ailemle görüşmüş"*) bunu doğruluyor ⇒ düzeltme onu geri getirdi.

⛔ Üç satırda ızgarayı onurlandırmak, **olmayan bir hukuki durumu uydurmayı**
gerektirirdi (Kural 3). Yapılmadı.

Betik: `scripts/analiz/2026-09-16-izgara-tohum-carpismasi.py` →
`reports/analiz/2026-09-16-izgara-tohum-carpismasi.json`

### 6c. Korpus hedefleri — altı eksenin altısı tam tuttu

`scripts/analiz/2026-09-15-v4-korpus-hedef-raporu.py` (değiştirilmedi, yalnız
yeni girdiyle koşuldu), 60 kayıt:

| eksen | sapma |
|---|---|
| `bicim` · `register` · `konusma_durumu` · `turn_ending` · `mi_process` · `turn_type` | **+0.0 puan, altısı da** |
| beyan ↔ metin tutarsızlığı | **yok** |

⚠️ **Bu bir başarı ölçüsü değil, bir tutarlılık ölçüsüdür.** Sapmanın sıfır
olması, üretimin **ızgarayı** izlediğini gösterir; ızgaranın doğru olduğunu
değil. §6b tam da ızgaranın bir sütununun yanlış olduğunu gösteriyor ve bu
tablo onu göremiyor.

---

## 7. Şerhler

- ⛔ **Ölçüt 1'in "adım" kararı elle verildi.** Alt-dizgeyle verilemez (§8b'nin
  kendi şartı) ⇒ sayı, **bir okuyucunun** kararıdır; ikinci okuyucu yok.
- ⛔ **Kalite ölçülmedi, ölçüt uyumu ölçüldü.** Judge ve uzman değerlendirmesi
  bu partiye **henüz uygulanmadı**.
- ⚠️ **Korpus hedefleri (§3a, §3b, §5a, §5c) bu raporun konusu değil** —
  blok 1 partinin **§8b dilimi**, dağılım raporu 60 kayıt tamamlanınca yazılır.
- ⛔ Kriz dilimi bu partide **yok** (etik kurul, §8b'nin Kural 3 sınırı).
- ⚠️ Şablon ölçümü **parti içi**; parti1 ve v0.0.2 ile çapraz tekrar ölçülmedi.
- ⛔ *«Talep taşıyor mu»* vekil ölçütü **soru işareti** sayıyor; soru işaretsiz
  emir kipi talep (*«bana bir program yaz»*) bu vekile takılmaz. Blok 1'de öyle
  bir kayıt kısa+tek tur değildi, yani vekil bu partide **sınanmadı**.
- ⚠️ §5a payları artık **60 kayıt üzerinden** ve `turn_ending` hedefi tam tuttu.
- ⛔ §7a dağılımı **n=6**; yüzde olarak okunmamalı.
- ⛔ Pasajların hepsi **sentetik** (§7b) — repoda belge korpusu yok. Öğretilen şey
  pasajın *içeriği* değil, pasaj karşısındaki **davranış**.
- ⚠️ `motivasyon` düzleştirmesinin 19 satırı **düzeltilmedi**, yalnız görünür
  kılındı; bunların 18'i `aile_baskisi → ic` ve korpus `motivation` dağılımı
  `ic` yönünde **yanlı**.
- ⛔ Vekil ölçüt kalitesi sayıları (kesinlik/duyarlılık) **tek okuyucunun** elle
  okumasına göre; ikinci okuyucu yok.
