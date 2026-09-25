#!/usr/bin/env python3
"""İnceleme kuyruğu — `run_checks`'in ELEMEDİĞİ ama işaretlediği her şey.

⛔⛔ **Neden var.** `src/checks.py` birkaç sinyali bilerek sert kapı yapmıyor ve
her birinin yanında aynı cümle yazılı: *«inceleme kuyruğuna gider»*. Ama kuyruğu
**okuyan bir şey yoktu**. En eskisi 2026-09-12'den beri bekliyor.

➡️⭐⭐ *Okunmayan bir sinyal, sinyal değildir. Bir kapıyı «rapor eden» yapmak, onu
susturmakla aynı şeydir — kuyruğu okuyan bir şey yazılmadıkça.* Bu oturum boyunca
kapıların SESSİZLİĞİ arandı; burada aranan şey kapıların **konuşup da kimsenin
dinlemediği** yer.

⭐ Kuyruktaki dört sinyal ve hepsinin gerekçesi `checks.py`'de yazılı:
  · yumuşak §15 kategorileri (`rol_siniri`, `bos_guvence`, …) — *«kelime taraması
    bağlamı ayırt edemez»* (2026-09-12 register sondası)
  · `number_candidates` — *«yıl gibi yanlış pozitifler olabilir»*
  · `reflection_question_ratio_ok` — *«bilgilendirici, sert kapı değil»* (K40)
  · `context_klinik_ad_izi` — *«bir ad iddia değildir»* (T150, 2026-09-18)

⭐⭐ **Okuyucu bir şey daha yapıyor: eşleşmenin NEREDE olduğunu söylüyor.** Bu
oturumun tekrarlanan dersi — bir ifade, kullanıcının sözünü AKTARIRKEN de geçebilir
ve o zaman ihlal değildir (T62'nin aynalama dersi, alıntı kapısının karşı olgusal
muafiyeti). ⇒ Her vuruş için: tırnak içinde mi, kullanıcının turunda geçiyor mu.

⛔ Bu betik KARAR VERMEZ ve hiçbir kaydı elemez; elle okunacak listeyi üretir.

Girdi : datasets/v*/train.jsonl (varsayılan: en yeni sürüm)
Çıktı : reports/analiz/2026-09-18-inceleme-kuyrugu.md
Kullanım: uv run python scripts/analiz/2026-09-18-inceleme-kuyrugu.py [set.jsonl]
"""
from __future__ import annotations

import hashlib
import datetime
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
# ⛔ K126 rapor tarihini betiğin ADINDAN türetir ve TEK SEFERLİK ölçümler için bu
# doğrudur: ad, sayının alındığı günü sabitler. Ama bu betik YENİDEN KOŞULABİLİR
# (her sürüm için bir rapor) ⇒ addaki tarih artık ölçümün değil betiğin YAZILDIĞI
# günü gösterir. 2026-09-19'da koşulan bir rapor «Tarih: 2026-09-18» diyordu.
# ➡️ *Yeniden koşulabilir bir betikte ad kimliktir, tarih değil.* İkisi de yazılır.
KOSU = datetime.date.today().isoformat()
RAPOR = KOK / f"reports/analiz/{TARIH}-inceleme-kuyrugu.md"

import checks as C  # noqa: E402
from tohum_guvenlik import i_sinifi, tr_fold, tr_kucult  # noqa: E402

GEREKCE = {
    "rol_siniri": "*«ben teşhis koyamam», «doz öneremem»* — model DOĞRU reddederken de geçer",
    "bos_guvence": "boş güvence ifadeleri — ama kullanıcının sözü aktarılırken de geçer",
    "zararli_normallestirme": "zararlı normalleştirme — aktarım ile onay ayrılmalı",
    "ahlaki_yargi_klinik": "bağlama duyarlı; eşleşme otomatik red değil",
    "sayi_adayi": "*«yıl gibi yanlış pozitifler olabilir»* (`checks.py:100`)",
    "yansitma_soru_orani": "K40: 20 kayıtlık ilk üretimde 17'si YALNIZ bunun yüzünden elenmişti",
    "klinik_ad_izi": "T150: bir ad iddia değildir; iddia yüklem gerektirir",
}


def _cumle(metin: str, ifade: str) -> str:
    """Eşleşmeyi taşıyan cümle — vuruşu bağlamıyla okumak için."""
    dusuk = i_sinifi(tr_kucult(metin))
    hedef = i_sinifi(tr_kucult(ifade))
    i = dusuk.find(hedef)
    if i < 0:
        return metin[:140]
    bas = max(metin.rfind(".", 0, i), metin.rfind("\n", 0, i)) + 1
    son = min([x for x in (metin.find(".", i), metin.find("\n", i)) if x != -1] or [len(metin)])
    return metin[bas:son + 1].strip()


def _nerede(r: dict, ifade: str, cumle: str) -> str:
    """⭐ Vuruş ihlal mi aktarım mı? Bu oturumun tekrarlanan dersi."""
    kul = tr_fold(" ".join(m.get("content", "") for m in r["messages"] if m["role"] == "user"))
    isaret = []
    if tr_fold(ifade) in kul:
        isaret.append("⚠️ **kullanıcı da yazmış**")
    if re.search(r'["«][^"»]*' + re.escape(ifade) + r'[^"»]*["»]', cumle, re.I):
        isaret.append("⚠️ **tırnak içinde**")
    return " · ".join(isaret) or "⛔ asistanın kendi cümlesi"


def main(yol: str | None) -> int:
    p = (Path(yol) if yol and Path(yol).is_absolute() else KOK / yol) if yol else \
        sorted(KOK.glob("datasets/v*/train.jsonl"))[-1]
    ham = p.read_bytes()
    kayitlar = [json.loads(s) for s in ham.decode("utf-8").splitlines() if s.strip()]

    kuyruk: dict[str, list] = {}
    for r in kayitlar:
        c = C.run_checks(r)
        asst = [m for m in r["messages"] if m["role"] == "assistant"][-1]
        metin = asst.get("content", "")
        for kat, ifadeler in (c.get("forbidden_hits") or {}).items():
            if kat in C.SERT_KATEGORILER:
                continue                       # ⛔ sert kapı: kuyrukta değil, elenmiş
            for i in ifadeler:
                cum = _cumle(metin, i)
                kuyruk.setdefault(kat, []).append(
                    {"id": r["id"], "oge": i, "cumle": cum, "yer": _nerede(r, i, cum)})
        for i in (c.get("number_candidates") or []):
            cum = _cumle(metin, i)
            kuyruk.setdefault("sayi_adayi", []).append(
                {"id": r["id"], "oge": i, "cumle": cum, "yer": _nerede(r, i, cum)})
        if c.get("reflection_question_ratio_ok") is False:
            # ⭐ REPLAY AYRI İŞARETLENİR: persona kapıları replay dilimine zaten
            # uygulanmıyor (§9 çeşitlilik) ⇒ oran orada bir sinyal değil, gürültü.
            # ⛔ İlk yazımda ayrılmamıştı ve kuyrukta *«Aldığınız eğitimden ne kadar
            # memnunsunuz?»* gibi bir ANKET sorusu duruyordu; elle okuyan kişi onu
            # her seferinde yeniden eleyecekti. ➡️ *Bir kuyruk, kapsamı dışındaki
            # ögeyi taşıyorsa okunma maliyetini kalıcı olarak artırır.*
            kuyruk.setdefault("yansitma_soru_orani", []).append(
                {"id": r["id"], "oge": f"oran {c.get('reflection_question_ratio')}",
                 "cumle": metin[:140],
                 "yer": "⚠️ **replay — persona kapıları kapsam dışı**"
                        if r.get("replay") else "—"})
        for i in (c.get("context_klinik_ad_izi") or []):
            kaynak = next((k for k in (r.get("context") or [])
                           if C.KLINIK_AD.search(i_sinifi(k.get("metin") or ""))), {})
            kuyruk.setdefault("klinik_ad_izi", []).append(
                {"id": r["id"], "oge": i, "cumle": (kaynak.get("metin") or "")[:150],
                 "yer": f"bağlam pasajı · `{kaynak.get('kaynak')}`"})

    toplam = sum(len(v) for v in kuyruk.values())
    kayit = len({x["id"] for v in kuyruk.values() for x in v})
    sat = ["# İnceleme kuyruğu — kapıların konuşup da kimsenin dinlemediği yer", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` (yazıldı {TARIH}) · "
           f"**koşu tarihi:** {KOSU}  ",
           f"**Girdi:** `{p.relative_to(KOK)}` · SHA256-16 `{hashlib.sha256(ham).hexdigest()[:16]}` "
           f"· **{len(kayitlar)}** kayıt", "",
           "⛔⛔ **`checks.py` birkaç sinyali bilerek sert kapı yapmıyor** ve her birinin yanında",
           "aynı cümle yazılı: *«inceleme kuyruğuna gider»*. Ama kuyruğu **okuyan bir şey**",
           "**yoktu**; en eskisi **2026-09-12**'den beri bekliyor.", "",
           "➡️⭐⭐ *Okunmayan bir sinyal, sinyal değildir. Bir kapıyı «rapor eden» yapmak, onu",
           "susturmakla aynı şeydir — kuyruğu okuyan bir şey yazılmadıkça.*", "",
           f"## Özet — **{toplam} vuruş / {kayit} kayıt**", "",
           "| sinyal | vuruş | ⛔ asistanın kendi cümlesi | ne için kuyrukta |",
           "|---|---:|---:|---|"]
    for kat, v in sorted(kuyruk.items(), key=lambda x: -len(x[1])):
        kendi = sum(1 for x in v if x["yer"].startswith("⛔"))
        kapsam_disi = sum(1 for x in v if "kapsam dışı" in x["yer"])
        ek = f" · ⚠️ {kapsam_disi} kapsam dışı" if kapsam_disi else ""
        sat.append(f"| `{kat}` | **{len(v)}** | {kendi} | "
                   f"{GEREKCE.get(kat, '⛔ gerekçe yazılmamış')}{ek} |")
    if not kuyruk:
        sat.append("| — | 0 | 0 | ⭐ kuyruk boş |")
    sat += ["", "⭐ *«Asistanın kendi cümlesi»* sütunu ayrı duruyor çünkü bu oturumun",
            "tekrarlanan dersi: bir ifade **kullanıcının sözünü aktarırken** de geçebilir ve",
            "o zaman ihlal değildir (T62 aynalama). Kuyruğu okurken önce o sütuna bakılır.", ""]

    for kat, v in sorted(kuyruk.items(), key=lambda x: -len(x[1])):
        sat += [f"## `{kat}` ({len(v)})", "", "| kayıt | öge | cümle | yer |", "|---|---|---|---|"]
        for x in v:
            c = x["cumle"].replace("|", "\\|").replace("\n", " ")
            sat.append(f"| `{x['id'][:10]}` | `{x['oge']}` | {c[:130]} | {x['yer']} |")
        sat.append("")

    sat += ["## ⭐ Elle okuma kararları (2026-09-18, `v0.0.9`)", "",
            "⭐ **On altı vuruşun on altısı da belgelenmiş yanlış pozitif sınıflarından;**",
            "kuyrukta **gerçek ihlal yok**. Ama kuyruk yine de işe yaradı: okunur okunmaz",
            "üretim filtresinde bir kusur ortaya çıkardı (aşağıya bakınız).", "",
            "| sinyal | karar |", "|---|---|",
            "| `klinik_ad_izi` (6) | ✅ altısı da yordam/uygunluk/gizlilik cümlesi — "
            "üçü tam tersini söylüyor: *«Araç tanı koymaz»* (T150) |",
            "| `yansitma_soru_orani` (4) | ✅ ikisi K40'ın tarif ettiği doğru MI kalıbı "
            "(bileşik yansıtma + tek soru), biri kriz sondası (*«kendine zarar vermeyi "
            "düşündüğün bir an oldu mu»* — doğrudan sorulması GEREKEN), biri replay ⇒ kapsam dışı |",
            "| `rol_siniri` (3) | ✅ üçü de *«doz»*; ikisi doğru reddin içinde "
            "(*«ben söyleyemem»*), biri kullanıcının kendi sözünün yansıtması |",
            "| `sayi_adayi` (2) | ✅ ikisi de replay: *«Versailles… 1919»* ve *«RX 6900XTX»* |",
            "| `zararli_normallestirme` (1) | ✅ *«herkes yapıyor»* tırnak içinde ve "
            "açıkça REDDEDİLİYOR: *«…cümlesini bir kenara koyuyorum»* |", "",
            "### ⛔⛔ Kuyruk okunur okunmaz bir üretim kusuru buldu", "",
            "`bos_guvence` altındaki tek satır bir boş güvence **değildi**: *«…sayıyı yine de",
            "merak ETMEK bunları geçersiz kılmıyor»*. Düz alt dizge araması, *«merak etme»*",
            "olumsuz emrini *«merak etmek»* mastarının içinde buluyordu. Bütün korpuslarda",
            "bu kategorinin **16 vuruşunun 16'sı** aynı kusurdandı ⇒ düzeltildi",
            "(`2026-09-18-yasak-ifade-eki.md`), kategori **16 → 0**.", "",
            "➡️⭐⭐ *Kuyruğun değeri içindekiler değildi — okunması oldu. Bir sinyali okumak,",
            "sinyali üreten aracı da denetlemektir.*", "",
            "## ⛔ Bu raporun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **Karar vermiyor** | her satır ELLE okunmalı; betik yalnız listeyi üretir |",
            "| ⛔ **Sözlüğe bağlı** | yumuşak kategoriler `configs/filters.yaml`'daki ifade "
            "listesinden geliyor ⇒ listede olmayan bir ihlal kuyruğa da girmez |",
            "| ⚠️ **«Kullanıcı da yazmış» muaf DEĞİL** | aynalamak meşru olabilir ama "
            "ONAYLAMAK değildir; sütun bir muafiyet değil, okuma sırası |",
            "| ⛔ **Tek set** | varsayılan olarak yalnız en yeni sürüm okunuyor |", ""]

    (KOK / f"reports/analiz/{TARIH}-inceleme-kuyrugu.json").write_text(
        json.dumps({"tarih": TARIH, "girdi": str(p.relative_to(KOK)),
                    "sha256_16": hashlib.sha256(ham).hexdigest()[:16],
                    "kayit": len(kayitlar), "kuyruk": kuyruk}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[10:]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else None))
