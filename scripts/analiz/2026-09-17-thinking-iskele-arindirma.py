#!/usr/bin/env python3
"""`thinking` alanından ÜRETİM İSKELESİNİ ayıklar; akıl yürütmeyi bırakır.

⛔⛔ **Neden var (T120).** `thinking:completion` oranının partiler boyunca
düştüğü fark edildi (1.62 → 1.16) ve sebebi arandığında iki ayrı kayma çıktı:
thinking kısalıyor (77 → 64 kelime) VE completion büyüyor (46 → 56). Kısalmanın
sebebi ise çok daha ciddi bir şeydi: thinking'in içeriği **akıl yürütmeden
üretim muhasebesine** kaymış.

| korpus | iskele ifadesi içeren kayıt |
|---|---|
| `v4-parti1` | **%0** |
| `v5-parti3` | %7 |
| `v5-parti4` | %55 |
| `v5-parti6` | %92 |
| `v5-parti7` / `v5-parti8` | **%100** |

⇒ Kayıt başına iskele ifadesi **0.1 → 3.3**.

➡️⭐⭐ *Kararlarımı denetlenebilir kılan disiplin, eğitim verisine dağıtılmış
modelde KARŞILIĞI OLMAYAN bir iskeleyi yazdırdı: «ızgara», «§5a″ md.1», «kota»,
«parti8 #52 ile aynı karar». Model çıkarımda ne ızgara görür ne §5a″ okur;
bunları öğrenmek, var olmayan bir belgeye atıf yapmayı öğrenmektir.
Denetlenebilirlik ile eğitilebilirlik burada ters yöne çekti ve ben yalnız
birini ölçüyordum.*

⭐ **Ayrılabilirlik ÖLÇÜLDÜ:** iskele taşıyan 483 paragrafın **460'ı** (%95)
paragrafın başında duruyor ⇒ satır olarak ayrılabilir. **23'ü** cümleye gömülü
ve elle yeniden yazılmalı; bu betik onları ayıklamaz, **listeler**.

⛔ Orijinal dosyalar DEĞİŞTİRİLMEZ (Kural 7): çıktı yeni sürüm dosyalarına yazılır.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
ISKELE = re.compile(r"[Iİ]zgara|ızgara|§\s?\d|md\.[1-4]|parti\d|T\d{2,3}|"
                    r"Kural \d|K\d{2,3}\b|kota(sı|lı|da)?\b|ölçüt")
# ⚠️ Paragrafın İLK 40 karakterinde iskele varsa ya da paragraf bir uyarı
# imiyle başlıyorsa, o paragraf muhasebe satırıdır ve ayrılabilir.
def _iskele_paragrafi(par: str) -> bool:
    if not ISKELE.search(par):
        return False
    return bool(ISKELE.search(par.strip()[:40])) or par.strip().startswith(("⛔", "⚠️"))


# ⭐ CÜMLEYE GÖMÜLÜ 23 öge elle okundu ve hepsi AYNI BİÇİMDE bozuk çıktı:
# gerçek akıl yürütme + sonuna eklenmiş bir iskele yan cümlesi. Yan cümleler
# burada listeleniyor ki arındırma yeniden üretilebilir olsun ve neyin
# çıkarıldığı tek tek okunabilsin.
GOMULU_DUZELTME = [
    ("; sorulmuş bir soruyu savuşturmak §5b'nin eleştirdiği hamle.",
     "; sorulmuş bir soruyu savuşturmak, cevap vermekten daha kötüdür."),
    ("Dayatmıyorum, izin istiyorum — K19'un asıl kapsamı bu.",
     "Dayatmıyorum, izin istiyorum."),
    ("Takdir de etmiyorum — ızgara takdir istiyor ve takdiri tarif edebilmesine bağlıyorum, yaptığı şeye değil.",
     "Takdiri sonuca değil, tarif edebilmesine bağlıyorum."),
    ("ama yönlendirme koymuyorum — ızgara `yok` diyor ve tür+adım vermeden reddetmek mümkün.",
     "ama yönlendirme koymuyorum; tür ve adım vermeden reddetmek mümkün."),
    ("Izgara bu kayda yönlendirme yasağı koymuştu; güvenlik ekseni o kotaya tabi olamaz.",
     "Yönlendirme koymam beklenmiyordu ama burada susmak görmezden gelmek olur."),
    ("Kararı ona bırakan cümleyi koyuyorum; ızgara özerklik istiyor ve burada tam yerinde.",
     "Kararı ona bırakan cümleyi koyuyorum; burada tam yerinde."),
    ("Kararı ona bırakan cümleyi koyuyorum — ızgara özerklik istiyor ve bu yaşta en çok gereken şey o.",
     "Kararı ona bırakan cümleyi koyuyorum; bu yaşta en çok gereken şey o."),
    ("Söyleyip söylememeyi ona bırakıyorum — ızgara özerklik istemiyor ama karar zaten onun ve ben oraya karışmam.",
     "Söyleyip söylememeyi ona bırakıyorum; karar zaten onun ve ben oraya karışmam."),
    ("ama görmezden de gelemem; ızgaranın yönlendirme yasağı burada geçersiz.",
     "ama görmezden de gelemem; burada susmak sessizce onaylamak olur."),
    ("— K18 rakamı ve kurum künyesini yasaklıyor, kullanıcı andı diye ben tekrarlamıyorum.",
     "; kullanıcı andı diye benim tekrarlamam gerekmiyor."),
    ("tam olarak T13'ün uydurma davranışı olurdu.", "tam olarak uydurma olurdu."),
    ("kurumun adını, numarasını vermiyorum (K18) — zaten metinde de yok.",
     "kurumun adını, numarasını vermiyorum — zaten metinde de yok."),
    ("Kural 3: klinik içerik uydurulmaz ve burada en kolay hata",
     "Klinik bir şey uydurmak yasak ve burada en kolay hata"),
    ("ben büyütmüyorum (T104: mekân da kırpma kusurunun bir üyesi).",
     "ben büyütmüyorum."),
    ("§8b'nin istediği tam olarak bu.", "Reddin işe yarar hâli bu."),
    ("Aynı hamle parti5 #18'de de işe yaramıştı ve rakama hiç dokunmuyor.",
     "Rakama hiç dokunmuyor."),
    ("hafızanın asimetrisi (parti7 #44 ile aynı aile):", "hafızanın asimetrisi:"),
    ("⛔ Kurum künyesi yok (K18).", "Kurum künyesi yok."),
    ("«bir tek bu kalmış» yokluk anlatıyor (parti8 #15 ile aynı aile).",
     "«bir tek bu kalmış» yokluk anlatıyor."),
    ("ona ait olmayan bir hükmü ona atfetmemek için — T104'ün tersten hâli.",
     "ona ait olmayan bir hükmü ona atfetmemek için."),
    ("eşanlamlı bir terimle anmaktan farklı bir şey (T109).",
     "eşanlamlı bir terimle anmaktan farklı bir şey."),
]
# ⛔ Üretim TARİHÇESİ notları (*«ilk yazımda … kapı yakaladı»*) tamamen atılır:
# bunlar korpusun nasıl üretildiğini anlatıyor, konuşmada geçen bir şeyi değil.
TARIHCE = re.compile(r"\s*⛔+ (Ama )?İLK YAZIMDA[^.]*\.(\s*[^.]*kapı yakaladı[^.]*\.)?", re.I)


def main(argv: list[str]) -> int:
    # ⛔⛔ VARSAYILAN LİSTE SÜPERSE EDİLMİŞ SÜRÜMÜ KULLANIYORDU. `v5-parti4`'ün
    # T115 düzeltmesi `v5-parti4.v2`'ye yazılmıştı; liste `v5-parti4` dediği için
    # arındırma DÜZELTİLMEMİŞ hâli aldı ve düzeltme sessizce kayboldu.
    # Judge bunu bağımsız olarak yakaladı (#2 → `riski_atlama`) — yani kusuru
    # gösteren şey bir kapı değil, kör bir okuyucu oldu.
    # ➡️ *Bir dosya adı listesi, hangi sürümün geçerli olduğunu bilmez;
    #    süperse edilmiş sürümler ADLARIYLA değil, AÇIKÇA elenmelidir.*
    hedef = argv or ["v5-parti4.v2", "v5-parti5", "v5-parti6", "v5-parti7", "v5-parti8"]
    gomulu, toplam_at, bos = [], 0, []
    for ad in hedef:
        gi = KOK / f"data/candidates/{ad}.jsonl"
        if not gi.exists():
            print(f"⛔ yok: {gi}"); return 1
        out = []
        for s in gi.read_text(encoding="utf-8").splitlines():
            if not s.strip():
                continue
            r = json.loads(s)
            for m in r["messages"]:
                if m.get("role") != "assistant" or not m.get("thinking"):
                    continue
                parcalar = [p for p in m["thinking"].split("\n\n") if p.strip()]
                tutulan = []
                for par in parcalar:
                    if _iskele_paragrafi(par):
                        toplam_at += 1
                        continue
                    for _e, _y in GOMULU_DUZELTME:
                        par = par.replace(_e, _y)
                    par = TARIHCE.sub("", par).strip()
                    if not par:
                        toplam_at += 1
                        continue
                    if ISKELE.search(par):
                        gomulu.append({"korpus": ad,
                                       "sira": r["gen_meta"]["parti_sira"],
                                       "paragraf": par.strip()})
                    tutulan.append(par)
                if not tutulan:
                    bos.append((ad, r["gen_meta"]["parti_sira"]))
                    tutulan = parcalar          # ⛔ hiç akıl yürütme kalmıyorsa DOKUNMA
                m["thinking"] = "\n\n".join(tutulan)
            out.append(json.dumps(r, ensure_ascii=False))
        ci = KOK / f"data/candidates/{ad}.arinmis.jsonl"
        ci.write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"→ {ci.relative_to(KOK)} ({len(out)} kayıt)")
    ozet = {"tarih": "2026-09-17",
            "betik": "scripts/analiz/2026-09-17-thinking-iskele-arindirma.py",
            "atilan_paragraf": toplam_at,
            "gomulu_kalan": len(gomulu),
            "thinking_tamamen_iskele_olan": bos,
            "gomulu": gomulu}
    (KOK / "reports/analiz/2026-09-17-thinking-iskele-arindirma.json").write_text(
        json.dumps(ozet, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n⭐ atılan iskele paragrafı: {toplam_at}")
    print(f"⛔ CÜMLEYE GÖMÜLÜ kalan (elle yazılmalı): {len(gomulu)}")
    print(f"⛔⛔ thinking'i TAMAMEN iskele olan kayıt: {len(bos)} {bos if bos else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
