#!/usr/bin/env python3
"""Korpus koşusu (v8 + v9): sonuçları toplar, türetir, v7 ile karşılaştırır, raporlar.

Tasarım (koşudan ÖNCE): reports/analiz/2026-09-15-korpus-v9-tasarim.md — Ö1-Ö7.

⚠️ Türetme AYRIMI önemli:
  · v8 kayıtları **kaynaksız** türetilir — v8'in anlambilimi budur ve v9 kodunun
    kaynaksız çağrıda v8 koduyla birebir aynı davrandığı sınamada kanıtlandı.
  · v9 kayıtları **kaynaklı** türetilir; kapı ancak öyle çalışır.

Kullanım: uv run python scripts/analiz/2026-09-15-korpus-v9-raporu.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import statistics as st
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402
from schemas import JudgeResult  # noqa: E402

_sp = _iu.spec_from_file_location("kp", KOK / "scripts/analiz/2026-09-15-korpus-v9-plan.py")
PLAN = _iu.module_from_spec(_sp)
_sp.loader.exec_module(PLAN)
_sp2 = _iu.spec_from_file_location("kd", KOK / "scripts/analiz/2026-09-15-v9-kapi-denetimi.py")
KD = _iu.module_from_spec(_sp2)
_sp2.loader.exec_module(KD)

ISLER = Path("/private/tmp/claude-501/-Users-pc-projects-birag-data-finetuning"
             "/fe6477c2-8e5e-439e-875d-df2b5ed62d91/scratchpad/judge-isleri")
HEDEF = KOK / "reports/analiz/korpus-v9"
CIKTI = KOK / "reports/analiz/2026-09-15-korpus-v9-kosusu.md"
DOKUM = HEDEF / "alinti-dogrulanmadi.json"
V7 = [KOK / "data/judged/v3-kumulatif.v7.jsonl",
      KOK / "data/judged/v3-kumulatif.v7-kontrol.jsonl",
      KOK / "data/judged/v3-kumulatif.v7-ucuncu.jsonl"]

BAYRAK = ["rol_siniri_ihlali", "klinik_guvenlik_ihlali", "bos_guvence",
          "tuzak_suclama", "tuzak_etiketleme"]
PUAN = ["anlasilirlik", "dogallik", "mi_uyumu", "grounding"]
DOKUNULMAYAN = ["anlasilirlik_holistik", "dogallik_holistik", "mi_uyumu_holistik",
                "duygusal_tepki", "yorumlama", "kesif"]
V9_KALKAN = ["teselli_ozgu_oge", "teselli_kalip", "teselli_kullanici_alintisi",
             "kurum_adi_kullanicidan"]
JUDGE_ADI = "claude-sonnet-subagent"


def turet(data: dict, surum: str, kaynak: dict | None) -> dict:
    data["judge_model"] = JUDGE_ADI
    data["prompt_version"] = f"judge-eksen1.{surum}"
    f.f_bolumu_turet(data, kaynak)
    for alan, hesap in (("anlasilirlik", f.anlasilirlik_hesapla),
                        ("dogallik", f.dogallik_hesapla),
                        ("mi_uyumu", f.mi_uyumu_hesapla)):
        d = hesap(data)
        if d is not None:
            data[alan] = d
    if any(k in data for k in f.TUZAKLAR):
        data["tuzak_ihlali"] = [ad for k, ad in f.TUZAKLAR.items() if data.get(k) is True]
    return JudgeResult(**data).model_dump()


def takas_oku(ad: str) -> dict:
    """Bildirilmiş sonuç-dosyası takasları: `no` → gerçekte o kayda ait `no`.

    ⛔ 2026-09-15: `korpus-v8`'de 075 ile 077'nin sonuçları karşılıklı yer değiştirmiş
    (geriye dönük eşleşme denetimi buldu). İş dosyaları DOĞRUYDU; kusur yazma
    adımında — `korpus-v9-p2` ile aynı sınıf (K123).

    ⭐ Ham arşive DOKUNULMUYOR: arşivin işi «subagent o dosyaya ne yazdı»yı saklamak
    ve `2026-09-15-geriye-donuk-eslesme.md` onun SHA256'sını taşıyor. Düzeltme bu
    yüzden ayrı bir bildirim dosyasında duruyor ve okuma anında uygulanıyor.
    """
    y = KOK / "reports/analiz/ham-judge" / f"{ad}.takas.json"
    if not y.exists():
        return {}
    h = {}
    for a, b in json.loads(y.read_text())["takas"]:
        h[a], h[b] = b, a
    return h


def oku(ad: str, surum: str, kaynaklar: dict | None) -> tuple[dict, list, list, dict]:
    d = ISLER / ad
    takas = takas_oku(ad)
    sonuc, eksik, bozuk, fazla = {}, [], [], {}
    for k in json.loads((d / "kimlikler.json").read_text()):
        y = d / "sonuc" / f"{takas.get(k['no'], k['no'])}.json"
        if not y.exists():
            eksik.append(k["no"]); continue
        try:
            ham = y.read_text().strip()
            if ham.startswith("```"):
                ham = ham.split("```")[1].removeprefix("json").strip()
            ham_d = json.loads(ham)
            if surum == "v9":
                fazla[k["id"]] = [a for a in V9_KALKAN if a in ham_d]
            kyn = kaynaklar[k["id"]] if kaynaklar is not None else None
            sonuc[k["id"]] = turet(ham_d, surum, kyn)
        except Exception as e:
            bozuk.append((k["no"], f"{type(e).__name__}: {e}"[:120]))
    return sonuc, eksik, bozuk, fazla


def main() -> int:
    HEDEF.mkdir(parents=True, exist_ok=True)
    korpus = {r["id"]: r for r in
              (json.loads(l) for l in PLAN.KORPUS.open(encoding="utf-8"))}
    kaynaklar = {i: f.kaynak_metinleri(r) for i, r in korpus.items()}
    baglamli = {i for i, r in korpus.items() if r.get("context")}
    turlu = {i for i, r in korpus.items()
             if sum(1 for m in r["messages"] if m["role"] == "assistant") > 1}

    v7g = []
    for p in V7:
        v7g.append({r["id"]: r["judge"] for r in
                    (json.loads(l) for l in p.open(encoding="utf-8")) if r.get("judge")})
    v8, e8, b8, _ = oku("korpus-v8", "v8", None)
    v9, e9, b9, fazla = oku("korpus-v9", "v9", kaynaklar)
    p2, _, bp2, _ = oku("korpus-v9-p2", "v9", kaynaklar)
    p3, _, bp3, _ = oku("korpus-v9-p3", "v9", kaynaklar)

    # ⛔ EŞLEŞME KAPISI — 2026-09-15 olayı. Bir subagent doğru iş dosyalarını okuyup
    # sonuçları YANLIŞ çıktı dosyalarına yazmıştı (korpus-v9-p2, 004→005→006→007→004)
    # ve dört kaydın judge çıktısı başka kayda ait olmuştu. Hiçbir şey hata vermedi;
    # gürültü tabanı o kayıtlarla hesaplandı. Artık rapor bu kapıdan geçmeden yazılmaz.
    # ⚠️ `korpus-v8` İLK SÜRÜMDE BU LİSTEDE YOKTU ve içindeki takas tam da bu yüzden
    # görünmedi: kapı yalnızca v9 dosyalarına bakıyordu (K124).
    # Bir kapı, raporun OKUDUĞU her arşivi kapsamazsa kapı değildir.
    kayma = []
    for ad in ("korpus-v8", "korpus-v9", "korpus-v9-p2", "korpus-v9-p3"):
        yol = KOK / "reports/analiz/ham-judge" / f"{ad}.jsonl"
        if not yol.exists():
            continue
        takas = takas_oku(ad)
        kayitlar = None
        if takas:
            ham = {r["no"]: r for r in
                   (json.loads(l) for l in yol.open(encoding="utf-8"))}
            kayitlar = [{**r, "ham": ham[takas.get(no, no)]["ham"]}
                        for no, r in ham.items()]
        kayma += KD.eslesme_denetimi(yol, kaynaklar, lambda r: r["id"], kayitlar)
    if kayma:
        print(f"⛔ SONUÇ ↔ KAYIT EŞLEŞMESİ KAYMIŞ ({len(kayma)}) — rapor yazılmadı:")
        for k in kayma:
            print(f"   · {k['dosya']} no={k['no']} kayıt={k['kayit'][:10]} "
                  f"kendi {k['kendi']}/{k['alinti']} · ait olduğu {k['ait_oldugu'][:10]}")
        return 1

    def bayrak_kume(j: dict | None) -> frozenset:
        return frozenset(a for a in BAYRAK if (j or {}).get(a) is True)

    # ── v7 nihai (k=3 çoğunluk) ───────────────────────────────────────────
    v7n = {}
    for i in korpus:
        oy = [bayrak_kume(g.get(i)) for g in v7g if g.get(i)]
        v7n[i] = frozenset(a for a in BAYRAK if sum(a in o for o in oy) > len(oy) / 2)

    # ── Ö3 — v9'un yansız gürültü tabanı ──────────────────────────────────
    kontrol = PLAN.kontrol_kumesi(list(korpus))
    bol = cift = ciftn = 0
    for i in kontrol:
        oy = [bayrak_kume(g.get(i)) for g in (v9, p2, p3) if g.get(i)]
        if len(set(oy)) > 1:
            bol += 1
        for a in range(len(oy)):
            for b in range(a + 1, len(oy)):
                ciftn += 1
                if oy[a] != oy[b]:
                    cift += 1
    taban = cift / max(ciftn, 1) * 100
    # v7'nin kendi tabanı — üç geçişten, AYNI ölçüyle
    c7 = n7 = 0
    for i in korpus:
        oy = [bayrak_kume(g.get(i)) for g in v7g if g.get(i)]
        for a in range(len(oy)):
            for b in range(a + 1, len(oy)):
                n7 += 1
                if oy[a] != oy[b]:
                    c7 += 1
    taban7 = c7 / max(n7, 1) * 100

    # ── Ö1 — Eksen 2'nin uyaramadığı iki yol ──────────────────────────────
    baglam_uyarildi = sum(1 for i in baglamli if f._f_dolu(v9.get(i) or {}, "rol_baglam_alintisi")
                          or f._f_dolu(v9.get(i) or {}, "yordam_baglam_alintisi"))
    dayanak_var = {i for i in korpus
                   if f._f_dolu(v9.get(i) or {}, "teselli_dayanak_alintisi")}
    # dayanak asistanın ÖNCEKİ turundan mı geliyor (kod ayırt etti mi)
    asistandan = 0
    for i in dayanak_var:
        j = v9[i]
        q = f.alinti_nrm(j.get("teselli_dayanak_alintisi"))
        k = kaynaklar[i]
        if q and q in k["konusma"] and q not in k["kullanici"]:
            asistandan += 1
    turlu_dayanak = len(dayanak_var & turlu)

    # ── Ö2 — atıf (v8 → v9) ───────────────────────────────────────────────
    atif, atif_ornek = collections.Counter(), []
    degisen78 = degisen89 = 0
    for i in korpus:
        s7, s8, s9 = v7n[i], bayrak_kume(v8.get(i)), bayrak_kume(v9.get(i))
        if s7 != s8:
            degisen78 += 1
        if s8 != s9:
            degisen89 += 1
            j9, j8 = v9.get(i) or {}, v8.get(i) or {}
            dn = j9.get("alinti_dogrulanmadi") or []
            dayanak = (j9.get("teselli_dayanak_alintisi") or "YOK").strip().upper()
            v8_alinti = (j8.get("teselli_kullanici_alintisi") or "YOK").strip().upper()
            v8_vekil = (j8.get("teselli_kalip") is False
                        or f._f_dolu(j8, "teselli_ozgu_oge"))
            fark = s8 ^ s9
            if dn:
                k = ("kod kapısı: kapsam" if any(x.endswith(":ic_muhakeme") for x in dn)
                     else "kod kapısı: alıntı doğrulanamadı")
            elif "bos_guvence" in fark and "bos_guvence" in s9 and v8_vekil \
                    and dayanak in ("YOK", "YOK."):
                k = "rubrik: F6 — v8'in vekil muafiyeti kalktı"
            elif "bos_guvence" in fark and "bos_guvence" in s8 \
                    and dayanak not in ("YOK", "YOK.") and v8_alinti in ("YOK", "YOK."):
                k = "rubrik: F6 — v9 dayanağı buldu"
            else:
                k = "⛔ ATFEDİLEMEZ"
                if len(atif_ornek) < 12:
                    atif_ornek.append((i[:8], sorted(s8), sorted(s9)))
            atif[k] += 1

    # ── Ö5 — döküm + kaç alıntı DENETLENDİ ────────────────────────────────
    ALINTI_ALAN = ["en_belirsiz_cumle", "en_somut_ayrinti", "rol_sinirina_en_yakin",
                   "rol_iddiasi", "guvenlige_en_yakin", "kisiye_dair_en_genel",
                   "sorumluluga_en_yakin", "en_teselli_edici", "teselli_dayanak_alintisi",
                   "kurum_yordam_en_yakin", "kurum_adi", "yordam_iddiasi",
                   "rol_baglam_alintisi", "yordam_baglam_alintisi"]
    denetlenen = sum(1 for j in v9.values() for a in ALINTI_ALAN if f._f_dolu(j, a))
    # ⚠️ BÜTÜN geçişlerden. İlk sürümde yalnızca aşama 1 sayılıyordu ve hakemlik
    # geçişlerindeki ateşlemeler rapora hiç girmiyordu — 2026-09-15 olayı böyle gizlendi.
    dokum = []
    for gecis, g in (("v9", v9), ("p2", p2), ("p3", p3)):
        for i, j in g.items():
            for x in (j.get("alinti_dogrulanmadi") or []):
                alan, sebep = x.split(":")
                dokum.append({"gecis": gecis, "id": i, "alan": alan, "sebep": sebep,
                              "alinti": j.get(alan)})
    DOKUM.write_text(json.dumps(dokum, ensure_ascii=False, indent=1))

    # ── Kayıt dosyası ─────────────────────────────────────────────────────
    with (HEDEF / "sonuclar.jsonl").open("w") as fh:
        for i in korpus:
            fh.write(json.dumps({
                "id": i, "baglamli": i in baglamli, "cok_turlu": i in turlu,
                "v7_nihai": sorted(v7n[i]), "v8": sorted(bayrak_kume(v8.get(i))),
                "v9": sorted(bayrak_kume(v9.get(i))),
                "v9_izler": {"alinti_dogrulama": (v9.get(i) or {}).get("alinti_dogrulama"),
                             "alinti_dogrulanmadi": (v9.get(i) or {}).get("alinti_dogrulanmadi"),
                             "teselli_dayanak_dogrulandi": (v9.get(i) or {}).get("teselli_dayanak_dogrulandi")},
                "judge_v8": v8.get(i), "judge_v9": v9.get(i),
            }, ensure_ascii=False) + "\n")

    # ── Rapor ─────────────────────────────────────────────────────────────
    def say(g, a):
        return sum(1 for i in korpus if a in bayrak_kume(g.get(i)))
    n = len(korpus)
    kaynakli = sum(1 for j in v9.values() if j.get("alinti_dogrulama") == "yapildi")
    sha9 = hashlib.sha256((KOK / "prompts/judge-eksen1.v9.md").read_bytes()).hexdigest()
    y = [
        "# Korpus koşusu — v9'un iki mekanizması İLK KEZ uyarılabildi",
        "",
        f"*2026-09-15 · betik `scripts/analiz/{Path(__file__).name}`*",
        f"*korpus `data/candidates/v3-kumulatif.jsonl` SHA256 "
        f"`{hashlib.sha256(PLAN.KORPUS.read_bytes()).hexdigest()[:16]}` · {n} kayıt*",
        f"*rubrik v9 SHA256 `{sha9[:16]}` · judge **{JUDGE_ADI}** (v7/v8 ile aynı aile)*",
        "*tasarım `reports/analiz/2026-09-15-korpus-v9-tasarim.md` — Ö1-Ö7 koşudan önce*",
        "",
        "## Küme",
        "",
        "| | |",
        "|---|---|",
        f"| kayıt | {n} |",
        f"| v7 | arşivli, **üç geçiş** (K106) |",
        f"| v8 | bu koşuda, k=1 — **korpusta ilk kez** |",
        f"| v9 | bu koşuda, k=1 + {len(kontrol)} kayıtta k=3 |",
        f"| kuyruk | v8 ↔ v9 baytı baytına aynı; render v7 commit'iyle **kod olarak** özdeş |",
        f"| doğrulama | **{kaynakli}/{len(v9)}** kayıtta kaynaklı |",
        "",
        "⛔ **v8 de koşuldu** çünkü korpusta hiç koşmamıştı; yalnızca v9 koşulsaydı",
        "v7→v9 farkı iki sürümü birden taşır ve hiçbir kaleme atfedilemezdi.",
        "⚠️ v8'e ayrı gürültü tabanı koşulmadı (köprü rolünde) — **v8'e ait farklar tek",
        "tek okunamaz**.",
        "",
        "## ⭐ Ö1 — Eksen 2'nin uyaramadığı iki yol",
        "",
        "| yol | korpusta kayıt | v9'da uyarıldı |",
        "|---|---:|---:|",
        f"| `context` taşıyan (bağlam kaçışı alıntısı) | {len(baglamli)} | **{baglam_uyarildi}** |",
        f"| çok turlu (dayanağın turu kodca bulunur) | {len(turlu)} | **{turlu_dayanak}** |",
        f"| dayanak KULLANICI turunda değil, BıRAG'ın turunda | — | **{asistandan}** |",
        "",
        f"Toplam `teselli_dayanak_alintisi` yazılan kayıt: **{len(dayanak_var)}**/{n}.",
        "",
        f"⭐ Bağlam kaçışı alıntısı **{baglam_uyarildi}** kez yazıldı — Eksen 2'de bu yol "
        "hiç uyarılamıyordu (orada bağlam belgesi taşıyan öğe yok).",
        "",
        "⛔ **Ama mekanizmanın YARISI hâlâ uyarılmadı:** dayanağın **kimin turundan** "
        f"geldiğini kodun ayırt etmesi gerekiyordu; {len(dayanak_var)} dayanaktan "
        f"**{asistandan} tanesi** BıRAG'ın kendi turundan geldi. Yani *«kod turu bulur»* "
        "kararı hiçbir vakada sonucu **değiştirmedi** — çok turlu 32 kayıtta bile "
        "judge'ların bulduğu dayanak hep kullanıcının sözüydü. ⚠️ v9'un bu parçası "
        "iki koşudur **sınanmamış** durumda.",
        "",
        "## Ö3 — gürültü tabanı",
        "",
        "| küme | ikili uyuşmazlık | oran |",
        "|---|---:|---:|",
        f"| **v9**, tohumla çekilmiş {len(kontrol)} kayıt | {cift}/{ciftn} | **%{taban:.0f}** |",
        f"| v7, üç geçiş, {n} kayıt (arşiv) | {c7}/{n7} | **%{taban7:.0f}** |",
        "",
        f"⚠️ Bayrak kümesi değişimi {n} kayıtta gürültüyle bile "
        f"**~{n * taban / 100:.0f} kayıt** demektir. Bundan küçük farklar okunamaz.",
        "",
        "## Ö4 — bayraklar: v7 → v8 → v9",
        "",
        "| bayrak | v7 (k=3) | v8 | v9 |",
        "|---|---:|---:|---:|",
    ]
    for a in BAYRAK:
        y.append(f"| `{a}` | {sum(1 for i in korpus if a in v7n[i])} | "
                 f"{say(v8, a)} | **{say(v9, a)}** |")
    y += [
        "",
        f"Bayrak kümesi değişen kayıt: **v7→v8 {degisen78}** · **v8→v9 {degisen89}** (n={n}).",
        "",
        f"⛔ **İKİSİ DE GÜRÜLTÜ BANDININ İÇİNDE.** Taban %{taban:.0f}, yani {n} kayıtta "
        f"tek başına ~{n * taban / 100:.0f} kayıtlık değişim bekleniyor; ölçülen "
        f"{degisen78} ve {degisen89}. ➡️ *«v9 korpus kararlarını şu kadar değiştirdi»* "
        "cümlesi **kurulamaz**. Kurulabilen tek şey: `bos_guvence` dışındaki dört "
        "bayrak korpusta zaten **hiç ya da neredeyse hiç** ateşlemiyor.",
        "",
        "⭐⭐ **YÖN, EKSEN 2'DEKİNİN TERSİ.** Eksen 2'de v9 `bos_guvence`'i her kolda "
        f"**düşürmüştü** (10→8, 12→9, …); korpusta **yükseltiyor** ({say(v8, 'bos_guvence')}→"
        f"{say(v9, 'bos_guvence')}). Sebep atıf tablosunda görünüyor: korpusta v8'in "
        "**vekil muafiyeti kalkan** kayıtlar (8), v9'un **dayanağı bulduğu** kayıtlardan (3) "
        "fazla; Eksen 2'de denge tersineydi. ➡️ *v9 «daha sıkı» ya da «daha gevşek» bir "
        "rubrik değil: bir VEKİLİ (kalıp) doğrulanabilir bir sınamayla değiştiriyor ve net "
        "yön, vekilin o veri kümesinde ne sıklıkta ateşlediğine bağlı.* ⚠️ Bu, tek bir veri "
        "kümesinde ölçülen rubrik etkisinin başka kümeye taşınamayacağı anlamına geliyor.",
        "",
        "## Ö2 — v8 → v9 değişimleri atfedilebiliyor mu",
        "",
        "| kaynak | kayıt |",
        "|---|---:|",
    ]
    for k, v in atif.most_common():
        y.append(f"| {k} | {v} |")
    atfedilen = sum(atif.values()) - atif["⛔ ATFEDİLEMEZ"]
    y += [
        f"| **toplam** | **{sum(atif.values())}** |",
        "",
        f"**{atfedilen}/{sum(atif.values())} değişim bir v9 mekanizmasına bağlanabiliyor.**",
    ]
    if atif_ornek:
        y += ["", "Atfedilemeyenler:", "", "| kayıt | v8 | v9 |", "|---|---|---|"]
        for i, a, b in atif_ornek:
            y.append(f"| `{i}` | `{a}` | `{b}` |")
    y += [
        "",
        "## Ö5 — doğrulayıcının kendi hata oranı",
        "",
        f"**Doğrulanamayan alıntı: {len(dokum)}** "
        f"(aşama 1 + iki hakemlik geçişi, {len(v9) + len(p2) + len(p3)} judge kararı).",
    ]
    if dokum:
        y += ["", "| kayıt | alan | sebep | alıntı |", "|---|---|---|---|"]
        for d in dokum[:20]:
            y.append(f"| `{d['gecis']}/{d['id'][:8]}` | `{d['alan']}` | `{d['sebep']}` | "
                     f"*«{(d['alinti'] or '')[:60]}»* |")
        y += ["", "⚠️ Bu kayıtlar **elle okunmalı**: *«judge uydurdu»* ile *«eşleştirici "
              f"bulamadı»* ayrılmalı. Döküm: `{DOKUM.relative_to(KOK)}`"]
    else:
        y += ["",
              f"Bu koşuda denetlenen alıntı: **{denetlenen}** (v9, {n} kayıt).",
              "",
              "⭐ Eksen 2'deki sonucun tekrarı: yanlış negatif yok — eşleştiricinin "
              "katılığı burada da kimseye zarar vermedi, üstelik **bağlam belgesinden** "
              f"yapılan {baglam_uyarildi} alıntı da kaynakta bulundu.",
              "",
              "⛔ **Ama aynı sayı, kod kapısının İKİNCİ KEZ hiç ateşlemediğini söylüyor.** "
              "Eksen 2'de bunun sebebi bağlam belgesi olmamasıydı; korpusta bağlam var ve "
              "kapı yine boşta kaldı. ➡️ İki koşu, iki veri kümesi, **sıfır ateşleme**. "
              "v9'un doğrulama kapısı hâlâ yalnızca 18 kapı vakasında sınanmış durumda ve "
              "*«çalışıyor»* denemez — denebilecek şey, **varlığının davranışı değiştirdiği** "
              "(T46)."]
    y += [
        "",
        "## Ö6 — maliyet",
        "",
        "| Denetim | v8 | v9 |",
        "|---|---:|---:|",
        f"| bozuk JSON | {len(b8)} | {len(b9)} |",
        f"| eksik sonuç | {len(e8)} | {len(e9)} |",
        f"| v9'da kalkan alanı yine de yazan kayıt | — | {sum(1 for v in fazla.values() if v)} |",
        f"| hakemlik geçişlerinde bozuk | — | {len(bp2) + len(bp3)} |",
        "",
        "## Ö7 — dokunulmayan boyutlar",
        "",
        "v9 Bölüm A-E'ye ve F1/F3/F4/F5'e dokunmadı. Ortalama:",
        "",
        "| boyut | v7 (1. geçiş) | v8 | v9 |",
        "|---|---:|---:|---:|",
    ]
    for a in DOKUNULMAYAN + PUAN:
        def ort(g):
            v = [(g.get(i) or {}).get(a) for i in korpus]
            v = [x for x in v if isinstance(x, (int, float))]
            return f"{st.mean(v):.2f}" if v else "—"
        y.append(f"| `{a}` | {ort(v7g[0])} | {ort(v8)} | {ort(v9)} |")
    y += [
        "",
        "⚠️ Buradaki kayma **rubriğe delil değildir**: v7'nin kendi kontrol koşusu bu",
        "boyutlarda rubrik etkisinden büyük kayma üretmişti (K61).",
        "",
        "## ⛔ Bu koşunun ölçmediği",
        "",
        "- **Judge ailesi sapması (K45).** Korpusu Claude yazdı, judge da Claude ailesi.",
        "- **Kriz davranışı.** Korpusta kriz kaydı yok (Kural 3); F2/F7 zayıf uyarılır.",
        "- **v8'e ait farkların tek tek okunması** — v8'in kendi tabanı ölçülmedi.",
        "- **Uzman uyumu** (K27).",
    ]
    CIKTI.write_text("\n".join(y) + "\n", encoding="utf-8")
    print(f"✅ {CIKTI.relative_to(KOK)}")
    print(f"   v8 {len(v8)} · v9 {len(v9)} · p2 {len(p2)} · p3 {len(p3)}")
    print(f"   Ö1 bağlam {baglam_uyarildi}/{len(baglamli)} · çok turlu dayanak "
          f"{turlu_dayanak}/{len(turlu)} · asistan turundan {asistandan}")
    print(f"   taban v9 %{taban:.0f} (v7 %{taban7:.0f}) · atıf {atfedilen}/{sum(atif.values())}")
    print(f"   doğrulanamayan alıntı {len(dokum)} · bozuk {len(b8)}+{len(b9)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
