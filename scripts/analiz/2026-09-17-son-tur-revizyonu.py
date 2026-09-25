#!/usr/bin/env python3
"""Son tur: §5a⁗, yapısal atıf ve kalan iki uydurma.

⭐ Bu betik, **ikinci okumadan** ve **yeni yazılan kapıdan** gelen kusurları
kapatır. İkisi de bir öncekinden sonra doğdu:
  · §5a⁗ — `v5-parti6 #33`'ü İKİ hakem birden `riski_atlama` saydı ve ben
    ikisine de yanıldığımı düşünmüştüm. Kural yazıldı, kayıt düzeltildi.
  · T104'ün altıncı üyesi (**yapısal atıf**) — *«aynı cümlede»* iddiası
    için kapı yazıldı ve dört gerçek kusur buldu.

⛔ **Anahtar `(parti, sıra, no)`** — aynı kayda birden çok düzeltme meşrudur
ve sözlükte sessiz üzerine yazma olmamalı (bir kez oldu, bir düzeltme yutuldu).
⭐ Tarama BÜTÜN asistan turlarında: ara turdaki kusur da modele gider.
"""
from __future__ import annotations
import collections, json, re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = "2026-09-17"

D: dict[tuple, tuple[str, str, str, str]] = {

 ("v5-parti6", 33, 1): (
   'Kilonun ne anlama geldiğini ben söyleyemem — bedende olanı yorumlamak benim işim değil.',
   'Kilonun ne anlama geldiğini ben söyleyemem — bedende olanı yorumlamak benim işim değil. '
   'Söyleyebilecek olan bir hekim; ne diyeceğini de bilmiyorum.',
   "§5a⁗",
   "⛔ İKİ hakem birden `riski_atlama` dedi ve ben ikisine de yanıldığımı düşünmüştüm. "
   "Cevap ayrıntıyı adlandırıyor, sonra yorumlamayı reddediyor, sonra sofra konusuna "
   "dönüyor. «Söyleyemem» bir kapı kapatır; başka kapı göstermemek çıkmaz bırakır. "
   "⭐ Kaynak TÜRÜ yazıldı, erişilebilirlik iddia edilmedi (§8b′)."),
 ("v5-parti6", 33, 2): (
   'Kurmanı da istemiyorum; yalnız ikisini aynı mesajda yazdığını söylüyorum.',
   'Kurmanı da istemiyorum; yalnız ikisini de senin yazdığını söylüyorum.',
   "T104 yapısal atıf",
   "⛔ «peynir karpuz» 1. turda, «pantolon» 3. turda — «aynı mesajda» YANLIŞ."),

 ("v5-parti3", 37, 1): (
   'ama meyhanede olduğunu da aynı cümlede söyledin.',
   'ama meyhanede olduğunu da sen yazdın, bir mesaj önce.',
   "T104 yapısal atıf",
   "⛔ Judge buldu: «meyhanedeydik» 2. turda, «alkolle alakası yok» 3. turda. "
   "İki söz aynı cümlede değil, aynı KONUŞMADA."),

 ("v5-parti5", 29, 1): (
   'İkisini aynı cümlede yazmışsın.',
   'İkisini aynı mesajda yazmışsın.',
   "T104 yapısal atıf",
   "«babamı iki hafta önce kaybettim.» ve «yine başladım» AYRI cümleler, aynı mesaj. "
   "⭐ İnce ama ölçülebilir: «cümle» ile «mesaj» ayrı düzeylerdir."),

 ("v5-parti8", 34, 1): (
   '"Azar azar gitti" ile "fark etmedim" aynı cümlede duruyor.',
   '"Azar azar gitti" ile "fark etmedim" aynı mesajda duruyor.',
   "T104 yapısal atıf",
   "Kullanıcı «azar azar gitti, bir seferde değil.» ve «o yüzden fark etmedim ben de» "
   "diye İKİ cümle yazdı; aynı tur, ayrı cümle."),

 ("v5-parti7", 17, 1): (
   'Akıl vermeyeceğim; istemedin ve zaten benim işim de değil.',
   'Akıl vermeyeceğim; benim işim değil.',
   "K120 dayanak",
   "⛔ Kullanıcı akıl istemediğini HİÇ söylemedi — tek turu «bu gece duvar "
   "dibindeyim. kimse açmadı kapıyı». Cevap ona söylemediği bir edimi atfediyordu."),

 ("v5-parti8", 26, 1): (
   'Aile hekimliği aklıma gelen yer; okulunda bir sağlık birimi varsa o da olur.',
   'Aile hekimliği aklıma gelen yer.',
   "K120 dayanak",
   "⛔⛔ BENİM KENDİ DÜZELTMEM UYDURMAYI TAŞIDI: özgün cümlede «öğrenci sağlık "
   "birimi» vardı ve ben onu «okulunda … varsa» diye koşullayarak koruduğumu "
   "sandım. Ama kullanıcı okuldan/öğrencilikten HİÇ söz etmiyor — «varsa» "
   "birimin varlığını koşullandırıyor, kullanıcının öğrenci olmasını değil. "
   "➡️ *Bir uydurmayı koşul kipine almak onu dayanaklı yapmaz.*"),
}

GIRDI = {"v5-parti3": "data/candidates/v5-parti3.v5.jsonl",
         "v5-parti5": "data/candidates/v5-parti5.v4.jsonl",
         "v5-parti6": "data/candidates/v5-parti6.v4.jsonl",
         "v5-parti7": "data/candidates/v5-parti7.v4.jsonl",
         "v5-parti8": "data/candidates/v5-parti8.v4.jsonl"}
CIKTI = {"v5-parti3": "data/candidates/v5-parti3.v6.jsonl",
         "v5-parti5": "data/candidates/v5-parti5.v5.jsonl",
         "v5-parti6": "data/candidates/v5-parti6.v5.jsonl",
         "v5-parti7": "data/candidates/v5-parti7.v5.jsonl",
         "v5-parti8": "data/candidates/v5-parti8.v5.jsonl"}


def main() -> int:
    ks = re.findall(r'^ \("(v5-parti\d)", (\d+), (\d+)\): \(',
                    Path(__file__).read_text(encoding="utf-8"), re.M)
    yin = [k for k, v in collections.Counter(ks).items() if v > 1]
    if yin:
        raise SystemExit(f"⛔ Yinelenen anahtar: {yin}")
    print(f"⭐ {len(ks)} düzeltme girdisi, yinelenme yok")

    hata = 0
    for parti, gir in GIRDI.items():
        kayitlar = [json.loads(s) for s in (KOK / gir).read_text(encoding="utf-8").splitlines() if s.strip()]
        degisen, uygulanan = [], 0
        for r in kayitlar:
            n = r["gen_meta"]["parti_sira"]
            islem = [v for k, v in D.items() if k[0] == parti and k[1] == n]
            if not islem:
                continue
            turlar = [m for m in r["messages"] if m["role"] == "assistant" and m.get("content")]
            for eski, yeni, kural, gerekce in islem:
                nerede = [m for m in turlar if m["content"].count(eski) == 1]
                if len(nerede) != 1:
                    print(f"  ⛔ EŞLEŞME {parti} #{n}: {len(nerede)} tur")
                    hata += 1
                    continue
                nerede[0]["content"] = nerede[0]["content"].replace(eski, yeni)
                uygulanan += 1
                r["gen_meta"].setdefault("revizyon", []).append(
                    {"tarih": TARIH, "kural": kural, "gerekce": gerekce,
                     "kaynak": "ikinci okuma + yapısal atıf kapısı"})
            r["judge"] = None
            degisen.append(n)
        bekle = len([k for k in D if k[0] == parti])
        (KOK / CIKTI[parti]).write_text(
            "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in kayitlar), encoding="utf-8")
        print(f"{parti}: {len(degisen)} kayıt · {uygulanan}/{bekle} düzeltme → {CIKTI[parti]}")
        if uygulanan != bekle:
            print(f"  ⛔ {bekle - uygulanan} düzeltme UYGULANMADI")
            hata += 1
    return 1 if hata else 0


if __name__ == "__main__":
    raise SystemExit(main())
