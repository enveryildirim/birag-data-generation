#!/usr/bin/env python3
"""`src/checks.py::run_checks` — ÜRETİM kapısının muafiyetleri sayılıyor.

⛔⛔ **Neden bu kapı ötekilerden önemli.** T141/T144'te sayılan sekiz kapı ANALİZ
aracı: bulgu üretirler, kimseyi elemezler. `run_checks` ise `build.py`'nin
elemesini belirler ⇒ **`datasets/` içine neyin gireceğine o karar veriyor.**
Muafiyetleri bugüne dek hiç sayılmadı.

⭐⭐ **Yöntem: koşulu çevir, GERÇEK kapıyı yeniden koş.** Muafiyetin bedeli için
ikinci bir karar kuralı yazmak K97'nin yasakladığı şeydir (iki tanım, iki sayı).
Onun yerine kaydın **kopyası** muafiyeti tetiklemeyecek biçimde değiştirilip
`run_checks` **olduğu gibi** çağrılıyor:

  · `replay` muafiyeti → kopyada `replay=False` ⇒ persona kapıları uygulanır
  · `uretim-v2` muafiyeti → kopyada `prompt_version="uretim-v3"` ⇒ §7b sertleşir

➡️⭐ *Bir muafiyetin bedeli, kuralı yeniden yazarak değil, KOŞULU çevirip aynı
kuralı yeniden koşarak ölçülür.*

⭐ **Ve ölçülen sayı doğrudan okunabilir:** yayımlanmış set zaten kapıdan geçmiş
kayıtlardan oluşuyor ⇒ burada sayılan şey *«bu sette olup da muafiyet olmasa
OLMAYACAK kayıt»*, yani muafiyetin veri setine kattığı tam miktar.

⛔ Bu betik hiçbir şeyi ELEMİYOR ve hiçbir dosyayı değiştirmiyor; yalnız sayıyor.

Girdi : datasets/v*/train.jsonl · data/candidates/*.jsonl
Çıktı : reports/analiz/2026-09-18-uretim-kapisi-muafiyetleri.md
Kullanım: uv run python scripts/analiz/2026-09-18-uretim-kapisi-muafiyetleri.py
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]          # ⛔ rapor tarihi betiğin ADINDAN (K126)
RAPOR = KOK / f"reports/analiz/{TARIH}-uretim-kapisi-muafiyetleri.md"

from checks import run_checks, KLINIK_IDDIA, uretim_surumu  # noqa: E402
# ⛔ Sürüm koşulu BURADA YENİDEN YAZILMAZ: ilk yazımda `startswith("uretim-v3")`
# kopyalanmıştı ve kapı düzeltilince bu rapor onu İZLEMEDİ — kapıyı hâlâ «kapalı»
# gösterdi. ➡️ *Bir kapıyı denetleyen betik, kapının koşulunu kopyalarsa kapıyı
# değil kopyasını denetler (K97).* ⇒ `checks.uretim_surumu` çağrılıyor.
def _sert(r: dict) -> bool:
    return (uretim_surumu(r) or 0) >= 3

# ⭐ Feragat sezgisi ÖNERİ olarak ölçülüyor, kapıya EKLENMİYOR (bkz. §4).
OLUMSUZ = re.compile(r"(koymaz|aranmaz|gerekmez|değildir|yapılmaz|verilmez|yoktur"
                     r"|taşımaz|sayılmaz)")


def _replaysiz(r: dict) -> dict:
    """Muafiyet çevrilmiş kopya: kayıt BıRAG kaydıymış gibi değerlendirilir."""
    k = copy.deepcopy(r)
    k["replay"] = False
    return k


def _v3(r: dict) -> dict:
    """Muafiyet çevrilmiş kopya: §7b sert kapı olarak uygulanır."""
    k = copy.deepcopy(r)
    k.setdefault("gen_meta", {})["prompt_version"] = "uretim-v3"
    return k


# (ad, kayıt bu muafiyetin kapsamında mı, muafiyeti çeviren dönüşüm, gerekçe)
MUAFIYETLER = [
    ("replay_persona_muafiyeti", lambda r: bool(r.get("replay")), _replaysiz,
     "§9 çeşitlilik: replay dilimine MI/persona kapıları uygulanmaz (kısa yanıt, "
     "farklı prompt, İngilizce tasarım gereği)"),
    ("uretim_v2_baglam_muafiyeti",
     lambda r: not str((r.get("gen_meta") or {}).get("prompt_version", "")).startswith("uretim-v3"),
     _v3, "§7b kapısı 2026-09-14'te yazıldı; `expert-70` (uretim-v2) ondan önce "
          "üretildi ve geriye dönük düzeltilmiyor (SHA256 üç raporda kayıtlı)"),
]


def _kaynaklar() -> list[Path]:
    y = sorted(KOK.glob("datasets/v*/train.jsonl"))
    y += sorted(KOK.glob("data/candidates/*.jsonl"))
    return y


def _tara(p: Path) -> dict:
    ham = p.read_bytes()
    kayitlar = [json.loads(s) for s in ham.decode("utf-8").splitlines() if s.strip()]
    o = {"dosya": str(p.relative_to(KOK)), "sha256_16": hashlib.sha256(ham).hexdigest()[:16],
         "kayit": len(kayitlar), "gecen": 0, "muafiyet": {}}
    for r in kayitlar:
        try:
            temel = run_checks(r)
        except Exception as e:                       # ⚠️ bozuk kayıt SESSİZ geçmesin
            o.setdefault("hata", []).append(f"{r.get('id')}: {type(e).__name__}")
            continue
        o["gecen"] += bool(temel.get("passed"))
        if not temel.get("passed"):
            continue                                  # ⭐ zaten elenmiş: muafiyet konu dışı
        for ad, kapsamda, cevir, _ in MUAFIYETLER:
            if not kapsamda(r):
                continue
            d = o["muafiyet"].setdefault(ad, {"kapsam": 0, "net": 0, "ornek": [], "id": []})
            d["kapsam"] += 1
            try:
                if not run_checks(cevir(r)).get("passed"):
                    d["net"] += 1
                    d["id"].append(r.get("id"))
                    if len(d["ornek"]) < 6:
                        d["ornek"].append({"id": r.get("id"),
                                           "sebep": _sebep(run_checks(cevir(r)))})
            except Exception as e:
                o.setdefault("hata", []).append(f"{r.get('id')} · {ad}: {type(e).__name__}")
    return o


def _sebep(c: dict) -> str:
    """Kapının hangi maddesi düşürdü — `run_checks`'in KENDİ alanlarından."""
    s = []
    if not c.get("length_ok"):
        s.append(f"uzunluk ({c.get('length_error')})")
    if not c.get("question_count_ok"):
        s.append(f"soru sayısı {c.get('question_count')}")
    if not c.get("thinking_dili_ok"):
        s.append(f"thinking dili {c.get('thinking_dili')}")
    if c.get("forbidden_hits"):
        s.append(f"yasak ifade {sorted(c['forbidden_hits'])}")
    if not c.get("context_ok"):
        s.append(f"bağlam ({c.get('context_error')})")
    if not c.get("replay_ok"):
        s.append("replay system prompt")
    return " · ".join(s) or "?"


def main() -> int:
    sonuc = [_tara(p) for p in _kaynaklar()]
    toplam: dict[str, dict] = {}
    for o in sonuc:
        for ad, d in o["muafiyet"].items():
            t = toplam.setdefault(ad, {"kapsam": 0, "net": 0, "ornek": [], "kimlik": set()})
            t["kapsam"] += d["kapsam"]
            t["net"] += d["net"]
            t["kimlik"].update(d.get("id", []))
            t["ornek"] += d["ornek"][:3]
    # ⛔ AYNI KAYIT BİRÇOK SÜRÜM DOSYASINDA DURUYOR (`v5-parti5.v3`, `.v4`, `.v5` …)
    # ⇒ ham toplam sürüm sayısınca şişer. `v5-parti5`in 3 kaydı altı dosyada 18 kez
    # sayılıyordu. ➡️ *Bir korpusta «kaç kayıt» sorusunun cevabı, dosya satırlarını
    # toplamak değildir; kimlik tekilleştirmesi olmadan her sayı sürüm sayısıyla çarpılır.*
    for t in toplam.values():
        t["tekil"] = len(t["kimlik"])
        t["kimlik"] = sorted(t["kimlik"])[:12]

    sat = ["# Üretim kapısının muafiyetleri — `run_checks` neyi bağışlıyor?", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}", "",
           "⛔⛔ **Bu kapı ötekilerden başka.** T141/T144'te sayılan sekiz kapı ANALİZ aracı:",
           "bulgu üretir, kimseyi elemezler. `run_checks` ise `build.py`'nin elemesini",
           "belirler ⇒ **`datasets/` içine neyin gireceğine o karar veriyor.**", "",
           "⭐⭐ **Yöntem:** muafiyetin bedeli için ikinci bir karar kuralı YAZILMADI (K97).",
           "Kaydın kopyasında muafiyetin koşulu çevrildi ve `run_checks` **olduğu gibi**",
           "yeniden çağrıldı. ➡️ *Bir muafiyetin bedeli, kuralı yeniden yazarak değil,",
           "koşulu çevirip aynı kuralı yeniden koşarak ölçülür.*", "",
           "⭐ Yayımlanmış setler zaten kapıdan geçmiş kayıtlardan oluşuyor ⇒ **net bağış**,",
           "*«bu sette olup da muafiyet olmasa OLMAYACAK kayıt»* sayısıdır.", "",
           "## 1. ⭐ Toplam", "",
           "| muafiyet | kapsamdaki kayıt | net bağış (ham) | ⛔ **net (tekil kayıt)** | ne için |",
           "|---|---:|---:|---:|---|"]
    for ad, kapsamda, cevir, gerekce in MUAFIYETLER:
        t = toplam.get(ad, {"kapsam": 0, "net": 0, "tekil": 0})
        sat.append(f"| `{ad}` | {t['kapsam']} | {t['net']} | **{t.get('tekil', 0)}** | {gerekce} |")
    sat += ["", "⛔ **Ham sayı sürüm sayısınca şişer:** aynı kayıt `v5-parti5.jsonl`, `.v3`, "
            "`.v4`, `.v5`, `.arinmis`, `.blok1` dosyalarının hepsinde duruyor. ➡️ *Bir korpusta "
            "«kaç kayıt» sorusunun cevabı dosya satırlarını toplamak değildir.* ⇒ Karar için "
            "okunacak sütun **tekil kayıt**.", "",
            "⚠️ *«Net bağış»* **kusur sayısı değildir**: muafiyetlerin ikisi de ilan",
            "edilmiş ve gerekçeli. Ölçülen şey, gerekçenin **bedeli** — o gerekçe olmasa",
            "veri setinde olmayacak kayıt sayısı.", ""]

    sat += ["## 2. Dosya dosya", "",
            "| dosya | SHA256-16 | kayıt | geçen | replay muaf (net) | v2 muaf (net) |",
            "|---|---|---:|---:|---:|---:|"]
    for o in sorted(sonuc, key=lambda x: x["dosya"]):
        r_ = o["muafiyet"].get("replay_persona_muafiyeti", {})
        v_ = o["muafiyet"].get("uretim_v2_baglam_muafiyeti", {})
        if not (r_.get("kapsam") or v_.get("kapsam")):
            continue
        sat.append(f"| `{o['dosya']}` | `{o['sha256_16']}` | {o['kayit']} | {o['gecen']} | "
                   f"{r_.get('kapsam', 0)} ({r_.get('net', 0)}) | "
                   f"{v_.get('kapsam', 0)} ({v_.get('net', 0)}) |")
    sat.append("")

    sat += ["## 3. ⛔ Muafiyet olmasa ne düşerdi — örnekler", ""]
    for ad, *_ in [(m[0],) for m in MUAFIYETLER]:
        t = toplam.get(ad)
        if not t or not t["ornek"]:
            sat += [f"### `{ad}`", "", "⭐ Net bağış **0** — bu muafiyet bugün hiçbir kaydı "
                    "ayakta tutmuyor. ⚠️ Yine de bir tuzak teli: kapsamı boş değil, "
                    "yalnız bedeli sıfır.", ""]
            continue
        sat += [f"### `{ad}` — {t['net']} kayıt", "", "| kayıt | muafiyet olmasa düşme sebebi |",
                "|---|---|"]
        for e in t["ornek"][:12]:
            sat.append(f"| `{str(e['id'])[:12]}` | {e['sebep']} |")
        sat.append("")

    # ---- §4: sert kapının kendi kendine kapanması
    sur: dict[str, int] = {}
    pasaj: dict[str, tuple] = {}
    for p in _kaynaklar():
        for satir in p.read_text(encoding="utf-8").splitlines():
            if not satir.strip():
                continue
            r = json.loads(satir)
            pv = str((r.get("gen_meta") or {}).get("prompt_version", "—"))
            sur[pv] = sur.get(pv, 0) + 1
            n = uretim_surumu(r)
            if n is None or n < 4:
                continue
            for k in (r.get("context") or []):
                met = k.get("metin") or ""
                m = KLINIK_IDDIA.search(met)
                if m and met not in pasaj:
                    cum = next((x for x in re.split(r"(?<=[.!?])\s+", met)
                                if m.group(0) in x), met)
                    pasaj[met] = (m.group(0), cum.strip(), bool(OLUMSUZ.search(cum)))
    feragat = sum(1 for v in pasaj.values() if v[2])
    kapali = sum(v for k, v in sur.items()
                 if not str(k).startswith("uretim-v3"))   # ⚠️ kusur ANINDAKİ kapsam

    sat += ["## 4. ⛔⛔ SERT KAPI KENDİ KENDİNE KAPANMIŞTI — ve aynı gün düzeltildi", "",
            "⭐ **Durum:** kusur bulundu, iki parçalı düzeltme yazıldı ve ölçüldü "
            "(`reports/analiz/2026-09-18-7b-kapi-duzeltmesi.md`): desen denkliği 25454/25454, "
            "regresyon 12/12, **kararı dönen kayıt 0**. Aşağıdaki anlatı kusurun BULUNDUĞU "
            "ândaki durumu tarif eder; tablodaki *«açık/kapalı»* sütunu ise kapının **şu anki** "
            "koşulunu `checks.uretim_surumu`'ye sorarak yazılır.", "",
            "`run_checks` §7b'yi sert kapı yapan koşulu şöyle kuruyor:", "", "```python",
            'v3_ve_sonrasi = str(...prompt_version).startswith("uretim-v3")', "```", "",
            "⛔⛔ **Değişkenin adı `v3_ve_sonrasi`, yorumu *«uretim-v3 ve sonrası»*, ama kodu",
            "yalnız v3'ü tutuyor.** Üretim v4'e, sonra v5'e geçince kapı **kendiliğinden",
            "kapandı** ve bunu kimse görmedi: kapının kapanması bir hata vermez, yalnız",
            "eleme yapmamaya başlar.", "",
            "| prompt_version | kayıt | §7b sert kapı |", "|---|---:|---|"]
    for k, v in sorted(sur.items(), key=lambda x: -x[1]):
        acik = _sert({"gen_meta": {"prompt_version": k}})
        sat.append(f"| `{k}` | {v} | {'✅ açık' if acik else '⛔ kapalı'} |")
    sat += ["", f"➡️ Kusur bulunduğunda kapı **{kapali}** kayıtta kapalıydı.", "",
            "### ⭐⭐ Ama bedeli ölçülünce işaret TERS çıktı", "",
            f"v4/v5 adaylarında §7b-2'ye takılan **benzersiz pasaj: {len(pasaj)}** — ve",
            f"**{feragat}'sı aynı cümlede olumsuzlama taşıyor**, yani feragat cümlesi:", "",
            "| vuruş | cümle | feragat mi? |", "|---|---|---|"]
    for t, cum, fer in list(pasaj.values())[:10]:
        sat.append(f"| `{t}` | {cum[:100]} | {'⭐ evet' if fer else '⛔ hayır'} |")
    sat += ["", ("⭐⭐ **Gerçek ihlal: 0.** Kapı açık olsaydı bu pasajların hepsini elerdi — "
                 "üçü tam tersini söylüyor: *«Araç tanı koymaz»*. ➡️⭐⭐⭐ *Hatalı kod, "
                 "kazara doğru sonucu üretmiş: sürüm koşulu YANLIŞ ama kapının kendisi de "
                 "yanlış olduğu için kapalı olması veriyi korudu. «Doğru sonuç, doğru kural "
                 "demek değildir» bu kez ters yönden geçerli.*"
                 if feragat == len(pasaj) else
                 f"⛔⛔ **{len(pasaj)-feragat} pasajda olumsuzlama YOK — elle okunmalı.**"), "",
            "⚠️ **İddia dar tutulmalı:** *«gerçek ihlal 0»* demek, **bu kelime tarayıcısının**",
            "başka bir şey bulmadığı demektir. Kapı kapalıyken üretilen bir korpusta üretici",
            "bu kuraldan geri bildirim de almadı ⇒ *«korpus §7b açısından temiz»* DEĞİL,",
            "*«kapının kendi ölçütüyle görünen bir şey yok»*.", "",
            "### ⭐ Önerilen düzeltme ÇİFT parçalı — tek parçası zarar verir", "",
            "| parça | ölçülen etki |", "|---|---|",
            f"| (a) sürüm koşulu *«v3 ve sonrası»* olsun | tek başına: {feragat} doğru kayıt "
            "**yanlışlıkla düşer**, 0 ihlal yakalanır |",
            f"| (b) `KLINIK_IDDIA` aynı cümledeki olumsuzlamayı görsün | {feragat}/{len(pasaj)} "
            "yanlış pozitif kalkar |",
            "| (a) + (b) birlikte | kapı açılır, bilinen yanlış pozitif sınıfı kapanır, "
            "kayıp kayıt 0 |", "",
            "⛔⛔ **Değişiklik YAPILMADI.** `src/checks.py` `build.py`'nin elemesini belirler ⇒",
            "sert kapıyı açmak bir sonraki bütün derlemeleri etkiler ve (b) yeni bir sezgi",
            "getirir; sezginin kendi regresyon sınaması yazılmadan üretime girmemeli.", ""]

    hatalar = [h for o in sonuc for h in o.get("hata", [])]
    sat += ["## 5. ⛔ Bu raporun söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔ **§7b kapısı 4070 kayıtta kapalıydı** | düzeltilmedi; çift parçalı öneri "
            "ölçüldü ve yazıldı (§4) |",
            "| ⛔ **Yalnız iki muafiyet ölçüldü** | `run_checks` başka kararlar da veriyor "
            "(`rol_siniri` ve `yansitma_soru_orani` SERT KAPI DEĞİL, inceleme kuyruğuna "
            "gider) ⇒ bunlar bir muafiyet değil **tasarım**, ama bedelleri de ölçülmedi |",
            "| ⛔ **`thinking_dili` None muafiyeti** | thinking'i olmayan kayıtta dil kapısı "
            "hiç çalışmıyor; koşulu çevirmek anlamsız (dil yok) ⇒ sayılmadı |",
            "| ⚠️ **Koşul çevirmek yan etki yaratır** | `replay=False` yapmak `replay_ok`'u da "
            "etkiler; ölçülen şey *«BıRAG kaydı olsaydı geçer miydi»*, muafiyetin tek "
            "başına etkisi değil |",
            f"| {'⛔ **Ayrıştırılamayan kayıt**' if hatalar else '⭐ Hata yok'} | "
            f"{len(hatalar)} kayıt `run_checks` sırasında hata verdi"
            f"{': ' + ', '.join(hatalar[:4]) if hatalar else ''} |", ""]

    (KOK / f"reports/analiz/{TARIH}-uretim-kapisi-muafiyetleri.json").write_text(
        json.dumps({"tarih": TARIH, "toplam": toplam, "dosyalar": sonuc},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[:1] + sat[14:]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
