#!/usr/bin/env python3
"""R1 — RAG soru envanteri: korpusumuzda DIŞ BİLGİ gerektiren sorular hangileri?

Neden: K73'ün hatası pasajları SORUYA değil SENARYOYA göre yazmaktı; dokuz pasajın
sekizinde pasajdan cevaba tek bir içerik sözcüğü geçmedi. Aynı hata gerçek korpusta
da yapılabilir — kaynak toplanır, kullanıcının sorduğu şey içinde olmaz. Bu yüzden
belge toplama, elimizdeki soruların envanterinden başlar (plan.md §17.6 R1).

Yöntem: kullanıcı turlarından soru cümleleri çıkarılır, A katmanı (yordam/kurum)
kategorilerine anahtar kelimeyle eşlenir. Eşleşmeyen kova AYRICA raporlanır —
asıl bilgi orada: sorulan ama A katmanının kapsamadığı şey ne?

⚠️ İKİ SINIR, raporda da yazılı:
1. Anahtar kelime vekili. Bu bir KAPI değil, okunacak bir ENVANTER; yanlış pozitif
   maliyeti düşük, yanlış negatif kovası zaten ayrıca basılıyor.
2. ⛔ Girdilerin TAMAMI sentetik. Gerçek BıRAG kullanım verisi yok (PROJECT_MEMORY
   açık soru). Envanter "kullanıcılar bunu soruyor"u değil, "BİZ bunu soruyor
   varsaydık"ı ölçer. Gerçek talep kanıtı İP5 pilotundan gelir.

Girdi : data/seeds.jsonl · data/candidates/*.jsonl · evals/*.jsonl
Çıktı : reports/analiz/2026-09-15-rag-soru-envanteri.md
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
CIKTI = KOK / "reports/analiz/2026-09-15-rag-soru-envanteri.md"

GIRDILER = [
    ("tohum", "data/seeds.jsonl"),
    ("korpus v3", "data/candidates/v3-kumulatif.jsonl"),
    ("korpus v4", "data/candidates/v4-parti1.jsonl"),
    ("uzman örneklemi", "data/candidates/expert-70.jsonl"),
    ("cetvel dev", "evals/golden.dev.jsonl"),
    ("cetvel test", "evals/golden.test.jsonl"),
    ("cetvel locked", "evals/golden.locked.jsonl"),
    ("eksen 4 bağlam", "evals/context_fidelity.jsonl"),
]

# A katmanı kategorileri — docs/arastirma-notlari.md BÖLÜM K'den türetildi.
# İKİ ELEK: `GENIS` ilk denemeydi ve gürültülü çıktı (aşağıda ölçülüyor); `DAR` yalnızca
# kuruma/yordama ÖZGÜ terim arar ve cümlenin soru olmasını da şart koşar. İkisi de
# raporlanıyor — arada kalan fark, anahtar kelime vekilinin yanlış pozitif payıdır.
GENIS = {
    "başvuru / erişim": r"başvur|randevu|nereye git|ön görüşme|sevk|kayıt ol|sıra|nasıl gid|müracaat",
    "gizlilik / kayıt": r"gizli|aileme|ailem|işveren|patron|sicil|duyar mı|öğrenir mi|kayıt.*(gider|kalır|tutul)|dosya",
    "hukuki yordam": r"denetimli|serbestlik|imza|idrar|test|mahkeme|savcı|ceza|dava|hapis|avukat|tck|yükümlü|tebliğ",
    "kurum haritası": r"amatem|çematem|yedam|yeşilay|\b191\b|poliklinik|hastane|merkez|kuruluş|danışmanlık merkez",
    "uygunluk / hak": r"\b18\b|yaş sınır|sigorta|sgk|ücret|para|ödeme|ücretsiz|veli|yakını|şart|hakkım",
}
# DAR: jenerik sözcük yok (para, test, sıra, merkez, dosya, kayıt, imza…). Yalnızca
# kurum adı, mevzuat adı ve yordam fiili. Bunlar meşru bağlamda da geçebilir ama
# ÜÇÜ BİRDEN olmadan (soru + özgü terim) eşleşmiyor.
DAR = {
    "başvuru / erişim": r"başvur\w*|randevu\w*|ön görüşme|sevk\b|müracaat|nereye gid|nasıl gider",
    "gizlilik / kayıt": r"aileme söyle|ailem\w* (duy|öğren)|işveren\w*|sicil\w*|dosyama işl|gizli kal|kayıt tutul",
    "hukuki yordam": r"denetimli serbestlik|imza at\w*|idrar test\w*|\btck\b|savcı\w*|avukat\w*|mahkeme\w*|dava aç",
    "kurum haritası": r"amatem|çematem|yedam|yeşilay|\b191\b|poliklinik|aile hekim\w*",
    "uygunluk / hak": r"18 yaş|yaş sınır\w*|sigorta\w*|\bsgk\b|ücret\w*|ne kadar tutu|ücretsiz",
}
GENIS_RE = {k: re.compile(v, re.IGNORECASE) for k, v in GENIS.items()}
DAR_RE = {k: re.compile(v, re.IGNORECASE) for k, v in DAR.items()}

# Soru tespiti: soru işareti VEYA soru eki/sözcüğü. "mı/mi/mu/mü" ayrı token olmalı —
# aksi hâlde "kımıldamak", "ismi" gibi sözcükler eşleşir (K65 ailesi).
SORU_EKI = re.compile(r"\b(mı|mi|mu|mü|mıyım|miyim|muyum|müyüm|mısın|misin|mısınız|misiniz)\b", re.IGNORECASE)
# Türkiye sisteminde karşılığı OLMAYAN / marjinal kurum işaretleri. Hedef soru listesine
# giren bir soru bu işaretleri taşıyorsa aranacak belge yoktur — doğru davranış §7a'nın
# `yetersiz` dalıdır. Kaynak: docs/arastirma-notlari.md §K (Türkiye kurumsal haritası).
ABD_CERCEVE = {
    "AA sponsoru": r"\bsponsor\w*\b|adsız alkolikler|\bAA toplantı",
    "işveren sigortası": r"kurumsal sigorta\w*|davranışsal sağlık|sigortam\w* (karşıl|kapsı)",
    "ABD kriz hattı": r"\b988\b|\b911\b",
    "rehab kurumu": r"\brehab\b|rehab merkez",
    "EAP / çalışan destek": r"\bEAP\b|çalışan destek program",
}
ABD_RE = {k: re.compile(v, re.IGNORECASE) for k, v in ABD_CERCEVE.items()}

SORU_SOZ = re.compile(r"\b(nasıl|nere\w*|ne zaman|kim\b|kaç\b|hangi|neden|niye|niçin|ne kadar)\b", re.IGNORECASE)


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def kullanici_metinleri(yol: Path) -> list[str]:
    cikti = []
    for satir in yol.read_text(encoding="utf-8").splitlines():
        if not satir.strip():
            continue
        r = json.loads(satir)
        if "user_message" in r:
            cikti.append(r["user_message"])
        for m in r.get("messages", []):
            if m.get("role") == "user":
                cikti.append(m.get("content", ""))
    return cikti


def sorular(metin: str) -> list[str]:
    # Bağlam bloğu kullanıcı turuna gömülü olabilir (K17) — pasaj metnini soru sayma.
    metin = re.sub(r"\[BAĞLAM\].*?\[/BAĞLAM\]|<context>.*?</context>", " ", metin,
                   flags=re.DOTALL | re.IGNORECASE)
    bulunan = []
    for c in re.split(r"(?<=[.!?])\s+|\n+", metin):
        c = c.strip()
        if not (8 <= len(c) <= 220):
            continue
        if c.endswith("?") or SORU_EKI.search(c) or SORU_SOZ.search(c):
            bulunan.append(c)
    return bulunan


def main() -> None:
    kaynak_sat, tum_soru = [], []
    toplam_tur = 0
    for etiket, yol_s in GIRDILER:
        yol = KOK / yol_s
        if not yol.exists():
            kaynak_sat.append(f"| {etiket} | `{yol_s}` | — | **yok** |")
            continue
        metinler = kullanici_metinleri(yol)
        s_ = [(etiket, q) for m in metinler for q in sorular(m)]
        toplam_tur += len(metinler)
        tum_soru += s_
        kaynak_sat.append(f"| {etiket} | `{yol_s}` | `{sha(yol)}` | {len(metinler)} tur · {len(s_)} soru |")

    def ele(rx_map, soru_sart: bool):
        kova = defaultdict(list)
        for etiket, q in tum_soru:
            if soru_sart and not (q.endswith("?") or SORU_EKI.search(q)):
                continue
            vuran = [k for k, rx in rx_map.items() if rx.search(q)]
            for k in vuran or ["— eşleşmeyen —"]:
                kova[k].append((etiket, q))
        return kova

    genis = ele(GENIS_RE, soru_sart=False)
    dar = ele(DAR_RE, soru_sart=True)

    # Türkiye geçerlilik denetimi — tohum METNİNİN tamamı taranır (yalnızca soru cümlesi
    # değil), çünkü çerçeve genelde soruyu kuşatan cümlede duruyor.
    abd, abd_ornek, n_tohum = Counter(), {}, 0
    for satir in (KOK / "data/seeds.jsonl").read_text(encoding="utf-8").splitlines():
        if not satir.strip():
            continue
        r = json.loads(satir)
        n_tohum += 1
        m = r.get("user_message", "") + " " + (r.get("scenario_context") or "")
        for k, rx in ABD_RE.items():
            g = rx.search(m)
            if g:
                abd[k] += 1
                abd_ornek.setdefault(k, m[max(0, g.start() - 60):g.start() + 80].replace("\n", " "))

    def essiz(kova):
        return len({q for k, v in kova.items() if k != "— eşleşmeyen —" for _, q in v})

    sat = [
        "# R1 — RAG soru envanteri: dış bilgi gerektiren sorular",
        "",
        f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}",
        "",
        "| girdi | dosya | SHA256 (ilk 16) | çıkarılan |",
        "|---|---|---|---|",
        *kaynak_sat,
        "",
        "---",
        "",
        "## 1. Neden bu envanter",
        "",
        "K73'ün hatası pasajları **soruya değil senaryoya** göre yazmaktı: dokuz pasajın",
        "sekizinde pasajdan cevaba tek bir içerik sözcüğü geçmedi. Belge toplamaya",
        "sorudan başlanmazsa aynı hata büyük ölçekte tekrarlanır.",
        "",
        "## 2. İki elek",
        "",
        f"Taranan kullanıcı turu **{toplam_tur}** · çıkarılan soru cümlesi **{len(tum_soru)}**.",
        "",
        "| elek | ne arıyor | eşleşme | eşsiz soru |",
        "|---|---|---|---|",
        f"| **geniş** | kategori sözcüğü (jenerik dahil: *para, test, sıra, merkez*) | {sum(len(v) for k, v in genis.items() if k != '— eşleşmeyen —')} | **{essiz(genis)}** |",
        f"| **dar** | kurum/mevzuat/yordam terimi **ve** cümlenin soru olması | {sum(len(v) for k, v in dar.items() if k != '— eşleşmeyen —')} | **{essiz(dar)}** |",
        "",
        "| kategori | geniş | dar |",
        "|---|---|---|",
        *[f"| {k} | {len(genis.get(k, []))} | {len(dar.get(k, []))} |" for k in GENIS],
        f"| — eşleşmeyen — | {len(genis['— eşleşmeyen —'])} | {len(dar['— eşleşmeyen —'])} |",
        "",
        "⚠️ **Geniş elek okunamaz durumda.** Örneklerine bakıldığında eşleşmelerin çoğu",
        "yanlış pozitif: *\"sıra sana mı gelsin\"* (başvuru sırası değil, aile sitemi),",
        "*\"o parayı nereden bulayım\"* (ücret sorusu değil), *\"iyi anne mi olduğumu test",
        "ediyormuş gibi\"* (idrar testi değil). Türkçe serbest metinde tek sözcüklü kapı",
        "yine tavana vurdu — bu desenin projede kaçıncı örneği olduğu `T22`'de izleniyor.",
        "**Aşağıdaki okuma DAR elekten yapılıyor.**",
        "",
        "## 3. Dar elek — örnekler",
        "",
    ]
    for k in GENIS:
        v = dar.get(k, [])
        sat += [f"### {k} ({len(v)})", ""]
        if not v:
            sat += ["*(hiç yok — korpusumuz bu soruyu hiç sormuyor)*", ""]
            continue
        gorulen = set()
        for etiket, q in v:
            if q in gorulen:
                continue
            gorulen.add(q)
            sat.append(f"- *{q}* — `{etiket}`")
            if len(gorulen) >= 8:
                break
        sat.append("")

    sat += [
        "## 4. Bulgu — korpusumuz bu soruları neredeyse hiç sormuyor",
        "",
        f"{len(tum_soru)} soru cümlesinin **{essiz(dar)}**'i dış bilgi gerektiriyor.",
        "Bu, K73'ün bağlam dilimi bulgusuyla aynı yöne işaret ediyor: dokuz bağlamlı",
        "kaydın **altısında** *\"kullanıcı zaten soru sormamış\"*tı. Ayrıca `plan.md` §6",
        "karışımın **%75'inin** doküman gerektirmediğini zaten söylüyor.",
        "",
        "**Sonuç, toplama planını değiştiriyor:** hedef belge listesi korpusumuzdan",
        "**türetilemez**, çünkü korpusumuz o soruları sormuyor. İki kaynağı ayırmak gerek:",
        "",
        "| Ne | Nereden gelir | Durum |",
        "|---|---|---|",
        "| Kullanıcı **fiilen** ne soruyor | İP5 pilotu | ⛔ yok — gerçek kullanım verisi yok |",
        "| Kullanıcı **ne sorabilir** | kurumsal harita (`arastirma-notlari` §K) | ✅ elimizde |",
        "",
        "Yani R2 kaynak haritası **kapsam** üstüne kurulur (kurumun cevapladığı soru",
        "kümesi), **talep** üstüne değil. Bu bir varsayımdır ve varsayım olduğu yazılı kalır.",
        "",
        "## 5. Türkiye geçerlilik denetimi — aranacak belgesi OLMAYAN sorular",
        "",
        "Hedef soru listesine giren her satır önce şu denetimden geçmeli: *bu sorunun",
        "Türkiye'de kurumsal bir karşılığı var mı?* Yoksa belge aranmaz — doğru model",
        "davranışı §7a'nın `yetersiz` dalıdır.",
        "",
        f"`data/seeds.jsonl` ({n_tohum} tohum) ABD sistemi çerçevesi için tarandı:",
        "",
        "| işaret | tohum | örnek |",
        "|---|---|---|",
        *[f"| {k} | **{n}** | …{abd_ornek[k]}… |" for k, n in abd.most_common()],
        "",
        f"**{sum(abd.values())} eşleşme / {n_tohum} tohum (%{100*sum(abd.values())/n_tohum:.1f}).**",
        "Dar bir artefakt — korpus geneli ABD çerçeveli DEĞİL. Ama dar elekten çıkan dört",
        "`gizlilik/kayıt` sorusundan **biri** buradan geliyor (*\"kurumsal sigortamız",
        "davranışsal sağlık notlarını görüyor mu\"*), yani hedef listesi denetimsiz",
        "kullanılamaz. `docs/rag-kaynak-haritasi.md` §1'de S4 bu gerekçeyle elendi.",
        "",
        "## 6. Sınırlar",
        "",
        "1. **Anahtar kelime vekili** — kapı değil, envanter. Geniş/dar farkı yanlış",
        "   pozitif payını görünür kılmak için basılıyor.",
        "2. Dar elek **yanlış negatif** verir: soru ekisiz, terimsiz sorulan bilgi",
        "   ihtiyacı (*\"oraya gitsem ne olur\"*) kaçar. Alt sınır ölçüyor, üst sınır değil.",
        "3. ⛔ **Girdilerin tamamı sentetik.** Gerçek BıRAG kullanım verisi yok",
        "   (`PROJECT_MEMORY.md` açık soru). Envanter *\"kullanıcılar bunu soruyor\"*u değil,",
        "   ***\"biz bunu soruyor varsaydık\"***ı ölçer.",
        "",
    ]
    CIKTI.write_text("\n".join(sat), encoding="utf-8")
    print(f"tur {toplam_tur} · soru {len(tum_soru)} · geniş {essiz(genis)} · dar {essiz(dar)}")
    print(CIKTI.relative_to(KOK))


if __name__ == "__main__":
    main()
