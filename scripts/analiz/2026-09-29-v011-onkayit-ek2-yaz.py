#!/usr/bin/env python3
"""`v0.1.1` ön kaydına EK-2 — eğitim ve üretim Colab + Unsloth'ta (👤 kullanıcı kararı, 2026-09-29).

Yazar: `configs/deney/2026-09-29-v011-on-kayit-ek2.json` + `reports/analiz/2026-09-29-v011-onkayit-ek2.md`.
⛔ Ana ön kayıt ve EK-1 DEĞİŞTİRİLMEZ; çelişen yerde EK-2 geçerlidir. ⛔ Herhangi bir kolun model
çıktısı bu depoda varsa DURUR. ⛔ Mühür varsa DURUR.
"""
from __future__ import annotations

import glob
import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from kunye import betik_tarihi  # noqa: E402

ANA = KOK / "configs/deney/2026-09-29-v011-on-kayit.json"
EK1 = KOK / "configs/deney/2026-09-29-v011-on-kayit-ek1.json"
MUHUR = KOK / "configs/deney/2026-09-29-v011-on-kayit-ek2.json"
RAPOR = KOK / "reports/analiz/2026-09-29-v011-onkayit-ek2.md"
DOSYALAR = [
    "notebooks/v011-unsloth-egitim.ipynb", "src/colab_egitim.py", "src/train.py",
    "configs/colab/sablon-referansi.json", "scripts/analiz/2026-09-29-colab-sablon-referansi.py",
    "scripts/analiz/2026-09-29-v011-colab-puanla.py", "scripts/analiz/2026-09-29-v011-onkayit-ek2-cozumleme.py",
    "datasets/v0.1.1/train.jsonl", "datasets/v0.1.1/manifest.json",
]


def _sha16(y: Path) -> str:
    return hashlib.sha256(y.read_bytes()).hexdigest()[:16]


def main() -> int:
    if MUHUR.exists():
        raise SystemExit(f"⛔ {MUHUR.name} zaten mühürlü")
    cikti = [p for on in ("v010u", "v011u", "v011") for k in ("eksen-kosu", "cok-turlu-kosu")
             for p in glob.glob(str(KOK / f"reports/analiz/{k}/*-{on}-t*"))]
    if cikti:
        raise SystemExit(f"⛔ model çıktısı VAR — ek sonuçtan önce yazılmalıydı: {cikti[:3]}")
    assert _sha16(KOK / "datasets/v0.1.1/train.jsonl") == json.loads(ANA.read_text())["kollar"]["v011"]["hazirlik_sha256_16"]

    m = {
        "tarih": "2026-09-29", "ek_no": 2,
        "ana_on_kayit": str(ANA.relative_to(KOK)), "ana_on_kayit_sha256_16": _sha16(ANA), "ana_on_kayit_commit": "13edc2e",
        "ek1": str(EK1.relative_to(KOK)), "ek1_sha256_16": _sha16(EK1), "ek1_commit": "9eae795",
        "karar": "kullanıcı — «bu makinede model çalıştıramayız; veri seti burada üretilir, Colab'da çalıştırılır» + «EK-2 yaz, Colab'da unsloth ile» (2026-09-29)",
        "neden": [
            "Ana ön kayıt MLX varsayıyordu (Apple Silicon); Colab NVIDIA GPU, MLX çalışmaz.",
            "Kıyas kolu olarak kayıtlı 48 MLX e3 koşusu, Colab'da eğitilmiş bir v011 koluyla kıyaslanırsa fark verinin değil ÇERÇEVENİN farkı olabilir ⇒ «değişen tek şey veri» ilkesi çöker.",
            "Birebir aktarım da mümkün değil: MLX AdamW bias_correction=False, torch AdamW'da hep açık.",
        ],
        "degisen_maddeler": {
            "kollar": {"eski": "e3 (kayıtlı 48 MLX koşusu) ↔ v011 (MLX)",
                       "yeni": {"v010u": "datasets/v0.1.0 (= v0.0.22, 6fcb6b1e16290575), Colab + Unsloth, tarif configs/training/e3-celiskili-k8qo-v022-t{t}.yaml",
                                "v011u": "datasets/v0.1.1 (f8fcaa1e96603cb2), Colab + Unsloth, tarif configs/training/v011-k8qo-t{t}.yaml"},
                       "kayitli_mlx_e3": "hükme GİRMEZ; yalnız başvuru"},
            "ortam": {"kural": "16 koşunun hepsinde colab_egitim.SABIT_ALANLAR aynı: model_id · model_revizyon · lora_yolu · şablon SHA · kütüphane sürümleri · üretim ayarı. Farklıysa çözümleme DURUR.",
                      "gpu": "hücre başına kaydedilir, zorunlu değil; bir tohumun iki kolu farklı GPU'daysa raporda işaretlenir",
                      "hassasiyet": "bf16, 4-bit YOK (K7 · e3 bf16). GPU ≥ 22 GB. 4-bit gerekirse ilk çıktıdan önce EK-3."},
            "tarif_esleme": {
                "LoRA ölçeği": "MLX y + scale·(xA)B, scale 20, r 8 ⇒ PEFT lora_alpha 160 (ölçek alpha/r)",
                "LoRA başlangıcı": "MLX A ~ U(±1/√in), B = 0 ⇒ PEFT kaiming_uniform(√5) aynı dağılım, B = 0",
                "hedef": "dil modelinin ÜST 8 katmanı, self_attn.q_proj + o_proj (MLX num_layers üstten N) — tam modül adlarıyla; görü/ses kuleleri hariç; kurulumda ve her eğitimde denetlenir",
                "optimizer": "AdamW β(0,9, 0,999) ε 1e-8 wd 0,01 · ⚠️ MLX bias_correction=False, torch'ta açık (iki kolda aynı sapma)",
                "LR": "1e-5 sabit, ısınma yok · gradyan kırpma yok (max_grad_norm 0)",
                "adım": "2538 = 846 eğitim × 3 · batch 1 · doğrulama her 423 adım · kontrol noktası her 846 adım",
                "kayıp": "yalnız son asistan turu: labels[:offset] = -100, offset = len(şablon(messages[:-1], add_generation_prompt=True)) — mlx_lm ChatDataset",
                "veri biçimi ve bölme": "src/train.py to_mlx_messages + prepare_data (random.Random(7), %20 doğrulama) ÇAĞRILIR — iki kol aynı kayıtları aynı bölmede görür",
                "şablon": "configs/chat_template_train.jinja (K44); gerçek tokenizer'ın çıktısı 35 referans dizgeyle birebir olmak zorunda (her eğitim ve üretim yüklemesinde)",
            },
            "uretim": {"ayar": "thinking kapalı · 1024 jeton · açgözlü — e3'ün 48 koşusuyla aynı",
                       "yol": "HF generate; istem golden_eval.prompt_kur, ayrıştırma golden_eval.cikti_ayir, çok turlu cok_turlu_eval.konus — ÇAĞRILIR",
                       "puanlama": "Colab puanlamaz; mühürlü src/eksen_eval.py --yeniden bu makinede puanlar (scripts/analiz/2026-09-29-v011-colab-puanla.py)"},
            "on_kayit_adim_2": {"eski": "bu makinede gerçek tokenizer ile ≤ 2048 jeton", "yeni": "Colab'da kurulum sınamasında ve her eğitimde (kodla DURUR)"},
            "cozumleme": {"yeni": "scripts/analiz/2026-09-29-v011-onkayit-ek2-cozumleme.py — EK-1 çözümlemesini (o da ana çözümlemeyi) içe aktarır; değişenler: kol önekleri, ortam kilidi, iki raporlanır ölçünün onarımı"},
            "onarim": {"kusur": "Ana çözümlemenin iki RAPORLANIR ölçüsü, puanlanmış sonuclar.jsonl'de BULUNMAYAN alanları okuyordu: R_uretim_token_ortanca `uretim_token` okur → her zaman 0 (gecikme vekili hiçbir şey ölçmüyordu); R_dejenere_payi `thinking_kapandi` okur → yok ⇒ bütçe tükenmesi bayrağı hiç yanmaz. Kayıtlı e3 koşularında da bu alanlar yok. Mühür sırasında fark edilmedi; EK-2 yazılırken bulundu.",
                       "duzeltme": "Colab'ın dokunulmamış ham.jsonl'ünden yeniden hesaplanır. İkisi de hükme girmez."},
            "sira": "tohum içinde dönüşümlü (v010u-t7, v011u-t7, …) — oturum/GPU değişimi iki kolu birlikte etkilesin",
        },
        "degismeyen": "ölçülerin tanımı · baş/ikinci ölçüler · bekçiler ve eşikleri · EK-1 kazanç şartı · tohumlar · çok turlu set · okuma tablosu",
        "maliyet": "16 eğitim (her biri 2538 adım) + 16 × (6 eksen + 40 çok turlu tur). Colab'da süre ölçülmedi; defter ilk koşudan sonra süreyi yazar.",
        "muhurlu_dosyalar": {d: _sha16(KOK / d) for d in DOSYALAR},
        "sinamalar_bu_makinede": [
            "tarif: 16 yapılandırma okundu, lora_alpha 160, 2538 adım, üst 8 katman q/o",
            "bölme: 846/212, iki kol aynı kayıtları aynı bölmede görüyor",
            "maske: iki veri setinin 2116 kaydının hepsinde hedef yalnız son asistan turu, önek hizası sağlam; uzunluk kapısı duruyor",
            "LoRA: Gemma benzeri sahte ağaçta 16 modül, katman 34-41, görü kulesi hariç; yalnız son ekle hedefleme (bütün katmanlar + görü) YAKALANIYOR",
            "üretim: eos sökülüyor, düşünme/cevap ayrışıyor, bütçe tükenince kesildi=True",
            "şablon referansı: 35 dizge; yanlış bos ve düşünmeyi silen şablon (K44 kusuru) YAKALANIYOR",
            "eğitim: küçük Gemma3 ile CPU'da 4 adım, doğrulama + kontrol noktası + adapter; biten atlanıyor; yarıda kalan kontrol noktasından SÜRÜYOR",
            "Colab çıktısı → bu makinede --yeniden puanlama: alan kümesi kayıtlı e3 koşularıyla aynı, ham.jsonl dokunulmuyor",
            "EK-2 çözümlemesi uçtan uca (v010u = v011u): 112 hücre, her Δ = 0, hüküm «kazanç şartı SAĞLANMADI»; ortam farkı DURDURUYOR",
        ],
        "tam_beyan": [
            "⛔ Unsloth ve Gemma 4 bu makinede koşulamadı: FastModel.from_pretrained(revision=…) ve get_peft_model(target_modules=<tam adlar>) davranışı SINANMADI. Bu yüzden LoRA hedefleri kurulumda ve her eğitimde denetlenir; Unsloth hedefleri yanlış uygularsa LORA_YOLU='peft' (ilk eğitimden önce).",
            "⚠️ MODEL_ID varsayılanı (unsloth/gemma-4-E4B-it) doğrulanmadı; kullanıcı doğrulamalı. Revizyon ilk oturumda çözülüp sabitlenir.",
            "Eşleme seçimleri BENİM: lora_alpha 160 · wd 0,01 · kırpma yok · sabit LR · bias_correction sapması kabul · adapter yüklemesi PeftModel ile · üretim HF generate (Unsloth hızlı çıkarımı KULLANILMIYOR — iki kolda aynı).",
            "Ana çözümlemedeki iki raporlanır ölçü kusuru BENİM hatam (mühürden önce sınanmadı).",
            "e3'ün kayıtlı değerleri ana ön kayıtta beyan edilmişti; bu ek onları kullanmıyor.",
        ],
        "bunun_soylemedikleri": [
            "⚠️ Colab sonuçları MLX sonuçlarıyla (T277 vd.) doğrudan karşılaştırılamaz — çerçeve farklı.",
            "⚠️ v010u'nun v0.1.0'ı MLX'teki e3 kadar iyi öğrendiği gösterilmedi; hüküm yalnız iki Colab kolu arasındadır.",
        ],
    }
    MUHUR.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    ms = _sha16(MUHUR)
    D = m["degisen_maddeler"]
    s = ["# `v0.1.1` ön kaydına EK-2 — Colab + Unsloth", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {betik_tarihi(__file__)}  ",
         f"**Mühür:** `{MUHUR.relative_to(KOK)}` · SHA256-16 **`{ms}`** · {len(DOSYALAR)} dosya  ",
         f"**Ana ön kayıt** `{_sha16(ANA)}` (`13edc2e`) · **EK-1** `{_sha16(EK1)}` (`9eae795`) — **değiştirilmedi**; çelişen yerde EK-2 geçerlidir.  ",
         "⭐ **Kullanıcı kararı:** bu makine yalnız veri üretimi; eğitim ve üretim Colab'da Unsloth ile. ⛔ Ek, hiçbir kolun model çıktısı yokken yazıldı (betik denetledi).", "",
         "## Neden", "", *[f"- {x}" for x in m["neden"]], "",
         "## Kollar", "", "| kol | veri | tarif |", "|---|---|---|",
         "| `v010u` | `datasets/v0.1.0` (= `v0.0.22`) `6fcb6b1e16290575` | `e3-celiskili-k8qo-v022-t{t}.yaml` |",
         "| `v011u` | `datasets/v0.1.1` `f8fcaa1e96603cb2` | `v011-k8qo-t{t}.yaml` |", "",
         "⛔ **Kayıtlı 48 MLX `e3` koşusu hükme girmez**; iki kol da aynı Colab ortamında eğitilip üretilir.", "",
         "## Ortam kuralı", "", f"- {D['ortam']['kural']}", f"- GPU: {D['ortam']['gpu']}", f"- {D['ortam']['hassasiyet']}", f"- Sıra: {D['sira']}", "",
         "## MLX → Unsloth/PEFT eşlemesi (mlx_lm 0.31.3 kaynağından)", "", "| | |", "|---|---|"]
    s += [f"| {k} | {v} |" for k, v in D["tarif_esleme"].items()]
    s += ["", "## Üretim ve puanlama", "", *[f"- **{k}:** {v}" for k, v in D["uretim"].items()], "",
          f"⭐ Ön kaydın adım 2'si (≤ 2048 jeton) artık Colab'da: {D['on_kayit_adim_2']['yeni']}.", "",
          "## ⛔ Mühürlü çözümlemede bulunan kusur — onarıldı", "", f"**Kusur.** {D['onarim']['kusur']}", "", f"**Düzeltme.** {D['onarim']['duzeltme']}", "",
          "## Bu makinede yapılan sınamalar", "", *[f"- ✅ {x}" for x in m["sinamalar_bu_makinede"]], "",
          "## Akış", "",
          "1. Colab: `notebooks/v011-unsloth-egitim.ipynb` — kurulum sınaması → 16 eğitim → 16 × (6 eksen + çok turlu) → paket",
          "2. Bu makine: paketi `reports/analiz/` altına aç → `scripts/analiz/2026-09-29-v011-colab-puanla.py`",
          "3. Bu makine: `scripts/analiz/2026-09-29-v011-onkayit-ek2-cozumleme.py` → hüküm", "",
          f"Maliyet: {m['maliyet']}", "",
          "## ⛔ Tam beyan", "", *[f"- {x}" for x in m["tam_beyan"]], "",
          "## ⛔ Bunun söylemedikleri", "", *[f"- {x}" for x in m["bunun_soylemedikleri"]]]
    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    print(f"✅ EK-2 {MUHUR.relative_to(KOK)} · SHA256-16 {ms} · {len(DOSYALAR)} dosya")
    return 0


if __name__ == "__main__":
    sys.exit(main())
