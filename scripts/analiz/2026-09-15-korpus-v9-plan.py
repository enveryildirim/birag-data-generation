#!/usr/bin/env python3
"""Korpus koşusunun TASARIMI — koşudan ÖNCE yazılır (T24).

v8 ve v9 bugüne dek yalnızca **Eksen 2'de** (safety_crisis, 20 kriz öğesi) ölçüldü.
Oysa ikisi de üretim hattının varsayılanı (K118/K120) ve hattın işlediği şey korpus.

⭐ Korpusun burada ölçebildiği, Eksen 2'nin ÖLÇEMEDİĞİ iki şey var:

  1. **Bağlam belgesi.** Eksen 2'nin hiçbir öğesinde `context` yok; korpusta **10**
     kayıtta var. v7'nin RAG kaçışı ile v9'un `rol_baglam_alintisi` /
     `yordam_baglam_alintisi` **doğrulaması** ancak orada uyarılabilir.
  2. **Çok turluluk.** Eksen 2'nin öğeleri tek turlu; korpusta **32** kayıt çok turlu.
     v9'un *«dayanak hangi turdan geliyor»* kararını KODUN vermesi ancak orada
     anlamlı — tek turlu bir konuşmada kullanıcı turu zaten tek adaydır.

⛔ **Kapsam kararı: v8 DE koşulur.** v8 korpusta hiç koşmadı; yalnızca v9 koşulsaydı
v7→v9 farkı **iki sürümü birden** taşırdı ve hiçbir kaleme atfedilemezdi. İki koşu,
zinciri korpusta da tamamlar (v7 → v8 → v9, aynı 104 kayıt).

Kullanım: uv run python scripts/analiz/2026-09-15-korpus-v9-plan.py
"""
from __future__ import annotations

import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402

KORPUS = KOK / "data/candidates/v3-kumulatif.jsonl"
V7JUDGE = KOK / "data/judged/v3-kumulatif.v7.jsonl"
RUBRIKLER = {v: KOK / f"prompts/judge-eksen1.{v}.md" for v in ("v7", "v8", "v9")}
CIKTI = KOK / "reports/analiz/2026-09-15-korpus-v9-tasarim.md"
# v7 korpus koşusunun commit'i — iş kurucusunun ve render'ın kimliği oradan doğrulanır.
V7_COMMIT = "0b3c43f"
KONTROL_TOHUM = 20260915
KONTROL_N = 24

OLCUTLER = [
 ("Ö1", "⭐ **KORPUSUN VARLIK SEBEBİ: iki yol ilk kez uyarılıyor.** (a) `context` taşıyan "
  "10 kayıtta bağlam kaçışının **doğrulaması**, (b) çok turlu 32 kayıtta dayanağın "
  "**hangi tura** ait olduğunun kodca bulunması. Her ikisinin kaç kez uyarıldığı "
  "raporlanır. ⛔ **Sıfır çıkarsa v9'un o parçaları hâlâ sınanmamıştır ve öyle yazılır** "
  "— Eksen 2 koşusunda kod kapısının 0 kez ateşlemesi (T46) tam olarak bu sebeple "
  "bir eksiklik olarak kaydedilmişti."),
 ("Ö2", "**Her değişen karar atfedilebilmeli.** v7→v8 ve v8→v9 ayrı ayrı okunur; "
  "v9'un makine-okunur izleri (`alinti_dogrulanmadi` · `teselli_dayanak_dogrulandi` · "
  "`alinti_dogrulama`) ve alan değerleri kullanılır. Atfedilemeyen değişim gürültüdür "
  "ve gürültü bandıyla karşılaştırılır."),
 ("Ö3", f"⛔ **Gürültü tabanı.** v7'nin korpusta **üç geçişi** var (K106), yani v7'nin "
  f"tabanı zaten ölçülü. v9 için taban, tohum `{KONTROL_TOHUM}` ile çekilen "
  f"**{KONTROL_N} rastgele kayıt** × 2 ek geçişle ölçülür; tohum ve büyüklük burada, "
  "koşudan önce yazılıdır. ⚠️ v8'e ayrı taban koşulmaz — v8 bu koşuda **köprü**, "
  "kendi başına bir iddia taşımıyor. Bu, v8'e ait farkların tek tek okunamayacağı "
  "anlamına gelir ve raporda öyle yazılır."),
 ("Ö4", "⭐ **ÜRETİM SONUCU ölçülür.** v9 hattın varsayılanı (K120): korpus kayıtlarının "
  "**bayrakları** (`rol_siniri_ihlali` · `klinik_guvenlik_ihlali` · `bos_guvence` · "
  "`tuzak_suclama` · `tuzak_etiketleme`) ve **hesaplanan üç puanı** v7'ye göre nasıl "
  "değişiyor. Bu sayı doğrudan hangi kaydın eğitime gireceğini etkiler."),
 ("Ö5", "⛔ **Doğrulayıcının kendi hata oranı yine ölçülür.** Eksen 2'de 0 çıktı ama "
  "orada bağlam belgesi yoktu. Korpusta `rol_baglam_alintisi` bir **belgeden** "
  "alıntı ister; belge metniyle eşleşme, konuşma metniyle eşleşmeden daha kırılgandır. "
  "`alinti_dogrulanmadi` kayıtlarının tamamı dökülür ve elle okunur."),
 ("Ö6", "**Maliyet:** bozuk JSON, eksik alan, kaldırılan alanı yine de yazan kayıt."),
 ("Ö7", "**Dokunulmayan boyutlar kaymamalı.** v9 F1/F3/F4/F5'e ve Bölüm A-E'ye "
  "dokunmadı; `anlasilirlik_holistik` · `dogallik_holistik` · `mi_uyumu_holistik` · "
  "`duygusal_tepki` · `yorumlama` · `kesif` ortalamaları raporlanır. ⚠️ Beklenti "
  "yazılmıyor: v7'nin kendi kontrol koşusu bu boyutlarda rubrik etkisinden BÜYÜK "
  "kayma üretmişti (K61), yani buradaki kayma **rubriğe delil değildir** — yalnızca "
  "gürültünün büyüklüğünü hatırlatır."),
]

REDDEDILEN = [
 ("Yalnızca v9'u koşmak",
  "⛔ v8 korpusta hiç koşmadı; v7→v9 farkı **iki sürümü birden** taşır ve hiçbir "
  "kaleme atfedilemez. Tam da bu projenin sürekli eleştirdiği türden bir sayı olurdu."),
 ("v8'e de gürültü tabanı koşmak",
  "⛔ v8 bu koşuda köprü; kendi başına bir iddiası yok. 24×2 ek iş, okunmayacak bir "
  "sayı için harcanırdı. ⚠️ Bedeli açık: v8'e ait farklar tek tek okunamaz."),
 ("İş dosyalarını v7'nin dizinlerinden kopyalamak",
  "⛔ O dosyalar Kural 8 gereği silinmiş. Yerine **daha güçlü** bir kanıt kullanılıyor: "
  f"iş kurucusu (`prompt_kur`) ve render (`_render_conversation`, `_last_assistant`) "
  f"commit `{V7_COMMIT}` ile **birebir aynı** — yani üretilen kuyruk v7'nin kuyruğuyla "
  "aynı olmak zorunda. Kimlik dosyadan değil **koddan** doğrulanıyor."),
 ("Korpusu yeniden ÜRETMEK",
  "⛔ Puanlanan metin değişmemeli; ölçülen şey rubrik."),
 ("Eksen 2'nin hakemlik kümesini korpusa taşımak",
  "⛔ Farklı nüfus. Korpusun kendi rastgele kümesi tohumla çekiliyor."),
]


def kontrol_kumesi(idler: list[str]) -> list[str]:
    return sorted(random.Random(KONTROL_TOHUM).sample(sorted(idler), KONTROL_N))


def main() -> int:
    hata = []
    kayitlar = [json.loads(l) for l in KORPUS.open(encoding="utf-8")]
    idler = [r["id"] for r in kayitlar]
    n = len(kayitlar)
    baglamli = [r["id"] for r in kayitlar if r.get("context")]
    turlu = [r["id"] for r in kayitlar
             if sum(1 for m in r["messages"] if m["role"] == "assistant") > 1]
    if n != 104:
        hata.append(f"korpus {n} kayıt, beklenen 104")

    # Render kimliği — v7'nin kuyruğuyla aynı olduğunun KANITI
    kimlik = {}
    for ad, dosya in (("_render_conversation", "src/filter.py"),
                      ("_last_assistant", "src/filter.py"),
                      ("prompt_kur", "scripts/analiz/2026-09-15-judge-isleri-hazirla.py")):
        eski = subprocess.run(["git", "show", f"{V7_COMMIT}:{dosya}"], cwd=KOK,
                              capture_output=True, text=True, check=True).stdout
        yeni = (KOK / dosya).read_text(encoding="utf-8")

        def cikar(metin: str, ad: str) -> str:
            sat, al = [], False
            for l in metin.splitlines():
                if l.startswith(f"def {ad}"):
                    al = True
                elif al and l.startswith("def "):
                    break
                if al:
                    sat.append(l)
            return "\n".join(sat)
        a, b = cikar(eski, ad), cikar(yeni, ad)
        kimlik[ad] = (a == b and bool(a))
        if not kimlik[ad]:
            hata.append(f"RENDER · `{ad}` {V7_COMMIT}'ten farklı — kuyruk kimliği kurulamaz")

    rub = {v: hashlib.sha256(p.read_bytes()).hexdigest()[:16] for v, p in RUBRIKLER.items()}
    if len({rub["v7"], rub["v8"], rub["v9"]}) != 3:
        hata.append("rubrik hash'leri ayrışmıyor")
    if not V7JUDGE.exists():
        hata.append(f"v7 judge dosyası yok: {V7JUDGE}")

    if hata:
        print("⛔ TASARIM VERİYLE UYUŞMUYOR — belge yazılmadı:")
        for h in hata:
            print("   ·", h)
        return 1

    kontrol = kontrol_kumesi(idler)
    y = [
        "# Korpus koşusu (v8 + v9) — TASARIM *(koşudan ÖNCE yazıldı)*",
        "",
        f"*2026-09-15 · betik `{Path(__file__).relative_to(KOK)}`*",
        f"*korpus `data/candidates/v3-kumulatif.jsonl` SHA256 "
        f"`{hashlib.sha256(KORPUS.read_bytes()).hexdigest()[:16]}` · {n} kayıt*",
        f"*rubrikler: v7 `{rub['v7']}` · v8 `{rub['v8']}` · v9 `{rub['v9']}`*",
        "",
        "## Soru",
        "",
        "v8 ve v9 üretim hattının varsayılanı (K118/K120) ama ikisi de yalnızca **Eksen",
        "2'de** (20 kriz öğesi) ölçüldü. Hattın işlediği şey korpus. İki soru:",
        "**(1)** v9 korpus kararlarını değiştiriyor mu — yani hangi kaydın eğitime gireceğini?",
        "**(2)** v9'un Eksen 2'de **hiç uyarılamayan** iki parçası burada uyarılıyor mu?",
        "",
        "## ⭐ Korpusun ölçebildiği, Eksen 2'nin ölçemediği",
        "",
        "| yol | Eksen 2 | korpus |",
        "|---|---:|---:|",
        f"| `context` (bağlam belgesi) taşıyan kayıt | **0**/114 | **{len(baglamli)}**/{n} |",
        f"| çok turlu kayıt (1'den fazla BıRAG turu) | **0**/114 | **{len(turlu)}**/{n} |",
        "",
        "⭐ v9'un iki mekanizması **yalnızca** bu iki yolda uyarılabilir: bağlam kaçışının",
        "alıntı **doğrulaması** ve dayanağın **hangi tura ait olduğunun** kodca bulunması.",
        "Eksen 2'de kod kapısının 0 kez ateşlemesi (T46) kısmen bunun sonucuydu.",
        "",
        "## Küme ve aşamalar",
        "",
        "| Aşama | Ne | k |",
        "|---|---|---|",
        f"| 1a | {n} kayıt, **v8** rubriğiyle, kör | 1 |",
        f"| 1b | {n} kayıt, **v9** rubriğiyle, kör | 1 |",
        f"| 2 | tohumla çekilmiş **{KONTROL_N}** kayıt, v9 ile 2 ek geçiş | 3 |",
        "",
        "⛔ **v8 DE koşuluyor** çünkü korpusta hiç koşmadı. Yalnızca v9 koşulsaydı v7→v9",
        "farkı iki sürümü birden taşır ve hiçbir kaleme atfedilemezdi.",
        "⚠️ v8'e ayrı gürültü tabanı **koşulmuyor** — köprü rolünde. Bunun bedeli:",
        "**v8'e ait farklar tek tek okunamaz.**",
        "",
        "### Kuyruk kimliği — dosya değil KOD doğrulandı",
        "",
        f"v7 korpus koşusunun iş dosyaları Kural 8 gereği silinmiş. Yerine commit "
        f"`{V7_COMMIT}` ile kod kimliği doğrulandı:",
        "",
        "| işlev | v7 commit'i ile aynı |",
        "|---|:--:|",
    ]
    for ad, ok in kimlik.items():
        y.append(f"| `{ad}` | {'✅' if ok else '⛔'} |")
    y += [
        "",
        "➡️ Üretilen konuşma kuyruğu v7'nin kuyruğuyla **aynı olmak zorunda**; kimlik",
        "dosya karşılaştırmasıyla değil **kod karşılaştırmasıyla** kuruluyor.",
        "",
        f"### Yansız kontrol kümesi — tohum `{KONTROL_TOHUM}`, {KONTROL_N} kayıt",
        "",
        "Ayrışmadan **bağımsız** çekildi; ayrışan kayıtlarla kesişmesi beklenen ve",
        "istenen bir durumdur. Çekilen kimlikler (ilk 8 hane):",
        "",
        "> " + " · ".join(f"`{i[:8]}`" for i in kontrol),
        "",
        "## Karar ölçütü *(T24 — önceden yazıldı, sonradan gevşetilmez)*",
        "",
    ]
    for kod, met in OLCUTLER:
        y.append(f"- **{kod}.** {met}")
    y += ["", "## Elenen alternatifler *(Kural 7)*", "",
          "| Alternatif | Neden değil |", "|---|---|"]
    for alt, neden in REDDEDILEN:
        y.append(f"| {alt} | {neden} |")
    y += [
        "",
        "## Bu koşunun ölçmeyeceği",
        "",
        "- **Judge ailesi sapması (K45).** Korpusu Claude yazdı, judge da Claude ailesi —",
        "  bilinen ve ölçülmüş bir sapma (+6/+11 puan). Karşılaştırma yine temiz (v7 de",
        "  aynı aile) ama mutlak puanlar bu sapmayı taşıyor.",
        "- **Uzman uyumu.** K27 örneklemi gerekir.",
        "- **Kriz davranışı.** Korpusta kriz kaydı yok (Kural 3); F2/F7 burada zayıf uyarılır.",
        "- **v8'e ait farkların tek tek okunması** — v8'in kendi tabanı ölçülmüyor.",
    ]
    CIKTI.write_text("\n".join(y) + "\n", encoding="utf-8")
    print(f"✅ {CIKTI.relative_to(KOK)}")
    print(f"   {n} kayıt · bağlamlı {len(baglamli)} · çok turlu {len(turlu)}")
    print(f"   kontrol {len(kontrol)} (tohum {KONTROL_TOHUM}) · render kimliği {kimlik}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
