# Colab'da ince ayar rehberi — `v0.1.1` Faz 4

> **Defter:** [`notebooks/v011-basit-egitim.ipynb`](../notebooks/v011-basit-egitim.ipynb) — Unsloth'un *Gemma4 (E4B) Text*
> örneğinin akışında, bütün eğitim kodu defterin içinde görünür.
> **Dayanak:** ön kayıt `configs/deney/2026-09-29-v011-on-kayit*.json` · tarif `configs/training/*-t{tohum}.yaml` ·
> Unsloth belgeleri *Gemma 4 — How to Run Locally* ve *Gemma 4 Fine-tuning Guide* (kullanıcı verdi, 2026-09-30).
>
> ⛔ **Ön kayıt notu:** EK-2 mühürlü defteri (`notebooks/v011-unsloth-egitim.ipynb` + `src/colab_egitim.py`) koşucu olarak
> tanımlıyordu. Bu defter onun yerine geçiyorsa, **ilk koşudan önce EK-3** yazılmalı (koşucu değişti, tarif aynı).
> Eski defter depoda kalır — mühürlü dosya olduğu için silinirse çözümleme durur.

---

## 0. Bir bakışta

| | |
|---|---|
| **Bir koşu** | bir kol × bir tohum: eğitim (2538 adım) + 6 eksen (124 öge) + çok turlu (10 konuşma × 4 tur) |
| **Faz 4** | 16 koşu — sıra defterin ilk hücresindeki tabloda (tohum içinde `v010u` → `v011u`) |
| **Kollar** | `v010u` = `datasets/v0.0.22` (içerik `v0.1.0` ile aynı) · `v011u` = `datasets/v0.1.1` |
| **GPU** | **A100 ya da L4.** Unsloth'a göre E4B LoRA ~17 GB ister; T4 (16 GB) yetmez |
| **Hassasiyet** | **bf16, 4-bit yok** |
| **Süre** | ⚠️ ölçülmedi — ilk eğitimin sonunda defter `N dk` yazar |
| **Colab'ın işi** | eğitim + ham üretim. **Puanlama ve hüküm veri makinesinde** (§5) |

---

## 1. Nasıl koşulur

1. Aç: `https://colab.research.google.com/github/enveryildirim/birag-data-generation/blob/main/notebooks/v011-basit-egitim.ipynb`
   (depo herkese açık — belirteç gerekmez).
2. **Çalışma zamanı → Çalışma zamanı türünü değiştir → A100 ya da L4.**
3. 2. hücrede **`KOL`** ve **`TOHUM`**'u seçin. Başka hiçbir şeye dokunmayın.
4. **Çalışma zamanı → Tümünü çalıştır.**
5. Bitince bir sonraki koşunun `KOL`/`TOHUM`'unu yazıp tekrar *Tümünü çalıştır*. **Çalışma zamanını yeniden başlatmak** bellek için iyi olur.

**Oturum koparsa:** aynı `KOL`/`TOHUM` ile yeniden *Tümünü çalıştır*. Adapter varsa eğitim atlanır; yarım eğitim Drive'daki
son kontrol noktasından sürer (846 adımda bir); bitmiş üretim setleri atlanır.

---

## 2. Hücreler

| # | hücre | ne görmelisiniz |
|---|---|---|
| 1 | Kurulum | (çıktı gizli) — Colab *«oturumu yeniden başlat»* isterse yeniden başlatıp devam |
| 2 | Parametreler | — |
| 3 | Drive + depo | `depo: <commit>` — veri makinesindeki `git log -1` ile aynı olmalı |
| 4 | Modeli yükle | `GPU: … · model: unsloth/gemma-4-E4B-it <revizyon>` |
| 5 | Şablon | — |
| 6 | Veri | `…: 846 eğitim / 212 doğrulama` |
| 7 | Eğit | `şablon denetimi: 35 …` · `dil katmanı N · LoRA katmanları … · 16 modül` · eğitilebilir parametre · kayıp günlüğü · `✅ kol-tT: N dk · son eval_loss …` |
| 8 | Ortam kaydı | ilk koşuda `referans yazıldı`, sonra `referansla aynı` |
| 9 | Üret | 6 eksen + `cokturlu` için `✅ <dizin>` |
| 10 | Paket | `üretimi tam koşu: N/16`; 16/16'da `✅ paket: …/v011-colab-ciktilari.zip` |

⭐ **Kayıp değeri yüksek görünebilir.** Unsloth belgesine göre E2B/E4B'de 13–15 civarı kayıp *normal* (çok kipli modellerin bir tuhaflığı).
100–300 gibi değerler ise gradyan biriktirme hatasının işaretidir; bizde biriktirme yok (batch 1).

---

## 3. Unsloth örneği ↔ bu defter — neden farklı

Defter Unsloth örneğinin yapısını izliyor ama **tarif ön kayıttan** geliyor. Örnekteki değerleri kullanmak `v010u` ↔ `v011u` kıyasını
kayıtlı `e3` tarifinden koparır.

| | Unsloth örneği | bu defter | neden |
|---|---|---|---|
| yükleme | `load_in_4bit = True` | **bf16**, 4-bit yok | `e3` bf16 eğitildi |
| LoRA hedefi | bütün katmanlar, dikkat + MLP | **üstten 8 dil katmanı, yalnız `q_proj`/`o_proj`**, tam adla | `e3` tarifi (K174/K175: güvenlik 12 katmana kadar duruyor) |
| `r` / `lora_alpha` | 8 / 8 | 8 / **160** | MLX `scale` 20 × r 8 (PEFT ölçeği alpha/r) |
| öğrenme oranı | 2e-4, doğrusal, ısınma 5 | **1e-5 sabit**, ısınma yok | `e3` tarifi |
| optimizer | `adamw_8bit`, wd 0.001 | **`adamw_torch`**, wd 0.01, gradyan kırpma yok | `e3` tarifi · ⚠️ MLX'te `bias_correction=False`, torch'ta hep açık — iki kolda aynı sapma |
| adım | 60 | **2538** (846 × 3 tur) | `e3` tarifi |
| şablon | `get_chat_template("gemma-4")` | **`configs/chat_template_train.jinja`** (K44) | kayıtlı koşular bu şablonla; Unsloth'un kendi uyarısı: eğitim ve çıkarım şablonu aynı olmalı |
| maske | `train_on_responses_only` — **bütün** asistan turları | **yalnız son** asistan turu | MLX `mask_prompt` böyle; 405 çok turlu kayıtta fark eder |
| üretim | `temperature 1.0 · top_p 0.95 · top_k 64` | **açgözlü**, `thinking` kapalı, 1024 jeton | ölçüm tekrarlanabilir olmalı; kayıtlı koşularla aynı ayar |
| kayıt | `save_pretrained("gemma_4_lora")` | Drive'a adapter + kontrol noktaları | oturum kopmasına dayanıklı |

**Gemma 4'e özgü, belgelerden:**

- ⛔ **`use_cache=False` E2B/E4B'de çöp üretir** (KV paylaşan katmanlar; transformers #45242). Unsloth bunu düzeltmiş. Bu yüzden defter
  yalnız Unsloth yolunu kullanır — eski defterdeki `"peft"` yedeği (düz HF + PEFT) bu hataya açık olabilirdi.
- ✅ **Çok turda geçmişe düşünme konmaz, yalnız görünen cevap.** Veride erken turlarda düşünme yok (1058 kaydın 0'ı; düşünme yalnız son
  turda), çok turlu üretim de geçmişe yalnız `cevap`'ı koyuyor.
- ✅ Düşünme, sistem isteminin başındaki `<|think|>` ile açılır — veride `has_thinking` kayıtlarda böyle (`src/train.py`).

---

## 4. Durursa

| mesaj | ne yapılır |
|---|---|
| `GPU … yetmez` | A100/L4 seçin. 4-bit'e geçmek tarifi değiştirir |
| `⛔ bos_token …` · `⛔ şablon çıktısı referansla uyuşmuyor` | **durun, bildirin** — tokenizer eğitim şablonunu farklı kodluyor (K44 sınıfı kusur); `MODEL_ID` yanlış olabilir |
| `N jeton > 2048` | **durun, bildirin** — veri tarafının işi |
| `önek hizası bozuk` | **durun, bildirin** — maske hedefin içine kayıyor |
| `LoRA yanlış yerde` | **durun, bildirin** — LoRA görü/ses kulesine ya da fazla modüle kondu |
| `⛔ ortam referanstan farklı … {alan: (eski, yeni)}` | çoğunlukla `pip install unsloth` yeni sürüm kurdu. **Durun** — iki kol aynı ortamda olmalı; sürümü sabitlemek EK-3 ister |
| CUDA *out of memory* | çalışma zamanını yeniden başlatıp *Tümünü çalıştır* |

---

## 5. Veri makinesine dönüş

1. Drive'dan `birag-v011/v011-colab-ciktilari.zip`'i indirin, açın:

   ```bash
   unzip ~/Downloads/v011-colab-ciktilari.zip -d /tmp/v011-colab
   ```

   ```bash
   cp -R /tmp/v011-colab/eksen-kosu /tmp/v011-colab/cok-turlu-kosu reports/analiz/
   ```

2. Puanlama (model koşmaz):

   ```bash
   uv run python scripts/analiz/2026-09-29-v011-colab-puanla.py
   ```

3. Hüküm:

   ```bash
   uv run python scripts/analiz/2026-09-29-v011-onkayit-ek2-cozumleme.py
   ```

   → `reports/analiz/2026-09-29-v011-onkayit-ek2-sonuc.md`. Çözümleme tamlık (2 kol × 8 tohum × 7 hücre) ve 16 koşunun
   `ortam.json`'larının aynılığı geçmeden puan okumaz.

✅ Defterin çıktı biçimi veri makinesinde sınandı: sahte üretimle yazılan bir eksen dizini `src/eksen_eval.py --yeniden` ile puanlandı
(2026-09-30). ⛔ Model yolu (yükleme, LoRA, eğitim, üretim) burada koşulamaz — ilk kez Colab'da görülecek.

---

## 6. Yapılmayacaklar

| ⛔ | neden |
|---|---|
| 2. hücredeki tarifi (`R`, `LORA_ALPHA`, `LR`, `ADIM` …) değiştirmek | ön kayıtlı `e3` tarifi |
| 16 koşu ortasında `MODEL_ID` değiştirmek, Drive'daki `ortam-referans.json`'ı silmek | iki kolun aynı ortamda olduğunun kanıtı |
| yalnız bir kolu koşup ötekini başka bir zaman/ortamda | kıyasın dayanağı aynı ortam |
| Colab'da puanlamak, sonuca bakıp yeniden eğitmek | puanlama ve hüküm veri makinesinde |
