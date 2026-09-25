#!/usr/bin/env python3
"""v7 ne yaptı — amaçlanan etki ile amaçlanmayan etkiyi AYRI ölçer.

`2026-09-15-judge-rubrik-korluk.py` "boyut varyans üretiyor mu" diye sorar; bu betik
farklı bir soru sorar: **v7'nin beş değişikliği hedeflediği şeyi mi yaptı?**

Karşılaştırma temiz kurulmuştur: aynı 48 baseline cevabı · aynı judge (Sonnet) ·
değişen tek şey rubrik. Ama "temiz" olması **nedensellik kanıtı vermez** — aynı judge
aynı girdiye iki kez farklı cevap verebilir (K98). Bu yüzden betik, v7'nin
DOKUNMADIĞI bölümleri de ölçer: orada da kayma varsa, hedef boyutlardaki kayma
değişikliğe atfedilemez.

Kullanım: uv run python scripts/analiz/2026-09-15-judge-v7-etki.py
"""
from __future__ import annotations

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
V6 = KOK / "reports/analiz/golden-kosu/20260915-080807-golden-baseline-sonnet"
V7 = KOK / "reports/analiz/golden-kosu/20260915-083830-golden-v7-sonnet"
RAPOR = KOK / f"reports/analiz/{TARIH}-judge-v7-etki.md"

ALINTI = ["en_somut_ayrinti", "rol_sinirina_en_yakin", "guvenlige_en_yakin",
          "kisiye_dair_en_genel", "sorumluluga_en_yakin", "en_teselli_edici"]
YENI = ["rol_iddiasi", "rol_baglam_alintisi", "teselli_ozgu_oge"]
# v7'nin TEK harfine dokunmadığı bölümler — kontrol grubu
DOKUNULMAYAN = ["anlasilirlik_holistik", "dogallik_holistik", "mi_uyumu_holistik",
                "duygusal_tepki", "yorumlama", "kesif"]


def yukle(d: Path) -> dict[str, dict]:
    return {json.loads(l)["id"]: (json.loads(l).get("judge") or {})
            for l in (d / "sonuclar.jsonl").open()}


def cevaplar(d: Path) -> dict[str, str]:
    return {json.loads(l)["id"]: json.loads(l).get("cevap", "") for l in (d / "sonuclar.jsonl").open()}


def dolu(v) -> bool:
    s = (v or "").strip()
    return bool(s) and s.upper() not in ("YOK", "YOK.")


def sha(d: Path) -> str:
    return hashlib.sha256((d / "sonuclar.jsonl").read_bytes()).hexdigest()[:16]


def bolum_ayni(bas: str, son: str) -> bool:
    def al(yol: str) -> str:
        t = (KOK / "prompts" / yol).read_text()
        i = t.index(bas)
        return t[i:t.index(son, i)]
    return al("judge-eksen1.v6.md") == al("judge-eksen1.v7.md")


def main() -> None:
    a, b = yukle(V6), yukle(V7)
    ortak = sorted(set(a) & set(b))
    n = len(ortak)
    y = ["# judge v7 — amaçlanan etki ve amaçlanmayan etki", "",
         f"- tarih: {TARIH} · betik: `scripts/analiz/{Path(__file__).name}`",
         f"- v6 koşusu: `{V6.relative_to(KOK)}` · SHA256 `{sha(V6)}…`",
         f"- v7 koşusu: `{V7.relative_to(KOK)}` · SHA256 `{sha(V7)}…`",
         f"- aynı {n} baseline cevabı · aynı judge (`claude-sonnet-subagent`) · değişen tek şey rubrik",
         "",
         "⚠️ **Puanlar karşılaştırılmıyor, davranış karşılaştırılıyor.** v6 ve v7 aynı cevaba",
         "farklı sayı verir; anlamlı olan judge'ın neye baktığı ve ne çıkardığı.", ""]

    # --- 1. F3a ---------------------------------------------------------------
    y += ["## 1. ✅ F3a'nın koşulu kalktı — hedeflenen etki net", "",
          "v6'da altı alıntı talimatından yalnızca F3a koşulluydu (*\"şu üçünden birini yapan",
          "cümleyi\"*); diğerleri *\"en yakınını yaz\"* diyordu. Sonuç, güvenlik ekseninin",
          "ikinci adımının neredeyse hiç sorulmamasıydı.", "",
          "| Alıntı alanı | v6 dolu | v7 dolu |", "|---|---:|---:|"]
    for alan in ALINTI:
        d6 = sum(dolu(a[k].get(alan)) for k in ortak)
        d7 = sum(dolu(b[k].get(alan)) for k in ortak)
        isaret = " ⭐" if alan == "guvenlige_en_yakin" else ""
        y.append(f"| `{alan}`{isaret} | {d6}/{n} | {d7}/{n} |")
    g6 = sum(dolu(a[k].get("guvenlige_en_yakin")) for k in ortak)
    g7 = sum(dolu(b[k].get("guvenlige_en_yakin")) for k in ortak)
    y += ["",
          f"`guvenlige_en_yakin` **{g6}/{n} → {g7}/{n}**. Yani `guvenlik_tipi` sorusu v6'da",
          f"{n-g6} kayıtta hiç sorulmuyordu, v7'de {n-g7} kayıtta sorulmuyor. Diğer beş alanın",
          "hiçbiri bu büyüklükte oynamadı — tek koşullu talimat tek büyük değişimi verdi.",
          "",
          "⚠️ Alıntı yazmak ihlal işaretlemek değildir; `guvenlik_tipi` 23 kaydın",
          f"{sum(1 for k in ortak if (b[k].get('guvenlik_tipi') or 'yok') != 'yok')}'ünde `yok` dışında bir değer aldı.",
          ""]

    # --- 2. rol_siniri_ihlali -------------------------------------------------
    y += ["## 2. `rol_siniri_ihlali` 2 → 0 — ikisi de alıntıya göre yanlış pozitifti", ""]
    y += ["| Öğe | v6 alıntısı | v6 `rol_alani` | v7 `rol_alani` |", "|---|---|---|---|"]
    for k in ortak:
        if a[k].get("rol_siniri_ihlali") and not b[k].get("rol_siniri_ihlali"):
            y.append(f"| `{k}` | «{(a[k].get('rol_sinirina_en_yakin') or '')[:70]}» | "
                     f"`{a[k].get('rol_alani')}` | `{b[k].get('rol_alani')}` |")
    y += ["",
          "İkisinde de v7 **kendisi** `yok` dedi; kod kapısının devreye girmesine gerek kalmadı.",
          "Biri riski **adlandırıyor** (uyarıdır, tavsiye değil), diğeri **izin sorusu** —",
          "system prompt'un emrettiği davranış.",
          "",
          "⚠️ **Bu tam bir örneklem dışı doğrulama değil.** v7'nin F2b'sine, korpusta görülen",
          "üç aşırı-atama örneği (özerklik cümlesi · izin sorusu · kullanıcının sözünün",
          "yansıtması) **açıkça yazıldı**. Kayıtlar yeni, ama **desen sınıfı örneklem içi**.",
          "Rubriğe kural yazmak meşrudur; burada kanıtlanan şey kuralın işlediği, keşfedildiği değil.",
          ""]

    # --- 3. yeni alanlar ------------------------------------------------------
    y += ["## 3. Yeni kanıt alanları dolduruluyor mu", "",
          "Tez: *soyut soru judge'ı bakmaya zorlamıyor, alıntı zorlar.* Alanlar hep `YOK`",
          "dönseydi tez çürümüş olurdu.", "",
          "| Alan | dolu | `YOK` | boş/eksik |", "|---|---:|---:|---:|"]
    for alan in YENI:
        d = sum(dolu(b[k].get(alan)) for k in ortak)
        yok = sum(1 for k in ortak if (b[k].get(alan) or "").strip().upper() in ("YOK", "YOK."))
        bos = sum(1 for k in ortak if alan not in b[k] or not (b[k].get(alan) or "").strip())
        y.append(f"| `{alan}` | {d} | {yok} | {bos} |")
    baglamdan = sum(1 for k in ortak if b[k].get("rol_bilgi_baglamdan"))
    y += ["",
          f"⛔ **RAG kaçışı bu koşuda SINANMADI.** `rol_bilgi_baglamdan` {baglamdan} kez `true` oldu",
          "çünkü `golden.dev`'de **bağlam taşıyan öğe yok** (K93 kapsam açığı). v7'nin en güçlü",
          "kanıta dayanan değişikliği (Fisher p=0.0001) burada hiç tetiklenemedi — sınavı",
          "korpus ya da bağlamlı öğe eklenmiş bir cetvel verecek.", ""]

    # --- 4. kod kapıları ------------------------------------------------------
    kapi1 = [k for k in ortak
             if (b[k].get("rol_alani") or "yok") != "yok"
             and dolu(b[k].get("rol_sinirina_en_yakin")) and not b[k].get("rol_reddediyor")
             and not dolu(b[k].get("rol_iddiasi"))]
    kapi2 = [k for k in ortak if b[k].get("teselli_kalip") and dolu(b[k].get("teselli_ozgu_oge"))]
    y += ["## 4. Kod kapıları ateşledi mi — hayır, gerek kalmadı", "",
          f"- `rol_alani` atanmış ama `rol_iddiasi` yazılamamış: **{len(kapi1)}**",
          f"- `teselli_kalip=true` ama özgü öge yazılmış: **{len(kapi2)}**", "",
          "Judge kendi içinde tutarlı davrandı; kodun hiçbir iddiayı ezmesi gerekmedi.",
          "**İşi rubriğin metni yaptı, kapı değil.** Kapılar bu koşuda filtre olarak",
          "sınanmadı — sınanmaları için judge'ın kanıtsız iddia ettiği bir malzeme gerekiyor",
          "(v6'nın iki kez kaydığı korpus gibi).", ""]

    # --- 5. bos_guvence -------------------------------------------------------
    acilan = [k for k in ortak if b[k].get("bos_guvence") and not a[k].get("bos_guvence")]
    sonen = [k for k in ortak if a[k].get("bos_guvence") and not b[k].get("bos_guvence")]
    ayni_cumle = [k for k in acilan
                  if (a[k].get("en_teselli_edici") or "") == (b[k].get("en_teselli_edici") or "")]
    sozunden_donen = [k for k in ayni_cumle
                      if a[k].get("teselli_kullanicinin_sozunden")
                      and not b[k].get("teselli_kullanicinin_sozunden")]
    t6 = sum(1 for k in ortak if a[k].get("bos_guvence"))
    t7 = sum(1 for k in ortak if b[k].get("bos_guvence"))
    y += ["## 5. ⚠️ AMAÇLANMAYAN — `bos_guvence` düşmedi, ARTTI", "",
          f"**{t6}/{n} → {t7}/{n}** · açılan {len(acilan)} · sönen {len(sonen)}.", "",
          "F6b'ye `teselli_ozgu_oge` eklenmesinin amacı, konuşmaya özgü cümlelere yanlışlıkla",
          "*kalıp* denmesini **azaltmaktı**. Olan bu değil:", "",
          f"Açılan {len(acilan)} kaydın **{len(ayni_cumle)}'sinde judge aynı cümleyi seçti** ve `teselli_kalip`",
          f"yine `true` kaldı; değişen şey **komşu soru**: `teselli_kullanicinin_sozunden`",
          f"**{len(sozunden_donen)} kayıtta `true` → `false` döndü.**", "",
          "| Öğe | Cümle | v6 `sozunden` | v7 `sozunden` | v7 `ozgu_oge` |", "|---|---|:--:|:--:|---|"]
    for k in sozunden_donen:
        y.append(f"| `{k}` | «{(b[k].get('en_teselli_edici') or '')[:52]}» | `True` | `False` | "
                 f"`{(b[k].get('teselli_ozgu_oge') or '')[:18]}` |")
    y += ["",
          "Yani *\"özgü öge yaz, çıplak gönderge sayılmaz\"* talimatı **yalnızca kendi sorusunu",
          "değil bloğun tamamını sertleştirdi** ve boş güvence eşiğini düşürdü. Yönü tasarımın",
          "tersi.",
          "",
          "⚠️ Bu **kusur olduğunu kanıtlamaz** — judge v7'de haklı, v6'da gevşek de olabilir.",
          "Cümlenin kullanıcının sözünden gelip gelmediği ancak konuşma okunarak bilinir",
          f"ve bu {len(sozunden_donen)} kayıt elle okunmayı hak ediyor. Kanıtlanan tek şey: **etki tasarlanan",
          "yerde değil, komşusunda çıktı.**", ""]

    # --- 6. dokunulmayan boyutlar --------------------------------------------
    y += ["## 6. ⛔ AMAÇLANMAYAN — dokunulmamış bölüm sistematik kaydı", "",
          f"- Bölüm B (anlaşılırlık kanıtı): v6 ↔ v7 **{'birebir aynı' if bolum_ayni('## Bölüm B', '## Bölüm C') else 'FARKLI'}**",
          f"- Bölüm E (EPITOME + `cevapsiz_soru`): v6 ↔ v7 **{'birebir aynı' if bolum_ayni('## Bölüm E', '## Bölüm F') else 'FARKLI'}**",
          "",
          "Tek harfi değişmemiş bölümlerde bile puanlar oynadı:", "",
          "| Boyut | v6 ort | v7 ort | ort kayma | ort mutlak | birebir uyum | dağılım |",
          "|---|---:|---:|---:|---:|---:|---|"]
    for alan in DOKUNULMAYAN:
        cift = [(a[k].get(alan), b[k].get(alan)) for k in ortak
                if isinstance(a[k].get(alan), (int, float)) and isinstance(b[k].get(alan), (int, float))]
        fark = [q - p for p, q in cift]
        dag = " · ".join(f"{d:+d}×{fark.count(d)}" for d in sorted(set(fark)) if d) or "—"
        y.append(f"| `{alan}` | {st.mean(p for p, _ in cift):.2f} | {st.mean(q for _, q in cift):.2f} | "
                 f"{st.mean(fark):+.2f} | {st.mean(abs(d) for d in fark):.2f} | "
                 f"%{100*sum(1 for d in fark if d == 0)/len(fark):.0f} | {dag} |")
    kf = [b[k]["kesif"] - a[k]["kesif"] for k in ortak]
    y += ["",
          f"`kesif` **tek yönlü**: {sum(1 for d in kf if d > 0)} kayıtta arttı, "
          f"{sum(1 for d in kf if d < 0)} kayıtta azaldı. Rastgele gürültü olsaydı iki yön",
          f"dengelenirdi — `duygusal_tepki` öyle davranıyor "
          f"({' · '.join(f'{d:+d}×{[b[k]['duygusal_tepki']-a[k]['duygusal_tepki'] for k in ortak].count(d)}' for d in (-1, 1))}).",
          "",
          "**Okuma: rubrik modüler değil.** F3/F6'ya dokunmak, bir harfi değişmemiş Bölüm E'deki",
          "bir boyutu yarım puan yukarı taşıdı. K98 ile aynı aile: alet, beklemediğimiz yerde",
          "oynuyor.",
          "",
          "⛔ **Sonuç — bu koşu bir kontrol grubu içermiyor.** Aynı judge'ın v7'yi iki kez",
          "koşturduğu bir tekrar-test olmadan, §1-§5'teki farkların ne kadarının rubrikten",
          "ne kadarının judge oynaklığından geldiği ayrılamaz. §1'deki F3a etkisi (2 → 23)",
          f"büyüklüğü sayesinde bu itirazın üstünde; §5'teki {len(sozunden_donen)} kayıt ise değil.", ""]

    RAPOR.write_text("\n".join(y))
    print(f"yazıldı: {RAPOR.relative_to(KOK)}")
    print(f"F3a: {g6}→{g7} · rol_siniri: {sum(1 for k in ortak if a[k].get('rol_siniri_ihlali'))}→"
          f"{sum(1 for k in ortak if b[k].get('rol_siniri_ihlali'))} · bos_guvence: {t6}→{t7} · "
          f"kapı1 {len(kapi1)} kapı2 {len(kapi2)}")


if __name__ == "__main__":
    main()
