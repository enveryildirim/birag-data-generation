#!/usr/bin/env python3
"""v0.0.8'in ESKİ katmanlarındaki alıntı/atıf kusurlarını düzeltir.

⛔⛔ **Bu katmanlar üç kapıyı hiç görmemişti.** `v4-parti1`, `v4-parti2` ve
`v5-parti3` zaman/kaynak · alıntı birebirlik · mekân kapıları yazılmadan önce
üretilmiş, yargılanmış ve `v0.0.7`'ye girmişti. Kapılar üzerlerinde koşturulunca
**17 aday** çıktı; elle okunduğunda **8'i gerçek**.

➡️ *Bir kapı yazıldığı anda yalnız sonraki veriyi korur; önceki veriyi ancak
ona geriye dönük koşulursa korur ve bu koşuyu kimse kendiliğinden yapmaz.*

⭐ Yanlış pozitifler de ölçüldü ve dördü adlandırıldı (gerekçeler betiğin
sonunda): kapının kendisine iki düzeltme çıktı (kök-önek deliği, asimetri).
"""
from __future__ import annotations
import json
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = "2026-09-17"

# (girdi judged dosyası, çıktı candidate dosyası, {sıra: [(eski, yeni, kural, gerekçe)]})
ISLER = [
 ("data/judged/v4-parti1.v7.jsonl", "data/candidates/v4-parti1.v8.jsonl", {
   8: [('hekimin haklı olma ihtimali', 'doktorun haklı olma ihtimali',
        "T125 eşanlamlı", "Kullanıcı «doktor haklı» dedi; cevap «hekim» yazdı. "
        "Anlam aynı, DAYANAK görünmez oluyor.")],
   12: [('"Ne diyeyim bilmiyorum" da bir cevap', '"ne diyim bilmiyorum" da bir cevap',
        "T105 alıntı", "Kullanıcı «ne diyim bilmiyorum» yazdı; alıntı yazımı "
        "düzeltilmiş. ⛔ Alıntı DÖNÜŞTÜRÜLEMEZ (T113: yansıtma dönüştürür, alıntı dönüştürmez).")],
 }),
 ("data/judged/v4-parti2.v2.v9.jsonl", "data/candidates/v4-parti2.v3.jsonl", {
   11: [('dün geceki içki tarafı', 'dün akşamki içki tarafı',
        "T125 eşanlamlı", "Kullanıcı «Dün akşam iki kadeh içtim» dedi.")],
   20: [('o masada bir şey değiştirmez. Orada oturan, tavlayı atan, o masayı bilen sensin',
         'orada bir şey değiştirmez. Orada oturan, tavlayı atan, orayı bilen sensin',
        "T122 mekân", "Kullanıcı «biz orda oturuyoruz tavla atıyoruz» dedi; «masa» "
        "makul bir ÇIKARIM ama kullanıcının sözü değil. Kendi sözcüğü kullanıldı."),
        ('Bildiğim tek şey, arkadaşının o cümleyi kurduğu',
         'Bildiğim tek şey, o çocuğun o cümleyi kurduğu',
        "T104 kaynak atfı", "Kullanıcı «bizim oradaki çocuklardan biri» dedi; "
        "«arkadaşın» ilişkiyi YÜKSELTİYOR — kullanıcının kurmadığı bir yakınlık."),
        ('Arkadaşın bunu söylediğinde masada ne oldu?', 'O bunu söylediğinde orada ne oldu?',
        "T104 + T122", "Aynı iki kusur, soru cümlesinde.")],
   32: [('Bir şey duymuşsun ve onunla ofise dönmüşsün.',
         'Bir şey duymuşsun ve onunla günün içine dönmüşsün.',
        "T122 mekân", "«ofis» konuşmada HİÇ geçmiyor — işyeri uydurulmuş. "
        "⭐ Bu cümle ARA turda; mekân kapısı yalnız SON cevaba bakıyor ve onu göremezdi."),
        ('Sen ofise dönmüşsün ve kafanda bir şey kalmış.',
         'Sen oradan çıkmışsın ve kafanda bir şey kalmış.',
        "T122 mekân", "Aynı uydurma, son cevapta.")],
   49: [('Her seferinde "son olsun" diyorsun', 'Her seferinde "son sigaram olsun" diyorsun',
        "T105 alıntı", "Kullanıcı «son sigaram olsun» yazdı; alıntı KIRPILMIŞ.")],
 }),
 ("data/candidates/v5-parti3.v4.jsonl", "data/candidates/v5-parti3.v5.jsonl", {
   9: [('"bırakmayı çok düşünmüyorum, sadece tuhaf oldum" diyorsun',
        '"bırakmayı çok düşünmüyorum aslında" diyorsun, arkasından da '
        '"sadece şu sayıyı görünce tuhaf oldum"',
        "T105 alıntı", "İki ayrı parça tek alıntı gibi birleştirilmiş ve aradaki "
        "«aslında» ile «şu sayıyı görünce» atılmıştı ⇒ alıntı EKLEMESİ (splice).")],
   52: [('sertleştiğin cümle "sözünü tutmuyorsun" idi',
         'sertleştiğin cümle "sözünü hiç tutmuyorsun" idi',
        "T105 alıntı", "«hiç» atılmış — alıntı, sevgilinin cümlesini HAFİFLETİYOR.")],
 }),
]


def main() -> int:
    hata = 0
    for gir, cik, D in ISLER:
        kayitlar = [json.loads(s) for s in (KOK / gir).read_text(encoding="utf-8").splitlines() if s.strip()]
        degisen = []
        for r in kayitlar:
            n = r["gen_meta"]["parti_sira"]
            if n not in D:
                continue
            # ⭐ SON cevap değil, BÜTÜN asistan turları taranır: ara turdaki bir
            # uydurma da modele gider (kapıların göremediği yer burası).
            turlar = [m for m in r["messages"] if m["role"] == "assistant" and m.get("content")]
            for eski, yeni, kural, gerekce in D[n]:
                nerede = [m for m in turlar if m["content"].count(eski) == 1]
                if len(nerede) != 1:
                    print(f"  ⛔ EŞLEŞME {gir} #{n}: {len(nerede)} tur")
                    hata += 1
                    continue
                nerede[0]["content"] = nerede[0]["content"].replace(eski, yeni)
                r["gen_meta"].setdefault("revizyon", []).append(
                    {"tarih": TARIH, "kural": kural, "gerekce": gerekce,
                     "kaynak": "kapıların eski katmanlara geriye dönük koşulması"})
            r["judge"] = None
            degisen.append(n)
        (KOK / cik).write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in kayitlar),
                               encoding="utf-8")
        print(f"{Path(cik).stem}: {len(degisen)} kayıt {sorted(degisen)} → {cik}")
    return 1 if hata else 0


if __name__ == "__main__":
    raise SystemExit(main())
