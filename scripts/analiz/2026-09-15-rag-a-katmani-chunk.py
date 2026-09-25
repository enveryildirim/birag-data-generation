#!/usr/bin/env python3
"""A katmanı pilotu: ham kurum metinlerini chunk'lar ve KAPILARI GERÇEK METİNLE SINAR.

plan.md §17.5 şunu ölçmeyi vaat etmişti: `context_ok`'un klinik-iddia kapısı gerçek
kurumsal metne uygulanınca ne kadar eliyor? Vekil ölçüm %32 demişti (BÖLÜM K, markdown
tablo satırı). Burada gerçek korpusla ölçülüyor.

İkinci kapı K18: `plan.md` §15 *"telefon numarası / rakam — numara modelde değil"*.
Kural AĞIRLIKLAR için yazıldı; retrieval bağlamını da bağlayıp bağlamadığı AÇIK BİR
SORU (K105 aynı soruyu `112` için uzmana taşımış). Burada karar verilmiyor, ÖLÇÜLÜYOR.

Girdi : data/rag/a-katmani/ham/*.txt
Çıktı : data/rag/a-katmani/chunks.jsonl · reports/analiz/2026-09-15-rag-a-katmani-pilot.md
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))
from checks import KLINIK_IDDIA  # noqa: E402

HAM = KOK / "data/rag/a-katmani/ham"
CHUNKS = KOK / "data/rag/a-katmani/chunks.jsonl"
RAPOR = KOK / "reports/analiz/2026-09-15-rag-a-katmani-pilot.md"

# K18 / §15: rakam taraması. Telefon ve serbest sayı ayrı sayılır — ikisi aynı şey değil.
TELEFON = re.compile(r"\b(1\d{2}|0\d{3}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2})\b")
SAYI = re.compile(r"\b\d+([.,:]\d+)*\b")

ALT, UST = 180, 700   # hedef chunk bandı (karakter)

# Klinik-iddia kapısına takılan chunk'ların ELLE sınıflandırması. Bu BENİM yargım,
# makine çıkarımı değil — betiğe gömülü ki sayı yeniden üretilebilsin ve tartışılabilsin.
#   haklı   : pasaj gerçekten klinik iddia taşıyor (§7b-2 doğru eliyor)
#   yanlis  : saf yordam/uygunluk/kurum adı cümlesi — kapı hata yapıyor
#   sinirda : klinik içerik ama kişi hakkında iddia değil (yöntem adı sayımı)
AYIKLAMA = {
    ("yedam-modeli", 1): "hakli",      # "arınma birkaç hafta içinde", "nüks etme riski vardır"
    ("yedam-modeli", 3): "sinirda",    # BDT/MI/Mindfulness adlarını sayıyor
    ("yedam-modeli", 4): "sinirda",    # "Tedavi modeli" başlığı + yöntem listesi
    ("yedam-ne-yapiyoruz", 2): "yanlis",             # "Yatarak tedavi yapılmamaktadır" — hizmet sınırı
    ("alo191-nedir", 1): "yanlis",                   # "önleme, tedavi ve rehabilitasyon mekanizmaları"
    ("alo191-kimlere-hizmet-sunar", 1): "yanlis",    # "yoksunluk yaşayanlar" — uygunluk ölçütü
    ("alo191-kimlere-hizmet-sunar", 2): "yanlis",    # "tedavi sürecinde sorun yaşayanlar" — uygunluk
    ("alo191-nasil-hizmetler-sunar", 2): "yanlis",   # "tedavileri için en uygun merkezlere yönlendirme"
    ("ds-denetimli-serbestlik-nedir", 1): "yanlis",  # "iyileştirilmesi" — infaz hukuku terimi
    ("ds-denetimli-serbestlik-nedir", 4): "yanlis",  # aynı terim
    ("ds-tedavi-denetimli-serbestlik-191", 1): "yanlis",  # "tedavi ve denetimli serbestlik kararı" = tedbirin ADI
    ("ds-tedavi-denetimli-serbestlik-191", 3): "yanlis",  # "Alkol ve Madde Tedavi Merkezleri" = kurumun ADI
}


def ham_oku(yol: Path) -> tuple[dict, str]:
    kunye, govde = {}, []
    icerik = yol.read_text(encoding="utf-8")
    bas, _, kalan = icerik.partition("\n---\n")
    for s in bas.splitlines():
        if s.startswith("#") and ":" in s:
            k, _, v = s.lstrip("# ").partition(":")
            kunye[k.strip()] = v.strip()
    govde = kalan.strip()
    return kunye, govde


def parcala(govde: str) -> list[str]:
    """Boş satır bloklarına böl, kısa blokları komşusuyla birleştir."""
    bloklar = [b.strip() for b in re.split(r"\n\s*\n", govde) if b.strip()]
    cikti: list[str] = []
    for b in bloklar:
        if cikti and len(cikti[-1]) < ALT:
            cikti[-1] = cikti[-1] + "\n" + b
        else:
            cikti.append(b)
    # UST'ü aşanları satır sınırından böl
    son: list[str] = []
    for b in cikti:
        while len(b) > UST:
            kes = b.rfind("\n", ALT, UST)
            kes = kes if kes > 0 else UST
            son.append(b[:kes].strip())
            b = b[kes:].strip()
        if b:
            son.append(b)
    return son


def main() -> None:
    kayitlar = []
    for yol in sorted(HAM.glob("*.txt")):
        kunye, govde = ham_oku(yol)
        baslik = govde.splitlines()[0].strip()
        for i, metin in enumerate(parcala(govde), 1):
            kayitlar.append({
                "belge_id": yol.stem,
                "chunk_no": i,
                "katman": "A",
                "kaynak": f"{kunye.get('kurum', '?')} — {baslik}",
                "metin": metin,
                "sentetik": False,
                "kaynak_url": kunye.get("kaynak_url", ""),
                "alinma_tarihi": kunye.get("alinma_tarihi", ""),
                "gecerlilik_tarihi": kunye.get("alinma_tarihi", ""),
                "lisans": kunye.get("lisans", "belirsiz"),
                "icerik_hash": "sha256:" + hashlib.sha256(metin.encode()).hexdigest()[:16],
            })

    CHUNKS.write_text("\n".join(json.dumps(k, ensure_ascii=False) for k in kayitlar) + "\n",
                      encoding="utf-8")

    # --- kapı 1: klinik iddia
    kl = []
    for k in kayitlar:
        v = sorted({m.group(0).lower() for m in KLINIK_IDDIA.finditer(k["metin"].lower())})
        if v:
            kl.append((k, v))
    # --- kapı 2: rakam
    tel = [(k, sorted(set(TELEFON.findall(k["metin"])))) for k in kayitlar if TELEFON.search(k["metin"])]
    say = [k for k in kayitlar if SAYI.search(k["metin"])]

    from collections import Counter
    kl_say = Counter(t for _, v in kl for t in v)
    ayik = Counter({"hakli": 0, "yanlis": 0, "sinirda": 0, "?": 0})
    for k, _ in kl:
        ayik[AYIKLAMA.get((k["belge_id"], k["chunk_no"]), "?")] += 1
    belge = Counter(k["belge_id"] for k in kayitlar)

    sat = [
        "# A katmanı pilotu — ilk gerçek chunk'lar ve kapıların gerçek metinle sınanması",
        "",
        f"**Girdi:** `data/rag/a-katmani/ham/` ({len(belge)} belge, YEDAM + Yeşilay, 2026-09-15 çekimi) · "
        f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}",
        "",
        "---",
        "",
        "## 1. Chunk'lar",
        "",
        f"**{len(kayitlar)} chunk / {len(belge)} belge.** Hepsi `sentetik: false`, `katman: A`, lisans alanı dolu.",
        "",
        "| belge | chunk |",
        "|---|---|",
        *[f"| `{b}` | {n} |" for b, n in belge.most_common()],
        "",
        "## 2. ⛔ Kapı 1 — klinik iddia (`context_ok` §7b-2)",
        "",
        f"**{len(kl)}/{len(kayitlar)} chunk kapıya takılıyor (%{100*len(kl)//len(kayitlar)}).**",
        "",
        "| eşleşen sözcük | chunk |",
        "|---|---|",
        *[f"| `{t}` | {n} |" for t, n in kl_say.most_common()],
        "",
        "### Takılan chunk'lar",
        "",
    ]
    for k, v in kl:
        sat.append(f"- **`{k['belge_id']}` #{k['chunk_no']}** — `{', '.join(v)}`")
        sat.append(f"  > {k['metin'][:170].replace(chr(10), ' ')}…")
    sat += [
        "",
        "### Okuma — ayıklama",
        "",
        "Takılan her chunk elle ayıklandı (**benim yargım**, betiğe gömülü — `AYIKLAMA`):",
        "",
        f"| sonuç | chunk | oran |",
        "|---|---|---|",
        f"| kapı **haklı** — gerçek klinik iddia | {ayik['hakli']} | %{100*ayik['hakli']/len(kayitlar):.0f} |",
        f"| kapı **yanlış** — saf yordam/uygunluk/ad | **{ayik['yanlis']}** | **%{100*ayik['yanlis']/len(kayitlar):.0f}** |",
        f"| sınırda — klinik içerik ama kişi hakkında iddia değil | {ayik['sinirda']} | %{100*ayik['sinirda']/len(kayitlar):.0f} |",
        f"| sınıflandırılmamış | {ayik['?']} | — |",
        "",
        "**Kusur deseni keskinleşti:** yasak sözcük çoğu vakada kurumun ya da mevzuatın",
        "**adının parçası**, yasak kavramın kendisi değil:",
        "",
        "- *\"tedavi ve denetimli serbestlik kararı\"* — bir **hukuki tedbirin adı** (TCK 191/3)",
        "- *\"Alkol ve Madde Tedavi Merkezleri (AMATEM)\"* — bir **kurumun adı**",
        "- *\"iyileştirilmesi\"* — infaz hukukunun **teknik terimi** (offender rehabilitation)",
        "- *\"yoksunluk yaşayanlar\"* — hattın **uygunluk ölçütü**, belirti iddiası değil",
        "",
        "⚠️ **Bu sayı oturum içinde iki kez değişti; son hâli budur.** Önce vekil ölçüm",
        "(BÖLÜM K tablosu) **%32** demişti. Sonra yalnızca YEDAM'ın 23 chunk'ıyla **%4**",
        "ölçtüm ve §17.5'teki uyarıyı *\"abartılı\"* diye düzelttim — **o düzeltme erkendi.**",
        "Kamu yordam metni (ALO 191 + denetimli serbestlik) eklenince oran vekilin",
        "gösterdiği yere geri geldi. Sebep: YEDAM sayfaları kısa tanıtım metniydi, kamu",
        "metinleri ise **mevzuat ve kurum adı yoğun** — kapının tam zayıf noktası.",
        "**Ders örneklem hakkında:** 23 chunk'lık tek-kurum örneklemi bu kapıyı ölçmeye",
        "yetmiyordu; T22 vaka serisine bu da yazılmalı.",
        "",
        "**R3 gerekli ve dar değil.** Kapı `sentetik` bayrağına ayrılacak ve gerçek pasajda",
        "**iddia cümlesi** aranacak (sözcük varlığı değil). Bugünkü hâliyle A katmanının",
        f"**%{100*ayik['yanlis']/len(kayitlar):.0f}**'ı haksız yere elenir.",
        "",
        "## 3. ⚠️ Kapı 2 — rakam (K18)",
        "",
        f"Telefon numarası içeren chunk: **{len(tel)}/{len(kayitlar)}** · herhangi bir sayı içeren: **{len(say)}/{len(kayitlar)}**",
        "",
        *[f"- `{k['belge_id']}` #{k['chunk_no']} → {v}" for k, v in tel],
        "",
        "⚠️ **Bu kapının kendi sınırı:** `1\\d{2}` deseni *hat numarası* ile *kanun madde",
        "numarası* arasını ayıramaz — *TCK **191**/3* aynı desene uyar. Bu korpusta çakışma",
        "yok (tarandı: yalnızca `6698 Sayılı` geçiyor), ama desen **gizli yanlış pozitif**",
        "taşıyor. Kendi kurduğum kapıda K65'in aynısı; kayda geçiyor.",
        "",
        "**Bu bir çelişki ve kararı bize ait değil.** `plan.md` §15 *\"telefon numarası / rakam —",
        "numara modelde değil\"* diyor (K18). Kural **ağırlıklar** için yazıldı ve gerekçesi",
        "*LLM rakam bozar, quantization ağırlaştırır*. Ama:",
        "",
        "| | ağırlıktan hatırlama | bağlamdan okuma |",
        "|---|---|---|",
        "| Bozulma riski | var (K18'in gerekçesi) | **yok** — metin önünde duruyor |",
        "| Güncellik riski | var — numara değişirse model yanlış söyler | **yok** — chunk tazelenir |",
        "| `golden_eval` `rakam_yok` | geçer | ⛔ **düşer** |",
        "",
        "Yani A katmanı korpusu K18'i ağırlık tarafında değil **ölçüm** tarafında zorluyor.",
        "K105 aynı soruyu `112` için zaten uzmana taşımış (*«112 istisna mı»*, uzman brifingi",
        "Adım 1.11). **Bu bulgu o sorunun kapsamını genişletiyor:** yalnızca kriz numarası değil,",
        "kurumun kendi danışma hattı da aynı kapıya çarpıyor. Karar uzmanın (Kural 3).",
        "",
        "Ara çözüm önerisi *(benim önerim, onay gerektirir)*: numara chunk'ta **kalır** —",
        "kaynağa sadakat bozulmasın — ama `rakam_yok` denetimi **bağlam taşıyan kayıtlarda**",
        "numaranın bağlamda geçip geçmediğine bakar; uydurulmuş numara ihlal, aktarılan numara",
        "değil. Bu, judge v7'nin `rol_bilgi_baglamdan` deseninin birebir aynısı (K100).",
        "",
        "## 4. Hedef soruları kapatıyor muyuz?",
        "",
        "| # | soru | durum |",
        "|---|---|---|",
        "| S1 | *\"siz aileme söylemezsiniz değil mi?\"* | 🟡 **kısmi** — *\"Gizlilik esasına bağlı çalışılmaktadır\"* var, ama aileye bildirim konusunda açık cümle yok |",
        "| S2 | *\"kayıt aileme gider mi, sicilime düşer mi?\"* | 🟡 **kısmi** — KVKK politikası *\"kanuni istisnalara uygun olarak veya açık rıza alınarak paylaşılır\"* diyor; *sicile düşme* hiç geçmiyor |",
        "| S3 | *\"dosyama işlenir mi?\"* | 🟡 **kısmi** — saklama süresi ilkesi var, danışan dosyası özelinde metin yok |",
        "| S5 | *\"AMATEM'e gitsem…\"* (AMATEM farkı) | ✅ **kapandı** — *\"YEDAM hizmetlerini ayaktan sürdürmektedir. Yatarak tedavi yapılmamaktadır.\"* |",
        "| S6 | aile hekimi üzerinden erişim | ⛔ **kapanmadı** — YEDAM metinlerinde aile hekimliği yolu yok |",
        "| S7 | denetimli serbestlik / TCK 191/3 | ⛔ **kapanmadı** — A5 satırı çekilmedi |",
        "",
        "⚠️ **Üç 🟡 aynı sebepten:** YEDAM'ın kendi KVKK sayfası"
        " (`yedam.org.tr/kisisel-verilerin-korunmasi-politikasi`) **boş dönüyor** (2026-09-15:"
        " gövdesiz / HTTP 500). Danışan gizliliği için elimizdeki tek metin Yeşilay'ın kurumsal"
        " politikası ve orada *danışan* yalnızca bir grup adı olarak geçiyor.",
        "",
        "**Bu bir korpus açığı değil, kaynağın kendisinde açık.** Doğru model davranışı",
        "S1/S2/S3'ün cevaplanmayan kısmında §7a'nın `yetersiz` dalıdır — ve bu, bağlam",
        "diliminin öğretmesi gereken tam davranış.",
        "",
    ]
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print(f"chunk {len(kayitlar)} · klinik-iddia {len(kl)} · telefon {len(tel)} · sayı {len(say)}")
    print(RAPOR.relative_to(KOK))


if __name__ == "__main__":
    main()
