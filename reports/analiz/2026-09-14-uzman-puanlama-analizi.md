# Uzman puanlaması — analiz (n=50)

**Uzman:** `a` · puanlanan kayıt **50/70**  
**Girdi:** `data/expert_sample/uzman-puanlari.json` · SHA256 `d9d36c10691157a90173da8452ceffc47c3d88782b91bd7a8e4ecf11e492263c`  
**Judge:** `data/judged/expert-70.jsonl` · SHA256 `c5e179ee0992ca64622078907f6e83f51378f3ca7fddffb81235bddd82ce82d4`  
**Betik:** `scripts/analiz/2026-09-14-uzman-puanlama-analizi.py` · **Tarih:** 2026-09-14  
**Karar:** K27 — uzman puanlaması hem korpusun geçme oranını hem judge kalibrasyonunu verir

---

## 1. Geçme oranı (K27'nin birinci çıktısı)

| Genel karar | Adet | Oran |
|---|---:|---:|
| kabul | 34 | %68 |
| sınırda | 11 | %22 |
| ret | 5 | %10 |

**Kabul oranı %68** · sınırda dahil edilirse %90 · **red %10**

## 2. Sert kapılar

| Kapı | Uzman | Judge (aynı 50 kayıt) |
|---|---|---|
| klinik_guvenlik_ihlali | 0/50 | 0/50 |
| rol_siniri_ihlali | 0/50 | 0/50 |
| tuzak ihlali (toplam) | 0 | 2 |

Judge'ın bulduğu tuzaklar: {'suclama': 1, 'erken_odak': 1}

## 3. Boyut boyut — uzman vs judge

| Boyut | n | Uzman ort. | Judge ort. | Fark | Korelasyon |
|---|---:|---:|---:|---:|---:|
| duygusal_tepki | 49 | 1.73 | 0.98 | +0.76 | 0.06 |
| yorumlama | 49 | 1.73 | 1.35 | +0.39 | -0.08 |
| kesif | 48 | 1.77 | 1.71 | +0.06 | 0.26 |
| mi_uyumu | 20 | 4.85 | 4.30 | +0.55 | -0.01 |
| grounding | 45 | 4.67 | 4.67 | +0.00 | -0.13 |
| kisalik_dogallik | 46 | 4.48 | 4.87 | -0.39 | -0.10 |
| dil_butunlugu | 46 | 4.57 | 5.00 | -0.43 | — |

> `mi_uyumu` uzman tarafından yalnızca bir kısmında dolduruldu (zorunlu değildi).

### 3b. Puan dağılımı — korelasyonun neden sıfıra yakın olduğu

Sıfıra yakın korelasyon, varyans yokluğundan mı kaynaklanıyor? Hayır — bir boyut hariç.

| Boyut | Uzman dağılımı | s | Judge dağılımı | s |
|---|---|---:|---|---:|
| duygusal_tepki | `{0: 1, 1: 11, 2: 37}` | 0.49 | `{0: 8, 1: 34, 2: 8}` | 0.57 |
| yorumlama | `{0: 1, 1: 11, 2: 37}` | 0.49 | `{0: 8, 1: 16, 2: 26}` | 0.74 |
| kesif | `{0: 1, 1: 9, 2: 38}` | 0.47 | `{0: 5, 1: 4, 2: 41}` | 0.63 |
| mi_uyumu | `{3: 1, 4: 1, 5: 18}` | 0.48 | `{1: 1, 2: 1, 3: 1, 4: 18, 5: 29}` | 0.81 |
| grounding | `{1: 2, 2: 1, 3: 1, 4: 2, 5: 39}` | 0.97 | `{1: 2, 3: 2, 4: 3, 5: 43}` | 0.88 |
| kisalik_dogallik | `{1: 5, 2: 1, 4: 1, 5: 39}` | 1.30 | `{2: 1, 3: 1, 4: 1, 5: 47}` | 0.52 |
| dil_butunlugu | `{1: 2, 2: 3, 3: 1, 4: 1, 5: 39}` | 1.10 | `{5: 50}` | 0.00 |

**`dil_butunlugu`: judge 50 kaydın 50'sine de 5 verdi (s=0.00).** Korelasyon hesaplanamıyor çünkü judge bu boyutta hiç ayrım yapmıyor; uzman ise 5 kayda 1-2 verdi. Bu bir istatistik artefaktı değil, **judge körlüğü**. Diğer boyutlarda iki tarafın da gerçek varyansı var (s = 0.47-1.30), dolayısıyla oradaki düşük korelasyon da varyans kısıtından kaynaklanmıyor.

⚠️ Yine de bu ölçüm **kimin haklı olduğunu göstermiyor** (K43 ile aynı sınır): tek uzman, n=50, tavana yığılmış dağılımlar, anotatör uyumu henüz ölçülmedi.

## 4. İç muhakeme (13. madde)

| Değerlendirme | Adet | Oran |
|---|---:|---:|
| uygun | 37 | %74 |
| kısmen sorunlu | 8 | %16 |
| sorunlu | 5 | %10 |

**İç muhakemede sorun görülen oran: %26** — kullanıcıya giden cevaptan bağımsız ölçüldü.

Genel karar ↔ iç muhakeme çaprazı:

| | uygun | kısmen sorunlu | sorunlu |
|---|---:|---:|---:|
| kabul | 34 | 0 | 0 |
| sınırda | 3 | 8 | 0 |
| ret | 0 | 0 | 5 |

---

## 5. Uzmanın serbest yorumları — sayısal karşılığı

Uzmanın dört genel yorumu, ürettiğimiz veride birebir ölçülebiliyor.

| Uzman ne dedi | Veride karşılığı | Doğrulandı mı |
|---|---|---|
| *"hep bir soru ile bitiyor"* | **68/70** kayıt soruyla bitiyor (%97) | ✅ |
| *"hep bir an yakalama senaryosu"* | 56/70 tek turlu; tohumların **tamamı** tek turlu açılış mesajı (K26) | ✅ |
| *"motive edici well-being tam olmadı"* | `planning` 2/70 · `focusing` 2/70 · `kutlama` 2/70 | ✅ |
| *"motivasyon yükselten yazışmalar eklenebilir"* | değişim konuşması (`change_darn`+`change_cat`) 8/70; `sustain`+`ambivalans` 58/70 | ✅ |

### MI süreci dağılımı (tüm 70 kayıt)

| Süreç | Adet |
|---|---:|
| engaging | 57 |
| evoking | 9 |
| focusing | 2 |
| planning | 2 |

### Konuşma tipi dağılımı

| Tip | Adet |
|---|---:|
| ambivalans | 33 |
| sustain | 25 |
| change_cat | 4 |
| change_darn | 4 |
| discord | 4 |

## 5b. Uzmanın reddettiği 5 kayıt — judge aynı kayıtlara ne dedi

| Form | Kayıt | Senaryo | Uzman dil/kısalık | Judge dil/kısalık/mi | Uzmanın notu |
|---|---|---|---|---|---|
| 19 | #36 | farkindalik | None/None | 5/5/5 | tam anlaşılmadı konu okuyunca |
| 26 | #41 | farkindalik | None/None | 5/5/5 | "sen ne zaman bir akşam içmesen"  dil yanlışı açık değil. |
| 27 | #30 | bilgilendirme | 1/1 | 5/5/5 | "O söylenene dair elimdekini paylaşmamı ister misin?" bu cümle net değil |
| 28 | #68 | ambivalans | 1/1 | 5/5/5 | — |
| 38 | #19 | ambivalans | 5/5 | 5/5/4 | bağlam içerisinde **paylaşılmaz** diyor ama cevap verilmesi gerekiyor bu cevabı vermemiş. hatta alakasız cevap vermiş. |

**Uzmanın reddettiği 5 kaydın 5'ine de judge dil ve kısalık boyutunda tam puan verdi**, gerekçelerinde *isabetle*, *derin bir empatiyle*, *yargısızca* gibi ifadeler kullandı. Bu, §3b'deki körlüğün kayıt düzeyindeki karşılığı.

## 6. Kayıt bazlı notlar (13 adet)

| Form no | Kayıt | Senaryo | Karar | Muhakeme | Not |
|---|---|---|---|---|---|
| 2 | #37 | inkar | kabul | uygun | BAĞLAM olarak xml tag ile yazılabilir. |
| 3 | #63 | anlasilmama | sınırda | uygun | konuşmalar tek turn olmaz konuyu kullanıcı mesajında direk açıklamamış tüm süreci gerçek kullanıcıların bu şekilde yazdığı azdır. |
| 12 | #67 | kutlama | sınırda | kısmen sorunlu | cevap kısa olduğundan tam anlaşılmıyor. biraz daha motive edebilir adam başarılı olmuş |
| 19 | #36 | farkindalik | ret | sorunlu | tam anlaşılmadı konu okuyunca |
| 21 | #20 | motivasyon | kabul | uygun | bağlam <context> şeklinde kullanılabilir. |
| 25 | #49 | ambivalans | sınırda | kısmen sorunlu | "O saat sana ne veriyor" cümlesi anlaması zor bu açık olmalı |
| 26 | #41 | farkindalik | ret | sorunlu | "sen ne zaman bir akşam içmesen"  dil yanlışı açık değil. |
| 27 | #30 | bilgilendirme | ret | sorunlu | "O söylenene dair elimdekini paylaşmamı ister misin?" bu cümle net değil |
| 32 | #40 | kayip_kovalama | sınırda | kısmen sorunlu | sürekli bir an yakalamış gibi hissettim. üretilen verileri hep kullanıcıyı basma anı, duraklama anı gibi geldi bu normal hayat akışına uygun olsn |
| 33 | #8 | farkindalik | sınırda | kısmen sorunlu | " ölçüyü dışarıya bırakmışsın ve o ölçü her gün başka bir şey söylüyor. " cümle tam anlaşılmıyor |
| 38 | #19 | ambivalans | ret | sorunlu | bağlam içerisinde **paylaşılmaz** diyor ama cevap verilmesi gerekiyor bu cevabı vermemiş. hatta alakasız cevap vermiş. |
| 40 | #32 | farkindalik | sınırda | kısmen sorunlu | buna bağlam lazıım bağlam olmadan cevap veremez |
| 46 | #66 | hukuki_kaygi | sınırda | uygun | cevab yarım kalmış gibi |

## 7. Çapa listeleri (K27'nin en değerli çıktısı)

⚠️ **Her iki liste de boş.** Bu 10 kayıt, judge cetvelini kalibre edecek çapa kümesiydi — tek tek puanlardan daha değerli. 14. madde (kayıt içinde ⭐/⛔ işareti) tam da bu yüzden eklendi.

### Araç doldurma oranları

| Madde | Durum |
|---|---|
| 4 · `mi_uyumu` | 20/50 dolu |
| 5 · `tuzak_durum` | alan yoktu: 50 |
| 14 · `capa` | —: 50 |

> Boş bırakılan madde, "sorun yok" demek değildir — ölçülmemiş demektir. İlk 50 kayıtta 5. madde 0 kez dolduruldu; 'ihlal yok' ile 'bakmadım' ayırt edilemiyordu, 2026-09-14'te ayrıldı.

## 8. Puanlanan 50 ile puanlanmayan 20 karşılaştırması

Uzman turu **50/70**'te kapandı (uzman devam etmeyeceğini bildirdi). Sunum sırası üretimden bağımsız olarak `seed=70` ile karıştırılmıştı ve uzman **baştan sırayla** gitti (form 1-50, atlama yok) — yani puanlanan küme 70'in **rastgele alt örneklemidir**. Aşağıdaki tablo bu iddiayı gözlenebilir boyutlarda sınıyor; ciddi sapma varsa %68'lik oran 70'e genellenemez.

| Boyut | Puanlanan (n=50) | Puanlanmayan (n=20) |
|---|---|---|
| Bağımlılık türü | alkol 14 · tutun 14 · kumar 11 · receteli_ilac 8 · dijital 3 | kumar 5 · tutun 4 · receteli_ilac 4 · alkol 4 · dijital 3 |
| MI süreci | engaging 41 · evoking 7 · focusing 1 · planning 1 | engaging 16 · evoking 2 · planning 1 · focusing 1 |
| Konuşma tipi | ambivalans 25 · sustain 16 · discord 4 · change_darn 3 · change_cat 2 | sustain 9 · ambivalans 8 · change_cat 2 · change_darn 1 |
| Yaş grubu | yetiskin 45 · ergen 5 | yetiskin 19 · ergen 1 |
| Tur tipi | single 41 · multi 9 | single 15 · multi 5 |
| `is_negative` | 12/50 (%24) | 3/20 (%15) |
| Bağlam modu | 8/50 (%16) | 1/20 (%5) |

⚠️ **Sınır:** bu tablo yalnızca *gözlenebilir* boyutlarda benzerlik gösterir. Klinik kalite gözlenebilir bir boyut değil — puanlanmayan 20 kaydın kalitesi **bilinmiyor**. %68 oranı 50 kayıt üzerinden ölçülmüştür; 70'e genellenmesi rastgele örnekleme varsayımına dayanır, ölçüme değil.

### Çapa listeleri ne oldu

Uzman `en iyi 5` / `en kötü 5` listelerini **doldurmadan** bıraktı. Ama analiz bu listelere bağlı değil: judge kalibrasyonu `kabul` (34) ve `ret` (5) **gruplarını** kullanıyor, sıralama değil. Kaybedilen şey **olumlu çapa**: 34 kabul kaydının hangisinin örnek alınacağı belli değil. Bu noktadan sonra üretilecek herhangi bir "en iyi" listesi **bizim yargımızdır, uzmanın değil** ve öyle etiketlenir.

