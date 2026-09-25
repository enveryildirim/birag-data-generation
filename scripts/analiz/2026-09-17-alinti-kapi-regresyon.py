#!/usr/bin/env python3
"""Alıntı birebirlik kapısı — düzeltmeden sonra HÂLÂ yakalıyor mu?

⛔⛔ **Neden var.** Bu oturumda bir kapı düzeltmesi, kusurun ZATEN onarılmış
olduğu bir dosyada «doğrulanmıştı» — yani hiçbir şey doğrulanmamıştı. Bir kapı
GEVŞETİLDİĞİNDE (burada iki muafiyet ayrıldı, bir desen daraltıldı) sorulacak
soru *«yeni hâli sessiz mi»* değil, **«eski yakaladıklarını hâlâ yakalıyor mu»**dur.

Vakalar elle yazıldı ve her biri bir KARAR'ı sınar; beklenen sonuç satırda yazılı.
⭐ 5. vaka düzeltmenin kendi gerekçesidir: eski kapı onu KAÇIRIYORDU.
⭐ 6. vaka eşleme düzeltmesinin gerekçesidir: kısa alıntı, sonrakini kaydırıyordu.

Kullanım: uv run python scripts/analiz/2026-09-17-alinti-kapi-regresyon.py
"""
from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "scripts/analiz"))
import _muafiyet as MUAF  # noqa: E402

_s = importlib.util.spec_from_file_location(
    "alinti", KOK / "scripts/analiz/2026-09-17-alinti-birebirlik-kapisi.py")
KAPI = importlib.util.module_from_spec(_s)
_s.loader.exec_module(KAPI)

# (ad, kullanıcı metni, cevap, beklenen bulgu sayısı, beklenen muafiyet adı)
VAKA = [
    ("temel yakalama — olumlu atıf, cümlede mastar yok",
     "Sabahları eller titriyor, hekime gitsem mi bilmiyorum.",
     'Sen "belki abartıyorum" dedin ve bu cümle kendi başına bir şey taşıyor.',
     1, None),
    ("gerçek karşı olgusal",
     "Masada içiyorlardı, ben de içtim.",
     '"Masada içiyorlardı" dedin, "bana verdiler" demedin.',
     0, "karsi_olgusal"),
    ("anma çerçevesi",
     "Bir şeyim yok diyorum ama içimden değil.",
     'Bunu sormak, "içimden gelmiyor" demekten farklı bir yerden geliyor.',
     0, "anma_oneri"),
    ("öneri çerçevesi",
     "Vizitte kimseyle konuşamıyorum.",
     'İlk adım, yarın vizitte "konuşabileceğim biri var mı" diye sormak olabilir.',
     0, "anma_oneri"),
    ("⭐ ESKİ KAPININ KAÇIRDIĞI — alakasız mastar muafiyeti ateşliyordu",
     "Sabahları eller titriyor.",
     'Hekime "belki abartıyorum" dediğin şeyi olduğu gibi anlatmak en yakın adım.',
     1, None),
    ("⭐ EŞLEME — kısa alıntı sonrakini kaydırıyordu",
     "Akşamları bira içiyorum, dersler aksıyor.",
     'Hiçbir şey söylemeyeceğim — ne "az" ne "çok". Sen "her akşam kustum" dedin.',
     1, None),
    ("⭐ ADFİİL + İYELİK — olumsuzluk değil (`söylemen` = «senin söylemen»)",
     "Sabahları eller titriyor.",
     'Hekime "belki abartıyorum" dediğin şeyi olduğu gibi söylemen bir adım olabilir.',
     1, None),
    ("⭐ EŞGÜDÜMLÜ ANMA — araya bağlaçlı ikinci alıntı giriyor",
     "Üç gecedir yarım tane alıp uyuyabiliyorum, doktora sormam lazım biliyorum.",
     'Senin yerine "devam et" ya da "bırak" demek bana düşmez; o karar senin.',
     0, "anma_oneri"),
    ("⭐ OLUMSUZ YETERLİLİK — «diyemem» (de- → di- ses değişimi)",
     "Haftalık kutusu yeter bence, öyle yapayım.",
     'Bunu anlıyorum. "Yeter bence" dediğin plana ben "olur" diyemem.',
     0, "olumsuz_yeterlilik"),
    ("⭐ ULAÇ ÇERÇEVESİ — «diyerek … almayacağım»",
     "Bu hafta sonu son bir kupon yapayım diyorum.",
     'Ben de "iyi olur" diyerek onu üstünden almayacağım.',
     0, "anma_ulac"),
    ("⭐ KARŞILAŞTIRMA — «X ile Y aynı şey değil»",
     "hep böyle dönüyorum zaten, bir şey olmuyor",
     '"Bir şey olmadı" ile "olmaz" aynı şey değil.',
     0, "karsilastirma"),
    ("⭐ KARŞIT «değil» — olumsuzluğu söz fiili değil sıfat taşıyor",
     # ⚠️ Kullanıcı metni ALINTIYI BİREBİR taşır; yoksa vaka iki şeyi birden sınar
     # ve *«de»* eklenmiş bir alıntının ayrı bulgusu muafiyet sapması sanılır.
     "Ortada bir şey söylemeden çekilmek tuhaf, gerçeği söylemek mümkün değil.",
     '"Gerçeği söylemek mümkün değil" demişsin, "istemiyorum" değil. Neyi kastediyorsun?',
     0, "karsit_degil"),
]


def _kos(kullanici: str, cevap: str) -> dict:
    kayit = {"id": "regresyon", "gen_meta": {"parti_sira": 0}, "context": [],
             "messages": [{"role": "user", "content": kullanici},
                          {"role": "assistant", "content": cevap}]}
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False,
                                     encoding="utf-8") as f:
        f.write(json.dumps(kayit, ensure_ascii=False) + "\n")
        yol = f.name
    MUAF.sifirla()
    with redirect_stdout(io.StringIO()):
        KAPI.main(yol)
    o = json.loads((KOK / f"reports/analiz/2026-09-17-alinti-birebirlik-"
                          f"{Path(yol).stem}.json").read_text(encoding="utf-8"))
    (KOK / f"reports/analiz/2026-09-17-alinti-birebirlik-{Path(yol).stem}.json").unlink()
    Path(yol).unlink()
    return {"bulgu": o["bulgu"], "muafiyet": [m["muafiyet"] for m in MUAF.DEFTER]}


def main() -> int:
    sat = ["# Alıntı kapısı — regresyon sınaması", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** 2026-09-17", "",
           "⛔ Bir kapı gevşetildiğinde sorulacak soru *«yeni hâli sessiz mi»* değil,",
           "**«eski yakaladıklarını hâlâ yakalıyor mu»**dur.", "",
           "| # | vaka | beklenen bulgu | çıkan | muafiyet | |", "|---:|---|---:|---:|---|---|"]
    hata = 0
    for i, (ad, kul, cev, bek, muaf_bek) in enumerate(VAKA, 1):
        s = _kos(kul, cev)
        tamam = len(s["bulgu"]) == bek and (muaf_bek is None or muaf_bek in s["muafiyet"])
        hata += not tamam
        sat.append(f"| {i} | {ad} | {bek} | {len(s['bulgu'])} | "
                   f"`{', '.join(s['muafiyet']) or '—'}` | {'✅' if tamam else '⛔ **SAPMA**'} |")
    sat += ["", (f"⭐ **{len(VAKA)} vakanın {len(VAKA)}'ü de beklendiği gibi.**" if not hata
                 else f"⛔⛔ **{hata} vaka sapıyor — kapı yayımlanamaz.**"), ""]
    (KOK / "reports/analiz/2026-09-17-alinti-kapi-regresyon.md").write_text(
        "\n".join(sat), encoding="utf-8")
    print("\n".join(sat))
    return 1 if hata else 0


if __name__ == "__main__":
    raise SystemExit(main())
