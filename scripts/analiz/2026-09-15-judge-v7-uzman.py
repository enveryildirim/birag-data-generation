#!/usr/bin/env python3
"""v7'yi İNSAN çapasına karşı ölçer — expert-70, tek uzman, 50 puanlı kayıt.

Bugüne kadarki bütün judge ölçümleri **göreliydi**: judge'lar birbirine, rubrikler
birbirine karşı. Doğru cevabın nerede olduğunu söyleyen tek kaynak bu 50 kayıt.

⚠️ Üç sınır baştan yazılı, çünkü sonucu bunlar belirliyor:

  1. **Tek uzman.** Anotatör uyumu yok; "uzman haklı" değil "uzman böyle dedi" denir.
  2. **Uzman formu v1 rubriğine göreydi.** Ortak zemin yalnızca altı alan; uzmanın
     `kisalik_dogallik`/`dil_butunlugu`'su v7'de yok, v7'nin bayraklarının çoğu
     uzman formunda yok.
  3. **İki sert kapıda uzmanda VARYANS YOK** (50/50 "Hayır") ve `tuzak_ihlali` boş.
     Orada "uyum" ölçülemez; ölçülebilen tek şey judge'ın YANLIŞ POZİTİFİ.

⚠️ v2/v3/v4 Gemini ile, v7 Claude Sonnet ile puanlandı (K97). Bu betik onları
birbirine karşı DEĞİL, **her birini ayrı ayrı insana karşı** koyar. Fark bir rubrik
farkı değil **judge+rubrik çifti** farkıdır ve öyle yazılır.

Kullanım: uv run python scripts/analiz/2026-09-15-judge-v7-uzman.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import statistics as st
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
PUAN = KOK / "data/expert_sample/uzman-puanlari.json"
SURUM = {"v4 · gemini": KOK / "data/judged/expert-70.v4.jsonl",
         "v7 · sonnet": KOK / "data/judged/expert-70.v7.jsonl"}
RAPOR = KOK / f"reports/analiz/{TARIH}-judge-v7-uzman.md"

EPITOME = ["duygusal_tepki", "yorumlama", "kesif"]
KAPILAR = ["klinik_guvenlik_ihlali", "rol_siniri_ihlali"]
ALINTI_ALANI = {"klinik_guvenlik_ihlali": "guvenlige_en_yakin",
                "rol_siniri_ihlali": "rol_sinirina_en_yakin"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def oku(p: Path) -> dict[str, dict]:
    return {json.loads(s)["id"]: (json.loads(s).get("judge") or {})
            for s in p.read_text().splitlines() if s.strip()}


def auc(dusuk: list, yuksek: list) -> float | None:
    """P(rastgele 'iyi' kayıt, rastgele 'kötü' kayıttan yüksek puan alır). 0.5 = kör."""
    if not dusuk or not yuksek:
        return None
    return sum(1.0 if d < y else 0.5 if d == y else 0.0
               for d in dusuk for y in yuksek) / (len(dusuk) * len(yuksek))


def main() -> None:
    puanlar = json.loads(PUAN.read_text())["uzmanlar"]["a"]["puanlar"]
    veri = {ad: oku(p) for ad, p in SURUM.items()}
    esli = [up for up in puanlar.values()
            if all(veri[s].get(up["kayit_id"]) for s in SURUM)]
    n = len(esli)

    y = ["# judge v7 — insan çapasına karşı (expert-70)", "",
         f"- tarih: {TARIH} · betik: `scripts/analiz/{Path(__file__).name}`",
         f"- uzman: `{PUAN.relative_to(KOK)}` · SHA256 `{sha(PUAN)}…` · puanlanan {len(puanlar)}"]
    for ad, p in SURUM.items():
        y.append(f"- {ad}: `{p.relative_to(KOK)}` · SHA256 `{sha(p)}…`")
    y += [f"- her iki sürümde de puanlanmış ve uzmanın değerlendirdiği kayıt: **{n}**", "",
          "⚠️ **Tek uzman, anotatör uyumu yok** — *\"uzman haklı\"* değil *\"uzman böyle dedi\"*.",
          "⚠️ **v4 Gemini, v7 Sonnet ile puanlandı (K97).** İkisi burada birbiriyle değil,",
          "**ayrı ayrı insanla** karşılaştırılıyor. Aradaki fark rubrik farkı değil,",
          "**judge+rubrik çifti** farkıdır; hangi bileşenden geldiği bu koşudan çıkarılamaz.", ""]

    # --- 0. Çapanın kendi sınırları ------------------------------------------
    y += ["## 0. Çapa neyi ölçebilir, neyi ölçemez", "",
          "| Uzman alanı | Dağılım | Ölçüm değeri |", "|---|---|---|"]
    for alan in KAPILAR:
        d = collections.Counter(up.get(alan) for up in esli)
        y.append(f"| `{alan}` | {' · '.join(f'{k}×{v}' for k, v in d.items())} | "
                 f"⛔ varyans yok — yalnızca **yanlış pozitif** sayılabilir |")
    tz = sum(len(up.get("tuzak_ihlali") or []) for up in esli)
    y.append(f"| `tuzak_ihlali` | {tz} işaret | ⛔ boş — uyum ölçülemez |")
    for alan in EPITOME:
        d = collections.Counter(up.get(alan) for up in esli)
        eksik = d.pop(None, 0)
        pay = max(d.values()) / sum(d.values())
        y.append(f"| `{alan}` | {' · '.join(f'{k}×{v}' for k, v in sorted(d.items()))}"
                 f"{f' · eksik×{eksik}' if eksik else ''} | "
                 f"{'⚠️ çarpık (%' + f'{100*pay:.0f}' + ' tek değerde)' if pay > 0.7 else '✅ kullanılabilir'} |")
    d = collections.Counter(up.get("mi_uyumu") for up in esli)
    eksik = d.pop(None, 0)
    y.append(f"| `mi_uyumu` | {' · '.join(f'{k}×{v}' for k, v in sorted(d.items()))} · eksik×{eksik} | "
             f"⚠️ {eksik}/{n} boş bırakılmış |")
    d = collections.Counter(up.get("genel_karar") for up in esli)
    y.append(f"| `genel_karar` ⭐ | {' · '.join(f'{k}×{v}' for k, v in d.items())} | "
             "✅ **en bilgilendirici değişken** |")
    y += ["",
          "Uzman iki sert kapının ikisinde de **hiç ihlal görmedi**. Bu, korpusun temiz olduğu",
          "anlamına gelebileceği gibi uzmanın o eksende ayrım yapmadığı anlamına da gelebilir —",
          "ikisi bu veriyle ayrılamaz. Ama tek yönlü bir şey **söylenebilir**: judge oralarda",
          "ateşlediyse insan onu doğrulamıyor.", ""]

    # --- 1. Sert kapılarda yanlış pozitif ------------------------------------
    y += ["## 1. ⭐ Sert kapılar — judge insanın görmediğini görüyor mu", "",
          "| Judge | `klinik_guvenlik_ihlali` | `rol_siniri_ihlali` |", "|---|---:|---:|"]
    for ad in SURUM:
        satir = [f"| {ad} "]
        for alan in KAPILAR:
            k = sum(1 for up in esli if veri[ad][up["kayit_id"]].get(alan))
            satir.append(f"| {k}/{n} ")
        y.append("".join(satir) + "|")
    y += ["", "> Uzman ikisinde de 0 dedi; buradaki her ateşleme **insana göre yanlış pozitif adayıdır**.",
          "> \"Aday\" çünkü tersi de mümkün: judge insanın kaçırdığını görmüş olabilir (K43'te iki kez oldu).", ""]

    for alan in KAPILAR:
        satirlar = []
        for ad in SURUM:
            for up in esli:
                j = veri[ad][up["kayit_id"]]
                if j.get(alan):
                    satirlar.append(f"| {ad} | `{up['kayit_id'][:12]}` | "
                                    f"«{(j.get(ALINTI_ALANI[alan]) or '')[:64]}» |")
        if satirlar:
            y += [f"### `{alan}` ateşlemeleri — alıntılarıyla", "",
                  "| Judge | Kayıt | Judge'ın çıkardığı cümle |", "|---|---|---|"] + satirlar + [""]

    # --- 2. genel_karar ayrımı ------------------------------------------------
    y += ["## 2. ⭐ Uzmanın `genel_karar`'ını ayırt edebiliyor mu", "",
          "Uzmanın en çok varyans taşıyan değişkeni bu. Soru: judge'ın puanı, uzmanın",
          "**kabul** dediği kayıtları **sınırda/ret** dediklerinden ayırıyor mu?", "",
          "AUC = rastgele bir *kabul* kaydının, rastgele bir *sınırda/ret* kaydından yüksek",
          "puan alma olasılığı. **0.5 = kör**, 1.0 = tam ayrım.", "",
          "| Boyut | " + " | ".join(SURUM) + " |",
          "|---|" + "---:|" * len(SURUM)]
    iyi = [up for up in esli if up.get("genel_karar") == "kabul"]
    kotu = [up for up in esli if up.get("genel_karar") in ("sınırda", "ret")]
    for boyut in ["anlasilirlik", "dogallik", "mi_uyumu", "grounding"] + EPITOME:
        hucre = []
        for ad in SURUM:
            d = [veri[ad][up["kayit_id"]].get(boyut) for up in kotu]
            h = [veri[ad][up["kayit_id"]].get(boyut) for up in iyi]
            d = [x for x in d if isinstance(x, (int, float))]
            h = [x for x in h if isinstance(x, (int, float))]
            a = auc(d, h)
            hucre.append("—" if a is None else f"{a:.2f}")
        y.append(f"| `{boyut}` | " + " | ".join(hucre) + " |")
    y += ["",
          f"n: kabul **{len(iyi)}** · sınırda+ret **{len(kotu)}**. Bu büyüklükte AUC'nin güven",
          "aralığı geniştir; 0.5'e yakın değerler *\"ayırmıyor\"*, 0.5'ten uzak olanlar",
          "*\"ayırıyor olabilir\"* diye okunur — kanıt değil işaret.", ""]

    # --- 3. EPITOME birebir uyum ---------------------------------------------
    y += ["## 3. EPITOME boyutlarında birebir uyum", "",
          "| Boyut | " + " | ".join(f"{ad} birebir · ort. fark" for ad in SURUM) + " |",
          "|---|" + "---|" * len(SURUM)]
    for boyut in EPITOME:
        hucre = []
        for ad in SURUM:
            cift = [(up[boyut], veri[ad][up["kayit_id"]].get(boyut)) for up in esli
                    if isinstance(up.get(boyut), int)
                    and isinstance(veri[ad][up["kayit_id"]].get(boyut), int)]
            birebir = sum(1 for u, j in cift if u == j) / len(cift)
            kayma = st.mean(j - u for u, j in cift)
            hucre.append(f"%{100*birebir:.0f} · {kayma:+.2f}")
        y.append(f"| `{boyut}` | " + " | ".join(hucre) + " |")
    y += ["",
          "*Ort. fark* judge eksi uzman: eksi değer judge'ın **daha sert** olduğunu söyler.",
          "",
          "⚠️ Uzmanın bu üç boyutta dağılımı çarpık (%75+ tek değerde). Yüksek birebir uyum,",
          "ayırt etme gücü değil **çoğunluk değerini tutturma** olabilir — §2'deki AUC bu",
          "yüzden daha bilgilendirici.", ""]

    # --- 4. Aynı kayıt, iki farklı gerekçe -----------------------------------
    odak = next((up for up in esli if up["kayit_id"].startswith("7e23c0dbb5a2")), None)
    if odak:
        j = veri["v7 · sonnet"][odak["kayit_id"]]
        y += ["## 4. ⭐ Aynı kaydı ikisi de reddetti — farklı gerekçeyle", "",
              f"`{odak['kayit_id'][:12]}` · uzman `genel_karar` = **{odak['genel_karar']}** · "
              f"uzman `klinik_guvenlik_ihlali` = **{odak['klinik_guvenlik_ihlali']}**", "",
              "**Kullanıcı:** *\"sabahları kalkarken göğsüm ağırlaşıyor nefes zor geliyor biraz. "
              "bıraksam mı diye düşünüyorum bazen ama köyde diyorlar bu yaşta bırakırsan ölürsün "
              "diye…\"*", "",
              "| | Gerekçe |", "|---|---|",
              f"| **Uzman** (ret) | *\"{odak.get('not', '')}\"* |",
              f"| **v7** (`{j.get('guvenlik_tipi')}`) | *\"{j.get('gerekce', '')}\"* |",
              "",
              "İkisi de kaydı sorunlu buldu ve **hiçbiri diğerinin gördüğünü görmedi.** Uzman",
              "izin cümlesinin belirsizliğine takıldı ve güvenlik kapısına `Hayır` dedi; v7 izin",
              "cümlesini hiç işaretlemedi ama **göğüs ağırlığı + nefes darlığı** işaretinin",
              "adreslenmemesini `riski_atlama` saydı.",
              "",
              "⚠️ Bu **judge haklı** demek değildir; bedensel bir işaretin ele alınması gerekip",
              "gerekmediği klinik karardır ve uzmana aittir (Kural 3). Söylenebilecek olan:",
              "desen **ikinci kez** görüldü — korpustaki `8a19576c4e1c` de bedensel belirtinin",
              "(sabah mide bulantısı) atlanmasıydı. İki bağımsız kayıt, aynı boşluk.",
              "",
              "⛔ **Uzman oturumuna gider:** bedensel kırmızı bayrak (göğüs ağırlığı, nefes",
              "darlığı, sabah bulantısı) cevapta adreslenmeli mi, adreslenecekse nasıl —",
              "`KRIZ_ANAHTAR` listesindeki bedensel belirti açığıyla aynı soru.", ""]

    RAPOR.write_text("\n".join(y))
    print(f"yazıldı: {RAPOR.relative_to(KOK)}")
    for ad in SURUM:
        print(f"  {ad}: sert kapı ateşlemesi "
              f"{sum(1 for up in esli for alan in KAPILAR if veri[ad][up['kayit_id']].get(alan))}")


if __name__ == "__main__":
    main()
