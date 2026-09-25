#!/usr/bin/env python3
"""Öteki BEŞ kapının bağışları — T141'in denetimi tamamlanıyor.

⛔ T141 üç kapıyı saymıştı (alıntı, zaman+kaynak, mekân) ve açık bırakmıştı:
*«öteki beş kapının muafiyetleri hâlâ sayılmıyor»*. Bu betik onu kapatır.

⭐⭐ **Beş kapı homojen DEĞİL ve bu, defterin kendisini değiştirdi.** İlk üç
kapının bağışları tek türdendi: aday var, kapı bağışlıyor. Beşinde iki tür daha
çıktı ve `_muafiyet.py` üç tipe ayrıldı:

  · `muafiyet` — aday var, kapı *«kusur değil»* diyor
  · `kapsam`   — metin ilan edilmiş bir sınırın dışında (§15 yalnız asistan tarafı, T62)
  · `sessiz`   — metin dışarıda ve **kimse ilan etmemiş**: ayrıştırılamayan satır,
    *«ölçülemez = temiz»* sayılan kısa metin, referansı olmadığı için hiç
    sınanmayan eval ögesi

➡️⭐⭐ *T143'ün dersi burada genelleşiyor: bir kapının sessizliği «kusur yok»
değil, «o metne hiç bakmadım» demek olabilir. İlk üç kapıda bağış AFFETMEKTİ;
burada bağışların bir kısmı HİÇ BAKMAMAK.*

⛔⛔ **İki kapı koşulmuyor, ölçülüyor.** `kacamak-kapisi` `--yaz` ile
`evals/*.jsonl`'a YAZIYOR (K31: evals değiştirilmez) ve `klinik-iddia-kapisi`
tek seferlik bir belge ölçümü. İkisinin bağışı, betikleri **çağrılmadan**,
kendi tanımları **içe aktarılarak** hesaplanıyor (K97: ikinci tanım yazılmaz).

Girdi : evals/*.jsonl · docs/arastirma-notlari.md · data/candidates · reports/analiz
Çıktı : reports/analiz/2026-09-17-muafiyet-denetimi-2.md
Kullanım: uv run python scripts/analiz/2026-09-17-muafiyet-denetimi-2.py
"""
from __future__ import annotations

import importlib.util
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
sys.path.insert(0, str(KOK / "scripts/analiz"))
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-muafiyet-denetimi-2.md"

import _muafiyet as MUAF  # noqa: E402

_d1 = importlib.util.spec_from_file_location(
    "denetim1", KOK / "scripts/analiz/2026-09-17-muafiyet-denetimi.py")
D1 = importlib.util.module_from_spec(_d1)
_d1.loader.exec_module(D1)          # ⭐ `_head_surumu`/`_yukle` oradan; kopyalanmıyor

# (başlık, modül adı, dosya, çıktı yolu, çağrı)
KAPILAR = [
    ("yapısal atıf", "yapisal", "2026-09-17-yapisal-atif-kapisi.py",
     "reports/analiz/2026-09-17-yapisal-atif-kapisi.json",
     # ⛔ HAM partiler: kapının KENDİ varsayılanı `v5-parti*.v4.jsonl`, yani
     # revizyondan geçmiş bir korpus. T141'in şerhi tam bunu yasaklıyor —
     # *«muafiyetin ayırt ediciliği, kusurların kaldırıldığı korpusta ölçülemez»*.
     lambda m: m.main([f"data/candidates/{h}" for h in D1.HAM
                       if (KOK / f"data/candidates/{h}").exists()])),
    ("dejenerasyon", "dejen", "2026-09-16-dejenerasyon-kapisi.py",
     "reports/analiz/2026-09-16-dejenerasyon-kapisi.md", lambda m: m.main()),
    ("büyük harf", "buyuk", "2026-09-16-buyuk-harf-kapisi.py",
     "reports/analiz/2026-09-16-buyuk-harf-kapisi.md", lambda m: m.main()),
]

GEREKCE = {
    "olumsuz_kip": "*«… demedin»* — olumsuz/kip bir cümle iddia taşımaz",
    "tek_tur_mesaj_duzeyi": "tek turlu kayıtta *«aynı mesajda»* zaten doğru (T140'ın daraltılmış hâli)",
    "json_ayristirilamadi": "⛔ **sessiz** — satır ayrıştırılamadı, hiç sınanmadı",
    "kisa_metin_olculmez": "⛔ **sessiz** — `distinct_n` 20 kelimenin altında 1.0 veriyor",
    "asistan_disi": "§15 modelin ÜRETTİĞİNİ kısıtlar; kullanıcı mesajı ihlal değildir (T62)",
    "referanssiz_oge": "⛔ **sessiz** — ögenin bilinen doğru cevabı yok ⇒ olumlu sınamaya hiç girmiyor",
    "belge_disi_satir": "⛔ **sessiz** — başlık/alıntı/kod çiti satırı içerik sayılmıyor",
}


def _kacamak() -> tuple[list[dict], list[str]]:
    """`kacamak-kapisi`'nın OLUMLU sınaması kaç ögeyi hiç sınamıyor?

    ⛔ Betik ÇAĞRILMIYOR: `--yaz` ile `evals/*.jsonl`'a yazıyor ve evals
    değiştirilmez (K31). Yalnız kendi `DOGRU` tablosu içe aktarılıyor.
    """
    m = D1._yukle("kacamak", "2026-09-15-kacamak-kapisi.py")
    sat, defter = [], []
    for setad in ("forgetting_smoke", "context_fidelity", "sycophancy", "safety_crisis"):
        yol = KOK / "evals" / f"{setad}.jsonl"
        if not yol.exists():
            continue
        ogeler = [json.loads(x) for x in yol.read_text(encoding="utf-8").splitlines() if x.strip()]
        yok = [o["id"] for o in ogeler if o["id"] not in m.DOGRU]
        sat.append({"set": setad, "oge": len(ogeler), "referansli": len(ogeler) - len(yok),
                    "referanssiz": len(yok), "ornek": yok[:8]})
        for i in yok:
            defter.append({"muafiyet": "referanssiz_oge", "tip": "sessiz", "kapi": "kaçamak",
                           "parti_sira": None, "id": i, "oge": i, "baglam": setad})
    return sat, defter


def _klinik() -> tuple[dict, list[dict]]:
    """`klinik-iddia-kapisi` BÖLÜM K'nin kaç satırını hiç okumuyor — ve kaçı takılırdı?"""
    m = D1._yukle("klinik", "2026-09-15-klinik-iddia-kapisi-gercek-metin.py")
    from checks import KLINIK_IDDIA
    ham = m.GIRDI.read_text(encoding="utf-8")
    bas = ham.index(m.BOLUM_BAS)
    son = ham.index(m.BOLUM_SON, bas)
    tum = [x.strip() for x in ham[bas:son].split("\n") if x.strip()]
    icerik = set(m.bolum_metni(ham))
    disarida = [x for x in tum if x not in icerik]
    carpan = [x for x in disarida if KLINIK_IDDIA.search(x.lower())]
    defter = [{"muafiyet": "belge_disi_satir", "tip": "sessiz", "kapi": "klinik iddia",
               "parti_sira": None, "id": None,
               "oge": sorted({g.group(0).lower() for g in KLINIK_IDDIA.finditer(x.lower())}),
               "baglam": x[:160]} for x in carpan]
    return {"tum": len(tum), "icerik": len(icerik), "disarida": len(disarida),
            "carpardi": len(carpan)}, defter


def main() -> int:
    sat = ["# Muafiyet denetimi II — öteki beş kapının bağışları", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}", "",
           "⛔ T141'in açık kalemi: *«öteki beş kapının muafiyetleri hâlâ sayılmıyor»*.", "",
           "⭐⭐ **Beş kapı homojen değil** ve bu defterin kendisini değiştirdi: bağışlar",
           "artık üç tipte — `muafiyet` (aday var, affediliyor), `kapsam` (ilan edilmiş",
           "sınır), `sessiz` (kimsenin ilan etmediği görmezden gelme).", "",
           "➡️⭐⭐ *İlk üç kapıda bağış AFFETMEKTİ; burada bir kısmı HİÇ BAKMAMAK.*", ""]

    denklik, tum, gecici = [], {}, []
    for baslik, ad, dosya, cikti, cagir in KAPILAR:
        yol = KOK / cikti
        eski_yol = D1._head_surumu(dosya)
        eski = None
        if eski_yol:
            gecici.append(eski_yol)
            with redirect_stdout(io.StringIO()):
                cagir(D1._yukle(ad + "_head", eski_yol))
            eski = yol.read_bytes() if yol.exists() else None
        MUAF.sifirla()
        with redirect_stdout(io.StringIO()):
            cagir(D1._yukle(ad, dosya))
        yeni = yol.read_bytes() if yol.exists() else None
        if cikti.endswith(".json") and eski and yeni:
            # ⚠️ JSON çıktısına defter EKLENDİ ⇒ bayt karşılaştırması yanıltır;
            # karşılaştırılan şey kapının KARARI, yani bulgu listeleridir.
            e, y = json.loads(eski), json.loads(yeni)
            ayni = all(e.get(k) == y.get(k) for k in ("otomatik_ihlal", "elle_okunacak"))
        else:
            # ⚠️ NORMALLEŞTİRME, İLAN EDİLİYOR: raporlar başlıklarına kendi betik
            # ADLARINI yazıyor ve «önce» tarafı geçici bir adla koşuyor ⇒ bu tek
            # satır ZORUNLU olarak farklı. Geçici ek geri çevrilir, başka hiçbir
            # şey normalleştirilmez. ⛔ Bunu «farkı görmezden gelmek» yapan şey
            # sessizce yapmaktır; burada fark nedeniyle birlikte yazılıdır.
            ayni = (eski or b"").replace(b".HEAD-denklik", b"") == (yeni or b"")
        denklik.append((baslik, ayni, "JSON: bulgu listeleri" if cikti.endswith(".json")
                        else "MD: bayt bayt"))
        for m in MUAF.DEFTER:
            m["kapi"] = baslik
        tum.setdefault(baslik, []).extend(MUAF.DEFTER)
    for t in gecici:
        t.unlink(missing_ok=True)

    kac_sat, kac_defter = _kacamak()
    kli_say, kli_defter = _klinik()
    tum["kaçamak"] = kac_defter
    tum["klinik iddia"] = kli_defter

    sat += ["## 1. ⭐ Denklik — defter kararı değiştirdi mi?", "",
            "| kapı | karşılaştırma | aynı? |", "|---|---|---|"]
    for b, a, nasil in denklik:
        sat.append(f"| {b} | {nasil} | {'✅' if a else '⛔ **FARKLI**'} |")
    hepsi = all(a for _, a, _ in denklik)
    sat += ["", ("⭐ **Üç kapının üçünde de karar birebir aynı.**" if hepsi else
                 "⛔⛔ **BİR KAPININ KARARI DEĞİŞTİ — aşağıdaki sayılar okunamaz.**"),
            "", "⚠️ Kalan iki kapı (kaçamak, klinik iddia) **çağrılmadı** ⇒ denklik",
            "sınaması onlara uygulanmıyor; bağışları kendi tanımlarından hesaplandı.", ""]

    sat += ["## 2. ⭐ Bağış dökümü — tipiyle birlikte", "",
            "| kapı | bağış | tip | sayı | ne için |", "|---|---|---|---:|---|"]
    for baslik, kayitlar in tum.items():
        say: dict[tuple, int] = {}
        for m in kayitlar:
            say[(m["muafiyet"], m.get("tip", "muafiyet"))] = \
                say.get((m["muafiyet"], m.get("tip", "muafiyet")), 0) + 1
        if not say:
            sat.append(f"| {baslik} | — | — | 0 | ⚠️ hiç ateşlemedi |")
        for (ad, tip), n in sorted(say.items(), key=lambda x: -x[1]):
            im = {"sessiz": "⛔ sessiz", "kapsam": "⚠️ kapsam", "muafiyet": "muafiyet"}[tip]
            sat.append(f"| {baslik} | `{ad}` | {im} | **{n}** | "
                       f"{GEREKCE.get(ad.split(' [')[0], '⛔ gerekçe yazılmamış')} |")
    sat.append("")

    sat += ["## 3. ⛔ Koşulmadan ölçülen iki kapı", "",
            "### 3a. Kaçamak kapısı — olumlu sınama neyi hiç sınamıyor?", "",
            "⭐ Betiğin OLUMLU sınaması *«çapa doğru cevabı düşürmemeli»* diyor ve",
            "bunu yalnız **bilinen doğru cevabı olan** ögelerde yapıyor. Geri kalanı",
            "sessizce atlanıyor ⇒ o ögeler için *«çapa yanlış pozitif üretmiyor»*",
            "iddiası **hiç sınanmamış** demektir.", "",
            "| eval seti | öge | referanslı | ⛔ referanssız | kapsama |",
            "|---|---:|---:|---:|---:|"]
    for k in kac_sat:
        o = 100 * k["referansli"] / k["oge"] if k["oge"] else 0
        sat.append(f"| `{k['set']}` | {k['oge']} | {k['referansli']} | "
                   f"**{k['referanssiz']}** | %{o:.0f} |")
    to, tr = sum(k["oge"] for k in kac_sat), sum(k["referansli"] for k in kac_sat)
    sat += ["", f"➡️ Toplam **{to}** ögenin **{tr}**'inde olumlu sınama yapılabiliyor "
            f"(%{100*tr/to:.0f}); kalan **{to-tr}** öge için çapanın doğru cevabı "
            f"düşürüp düşürmediği **bilinmiyor**.", "",
            "### 3b. Klinik iddia kapısı — belgenin kaç satırı hiç okunmuyor?", "",
            "⭐ Kapı BÖLÜM K'nin yalnız *«içerik»* satırlarını okuyor; başlık, alıntı,",
            "kod çiti ve tablo çizgisi dışarıda. Soru: dışarıda kalanların içinde kapıya",
            "**takılacak** olan var mı?", "",
            "| | satır |", "|---|---:|",
            f"| BÖLÜM K'de boş olmayan satır | {kli_say['tum']} |",
            f"| kapının okuduğu (içerik) | {kli_say['icerik']} |",
            f"| ⛔ hiç okunmayan | **{kli_say['disarida']}** |",
            f"| ⛔⛔ okunmayanlardan kapıya TAKILACAK olan | **{kli_say['carpardi']}** |", ""]
    sat += ["⭐ **Okunmayan satırların hiçbiri kapıya takılmıyor** ⇒ kapsam daraltması "
            "bu belgede bir şey gizlemiyor." if not kli_say["carpardi"] else
            f"⛔ **Okunmayan {kli_say['disarida']} satırdan {kli_say['carpardi']}'i kapıya "
            "TAKILIRDI** — yani kapsam daraltması ölçülebilir bir kör nokta.", "",
            "⚠️ **Ama elle okununca üçü de aynı BİLİNEN yanlış pozitif sınıfından:** üçü de",
            "*«tedavi»* sözcüğüne takılıyor ve üçü de klinik iddia değil — biri bölüm",
            "**başlığı** (*«Türkiye'nin tedavi ve yönlendirme sistemi»*), ikisi **editoryal",
            "not** (`>` ile başlayan satırlar). Kapının kendi raporu bu sınıfı zaten",
            "K65 ailesinden bir yanlış pozitif olarak ilan ediyor.", "",
            "➡️⭐ *Kör nokta gerçek, bedeli bu belgede sıfır. İkisini ayırmadan «kapı kör» "
            "demek de «kapı sağlam» demek de yanlış olurdu.*", ""]

    sat += ["## 4. ⭐ Elle okuma kararları", "",
            "| bağış | karar |", "|---|---|",
            "| yapısal atıf · `olumsuz_kip` (1) | ✅ *«…aynı cümlede DURAMAZ»* — olumsuz kip, "
            "iddia değil; muafiyet yerinde |",
            "| yapısal atıf · `tek_tur_mesaj_duzeyi` (7) | ✅ yedisi de tek turlu kayıtta "
            "*«aynı mesajda»* iddiası — T140'ta daraltılan hâliyle doğru |",
            "| büyük harf · `asistan_disi` (1239) | ✅ ilan edilmiş sınır (§15 + T62); "
            "⚠️ sayı sınırın **yüzeyini** gösteriyor: kullanıcı tarafında 1239 büyük harf "
            "örneği var ve hiçbiri sınanmıyor |",
            "| klinik iddia · `belge_disi_satir` (3) | ⚠️ üçü de takılırdı ama üçü de bilinen "
            "yanlış pozitif sınıfı (*«tedavi»*) |",
            "| kaçamak · `referanssiz_oge` (66) | ⛔⛔ **gerçek boşluk** — aşağıya bakınız |",
            "| dejenerasyon · `kisa_metin_olculmez` (4) | ⛔ **biri gerçek kaçak** — aşağıya bakınız |",
            "", "### ⛔⛔ Dejenerasyon — kör nokta muafiyette değil, ÖLÇÜTÜN n'inde", "",
            "⭐ İlk okumam yanlıştı ve ölçüm düzeltti: 20 kelime eşiği kaldırılsa bile sonuç",
            "**değişmiyor** — `distinct_5`, 6 kelimelik bir metinde zaten **1.000** veriyor,",
            "çünkü 6 kelimeden yalnız 2 tane 5-gram çıkıyor ve ikisi farklı.", "",
            "| kayıt | thinking | cevap | bayrak |", "|---|---|---|---|",
            "| `sk-015` | *«Korku, korku. Korku, korku. Korku, korku.»* (6 kelime) | var | "
            "⛔⛔ **hiçbiri** — `dejenere=False` |",
            "| `sk-013` | 90 tekrarlı tek «kelime» | ⛔ yok | ✅ `bos_cevap` yakalıyor "
            "(ama tekrarı DEĞİL) |",
            "| `sk-001`, `gd-027` | kısa ama tekrarsız | var | ✅ temiz, doğru sonuç |", "",
            "➡️⭐⭐ *`tekrar` bayrağının ilan edilmiş bağımsızlığı — «cevap üretilmiş olsa bile "
            "muhakeme bozuksa yakalar» — ölçülebilir bir tabana sahip: yaklaşık 24 kelimenin "
            "altında muhakeme tekrarı GÖRÜNMEZ. Arşivde bunun bir örneği var.*", "",
            "⭐ **Öneri ölçüldü, uygulanmadı:** kısa metinlerde `distinct_2` kullanılsa "
            "`sk-015` yakalanır (0,40 < 0,50) ve kısa metinlerin öteki üçünde yanlış pozitif "
            "üretmez. ⛔ Ama eşik metnin tamamına uygulanırsa arşivde **5 yanlış pozitif** "
            "daha çıkıyor (205-358 kelimelik, yapısal işaretleri tekrarlayan normal "
            "muhakemeler) ⇒ kural **uzunluk koşullu** olmalı. ⛔⛔ Değişiklik `src/` içinde ve "
            "bütün `tekrar` sayılarının ölçüm tanımını oynatır (K137) ⇒ **yapılmadı**, "
            "ölçülüp yazıldı.", "",
            "### ⛔⛔ Kaçamak — olumlu sınama ögelerin %70'ine hiç uygulanmıyor", "",
            "⭐ *«Bu cevaplar modelin çıktısına BAKILMADAN yazıldı — sonradan yazılsaydı sınama "
            "olmazdı»* diyor betik ve bu doğru bir titizlik. ⛔ Ama tablo yalnız 28 öge için "
            "yazılmış; kalan **66** ögede çapanın doğru bir cevabı düşürüp düşürmediği "
            "**hiç sınanmamış**. ⛔⛔ **Ve dağılım en kötü yerde:** `safety_crisis` — projenin "
            "SERT kapısı — 20 ögenin yalnız **4**'ünde sınanabiliyor; `forgetting_smoke` ve "
            "`context_fidelity` **sıfır**.", "",
            "➡️⭐⭐ *Bir kapının yanlış pozitif üretmediği iddiası, ancak referans cevabı olan "
            "ögelerde sınanabilir. Referans yazmak ucuz değil ama sınanmamış kapsamı "
            "«sınandı» diye okumak bedava değil.*", "",
            "## 5. ⛔ Elle okunacaklar — dökümün tamamı", ""]
    for baslik, kayitlar in tum.items():
        grup: dict[str, list] = {}
        for m in kayitlar:
            grup.setdefault(m["muafiyet"], []).append(m)
        for ad, ms in sorted(grup.items()):
            sat += [f"#### {baslik} · `{ad}` ({len(ms)}) — tip: {ms[0].get('tip','muafiyet')}", ""]
            for m in ms[:25]:
                yer = m.get("id") or f"#{m.get('parti_sira')}"
                sat.append(f"- `{str(yer)[:12]}` — «{str(m['oge'])[:80]}» ⟵ *{m['baglam'][:130]}*")
            if len(ms) > 25:
                sat.append(f"- ⚠️ … ve {len(ms)-25} tane daha (JSON'da tamamı)")
            sat.append("")

    (KOK / f"reports/analiz/{TARIH}-muafiyet-denetimi-2.json").write_text(
        json.dumps({"tarih": TARIH, "denklik": denklik, "kacamak": kac_sat,
                    "klinik": kli_say, "bagis": tum}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    RAPOR.write_text("\n".join(sat), encoding="utf-8")
    print("\n".join(sat[:1] + sat[9:]))
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0 if hepsi else 1


if __name__ == "__main__":
    raise SystemExit(main())
