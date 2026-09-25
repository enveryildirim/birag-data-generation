# `grounding` bir tek-ayrıntı sondasıdır

**Betik:** `scripts/analiz/2026-09-22-grounding-tek-ayrinti-sondasi.py` · **Tarih:** 2026-09-22  
**Girdi:** `data/judged/v6-parti{1,2,3}.jsonl` (160 Gemini yargısı)  

## Mekanizma

`grounding` judge'dan gelmez; `src/filter.py` **tek bir alandan** türetir:

```python
uydurma = (_dogrula(data, "en_somut_ayrinti", ...)
           and not data.get("ayrinti_konusmada_var")
           and not data.get("ayrinti_hipotez_olarak_isaretli"))
data["grounding"] = 2 if uydurma else 5
```

⛔⛔ Ölçü *«cevapta uydurma var mı»* diye **sormuyor**; *«judge'ın SEÇTİĞİ tek ayrıntı dayanaklı mı»* diye soruyor. Aynı cevapta hem dayanaklı hem uydurma bir ayrıntı varsa, puanı **seçim** belirler.

## ⭐⭐⭐ Eşli kanıt — aynı kayıt, iki judge

`v6-parti3 / 9bba8db7` bugünkü koşuda **eşli** kümedeydi: Gemini onu daha önce, Claude bugün yargıladı. Cevabın son cümlesi:

> *«…iki gündür aldığın bir ilaç, birbirini tutmayan iki yazı, **uyuyamadığın geceler** ve yanında kimse yok.»*

Kullanıcı uykudan **hiç söz etmiyor**.

| | Gemini | Claude |
|---|---|---|
| seçtiği `en_somut_ayrinti` | *«iki gündür aldığın bir ilaç»* | *«uyuyamadığın geceler»* |
| `ayrinti_konusmada_var` | `True` | `False` |
| ⇒ türetilen `grounding` | **5** | **2** |
| kendi `gerekce`'si | ⭐ *«…konuşmada geçmeyen uyuyamadığı ayrıntısını eklemektedir»* | *«…hiç söylemediği bir ayrıntıyı kesin bir liste içinde sunuyor»* |

⭐⭐⭐ **İki judge metin konusunda ANLAŞIYOR.** İkisi de uydurmayı gördü ve ikisi de gerekçesinde yazdı. Puanları ayıran şey sertlik değil, **hangi ayrıntıyı adlandırdıkları**.

⛔⛔ Bu, K45'in bir cümlesini niteler. K45 *«Gemini grounding'de 5.00 verdi — uydurulmuş «beş gece» hatasını **o da kaçırdı**»* diyordu. Burada Gemini **kaçırmadı**: gördü, yazdı, ve **ölçü onu attı**. ⇒ *«judge kaçırdı»* ile *«ölçü taşımadı»* ayrı şeyler ve grounding sayısı ikisini ayırt etmiyor.

## Tarama — ölçü kendi gerekçesiyle kaç kez çelişiyor

| | |
|---|---:|
| Gemini yargısı | 160 |
| `grounding` = 5 | 153 |
| `grounding` = 2 | 7 |
| ⛔ **5 ama gerekçe uydurma diyor** | **2** |

| kayıt | seçilen ayrıntı | konuşmada var? | gerekçe |
|---|---|---|---|
| `v6-parti2 / a66146ca` | *«İki yıl»* | `True` | Kullanıcının söylemediği bir durumu kendisi söylemiş gibi yansıtması ve diyaloğu sürdürecek bir keşif alanı aç |
| `v6-parti3 / 9bba8db7` | *«iki gündür aldığın bir ilaç»* | `True` | Kullanıcının yalnızlık hissine empatik yaklaşmak yerine doğrudan düzeltme refleksiyle itiraz etmekte ve konuşm |

⛔⛔ **Bu sayı bir ALT SINIRDIR ve seziciye güvenilmez.** Çelişkiyi arayan şey `gerekce` üzerinde koşan **düz bir düzenli ifade** — yani T22 serisinin tam olarak uyardığı biçim. Ayrıca `gerekce` tek cümledir: bir uydurma varken judge'ın ondan söz etmemesi olağan ⇒ görülmeyenler sayılamaz. ⭐ Asıl kanıt sayıda değil, **eşli vakadadır**: orada mekanizma doğrudan görülüyor.

## ⭐ Bu ölçümün koşuya etkisi

| | |
|---|---|
| ⛔⛔ **`grounding` farkı bir SERTLİK farkı sayılamaz** | iki judge arasındaki `grounding` ayrışması **örnekleme** farkından gelebilir (hangi ayrıntı seçildi) ⇒ Claude↔Gemini kalibrasyonunda bu boyut böyle okunmalı |
| ⭐ **K98'in tabanı bu boyutta %100'dü** | yani judge kendisiyle hep aynı ayrıntıyı seçiyor; ⛔ ama **aynı judge** demek **aynı seçim eğilimi** demek ⇒ yüksek taban, sondanın dar olduğunu gizler |
| ⚠️ **Onarım önerisi ölçülmedi** | *«bu benim önerim»*: alan **çoğul** olmalı (`en_somut_ayrintilar`) ya da ayrı bir *«başka dayanaksız ayrıntı var mı»* sorusu eklenmeli. İkisinin de maliyeti ve yanlış-pozitif oranı ölçülmedi |

## ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔ **Uydurma SIKLIĞI ölçülmedi** | ölçülen şey, ölçünün bir uydurmayı taşıyıp taşımadığı; korpusta kaç uydurma olduğu **hâlâ bilinmiyor** ve bu sonda ile bilinemez |
| ⛔ **İki vaka ELLE doğrulandı, ötekiler değil** | 160 yargının 158'inin gerekçesi okunmadı |
| ⚠️ **Claude tarafı henüz eksik** | bu tarama yalnız Gemini yargıları üzerinde koştu; Claude yargıları koşu bitince aynı betikle taranabilir |
