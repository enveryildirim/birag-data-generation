#!/usr/bin/env python3
"""`v0.1.1` ön kaydına EK-3 — koşucu basit defter, kütüphane sürümleri sabit (👤 kullanıcı kararı, 2026-09-30).

Yazar: `configs/deney/2026-09-30-v011-on-kayit-ek3.json` + `reports/analiz/2026-09-30-v011-onkayit-ek3.md`.
⛔ Ana ön kayıt, EK-1 ve EK-2 DEĞİŞTİRİLMEZ; çelişen yerde EK-3 geçerlidir. ⛔ Herhangi bir kolun model
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

EK2 = KOK / "configs/deney/2026-09-29-v011-on-kayit-ek2.json"
MUHUR = KOK / "configs/deney/2026-09-30-v011-on-kayit-ek3.json"
RAPOR = KOK / "reports/analiz/2026-09-30-v011-onkayit-ek3.md"
DOSYALAR = ["notebooks/v011-basit-egitim.ipynb", "scripts/analiz/2026-09-30-v011-onkayit-ek3-cozumleme.py"]


def _sha16(y: Path) -> str:
    return hashlib.sha256(y.read_bytes()).hexdigest()[:16]


def main() -> int:
    if MUHUR.exists():
        raise SystemExit(f"⛔ {MUHUR.name} zaten mühürlü")
    cikti = [p for on in ("v010u", "v011u", "v011") for k in ("eksen-kosu", "cok-turlu-kosu")
             for p in glob.glob(str(KOK / f"reports/analiz/{k}/*-{on}-t*"))]
    if cikti:
        raise SystemExit(f"⛔ model çıktısı VAR — ek sonuçtan önce yazılmalıydı: {cikti[:3]}")
    e2 = json.loads(EK2.read_text(encoding="utf-8"))
    kotu = [y for y, s in e2["muhurlu_dosyalar"].items() if _sha16(KOK / y) != s]
    assert not kotu, f"⛔ EK-2 mührü bozuk: {kotu}"

    m = {
        "tarih": "2026-09-30", "ek_no": 3,
        "ek2": str(EK2.relative_to(KOK)), "ek2_sha256_16": _sha16(EK2), "ek2_commit": "652188c",
        "karar": "kullanıcı — «oluşturduğun notebook çok fazla kod … basit bir notebook oluşturmanı istiyorum» (Unsloth "
                 "Gemma4 (E4B) Text örneği ve iki Unsloth belgesi verildi) + «EK-3'ü yaz ve push et» (2026-09-30)",
        "neden": [
            "EK-2 koşucu olarak notebooks/v011-unsloth-egitim.ipynb + src/colab_egitim.py'yi mühürlemişti; kullanıcı onun yerine "
            "Unsloth örneği tarzında, eğitim kodu görünür bir defter istedi ⇒ koşucu değişiyor.",
            "EK-2'de her oturum `pip install unsloth` ile EN SON sürümü kuruyordu ⇒ 16 koşu birkaç oturuma yayılınca sürüm "
            "değişir, ortam kilidi deneyi yarıda durdururdu. Çıktı yokken sabitlemek sapma değil.",
            "Unsloth belgesine göre Gemma 4 E2B/E4B'de use_cache=False çöp logit üretir (KV paylaşan katmanlar; transformers "
            "#45242) ve Unsloth bunu düzeltmiştir ⇒ EK-2'nin düz PEFT yedeği (LORA_YOLU='peft') bu hataya açık olabilirdi.",
        ],
        "degisen_maddeler": {
            "kosucu": {"eski": "notebooks/v011-unsloth-egitim.ipynb + src/colab_egitim.py (eğitim döngüsü modülde)",
                       "yeni": "notebooks/v011-basit-egitim.ipynb — bir koşu = bir KOL × TOHUM; eğitim, maske, LoRA hedefleri, "
                               "üretim ve çıktı yazımı defterin İÇİNDE",
                       "cagrilan": "src/train.py prepare_data (bölme + düşünme gömme) · golden_eval.prompt_kur / cikti_ayir · "
                                   "colab_egitim: sablon_referansi_denetle, ortam_denetle, EKSEN, COK_TURLU, KUTUPHANE — mühürlü, değişmedi",
                       "eski_defter": "depoda kalır (EK-2 mühürlü dosyası; silinirse EK-2 çözümlemesi durur), KULLANILMAZ"},
            "surum_sabitleme": {"kural": "ilk koşu en son unsloth'u kurar ve sürümleri ortam-referans.json'a yazar; sonraki her koşu "
                                         "o sürümleri (torch hariç, ortam-referans.json → surumler) `pip install p==v` ile kurar",
                                "torch": "Colab'ın kendi sürümü; değişirse ortam kilidi DURUR (EK-2 kuralı, değişmedi)"},
            "lora_yolu": {"eski": "'unsloth' ya da 'peft' (yedek)", "yeni": "yalnız 'unsloth'"},
            "kosucu_damgasi": "her ortam.json'a `kosucu` alanı eklenir (SABIT_ALANLAR'a girmez)",
            "cozumleme": {"yeni": "scripts/analiz/2026-09-30-v011-onkayit-ek3-cozumleme.py — EK-3 mührü + her çıktı dizininin "
                                  "kosucu'su ve git_rev'deki defterin mühürlü defterle aynılığı; sonra EK-2 çözümlemesi DEĞİŞMEDEN",
                          "hukum_raporu": "reports/analiz/2026-09-29-v011-onkayit-ek2-sonuc.md (EK-2 çözümlemesi yazar)"},
            "denetim_farklari": {
                "kurulum_sinamasi": "EK-2 defteri eğitimden önce ayrı bir sınama hücresi koşuyordu; basit defterde aynı denetimler "
                                    "eğitim hücresinin içinde (şablon 35 dizge · ≤ 2048 jeton · önek hizası · LoRA modülleri)",
                "mühür": "EK-2 defteri Colab'da 55 dosyanın mührünü denetliyordu; basit defter denetlemez — yerine EK-3 çözümlemesi "
                         "her çıktının git_rev'indeki defteri denetler, EK-2 çözümlemesi veri ve kod mühürlerini",
                "LoRA": "eğitilebilir parametre sayısı denetimi yerine: LoRA taşıyan modül sayısı = hedef sayısı ve hiçbiri görü/ses "
                        "kulesinde değil + print_trainable_parameters",
                "uzunluk": "EK-2 kolun bütün kayıtlarını ayrı denetliyordu; basit defter eğitim + doğrulama kayıtlarının hepsini "
                           "kodlarken denetler (aynı küme)",
            },
        },
        "degismeyen": "tarif (bf16 · üst 8 dil katmanı q/o · r 8 / lora_alpha 160 · AdamW wd 0,01 · LR 1e-5 sabit · 2538 adım · "
                      "batch 1 · kırpma yok) · veri ve bölme · şablon · yalnız son tur maskesi · üretim ayarı (thinking kapalı, "
                      "1024 jeton, açgözlü) · çıktı biçimi · ortam kilidi (SABIT_ALANLAR) · ölçüler · bekçiler · EK-1 kazanç şartı · "
                      "tohumlar · sıra (tohum içinde v010u → v011u)",
        "muhurlu_dosyalar": {d: _sha16(KOK / d) for d in DOSYALAR},
        "sinamalar_bu_makinede": [
            "defter nbformat şemasına uygun; 10 kod hücresinin hepsi sözdizimsel olarak geçerli",
            "LoRA hedef kalıbı: dil katmanının q_proj'u eşleşiyor, görü kulesininki ikinci denetimle eleniyor, lora_A alt modülü eşleşmiyor",
            "çıktı biçimi: defterin yaz() işleviyle sahte üretimden yazılan eksen dizini mühürlü src/eksen_eval.py --yeniden ile puanlandı",
            "veri: 1058 kaydın hiçbirinde erken turda düşünme yok (Gemma 4 çok tur kuralı); 405 çok turlu kayıt ⇒ "
            "train_on_responses_only KULLANILMADI (bütün asistan turlarını eğitirdi)",
            "EK-3 çözümlemesi: mühür denetimi geçiyor; kosucu denetimi yanlış koşucuyu, olmayan git_rev'i ve farklı defteri DURDURUYOR, "
            "doğru dizini geçiriyor; dizin yoksa DURUYOR",
        ],
        "tam_beyan": [
            "⛔ Model yolu (Unsloth yükleme, get_peft_model(target_modules=<tam adlar>), eğitim, PeftModel ile üretim) bu makinede "
            "koşulamadı; ilk kez Colab'da görülecek. Defterin denetimleri bunun için var.",
            "Basit defteri Claude Code yazdı (kullanıcı isteğiyle); Unsloth örneğinden farkları docs/colab-egitim-rehberi.md §3.",
            "Sürüm sabitleme torch'u kapsamaz; Colab görüntüsü torch'u güncellerse deney ortam kilidinde durur ve yeni bir ek gerekir.",
        ],
        "bunun_soylemedikleri": [
            "⚠️ Sürüm sabitleme ilk koşunun kurduğu sürümlerin DOĞRU çalıştığını göstermez; yalnız 16 koşunun aynı sürümlerle koşmasını sağlar.",
        ],
    }
    MUHUR.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    ms = _sha16(MUHUR)
    D = m["degisen_maddeler"]
    s = ["# `v0.1.1` ön kaydına EK-3 — koşucu basit defter, sürümler sabit", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {betik_tarihi(__file__)}  ",
         f"**Mühür:** `{MUHUR.relative_to(KOK)}` · SHA256-16 **`{ms}`** · {len(DOSYALAR)} dosya  ",
         f"**EK-2** `{_sha16(EK2)}` (`652188c`) — **değiştirilmedi**; ana ön kayıt ve EK-1 de. Çelişen yerde EK-3 geçerlidir.  ",
         "⭐ **Kullanıcı kararı.** ⛔ Ek, hiçbir kolun model çıktısı yokken yazıldı (betik denetledi).", "",
         "## Neden", "", *[f"- {x}" for x in m["neden"]], "",
         "## Değişenler", "", "| | eski | yeni |", "|---|---|---|",
         f"| koşucu | {D['kosucu']['eski']} | {D['kosucu']['yeni']} |",
         f"| sürümler | her oturum en son `unsloth` | {D['surum_sabitleme']['kural']} |",
         f"| LoRA yolu | {D['lora_yolu']['eski']} | {D['lora_yolu']['yeni']} |",
         f"| çözümleme | EK-2 çözümlemesi | {D['cozumleme']['yeni']} |", "",
         f"- Çağrılan mühürlü işlevler: {D['kosucu']['cagrilan']}.",
         f"- Eski defter: {D['kosucu']['eski_defter']}.",
         f"- torch: {D['surum_sabitleme']['torch']}.", f"- Damga: {D['kosucu_damgasi']}.", "",
         "## Denetim farkları (EK-2 defteri ↔ basit defter)", "", "| | |", "|---|---|"]
    s += [f"| {k} | {v} |" for k, v in D["denetim_farklari"].items()]
    s += ["", "## Değişmeyen", "", m["degismeyen"], "",
          "## Bu makinede yapılan sınamalar", "", *[f"- ✅ {x}" for x in m["sinamalar_bu_makinede"]], "",
          "## Akış", "",
          "1. Colab: `notebooks/v011-basit-egitim.ipynb`, 16 kez (her biri bir `KOL` × `TOHUM`) → son koşuda paket",
          "2. Bu makine: paketi `reports/analiz/` altına aç → `scripts/analiz/2026-09-29-v011-colab-puanla.py`",
          "3. Bu makine: `scripts/analiz/2026-09-30-v011-onkayit-ek3-cozumleme.py` → hüküm "
          f"(`{D['cozumleme']['hukum_raporu']}`)", "",
          "## ⛔ Tam beyan", "", *[f"- {x}" for x in m["tam_beyan"]], "",
          "## ⛔ Bunun söylemedikleri", "", *[f"- {x}" for x in m["bunun_soylemedikleri"]]]
    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    print(f"✅ EK-3 {MUHUR.relative_to(KOK)} · SHA256-16 {ms} · {len(DOSYALAR)} dosya")
    return 0


if __name__ == "__main__":
    sys.exit(main())
