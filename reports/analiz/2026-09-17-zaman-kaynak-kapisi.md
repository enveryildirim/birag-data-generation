# Zaman ve kaynak-atfı kapısı — ölçülmüş gücü ve sınırı

**Betik:** `scripts/analiz/2026-09-17-zaman-kaynak-kapisi.py` · **Tarih:** 2026-09-17

T104 ölçtü: `uretim-v5` §3a′ uydurulmuş ayrıntıyı önlemek için yazıldı ve kusur
**2/54 → 6/58** çıktı. Altısının **hiçbiri tırnaklı değildi** ⇒ mevcut
`thinking-alinti-denetimi` (dizge arar) hiçbirini göremezdi.

Bu kapı ailenin **sözlükle aranabilen iki üyesini** hedefliyor:
**zaman ifadesi** ve **kaynak atfı** (2. tekil iyelik + tamlayan).

---

## 1. Güç ölçümü — bilinen kusurlu/temiz çift

⭐ Elde **mükemmel bir çift** vardı: judge'ın 6 uydurma bulduğu `v5-parti3` ve
düzeltilmiş `v5-parti3.v2`.

| korpus | işaretli kayıt | not |
|---|---:|---|
| `v5-parti3` (kusurlu) | **5** | |
| `v5-parti3.v2` (düzeltilmiş) | **2** | |
| `v4-parti2.v2` | 7 | ⚠️ elle okunmadı |
| `v4-parti1` | 2 | ⚠️ elle okunmadı |

⭐ **Ayrım tuttu:** düzelttiğim üç ögenin **üçünü de** yakaladı —
`#2` «doktorunun» · `#21` «aynı akşam» · `#39` «öğleden sonra».

⛔ **Duyarlılık %50:** judge 6 uydurma bulmuştu, kapı 3'ünü görüyor. Görmedikleri:
`#10` (anlatılmamış bir **örüntünün tamamı**), `#47` («merdivende» — **mekân**),
`#55` («dün gece» — kullanıcı «dün» demişti, kök eşleşti).

---

## 2. ⛔⛔ Kapının ÜÇ kusuru ölçülerek bulundu — üçü de öğretici

**(1) Yalın gün adları gürültü üretiyordu.** İlk sürüm 60 kaydın **33'ünde**
ateşledi. Sebep: asistan konuşmanın kendi gününe atıf yapıyor (*«Bunu bugün sen
yaptın»*) ve bunun için kullanıcının «bugün» demesi gerekmiyor. ⇒ Yalın
«bugün/dün/yarın» çıkarıldı, yalnız **bileşik** zaman ifadeleri kaldı.

**(2) ⭐⭐ Asistan kişi ekini DEĞİŞTİRMEK ZORUNDA.** Kullanıcı «eşim» der, asistan
«eşin» demek zorundadır. Dizge karşılaştırması bu yüzden **doğru davranışın
tamamında** ateşliyordu. ⇒ Karşılaştırma **kök** üzerinden yapılıyor.

➡️⭐⭐ *Alıntı doğrulaması (model KOPYALAR) dizgeyle çalışır; yansıtma
doğrulaması (model DÖNÜŞTÜRMEK ZORUNDADIR) dizgeyle çalışmaz. İki kusur aynı
aileden ama kapıları aynı olamaz.*

**(3) ⛔ Muafiyet listesi hiç ateşlemedi ve sebebi bu deponun kendi tuzağı.**
*«hekimin işi»* bir **tür adlandırma**dır (§8b'nin istediği), atıf değil — muaf
tutulacaktı. Liste düz ASCII yazılmıştı (`"isi"`) ama `tr_fold("işi")` **`"ışı"`**
veriyor: i-sınıfı `i`yi `ı`ya çeker, `ş` korunur. ⇒ Muafiyet 60 kayıtta **sıfır
kez** çalıştı ve 11 yanlış pozitif üretti. T73/T75/T76'nın ailesi, bu kez
**benim yazdığım** kapıda. ➡️ *Desen ile metin aynı katlamadan geçmezse kapı
sessizce körelir.*

---

## 3. ⭐ Kapı ile judge AYNI ögeleri bulmuyor

`v4-parti2.v2`'de judge **2** uydurma bulmuştu (ve ikisi düzeltildi). Kapı **7**
kayıt işaretliyor ve içlerinde judge'ın hiç anmadığı adaylar var:
`#34` «aynı akşam» · `#41` «aynı gün» · `#56` «aynı gece» · `#50` «doktorun».

➡️ *İki ölçüm aracı aynı kusur ailesini ölçüyor ama farklı üyelerini görüyor;
hiçbiri ötekinin üst kümesi değil.* ⛔ Bu adaylar **elle okunmadı** — borç.

---

## 4. Şerhler

- ⛔ **Kapsam: ailenin iki üyesi.** Mekân ve örüntü **kapalı sözlükle aranamaz**;
  bulunan sayı bir **ALT SINIRDIR**.
- ⛔ **Duyarlılık %50** (3/6), **kesinlik ölçülmedi**: kalan işaretlerin kaçının
  gerçek olduğu elle okunmadı (`v5-parti3.v2`'de 2 aday, ikisi de sınırda).
- ⚠️ Sözlükler **elle yazıldı**; kapsam dışı zaman ifadeleri ve kişi adları var.
- ⛔ Kapı `checks.py`'ye **eklenmedi** — kesinliği ölçülmeden sert kapı olamaz.
  Şimdilik üretim sonrası bir **aday listeleyici**.
