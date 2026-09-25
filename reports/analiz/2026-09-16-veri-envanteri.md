# Veri envanteri — ne kadar var, ve ne kadarı kullanılabilir

**Betik:** `scripts/analiz/2026-09-16-veri-envanteri.py` · **Tarih:** 2026-09-16

---

## 1. Katmanlar

| katman | dosya | **dosya satırı** | ⭐ **tekil kayıt** |
|---|---:|---:|---:|
| tohum havuzu (`data/seeds*`) | 2 | **4480** | **2240** |
| örneklem planı (`data/plan/`) | 6 | **170** | **170** |
| üretilen aday (`data/candidates/`) | 13 | **732** | **278** |
| yargılanmış (`data/judged/`) | 21 | **1588** | **252** |
| yayımlanmış dataset (`datasets/v*`) | 5 | **602** | **175** |
| eval seti (`evals/`) | 9 | **273** | **273** |
| ⛔ karantina | 1 | **8** | **8** |

⛔⛔ **Dosya satırı ile tekil kayıt arasındaki fark tesadüf değil, TASARIM.**
`datasets/v0.0.3`, `v0.0.4` ve `v0.0.5` **aynı 155 kaydın** üç sürümü: aynı
`id`, aynı kullanıcı mesajları; tek fark eklenen yönlendirme cümleleri (K114,
doz-yanıt kolları). ⇒ Dosya satırlarını toplamak **aynı veriyi üç kez sayar**.

➡️ *Bir veri kümesinin büyüklüğü, dosyalarının büyüklüğü değildir — ve ikisini*
*karıştırmak tezde veri setini olduğundan büyük gösterir.*

---

## 2. Dataset sürümleri — hangisi neyin üstüne biniyor

| sürüm | kayıt | bir öncekiyle ortak `id` | yeni |
|---|---:|---:|---:|
| `v0.0.1` | 20 | 0 | **20** |
| `v0.0.2` | 117 | 0 | **117** |
| `v0.0.3` | 155 | 117 | **38** |
| `v0.0.4` | 155 | 155 | **0** |
| `v0.0.5` | 155 | 155 | **0** |

⭐ **Beş sürümün tekil kayıt birleşimi: 175.** Dosya satırı toplamı 602 — **427 satır tekrar**.

---

## 3. Metin hacmi — en güncel sürüm (`v0.0.5`)

| | |
|---|---:|
| kayıt | **155** |
| bunlardan replay (§9 unutma savunması) | 18 |
| terapötik kayıt | **137** |
| mesaj (tur) | **614** |
| kullanıcı kelimesi | **5.966** |
| asistan cevap kelimesi | **7.874** |
| asistan thinking kelimesi | **11.753** |
| **toplam** | **25.593** |

⭐ Kayıt başına ortalama **165** kelime · thinking payı **%46**.

⚠️ Birim **kelime** (K46/T81 ile aynı, Kural 5) — token değil.

---

## 4. ⛔ Asıl soru: ne kadarı KULLANILABİLİR

| eksik | durum |
|---|---|
| **kriz dilimi** (~%10 hedef) | ⛔ üretilmedi — etik kurul + uzman onayı bekliyor (Kural 3) |
| **vahşi doğa dilimi** | ⛔ üretilemedi — aday kaynakların tamamı elendi (`oasst2`'de yalnızca 10 Türkçe prompter mesajı) |
| karantina | ⛔ **8 kayıt** eğitim setine giremiyor; gerekçesi (K76) **yazılmamış** |
| uzman puanlaması | ◐ 50/70'te kapandı (K58) |

⭐ **En güncel sürümün senaryo dağılımı** (137 terapötik kayıt):

| senaryo | kayıt |
|---|---:|
| `farkindalik` | 25 |
| `ambivalans` | 23 |
| `rol_siniri` | 14 |
| `inkar` | 10 |
| `hedef_belirleme` | 10 |
| `nazikce_karsi_cikma` | 9 |
| `kayma_nuks` | 7 |
| `motivasyon` | 7 |
| `bilgilendirme` | 7 |
| `kutlama` | 5 |
| `durtu` | 4 |
| `hukuki_kaygi` | 4 |
| `anlasilmama` | 3 |
| `discord` | 3 |
| `borc_finansal` | 2 |
| `bilmiyorum_cikmazi` | 2 |
| `kayip_kovalama` | 2 |

⛔⛔ **Ölçek bağlamı: tohum havuzu 2.240, yayımlanmış tekil kayıt 175.** Yani havuzun **%7.8**'i üretime girdi. ➡️ *Darboğaz tohum değil; üretim, yargılama ve **onay**.*

## ⛔ Bu envanterin söylemedikleri

| | |
|---|---|
| ⛔ **Kalite** | sayılan şey hacim; `datasets/v0.0.1`'in kalite hedefi **yoktu** (Faz 2 dikey dilim) ve o da bu toplamın içinde |
| ⛔ **Token değil kelime** | tokenizer'a bağlı bir sayı istenirse yeniden ölçülmeli (K46/T81 ile karşılaştırılabilirlik için kelime seçildi) |
| ⚠️ `data/judged` ↔ `data/candidates` örtüşmesi | ikisi de aynı kayıtların farklı aşamaları; tekil sayılar bunu düzeltir ama **aşama** bilgisi bu tabloda yok |
| ⛔ Eval setleri **eğitim verisi değil** | mühürlü (K31) ve toplama dahil edilmemeli |
| ⚠️ Arşiv (`reports/analiz/ham-judge`, `*/sonuclar.jsonl`) | **ölçüm çıktısı**, veri seti değil — kapsam dışı |

