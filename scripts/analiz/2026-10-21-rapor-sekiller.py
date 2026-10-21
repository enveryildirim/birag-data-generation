"""Gelişme raporu (0–12. ay) şekilleri.

Her şekil `reports/analiz/sekiller/` altına PNG olarak yazılır; girdi dosyaları ve
SHA256-16 değerleri `reports/analiz/2026-10-21-rapor-sekiller.md` künyesine düşer (Kural 7).
Grafiklerdeki her sayı girdi dosyasından okunur; Ş1 bir diyagramdır (sayıları `configs/taxonomy.yaml`).

Kullanım: uv run --with matplotlib python scripts/analiz/2026-10-21-rapor-sekiller.py
"""

import datetime as dt
import hashlib
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "reports/analiz/sekiller"
RAPOR = KOK / "reports/analiz/2026-10-21-rapor-sekiller.md"

# Görselleştirme paleti (dataviz başvuru paleti, açık tema; baskı için beyaz zemin)
MAVI, TURUNCU, CAMGOBEGI = "#2a78d6", "#eb6834", "#1baf7a"
GRI, ACIK_GRI = "#9a9993", "#d9d8d3"
METIN, IKINCIL = "#0b0b0b", "#52514e"

plt.rcParams.update({
    "font.family": "Arial", "font.size": 9, "axes.edgecolor": ACIK_GRI,
    "axes.labelcolor": IKINCIL, "xtick.color": IKINCIL, "ytick.color": IKINCIL,
    "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 200,
})

GIRDILER = []  # (şekil, yol, sha16)


def sha16(yol):
    return hashlib.sha256(Path(yol).read_bytes()).hexdigest()[:16]


def girdi(sekil, yol):
    yol = KOK / yol
    GIRDILER.append((sekil, yol.relative_to(KOK), sha16(yol)))
    return yol


def kaydet(fig, ad):
    CIKTI.mkdir(parents=True, exist_ok=True)
    fig.savefig(CIKTI / ad, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def tr_sayi(x, ondalik=0):
    s = f"{x:,.{ondalik}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s


# --- Ş1 boru hattı ----------------------------------------------------------------

def sekil_boru_hatti():
    fig, ax = plt.subplots(figsize=(10, 4.1))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 42)
    ax.axis("off")

    def kutu(x, y, w, h, baslik, alt, renk):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.25,rounding_size=1.2",
                                    fc="white", ec=renk, lw=1.4))
        ax.text(x + w / 2, y + h - 2.4, baslik, ha="center", va="top", fontsize=8.6,
                fontweight="bold", color=METIN)
        ax.text(x + w / 2, y + h - 6.0, alt, ha="center", va="top", fontsize=7.2,
                color=IKINCIL, linespacing=1.25)

    def ok(x1, y1, x2, y2, renk=GRI, stil="-|>", cizgi="-"):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=stil, mutation_scale=10,
                                     color=renk, lw=1.2, linestyle=cizgi))

    ax.text(0.5, 40.5, "İP1 · Talimat veri kümesi", fontsize=9.5, fontweight="bold", color=MAVI)
    ust = [
        ("Seed'ler", "2.240 senaryo seed'i\ntaksonomi\n(19 senaryo, 6 tür)"),
        ("Üretim", "LLM subagent'ları\nkullanıcı + thinking\n+ cevap"),
        ("Otomatik kontroller", "şema · yasak ifade\nkriz yasağı · numara\nsoru sayısı · uzunluk"),
        ("LLM-judge", "EPITOME + MI\nklinik güvenlik\nhallucination (grounding)"),
        ("Uzman örneklemi", "kabul / sınırda / ret\njudge kalibrasyonu"),
        ("Immutable sürüm", "manifest + SHA256\nveri kartı\n(v0.1.0 · v0.1.1)"),
    ]
    w, h, y = 14.6, 15.5, 22.5
    xs = [0.5 + i * 16.6 for i in range(len(ust))]
    for x, (b, a) in zip(xs, ust):
        kutu(x, y, w, h, b, a, MAVI)
    for x in xs[:-1]:
        ok(x + w + 0.3, y + h / 2, x + 16.6 - 0.3, y + h / 2)
    # judge → üretim geri besleme (kutuların altından yay)
    ax.add_patch(FancyArrowPatch((xs[3] + w / 2, y - 0.4), (xs[1] + w / 2, y - 0.4),
                                 connectionstyle="arc3,rad=-0.25", arrowstyle="-|>",
                                 mutation_scale=10, color=TURUNCU, lw=1.2, linestyle="--"))
    ax.text((xs[1] + xs[3] + w) / 2, y - 6.4, "ret / düzeltme döngüsü", ha="center", fontsize=7,
            color=TURUNCU)

    # İP2 sağdan sola akar: sürüm kutusunun altından başlar (yılan düzeni)
    ax.text(xs[-1] - 1.5, 15.6, "İP2 · Model geliştirme ve ince ayar", fontsize=9.5,
            fontweight="bold", color=CAMGOBEGI, ha="right")
    alt = [
        ("Chat template", "Gemma 4 template\nthinking korunur"),
        ("LoRA ince ayar", "bf16 LoRA\nMLX (yerel) · Unsloth (Colab)"),
        ("5 eksenli değerlendirme", "kalite · güvenlik · forgetting\ncontext · sycophancy\n→ bulgular İP1’e döner"),
        ("Model seçimi", "Pareto kuralı\ninsan + iki judge"),
        ("Teslim (İP3/İP4)", "model kartı · uç nokta\ngüvenlik katmanı notu"),
    ]
    w2, h2, y2 = 18.0, 13.0, 0.5
    xs2 = [99.5 - w2 - i * 20.0 for i in range(len(alt))]
    for x, (b, a) in zip(xs2, alt):
        kutu(x, y2, w2, h2, b, a, CAMGOBEGI)
    for x in xs2[:-1]:
        ok(x - 0.3, y2 + h2 / 2, x - 2.0 + 0.3, y2 + h2 / 2)
    # sürüm → template (dikey)
    ok(xs[-1] + w / 2, y - 0.4, xs[-1] + w / 2, y2 + h2 + 0.6, renk=GRI)
    ax.text(xs[-1] + w / 2 - 1.0, 19.6, "v0.1.x", ha="right", fontsize=7, color=IKINCIL)
    kaydet(fig, "s1-boru-hatti.png")


# --- Ş3 senaryo ve bağımlılık türü dağılımı ------------------------------------------

SENARYO_AD = {
    "ambivalans": "Ambivalans", "rol_siniri": "Rol sınırı", "nazikce_karsi_cikma": "Nazikçe karşı çıkma",
    "belirsiz": "Belirsiz (liste dışı)", "farkindalik": "Farkındalık", "inkar": "İnkâr",
    "hedef_belirleme": "Hedef belirleme", "kayma_nuks": "Kayma / nüks", "anlasilmama": "Anlaşılmama",
    "hukuki_kaygi": "Hukuki kaygı", "borc_finansal": "Borç / finansal", "durtu": "Dürtü",
    "kutlama": "Kutlama", "bilgilendirme": "Bilgilendirme", "kayip_kovalama": "Kayıp kovalama",
    "discord": "Uyumsuzluk (discord)", "motivasyon": "Motivasyon",
    "bilmiyorum_cikmazi": "«Bilmiyorum» çıkmazı", "kriz": "Kriz", "tetikleyici": "Tetikleyici",
}
TUR_AD = {"alkol": "Alkol", "tutun": "Tütün", "kumar": "Kumar", "receteli_ilac": "Reçeteli ilaç",
          "dijital": "Dijital", "madde": "Madde"}


def yatay_cubuk(ax, etiketler, degerler, renk, toplam):
    y = list(range(len(etiketler)))[::-1]
    ax.barh(y, degerler, color=renk, height=0.68, edgecolor="white", linewidth=1)
    ax.set_yticks(y, etiketler)
    ax.tick_params(axis="y", length=0)
    ust = max(degerler)
    for yi, d in zip(y, degerler):
        ax.text(d + ust * 0.015, yi, f"{d}  (%{tr_sayi(100 * d / toplam, 1)})", va="center",
                fontsize=7.4, color=METIN)
    ax.set_xlim(0, ust * 1.32)
    ax.xaxis.grid(True, color="#eeeeec", lw=0.6)
    ax.set_axisbelow(True)


def sekil_dagilim():
    m = json.loads(girdi("Ş3", "datasets/v0.1.0/manifest.json").read_text(encoding="utf-8"))
    sen = {k: v for k, v in m["scenario_counts"].items() if k != "genel"}  # genel = replay
    sen = sorted(sen.items(), key=lambda kv: -kv[1])
    tur = {k: v for k, v in m["addiction_type_counts"].items() if k in TUR_AD}
    tur = sorted(tur.items(), key=lambda kv: -kv[1])

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.9), gridspec_kw={"width_ratios": [1.5, 1]})
    yatay_cubuk(a1, [SENARYO_AD.get(k, k) for k, _ in sen], [v for _, v in sen], MAVI,
                sum(v for _, v in sen))
    a1.set_title(f"Senaryo (replay hariç, n={sum(v for _, v in sen)})", fontsize=9, loc="left",
                 color=METIN)
    yatay_cubuk(a2, [TUR_AD[k] for k, _ in tur], [v for _, v in tur], MAVI, sum(v for _, v in tur))
    a2.set_title(f"Bağımlılık türü (n={sum(v for _, v in tur)})", fontsize=9, loc="left",
                 color=METIN)
    fig.tight_layout()
    kaydet(fig, "s3-dagilim.png")
    return {"senaryo": dict(sen), "tur": dict(tur)}


# --- Ş4 sürümlerin gelişimi ------------------------------------------------------------

def surum_anahtari(ad):
    return tuple(int(x) for x in ad.lstrip("v").split("."))


def sekil_surumler():
    satirlar = []
    for d in sorted((KOK / "datasets").iterdir(), key=lambda p: surum_anahtari(p.name)):
        mf = d / "manifest.json"
        if not mf.exists():
            continue
        m = json.loads(girdi("Ş4", mf.relative_to(KOK)).read_text(encoding="utf-8"))
        kart = (d / "CARD.md").read_text(encoding="utf-8") if (d / "CARD.md").exists() else ""
        bas = "\n".join(kart.splitlines()[:12])
        deney = bool(re.search(r"DENEY|deney kolu", bas))
        n = m.get("n_kept", m.get("n_total"))
        satirlar.append((d.name, m["date"], n, deney))

    fig, ax = plt.subplots(figsize=(10, 3.6))
    x = list(range(len(satirlar)))
    renkler = [ACIK_GRI if de else (TURUNCU if ad.startswith("v0.1") else MAVI)
               for ad, _, _, de in satirlar]
    ax.bar(x, [n for _, _, n, _ in satirlar], color=renkler, width=0.72, edgecolor="white", lw=1)
    ax.set_xticks(x, [ad for ad, *_ in satirlar], rotation=60, ha="right", fontsize=7.2)
    for xi, (ad, tarih, n, de) in zip(x, satirlar):
        if not de and (ad in ("v0.0.1", "v0.0.2", "v0.0.6", "v0.0.8", "v0.0.15", "v0.0.18")
                       or ad.startswith("v0.1")):
            ax.text(xi, n + 25, f"{tr_sayi(n)}\n{tarih[5:].replace('-', '.')}", ha="center",
                    fontsize=6.6, color=METIN)
    ax.set_ylabel("Kayıt sayısı")
    ax.set_ylim(0, max(n for _, _, n, _ in satirlar) * 1.18)
    ax.yaxis.grid(True, color="#eeeeec", lw=0.6)
    ax.set_axisbelow(True)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=MAVI, label="Ana hat (v0.0.x)"),
                       Patch(color=TURUNCU, label="Kesinleşmiş araştırma sürümü (v0.1.x)"),
                       Patch(color=ACIK_GRI, label="Deney kolu (ana hatta girmez)")],
              loc="upper left", fontsize=7.2, frameon=False)
    fig.tight_layout()
    kaydet(fig, "s4-surumler.png")
    return satirlar


# --- İP2 şekilleri ------------------------------------------------------------------------

def md_tablo(metin, baslik_deseni):
    """Rapordaki `baslik_deseni` ile başlayan ilk markdown tablosunun satırlarını döndürür."""
    satirlar = metin.splitlines()
    i = next(k for k, s in enumerate(satirlar) if s.startswith("|") and re.search(baslik_deseni, s))
    tablo = []
    for s in satirlar[i + 2:]:
        if not s.startswith("|"):
            break
        tablo.append([h.strip() for h in s.strip().strip("|").split("|")])
    return tablo


def sekil_lora():
    """Sol: katman sayısı ↔ kriz puanı (uçurum haritası). Sağ: yönlendirme dozu ↔ yönlendirmesiz öğe."""
    ucurum = girdi("Ş5", "reports/analiz/2026-09-17-ucurum-haritasi.md").read_text(encoding="utf-8")
    satir = md_tablo(ucurum, r"katman \| kesilen")
    noktalar = []
    for h in satir:
        ad = h[0].replace("*", "").strip()
        if "max_tokens" in ad:
            continue
        yuzde = int(re.search(r"%(\d+)", h[3]).group(1))
        noktalar.append((0 if "ham" in ad else int(ad), yuzde))
    doz = json.loads(girdi("Ş5", "reports/analiz/2026-09-15-f4c-doz-egrisi.json").read_text(encoding="utf-8"))

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.7))
    taban = next(v for k, v in noktalar if k == 0)
    katman = [(k, v) for k, v in noktalar if k]
    a1.axhline(taban, color=GRI, lw=1, ls="--")
    a1.text(katman[-1][0], taban + 2, f"eğitilmemiş model %{taban}", ha="right", fontsize=7.4,
            color=IKINCIL)
    a1.plot([k for k, _ in katman], [v for _, v in katman], color=MAVI, lw=2, marker="o", ms=5)
    for k, v in katman:
        a1.text(k, v + 3, f"%{v}", ha="center", fontsize=7.4, color=METIN)
    a1.axvspan(12, 13, color=TURUNCU, alpha=0.12, lw=0)
    a1.text(13.15, 30, "12 → 13 arası\nçöküş", ha="left", fontsize=7.4, color=TURUNCU)
    a1.set_xticks([k for k, _ in katman])
    a1.set_xlabel("LoRA uygulanan üst katman sayısı (q_proj, rank 8)")
    a1.set_ylabel("Kriz dilimi puanı (kesilmeyenlerde, %)")
    a1.set_ylim(0, 85)
    a1.set_title("a) Katman derinliği ↔ kriz davranışı (E4B, v0.0.8)", fontsize=9, loc="left",
                 color=METIN)

    anahtar = [("v0.0.3_duzeltilmis", "v0.0.3"), ("doz10_duzeltilmis", "v0.0.4"),
               ("doz25_duzeltilmis", "v0.0.5")]
    xs = [float(re.search(r"%([\d,]+)", doz["dozlar"][s]).group(1).replace(",", ".")) for _, s in anahtar]
    renk = [MAVI, TURUNCU, CAMGOBEGI, "#eda100", "#6250d6"]
    son = {}
    for (kol, d), r in zip(doz["egri"].items(), renk):
        ys = [d[a] for a, _ in anahtar]
        a2.plot(xs, ys, color=r, lw=2, marker="o", ms=5)
        son.setdefault(ys[-1], []).append(kol)
    for y, kollar in son.items():
        a2.text(xs[-1] + 0.6, y, " · ".join(kollar), va="center", fontsize=7.4, color=METIN)
    a2.axhline(doz["taban"]["yonlendirme_yok"], color=GRI, lw=1, ls="--")
    a2.text(xs[0], doz["taban"]["yonlendirme_yok"] + 0.4, "eğitilmemiş model", fontsize=7.4,
            color=IKINCIL)
    a2.set_xticks(xs, [f"%{tr_sayi(x, 1)}" for x in xs])
    a2.set_xlim(3, 30)
    a2.set_ylim(0, 16)
    a2.set_xlabel("Eğitim verisinde yönlendirme içeren kayıt payı")
    a2.set_ylabel("Yönlendirmesiz cevap (16 öğede)")
    a2.set_title("b) Yönlendirme dozu ↔ yönlendirme kaybı (5 LoRA kolu)", fontsize=9, loc="left",
                 color=METIN)
    for a in (a1, a2):
        a.yaxis.grid(True, color="#eeeeec", lw=0.6)
        a.set_axisbelow(True)
    fig.tight_layout()
    kaydet(fig, "s5-lora-katman-doz.png")
    return {"ucurum": noktalar, "doz_x": xs,
            "doz": {k: [d[a] for a, _ in anahtar] for k, d in doz["egri"].items()}}


T311 = "reports/analiz/2026-10-20-taban-vs-ince-basit-inceleme.md"


def sekil_t311_kazanan():
    metin = girdi("Ş6", T311).read_text(encoding="utf-8")
    satir = md_tablo(metin, r"kaynak \| ince \| taban")
    adlar = {"insan": "İnsan", "gemma": "Gemma-4-31B judge", "qwen": "Qwen3.8-27B judge",
             "jüri": "Jüri (iki judge uyuşursa)"}

    def ad(h):
        bas, _, kalan = h.partition(" ")
        return f"{adlar.get(bas, bas)} {kalan}".strip()

    veri = [(ad(h[0]), int(h[1]), int(h[3]), int(h[2]), h[4].replace(".", ",")) for h in satir]
    fig, ax = plt.subplots(figsize=(10, 2.9))
    for i, (ad, ince, esit, taban, p) in enumerate(veri[::-1]):
        n = ince + esit + taban
        sol = 0
        for deger, renk in ((ince, CAMGOBEGI), (esit, ACIK_GRI), (taban, MAVI)):
            ax.barh(i, 100 * deger / n, left=sol, color=renk, height=0.62, edgecolor="white", lw=2)
            if deger:
                ax.text(sol + 100 * deger / n / 2, i, str(deger), ha="center", va="center",
                        fontsize=7.6, color=METIN if renk == ACIK_GRI else "white", fontweight="bold")
            sol += 100 * deger / n
        ax.text(101.5, i, f"p = {p}", va="center", fontsize=7.6, color=IKINCIL)
    ax.set_yticks(range(len(veri)), [v[0] for v in veri[::-1]])
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 112)
    ax.set_xticks([0, 25, 50, 75, 100], ["%0", "%25", "%50", "%75", "%100"])
    ax.spines["left"].set_visible(False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=CAMGOBEGI, label="İnce ayarlı model daha iyi"),
                       Patch(color=ACIK_GRI, label="Eşit"),
                       Patch(color=MAVI, label="Taban model daha iyi")],
              loc="upper center", bbox_to_anchor=(0.45, 1.2), ncol=3, fontsize=7.6, frameon=False)
    fig.tight_layout()
    kaydet(fig, "s6-taban-ince.png")
    return veri


def sekil_t311_risk():
    metin = girdi("Ş7", T311).read_text(encoding="utf-8")
    satir = md_tablo(metin, r"öğe \| sonda \| taban \| ince")
    fig, ax = plt.subplots(figsize=(10, 2.0))
    for j, (ad, kol) in enumerate((("Taban", 2), ("İnce", 3))):
        for i, h in enumerate(satir):
            var = h[kol] == "✓"
            kayip = h[2] == "✓" and h[3] != "✓"
            ax.scatter(i, 1 - j, s=150, marker="o",
                       color=(MAVI if j == 0 else CAMGOBEGI) if var else "white",
                       edgecolor=(TURUNCU if (kayip and j == 1) else
                                  ((MAVI if j == 0 else CAMGOBEGI) if var else GRI)),
                       linewidth=2.2 if (kayip and j == 1) else 1.2, zorder=3)
    for i, h in enumerate(satir):
        if h[2] == "✓" and h[3] != "✓":
            ax.text(i, -0.55, "kayıp", ha="center", fontsize=7, color=TURUNCU)
    ax.set_xticks(range(len(satir)), [h[0] for h in satir], rotation=0, fontsize=7.2)
    ax.set_yticks([1, 0], ["Taban", "İnce ayarlı"])
    ax.set_ylim(-0.8, 1.6)
    ax.set_xlim(-0.6, len(satir) - 0.4)
    for k in ("left", "bottom"):
        ax.spines[k].set_visible(False)
    ax.tick_params(length=0)
    ax.text(-0.6, 1.45, "● dolu: cevapta yönlendirme var   ○ boş: yok   turuncu halka: tabanda var, incede yok",
            fontsize=7.4, color=IKINCIL)
    fig.tight_layout()
    kaydet(fig, "s7-risk-yonlendirme.png")
    return [(h[0], h[2], h[3]) for h in satir]


def sekil_gecikme():
    """Tek istek yanıt süresi: thinking beklemesi + görünen cevabın akışı (ortancalar), 2 sn hedef çizgisi."""
    import statistics as st
    kollar = [("taban-dusunme", "Taban, thinking açık"), ("ince-dusunme", "İnce ayarlı, thinking açık"),
              ("ince-dusunmesiz", "İnce ayarlı, thinking kapalı")]
    veri = []
    for dosya, ad in kollar:
        yol = girdi("Ş8", f"birag-rapor-olcum/gecikme/{dosya}.jsonl")
        R = [json.loads(x) for x in yol.read_text(encoding="utf-8").splitlines() if x.strip()]
        veri.append((ad, st.median(r["ilk_jeton_sn"] for r in R), st.median(r["cevap_bas_sn"] for r in R),
                     st.median(r["toplam_sn"] for r in R), len(R)))

    fig, ax = plt.subplots(figsize=(10, 2.6))
    for i, (ad, ilk, bas, top, n) in enumerate(veri[::-1]):
        ax.barh(i, bas, color=ACIK_GRI, height=0.55, edgecolor="white", lw=1)
        ax.barh(i, top - bas, left=bas, color=CAMGOBEGI if "İnce" in ad else MAVI, height=0.55,
                edgecolor="white", lw=1)
        ax.text(top + 2, i, f"toplam {tr_sayi(top, 1)} sn · cevap {tr_sayi(bas, 2 if bas < 10 else 1)} sn'de başlıyor",
                va="center", fontsize=7.6, color=METIN)
    ax.axvline(2, color=TURUNCU, lw=1.2, ls="--")
    ax.text(2.8, len(veri) - 0.45, "2 sn hedefi", fontsize=7.4, color=TURUNCU)
    ax.set_yticks(range(len(veri)), [v[0] for v in veri[::-1]])
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Saniye (ortanca, tek istek, 48 soru)")
    ax.set_xlim(0, max(v[3] for v in veri) * 1.55)
    ax.xaxis.grid(True, color="#eeeeec", lw=0.6)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=ACIK_GRI, label="Thinking bitene kadar bekleme"),
                       Patch(color=CAMGOBEGI, label="Görünen cevabın akışı (ince ayarlı)"),
                       Patch(color=MAVI, label="Görünen cevabın akışı (taban)")],
              loc="lower right", fontsize=7.2, frameon=False)
    fig.tight_layout()
    kaydet(fig, "s8-gecikme.png")
    return veri


def main():
    sekil_boru_hatti()
    dag = sekil_dagilim()
    sur = sekil_surumler()
    lora = sekil_lora()
    kaz = sekil_t311_kazanan()
    risk = sekil_t311_risk()
    gec = sekil_gecikme()

    tarih = dt.date.today().isoformat()
    satir = [f"# Gelişme raporu şekilleri\n",
             f"- Betik: `scripts/analiz/2026-10-21-rapor-sekiller.py` · tarih: {tarih}",
             f"- Çıktı: `reports/analiz/sekiller/*.png`\n", "## Girdiler\n",
             "| Şekil | Girdi | SHA256-16 |", "|---|---|---|"]
    for s, y, h in GIRDILER:
        satir.append(f"| {s} | `{y}` | `{h}` |")
    satir += ["", "## Ş3 · v0.1.0 dağılımı (şekildeki sayılar)", "",
              "| Senaryo | n |", "|---|---:|"]
    satir += [f"| {SENARYO_AD.get(k, k)} | {v} |" for k, v in dag["senaryo"].items()]
    satir += ["", "| Tür | n |", "|---|---:|"]
    satir += [f"| {TUR_AD[k]} | {v} |" for k, v in dag["tur"].items()]
    satir += ["", "## Ş4 · sürümler", "", "| Sürüm | Tarih | Kayıt | Deney kolu |", "|---|---|---:|---|"]
    satir += [f"| {a} | {t} | {n} | {'evet' if d else ''} |" for a, t, n, d in sur]
    satir += ["", "## Ş5 · LoRA derinliği ve doz", "", "| Katman (0 = eğitilmemiş) | Kriz puanı % |", "|---:|---:|"]
    satir += [f"| {k} | {v} |" for k, v in lora["ucurum"]]
    satir += ["", "| Kol | " + " | ".join(f"%{tr_sayi(x, 1)}" for x in lora["doz_x"]) + " |",
              "|---|" + "---:|" * len(lora["doz_x"])]
    satir += [f"| {k} | " + " | ".join(str(v) for v in vs) + " |" for k, vs in lora["doz"].items()]
    satir += ["", "## Ş6 · taban ↔ ince kazanan", "", "| Kaynak | İnce | Eşit | Taban | p |", "|---|---:|---:|---:|---|"]
    satir += [f"| {a} | {i} | {e} | {t} | {p} |" for a, i, e, t, p in kaz]
    satir += ["", "## Ş7 · 15 risk öğesinde yönlendirme", "", "| Öğe | Taban | İnce |", "|---|:-:|:-:|"]
    satir += [f"| {a} | {t} | {i} |" for a, t, i in risk]
    satir += ["", "## Ş8 · tek istek yanıt süresi (ortanca, sn)", "",
              "| Kol | n | İlk token | Görünen cevabın başlaması | Toplam |", "|---|---:|---:|---:|---:|"]
    satir += [f"| {a} | {n} | {tr_sayi(i, 2)} | {tr_sayi(b, 2)} | {tr_sayi(t, 2)} |" for a, i, b, t, n in gec]
    RAPOR.write_text("\n".join(satir) + "\n", encoding="utf-8")
    print(RAPOR.relative_to(KOK))


if __name__ == "__main__":
    main()
