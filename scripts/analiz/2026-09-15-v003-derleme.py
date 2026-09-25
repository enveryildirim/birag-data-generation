#!/usr/bin/env python3
"""`datasets/v0.0.3/` girdisini derler — v0.0.2 + `uretim-v4` ilk partisi (K111).

v0.0.2 derlemesinin (`2026-09-15-v002-derleme.py`) aynı deseni: elde duran parçalar
`build.py`'nin beklediği biçimde değil, bu yüzden kapılar burada **yeniden** koşuluyor
(deterministik) ve judge sonucu üzerine bindiriliyor.

Parçalar:
  · data/candidates/v3-kumulatif.jsonl   104 kayıt · judge v7 ayrı dosyada
  · data/judged/v3-kumulatif.v7.jsonl    aynı 104 kaydın v7 judge'ı (K100)
  · data/candidates/replay-v1.jsonl       18 kayıt · judge'a GİRMEZ (K88/K89)
  · data/judged/v4-parti1.v7.jsonl        40 kayıt · judge v7, aynı rubrik

⚠️ v0.0.2 betiği DEĞİŞTİRİLMEDİ — çıktısı `datasets/v0.0.2/`'nin üretim kaydı (Kural 7).

⚠️ REPLAY PAYI DÜŞÜYOR ve bu bilerek kayda geçiyor: v0.0.2'de %15,4 (§9 önlem 1
hedefi %15, K12), v0.0.3'te terapötik kayıt 99 → 139 çıkarken replay 18'de kalıyor,
yani pay **%11,5**. Elimizde başka açık veri replay kaydı yok. Eksen 3 (unutma)
ölçümü bu partiden sonra bu yüzden **iki değişkenle** birden okunacak: yeni dilim ve
seyrelen replay. Ayrıştırmak için replay'i büyütmek ayrı bir iş.

Çıktı: data/judged/v0.0.3.jsonl → uv run python src/build.py data/judged/v0.0.3.jsonl v0.0.3

Kullanım: uv run python scripts/analiz/2026-09-15-v003-derleme.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).parent.parent.parent
sys.path.insert(0, str(KOK / "src"))
from checks import run_checks  # noqa: E402

V3_ADAY = KOK / "data/candidates/v3-kumulatif.jsonl"
V3_JUDGE = KOK / "data/judged/v3-kumulatif.v7.jsonl"
REPLAY = KOK / "data/candidates/replay-v1.jsonl"
V4_JUDGE = KOK / "data/judged/v4-parti1.v7.jsonl"
CIKTI = KOK / "data/judged/v0.0.3.jsonl"


def oku(p: Path) -> list[dict]:
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def main() -> int:
    v3, v3j, replay, v4 = oku(V3_ADAY), oku(V3_JUDGE), oku(REPLAY), oku(V4_JUDGE)

    jmap = {r["id"]: r.get("judge") for r in v3j}
    if set(jmap) != {r["id"] for r in v3}:
        print("HATA: v3 aday ve judge kimlik kümeleri farklı — birleştirme güvenli değil.")
        return 1

    # Kimlik çakışması: üç kaynak arasında aynı id olursa kayıt sessizce ezilirdi.
    hepsi = [r["id"] for r in v3] + [r["id"] for r in replay] + [r["id"] for r in v4]
    cakisan = [i for i, n in Counter(hepsi).items() if n > 1]
    if cakisan:
        print(f"HATA: kimlik çakışması ({len(cakisan)}): {cakisan[:5]}")
        return 1

    cikti, kapi_dusen, judgesiz = [], [], []
    for r in v3 + replay + v4:
        r = dict(r)
        if r["id"] in jmap:
            r["judge"] = jmap[r["id"]]
        chk = run_checks(r)
        r["_checks"] = chk
        if not chk.get("passed"):
            kapi_dusen.append((r["id"], chk))
        if not r.get("replay") and not isinstance(r.get("judge"), dict):
            judgesiz.append(r["id"])
        cikti.append(r)

    if judgesiz:
        print(f"HATA: judge'suz {len(judgesiz)} terapötik kayıt: {judgesiz[:5]}")
        return 1

    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in cikti),
                     encoding="utf-8")

    jm = Counter(r["judge"].get("judge_model") for r in cikti
                 if isinstance(r.get("judge"), dict))
    rub = Counter(r["judge"].get("prompt_version") for r in cikti
                  if isinstance(r.get("judge"), dict))
    terapotik = sum(1 for r in cikti if not r.get("replay"))
    rep = len(cikti) - terapotik

    print(f"v3 aday    {V3_ADAY.name:26} {len(v3):>4} kayıt  sha {sha(V3_ADAY)}")
    print(f"v3 judge   {V3_JUDGE.name:26} {len(v3j):>4} kayıt  sha {sha(V3_JUDGE)}")
    print(f"replay     {REPLAY.name:26} {len(replay):>4} kayıt  sha {sha(REPLAY)}")
    print(f"v4 judge   {V4_JUDGE.name:26} {len(v4):>4} kayıt  sha {sha(V4_JUDGE)}")
    print(f"\nkapı: {len(cikti) - len(kapi_dusen)}/{len(cikti)} geçti")
    for i, c in kapi_dusen:
        print(f"  DÜŞTÜ {i}: {[k for k, v in c.items() if v is False]}")
    print(f"judge_model: {dict(jm)}")
    print(f"rubrik:      {dict(rub)}")
    print(f"⚠️ K97: iki ayrı judge dalgası varsa sayılar AYNI tabloda karşılaştırılamaz.")
    print(f"\nterapötik {terapotik} · replay {rep} · replay payı %{100*rep/len(cikti):.1f} "
          f"(§9 hedefi %15 — v0.0.2'de %15,4)")
    ihlal = [r["id"] for r in cikti if isinstance(r.get("judge"), dict)
             and r["judge"].get("klinik_guvenlik_ihlali")]
    print(f"klinik güvenlik ihlali: {len(ihlal)}/{terapotik}" + (f" → {ihlal}" if ihlal else ""))
    print(f"\nyazıldı: {CIKTI.relative_to(KOK)}  sha {sha(CIKTI)}")
    print("sıradaki: uv run python src/build.py data/judged/v0.0.3.jsonl v0.0.3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
