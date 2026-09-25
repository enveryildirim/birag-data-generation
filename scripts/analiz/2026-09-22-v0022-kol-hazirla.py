#!/usr/bin/env python3
"""`v0.0.22` ince ayar kolunun 8 yapılandırmasını kurar — ÖN KAYITLA.

⛔⛔ **Ön kayıt koşudan ÖNCE mühürlenir (K31).** Ölçüt, karıştırıcılar ve
**bulaşma** bu dosyalara yazılır; koştuktan sonra hangi sayının
«asıl sonuç» olduğuna karar vermek ön kaydı geçersiz kılar.

⛔⛔⛔ **BULAŞMA ÖLÇÜLDÜ VE HÜKÜM ÖNCEDEN VERİLDİ.**
`2026-09-22-celiskili-eval-bulasma.md`: `context_fidelity`'nin 5
`celiskili` ögesinin **5'inde de** eğitim bankasıyla konu ortaklığı var
ve **4 değer birebir çakışıyor** (`randevusuz`, `randevu gerekir`,
`ücretsiz`, `belge gerekmez`). ⇒ **`celiskili` alt puanı temiz bir
sınama DEĞİLDİR ve baş sonuç olarak raporlanmayacaktır.**

⭐ **Değişen tek şey veri.** Kapsam `d1-veri2x-k8qo-v018` ile birebir:
8 katman, q+o, rank 8, scale 20, LR 1e-5, mask_prompt, batch 1,
max_seq 2048, 3 epoch. Tohumlar da **aynı sekizli** (7/13/23/31/37/41/
43/47) ⇒ iki kol yan yana konabilir.

⛔⛔ **KARIŞTIRICI, KOŞUDAN ÖNCE YAZILI.** Epoch sabit (3) ⇒ adım
2478 → 2538. Adımı sabit tutmak epoch'u karıştırırdı; ikisi birden
sabitlenemez. ⇒ Bu kol *«+25 kayıt, üç epoch»*u ölçer.

Çıktı: configs/training/e3-celiskili-k8qo-v022-t*.yaml
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from kunye import betik_tarihi  # noqa: E402

TOHUMLAR = [7, 13, 23, 31, 37, 41, 43, 47]      # d1 kolunun sekizlisi
SURUM = "v0.0.22"
ONCEKI_KOL = "d1-veri2x-k8qo-v018"
DIZIN = KOK / "configs/training"

BASLIK = """# Faz 6 · §7a″ `celiskili` KOTASI TUTTURULDU — ÖN KAYIT (K31 deseni)
#
# ⭐ **NEDEN.** `celiskili` sınıfı `context_fidelity` eksenine karşı
# tasarlandı (T262) ve `v0.0.21`'de payı yalnız %5,1'di — etkisi
# okunamazdı. `v0.0.22`'de pay **%10,1** (25/247), yani §7a″ kotası ilk
# kez tutturuldu (T272). Bu kol o kotanın ölçülebilir bir şey yapıp
# yapmadığını sınar.
#
# ⭐⭐ **DEĞİŞEN TEK ŞEY VERİ.** Kapsam `{onceki}` ile birebir; tohumlar da
# aynı sekizli ⇒ iki kol yan yana konabilir.
#
# ⛔⛔⛔ **BULAŞMA — KOŞUDAN ÖNCE ÖLÇÜLDÜ VE HÜKÜM ÖNCEDEN VERİLDİ.**
# `reports/analiz/2026-09-22-celiskili-eval-bulasma.md`:
# `context_fidelity`'nin 5 `celiskili` ögesinin **5'inde de** eğitim
# bankasıyla konu ortaklığı var; **4 değer birebir çakışıyor**
# («randevusuz», «randevu gerekir», «ücretsiz», «belge gerekmez»).
# ⇒ **`celiskili` alt puanı EZBERDEN AYIRT EDİLEMEZ** ve **baş sonuç
#   olarak raporlanmayacaktır.** Koştuktan sonra bu hükmü gevşetmek ön
#   kaydı geçersiz kılar.
#
# ⛔⛔ **KOŞUDAN ÖNCE İLAN EDİLEN ÖLÇÜT.** Karşılaştırma kolu `{onceki}`
# (aynı 8 tohum). Baş sonuç **temiz ölçülerden** okunur:
#
#   1. **BAŞ ÖLÇÜ — `context_fidelity`'nin bulaşmamış 15 ögesi**
#      (`yeterli`+`distractor`+`yetersiz`). Fark 2·SE'yi aşarsa okunabilir.
#      · anlamlı **artış** ⇒ sınıf, kendi kategorisinin dışına da taşan
#        bir bağlam sadakati kazandırdı — güçlü bulgu
#      · anlamlı **düşüş**  ⇒ kota öteki kategorileri seyreltti
#      · okunamaz ⇒ **bu da bir sonuçtur**: %10 kota tek başına yetmiyor
#   2. **İKİNCİ ÖLÇÜ — `context_fidelity.real` (15 gerçek öge).** `d1`
#      kolunda tabana göre **+1,33** ile okunabilir tek kazançtı; düşerse
#      kota o kazancı bozmuş demektir.
#   3. ⛔⛔ **SERT KAPI — `safety_crisis` (Kural 3).** `d1` kolu tabana
#      göre zaten **−2,25** gerilemişti. Bu kol `d1`'in **altına** inerse
#      sürüm **eğitime uygun sayılmaz**; kota geri alınır. Güvenlikte
#      gerileme «kabul edilebilir» değildir.
#   4. **İZLENEN — `forgetting_smoke`** (`d1`'de −1,25) ve `sycophancy`.
#   5. **RAPORLANIR AMA BAŞ SONUÇ DEĞİL — `celiskili` alt puanı (5 öge).**
#      Bulaşmalı; yükselirse bile *öğrenme* diye okunamaz.
#
# ⛔ Eşik keyfi değil: her eksende 8 tohumun **2·SE**'si kullanılır ve
#   `d1` kolunun kendi SE'siyle karşılaştırılır (K213: tek koşu bir
#   çekiliştir).
#
# ⛔⛔ **KARIŞTIRICI, KOŞUDAN ÖNCE YAZILI.** Epoch sabit (3) ⇒ adım
# 2478 → 2538. Adımı sabit tutmak epoch'u karıştırırdı; ikisi birden
# sabitlenemez. Bu kol *«+25 kayıt, üç epoch»*u ölçer.
#
# ⚠️ `v0.0.22`, `v0.0.18`'in üst kümesidir: eklenen 25 kaydın dışında
#   hiçbir kayıt düşmedi (T272) ⇒ fark **yalnız** eklenen sınıftır.
#   Bu, `d1`↔`z-h9` karşılaştırmasında olmayan bir temizlik.
"""


def main() -> int:
    n = sum(1 for _ in open(KOK / f"datasets/{SURUM}/train.jsonl"))
    n_valid = max(1, round(n * 0.2))
    n_train = n - n_valid
    iters = n_train * 3
    print(f"{SURUM}: {n} kayıt → train {n_train} · valid {n_valid} · "
          f"iters {iters}")

    yazilan = []
    for t in TOHUMLAR:
        ad = f"e3-celiskili-k8qo-{SURUM.replace('.', '').replace('v00', 'v0')}-t{t}"
        ad = f"e3-celiskili-k8qo-v022-t{t}"
        p = DIZIN / f"{ad}.yaml"
        if p.exists():
            raise SystemExit(f"⛔ {p.name} zaten var — üzerine yazılmaz")
        govde = BASLIK.format(onceki=ONCEKI_KOL) + f"""ad: {ad}
model: mlx-community/gemma-4-E4B-it-bf16     # bf16 — K7
dataset: datasets/{SURUM}/train.jsonl

veri:
  valid_orani: 0.2
  seed: 7                    # bölme tohumu SABİT — kollar aynı bölmeyi görsün
  chat_template: configs/chat_template_train.jinja   # K44

mlx:
  fine_tune_type: lora
  optimizer: adamw
  mask_prompt: true          # §9 madde 5
  num_layers: 8              # d1 ile AYNI
  batch_size: 1
  iters: {iters}                # {n_train} eğitim × 3 epoch
  learning_rate: 1.0e-5      # d1 ile AYNI
  steps_per_report: 50
  steps_per_eval: {iters // 6}        # her ~0.5 epoch
  val_batches: -1
  max_seq_length: 2048
  save_every: {n_train}          # epoch başına bir kontrol noktası
  seed: {t}
  lora_parameters:
    rank: 8
    scale: 20.0
    dropout: 0.0
    keys: ["self_attn.q_proj", "self_attn.o_proj"]
"""
        p.write_text(govde, encoding="utf-8")
        assert p.exists()
        yazilan.append(p.name)

    # ⭐ Ön kaydın mühürlenmesi: dosya listesi + tarih + bulaşma raporu
    muhur = {
        "tarih": betik_tarihi(__file__),
        "kol": "e3-celiskili-k8qo-v022",
        "karsilastirma": ONCEKI_KOL,
        "tohumlar": TOHUMLAR,
        "surum": SURUM, "kayit": n, "train": n_train, "iters": iters,
        "bas_olcu": "context_fidelity — bulaşmamış 15 öge",
        "ikinci_olcu": "context_fidelity.real (15 öge)",
        "sert_kapi": "safety_crisis — d1'in altına inerse sürüm reddedilir",
        "bulasmali_olcu": "context_fidelity celiskili alt puanı (5 öge)",
        "bulasma_raporu": "reports/analiz/2026-09-22-celiskili-eval-bulasma.md",
        "yapilandirmalar": yazilan,
    }
    mp = KOK / "configs/deney/2026-09-22-v0022-celiskili-on-kayit.json"
    mp.parent.mkdir(parents=True, exist_ok=True)
    if mp.exists():
        raise SystemExit(f"⛔ ön kayıt zaten mühürlü: {mp.name}")
    mp.write_text(json.dumps(muhur, ensure_ascii=False, indent=1),
                  encoding="utf-8")
    print(f"⭐ {len(yazilan)} yapılandırma · ön kayıt mühürlendi")
    print(f"→ {mp.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
