# `yansitma` kurallarının kalibrasyonu — 1176 etiketli kayıt

**Betik:** `scripts/analiz/2026-09-22-yansitma-kalibrasyon.py` · **Tarih:** 2026-09-22  
**Girdi:** `data/judged/*.jsonl` tekilleştirilmiş  
**Altın etiket:** yargıcın `ayrinti_konusmada_var == False`  
**Pozitif:** 116/1176 (%10)  

⛔⛔ **Altın etiket altın değil** — bir yargıcın kanısı, tek anotatör, ve **tek ayrıntı** sondası. Aşağıdaki «duyarlılık», kapının gerçek duyarlılığı değil **yargıcın işaretlediği ayrıntıyı yakalama oranıdır**.

## Sonuç

| kural | DP | YP | YN | kesinlik | duyarlılık | F1 |
|---|---:|---:|---:|---:|---:|---:|
| A — alıntı (kapı adayı) | 1 | 0 | 115 | %100 | %1 | 2 |
| B — yansıtma, ≥1 yeni kök | 62 | 609 | 54 | %9 | %53 | 16 |
| B′ — yansıtma, ≥2 yeni kök | 58 | 538 | 58 | %10 | %50 | 16 |
| B″ — yansıtma, ≥3 yeni kök | 52 | 419 | 64 | %11 | %45 | 18 |
| A ∪ B″ | 53 | 419 | 63 | %11 | %46 | 18 |

## Hüküm

⭐ **A kuralı KAPI olabilir:** kesinlik %100 (1 doğru / 0 yanlış pozitif). Alıntıyla atıf en sert iddiadır ve parafraz riski taşımaz.

⛔ **B kuralı RAPOR kalır:** kesinlik %9, 609 yanlış pozitif. Parafrazı yeniden ifade olarak tanıyamıyor — *«içmeye başlamışsın»* ile *«alıyorum»* aynı şeydir ama kök eşlemesi bunu göremez.

⭐ Eşik yükseltmek kesinliği artırıyor ama duyarlılığı düşürüyor; tablodaki B/B′/B″ satırları bu takası gösteriyor.

## ⛔ Bunun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Duyarlılık yanıltıcı** | altın etiket tek ayrıntıya bakıyor; kapı başka bir uydurmayı yakalarsa **yanlış pozitif** sayılıyor ⇒ gerçek kesinlik ölçülenden **yüksek** olabilir |
| ⛔ **Kök eşleme 5 harf** | Türkçe ek sorununun kaba çözümü; `güven`/`güvenlik` ayrımı yapılamaz |
| ⛔ **Durak listesi elle** | listeye eklenen her sözcük ölçümü daraltır; liste `src/yansitma.py` içinde açık yazılı |
| ⛔ **Tek yargıç ailesi** | etiketlerin bir bölümü Gemini'den, çoğu Claude'dan; K97 gereği iki yargıcın notu aynı tabloda birleştirilmedi ama **etiket olarak** birlikte kullanıldı — bu bir gevşemedir ve burada yazılıdır |
