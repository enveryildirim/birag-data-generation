# Koşu kaydı §3.2'yi tutuyor mu — ve `datasets/` gerçekten değişmez mi?

**Betik:** `scripts/analiz/2026-09-16-kosu-kaydi-denetimi.py` · **Tarih:** 2026-09-16  
**Girdi:** `runs/*/metrics.json` — **24** koşu  
**Girdi:** `datasets/v*/` — **5** sürüm  
**Girdi:** `src/build.py` SHA256 `fb37ac9b76a38c1d` (türetme **çağrılıyor**)  
**Girdi:** `src/train.py` SHA256 `ec4d5b61a1a2899d`  
**Girdi:** `docs/tez/tez-plani.md` SHA256 `ee22ce0e736d5cb6`  
**Girdi:** `plan.md` SHA256 `03890b9dc3e204b3`

---

## Neden

T65 *«donanım hiçbir koşuda kayıtlı değil»* dedi ve doğruydu — ama §3.2'nin
**tek** kalemine bakmıştı. Bir kural ilan edilip denetlenmezse tutulmuyor;
⭐ denetlenmemiş kalem sayısı bilinmiyorsa **dersin kendisi de ölçülmemiş**
demektir. Burada ilan edilen bütün kalemler tek tek sınanıyor.

**İlan yerleri — okur karşılaştırabilsin diye basılıyor:**

· `docs/tez/tez-plani.md:75` → *`metrics.json` · `samples.md` · dataset sürümü + hash · **rastgele tohum** ·*  
· `plan.md:659` → *| Deney takibi | `runs/<ts>/{config.yaml, metrics.json, samples.md}` |*

---

## 1. §3.2'nin sekiz kalemi — hangisi kaç koşuda var

| Kalem | Tutan koşu | |
|---|---:|---|
| `config.yaml` | **24**/24 | ✅ |
| `metrics.json` | **24**/24 | ✅ |
| `samples.md` | **0**/24 | ⛔ **hiçbirinde** |
| `dataset sürümü` | **24**/24 | ✅ |
| `dataset hash` | **0**/24 | ⛔ **hiçbirinde** |
| `rastgele tohum` | **24**/24 | ✅ |
| `git commit` | **24**/24 | ✅ |
| `donanım` | **0**/24 | ⛔ **hiçbirinde** |

⛔ **3 kalem 24 koşunun HİÇBİRİNDE yok:** `samples.md`, `dataset hash`, `donanım`.

⚠️ Bunların **yalnızca biri** (`donanım`) daha önce ölçülmüştü (T65). Öteki 2 kalem ilan edildiği günden beri **hiç sorulmamıştı** — ve `samples.md` **iki ayrı yerde** ilan edilip **hiçbir yerde üretilmiyor**.

➡️ *İlan ile üretim arasındaki mesafe tek bir kalemde ölçülünce küçük görünür;*
*kalem sayısı ölçülünce kuralın kendisinin işlemediği görünür.*

## 2. Koşu kırılımı — eksik kalem koşuya göre değişiyor mu

| Koşu | eksik |
|---|---|
| `20260912-154712-e4b-v0.0.1-pilot` | `samples.md`, `dataset hash`, `donanım` |
| `20260912-181209-e4b-thinking-dili-ustsinir` | `samples.md`, `dataset hash`, `donanım` |
| `20260912-182429-e4b-thinking-dili-genis` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-113647-f4-kapsam-A-dar` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-113813-f4-kapsam-B-derin` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-114013-f4-kapsam-C-dikkat` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-114222-f4-kapsam-D-tam` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-114455-f4-kapsam-E-genis` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-134832-f4b-kapsam-A-dar` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-135039-f4b-kapsam-B-derin` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-135336-f4b-kapsam-C-dikkat` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-135702-f4b-kapsam-D-tam` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-140038-f4b-kapsam-E-genis` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-140420-f4b-kapsam-A-dar-280adim` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-162051-f4c-doz10-A-dar` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-162241-f4c-doz10-B-derin` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-162537-f4c-doz10-C-dikkat` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-162837-f4c-doz10-D-tam` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-163205-f4c-doz10-E-genis` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-163538-f4c-doz25-A-dar` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-163738-f4c-doz25-B-derin` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-164037-f4c-doz25-C-dikkat` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-164339-f4c-doz25-D-tam` | `samples.md`, `dataset hash`, `donanım` |
| `20260915-164715-f4c-doz25-E-genis` | `samples.md`, `dataset hash`, `donanım` |

⭐ **1 farklı eksik deseni** var. Tek desen ⇒ bu bir koşu hatası değil, **yazıcının kendisinin** eksiği: `src/train.py` bu alanları hiç üretmiyor.

## 3. ⭐⭐ `datasets/` IMMUTABLE ilan edildi — ilk kez DOĞRULANIYOR

Kural 4 `datasets/vX.Y.Z/`'yi değişmez ilan ediyor. `manifest.json` bir SHA256
taşıyor — ⛔ ama o hash **yukarı akıştaki** `data/judged/*.jsonl` dosyasının,
**setin kendi artefaktının değil**. ⇒ `train.jsonl` bugün değiştirilse hiçbir
kayıt bunu göstermez. İki bağımsız yoldan bakılıyor.

### 3a. Yukarı akış — ilan edilen hash bugün tutuyor mu

| Sürüm | `input_file` | ilan | bugün | |
|---|---|---|---|---|
| `v0.0.1` | `data/judged/v0.0.1.jsonl` | `d7d1e578e8a39977` | `d7d1e578e8a39977` | ✅ |
| `v0.0.2` | `data/judged/v0.0.2.jsonl` | `ee1b6d88dafa6b49` | `ee1b6d88dafa6b49` | ✅ |
| `v0.0.3` | `data/judged/v0.0.3.jsonl` | `9451388c0533f9ea` | `9451388c0533f9ea` | ✅ |
| `v0.0.4` | `data/judged/v0.0.4.jsonl` | `e0e0ca6464ddf74f` | `e0e0ca6464ddf74f` | ✅ |
| `v0.0.5` | `data/judged/v0.0.5.jsonl` | `c61a40e538fa6653` | `c61a40e538fa6653` | ✅ |

**5/5** tutuyor.

### 3b. ⭐ Artefaktın kendisi — `src/build.py` ÇAĞRILARAK yeniden türetildi

Türetme mantığı **kopyalanmıyor**: `src/build.py` içe aktarılıp `main()`
çağrılıyor, değişen tek şey çıktı kökü (geçici dizin). ⛔ `datasets/` yazılmıyor.

| Sürüm | `train.jsonl` bugün | yeniden türetilen | satır | |
|---|---|---|---:|---|
| `v0.0.1` | `cff23210d80ebd81` | `cff23210d80ebd81` | 20 | ✅ **bayt bayt aynı** |
| `v0.0.2` | `b78103aecb627e63` | `b78103aecb627e63` | 117 | ✅ **bayt bayt aynı** |
| `v0.0.3` | `b50f7588e085f212` | `b50f7588e085f212` | 155 | ✅ **bayt bayt aynı** |
| `v0.0.4` | `8c15ee2349e45124` | `8c15ee2349e45124` | 155 | ✅ **bayt bayt aynı** |
| `v0.0.5` | `d8e465c50bea4fca` | `d8e465c50bea4fca` | 155 | ✅ **bayt bayt aynı** |

⭐⭐ **5/5 sürüm bayt bayt yeniden türetiliyor.** Kural 4'ün değişmezlik iddiası ilan edildiği günden beri ilk kez **sınandı** ve tuttu.

⚠️ **Ama bu güvence KOŞULLU ve hash kaydının yerine GEÇMEZ.** (3b) yalnızca
`build.py` saf bir fonksiyon olduğu sürece çalışır. Betik yarın değişirse
karşılaştırma bozulur ve ⛔ *«set mi değişti, türetici mi»* sorusu **cevapsız**
kalır — çünkü ayıracak bir kayıt yok. ➡️ *Yeniden türetme değişmezliği ölçmez;*
*değişmezlik ile türeticinin kararlılığının ÇARPIMINI ölçer. Hash kaydı ikisini*
*ayırabilen tek şeydir — ve tam bu yüzden gerekli.*

## 4. Bugünün mührü — geçmişe yazılamıyor, buraya yazılıyor

⛔ `datasets/` IMMUTABLE olduğu için 5 manifest'e hash **eklenemez** (Kural 4),
geçmiş 24 koşuya donanım **yazılamaz** (Kural 7: `runs/` üzerine yazılmaz).
⭐ Kaydın gidebileceği tek yer bu rapor: tarihli, betiğe bağlı, üzerine
yazılmayan bir dosya. **Bundan sonraki her sapma buraya karşı ölçülür.**

| Artefakt | SHA256 (16) |
|---|---|
| `datasets/v0.0.1/train.jsonl` | `cff23210d80ebd81` |
| `datasets/v0.0.1/manifest.json` | `0186afd84f20188e` |
| `datasets/v0.0.2/train.jsonl` | `b78103aecb627e63` |
| `datasets/v0.0.2/manifest.json` | `8ef61d9adfe2a5d0` |
| `datasets/v0.0.3/train.jsonl` | `b50f7588e085f212` |
| `datasets/v0.0.3/manifest.json` | `893ff1f3be9ab119` |
| `datasets/v0.0.4/train.jsonl` | `8c15ee2349e45124` |
| `datasets/v0.0.4/manifest.json` | `8eed01e09bb9ac10` |
| `datasets/v0.0.5/train.jsonl` | `d8e465c50bea4fca` |
| `datasets/v0.0.5/manifest.json` | `f2fe89112deab912` |
| `src/build.py` | `fb37ac9b76a38c1d` |

## 5. `src/train.py` bugün hangi alanları yazıyor

⚠️ Bu liste **koşulardan değil betikten** okunuyor — yani bundan sonraki
koşuların ne taşıyacağını gösterir, geçmişin ne taşıdığını değil.

| | |
|---|---|
| `metrics` sözlüğünün alanları | `config`, `dataset`, `donanim`, `donus_kodu`, `git_rev`, `iters`, `model`, `n_train`, `n_valid`, `run`, `seed`, `sure_saniye`, `tarih` |
| `samples.md` üretiliyor mu | ✅ evet |

## 5b. ⭐ İlk otomatik donanım kaydı — elle yazılanla karşılaştırıldı

⛔ Geçmiş 24 koşuda donanım yok; tez bunun yerine `PROJECT_MEMORY.md`'nin
**elle yazılmış** ortam başlığına dayanacaktı. O başlık şimdi ilk kez
ölçümle karşılaştırılıyor — donanım okuması `src/train.py`'den **çağrılıyor**,
burada yeniden yazılmıyor.

**Elle yazılan** (`PROJECT_MEMORY.md:36`): ***Donanım:** Apple M5 Max (18 çekirdek) · 128 GB unified memory · macOS 26.6.2 (Darwin 25.6.0) · Metal çalışma kümesi 107.5 GB*

**Ölçülen:**

| Alan | Değer |
|---|---|
| `platform` | `macOS-26.6.2-arm64-arm-64bit` |
| `makine` | `arm64` |
| `islemci` | `Apple M5 Max` |
| `cekirdek` | `18` |
| `bellek_gb` | `128.0` |
| `python` | `3.12.14` |
| `mlx` | `0.32.2` |
| `mlx_lm` | `0.31.3` |
| `metal_calisma_kumesi_gb` | `107.5` |

✅ **Sürüm dizgesi tutuyor.**

⚠️ Ama bu satır 2026-09-16'ya kadar `macOS 25.6` taşıyordu ve o **Darwin çekirdek** sürümüdür, macOS sürümü değil (K144 · T72). ⛔ Çelişki 24 koşu boyunca kimsenin gözüne çarpmadı; ⭐ onu gösteren ilk şey **ilk otomatik kayıt** oldu.

➡️ *T65'in dersi burada kendini gösteriyor: elle tutulan alan sessizce*
*kayar ve kaydığını gösteren bir şey yoktur. Yanlış olan sayı büyük değil —*
*⚠️ önemli olan, yanlışlığın ancak ölçüm devreye girince görünmesi.*

## 6. ⭐ Yazıcı sınandı — geçici kökte gerçek bir koşu

§1 **geçmişi** ölçüyor, §5 **betiği okuyor**. ⛔ İkisi de yazıcının
gerçekten yazdığını göstermez: bir alanın kodda görünmesi, koşu bittiğinde
dosyaya düştüğü anlamına gelmez. ⭐ Burada `src/train.py:main()` **çağrılıyor**
— 50 adım gerçek MLX LoRA — ama kök geçici bir dizin, ⛔ `runs/` dokunulmuyor.

| Kalem | Yazıldı mı |
|---|---|
| `config.yaml` | ✅ |
| `metrics.json` | ✅ |
| `samples.md` | ✅ |
| `dataset sürümü` | ✅ |
| `dataset hash` | ✅ |
| `rastgele tohum` | ✅ |
| `git commit` | ✅ |
| `donanım` | ✅ |
| `dönüş kodu 0` | ✅ |

⭐ **9/9** — yazıcı §3.2'nin sekiz kalemini de üretiyor ve koşu sıfırla dönüyor.

⭐ **Çapraz kontrol:** koşunun yazdığı `dataset_sha256_16` = `cff23210d80ebd81`, §4'te mühürlenen `datasets/v0.0.1/train.jsonl` = `cff23210d80ebd81` → **aynı**. Yani kaydedilen hash gerçekten setin hash'i.

⚠️ **Bu bir koşu kaydı DEĞİL** — geçici kökte koştu ve silindi. `runs/`
hâlâ 24 koşu taşıyor ve **hiçbirinde** bu alanlar yok. ➡️ *Kalem*
*«düzeltildi» değil «yazıcıda kapandı, kayıtta henüz açık»dır; ilk gerçek*
*koşuya kadar §1 tablosu 0/24 göstermeye devam edecek ve göstermelidir.*

## ⛔ Bu denetimin söylemedikleri

| | |
|---|---|
| ⛔ `samples.md`'nin **içeriği** | §3.2 dosyayı ilan ediyor, içeriğini tanımlamıyor. Ne yazılacağı bir karardır, ölçüm değil |
| ⛔ Geçmiş 24 koşunun donanımı | geri yazılamaz; tezde *«koşu kaydında yok, ortam `PROJECT_MEMORY.md` başlığında sabit»* notu düşülecek |
| ⚠️ (3b)'nin güvencesi | koşullu — `build.py` değişirse ayrım kaybolur (§3b) |
| ⚠️ `eval` koşuları | bu denetim yalnızca **eğitim** koşularına bakıyor; `runs/*/eval/*` ayrı bir kayıt disiplini ve ayrıca sınanmadı |

