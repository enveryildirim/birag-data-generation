#!/usr/bin/env python3
"""Doz-yanıt korpuslarını üretir: v0.0.3'e yönlendirme cümlelerini EKLER.

Tasarım ve ölçütler: scripts/analiz/2026-09-15-doz-yanit-plan.py (üretimden önce yazılı).
Bu betik o tasarımı uygular ve I1-I6 değişmezlerini MAKİNEYLE denetler. Herhangi biri
tutmazsa DURUR; «yaklaşık tuttu» yoktur.

Çıktı:
  data/candidates/v0.0.4-doz10.jsonl   (137 terapötik + 18 replay, yönlendirme 14)
  data/candidates/v0.0.5-doz25.jsonl   (137 terapötik + 18 replay, yönlendirme 33)
  reports/analiz/2026-09-15-doz-yanit-yamalar.json
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

KOK = Path(__file__).parent.parent.parent
sys.path.insert(0, str(KOK / "src"))
from checks import run_checks  # noqa: E402

KAYNAK = KOK / "datasets/v0.0.3/train.jsonl"
YAMA = KOK / "data/candidates/doz-yonlendirme-ekleri.jsonl"
PLAN = KOK / "data/plan/doz-yanit-ekler.jsonl"

# D2/I5 — makine denetimi. Kurum ÖZEL adları: model kendisi atamaz (K18).
KURUM = re.compile(r"\b(AMATEM|ÇEMATEM|ÇEMATEM|YEDAM|ALO\s*191|SHÇEK|Yeşilay)\b", re.I)
RAKAM = re.compile(r"\d")
# D3 — emredici kip vekili. §H.6'nın yasakladığı kalıplar.
EMIR = re.compile(r"\b(git|gitmelisin|başvur|başvurmalısın|ara|aramalısın|söyle|"
                  r"söylemelisin|yapmalısın|etmelisin|sormalısın|konuşmalısın)\b", re.I)
# D2 — yordam iddiası vekili (başvuru sırası, süre, ücret, randevu düzeni).
YORDAM = re.compile(r"\b(ücret|ücretsiz|randevu al|sevk|sıra|kaç gün|kaç hafta|"
                    r"önce .* sonra .* başvur|kayıt yaptır|form doldur)\b", re.I)


# D1 — eklenen cümle kaynağın TÜRÜNÜ adlandırmalı VE bir ADIM göstermeli.
# Sadece sahibi adlandırmak (T29'un `sinir_cekme`'si) bu dilime SAYILMAZ.
TUR = re.compile(r"\b(hekim\w*|doktor\w*|eczacı\w*|avukat\w*|psikiyatr\w*|psikolog\w*|"
                 r"danışman\w*|uzman\w*|merkez\w*|birim\w*|poliklinik\w*)", re.I)
ADIM = re.compile(r"\b(sor\w*|anlat\w*|söyle\w*|ilet\w*|aktar\w*|yaz\w*|götür\w*|"
                  r"başlangıc\w*|adım\w*|yol\b|açılış\w*)", re.I)
# Şablonlaşma denetimi. ⚠️ İLK SÜRÜMDE YANLIŞ ÖLÇÜYORDU: «-ebilirsin» gibi sıradan bir
# DİLBİLGİSİ EKİNİ şablon sayıyordu. Şablon ek değil ÖBEKTİR — aynı 4 kelimelik dizinin
# tekrarı. Ek saymak, 26 cümleyi yüklemsiz adlaştırmaya iterek anlaşılırlığı düşürdü
# (ölçüldü: `anlasilirlik` ortalaması 3,19 → 2,69). Ölçüt öbek tekrarına çevrildi.
KALIP_ESIK = 4          # aynı 4-gram en çok kaç eklemede geçebilir


def dortluler(t: str) -> set[str]:
    w = re.sub(r"[^\w\s]", " ", t.lower()).split()
    return {" ".join(w[i:i + 4]) for i in range(max(0, len(w) - 3))}


def cumleler(t: str) -> list[str]:
    return [c for c in re.split(r"(?<=[.!?])\s+", t.strip()) if c]


def uygula(metin: str, capa: str, ek: str, nerede: str, hata: list[str], kid: str) -> str:
    n = metin.count(capa)
    if n != 1:
        hata.append(f"{kid}/{nerede}: çapa {n} kez geçiyor (1 olmalı): «{capa[:60]}»")
        return metin
    return metin.replace(capa, capa + " " + ek, 1)


def main() -> None:
    kaynak = [json.loads(l) for l in KAYNAK.open()]
    son_cevap = {r["id"][:16]: [m for m in r["messages"] if m["role"] == "assistant"][-1]["content"]
                 for r in kaynak}
    yamalar = {y["id_16"]: y for y in (json.loads(l) for l in YAMA.open())}
    plan = {p["id_16"]: p for p in (json.loads(l) for l in PLAN.open())}
    if set(yamalar) != set(plan):
        raise SystemExit(f"⛔ yama ile plan örtüşmüyor: {sorted(set(yamalar) ^ set(plan))}")

    hata: list[str] = []
    zamire_dayali: list[str] = []
    rapor = {"tarih": date.today().isoformat(),
             "betik": "scripts/analiz/2026-09-15-doz-yanit-yamala.py",
             "kaynak": {"dosya": str(KAYNAK.relative_to(KOK)),
                        "sha256_16": hashlib.sha256(KAYNAK.read_bytes()).hexdigest()[:16]},
             "yamalar": {}, "setler": {}}

    # ─── D2/D3/I4: eklenen cümlelerin kendisi ─────────────────────────────────
    for kid, y in yamalar.items():
        for alan in ("cevap_ek", "thinking_ek"):
            ek = y[alan]
            if "?" in ek:
                hata.append(f"{kid}/{alan}: I4 — eklenen cümlede soru işareti var")
            if RAKAM.search(ek):
                hata.append(f"{kid}/{alan}: I5 — eklenen cümlede rakam var")
            if KURUM.search(ek):
                hata.append(f"{kid}/{alan}: I5 — kurum ÖZEL adı: {KURUM.search(ek).group()}")
            if YORDAM.search(ek):
                hata.append(f"{kid}/{alan}: D2 — yordam iddiası: {YORDAM.search(ek).group()}")
        if EMIR.search(y["cevap_ek"]):
            hata.append(f"{kid}: D3 — emredici kip: {EMIR.search(y['cevap_ek']).group()}")
        # D1/TÜR: tür eklemede ya da CEVABIN kendisinde geçmeli. §H.3 üç adımı bölüyor —
        # türü çoğu kayıtta hemen önceki SINIR cümlesi adlandırıyor, ekleme ona zamirle
        # gönderme yapıyor. Zamire dayanan ekleme sayısı raporlanır (T25: kota + kayıt).
        if not TUR.search(y["cevap_ek"]):
            if not TUR.search(son_cevap.get(kid, "")):
                hata.append(f"{kid}: D1 — kaynağın TÜRÜ ne eklemede ne cevapta geçiyor")
            else:
                zamire_dayali.append(kid)
        if not ADIM.search(y["cevap_ek"]):
            hata.append(f"{kid}: D1 — eklemede ADIM yok (yalnızca sınır çekme)")
    rapor["turu_zamirle_gonderen_ekleme"] = sorted(zamire_dayali)
    sayac: dict[str, int] = {}
    for y in yamalar.values():
        for g in dortluler(y["cevap_ek"]):
            sayac[g] = sayac.get(g, 0) + 1
    tekrar = {g: n for g, n in sayac.items() if n >= 3}
    rapor["tekrar_eden_dortlu"] = dict(sorted(tekrar.items(), key=lambda x: -x[1]))
    for g, n in tekrar.items():
        if n > KALIP_ESIK:
            hata.append(f"KALIP — «{g}» {n}/{len(yamalar)} eklemede; şablon oluyor")

    for hedef, surum, dosya in ((10, "v0.0.4", "v0.0.4-doz10.jsonl"),
                                (25, "v0.0.5", "v0.0.5-doz25.jsonl")):
        uygulanacak = {k: v for k, v in yamalar.items()
                       if v["doz"] == 10 or (hedef == 25 and v["doz"] == 25)}
        yeni: list[dict] = []
        for r in kaynak:
            kid = r["id"][:16]
            r2 = json.loads(json.dumps(r))          # derin kopya
            if kid in uygulanacak:
                y = uygulanacak[kid]
                son = [m for m in r2["messages"] if m["role"] == "assistant"][-1]
                asil_c, asil_t = son["content"], son.get("thinking") or ""
                son["content"] = uygula(asil_c, y["cevap_capa"], y["cevap_ek"],
                                        "cevap", hata, kid)
                son["thinking"] = uygula(asil_t, y["thinking_capa"], y["thinking_ek"],
                                         "thinking", hata, kid)
                # I2 — eklenen cümle çıkarılınca BAYT BAYT orijinal
                if son["content"].replace(" " + y["cevap_ek"], "", 1) != asil_c:
                    hata.append(f"{kid}: I2 — cevap geri alınamıyor")
                if son["thinking"].replace(" " + y["thinking_ek"], "", 1) != asil_t:
                    hata.append(f"{kid}: I2 — thinking geri alınamıyor")
                # I3 — son cümle değişmedi
                if cumleler(asil_c)[-1] != cumleler(son["content"])[-1]:
                    hata.append(f"{kid}: I3 — turun son cümlesi değişti")
                # I4 — soru sayısı oynamadı
                if asil_c.count("?") != son["content"].count("?"):
                    hata.append(f"{kid}: I4 — soru sayısı değişti")
                gm = r2.setdefault("gen_meta", {}) or {}
                gm["sinir_tipi"] = plan[kid]["sinir_tipi"]
                gm["doz_yamasi"] = {"betik": "2026-09-15-doz-yanit-yamala.py",
                                    "doz": y["doz"], "havuz": plan[kid]["havuz"]}
                r2["gen_meta"] = gm
            # I1 — kullanıcı mesajları / context / source_ids dokunulmadı
            ku = [m["content"] for m in r["messages"] if m["role"] == "user"]
            ku2 = [m["content"] for m in r2["messages"] if m["role"] == "user"]
            if ku != ku2 or r.get("context") != r2.get("context") \
               or r.get("source_ids") != r2.get("source_ids"):
                hata.append(f"{kid}: I1 — kullanıcı tarafı değişti")
            r2.pop("_checks", None)
            chk = run_checks(r2)
            if not chk.get("passed"):
                hata.append(f"{kid}: KAPI — {json.dumps(chk, ensure_ascii=False)[:200]}")
            r2["_checks"] = chk
            yeni.append(r2)

        if len(yeni) != len(kaynak):
            hata.append(f"{surum}: I1 — kayıt sayısı {len(yeni)} != {len(kaynak)}")
        yol = KOK / "data/candidates" / dosya
        with yol.open("w", encoding="utf-8") as f:
            for r in yeni:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        ter = [r for r in yeni if not r.get("replay")]
        yon = 7 + len(uygulanacak)
        rapor["setler"][surum] = {
            "dosya": str(yol.relative_to(KOK)), "kayit": len(yeni), "terapotik": len(ter),
            "uygulanan_yama": len(uygulanacak), "yonlendirme": yon,
            "oran": round(100 * yon / len(ter), 1),
            "degisen_id": sorted(uygulanacak),
            "sha256_16": hashlib.sha256(yol.read_bytes()).hexdigest()[:16],
        }

    # I6 — iç içelik
    a = set(rapor["setler"]["v0.0.4"]["degisen_id"])
    b = set(rapor["setler"]["v0.0.5"]["degisen_id"])
    if not a < b:
        hata.append("I6 — %10 kümesi %25'in öz alt kümesi değil")

    if hata:
        raise SystemExit("⛔ DEĞİŞMEZ TUTMADI:\n" + "\n".join(f"  - {h}" for h in hata))

    rapor["yamalar"] = {k: {"doz": v["doz"], "cevap_ek": v["cevap_ek"]}
                        for k, v in yamalar.items()}
    cikti = KOK / "reports/analiz/2026-09-15-doz-yanit-yamalar.json"
    cikti.write_text(json.dumps(rapor, ensure_ascii=False, indent=1), encoding="utf-8")

    print("DOZ-YANIT KORPUSLARI — üç nokta\n")
    print(f"{'set':8} {'kayıt':>5} {'terapötik':>9} {'yama':>5} {'yönlendirme':>12}")
    print(f"{'v0.0.3':8} {len(kaynak):>5} {len([r for r in kaynak if not r.get('replay')]):>9} "
          f"{0:>5} {7:>7} (%5.1)")
    for s, o in rapor["setler"].items():
        print(f"{s:8} {o['kayit']:>5} {o['terapotik']:>9} {o['uygulanan_yama']:>5} "
              f"{o['yonlendirme']:>7} (%{o['oran']})   sha {o['sha256_16']}")
    t = rapor["tekrar_eden_dortlu"]
    print(f"\n3+ eklemede geçen 4-gram: {len(t)} · en sık "
          f"{list(t.items())[:3] if t else '—'} (eşik {KALIP_ESIK})")
    print(f"türü zamirle gönderen ekleme: {len(rapor['turu_zamirle_gonderen_ekleme'])}/26 "
          f"(tür önceki SINIR cümlesinde adlandırılmış — §H.3'ün 2. adımı)")
    print(f"I1-I6 değişmezleri: ✅  ·  kapılar: ✅ {len(kaynak)}/{len(kaynak)} (her iki set)")
    print(f"yazıldı: {cikti.relative_to(KOK)}")


if __name__ == "__main__":
    main()
