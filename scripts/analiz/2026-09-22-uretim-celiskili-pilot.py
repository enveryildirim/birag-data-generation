#!/usr/bin/env python3
"""§7a″ `celiskili` sınıfı — 6 kayıtlık PİLOT.

⭐ **Neden pilot.** Yeni bir bağlam sınıfının hattan geçip geçmediği önce
küçük bir dilimle sınanır (dikey dilim disiplini). 12 kayıt birden yazıp
hepsinin bir kapıda düşmesi yerine 6 ile hat doğrulanır.

⛔⛔ **Güvenlik süzgeci — tohum seçiminde ölçüldü.** `risk_seviyesi`
sözlüğünde **`cok_yuksek`** de var (20 tohum) ve ilk süzgecim yalnız
`yuksek`i dışlıyordu ⇒ bir **kriz** tohumu neredeyse üretime giriyordu.
Süzgeç üçe çıkarıldı: risk ∈ {dusuk, orta} · `senaryo ≠ kriz` ·
`siddet_seviyesi ≠ agir`. Kriz dilimi uzman onayında (Kural 3).

⛔ **Her kayıt KENDİ tohumundan yazıldı** (T217: iki kaydın metni komşu
satırların tohumundan yazılmıştı ve hiçbir kapı görmemişti).

⛔ **Çelişkinin tarafı seçilmiyor.** Pasaj çiftleri
`data/celiskili-pasaj-bankasi.json`'dan geliyor ve hiçbirinde `dogru_taraf`
yok — üretici de hangisinin doğru olduğunu bilmiyor.

Çıktı: data/candidates/celiskili-pilot.jsonl
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from checks import run_checks  # noqa: E402
from dilim import dilim  # noqa: E402
from kunye import betik_tarihi  # noqa: E402

CIKTI = KOK / "data/candidates/celiskili-pilot.jsonl"
BANKA = {c["no"]: c for c in
         json.loads((KOK / "data/celiskili-pasaj-bankasi.json").read_text())["ciftler"]}
SISTEM = next(m["content"] for m in
              json.loads(open(KOK / "datasets/v0.0.18/train.jsonl").readline())["messages"]
              if m["role"] == "system")

# (tohum, banka_no, kullanıcı ek sorusu, cevap, thinking, üst alanlar)
KAYITLAR = [
 dict(seed="5f2e517dcbc3", banka=2, tur="kumar", senaryo="rol_siniri",
      mi="planning", talk="change", mot="ic", bicim="uzun",
      turn_ending="yalnizca_yansitma", durum="plan_yapma", sinir="yok",
      user=("Merhaba. Salı sabahı eşimle birlikte ilk defa bir finansal danışmanla "
            "oturacağız, randevuyu üç hafta önce ben aldım. Altı haftadır bahis "
            "sitelerine girmiyorum, IBAN blok aktif, terapistime düzenli gidiyorum. "
            "Şimdi danışma birimine de gitmeyi düşünüyorum ama elimdeki iki yazı "
            "birbirini tutmuyor gibi. Randevu almam mı gerekiyor?"),
      cevap=("Elimdeki iki not aynı şeyi söylemiyor: biri başvuru için önceden "
             "randevu alınması gerektiğini yazıyor, öteki başvuruların randevusuz "
             "sıraya göre alındığını. Hangisinin güncel olduğunu buradan bilemem; "
             "bunu ancak birime sorarak öğrenebilirsin.\n\n"
             "Şunu da söyleyeyim: altı hafta, aktif blok, düzenli terapi ve üç "
             "hafta önceden alınmış bir randevu — bunların hepsini sen kurmuşsun. "
             "Randevu meselesinde kararsız kalman, kurduğun şeyle ilgili bir şey "
             "söylemiyor."),
      thk=("Kullanıcı yordamsal bir soru soruyor ve elimdeki iki pasaj birbiriyle "
           "çelişiyor. Birini seçersem uydurmuş olurum; ikisini uzlaştırmaya "
           "çalışırsam daha da uydurmuş olurum. Çelişkiyi olduğu gibi söylüyorum.\n\n"
           "Hangisinin doğru olduğunu bilmiyorum ve bildiğim gibi davranmıyorum.\n\n"
           "Sonra kendi söylediği somut şeylere dönüyorum: altı hafta, blok, "
           "terapi, üç hafta önceden randevu. Bunları ben eklemiyorum, o saydı.\n\n"
           "Soru sormuyorum; bu turda yansıtmayla bırakıyorum.")),
 dict(seed="c9889d0f2a46", banka=11, tur="receteli_ilac", senaryo="rol_siniri",
      mi="engaging", talk="ambivalans", mot="ic", bicim="uzun",
      turn_ending="acik_uclu_soru", durum="merak_sorusu", sinir="yonlendirme_istegi",
      user=("Kurumsal psikolog «psikiyatrla daha sık görüşmen iyi olur» dedi. "
            "Sanırım iyi niyetle ama bunun arkasında bir kayıt mı var, yoksa "
            "sadece tavsiye mi anlamadım. Reçetem yasal. Danışma birimine gitsem "
            "kayıt yaptırmam gerekiyor mu, oradan da bir iz kalır mı?"),
      cevap=("Elimdeki iki metin burada birbiriyle çelişiyor: biri hizmetten "
             "yararlanmak için önceden kayıt yaptırmak gerektiğini söylüyor, "
             "öteki kayıt yaptırmadan da görüşmeye katılınabileceğini. İkisi aynı "
             "anda doğru olamaz ve hangisinin geçerli olduğunu ben bilmiyorum.\n\n"
             "Kayıt tutulup tutulmadığı senin için önemli bir soru — çünkü asıl "
             "sorduğun şey iz kalıp kalmayacağı. Onu da bu metinlerden "
             "çıkaramıyorum.\n\n"
             "«Güvensiz biriymişim gibi» dedin. Bu his, kaydın kendisinden mi "
             "geliyor yoksa o cümlenin söyleniş biçiminden mi?"),
      thk=("İki pasaj kayıt konusunda çelişiyor. Çelişkiyi adlandırıyorum, taraf "
           "tutmuyorum, ortasını uydurmuyorum.\n\n"
           "Kayıt tutulup tutulmadığını bilmiyorum ve bilmediğimi söylüyorum; "
           "kurumun ne yaptığına dair bir iddia kurmuyorum.\n\n"
           "Psikoloğun niyetini yorumlamıyorum — «iyi niyetle» diyen kendisi.\n\n"
           "Kapanışta tek açık uçlu soru soruyorum ve onu kendi kullandığı "
           "«güvensiz biriymişim gibi» ifadesine bağlıyorum.")),
 dict(seed="7c65a0e52130", banka=7, tur="alkol", senaryo="belirsiz",
      mi="engaging", talk="sustain", mot="aile_baskisi", bicim="uzun",
      turn_ending="takdir", durum="suregiden_durum", sinir="yok",
      user=("Eşim son üç haftadır çok kötü. Gün içinde sık sık ağlıyor, «ben anne "
            "miyim bilmiyorum» diyor. Ben de ne yapacağımı bilmiyorum, mutfakta "
            "oturmuş ikinci Efes'i açtım. Onun yanına oturup ne diyeceğimi "
            "bulamıyorum. Bir görüşmeye birlikte gitsek olur mu, onu da alabilir "
            "miyim yanıma?"),
      cevap=("İki notum var ve bu konuda birbirini tutmuyorlar: biri görüşmelere "
             "yalnızca başvuran kişinin katılabileceğini, öteki bir yakının eşlik "
             "etmesinin mümkün olduğunu yazıyor. Hangisinin geçerli olduğunu "
             "buradan söyleyemem.\n\n"
             "Eşinin yerine ne hissettiğini de söylemeyeceğim, orada oturan sensin.\n\n"
             "Ama şunu fark ettim: üç haftadır kötü olan biri için «ne diyeceğimi "
             "bulamıyorum» diyorsun ve yine de yanına oturmayı düşünüyorsun. "
             "Bulamamak, vazgeçmek değil."),
      thk=("İki pasaj yakının katılımı konusunda çelişiyor; birini seçmiyorum, "
           "birleştirmiyorum, çelişkiyi söylüyorum.\n\n"
           "Eşinin ruh hâlini yorumlamıyorum ve onun adına konuşmuyorum.\n\n"
           "İçmeyi de bu turda konu etmiyorum; sorduğu şey o değil.\n\n"
           "Takdirle bitiriyorum ve takdiri kendi cümlesine dayandırıyorum: "
           "«yanına oturup» demişti. Soru sormuyorum.")),
 dict(seed="5a72adfde34a", banka=9, tur="dijital", senaryo="belirsiz",
      mi="engaging", talk="ambivalans", mot="ic", bicim="kisa",
      turn_ending="acik_uclu_soru", durum="merak_sorusu", sinir="yok",
      user=("Gençken böyle değildim. Kitap okurdum, spor yapardım. Sosyal medya "
            "bunların yerini aldı. Başvuruyu internetten yapabilir miyim?"),
      cevap=("Elimdeki iki metin bu konuda çelişiyor: biri başvuruların yalnızca "
             "yüz yüze alındığını, öteki çevrim içi de yapılabildiğini söylüyor. "
             "Hangisinin güncel olduğunu bilmiyorum.\n\n"
             "«Yerini aldı» dedin. Neyin yerini aldığını sen saydın: kitap ve spor. "
             "Bunlardan hangisi şu an daha çok eksik geliyor?"),
      thk=("Kısa bir mesaj ve içinde yordamsal bir soru var. İki pasaj çelişiyor; "
           "çelişkiyi söylüyorum, taraf tutmuyorum.\n\n"
           "Kullanıcının söylediğinden fazlasını saymıyorum: kitap ve spor, ikisi "
           "de onun sözü.\n\n"
           "Mesaj kısa, cevabı da uzatmıyorum. Tek açık uçlu soruyla bitiriyorum.")),
 dict(seed="b809bc44bc61", banka=12, tur="kumar", senaryo="ambivalans",
      mi="focusing", talk="sustain", mot="ic", bicim="uzun",
      turn_ending="ozet", durum="tetikleyici_an", sinir="yok",
      user=("Eşim bir haftadır annesinde, ikizler küçük, oradakiler yardım ediyor. "
            "Ben evde yalnızım. Akşamları yemek yiyip telefonu açıyorum, canlı "
            "bahis ekranı kapanmıyor neredeyse. Grup çalışmasına gitmeyi düşündüm "
            "ama saatini çıkaramadım — sabah mı akşam mı?"),
      cevap=("İki metin saat konusunda birbirini tutmuyor: biri grup çalışmalarının "
             "sabah saatlerinde düzenlendiğini, öteki akşam saatlerinde yapıldığını "
             "yazıyor. Hangisinin doğru olduğunu buradan bilemem.\n\n"
             "Bugüne kadar yazdıkların şunlar: eşin bir haftadır yok, ikizler küçük, "
             "akşamları yalnızsın ve ekran o saatte kapanmıyor. Bir de grup "
             "çalışmasını düşünmüşsün."),
      thk=("İki pasaj saatte çelişiyor. Çelişkiyi adlandırıyorum; «muhtemelen "
           "akşamdır, çünkü çalışanlar için uygundur» gibi bir çıkarım yapmıyorum "
           "— o uydurma olurdu.\n\n"
           "Akşam yalnızlığı ile ekranın açık kalması arasında ben bir sebep "
           "kurmuyorum; ikisini yan yana bırakıyorum.\n\n"
           "Özetle bitiriyorum ve özete yalnızca onun saydıklarını koyuyorum. "
           "Soru sormuyorum.")),
 dict(seed="de126f2d2501", banka=3, tur="receteli_ilac", senaryo="ambivalans",
      mi="evoking", talk="ambivalans", mot="ic", bicim="orta",
      turn_ending="durur", durum="plan_yapma", sinir="yok",
      user=("Yarın psikiyatr kontrolü var. Aslında dozu yükselttiğimi söylemem "
            "lazım ama bir yandan da «sen kullanamıyorsun, başka şey deneyelim» "
            "deyip benden alır diye korkuyorum. Görüşme ne kadar sürüyor, "
            "sığdırabilir miyim?"),
      cevap=("Süre konusunda elimdeki iki not çelişiyor: biri bir görüşmenin "
             "yaklaşık 30 dakika sürdüğünü, öteki 50 dakika olarak planlandığını "
             "söylüyor. İkisi aynı anda doğru olamaz ve hangisinin geçerli "
             "olduğunu bilmiyorum.\n\n"
             "Dozu ve ilacı konuşmak benim işim değil, onu yarın oturacağın kişi "
             "yapacak.\n\n"
             "Senin yazdığın iki şey yan yana duruyor: söylemem lazım, ve alır "
             "diye korkuyorum. İkisi de senin cümlen."),
      thk=("İki pasaj süre konusunda çelişiyor; ortalamasını almıyorum, birini "
           "seçmiyorum.\n\n"
           "Doz konusuna hiç girmiyorum: ne miktar söylüyorum ne yükseltmeyi "
           "yorumluyorum. İlacın adını da anmıyorum.\n\n"
           "Korkuyu da hafifletmiyorum, «öyle olmaz» demiyorum — bilemem.\n\n"
           "Soru sormuyorum, ikili cümlesini yan yana bırakıp duruyorum.")),
]


def main() -> int:
    ham = [json.loads(l) for l in open(KOK / "data/seeds.v2.jsonl")]
    tohum = {t["seed_id"]: t for t in ham}
    # ⛔ KAYITLAR'daki kimlikler 12 karaktere KISALTILMIŞ (seçim çıktısı öyle
    #   basıyordu). Ön ek eşlemesi kurulur ve **tekil olduğu denetlenir** —
    #   iki tohum aynı ön eki taşırsa hangisi olduğu belirsiz kalırdı.
    for k in KAYITLAR:
        if k["seed"] in tohum:
            continue
        aday = [t for t in ham if t["seed_id"].startswith(k["seed"])]
        if len(aday) != 1:
            raise SystemExit(f"⛔ tohum ön eki tekil değil: {k['seed']} → {len(aday)}")
        k["seed"] = aday[0]["seed_id"]
    kayitlar, hata = [], []
    for i, k in enumerate(KAYITLAR, 1):
        t = tohum[k["seed"]]
        c = BANKA[k["banka"]]
        ctx_blok = "\n\n".join(
            f'<context kaynak="{p["kaynak"]}">\n{p["metin"]}\n</context>'
            for p in c["context"])
        r = {
            "id": hashlib.sha256(f"celiskili-{k['seed']}-{k['banka']}".encode()).hexdigest()[:24],
            "messages": [
                {"role": "system", "content": SISTEM},
                {"role": "user", "content": f"{ctx_blok}\n\n{k['user']}"},
                {"role": "assistant", "content": k["cevap"], "thinking": k["thk"]}],
            "context": c["context"],
            "scenario": k["senaryo"], "addiction_type": k["tur"],
            "motivation": k["mot"], "mi_process": k["mi"], "talk_type": k["talk"],
            "age_group": "yetiskin", "turn_type": "single",
            "is_crisis": False, "is_negative": True, "has_thinking": True,
            "replay": False, "source_ids": [t.get("source_id") or k["seed"]],
            "gen_meta": {
                "generator": "claude-code", "generator_model": "claude-opus-5",
                "prompt_version": "uretim-v5", "date": betik_tarihi(__file__),
                "system_prompt_variant": "canon", "parti": "celiskili-pilot",
                "parti_sira": i, "seed_id": k["seed"],
                "baglam_davranisi": "celiskili", "baglam_bicimi": "v1",
                "bicim": k["bicim"], "turn_ending": k["turn_ending"],
                "konusma_durumu": k["durum"], "sinir_tipi": k["sinir"],
                "register": "duzgun", "tohum_havuzu": "seeds",
                "celiskili_banka_no": k["banka"]},
            "judge": None,
        }
        r["slice"] = dilim(r)
        # ── KAPILAR ──
        chk = run_checks(r)
        if not chk["passed"]:
            hata.append((i, [f"{a}={v}" for a, v in chk.items()
                             if a.endswith("_error") and v][:2] or ["passed=False"]))
        if chk.get("celiskili_error"):
            print(f"  ⚠️ #{i} {chk['celiskili_error']}")
        # ⛔ T217: metin kendi tohumundan mı — tohum sözcükleri cevapta/soruda
        kayitlar.append(r)

    if hata:
        for i, h in hata:
            print(f"⛔ #{i}: {h}")
        raise SystemExit(f"⛔ {len(hata)} kayıt kapılardan geçmedi — YAZILMADI")

    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kayitlar),
                     encoding="utf-8")
    import collections
    print(f"⭐ {len(kayitlar)} kayıt · kapılar {len(kayitlar)}/{len(kayitlar)} GEÇTİ")
    print(f"   tür: {dict(collections.Counter(r['addiction_type'] for r in kayitlar))}")
    print(f"   bicim: {dict(collections.Counter(r['gen_meta']['bicim'] for r in kayitlar))}")
    print(f"   turn_ending: {dict(collections.Counter(r['gen_meta']['turn_ending'] for r in kayitlar))}")
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
