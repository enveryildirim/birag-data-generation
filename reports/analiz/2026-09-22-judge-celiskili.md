# `celiskili` sınıfının ilk yargısı — 12 kayıt

**Betik:** `scripts/analiz/2026-09-22-judge-sonuclari-celiskili-topla.py` · **Tarih:** 2026-09-22  
**Girdi:** `data/candidates/celiskili-pilot.jsonl` · `data/candidates/celiskili-parti2.jsonl`  
**Yargıç:** claude-sonnet-subagent · **rubrik:** judge-eksen1.v9  
**Toplanan:** 12/12 · bozuk 0 · eksik 0  

## Not ortalamaları

| boyut | ortalama | ölçek |
|---|---:|:--|
| `mi_uyumu` | 4.92 | 1-5 |
| `dogallik` | 4.92 | 1-5 |
| `grounding` | 4.25 | 2/5 |
| `anlasilirlik` | 3.33 | 1-5 |
| `duygusal_tepki` | 1 | 0-2 |
| `yorumlama` | 0.92 | 0-2 |
| `kesif` | 0.42 | 0-2 |

⛔⛔ **Boyutlar aynı ölçekte değil** — EPITOME üçlüsü (`duygusal_tepki`, `yorumlama`, `kesif`) **0-2**, ötekiler 1-5. Sütunu ölçeksiz okumak yanıltır.

⚠️ `kesif` düşük (0.42/2) ve bu **kısmen tasarımın sonucu**: bu sınıfta 12 cevabın 11'i `turn_ending ∈ {durur, ozet, yalnizca_yansitma, takdir}` ile bitiyor, yani açık uçlu soruyla davet etmiyor. ⛔ «Tasarım gereği» demek **savunma değildir**: kotanın bu boyutu bastırıp bastırmadığı ölçülmedi.

⛔ Ortalama **karşılaştırmasız** bir sayıdır: bu kayıtların başka bir kümeyle kıyası yapılmadı ve n=12.

## A. Bu dalganın gürültü tabanı

Tekrar çifti: **4** (aynı kayıt, iki numara, ayrı öbek)

| boyut | aynı not % | ort. mutlak fark |
|---|---:|---:|
| `kesif` | 100 | 0 |
| `mi_uyumu` | 100 | 0 |
| `grounding` | 100 | 0 |
| `dogallik` | 100 | 0 |
| `duygusal_tepki` | 75 | 0.25 |
| `yorumlama` | 75 | 0.25 |
| `anlasilirlik` | 75 | 0.75 |

⛔⛔ **n=4 çift.** Taban kaba; güven aralığı hesaplanmadı ve başka bir dalganın tabanının yerine geçmez (K137: rubrik sürümü değişirse karşılaştırma geçersiz).

## B. Uydurma sondası — sınıfın kendi iddiası ÇÜRÜDÜ mü?

`grounding == 2` (yargıç: somut ayrıntının konuşmada karşılığı yok): **3/12 = %25**

⛔⛔ §7a″ bu sınıfı **uydurmaya karşı** tasarlamıştı. Ölçülen oran korpus tabanının (T238: %12) **ÜSTÜNDE**. ⇒ **Tasarım iddiası bu ölçümde DESTEKLENMEDİ.**

`klinik_guvenlik_ihlali`: **0/12** (Kural 3 tarafı temiz)

### Mekanizma — iddia değil, ölçüm

Hipotez: **cevabı tohumdan yazdım, kullanıcı mesajı ise tohumun kısaltması.** Yansıttığım ayrıntı mesajda yok, tohumda var. Sınama: uydurulan ayrıntının kökleri kullanıcı mesajında yok ama tohum metninde var mı?

| banka | uydurulan ayrıntı | mesajda yok | **tohumda var** | örnek kök |
|---:|---|---:|---:|---|
| #11 | «Güvensiz biriymişim gibi» dedin. | 3 | **2** | `biriy`, `güven` |
| #6 | baş ağrısıyla | 1 | **1** | `ağrıs` |
| #1 | arkadaşın şaka gibi söylemiş, sen yine de kafana takmışsın ve şimdi bi | 7 | **2** | `arkad`, `şaka` |

⇒ **3/3** uydurmada, mesajda bulunmayan ayrıntı **tohumda duruyor**. Uydurma serbest değil, **tohumdan sızıyor**.

⭐⭐⭐ **Eksik kapı, az önce yazdığım kapının AYNASI.** T264'te T217 kapısını yazdım: *«kullanıcı metni kendi tohumundan mı?»* Kimse tersini sormadı: ***«cevap yalnız kullanıcı metninden mi?»*** Tohum→mesaj kısaltması bilgiyi düşürüyor, cevap ise düşmeden önceki tohumu hatırlıyor. ⇒ Bu, kural yazılı-kapı yok ailesinin (T22) yeni bir üyesidir: `uretim-v5` uydurmayı **yasaklıyor**, hiçbir kapı **bakmıyor**.

⛔ **`celiskili_ok` 12/12 geçirdi** — çünkü o kapı yalnız çelişkinin adlandırılmasına ve iki pasaja atfa bakıyor; **yansıtma cümlesine bakmıyor**. Kapıdan geçmek temiz olmak değildir.

⛔⛔ **Şerhler — bu sayı ne kadar sağlam:** (1) n=12 ⇒ bir kayıt oranı ~%8 oynatır, güven aralığı hesaplanmadı, anlamlılık sınanmadı · (2) %12 **başka bir dalgada, başka kayıtlarla** ölçüldü ⇒ bu tam bir karşılaştırma değil, iki ayrı gözlemin yan yana konmasıdır · (3) `grounding` türetmesi **tek ayrıntı** sondasıdır (`en_somut_ayrinti`) ⇒ ölçülen oran bir **alt sınırdır**, gerçek uydurma bundan fazla olabilir · (4) tek yargıç ailesi, doğrulayan ikinci anotatör yok · (5) kök eşleme 5 harfe kısaltıyor ⇒ mekanizma tablosu yanlış pozitif verebilir.

## Yazılan dosyalar

| dosya | yargılanan | toplam |
|---|---:|---:|
| `data/judged/celiskili-parti2.claude.jsonl` | 6 | 6 |
| `data/judged/celiskili-pilot.claude.jsonl` | 6 | 6 |

## ⛔ Bunun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Körlük tam değil** | 12 kaydın hepsinde iki çelişkili `<context>` var ve cevapların hepsi çelişkiyi adlandırıyor ⇒ yargıç bunların **aynı sınıftan** olduğunu metinden anlayabilir. Numara karıştırma partiyi gizler, **sınıfı gizlemez** |
| ⛔ **Öbekleme bağımsızlık kaybı** | bir subagent öbeğindeki 8 kayıt aynı bağlamda duruyor ⇒ sıra ve çapa etkisi olabilir; tekrar çiftleri ayrı öbeklere düşürülerek bu etki tabana dahil edildi, ama **ayrıştırılmadı** |
| ⛔ **Tek yargıç ailesi** | yalnız Claude; bu kayıtlar için Gemini yargısı **yok** ⇒ K97'nin çapraz karşılaştırması burada yapılamadı |
| ⛔ **Kapı ≠ not** | 12 kaydın 12'si `celiskili_ok`'tan geçti; bu, iyi not aldıkları anlamına gelmez |
| ⚠️ **Kayıtları ben yazdım** | K30/K260: üretici de yargıyı okuyan da aynı taraf; bağımsız anotatör hâlâ borç |
