# ⛔⛔⛔ Ön kaydın «bulaşmamış» baş ölçüsü — ölçüldü

**Betik:** `scripts/analiz/2026-09-23-cf-onkayit-bulasma.py` · **Tarih:** 2026-09-23  
**Ön kayıt:** `configs/deney/2026-09-22-v0022-celiskili-on-kayit.json` — baş ölçü: *«context_fidelity — bulaşmamış 15 öge»*  
**Eğitim bankası:** 25 çift  

⛔⛔ **Ne oldu.** Ön kayıt baş ölçüyü *«bulaşmamış 15 öge»* diye koydu; 09-22 bulaşma raporu da *«Temiz kalan ölçüler»* diye aynı 15'i saydı. **O 15 öge hiç ölçülmedi** — ölçü yalnız 5 `celiskili` ögesine koşuldu, öteki 15'i **kategorisi yüzünden** temiz sayıldı. *İddia yazılı, ölçüm yok* (T22 ailesi).

## Aynı ölçü, üç grup

| grup | öge | değer çakışması olan öge |
|---|---:|---:|
| eski `celiskili` (09-22'de bulaşmalı ilan edilen) | 5 | **3/5** |
| eski `yeterli` — ⛔ ön kaydın baş ölçüsü | 5 | **5/5** |
| eski `distractor` — ⛔ ön kaydın baş ölçüsü | 5 | **2/5** |
| eski `yetersiz` — ⛔ ön kaydın baş ölçüsü | 5 | **0/5** |
| ⭐ yeni örtüşmez set | 15 | **0/15** |

⛔⛔⛔ **Baş ölçünün 7/15 ögesinde** bir eğitim çiftinin değer kökleri pasajda geçiyor. Çakışma `yeterli` ve `distractor` kategorilerinde toplanıyor; `yetersiz` temiz.

## Öge başına

| öge | kategori | çakışan eğitim değerleri |
|---|---|---|
| `cf-001` | yeterli | #2 «randevu gerekir», #2 «randevusuz», #25 «yazılı olarak» |
| `cf-002` | yeterli | #11 «kayıt gerekir», #2 «randevu gerekir», #2 «randevusuz», #4 «belge gerekmez» |
| `cf-003` | yeterli | #11 «kayıt gerekir» |
| `cf-004` | yeterli | #2 «randevu gerekir», #2 «randevusuz» |
| `cf-005` | yeterli | #6 «ücretsiz» |
| `cf-006` | distractor | — |
| `cf-007` | distractor | #2 «randevu gerekir», #2 «randevusuz», #25 «yazılı olarak» |
| `cf-008` | distractor | — |
| `cf-009` | distractor | — |
| `cf-010` | distractor | #6 «ücretsiz» |
| `cf-011` | yetersiz | — |
| `cf-012` | yetersiz | — |
| `cf-013` | yetersiz | — |
| `cf-014` | yetersiz | — |
| `cf-015` | yetersiz | — |

## Neden önemli — bulaşmanın yönü belirsiz

`e3` kolu, `d1`'den **yalnız** bu 25 çiftle ayrılıyor. Baş ölçünün ögeleri o çiftlerin pasajlarını (*«Görüşmeler ücretsizdir»*, *«randevusuz yapılabilir»*…) taşıyorsa, iki kol arasındaki bir fark **genel bağlam sadakatinden** değil, **o pasajlara aşinalıktan** gelebilir. ⛔ Yön de bilinmiyor:

- **kayırabilir** — model bu cümleleri eğitimde görmüş, cevabı çıkarması kolaylaşır;
- **bozabilir** — model «ücretsiz» görünce *çelişki var* demeyi öğrendi; tek pasajlı bir `yeterli` ögesinde olmayan bir çelişkiyi adlandırabilir.

⇒ Her iki durumda da fark **yorumlanamaz**.

## ⭐ Ön kayıt SONUÇ GÖRÜLMEDEN düzeltilebilir — ama bu bir karar

Ölçüm 5/40'ta durdu (K272) ve t7 **çözümlenmedi** ⇒ baş ölçüyü değiştirmek şu an hâlâ temiz. Değiştirmek ise ön kaydın kendisini değiştirmektir ⇒ **bu betik değiştirmiyor**. Seçenekler:

1. **Baş ölçüyü çakışmasız ögelere daralt** — 8 öge kalır: `cf-006`, `cf-008`, `cf-009`, `cf-011`, `cf-012`, `cf-013`, `cf-014`, `cf-015`. ⛔ Güç düşer (n küçülür).
2. **Baş ölçüyü örtüşmez sete taşı** — `evals/context_fidelity.ortusmez.jsonl` (15 öge, değer çakışması 0). ⛔ Ama o set **yalnız `celiskili`** davranışını ölçer; genel bağlam sadakatini değil.
3. **İkisini birlikte** ve sıralarını şimdi, sonuçtan önce yaz.

*Hangisi — bu benim kararım değil.*

## ⛔ Bunun söylemedikleri

| | |
|---|---|
| ⛔ **Sözcük ölçüsü** | kök düzeyinde; anlamsal bulaşmayı görmez, işlev sözcüğünü içerikten ayıramaz. Değer çakışması bu ölçünün en güçlü ama yine kaba sinyali |
| ⛔ **Yalnız `celiskili` bankasına karşı** | `d1`'in (v0.0.18) kendi `cevap_var`/`cevap_yok` kayıtlarının pasajlarıyla örtüşme **ölçülmedi** — ama o kayıtlar iki kolda da var, fark yaratmıyor |
| ⛔ **Bulaşmanın büyüklüğü ≠ etkisi** | pasajın eğitimde geçmesi, puanı ne kadar oynattığını söylemez |
| ⚠️ **Bunu ben kaçırmıştım** | 09-22 raporunda «temiz kalan ölçüler» cümlesini ben yazdım, ölçmeden |
