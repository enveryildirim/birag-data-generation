# Replay Türkçe kalitesi — kör sonda

**Sonda:** `prompts/turkce-dogallik-sondasi.v1.md` · **Model:** `agy:gemini-3.8-flash-high`  
**Betik:** `scripts/analiz/2026-09-14-replay-turkce-kalitesi.py` · **Tarih:** 2026-09-14 · **Tohum:** 4242 · **Grup başına:** 25 metin · **Uzunluk bandı:** 150-400 karakter  
**Ham çıktı:** `reports/analiz/replay-turkce-kalitesi/sonda-ciktilari.jsonl` · SHA256 `ab8dd585ee3cc0be929e75dd260b400cec6a36a9160729daee3db874ece2cf42`

---

## 0. Yöntem ve sınırları

K88 replay kaynaklarının makine çevirisi olduğunu işaretlemiş ama **ölçmemişti**. Dil doğallığı bu projenin ana kalite ekseni (K48, §5d).

**Belirlenimli işaretler denendi ve elendi:** *"bir" yoğunluğu* üç korpusta da aynı çıktı (0.035-0.036); *kelime tekrarı* konusal olduğu için kusur ölçmüyor ("hidroelektrik" × 3 bir çeviri hatası değil). Bu yüzden LLM sondası kullanıldı.

**Sonda K62'ye göre kuruldu:** soyut puan sorulmuyor, **alıntılanabilir kanıt** isteniyor — kusur varsa metinden birebir alıntı ve doğal karşılığı.

> ⚠️ **Araç kendi üzerinde sınanıyor.** Aynı sonda bizim **elle yazdığımız** BıRAG metinlerine de koşuldu. Sonda ikisini ayırt edemezse araç işe yaramaz (K61'in şartı).

> ⚠️ **Kontrol edilemeyen karıştırıcı:** iki korpus **tür** olarak farklı — bizimkiler terapötik diyalog, Alpaca açıklayıcı talimat-cevap. Sonda diyalog parçalarını "eksik cümle" sanabilir. Bu yüzden yalnızca **büyük** farklar yorumlanır.

## 1. Sonuç

| Grup | n | kusur bulunan | hata |
|---|---:|---:|---:|
| TFLai/Turkish-Alpaca | 25 | 20 (%80) | 0 |
| merve/turkish_instructions | 23 | 19 (%83) | 2 |
| BıRAG (elle yazılmış) | 25 | 4 (%16) | 0 |

## 2. Sondanın alıntıladığı kusurlar

### TFLai/Turkish-Alpaca

| tür | alıntı | doğal hâli |
|---|---|---|
| ceviri_kokusu | düşünceler ve duygular hakkında farkında olmasına | düşünce ve duyguların farkında olmasına |
| ceviri_kokusu | büyüsünü kullandığı ünü olan | büyüsünü kullanmasıyla ün salmış |
| ceviri_kokusu | Diğer ilk 10 eyalet | İlk 10'daki diğer eyaletler |
| ceviri_kokusu | Tesla'nın elektrikli arabalarına genel halk görüşü | Tesla'nın elektrikli arabalarına yönelik genel görüş |
| ceviri_kokusu | köyün ötesine cesur maceracıların gittiği ve harika hikayelerle geri d | köyün ötesine gidip harika hikayelerle geri dönen cesur maceracıların  |
| ceviri_kokusu | 2AM | 02:00 |

### merve/turkish_instructions

| tür | alıntı | doğal hâli |
|---|---|---|
| ceviri_kokusu | girişim desteklidir | girişim sermayesi desteklidir |
| soz_dizimi | Haziran 7 | 7 Haziran |
| soz_dizimi | eğitilmelidir. Anka kuşu." | eğitilmelidir. |
| ceviri_kokusu | birden fazla talep arasında denge kurmayı | farklı sorumluluklar arasında denge kurmayı |
| ceviri_kokusu | başkalarını motive etme ve ilham verme | başkalarını motive etme ve onlara ilham verme |
| ceviri_kokusu | motive ve ilhamlı kalacağım | motivasyonumu ve ilhamımı koruyacağım |

### BıRAG (elle yazılmış)

| tür | alıntı | doğal hâli |
|---|---|---|
| ceviri_kokusu | İki gün tuttun. | İki gün dayandın. |
| ceviri_kokusu | Sence o boşluğa ne girerdi? | Sence o boşluğu ne doldururdu? |
| ceviri_kokusu | Bunu bir karar olarak vermediğini | Böyle bir karar almadığını |
| ceviri_kokusu | fikir şimdi, yeni şehirde geri geldi | bu düşünce şimdi, yeni şehirde tekrar aklına geldi |

## 3. Ayrım anlamlı mı

Kontrol grubu **BıRAG (elle yazılmış)**. Her kaynak ona karşı sınanıyor. Fisher kesin testi, iki yanlı. "Büyük fark" eşiği **30 puan** — bu bizim konvansiyonumuz, literatürden gelmiyor (Kural 6).

| Grup | kusur | oran | %95 Wilson | kontrole karşı | Fisher p |
|---|---:|---:|---:|---:|---:|
| TFLai/Turkish-Alpaca | 20/25 | %80 | %61-91 | +64 p | 1.2e-05 |
| merve/turkish_instructions | 19/23 | %83 | %63-93 | +67 p | 6.9e-06 |
| BıRAG (elle yazılmış) | 4/25 | %16 | %6-35 | — (kontrol) | — |

**Sonda ayırt ediyor.** İki kaynağın da kontrolden farkı 30 puanın üstünde (+64 p ve +67 p) ve iki testte de p < 0.05 (en büyüğü 1.2e-05). K61'in şartı sağlandı: araç kendi üzerinde sınandı ve iki tarafı ayırdı.

## 4. Okuma

- **Yanlış pozitif tabanı %16.** Sonda elle yazdığımız 25 metnin 4'ini işaretledi. §2'deki BıRAG alıntıları buna örnek: *"İki gün tuttun"* bağlamında doğru bir Türkçe. Yani kaynaklardaki %80'lik oranın bir kısmı da gürültüdür; fark gerçek, mutlak seviye şişkindir.
- **Tür karıştırıcısı bulgunun aleyhine çalışıyor.** Karıştırıcı, sonda diyalog parçalarını "eksik cümle" sanacağı için **bizim** metinlerimizde daha çok işaret beklenmesini gerektirirdi. Gözlenen tersi: kontrol grubu (%16) her iki kaynaktan da düşük. Karıştırıcı farkı yaratmıyor, küçültüyor.
- 2 çağrı 3 denemede de zaman aşımına uğradı (K86) ve paydadan düşürüldü; işaretli sayılmadı.
- Bu ölçüm **kusurun varlığını** gösterir, **eğitime etkisini** göstermez. Replay diliminin Türkçeyi bozup bozmadığı ancak ablasyonla (Faz 5, replay oranı) bilinir. Bu rapor o ablasyona girdi verir, yerine geçmez.

