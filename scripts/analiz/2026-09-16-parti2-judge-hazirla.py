#!/usr/bin/env python3
"""v4-parti2'nin 60 kaydı için judge işlerini kurar — rubrik **v9**.

⛔ **Körlük (K97):** iş dosyasında yalnızca rubrik + konuşma var; kaydın hangi
parti/dilim olduğu, neyle karşılaştırılacağı YAZMAZ. Eşleme yalnızca
`kimlikler.json`'da ve birleştirme betiğinde.

⭐ **Kuyruk KOPYALANMIYOR, İMPORT EDİLİYOR** (K103): `2026-09-15-korpus-v9-is-hazirla.py`
içindeki `kuyruk()` çağrılır. Ayrıca `filter.judge_record`'un kurduğu istem ile
**baytı baytına** karşılaştırılır — iki yol ayrışırsa betik durur.

⚠️ **Neden v9 ve v7 değil.** parti1 ve `v0.0.5` **v7** ile puanlandı; doğrudan
karşılaştırma bu yüzden geçerli DEĞİL (K137: rubrik sürümü sıralamayı çeviriyor).
Yine de v9 seçildi, üç gerekçe:
  1. v9 geçerli rubrik (`filter.JUDGE_PROMPT_VERSION` varsayılanı) ve korpusta
     bir kez koştu (K120 → `reports/analiz/2026-09-15-korpus-v9-kosusu.md`).
  2. `build.py`nin judge KAPISI tek alan: `klinik_guvenlik_ihlali`. Öteki puanlar
     rapor, kapı değil ⇒ rubrik karışımı **dahil/hariç** kararını yalnızca bu
     bayrak üzerinden etkiler.
  3. v9'un asimetrisi bu bayrağı **ihlali arttırma** yönünde oynatıyor (K120):
     doğrulanamayan muafiyet düşer. Kural 3 açısından güvenli yön.
⛔ Buna rağmen `datasets/v0.0.6` **rubrik KARIŞIK** olacak (155 kayıt v7 + 60
kayıt v9) ve bu veri kartına yazılmalı; tekdüzelik istenirse 155 kayıt v9 ile
YENİDEN puanlanmalı — ayrı ve büyük bir karar.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402

# `kuyruk()` buradan gelir — tek türetme.
_sp = _iu.spec_from_file_location("v9ih", KOK / "scripts/analiz/2026-09-15-korpus-v9-is-hazirla.py")
V9IH = _iu.module_from_spec(_sp)
_sp.loader.exec_module(V9IH)

# ⚠️ Varsayılanlar DEĞİŞMEDİ; ortam değişkeni yalnızca revizyon dalgası için
# (düzeltilen kayıtların yeniden puanlanması) ek bir giriş açıyor.
KORPUS = KOK / os.environ.get("BIRAG_JUDGE_KORPUS", "data/candidates/v4-parti2.jsonl")
RUBRIK_YOL = KOK / "prompts/judge-eksen1.v9.md"
ETIKET = os.environ.get("BIRAG_JUDGE_ETIKET", "parti2-v9")
# Yalnız belirli `parti_sira` değerleri için iş kur (virgüllü liste); boşsa hepsi.
SADECE = {int(x) for x in os.environ.get("BIRAG_JUDGE_SADECE", "").split(",") if x.strip()}
# ⚠️ Toplayıcı (`2026-09-15-judge-sonuclari-topla.py`) bu yolu SABİT tutuyor;
# betiği değiştirmemek için işler oraya yazılıyor (Kural 7).
ISLER = V9IH.ISLER
PARCA = 10  # bir alt-ajanın alacağı iş sayısı


def _metin_sha(r: dict) -> str:
    """Puanlanan metnin parmak izi: kullanıcı turları + asistan cevapları.

    ⚠️ `thinking` DIŞARIDA — judge onu puanlamaz (T120) ve arındırma onu
    değiştirir; içeri alınırsa meşru devralmalar haksız yere reddedilirdi.
    """
    par = []
    for m in r["messages"]:
        if m["role"] == "user":
            par.append("U:" + m["content"])
        elif m["role"] == "assistant":
            par.append("A:" + (m.get("content") or ""))
    return hashlib.sha256("\n".join(par).encode("utf-8")).hexdigest()[:16]


def main() -> int:
    kayitlar = [json.loads(s) for s in KORPUS.read_text(encoding="utf-8").splitlines() if s.strip()]
    if SADECE:
        kayitlar = [r for r in kayitlar if r["gen_meta"]["parti_sira"] in SADECE]
    rub = RUBRIK_YOL.read_text(encoding="utf-8")

    d = ISLER / ETIKET
    if d.exists():
        # ⛔⛔ BU SATIR TAMAMLANMIŞ YARGILARI SİLİYOR ve sessizce siliyordu.
        # v5-parti4'ün işleri düzeltilmiş korpusla YENİDEN kurulduğunda, o sırada
        # bitmiş 30 yargı (`sonuc/`) yok oldu; yalnız 1 iş dosyası değişmişti.
        # ➡️ *Yeniden hazırlamak, yeniden yargılamak demek değildir; ikisini
        #    birbirine bağlayan bir `rmtree` pahalı işi sessizce çöpe atar.*
        # ⇒ `sonuc/` doluysa betik DURUR; silmek isteyen açıkça söyler.
        _sonuc = d / "sonuc"
        if _sonuc.exists() and any(_sonuc.iterdir()) and not os.environ.get("BIRAG_JUDGE_SONUC_SIL"):
            raise SystemExit(
                f"⛔ {_sonuc} içinde {len(list(_sonuc.iterdir()))} tamamlanmış yargı var.\n"
                f"   Yeniden hazırlamak onları SİLER. Bilerek yapıyorsan:\n"
                f"   BIRAG_JUDGE_SONUC_SIL=1 ile yeniden koş.")
        shutil.rmtree(d)
    (d / "istek").mkdir(parents=True)
    (d / "sonuc").mkdir()

    kimlikler, sapan = [], []
    for i, r in enumerate(kayitlar, 1):
        no = f"{i:03d}"
        istem = rub + V9IH.kuyruk(r)

        # ⭐ `filter.judge_record`ün kurduğu istemle BAYTI BAYTINA aynı mı?
        asst = f._last_assistant(r)
        beklenen = (f"{rub}\n\n---\n\n## Değerlendirilecek konuşma\n\n"
                    f"{f._render_conversation(r)}\n\n"
                    f"(iç muhakeme — değerlendirme dışı, yalnızca bağlam için: "
                    f"{(asst.get('thinking') or '')[:500]})")
        if istem != beklenen:
            sapan.append(no)

        (d / "istek" / f"{no}.txt").write_text(istem, encoding="utf-8")
        # ⭐⭐ PUANLANAN METNİN PARMAK İZİ. Bir yargı, kuyruğa girdiği andaki
        # metni tarif eder; korpus sonradan değişirse o puan artık BAŞKA bir
        # metne aittir ve bunu kaynaştırıcı kendi başına göremez.
        # ➡️ *Bir ölçümü taşınabilir kılan şey sayının kendisi değil, neyin
        #    ölçüldüğünün kayıtlı olmasıdır.*
        kimlikler.append({"no": no, "id": r["id"], "metin_sha": _metin_sha(r)})

    if sapan:
        print(f"⛔ {len(sapan)} işte kuyruk filter.judge_record'dan SAPIYOR: {sapan[:5]}")
        return 1

    (d / "kimlikler.json").write_text(json.dumps(kimlikler, ensure_ascii=False, indent=1),
                                      encoding="utf-8")

    # ⛔ Körlük denetimi: istek dosyalarında parti/kimlik izi olmamalı.
    sizinti = []
    for p in sorted((d / "istek").glob("*.txt")):
        m = p.read_text(encoding="utf-8")
        # ⚠️ Parti adı SABİT yazılmıştı ("v4-parti2") ve başka bir partide
        # sızıntı denetimi sessizce zayıflardı. Ad artık kayıtlardan okunuyor.
        partiler = {r["gen_meta"].get("parti") for r in kayitlar if r.get("gen_meta")}
        for iz in tuple(partiler) + ("parti_sira", "gen_meta", "seed_id"):
            if iz in m:
                sizinti.append((p.name, iz))
    if sizinti:
        print(f"⛔ körlük sızıntısı: {sizinti[:5]}")
        return 1

    partiler = [(k, min(k + PARCA - 1, len(kimlikler))) for k in range(1, len(kimlikler) + 1, PARCA)]
    print(f"✅ {len(kimlikler)} iş → {d}")
    print(f"   rubrik SHA256 {hashlib.sha256(RUBRIK_YOL.read_bytes()).hexdigest()[:16]}")
    print(f"   korpus SHA256 {hashlib.sha256(KORPUS.read_bytes()).hexdigest()[:16]}")
    print(f"   kuyruk filter.judge_record ile birebir · körlük temiz")
    print(f"   {len(partiler)} parça × {PARCA}: " +
          ", ".join(f"{a:03d}-{b:03d}" for a, b in partiler))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
