# `golden.dev.jsonl` — parti 1

**Çıktı:** `evals/golden.dev.jsonl` · SHA256 `1396c6713e9b2b5d1dba3c65f9ff3fae6c5961d676f86dbf6b6528fd5c258fa2`  
**Betik:** `scripts/analiz/2026-09-14-golden-dev.py` · **Tarih:** 2026-09-14  
**Mühür:** `evals/bolme.json` · **Öğe:** 48

---

## 0. Bu ne değil

Eğitim kaydı değil, **ölçüm aleti**. Öğelerde referans cevap YOK: girdi ve o girdinin hangi kusuru yemlediği yazılı, cevabı model üretecek, rubrik puanlayacak. Referans yazsaydım korpusu da cetveli de aynı kişi yazmış olurdu (K20-C); bu kurulumda payım **girdi seçimiyle** sınırlı.

**Ayrım gücü örneklem büyüklüğünden değil öğe tasarımından geliyor.** K85/K86'da judge'ın n=40'ta fark göremediği ölçüldü. Tipik girdilerden kurulu bir set aynı duvara toslar; bu yüzden her öğe bir kusuru yemler — girdi, yanlış hamlenin cazip olduğu yere kurulur.

## 1. Kapılar

- `golden_checks.py`: **48/48** geçti
- Mühür: her öğenin tohumu `dev` havuzunda doğrulandı (K31)
- Referanssızlık: hiçbir öğe asistan cevabı taşımıyor

## 2. Dilim

| Dilim | Öğe |
|---|---:|
| `tuzak` | 10 |
| `cok_turlu` | 10 |
| `seyrek_girdi` | 9 |
| `rol_siniri` | 5 |
| `nazikce_karsi_cikma` | 4 |
| `yorumlama` | 4 |
| `kapsam_disi` | 4 |
| `cevapsiz_soru` | 2 |

## 3. İddia tipleri

| Tip | Adet | Maliyet |
|---|---:|---|
| `otomatik` | 60 | bedava, deterministik |
| `judge` | 141 | LLM çağrısı, gürültülü |
| `uzman` | 2 | insan, kıt |

> `otomatik` iddialar yalnızca **yokluk** iddia eder. Bu bir tasarım kuralı: bu oturumda Türkçe serbest metinde anahtar-kelime kapılarının tavana vurduğu altı örnek çıktı ve *varlık* iddiaları eval'de **yanlış negatif** üretir — model doğru davranır, alet 'başarısız' der, veri o yöne revize edilir.

## 4. Judge boyutlarının kapsanması

| Boyut | Kaç öğede |
|---|---:|
| `mi_uyumu` | 21 |
| `tuzak_suclama` | 15 |
| `duygusal_tepki` | 10 |
| `rol_siniri_ihlali` | 10 |
| `grounding` | 9 |
| `tuzak_etiketleme` | 9 |
| `ozerklik_vurgusu` | 9 |
| `tuzak_erken_tavsiye` | 8 |
| `yansitma_var` | 7 |
| `tuzak_uzman` | 7 |
| `kesif` | 5 |
| `tuzak_erken_odak` | 5 |
| `yorumlama` | 5 |
| `bos_guvence` | 4 |
| `karmasik_yansitma` | 4 |
| `cevapsiz_soru` | 4 |
| `klise_acilis` | 2 |
| `klinik_guvenlik_ihlali` | 2 |
| `tuzak_soru_cevap` | 2 |
| `takdir_var` | 1 |
| `ozet_var` | 1 |
| `ovgu_tonu` | 1 |

### 4b. Eşiksiz boyutlar

⚠️ **Dikkat, bu "ölçülmüyor" demek değil.** Judge rubriğin HER boyutunu HER cevapta puanlıyor; `iddialar` ise o boyuta bu öğede bir **eşik** koyar (*"burada `tuzak_suclama` false olmalı"*). Aşağıdakiler puanlanıyor ama hiçbir öğede eşikleri yok: gerileme sayıda görünür, **başarısızlık sayılmaz**.

Rubrikte **37** boyut, eşikli **22**, eşiksiz **15**. Eşiksizler iki ayrı kalem:

**(a) Bütünsel/üslup — öğe eşiği anlamsız, korpus düzeyinde eşik gerekir.** Girdi yemlemese de her cevapta ateşlerler:

`anlasilirlik` · `anlasilirlik_holistik` · `belirsiz_gonderge` · `devrik_eksiltili` · `dil_butunlugu` · `dogallik` · `dogallik_holistik` · `kisalik_dogallik` · `kurulmamis_mecaz` · `mi_uyumu_holistik` · `siz_kaymasi` · `soyut_adlastirma` · `terapi_jargonu` · `tuzak_ihlali` · `ust_uste_yan_cumle`

**(b) Ancak girdi yemlerse ateşleyen boyutlar** — bunlar için öğe yazmak şart, yoksa boyut hiç denenmemiş olur:

_Yok — girdi tasarımı gerektiren her boyutta en az bir öğe var._

> Yani öğe düzeyinde kapanmamış boyut kalmadı. Kalan iş **korpus düzeyi eşikleri**: `dogallik`, `dil_butunlugu` gibi boyutlara tek tek öğe değil, 48 cevabın dağılımına bakan bir eşik gerekiyor ve o eşik henüz yok.


## 5. Girdi kaynağı

| Kaynak | Öğe | Benim payım |
|---|---:|---|
| tohum | 30 | yalnızca hangi tohumu seçtiğim |
| tohum + elle devam | 10 | açılış tohumdan, sonraki turlar benden |
| elle | 8 | tamamı benden |

> ⚠️ **Çok turlu öğelerde bir sızıntı var ve kapatılamıyor, yalnızca sınırlanıyor.** Önceki asistan turlarını ben yazıyorum ve bunlar modele bağlam içi ÖRNEK olur; parlak yazsaydım öğe "MI sürdürebiliyor mu"yu değil "taklit edebiliyor mu"yu ölçerdi. Panzehir kapıda: önceki asistan turları 220 karakterle sınırlı ve bilerek yavan yazıldı. Yine de bu öğelerin puanı kısmen benim yazdığım geçmişi ölçüyor — sayıyı okurken bu akılda tutulmalı.

| Kullanıcı turu | Öğe |
|---|---:|
| 1 | 38 |
| 2 | 6 |
| 3 | 4 |

## 5b. Girdi çeşitliliği

| Yaş grubu | Öğe |
|---|---:|
| yetiskin | 14 |
| genc_yetiskin | 12 |
| — (elle) | 8 |
| ergen | 7 |
| orta_yas | 4 |
| yasli | 3 |

| Bağımlılık türü | Öğe |
|---|---:|
| dijital | 10 |
| alkol | 10 |
| tutun | 9 |
| — (elle) | 8 |
| receteli_ilac | 6 |
| kumar | 5 |

## 6. Ölçülmeyen

- ⛔ **Kriz ve yüksek risk yok.** Havuzdan elendi (Kural 3, uzman Oturum 1). `evals/safety_crisis.jsonl` bekliyor — bu set sınır davranışını ölçmez.
- ⛔ **Çok turlu öğe yok.** Tohum havuzunun tamamı `turn_count=1`; çok turlu öğeler elle kurulacak ve kaynağı öyle işaretlenecek (parti 2).
- ⛔ **RAG / context sadakati yok** — Eksen 4, ayrı dosya.
- Eksen 5 (dalkavukluk) ile `nazikce_karsi_cikma` dilimi **örtüşüyor**; buradaki öğeler MI uyumu boyutundan puanlanıyor, Eksen 5'in kendi seti ayrıca gerekir.

