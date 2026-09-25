# Gösterge seçimi sınaması — bayraklar neden ateşlemiyor

**Girdi:** `data/candidates/expert-70.jsonl` · SHA256 `ee61043de8d38187cc41b7a6c5391b735bfcc8daf9e12af504317ef0041aa775`  
**Uzman:** `data/expert_sample/uzman-puanlari.json` · SHA256 `d9d36c10691157a90173da8452ceffc47c3d88782b91bd7a8e4ecf11e492263c`  
**Betik:** `scripts/analiz/2026-09-14-gosterge-secimi.py` · **Tarih:** 2026-09-14  
**Kayıt:** 70

> v4'ün `dogallik` bayrakları ve TIP 35 tuzakları hiç ateşlemedi. İki rakip açıklama: **(A)** judge gevşek · **(B)** kusur korpusta yok çünkü `checks.py` onu üretimde zaten eliyor. Bu betik ikisini ayırıyor — judge'a hiç bakmadan, yalnızca metni tarayarak.

---

## 1. Yasak ifade kapısı korpusta ne buluyor

`configs/filters.yaml` kategorileri, 70 cevabın metninde:

| Kategori | Eşleşen kayıt | v4'teki karşılığı |
|---|---:|---|
| `bos_guvence` | 0/70 | `bos_guvence` bayrağı |
| `etiketleme` | 0/70 | `tuzak_etiketleme` |
| `emredici_kip` | 0/70 | `tuzak_erken_tavsiye` ile akraba |
| `utanc_buyutme` | 0/70 | `tuzak_suclama` ile akraba |
| `zararli_normallestirme` | 0/70 | — |
| `ahlaki_yargi_klinik` | 0/70 | — |
| `rol_siniri` | 1/70 | `rol_siniri_ihlali` |
| `kriz_yasagi` | 0/70 | — |

**Bu tablo (B) şıkkını destekliyor:** doğallık bayraklarının üçü (`bos_guvence`, etiketleme kaynaklı `tuzak_etiketleme`, emredici kip) üretimde **zaten eleniyor**. Judge'a ulaşan korpus bu kusurları taşımıyor; dolayısıyla o bayrakların ateşlememesi doğru davranıştır, körlük değil.

## 2. Diğer doğallık göstergeleri — kodla tarandığında

| Gösterge | Desen | Eşleşen kayıt |
|---|---|---:|
| `siz_kaymasi` | `siz` / `-sınız` | 0/70 |
| `klise_acilis` | cevabın ilk kelimeleri | 0/70 |
| `terapi_jargonu` | farkındalık · içgörü · duygudurum … | 0/70 |
| `ovgu_tonu` | harika · mükemmel · gurur duy … | 0/70 |

⚠️ Bunlar **vekil** desenler (K40): kalıbı yakalar, anlamı değil. Sıfıra yakın çıkmaları, göstergenin bu korpusta **ayırt edici olmadığını** gösterir — judge'ın onları görememesinden bağımsız bir bulgu.

## 3. `ozerklik_vurgusu` — judge 0 buldu, metin ne diyor

K20 ifade bankasının *Özerklik saygısı* kalıplarıyla tarandığında: **2/70** kayıtta eşleşme.

| Kayıt | Eşleşen bölüm |
|---|---|
| #28 | …un ve ikisi de senin. Ne yapacağını ben söylemeyeceğim; söylesem bile o iki ses yerinde durmay… |
| #55 | …eremem; o kapıdan girmek de girmemek de senin kararın olmalı, benim değil.

İçeri girersen ki… |

Bu bir **çelişki sinyali** olabilir: judge hiçbir kayıtta özerklik vurgusu görmediyse ama metinde kalıp varsa, ikili sorunun tanımı dar ya da judge bu beceriyi tanımıyor demektir. Tersine, metinde de yoksa üretim talimatının özerklik vurgusunu **yeterince üretmediği** anlaşılır — bu ikincisi `uretim-v3.md` için doğrudan bir düzeltme kalemidir.

## 4. Uzmanın gözünde `dogallik` ayrı bir boyut mu

Uzmanın **dil bütünlüğü** ile **kısalık/doğallık** puanları (n=46):

| Ölçüm | Değer |
|---|---|
| Pearson r | **+0.97** |
| İki puanın birebir aynı olduğu kayıt | 43/46 (%93) |
| Dil dağılımı | `{1: 2, 2: 3, 3: 1, 4: 1, 5: 39}` |
| Doğallık dağılımı | `{1: 5, 2: 1, 4: 1, 5: 39}` |

**r = +0.97 — uzman bu iki maddeyi pratikte tek bir şey olarak doldurmuş.** Doğallık bu korpusta ayrı bir boyut değil; bir cevabı "yapay" bulduğunda zaten "anlaşılmaz" da buluyor. Bu durumda `dogallik` için ayrım aramak, **var olmayan bir ayrımı aramaktır** — v4'ün negatif sonucunun uzman tarafındaki karşılığı.

## 5. Sonuç — gösterge nasıl seçilmeli

1. **Ayrıştırma, ayrıştırılan özellik korpusta değişmiyorsa ayrım üretemez.** `anlasilirlik` çalıştı çünkü anlaşılmazlık **hiçbir kapıdan geçmiyor**: ölçülmediği için korpusta duruyor ve varyansı var.
2. **Zaten kapıda elenen kusuru judge'a sormak boşa soru.** Doğallık bayraklarının üçü `configs/filters.yaml` listelerinin kopyası; o kusurlar judge'a ulaşmadan eleniyor.
3. **Gösterge seçme kuralı (öneri):** bir boyutu ayrıştırırken, önce o göstergenin korpusta **ateşleyip ateşlemediğine kodla bak**. Ateşlemiyorsa ya kapı zaten hallediyordur ya da gösterge yanlıştır; ikisinde de judge'a sormanın getirisi yok.

> Bu rapor judge çıktısına **hiç bakmadan** yazıldı; yalnızca korpus metni ve uzman puanları kullanıldı. v4 sonucundan bağımsız olarak geçerlidir.

