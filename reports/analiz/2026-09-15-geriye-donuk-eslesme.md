# Geriye dönük eşleşme denetimi — v7/v8 arşivlerinde de kayma var mı

*2026-09-15 · betik `scripts/analiz/2026-09-15-geriye-donuk-eslesme.py`*
*girdi: `reports/analiz/ham-judge/` — arşivlenmiş HAM judge çıktısı; **yeniden puanlama YOK**, hiçbir yayımlanmış sayı bu betikle değişmez*

## Soru

`korpus-v9-p2`'de bir subagent doğru iş dosyalarını okuyup sonuçları **yanlış**
çıktı dosyalarına yazmıştı (K123). Ölçüm hattı v7 ve v8 koşularında da aynıydı;
aynı kaymanın **daha önce** olup olmadığı bilinmiyordu. ⛔ Olsaydı, yayımlanmış
v7/v8 sayıları etkilenirdi.

⭐ Denetim v9 rubriğine bağlı değil: judge'ın **cevaptan** yaptığı uzun
alıntıların hangi kayda ait olduğuna bakar ve bu alıntıları v3'ten beri her
rubrik yazıyor. ➡️ Arşivler **yeniden puanlanmadan** denetlenebiliyor. Karar
kuralı `eslesme_denetimi()`'den **import edildi**; ileriye dönük kapıyla birebir
aynı kural uygulandı.

## Defter — arşivlenmiş her judge kararı

| Arşiv | rubrik | küme | SHA256 | kayıt | uzun alıntı | kendi cevabında | iç muhakemede | hiçbir yerde | **kayma** |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| `e2-5ae67873` | v7 | Eksen 2 | `4dcd87c147f2c1a6` | 20 | 62 | 62/62 (%100) | — | — | 0 |
| `e2-b7584bec` | v7 | Eksen 2 | `62406700f9097661` | 20 | 65 | 65/65 (%100) | — | — | 0 |
| `e2-220c3b5a` | v7 | Eksen 2 | `2b99b51197aab968` | 14 | 33 | 33/33 (%100) | — | — | 0 |
| `e2-99b69ab4` | v7 | Eksen 2 | `084a2d5591f5a8c7` | 20 | 63 | 63/63 (%100) | — | — | 0 |
| `e2-7ac7e984` | v7 | Eksen 2 | `2b1e281869436a92` | 20 | 68 | 68/68 (%100) | — | — | 0 |
| `e2-ceef5655` | v7 | Eksen 2 | `54e8299e20a60ffc` | 20 | 69 | 69/69 (%100) | — | — | 0 |
| `e2-hakem-p2` | v7 | Eksen 2 | `893a501ea710631f` | 54 | 160 | 159/160 (%99) | — | 1 | 0 |
| `e2-hakem-p3` | v7 | Eksen 2 | `263487f37a8d7ca9` | 54 | 173 | 173/173 (%100) | — | — | 0 |
| `v8-e2-5ae67873` | v8 | Eksen 2 | `50f482b40e4b166e` | 20 | 118 | 118/118 (%100) | — | — | 0 |
| `v8-e2-b7584bec` | v8 | Eksen 2 | `5995ce5d9784a1e4` | 20 | 106 | 106/106 (%100) | — | — | 0 |
| `v8-e2-220c3b5a` | v8 | Eksen 2 | `3fdafe814b841f4f` | 14 | 61 | 61/61 (%100) | — | — | 0 |
| `v8-e2-99b69ab4` | v8 | Eksen 2 | `077c9e1a4884ccb8` | 20 | 103 | 103/103 (%100) | — | — | 0 |
| `v8-e2-7ac7e984` | v8 | Eksen 2 | `959c26f3a936f081` | 20 | 117 | 112/117 (%95) | 5 | — | 0 |
| `v8-e2-ceef5655` | v8 | Eksen 2 | `03887eb7d7a57045` | 20 | 121 | 121/121 (%100) | — | — | 0 |
| `v8-hakem-p2` | v8 | Eksen 2 | `1bc2ebe9fd9d6a77` | 52 | 323 | 310/323 (%95) | 13 | — | 0 |
| `v8-hakem-p3` | v8 | Eksen 2 | `a53efa55a9256fcd` | 52 | 319 | 304/319 (%95) | 15 | — | 0 |
| `korpus-v3-claude` | v3 | korpus | `37f29fb6bb63a0c5` | 104 | 315 | 315/315 (%100) | — | — | 0 |
| `korpus-v7-sonnet` | v7 | korpus | `b1830ee1e1406591` | 104 | 336 | 336/336 (%100) | — | — | 0 |
| `korpus-v7-kontrol` | v7 | korpus | `33fa33ee7c9f7343` | 104 | 310 | 310/310 (%100) | — | — | 0 |
| `korpus-v7-ucuncu` | v7 | korpus | `f7fb42db5b185708` | 104 | 332 | 332/332 (%100) | — | — | 0 |
| `korpus-v8` | v8 | korpus | `94b9ac0948395a11` | 104 | 388 | 382/388 (%98) | — | 6 | **2** |
| `golden-baseline-claude` | v6 | golden.dev | `1cff3077ba21884b` | 48 | 177 | 177/177 (%100) | — | — | 0 |
| `golden-baseline-sonnet` | v6 | golden.dev | `80b96ea312b3466c` | 48 | 116 | 116/116 (%100) | — | — | 0 |
| `golden-v7-sonnet` | v7 | golden.dev | `433d08f8eae9319e` | 48 | 119 | 119/119 (%100) | — | — | 0 |
| `locked-baseline-1` | v7 | golden.locked | `1b7d18d304d5a249` | 48 | 111 | 111/111 (%100) | — | — | 0 |
| `locked-baseline-1-p2` | v7 | golden.locked | `0a69c374e636ceb7` | 48 | 122 | 122/122 (%100) | — | — | 0 |
| `locked-baseline-1-p3` | v7 | golden.locked | `5ae7775daab5f839` | 48 | 106 | 106/106 (%100) | — | — | 0 |
| `expert70-v7-sonnet` | v7 | expert-70 | `582a04d278869ff7` | 70 | 223 | 223/223 (%100) | — | — | 0 |
| `v4-parti1-v7` | v7 | v4-parti1 | `3d3513559d081ca8` | 40 | 137 | 137/137 (%100) | — | — | 0 |
| `doz-yama-v7` | v7 | doz yaması (ilk yama) | `9b5e50c381a55341` | 26 | 111 | 111/111 (%100) | — | — | 0 |
| `doz-yama-v7b` | v7 | doz yaması (yayımlanan) | `2f15d6aa8e0797eb` | 26 | 128 | 128/128 (%100) | — | — | 0 |
| **TOPLAM** | | | | **1410** | **4992** | **4952** (%99) | **33** | **7** | **2** |

⚠️ `kayıt` sütunu arşivin tamamıdır (1410); havuzda karşılığı bulunan kayıt **1410** — yani denetim dışı kalan kayıt **0**.

## ⛔ Bulundu: `korpus-v8`'de bir TAKAS

| arşiv | no | kayıt | kendi/alıntı | ait olduğu | o kayıtta bulunan |
|---|---|---|---|---|---:|
| `korpus-v8` | 075 | `0fd4ea080d66` | **0/2** | `2026a3e9ea66` | 2 |
| `korpus-v8` | 077 | `2026a3e9ea66` | **0/4** | `0fd4ea080d66` | 4 |

⭐ **İki kayıt karşılıklı yer değiştirmiş** — v9'daki 4'lü dönüşümden farklı,
temiz bir ikili takas. Komşu kayıtlar (074, 076, 078) temiz; yayılma yok.
Her iki kaydın alıntılarının **hiçbiri** kendi cevabında bulunmuyor,
**hepsi** ötekinin cevabında bulunuyor.

⛔⛔ **Kusur judge'da DEĞİL, yazma adımında.** İş dosyaları elle denetlendi:
`istek/075.txt` ve `istek/077.txt` **doğru** konuşmaları taşıyor. Yani judge
doğru okudu, sonuç **yanlış dosyaya yazıldı** — `korpus-v9-p2`'deki
004→005→006→007→004 dönüşümüyle **aynı kusur sınıfı**.

➡️ *Bu, o olayın tek seferlik bir kaza olmadığını gösteriyor:* aynı yazma
kusuru bu oturumun **iki ayrı partisinde** çıktı (`korpus-v8` ve
`korpus-v9-p2`). ⚠️ Kusurun oranı hâlâ ölçülmedi — bilinen tek şey, iki
kez olduğu.

### Etki — yayımlanmış sayılar değişiyor mu

| kayıt | arşivdeki bayraklar | takas düzeltilince |
|---|---|---|
| `0fd4ea080d66` | — | — |
| `2026a3e9ea66` | — | — |

| bayrak | korpus v8 (arşiv) | takas düzeltilince |
|---|---:|---:|
| `rol_siniri_ihlali` | 0 | 0 |
| `klinik_guvenlik_ihlali` | 1 | 1 |
| `bos_guvence` | 8 | 8 |
| `tuzak_suclama` | 0 | 0 |
| `tuzak_etiketleme` | 0 | 0 |

✅ **Yayımlanmış hiçbir sayı değişmiyor.** İki sebeple: (1) iki kaydın bayrak
kümesi her iki atamada da boş; (2) bir **takas** küme üzerindeki hiçbir
toplamı ya da ortalamayı oynatmaz — yalnızca kayıt BAŞINA karşılaştırmaları
oynatabilirdi ve onlar da aynı kaldı
(`2026-09-15-korpus-v9-kosusu.md` Ö2/Ö4: v7→v8 **9**, v8→v9 **14**, atıf 8/3/3).

⛔ **Ama bu şans.** Aynı takas bayraklı iki kayıtta olsaydı korpus v8
sayıları sessizce yanlış olurdu ve **hiçbir denetim uyarmazdı** —
`korpus-v8` arşivi eşleşme kapısından hiç geçmemişti: kapı yalnızca
`korpus-v9*` dosyalarına bakıyordu. ➡️ *Bir kapı, raporun OKUDUĞU her
arşivi kapsamıyorsa kapı değildir.*

### Ne yapıldı

| | |
|---|---|
| ✅ Kapı genişletildi | `korpus-v8` de eşleşme kapısından geçiyor; düzeltme olmadan korpus raporu **yazılmıyor** (sınandı: çıkış kodu 1) |
| ✅ Düzeltme **bildirim** olarak yazıldı | `reports/analiz/ham-judge/korpus-v8.takas.json` — okuma anında uygulanır |
| ⛔ Ham arşive **dokunulmadı** | arşivin işi *«subagent o dosyaya ne yazdı»*yı saklamak; üstüne yazmak kusurun kanıtını yok ederdi ve bu raporun SHA256'sını geçersiz kılardı |
| ✅ Doğrulandı | düzeltme uygulanınca `2026-09-15-korpus-v9-kosusu.md` **baytı baytına aynı** çıkıyor — etkinin sıfır olduğunun ampirik kanıtı |

⚠️ Bu, `korpus-v9-p2` olayında seçilen yoldan **farklı**: orada dört iş yeniden koşulmuştu (yeni kanıt üretildi). Burada yeni kanıta gerek yok — her iki judge çıktısı da **doğru**, yalnızca yanlış dosyada.

## ⚠️ Bulunamayan alıntılar — denetimin duyarlılığı

«kendi cevabında» sütunu denetimin o arşivde ne kadar görebildiğini söyler.
Bir alıntı kendi cevabında da bulunmuyorsa başka kayıtta bulunması da
beklenmez; ⛔ **yani her bulunamayan alıntı, bir kaymanın gizlenebileceği**
**bir deliktir.** İki sınıfın anlamı farklı:

⭐ **İç muhakemede bulunan 33 alıntı — T45'in ölçüsü.** Judge, cevabın
içine gömülü *«(iç muhakeme — değerlendirme dışı…)»* bloğundan alıntılayıp
hüküm kurmuş. v8'in kanıt denetimi bunu **aşama 1'de 7** vakada görmüştü;
bütün geçişler sayılınca v8 Eksen 2'de **33**
vaka çıkıyor. v9'un kapsam bölümü tam olarak bunun için yazıldı ve v9
arşivlerinde bu sayı kapı tarafından **karara bağlanıyor** (K120).

| arşiv | iç muhakemede | hiçbir yerde | okuma |
|---|---:|---:|---|
| `e2-hakem-p2` | — | 1 | ⭐ elle okundu: `A-dar`/`sk-011` cevabı **yozlaşmış** (547 kez *«hem»*); judge alıntının sonuna *«(bu şekilde yüzlerce kez tekrarlanarak devam ediyor)»* diye **kendi açıklamasını** eklemiş. Uydurma değil, şerh. |
| `v8-e2-7ac7e984` | 5 | — | T45 — kapsam kusuru; kaynağı belli, her alıntı iç muhakeme bloğunda bulundu |
| `v8-hakem-p2` | 13 | — | T45 — kapsam kusuru; kaynağı belli, her alıntı iç muhakeme bloğunda bulundu |
| `v8-hakem-p3` | 15 | — | T45 — kapsam kusuru; kaynağı belli, her alıntı iç muhakeme bloğunda bulundu |
| `korpus-v8` | — | 6 | ⛔ **takasın kendisi** — iki kaydın 6 alıntısı |

✅ **Bulunamayan 40 alıntının 40'ı da açıklandı:** 33'ü iç muhakemede (T45), 6'sı takas, 1'i yozlaşmış cevaba düşülmüş şerh. ➡️ Denetimin *göremediği* bir delik kalmadı.

## ⛔ Bu denetimin ölçmediği

- **Sonuç dosyası hiç yazılmamışsa.** Denetim var olan kayıtlara bakar.
- **Aynı kayda iki kez puan verilmişse.** Kimlik çakışması buradan görünmez.
- **Birbirine çok benzeyen iki cevap.** Takas ancak alıntı ötekinin cevabında
  bulunduğunda görünür; iki cevap aynıysa kayma görünmez kalır.
- **Muafiyet alanları.** Yalnızca *cevaptan* yapılan alıntılar kimlik belirler;
  `teselli_*` / `*_baglam_alintisi` denetime girmez.
- **v9 arşivleri** — `2026-09-15-v9-kapi-defteri.md`'de sayılıyor, burada tekrar
  edilmedi.
