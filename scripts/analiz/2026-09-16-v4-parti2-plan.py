#!/usr/bin/env python3
"""v4-parti2 tasarım ızgarası — 60 kayıt. Üretimden ÖNCE yazılır, sonra dondurulur.

⭐ Havuz, hariç tutma ve tohum seçme mantığı `2026-09-15-v4-parti1-plan.py`'den
**ÇAĞRILIYOR** — kopyalanmıyor. Değişen tek şey ızgara ve kotalar.

⭐⭐ **§8b payı bilerek artırıldı: 10/40 (%25) → 20/60 (%33).** Gerekçe ölçülü:
K109 kolların neden elendiğini *«sebep config değil korpus»* diye ölçtü —
`datasets/v0.0.2`'de yönlendirme davranışı yoktu. K112'de v0.0.3'ün 155 kaydının
**5'inde** yönlendirme hamlesi var (%3,2). §8b'nin ilan edilen kotası ~%19
(6+8+5) ve o bir **korpus** hedefi, parti hedefi değil. Aritmetik:

    bugün      5 / 155  = %3,2
    parti2 ile 25 / 215 = %11,6      ⇒ hedefe doğru ÖLÇÜLÜ bir adım
    %19 için   41 / 215                ⇒ ⛔ bir parti daha gerekir

⚠️ Partiyi %19'a çekmek 36/60 (%60) §8b demekti ve öteki bütün eksenleri
bozardı. ⇒ *Korpus hedefi parti hedefine eşit değildir; ikisini karıştırmak
ya hedefi ıskalar ya partiyi bozar.*

⛔ **KRİZ DİLİMİ BU PARTİDE YOK** — etik kurul + uzman onayı bekliyor (Kural 3).
Hariç tutma `parti1`'in `KRIZ_ANAHTAR` deseniyle yapılıyor.

⛔ §8b'nin 20 tohumu **ELLE** seçildi: parti1'in dersi, otomatik seçicinin bu
dilimde isabetsiz olması (alt-dizge eşleşmesi, K65/T27 ailesi). Her satırın
gerekçesi yazılı ve denetlenebilir.

Kullanım: uv run python scripts/analiz/2026-09-16-v4-parti2-plan.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "data/plan/v4-parti2.jsonl"
_sp = _iu.spec_from_file_location("p1", KOK / "scripts/analiz/2026-09-15-v4-parti1-plan.py")
P1 = _iu.module_from_spec(_sp)
sys.argv = [sys.argv[0]]
_sp.loader.exec_module(P1)          # ⭐ havuz/hariç tutma/seçici ORADAN

# a=sinir_tipi b=bicim r=register k=konusma_durumu t=turn_ending m=mi_process
# ç=turn_type n=is_negative ö=özerklik c=context tür/yaş/motivasyon havuz
G = [
 # ── §8b dilimi: 20 kayıt (tohumlar ELLE, aşağıda) ──
 (1,"yonlendirme_istegi","orta","duzgun","merak_sorusu","acik_uclu_soru","engaging","single",0,1,0,"tutun","yetiskin","ic",None),
 (2,"yonlendirme_istegi","orta","duzgun","tetikleyici_an","acik_uclu_soru","engaging","single",0,1,0,"tutun","yetiskin","ic",None),
 (3,"yonlendirme_istegi","kisa","bozuk","suregiden_durum","acik_uclu_soru","engaging","multi",0,0,0,"tutun","yetiskin","ic",None),
 (4,"yonlendirme_istegi","uzun","duzgun","merak_sorusu","yalnizca_yansitma","focusing","single",0,0,0,"tutun","yetiskin","ic",None),
 (5,"yonlendirme_istegi","uzun","duzgun","suregiden_durum","acik_uclu_soru","engaging","single",0,0,0,"alkol","yetiskin","yasal_zorunluluk",None),
 (6,"rol_siniri_yonlendirme","orta","duzgun","plan_yapma","acik_uclu_soru","focusing","single",1,1,0,"alkol","yetiskin","ic",None),
 (7,"rol_siniri_yonlendirme","kisa","duzgun","merak_sorusu","acik_uclu_soru","engaging","single",1,0,0,"receteli_ilac","yetiskin","ic",None),
 (8,"rol_siniri_yonlendirme","kisa","duzgun","tetikleyici_an","yalnizca_yansitma","engaging","single",1,0,0,"receteli_ilac","yetiskin","ic",None),
 (9,"rol_siniri_yonlendirme","kisa","duzgun","suregiden_durum","acik_uclu_soru","evoking","single",0,0,0,"receteli_ilac","yetiskin","ic",None),
 (10,"rol_siniri_yonlendirme","orta","bozuk","tetikleyici_an","acik_uclu_soru","engaging","multi",0,0,0,"kumar","yetiskin","ic",None),
 (11,"rol_siniri_yonlendirme","uzun","duzgun","tetikleyici_an","acik_uclu_soru","engaging","single",1,1,0,"alkol","yetiskin","yasal_zorunluluk",None),
 (12,"rol_siniri_yonlendirme","uzun","duzgun","plan_yapma","acik_uclu_soru","focusing","single",1,1,0,"tutun","yetiskin","ic",None),
 (13,"yonlendirme_gereksiz","uzun","duzgun","suregiden_durum","yalnizca_yansitma","engaging","single",0,0,0,"tutun","yetiskin","ic",None),
 (14,"yonlendirme_gereksiz","orta","duzgun","tetikleyici_an","yalnizca_yansitma","engaging","single",0,0,0,"alkol","yetiskin","ic",None),
 (15,"yonlendirme_gereksiz","uzun","duzgun","plan_yapma","acik_uclu_soru","planning","single",0,0,0,"kumar","yetiskin","ic",None),
 (16,"yonlendirme_gereksiz","kisa","duzgun","suregiden_durum","acik_uclu_soru","engaging","multi",0,0,0,"dijital","yetiskin","ic",None),
 (17,"sinir_cekme","kisa","bozuk","merak_sorusu","acik_uclu_soru","engaging","multi",0,0,0,"tutun","yetiskin","ic",None),
 (18,"sinir_cekme","orta","duzgun","tetikleyici_an","yalnizca_yansitma","engaging","single",1,0,0,"tutun","yetiskin","ic",None),
 (19,"sinir_cekme","orta","duzgun","suregiden_durum","acik_uclu_soru","engaging","single",0,1,0,"alkol","ergen","aile_baskisi",None),
 (20,"sinir_cekme","orta","bozuk","merak_sorusu","acik_uclu_soru","engaging","multi",0,0,0,"tutun","yetiskin","ic",None),
 # ── kısa açılış bloğu (§3a %40 · §3c çoğu çok turlu) ──
 (21,"yok","kisa","bozuk","tetikleyici_an","acik_uclu_soru","engaging","multi",0,0,0,"alkol","yetiskin","ic",None),
 (22,"yok","kisa","bozuk","tetikleyici_an","acik_uclu_soru","evoking","multi",0,0,0,"tutun","ergen","ic",None),
 (23,"yok","kisa","bozuk","tetikleyici_an","yalnizca_yansitma","engaging","multi",0,0,0,"kumar","yetiskin","ic",None),
 (24,"yok","kisa","bozuk","suregiden_durum","durur","focusing","multi",0,0,0,"alkol","yetiskin","ic",None),
 (25,"yok","kisa","bozuk","iyi_giden_paylasim","takdir","engaging","multi",0,1,0,"tutun","yetiskin","ic",None),
 (26,"yok","kisa","bozuk","aradan_donus","durur","evoking","multi",0,0,0,"dijital","ergen","ic",None),
 (27,"yok","kisa","bozuk","tetikleyici_an","ozet","engaging","multi",0,0,0,"tutun","yetiskin","ic",None),
 (28,"yok","kisa","bozuk","plan_yapma","acik_uclu_soru","planning","multi",0,0,0,"kumar","yetiskin","ic",None),
 (29,"yok","kisa","bozuk","iyi_giden_paylasim","takdir","evoking","multi",0,1,0,"alkol","yetiskin","ic",None),
 (30,"yok","kisa","bozuk","suregiden_durum","ozet","focusing","multi",0,0,0,"tutun","yetiskin","ic",None),
 (31,"yok","kisa","bozuk","tetikleyici_an","takdir","evoking","multi",0,0,0,"kumar","yetiskin","ic",None),
 (32,"yok","kisa","duzgun","tetikleyici_an","ozet","evoking","multi",0,0,0,"alkol","yetiskin","ic",None),
 (33,"yok","kisa","duzgun","iyi_giden_paylasim","takdir","engaging","multi",0,0,0,"tutun","yetiskin","ic",None),
 (34,"yok","kisa","duzgun","merak_sorusu","yalnizca_yansitma","focusing","multi",0,0,0,"alkol","yetiskin","ic",None),
 (35,"yok","kisa","duzgun","plan_yapma","acik_uclu_soru","planning","multi",0,0,0,"tutun","yetiskin","ic",None),
 (36,"yok","kisa","duzgun","tetikleyici_an","acik_uclu_soru","evoking","multi",0,0,0,"receteli_ilac","yetiskin","ic",None),
 (37,"yok","kisa","duzgun","aradan_donus","ozet","focusing","single",0,0,0,"kumar","yetiskin","ic",None),
 (38,"yok","kisa","duzgun","iyi_giden_paylasim","takdir","evoking","single",0,0,0,"alkol","yetiskin","ic",None),
 # ── orta blok ──
 (39,"yok","orta","duzgun","tetikleyici_an","acik_uclu_soru","evoking","single",0,0,0,"kumar","yetiskin","ic",None),
 (40,"yok","orta","duzgun","suregiden_durum","acik_uclu_soru","focusing","multi",0,0,1,"alkol","yetiskin","ic",None),
 (41,"yok","orta","duzgun","iyi_giden_paylasim","takdir","evoking","single",0,0,0,"tutun","yetiskin","ic",None),
 (42,"yok","orta","duzgun","plan_yapma","acik_uclu_soru","planning","single",0,0,0,"receteli_ilac","yetiskin","ic",None),
 (43,"yok","orta","duzgun","tetikleyici_an","takdir","engaging","single",0,0,1,"tutun","yetiskin","ic",None),
 (44,"yok","orta","duzgun","iyi_giden_paylasim","ozet","evoking","single",0,0,0,"kumar","yetiskin","yasal_zorunluluk",None),
 (45,"yok","orta","duzgun","tetikleyici_an","acik_uclu_soru","planning","multi",0,0,0,"alkol","yetiskin","ic",None),
 (46,"yok","orta","duzgun","tetikleyici_an","yalnizca_yansitma","focusing","single",0,0,0,"dijital","ergen","aile_baskisi",None),
 (47,"yok","orta","duzgun","iyi_giden_paylasim","takdir","focusing","single",1,0,0,"tutun","yetiskin","ic",None),
 (48,"yok","orta","duzgun","tetikleyici_an","ozet","evoking","single",0,0,0,"alkol","ergen","ic",None),
 (49,"yok","orta","duzgun","plan_yapma","ozet","planning","single",0,1,0,"tutun","yetiskin","ic",None),
 (50,"yok","orta","duzgun","suregiden_durum","acik_uclu_soru","engaging","single",1,0,1,"receteli_ilac","yetiskin","ic",None),
 (51,"yok","orta","duzgun","tetikleyici_an","acik_uclu_soru","planning","single",0,1,0,"kumar","yetiskin","ic",None),
 # ── uzun blok ──
 (52,"yok","uzun","duzgun","suregiden_durum","acik_uclu_soru","evoking","single",0,0,1,"alkol","yetiskin","ic",None),
 (53,"yok","uzun","duzgun","tetikleyici_an","ozet","evoking","single",0,0,0,"kumar","yetiskin","ic",None),
 (54,"yok","uzun","duzgun","iyi_giden_paylasim","takdir","engaging","single",0,1,0,"tutun","yetiskin","ic",None),
 (55,"yok","uzun","duzgun","plan_yapma","acik_uclu_soru","planning","multi",0,0,1,"receteli_ilac","yetiskin","ic",None),
 (56,"yok","uzun","duzgun","aradan_donus","ozet","focusing","single",0,0,0,"tutun","yetiskin","ic",None),
 (57,"yok","uzun","duzgun","tetikleyici_an","acik_uclu_soru","evoking","single",1,0,0,"kumar","yetiskin","yasal_zorunluluk",None),
 (58,"yok","uzun","duzgun","iyi_giden_paylasim","durur","engaging","single",0,0,0,"alkol","yetiskin","ic",None),
 (59,"yok","uzun","duzgun","plan_yapma","acik_uclu_soru","planning","single",0,1,1,"tutun","yetiskin","yasal_zorunluluk",None),
 (60,"yok","uzun","duzgun","suregiden_durum","yalnizca_yansitma","focusing","single",0,0,0,"alkol","yetiskin","ic",None),
]

# ─── §8b satırlarının tohumları ELLE seçildi (parti1'in dersi) ───
TOHUM_ELLE = {
 1: ("1110b1eb8f7f994a", "«nereden başlayacağımı bilmiyorum» + üç gündür randevu alamıyor — yönlendirmeyi AÇIKÇA istiyor, kriz yok"),
 2: ("cc539e9c928ccd56", "doktor erken tıkanıklık dedi; «bu sefer kendim için» + «nereden başlayacağımı bilmiyorum»"),
 3: ("3157a875fbcd21c2", "«bir şeyler yapmak istiyorum ama nereden başlayacağımı bilmiyorum» — kendi sözüne güven kaybı"),
 4: ("ad6731943592779e", "⭐ kampüs danışma merkezi biliyor ama «hak edecek kadar ciddi miyim» — EŞİK endişesi, yönlendirmenin farklı bir yüzü"),
 5: ("abb8cf505517dded", "denetimli serbestlik + zorunlu terapi; süreci uzaktan izliyor — yönlendirme kurumsal, kriz yok"),
 6: ("ebe42acbef8090dd", "⛔⛔ «bana bir program yaz: üçten ikiye, sonra bire» + antidepresan kullanıyor — BIRAKMA PROTOKOLÜ, sert rol sınırı"),
 7: ("1bd574501e7279cc", "⛔ «günde kaç tane azaltayım, yarım mı içeyim» — DOZ kararı"),
 8: ("c45d179d616d1764", "⛔ doz azaltma sonrası kramp/terleme; «yanlış bir şey mi yaptım» — yoksunluk belirtisi YORUMU"),
 9: ("37f92465bb97ce3a", "⛔ «bağımlı mı oldum» — TANI sorusu, kendi kendine yanıtlamaya da çalışıyor"),
 10: ("43702a997acd944f", "⛔ «bağımlı mıyım gerçekten?» + 110 bin borç — tanı sorusu, kumar"),
 11: ("721ef770677b652b", "⛔⛔ «testi etkileyecek bir yöntem var mı» — HEM hukuki HEM test manipülasyonu; en sert vaka"),
 12: ("3164236c4f0b7ff7", "⛔ reçetesiz vareniklin almış, «doktora gitmeden nasıl kullanırım … ne yapmalıyım sence»"),
 13: ("c4fd4462be1af107", "«söyleyebileceğim kimse yok» — yalnızlık ifadesi, TALEP yok; yönlendirme gereksiz"),
 14: ("c37d51743f522b36", "⭐ «Bana ne diyorsa söyleme, sadece dinle» — talebi AÇIKÇA reddediyor"),
 15: ("26e268540eb0a8f9", "⭐ terapisti ZATEN GA'ya yönlendirmiş; koruma katmanları kurulu — model kurumu tekrar önermemeli"),
 16: ("202af3867aefae3b", "«Destek alıyorum» — zaten destekte; 11 kelime, kısa açılış"),
 17: ("75baff2bca903a7e", "«hanıma ne diyeyim de susturayım» — model eş çatışmasında TARAF olamaz"),
 18: ("e9f344fe074ca553", "eşi defteri gösterip «sen söyle» demiş; kullanıcı da modelden aynısını istiyor — hüküm verme talebi"),
 19: ("ec0683e24409ebdf", "ergen: «babana sen söyle» + «bu yük benim mi sence» — aile içi arabuluculuk talebi"),
 20: ("39c2782f7fd80649", "«sen ne dersin bu işe» — model yerine karar verme talebi; bozuk register"),
}

ALANLAR = P1.ALANLAR
HEDEF = {
 "bicim":          {"kisa": 24, "orta": 21, "uzun": 15},
 "register":       {"bozuk": 15, "duzgun": 45},
 # ⚠️ Hedefler parti1'in (40) kotalarının ×1,5 ölçeklenmişi — toplamları 60 ETMELİ.
 # ⛔ İlk yazımda üç eksende toplam 60 tutmuyordu (57, 56, 57) ve assert yakaladı:
 #    hata ızgarada değil HEDEFTEYDİ. *Bir kota tablosu, kendi toplamını sınamıyorsa
 #    ızgarayı değil kendini ölçer.*
 "konusma_durumu": {"tetikleyici_an": 21, "suregiden_durum": 12, "iyi_giden_paylasim": 9,
                    "plan_yapma": 9, "merak_sorusu": 6, "aradan_donus": 3},
 "turn_ending":    {"acik_uclu_soru": 30, "takdir": 9, "ozet": 9,
                    "yalnizca_yansitma": 9, "durur": 3},
 "mi_process":     {"engaging": 24, "focusing": 12, "evoking": 15, "planning": 9},
 "turn_type":      {"multi": 24, "single": 36},
 "sinir_tipi":     {"yonlendirme_istegi": 5, "rol_siniri_yonlendirme": 7,
                    "yonlendirme_gereksiz": 4, "sinir_cekme": 4, "yok": 40},
}
HEDEF_SAYI = {"is_negative": 9, "ozerklik": 12, "context": 6}


def main() -> None:
    izgara = [dict(zip(ALANLAR, s)) for s in G]
    assert len(izgara) == 60, f"ızgara {len(izgara)} satır, 60 bekleniyor"
    hata = []
    for alan, hedef in HEDEF.items():
        if sum(hedef.values()) != 60:
            hata.append(f"  ⛔ HEDEF TABLOSU bozuk: {alan} toplamı {sum(hedef.values())} ≠ 60")
        c = dict(sorted(Counter(s[alan] for s in izgara).items()))
        if c != dict(sorted(hedef.items())):
            hata.append(f"  {alan}:\n     ızgara {c}\n     hedef  {dict(sorted(hedef.items()))}")
    for alan, hedef in HEDEF_SAYI.items():
        n = sum(s[alan] for s in izgara)
        if n != hedef:
            hata.append(f"  {alan}: ızgara {n} ≠ hedef {hedef}")
    if hata:
        raise SystemExit("⛔ kota tutmuyor:\n" + "\n".join(hata))

    hav = P1.havuz()
    hav_kimlik = {t["seed_id"]: t for t in hav}
    alinmis: set[str] = set()
    eksik = []
    for s in izgara:
        if s["sira"] in TOHUM_ELLE:
            sid, gerekce = TOHUM_ELLE[s["sira"]]
            t = hav_kimlik.get(sid)
            if t is None:
                raise SystemExit(f"⛔ elle seçilen tohum havuzda yok: satır {s['sira']} {sid}")
            s["tohum_gerekce"] = gerekce
        else:
            t = P1.sec(s, hav, alinmis)
        if t is None:
            eksik.append(s["sira"])
            continue
        alinmis.add(t["seed_id"])
        s["seed_id"] = t["seed_id"]
        s["source_id"] = t["source_id"]
        s["tohum_senaryo"] = t["meta"].get("senaryo")
        s["tohum_kelime"] = len(t["user_message"].split())
        s["tohum_metin"] = t["user_message"]
    if eksik:
        raise SystemExit(f"⛔ tohum bulunamayan satırlar: {eksik}")

    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    with open(CIKTI, "w", encoding="utf-8") as f:
        for s in izgara:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"\n✅ kotalar tuttu · {len(izgara)} satır → {CIKTI.relative_to(KOK)}")
    print("bağımlılık türü:", dict(Counter(s["tur"] for s in izgara)))
    print("yaş:", dict(Counter(s["yas"] for s in izgara)))
    print("§8b:", dict(Counter(s["sinir_tipi"] for s in izgara if s["sinir_tipi"] != "yok")))


if __name__ == "__main__":
    main()
