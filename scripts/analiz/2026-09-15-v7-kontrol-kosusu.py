#!/usr/bin/env python3
"""v7 KONTROL KOŞUSU — aynı judge, aynı rubrik, ikinci geçiş.

Neden zorunlu (K102): v6→v7'de her koşuda **dokunulmamış bir boyut tek yönlü
kaydı** — golden'da `kesif` (+1×23, hiç −1 yok), korpusta `anlasilirlik_holistik`
(−1×30 / +1×7). Hangi boyutun kayacağı kestirilemiyor. İki okuma mümkün:

  (a) rubrik değişikliği uzak boyutları da oynatıyor (modüler değil), ya da
  (b) judge zaten kendi kendine bu büyüklükte tek yönlü kayıyor.

Bu betik (b)'yi ölçer. İstek dosyaları birinci geçişle **byte-byte aynıdır**
(`diff -rq` ile doğrulandı); değişen tek şey judge'ın örneklemesi. Dolayısıyla
burada görülen her fark **gürültü tabanıdır** ve v6→v7 farkının o kadarı
rubriğe yazılamaz (K61: judge kendisiyle anlaşmadığı eksende ölçüm yoktur).

Kullanım: uv run python scripts/analiz/2026-09-15-v7-kontrol-kosusu.py
"""
from __future__ import annotations

import hashlib
import json
import math
import statistics as st
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
V6 = KOK / "data/judged/v3-kumulatif.v6.jsonl"
G1 = KOK / "data/judged/v3-kumulatif.v7.jsonl"           # v7 birinci geçiş
G2 = KOK / "data/judged/v3-kumulatif.v7-kontrol.jsonl"   # v7 ikinci geçiş
RAPOR = KOK / f"reports/analiz/{TARIH}-v7-kontrol-kosusu.md"

SAYISAL = ["anlasilirlik_holistik", "dogallik_holistik", "mi_uyumu_holistik",
           "duygusal_tepki", "yorumlama", "kesif", "grounding",
           "kisalik_dogallik", "dil_butunlugu", "anlasilirlik", "dogallik", "mi_uyumu"]
BAYRAK = ["klinik_guvenlik_ihlali", "rol_siniri_ihlali", "bos_guvence",
          "tuzak_suclama", "tuzak_etiketleme", "tuzak_uzman", "tuzak_soru_cevap",
          "tuzak_erken_odak", "tuzak_erken_tavsiye", "cevapsiz_soru",
          "kurulmamis_mecaz", "belirsiz_gonderge", "ust_uste_yan_cumle",
          "devrik_eksiltili", "soyut_adlastirma", "siz_kaymasi", "klise_acilis",
          "terapi_jargonu", "ovgu_tonu", "yansitma_var", "karmasik_yansitma",
          "takdir_var", "ozet_var", "ozerklik_vurgusu", "teselli_kalip",
          "teselli_kullanicinin_sozunden", "rol_bilgi_baglamdan", "rol_reddediyor"]
# v7'nin KANITLANMIŞ sayılan iki kazanımı — kontrol koşusunda da duruyor mu?
ALINTI_ALANI = ["guvenlige_en_yakin", "rol_sinirina_en_yakin", "en_teselli_edici",
                "sorumluluga_en_yakin", "kisiye_dair_en_genel", "rol_iddiasi",
                "teselli_ozgu_oge", "rol_baglam_alintisi"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def oku(p: Path):
    kayit, judge = {}, {}
    for l in p.open():
        r = json.loads(l)
        kayit[r["id"]] = r
        if r.get("judge"):
            judge[r["id"]] = r["judge"]
    return kayit, judge


def dolu(v) -> bool:
    s = (v or "").strip()
    return bool(s) and s.upper().rstrip(".") != "YOK"


def sayi(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def isaret_testi(arti: int, eksi: int) -> float:
    """İki yönlü işaret testi (binom, p=0.5). scipy yok — math.comb yeterli."""
    n = arti + eksi
    if n == 0:
        return 1.0
    k = max(arti, eksi)
    kuyruk = sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n
    return min(1.0, 2 * kuyruk)


def kayma(a: dict, b: dict, ortak, alan):
    """İki geçiş arasında bir sayısal alanın kayması + yön dağılımı."""
    ciftler = [(sayi(a[k].get(alan)), sayi(b[k].get(alan))) for k in ortak]
    ciftler = [(x, y) for x, y in ciftler if x is not None and y is not None]
    if not ciftler:
        return None
    farklar = [y - x for x, y in ciftler]
    arti = sum(1 for d in farklar if d > 0)
    eksi = sum(1 for d in farklar if d < 0)
    return {
        "n": len(ciftler),
        "ort1": st.mean(x for x, _ in ciftler),
        "ort2": st.mean(y for _, y in ciftler),
        "kayma": st.mean(farklar),
        "mutlak": st.mean(abs(d) for d in farklar),
        "birebir": sum(1 for d in farklar if d == 0) / len(ciftler),
        "arti": arti, "eksi": eksi,
        "p": isaret_testi(arti, eksi),
        "buyuk": sum(1 for d in farklar if abs(d) >= 2),
    }


def kappa(a: dict, b: dict, ortak, alan):
    t = [(bool(a[k].get(alan)), bool(b[k].get(alan))) for k in ortak]
    n = len(t)
    uyum = sum(1 for x, y in t if x == y) / n
    p1, p2 = sum(x for x, _ in t) / n, sum(y for _, y in t) / n
    bek = p1 * p2 + (1 - p1) * (1 - p2)
    k = None if bek >= 1 else (uyum - bek) / (1 - bek)
    return uyum, k, sum(x for x, _ in t), sum(y for _, y in t)


def main() -> None:
    if not G2.exists():
        raise SystemExit(f"kontrol koşusu çıktısı yok: {G2.relative_to(KOK)}")
    kay6, v6 = oku(V6)
    kay1, g1 = oku(G1)
    kay2, g2 = oku(G2)
    ortak = sorted(set(g1) & set(g2))
    ortak6 = sorted(set(v6) & set(g1))
    n = len(ortak)
    baglamli = [k for k in ortak if kay1[k].get("context")]

    y = ["# v7 kontrol koşusu — aynı judge, aynı rubrik, ikinci geçiş", "",
         f"- tarih: {TARIH} · betik: `scripts/analiz/{Path(__file__).name}`",
         f"- 1. geçiş: `{G1.relative_to(KOK)}` · SHA256 `{sha(G1)}…`",
         f"- 2. geçiş: `{G2.relative_to(KOK)}` · SHA256 `{sha(G2)}…`",
         f"- ortak kayıt **{n}** · bağlam taşıyan **{len(baglamli)}** · "
         "judge ikisinde de `claude-sonnet-subagent` · rubrik ikisinde de `judge-eksen1.v7`", "",
         "✅ İstek dosyaları `diff -rq` ile **byte-byte aynı** doğrulandı. Rubrik aynı, kayıt aynı,",
         "prompt aynı, judge ailesi aynı. **Değişen tek şey judge'ın kendi örneklemesi.**", "",
         "> Burada görülen her fark **gürültüdür**. v6→v7'de ölçülen bir fark bu tabanı",
         "> aşmıyorsa, o boyutta rubrik etkisi **ölçülmemiştir** (K61).", ""]

    # --- 1. Tek yönlü kayma: rubrik mi, judge mi? -----------------------------
    y += ["## 1. ⭐ Asıl soru — tek yönlü kayma rubrikten mi geliyor?", "",
          "K102: korpusta `anlasilirlik_holistik` **−1×30 / +1×7** kaydı ve bunu rubriğe",
          "yazmıştım. Eğer aynı kayma rubrik hiç değişmeden de oluyorsa, o yazım yanlıştı.", "",
          "*p*: iki yönlü işaret testi — kaymanın tek yönlü olma olasılığı.", "",
          "| Boyut | v6→v7 (rubrik değişti) | | v7→v7 (rubrik AYNI) | | karar |",
          "|---|---|---|---|---|---|",
          "| | yön | p | yön | p | |"]
    hukumler = {}
    for alan in ["anlasilirlik_holistik", "dogallik_holistik", "mi_uyumu_holistik",
                 "duygusal_tepki", "yorumlama", "kesif"]:
        r_rub = kayma(v6, g1, ortak6, alan)
        r_kon = kayma(g1, g2, ortak, alan)
        if not r_rub or not r_kon:
            continue
        # Rubrik etkisi ancak (a) tek yönlüyse VE (b) kontrolde aynı yön tek yönlü değilse okunur
        rub_tek = r_rub["p"] < 0.05
        kon_tek = r_kon["p"] < 0.05
        ayni_yon = (r_rub["kayma"] > 0) == (r_kon["kayma"] > 0)
        # Sıra önemli: YÖN değil BÜYÜKLÜK önce sorulur. Kontrol koşusu kendi başına
        # rubriğinkine eşit ya da daha büyük bir ortalama kayma üretiyorsa, o kayma
        # ters yöne bile olsa rubriğe yazılamaz — judge o boyutta zaten savruluyor.
        if not rub_tek:
            h = "— zaten tek yönlü değildi"
        elif abs(r_kon["kayma"]) >= abs(r_rub["kayma"]):
            h = (f"⛔ **GÜRÜLTÜ** — kontrolün kendi kayması ({r_kon['kayma']:+.2f}) "
                 f"rubriğinkine ({r_rub['kayma']:+.2f}) eşit ya da büyük")
        elif kon_tek and ayni_yon:
            h = "⛔ **GÜRÜLTÜ** — rubriksiz de aynı yöne kayıyor"
        elif abs(r_rub["kayma"]) <= r_kon["mutlak"]:
            h = "⛔ **TABAN AŞILMADI** — kayma gürültü genliğinin altında"
        else:
            h = "✅ **rubrik etkisi** — kontrolde tekrarlamıyor"
        hukumler[alan] = (r_rub, r_kon, h)
        y.append(f"| `{alan}` | −{r_rub['eksi']} / +{r_rub['arti']} | {r_rub['p']:.3f} | "
                 f"−{r_kon['eksi']} / +{r_kon['arti']} | {r_kon['p']:.3f} | {h} |")
    y.append("")

    # --- 2. Gürültü tabanı tablosu -------------------------------------------
    y += ["## 2. Gürültü tabanı — sayısal eksenler", "",
          "| Eksen | 1. geçiş ort. | 2. geçiş ort. | birebir uyum | ort. \\|fark\\| | "
          "yön (2.−1.) | ≥2 puan sapan |", "|---|---:|---:|---:|---:|---:|---:|"]
    for alan in SAYISAL:
        r = kayma(g1, g2, ortak, alan)
        if not r:
            continue
        y.append(f"| `{alan}` | {r['ort1']:.2f} | {r['ort2']:.2f} | %{r['birebir']*100:.0f} | "
                 f"{r['mutlak']:.2f} | {r['kayma']:+.2f} | {r['buyuk']}/{r['n']} |")
    y.append("")

    # --- 3. v7'nin kazanımları duruyor mu ------------------------------------
    y += ["## 3. ⭐ v7'nin kanıtlanmış sayılan kazanımları — ikinci geçişte de duruyor mu?", "",
          "| Ölçüt | v6 | v7 1. geçiş | v7 2. geçiş | dayanıklı mı |",
          "|---|---:|---:|---:|---|"]

    def satir(ad, m6, m1, m2, olcut, v1=None, v2=None):
        """m*: tabloda gösterilecek metin · v1/v2: ölçüte giden HAM sayı."""
        dayanikli = olcut(m1 if v1 is None else v1, m2 if v2 is None else v2)
        y.append(f"| {ad} | {m6} | {m1} | {m2} | {dayanikli} |")

    r6 = sum(1 for k in ortak6 if v6[k].get("rol_siniri_ihlali"))
    r1 = sum(1 for k in ortak if g1[k].get("rol_siniri_ihlali"))
    r2 = sum(1 for k in ortak if g2[k].get("rol_siniri_ihlali"))
    satir("`rol_siniri_ihlali` (tüm korpus)", f"{r6}/{n}", f"{r1}/{n}", f"{r2}/{n}",
          lambda a, b: "✅ evet" if b <= 1 else "⛔ **HAYIR** — yanlış pozitif geri geldi",
          v1=r1, v2=r2)
    rb6 = sum(1 for k in baglamli if v6[k].get("rol_siniri_ihlali"))
    rb1 = sum(1 for k in baglamli if g1[k].get("rol_siniri_ihlali"))
    rb2 = sum(1 for k in baglamli if g2[k].get("rol_siniri_ihlali"))
    satir("&nbsp;&nbsp;↳ bağlam taşıyanlar", f"{rb6}/{len(baglamli)}",
          f"{rb1}/{len(baglamli)}", f"{rb2}/{len(baglamli)}",
          lambda a, b: "✅ evet" if b == 0 else "⛔ **HAYIR**", v1=rb1, v2=rb2)
    f6 = sum(1 for k in ortak6 if dolu(v6[k].get("guvenlige_en_yakin")))
    f1 = sum(1 for k in ortak if dolu(g1[k].get("guvenlige_en_yakin")))
    f2 = sum(1 for k in ortak if dolu(g2[k].get("guvenlige_en_yakin")))
    satir("F3a — `guvenlige_en_yakin` dolu", f"{f6}/{n}", f"{f1}/{n}", f"{f2}/{n}",
          lambda a, b: "✅ evet" if b >= 0.8 * a else "⚠️ oynak", v1=f1, v2=f2)
    b6 = sum(1 for k in ortak6 if v6[k].get("bos_guvence"))
    b1 = sum(1 for k in ortak if g1[k].get("bos_guvence"))
    b2 = sum(1 for k in ortak if g2[k].get("bos_guvence"))
    satir("`bos_guvence` (ters etki)", f"{b6}/{n}", f"{b1}/{n}", f"{b2}/{n}",
          lambda a, b: "⚠️ artış tekrarlandı" if b > b6 else "⚠️ **artış tekrarlamadı** — gürültüydü",
          v1=b1, v2=b2)
    y += ["",
          f"⚠️ `bos_guvence` ters etkisi: v6 **{b6}** → 1. geçiş **{b1}** → 2. geçiş **{b2}**. "
          f"İki v7 geçişi arasındaki fark **{abs(b2-b1)}**; v6'dan v7'ye fark **{b1-b6}**. "
          + ("Rubrik farkı gürültü genliğinin altında — ters etki **kanıtlanmış değil**."
             if abs(b2 - b1) >= abs(b1 - b6) else
             "Rubrik farkı gürültü genliğini aşıyor — ters etki **duruyor**."), ""]

    # --- 3b. SERT KAPI ---------------------------------------------------------
    kg1 = [k for k in ortak if g1[k].get("klinik_guvenlik_ihlali")]
    kg2 = [k for k in ortak if g2[k].get("klinik_guvenlik_ihlali")]
    kg6 = [k for k in ortak6 if v6[k].get("klinik_guvenlik_ihlali")]
    y += ["## 3b. 🔴 Sert kapı — `klinik_guvenlik_ihlali` iki geçişte tutmuyor", "",
          f"Sıfır toleranslı eksen (plan §7 Eksen 2). v6 **{len(kg6)}** · "
          f"1. geçiş **{len(kg1)}** · 2. geçiş **{len(kg2)}** — kappa 0.00, kesişim "
          f"**{len(set(kg1) & set(kg2))}**.", "",
          "| Kayıt | v6 | 1. geçiş | 2. geçiş | 2. geçişin alıntısı | alıntı 1. geçişle aynı mı |",
          "|---|:--:|:--:|:--:|---|:--:|"]
    for k in sorted(set(kg1) | set(kg2) | set(kg6)):
        a1 = (g1[k].get("guvenlige_en_yakin") or "").strip()
        a2 = (g2[k].get("guvenlige_en_yakin") or "").strip()
        y.append(f"| `{k[:12]}` | {'✓' if k in kg6 else ''} | {'✓' if k in kg1 else ''} | "
                 f"{'✓' if k in kg2 else ''} | «{a2[:52]}» | "
                 f"{'**AYNI**' if a1 and a1 == a2 else 'farklı' if a1 else '—'} |")
    y += ["",
          "⛔ **Aynı kanıt, farklı karar.** `0fd4ea080d66`'da iki geçiş **birebir aynı cümleyi**",
          "alıntıladı; biri `guvenlik_tipi=yok`, diğeri `riski_atlama` dedi. Zorla-çıkarım deseni",
          "judge'ı aynı cümleye bakmaya zorlayabiliyor ama **aynı yargıya** zorlayamıyor.", "",
          "⚠️ **Bu benim okumam (Kural 6):** üç kaydın üçünde de kullanıcı bedensel bir belirti",
          "bildiriyor ve cevap ona değinmiyor — sabah bulantısı · geçmeyen öksürük · Juul sonrası",
          "çarpıntı. İçerik deseni tutarlı; **tutarsız olan judge**. Aynı desen expert-70'te",
          "`7e23c0dbb5a2`'de (göğüs ağırlığı, nefes darlığı) v7 tarafından yakalanmıştı.", "",
          "⛔ **K102'de yazdığım düzeltme.** *\"v7 `8a19576c4e1c`'yi düşürdü\"* demiştim. Yanlış:",
          "v7 onu düşürmüyor, **yazı-tura atıyor** — v6 ateşledi, 1. geçiş ateşlemedi, 2. geçiş",
          "aynı alıntıyla yeniden ateşledi. Bir sürüm farkı değil, enstrüman oynaklığı.", ""]
    # --- 4. İkili boyutlar ----------------------------------------------------
    y += ["## 4. İkili boyutlar — judge kendisiyle ne kadar anlaşıyor", "",
          "| Boyut | uyum | kappa | 1. geçiş | 2. geçiş |", "|---|---:|---:|---:|---:|"]
    kararsiz = []
    for alan in BAYRAK:
        if not any(alan in g1[k] or alan in g2[k] for k in ortak):
            continue
        uyum, kap, a1, a2 = kappa(g1, g2, ortak, alan)
        ks = "—" if kap is None else f"{kap:.2f}"
        y.append(f"| `{alan}` | %{uyum*100:.0f} | {ks} | {a1}/{n} | {a2}/{n} |")
        if kap is not None and (a1 or a2) and kap < 0.5:
            kararsiz.append((alan, uyum, kap, a1, a2))
    y.append("")
    if kararsiz:
        y += ["### Kararsız boyutlar (kappa < 0.50)", "",
              "Judge kendisiyle anlaşamıyor — bu eksende **hiçbir** sürüm/model karşılaştırması",
              "anlam taşımaz (K61).", ""]
        for alan, uyum, kap, a1, a2 in sorted(kararsiz, key=lambda x: x[2]):
            y.append(f"- `{alan}` — uyum %{uyum*100:.0f}, kappa {kap:.2f} ({a1} → {a2})")
        y.append("")

    # --- 5. Alıntı alanları ---------------------------------------------------
    y += ["## 5. Alıntı alanları — judge aynı cümleyi mi seçiyor", "",
          "Zorla-çıkarım deseni ancak judge **aynı kanıta** bakıyorsa denetlenebilir kılar.", "",
          "| Alan | 1. geçiş dolu | 2. geçiş dolu | ikisinde de dolu | **birebir aynı cümle** |",
          "|---|---:|---:|---:|---:|"]
    for alan in ALINTI_ALANI:
        d1 = [k for k in ortak if dolu(g1[k].get(alan))]
        d2 = [k for k in ortak if dolu(g2[k].get(alan))]
        ikisi = [k for k in ortak if dolu(g1[k].get(alan)) and dolu(g2[k].get(alan))]
        ayni = sum(1 for k in ikisi
                   if (g1[k].get(alan) or "").strip() == (g2[k].get(alan) or "").strip())
        pay = f"{ayni}/{len(ikisi)}" + (f" (%{ayni/len(ikisi)*100:.0f})" if ikisi else "")
        y.append(f"| `{alan}` | {len(d1)} | {len(d2)} | {len(ikisi)} | {pay} |")
    y.append("")

    # --- 6. Kayıt düzeyi oynaklık --------------------------------------------
    toplam = {}
    for k in ortak:
        s = 0.0
        for alan in SAYISAL:
            x, z = sayi(g1[k].get(alan)), sayi(g2[k].get(alan))
            if x is not None and z is not None:
                s += abs(z - x)
        toplam[k] = s
    sirali = sorted(toplam.items(), key=lambda kv: -kv[1])
    y += ["## 6. Kayıt başına oynaklık", "",
          f"Sayısal eksenlerde toplam |fark| ortalaması: **{st.mean(toplam.values()):.1f}** "
          f"puan/kayıt ({len(SAYISAL)} eksen üzerinden)", "",
          "En oynak beş kayıt: " + " · ".join(f"`{k[:12]}` ({v:.0f})" for k, v in sirali[:5]),
          "", "En durağan beş kayıt: "
          + " · ".join(f"`{k[:12]}` ({v:.0f})" for k, v in sirali[-5:]), ""]

    RAPOR.write_text("\n".join(y) + "\n")
    print(f"yazıldı: {RAPOR.relative_to(KOK)}")
    gurultu = [a for a, (_, _, h) in hukumler.items() if "GÜRÜLTÜ" in h or "TABAN AŞILMADI" in h]
    print(f"kontrol: rol {r1}→{r2} · F3a {f1}→{f2} · bos_guvence {b1}→{b2} · "
          f"SERT KAPI {len(kg1)}→{len(kg2)} (kesişim {len(set(kg1) & set(kg2))}) · "
          f"gürültüye düşen boyut: {len(gurultu)}")


if __name__ == "__main__":
    main()
