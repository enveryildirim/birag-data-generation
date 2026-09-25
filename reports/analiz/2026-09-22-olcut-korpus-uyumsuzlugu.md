# Ölçüt, korpusun öğretmediği bir davranışı ölçüyor

**Betik:** `scripts/analiz/2026-09-22-olcut-korpus-uyumsuzlugu.py` · **Tarih:** 2026-09-22  
**Ölçüt:** `safety_crisis`'in **kriz kutuplu 15 ögesi**, her biri 0/1/2 ⇒ tavan **30**  
**Korpus:** `datasets/v0.0.18` (1033 kayıt)  

## ⛔⛔⛔ Asıl bulgu

| | |
|---|---:|
| korpusta `is_crisis` kaydı | **0** |
| yönlendirme terimi geçen cevap | 188 (%18.2) |
| ölçüte göre *«devrediyor»* (derece 2) | 101 (%9.8) |

⛔⛔⛔ **Korpusta kriz kaydı YOK** — kriz dilimi **uzman onayına kadar bekletiliyor** (Kural 3). Ölçüt ise yalnız kriz ögelerinde yönlendirme arıyor.

➡️⭐⭐⭐ *Bu bir ÖĞRENME sınaması değil, bir **dağılım dışı aktarım** sınamasıdır. Korpusa kriz içermeyen kayıt eklendiği sürece bu ölçüt kıpırdamaz — ve T245/T246'nın «fark okunamadı» sonucu ölçüm gücünün değil bu YAPISAL uyumsuzluğun sonucudur.*

## Belirti — ölçüt neden bu kadar oynak

| kol | sabit öge | ortalama | en düşük–en yüksek |
|---|---|---:|---|
| z-h9 (571) | **4/15** | 6.38 / 30 | 3–11 |
| d1 (1033) | **5/15** | 5.12 / 30 | 0–11 |

⭐ Ortalamalar tavanın yalnız **%21**'i ve **%17**'i. Ögelerin üçte ikisi tohumlar arasında 0↔2 zıplıyor. ⇒ Model bu davranışı **kararlı biçimde öğrenmiş değil**; her tohum kendi idiosenkratik siyasetini üretiyor. Ölçütün oynaklığı bir ölçüm kusuru değil, **öğrenilmemişliğin belirtisi**.

⛔ **Üretim deterministik** (`temp=0.0`) ⇒ oynaklık örnekleme değil, gerçek model-model farkı. Okuma doğruladı: bir tohum krizde 112'ye yönlendiriyor, bir başkası konuyu karaciğere çeviriyor.

## Yan bulgu — T22 ailesinin 12. üyesi (ama aranan kusur DEĞİL)

`DEVRET` deseni **yalın emir kipini kaçırıyor**:

| ifade | eşleşiyor mu |
|---|---|
| `112'yi arayabilirsin` | ✅ |
| **`112'yi ara`** | ❌ |
| `hekimine sormak` | ✅ |
| **`hekimine sor`** | ❌ |
| `bir uzmandan yardım iste` | ❌ |

⚠️ Kriz yönlendirmesinde en doğal biçim emir kipidir ⇒ desen sistematik olarak **düşük puanlıyor**. ⛔ **Ama etkisi ölçüldü ve küçük:**

| kol | mevcut | genişletilmiş | kaçan 1→2 |
|---|---:|---:|---:|
| z-h9 (571) | 6.38 | 6.38 | 0 |
| d1 (1033) | 5.12 | 5.12 | 0 |

Fark: mevcut **-1.25** → genişletilmiş **-1.25** ⇒ ⭐⭐ **bulunan kusur gerçek ama aranan kusur değil.** Oynaklığı açıklamıyor ve iki kolun sırasını değiştirmiyor.

## ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Kriz dilimini üretmek bir ÇÖZÜM ÖNERİSİ DEĞİLDİR** | kriz davranışı kararı **uzman ve etik kuruluna** aittir (Kural 3); bu rapor eksikliği gösterir, doldurmayı önermez |
| ⛔ **Ölçüt yanlış değil, YERSİZ** | `safety_crisis` geçerli bir eksendir ve tabanın ölçülmesi doğruydu; yanlış olan, onu **korpus büyütmenin etkisini ölçmek için** kullanmaktı |
| ⚠️ **Desen boşluğu ONARILMADI** | etkisi ölçüldü, küçük çıktı; onarım ayrı bir karar ve ölçütün sürümünü değiştirir (K137: sürüm değişirse eski sayılarla karşılaştırma geçersiz) |
| ⚠️ **%9,8 «devrediyor» kaydı kriz DIŞI bağlamlardan** | korpus yönlendirmeyi öğretiyor, ama krizde değil |
