# LoRA kapsam merdiveni — ÜÇÜNCÜ tarama (`datasets/v0.0.8`)

**Betik:** `scripts/analiz/2026-09-17-kapsam-merdiveni-raporu.py` · **Tarih:** 2026-09-17

⛔ Önceki iki tarama (`f4b`, `f4c`) `v0.0.5` üzerindeydi ve **beş kolun beşi de**
Eksen 2'de elendi. Bu tarama `v0.0.8` (571 kayıt) üzerinde ⇒ eski sayılarla
**karşılaştırılamaz**; karşılaştırma iki ÇAPA kol üzerinden kurulur.

**Taban (Faz 3, K105/K106):** Eksen 2 **11/20** · yönlendirme-yok **1** öğe · Eksen 3 **28/30**

## 1. Merdiven

| kol | katman | anahtar | rank | train loss | en iyi val | E2 geçen | **E2 yönl.-yok** | E3 | **kapı** |
|---|---:|---:|---:|---|---|---|---:|---|---|
| `h1-capa-k8` | 8 | 1 | 8 | 2.622 | 2.654 | 10/20 | **4** | *ölçülmedi* | ⛔ elendi (+3) |
| `h2-k16` | 16 | 1 | 8 | 2.365 | 2.428 | 7/20 | **9** | *ölçülmedi* | ⛔ elendi (+8) |
| `h3-k24` | 24 | 1 | 8 | 2.133 | 2.209 | 7/20 | **13** | *ölçülmedi* | ⛔ elendi (+12) |
| `h4-k32` | 32 | 1 | 8 | 2.045 | 2.126 | 7/20 | **13** | *ölçülmedi* | ⛔ elendi (+12) |
| `h5-k16-qo` | 16 | 2 | 8 | 2.007 | 2.073 | 6/20 | **14** | *ölçülmedi* | ⛔ elendi (+13) |
| `h6-k24-qo` | 24 | 2 | 8 | 1.725 | 1.856 | 8/20 | **10** | *ölçülmedi* | ⛔ elendi (+9) |
| `h7-k24-qo-r16` | 24 | 2 | 16 | 1.594 | 1.809 | 11/20 | **8** | *ölçülmedi* | ⛔ elendi (+7) |
| `h8-capa-k42-qo` | 42 | 2 | 8 | ⛔ **YARIM** | — | *koşulamaz* | — | — | ⛔ eğitim kesildi |

| **taban** | — | — | — | — | — | 11/20 | **1** | 28/30 | — |

⭐ **Sert kapı:** `yonlendirme_yok` ≤ taban. §9 + Kural 3: *«güvenlik ekseninde gerileme kabul edilebilir değildir»*.


## 2. ⭐⭐ Kapsam, hasarı açıklıyor mu?

| kol | katman | kapsam\* | val | **yönl.-yok** |
|---|---:|---:|---:|---:|
| `h1-capa-k8` | 8 | 64 | 2.654 | **4** |
| `h7-k24-qo-r16` | 24 | 768 | 1.809 | **8** |
| `h2-k16` | 16 | 128 | 2.428 | **9** |
| `h6-k24-qo` | 24 | 384 | 1.856 | **10** |
| `h3-k24` | 24 | 192 | 2.209 | **13** |
| `h4-k32` | 32 | 256 | 2.126 | **13** |
| `h5-k16-qo` | 16 | 256 | 2.073 | **14** |

\* kapsam = katman × anahtar × rank (kaba parametre vekili)

| ilişki | Spearman ρ |
|---|---:|
| katman ↔ yönlendirme-yok | **+0.36** |
| kapsam ↔ yönlendirme-yok | **+0.25** |
| val kaybı ↔ yönlendirme-yok | **-0.25** |

⛔⛔ **Üçü de zayıf ve n=7'de hiçbiri anlamlı değil** (anlamlılık için |ρ| ≈ 0.75 gerekirdi). ➡️⭐⭐ *Her kol hasarlı (4–14, taban 1) ama NE KADAR hasarlı olduğu kapsamı izlemiyor. En dar kol en az hasarlı, ama ondan sonrası sıralanmıyor: `h7` (en büyük kapsam, en düşük val) `h3`'ten (üçte bir kapsam) **daha az** hasarlı.*

⇒ Kapsam, aranan değişken **değil**.

## 3. ⭐ Karar

⛔⛔ **Ölçülen 7 kolun 7'i de sert kapıda elendi.** Üçüncü tarama da aynı sonucu verdi.

⭐⭐ **Ve ÇAPA kol sorunun ne OLMADIĞINI gösterdi.** `h1-capa-k8`, eski `A-dar` ile **birebir aynı kapsam** — tek fark veri. Eski koşuda (`v0.0.5`, 155 kayıt, 30 yönlendirme kaydı) yönlendirme-yok **4**'tü; yeni koşuda (`v0.0.8`, 571 kayıt, 96 yönlendirme kaydı) yine **4**.

➡️⭐⭐⭐ *Veriyi 3,7 kat, yönlendirme kaydını 3,2 kat büyütmek aynı kapsamda HİÇBİR ŞEYİ değiştirmedi. «Veride yönlendirme az» açıklaması böylece iki yönden birden çürüdü: pay ölçüldü (sabit, %17-19) ve miktar denendi (etkisiz).*

➡️ *Ve bu bir kapsam sorunu da değil.* Kapsam üç taramada toplam **17 kolda** tarandı (8→42 katman, 1→5 anahtar, rank 8→32, iki ayrı veri seti) ve üçünde de bağlayıcı kapı aynı yerde; üstelik hasar kapsamı izlemiyor (Bölüm 2).

⇒ ⭐ **Geriye ölçülmüş tek aday kalıyor:** korpus yönlendirmeyi az öğretmiyor, **yönlendirMEMEYİ çok** öğretiyor — ret/özerklik kalıbı `v0.0.2` %22,2'den `v0.0.8` %32,2'ye çıktı ve yönlendirmeye oranı 1,2× → 1,9× oldu (`2026-09-17-yonlendirmeme-refleksi.md`). ⛔ Bu bir **hipotez**; karşı olgusal korpus yok.

⛔ Eksen 1 (kalite) **koşulmadı** — sert kapıyı geçen kol yok (K97).
⛔ Eksen 3 (unutma) **koşulmadı** — §9'un Pareto sırası gereği sert kapıyı geçemeyen kol için gereksiz iş (ve makine ısınması nedeniyle bilerek atlandı).

## ⛔ Bu taramanın söylemedikleri

| | |
|---|---|
| ⛔ **Tek tohum** | üretim deterministik (K105) ama tohum tek; başka tohumla sıralama değişebilir ve bu ölçülmedi |
| ⛔ **n küçük** | Eksen 2'de 20 öğe, Eksen 3'te 30; tek öğe bir puandır |
| ⛔ **Kalite ölçülmedi** | Eksen 1 yalnız sert kapıyı geçen kollar için koşulur |
| ⚠️ **Eksen 3 bir alarm, kapı değil** | eşik konmadı; 28/30 taban yalnız referans |
| ⚠️ **`safety_crisis` ölçütünün kendi kusuru var** (T31) | düzeltilmiş ikinci set ayrı raporda |
