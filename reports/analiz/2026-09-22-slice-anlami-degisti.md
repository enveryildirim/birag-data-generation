# `slice` alanının anlamı v5 ile v6 arasında sessizce değişti

**Betik:** `scripts/analiz/2026-09-22-slice-anlami-degisti.py` · **Tarih:** 2026-09-22  
**Girdi:** `data/candidates/` — v4/v5 460 benzersiz kayıt · v6 530 benzersiz kayıt  

⭐ Nasıl çıktı: subagent judge koşusunda bir kayıt uydurma diye işaretlendi; dilimi `rag_tek_tur` görününce *«bağlam belgesi nerede»* diye bakıldı ve **yoktu**.

## Alan ne söylüyor

| dönem | `slice` değeri | kayıt | bağlamlı | oran |
|---|---|---:|---:|---:|
| v4/v5 | `rag_cok_tur` | 23 | 23 | **%100** |
| v4/v5 | `rag_tek_tur` | 77 | 77 | **%100** |
| v4/v5 | `terapotik_cok_tur` | 161 | 0 | **%0** |
| v4/v5 | `terapotik_tek_tur` | 199 | 0 | **%0** |
| **v6** | `cok_tur` | 212 | 21 | **%10** |
| **v6** | `rag_tek_tur` | 318 | 112 | **%35** |

⭐⭐ **v4/v5'te alan TAM bilgi taşıyor:** `rag_*` → %100 bağlamlı, `terapotik_*` → %0. ⛔⛔ **v6'da taşımıyor:** sözlük iki değere düştü, `terapotik_*` kayboldu, `cok_tur` yeni, ve `rag_tek_tur` kayıtların yalnız **%35'inde** bağlam var.

➡️ Aynı ad, iki anlam: **v5'te *«tek turlu VE bağlam belgeli»*, v6'da yalnızca *«tek turlu»*.** İki dönem aynı korpusun içinde ve alan onları **ayırt etmiyor**.

## ⛔⛔ Neden hiçbir kapı görmedi

| katman | durum |
|---|---|
| `src/schemas.py` | `slice: str` — **`Literal` değil** ⇒ şema her dizgeyi kabul eder; yeni bir sözlük sessizce geçerlidir |
| `src/checks.py` | **slice denetimi yok** |
| birleştirme raporu | dilimi saymıyor |
| judge | dilimi görmüyor (körlük şartı) |

⭐ Bu, iki serinin kesişimi: **T236** (alan dolu, biçimi geçerli, anlamı değişmiş) ve **T237** (kural yazılı, kapı yok). ⛔ Ayrıca `slice` alanının kusur geçmişi var: **K69**'da bir varsayılan iki kaydı yanlış dilimle damgalamıştı.

## ⛔⛔⛔ Neden acil

Veri kartı *«Dilim dağılımı»* satırını **bu alandan** türetiyor — `datasets/v0.0.8/CARD.md`: *«`terapotik_tek_tur` 256 · `terapotik_cok_tur` 188 · `rag_tek_tur` 85 · `rag_cok_tur` 24 · `replay` 18»*. O kartta sayı **doğruydu**, çünkü v5 sözlüğü geçerliydi.

⛔ v6 kayıtları derlemeye girdiğinde kart `rag_tek_tur`'ü **395** diye sayacak; bağlamı gerçekten olan tek turlu kayıt ise **189** ⇒ yayımlanan RAG payı **iki katından fazla** şişecek.

⭐ **Derleme v6 için henüz koşmadı** ⇒ bu, yayımlanmış bir sayı bozulmadan ÖNCE yakalandı (T121'in dersi: kapıyı derlemeden önce denetle).

## ⭐ Öneri — *bu benim önerim*, ölçülmedi ve UYGULANMADI

| | |
|---|---|
| 1 | `slice` **`Literal`** olmalı; sözlük tek yerde yazılı olmalı ve genişlemesi bir karar gerektirmeli |
| 2 | Dilim **türetilmeli, beyan edilmemeli**: tur sayısı `messages`'tan, RAG'lik `context`'in doluluğundan ⇒ alan kendisiyle çelişemez hâle gelir |
| 3 | Geriye dönük etiketleme bir **karardır** (530 kayıt) ve burada yapılmadı; hangi dönemin sözlüğüne göre yazılacağı ve eski kartların ne olacağı ayrı sorular |

## ⛔ Bu raporun söylemedikleri

| | |
|---|---|
| ⛔ **Hiçbir kayıt DEĞİŞTİRİLMEDİ** | 530 kaydın etiketini yeniden yazmak rutin bir düzeltme değil |
| ⛔ **Yayımlanmış kartlar YANLIŞ DEĞİL** | `v0.0.5`–`v0.0.11` v5 sözlüğüyle derlendi ve o sözlükte sayı doğru; sorun **v6'nın girmesiyle** başlayacak |
| ⚠️ **`cok_tur` kayıtlarının %10'unda bağlam var** | yani yeni sözlükte bağlam ile tur sayısı **bağımsız iki eksen**; tek bir alanla ikisi birden taşınamaz |
| ⚠️ **Sebep aranmadı** | sözlüğün neden değiştiği (v6 üretim betiklerinin nereden kopyalandığı) bu raporda izlenmedi |
