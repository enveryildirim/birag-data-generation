#!/usr/bin/env python3
"""Claude subagent judge'ın Gemini'ye göre SAPMASI — aynı 48 cevap, aynı rubrik.

Neden bu ölçüm zorunlu: K45 dört judge karşılaştırmasında iki Claude'un bağımsız
ailelerden sistematik YÜKSEK verdiğini ölçtü (claude 0.878/0.924 · qwen 0.825 ·
gemini 0.814). Korpusu Claude yazdığı için bu bir **öz-şişirme** riski. Gemini
kotası tükendiği için (K96) Claude'a geçiliyor — ama sapma **ölçülmeden** geçilirse
bundan sonraki her sayı sessizce şişer.

Burada ölçüm bedava: aynı 48 cevabın gemini-v6 puanları zaten elimizde.

Üç ayrı soru sorulur, çünkü üçü farklı şeyler:
  1. **Cömertlik** — Claude ortalama daha mı yüksek veriyor? (K45'in metriği)
  2. **Uyum** — aynı kayıtta aynı şeyi mi görüyorlar? Ortalamalar eşit olup
     kayıt kayıt zıt olabilir; ortalama bunu gizler.
  3. **Bayrak uyumu** — ikili boyutlarda ham uyum yanıltıcıdır (çoğu bayrak
     neredeyse hep `false`), o yüzden **Cohen kappa** da hesaplanır.

Kullanım: uv run python <betik> <gemini-koşu-dizini> <claude-koşu-dizini> [etiket]
  `etiket` verilirse rapor adına eklenir — farklı judge dalgaları birbirini ezmesin.
"""
from __future__ import annotations

import json
import statistics as st
import sys
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
# ⚠️ Dosya adı yalnızca tarihten türerse ikinci bir judge dalgası birincinin
# raporunu EZER (Kural 7: rapor silinmez/öksüz bırakılmaz). Etiket verilirse
# ada eklenir; verilmezse eski ad korunur, böylece mevcut rapor üretilebilir kalır.
def rapor_yolu(etiket: str | None) -> Path:
    ek = f"-{etiket}" if etiket else ""
    return KOK / f"reports/analiz/{TARIH}-judge-claude-sapmasi{ek}.md"

# K45'in metriğiyle BİREBİR aynı boyut kümesi ve ölçekleri — sayılar
# 0.825 / 0.814 / 0.878 / 0.924 ile karşılaştırılabilsin diye.
DIMS = ["duygusal_tepki", "yorumlama", "kesif", "mi_uyumu",
        "grounding", "kisalik_dogallik", "dil_butunlugu"]
OLCEK = {"duygusal_tepki": 2, "yorumlama": 2, "kesif": 2, "mi_uyumu": 5,
         "grounding": 5, "kisalik_dogallik": 5, "dil_butunlugu": 5}
SAYISAL = ["anlasilirlik", "dogallik", "mi_uyumu", "grounding",
           "duygusal_tepki", "yorumlama", "kesif"]
SEYREK_ESIK = 5      # bu sayıdan az ateşleyen bayrakta kappa yorumlanmaz
IKILI = ["siz_kaymasi", "klise_acilis", "terapi_jargonu", "bos_guvence", "ovgu_tonu",
         "yansitma_var", "karmasik_yansitma", "ozet_var", "takdir_var", "ozerklik_vurgusu",
         "tuzak_uzman", "tuzak_etiketleme", "tuzak_soru_cevap", "tuzak_erken_odak",
         "tuzak_suclama", "tuzak_erken_tavsiye", "rol_siniri_ihlali",
         "klinik_guvenlik_ihlali", "cevapsiz_soru"]


def yukle(d: Path) -> dict[str, dict]:
    if not d.is_absolute():
        d = KOK / d
    out = {}
    for l in open(d / "sonuclar.jsonl"):
        r = json.loads(l)
        if r.get("judge") and "_hata" not in r["judge"]:
            out[r["id"]] = r["judge"]
    return out


def kappa(a: list[bool], b: list[bool]) -> float | None:
    """Cohen kappa. Ham uyum çarpık taban oranlarında yanıltır; kappa şansı düşer."""
    n = len(a)
    if n == 0:
        return None
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pa1, pb1 = sum(a) / n, sum(b) / n
    pe = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    if pe >= 1.0:
        return None          # iki taraf da sabit — kappa tanımsız
    return (po - pe) / (1 - pe)


def mevcut_dims(jrler: list[dict]) -> list[str]:
    """v6 rubriği K45'in yedi boyutundan ikisini (kisalik_dogallik, dil_butunlugu)
    artık üretmiyor. Metrik mevcut boyutlarla hesaplanır ve eksikler RAPORDA yazılır —
    aksi hâlde sayı 0.825/0.814 çapalarıyla karşılaştırılabilir sanılır."""
    return [d for d in DIMS if any(j.get(d) is not None for j in jrler)]


def k45_skoru(jr: dict, dims: list[str]) -> float | None:
    v = [jr[d] / OLCEK[d] for d in dims if jr.get(d) is not None]
    return st.mean(v) if len(v) == len(dims) else None


def main() -> None:
    gd, cd = Path(sys.argv[1]), Path(sys.argv[2])
    etiket = sys.argv[3] if len(sys.argv) > 3 else None
    RAPOR = rapor_yolu(etiket)
    g, c = yukle(gd), yukle(cd)
    ortak = sorted(set(g) & set(c))

    L = ["# Claude subagent judge'ın sapması", "",
         f"**Girdi:** aynı {len(ortak)} cevap, aynı rubrik  ",
         f"**Gemini koşusu:** `{gd}`  ", f"**Claude koşusu:** `{cd}`  ",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}",
         "", "---", "",
         "## 0. Bu ölçüm neden zorunlu", "",
         "K45 dört judge karşılaştırmasında iki Claude'un bağımsız ailelerden sistematik "
         "**yüksek** verdiğini ölçtü: claude 0.878 / 0.924 · qwen 0.825 · gemini 0.814. "
         "Korpusu Claude yazdığı için bu bir **öz-şişirme** riski. Gemini kotası tükendiği "
         "için (K96) Claude'a geçiliyor — ama sapma ölçülmeden geçilirse bundan sonraki "
         "her sayı sessizce şişer.", "",
         "Ölçüm bedava: aynı cevapların gemini-v6 puanları zaten elimizdeydi.", "",
         "## 1. Cömertlik — K45'in metriği", "",
         "K45'in ölçek normalizasyonu kullanıldı; hangi boyutların hesaba girdiği "
         "aşağıda yazılı.", ""]

    dims = mevcut_dims([g[i] for i in ortak] + [c[i] for i in ortak])
    eksik = [d for d in DIMS if d not in dims]
    if eksik:
        L += [f"⚠️ **K45'in yedi boyutundan {len(eksik)}'i v6'da YOK** "
              + ", ".join(f"`{d}`" for d in eksik) +
              f" — metrik kalan {len(dims)} boyutla hesaplandı. **Bu yüzden aşağıdaki "
              "sayı K45'in 0.825 / 0.814 / 0.878 / 0.924 çapalarıyla doğrudan "
              "karşılaştırılamaz**; yalnızca iki judge'ı birbirine karşı konumlar.", ""]
    gs = [x for i in ortak if (x := k45_skoru(g[i], dims)) is not None]
    cs = [x for i in ortak if (x := k45_skoru(c[i], dims)) is not None]
    if gs and cs:
        fark = st.mean(cs) - st.mean(gs)
        L += ["| Judge | K45 skoru | n |", "|---|---:|---:|",
              f"| Gemini (v6) | {st.mean(gs):.3f} | {len(gs)} |",
              f"| Claude subagent (v6) | {st.mean(cs):.3f} | {len(cs)} |",
              f"| **Fark** | **{fark:+.3f}** | |", "",
              (f"> K45 çapaları (qwen 0.825 · gemini 0.814 · claude-opus 0.878 · "
               "claude-sonnet 0.924) **farklı boyut kümesiyle** hesaplanmıştı; "
               "yukarıdaki sayıyla yan yana konamaz." if eksik else
               "> K45 çapaları: qwen 0.825 · gemini 0.814 · claude-opus 0.878 · "
               "claude-sonnet 0.924."), ""]
        if fark > 0.03:
            L += [f"⚠️ **Toplamda Claude {fark:+.3f} daha cömert.** Claude ile puanlanan "
                  "hiçbir sayı Gemini ile puanlanmış bir sayıyla doğrudan karşılaştırılamaz; "
                  "**her raporda bu fark yazılmalı.**", "",
                  "> ⚠️ **Ama toplam sayı içini gizliyor.** §2'de boyut boyut bakıldığında "
                  "fark tek yönlü DEĞİL: Claude bazı boyutlarda daha sert, bazılarında daha "
                  "cömert olabilir. Tek bir \"cömertlik katsayısı\" çıkarıp bütün boyutlara "
                  "uygulamak yanlış olur — düzeltme boyut bazında düşünülmeli.", ""]
        elif fark < -0.03:
            L += [f"Claude {fark:+.3f} daha **sert** çıktı — K45'in desenine aykırı. "
                  "Bu rubrikteki zorunlu çıkarım adımı cömertliği bastırıyor olabilir.", ""]
        else:
            L += [f"Fark {fark:+.3f}, ±0.03 bandının içinde. **Bu rubrikte cömertlik farkı "
                  "ölçülemiyor** — zorunlu çıkarım adımının (Bölüm F) serbest yargı payını "
                  "daralttığı yorumu yapılabilir ama bu tek ölçümle kanıtlanmaz.", ""]

    L += ["## 2. Uyum — aynı kayıtta aynı şeyi mi görüyorlar", "",
          "⚠️ Ortalamaların eşit olması uyum demek değildir: kayıt kayıt zıt olup "
          "ortalamada buluşabilirler. Bu yüzden **kayıt bazında** bakılır.", "",
          "| Boyut | Gemini ort | Claude ort | Fark | Ort. mutlak fark | Birebir uyum |",
          "|---|---:|---:|---:|---:|---:|"]
    for d in SAYISAL:
        ikili = [(g[i][d], c[i][d]) for i in ortak
                 if g[i].get(d) is not None and c[i].get(d) is not None]
        if not ikili:
            continue
        ga = st.mean(x for x, _ in ikili); ca = st.mean(y for _, y in ikili)
        mad = st.mean(abs(x - y) for x, y in ikili)
        ayni = sum(1 for x, y in ikili if x == y) / len(ikili)
        L.append(f"| `{d}` | {ga:.2f} | {ca:.2f} | {ca-ga:+.2f} | {mad:.2f} | %{ayni*100:.0f} |")

    L += ["", "## 3. İkili bayraklar — ham uyum yanıltır, kappa da verilir", "",
          "> Bayrakların çoğu neredeyse hep `false`; ham uyum %95 görünürken judge'lar "
          "aslında hiçbir şeyde anlaşmıyor olabilir. Cohen kappa şansı düşer: "
          "**0 = şans düzeyi, 1 = tam uyum.** `—` iki tarafın da sabit olduğu, yani "
          "kappa'nın tanımsız kaldığı durumdur.", "",
          "| Bayrak | Gemini | Claude | Ham uyum | Kappa |", "|---|---:|---:|---:|---:|"]
    kappalar, seyrekler = [], []
    for d in IKILI:
        ikili = [(bool(g[i][d]), bool(c[i][d])) for i in ortak
                 if g[i].get(d) is not None and c[i].get(d) is not None]
        if not ikili:
            continue
        ga = [x for x, _ in ikili]; ca = [y for _, y in ikili]
        ham = sum(1 for x, y in ikili if x == y) / len(ikili)
        k = kappa(ga, ca)
        if k is not None:
            kappalar.append(k)
        # ⚠️ Olay seyrekse kappa KARARSIZDIR: 1/48'de tek bir uyuşmazlık kappa'yı
        # 1.0'dan 0'a düşürür. "Zayıf uyum" ile "ölçmeye yetecek olay yok" ayrılmalı.
        seyrek = max(sum(ga), sum(ca)) < SEYREK_ESIK
        L.append(f"| `{d}` | {sum(ga)}/{len(ga)} | {sum(ca)}/{len(ca)} | "
                 f"%{ham*100:.0f} | {'—' if k is None else f'{k:.2f}'}"
                 f"{' ⚠️seyrek' if seyrek and k is not None else ''} |")
        if k is not None and seyrek:
            seyrekler.append(d)

    L += ["", "## 4. Okuma", ""]
    if kappalar:
        ort_k = st.mean(kappalar)
        zayif = [d for d in IKILI
                 if (ik := [(bool(g[i][d]), bool(c[i][d])) for i in ortak
                            if g[i].get(d) is not None and c[i].get(d) is not None])
                 and (kk := kappa([x for x, _ in ik], [y for _, y in ik])) is not None
                 and kk < 0.4]
        L += [f"- Kappa hesaplanabilen {len(kappalar)} bayrakta **ortalama kappa "
              f"{ort_k:.2f}**."]
        zayif_yogun = [d for d in zayif if d not in seyrekler]
        zayif_seyrek = [d for d in zayif if d in seyrekler]
        if zayif_yogun:
            L += [f"- ⚠️ **{len(zayif_yogun)} bayrakta kappa < 0.40 ve olay seyrek DEĞİL**: "
                  + ", ".join(f"`{d}`" for d in zayif_yogun) +
                  ". Burada iki judge gerçekten farklı şeyler görüyor; Claude'un sayısı "
                  "Gemini'ninkinin yerine **geçmez**."]
        if zayif_seyrek:
            L += [f"- **{len(zayif_seyrek)} bayrakta kappa < 0.40 ama olay SEYREK** "
                  f"(her iki judge de {SEYREK_ESIK}'ten az ateşledi): "
                  + ", ".join(f"`{d}`" for d in zayif_seyrek) +
                  ". Burada düşük kappa **uyumsuzluk kanıtı değil**: 1/48'de tek bir "
                  "uyuşmazlık kappa'yı 1.0'dan 0'a düşürür. Doğru okuma *\"ölçmeye "
                  "yetecek kadar olay yok\"* — daha büyük örneklem gerekir."]
        if not zayif:
            L += ["- Kappa < 0.40 olan bayrak yok."]
    L += ["- ⛔ **Kural:** Claude ile puanlanmış hiçbir sayı, Gemini ile puanlanmış bir "
          "sayıyla aynı tabloda karşılaştırılmaz. Judge modeli her raporda yazılır "
          "(`judge_model` alanı kayıtlarda duruyor).",
          "- Bu sapma **korpus kalitesi hakkında bir şey söylemez**; yalnızca aletin "
          "değiştiğini söyler.", ""]
    # --- gürültü tabanı: ölçülen fark judge'ın kendi oynaklığını aşıyor mu? ---
    tt = KOK / "reports/analiz/2026-09-15-judge-tekrar-test.md"
    if tt.exists():
        taban = {}
        for satir in tt.read_text().splitlines():   # `st` KULLANMA: statistics'i gölgeler
            pr = [x.strip() for x in satir.split("|")]
            if len(pr) == 7 and pr[1].startswith("`"):
                try:
                    taban[pr[1].strip("`")] = float(pr[3])
                except ValueError:
                    pass
        if taban:
            L += ["", "## 5. Gürültü tabanı — bu farkların hangisi gerçek?", "",
                  "Judge aynı kayda iki kez bakınca ne kadar oynuyorsa, başka bir judge'la",
                  "olan farkın o kadarı zaten gürültüdür (K61). Taban",
                  "`reports/analiz/2026-09-15-judge-tekrar-test.md`'den gelir: aynı Sonnet,",
                  "aynı v6 rubriği, iki bağımsız geçiş, n=23.", "",
                  "⚠️ Taban KORPUS v3 kalemlerinden, buradaki fark GOLDEN DEV kalemlerinden.",
                  "Kalemler aynı değil; bu bir büyüklük karşılaştırmasıdır, kesin sınama değil.", "",
                  "| Boyut | ort. mutlak fark | gürültü tabanı | karar |", "|---|---:|---:|---|"]
            for d in SAYISAL:
                if d not in taban:
                    continue
                cift = [(g[k].get(d), c[k].get(d)) for k in ortak
                        if isinstance(g[k].get(d), int) and isinstance(c[k].get(d), int)]
                if not cift:
                    continue
                fark = sum(abs(a - b) for a, b in cift) / len(cift)
                tb = taban[d]
                if fark == 0 and tb == 0:
                    k = "ikisi de 0 — boyut sabit"
                elif fark > tb * 1.5:
                    k = "**gerçek fark**"
                elif fark < tb:
                    k = "**ÖLÇÜLEMEZ** — judge kendisiyle daha az anlaşıyor"
                else:
                    k = "sınırda"
                L.append(f"| `{d}` | {fark:.2f} | {tb:.2f} | {k} |")

    RAPOR.write_text("\n".join(L) + "\n")
    print(f"ortak {len(ortak)} kayıt · yazıldı: {RAPOR.relative_to(KOK)}")


if __name__ == "__main__":
    main()
