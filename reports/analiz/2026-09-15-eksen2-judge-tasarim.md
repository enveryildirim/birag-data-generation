# Eksen 2 judge — koşu tasarımı *(koşudan ÖNCE yazıldı)*

*2026-09-15 · betik `scripts/analiz/2026-09-15-eksen2-judge-plan.py`*
*girdi: `evals/safety_crisis.jsonl` · SHA256 `4d68e721eb9c5d71`*

## Neden

`safety_crisis` üç taramadır koşuyor ve her koşuda 20 öğenin **hepsinde**
`judge_bekleyen_oge` yazıyor: üç alan hiç denetlenmedi —
`rol_siniri_ihlali` · `bos_guvence` · `tuzak_suclama`. Yani bugüne kadarki
bütün Eksen 2 sayıları otomatik kuralların verdiği bir **alt sınır**; kapsam
kararı (A-dar → E-geniş) bu alt sınırla veriliyor.

⚠️ Judge bu sette bir kolu **kurtaramaz**: iddialar birleşik (AND) bağlı,
otomatik kurallar zaten koştu. Judge yalnızca düşürebilir. Ölçülen şey
«kol geçer mi» değil, **alt sınır ile gerçek arasındaki mesafe**.

## Küme

| kol | koşu | otomatik geçen | boş cevap | judge işi |
|---|---|---|---|---|
| taban | `20260915-105829-safety_crisis-baseline-1` | 11/20 | 0 | 20 |
| A-dar | `20260915-140907-sc2-A-dar` | 7/20 | 0 | 20 |
| B-derin | `20260915-141354-sc2-B-derin` | 5/20 | 6 | 14 |
| C-dikkat | `20260915-141743-sc2-C-dikkat` | 8/20 | 0 | 20 |
| D-tam | `20260915-142010-sc2-D-tam` | 9/20 | 0 | 20 |
| E-genis | `20260915-142308-sc2-E-genis` | 7/20 | 0 | 20 |
| **toplam** | | | | **114** |

Taban + `v0.0.3` taramasının beş kolu. Boş cevap judge'a gitmez — ön koşul
onu zaten düşürdü (`eksen_eval.py`), boş metin rubrikte tanımsız.

## Judge

| | |
|---|---|
| model | Claude **Sonnet** subagent (K97; Gemini kotası K96'da tükendi) |
| rubrik | **v7** — Eksen 2'nin üç alanı zaten v7'de tanımlı ve koddan türetiliyor |
| körlük | iş dosyasında **yalnızca rubrik + konuşma**; kolun adı, korpus, karşılaştırma YOK |
| işleme | `filter.f_bolumu_turet` — Gemini yolunun birebir aynısı (hesap farkı olmasın) |

⚠️ **Bir subagent aynı eval öğesinin iki cevabını görmez.** İşler kol içinde
beşerli bölünür; bir subagent'in gördüğü beş konuşmanın kullanıcı mesajları
birbirinden farklıdır. Aynı öğenin iki kolunu bir arada görseydi puanlama
**karşılaştırma** olurdu, körlük kalmazdı.

## k — iki aşamalı ve İKİ YÖNLÜ

```
aşama 1  tarama     k=1   114 iş
aşama 2  hakemlik   k=3   (işaretlenen her öğe) + (eşit sayıda işaretlenmeyen)
```

Hakemlik kümesi **koşudan önce** tanımlı:

1. Aşama 1'de üç alandan **herhangi biri** `true` gelen her (koşu, öğe).
2. Her biri için **aynı koşudan**, id sırasında ondan sonra gelen ve üç alanı
   da `false` olan ilk öğe (liste sonunda başa sarar). Eşit sayıda, deterministik.

> Gerekçe: K103 sert kapının kendisiyle tutmadığını ölçtü. Yalnızca pozitifi
> yeniden yargılamak pozitifleri tek yönlü eritir ve yanlış **negatif** oranını
> hiç ölçmez. Eşleştirilmiş kontrol ikisini birden verir.

Hüküm: k=3'te **çoğunluk** (K106).

## Karar ölçütü *(T24 — önceden yazıldı, sonradan gevşetilmez)*

| # | Ölçüt | Ne demek |
|---|---|---|
| Ö1 | Her kolun judge sonrası Eksen 2 skoru **≤** otomatik skoru | Aksi imkânsız; çıkarsa **alette** hata var, modelde değil |
| Ö2 | Taban da düşerse gerileme **taban-sonrası** sayılır | Gerileme = tabanda geçip kolda düşen öğe; taban kayarsa payda kayar |
| Ö3 | Judge hiçbir öğeyi düşürmezse sonuç **«otomatik kurallar bu sette yeterliydi»** | Negatif sonuç da sonuçtur; alt sınır = gerçek demektir |
| Ö4 | Hakemlikte çoğunluk aşama 1'i bozarsa **aşama 1 sayısı değil çoğunluk** raporlanır | Ve iki sayı arasındaki fark *judge gürültüsü* olarak ayrıca yazılır |
| Ö5 | Kol sıralaması otomatik ile judge arasında değişirse **kapsam cümlesi yeniden yazılır** | K109/K113/K115'in «kapsam genişledikçe siliniyor» cümlesi alt sınıra dayanıyor |

## Reddedilen alternatifler

| Alternatif | Neden değil |
|---|---|
| tarama 1 (`sc-*`, v0.0.2/280 adım) | Korpusu v0.0.3 süperse etti ve adım farkı (280/372) K113'te ölçüldü; aynı tabloya girerse judge farkı ile adım farkı ayrışmaz |
| tarama 3 (`sc3-doz*`, v0.0.4/v0.0.5) | Doz korpusları bir DENEY nesnesi, aday korpus değil (K114). Kapsam kararı gönderilecek korpusta verilir; doz kollarını judge'lamak 10 koşu daha demek |
| `sc-taban-thinking-acik` | K108 Faz 4 ölçümlerini thinking=kapalı modda mühürledi; açık mod tabanı aynı tabloya girerse mod farkı judge farkı sanılır |
| k=3 tam tarama (114 → 342 iş) | K106 mühür koşusunda k=3 kullandı ama orada 48 öğe vardı ve SINIR vakası yoktu. Burada maliyet üç katına çıkarken kazanç yalnızca işaretlenen öğelerde; hakemlik o öğelere ve eşleştirilmiş kontrolüne yoğunlaştırıldı |
| yalnızca işaretlenen öğeyi yeniden yargılamak | ⛔ TEK YÖNLÜ. Pozitifi üç kez sınayıp negatifi bir kez sınamak pozitifleri sistematik olarak eritir; yanlış NEGATİF oranı hiç ölçülmez |
| Gemini ile puanlamak (K45 bağımsız aile) | Kota tükendi (K96); K97 bu yüzden subagent'a geçti. Körlük şartı korunuyor |

## Kapsam dışı — bilerek

- **Eksen 1 judge'ı** (`golden.*`): kapıyı geçen kol yok, K97 gereği koşmaz.
- **`safety_crisis` ölçüt düzeltmesi** (T31 kurum özel adı · T34 payda 16):
  K31 gereği **ikinci set** olarak eklenir, mevcut set durur. Bu koşu mevcut
  setle koşuyor; düzeltme ayrı iş.
- **Kriz dilimi**: uzman + etik kurul kapısında (Kural 3).

