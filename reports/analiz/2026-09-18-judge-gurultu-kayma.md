# Gürültü mü kayma mı — ve üçüncü şık: başka judge

**Betik:** `scripts/analiz/2026-09-18-judge-gurultu-kayma.py` · **Tarih:** 2026-09-18  
**Girdi:** `data/judged/v0.0.14.jsonl` · SHA256 `0972b567a03904fd`  
**Örnek:** 18 kayıt, metni hiç değişmemiş · rubrik `judge-eksen1.v9`  
**A (kayıtlı):** `claude-sonnet-subagent` · **B, C (bugün, taze):** `agy:gemini-3.8-flash-high`

⛔⛔⛔ **Bu betiğin ilk sürümü yanlış ölçtü ve yanlışı burada kayıtlıdır.** `llm.call` içerik-özetli zorunlu önbellek tutar; arka arkaya iki çağrıdan ikincisi birincinin yazdığı dosyayı okur. İlk sürüm bu yüzden *«%0 değişti»* buldu — judge'ın belirlenimciliği değil, **önbelleğin totolojisi**. Bu sürümde her çekiliş için `llm.CACHE_DIR` boş bir geçici dizine çevrilir ⇒ çağrı servise gider.

Doğrulama: B 0 taze çağrı, C 0 taze çağrı (her ikisi de = örnek boyu olmalı; değilse ölçüm yine önbellekten okumuştur).

## 1. ⭐ GÜRÜLTÜ — aynı gün, aynı model, iki taze çekiliş (B ↔ C)

| | |
|---|---:|
| kayıt | 18 |
| **puanı değişen kayıt** | **11** (%61) |
| alan düzeyinde düştü / yükseldi | 9 / 5 |

| boyut | ↓ | ↑ |
|---|---:|---:|
| `duygusal_tepki` | 1 | 1 |
| `kesif` | 4 | 1 |
| `mi_uyumu` | 1 | 0 |
| `yorumlama` | 3 | 3 |

⭐ **Gürültü ölçüldü: %61 kayıt oynak.** Yön simetrik ⇒ saf gürültü.

## 2. ⛔⛔ «Kayma» değil — A ile B AYNI MODEL DEĞİL

| boyut | A (Claude) | B (Gemini) | C (Gemini) | A → bugün |
|---|---:|---:|---:|---:|
| `duygusal_tepki` | 1.17 | 1.22 | 1.22 | **+0.06** |
| `yorumlama` | 1.83 | 1.50 | 1.50 | **-0.33** |
| `kesif` | 1.17 | 1.28 | 1.11 | **+0.03** |
| `mi_uyumu` | 4.83 | 4.78 | 4.72 | **-0.08** |
| `grounding` | 5.00 | 5.00 | 5.00 | **+0.00** |

A ↔ B: **9/18** kayıt farklı · alan düzeyinde 8 düştü / 5 yükseldi.

⛔⛔ **Bu fark ne gürültü ne kayma — iki ayrı modelin anlaşmazlığıdır.** Kayıtlı yargılar `claude-sonnet-subagent` ile, bugünküler `agy:gemini-3.8-flash-high` ile üretildi. ➡️ *Kayma ancak aynı modelin iki farklı günü karşılaştırılarak ölçülebilir; elimizde Gemini'nin ikinci bir günü yok, bu yüzden **kayma bu veriyle hâlâ ölçülmemiştir**.*

## 3. ⛔⛔⛔ T173 düzeltilir

| T173'te yazan | burada bulunan |
|---|---|
| «judge kayıt düzeyinde %50 kararsız» | o %50 **aynı judge'ın iki çekilişi değil**, Claude ↔ Gemini anlaşmazlığıydı |
| «`yorumlama`/`kesif` sistematik düşüyor ⇒ kayma olabilir» | düşüş **model farkının** yönü; kayma iddiası dayanaksız kaldı |
| — | aynı modelin gerçek gürültüsü ilk kez burada ölçüldü: **11/18** |

## 4. ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔ **n=18 küçük** | oranlar geniş güven aralığı taşır |
| ⛔⛔ **Kayma ölçülmedi** | aynı modelin ikinci bir günü yok |
| ⛔⛔ **Havuzun judge'ı Claude** | `v0.0.14`'te 527 kayıt `claude-sonnet-subagent`; K43/K45 puanlayan judge'ın Claude olamayacağını söyler. Bu, kullanıcının açık yönergesiyle böyle yapıldı — ama **ölçütün dayandığı zemin budur** ve karar uzmanındır |
| ⚠️ **Doğruluk ölçülmedi** | üç çekiliş de yanlış olabilir; ölçülen tutarlılık |
| ⚠️ **C çekilişinde 6 çağrı düştü** | `agy` boş içerik döndürdü ve aynı kayıtlar yeniden çağrıldığında YİNE düştü ⇒ dalgalanma değil. Ayırt edici özellik ARANDI ve bulunamadı: istem uzunluğu ortanca 1057 krk (düşen) ↔ 1077 krk (geçen). ⛔ Neden bilinmiyor; n=18 bu yüzden **sistematik yanlı sayılmadı, ama yansızlığı da kanıtlanmadı** |
| ⛔⛔ **Betik kendi sayısını yeniden üretmez** | ölçtüğü şey çekiliştir; yeniden koşmak yeni bir çekiliş olur. Ham puanlar JSON'a dökülür, `--kurtar` kipi aynı cevaplardan aynı tabloyu türetir |

## 5. ⭐⭐ Asıl sonuç — toplam sağlam, kayıt çekiliş

Aynı iki taze çekilişte **kayıtların %61'i oynadı**, ama boyut ortalamaları neredeyse yerinde durdu (§2'deki B ↔ C sütunları: `duygusal_tepki` 1.22↔1.22, `yorumlama` 1.50↔1.50, `kesif` 1.28↔1.11, `mi_uyumu` 4.78↔4.72, `grounding` 5.00↔5.00).

➡️ **Gürültü toplamda sönümleniyor, kayıtta sönümlenmiyor.** Bunun işlemsel karşılığı şudur: judge puanı **kümeler için** okunabilir, **tek kayıt hakkında karar vermek için okunamaz**. Tek bir kaydı puanına bakıp elemek ya da tutmak, ölçüm değil kura çekmektir.

## 6. ⭐⭐⭐ Kura ürüne ulaşıyor mu — kapı bayrakları

`src/build.py:71` judge'ın 1-5 puanlarını **hiç okumaz**; derlemeden eleyen tek judge ölçütü `klinik_guvenlik_ihlali` ikili bayrağıdır. Dolayısıyla §1'deki %61 oynaklık ancak bu bayrağı çevirdiği ölçüde ürüne ulaşır.

| bayrak | A (Claude) | B | C | ⛔ B↔C çevrilen |
|---|---:|---:|---:|---:|
| `klinik_guvenlik_ihlali` **(eleyen)** | 1 | 1 | 0 | **1** |
| `rol_siniri_ihlali` | 0 | 0 | 0 | **0** |
| `tuzak_suclama` | 0 | 0 | 1 | **1** |
| `kurum_yordam_ihlali` | 0 | 0 | 0 | **0** |

⛔⛔⛔ **Eleyen bayrak 1 kayıtta çevrildi.** Aynı metin, aynı gün, aynı model — ama biri derlemeye giriyor öteki elenmiyor. Derlemenin içeriği kısmen çekilişe bağlı demektir; bu, ölçüm değil kura ile veri seçmektir.

**Çevrilen kayıt:** `kimyasal_madde:st_001:0105` · A(Claude)=True B=True C=False · `guvenlik_tipi: riski_atlama`  
⛔⛔ Bu kayıt `datasets/v0.0.14`'ten **elendi** (`judge_safety_violation`). İkinci çekiliş kazansaydı **girecekti**. ➡️ *Kural 3 güvenlik ekseninde sert kapı ister; girdisi çekiliş olan bir kapı sert değildir.*

⚠️ Öteki kapı bayraklarında toplam **2** çevrilme var; bunlar bugün elemiyor ama raporlanıyor.

⚠️ Bu 18 kayıtta eleyen bayrak A, B, C'nin üçünde de 1/18 ateşledi — **örneklemde neredeyse hiç pozitif yok**, yani kararlılık burada «hep hayır demek»le de açıklanabilir. ⛔ Bayrağın gerçek kararlılığı ancak pozitifçe zengin bir kümede ölçülür; bu ölçüm onu yapmıyor.
