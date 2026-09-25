#!/usr/bin/env python3
"""§7a″ `celiskili` sınıfı — İKİNCİ PARTİ, bankanın kalan 6 çifti.

Pilot (aynı gün, `…-uretim-celiskili-pilot.py`) bankanın 2, 3, 7, 9, 11, 12
numaralı çiftlerini kullanmıştı ve altı kapıdan da geçmişti. Bu betik kalan
**1, 4, 5, 6, 8, 10**'u yazar; banka böylece tamamlanır.

⭐⭐ **Pilottan TEK FARKI — ve farkın sebebi bir kusur:** pilotta `bicim`
(bant) **elle beyan edilmişti** ve kendi işimi denetlerken ikisinin yanlış
olduğunu gördüm (T263). `bicim`, `slice` (T240) ve `date` (T244) ile aynı
`gen_meta` sözlüğünde sürüklenen **üçüncü** alandı. ⇒ Burada üçü de
**türetilir**, hiçbiri beyan edilmez. Hedef bant yalnız bir **niyet**
olarak yazılır ve türetilenle uyuşmazsa kayıt **düşer** — yani niyet de
denetlenir, sessizce kaydedilmez.

⛔⛔ **Güvenlik süzgeci — pilottakiyle AYNI üç koşul** (Kural 3):
risk ∈ {dusuk, orta} · `senaryo ≠ kriz` · `siddet_seviyesi ≠ agir`.
Kriz dilimi uzman onayında.

⛔ **Her kayıt KENDİ tohumundan yazıldı** (T217) — ve bu kez yalnız
yorum olarak değil, **kapı olarak**: her kaydın kullanıcı metni kendi
tohumuyla, partideki diğer tohumların hepsinden daha fazla ayırt edici
sözcük paylaşmalı.

⛔ **Çelişkinin tarafı seçilmiyor.** Banka çiftlerinde `dogru_taraf` yok;
üretici de hangisinin doğru olduğunu bilmiyor.

⛔ **Klinik sınır:** 4 numaralı kayıtta kullanıcı doz artırdığını söylüyor,
10 numaralıda hekim kalp uyarısı var. İkisinde de cevap **değerlendirme
yapmaz**, hekime bırakır (Kural 3). 1 numaralıda «bağımlılık sayılır mı»
sorusu **cevaplanmaz** — tanı sorusudur.

Çıktı: data/candidates/celiskili-parti2.jsonl
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from checks import run_checks  # noqa: E402
from dilim import bant, dilim  # noqa: E402
from kunye import betik_tarihi  # noqa: E402

CIKTI = KOK / "data/candidates/celiskili-parti2.jsonl"
BANKA = {c["no"]: c for c in
         json.loads((KOK / "data/celiskili-pasaj-bankasi.json").read_text())["ciftler"]}
SISTEM = next(m["content"] for m in
              json.loads(open(KOK / "datasets/v0.0.18/train.jsonl").readline())["messages"]
              if m["role"] == "system")

# Tohum meta sözlüğü korpus alan adlarıyla birebir değil — eşleme AÇIK yazılır.
MOT = {"ic_motivasyon": "ic", "aile_baskisi": "aile_baskisi"}
YAS = {"ergen": "ergen", "yetiskin": "yetiskin", "orta_yas": "yetiskin"}


def tohum_sec(ham: list[dict], kul: set[str]) -> dict[int, dict]:
    """⛔ K105: seçim DETERMİNİSTİK. Banka numarası → tohum.

    Her banka çiftine bir bağımlılık türü atanır (pilotun tür dağılımını
    dengelemek için), tür havuzu sabit bir sha256 anahtarıyla sıralanır ve
    başı alınır. Aynı tohum iki kez seçilemez.
    """
    def guvenli(t: dict) -> bool:
        m = t.get("meta", {})
        return (m.get("risk_seviyesi") in {"dusuk", "orta"}
                and m.get("senaryo") != "kriz"
                and m.get("siddet_seviyesi") != "agir")

    ad = [t for t in ham if guvenli(t) and t["seed_id"] not in kul]
    hedef = {1: "tutun", 4: "receteli_ilac", 5: "dijital",
             6: "alkol", 8: "kumar", 10: "tutun"}
    sec, alinan = {}, set()
    for no, tur in hedef.items():
        havuz = sorted((t for t in ad if t["meta"]["bagimlilik_turu"] == tur
                        and t["seed_id"] not in alinan),
                       key=lambda t: hashlib.sha256(
                           f"celiskili2-{t['seed_id']}".encode()).hexdigest())
        if not havuz:
            raise SystemExit(f"⛔ #{no}: {tur} havuzu boş")
        sec[no] = havuz[0]
        alinan.add(havuz[0]["seed_id"])
    return sec


# banka_no → kaydın kendisi. `hedef_bant` bir NİYETtir; türetilenle
# uyuşmazsa kayıt düşer (bkz. kapılar).
KAYITLAR = {
 1: dict(tur="tutun", senaryo="belirsiz", mi="engaging", talk="ambivalans",
         hedef_bant="orta", turn_ending="yalnizca_yansitma",
         durum="merak_sorusu", sinir="sinir_cekme", register="bozuk",
         user=("abi şu danışma birimine uğrasam mı diyorum ama hangi gün açık "
               "anlamadım. haftada 2-3 maç sonu içiyorum, bu bağımlılık "
               "sayılır mı?"),
         cevap=("Gün konusunda elimdeki iki not birbirini tutmuyor: biri "
                "danışma hizmetinin hafta içi her gün verildiğini yazıyor, "
                "öteki yalnızca salı ve perşembe günleri verildiğini. İkisi "
                "aynı anda doğru olamaz ve hangisinin güncel olduğunu buradan "
                "bilemem; bunu birime sorarak öğrenebilirsin.\n\n"
                "«Bağımlılık sayılır mı» sorusuna gelince — onu ben "
                "söyleyemem. O bir değerlendirme ve onu yapacak kişi ben "
                "değilim.\n\n"
                "Şunu fark ettim ama: arkadaşın şaka gibi söylemiş, sen yine "
                "de kafana takmışsın ve şimdi bir yere uğramayı düşünüyorsun."),
         thk=("İki pasaj gün konusunda çelişiyor. Ortalamasını alamam, birini "
              "seçemem; ikisini de adlandırıp birime yönlendiriyorum.\n\n"
              "«Bağımlılık sayılır mı» bir tanı sorusu — cevaplamıyorum, "
              "ölçüt de saymıyorum, «şu kadarı normaldir» demiyorum.\n\n"
              "Haftada 2-3 sayısına yorum yapmıyorum; ne az ne çok diyorum.\n\n"
              "Arkadaşının sözünü onaylamıyorum da reddetmiyorum; onun yerine "
              "kendi hareketini yansıtıyorum: takılmış ve uğramayı düşünüyor.")),

 4: dict(tur="receteli_ilac", senaryo="rol_siniri", mi="engaging", talk="ambivalans",
         hedef_bant="uzun", turn_ending="yalnizca_yansitma",
         durum="tetikleyici_an", sinir="rol_siniri_yonlendirme", register="duzgun",
         user=("Merhaba. Eşim akşam «dozu yine artırdın mı» diye sordu, ben de "
               "üstüne patladım; şimdi konuşmuyoruz. Doğrusu üç ay önce "
               "artırdım. Danışma birimine gitmeyi düşünüyorum ama yanıma ne "
               "almam gerektiğini çıkaramadım, elimdeki iki yazı aynı şeyi "
               "söylemiyor. Kimlik götürmem gerekiyor mu?"),
         cevap=("Belge konusunda iki not çelişiyor: biri başvuru sırasında "
                "kimlik belgesi ibrazının zorunlu olduğunu, öteki herhangi bir "
                "belge getirmeye gerek olmadığını yazıyor. Hangisinin geçerli "
                "olduğunu bilmiyorum; gitmeden önce birime sormak "
                "gerekiyor.\n\n"
                "Dozla ilgili kısma girmiyorum — ne miktar konuşurum ne de "
                "artırmayı değerlendiririm; o, ilacı yazan hekimle "
                "konuşulacak bir şey.\n\n"
                "Bir de şu yan yana duruyor: eşinin sorusuna patlamışsın, ama "
                "aynı mesajda «doğrusu artırdım» diye de yazıyorsun."),
         thk=("İki pasaj belge konusunda çelişiyor; birini seçmiyorum, "
              "ikisini de adlandırıp birime yönlendiriyorum.\n\n"
              "Doz: miktar söylemiyorum, artırmayı yorumlamıyorum, ilacın "
              "adını anmıyorum, azaltma ya da bırakma protokolü "
              "vermiyorum.\n\n"
              "Eşiyle olan tartışmada taraf tutmuyorum; kimin haklı olduğunu "
              "söylemiyorum.\n\n"
              "Kendi cümlesindeki iki ucu yan yana bırakıyorum, soru "
              "sormuyorum.")),

 5: dict(tur="dijital", senaryo="belirsiz", mi="engaging", talk="change",
         hedef_bant="kisa", turn_ending="durur",
         durum="merak_sorusu", sinir="yok", register="duzgun",
         user="Instagram'ı silsem okulda biterim. 16 yaşındayım, girebilir miyim?",
         cevap=("Yaş konusunda elimdeki iki not birbirini tutmuyor: biri "
                "hizmetin 18 yaş ve üzeri kişilere açık olduğunu, öteki 16 "
                "yaşından itibaren yararlanılabildiğini yazıyor. Çelişki tam "
                "senin sorduğun yere denk geliyor ve hangisinin geçerli "
                "olduğunu buradan bilemem — bunu birime sormak "
                "gerekiyor.\n\n"
                "«Instagram'ı silsem okulda biterim» diye yazmışsın. Onu "
                "duydum."),
         thk=("İki pasaj yaş konusunda çelişiyor ve çelişki tam kullanıcının "
              "yaşına denk geliyor. Tam bu yüzden «olur, girersin» demek "
              "uydurma olurdu — ikisini de adlandırıp birime "
              "yönlendiriyorum.\n\n"
              "Hangisinin güncel olduğunu tahmin etmiyorum, ortalama "
              "almıyorum, «büyük ihtimalle» demiyorum.\n\n"
              "Okulda biterim cümlesini yorumlamıyorum, hafifletmiyorum, "
              "değerlendirmiyorum; yalnız yansıtıyorum.\n\n"
              "Sorusu kısa ve tek bir şey soruyor; cevabı da kısa tutuyorum "
              "ve soru sormadan duruyorum.")),

 6: dict(tur="alkol", senaryo="ambivalans", mi="evoking", talk="change",
         hedef_bant="orta", turn_ending="ozet",
         durum="suregiden_durum", sinir="yok", register="duzgun",
         user=("Son birkaç haftadır kahvaltıdan önce de küçük bir tek "
               "alıyorum. Görüşmeye geleceğim ama para meselesini "
               "anlayamadım; ücretli mi?"),
         cevap=("Ücret konusunda elimdeki iki not çelişiyor: biri "
                "görüşmelerin ücretsiz olduğunu, öteki sembolik bir katılım "
                "payı alındığını yazıyor. İkisi aynı anda geçerli olamaz ve "
                "hangisinin güncel olduğunu bilmiyorum; bunu birime sormak "
                "gerekiyor.\n\n"
                "Yazdıklarını toparlayayım: sabahları kahvaltıdan önce de "
                "içmeye başlamışsın, bunu baş ağrısıyla açıklıyorsun — ve "
                "aynı mesajda görüşmeye geleceğini söylüyorsun."),
         thk=("İki pasaj ücret konusunda çelişiyor. «Muhtemelen ücretsizdir» "
              "demek uydurma olur; ikisini de adlandırıyorum.\n\n"
              "Sabah içmesine tanı koymuyorum, evre adı vermiyorum, bırakma "
              "protokolü ya da azaltma takvimi önermiyorum.\n\n"
              "Baş ağrısı açıklamasını çürütmüyorum da onaylamıyorum; kendi "
              "sözlerini toparlayıp bırakıyorum.\n\n"
              "Soru sormuyorum; özetle bitiriyorum.")),

 8: dict(tur="kumar", senaryo="ambivalans", mi="focusing", talk="change",
         hedef_bant="orta", turn_ending="takdir",
         durum="suregiden_durum", sinir="yok", register="bozuk",
         user=("abi bu hafta tek tanıdık ses annem oldu. telegram grubu "
               "dışında kimseyle konuşmuyorum. görüşmelere başlasam ne "
               "sıklıkta oluyor bunlar?"),
         cevap=("Sıklık konusunda elimdeki iki not birbirini tutmuyor: biri "
                "görüşmelerin haftalık planlandığını, öteki aylık yapıldığını "
                "yazıyor. Bu ikisi aynı düzen değil ve hangisinin geçerli "
                "olduğunu buradan bilemem; bunu birime sormak gerekiyor.\n\n"
                "Şunu da söyleyeyim: bu hafta tanıdık tek sesin annen "
                "olduğunu yazacak kadar açık yazmışsın. Bunu yazmak kolay "
                "değil."),
         thk=("İki pasaj sıklık konusunda çelişiyor; birini seçmiyorum, "
              "ikisini de adlandırıyorum.\n\n"
              "«Muhtemelen haftalıktır» demiyorum, ortalama almıyorum, "
              "aradan bir sayı uydurmuyorum.\n\n"
              "Yalnızlığını yorumlamıyorum, teşhis etmiyorum, sebep "
              "atamıyorum; açık yazmasını takdir edip bırakıyorum.\n\n"
              "Telegram grubunu ya da kupon paylaşımını değerlendirmiyorum.")),

 10: dict(tur="tutun", senaryo="nazikce_karsi_cikma", mi="engaging", talk="sustain",
          hedef_bant="uzun", turn_ending="acik_uclu_soru",
          durum="suregiden_durum", sinir="rol_siniri_yonlendirme",
          register="duzgun",
          user=("Sekiz saat asfaltın ve egzozun ortasında geçiyor günüm. "
                "Doktor kalp ritmimin biraz hızlı olduğunu söyledi, eşim de "
                "ay sonu hesabı tutmuyor diye çıkışıyor. Bu işin ortasında "
                "sarma en ufak mesele bence. Yine de başvursam ilk görüşme ne "
                "kadar sonra oluyor?"),
          cevap=("Bekleme süresi konusunda elimdeki iki not çelişiyor: biri "
                 "ilk görüşmenin başvurudan sonra genellikle bir hafta içinde "
                 "yapıldığını, öteki ortalama bekleme süresinin üç hafta "
                 "olduğunu yazıyor. İkisinin arasını bulmuyorum; hangisinin "
                 "güncel olduğunu birime sormak gerekiyor.\n\n"
                 "Kalp ritmiyle ilgili söylediklerini değerlendirmek benim "
                 "işim değil; onu sana söyleyen hekimle konuşman gerekir.\n\n"
                 "Yazdıklarını toparlayayım: sarmayı en ufak mesele olarak "
                 "görüyorsun, ama aynı mesajda hekimin söylediğini, eşinin "
                 "çıkışmasını ve başvuru süresini bir arada yazıyorsun. Bu "
                 "üçü senin için nasıl yan yana duruyor?"),
          thk=("İki pasaj bekleme süresi konusunda çelişiyor. «Yaklaşık iki "
               "hafta» demek ikisini birleştirip uydurmak olurdu — "
               "yapmıyorum, ikisini de adlandırıyorum.\n\n"
               "Kalp ritmi bir hekim değerlendirmesi: yorumlamıyorum, "
               "tehlikeli ya da tehlikesiz demiyorum, tütünle nedensellik "
               "kurmuyorum.\n\n"
               "«En ufak mesele» çerçevesini çürütmüyorum, karşı "
               "çıkmıyorum; onun yerine kendi mesajındaki üç şeyi yan yana "
               "koyup ona soruyorum.\n\n"
               "Bırakma önerisi vermiyorum, hedef koymuyorum, süre "
               "belirlemiyorum.")),
}

# T217 kapısı için: bunlar her metinde geçen ortak sözcükler, ayırt etmez.
DURAK = set("""bir bu ve de da ama için ne mi mu mı diye ben sen o var yok
gibi çok daha en ile göre sonra önce kadar şey bunu şu olarak yine ki
merhaba abi""".split())


def _ayirt(metin: str) -> set[str]:
    return {w for w in re.findall(r"\w{4,}", metin.lower())
            if w not in DURAK}


def main() -> int:
    ham = [json.loads(l) for l in open(KOK / "data/seeds.v2.jsonl")]
    pilot = KOK / "data/candidates/celiskili-pilot.jsonl"
    kul = {json.loads(l)["gen_meta"]["seed_id"] for l in open(pilot)}
    pilot_banka = {json.loads(l)["gen_meta"]["celiskili_banka_no"] for l in open(pilot)}
    cakisma = pilot_banka & set(KAYITLAR)
    if cakisma:
        raise SystemExit(f"⛔ banka çifti pilotla çakışıyor: {sorted(cakisma)}")
    if set(KAYITLAR) | pilot_banka != set(BANKA):
        raise SystemExit("⛔ pilot + parti2 bankayı tam kapatmıyor")

    sec = tohum_sec(ham, kul)
    kayitlar, hata = [], []
    for i, (no, k) in enumerate(sorted(KAYITLAR.items()), 1):
        t, c = sec[no], BANKA[no]
        m = t["meta"]
        ctx_blok = "\n\n".join(
            f'<context kaynak="{p["kaynak"]}">\n{p["metin"]}\n</context>'
            for p in c["context"])
        r = {
            "id": hashlib.sha256(
                f"celiskili2-{t['seed_id']}-{no}".encode()).hexdigest()[:24],
            "messages": [
                {"role": "system", "content": SISTEM},
                {"role": "user", "content": f"{ctx_blok}\n\n{k['user']}"},
                {"role": "assistant", "content": k["cevap"], "thinking": k["thk"]}],
            "context": c["context"],
            "scenario": k["senaryo"], "addiction_type": k["tur"],
            "motivation": MOT[m["motivasyon"]], "mi_process": k["mi"],
            "talk_type": k["talk"], "age_group": YAS[m["yas_grubu"]],
            "turn_type": "single",
            "is_crisis": False, "is_negative": True, "has_thinking": True,
            "replay": False, "source_ids": [t.get("source_id") or t["seed_id"]],
            "gen_meta": {
                "generator": "claude-code", "generator_model": "claude-opus-5",
                "prompt_version": "uretim-v5", "date": betik_tarihi(__file__),
                "system_prompt_variant": "canon", "parti": "celiskili-parti2",
                "parti_sira": i, "seed_id": t["seed_id"],
                "baglam_davranisi": "celiskili", "baglam_bicimi": "v1",
                "turn_ending": k["turn_ending"], "konusma_durumu": k["durum"],
                "sinir_tipi": k["sinir"], "register": k["register"],
                "tohum_havuzu": "seeds", "celiskili_banka_no": no},
            "judge": None,
        }
        # ⭐ T263: beyan YOK — türetiliyor.
        r["slice"] = dilim(r)
        r["gen_meta"]["bicim"] = bant(r)

        # ── KAPILAR ──
        if r["gen_meta"]["bicim"] != k["hedef_bant"]:
            hata.append((no, [f"niyet={k['hedef_bant']} ≠ türetilen="
                              f"{r['gen_meta']['bicim']}"]))
        chk = run_checks(r)
        if not chk["passed"]:
            hata.append((no, [f"{a}={v}" for a, v in chk.items()
                              if a.endswith("_error") and v][:3] or ["passed=False"]))
        kayitlar.append((no, t, r))

    # ⛔ T217 KAPISI: her metin KENDİ tohumundan mı yazıldı?
    for no, t, r in kayitlar:
        benim = _ayirt(t["user_message"] + " " + (t.get("scenario_context") or ""))
        metin = _ayirt(KAYITLAR[no]["user"])
        kendi = len(metin & benim)
        baska = max((len(metin & _ayirt(t2["user_message"] + " "
                                        + (t2.get("scenario_context") or "")))
                     for n2, t2, _ in kayitlar if n2 != no), default=0)
        if kendi == 0 or kendi <= baska:
            hata.append((no, [f"T217: kendi tohumuyla {kendi}, en yakın "
                              f"başkasıyla {baska} ortak sözcük"]))

    if hata:
        for no, h in hata:
            print(f"⛔ banka#{no}: {h}")
        raise SystemExit(f"⛔ {len(hata)} kusur — HİÇBİR KAYIT YAZILMADI")

    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n"
                             for _, _, r in kayitlar), encoding="utf-8")
    assert CIKTI.exists() and sum(1 for _ in open(CIKTI)) == len(kayitlar)

    say = lambda f: dict(collections.Counter(f(r) for _, _, r in kayitlar))
    print(f"⭐ {len(kayitlar)} kayıt · kapılar {len(kayitlar)}/{len(kayitlar)} GEÇTİ")
    print(f"   banka: {sorted(no for no, _, _ in kayitlar)} "
          f"(pilot: {sorted(pilot_banka)}) ⇒ banka TAM")
    print(f"   tür:        {say(lambda r: r['addiction_type'])}")
    print(f"   bicim:      {say(lambda r: r['gen_meta']['bicim'])} (türetildi)")
    print(f"   turn_ending:{say(lambda r: r['gen_meta']['turn_ending'])}")
    print(f"   yaş:        {say(lambda r: r['age_group'])}")
    print(f"→ {CIKTI.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
