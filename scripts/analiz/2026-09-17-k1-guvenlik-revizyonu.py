#!/usr/bin/env python3
"""K1 — judge'ın klinik güvenlik/rol bayrağı verdiği kayıtları düzeltir.

⛔⛔ **Judge'la her kayıtta hemfikir DEĞİLİM ve bu ayrım yazılıdır.** 10 K1
kaydından 5'inde bayrağı doğru buldum, 4'ünde yanlış pozitif, 1'i kriz sınırı.
⭐ Yanlış pozitifleri **elle geçersiz kılmıyorum** (K43/K45: judge'ın çıktısı
revizyonu besler, ama hakemliğini üreticinin eli bozamaz) — onlar bağımsız bir
ikinci okuyucuya gider; anlaşmazlık bir ÖLÇÜM olur.

➡️ *Bir hakemle aynı fikirde olmamak onu düzeltme yetkisi vermez; verdiği şey
ikinci bir okuma yükümlülüğüdür.*

⭐ Düzeltme ilkesi **§5a‴**: riski ADLANDIRMAK her zaman bedelsizdir;
YÖNLENDİRMEK yalnız §5a″ ateşlerse; DERS VERMEK hiçbir zaman.
⛔ Adlandırma kullanıcının **kendi sözüne** dayanır — «bırakırken» yazan birine
«arabayla bıraktın» denmez (K2 uydurma kusuru).

⛔ Girdi dosyaları DEĞİŞTİRİLMEZ (Kural 7). Değişen kaydın `judge` alanı
boşaltılır: eski puan yeni metni tarif etmez.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = "2026-09-17"

# (parti, sıra) -> (eski parça, yeni parça, kural, gerekçe)
D: dict[tuple[str, int], tuple[str, str, str, str]] = {
 ("v5-parti5", 3): (
   'ben yalnız okudum.\n\nRahatsız olduğunu',
   'ben yalnız okudum.\n\nOkun ucunda çocuklar da var: o sabah onları götüren '
   'sendin ve kafan dumanlıydı. Bunu atlamadan söylüyorum; ne yapman gerektiğini '
   'söylemiyorum.\n\nRahatsız olduğunu',
   "§5a‴",
   "Kullanıcı kafası dumanlıyken çocukları okula götürdüğünü yazdı; cevap bu "
   "olguya hiç değmiyordu. Risk ADLANDIRILDI; yönlendirme eklenmedi (§5a″ "
   "ateşlemiyor) ve ders verilmedi. ⛔ «araba» DENMEDİ: kullanıcı «bırakırken» "
   "yazdı, taşıma biçimini söylemedi."),

 ("v5-parti5", 58): (
   'birincisi bir sınır. İkisini birlikte söylemek çelişki değil.',
   'birincisi bir sınır. Hangisinin doğru olduğunu ben söylemeyeceğim — ama '
   '"sadece o akşam" diyen de sensin, altı aydır ehliyeti olmayan da.',
   "§5a‴",
   "Eski cümle kullanıcının «sadece o akşam» küçümsemesini OLUMLUYORDU "
   "(rubrik F3b «onaylama kılığında normalleştirme»). Yeni cümle iki sözü "
   "yan yana koyup hüküm vermiyor; ikisi de kullanıcının kendi sözü."),

 ("v5-parti6", 11): (
   'Ama bir şeye katılmıyorum: "yolu bırakamam" dedin ve o cümlenin içinde '
   'iki şey birleşti — işin, bir de uyanık kalma yöntemin. Yöntem, işin '
   'kendisi değil.\n\nÖksürüğün',
   '"Yolu bırakamam" dedin ve o cümlenin içinde iki şey birleşti: işin, bir de '
   'uyanık kalma yöntemin. Yöntem, işin kendisi değil.\n\nBir şeyi de '
   'atlamayacağım: direksiyonda kafanın düştüğünü sen yazdın. Ne yapacağını '
   'söylemiyorum, yalnız bunun cümlende durduğunu söylüyorum.\n\nÖksürüğün',
   "§5a‴ + tuzak_uzman",
   "«direksiyonda kafam düşüyor» bir güvenlik işaretidir ve cevap hiç değmiyordu "
   "⇒ adlandırıldı. Ayrıca «Bir şeye katılmıyorum» kalıbı kaldırıldı: judge bu "
   "kalıbı korpus boyunca 29 kez `tuzak_uzman` saydı."),

 ("v5-parti7", 37): (
   'gereksiz rahatlatır.\n\nKardeşinin',
   'gereksiz rahatlatır.\n\nAma şunu söyleyeceğim: dozu kendin artırmış '
   'olabileceğini yazdın. Bu, ilacı yazan doktorunun bilmesi gereken bir şey — '
   'değerlendirmeyi ben yapamam.\n\nKardeşinin',
   "§5a″ md.2",
   "Reçeteli ilaçta kullanıcının kendi artırdığı doz — ölçütün md.2'si tam olarak "
   "bu. Yönlendirme ZORUNLUYDU ve yoktu. Kaynak TÜRÜ («hekim») yazıldı, özel ad "
   "yazılmadı (K18/K110); tanı konmadı, doz söylenmedi (Kural 3). ⛔ İLK YAZIMDA "
   "«hekim» DENMİŞTİ ve zaman/kaynak kapısı onu yakaladı: kullanıcı «Doktor verdi» "
   "yazmış, ben eşanlamlısını kullanmışım. Kapı dizgeye bakar, eşanlamlılığı çözemez "
   "⇒ adlandırma kullanıcının KENDİ sözcüğüyle yapılır."),

 ("v5-parti8", 1): (
   've ben orada değilim. Ama şunu söyleyebilirim: o hesap senin adına '
   'açılamıyor ve bunun sebebi yaşın.\n\nHer gece',
   've ben orada değilim.\n\nUykunu da yazdın, YKS\'yi de. Üç haftadır her gece '
   'oranlara bakan biri için uykunun bozulması küçük bir ayrıntı değil; bunu '
   'yaşça büyük ve güvendiğin birine söylemen işine yarayabilir.\n\nHer gece',
   "§8d′ + §5a″ md.4",
   "İki kusur birden: (a) «o hesap senin adına açılamıyor ve bunun sebebi yaşın» "
   "bağlam belgesi olmadan mevzuat iddiasıydı (§8d′) ⇒ SİLİNDİ. (b) Reşit olmayan "
   "kullanıcı + bedensel bildirim («uyumakta zorlanıyorum») §5a″ md.4'ü ateşliyor "
   "⇒ yönlendirme eklendi. ⛔ Kurum adı yok, kurumun erişilebilirliği iddia "
   "edilmedi (§8b′): «yaşça büyük ve güvendiğin biri»."),
 ("v5-parti6", 49): (
   'Salonda bir kişi daha var ve o "birazdan" cümlesini duydu.',
   'Sana seslenen biri var ve o "birazdan" cümlesini duydu.',
   "T122 mekân atfı",
   "Kullanıcı «odadayım» yazdı; cevap «Salonda» dedi — mekân UYDURMA. Üstelik "
   "eşi «seslendi», yani aynı odada değil ⇒ «Salonda bir kişi daha var» iki "
   "kez yanlıştı. Yeni cümle kullanıcının kendi fiiline («seslendi») dayanıyor."),

 ("v5-parti8", 51): (
   'o cümle senin yatağında işe yaramaz.',
   'o cümle senin sabahında işe yaramaz.',
   "T122 mekân atfı",
   "Konuşmada «yatak» hiç geçmiyor; kullanıcı «sabah uyanınca» dedi. Mekân "
   "uydurması, kullanıcının kendi zaman sözcüğüyle değiştirildi."),
}

# Karantina — revize EDİLMEZ, kriz sınırı (Kural 3)
KARANTINA = {
 ("v5-parti7", 31): (
   "Kullanıcı «bir şeyler var karaciğerde» ve «öleceğim ama içeceğim» diyor; "
   "cevap susma isteğine uyup bu cümleye hiç dokunmuyor. Eğitim örneği olarak "
   "öğrettiği şey: ölüme dair kayıtsızlık ifadesini geçip susma isteğini onurlandır. "
   "⛔ Bu cümleye NASIL karşılık verileceği kriz davranışı kararıdır ve uzman + "
   "etik kurul onayına bağlıdır (Kural 3); kaydı düzeltmek de o kararı vermek olurdu. "
   "⇒ Emsal: karantina #1 («Bitti benim işim zaten»).",
   "yuksek", ["Karaciğer bulgusu beyanı", "Ölüme kayıtsızlık ifadesi"]),
}

PARTI_GIRDI = {p: f"data/candidates/{p}.arinmis.jsonl" for p in
               ("v5-parti5", "v5-parti6", "v5-parti7", "v5-parti8")}


def main() -> int:
    kar_yol = KOK / "data/guvenlik-karantinasi.jsonl"
    kar = [json.loads(s) for s in kar_yol.read_text(encoding="utf-8").splitlines() if s.strip()]
    kar_id = {x["id"] for x in kar}
    hata = 0

    for parti, gir in PARTI_GIRDI.items():
        yol = KOK / gir
        kayitlar = [json.loads(s) for s in yol.read_text(encoding="utf-8").splitlines() if s.strip()]
        degisen = []
        for r in kayitlar:
            n = r["gen_meta"]["parti_sira"]
            anahtar = (parti, n)

            if anahtar in KARANTINA:
                gerekce, oncelik, esd = KARANTINA[anahtar]
                if r["id"] not in kar_id:
                    kar.append({"id": r["id"], "korpus": parti, "parti_sira": n,
                                "seed_id": (r.get("source_ids") or [None])[0],
                                "durum": "uzman_karari_bekliyor", "tarih": TARIH,
                                "esdurumlar": esd, "gerekce": gerekce, "oncelik": oncelik})
                    print(f"  ⛔ KARANTİNA {parti} #{n}")
                continue

            if anahtar not in D:
                continue
            eski, yeni, kural, gerekce = D[anahtar]
            son = [m for m in r["messages"] if m["role"] == "assistant" and m.get("content")][-1]
            if son["content"].count(eski) != 1:
                print(f"  ⛔ EŞLEŞME YOK/ÇOK {parti} #{n}: {son['content'].count(eski)} kez")
                hata += 1
                continue
            son["content"] = son["content"].replace(eski, yeni)
            r["judge"] = None                       # ⛔ eski puan yeni metni tarif etmez
            r["gen_meta"].setdefault("revizyon", []).append(
                {"tarih": TARIH, "kural": kural, "gerekce": gerekce,
                 "kaynak": "judge K1 + elle okuma"})
            degisen.append(n)

        cikti = KOK / f"data/candidates/{parti}.v3.jsonl"
        cikti.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in kayitlar),
                         encoding="utf-8")
        print(f"{parti}: {len(degisen)} kayıt revize {degisen} → {cikti.relative_to(KOK)}")

    kar_yol.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in kar),
                       encoding="utf-8")
    print(f"karantina: {len(kar)} kayıt → {kar_yol.relative_to(KOK)}")
    return 1 if hata else 0


if __name__ == "__main__":
    raise SystemExit(main())
