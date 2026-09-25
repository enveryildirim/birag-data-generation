#!/usr/bin/env python3
"""Üçüncü vaka serisi — «kural yazılı, KAPI YOK».

⛔⛔ Üçlünün tamamlayıcısı. Aynı kusur üç ayrı yerde durabiliyor:
  · **T22 serisi** — kapı VAR, yanlış ateşliyor (kusur kapının HÜKMÜNDE)
  · **T236 serisi** — kapı VAR, hiç göremiyor (kusur kapının BAKTIĞI ŞEYDE)
  · **bu seri** — kapı **YOK** (kusur kapının VARLIĞINDA)

⭐ **ALMA ÖLÇÜTÜ (önce yazıldı — T22'nin dersi).** Dördü birden:
  1. bir kural / sınır / hedef / iddia **yazılıydı** (belge, plan, talimat
     ya da karar),
  2. onu **uygulayan kod ya da ölçen rapor satırı yoktu** — ya da vardı
     ama o satırlarda hiç **koşmuyordu**,
  3. bu yüzden ihlal **sessizce geçti**, ya da *«denetlendi ve temiz»* ile
     *«hiç denetlenmedi»* **ayırt edilemez** oldu,
  4. eksikliği ortaya çıkaran şey kuralın kendisi değil **başka bir iş**.

⭐⭐ **Bu serinin ötekilerden farkı: ÇARESİ BİLİNİYOR ve ÖLÇÜLDÜ.** T209
aynı kuralı iki partide karşılaştırdı — parti3'te talimat, parti4'te kapı.
Öteki iki seride böyle bir karşılaştırma yok.

⛔⛔ Seri yine bir **ALT SINIRDIR** ve derleyeni benim (K30).
⛔ Satır ≠ üye: `K66` tek satır ama defterde **4 örneği** yazılı (T236'nın
   dersi — T22 serisinde bir aileyi 2 sayıp eksiltmiştim).

Çıktı: reports/analiz/2026-09-22-ucuncu-vaka-serisi.md
"""
from __future__ import annotations

import collections
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
RAPOR = KOK / f"reports/analiz/{TARIH}-ucuncu-vaka-serisi.md"

UYE = {"K66": 4}          # ⛔ defterde dört örneği tek tek yazılı

# ⛔⛔ Buluş sınıfı DİZGE EŞLEMESİYLE değil ELLE yazılır. Bir önceki
#   sürümde `"okuma" in metin` ile sınıflandırmıştım; *«ölçüm (3) +
#   gözden geçirme (1)»* böylece OKUMA sayıldı. ⭐ Tam da bu serinin ve
#   T22'nin uyardığı şey: mekanik eşleme Türkçe serbest metinde yanılır.
#   ⭐ Karma vakalar muhafazakârca ÖLÇÜM tarafında değil, ayrı sayılıyor.
BULUS_SINIF = {
    "K66": "karma", "K84": "okuma", "T35": "ölçüm", "T57": "denetim",
    "T82": "ölçüm", "T121": "okuma", "T139": "karma", "T145": "okuma",
    "T209": "ölçüm", "T213": "okuma",
}

# (kayıt, yazılı kural, kapı neden yoktu, biçim, nasıl bulundu, sonra ne oldu)
VAKA = [
 ("K66", "dört ayrı kural: thinking 4x tavanı · §5a-§3b hedefleri · "
  "özerklik vurgusu · `ELENEN_GUVENLIK` sözlüğü",
  "dördü de **yazıldı ve orada bırakıldı**; hiçbiri aynı commit'te koda ya "
  "da rapora bağlanmadı",
  "kod hiç yazılmadı",
  "ölçüm (3) + gözden geçirme (1)",
  "⭐ kalıp **adlandırıldı** ve kural oldu: *bir sınır yazıldığında aynı "
  "commit'te onu uygulayan kod ya da ölçen rapor satırı da yazılır*"),
 ("K84", "*«rapor üreticisinde hiçbir hüküm cümlesi sabit yazılmaz»* (K80'de "
  "yazılmıştı)", "kuralı denetleyen bir şey yoktu ⇒ **aynı kişi aynı gün "
  "ikinci betikte tekrarladı**; tablo *«3+ turlu 14»* derken metin "
  "*«istenilen derinlikte kayıt yok»* diyordu",
  "kural insan için yazılı, sınama için değil", "raporu okuma",
  "kural yazıldı; ⛔ denetimi hâlâ okumaya bağlı"),
 ("T35", "`safety_crisis`'in her öğesi **üç** `tip: judge` iddiası taşıyor "
  "(`rol_siniri_ihlali` · `bos_guvence` · `tuzak_suclama`)",
  "üç taramada da *«denetlenemedi»* kaldı — iddia yazılıydı, onu soran "
  "hiçbir koşu yoktu",
  "⛔ iddia hiç denetlenmedi",
  "ölçüm (üçü taramaya eklenerek)",
  "⭐ eksikliğin **yansız olmadığı** ölçüldü: ölçülmeyen eksen hangi "
  "taraftaysa orayı kayırıyor"),
 ("T57", "**Kural 7** — *«bir sayı raporlanıyorsa nasıl ölçüldüğü yazılı "
  "olmalı»*", "⭐⭐ kural *«yazılı»*yı denetliyordu ama **iki ayrı şey** var: "
  "İNSAN için yazılı ve SINAMA için yazılı. 7 betiğin argümanları rapor "
  "başlığında ilan edilmişti — insan okuyup koşabilir, sınama koşamaz",
  "kural insan için yazılı, sınama için değil", "Kural 7 denetimi (T54 izi)",
  "⛔ ayrım adlandırıldı; kuralın kendisi değişmedi"),
 ("T82", "`plan.md`: *«B-derin 3 öğede 1024 token'ı thinking içinde tüketip "
  "cevabı boş bıraktı»*",
  "olgu belgede yazılıydı, **eval tarafında kapı yoktu**",
  "kod hiç yazılmadı", "arşivi sayma",
  "⭐ 3226 kaydın **183'ü** dejenere çıktı — ve tek kusur değil ÜÇ kusurdu "
  "(`uretim_yok` 133 · `bos_cevap` 41 · `tekrar` 48)"),
 ("T121", "*«klinik güvenlik ihlali taşıyan kayıt korpusa giremez»* — "
  "`build.py`'nin **tek** otomatik güvenlik kapısı",
  "⛔⛔ kapı `if jr and jr.get(\"klinik_guvenlik_ihlali\")` yazıyordu: "
  "`judge` alanı **NULL** olan kayıt koşulun ilk yarısında düşüyor ve "
  "**kabul ediliyordu** ⇒ *«denetlendi ve temiz»* ile *«hiç denetlenmedi»* "
  "aynı kapıdan geçiyordu",
  "kapı vardı, kapsamı sessizce boştu", "kapı koşulunu okuma",
  "⛔ v0.0.8 için hazırlanan **300 yargılanmamış kayıt** derlenseydi klinik "
  "kapı hiçbirinde koşmamış olacaktı"),
 ("T139", "*«şablonlaşma korpusun kalitesini düşürür»* — §5a⁗ ve öncesi",
  "kalıpları yakalayan **hiçbir alan yoktu**; `klise_acilis` yalnız *kabul* "
  "cümlelerini soruyor", "kod hiç yazılmadı", "judge'ın düştüğü not + ölçüm",
  "⭐⭐ kapı yazıldı (K193) ve **elle yazılan liste 13 kalıp kaçırmış** çıktı "
  "— korpusun en büyük ikinci kalıbı listede yoktu (%7,5)"),
 ("T145", "*«çapa doğru cevabı düşürmemeli»* — `kacamak-kapisi`'nin OLUMLU "
  "sınaması", "sınama vardı ve doğruydu, ama `if o[\"id\"] not in DOGRU: "
  "continue` satırı ögelerin **%70'ini sessizce atlıyordu**; en kötü dağılım "
  "**sert** kapıda", "kapı vardı, kapsamı sessizce daraldı",
  "sınama betiğini okuma", "⛔ *«yanlış pozitif üretmiyor»* iddiası bu "
  "ögelerde **hiç sınanmamış** çıktı"),
 ("T209", "iki cümle ailesinin oranı tavanı aşmamalı",
  "parti3'te kural **yalnız talimatta** duruyordu; talimat dikkat kaymasına "
  "karşı işe yaramadı (itiraz %2→%8→**%20**, fark etme %3→%3→**%18**)",
  "kod hiç yazılmadı", "parti oranlarını ölçme",
  "⭐⭐⭐ **ÇARE ÖLÇÜLDÜ:** parti4'te aynı kural blok kapısına kondu (tavan "
  "%10, aşarsa **reddeder**) ⇒ talimat ve kapı **aynı kural üzerinde** yan "
  "yana kondu"),
 ("T213", "*«planın her satırı üretimden önce okunur»*",
  "ön tarama yalnız **işaretlediği** satırı okutuyordu; işaretlemediği satır "
  "üretim anına kadar hiç okunmuyordu",
  "kapı vardı, kapsamı sessizce daraldı", "üretim anında okuma",
  "⛔ `v6-parti5`'in **en ağır iki satırı** (`#33` emziren anne + md.2, "
  "`#39` el titremesi) işaretlenmemişti ⇒ kural *«her satır okunur»* oldu"),
]


def main() -> int:
    uye = lambda v: UYE.get(v[0], 1)
    N_SATIR, N_UYE = len(VAKA), sum(uye(v) for v in VAKA)
    bicim, bul = collections.Counter(), collections.Counter()
    for v in VAKA:
        bicim[v[3]] += uye(v)
        bul[BULUS_SINIF[v[0]]] += 1

    sat = ["# Üçüncü vaka serisi — «kural yazılı, KAPI YOK»", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Seri satırı:** {N_SATIR} · **belgelenmiş vaka:** {N_UYE}  ", "",
           "⭐ **Alma ölçütü (önce yazıldı):** kural yazılıydı · onu uygulayan "
           "kod ya da ölçen rapor satırı yoktu (ya da hiç koşmuyordu) · ihlal "
           "sessizce geçti veya *«denetlendi»* ile *«denetlenmedi»* ayırt "
           "edilemez oldu · eksikliği başka bir iş ortaya çıkardı.", "",
           "⛔⛔ **Üçlünün tamamlayıcısı** — aynı kusur üç ayrı yerde durabiliyor:", "",
           "| seri | kapı | kusur nerede |", "|---|---|---|",
           "| T22 | **var**, yanlış ateşliyor | kapının **hükmünde** |",
           "| T236 | **var**, hiç göremiyor | kapının **baktığı şeyde** |",
           "| ⭐ **bu seri** | **yok** | kapının **varlığında** |", "",
           "## Seri", "",
           "| # | kayıt | yazılı kural | kapı neden yoktu | biçim | nasıl bulundu | sonra ne oldu | üye |",
           "|---:|---|---|---|---|---|---|---:|"]
    for i, v in enumerate(VAKA, 1):
        n = UYE.get(v[0])
        sat.append("| " + str(i) + " | " + " | ".join(v) + " | "
                   + (f"**{n}**" if n else "1") + " |")

    sat += ["", "## Eksikliğin biçimi", "", "| biçim | vaka |", "|---|---:|"]
    sat += [f"| {k} | {v} |" for k, v in bicim.most_common()]
    sat += ["", "⭐⭐ **İkisi aynı ağırlıkta değil.** *«Kod hiç yazılmadı»* "
            "görünür bir boşluktur: kimse *«bu denetlendi»* demiyor. "
            "⛔⛔ *«Kapsamı sessizce daraldı»* ise **daha tehlikelidir** — "
            "kapı vardır, koşar, rapor *«geçti»* yazar, ama o satırlarda hiç "
            "bakmamıştır. `T121` bunun en saf hâli: kapı `NULL` yargıyı "
            "**kabul** ediyordu ⇒ *«denetlendi ve temiz»* ile *«hiç "
            "denetlenmedi»* aynı çıktıyı veriyordu.", "",
            "## Bunları ne buldu", "",
        "⛔ Sınıflar **elle** yazıldı, dizge eşlemesiyle değil — ilk "
        "sürümde `\"okuma\" in metin` karma bir vakayı okuma saymıştı. "
        "Satır bazındaki ayrıntı yukarıdaki tabloda duruyor.", "",
        "| bulan | satır |", "|---|---:|"]
    sat += [f"| {k} | {v} |" for k, v in bul.most_common()]
    okuma = bul["okuma"]
    sat += ["", f"⭐⭐⭐ **{N_SATIR} satırın {okuma}'ü doğrudan bir OKUMAYLA "
            "çıktı** (raporu okuma, kapı koşulunu okuma, sınama betiğini okuma, "
            "üretim anında satır okuma), ikisi de okuma+ölçüm karması. Kalanları ölçüm ve bir denetim buldu — ama **hiçbirini bir "
            "kapı bulmadı**, çünkü eksik olan şey zaten kapının kendisiydi. "
            "⛔ Bu, serinin kurucu döngüsü: *var olmayan kapıyı var olmayan "
            "kapı bulamaz.*", "",
            "## ⭐⭐⭐ Bu serinin ötekilerde olmayan şeyi: çare ölçüldü", "",
            "T209 aynı kuralı **iki partide yan yana** koydu:", "",
            "| | parti3 | parti4 |", "|---|---|---|",
            "| kural nerede | **yalnız talimatta** | **blok kapısında** |",
            "| itiraz ailesi | %2 → %8 → **%20** | tavan %10, aşarsa **reddedilir** |",
            "| fark etme ailesi | %3 → %3 → **%18** | — |", "",
            "➡️⭐⭐⭐ *Bir kuralın ihlali ancak iş bittikten sonra görünüyorsa "
            "hatırlatma yetmez, kapı gerekir. Talimat dikkat kaymasına karşı "
            "korumaz; korpus büyüdükçe ihlal oranı artar, çünkü talimat "
            "yazarın belleğine, kapı ise koşuya bağlıdır.*", "",
            "⭐ K66'nın kuralı bu serinin tek cümlelik özeti: **bir sınır, "
            "hedef ya da eleme yazıldığında aynı commit'te (a) onu uygulayan "
            "kod ya da (b) onu ölçen rapor satırı da yazılır.**", "",
            "## ⛔ Hâlâ açık olan", "",
            "| | |", "|---|---|",
            "| ⛔⛔ **`T121`'in canlı örneği bugüne kadar sürdü** | 370 kayıt "
            "yargılanmamıştı; `build.py`'nin kapısı onarıldı ama derleme o "
            "kayıtlarla yapılsaydı klinik kapı hiçbirinde koşmayacaktı |",
            "| ⛔ **`T35` kapanmadı** | üç `tip: judge` iddiası ölçüldü, ama "
            "denetimleri sürekli bir kapıya bağlanmadı |",
            "| ⚠️ **`T57` bir AYRIM, çare değil** | *«sınama için yazılı»* "
            "ölçütü adlandırıldı; Kural 7 hâlâ *«insan için yazılı»*yı ölçüyor |", "",
            "## ⛔ Bu serinin söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **ALT SINIR** | yalnız yakalanmış vakalar; **yazılıp hiç "
            "bağlanmamış ve hâlâ fark edilmemiş** kuralların sayısı tanımı "
            "gereği bilinemez ⇒ bu seri üçünün içinde **en eksik olanı** |",
            "| ⛔⛔ **Derleyen benim (K30)** | ölçüt yazılı, uygulaması benim |",
            "| ⛔ **T209 tek deney** | talimat↔kapı karşılaştırması bir kural "
            "ve iki parti üzerinde; yinelenmedi ⇒ *«kapı hep daha iyidir»* "
            "genellemesi bu tek karşılaştırmadan çıkarılamaz |",
            "| ⚠️ **Kapı yazmanın MALİYETİ ölçülmedi** | her kural bir kapı "
            "olursa kapı sayısı artar ve T22 serisi **kapıların da yanıldığını** "
            "gösteriyor ⇒ *«her kurala kapı»* ücretsiz değil |"]
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("\n".join(sat[sat.index("## Eksikliğin biçimi"):]))
    print(f"\n→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
