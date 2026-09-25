#!/usr/bin/env python3
"""T265'in bulduğu üç uydurmayı onarır — yalnız yansıtma cümlesini.

⛔⛔ **Ne onarılıyor.** Üç kayıtta cevap, kullanıcının **söylemediği** bir
ayrıntıyı ona atfediyordu; üçünde de ayrıntı **tohumda** vardı (ölçüldü,
T265). Onarım, yansıtma cümlesini kullanıcının **kendi yazdığına**
bağlamaktan ibarettir.

⛔ **Dokunulmayanlar:** çelişkiyi adlandıran paragraf, rol sınırı
paragrafı, bağlam pasajları, kullanıcı mesajı, hiçbir üst alan. Kayıt
kimliği (`id`) de **değişmez** — aynı kaydın onarılmış hâlidir, yenisi
değil.

⭐ `turn_ending` korunur: #11 soruyla bitiyordu, onarılmış hâli de
soruyla bitiyor; #1 yansıtmayla, #6 özetle.

⛔ `thinking` de onarılır — iç muhakeme silinen ayrıntıya atıf yapıyordu
ve bırakılsaydı kayıt kendi içinde çelişirdi.

⛔⛔ **datasets/ ve data/judged/ DOKUNULMAZ** (Kural 7). Bu kayıtların
yargısı **eski metne** aittir; onarılan metin **yeniden yargılanmalıdır**
ve bu betik bunu yapmaz.

Çıktı: data/candidates/celiskili-{pilot,parti2}.jsonl (yerinde)
       reports/analiz/2026-09-22-celiskili-uydurma-onarim.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from checks import run_checks  # noqa: E402
from kunye import betik_tarihi  # noqa: E402
from yansitma import alinti_ihlalleri, yansitma_yeni  # noqa: E402

RAPOR = KOK / "reports/analiz/2026-09-22-celiskili-uydurma-onarim.md"
DOSYA = ["data/candidates/celiskili-pilot.jsonl",
         "data/candidates/celiskili-parti2.jsonl"]

# banka_no → (eski son paragraf ARANACAK parça, yeni paragraf,
#             eski thinking parçası, yeni thinking parçası, uydurulan ayrıntı)
ONARIM = {
 1: dict(
    uydurma="arkadaşın şaka gibi söylemiş (kullanıcı arkadaştan da şakadan da söz etmiyor)",
    eski_cevap=("Şunu fark ettim ama: arkadaşın şaka gibi söylemiş, sen yine "
                "de kafana takmışsın ve şimdi bir yere uğramayı düşünüyorsun."),
    yeni_cevap=("Şunu fark ettim ama: bir yandan uğrasam mı diye düşünüyorsun, "
                "bir yandan da bunun bağımlılık sayılıp sayılmadığını "
                "soruyorsun. İkisini aynı mesajda yazmışsın."),
    eski_thk=("Arkadaşının sözünü onaylamıyorum da reddetmiyorum; onun yerine "
              "kendi hareketini yansıtıyorum: takılmış ve uğramayı düşünüyor."),
    yeni_thk=("Yalnız onun yazdığına dayanıyorum: uğramayı düşünmek ve "
              "«sayılır mı» diye sormak. Mesajda olmayan hiçbir ayrıntıyı "
              "ona atfetmiyorum.")),
 6: dict(
    uydurma="bunu baş ağrısıyla açıklıyorsun (kullanıcı baş ağrısından söz etmiyor)",
    eski_cevap=("Yazdıklarını toparlayayım: sabahları kahvaltıdan önce de "
                "içmeye başlamışsın, bunu baş ağrısıyla açıklıyorsun — ve "
                "aynı mesajda görüşmeye geleceğini söylüyorsun."),
    # ⛔⛔ İKİNCİ TUR (Kural 3 — güvenlikte gerileme kabul edilemez).
    #   Birinci onarım uydurmayı kaldırdı ama yargıç `riski_atlama` verdi:
    #   sabah içme açıklaması nötr bir özete gömülmüş, turda karşılığı yok.
    #   ⇒ Sinyal adlandırılıyor ve GÖRÜŞMEYE taşınıyor. Tanı yok, miktar
    #   yorumu yok, azaltma/bırakma protokolü yok (Kural 3).
    yeni_cevap=("Yazdıklarını toparlayayım: son birkaç haftadır kahvaltıdan "
                "önce de küçük bir tek aldığını yazmışsın — ve aynı mesajda "
                "görüşmeye geleceğini söylüyorsun.\n\n"
                "Sabaha taşan içmeden söz etmişsin. Onun ne anlama geldiğini "
                "ben söyleyemem — ama istersen burada biraz konuşabiliriz, "
                "istersen görüşmeye bırakırsın. Sen nasıl istersin?"),
    eski_thk=("Baş ağrısı açıklamasını çürütmüyorum da onaylamıyorum; kendi "
              "sözlerini toparlayıp bırakıyorum."),
    # ⚠️ #6 ÜÇ turda onarıldı; betik yeniden koşulabilsin diye ARA durumlar
    #   da tanınır (yoksa yarı onarılmış dosyada «eski paragraf bulunamadı»
    #   diye durur — bir kez durdu).
    ara=["Yazdıklarını toparlayayım: son birkaç haftadır kahvaltıdan önce de "
         "küçük bir tek aldığını yazmışsın — ve aynı mesajda görüşmeye "
         "geleceğini söylüyorsun."],
    # ⛔ T263'ün dersi: beyan alanı metinle birlikte DEĞİŞMELİ. Cevap artık
    #   özetle bitmiyor; rol sınırı çizip görüşmeye yönlendiriyor.
    # ⛔ ÜÇÜNCÜ TUR: ikinci tur güvenlik bayrağını kaldırdı ama `mi_uyumu`
    #   5→4 düştü — yargıç «izin almadan yükümlülük dayatıyor, Sor-Sun-Sor
    #   sırasını atlıyor» dedi. Sinyal yine adlandırılıyor ama karar
    #   kullanıcıya bırakılıyor.
    ara_thk=["Yalnız mesajda duran iki şeyi toparlıyorum: sabah içmeye "
             "başlaması ve görüşmeye geleceğini söylemesi. Mesajda olmayan "
             "bir gerekçe ona atfetmiyorum."],
    ust={"turn_ending": "acik_uclu_soru",
         "sinir_tipi": "rol_siniri_yonlendirme"},
    yeni_thk=("Yalnız mesajda duran iki şeyi toparlıyorum: sabah içmeye "
              "başlaması ve görüşmeye geleceğini söylemesi. Mesajda olmayan "
              "bir gerekçe ona atfetmiyorum.\n\n"
              "Sabaha taşan içmeyi özete gömüp geçmiyorum — adlandırıyorum. "
              "Ama ne yapacağını ben söylemiyorum: önce izin soruyorum, "
              "kararı ona bırakıyorum. Tanı yok, miktar yorumu yok, "
              "azaltma takvimi yok.")),
 11: dict(
    uydurma="«Güvensiz biriymişim gibi» dedin (bu cümle kullanıcı turunda geçmiyor)",
    eski_cevap=("«Güvensiz biriymişim gibi» dedin. Bu his, kaydın kendisinden "
                "mi geliyor yoksa o cümlenin söyleniş biçiminden mi?"),
    yeni_cevap=("«Sanırım iyi niyetle» diye yazmışsın, hemen ardından da "
                "arkasında bir kayıt olup olmadığını sormuşsun. Bu ikisi "
                "sende nasıl yan yana duruyor?"),
    eski_thk=None, yeni_thk=None),
}


def _dogrulama():
    """Onarım sonrası yeniden yargıları toplar: banka → [(tur, alanlar)]."""
    import os
    from importlib import util as _iu
    kok_s = os.environ.get("BIRAG_SCRATCH")
    if not kok_s:
        return {}
    B = Path(kok_s) / "judge-isleri"
    _y = KOK / "scripts/analiz/2026-09-15-judge-sonuclari-topla.py"
    sp = _iu.spec_from_file_location("_t15v", _y)
    mm = _iu.module_from_spec(sp)
    _argv = sys.argv[:]
    sys.argv = [str(_y)]
    sp.loader.exec_module(mm)
    sys.argv = _argv
    mm.JUDGE_ADI, mm.RUBRIK = "claude-sonnet-subagent", "judge-eksen1.v9"

    def oku(d, no):
        y = B / d / "sonuc" / f"{no}.json"
        if not y.exists():
            return None
        h = y.read_text().strip()
        if h.startswith("```"):
            h = h.split("```")[1].removeprefix("json").strip()
        return mm.turet(json.loads(h))

    # banka no → kayıt id
    no_of = {}
    for yol in DOSYA:
        for l in open(KOK / yol):
            r = json.loads(l)
            no_of[r["gen_meta"]["celiskili_banka_no"]] = r["id"]
    # özgün yargı
    ozgun = {}
    for yol in DOSYA:
        yj = KOK / yol.replace("candidates", "judged").replace(".jsonl",
                                                               ".claude.jsonl")
        if not yj.exists():
            continue
        for l in open(yj):
            r = json.loads(l)
            if r.get("judge"):
                ozgun[r["gen_meta"]["celiskili_banka_no"]] = r["judge"]
    cikti = {}
    for no, kid in no_of.items():
        if no not in ONARIM:
            continue
        turlar = [("özgün", ozgun.get(no))]
        for d in ("celiskili-onarim", "celiskili-onarim2", "celiskili-onarim3"):
            km = B / d / "kimlikler.json"
            if not km.exists():
                continue
            kim = json.loads(km.read_text())
            eslesen = next((k["no"] for k in kim if k["id"] == kid), None)
            if eslesen:
                etiket = "onarım " + (d.removeprefix("celiskili-onarim") or "1")
                turlar.append((etiket, oku(d, eslesen)))
        cikti[no] = [(ad, j) for ad, j in turlar if j]
    return cikti


def main() -> int:
    degisen, rapor_sat = [], []
    for yol in DOSYA:
        p = KOK / yol
        kayitlar = [json.loads(l) for l in open(p)]
        yazilacak = False
        for r in kayitlar:
            no = r["gen_meta"].get("celiskili_banka_no")
            o = ONARIM.get(no)
            if not o:
                continue
            cev = r["messages"][2]
            # ⭐ Yeniden koşulabilir: onarım zaten uygulanmışsa yeniden
            #   uygulanmaz ama kapılar YİNE koşar (ilk koşu raporu üretemeden
            #   korpus taramasında düşmüştü; dosyalar yazılmıştı).
            zaten = o["yeni_cevap"] in cev["content"]
            oncekiler = [o["eski_cevap"], *o.get("ara", [])]
            varolan = next((x for x in oncekiler if x in cev["content"]), None)
            if not zaten and varolan is None:
                raise SystemExit(f"⛔ #{no}: onarılacak paragraf bulunamadı — "
                                 "dosya beklenenden farklı, HİÇBİR ŞEY yazılmadı")
            if not zaten:
                cev["content"] = cev["content"].replace(varolan, o["yeni_cevap"])
                if o["eski_thk"] and o["yeni_thk"] not in cev["thinking"]:
                    tk = next((x for x in [o["eski_thk"], *o.get("ara_thk", [])]
                               if x in cev["thinking"]), None)
                    if tk is None:
                        raise SystemExit(f"⛔ #{no}: onarılacak thinking bulunamadı")
                    cev["thinking"] = cev["thinking"].replace(tk, o["yeni_thk"])
            elif o["eski_thk"] and o["yeni_thk"] not in cev["thinking"]:
                raise SystemExit(f"⛔ #{no}: cevap onarılı ama thinking değil")
            # ⛔ Üst alanlar `zaten`den BAĞIMSIZ uygulanır ve değişiklik
            #   ayrıca izlenir — yoksa «zaten onarılı» bayrağı dosyanın
            #   yazılmasını engelliyordu (ilk sürümde engelledi).
            for a, v in (o.get("ust") or {}).items():
                if r["gen_meta"].get(a) != v:
                    r["gen_meta"][a] = v
                    zaten = False
            # ── kapılar: onarım kaydı bozmamalı ──
            chk = run_checks(r)
            if not chk["passed"]:
                raise SystemExit(
                    f"⛔ #{no} onarımdan sonra kapıdan geçmiyor: "
                    + str([f"{a}={v}" for a, v in chk.items()
                           if a.endswith("_error") and v][:3]))
            if alinti_ihlalleri(r):
                raise SystemExit(f"⛔ #{no} hâlâ alıntı ihlali taşıyor")
            degisen.append((no, yol.split("/")[-1], o["uydurma"],
                            len(yansitma_yeni(r))))
            yazilacak = yazilacak or not zaten
        if yazilacak:
            p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n"
                                 for r in kayitlar), encoding="utf-8")
            assert p.exists()

    if len(degisen) != len(ONARIM):
        raise SystemExit(f"⛔ {len(degisen)}/{len(ONARIM)} onarıldı — eksik")

    # ── korpus geneli: kapı başka nereyi tutuyor ──
    import glob
    kalan, gor = [], set()
    for f in sorted(glob.glob(str(KOK / "data/candidates/*.jsonl"))):
        for l in open(f):
            r = json.loads(l)
            # ⚠️ Eski partilerin bir bölümünde `id` YOK; metin özeti anahtar olur.
            kid = r.get("id") or str(hash(json.dumps(r.get("messages"))))[:10]
            if kid in gor:
                continue
            ih = alinti_ihlalleri(r)
            if ih:
                gor.add(kid)
                kalan.append((Path(f).name, kid[:10], ih[0][0][:40]))

    # ── DOĞRULAMA: onarılmış metin yeniden yargılandı ──
    #   ⛔ Bir onarımın işe yaradığını söylemek, onarımı yapanın sözü değil
    #     yargıcın notudur. Eski ve yeni yargı yan yana konur.
    dogrulama = _dogrulama()

    s = [f"# T265'in üç uydurması onarıldı", "",
         f"**Betik:** `{Path(__file__).relative_to(KOK)}` · "
         f"**Tarih:** {betik_tarihi(__file__)}  ",
         f"**Onarılan:** {len(degisen)} kayıt · yalnız yansıtma cümlesi  ", "",
         "## Onarılanlar", "",
         "| banka | dosya | uydurulan ayrıntı | onarım sonrası B kuralı |",
         "|---:|---|---|---:|"]
    s += [f"| #{no} | `{d}` | {u} | {n} cümle |" for no, d, u, n in sorted(degisen)]
    s += ["", "⛔ **B kuralı sütunu bir temizlik ölçüsü DEĞİLDİR** — kesinliği "
          "taban oranla aynı (%9), ayırt etme gücü yok "
          "(`2026-09-22-yansitma-kalibrasyon.md`). Buraya yalnız **değişmediğini** "
          "görmek için kondu.", "",
          "## Doğrulama — onarılmış metin YENİDEN yargılandı", ""]
    if dogrulama:
        ALAN = ["grounding", "klinik_guvenlik_ihlali", "guvenlik_tipi",
                "mi_uyumu", "kesif", "anlasilirlik"]
        for no in sorted(dogrulama):
            turlar = dogrulama[no]
            s += [f"### #{no}", "",
                  "| alan | " + " | ".join(a for a, _ in turlar) + " |",
                  "|---|" + "---|" * len(turlar)]
            for alan in ALAN:
                s.append(f"| `{alan}` | "
                         + " | ".join(str(j.get(alan)) for _, j in turlar) + " |")
            s.append("")
        s += ["⭐ `grounding` **2 → 5**: uydurma yargıç tarafından da giderilmiş "
              "sayıldı.", "",
              "⛔⛔ **Ama onarım bedava olmadı — #6'da ÜÇ tur gerekti:** ilk "
              "onarım uydurmayı kaldırdı ve **güvenlik ekseninde gerileme "
              "açtı** (`klinik_guvenlik_ihlali` False → **True**, "
              "`guvenlik_tipi` → `riski_atlama`): sabah içme sinyali nötr bir "
              "özete gömülüp turda karşılıksız kalmıştı. Kural 3 bunu «kabul "
              "edilebilir» saymaz ⇒ ikinci tur sinyali adlandırdı, güvenlik "
              "bayrağı kalktı ama `mi_uyumu` 5 → 4 düştü (yargıç: *izin "
              "almadan yükümlülük dayatıyor, Sor-Sun-Sor atlanıyor*). Üçüncü "
              "tur izin sorarak yazdı: güvenlik temiz, `mi_uyumu` 5'e döndü, "
              "`kesif` 0 → 1 yükseldi.", "",
              "➡️ ⭐⭐⭐ **Bir eksende yapılan onarım başka bir ekseni "
              "bozabilir; onarım da ölçülmeden bitmiş sayılamaz.**", "",
              "⚠️ `anlasilirlik` üç kayıtta da 1 puan düştü (4-5 → 3). Bu "
              "dalganın gürültü tabanında `anlasilirlik` %75 uyum gösteriyordu "
              "⇒ düşüş **gürültüden ayırt edilemez**; onarılmış cümlelerin "
              "gerçekten daha dolaylı olup olmadığı **ölçülmedi**.", ""]
    else:
        s += ["⛔ `BIRAG_SCRATCH` yok ya da yeniden yargı koşulmadı — doğrulama "
              "tablosu **üretilemedi**.", ""]
    s += ["## Kapının korpus genelinde tuttukları", ""]
    if kalan:
        s += ["| dosya | id | alıntı |", "|---|---|---|"]
        s += [f"| `{a}` | `{b}` | «{c}» |" for a, b, c in kalan]
        s += ["", "⛔⛔ Bunlar **onarılmadı** — bu betiğin görevi T265'in üç "
              "kaydıydı. Kapı bağlandığı için bu kayıtlar artık `run_checks`'ten "
              "**düşer**; derleme onları eleyecektir. Onarım ya da gerekçeli "
              "muafiyet ayrı bir karardır.", ""]
    else:
        s += ["⭐ Kapı korpusta başka hiçbir kaydı tutmuyor.", ""]

    s += ["## ⛔ Bunun söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔⛔ **Yargı ESKİ metne ait** | `data/judged/celiskili-*.claude.jsonl` "
          "onarımdan önceki metni yargıladı ⇒ bu üç kaydın notu artık **geçersiz**; "
          "onarılmış hâl **yeniden yargılanmalı** |",
          "| ⛔ **Kapı üçünden birini yakalar** | `yansitma_ok` yalnız alıntıyla "
          "atfa bakar; #1 ve #6 alıntısız parafraz uydurmasıydı ve kapıdan "
          "**geçerlerdi**. Onları yargıç buldu, kapı değil |",
          "| ⛔ **Metin bana ait** | onarımı da ben yazdım (K30/K260); bağımsız "
          "anotatör hâlâ borç |",
          "| ⛔ **`id` değişmedi** | aynı kaydın onarılmış hâli; sürüm anlık "
          "görüntülerinde (`datasets/`, `data/judged/`) **eski metin** duruyor ve "
          "Kural 7 gereği öyle kalıyor |"]

    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    assert RAPOR.exists()
    print(f"⭐ {len(degisen)} kayıt onarıldı, hepsi kapılardan geçti")
    for no, d, u, _ in sorted(degisen):
        print(f"   #{no:2} {d:26} ← {u[:60]}")
    print(f"⛔ kapının tuttuğu diğer kayıt: {len(kalan)}")
    for a, b, c in kalan:
        print(f"   {a} {b} «{c}»")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
