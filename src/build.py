"""judged/ -> datasets/vX.Y.Z/ (IMMUTABLE). Bkz. plan.md §11, §13.

Kullanım: uv run python src/build.py data/judged/v0.0.1.jsonl v0.0.1
"""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent


def _git_rev() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                               capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "no-git"


# Güvenlik karantinası (2026-09-14). Tohum meta'sında riskli eşdurum (intihar
# düşüncesi, yoksunluk vakası vb.) taşıyan ve yazılmış kaydı uzman incelemesi
# gerektiren kayıtlar. Kriz davranışı kararı uzmana ait (AGENTS Kural 3), bu yüzden
# kayıtlar SİLİNMİYOR (Kural 7) ama uzman karar verene kadar eğitim setine girmiyor.
KARANTINA_YOL = ROOT / "data" / "guvenlik-karantinasi.jsonl"


def _karantina() -> dict[str, dict]:
    if not KARANTINA_YOL.exists():
        return {}
    return {k["id"]: k for k in
            (json.loads(l) for l in open(KARANTINA_YOL) if l.strip())
            if k.get("durum") != "uzman_onayladi"}


def main(judged_path: str, version: str):
    records = [json.loads(l) for l in open(judged_path) if l.strip()]
    karantina = _karantina()

    kept, dropped = [], []
    for r in records:
        if r.get("id") in karantina:
            dropped.append({"source_ids": r.get("source_ids"), "reason": "guvenlik_karantinasi",
                            "detail": karantina[r["id"]]})
            continue
        chk = r.pop("_checks", {})
        jr = r.get("judge")
        if not chk.get("passed", False):
            dropped.append({"source_ids": r.get("source_ids"), "reason": "checks_failed", "detail": chk})
            continue
        # ⛔⛔ KAPI AÇIĞA DÜŞÜYORDU. Koşul `if jr and ...` idi: `judge` alanı NULL
        # olan kayıt, yargılanıp temiz çıkmış kayıtla AYNI şekilde geçiyordu.
        # Yani korpusun tek otomatik klinik güvenlik kapısı, «denetlendi ve
        # temiz» ile «hiç denetlenmedi»yi ayırt edemiyordu.
        # ⭐ Şimdiye kadar buradan yalnız `replay` dilimi (18 kayıt) geçti ve o
        # BİLEREK yargılanmıyor — ama bu ayrımı kod değil, üreticinin bilgisi
        # taşıyordu. ➡️ *Bir muafiyet kodda yazılı değilse, o bir muafiyet değil
        # bir şanstır.* ⇒ Muafiyet yazıldı, kapı KAPALI düşüyor.
        if not jr:
            if r.get("replay"):
                pass                      # ⭐ §9 replay dilimi: yargı dışı, YAZILI muafiyet
            else:
                dropped.append({"source_ids": r.get("source_ids"),
                                "reason": "judge_yok",
                                "detail": "yargılanmamış kayıt derlemeye giremez"})
                continue
        elif jr.get("klinik_guvenlik_ihlali"):
            dropped.append({"source_ids": r.get("source_ids"), "reason": "judge_safety_violation", "detail": jr})
            continue
        # ⛔⛔ UYDURMA KAPISI — kullanıcı kararı (2026-09-22).
        # `grounding == 2`: judge'ın adlandırdığı somut ayrıntı konuşmada YOK
        # ve hipotez olarak da işaretlenmemiş ⇒ cevap, kullanıcının söylemediği
        # bir şeyi söylemiş gibi sunuyor. Böyle bir kaydı eğitmek modele
        # uydurmayı öğretir.
        # ⚠️ ÜÇ ŞERH, hepsi ölçülmüş:
        #  (1) ALT SINIR (T238): `grounding` TEK-AYRINTI sondasıdır — judge'ın
        #      adlandırdığı tek ayrıntı dayanaklıysa 5 verir ve aynı cevaptaki
        #      başka bir uydurmayı GÖRMEZ. ⇒ Bu kapı yakaladığını eler,
        #      korpusu uydurmadan ARINDIRMAZ.
        #  (2) SONDANIN DUYARLILIĞI JUDGE'A GÖRE DEĞİŞİYOR: Claude 921 yargıda
        #      54, Gemini 150 yargıda 4 ateşliyor ⇒ Gemini ile puanlanmış
        #      kayıtlar daha AZ süzülüyor. Kapı korpusa judge-bağımlı bir
        #      asimetri sokuyor ve bu veri kartına yazılmalıdır.
        #  (3) `replay` dilimi muaf: `judge` alanı yok, yukarıdaki `if not jr`
        #      kolundan geçiyor (§9 yazılı muafiyet).
        elif jr.get("grounding") == 2:
            dropped.append({"source_ids": r.get("source_ids"),
                            "reason": "judge_uydurma",
                            "detail": {k: jr.get(k) for k in
                                       ("grounding", "en_somut_ayrinti",
                                        "ayrinti_konusmada_var", "judge_model",
                                        "gerekce")}})
            continue
        kept.append(r)

    out_dir = ROOT / "datasets" / version
    if out_dir.exists():
        print(f"HATA: {out_dir} zaten var — datasets/ IMMUTABLE, üzerine yazılmaz.")
        sys.exit(1)
    out_dir.mkdir(parents=True)

    train_path = out_dir / "train.jsonl"
    with open(train_path, "w") as f:
        for r in kept:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    input_hash = hashlib.sha256(Path(judged_path).read_bytes()).hexdigest()[:16]
    manifest = {
        "version": version,
        "date": str(date.today()),
        "git_rev": _git_rev(),
        "input_file": judged_path,
        "input_sha256_16": input_hash,
        "n_total": len(records),
        "n_kept": len(kept),
        "n_dropped": len(dropped),
        "dropped": dropped,
        "scenario_counts": dict(Counter(r["scenario"] for r in kept)),
        "addiction_type_counts": dict(Counter(r["addiction_type"] for r in kept)),
        "age_group_counts": dict(Counter(r["age_group"] for r in kept)),
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

    print(f"yazıldı: {train_path}  ({len(kept)}/{len(records)} kayıt)")
    print(f"manifest: {out_dir / 'manifest.json'}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("kullanım: uv run python src/build.py <judged.jsonl> <version>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
