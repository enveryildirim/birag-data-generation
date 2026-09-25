#!/usr/bin/env python3
"""Judge rubrik karşılaştırması: kör boyutlar açıldı mı? AYNI cevaplar, iki rubrik.

Bu temiz bir A/B: cevaplar sabit (aynı baseline üretimi), değişen tek şey rubrik.
Tek soru şu — v4'ün 48 cevapta hiç varyans üretmediği altı boyutta v5 varyans
üretiyor mu? Üretmiyorsa müdahale işe yaramamıştır ve öyle yazılır.

⚠️ v4 ve v5 puanları KARŞILAŞTIRILABİLİR DEĞİL: aynı cevaba farklı sayı verirler.
Karşılaştırılan şey puanlar değil, **aletin ayırt etme kapasitesi**.

Kullanım: uv run python <betik> <v4-koşu-dizini> <v5-koşu-dizini>
"""
from __future__ import annotations

import collections
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
# Etiketler koşu meta'sındaki `judge_rubrik` alanından gelir; rapor adı da ondan.

# golden koşu raporunun kör bulduğu altı boyut
HEDEF = ["grounding", "rol_siniri_ihlali", "tuzak_suclama", "tuzak_etiketleme",
         "bos_guvence", "klinik_guvenlik_ihlali"]
# müdahalenin dokunmaması gereken boyutlar — yan etki kontrolü
KONTROL = ["anlasilirlik", "dogallik", "mi_uyumu", "duygusal_tepki", "yorumlama",
           "kesif", "siz_kaymasi", "klise_acilis", "yansitma_var", "tuzak_uzman"]


def yukle(d: Path) -> tuple[dict[str, dict], str]:
    if not d.is_absolute():
        d = KOK / d
    satirlar = {json.loads(l)["id"]: json.loads(l) for l in open(d / "sonuclar.jsonl")}
    meta = json.loads((d / "kosu.json").read_text())
    # `judge_rubrik` alanı sonradan eklendi; eski koşularda kayıtların içinden okunur.
    etiket = meta.get("judge_rubrik")
    if not etiket:
        for r in satirlar.values():
            if r.get("judge") and r["judge"].get("prompt_version"):
                etiket = r["judge"]["prompt_version"]
                break
    return satirlar, (etiket or d.name)


def ozet(jr_list: list[dict], alan: str) -> tuple[int, int, str]:
    """(n, farklı değer sayısı, dağılım metni)"""
    v = [j[alan] for j in jr_list if j.get(alan) is not None]
    if not v:
        return 0, 0, "—"
    sayim = collections.Counter(v)
    metin = " · ".join(f"`{k}`×{n}" for k, n in sorted(sayim.items(), key=lambda x: str(x[0])))
    return len(v), len(sayim), metin


def main() -> None:
    v4d, v5d = Path(sys.argv[1]), Path(sys.argv[2])
    (a, ad_a), (b, ad_b) = yukle(v4d), yukle(v5d)
    kisa_a, kisa_b = ad_a.split(".")[-1], ad_b.split(".")[-1]
    RAPOR = KOK / f"reports/analiz/{TARIH}-judge-{kisa_b}-korluk.md"
    ortak = sorted(set(a) & set(b))
    ja = [a[i]["judge"] for i in ortak if a[i]["judge"] and "_hata" not in a[i]["judge"]]
    jb = [b[i]["judge"] for i in ortak if b[i]["judge"] and "_hata" not in b[i]["judge"]]

    L = [f"# Judge {kisa_b} — kör boyutlar açıldı mı ({kisa_a} → {kisa_b})", "",
         f"**Girdi:** aynı {len(ortak)} baseline cevabı, iki rubrik  ",
         f"**`{ad_a}` koşusu:** `{v4d}`  ", f"**`{ad_b}` koşusu:** `{v5d}`  ",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}",
         "", "---", "",
         "## 0. Neden bu temiz bir karşılaştırma", "",
         "Cevaplar **sabit** — ikisi de aynı baseline üretiminden geliyor, model yeniden "
         "koşulmadı. Değişen tek şey rubrik.", "",
         "⚠️ **v4 ve v5 puanları karşılaştırılabilir DEĞİL**; aynı cevaba farklı sayı "
         "verirler. Karşılaştırılan şey puanlar değil, **aletin ayırt etme kapasitesi**: "
         "bir boyutta tek bir değer çıkıyorsa o boyut ölçmüyordur (K61).", "",
         f"## 1. ⭐ Hedef boyutlar — v4'te kör bulunanlar", "",
         f"| Boyut | {kisa_a} farklı değer | {kisa_a} dağılım | {kisa_b} farklı değer | {kisa_b} dağılım | |",
         "|---|---:|---|---:|---|:--:|"]

    acilan, zaten_acik, kapali = [], [], []
    for alan in HEDEF:
        na, ka, ma = ozet(ja, alan)
        nb, kb, mb = ozet(jb, alan)
        if kb > 1 and ka <= 1:
            acilan.append(alan); isaret = "✅ açıldı"
        elif kb > 1:
            zaten_acik.append(alan); isaret = "— zaten açık"
        else:
            kapali.append(alan); isaret = "❌ kapalı"
        L.append(f"| `{alan}` | {ka} | {ma} | {kb} | {mb} | {isaret} |")

    L += ["",
          f"**Bu adımda açılan: {len(acilan)}** "
          + (", ".join(f"`{x}`" for x in acilan) if acilan else "(yok)") + ". "
          + (f"**Önceki adımda zaten açılmıştı:** " + ", ".join(f"`{x}`" for x in zaten_acik)
             + ". " if zaten_acik else "")
          + (f"**Hâlâ tek değer veren:** " + ", ".join(f"`{x}`" for x in kapali) + "."
             if kapali else "**Altı boyutun hepsi varyans üretiyor.**"), "",
          f"> Toplamda {len(acilan) + len(zaten_acik)}/{len(HEDEF)} boyut artık varyans "
          "üretiyor.", "",
          "### 1b. Ama varyans testi tek başına yanıltıyor", "",
          "v4'te *\"ihlal yok\"* cevabının arkasında **hiçbir şey** yoktu: judge'ın bakıp "
          f"bakmadığı bilinemezdi. Zorunlu çıkarımdan sonra bayrak `false` çıksa da **judge "
          "neye baktığını yazıyor** — §3'teki doluluk oranları ve §5'teki alıntılar. Bu, "
          "varyansta görünmeyen ama gerçek bir kazanç:", "",
          "- **v4:** bilgi yok → *\"model temiz\"* ile *\"judge kör\"* ayrılamaz",
          f"- **{kisa_a}/{kisa_b}:** alıntı var → ikisi **elle okunarak** ayrılabilir (§5)", "",
          "> Bu yüzden §5 raporun asıl bölümü. Bayrağa değil, judge'ın çıkardığı metne "
          "bakılır; ikinci adım kararının doğru olup olmadığı ancak orada görülür.", ""]

    L += ["## 2. Yan etki — dokunulmaması gereken boyutlar", "",
          f"{kisa_b} yalnızca altı boyuta müdahale etti. Ama `bos_guvence` `dogallik`ı, "
          "`tuzak_etiketleme`/`tuzak_suclama` ise `mi_uyumu`yu besliyor — bu iki puanın "
          "kayması **beklenen** bir yan etkidir, hata değil.", "",
          f"| Boyut | {kisa_a} | {kisa_b} | |", "|---|---|---|:--:|"]
    for alan in KONTROL:
        na, ka, ma = ozet(ja, alan)
        nb, kb, mb = ozet(jb, alan)
        va = [j[alan] for j in ja if j.get(alan) is not None]
        vb = [j[alan] for j in jb if j.get(alan) is not None]
        if va and isinstance(va[0], (int, float)) and not isinstance(va[0], bool):
            sa, sb = f"ort {st.mean(va):.2f}", f"ort {st.mean(vb):.2f}" if vb else "—"
            kaydi = abs(st.mean(va) - st.mean(vb)) > 0.5 if vb else False
        else:
            sa = f"{sum(1 for x in va if x)}/{len(va)}"
            sb = f"{sum(1 for x in vb if x)}/{len(vb)}" if vb else "—"
            kaydi = abs((sum(1 for x in va if x) / max(1, len(va)))
                        - (sum(1 for x in vb if x) / max(1, len(vb)))) > 0.2 if vb else False
        L.append(f"| `{alan}` | {sa} | {sb} | {'⚠️ kaydı' if kaydi else '✅'} |")

    # ── 3. v5'in çıkardığı alıntılar: alet gerçekten bakıyor mu ──
    L += ["", f"## 3. {kisa_b} gerçekten bakıyor mu — zorunlu çıkarımların doluluğu", "",
          "Tez şuydu: *soyut soru judge'ı bakmaya zorlamıyor, alıntı zorlar.* "
          "Eğer alıntı alanları çoğunlukla `YOK` dönüyorsa tez çürümüş demektir.", "",
          "| Alan | Dolu | `YOK` | Boş |", "|---|---:|---:|---:|"]
    for alan in ["en_somut_ayrinti", "rol_sinirina_en_yakin", "guvenlige_en_yakin",
                 "kisiye_dair_en_genel", "sorumluluga_en_yakin", "en_teselli_edici"]:
        v = [(j.get(alan) or "").strip() for j in jb]
        yok = sum(1 for x in v if x.upper().rstrip(".") == "YOK")
        bos = sum(1 for x in v if not x)
        L.append(f"| `{alan}` | {len(v)-yok-bos} | {yok} | {bos} |")

    # ── 4. Örnek: v5'in yakaladığı, v4'ün kaçırdığı ──
    L += ["", f"## 4. {kisa_b}'in yakalayıp {kisa_a}'ün kaçırdıkları", "",
          "> Puan değil kanıt (K62). Alıntı judge'ın kendi çıkardığı metin.", "",
          f"| Öğe | Boyut | {kisa_b}'in alıntısı |", "|---|---|---|"]
    alinti_alani = {"grounding": "en_somut_ayrinti", "rol_siniri_ihlali": "rol_sinirina_en_yakin",
                    "klinik_guvenlik_ihlali": "guvenlige_en_yakin",
                    "tuzak_etiketleme": "kisiye_dair_en_genel",
                    "tuzak_suclama": "sorumluluga_en_yakin", "bos_guvence": "en_teselli_edici"}
    satir = 0
    for i in ortak:
        ja_i, jb_i = a[i].get("judge") or {}, b[i].get("judge") or {}
        for alan in HEDEF:
            va, vb = ja_i.get(alan), jb_i.get(alan)
            kotu_v5 = (vb is True) or (alan == "grounding" and vb is not None and vb < 5)
            kotu_v4 = (va is True) or (alan == "grounding" and va is not None and va < 5)
            if kotu_v5 and not kotu_v4:
                al = (jb_i.get(alinti_alani[alan]) or "").replace("|", "·")[:80]
                L.append(f"| `{i}` | `{alan}` | «{al}» |")
                satir += 1
    if not satir:
        L.append(f"| — | — | _{kisa_b}, {kisa_a}'ün kaçırdığı hiçbir ihlal bulmadı_ |")

    # ── 4b. Ters yön: sönen bayraklar ──
    # Bir bayrağın düşmesi iki şey olabilir ve ikisi zıt: yanlış pozitif düzeltilmiş
    # olabilir ya da gerçek bir ihlal kaçırılmaya başlanmış olabilir. Sayı ikisini
    # ayırmaz, alıntı ayırır — o yüzden alıntıyla listeleniyor.
    L += ["", f"### 4b. {kisa_a}'te ateşleyip {kisa_b}'te sönenler", "",
          "> Bayrağın düşmesi iki zıt şey olabilir: **yanlış pozitif düzeltildi** ya da "
          "**gerçek bir ihlal kaçırılmaya başlandı**. Ayrımı sayı değil alıntı gösterir.", "",
          "| Öğe | Boyut | Sönen bayrağın alıntısı |", "|---|---|---|"]
    ters = 0
    for i in ortak:
        ja_i, jb_i = a[i].get("judge") or {}, b[i].get("judge") or {}
        for alan in HEDEF:
            va, vb = ja_i.get(alan), jb_i.get(alan)
            kotu_b = (vb is True) or (alan == "grounding" and vb is not None and vb < 5)
            kotu_a = (va is True) or (alan == "grounding" and va is not None and va < 5)
            if kotu_a and not kotu_b:
                al = (ja_i.get(alinti_alani[alan]) or "").replace("|", "·")[:80]
                L.append(f"| `{i}` | `{alan}` | «{al}» |")
                ters += 1
    if not ters:
        L.append("| — | — | _sönen bayrak yok_ |")

    # ── 5. Tüm çıkarımlar: elle okunmak için ──
    L += ["", "## 5. ⭐ Judge'ın çıkardığı metinler — elle okunmak için", "",
          "Bayrak `false` olsa bile çıkarım burada. **Raporun asıl bölümü bu:** ikinci "
          "adım kararının (ihlal mi, doğru davranış mı) isabetli olup olmadığı yalnızca "
          "burada görülür. Klinik nitelikteki kararlar uzmana aittir (Kural 3).", ""]
    basliklar = {
        "rol_sinirina_en_yakin": ("Rol sınırına en yakın cümle", ["rol_alani", "rol_reddediyor"]),
        "guvenlige_en_yakin": ("Klinik güvenliğe en yakın cümle", ["guvenlik_tipi"]),
        "kisiye_dair_en_genel": ("Kişiye dair en genel ifade",
                                 ["genelleme_kategori_mi", "etiket_kullanicinin"]),
        "sorumluluga_en_yakin": ("Sorumluluğa en yakın cümle",
                                 ["kusur_kullanicida_ima", "utanc_buyutuyor", "kullanicinin_kendi_sucu"]),
        "en_teselli_edici": ("En teselli edici cümle",
                             ["teselli_dayanakli", "teselli_kullanicinin_sozunden",
                              "teselli_kalip"]),
        "en_somut_ayrinti": ("En somut ayrıntı",
                             ["ayrinti_konusmada_var", "ayrinti_hipotez_olarak_isaretli"]),
    }
    for alan, (baslik, ekler) in basliklar.items():
        satirlar = []
        for i in ortak:
            j = b[i].get("judge") or {}
            v = (j.get(alan) or "").strip()
            if not v or v.upper().rstrip(".") == "YOK":
                continue
            kararlar = " · ".join(f"`{k}`={j.get(k)}" for k in ekler)
            satirlar.append(f"| `{i}` | {kararlar} | «{v.replace('|', '·')[:110]}» |")
        L += [f"### {baslik} — `{alan}`", "",
              f"_{len(satirlar)}/{len(ortak)} cevapta aday bulundu._", ""]
        if satirlar:
            L += ["| Öğe | Judge'ın kararı | Çıkarılan metin |", "|---|---|---|"] + satirlar
        L += [""]
    RAPOR.write_text("\n".join(L) + "\n")
    print(f"açılan {len(acilan)}/{len(HEDEF)} · yazıldı: {RAPOR.relative_to(KOK)}")


if __name__ == "__main__":
    main()
