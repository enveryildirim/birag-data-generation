"""Gelişme raporu: `docs/rapor/ip*.md` taslaklarını `rapor-bırag.docx` şablonuna döker.

Şablondaki tek hücreli dış tablonun içindeki İP bloğu (bilgi tablosu + «a) Yapılan
Çalışmalar» + «b) Başarı Ölçütleri») her İP için çoğaltılır ve doldurulur. Özgün
şablona dokunulmaz; çıktı `rapor-bırag-dolu.docx`.

Taslak biçimi (markdown alt kümesi):
    <!-- ip_no: 1 -->  <!-- ip_adi: ... -->  <!-- tamamlanma: ... -->
    # Çalışmalar          → şablonun a) başlığının altı
    # Gerçekleşme         → şablonun b) başlığının altı
    ## 1.1 Başlık         → kalın alt başlık
    ### Başlık            → kalın-italik ara başlık
    paragraf, **kalın**, *italik*, `kod`
    - madde / 1. madde
    | tablo | (ilk satır başlık)
    ![Şekil 1. Açıklama](reports/analiz/sekiller/s1.png)
    > not                 → küçük italik açıklama (tablo/şekil kaynağı)

Kullanım: uv run python scripts/analiz/2026-10-21-rapor-docx.py
"""

import html
import re
import shutil
import struct
import sys
import tempfile
import zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
SABLON = KOK / "rapor-bırag.docx"
CIKTI = KOK / "rapor-bırag-dolu.docx"
TASLAKLAR = [KOK / "docs/rapor/ip1.md", KOK / "docs/rapor/ip2.md"]

GOVDE_PT = 20  # yarım punto: 10 pt, şablonun gövde boyutu
TABLO_PT = 17
TABLO_GENISLIK = 9180  # dxa, iç tablonun genişliği
SEKIL_GENISLIK_EMU = 5_760_000  # ≈ 16 cm

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


# --- satır içi ------------------------------------------------------------------

def run(metin, kalin=False, italik=False, kod=False, boyut=GOVDE_PT, renk=None):
    rpr = []
    if kod:
        rpr.append('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>')
    if kalin:
        rpr.append("<w:b/><w:bCs/>")
    if italik:
        rpr.append("<w:i/><w:iCs/>")
    if renk:
        rpr.append(f'<w:color w:val="{renk}"/>')
    rpr.append(f'<w:sz w:val="{boyut}"/><w:szCs w:val="{boyut}"/>')
    return (f'<w:r><w:rPr>{"".join(rpr)}</w:rPr>'
            f'<w:t xml:space="preserve">{html.escape(metin, quote=False)}</w:t></w:r>')


SATIR_ICI = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)")


def satir_ici(metin, boyut=GOVDE_PT, kalin=False, italik=False):
    parcalar = []
    for p in SATIR_ICI.split(metin):
        if not p:
            continue
        if p.startswith("**"):
            parcalar.append(satir_ici(p[2:-2].replace("**", ""), boyut, kalin=True, italik=italik))
        elif p.startswith("`"):
            parcalar.append(run(p[1:-1], kod=True, kalin=kalin, italik=italik, boyut=boyut - 2))
        elif p.startswith("*"):
            parcalar.append(run(p[1:-1], kalin=kalin, italik=True, boyut=boyut))
        else:
            parcalar.append(run(p, kalin=kalin, italik=italik, boyut=boyut))
    return "".join(parcalar)


def paragraf(icerik, jc="both", once=60, sonra=60, girinti=None, numara=None,
             ayni_sayfa=False):
    ppr = []
    if ayni_sayfa:
        ppr.append("<w:keepNext/>")
    if numara:
        ppr.append(f'<w:numPr><w:ilvl w:val="0"/><w:numId w:val="{numara}"/></w:numPr>')
    ppr.append(f'<w:spacing w:before="{once}" w:after="{sonra}"/>')
    if girinti:
        ppr.append(girinti)
    ppr.append(f'<w:jc w:val="{jc}"/>')
    return f'<w:p><w:pPr>{"".join(ppr)}</w:pPr>{icerik}</w:p>'


# --- tablo ----------------------------------------------------------------------

def hucre(metin, genislik, baslik=False, sag=False):
    golge = '<w:shd w:val="clear" w:color="auto" w:fill="E7E6E6"/>' if baslik else ""
    jc = "right" if sag else "left"
    return (f'<w:tc><w:tcPr><w:tcW w:w="{genislik}" w:type="dxa"/>{golge}'
            f'<w:tcMar><w:top w:w="30" w:type="dxa"/><w:bottom w:w="30" w:type="dxa"/></w:tcMar>'
            f'<w:vAlign w:val="center"/></w:tcPr>'
            f'<w:p><w:pPr><w:spacing w:before="0" w:after="0"/><w:jc w:val="{jc}"/></w:pPr>'
            f'{satir_ici(metin, TABLO_PT, kalin=baslik)}</w:p></w:tc>')


def sayisal(metin):
    return bool(re.fullmatch(r"[\s%≈<>~+−–\-\d.,/()×p=]+", metin.replace("**", ""))) and any(
        c.isdigit() for c in metin)


def tablo(satirlar):
    hucreler = [[h.strip() for h in s.strip().strip("|").split("|")] for s in satirlar]
    hucreler = [s for s in hucreler if not all(re.fullmatch(r":?-{3,}:?", h) for h in s)]
    sutun = max(len(s) for s in hucreler)
    uzun = [max(min(len(s[i]) if i < len(s) else 0, 60) for s in hucreler) + 6 for i in range(sutun)]
    # sözcük bölünmesin: her sütun en uzun sözcüğü (≈ 115 dxa/karakter) sığdırır
    taban = [max(len(w) for s in hucreler if i < len(s) for w in (s[i].replace("**", "").split() or [""])) * 115 + 240
             for i in range(sutun)]
    genislik = [round(TABLO_GENISLIK * u / sum(uzun)) for u in uzun]
    for _ in range(5):
        dar = [i for i in range(sutun) if genislik[i] < taban[i]]
        if not dar:
            break
        eksik = sum(taban[i] - genislik[i] for i in dar)
        genis = [i for i in range(sutun) if i not in dar]
        toplam_genis = sum(genislik[i] for i in genis)
        for i in dar:
            genislik[i] = taban[i]
        for i in genis:
            genislik[i] = round(genislik[i] - eksik * genislik[i] / toplam_genis)
    genislik[-1] += TABLO_GENISLIK - sum(genislik)
    kenar = "".join(f'<w:{k} w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
                    for k in ("top", "left", "bottom", "right", "insideH", "insideV"))
    xml = [f'<w:tbl><w:tblPr><w:tblW w:w="{TABLO_GENISLIK}" w:type="dxa"/>'
           f'<w:jc w:val="center"/><w:tblBorders>{kenar}</w:tblBorders>'
           f'<w:tblLayout w:type="fixed"/><w:tblLook w:val="04A0"/></w:tblPr><w:tblGrid>'
           + "".join(f'<w:gridCol w:w="{g}"/>' for g in genislik) + "</w:tblGrid>"]
    # bir sütun yalnız bütün dolu hücreleri sayısalsa sağa yaslanır
    sag_sutun = [j > 0 and all(sayisal(s[j]) for s in hucreler[1:] if j < len(s) and s[j] not in ("", "—"))
                 for j in range(sutun)]
    for i, s in enumerate(hucreler):
        s = s + [""] * (sutun - len(s))
        tr = '<w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>' if i == 0 else '<w:trPr><w:cantSplit/></w:trPr>'
        xml.append("<w:tr>" + tr + "".join(
            hucre(h, genislik[j], baslik=(i == 0), sag=(i > 0 and sag_sutun[j]))
            for j, h in enumerate(s)) + "</w:tr>")
    xml.append("</w:tbl>")
    return "".join(xml)


# --- şekil ----------------------------------------------------------------------

def png_boyut(yol):
    with open(yol, "rb") as f:
        bas = f.read(24)
    assert bas[:8] == b"\x89PNG\r\n\x1a\n", yol
    return struct.unpack(">II", bas[16:24])


class Sekiller:
    def __init__(self):
        self.liste = []  # (rId, hedef ad, kaynak yol)

    def ekle(self, yol):
        yol = KOK / yol
        n = len(self.liste) + 1
        rid, ad = f"rIdSekil{n}", f"sekil{n}.png"
        self.liste.append((rid, ad, yol))
        en, boy = png_boyut(yol)
        cx = SEKIL_GENISLIK_EMU
        cy = round(cx * boy / en)
        return (f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
                f'<wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{n}" name="Şekil {n}"/>'
                f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
                f'<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
                f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
                f'<pic:nvPicPr><pic:cNvPr id="{n}" name="{ad}"/><pic:cNvPicPr/></pic:nvPicPr>'
                f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
                f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
                f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
                f'</a:graphicData></a:graphic></wp:inline></w:drawing></w:r>')


# --- markdown → OOXML ----------------------------------------------------------

def hizala(metin):
    """Bölünemeyen adres (URL) iki yana yaslı satırda boşlukları açar; o paragraf sola yaslanır."""
    return "left" if "http" in metin else "both"


def blok_xml(satirlar, sekiller, numaralar):
    """Bir bölümün (Çalışmalar / Gerçekleşme) satırlarını OOXML paragraflarına çevirir."""
    cikti, i = [], 0
    while i < len(satirlar):
        s = satirlar[i].rstrip()
        if not s.strip():
            i += 1
            continue
        if s.startswith("## "):
            cikti.append(paragraf(run(s[3:].strip(), kalin=True), jc="left", once=200, sonra=60,
                                  ayni_sayfa=True))
        elif s.startswith("### "):
            cikti.append(paragraf(run(s[4:].strip(), kalin=True, italik=True), jc="left",
                                  once=120, sonra=40, ayni_sayfa=True))
        elif s.startswith("|"):
            j = i
            while j < len(satirlar) and satirlar[j].lstrip().startswith("|"):
                j += 1
            cikti.append(tablo(satirlar[i:j]))
            cikti.append(paragraf("", once=0, sonra=0))
            i = j
            continue
        elif m := re.match(r"!\[(.+?)\]\((.+?)\)", s):
            cikti.append(paragraf(sekiller.ekle(m.group(2)), jc="center", once=120, sonra=0,
                                  ayni_sayfa=True))
            cikti.append(paragraf(satir_ici(m.group(1), TABLO_PT, italik=False), jc="center",
                                  once=40, sonra=160))
        elif s.startswith("> "):
            cikti.append(paragraf(satir_ici(s[2:], TABLO_PT, italik=True), jc="left",
                                  once=0, sonra=100))
        elif re.match(r"- |\d+\. ", s):
            numarali = bool(re.match(r"\d+\. ", s))
            numara = numaralar.yeni_sirali() if numarali else numaralar.MADDE
            while i < len(satirlar) and re.match(r"- |\d+\. ", satirlar[i]):
                madde = re.sub(r"^(- |\d+\. )", "", satirlar[i].rstrip())
                i += 1
                while i < len(satirlar) and satirlar[i].startswith("  ") and satirlar[i].strip():
                    madde += " " + satirlar[i].strip()
                    i += 1
                cikti.append(paragraf(satir_ici(madde), jc=hizala(madde), numara=numara, once=20, sonra=20))
            continue
        else:
            metin = [s.strip()]
            i += 1
            while (i < len(satirlar) and satirlar[i].strip()
                   and not re.match(r"(#|\||!\[|> |- |\d+\. )", satirlar[i])):
                metin.append(satirlar[i].strip())
                i += 1
            cikti.append(paragraf(satir_ici(" ".join(metin)), jc=hizala(" ".join(metin))))
            continue
        i += 1
    return "".join(cikti)


def taslak_oku(yol):
    metin = yol.read_text(encoding="utf-8")
    ust = dict(re.findall(r"<!--\s*(\w+):\s*(.+?)\s*-->", metin))
    metin = re.sub(r"<!--.*?-->", "", metin, flags=re.S)
    bolumler, ad = {}, None
    for s in metin.splitlines():
        if s.startswith("# "):
            ad = s[2:].strip()
            bolumler[ad] = []
        elif ad:
            bolumler[ad].append(s)
    assert set(bolumler) == {"Çalışmalar", "Gerçekleşme"}, (yol, list(bolumler))
    return ust, bolumler


# --- numaralandırma ---------------------------------------------------------------

class Numaralar:
    """Şablonun numbering.xml'ine madde imi, sıralı liste ve İP başına a)/b) yeniden başlatma ekler."""
    MADDE = 101

    def __init__(self):
        self.ek_num, self.sayac = [], 200

    def yeni_sirali(self):
        self.sayac += 1
        self.ek_num.append(f'<w:num w:numId="{self.sayac}"><w:abstractNumId w:val="91"/>'
                           f'<w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>')
        return self.sayac

    def yeni_ab(self):
        self.sayac += 1
        self.ek_num.append(f'<w:num w:numId="{self.sayac}"><w:abstractNumId w:val="1"/>'
                           f'<w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>')
        return self.sayac

    def uygula(self, numbering):
        soyut = (
            '<w:abstractNum w:abstractNumId="90"><w:multiLevelType w:val="singleLevel"/>'
            '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/>'
            '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="567" w:hanging="283"/></w:pPr>'
            '<w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/></w:rPr></w:lvl></w:abstractNum>'
            '<w:abstractNum w:abstractNumId="91"><w:multiLevelType w:val="singleLevel"/>'
            '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/>'
            '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="567" w:hanging="340"/></w:pPr></w:lvl></w:abstractNum>'
        )
        # abstractNum'lar num'lardan önce gelmeli (şema sırası)
        i = numbering.index("<w:num ")
        numbering = numbering[:i] + soyut + numbering[i:]
        ek = f'<w:num w:numId="{self.MADDE}"><w:abstractNumId w:val="90"/></w:num>' + "".join(self.ek_num)
        return numbering.replace("</w:numbering>", ek + "</w:numbering>")


# --- şablon ---------------------------------------------------------------------

def ust_duzey_parcalar(xml, etiket):
    """xml içindeki en üst düzey <w:p>/<w:tbl> öğelerini sırayla döndürür."""
    parcalar, i = [], 0
    desen = re.compile(r"<w:(p|tbl)[ >/]")
    while (m := desen.search(xml, i)):
        ad = m.group(1)
        bas = m.start()
        if xml.startswith("/>", xml.index(">", bas) - 1):
            son = xml.index(">", bas) + 1
        else:
            derinlik, j = 0, bas
            ac, kapa = re.compile(rf"<w:{ad}[ >]"), f"</w:{ad}>"
            while True:
                a = ac.search(xml, j + 1)
                k = xml.index(kapa, j + 1 if j > bas else bas)
                if a and a.start() < k:
                    derinlik += 1
                    j = a.start()
                    continue
                if derinlik == 0:
                    son = k + len(kapa)
                    break
                derinlik -= 1
                j = k
        parcalar.append(xml[bas:son])
        i = son
    return parcalar


def metin(p):
    return "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p))


def doldur_bilgi_tablosu(tbl, no, ad, tamamlanma):
    bos = re.compile(r'(<w:p [^>]*>(?:<w:pPr>.*?</w:pPr>)?)(</w:p>)', re.S)
    degerler = iter([no, ad, tamamlanma])

    def degis(m):
        return m.group(1) + run(next(degerler), kalin=False) + m.group(2)

    # yalnızca içi boş (run'sız) değer hücrelerini doldur
    hucreler = re.split(r"(?=<w:tc>)", tbl)
    for k, h in enumerate(hucreler):
        if h.startswith("<w:tc>") and "<w:r>" not in h and "<w:r " not in h:
            hucreler[k] = bos.sub(degis, h, count=1)
    return "".join(hucreler)


def main():
    assert SABLON.exists(), SABLON
    taslaklar = [taslak_oku(y) for y in TASLAKLAR]

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        with zipfile.ZipFile(SABLON) as z:
            z.extractall(tmp)
        belge = (tmp / "word/document.xml").read_text(encoding="utf-8")

        govde_bas = belge.index("<w:body>") + len("<w:body>")
        sect = belge.index("<w:sectPr")
        dis = ust_duzey_parcalar(belge[govde_bas:sect], "body")
        assert len(dis) == 2 and dis[0].startswith("<w:tbl>"), [d[:20] for d in dis]
        dis_tbl = dis[0]
        tc_bas = dis_tbl.index("</w:tcPr>") + len("</w:tcPr>")
        tc_son = dis_tbl.rindex("</w:tc>")
        ic = ust_duzey_parcalar(dis_tbl[tc_bas:tc_son], "tc")
        metinler = [metin(p) for p in ic]

        baslik = ic[0]
        bilgi_tbl = next(p for p in ic if p.startswith("<w:tbl"))
        a_i = next(k for k, t in enumerate(metinler) if t.startswith("İP Kapsamında"))
        b_i = next(k for k, t in enumerate(metinler) if t.startswith("İP Sonuçlarının"))
        a_bas, a_aciklama = ic[a_i], ic[a_i + 1]
        b_bas, b_aciklama = ic[b_i], ic[b_i + 1]

        sekiller, numaralar = Sekiller(), Numaralar()
        # her İP kendi dış tablosunda; sayfa sonu tablolar arasında (hücre içindeki kırılma yok sayılır)
        dis_tablolar = []
        for k, (ust, bolum) in enumerate(taslaklar):
            yeni = [baslik] if k == 0 else []
            yeni.append(doldur_bilgi_tablosu(bilgi_tbl, ust["ip_no"], ust["ip_adi"], ust["tamamlanma"]))
            yeni.append(paragraf("", once=0, sonra=0))
            ab = 1 if k == 0 else numaralar.yeni_ab()
            yeni.append(re.sub(r'w:numId w:val="1"', f'w:numId w:val="{ab}"', a_bas))
            yeni.append(a_aciklama)
            yeni.append(blok_xml(bolum["Çalışmalar"], sekiller, numaralar))
            yeni.append(paragraf("", once=0, sonra=0))
            yeni.append(re.sub(r'w:numId w:val="1"', f'w:numId w:val="{ab}"', b_bas))
            yeni.append(b_aciklama)
            yeni.append(blok_xml(bolum["Gerçekleşme"], sekiller, numaralar))
            yeni.append(paragraf("", once=0, sonra=0))
            dis_tablolar.append(dis_tbl[:tc_bas] + "".join(yeni) + dis_tbl[tc_son:])

        dis_yeni = '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'.join(dis_tablolar)
        belge = belge[:govde_bas] + dis_yeni + dis[1] + belge[sect:]
        (tmp / "word/document.xml").write_text(belge, encoding="utf-8")

        num = (tmp / "word/numbering.xml").read_text(encoding="utf-8")
        (tmp / "word/numbering.xml").write_text(numaralar.uygula(num), encoding="utf-8")

        rels_yol = tmp / "word/_rels/document.xml.rels"
        rels = rels_yol.read_text(encoding="utf-8")
        (tmp / "word/media").mkdir(exist_ok=True)
        ek = []
        for rid, ad, yol in sekiller.liste:
            shutil.copy(yol, tmp / "word/media" / ad)
            ek.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
                      f'officeDocument/2006/relationships/image" Target="media/{ad}"/>')
        rels_yol.write_text(rels.replace("</Relationships>", "".join(ek) + "</Relationships>"),
                            encoding="utf-8")
        ct_yol = tmp / "[Content_Types].xml"
        ct = ct_yol.read_text(encoding="utf-8")
        if 'Extension="png"' not in ct:
            ct = ct.replace("<Default ", '<Default Extension="png" ContentType="image/png"/><Default ', 1)
        ct_yol.write_text(ct, encoding="utf-8")

        if CIKTI.exists():
            CIKTI.unlink()
        with zipfile.ZipFile(SABLON) as z:
            sira = [i.filename for i in z.infolist()]
        tum = sira + [f"word/media/{ad}" for _, ad, _ in sekiller.liste]
        with zipfile.ZipFile(CIKTI, "w", zipfile.ZIP_DEFLATED) as z:
            for ad in tum:
                z.write(tmp / ad, ad)
    print(f"{CIKTI.name}: {len(taslaklar)} İP, {len(sekiller.liste)} şekil")


if __name__ == "__main__":
    sys.exit(main())
