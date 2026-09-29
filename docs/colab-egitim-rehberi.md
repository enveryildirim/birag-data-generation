# Colab'da ince ayar rehberi — `v0.1.1` Faz 4 (ön kayıt EK-2)

> **Kime:** eğitimi Colab'da koşturacak kişi. **Ne:** `notebooks/v011-unsloth-egitim.ipynb`'i baştan sona,
> ön kaydı bozmadan koşturmak ve çıktıyı veri makinesine geri getirmek.
> **Dayanak:** `configs/deney/2026-09-29-v011-on-kayit-ek2.json` (mühür `bcc34e55726e2c94`) ·
> `reports/analiz/2026-09-29-v011-onkayit-ek2.md` · `src/colab_egitim.py`.
>
> ⛔ Defter ve `src/colab_egitim.py` **mühürlü**. Bu rehber onları değiştirmez; yalnız nasıl koşulacaklarını anlatır.
> Aşağıdaki kurallardan birine uyulamıyorsa **ilk çıktıdan önce durulur ve EK-3 yazılır** — koşup sonra düzeltilmez.

---

## 0. Bir bakışta

| | |
|---|---|
| **İş** | 2 kol × 8 tohum = **16 LoRA eğitimi** (her biri 2538 adım, batch 1 ⇒ 846 kayıtta 3 tur) + her biri için **6 eksen (124 öge) + çok turlu (10 konuşma × 4 tur)** üretim |
| **Kollar** | `v010u` = `datasets/v0.0.22/train.jsonl` (içerik `v0.1.0` ile aynı, `6fcb6b1e16290575`) · `v011u` = `datasets/v0.1.1/train.jsonl` (`f8fcaa1e96603cb2`) |
| **Tohumlar** | 7 · 13 · 23 · 31 · 37 · 41 · 43 · 47 |
| **Donanım** | GPU ≥ 22 GB — **A100 ya da L4**. T4 (16 GB) yetmez; defter durur |
| **Hassasiyet** | **bf16, 4-bit YOK** |
| **Süre** | ⚠️ **Ölçülmedi.** İlk eğitimin sonunda defter `sure_dk` yazar; toplamı oradan hesaplayın (≈ 16 × o değer + üretim) |
| **Colab'ın işi** | yalnız **eğitim + ham üretim**. Puanlama ve hüküm veri makinesinde (§7) |

---

## 1. Başlamadan önce — kontrol listesi

- [ ] **Depo güncel mi?** Colab kodu GitHub'dan klonluyor. Veri makinesinde `git status -sb` → `## main...origin/main` (ileride commit yok) olmalı.
      2026-09-29 itibarıyla senkron; depo **herkese açık** ⇒ `GITHUB_TOKEN` gerekmez.
- [ ] **Colab planı** A100 ya da L4 veriyor mu? (Ücretsiz katman genelde T4 verir — yetmez.)
- [ ] **Google Drive'da yer** var mı? Adapter'lar küçük (r = 8, 8 katman, yalnız q/o), ama kontrol noktaları ve üretim dosyaları 16 koşu boyunca birikir. Birkaç GB boş yer bırakın.
- [ ] **İki kararı verdiniz mi?** (§2) — ilk oturumdan sonra **değiştirilemez**.

---

## 2. İlk oturumdan önce verilecek iki karar

Defterin 1. hücresindeki iki parametre, ilk oturumda `ortam-referans.json`'a yazılır ve **sonraki 15 koşuda aynı olmak zorundadır**
(`SABIT_ALANLAR`: model kimliği · model revizyonu · LoRA yolu · şablon SHA · kütüphane sürümleri · üretim ayarı).

### 2.1 `MODEL_ID`

| seçenek | durum |
|---|---|
| `unsloth/gemma-4-E4B-it` (defter varsayılanı) | ✅ Hugging Face'te var, **BF16 tam ağırlık** (nicemlenmiş değil), apache-2.0, erişim kapısı görülmedi (sayfa 2026-09-29'da açıldı) |
| `google/gemma-4-E4B-it` (aslı) | `plan.md` §0'da onaylı model kartı. `e3`'ün MLX tabanı bunun kopyasıydı |

⚠️ Unsloth kopyasının ağırlıklarının Google aslıyla **birebir aynı** olduğu doğrulanmadı. EK-2'de iki kol da aynı tabanı kullandığı için
**kıyas geçerli kalır** — önemli olan 16 koşunun aynı tabanı kullanması. Revizyon (commit SHA) ilk oturumda kendiliğinden sabitlenir.

### 2.2 `LORA_YOLU`

`"unsloth"` (varsayılan) ile başlayın. Kurulum sınaması (§4, hücre 7) **LoRA denetiminde durursa** ve **henüz hiç eğitim yapılmadıysa**
`"peft"` yapıp 1. hücreden yeniden koşun. Referans yazıldıktan sonra değiştirmek ortam denetimini durdurur — bu tasarım gereği.

---

## 3. Defteri açma

1. Tarayıcıda açın:
   `https://colab.research.google.com/github/enveryildirim/birag-data-generation/blob/main/notebooks/v011-unsloth-egitim.ipynb`
2. **Çalışma zamanı → Çalışma zamanı türünü değiştir → GPU: A100 (ya da L4)**.
3. İlk hücrede yalnız `MODEL_ID` / `LORA_YOLU`'na dokunun (§2). `DRIVE_KOK` varsayılanı `/content/drive/MyDrive/birag-v011` —
   değiştirirseniz **her oturumda aynı** yolu verin; aksi hâlde defter biten işi göremez ve baştan başlar.

⛔ Başka hücreyi düzenlemeyin. Colab'daki düzenleme depoya yazılmaz ama koşulan kod artık mühürlü kod olmaz.

---

## 4. Hücre hücre

| hücre | ne yapar | normalde ne görürsünüz | durursa |
|---|---|---|---|
| **2 · Parametreler** | §2 | — | — |
| **4 · Drive + depo** | Drive'ı bağlar, depoyu klonlar (varsa `pull --ff-only`) | son commit satırı — veri makinesindeki `git log -1` ile **aynı** olmalı | `pull` reddedilirse Colab'daki klon kirlenmiş: `/content/birag-data-generation`'ı silip yeniden koşun |
| **5 · Kurulum** | `pip install unsloth` | Colab *«oturumu yeniden başlat»* isteyebilir | yeniden başlatıp **1. hücreden** devam |
| **7 · Kurulum sınaması** | mühür (55 dosya) · GPU ≥ 22 GB · 35 şablon dizgesi · ≤ 2048 jeton (iki kol) · LoRA hedefleri ve parametre sayısı · ortam referansı | `mühürlü dosya: 55` · `şablon: 35` · `LoRA denetimi: …` · ilk oturumda `ortam: referans yazıldı`, sonra `referansla aynı` | §6'daki tablo |
| **9 · Eğitim** | 16 koşu, tohum içinde dönüşümlü (`v010u-t7`, `v011u-t7`, `v010u-t13` …). Adapter varsa atlar, yarıda kaldıysa son kontrol noktasından sürer | her koşu için `✅ kol-tT: N dk · sürdü=… · son eval_loss …` | §6 |
| **11 · Üretim** | her koşu için 6 eksen + çok turlu; `thinking` kapalı · 1024 jeton · açgözlü | her dizin adı; biten koşu `üretim zaten tam` | `⛔ … eğitilmemiş` ⇒ önce hücre 9 |
| **13 · Paket** | `eğitim N/16 · üretim M/16`; 16/16 olunca `v011-colab-ciktilari.zip` | `✅ paket: …/v011-colab-ciktilari.zip` | 16/16 değilse paket yazılmaz — hücre 9/11'e dönün |

⭐ **İlk eğitim bittiğinde** `sure_dk` değerini not edin. Toplam süre ve kaç oturum gerektiği buradan çıkar.

---

## 5. Oturum koparsa

Colab oturumları zaman aşımıyla kapanır; defter buna göre yazıldı.

1. Aynı GPU türünü seçin (farklı GPU **uyarı** verir ama durdurmaz; model/kütüphane/LoRA yolu farkı **durdurur**).
2. **1. hücreden** sırayla yeniden koşun. Biten eğitim ve üretim atlanır; yarıda kalan eğitim `ckpt/checkpoint-*`'ten sürer (846 adımda bir kayıt).
3. ⚠️ `pip install unsloth` her yeni oturumda **en son** sürümü kurar. Sürüm değişmişse hücre 7 `⛔ ortam referanstan farklı … surumler` der.
   Bu durumda **durun** — ortam referansındaki sürümleri sabitlemek (`pip install unsloth==…`) bir sapmadır ve EK-3 gerektirir.
   ⭐ Önlem: ilk oturumda `ortam-referans.json`'daki `surumler` alanını not edin.

⛔ Oturum ortasında `DRIVE_KOK`'taki bir dizini silmeyin; özellikle `ortam-referans.json`'ı. Silinirse bir sonraki oturum yeni referans yazar
ve iki kolun aynı ortamda olduğu kanıtı kaybolur.

---

## 6. Durma mesajları — ne demek, ne yapılır

Her `⛔` mesajı **tasarım gereği** durdurur. Kodu düzenleyerek geçmeyin.

| mesaj | anlamı | ne yapılır |
|---|---|---|
| `⛔ mühür bozuk (…)` | klonlanan dosyalar ön kayıttaki SHA ile aynı değil | Colab'daki klonu silip yeniden klonlayın. Sürerse veri makinesinde bildirin — mühürlü bir dosya değişmiş olabilir |
| `⛔ GPU N GB — …` | T4 ya da küçük GPU | A100/L4 seçin. 4-bit'e geçmek EK-3 gerektirir |
| `⛔ bos_token … ≠ referans` · `⛔ şablon çıktısı referansla uyuşmuyor` | tokenizer, eğitim şablonunu farklı kodluyor (K44 sınıfı kusur) | **durun, bildirin.** `MODEL_ID` yanlış model olabilir |
| `⛔ N jeton > max_seq 2048` | bir kayıt 2048 jetonu aşıyor; sessiz kırpma kıyası bozar | **durun, bildirin** — veri tarafının işi |
| `⛔ önek hizası bozuk` | kayıp maskesi hedefin içine kayıyor | **durun, bildirin** |
| `⛔ LoRA hedefleri uyuşmuyor` · `⛔ eğitilebilir parametre … ≠ beklenen` | LoRA yanlış modüllere ya da fazladan modüle (ör. görü kulesi) kondu | **hiç eğitim yapılmadıysa** `LORA_YOLU = "peft"` (§2.2); yapıldıysa durun |
| `⛔ ortam referanstan farklı … {alan: (eski, yeni)}` | model / revizyon / LoRA yolu / şablon / kütüphane sürümü değişti | §5 madde 3. Hangi alanın değiştiğini not edip bildirin |
| `⛔ … eğitilmemiş — önce 4. adım` | üretim, adapter'dan önce çağrıldı | hücre 9'u bitirin |
| CUDA *out of memory* | GPU belleği yetmedi | çalışma zamanını yeniden başlatıp 1. hücreden. Sürerse daha büyük GPU |

---

## 7. Veri makinesine dönüş

1. Drive'dan `birag-v011/v011-colab-ciktilari.zip`'i indirin.
2. Depoda açın — içindeki `eksen-kosu/` ve `cok-turlu-kosu/` dizinleri **`reports/analiz/` altına** gelecek:

   ```bash
   unzip ~/Downloads/v011-colab-ciktilari.zip -d /tmp/v011-colab
   ```

   ```bash
   cp -R /tmp/v011-colab/eksen-kosu /tmp/v011-colab/cok-turlu-kosu reports/analiz/
   ```

3. Puanlama (model koşmaz; `ham.jsonl` ve `ortam.json`'a dokunmadığını kendisi denetler):

   ```bash
   uv run python scripts/analiz/2026-09-29-v011-colab-puanla.py
   ```

4. Hüküm:

   ```bash
   uv run python scripts/analiz/2026-09-29-v011-onkayit-ek2-cozumleme.py
   ```

   → `reports/analiz/2026-09-29-v011-onkayit-ek2-sonuc.md`. Çözümleme mühür, tamlık (2 kol × 8 tohum × 7 hücre), ayar ve ortam
   kilitleri geçmeden **puan okumaz**.

⭐ Adapter'lar (`runs/*/adapter`) pakete **girmez** — hüküm için gerekmiyor. Saklamak isterseniz Drive'da bırakın; `runs/` hiçbir zaman silinmez kuralı
buraya da uygulanır.

---

## 8. Yapılmayacaklar

| ⛔ | neden |
|---|---|
| 4-bit / QLoRA yükleme | `e3` bf16; ön kayıt bf16 varsayıyor |
| Yalnız bir kolu koşmak, ya da bir kolu başka oturumda/ortamda bitirip ötekini sonra | EK-2'nin bütün dayanağı iki kolun aynı ortamda olması; dönüşümlü sıra bunun için |
| Hücreleri, tarifi (`configs/training/*.yaml`) ya da `src/colab_egitim.py`'yi Colab'da düzenlemek | mühürlü kodla koşulmayan ölçüm ön kayda ait değildir |
| Referans yazıldıktan sonra `MODEL_ID` / `LORA_YOLU` değiştirmek | ortam denetimi durdurur; aşmak kıyası geçersiz kılar |
| Colab'da puanlamak ya da sonuçlara bakıp yeniden eğitmek | puanlama ve hüküm veri makinesinde; sonuç görüldükten sonra yapılan değişiklik ön kaydın dışındadır |
| Kayıtlı MLX `e3` koşularıyla Colab sonuçlarını doğrudan karşılaştırmak | farklı çerçeve; EK-2 onları hükümden çıkardı |

---

## 9. Bilinenler ve bilinmeyenler

- ✅ Maske, bölme (846/212, `random.Random(7)`), LoRA hedefi, şablon ve puanlama yolu veri makinesinde **modelsiz** sınandı (`reports/analiz/2026-09-29-v011-onkayit-ek2.md`).
- ⛔ Unsloth + gerçek Gemma 4 **hiç koşulmadı** — `FastModel.from_pretrained(revision=…)` ve tam adlı `target_modules` davranışı ilk kez Colab'da görülecek. Hücre 7'nin denetimleri bunun için var.
- ⚠️ MLX AdamW `bias_correction=False`, torch'ta hep açık: **yapılandırma düzeyindeki** tek birebir aktarılamayan ayar; iki kolda aynı. Sayısal eşdeğerlik zaten beklenmez (`docs/tez/makale-literatur-taramasi.md` §4.5).
- ⚠️ Süre ve maliyet ölçülmedi (§0).
