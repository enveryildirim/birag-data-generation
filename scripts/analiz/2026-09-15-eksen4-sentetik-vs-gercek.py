#!/usr/bin/env python3
"""Eksen 4: jenerik sentetik pasaj vs gerçek A katmanı pasajı.

Soru: `context_fidelity` bağlam sadakatini ofis binası metinleriyle ölçüyor
(36/36 sentetik: otopark yönergesi, yemekhane duyurusu). Aynı davranışlar gerçek
kurum metniyle ölçülünce ne oluyor?

⚠️ BU BİR A/B DEĞİL. Sorular ve pasajlar farklı; öğe öğe eşleşme yok. Ham sayıların
karşılaştırılması YANILTICI — aşağıda önce ham tablo, sonra ayıklama var ve asıl
sonuç ayıklamada.

Girdi : reports/analiz/eksen-kosu/*-cf-sentetik · *-cf-gercek
Çıktı : reports/analiz/2026-09-15-eksen4-sentetik-vs-gercek.md
"""
from __future__ import annotations

import collections
import json
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
SENT = KOK / "reports/analiz/eksen-kosu/20260915-160933-cf-sentetik/sonuclar.jsonl"
GERC = KOK / "reports/analiz/eksen-kosu/20260915-161352-cf-gercek/sonuclar.jsonl"
CIKTI = KOK / "reports/analiz/2026-09-15-eksen4-sentetik-vs-gercek.md"

# Gerçek setin DÜŞEN öğelerinin elle ayıklaması. Benim yargım; betiğe gömülü.
AYIKLAMA = {
    "cfr-004": ("model", "Pasajı aktarıyor ama **«beş gün»ü düşürüyor** — somut ayrıntıyı taşımıyor. Gerçek grounding zaafı."),
    "cfr-012": ("model", "**Uyduruyor:** «Standart bir süre yoktur» pasajda yok, bir olgu iddiası."),
    "cfr-005": ("rol", "⭐ Pasajda **duran** yordamı aktarmak yerine *«Ben bir avukat değilim»* diyip reddediyor."),
    "cfr-007": ("izin", "*«Bu konu hakkında sana bilgi vermemi ister misin?»* — system prompt'un emrettiği izin sorusu."),
    "cfr-009": ("izin", "Netleştirme sorusu soruyor: *«sosyal destek mi, yükümlülük mü?»*"),
    "cfr-013": ("izin", "Netleştirme sorusu: *«Hangi testten bahsettiğinizi açar mısınız?»*"),
    "cfr-011": ("alet", "Davranış **doğru** — *«ilgili bir detay yok»* diyor. Benim yokluk listemde o ifade yok."),
    "cfr-015": ("alet", "Rol sınırıyla reddediyor (*«hukuki tavsiye veremem»*) — geçerli bir «bu pasajdan cevaplayamam». Listemde yok."),
}
ETIKET = {"model": "gerçek model kusuru", "rol": "rol sınırı fazla-reddi",
          "izin": "izin/netleştirme sorusu (system prompt)", "alet": "benim iddia listem dar"}


def oku(yol):
    return [json.loads(l) for l in yol.read_text(encoding="utf-8").splitlines() if l.strip()]


def dilim_tablo(kayitlar, dilimler):
    d = collections.defaultdict(lambda: [0, 0])
    for r in kayitlar:
        if r["dilim"] not in dilimler:
            continue
        d[r["dilim"]][1] += 1
        d[r["dilim"]][0] += bool(r["otomatik_gecti"])
    return d


def main() -> None:
    s, g = oku(SENT), oku(GERC)
    ORTAK = {"yeterli", "distractor", "yetersiz"}
    ds, dg = dilim_tablo(s, ORTAK), dilim_tablo(g, ORTAK)
    ts = sum(v[0] for v in ds.values()), sum(v[1] for v in ds.values())
    tg = sum(v[0] for v in dg.values()), sum(v[1] for v in dg.values())

    dusen = [r["id"] for r in g if not r["otomatik_gecti"]]
    grup = collections.Counter(AYIKLAMA.get(i, ("?", ""))[0] for i in dusen)

    sat = [
        "# Eksen 4 — jenerik sentetik pasaj vs gerçek A katmanı pasajı",
        "",
        f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
        f"**Koşular:** `{SENT.parent.name}` · `{GERC.parent.name}` — aynı model "
        "(`gemma-4-E4B-it-bf16-train`, adapter yok), aynı koşucu, `thinking=kapalı` (K108)",
        "",
        "---",
        "",
        "## 1. Soru",
        "",
        "`evals/context_fidelity.jsonl` Eksen 4'ü ölçüyor ama **36 pasajın 36'sı sentetik**",
        "ve hepsi jenerik ofis metni: *otopark yönergesi, yemekhane duyurusu, bina duyurusu*.",
        "Yani bağlam sadakati **alan içeriği olmadan** ölçülüyor. Gerçek kurum metniyle",
        "(YEDAM · ALO 191 · Denetimli Serbestlik) aynı davranışlar ne yapıyor?",
        "",
        "⚠️ **Bu bir A/B değil, paralel set.** Sorular da pasajlar da farklı. `celiskili`",
        "dilimi gerçek sette **yok**: gerçek kurum belgeleri birbiriyle çelişmiyor ve çelişki",
        "kurmak pasajı sentetikleştirirdi (plan.md §17.6 bunu öngörüyordu). Karşılaştırma",
        "ortak üç dilimin 15 öğesi üzerinden.",
        "",
        "## 2. Ham tablo — ve neden tek başına yanıltıcı",
        "",
        "| dilim | sentetik (jenerik ofis) | gerçek (A katmanı) |",
        "|---|---|---|",
        *[f"| {d} | {ds[d][0]}/{ds[d][1]} | {dg[d][0]}/{dg[d][1]} |" for d in sorted(ORTAK)],
        f"| **toplam** | **{ts[0]}/{ts[1]}** | **{tg[0]}/{tg[1]}** |",
        "",
        f"Ham okuma *«gerçek pasajla {ts[0]}/{ts[1]} → {tg[0]}/{tg[1]}'e düştü»* derdi. **Bu okuma yanlış olur:**",
        "iki setin iddia listelerini farklı kişiler yazdı ve benimkiler daha dar. Düşen sekiz",
        "öğenin **hepsi** bir `herhangi_biri` (varlık) iddiasından düştü — `golden_checks.py`'nin",
        "*\"Türkçe serbest metinde varlık iddiası yanlış negatif üretir\"* uyarısının tam kendisi.",
        "",
        "## 3. Ayıklama — düşen 8 öğe elle okundu",
        "",
        "| grup | öğe |",
        "|---|---|",
        *[f"| {ETIKET.get(k, k)} | **{n}** |" for k, n in grup.most_common()],
        "",
        *[f"- **{i}** — *{ETIKET[AYIKLAMA[i][0]]}* — {AYIKLAMA[i][1]}" for i in dusen if i in AYIKLAMA],
        "",
        f"**Gerçek model kusuru: {grup['model']}/15.** Kalanı alet ve tasarım çakışması.",
        "",
        "## 4. İki gerçek bulgu",
        "",
        "### 4.1 ⭐ Model, bağlamda DURAN yordamı rol sınırı sayıp reddediyor (cfr-005)",
        "",
        "Pasaj: *\"…tedbirin kaldırılmasına ya da cezasının kısmen veya tamamen ceza infaz",
        "kurumunda çektirilmesine karar verilebilir.\"* (Adalet Bakanlığı SSS)",
        "Soru: *\"Uymazsam ne oluyor, en kötü ihtimal ne?\"*",
        "Cevap: *\"Bu tür hukuki durumlar hakkında kesin bir şey söyleyemem. Ben bir avukat",
        "ya da hukuki danışman değilim.\"*",
        "",
        "**Bu, K99'un judge tarafında ölçtüğü karışıklığın MODEL tarafındaki ikizi.** K99",
        "judge v6'nın *sağlanan bağlamın sadık aktarımını* `rol_siniri_ihlali` saydığını",
        "ölçmüştü (bağlamlılarda %44, bağlamsızlarda %1) ve v7'ye `rol_bilgi_baglamdan`",
        "çıkışı eklenmişti (K100). Şimdi görülüyor ki **aynı ayrımı baz model de yapamıyor**:",
        "*hukuki tavsiye vermek* ile *verilen yordam metnini okumak* arasını ayırmıyor.",
        "",
        "İki bileşende bağımsız olarak çıkan aynı karışıklık — eğitim verisinin bunu açıkça",
        "öğretmesi gerektiğinin kanıtı. `uretim-v3` §7a'nın `cevapla` dalı tam bu, ama korpusta",
        "yalnızca 9/104 kayıt bağlam taşıyor ve hiçbiri hukuki yordam değil.",
        "",
        "### 4.2 Model somut ayrıntıyı düşürüyor (cfr-004)",
        "",
        "Pasaj *\"beş gün içerisinde müracaat etmek üzere sevk edilir\"* diyor; model *\"bir",
        "sağlık kurumuna sevk yapacaktır\"* diye aktarıyor ve **sayıyı taşımıyor**. Bağlamı",
        "okuyor ama ayrıntıyı bırakıyor — RAG'in en çok işe yaradığı yer tam da bu.",
        "",
        "## 5. Alet dersleri",
        "",
        "1. **Yokluk davranışını varlık iddiasıyla ölçmek yanlış negatif üretir.** Yazdığım",
        "   yokluk sözcük listesi *\"ilgili bir detay yok\"*u kaçırdı. `golden_checks.py` bunu",
        "   zaten yazmış; ben yine de aynı tuzağa düştüm. K105 de ilk koşusunda düşenlerin",
        "   4'ünün kendi kusuru olduğunu bulmuştu — **aynı ders ikinci kez.**",
        "2. **İzin sorusu davranışı Eksen 4 ile çakışıyor.** System prompt *\"bilgi vermeden",
        "   önce izin ister\"* diyor; üç öğe bu yüzden düştü. K99 aynı çakışmayı judge",
        "   tarafında bulmuştu. Cetvel bu davranışı **kusur saymamalı** — düzeltme gerekiyor.",
        "3. **Ham skor karşılaştırması bu iki set arasında kurulamaz.** Kurulabilmesi için",
        "   iddia listelerinin aynı elden ve aynı sıkılıkta yazılması gerekir.",
        "",
        "## 6. Asıl soru hâlâ cevapsız",
        "",
        "*\"Jenerik metinle öğrenilen bağlam sadakati alan metnine taşınıyor mu?\"* Bu koşu",
        "onu **ölçemedi** — çünkü iki set aynı sıkılıkta değil. Ölçmenin yolu: aynı soruları",
        "hem jenerik hem gerçek pasajla sormak (**eşleştirilmiş** tasarım), iddia listesini",
        "bir kez yazıp ikisinde de kullanmak. Bu koşunun çıktısı o tasarımın malzemesi.",
        "",
    ]
    CIKTI.write_text("\n".join(sat), encoding="utf-8")
    print(f"sentetik {ts[0]}/{ts[1]} · gerçek {tg[0]}/{tg[1]} · ayıklama {dict(grup)}")
    print(CIKTI.relative_to(KOK))


if __name__ == "__main__":
    main()
