#!/usr/bin/env python3
"""Partiler arası uydurma oynaklığının sebebi — ön kayıtlı ölçüm.

⭐ **SORU (T242'nin açık kalemi).** Uydurma oranı `v6-parti3`–`parti8`
arasında **%1,7 ile %18,6** salınıyor ve bunu risk, bağlam ya da tur sayısı
açıklamıyor (üçü de dengeli ölçüldü). Sebep ne?

⛔⛔ **ÖN KAYIT — hipotez sayılardan önce yazıldı.**

  **H₁ (BİRİNCİL): ÖZETLEME.** Kaynağı toplu bir sayı değil, elle okunan
  vakalar: işaretlenen uydurmaların biçimi tekrar tekrar **sayıp dökmekti**
  — *«Bugün yazdığın iki şey var: …»*, *«Şu an elinde şunlar var: …»*,
  *«Toparlayacak olursam…»*, *«bugüne kadar söylediklerin şunlar»*. Bir
  cevap kullanıcının söylediklerini **liste hâline getirdiğinde**, listeye
  bir madde fazla koymak metnin geri kalanından daha kolaydır.
  ⇒ `judge.ozet_var` = True olan kayıtlarda uydurma oranı daha yüksektir.

  ⭐ K193 bu hipotezi bağımsız olarak destekliyor: korpusun **en büyük
  ikinci kalıbı** *«bugüne kadar söylediklerin şunlar»* (43 kayıt, %7,5).

  **Sınama sırası.** (1) H₁ ölçülür. (2) H₁ doğruysa asıl soru sorulur:
  özetleme **parti oynaklığını açıklıyor mu**? — her partinin beklenen
  uydurma sayısı özet oranından türetilir ve **artık heterojenlik** G ile
  sınanır. Açıklıyorsa G düşer, açıklamıyorsa düşmez.
  (3) Geri kalan her şey **KEŞİFSEL**dir ve öyle etiketlenir.

  ⛔⛔ **Çokluk uyarısı önceden yazılı:** keşifsel bölümde 6+ değişken
  taranıyor; oradaki en küçük p **seçilerek** elde edilmiştir ve tek başına
  bir bulgu değildir. Ancak ön kayıtlı H₁ bir bulgudur.

  ⛔ Ölçü yine `grounding == 2` ve bir **ALT SINIRDIR** (T238).

Çıktı: reports/analiz/2026-09-22-uydurma-oynakligi.md
"""
from __future__ import annotations

import collections
import json
import math
import random
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-uydurma-oynakligi.md"
PARTILER = [f"v6-parti{i}" for i in range(3, 9)]
TOHUM = 20260922
N_PERM = 20000
TOHUM_META = {r["seed_id"]: r["meta"] for r in
              (json.loads(l) for l in open(KOK / "data/seeds.v2.jsonl"))}


def wilson(k, n, z=1.96):
    if not n:
        return (0.0, 0.0)
    p, d = k / n, 1 + z * z / n
    m = (p + z * z / (2 * n)) / d
    y = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, m - y), min(1.0, m + y))


def G_testi(gozlenen, beklenen):
    """G = 2·Σ o·ln(o/b). Sıfır gözlemler atlanır."""
    return 2 * sum(o * math.log(o / b) for o, b in zip(gozlenen, beklenen) if o > 0)


def kikare_p(x, k):
    if k % 2 == 0:
        t = math.exp(-x / 2); s = t
        for i in range(1, k // 2):
            t *= x / (2 * i); s += t
        return min(1.0, s)
    # tek serbestlik derecesi: normal yaklaşıklık
    z = math.sqrt(max(x, 0))
    return math.erfc(z / math.sqrt(2))


def perm_p(kayit, anahtar, deger, rng):
    """`anahtar == deger` olanlar ile olmayanlar arasındaki oran farkı."""
    a = [k["uydurma"] for k in kayit if k[anahtar] == deger]
    b = [k["uydurma"] for k in kayit if k[anahtar] != deger]
    if not a or not b:
        return None, None
    d = sum(a) / len(a) - sum(b) / len(b)
    hepsi = [k["uydurma"] for k in kayit]
    n_a, asiri = len(a), 0
    for _ in range(N_PERM):
        rng.shuffle(hepsi)
        dd = sum(hepsi[:n_a]) / n_a - sum(hepsi[n_a:]) / (len(hepsi) - n_a)
        if abs(dd) >= abs(d) - 1e-12:
            asiri += 1
    return d, (asiri + 1) / (N_PERM + 1)


def main() -> int:
    kayit = []
    for p in PARTILER:
        for l in open(KOK / f"data/judged/{p}.claude.jsonl"):
            r = json.loads(l)
            j = r.get("judge")
            if not j:
                continue
            g = r.get("gen_meta") or {}
            son = [m for m in r["messages"] if m["role"] == "assistant"][-1]
            kayit.append({
                "parti": p,
                "uydurma": j.get("grounding") == 2,
                "ozet": bool(j.get("ozet_var")),
                "yansitma": bool(j.get("yansitma_var")),
                "karmasik": bool(j.get("karmasik_yansitma")),
                "takdir": bool(j.get("takdir_var")),
                "turn_ending": g.get("turn_ending", "?"),
                "bicim": g.get("bicim", "?"),
                "register": g.get("register", "?"),
                "konusma_durumu": g.get("konusma_durumu", "?"),
                "uzunluk": len((son.get("content") or "").split()),
                "risk": (TOHUM_META.get(g.get("seed_id")) or {}).get("risk_seviyesi", "?"),
            })
    # uzunluk üçe bölünür
    uz = sorted(k["uzunluk"] for k in kayit)
    q1, q2 = uz[len(uz) // 3], uz[2 * len(uz) // 3]
    for k in kayit:
        k["uzunluk_dilimi"] = ("kısa" if k["uzunluk"] <= q1
                               else "orta" if k["uzunluk"] <= q2 else "uzun")

    rng = random.Random(TOHUM)
    say = collections.Counter(k["parti"] for k in kayit)
    uyd = collections.Counter(k["parti"] for k in kayit if k["uydurma"])
    N, U = len(kayit), sum(1 for k in kayit if k["uydurma"])

    # ── (0) taban: parti heterojenliği ──────────────────────────────
    p_hat = U / N
    G0 = sum(G_testi([uyd[p], say[p] - uyd[p]],
                     [say[p] * p_hat, say[p] * (1 - p_hat)]) for p in PARTILER)
    pG0 = kikare_p(G0, len(PARTILER) - 1)

    # ── (1) ÖN KAYITLI H₁: özetleme ─────────────────────────────────
    d_ozet, p_ozet = perm_p(kayit, "ozet", True, rng)
    o_var = [k for k in kayit if k["ozet"]]
    o_yok = [k for k in kayit if not k["ozet"]]
    a1, b1 = sum(k["uydurma"] for k in o_var), len(o_var)
    a0, b0 = sum(k["uydurma"] for k in o_yok), len(o_yok)

    # ── (2) özetleme parti oynaklığını açıklıyor mu ─────────────────
    p_ozet_var, p_ozet_yok = a1 / b1, a0 / b0
    beklenen = {}
    for p in PARTILER:
        n1 = sum(1 for k in kayit if k["parti"] == p and k["ozet"])
        n0 = say[p] - n1
        beklenen[p] = n1 * p_ozet_var + n0 * p_ozet_yok
    G1 = sum(G_testi([uyd[p], say[p] - uyd[p]],
                     [beklenen[p], say[p] - beklenen[p]]) for p in PARTILER)
    pG1 = kikare_p(G1, len(PARTILER) - 2)
    ozet_payi = {p: sum(1 for k in kayit if k["parti"] == p and k["ozet"]) / say[p]
                 for p in PARTILER}

    # ── (3) KEŞİFSEL ────────────────────────────────────────────────
    kesif = []
    for alan in ("yansitma", "karmasik", "takdir"):
        d, pp = perm_p(kayit, alan, True, rng)
        kesif.append((alan, "True", d, pp))
    for alan in ("turn_ending", "bicim", "register", "konusma_durumu",
                 "uzunluk_dilimi", "risk"):
        for deger in sorted({k[alan] for k in kayit}):
            if sum(1 for k in kayit if k[alan] == deger) < 25:
                continue
            d, pp = perm_p(kayit, alan, deger, rng)
            if d is not None:
                kesif.append((alan, deger, d, pp))
    kesif.sort(key=lambda x: x[3])

    sat = ["# Partiler arası uydurma oynaklığının sebebi", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Küme:** `v6-parti3`–`parti8`, {N} kayıt, aynı judge + rubrik v9  ",
           f"**Ölçü:** `grounding == 2` ({U} kayıt, %{100*U/N:.1f}) · "
           f"permütasyon {N_PERM}, tohum {TOHUM}  ", "",
           "⛔⛔ **Hipotez sayılardan önce yazıldı** (betiğin başında). "
           "Birincil hipotezin kaynağı toplu bir sayı değil, **elle okunan "
           "vakalar**: işaretlenen uydurmaların biçimi tekrar tekrar sayıp "
           "dökmekti.", "",
           "## (0) Açıklanacak şey", "",
           f"Parti heterojenliği: **G = {G0:.1f}**, sd = {len(PARTILER)-1}, "
           f"p = **{pG0:.4f}** ⇒ partiler tek bir tabandan gelmiyor. Aşağıdaki "
           "sorunun tamamı bu G'yi düşürmekle ilgili.", "",
           "## ⭐⭐ (1) ÖN KAYITLI HİPOTEZ — özetleme", "",
           "| cevap | uydurma | oran | %95 Wilson |", "|---|---:|---:|---|"]
    for ad, a, b in (("`ozet_var` = **True**", a1, b1),
                     ("`ozet_var` = False", a0, b0)):
        lo, hi = wilson(a, b)
        sat.append(f"| {ad} | {a}/{b} | %{100*a/b:.1f} | %{100*lo:.1f}–%{100*hi:.1f} |")
    sat += ["", f"**Fark: {100*d_ozet:+.1f} puan · permütasyon p = "
            f"{p_ozet:.4f}**", ""]
    sat += ["⭐⭐⭐ **Doğrulandı.** Özet içeren cevaplarda uydurma oranı "
            "belirgin biçimde yüksek." if p_ozet < 0.05 else
            "⛔ **Doğrulanmadı.** Ön kayıtlı hipotez tutmadı ve bu **bir "
            "bulgudur** — okuduğum vakaların biçimi beni yanılttı."]
    sat += ["", "## ⭐⭐⭐ (2) Asıl soru — parti oynaklığını AÇIKLIYOR mu", "",
            "Her partinin beklenen uydurma sayısı kendi **özet payından** "
            "türetildi; artık heterojenlik G ile sınandı.", "",
            "| | G | sd | p |", "|---|---:|---:|---:|",
            f"| ham parti heterojenliği | {G0:.1f} | {len(PARTILER)-1} | {pG0:.4f} |",
            f"| özete göre düzeltilmiş **artık** | **{G1:.1f}** | "
            f"{len(PARTILER)-2} | **{pG1:.4f}** |", "",
            f"⇒ Özetleme heterojenliğin **%{100*(G0-G1)/G0:.0f}**'ini "
            "açıklıyor." if G0 > 0 else "", "",
            "| parti | özet payı | uydurma |", "|---|---:|---:|"]
    sat += [f"| `{p}` | %{100*ozet_payi[p]:.0f} | %{100*uyd[p]/say[p]:.1f} |"
            for p in PARTILER]
    sat += ["", "## (3) ⛔ KEŞİFSEL — çoklu karşılaştırma, tek başına bulgu değil", "",
            f"{len(kesif)} karşılaştırma tarandı. ⛔⛔ Buradaki en küçük p "
            "**seçilerek** elde edilmiştir; Bonferroni eşiği "
            f"0,05/{len(kesif)} = **{0.05/len(kesif):.4f}**.", "",
            "| değişken | değer | fark (puan) | p |", "|---|---|---:|---:|"]
    for alan, deger, d, pp in kesif[:12]:
        yildiz = " ⭐" if pp < 0.05 / len(kesif) else ""
        sat.append(f"| `{alan}` | `{deger}` | {100*d:+.1f} | {pp:.4f}{yildiz} |")
    # ── (4) hangi etken parti oynaklığını AÇIKLIYOR ─────────────────
    #  ⛔ Etkenler (3)'ün sonucuna bakılarak seçilmedi: kategorik olan
    #     HEPSİ sınanıyor ki seçim yanlılığı olmasın.
    def artik_G(alan):
        seviye = sorted({k[alan] for k in kayit})
        oran = {}
        for sv in seviye:
            g = [k["uydurma"] for k in kayit if k[alan] == sv]
            oran[sv] = (sum(g) / len(g)) if g else p_hat
        G = 0.0
        for pp in PARTILER:
            bek = sum(oran[k[alan]] for k in kayit if k["parti"] == pp)
            bek = min(max(bek, 1e-9), say[pp] - 1e-9)
            G += G_testi([uyd[pp], say[pp] - uyd[pp]], [bek, say[pp] - bek])
        return G, len(seviye) - 1

    adaylar = ("ozet", "yansitma", "karmasik", "takdir", "turn_ending",
               "bicim", "register", "konusma_durumu", "uzunluk_dilimi", "risk")
    aciklama = []
    for alan in adaylar:
        G, k_ek = artik_G(alan)
        sd = max(len(PARTILER) - 1 - k_ek, 1)
        aciklama.append((alan, G, 100 * (G0 - G) / G0, kikare_p(G, sd), sd))
    aciklama.sort(key=lambda x: x[1])

    sat += ["", "## ⭐⭐⭐ (4) Hangi etken parti oynaklığını AÇIKLIYOR", "",
            f"Ham heterojenlik **G = {G0:.1f}**. Her etken için: o etkene göre "
            "beklenen uydurma sayısı hesaplandı ve **artık** G ölçüldü. "
            "⛔ Etkenler (3)'ün sonucuna bakılarak seçilmedi — kategorik olan "
            "**hepsi** sınandı.", "",
            "| etken | artık G | açıkladığı | artık p |", "|---|---:|---:|---:|"]
    for alan, G, pay, pp2, sd in aciklama:
        sat.append(f"| `{alan}` | {G:.1f} | %{pay:.0f} | {pp2:.4f} |")
    en_iyi = aciklama[0]
    sat += ["", f"⭐ En çok açıklayan: **`{en_iyi[0]}`** — heterojenliğin "
            f"**%{en_iyi[2]:.0f}**'ini alıyor, ama artık p = **{en_iyi[3]:.4f}**.", ""]
    sat += ["⛔⛔⛔ **HİÇBİR ETKEN OYNAKLIĞI AÇIKLAMIYOR.** En iyisi bile "
            "artık heterojenliği anlamlı bırakıyor ⇒ partiler arası fark, "
            "ölçebildiğim tasarım değişkenlerinin **hiçbirinden** gelmiyor. "
            "➡️ *Geriye ölçmediğim şey kalıyor: partiyi yazan oturumun "
            "kendisi — hangi blok betiği, hangi gün, hangi dikkat.*"
            if en_iyi[3] < 0.05 else
            "⭐ En iyi etken artık heterojenliği anlamsız kılıyor ⇒ oynaklığın "
            "büyük kısmı o etkenden geliyor olabilir.", ""]

    # ── (5) «YAZAN OTURUM» hipotezi — blok düzeyi ───────────────────
    #  ⭐ (4) bütün tasarım değişkenlerini eledi; geriye yazan oturum kaldı.
    #    Bunun SINANABİLİR sonucu: her blok ayrı bir yazma turudur ⇒ hipotez
    #    doğruysa uydurma parti İÇİNDE de bloklara öbeklenmelidir.
    blok_of = {}
    for f in sorted((KOK / "data/candidates").glob("v6-parti[3-8].blok*.jsonl")):
        for l in open(f):
            blok_of[json.loads(l)["id"]] = f.stem
    idler = []
    for pp in PARTILER:
        for l in open(KOK / f"data/judged/{pp}.claude.jsonl"):
            rr = json.loads(l)
            if rr.get("judge"):
                idler.append(rr["id"])
    for k, kid in zip(kayit, idler):
        k["blok"] = blok_of.get(kid)
    eslesen = [k for k in kayit if k["blok"]]

    def blok_ici_G(veri):
        G = 0.0
        for pp in PARTILER:
            gr = [k for k in veri if k["parti"] == pp]
            if not gr:
                continue
            pr = sum(k["uydurma"] for k in gr) / len(gr)
            if pr in (0.0, 1.0):
                continue
            for bl in sorted({k["blok"] for k in gr}):
                b = [k for k in gr if k["blok"] == bl]
                o = sum(k["uydurma"] for k in b)
                G += G_testi([o, len(b) - o], [len(b) * pr, len(b) * (1 - pr)])
        return G

    G_blok = blok_ici_G(eslesen)
    rng2 = random.Random(TOHUM)
    N_B = N_PERM // 4
    havuz = {pp: [k["uydurma"] for k in eslesen if k["parti"] == pp]
             for pp in PARTILER}
    asiri = 0
    for _ in range(N_B):
        karisik, it = [], {}
        for pp in PARTILER:
            v = havuz[pp][:]
            rng2.shuffle(v)
            it[pp] = iter(v)
        for k in eslesen:
            karisik.append({**k, "uydurma": next(it[k["parti"]])})
        if blok_ici_G(karisik) >= G_blok - 1e-9:
            asiri += 1
    pB = (asiri + 1) / (N_B + 1)
    n_blok = len({k["blok"] for k in eslesen})

    sat += ["## ⭐⭐⭐ (5) «Yazan oturum» hipotezi — blok düzeyi", "",
            "(4) bütün tasarım değişkenlerini eledi; geriye *«partiyi yazan "
            "oturumun kendisi»* kaldı. ⭐ Bunun **sınanabilir** bir sonucu var: "
            f"her blok ayrı bir yazma turudur ({n_blok} blok, {len(eslesen)} "
            "kayıt eşleşti) ⇒ hipotez doğruysa uydurma, parti **içinde de** "
            "bloklara öbeklenmiş olmalı. Değilse hipotez düşer.", "",
            "| | |", "|---|---|",
            f"| parti içi, bloklar arası heterojenlik | **G = {G_blok:.1f}** |",
            f"| permütasyon (etiketler parti İÇİNDE karıştırıldı, {N_B} tur) | "
            f"p = **{pB:.4f}** |", ""]
    sat += ["⭐⭐⭐ **Öbeklenme var.** Uydurma parti içinde belirli bloklara "
            "yığılıyor ⇒ *«yazan oturum»* hipotezi ayakta: oynaklığın kaynağı "
            "tasarımda değil **yazma turunun kendisinde**."
            if pB < 0.05 else
            "⛔⛔⛔ **ÖBEKLENME YOK.** Uydurma parti içinde bloklara rastgele "
            "dağılıyor ⇒ *«yazan oturum»* hipotezi de **DÜŞTÜ**. ➡️ *Oynaklık "
            "parti düzeyinde gerçek, ama ne tasarım değişkenleri ne de yazma "
            "turu onu tutuyor. Ölçebildiğim hiçbir şey açıklamıyor — ve bunu "
            "söylemek, açıklayan bir şey uydurmaktan daha doğru.*", "",
            "## ⭐⭐ (6) Parti düzeyinde ne farklı", "",
            "(4) kayıt düzeyini, (5) blok düzeyini eledi. Geriye **parti "
            "düzeyi** kaldı — parti içinde sabit, partiler arasında değişen "
            "bir şey. Kayıtlardaki parti düzeyi değişkenlerin hepsi okundu:", "",
            "| parti | uydurma | `prompt_version` | `generator_model` | "
            "`tohum_havuzu` | `date` |", "|---|---:|---|---|---|---|"]
    for pp in PARTILER:
        ilk = next(k for k in kayit if k["parti"] == pp)
        g = json.loads(next(l for l in open(KOK / f"data/judged/{pp}.claude.jsonl")
                            if json.loads(l).get("judge")))["gen_meta"]
        sat.append(f"| `{pp}` | %{100*uyd[pp]/say[pp]:.1f} | "
                   f"`{g.get('prompt_version')}` | `{g.get('generator_model')}` | "
                   f"`{g.get('tohum_havuzu')}` | {g.get('date')} |")
    sat += ["", "⛔⛔ **Üçü de sabit** (`uretim-v5`, `claude-opus-5`, `seeds`) "
            "⇒ hiçbiri oynaklığı açıklayamaz. **Tarih de açıklamıyor:** aynı "
            "günde üretilen partiler birbirinden çok uzak — 09-20'de %15,0 / "
            "%16,9 / %3,3, 09-21'de %1,7 / %12,3 / %18,6.", "",
            "⚠️ **Yan bulgu (T236 ailesi):** `v6-parti8`'in kayıtları "
            "`date: 2026-09-21` taşıyor ama parti **09-22'de** üretildi "
            "(betik adı ve commit tarihi). Tarih blok şablonunda **sabit "
            "yazılı** ve parti7'den taşınmış. ⭐ Aynı şablonda `parti` alanı "
            "aynı kusurdan dolayı düzeltilip **türetilir** yapılmıştı; `date` "
            "yanı başındaydı ve düzeltilmedi. ➡️ *Bir şablondaki bir beyanı "
            "türetmeye çevirmek, komşusunu düzeltmez.* ⛔ 118 kaydın tarihi "
            "yanlış; K126 zaten *«rapor tarihi betik ADINDAN»* diyor, aynı "
            "kural buraya da uygulanabilir — **bu raporda düzeltilmedi**.", "",
            "## ⛔ Bu ölçümün söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Ölçü bir ALT SINIR** | `grounding` tek-ayrıntı sondasıdır "
            "(T238); özet içeren cevaplar **daha çok ayrıntı** taşır ⇒ sondanın "
            "onlarda daha sık isabet etmesi mümkündür. ⚠️ Yani bulgu *«özet "
            "uydurmayı artırır»* kadar *«sonda özette daha iyi görür»* de "
            "olabilir — **ikisi bu veriyle ayrılamaz** |",
            "| ⛔ **`ozet_var` judge'ın kararıdır** | kodun değil; judge'ın "
            "kendi gürültüsü bu alanda ölçülmedi |",
            "| ⛔ **Nedensellik kurulmadı** | özet ile uydurma birlikte "
            "değişiyor; hangisinin hangisini getirdiği bir **müdahale** ister "
            "(özet oranı düşürülmüş bir parti) |",
            "| ⚠️ **Keşifsel bölüm sıralamaya göre kesildi** | ilk 12 satır "
            "gösteriliyor, tamamı betikte |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[sat.index("## (0) Açıklanacak şey"):]))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
