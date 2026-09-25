# Claude subagent judge'ın sapması

**Girdi:** aynı 48 cevap, aynı rubrik  
**Gemini koşusu:** `reports/analiz/golden-kosu/20260915-012409-baseline-v6`  
**Claude koşusu:** `reports/analiz/golden-kosu/20260915-063352-golden-baseline-claude`  
**Betik:** `scripts/analiz/2026-09-15-judge-claude-sapmasi.py` · **Tarih:** 2026-09-15

---

## 0. Bu ölçüm neden zorunlu

K45 dört judge karşılaştırmasında iki Claude'un bağımsız ailelerden sistematik **yüksek** verdiğini ölçtü: claude 0.878 / 0.924 · qwen 0.825 · gemini 0.814. Korpusu Claude yazdığı için bu bir **öz-şişirme** riski. Gemini kotası tükendiği için (K96) Claude'a geçiliyor — ama sapma ölçülmeden geçilirse bundan sonraki her sayı sessizce şişer.

Ölçüm bedava: aynı cevapların gemini-v6 puanları zaten elimizdeydi.

## 1. Cömertlik — K45'in metriği

K45'in ölçek normalizasyonu kullanıldı; hangi boyutların hesaba girdiği aşağıda yazılı.

⚠️ **K45'in yedi boyutundan 2'i v6'da YOK** `kisalik_dogallik`, `dil_butunlugu` — metrik kalan 5 boyutla hesaplandı. **Bu yüzden aşağıdaki sayı K45'in 0.825 / 0.814 / 0.878 / 0.924 çapalarıyla doğrudan karşılaştırılamaz**; yalnızca iki judge'ı birbirine karşı konumlar.

| Judge | K45 skoru | n |
|---|---:|---:|
| Gemini (v6) | 0.591 | 48 |
| Claude subagent (v6) | 0.671 | 48 |
| **Fark** | **+0.080** | |

> K45 çapaları (qwen 0.825 · gemini 0.814 · claude-opus 0.878 · claude-sonnet 0.924) **farklı boyut kümesiyle** hesaplanmıştı; yukarıdaki sayıyla yan yana konamaz.

⚠️ **Toplamda Claude +0.080 daha cömert.** Claude ile puanlanan hiçbir sayı Gemini ile puanlanmış bir sayıyla doğrudan karşılaştırılamaz; **her raporda bu fark yazılmalı.**

> ⚠️ **Ama toplam sayı içini gizliyor.** §2'de boyut boyut bakıldığında fark tek yönlü DEĞİL: Claude bazı boyutlarda daha sert, bazılarında daha cömert olabilir. Tek bir "cömertlik katsayısı" çıkarıp bütün boyutlara uygulamak yanlış olur — düzeltme boyut bazında düşünülmeli.

## 2. Uyum — aynı kayıtta aynı şeyi mi görüyorlar

⚠️ Ortalamaların eşit olması uyum demek değildir: kayıt kayıt zıt olup ortalamada buluşabilirler. Bu yüzden **kayıt bazında** bakılır.

| Boyut | Gemini ort | Claude ort | Fark | Ort. mutlak fark | Birebir uyum |
|---|---:|---:|---:|---:|---:|
| `anlasilirlik` | 4.65 | 3.77 | -0.87 | 0.92 | %35 |
| `dogallik` | 3.92 | 4.04 | +0.13 | 0.33 | %69 |
| `mi_uyumu` | 4.56 | 4.58 | +0.02 | 0.15 | %85 |
| `grounding` | 5.00 | 5.00 | +0.00 | 0.00 | %100 |
| `duygusal_tepki` | 0.79 | 0.90 | +0.10 | 0.15 | %85 |
| `yorumlama` | 0.29 | 0.52 | +0.23 | 0.23 | %77 |
| `kesif` | 1.00 | 1.46 | +0.46 | 0.54 | %46 |

## 3. İkili bayraklar — ham uyum yanıltır, kappa da verilir

> Bayrakların çoğu neredeyse hep `false`; ham uyum %95 görünürken judge'lar aslında hiçbir şeyde anlaşmıyor olabilir. Cohen kappa şansı düşer: **0 = şans düzeyi, 1 = tam uyum.** `—` iki tarafın da sabit olduğu, yani kappa'nın tanımsız kaldığı durumdur.

| Bayrak | Gemini | Claude | Ham uyum | Kappa |
|---|---:|---:|---:|---:|
| `siz_kaymasi` | 13/48 | 14/48 | %98 | 0.95 |
| `klise_acilis` | 21/48 | 14/48 | %85 | 0.69 |
| `terapi_jargonu` | 4/48 | 8/48 | %92 | 0.62 |
| `bos_guvence` | 13/48 | 8/48 | %85 | 0.58 |
| `ovgu_tonu` | 1/48 | 2/48 | %98 | 0.66 ⚠️seyrek |
| `yansitma_var` | 32/48 | 33/48 | %98 | 0.95 |
| `karmasik_yansitma` | 14/48 | 11/48 | %94 | 0.84 |
| `ozet_var` | 1/48 | 4/48 | %94 | 0.38 ⚠️seyrek |
| `takdir_var` | 1/48 | 4/48 | %94 | 0.38 ⚠️seyrek |
| `ozerklik_vurgusu` | 6/48 | 10/48 | %92 | 0.70 |
| `tuzak_uzman` | 2/48 | 2/48 | %96 | 0.48 ⚠️seyrek |
| `tuzak_etiketleme` | 0/48 | 0/48 | %100 | — |
| `tuzak_soru_cevap` | 1/48 | 3/48 | %96 | 0.48 ⚠️seyrek |
| `tuzak_erken_odak` | 1/48 | 1/48 | %96 | -0.02 ⚠️seyrek |
| `tuzak_suclama` | 0/48 | 0/48 | %100 | — |
| `tuzak_erken_tavsiye` | 3/48 | 3/48 | %96 | 0.64 ⚠️seyrek |
| `rol_siniri_ihlali` | 0/48 | 1/48 | %98 | 0.00 ⚠️seyrek |
| `klinik_guvenlik_ihlali` | 3/48 | 6/48 | %94 | 0.64 |
| `cevapsiz_soru` | 3/48 | 4/48 | %98 | 0.85 ⚠️seyrek |

## 4. Okuma

- Kappa hesaplanabilen 17 bayrakta **ortalama kappa 0.58**.
- **4 bayrakta kappa < 0.40 ama olay SEYREK** (her iki judge de 5'ten az ateşledi): `ozet_var`, `takdir_var`, `tuzak_erken_odak`, `rol_siniri_ihlali`. Burada düşük kappa **uyumsuzluk kanıtı değil**: 1/48'de tek bir uyuşmazlık kappa'yı 1.0'dan 0'a düşürür. Doğru okuma *"ölçmeye yetecek kadar olay yok"* — daha büyük örneklem gerekir.
- ⛔ **Kural:** Claude ile puanlanmış hiçbir sayı, Gemini ile puanlanmış bir sayıyla aynı tabloda karşılaştırılmaz. Judge modeli her raporda yazılır (`judge_model` alanı kayıtlarda duruyor).
- Bu sapma **korpus kalitesi hakkında bir şey söylemez**; yalnızca aletin değiştiğini söyler.


## 5. Gürültü tabanı — bu farkların hangisi gerçek?

Judge aynı kayda iki kez bakınca ne kadar oynuyorsa, başka bir judge'la
olan farkın o kadarı zaten gürültüdür (K61). Taban
`reports/analiz/2026-09-15-judge-tekrar-test.md`'den gelir: aynı Sonnet,
aynı v6 rubriği, iki bağımsız geçiş, n=23.

⚠️ Taban KORPUS v3 kalemlerinden, buradaki fark GOLDEN DEV kalemlerinden.
Kalemler aynı değil; bu bir büyüklük karşılaştırmasıdır, kesin sınama değil.

| Boyut | ort. mutlak fark | gürültü tabanı | karar |
|---|---:|---:|---|
| `anlasilirlik` | 0.92 | 0.78 | sınırda |
| `dogallik` | 0.33 | 0.09 | **gerçek fark** |
| `mi_uyumu` | 0.15 | 0.00 | **gerçek fark** |
| `grounding` | 0.00 | 0.00 | ikisi de 0 — boyut sabit |
| `duygusal_tepki` | 0.15 | 0.30 | **ÖLÇÜLEMEZ** — judge kendisiyle daha az anlaşıyor |
| `yorumlama` | 0.23 | 0.35 | **ÖLÇÜLEMEZ** — judge kendisiyle daha az anlaşıyor |
| `kesif` | 0.54 | 0.09 | **gerçek fark** |
