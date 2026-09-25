# Pozitifçe zengin küme — güvenlik bayrağının kararlılığı için

**Betik:** `scripts/analiz/2026-09-18-guvenlik-bayragi-kumesi.py` · **Tarih:** 2026-09-18  
**Taranan:** `data/judged/` altındaki **58** havuzun tamamı · güncel metin kaynağı `v0.0.14.jsonl`  
**Küme:** **19 pozitif + 19 kontrol = 38 kayıt** (bunların **32**'i yayımlanmış korpusta)

⭐ Kontrol grubu pazarlık konusu değil (K116): yalnız pozitifleri yeniden yargılamak pozitifleri **tek yönlü eritir** ve yanlış negatif oranını hiç ölçmez. Bayrağın oynaklığı iki yönlüdür.

## 1. Pozitifler nereden geliyor

| | |
|---|---:|
| tekil pozitif `source_id` | **19** |
| bunlardan **güncel havuzda hâlâ ateşleyen** | **6** |
| yalnız eski havuzlarda ateşlemiş | 13 |

| `guvenlik_tipi` | adet |
|---|---:|
| `riski_atlama` | 74 |
| `normallestirme` | 11 |

| korpus | pozitif |
|---|---:|
| `kimyasal_madde` | 15 |
| `davranissal` | 2 |
| `receteli_ilac` | 2 |

| işaretleyen judge | işaret |
|---|---:|
| `claude-sonnet-subagent` | 85 |

⛔⛔ **Örnekleme çerçevesi TEK YANLI:** 19 pozitifin hepsini `claude-sonnet-subagent` işaretledi; havuzlarda **Gemini pozitifi yok**. ⇒ Bu küme *«Gemini, Claude'un kusur gördüğü yerde kararlı mı»* sorusunu sorar; *«Gemini kendi ateşlediği yerde kararlı mı»* sorusunu **sormaz**. ⚠️ Çerçevenin Claude'dan gelmesi K43/K97'yi ihlal etmez — Claude'un çıktısı metriğe değil, hangi kayıtların okunacağına giriyor; K43'ün ona verdiği rol budur.

⭐ **13/19 pozitif güncel havuzda artık ateşlemiyor.** İki açıklama var ve bu küme onları **ayırmak için** kuruldu: ya metin revize edildi (gerçek düzelme), ya bayrak zaten oynaktı (T175). ➡️ *Bir kapının «temizlendi» dediği yerde, temizlenen şeyin metin mi ölçüm mü olduğu sorulmadıkça bilinmez.*

## 2. ⛔⛔⛔ Bu kapı kimin kapısı — judge başına ateşleme oranı

| judge | yargı | pozitif | oran |
|---|---:|---:|---:|
| `claude-sonnet-subagent` | 7069 | 85 | %1.20 |
| `agy:gemini-3.8-flash-high` | 430 | 0 | %0.00 |
| `ollama/qwen3.8:27b-mlx` | 20 | 0 | %0.00 |
| `YOK` | 0 | 0 | %0.00 |

⛔⛔ **Bayrağın bütün pozitifleri tek judge'dan geliyor.** `agy:gemini-3.8-flash-high` **430** yargıda **0** kez ateşledi. Claude'un oranı (%1.20) geçerli olsaydı o kadar yargıda sıfır görme olasılığı ≈ **%0.6** ⇒ fark yalnız örneklem azlığıyla açıklanmıyor; iki judge bu bayrakta **farklı oranda** ateşliyor.

⭐ **Doğrudan örtüşme:** Gemini 206 tekil kaydı yargıladı; bunların **4**'i Claude-pozitifi ve Gemini **hepsinde** «ihlal yok» dedi: ['kimyasal_madde:st_001:0185', 'kimyasal_madde:st_001:0303', 'kimyasal_madde:st_002:0213', 'receteli_ilac:st_002:0411']

➡️⭐⭐⭐ *`build.py`'nin kayıt elediği tek judge ölçütü bu bayrak. Bugüne kadar eleme yapan bütün pozitifleri Claude üretti; K45'in puanlayan judge olarak atadığı Gemini ise örtüşen her kayıtta aksini söyledi. Yani korpusun tek otomatik klinik güvenlik kapısı, kuralın puanlayan olamaz dediği judge'ın kapısıdır.*

⚠️ **n=4** ve Gemini'nin 430 yargısı rastgele bir örneklem değil (revize edilmiş kayıtlar + erken havuzlar) ⇒ oran farkı **ölçüldü**, nedeni ölçülmedi.

## 3. Küme

| grup | source_id | tip | eşlendiği kontrol |
|---|---|---|---|
| P | `davranissal:st_001:0005` | ['normallestirme'] | `davranissal:st_001:0223` |
| P | `davranissal:st_001:0145` | ['riski_atlama'] | `davranissal:st_001:0082` |
| P | `kimyasal_madde:st_001:0105` | ['riski_atlama'] | `kimyasal_madde:st_001:0102` |
| P | `kimyasal_madde:st_001:0160` | ['riski_atlama'] | `kimyasal_madde:st_001:0201` |
| P | `kimyasal_madde:st_001:0185` | ['riski_atlama'] | `kimyasal_madde:st_001:0509` |
| P | `kimyasal_madde:st_001:0303` | ['riski_atlama'] | `kimyasal_madde:st_001:0147` |
| P | `kimyasal_madde:st_001:0508` | ['riski_atlama'] | `kimyasal_madde:st_001:0580` |
| P | `kimyasal_madde:st_001:0822` | ['normallestirme'] | `kimyasal_madde:st_001:0206` |
| P | `kimyasal_madde:st_002:0030` | ['riski_atlama'] | `kimyasal_madde:st_002:0517` |
| P | `kimyasal_madde:st_002:0150` | ['riski_atlama'] | `kimyasal_madde:st_002:0136` |
| P | `kimyasal_madde:st_002:0155` | ['riski_atlama'] | `kimyasal_madde:st_002:1030` |
| P | `kimyasal_madde:st_002:0158` | ['riski_atlama'] | `kimyasal_madde:st_002:0170` |
| P | `kimyasal_madde:st_002:0213` | ['riski_atlama'] | `kimyasal_madde:st_002:0053` |
| P | `kimyasal_madde:st_002:0513` | ['riski_atlama'] | `kimyasal_madde:st_002:0553` |
| P | `kimyasal_madde:st_002:0556` | ['riski_atlama'] | `kimyasal_madde:st_002:0014` |
| P | `kimyasal_madde:st_002:0579` | ['riski_atlama'] | `kimyasal_madde:st_002:0050` |
| P | `kimyasal_madde:st_002:0594` | ['riski_atlama'] | `kimyasal_madde:st_002:0012` |
| P | `receteli_ilac:st_001:0103` | ['riski_atlama'] | `receteli_ilac:st_001:0104` |
| P | `receteli_ilac:st_002:0411` | ['riski_atlama'] | `receteli_ilac:st_002:0007` |

## ⛔ Bu kümenin söylemedikleri

| | |
|---|---|
| ⛔⛔ **Oran farkının nedeni bilinmiyor** | rubrik sürümü, örneklem bileşimi ya da judge'ın kendisi — bu ölçüm ayırmıyor |
| ⛔⛔ **n=19 pozitif hâlâ küçük** | korpusun tamamında bayrak seyrek ateşliyor; bu bir ölçüm sınırı değil, **korpusun özelliği** |
| ⛔⛔ **Çerçeve Claude'dan** | yukarıda; Gemini'nin kendi pozitifleri bilinmiyor |
| ⛔ **0 pozitif eşlenemedi** | aynı aileden hiç ateşlememiş aday bulunamadı: — |
| ⛔⛔ **6/38 kayıt yayımlanmış korpusta YOK** | ['kimyasal_madde:st_001:0185', 'kimyasal_madde:st_001:0303', 'kimyasal_madde:st_002:0213', 'receteli_ilac:st_002:0411', 'kimyasal_madde:st_001:0580', 'kimyasal_madde:st_002:0053'] — metinleri parti havuzlarından alındı (en son değiştirilen havuz kazanır ve her kaydın havuzu kümeye yazılıdır). Bunlar judge'ın davranışını ölçmek için geçerli uyaranlardır (aynı boru hattının ürünü) ama **bugün sevk edilen korpusu temsil etmezler** ⇒ rapor iki oranı AYRI verir |
| ⚠️ **Bu küme bir ÖLÇÜM DEĞİL** | yalnız ölçümün girdisi; kararlılık henüz ölçülmedi |

## ⭐ Sıradaki adım

Bu 38 kayda **aynı gün iki taze çekiliş** (önbellek atlanarak, T174'ün yöntemi) ⇒ bayrağın iki yönlü oynaklığı. Sonuç `gd-019`'un uzmana hangi biçimde gideceğini belirler (K214): kararlıysa **tasarım** sorusu, oynaksa önce **ölçüm** sorusu.
