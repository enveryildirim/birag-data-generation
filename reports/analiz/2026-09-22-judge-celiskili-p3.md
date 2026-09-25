# `celiskili` sınıfının ilk yargısı — 13 kayıt

**Betik:** `scripts/analiz/2026-09-22-judge-sonuclari-celiskili-topla.py` · **Tarih:** 2026-09-22  
**Girdi:** `data/candidates/celiskili-parti3.jsonl`  
**Yargıç:** claude-sonnet-subagent · **rubrik:** judge-eksen1.v9  
**Toplanan:** 13/13 · bozuk 0 · eksik 0  

## Not ortalamaları

| boyut | ortalama | ölçek |
|---|---:|:--|
| `mi_uyumu` | 5 | 1-5 |
| `grounding` | 5 | 2/5 |
| `dogallik` | 5 | 1-5 |
| `anlasilirlik` | 3.54 | 1-5 |
| `duygusal_tepki` | 0.69 | 0-2 |
| `yorumlama` | 0.46 | 0-2 |
| `kesif` | 0.31 | 0-2 |

⛔⛔ **Boyutlar aynı ölçekte değil** — EPITOME üçlüsü (`duygusal_tepki`, `yorumlama`, `kesif`) **0-2**, ötekiler 1-5. Sütunu ölçeksiz okumak yanıltır.

⚠️ `kesif` düşük (0.31/2) ve bu **kısmen tasarımın sonucu**: bu sınıfta 12 cevabın 11'i `turn_ending ∈ {durur, ozet, yalnizca_yansitma, takdir}` ile bitiyor, yani açık uçlu soruyla davet etmiyor. ⛔ «Tasarım gereği» demek **savunma değildir**: kotanın bu boyutu bastırıp bastırmadığı ölçülmedi.

⛔ Ortalama **karşılaştırmasız** bir sayıdır: bu kayıtların başka bir kümeyle kıyası yapılmadı ve n=12.

## A. Bu dalganın gürültü tabanı

Tekrar çifti: **3** (aynı kayıt, iki numara, ayrı öbek)

| boyut | aynı not % | ort. mutlak fark |
|---|---:|---:|
| `kesif` | 100 | 0 |
| `mi_uyumu` | 100 | 0 |
| `grounding` | 100 | 0 |
| `dogallik` | 100 | 0 |
| `duygusal_tepki` | 67 | 0.33 |
| `anlasilirlik` | 67 | 0.67 |
| `yorumlama` | 33 | 0.67 |

⛔⛔ **n=3 çift.** Taban kaba; güven aralığı hesaplanmadı ve başka bir dalganın tabanının yerine geçmez (K137: rubrik sürümü değişirse karşılaştırma geçersiz).

## B. Uydurma sondası — sınıfın kendi iddiası ÇÜRÜDÜ mü?

`grounding == 2` (yargıç: somut ayrıntının konuşmada karşılığı yok): **0/13 = %0**

⛔⛔ §7a″ bu sınıfı **uydurmaya karşı** tasarlamıştı. Ölçülen oran korpus tabanının (T238: %12) **ALTINDA**. ⇒ **Tasarım iddiası bu ölçümde DESTEKLENMEDİ.**

`klinik_guvenlik_ihlali`: **2/13** — `58dfb0b9008a1a856f8a61b1`, `6b60b8313b34ec9e1dd1c69b`

### Mekanizma — iddia değil, ölçüm

Hipotez: **cevabı tohumdan yazdım, kullanıcı mesajı ise tohumun kısaltması.** Yansıttığım ayrıntı mesajda yok, tohumda var. Sınama: uydurulan ayrıntının kökleri kullanıcı mesajında yok ama tohum metninde var mı?

| banka | uydurulan ayrıntı | mesajda yok | **tohumda var** | örnek kök |
|---:|---|---:|---:|---|

⇒ **0/0** uydurmada, mesajda bulunmayan ayrıntı **tohumda duruyor**. Uydurma serbest değil, **tohumdan sızıyor**.

⭐⭐⭐ **Eksik kapı, az önce yazdığım kapının AYNASI.** T264'te T217 kapısını yazdım: *«kullanıcı metni kendi tohumundan mı?»* Kimse tersini sormadı: ***«cevap yalnız kullanıcı metninden mi?»*** Tohum→mesaj kısaltması bilgiyi düşürüyor, cevap ise düşmeden önceki tohumu hatırlıyor. ⇒ Bu, kural yazılı-kapı yok ailesinin (T22) yeni bir üyesidir: `uretim-v5` uydurmayı **yasaklıyor**, hiçbir kapı **bakmıyor**.

⛔ **`celiskili_ok` 13/13 geçirdi** — çünkü o kapı yalnız çelişkinin adlandırılmasına ve iki pasaja atfa bakıyor; **yansıtma cümlesine bakmıyor**. Kapıdan geçmek temiz olmak değildir.

⛔⛔ **Şerhler — bu sayı ne kadar sağlam:** (1) n=13 ⇒ bir kayıt oranı ~%8 oynatır, güven aralığı hesaplanmadı, anlamlılık sınanmadı · (2) %12 **başka bir dalgada, başka kayıtlarla** ölçüldü ⇒ bu tam bir karşılaştırma değil, iki ayrı gözlemin yan yana konmasıdır · (3) `grounding` türetmesi **tek ayrıntı** sondasıdır (`en_somut_ayrinti`) ⇒ ölçülen oran bir **alt sınırdır**, gerçek uydurma bundan fazla olabilir · (4) tek yargıç ailesi, doğrulayan ikinci anotatör yok · (5) kök eşleme 5 harfe kısaltıyor ⇒ mekanizma tablosu yanlış pozitif verebilir.

## Yazılan dosyalar

| dosya | yargılanan | toplam |
|---|---:|---:|
| `data/judged/celiskili-parti3.claude.jsonl` | 13 | 13 |

## ⛔ Bunun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Körlük tam değil** | 12 kaydın hepsinde iki çelişkili `<context>` var ve cevapların hepsi çelişkiyi adlandırıyor ⇒ yargıç bunların **aynı sınıftan** olduğunu metinden anlayabilir. Numara karıştırma partiyi gizler, **sınıfı gizlemez** |
| ⛔ **Öbekleme bağımsızlık kaybı** | bir subagent öbeğindeki 8 kayıt aynı bağlamda duruyor ⇒ sıra ve çapa etkisi olabilir; tekrar çiftleri ayrı öbeklere düşürülerek bu etki tabana dahil edildi, ama **ayrıştırılmadı** |
| ⛔ **Tek yargıç ailesi** | yalnız Claude; bu kayıtlar için Gemini yargısı **yok** ⇒ K97'nin çapraz karşılaştırması burada yapılamadı |
| ⛔ **Kapı ≠ not** | 12 kaydın 12'si `celiskili_ok`'tan geçti; bu, iyi not aldıkları anlamına gelmez |
| ⚠️ **Kayıtları ben yazdım** | K30/K260: üretici de yargıyı okuyan da aynı taraf; bağımsız anotatör hâlâ borç |
