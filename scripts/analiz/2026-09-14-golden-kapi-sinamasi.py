#!/usr/bin/env python3
"""`golden_checks.py` kapılarının KÖR SINAMASI — kapı gerçekten ateşliyor mu.

Neden: bu oturumda "kapı geçti" ile "kapı çalışıyor" arasındaki farkın altı kez
canı yandı (K65, K70, K76, §7b, `iyi_giden_uygun`, `YOKSUNLUK_BELIRTI`). Temiz
geçen bir kapı ya doğru çalışıyordur ya da hiçbir şey ölçmüyordur; ikisi dışarıdan
aynı görünür. Bu betik kasten BOZUK öğeler üretip her kapının ateşlediğini
doğrular. Bir vaka kaçarsa çıkış kodu 1.

Kullanım: uv run python scripts/analiz/2026-09-14-golden-kapi-sinamasi.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import golden_checks as gk  # noqa: E402


def vakalar(temel: dict, atama: dict) -> dict[str, dict]:
    test_t = next(s for s, d in atama.items() if d == "test")
    locked_t = next(s for s, d in atama.items() if d == "locked")
    return {
        "MÜHÜR: test havuzundan tohum çekilmiş":
            {**temel, "kaynak": {**temel["kaynak"], "seed_id": test_t}},
        "MÜHÜR: locked havuzundan tohum çekilmiş":
            {**temel, "kaynak": {**temel["kaynak"], "seed_id": locked_t}},
        "MÜHÜR: havuzda olmayan tohum":
            {**temel, "kaynak": {**temel["kaynak"], "seed_id": "yok-boyle-bir-sey"}},
        "REFERANS: öğeye asistan cevabı yazılmış":
            {**temel, "messages": temel["messages"] + [{"role": "assistant", "content": "Zor bir gün olmuş."}]},
        "İLKE: varlık iddiası otomatiğe konmuş":
            {**temel, "iddialar": [{"tip": "otomatik", "kural": "yansitma_olmali"}]},
        "KAPALI KÜME: duygu sözcüğü uydurma_yok'a konmuş":
            {**temel, "iddialar": [{"tip": "otomatik", "kural": "uydurma_yok",
                                    "kavramlar": ["yalnız", "suçluluk"]}]},
        "TRİVYAL: yasaklanan kavram zaten girdide geçiyor":
            {**temel, "iddialar": [{"tip": "otomatik", "kural": "uydurma_yok",
                                    "kavramlar": ["sigara"]}],
             "messages": [temel["messages"][0],
                          {"role": "user", "content": "Günde bir paket sigara içiyorum."}]},
        "İddiasız öğe": {**temel, "iddialar": []},
        "Sondasız öğe": {**temel, "sonda": ""},
        "Elle yazılmış ama gerekçesiz": {**temel, "kaynak": {"tip": "elle"}},
        "Bilinmeyen iddia tipi": {**temel, "iddialar": [{"tip": "sezgi", "alan": "x"}]},
        "Yanlış bölme alanı": {**temel, "bolme": "locked"},
    }


def main() -> None:
    atama = json.loads((KOK / "evals/bolme.json").read_text())["atama"]
    temel = json.loads(open(KOK / "evals/golden.dev.jsonl").readline())

    kacan = []
    for ad, oge in vakalar(temel, atama).items():
        ihlal = gk.oge_kapilari(oge, "dev", atama)
        print(f"{'  yakaladı' if ihlal else '  ⚠️ KAÇIRDI'}  {ad}")
        if not ihlal:
            kacan.append(ad)

    # Küme kapısı ayrı: iki öğe, aynı kullanıcı metni, farklı id.
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
        f.write(json.dumps(temel, ensure_ascii=False) + "\n")
        f.write(json.dumps({**temel, "id": "gd-999"}, ensure_ascii=False) + "\n")
        yol = Path(f.name)
    _, rapor = gk.dosya_kapilari(yol, "dev")
    tamam = bool(rapor["kume"])
    print(f"{'  yakaladı' if tamam else '  ⚠️ KAÇIRDI'}  KÜME: aynı kullanıcı metni iki öğede")
    if not tamam:
        kacan.append("KÜME: aynı kullanıcı metni")
    yol.unlink()

    # Olumlu kontrol: gerçek dosya temiz geçmeli, yoksa kapılar her şeyi yakıyordur.
    _, gercek = gk.dosya_kapilari(KOK / "evals/golden.dev.jsonl", "dev")
    if gercek["ihlal"] or gercek["kume"]:
        print(f"  ⚠️ YANLIŞ POZİTİF: gerçek set kapıdan düştü — {gercek['ihlal']} {gercek['kume']}")
        kacan.append("yanlış pozitif")
    else:
        print(f"  yakaladı  (olumlu kontrol: gerçek {gercek['toplam']} öğe temiz geçti)")

    if kacan:
        print(f"\nBAŞARISIZ — {len(kacan)} vaka kaçtı: {kacan}")
        sys.exit(1)
    print("\nTüm vakalar yakalandı; kapılar ateşliyor.")


if __name__ == "__main__":
    main()
