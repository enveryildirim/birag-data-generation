# v5-parti8 üretildi — 60 kayıt, altı eksen +0.0, ölçüt üretim sırasında iki kez değişti

*2026-09-17 · `data/candidates/v5-parti8.jsonl` SHA256 `ad4276805d3f07c3` · 60 kayıt*

## 1. Kapılar

| kapı | sonuç |
|---|---|
| `src/checks.py` | **60/60** ✅ |
| zaman/kaynak atfı | **0 bayrak** |
| alıntı birebirlik | **0 bayrak** |
| ızgara↔tohum | **60/60 tam uyum, 0 uydurma** |
| beyanla kriz tohumu | SERT 0 · PERSONA 0 ✅ |
| altı eksen marjinali | hepsi **+0.0** |
| thinking:completion | ortanca **1.16x**, maks **2.15x** |

⚠️ `thinking:completion` ortancası partiler boyunca düşüyor: 1.62 → 1.72 →
1.48 → 1.16. Bu ölçülmedi ve **açıklanmadı**; thinking'in kısalması bir kalite
kaybı da olabilir, gereksiz tekrarın azalması da.

## 2. Altı ilan edilmiş sapma

| # | ölçüt maddesi | tablo |
|---|---|---|
| `#9` | md.4 | ergen + *«başım döndü»* |
| `#12` | md.2 + md.3 | *«bir tane daha alayım mı»* |
| `#18` | md.2 | *«belki ben de bir anda kessem»* |
| `#26` | md.1 | hafıza boşluğu |
| `#28` | md.1 | hafıza boşluğu |
| `#35` | md.1 + md.3 | *«tutundum»* + *«kime sorsam bilmiyorum»* |

⭐ `#9`'un ilanı bir ayrımı da yazıyor: aynı belirti (baş dönmesi) **yetişkinde**
md.1'in listesinde yok ve v5-parti7 `#59`'da sapılmamıştı. Fark belirtiden
değil **yaştan** geliyor.

## 3. ⛔⛔ Ölçüt üretim sırasında İKİ KEZ değişti

| ne | neden |
|---|---|
| **md.2 daraltıldı** (reçeteli ilaç kararı) | geniş hâli *«bu akşam çok içerim»*i de kapsıyordu; bedel sayı değil **araç uyuşmazlığı** — oraya yönlendirme koymak fazladan değil **yanlış** bir cevap verir |
| **md.1 genişletildi** (kollapsa yaklaşma) | `#35` *«tutundum»* diyordu ve ölçüt kapsamıyordu; **esnetmek yerine değiştirmek** seçildi — esnetmek T115'in ölçtüğü denetlenemezliği geri getirir |

## 4. Sapma dizisi ve neden okunamıyor

| | parti3 | parti4 | parti5 | parti6 | parti7 | parti8 |
|---|---:|---:|---:|---:|---:|---:|
| güvenlik sapması | 3 | 5 | 1 | 6 | **5** | **6** |

§5a″ öncesi (parti3–6): ortalama **3.75**, aralık **5**.
§5a″ sonrası (parti7–8): ortalama **5.5**, aralık **1**.

⛔⛔ **Bu tablodan «§5a″ varyansı düşürdü» ÇIKARILAMAZ**, iki sebeple:

1. **n=2.** İki gözlemin aralığı 1 çıkması beklenen bir şey.
2. ⛔ **Ölçüt iki parti arasında iki kez değişti.** parti7 ile parti8 **aynı
   ölçüt altında üretilmedi** ⇒ seviye karşılaştırması da sallantılı.

➡️ *Kendini düzelten bir ölçüt, kendi etkisinin ölçülmesini zorlaştırıyor:
her düzeltme karşılaştırmanın temelini kaydırıyor. Ölçütü dondurmadan etkisini
ölçmek mümkün değil — ama dondurmak da bulunmuş kusurları yaşatmak demek.*

## ⛔ Bu raporun söylemedikleri

- Judge geçmedi; hiçbir sayı kalite ölçümü değil.
- v5'in üç bahsi hâlâ ölçülmedi (v0.0.8 eğitimi bekliyor).
- `thinking:completion` düşüşü açıklanmadı.
- Sapmaların DOĞRU olduğunu söyleyecek ikinci okuyucu yok (K30).
