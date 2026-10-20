#!/usr/bin/env python3
"""İP1 başarı ölçütleri — gelişme raporu (dönem 0–12. ay) için.

Başvuru formu İP1 ölçütleri (s.3 · s.16) ve bu betiğin onları nasıl ölçtüğü:
  1. 10.000 talimat örneği          → dondurulmuş sürümlerin ve sürmekte olan ölçek-5k'nın kayıt sayısı
  2. %90 hedef senaryolarla uyumlu   → (a) üretilen adayların bütün kapılardan geçme oranı (manifest)
     ve doğru biçimlendirilmiş         (b) son sürümde senaryo alanının kanonik listede olma oranı
                                       (c) son sürümde `run_checks` geçme oranı
  3. %95 dil modeliyle uyumlu        → şema (TrainRecord) + konuşma yapısı + eğitim chat template'inin
                                       kaydı hatasız işlemesi + son asistan turunda düşünce
  4. %100 etik ve anonim             → kişisel veri deseni taraması (e-posta, telefon, TC kimlik, IBAN,
                                       kart, URL, adres, doğum tarihi) + §15 sert yasak ifade + kriz kaydı
  (%70 Türkçe olumlu değerlendirme bu betikte yeniden hesaplanmaz: uzman puanlaması raporuna atıf.)

⚠️ Kişi adı taraması YOK: ad listesi uydurmak gerekirdi (Kural 3). Veri sentetik; adlar varsa kurgusal.
⚠️ Jeton uzunluğu burada ölçülmez (tokenizer bu makinede yok); Colab eğitimi her kaydı
   `src/colab_egitim.py:uzunluk_denetle` ile 2048 jetona karşı denetliyor ve aşanı durduruyor.

Girdi : datasets/v0.1.0/{train.jsonl,manifest.json} · datasets/v0.1.1/train.jsonl
        data/candidates/olcek5k/kayit/*.jsonl (anlık — koşu sürüyor) · configs/taxonomy.yaml
        configs/chat_template_train.jinja
Çıktı : reports/analiz/2026-10-20-ip1-olcutler.md
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import jinja2
import yaml

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from checks import SERT_KATEGORILER, run_checks, scan_forbidden, schema_valid, turn_structure_ok  # noqa: E402
from train import to_mlx_messages  # noqa: E402

SURUMLER = ("v0.1.0", "v0.1.1")
SON = "v0.1.1"
OLCEK5K = KOK / "data/candidates/olcek5k/kayit"
TAKSONOMI = KOK / "configs/taxonomy.yaml"
SABLON = KOK / "configs/chat_template_train.jinja"
RAPOR = KOK / "reports/analiz/2026-10-20-ip1-olcutler.md"
HEDEF_HACIM = 10_000

# Kişisel veri desenleri. Hepsi DAR yazıldı: geniş desen (ör. her 3+ hane) sentetik metindeki
# yaş, süre, para gibi masum sayıları yakalar ve oranı anlamsızlaştırır. Geniş rakam taraması
# ayrıca `checks.detect_number_candidates` ile raporlanır.
PII = {
    "e-posta": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "URL": r"https?://\S+|www\.\S+",
    "cep telefonu": r"(?<!\d)(?:\+?90[\s-]?)?0?5\d{2}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}(?!\d)",
    "sabit telefon": r"(?<!\d)0?[234]\d{2}[\s-]\d{3}[\s-]?\d{2}[\s-]?\d{2}(?!\d)",
    "TC kimlik (11 hane)": r"(?<!\d)[1-9]\d{10}(?!\d)",
    "IBAN": r"\bTR\d{2}[\s]?(?:\d{4}[\s]?){5}\d{2}\b",
    "kart numarası": r"(?<!\d)(?:\d{4}[\s-]?){3}\d{4}(?!\d)",
    "adres": r"[Mm]ahallesi|\b[Nn]o\s?:\s?\d|\b[Dd]aire\s?:?\s?\d|\b[Aa]pt\.",
    "doğum tarihi biçimi": r"(?<!\d)\d{1,2}[./]\d{1,2}[./](?:19|20)\d{2}(?!\d)",
}


# Öz-sınama: sıfır eşleşme «temiz» mi yoksa «desen kör» mü — ayırt etmek için her desen bilinen bir
# örneği yakalamalı, masum bir sentetik cümleyi yakalamamalı.
PII_ORNEK = {
    "e-posta": ("bana ali.k@ornek.com yaz", "bunu e-posta ile soracağım"),
    "URL": ("https://ornek.org/x bak", "web sitesine baktım"),
    "cep telefonu": ("numaram 0532 123 45 67", "25 yaşındayım, 3 yıldır içiyorum"),
    "sabit telefon": ("0262 303 10 00 arayın", "saat 23 30 gibi uyudum"),
    "TC kimlik (11 hane)": ("kimlik 10000000146", "1000 lira borç"),
    "IBAN": ("TR33 0006 1005 1978 6457 8413 26", "TR ile başlayan bir şey"),
    "kart numarası": ("4111 1111 1111 1111", "2024 yılında 4 kez denedim"),
    "adres": ("Yenimahalle Cumhuriyet mahallesi no: 5", "sokakta yürüdüm"),
    "doğum tarihi biçimi": ("12.05.1990 doğumluyum", "12.05 gibi çıktım"),
}


def pii_oz_sinama() -> None:
    for ad, (yakala, yakalama) in PII_ORNEK.items():
        assert pii_eslesme(PII[ad], ad, yakala), f"desen kör: {ad}"
        assert not pii_eslesme(PII[ad], ad, yakalama), f"desen masum metni yakalıyor: {ad}"


def jl(p: Path) -> list[dict]:
    return [json.loads(x) for x in p.open(encoding="utf-8") if x.strip()]


def sha16(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def yuzde(a: int, b: int) -> str:
    return f"%{100 * a / b:.1f}" if b else "—"


def tc_gecerli(s: str) -> bool:
    d = [int(c) for c in s]
    return d[9] == ((d[0] + d[2] + d[4] + d[6] + d[8]) * 7 - (d[1] + d[3] + d[5] + d[7])) % 10 \
        and d[10] == sum(d[:10]) % 10


def metinler(r: dict) -> list[str]:
    return [x for m in r["messages"] for x in (m.get("content"), m.get("thinking")) if x]


def pii_eslesme(desen: str, ad: str, t: str) -> list[re.Match]:
    # Büyük/küçük harf desenin içinde açıkça yazılı ([Mm]…): re.I Türkçe İ/ı'da güvenilmez (Kural 4)
    return [m for m in re.finditer(desen, t) if not ad.startswith("TC") or tc_gecerli(m.group(0))]


def pii_bul(r: dict) -> list[tuple[str, str]]:
    """(desen adı, bağlamlı alıntı) — kaydın bütün mesaj ve düşüncelerinde."""
    return [(ad, t[max(0, m.start() - 40):m.end() + 40])
            for ad, desen in PII.items() for t in metinler(r) for m in pii_eslesme(desen, ad, t)]


def ilk_dusen_kapi(k: dict) -> str:
    return next((a for a, v in k.items() if (a.endswith("_ok") or a == "schema_valid") and v is False), "diğer")


def sablon_yukle() -> jinja2.Template:
    env = jinja2.Environment(extensions=["jinja2.ext.loopcontrols"])

    def hata(msg):
        raise jinja2.TemplateError(msg)

    env.globals["raise_exception"] = hata
    return env.from_string(SABLON.read_text(encoding="utf-8"))


def lm_uyumu(r: dict, sablon: jinja2.Template) -> list[str]:
    """Kaydı dil modeline uygunsuz kılan sebepler; boşsa uyumlu."""
    neden = []
    if not schema_valid(r)[0]:
        neden.append("şema")
    elif not turn_structure_ok(r)[0]:
        neden.append("konuşma yapısı")
    else:
        son = [m for m in r["messages"] if m["role"] == "assistant"][-1]
        try:
            # Eğitimle AYNI dönüşüm: düşünce son asistan turuna gömülür (train.py, Colab da bunu çağırıyor)
            metin = sablon.render(messages=to_mlx_messages(r)["messages"], add_generation_prompt=False,
                                  bos_token="<bos>")
            if son["content"].strip() not in metin:
                neden.append("şablon son cevabı düşürdü")
            if r.get("has_thinking") and (son.get("thinking") or "").strip() not in metin:
                neden.append("şablon düşünceyi düşürdü")
        except jinja2.TemplateError as e:
            neden.append(f"şablon hatası: {str(e)[:60]}")
        if r.get("has_thinking") and not (son.get("thinking") or "").strip():
            neden.append("düşünce beyanı var, düşünce yok")
    return neden


def main() -> None:
    pii_oz_sinama()
    girdiler = [KOK / f"datasets/{v}/train.jsonl" for v in SURUMLER] + [KOK / "datasets/v0.1.0/manifest.json",
                                                                       TAKSONOMI, SABLON]
    veri = {v: jl(KOK / f"datasets/{v}/train.jsonl") for v in SURUMLER}
    son = veri[SON]
    manifest = json.loads((KOK / "datasets/v0.1.0/manifest.json").read_text(encoding="utf-8"))
    kanonik = set(yaml.safe_load(TAKSONOMI.read_text(encoding="utf-8"))["senaryo"]["kanonik"])
    sablon = sablon_yukle()

    # ── 1. hacim
    o5 = sorted(OLCEK5K.glob("*.jsonl"))
    o5_say = sum(1 for p in o5 for x in p.open(encoding="utf-8") if x.strip())
    o5_asama = Counter(p.name.split(".")[-2] for p in o5)

    # ── 2. senaryo ve biçim
    neden_dus = Counter(d["reason"] for d in manifest["dropped"])
    terapotik = [r for r in son if not r.get("replay")]
    sen = Counter(r["scenario"] for r in terapotik)
    kanonikte = sum(n for s, n in sen.items() if s in kanonik)
    disari = {s: n for s, n in sen.items() if s not in kanonik}
    kapi = [run_checks(r) for r in son]
    kapi_gecen = sum(k["passed"] for k in kapi)
    kapi_dusen = Counter(ilk_dusen_kapi(k) for k in kapi if not k["passed"])

    # ── 3. dil modeli uyumu
    lm = {v: [lm_uyumu(r, sablon) for r in veri[v]] for v in SURUMLER}

    # ── 4. etik ve anonim
    pii_say, pii_ornek, temiz = Counter(), {}, Counter()
    for v in SURUMLER:
        for r in veri[v]:
            bulunan = pii_bul(r)
            temiz[v] += not bulunan
            for ad, alinti in bulunan:
                pii_say[(v, ad)] += 1
                pii_ornek.setdefault(ad, f"{r['id']}: …{alinti}…")
    sert = Counter()
    for r in son:
        for m in r["messages"]:
            if m["role"] == "assistant":
                for kat, ifadeler in scan_forbidden(m["content"]).items():
                    if kat in SERT_KATEGORILER:
                        sert[kat] += len(ifadeler)
    kriz = sum(bool(r.get("is_crisis")) for r in son)

    L = ["# İP1 başarı ölçütleri — gelişme raporu (0–12. ay)", "",
         f"- Betik: `scripts/analiz/{Path(__file__).name}` · tarih 2026-10-20",
         "- Ölçüt kaynağı: başvuru formu İP1 (s.3 Tablo 1 · s.16 iş-zaman çizelgesi); eşleme `docs/rapor/oneri-rapor-esleme.md`",
         "- Girdiler (SHA256-16):", ""]
    L += [f"  - `{p.relative_to(KOK)}` `{sha16(p)}`" for p in girdiler]
    L += [f"  - `{OLCEK5K.relative_to(KOK)}/*.jsonl` — {len(o5)} parça, **anlık** (koşu sürüyor; SHA yok, sayı bitince değişir)",
          "", "## 1. Hacim — hedef 10.000 talimat örneği", "",
          "| küme | kayıt | durum |", "|---|---:|---|"]
    for v in SURUMLER:
        L.append(f"| `datasets/{v}` | {len(veri[v])} | dondurulmuş |")
    L += [f"| ölçek-5k ara kayıtları | {o5_say} | üretimde · aşama dağılımı {dict(o5_asama)} · plan 5000 |", "",
          f"Dondurulmuş benzersiz kayıt: **{len(son)}** ({yuzde(len(son), HEDEF_HACIM)} / 10.000). "
          f"`v0.1.1`, `v0.1.0`'ın aynı kayıtlarıdır (düşünce yeniden kuruldu) — toplanmaz. "
          f"Ölçek-5k tamamlanıp donarsa toplam ≈ {len(son) + 5000} olur.", "",
          "## 2. Hedef senaryolarla uyum ve doğru biçim — hedef %90", "",
          f"**(a) Üretilen adayların kapılardan geçme oranı** (`v0.1.0` manifest): {manifest['n_kept']} / "
          f"{manifest['n_total']} = **{yuzde(manifest['n_kept'], manifest['n_total'])}**. "
          f"Elenme sebepleri: {dict(neden_dus)}", "",
          f"**(b) Senaryo alanı kanonik listede** (`{SON}`, replay hariç {len(terapotik)} kayıt): "
          f"{kanonikte} = **{yuzde(kanonikte, len(terapotik))}**. Liste dışı: {disari}. "
          "`belirsiz` = tohum açılış mesajı, arketip üretim zamanında seçilmedi (K37); ayrı bir senaryo değil.", "",
          f"**(c) Son sürümde bütün deterministik kapılar** (`run_checks`): {kapi_gecen} / {len(son)} = "
          f"**{yuzde(kapi_gecen, len(son))}**" + (f" · ilk düşen kapı: {dict(kapi_dusen)}" if kapi_dusen else ""), "",
          "Senaryo dağılımı (replay hariç):", "", "| senaryo | kayıt |", "|---|---:|"]
    L += [f"| {s}{'' if s in kanonik else ' *(liste dışı)*'} | {n} |" for s, n in sen.most_common()]
    L += ["", "## 3. Dil modeliyle uyum — hedef %95", "",
          "Uyumlu = şema (`TrainRecord`) + konuşma yapısı + eğitim chat template'i (`configs/chat_template_train.jinja`, K44) "
          "kaydı hatasız işliyor ve son cevabı/düşünceyi koruyor + düşünce beyanı olan kayıtta düşünce dolu.", "",
          "| sürüm | uyumlu | oran | uyumsuzluk sebepleri |", "|---|---:|---:|---|"]
    for v in SURUMLER:
        iyi = sum(not n for n in lm[v])
        L.append(f"| `{v}` | {iyi} / {len(lm[v])} | **{yuzde(iyi, len(lm[v]))}** | "
                 f"{dict(Counter(x for n in lm[v] for x in n)) or '—'} |")
    L += ["", "⚠️ Jeton uzunluğu (≤ 2048) bu makinede ölçülmedi; Colab eğitimi aşan kaydı durdurur (`src/colab_egitim.py`).", "",
          "## 4. Etik ve anonim — hedef %100", "",
          "Kişisel veri desen taraması — bütün mesajlar ve düşünceler:", "",
          "| desen | " + " | ".join(f"`{v}`" for v in SURUMLER) + " |", "|---|" + "---:|" * len(SURUMLER)]
    for ad in PII:
        L.append(f"| {ad} | " + " | ".join(str(pii_say[(v, ad)]) for v in SURUMLER) + " |")
    L += ["", "Desenler her koşuda öz-sınamadan geçer (bilinen bir örneği yakalar, masum bir cümleyi yakalamaz) — "
          "sıfır, desenin kör olduğu anlamına gelmez.", "", "Desen taşımayan kayıt: " + " · ".join(f"`{v}` {temiz[v]} / {len(veri[v])} = **{yuzde(temiz[v], len(veri[v]))}**"
                                                     for v in SURUMLER), ""]
    if pii_ornek:
        L += ["Eşleşmelerden birer örnek (elle okunmalı — sentetik metinde kurgusal olabilir):", ""]
        L += [f"- {ad}: `{o.replace(chr(10), ' ').replace('`', '')}`" for ad, o in pii_ornek.items()]
        L.append("")
    L += [f"- §15 **sert** yasak ifade (`{', '.join(sorted(SERT_KATEGORILER))}`) asistan turlarında, `{SON}`: **{sum(sert.values())}**",
          f"- Kriz kaydı (`is_crisis`): **{kriz}** — kriz dilimi uzman ve etik onayına kadar bilerek üretilmedi (Kural 3).",
          "- Veri tamamen sentetik: gerçek kişi, hasta kaydı ya da forum metni yok (form Tablo 3'teki bu iki kaynak "
          "etik onay beklediği için kullanılmadı). Uzman korpusu eğitim satırı olarak kullanılmadı (K20).",
          "- ⚠️ Kişi adı taraması yapılmadı (bkz. betik başlığı).", "",
          "## 5. %70 Türkçe olumlu değerlendirme", "",
          "Bu betikte yeniden hesaplanmadı. Kaynak: `reports/analiz/2026-09-14-uzman-puanlama-analizi.md` "
          "(uzman puanlaması, 50/70 kayıt, K58).", ""]
    RAPOR.write_text("\n".join(L), encoding="utf-8")
    print(f"yazıldı: {RAPOR.relative_to(KOK)}")


if __name__ == "__main__":
    main()
