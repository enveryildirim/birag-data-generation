#!/usr/bin/env python3
"""T63 ve T68 birer SÖZ bırakmıştı — T70 sözlerin tutulmadığını ölçtü. Söz denetime bağlanıyor.

İki kalem planda şöyle duruyordu:

  · **T68** — *«ihlal sayılarımız ÜST SINIRDIR; bundan sonraki Eksen 2
    raporlarında bu standart şerh olmalı»*
  · **T63** — *«kol tablolarında sıra numarası yazılacaksa yanına eşitlik ve
    ters çift sayısı da yazılmalı»*

⛔ İkisi de **yalnızca plana yazılmış birer niyet**ti. Aynı oturumda T70 tam
olarak bunun bedelini ölçtü: `samples.md` **iki ayrı yerde** ilan edilmiş,
**24 koşunun hiçbirinde** üretilmemişti — çünkü ilanı sınayan bir şey yoktu.
➡️ *Bir yazım kuralı, denetlenmediği sürece bir kural değil bir dilektir.*

⭐ Bu betik iki kuralı **tetikleyici + uyum** çiftine çeviriyor:

| | Tetikleyici | Uyum |
|---|---|---|
| Ş1 (T68) | rapor bir **sert kapı bayrağını SAYIYLA** bildiriyor | *«üst sınır»* şerhi var |
| Ş2 (T63) | rapor **≥3 kolu** adlandırıp bir **sıra** kuruyor | *«ters çift»* sayısı var |

⛔ **Bayrak adları ve kol adları ELLE YAZILMIYOR:** bayraklar rubrikten
(`prompts/judge-eksen1.v9.md`), kollar eğitim config'lerinin `ad:` alanından
okunuyor. Liste kayarsa denetim onunla birlikte kayar.

⚠️ **Kapsam KESME TARİHİYLE sınırlı (Kural 7):** geçmiş raporlar değiştirilmez;
kural ilan edildiği günden itibaren işler. Kesme tarihinden önceki tetiklenen
raporlar ayrıca sayılıyor — ⭐ *bir kuralın geriye dönük borcu, ileriye dönük
yükümlülüğünden ayrı bir sayıdır ve ikisi karıştırılırsa hiçbiri okunamaz.*

Girdi : reports/analiz/*.md · prompts/judge-eksen1.v9.md · configs/training/f4*.yaml
Çıktı : reports/analiz/2026-09-16-rapor-serh-denetimi.md
Kullanım: uv run python scripts/analiz/2026-09-16-rapor-serh-denetimi.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import checks as C  # noqa: E402

_s = importlib.util.spec_from_file_location("_tg", KOK / "src/tohum_guvenlik.py")
TG = importlib.util.module_from_spec(_s)
_s.loader.exec_module(TG)


def tr_ara(igne: str, saman: str) -> bool:
    """⛔⭐ BU SATIR BİR HATANIN ÜSTÜNE YAZILDI — ve hata AYNI OTURUMDA oldu.

    Uyum sınaması önce `"üst sınır" in metin.lower()` diye yazılmıştı. Şerhin
    metni *«ÜST SINIRDIR»* diyor ve `"SINIRDIR".lower()` Python'da `"sinirdir"`
    veriyor (`I` → `i`, `ı` DEĞİL) ⇒ ⛔ **şerh yazıldığı hâlde denetim onu
    görmedi.** Yani T73'ün ölçtüğü tuzak, T73 yazıldıktan dakikalar sonra,
    aynı elden çıkan YENİ bir denetimde tekrarladı.

    ➡️ *Bu ailenin beşinci örneği bir «dikkatsizlik» değil: Türkçe + Python'da
    dizge karşılaştırmasının VARSAYILAN hâli yanlış, doğrusu ek çaba istiyor.
    Bu yüzden arama artık `checks.i_sinifi` ÇAĞRILARAK yapılıyor.*
    """
    n = lambda x: C.i_sinifi(TG.tr_kucult(x))
    return n(igne) in n(saman)
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL (K126).
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-rapor-serh-denetimi.md"
RUBRIK = KOK / "prompts/judge-eksen1.v9.md"
# ⛔ Kural ilan edildiği günden itibaren işler; geçmiş raporlar değiştirilmez.
KESME = "2026-09-16"
# ⚠️ Kendi raporu ve denetim raporları kapsam dışı: bayrak adlarını SAYMADAN,
#    ALINTILAYARAK taşıyorlar. Dışlama gizlenmiyor, raporda listeleniyor.
DISLANAN = {
    f"{TARIH}-rapor-serh-denetimi.md": "denetimin kendisi (yapısal, T64'ün sınıfı)",
    f"{TARIH}-rapor-yeniden-uretilebilirlik.md": "betik adı sayar, bayrak saymaz",
    f"{TARIH}-ilan-edilen-sha-denetimi.md": "SHA sayar, bayrak saymaz",
    f"{TARIH}-katki-defteri-denetimi.md": "katkı sayar, bayrak saymaz",
    f"{TARIH}-tez-plani-turetme.md": "artefakt sayar, bayrak saymaz",
}


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def bayraklar() -> list[str]:
    """Sert kapı bayrakları — **rubrikten** okunur, elle yazılmaz."""
    return sorted(set(re.findall(r"`([a-z_]+_ihlali|bos_guvence)`",
                                 RUBRIK.read_text(encoding="utf-8"))))


def kollar() -> list[str]:
    """Kol adları — eğitim config'lerinin `ad:` alanından, elle yazılmaz."""
    out = set()
    for p in sorted((KOK / "configs/training").glob("f4*.yaml")):
        m = re.search(r"^ad:\s*(\S+)", p.read_text(encoding="utf-8"), re.M)
        if m:
            out.add(m.group(1).split("-", 2)[-1])
    return sorted(out)


# --- Ş1 (T68) ----------------------------------------------------------------
def s1_tetik(metin: str, bayrak: list[str]) -> list[str]:
    """⭐ *Adı geçmesi* yetmez — bayrağın yanında bir SAYI olmalı. Bir bayrağı
    tartışan rapor ile onu SAYAN rapor farklı şeyler; şerh yalnızca ikincisine
    borç."""
    return [b for b in bayrak
            if re.search(rf"`{b}`[^\n|]*\|[^\n]*\d", metin)
            or re.search(rf"\|[^\n]*`{b}`[^\n]*\|\s*\**\d", metin)]


def s1_uyum(metin: str) -> bool:
    return tr_ara("üst sınır", metin)


# --- Ş2 (T63) ----------------------------------------------------------------
def s2_tetik(metin: str, kol: list[str]) -> tuple[bool, list[str]]:
    """≥3 kol adlandırılmış VE bir sıra kurulmuş mu (kolon · söz · numaralı liste)."""
    var = [k for k in kol if k in metin]
    if len(var) < 3:
        return False, var
    sira = (bool(re.search(r"\|\s*(sıra|rank|#)\s*\|", metin, re.I))  # lower-muaf: tablo başlığı; `sıra` küçük harf yazılır, büyük harf başlık kullanılmıyor
            or bool(re.search(r"sırala|en iyi kol|birinci kol", metin, re.I))  # lower-muaf: aynı
            or bool(re.search(r"^\s*\d\.\s+\*?\*?`?(" + "|".join(map(re.escape, kol)) + ")",
                              metin, re.M)))
    return sira, var


def s2_uyum(metin: str) -> bool:
    return tr_ara("ters çift", metin) or tr_ara("ters dönen", metin)


def main() -> int:
    bayrak, kol = bayraklar(), kollar()
    raporlar = sorted((KOK / "reports/analiz").glob("*.md"))
    L: list[str] = []

    L += ["# Rapor şerh denetimi — T63 ve T68 artık sınanıyor", "",
          f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
          f"**Girdi:** `reports/analiz/*.md` — **{len(raporlar)}** rapor  ",
          f"**Girdi:** `prompts/judge-eksen1.v9.md` SHA256 `{sha(RUBRIK)}` "
          f"(bayrak adları buradan)  ",
          f"**Girdi:** `configs/training/f4*.yaml` — **{len(list((KOK/'configs/training').glob('f4*.yaml')))}** "
          f"config (kol adları buradan)  ",
          f"**Kesme tarihi:** `{KESME}` — kural bu günden itibaren borç doğurur (Kural 7)", "",
          "---", "", "## Neden", "",
          "T63 ve T68 birer **yazım kuralı** bırakmıştı ve ikisi de yalnızca `plan.md`'ye",
          "yazılmıştı. ⛔ Aynı oturumda T70 bunun bedelini ölçtü: `samples.md` **iki ayrı**",
          "**yerde** ilan edilmiş, **24 koşunun hiçbirinde** üretilmemişti — çünkü ilanı",
          "sınayan bir şey yoktu. ➡️ *Bir yazım kuralı, denetlenmediği sürece bir kural*",
          "*değil bir dilektir.* Burada ikisi de **tetikleyici + uyum** çiftine çevriliyor.", "",
          "| | Tetikleyici | Uyum |", "|---|---|---|",
          "| **Ş1** (T68) | rapor bir sert kapı bayrağını **sayıyla** bildiriyor | "
          "*«üst sınır»* şerhi var |",
          "| **Ş2** (T63) | rapor **≥3 kolu** adlandırıp bir **sıra** kuruyor | "
          "*«ters çift»* sayısı var |", "",
          f"⛔ Listeler elle yazılmıyor: **{len(bayrak)} bayrak** rubrikten "
          f"({', '.join(f'`{b}`' for b in bayrak)}), **{len(kol)} kol** config'lerin "
          f"`ad:` alanından ({', '.join(f'`{k}`' for k in kol)}).", "", "---", ""]

    borclu = {"Ş1": [], "Ş2": []}
    uyan = {"Ş1": [], "Ş2": []}
    gecmis = {"Ş1": [], "Ş2": []}
    rastlantisal = {"Ş1": 0, "Ş2": 0}   # kesme öncesi olup yine de şerhi olanlar
    for p in raporlar:
        if p.name in DISLANAN:
            continue
        metin = p.read_text(encoding="utf-8")
        yeni = p.name[:10] >= KESME
        # ⭐ Önce KESME, sonra uyum: kesme öncesi rapor kuralın borçlusu değildir,
        #    şerhi olsa da olmasa da. Yoksa *«uyan»* sayısı iki ayrı şeyi karıştırır.
        v1 = s1_tetik(metin, bayrak)
        if v1:
            if not yeni:
                gecmis["Ş1"].append((p.name, len(v1)))
                rastlantisal["Ş1"] += s1_uyum(metin)
            else:
                (uyan if s1_uyum(metin) else borclu)["Ş1"].append((p.name, len(v1)))
        t2, k2 = s2_tetik(metin, kol)
        if t2:
            if not yeni:
                gecmis["Ş2"].append((p.name, len(k2)))
                rastlantisal["Ş2"] += s2_uyum(metin)
            else:
                (uyan if s2_uyum(metin) else borclu)["Ş2"].append((p.name, len(k2)))

    for ad, baslik, aciklama in [
        ("Ş1", "1. Ş1 (T68) — sert kapı sayısı bildiren rapor *«üst sınır»* diyor mu",
         "Güvenlik judge'ları **tek yönlü tedbirli sapma** gösteriyor ve bizim "
         "asimetrimiz bu sapmayı azaltmıyor, **aynı yöne ekliyor** (T68). "
         "⇒ Bildirdiğimiz ihlal sayıları **üst sınırdır** ve bu her sayının yanında "
         "yazılı olmalı."),
        ("Ş2", "2. Ş2 (T63) — kol sırası kuran rapor **ters çift** sayısı veriyor mu",
         "Eşitliğin sık olduğu 6 kolluk bir kümede sıra numarası **eşitlik bozucu ada** "
         "duyarlıdır; ilk hesap *«4 kolun sırası değişti»* dedi, doğru sayı **1**'di. "
         "⇒ Sıra yazılacaksa yanında **kesin ters dönen çift** sayısı olmalı."),
    ]:
        L += [f"## {baslik}", "", aciklama, "",
              "| | rapor |", "|---|---:|",
              f"| ⛔ **borçlu** (kesme sonrası, şerh yok) | **{len(borclu[ad])}** |",
              f"| ✅ uyan | {len(uyan[ad])} |",
              f"| ⚪ kesme öncesi (değiştirilmez, Kural 7) | {len(gecmis[ad])} |", ""]
        if borclu[ad]:
            L += ["⛔ **Borçlu raporlar:**", ""]
            L += [f"· `{n}` ({k} tetikleyici)  " for n, k in borclu[ad]] + [""]
        if uyan[ad]:
            L += ["✅ **Uyanlar:** " + ", ".join(f"`{n}`" for n, _ in uyan[ad]), ""]
        if gecmis[ad]:
            L += [f"⚪ **Kesme öncesi {len(gecmis[ad])} rapor** tetikliyor; "
                  f"{rastlantisal[ad]}'inde şerh **rastlantıyla** var. "
                  "Şerhsiz olanlar bir kusur **değil**: kural o gün yoktu ve geçmiş rapor "
                  "değiştirilmez (Kural 7). ⚠️ Ama tezde bu raporlardan sayı "
                  "alınırken şerh **oradan değil buradan** okunmalı:", ""]
            L += [", ".join(f"`{n}`" for n, _ in gecmis[ad]), ""]

    L += ["## ⛔ Bu denetimin söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ Şerhin **doğru yerde** olduğu | dizge aranıyor, konumu değil: raporun "
          "sonunda tek cümle de sayılır. ⚠️ İnsan okuması gerekli |",
          "| ⛔ Tetikleyicinin **tam** olduğu | bayrağı sayıyla bildirmenin tek biçimi "
          "tablo değil; düzyazıyla verilen bir sayı görünmez |",
          "| ⚠️ Ş2 bugün **neredeyse boş çalışıyor** | kesme sonrası tek tetikleyen rapor "
          "var ve o zaten uyuyor. Kuralın değeri ilk ihlalde ortaya çıkacak — ⭐ *boş "
          "çalışan bir denetim, yokluğu ölçülemeyen bir denetimden farklıdır* |",
          "| ⛔ Kendi raporu ve 4 denetim raporu | kapsam dışı (aşağıda), çünkü bayrak "
          "adlarını **sayarak değil alıntılayarak** taşıyorlar |", "",
          "**Kapsam dışı bırakılanlar — gerekçesiyle:**", ""]
    L += [f"· `{ad}` — {gerekce}  " for ad, gerekce in sorted(DISLANAN.items())] + [""]

    RAPOR.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✅ {RAPOR.relative_to(KOK)}")
    for ad in ("Ş1", "Ş2"):
        print(f"   {ad}: borçlu {len(borclu[ad])} · uyan {len(uyan[ad])} · "
              f"kesme öncesi {len(gecmis[ad])}")
    return 1 if (borclu["Ş1"] or borclu["Ş2"]) else 0


if __name__ == "__main__":
    sys.exit(main())
