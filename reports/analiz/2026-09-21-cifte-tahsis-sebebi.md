# Çifte tahsisin sebebi — ve T219'un çürümesi

**Betik:** `scripts/analiz/2026-09-21-cifte-tahsis-sebebi.py` · **Tarih:** 2026-09-21  
**Kanıt:** git geçmişi — plan v1 `6816874` (09:49) · üretim sonu `4969d6f` (10:30) · planın ezildiği commit `1231d2b` (10:51)

## 0. ⭐⭐⭐ Sebep

| adım | saat | ne oldu |
|---|---|---|
| 1 | 09:48–09:49 | `v6-parti1` planlandı (**v1**) |
| 2 | 09:51–10:30 | parti1 v1'den ÜRETİLDİ; 59 kaydın 59'unun `source_ids`'i v1 ile birebir uyumlu (**59/59**) |
| 3 | 10:51 | ⛔⛔ **parti1 planı YENİDEN ÜRETİLİP ÜSTÜNE YAZILDI (v2)** — 60 tohumun **60/60**'ı değişti, ortak kalan **0** |
| 4 | 10:51 | parti2 aynı commit'te planlandı. `kullanilmis()` yalnız `data/candidates`'ı tarar, **bir PLANI göremez** ⇒ iki plan **26** satırda aynı tohumu aldı |
| 5 | 10:32–11:06 | blok betikleri başka kusurlar için yeniden koştu. Betik `source_ids`'i **plandan** yazıyor (`"source_ids": [p["source_id"]]`) ⇒ **59/59 kaydın künyesi yeni plandan yeniden damgalandı** |

⭐ Sonuç: 37 tohum iki kez üretilmiş görünüyor. ⛔ Ama bu bir *«çifte tahsis»* değil, **bir künye bozulmasının yan etkisi**: parti1'in kayıtları kendi tohumlarını kaybetti ve parti2'ninkileri üstlendi.

## 1. ⛔⛔⛔ T219 çürüdü

| karşılaştırma | ortalama | medyan | sıfır örtüşen |
|---|---:|---:|---:|
| **v1 — üretildiği plan** | **%53** | %50 | 0/59 |
| v2 — bugünkü plan | **%6** | %5 | 21/59 |

⛔ T219 *«parti1 başka bir üretim rejiminde yazıldı; tohum ızgarayı verdi, sahneyi ben yazdım»* diyordu ve dayanağı %6'lık örtüşmeydi. Kayıtlar **üretildikleri plana göre %53 örtüşüyor** ve sıfır örtüşen kayıt yok — `v6-parti2` (%49) ile aynı düzeyde. ⇒ **Rejim farkı diye bir şey yok; bir veri bozulması var.** ➡️⭐⭐⭐ *İki açıklama aynı sayıyı üretiyordu — «başka türlü yazdım» ve «yanlış tohumla karşılaştırıyorum» — ve ben ölçmeden kolayını seçtim.*

## 2. ⛔ Etkilenen ölçümler

| ölçüm | durum |
|---|---|
| **T219** | ⛔ **ÇÜRÜDÜ** — parti1 rejimi diye bir şey yok |
| **T220 / T222** (parti1'in 6 ekseni) | ⛔ **GEÇERSİZ** — yanlış tohumların meta'sına karşı ölçüldü; yeniden ölçülmeli |
| **T221** (parti1 ↔ parti3-6) | ◐ parti3-6 tarafı ayakta, **parti1 tarafı düştü** ⇒ karşılaştırma geçersiz |
| **T223** (kaynak ayrımı) | ◐ parti1 dahil edilmişti; parti3-6 sonucu (bant içinde) parti1 çıkarılınca da ayakta kalır mı, **ölçülmedi** |
| T217 (tohum karşılığı kapısı) | ⭐ etkilenmedi; kapı zaten bu sınıfı yakalamak için kuruldu |
| Kapsama envanterleri | ⛔ parti1'in 59 kaydı **yanlış tohum meta'sıyla** sayılıyor ⇒ T211'in hedefleri o kadarıyla yanlış zemine oturuyor |

## 3. ⭐ Onarım mümkün ve kayıpsız

| | |
|---|---|
| plan v1 git'te duruyor | `6816874:data/plan/v6-parti1.jsonl` |
| üretim anındaki künye git'te duruyor | `4969d6f` — 59/59 kayıt |
| kayıt METİNLERİ | bugünkü hâlleri korunur; onarım yalnız `source_ids` + `gen_meta.seed_id` alanlarına dokunur |
| çifte tahsis | onarımdan sonra **kendiliğinden kalkar**: plan v1 ∩ plan2 = **0** |

⛔⛔ **ONARIM YAPILMADI.** `data/plan/` ve `data/candidates/` işlenmiş veridir; 59 kaydın künyesini değiştirmek ve ardından kapsama envanterlerini yeniden üretmek bir zincir başlatır. Karar kullanıcının.

## 4. ⭐⭐⭐ ONARIM YAPILDI — ve gerçek hasarı görünür kıldı

| | |
|---|---:|
| plan v1 geri kondu · künyesi düzeltilen kayıt | **59/59** |
| onarım sonrası kayıt–tohum örtüşmesi | **%53** (sıfır örtüşen 0) |
| ⛔ **çift üretilen tohum: 24 → 37** | parti1+parti2 çifti **sıfırlandı**, yerine parti1+parti3 (22) · parti1+parti4 (8) · parti1+parti5 (4) · parti1+parti6 (3) çıktı |

⛔⛔ **Onarım hasarı YARATMADI, GÖRÜNÜR KILDI.** Bozulma sırasında parti1'in gerçek tohumları künyeden düştüğü için `kullanilmis()` onları **boşta** saydı ve parti3-6 onları yeniden çekti. Yani parti1'in 59 tohumunun **37'si** (%63) sonraki bir partide ikinci kez kullanılmış. ⭐ Asistan cevapları farklı (Jaccard ort. %10) ama **kullanıcı turları ortalama %35, en yükseği %85 örtüşüyor** ⇒ eğitim girdisinde gerçek bir yakın-tekrar var ve bu, künye bozulmasının asıl bedeli.

## 5. ⭐ Kurulan iki kapı

| kapı | ne yapar |
|---|---|
| **künye kapısı** (`birlestir.py`) | her kayıt için `source_ids` ve `gen_meta.seed_id`'yi PLANA karşı denetler; uyuşmazsa birleştirme reddeder. Uçtan uca sınandı |
| **plan kapısı** (`P1.havuz`) | havuz artık `kullanilmis()` yanında **başka partilerin PLANLARINI** da dışlıyor (kendi çıktısı hariç) ⇒ iki plan aynı anda aynı tohumu alamaz |

## ⛔ Bu soruşturmanın söylemedikleri

| | |
|---|---|
| ⛔⛔ **Planın NEDEN yeniden üretildiği kesin değil** | commit mesajı parti1'in elle yazılmış hedef listesinin kapanmış açıkları kovaladığını söylüyor; plan muhtemelen bu yüzden yeniden türetildi. Ama üretilmiş bir partinin planını yeniden üretmenin **hiçbir işe yaramayacağı** o an fark edilmemiş |
| ⭐ **Kapılar kuruldu** | bkz. §5; ama *«üretilmiş bir partinin planı hiç değişemez»* diye doğrudan bir yazma kilidi hâlâ yok — künye kapısı değişikliği ancak BİRLEŞTİRMEDE yakalar |
| ⛔⛔ **T224'te bir cümle yanlıştı ve düzeltildi** | *«`gd-021`'in tohumu `v6-parti1#4`'te ÜRETİLMİŞTİ»* demiştim; o tohum **plan v1'de yok**, yalnız bozuk v2 planında vardı ⇒ kriz tohumu parti1'de hiç üretilmemiş. Bozuk planı okumaktan gelen bir iddiaydı |
| ⛔ **`kullanilmis()` planları görmüyor** | iki plan aynı anda üretilirse hâlâ çakışabilirler; bu da düzeltilmedi |
| ⚠️ **12 kaydın metni de değişmiş** | üretimden sonraki meşru düzeltmeler (elle onay, `is_negative`, iskele temizliği); onarım bunlara dokunmamalı |
