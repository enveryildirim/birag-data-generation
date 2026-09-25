# Ön kayıt — «yönlendirmeme refleksi» hipotezi karşı olgusalla sınanıyor

**Tarih:** 2026-09-17 · **Yazıldığı an:** korpuslar kuruldu, **hiçbir eğitim koşulmadı.**

⛔ **Bu dosya sonuç GÖRÜLMEDEN yazılmıştır** (T117 ve §8c′ ön kayıtlarıyla aynı
usul): tahmin önce yazılır, sonra ölçülür, tutmazsa **tutmadığı yazılır**.

---

## 1. Hipotez (T132'den)

Üç kapsam taraması (17 kol, 8→42 katman, 1→5 anahtar, rank 8→32, iki veri seti)
ince ayarın profesyonel yönlendirme refleksini sildiğini gösterdi. İki açıklama
ölçülüp **çürüdü**:

| açıklama | nasıl çürüdü |
|---|---|
| *«Kapsam çok geniş»* | hasar kapsamı izlemiyor (Spearman +0.36 / +0.25 / −0.25, n=7'de hepsi anlamsız) |
| *«Veride yönlendirme az»* | ÇAPA kol: veri 3,7 kat, yönlendirme kaydı 3,2 kat büyüdü, **sayı değişmedi** (4 → 4) |

⭐ **Kalan aday:** korpus yönlendirmeyi az öğretmiyor, **yönlendirMEMEYİ çok**
öğretiyor. Ret/özerklik kalıbı `v0.0.2` %22,2 → `v0.0.8` **%32,2**; yönlendirmeye
oranı 1,2× → **1,9×**.

---

## 2. Kollar — hepsi `h1` kapsamıyla (8 katman, `q_proj`, rank 8)

⭐ Kapsam kasten **en dar** olan seçildi: hasarın en az olduğu kol (4) ve
K50'nin *«en dar»* arayışının ucu. Taban kol **zaten eğitilmiş**.

| kol | korpus | durum |
|---|---|---|
| **TABAN** | `datasets/v0.0.8` | ✅ eğitildi (`h1-capa-k8`) · yönlendirme-yok **4** |
| **A** | `data/ablasyon/v0.0.8-A-ilan-seyreltilmis.jsonl` | ⏳ eğitilmedi |
| **P** | `data/ablasyon/v0.0.8-P-plasebo.jsonl` | ⏳ eğitilmedi |

⚠️ A ve P, `h1` config'inin **yalnız `dataset:` satırı** değiştirilerek koşulur.
LR, tohum, adım, batch, kapsam: **birebir aynı**.

---

## 3. Korpusların ÖLÇÜLMÜŞ özellikleri

| | yönlendirmeme | `ret_tavsiye` | `özerklik` | `ret_bilgi` | **yönlendirme** | checks | kelime |
|---|---:|---:|---:|---:|---:|---:|---:|
| TABAN | **184** (%32,2) | 13 | 60 | 139 | **96** (%16,8) | ✅ 0 | 31.848 |
| **A** | **140** (%24,5) | **1** | **7** | 136 | **96** (%16,8) | ✅ 0 | 31.347 |
| P | **184** (%32,2) | 13 | 60 | 139 | **96** (%16,8) | ✅ 0 | 31.460 |

⭐ **Tasarımın üç şartı da tutuyor:**
1. A hedefi oynatıyor (%32,2 → %24,5), P oynatmıyor.
2. **Yönlendirme sayısı üçünde de aynı (96)** — kontrol değişkeni sabit.
3. Üçü de `checks`ten geçiyor ve **kapı bayrakları birebir aynı** (7 zaman, 16 alıntı).

---

## 4. ⭐ Tahmin

**A kolunda yönlendirme-yok öğe sayısı 4'ten 3 veya altına inecek; P kolunda
4'te kalacak (±1).**

⚠️ Taban 1, hasar 4 ⇒ oynama alanı **yalnız 3 öğe**. Bu tahmin kaba ve n küçük.

---

## 5. ⛔⛔ Tahminin ŞİMDİDEN bilinen zayıflıkları

| | |
|---|---|
| ⛔⛔ **Manipülasyon zayıf ve bunun sebebi yapısal** | Hipotezin suçladığı şeyin büyük kısmı (`ret_bilgi`, 139 kayıt) **Kural 3'ün ZORUNLU kıldığı** şeyle aynı: *«ne olduğunu ben söyleyemem»* silinirse veri modele yorumlayabileceğini öğretir. Ablasyon ancak azınlığa (%32,2 → %24,5) dokunabiliyor ⇒ **negatif sonuç «hipotez yanlış» demek olmayacak**, «bu manipülasyon zayıftı» demek olabilecek |
| ⛔ **n = 20 öğe, oynama alanı 3** | tek öğe bir puandır; 4 → 3 gürültüden ayrılamaz |
| ⛔ **Tek tohum** | üretim deterministik (K105) ama tohum tek |
| ⛔ **Yakınsama yok** | `h1` 3 epoch'ta yakınsamamıştı (en iyi val son adımda); A ve P de yakınsamayacak |
| ⚠️ **Kelime dengesizliği** | A −501 kelime, P −388 kelime (fark 113, korpusun %0,36'sı) — eşitlenmedi |
| ⚠️ **`ret_bilgi` 139 → 136** | üç kayıtta silinen ilan cümlesi **aynı anda** bir `ret_bilgi` kalıbı da taşıyordu (*«senin kararın, orası bana düşmez»*) ⇒ hedef dışı küçük bir sızıntı, ölçüldü ve yazıldı |
| ⛔ **Ablasyon korpusu YAYIMLANAMAZ** | MI ekseninde daha kötüdür (özerklik vurgusu MI'nin ilkesi) ve `datasets/` altına yazılmadı; tek amacı bir değişkeni yalıtmak |

---

## 6. ⭐ Asıl hedef bu DEĞİL — ve o da ölçüldü

Ablasyon kurulurken daha keskin bir desen çıktı:

**Yorumlamayı reddeden kayıtların %58'inde DEVRETME YOK.**

| sürüm | `ret_bilgi` taşıyan | devretme var | ⛔ **çıkmaz** |
|---|---:|---:|---:|
| `v0.0.5` | 30 | 15 | **15** (%50) |
| `v0.0.7` | 51 | 22 | **29** (%57) |
| `v0.0.8` | 139 | 58 | **81** (%58) |

➡️⭐⭐ *Bugün tek bir judge bulgusundan yazdığım **§5a⁗** («reddetmek devretmeyi
gerektirir»), meğer korpus çapında bir desenmiş: 81 kayıt modele «söyleyemem»
öğretip «kimin söyleyebileceğini» öğretmiyor.*

⛔ **Bu 81 kayıt bu ablasyonda DÜZELTİLMEDİ ve nedeni yazılı:** düzeltmek
**cümle eklemek** demek, yani yeniden yazmak. *Bir ablasyonda silinir, yeniden
yazılmaz* — yeniden yazmak iki şeyi birden değiştirir. Üstelik 81 kayda
şablonla cümle eklemek, bugün ölçülen kalıp kusurunun (`tuzak_uzman`, 26 kayıt)
aynısını üretirdi.

⇒ ⭐ **81 kaydın §5a⁗ ile düzeltilmesi ayrı bir ÜRETİM işidir** ve normal
döngüden geçmelidir: üret → kapı → judge → derle. Hedef listesi
`reports/analiz/2026-09-17-cikmaz-kayitlar.json`.
