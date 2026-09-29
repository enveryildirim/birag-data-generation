#!/usr/bin/env python3
"""`v0.1.1` ön kaydı EK-2 çözümlemesi — Colab + Unsloth, iki kol aynı ortamda (2026-09-29).

⭐ Zincir: bu betik → EK-1 çözümlemesi (kazanç şartlı hüküm) → ana çözümleme (mühür, tamlık,
ayar kilitleri, ölçüler, `ozet`, bekçiler). Üçü de mühürlü; burada yalnız EK-2'nin
değiştirdikleri var:

  1. kollar   `v011u` (datasets/v0.1.1) ↔ `v010u` (datasets/v0.1.0), ikisi de Colab'da eğitildi.
              Kayıtlı MLX `e3` koşuları hükme GİRMEZ.
  2. ortam    16 koşunun hepsinde `colab_egitim.SABIT_ALANLAR` aynı olmak ZORUNDA (DUR);
              GPU hücre başına raporlanır, bir tohumun iki kolu farklı GPU'daysa işaretlenir.
  3. onarım   ana çözümlemenin iki RAPORLANIR ölçüsü puanlanmış `sonuclar.jsonl`'de olmayan
              alanları okuyordu (`uretim_token` → hep 0 · `thinking_kapandi` → yok). Colab'ın
              dokunulmamış `ham.jsonl`'ünden yeniden hesaplanır. İkisi de hükme girmez.

Kullanım: önce `scripts/analiz/2026-09-29-v011-colab-puanla.py`, sonra bu betik.
"""
from __future__ import annotations

import hashlib
import json
import statistics as st
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import colab_egitim as CE  # noqa: E402
import v011_olcu as O  # noqa: E402

EK2 = KOK / "configs/deney/2026-09-29-v011-on-kayit-ek2.json"
RAPOR = KOK / "reports/analiz/2026-09-29-v011-onkayit-ek2-sonuc.md"
KOLLAR = {"v011": "v011u", "e3": "v010u"}          # ana çözümlemenin kol adları → EK-2 önekleri


def _modul(ad: str, yol: str):
    y = KOK / yol
    sp = _iu.spec_from_file_location(ad, y)
    m = _iu.module_from_spec(sp)
    argv, sys.argv = sys.argv[:], [str(y)]
    sp.loader.exec_module(m)
    sys.argv = argv
    return m


E1 = _modul("_v011_ek1c", "scripts/analiz/2026-09-29-v011-onkayit-ek1-cozumleme.py")
A = E1.A


def _sha16(y: Path) -> str:
    return hashlib.sha256(y.read_bytes()).hexdigest()[:16]


def ortam_denetle(h: dict) -> tuple[dict, dict, list[int]]:
    ort = {}
    for key, d in h.items():
        for f in ("ortam.json", "ham.jsonl"):
            if not (d / f).exists():
                raise SystemExit(f"⛔ {d.name}: {f} yok — Colab çıktısı eksik")
        if key[2] != "cokturlu" and "otomatik_gecti" not in json.loads((d / "sonuclar.jsonl").read_text(encoding="utf-8").splitlines()[0]):
            raise SystemExit(f"⛔ {d.name} puanlanmamış — önce scripts/analiz/2026-09-29-v011-colab-puanla.py")
        ort[key] = json.loads((d / "ortam.json").read_text(encoding="utf-8"))
    ref = next(iter(ort.values()))
    fark = sorted({(k[0], k[1], a) for k, o in ort.items() for a in CE.SABIT_ALANLAR if o.get(a) != ref.get(a)})
    if fark:
        raise SystemExit(f"⛔ ortam koşular arasında farklı — iki kol aynı ortamda değil (EK-2): {fark[:6]}")
    if ref["uretim"] != CE.URETIM:
        raise SystemExit(f"⛔ üretim ayarı {ref['uretim']} ≠ ön kayıt {CE.URETIM}")
    gpu = {(kol, t): sorted({o.get("gpu") or "—" for k, o in ort.items() if k[:2] == (kol, t)})
           for kol in KOLLAR for t in A.TOHUM}
    karisik = [t for t in A.TOHUM if gpu[("v011", t)] != gpu[("e3", t)]]
    return ref, gpu, karisik


def ham_onar(h: dict, kol: str) -> dict[str, list[float]]:
    tok, dej = [], []
    for t in A.TOHUM:
        rows = [json.loads(x) for k in A.BIRAG for x in (h[(kol, t, k)] / "ham.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
        tok.append(st.median(r["uretim_token"] for r in rows))
        dej.append(O.tek_tur_ozet(rows)["dejenere_payi"])
    return {"R_uretim_token_ortanca": tok, "R_dejenere_payi": dej}


def main() -> int:
    E1._sina()
    e2 = json.loads(EK2.read_text(encoding="utf-8"))
    e1 = json.loads(E1.EK1.read_text(encoding="utf-8"))
    m = json.loads(A.ONKAYIT.read_text(encoding="utf-8"))
    kotu = [(y, s) for y, s in e2["muhurlu_dosyalar"].items() if not (KOK / y).exists() or _sha16(KOK / y) != s]
    if kotu:
        raise SystemExit(f"⛔ EK-2 mührü bozuk — puan OKUNMADI: {kotu}")
    if _sha16(E1.EK1) != e2["ek1_sha256_16"] or _sha16(A.ONKAYIT) != e2["ana_on_kayit_sha256_16"]:
        raise SystemExit("⛔ EK-1 ya da ana ön kayıt EK-2'nin gördüğüyle aynı değil — puan OKUNMADI")
    if [(y, s) for y, s in e1["muhurlu_dosyalar"].items() if _sha16(KOK / y) != s]:
        raise SystemExit("⛔ EK-1 mührü bozuk — puan OKUNMADI")
    A._muhur(m)
    h = A._hucreler(m, KOLLAR)
    ref, gpu, karisik = ortam_denetle(h)
    Y, E = A.olc(h, "v011", m), A.olc(h, "e3", m)
    Y.update(ham_onar(h, "v011")); E.update(ham_onar(h, "e3"))
    z = {ad: A.ozet(Y[ad], E[ad]) for ad in Y}
    hk, ates = E1.hukum(z, m)

    s = ["# `v0.1.1` ön kaydı — sonuç (EK-1 + EK-2 · Colab)", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **EK-2** `{_sha16(EK2)}` · **EK-1** `{_sha16(E1.EK1)}` · "
         f"**ana** `{_sha16(A.ONKAYIT)}` (üçü de denetlendi)  ",
         f"**Kollar:** `v011u` (datasets/v0.1.1) ↔ `v010u` (datasets/v0.1.0), ikisi de Colab · tohumlar {A.TOHUM} · hücreler tam  ",
         f"**Ortam (16 koşuda aynı):** `{ref['model_id']}` @ `{ref['model_revizyon']}` · LoRA yolu `{ref['lora_yolu']}` · "
         + " · ".join(f"{k} {v}" for k, v in ref["surumler"].items() if v), "",
         "## Hüküm", "", f"**{hk}**", ""]
    if ates:
        s += [f"Ateşleyen bekçiler: {', '.join('`' + a + '`' for a in ates)}", ""]
    s += ["| ölçü | ort v011u | ort v010u | Δ | SE_b | okuma |", "|---|---:|---:|---:|---:|---|"]
    s += [f"| `{ad}` | {v['ort_v011']:.2f} | {v['ort_e3']:.2f} | {v['delta']:+.2f} | {v['se_b']:.2f} | "
          f"{v['yon']}{' ⛔' if ad in ates else ''} |" for ad, v in z.items()]
    s += ["", "`R_uretim_token_ortanca` ve `R_dejenere_payi` `ham.jsonl`'den yeniden hesaplandı (EK-2 onarımı).", "",
          "## GPU", "", "| tohum | v011u | v010u |", "|---:|---|---|"]
    s += [f"| {t} | {', '.join(gpu[('v011', t)])} | {', '.join(gpu[('e3', t)])} |{' ⚠️ farklı' if t in karisik else ''}" for t in A.TOHUM]
    s += ["", "## ⛔ Bunun söylemedikleri", "",
          *[f"- {x}" for x in m["bunun_soylemedikleri"] + json.loads(E1.EK1.read_text())["bunun_soylemedikleri"] + e2["bunun_soylemedikleri"]]]
    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    print(hk); print(f"yazıldı: {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
