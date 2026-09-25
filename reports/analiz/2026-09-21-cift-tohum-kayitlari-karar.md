# Aynı tohumdan iki kez üretilmiş kayıtlar — karar

**Betik:** `scripts/analiz/2026-09-21-cift-tohum-kayitlari-karar.py` · **Tarih:** 2026-09-21  
**Girdi:** `data/candidates/v6-parti{1..7}.jsonl` · 412 kayıt  

| | |
|---|---:|
| iki kez kullanılmış tohum | **37** |
| kayıt çifti | **37** |
| ⭐ **ilk kullanıcı mesajı** Jaccard ort. | **%29** (en yüksek **%100**) |
| birleşik kullanıcı turları Jaccard ort. | %35 |
| asistan turu Jaccard ortalaması | %12 |
| ⛔ ızgara hücresi TAMAMEN aynı olan çift | **0** |

## Ayrım: örtüşme nerede

⭐ Eşikler bir SEÇİM: kullanıcı turu ≥%50 «girdi yakın», asistan turu ≥%30 «hedef de yakın». Gerekçe: asistan turları ızgara hücresi farklıyken bile ortak sözcük taşır (aynı konu, aynı sözlük), o yüzden hedef eşiği girdi eşiğinden düşük tutuldu.

| sınıf | çift | ne demek |
|---|---:|---|
| ⛔⛔ **ezber riski** | **0** | girdi ve hedef birlikte yakın |
| ⭐ çeşitlilik | 6 | girdi yakın, hedef ayrı |
| — uzak | 31 | girdi zaten yakın değil |

### En yüksek girdi örtüşmesi — ilk mesaja göre (ilk 10)

| tohum | a | b | ilk mesaj | asistan | ızgara farkı |
|---|---|---|---:|---:|---|
| `06a8c120` | `v6-parti1#24` | `v6-parti3#39` | %100 | %12 | `konusma_durumu`, `senaryo_hedefi` |
| `5e52039e` | `v6-parti1#38` | `v6-parti3#33` | %72 | %9 | `register`, `konusma_durumu` |
| `0b86e8e0` | `v6-parti1#53` | `v6-parti4#23` | %66 | %19 | `turn_ending`, `konusma_durumu` |
| `0c45549c` | `v6-parti1#32` | `v6-parti3#10` | %59 | %18 | `bicim`, `konusma_durumu` |
| `14ee5db3` | `v6-parti1#57` | `v6-parti4#15` | %50 | %21 | `turn_ending`, `sinir_tipi`, `senaryo_hedefi` |
| `27b8199e` | `v6-parti1#45` | `v6-parti5#50` | %50 | %12 | `konusma_durumu`, `sinir_tipi`, `senaryo_hedefi`, `baglam_davranisi` |
| `122a11c1` | `v6-parti1#25` | `v6-parti3#55` | %48 | %14 | `bicim`, `konusma_durumu`, `senaryo_hedefi` |
| `0c9223ab` | `v6-parti1#20` | `v6-parti3#26` | %43 | %15 | `register`, `konusma_durumu`, `baglam_davranisi` |
| `09d85143` | `v6-parti1#15` | `v6-parti3#31` | %38 | %22 | `turn_ending`, `bicim`, `konusma_durumu`, `sinir_tipi`, `baglam_davranisi` |
| `063e7aeb` | `v6-parti1#21` | `v6-parti3#13` | %35 | %6 | `turn_ending`, `bicim`, `konusma_durumu` |

## ⭐⭐⭐ KARAR: HİÇBİRİ DÜŞMÜYOR

Gerekçe üç sayıda duruyor ve üçü de aynı yöne bakıyor:

1. **Hiçbir çiftte girdi ve hedef birlikte yakınlaşmıyor.** Asistan turu örtüşmesi ortalama %12, en yüksek %32.
2. **Hiçbir çift aynı ızgara hücresinde değil** (0/37); her çift en az bir hücrede ayrılıyor, yani iki kayıt aynı sahneyi FARKLI bir hamleyle yazıyor.
3. En yakın çiftte bile (v6-parti1#24 ↔ v6-parti3#39, ilk mesaj %100) hedefler ayrı: asistan örtüşmesi %12, ayrılan hücreler `konusma_durumu`, `senaryo_hedefi`.

⇒ Bunlar ince ayar açısından TEKRAR değil, aynı tohumun iki ayrı hücrede iki ayrı cevapla işlenmesi. Düşürmek çeşitliliği azaltır ve kapsama açıklarını büyütür.

⚠️ **Tek işaretli çift:** `v6-parti1#24` ↔ `v6-parti3#39` — ilk kullanıcı mesajları birbirinin sözcük sırası permütasyonu (*«Dozu iki ay önce artırdılar»* / *«İki ay önce dozu artırdılar»*). Hedefleri ve iki hücresi ayrı olduğu için kalıyor, ama kayda geçsin diye buraya yazıldı.

⛔⛔ **BU KARAR T225'İN SAYIM SORUNUNU ÇÖZMÜYOR** ve o açık kalıyor: kapsama envanteri tohumu bir kez sayıyor, korpus iki kayıt taşıyor ⇒ 37 tohumda envanterin gördüğü büyüklük ile korpusun taşıdığı büyüklük ayrışıyor. Düşürme kararı bunu kapatmaz; envanterin birimi değişmeli.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **İLK ÖLÇÜM FAZLA TOPLAYICIYDI ve düzeltildi** | bütün kullanıcı turları birleştirilince en yüksek örtüşme %72 görünüyordu; yalnız İLK MESAJA bakınca %100 örtüşen bir çift çıktı. Model ilk mesajda koşullanıyor ⇒ birim o olmalıydı |
| ⛔⛔ **Eşikler seçimdir, ölçüm değil** | %50 ve %30 gerekçeli ama türetilmedi; başka eşikle sınıf sayıları değişir ve tablo ham Jaccard'ları da veriyor ki karar denetlenebilsin |
| ⛔ **Jaccard anlamı değil örtüşmeyi ölçer** | iki farklı sahne aynı sözlüğü kullanıyorsa yüksek çıkar; ezber riski bir TAHMİNDİR, ölçülmüş bir eğitim etkisi değil |
| ⛔⛔ **Eğitim etkisi ÖLÇÜLMEDİ** | yakın-tekrarın ince ayara ne yaptığı bu depoda hiç ölçülmedi (T21'in açık kalemi) ⇒ karar bir önlem, bir bulgu değil |
| ⚠️ **Ölçüt T217 ile aynı** | 5 harflik gövde öneki + `tr_sadelestir`; ikinci bir tanım kurulmadı (K97) |
