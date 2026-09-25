#!/usr/bin/env python3
"""judge v7'nin beş değişikliğinin sayısal dayanağı — rubrik yazılmadan ÖNCE ölçüldü.

Üç kalem `2026-09-15-korpus-v6-isaret-ayiklamasi.md`'de zaten ölçülüydü (RAG yanlış
pozitifi Fisher p = 0.0001 · iki `teselli_kalip` judge hatası); onlar burada
TEKRARLANMAZ, atıfla geçilir. Bu betik yalnızca **henüz hiçbir raporda olmayan**
dört sayıyı üretir:

  A. Bölüm F alıntı alanlarının doluluk oranı        → F3a ifadesi neden değişiyor
  B. `siz_kaymasi` gd-006: üç dalga, iki farklı cevap → dilbilgisel çoğul istisnası
  C. Çıktı şablonu belirsizliği: aynı dalga bölündü   → şablondan üç alan çıkıyor
  D. Bağlam doğrulaması: kaçış bir muafiyet mi, kanıt mı

⚠️ A ve D gözlemdir, nedensellik kanıtı değildir — hangi cümle rapor metninde
   hangi güçte yazıldığına dikkat edildi (Kural 6).

Kullanım: uv run python scripts/analiz/2026-09-15-v7-gerekce.py
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⚠️ GİRDİ BİR DİZİN GLOB'U: `reports/analiz/ham-judge/*.jsonl`. Arşive her yeni
# aile eklendiğinde tabloya satır giriyor, dolayısıyla betik kendi 09-15 raporunu
# yeniden üretemez. 09-16'da eklenen satırların hepsi `0` — hiçbir iddia değişmiyor,
# ama tablo büyüyor. ➡️ Bir raporun girdisi "o an ne varsa" ise, hangi sürümü
# anlattığı yazılı DEĞİLDİR (Kural 7).

# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
KORPUS = KOK / "data/judged/v3-kumulatif.v6.jsonl"
HAM = KOK / "reports/analiz/ham-judge"
RAPOR = KOK / f"reports/analiz/{TARIH}-v7-gerekce.md"

DALGALAR = {
    "gemini-v6": KOK / "reports/analiz/golden-kosu/20260915-012409-baseline-v6/sonuclar.jsonl",
    "claude-varsayilan": KOK / "reports/analiz/golden-kosu/20260915-063352-golden-baseline-claude/sonuclar.jsonl",
    "claude-sonnet": KOK / "reports/analiz/golden-kosu/20260915-080807-golden-baseline-sonnet/sonuclar.jsonl",
}

# Bölüm F'nin altı alıntı alanı + B1. Sırası rubrikteki sıra.
ALINTI_ALANLARI = [
    ("en_belirsiz_cumle", "B1", "en az anlaşılır cümleyi alıntıla"),
    ("en_somut_ayrinti", "F1a", "en somut ayrıntıyı alıntıla"),
    ("rol_sinirina_en_yakin", "F2a", "en çok YAKLAŞAN cümleyi alıntıla"),
    ("guvenlige_en_yakin", "F3a", "şu üçünden BİRİNİ YAPAN cümleyi alıntıla"),
    ("kisiye_dair_en_genel", "F4a", "en genelleyici ifadeyi alıntıla"),
    ("sorumluluga_en_yakin", "F5a", "en çok DEĞİNEN cümleyi alıntıla"),
    ("en_teselli_edici", "F6a", "en teselli edici cümleyi alıntıla"),
]

TURETILEN = ("bos_guvence", "tuzak_etiketleme", "tuzak_suclama")

# Hangi yanlış pozitifi v7'nin hangi değişikliği kapatıyor — BENİM OKUMAM (Kural 6),
# aşağıdaki kök eşleşmesi tablosu okunarak verildi.
MEKANIZMA = {
    "16c95f92088a": "`rol_bilgi_baglamdan` (bağlam kaçışı)",
    "52545776925e": "`rol_bilgi_baglamdan` (bağlam kaçışı)",
    "620a46f81e40": "F2b kanıt kapısı — cümle özerklik cümlesi, `rol_alani` = `yok`",
    "28f93b83dc7a": "F2b kanıt kapısı — cümle izin sorusu, `rol_alani` = `yok`",
    "4b31c887aa3a": "F2b kanıt kapısı — kullanıcının sözünün yansıtması, `rol_alani` = `yok`",
}


def sha(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()


def dolu(deger) -> bool:
    v = (deger or "").strip()
    return bool(v) and v.upper() not in ("YOK", "YOK.")


def govdeler(kayit: dict) -> tuple[str, str]:
    """(kullanıcının kendi sözleri, verilen bağlam metni) — küçük harfe indirilmiş."""
    kul = " ".join(m["content"] for m in kayit["messages"] if m["role"] == "user")
    bag = " ".join((k.get("metin") or k.get("text") or "")
                   for k in (kayit.get("context") or []))
    return kul.lower(), bag.lower()


KELIME = re.compile(r"[a-zçğıöşü]{5,}")


def kok_orani(cumle: str, metin: str) -> tuple[int, int]:
    """Cümlenin içerik kelimelerinden kaçı metinde geçiyor (6 harflik kök önekiyle).

    Türkçe çekimli; tam kelime eşleşmesi «hâller» ile «hâlleri»ni ayrı sayardı.
    Kök öneki kaba bir vekildir — kesinlik iddiası yok, yön göstergesi.
    """
    kokler = {k[:6] for k in KELIME.findall(cumle.lower())}
    if not kokler:
        return 0, 0
    return sum(1 for k in kokler if k in metin), len(kokler)


def main() -> None:
    kayitlar = [json.loads(l) for l in KORPUS.open()]
    judged = [(r, r["judge"]) for r in kayitlar if r.get("judge")]
    n = len(judged)
    y = [f"# judge v7 — beş değişikliğin sayısal dayanağı", "",
         f"- tarih: {TARIH} · betik: `scripts/analiz/{Path(__file__).name}`",
         f"- korpus: `{KORPUS.relative_to(KOK)}` · SHA256 `{sha(KORPUS)[:16]}…` · kayıt: {n}",
         "",
         "> RAG yanlış pozitifi (Fisher **p = 0.0001**) ve iki `teselli_kalip` judge hatası",
         "> `2026-09-15-korpus-v6-isaret-ayiklamasi.md`'de ölçüldü; burada tekrarlanmıyor.",
         ""]

    # ---- A. Alıntı alanlarının doluluk oranı --------------------------------
    y += ["## A. Bölüm F alıntı alanları — hangisi doluyor (F3a gerekçesi)", "",
          "Bölüm F'nin deseni *önce alıntıla, sonra yalnızca o alıntı hakkında karar ver*.",
          "Alıntı boş kalırsa **ikinci adım hiç sorulmaz** — o boyut o kayıtta ölçülmemiş olur.",
          "",
          "| Alan | Soru | Talimatın kipi | Dolu |",
          "|---|---|---|---:|"]
    for alan, bolum, kip in ALINTI_ALANLARI:
        d = sum(1 for _, j in judged if dolu(j.get(alan)))
        kosullu = "**koşullu**" if "BİRİNİ YAPAN" in kip else "en yakın"
        y.append(f"| `{alan}` | {bolum} | {kosullu} | {d}/{n} (%{100*d/n:.0f}) |")
    g = sum(1 for _, j in judged if dolu(j.get("guvenlige_en_yakin")))
    y += ["",
          f"`guvenlige_en_yakin` **{n-g}/{n}** kayıtta boş — yedi alanın en düşüğü. Talimatı da",
          "tek farklı olan o: diğerleri *\"en yakın cümleyi yaz\"* derken F3a *\"şu üçünden birini",
          "yapan cümleyi\"* diyor, yani judge önce bir **eşik** kararı veriyor, alıntıyı ancak",
          "eşiği geçerse yazıyor.",
          "",
          "⚠️ **Bu bir korelasyon, nedensellik değil.** Korpus zaten güvenlik kusurundan kaçınmak",
          "için yazıldı; düşük doluluk gerçeği yansıtıyor da olabilir. Değişikliğin dayanağı",
          "bu sayı değil, **maliyet asimetrisi**: F3a koşullu kaldığında `guvenlik_tipi` sorusu",
          f"kayıtların %{100*(n-g)/n:.0f}'inde hiç sorulmuyor ve sıfır toleranslı eksen ikinci bakışı",
          "kaybediyor. Koşulu kaldırmak yanlış pozitif üretmez: `guvenlik_tipi`'nin `yok` çıkışı",
          "duruyor ve türetme `!= \"yok\"` şartına bağlı (`src/filter.py::f_bolumu_turet`).",
          ""]

    # ---- B. siz_kaymasi gd-006 ---------------------------------------------
    y += ["## B. `siz_kaymasi` — dilbilgisel çoğul (gd-006)", ""]
    cevap = ""
    satirlar = []
    for ad, yol in DALGALAR.items():
        d = {json.loads(l)["id"]: json.loads(l) for l in yol.open()}
        r = d.get("gd-006")
        if not r:
            continue
        cevap = cevap or r.get("cevap", "")
        j = r.get("judge") or {}
        toplam = sum(1 for x in d.values() if (x.get("judge") or {}).get("siz_kaymasi"))
        satirlar.append(f"| {ad} | `{j.get('siz_kaymasi')}` | {toplam}/48 |")
    cumle = next((c.strip() for c in re.split(r"(?<=[.!?])\s+", cevap) if "yaşıyorsanız" in c), "")
    y += [f"> «{cumle}»", "",
          "| Dalga | gd-006 `siz_kaymasi` | Dalgada toplam |", "|---|:--:|---:|"] + satirlar
    y += ["",
          "Cevap `sen` register'ını **koruyor** — *\"sen veya arkadaşın\"*. `-sanız` çekimi",
          "`siz` hitabı değil, **iki özneli** yüklemin zorunlu çoğulu. Gemini bunu ayırdı,",
          "iki Claude dalgası da ayıramadı.",
          "",
          "⚠️ Bu tek kayıt iki judge'ı ayıran **tek** uyuşmazlık: sapma raporunda `siz_kaymasi`",
          "%98 ham uyum ve κ=0.95 ile en uyumlu bayraklardan biri. Yani sorun bayrağın",
          "geneli değil, tanımında kapatılmamış tek delik.",
          ""]

    # ---- C. Çıktı şablonu belirsizliği -------------------------------------
    y += ["## C. Çıktı şablonu — not ile şablon çelişiyor", "",
          "v6 şablonu `bos_guvence`, `tuzak_etiketleme`, `tuzak_suclama` alanlarını **listeliyor**;",
          "aynı dosyanın altındaki not *\"bunlar çıktıda YOKTUR, kod hesaplar\"* diyor.",
          "Sonuç, **aynı dalga içinde** bölünme:", "",
          "| Dalga | n | üç alanı yazan | yazmayan |", "|---|---:|---:|---:|"]
    riskli_toplam = 0
    for yol in sorted(HAM.glob("*.jsonl")):
        kayitlar_ham = [json.loads(l) for l in yol.open()]
        yazan = yazmayan = riskli = 0
        for k in kayitlar_ham:
            ham = k["ham"].strip()
            if ham.startswith("```"):
                ham = ham.split("```")[1].removeprefix("json").strip()
            try:
                d = json.loads(ham)
            except Exception:
                continue
            if any(a in d for a in TURETILEN):
                yazan += 1
            else:
                yazmayan += 1
            # Sessiz kırılma yolu: judge `bos_guvence` yazmış AMA türetmeyi
            # tetikleyen iki teselli alanını yazmamış → judge'ın değeri AYAKTA KALIR.
            if ("bos_guvence" in d and "teselli_kalip" not in d
                    and "teselli_kullanicinin_sozunden" not in d):
                riskli += 1
        riskli_toplam += riskli
        y.append(f"| `{yol.stem}` | {len(kayitlar_ham)} | {yazan} | {yazmayan} |")
    y += ["",
          "Bugün sonucu değiştirmedi: `f_bolumu_turet()` üçünü de üzerine yazıyor. Ama **koşullu**",
          "yazıyor — `if \"teselli_kalip\" in data or …`. Judge `bos_guvence` yazıp o iki alanı",
          "yazmasaydı türetme dalı hiç ateşlemez ve **judge'ın kendi değeri `dogallik` puanına",
          f"girerdi.** Bu yol bugün {riskli_toplam} kayıtta gerçekleşti — ama açık duruyor;",
          "K44/K47/K49 ile aynı aile: hata vermeyen, sessizce yanlış çalışan katman.",
          "",
          "**v7:** üç alan şablondan çıkarılır. Belirsizlik ortadan kalkar, yol kapanır.",
          ""]

    # ---- D. Bağlam kaçışı: muafiyet mi, kanıt mı ---------------------------
    y += ["## D. Beş yanlış pozitif tek mekanizmayla kapanmıyor", "",
          "Ayıklama raporu beş yanlış pozitifin hepsini RAG kaçışına bağlamıştı. Alıntılanan",
          "cümlenin içerik köklerini **verilen bağlamda** ve **kullanıcının kendi sözlerinde**",
          "ayrı ayrı arayınca ikiye ayrıldılar:", "",
          "| Kayıt | Bağlam | kökler bağlamda | kullanıcının sözünde | v7'de kapatan mekanizma |",
          "|---|:--:|---:|---:|---|"]
    bayrakli = [(r, j) for r, j in judged if j.get("rol_siniri_ihlali")]
    for r, j in sorted(bayrakli, key=lambda t: t[0]["id"]):
        cumle = j.get("rol_sinirina_en_yakin") or ""
        kul, bag = govdeler(r)
        b_var, b_top = kok_orani(cumle, bag)
        k_var, _ = kok_orani(cumle, kul)
        isaret = "✓" if r.get("context") else ""
        mek = MEKANIZMA.get(r["id"][:12], "?")
        y.append(f"| `{r['id'][:12]}` | {isaret} | {b_var}/{b_top} | {k_var}/{b_top} | {mek} |")
    y += ["",
          "**Yalnızca ikisinde** (`16c95f92088a` 6/7, `52545776925e` 13/16) alıntılanan cümlenin",
          "bilgisi gerçekten bağlam belgesinde duruyor — kaçış bunları kapatır ve kaçışın",
          "isteyeceği alıntı fiilen mevcut.",
          "",
          "Kalan üçünde bağlam örtüşmesi yok (0/3 · 2/9 · 0/6) çünkü sorun başka: **alıntılanan",
          "cümle rol sınırı alanına hiç girmiyor.** «Söylemek zorunda değilsin» bir özerklik",
          "cümlesi, «Bugün işine yarar mı?» izin sorusu, «sabah ve öğlene doğru bir şey alıyorsun»",
          "kullanıcının sözünün yansıtması. Judge üçünde de `rol_alani`'na `yok` demeliydi;",
          "`yok` çıkışı v6'da **zaten var** ve kullanılmadı.",
          "",
          "Yani kaçış tek başına 5 yanlış pozitifin **2'sini** kapatır. v7 bu yüzden ikinci adımı",
          "da kanıta bağlıyor: `rol_alani` bir alana atanacaksa cümlenin **hangi iddiayı** taşıdığı",
          "yazılacak (tanı adı · doz/kullanım talimatı · protokol adımı · hukuki sonuç). Yazılamıyorsa",
          "`yok`. Aynı desen Bölüm B'de ve F1'de işe yaradı: soyut soru varsayılana oturuyor,",
          "alıntı zorunluluğu bakmaya zorluyor.",
          "",
          "⚠️ Kök öneki eşleşmesi kaba bir vekildir ve **kanıt üretmez**; hangi kaydın hangi",
          "mekanizmaya düştüğü benim okumamdır (Kural 6). Tablonun kurduğu tek şey şu: beş vaka",
          "homojen değil, tek düzeltmeyle kapandığını varsaymak yanlış olurdu.",
          "",
          "---", "",
          "## Bağlam taşıyan kayıt sayısı — iki yöntem, iki sayı", "",
          f"- `context` alanı dolu: **{sum(1 for r in kayitlar if r.get('context'))}/{len(kayitlar)}**",
          "- gövde metninde bağlam işareti arayan regex (ayıklama raporu): **9**",
          "",
          "Fark tek kayıt ve sebebi K17: bağlam kullanıcı turunun içine gömülür, ama",
          "parafraz edildiyse gövdede işaret kalmaz. **Doğru ölçüt `context` alanıdır**;",
          "ayıklama raporunun Fisher tablosu regex'e dayandığı için o kaydı bağlamsız saydı",
          "— yön değişmiyor, testin gücü bir kayıt kadar eksik hesaplanmış oldu.",
          ""]

    RAPOR.write_text("\n".join(y))
    print(f"yazıldı: {RAPOR.relative_to(KOK)}")


if __name__ == "__main__":
    main()
