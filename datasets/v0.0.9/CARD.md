# BıRAG veri kümesi — v0.0.9

**Tarih:** 2026-09-17 · **Girdi:** `data/judged/v0.0.9.jsonl`
**Çıktı:** `train.jsonl` SHA256 `667ec2c580cb7b59`
**Kayıt:** 571/577 (elenen **6**) — v0.0.8 ile **aynı sayıda**

---

## 1. v0.0.8'den farkı: 14 kayıt, tek bir kural

⛔ **Yeni kayıt YOK.** Bu sürüm bir büyüme değil, bir **düzeltme**.

| kural | kayıt | ne yapıldı |
|---|---:|---|
| ⭐ **§5a⁗** — reddetmek devretmeyi gerektirir | **13** | cevap bedensel bir bildirimi yorumlamayı reddediyor ama **kimin söyleyebileceğini** söylemiyordu; kaynak TÜRÜ eklendi |
| tanı iddiası | 1 | kaynaksız bir fizyolojik iddia (*bir etiyolojiyi eliyordu*) söylemsel bir gözleme çevrildi |
| T104 yapısal atıf | 2 | *«aynı cümlede»* → *«aynı mesajda»* (iki alıntı ayrı cümlelerdeydi) |

⭐ **Ölçülen etki:** §5a⁗ çıkmazı **16 → 4**.

---

## 2. ⭐⭐ 81 değil 13 — ve eleme işin asıl kısmıydı

İlk tarama *«reddedip devretmeyen»* 81 kayıt bulmuştu. Her eleme ölçüldü:

| eleme | kaç | neden |
|---|---:|---|
| zaten kaynak türü veriyor | **12** | `safety_crisis`'in kabul listesi **kriz odaklı**; *«borç danışmanlığı»*, *«rehberlik birimi»* gibi türleri görmüyor ⇒ saptayıcının yanlış pozitifi |
| §5a⁗ kapsamı **dışı** | **61** | *«Bu akşam ne yapacağına ben karar veremem»* bir **özerklik** cümlesi, bedensel bildirim reddi değil. Oraya kaynak türü koymak `tuzak_erken_tavsiye` üretirdi |
| mecaz | 1 | *«başka annelerin nasıl nefes aldığını bilemem»* |
| zaten devrediyor | 1 | bağlam belgesine işaret ediyor |
| ⭐ **gerçek çıkmaz** | **13** | 12 klinik + 1 hukuki |

➡️ *Bir kuralı, doğurduğu ölçütten daha geniş uygulamak, kuralı uygulamak değil onu **genişletmektir**.*

---

## 3. ⛔⛔ AYNI `id`, FARKLI METİN — 14 kayıt

v0.0.8 ile v0.0.9'da **14 kaydın metni farklıdır** ve v0.0.8 değişmez (Kural 4).
⇒ İki sürümün puanları kayıt düzeyinde **karşılaştırılamaz**.

⚠️ v0.0.7 ile karşılaştırma yapılacaksa oradaki **16 kayıtlık** uyarı da geçerli
ve iki liste **aynı kayıtlar değildir**.

---

## 4. Elenen 6 kayıt — değişmedi

| gerekçe | kayıt |
|---|---:|
| `judge_safety_violation` | 3 |
| `guvenlik_karantinasi` | 3 |

---

## 5. Bu sürümde öğrenilenler (veriye girmeyen ama kararı belirleyen)

| bulgu | nerede |
|---|---|
| ⭐⭐ `safety_crisis` ölçütünün **üç kusuru** — yankı, olumsuzlama ve **yasak davranış ödülü**; ham modelin 13 yönlendirmesinin 8'i K18 ihlalli | `2026-09-17-k18-temiz-yonlendirme.md` |
| ⭐⭐ Güvenlik davranışı **12 katmana kadar duruyor, 13'te çöküyor**; çöküşün üçte ikisi **katman 29'un kimliğinden** | `2026-09-17-ucurum-haritasi.md` |
| ⭐⭐ **Her yeni kural, bir sonraki şablonun tohumu** — *«Bir şeye katılmıyorum»* %0 → **%12,4** | `2026-09-17-sablon-buyumesi.md` |
| ⭐ Eksen 2'nin **gürültü tabanı 2 öğe** ⇒ bundan küçük farklar okunamaz | `2026-09-17-karsi-olgusal-sonuc.md` |

---

## ⛔ Bu kartın söylemedikleri

| | |
|---|---|
| ⛔⛔ **K3 (MI tuzağı) kasten düzeltilmedi** | 84 tuzak sette **duruyor**; ilk eğitim ölçülmeden hepsini düzeltmek hangi revizyonun işe yaradığını ölçülemez yapardı. `#13` bu sürümde de `tuzak_uzman` alıyor |
| ⛔⛔ **Şablonlaşma düzeltilmedi** | *«Bir şeye katılmıyorum»* 71 kayıtta; ölçüldü, kapı yazılmadı |
| ⛔ **26 «aynı cümlede» iddiası elle okunmadı** | kapı yalnız ≥2 alıntılı olanları otomatik sınıyor |
| ⛔ **Kriz dilimi hâlâ yok** | etik kurul + uzman onayı bekliyor (Kural 3) |
| ⛔ **Rubrik karışımı sürüyor** (K137) | v9 %73, v7 %24 — puanlar sürüme göre ayrılmadan havuzlanamaz |
| ⛔ **Hakem Claude ailesinden** (K43/K45) | judge çıktısı **metrik değil** |
| ⚠️ **§5a⁗ cümleleri şablon değil ama tek elden** | 13'ü de aynı üretici yazdı (K30); çeşitlilik ölçülmedi |
