#!/usr/bin/env python3
"""thinking'deki TIRNAK İÇİ alıntılar konuşmada gerçekten geçiyor mu.

⛔⛔ **Neden var.** Modelin eğitim hedefi `thinking + completion`
(`configs/chat_template_train.jinja`: *«eğitim hedefi olan son turun thinking'i
korunmalı»*, `mask_prompt: true`). Ama:
  · judge rubriği thinking'i **kapsam dışı** tutuyor (K120 §3 — bilerek, sızıntıyı
    önlemek için) ⇒ uydurma bir thinking cümlesini **görmez**;
  · `checks.py` thinking'i yalnızca uzunluk ve DİL için okuyor;
  · §8b denetimi, şablon taraması, korpus raporu — hiçbiri thinking'in
    içeriğine bakmıyor.
⇒ thinking, **eğitilen ama denetlenmeyen** tek bölge.

⭐ Bu betik ucuz bir alt sınır ölçüyor: thinking `"..."` ya da `«...»` ile bir
şey alıntılıyorsa, o dizge konuşmanın herhangi bir turunda geçmeli.
Doğrulama `filter.alinti_nrm` ile yapılır — judge alıntılarında kullanılan
**aynı** işlev (tek türetme).

⚠️ **Vekil, kanıt değil:** tırnaksız uydurma iddiaları görmez (`#25`'in ilk
hâlindeki *«Otoparkta yanında kimse yoktu»* tırnaklıydı ve yakalanırdı, ama
*«Geçen hafta da yazmıştın»* tırnaksızdı ve yakalanmazdı). Alt sınır.

Kullanım: uv run python scripts/analiz/2026-09-16-thinking-alinti-denetimi.py <kayitlar.jsonl>
"""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import filter as f  # noqa: E402

TIRNAK = re.compile(r'"([^"\n]{4,})"|«([^»\n]{4,})»')

# ─── ELLE OKUNMUŞ SINIFLAR ────────────────────────────────────────────────
# ⛔ Ham "bulunamadı" sayısı KUSUR SAYISI DEĞİLDİR. Üç ayrı şey var ve
# ikisi meşru:
#   · `karsiolgusal` — thinking YAPMADIĞI hamleyi alıntılıyor (*«"Dayanıklısın"
#     gibi bir sıfat kullanırsam…»*). `uretim-v4` §4 bunu ZATEN İSTİYOR:
#     *«hangi hamle ve neden o hamle değil de bu»*. Kaynakta bulunmaması
#     tanım gereği.
#   · `parafraz` — kullanıcının sözü tırnak içinde ama çekim/sözcük farkıyla
#     (*«Grup biter»* ← *«o grup da biter gibi geliyo»*). Özensiz, uydurma değil.
#   · ⛔ `hayalet` — konuşmada karşılığı OLMAYAN bir şeyi kullanıcıya atfediyor.
#     KUSUR. Bu partide üçü de aynı mekanizmadan: tohum metni `bicim` bandına
#     KIRPILDI, thinking kırpılan parçaya atıf yapmayı sürdürdü.
SINIF = {
    ("karsiolgusal", 5): ["şöyle işler"], ("karsiolgusal", 8): ["hekimine söyle"],
    ("karsiolgusal", 9): ["neden", "Neden"],
    ("karsiolgusal", 11): ["Böyle bir şey düşünmemelisin"],
    ("karsiolgusal", 12): ["yapamam"], ("karsiolgusal", 17): ["Benim alanım değil"],
    ("karsiolgusal", 22): ["endişelenme"], ("karsiolgusal", 26): ["ama onlar gerçek değil"],
    ("karsiolgusal", 29): ["Dayanıklısın"], ("karsiolgusal", 36): ["Neden üç tane aldın"],
    ("karsiolgusal", 37): ["Suçlu hissediyorsun"],
    ("karsiolgusal", 42): ["Ne kaçırmış olurdun", "ne olur"],
    ("karsiolgusal", 51): ["Ne düşünüyorsun"], ("karsiolgusal", 52): ["Elimdeki metin ilgisiz"],
    ("karsiolgusal", 56): ["bebeğin için"],
    ("karsiolgusal", 57): ["Evet", "hayır", "Neden yalan söyledin"],
    ("karsiolgusal", 58): ["Sözünü tutmalısın"], ("karsiolgusal", 60): ["Üç kuşak"],
    ("parafraz", 4): ["tamamen bırakmadım", "eskisi gibi değilim", "yeterince ciddi miyim"],
    ("parafraz", 28): ["Grup biter"], ("parafraz", 30): ["istemekle yapabilmek arasındaki aralık"],
    ("parafraz", 31): ["Bir kupon tuttursam borçlar biter"], ("parafraz", 42): ["Bırakmak istiyorum ama"],
    ("parafraz", 44): ["Tuhaf rahatlama"], ("parafraz", 50): ["azaltmak istiyorum"],
}
_TERS = {(s, a): k for (k, s), lst in SINIF.items() for a in lst}

# ─── v5-parti3 elle okuması ───────────────────────────────────────────────
# ⭐ Aynı üç sınıf. 44 adayın 4'ü HAYALET çıktı (#18, #31, #41, #49) ve
# düzeltildi; ikisi (#41, #49) CEVABIN kendisindeydi, ikisi thinking'deydi.
# ⛔⛔ Dördü de aynı mekanizma: tohumdaki bir ayrıntı kullanıcı mesajı
# yazılırken düştü, cevap/thinking ona atıf yapmayı sürdürdü — yani §3a′
# bu oturumda YAZILDIĞI HÂLDE ihlal edildi ve yalnız bu kapı gördü.
SINIF_P3 = {
    "karsiolgusal": {
        8: ["Yanlış düşünüyorsun", "ikimiz de bilmiyoruz"],
        13: ["Nasıl bırakılır", "o an ne geçti"], 14: ["Paranoya mı bu"],
        15: ["Neden korktun"], 47: ["bu metin ilgisiz"], 49: ["bence yapabilirsin"],
        4: ["sana kim söyledi", "kimse", "Çıkarsam bırakmış olurum"],
        12: ["belki şaşırmıştır", "kötü niyetli değildir"],
        27: ["hekimine söyle", "Neden"], 53: ["azaltmak"], 3: ["Neden tutamıyorsun"],
        5: ["Bravo", "nasıl hissettin"], 16: ["Ne zamandır", "ne bu"],
        20: ["Bağımlı değilim"], 26: ["Harika bir şey yaptın"],
        30: ["Şans diye bir şey yok"], 34: ["haklı", "haksız"], 37: ["Alakası var"],
        39: ["bugün seni buna iten ne oldu"], 43: ["haklıydı", "haksızdı"],
        45: ["söylesen iyi olur"], 54: ["Nasıl başardın"],
    },
    "parafraz": {
        13: ["nereden başlanır"], 28: ["mükemmeliyetçisin, büyütüyorsun"],
        47: ["yine yaktım"], 49: ["formda da öyle geçiyordur, değil mi"],
        50: ["Haklı görünmek istemiyorum"], 57: ["ne istiyorsanız söyleyin, bitirelim"],
        9: ["Bırakmayı düşünmüyorum"], 17: ["Şablon mesajdır"],
    },
}
for _k, _d in SINIF_P3.items():
    for _s, _lst in _d.items():
        for _a in _lst:
            _TERS.setdefault((_s, _a), _k)

# ⛔ Elle okuma YALNIZCA bu korpus için yapıldı. Başka bir dosyada koşarsa
# sınıflandırılmamış her öge `hayalet` sayılırdı ve betik 23 yalancı bulgu
# üretirdi (parti1'de bire bir yaşandı). ⇒ Kapsam AÇIKÇA ilan ediliyor:
# kapsam dışı ögeler `siniflanmadi` olur ve çıkış kodunu düşürmez.
ELLE_OKUNAN_KORPUS = {"v4-parti2.v2", "v5-parti3"}


def sinifla(sira: int, alinti: str, korpus: str) -> str:
    if korpus not in ELLE_OKUNAN_KORPUS:
        return "siniflanmadi"
    return _TERS.get((sira, alinti), "hayalet")


def main(yol: str) -> int:
    p = Path(yol) if Path(yol).is_absolute() else KOK / yol
    kayitlar = [json.loads(s) for s in p.read_text(encoding="utf-8").splitlines() if s.strip()]
    bulgular, tarama = [], 0
    for r in kayitlar:
        asst = [m for m in r["messages"] if m["role"] == "assistant"][-1]
        th = asst.get("thinking") or ""
        if not th:
            continue
        # Kaynak: konuşmanın TAMAMI (kullanıcı + asistan turları + bağlam).
        kaynak = f.alinti_nrm(" \n ".join(
            [m.get("content", "") for m in r["messages"] if m["role"] != "system"]
            + [c.get("metin", "") for c in (r.get("context") or [])]))
        for m in TIRNAK.finditer(th):
            alinti = (m.group(1) or m.group(2)).strip()
            tarama += 1
            if f.alinti_nrm(alinti) not in kaynak:
                sira = r["gen_meta"]["parti_sira"]
                bulgular.append({"parti_sira": sira, "id": r["id"][:16],
                                 "alinti": alinti,
                                 "sinif": sinifla(sira, alinti, p.stem)})
    ozet = {"tarih": "2026-09-16", "girdi": str(p.relative_to(KOK)),
            "girdi_sha256_16": hashlib.sha256(p.read_bytes()).hexdigest()[:16],
            "kayit": len(kayitlar), "taranan_alinti": tarama,
            "bulunamayan": bulgular,
            "sinif_dagilimi": {k: sum(1 for b in bulgular if b["sinif"] == k)
                               for k in ("karsiolgusal", "parafraz", "hayalet",
                                         "siniflanmadi")},
            "elle_okunan_korpus": sorted(ELLE_OKUNAN_KORPUS)}
    cikti = KOK / f"reports/analiz/2026-09-16-thinking-alinti-{p.stem}.json"
    cikti.write_text(json.dumps(ozet, ensure_ascii=False, indent=2), encoding="utf-8")
    hayalet = [b for b in bulgular if b["sinif"] == "hayalet"]
    print(f"{len(kayitlar)} kayıt · {tarama} tırnaklı alıntı · "
          f"kaynakta bulunamayan {len(bulgular)}")
    print(f"  sınıf: {ozet['sinif_dagilimi']}")
    if ozet["sinif_dagilimi"]["siniflanmadi"]:
        print(f"  ⚠️ bu korpus ELLE OKUNMADI ({ELLE_OKUNAN_KORPUS} için okundu) — "
              f"{ozet['sinif_dagilimi']['siniflanmadi']} öge sınıflanmadı, "
              f"hiçbiri kusur SAYILMADI")
    for b in hayalet:
        print(f"  ⛔ HAYALET #{b['parti_sira']:>2} «{b['alinti'][:70]}»")
    print(f"→ {cikti.relative_to(KOK)}")
    return 1 if hayalet else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "data/candidates/v4-parti2.v2.jsonl"))
