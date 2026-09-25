# §15 yasak ifade taramasında ek kusuru

**Betik:** `scripts/analiz/2026-09-18-yasak-ifade-eki.py` · **Tarih:** 2026-09-18

⛔⛔ **Kusuru inceleme kuyruğu buldu** — 2026-09-12'den beri okunmamış kuyruk.
`bos_guvence` altında çıkan satır bir boş güvence değil, tam tersiydi:
*«…sayıyı yine de merak ETMEK bunları geçersiz kılmıyor»*. Sebep düz alt dizge
araması: *«merak etme»* (olumsuz emir), *«merak etmek»*in (mastar) içinde.

➡️⭐⭐ *Okunmayan bir sinyal, sinyal değildir — ve okunmadığı sürece onu üreten
kusur da görünmez.*

## 1. ⭐ Regresyon — yumuşak kategoriler

| beklenti | vaka | cümle | sonuç |
|---|---|---|---|
| ⛔ yakalanmalı (gerçek boş güvence) | Merak etme, her şey yoluna girecek. | `{"bos_guvence": ["merak etme", "her şey yoluna girecek"]}` | ✅ |
| ⭐ geçmeli (⭐ mastar — kip başka) | Sayıyı merak etmek bunları geçersiz kılmıyor. | `—` | ✅ |
| ⭐ geçmeli (⭐ zarf-fiil — kip başka) | Sayıyı merak etmeden önce fark etmişsin. | `—` | ✅ |
| ⛔ yakalanmalı (tek sözcük + Türkçe ek) | Dozu azaltan hekim bunu bilir. | `{"rol_siniri": ["doz"]}` | ✅ |
| ⛔ yakalanmalı (tek sözcük, çekimsiz) | Teşhis koymak benim işim değil. | `{"rol_siniri": ["teşhis"]}` | ✅ |
| ⛔ yakalanmalı (çok sözcüklü, sınırda biter) | Bunu herkes yapıyor zaten. | `{"zararli_normallestirme": ["herkes yapıyor"]}` | ✅ |
| ⛔ yakalanmalı (etiketleme) | Sen bağımlısın. | `{"etiketleme": ["bağımlısın"]}` | ✅ |
| ⭐ geçmeli (⭐⭐ «keş» ≠ «keşke» — çekim değil, başka sözcük) | "Keşke kavga etseydik" cümlesinin altında kavga isteği yok. | `—` | ✅ |
| ⛔ yakalanmalı (tek sözcük + iyelik eki) | Dozun eskisi gibi işlememesi başka bir şey. | `{"rol_siniri": ["doz"]}` | ✅ |

⭐ **9 vakanın hepsi beklendiği gibi.**

## 2. ⛔⛔ Sert kategori — DEĞİŞTİRİLMEDİ ve neden

`kriz_yasagi`'da eşleşme aynen korundu. Aşağıdaki tablo kapının BUGÜNKÜ
davranışını gösteriyor — üç cümlenin üçü de düşüyor, oysa yalnız biri ihlal:

| vaka | cümle | kapı | doğru mu? |
|---|---|---|---|
| gerçek ihlal | Bana söz ver, bir daha içmeyeceksin. | ⛔ düşürür | ✅ doğru |
| ⛔⛔ DOĞRU REDDİ DE DÜŞÜRÜYOR | Senden bana söz vermeni istemiyorum. | ⛔ düşürür | ⛔ **YANLIŞ POZİTİF** |
| ⛔ aktarım da düşüyor | Bana söz verdiğini söyledin. | ⛔ düşürür | ⛔ **YANLIŞ POZİTİF** |

⚠️ **Sözcük sınırı kuralı buraya UYGULANMADI** çünkü uygulanırsa
*«bana söz verir misin»* kaçar ⇒ güvenlik ekseninde **yanlış negatif** doğar.
*«Güvenlik ekseninde gerileme kabul edilebilir değildir»* (Kural 3).

➡️⛔⛔ **Doğru çözüm ifade listesini düzeltmektir ve o bir UZMAN KARARIDIR.**
Bugünkü hâliyle kapı, *«Senden bana söz vermeni istemiyorum»* diyen — yani
§15'in tam olarak istediğini yapan — bir kaydı **sessizce eler**. Korpusta
böyle bir cümle bugün **yok** (ölçüldü: bütün korpuslarda `kriz_yasagi` 0 vuruş),
ama kapı o cümle yazıldığı gün onu silmeye hazır bekliyor.

## 3. ⛔ Bedel

Bütün korpuslar · **5642** kayıt.

| kategori | önce | sonra | fark |
|---|---:|---:|---:|
| `rol_siniri` | 26 | 26 | +0 · |
| `zararli_normallestirme` | 9 | 9 | +0 · |

| `passed` değeri dönen kayıt | **0 tekil** |
|---|---|

⭐⭐ **Hiçbir kaydın kararı dönmedi** — düzeltme yalnız YUMUŞAK kategorileri etkiledi, yani inceleme kuyruğunu temizledi, eleme davranışını değil. ⚠️ Tek sözcük kuralının bugünkü bedeli **sıfır**, çünkü *«keşke»* asistan cevaplarında henüz hiç geçmiyor (kullanıcı turlarında 9, `thinking`'de 9). ➡️ *Ölçülen bedelin sıfır olması, kuralın gereksiz olduğu anlamına gelmez: bazı düzeltmeler bugünü değil, tuzağın kurulduğu günü hedefler.*

## ⛔ Bu düzeltmenin söylemedikleri

| | |
|---|---|
| ⛔⛔ **Sert kapının yanlış pozitifi DURUYOR** | *«bana söz vermeni istemiyorum»* hâlâ düşer; Kural 3 gereği dokunulmadı, uzman kararı bekliyor |
| ⭐ **Tek sözcük kuralı kapatıldı** | kök yalnız AD ÇEKİM EKİ alabilir; *«keş»* artık *«keşke»*ye bağlanmıyor. ⚠️ Ama ölçülen bedel **0**: tuzak henüz `content`te hiç ateşlememişti ⇒ bu bir ÖNLEYİCİ düzeltme, sayıya yansımıyor |
| ⛔ **Fiil çekimi kapsam dışı** | liste AD çekimi için; *«geçecek»* → *«geçecekti»* eşleşmez. Çıplak biçim yine yakalanır, türemiş kip yakalanmaz |
| ⚠️ **Liste sözlüğe bağlı** | `configs/filters.yaml`'da olmayan bir ihlal ne kapıya ne kuyruğa girer |
