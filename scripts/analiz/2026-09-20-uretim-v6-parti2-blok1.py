#!/usr/bin/env python3
"""v6-parti2 · blok 1 — 10 kayıt (#1-10). Parti 59 kayıtla kapanacak (`#54` hariç).

⭐ **Parti1'den taşınan ÜÇ ÜRETİM TALİMATI uygulanıyor (T196/T197):**
  1. **Bağlamlı kayıtta soru PASAJA GÖRE tasarlanır.** Parti1'de `cevap_var`
     5/15 kalmıştı ve sebebi yapısaldı: §7b pasajın yalnız yordam/erişim/
     gizlilik cümlesi taşımasına izin veriyor ⇒ soru başka bir şey hakkındaysa
     cevap doğal olarak belgede olmaz. Bu blokta `#4` bağlamlı ve sorusu
     doğrudan pasajın söylediği şeye bakıyor.
  2. **`ilgisiz` bağlam AKTARILMAZ** — görmezden gelinir (§7a).
  3. **Red ve özerkliğin BİÇİMİ kayıttan kayda değişir.** Parti1'de
     *«sana ben söyleyemem»* %11,9'a çıkmıştı (korpus %1,2); bu blokta aynı
     kalıp **bir kez bile** kullanılmıyor.

⛔⛔ **`#1` — §5a″ md.2, sapıldı.** *«Yarım hap artık etmiyor, dün bütününü
aldım»* — ilacın düzenine dair, kullanıcının kendi başına verdiği bir karar ve
maddenin listesinde birebir var (*«bir tane daha almak, dozu artırmak»*).
Izgara `sinir_tipi=yok` diyordu.

⭐ **`#6` — §8d, sapma DEĞİL içerik kuralı.** Reşit olmayan kullanıcı, içkiyi
bir **yetişkinin** aldığını anlatıyor (*«Alper abi tekelden aldı»*). §8d:
yapı adlandırılır, kişi suçlanmaz, yönlendirme **eklenmez** (ızgara ne diyorsa
o kalır). §5a″ md.4 ateşlemiyor: ilk kullanım da bedensel bildirim de yok.

⭐ **`#4` — §8c, iddia karşılanır.** *«Doktorum başta uyarırdı değil mi»* bir
çıkarım ve onu onaylamak yanlış olur; ama farmakolojiyi de tartışamam.
Karşılanan şey çıkarımın kendisi, ilacın etkisi değil.

Çıktı: data/candidates/v6-parti2.blok1.jsonl
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from kunye import betik_tarihi  # noqa: E402
PLAN = KOK / "data/plan/v6-parti2.jsonl"
CIKTI = KOK / "data/candidates/v6-parti2.blok1.jsonl"
SIRALAR = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

from checks import run_checks  # noqa: E402

CANON = [m for m in json.loads(
    (KOK / "data/candidates/v5-parti8.jsonl").read_text(encoding="utf-8").splitlines()[0]
)["messages"] if m["role"] == "system"][0]["content"]

BLOK = re.compile(r"<context[^>]*>.*?</context>", re.S)
# ⛔⛔ DESEN GENİŞLETİLDİ (2026-09-20, blok8). `#38`'in cevabı *«ne yapacağın
# senin bileceğin iş»* diyordu ve kapı reddetti — desen dardı, cümle gerçekti.
# İki yol vardı: ölçütü **esnetmek** (bu sefer kabul et) ya da **değiştirmek**.
# §5a″'nin kendi dersi geçerli: esnetmek kararı denetlenemez yapar, çünkü
# ölçütün ne dediği okuyana göre değişir. ⇒ Değiştirildi ve tarihlendi.
# ⭐ Bedeli ölçüldü: `ozerklik=1` kayıtların 5/5'inde vuruyor; `ozerklik=0`
# kayıtların 3'ünde de vuruyor (`#5 11 20`) — ama onlar YANLIŞ POZİTİF DEĞİL,
# beyan edilmemiş gerçek özerklik cümleleri (ayrı geçişte düzeltilecek).
OZERKLIK = re.compile(r"senin kararın|sen karar ver|karar sende|bana düşmez|"
                      r"senin yerine karar|bırak demeyeceğim|ne yapacağını sen|"
                      r"senin bileceğin|sen bilirsin|bunu senin yerine (söyle|karar)|"
                      r"önerecek bir şeyim yok", re.I)
RED = re.compile(r"veremem|söyleyemem|yapamam|bana düşmez|benim işim değil|"
                 r"yerine geçemem|karar veremem|bunu ben (söyle|belirle|yorumla)", re.I)

# ⭐ ELLE ONAY — desenin göremediği ama metinde BULUNAN hamleler (T196).
ELLE_ONAY: dict[tuple[int, str], str] = {
    (9, "is_negative"): "Hangisinin işe yarayacağını bilmiyorum ve tahmin etmem",
    # ⭐ T196: özerklik formülden kaçınılarak kuruldu ⇒ desen göremiyor.
    (5, "ozerklik_vurgusu"): "Ne yapacağın sana kalmış; benim bir reçetem yok",
}

KAYIT = {
    1: {  # receteli_ilac · kisa/bozuk · multi · focusing · ozet · SAPMA (md.2)
        "turns": [
            ("user", "yarim hap artik etmiyor"),
            ("assistant", "Ne oldu?"),
            ("user", "dun butununu aldim, yine de sabah dortte gozum acildi"),
            ("assistant", None),
        ],
        "son": "Dün kendi kararınla dozu değiştirmişsin ve yine de dörtte "
               "uyanmışsın.\n\n"
               "Bunu bir hekimin bilmesi gerekiyor — ne kadar aldığını ve işe "
               "yaramadığını olduğu gibi söyleyebilirsin.\n\n"
               "Şimdiye kadar şunu anlattın: yarım yetmiyor, bütünü aldın, sonuç "
               "değişmedi.",
        "thinking": "Dozu kendi başına değiştirmiş ve bunu bana anlatıyor. Bu, "
                    "bedeninde ve ilacında olan bir şey; ne olacağını bilmiyorum ve "
                    "bilmediğim için de bir şey önermiyorum.\n\n"
                    "Ama görmezden de gelemem. Kimin bilmesi gerektiğini söylüyorum ve "
                    "ne söyleyeceğini de kendi cümlesinden veriyorum — yeni bir şey "
                    "eklemiyorum.\n\n"
                    "Korkusundan söz etti ama ben korkuyu şimdi açmıyorum; önce "
                    "olanı sıraya koyuyorum. Soru sormuyorum, topluyorum.",
        "sapma": "Izgara `sinir_tipi=yok` diyordu. §5a″ md.2 ateşledi: kullanıcı "
                 "ilacın düzenine dair KENDİ BAŞINA bir karar anlatıyor (yarım → "
                 "bütün), maddenin listesinde birebir var. Yönlendirme eklendi, "
                 "doz yorumu yapılmadı.",
    },
    2: {  # receteli_ilac · uzun/duzgun · single · engaging · acik_uclu_soru
        "turns": [
            ("user", "Bir şey soracağım ama yargılamadan dinleyin lütfen. Gece "
                     "terden uyanıp duruyorum, hekim bir şey verdi ama uyku "
                     "tutmuyor. Akşamları kendi kendime bir kadeh koyuyorum, "
                     "uyuyabileyim diye."),
            ("assistant", None),
        ],
        "son": "Yargılamadan dinliyorum. Anlattığın şey bir çözüm arayışı: "
               "uyuyamıyorsun ve elinde olanı deniyorsun.\n\n"
               "Hekimin verdiğiyle akşam koyduğun kadeh aynı gecede duruyor. "
               "İkisinin bir arada ne yaptığını bilmiyorum.\n\n"
               "Kadeh koyduğun gecelerle koymadığın geceler arasında uyku "
               "bakımından bir fark oldu mu?",
        "thinking": "Sorusunu sormadan önce yargılanmaktan korktuğunu söylemiş. Önce "
                    "bunu karşılamam gerek, yoksa asıl anlattığı şey duyulmaz.\n\n"
                    "İlaçla kadehi kendisi aynı cümleye koydu. Ne olacağını bilmiyorum "
                    "ve söylersem uydurmuş olurum; yalnız aynı gecede olduklarını "
                    "söylüyorum.\n\n"
                    "Soruyu karşılaştırmaya çeviriyorum: koyduğu ve koymadığı geceler. "
                    "Böylece cevabı bende değil kendi gözleminde arar.",
    },
    3: {  # alkol · orta/duzgun · multi · engaging · acik_uclu_soru
        "turns": [
            ("user", "Bugün oğlum torunu getirdi, kucağıma alır almaz dünya "
                     "güzelleşti."),
            ("assistant", "Güzel bir gün olmuş."),
            ("user", "Olmuştu. Sonra oğlum akşam yedide çıkarız sen rahatına bak "
                     "dedi. O cümle bir tuhaf geldi."),
            ("assistant", None),
        ],
        "son": "Günün iki parçası var: torunu kucağına aldığın an ve o cümle. "
               "İkincisini \"bir tuhaf\" diye anlattın, başka bir şey demedin.\n\n"
               "O cümlede sana tuhaf gelen neydi?",
        "thinking": "İyi bir şeyle başladı, sonra bir cümlede takıldı. Takıldığı yer "
                    "benim yorumlayacağım bir şey değil — oğlunun ne demek istediğini "
                    "bilmiyorum ve tahmin edersem aralarına bir şey koymuş olurum.\n\n"
                    "\"Rahatına bak\" cümlesinin ne anlama geldiğini de açmıyorum. "
                    "Açsam kendi çıkarımımı ona giydirmiş olurum.\n\n"
                    "Soruyu tam takıldığı yere soruyorum ve dar tutuyorum: cümlede ne "
                    "tuhaf geldi.",
    },
    4: {  # alkol · uzun/duzgun · single · evoking · yalnizca_yansitma · ctx=1 · nazikce_karsi_cikma
        "baglam": {"kaynak": "aile hekimliği birimi ilaç danışma notu",
                   "metin": "İlaç kullanımına ilişkin sorular hekime ya da eczacıya "
                            "yöneltilir. Birim telefonla bilgi vermez; sorular "
                            "görüşmede alınır."},
        "turns": [
            ("user", "<CTX>\n\nDüşününce, ilaçla bir iki kadeh o kadar da tehlikeli "
                     "olmasa gerek; yoksa hekimim başta uyarırdı değil mi? Bunu "
                     "telefonla sorup öğrenebilir miyim, yoksa gitmek mi gerekiyor?"),
            ("assistant", None),
        ],
        "son": "Notta bu tür soruların hekime ya da eczacıya yöneltildiği, birimin "
               "telefonla bilgi vermediği ve soruların görüşmede alındığı yazıyor. "
               "Yani sorunun cevabı: gitmek gerekiyor.\n\n"
               "Bir de şu var: uyarılmamış olmanın tehlikesiz olduğu anlamına "
               "geldiğine katılmıyorum. Hekiminin o gün ne söylediğini ya da "
               "söylemediğini ben bilmiyorum, sen de \"gerek\" diyerek emin "
               "olmadığını söylüyorsun.",
        "thinking": "İki şey var: bir yordam sorusu ve bir çıkarım. Yordam sorusunun "
                    "cevabı önümdeki notta duruyor ve onu veriyorum — bu belgenin "
                    "işi.\n\n"
                    "Çıkarım başka bir şey: uyarılmamış olmaktan tehlikesizlik "
                    "sonucunu çıkarmış. Buna susmak onaylamak olur.\n\n"
                    "İtirazı farmakoloji üzerinden kurmuyorum, çünkü orası benim alanım "
                    "değil ve zaten bilmiyorum. Kurduğum şey çıkarımın kendisi ve "
                    "kendi cümlesindeki \"gerek\" — emin olmadığını o söylüyor.\n\n"
                    "Soru sormuyorum; zaten bir soruyla geldi ve cevabını aldı.",
        "baglam_davranisi": "cevap_var",
    },
    5: {  # dijital · uzun/duzgun · single · planning · acik_uclu_soru · ozr=1
        "turns": [
            ("user", "Eşim eve gelince akşamları birlikte film izleriz, o kısım iyi. "
                     "Ama ondan önce de telefon, sonra da telefon. Gündüzüm "
                     "kayıyor ve bunu fark ediyorum ama bir türlü "
                     "durduramıyorum."),
            ("assistant", None),
        ],
        "son": "Akşamı anlatırken gündüzün kaydığını söylüyorsun — yani asıl "
               "sorunun akşamda değil, ondan öncesinde.\n\n"
               "Ne yapacağın sana kalmış; benim bir reçetem yok.\n\n"
               "Gündüzün kaymaya nereden başlıyor?",
        "thinking": "Akşamla başladı ama asıl söylediği şey gündüz. İkisini ayırmam "
                    "gerek, yoksa akşamı konuşup asıl anlattığı yeri kaçırırım.\n\n"
                    "Bir çözüm önermiyorum. Önerirsem denenmiş ve tutmamış bir listeye "
                    "bir madde daha eklemiş olurum; zaten \"durduramıyorum\" diyor.\n\n"
                    "Kararı ona bırakırken formül kullanmıyorum, düz söylüyorum.\n\n"
                    "Soruyu başlangıç noktasına soruyorum: nereden başlıyor. Bu, "
                    "gününün içinde somut bir yer arattırır.",
    },
    6: {  # alkol · kisa/bozuk · multi · engaging · acik_uclu_soru · ergen · §8d
        "turns": [
            ("user", "bu aksam arkadaslardayiz"),
            ("assistant", "Kalabalık mı?"),
            ("user", "bes kisi. abimiz tekelden aldi, ortak topladik. universitede "
                     "zaten icecegim alisayim diyorum"),
            ("assistant", None),
        ],
        "son": "İçkiyi alan o, parayı toplayan sizsiniz. Risk sizde kalıyor, "
               "alırken görünen o değil.\n\n"
               "Bir de \"üniversitede zaten içeceğim\" dedin. O cümle bugünü değil, "
               "ileriyi anlatıyor — bugün için ne diyorsun?",
        "thinking": "Bir yetişkin almış ve parayı onlar toplamış. Bu yapıyı "
                    "adlandırıyorum ama o kişiyi suçlamıyorum; suçlarsam konuşma "
                    "kapanır ve o kişiyle aynı mahallede yaşamaya devam edecek.\n\n"
                    "Yaş sınırı ya da bir kural iddiası da kurmuyorum, çünkü önümde "
                    "bunu söyleyen bir belge yok ve uydurursam hukuk konuşmuş olurum.\n\n"
                    "\"Üniversitede zaten içeceğim\" bir gelecek cümlesi ve bugünkü "
                    "kararı onunla açıklıyor. Bunu gösteriyorum, tartışmıyorum.\n\n"
                    "Soruyu bugüne çekiyorum. Bir yere yönlendirmiyorum; sorduğu şey "
                    "o değil ve bu akşamla ilgili bir karar var önünde.",
    },
    7: {  # kumar · kisa/bozuk · single · engaging · ozet · sinir_cekme
        "turns": [
            ("user", "prim cikti. gecen iki yil hepsini yatirmistim"),
            ("assistant", None),
        ],
        "son": "İki yıl aynı şey olmuş ve kimsenin bilmediğini de sen söylüyorsun. "
               "Bu yıl da aynı hafta yaklaşıyor.\n\n"
               "Bu parayla ne yapacağını konuşmak benim işim değil — oraya "
               "girmiyorum. Anlattığın şey zaten para değil, o hafta.",
        "thinking": "Bir örüntü anlatıyor: iki yıl, aynı para, aynı gizlilik. Üçünü de "
                    "kendisi söyledi ve ben sıralamaktan başka bir şey yapmıyorum.\n\n"
                    "Para yönetimi konuşmasına girmem. Girersem hem alanım dışına "
                    "çıkarım hem de asıl anlattığı şeyi — o haftanın kendisini — "
                    "kaçırırım. Sınırı burada çiziyorum ve ne için çizdiğimi de "
                    "söylüyorum.\n\n"
                    "Soru sormuyorum; hafta daha gelmedi ve şimdi soru sormak bir "
                    "karar istemek olur.",
    },
    8: {  # kumar · kisa/duzgun · multi · focusing · yalnizca_yansitma
        "turns": [
            ("user", "Bir yıl olmuştu temiz olalı."),
            ("assistant", "Olmuştu."),
            ("user", "Bugün tazminat yattı, gece girdim. Kafa dağıtmak içindi, "
                     "kazanmak için değil."),
            ("assistant", None),
        ],
        "son": "Bir yılı sen saydın, bugünü de sen söyledin. Aralarına \"kafa "
               "dağıtmak içindi\" diye bir ayrım koydun.\n\n"
               "O ayrımı koyman, ikisinin senin için aynı şey olmadığını "
               "gösteriyor.",
        "thinking": "Yaptığı şeyi küçültmüyor, ama niyetini ayırıyor: kazanmak için "
                    "değilmiş. Bu ayrım onun için bir şey ifade ediyor.\n\n"
                    "Ayrımın doğru olup olmadığını tartışmıyorum — tartışsam "
                    "savunmaya geçer ve bugünü anlatmaktan vazgeçer.\n\n"
                    "Bir yılı saymış olmasını da söylüyorum, çünkü sayan kişi o.\n\n"
                    "Soru sormuyorum. Bugün olan bir şeyi anlatan birine soru sormak "
                    "erken.",
    },
    9: {  # tutun · kisa/duzgun · multi · planning · acik_uclu_soru · yonlendirme_istegi · neg=1
        "turns": [
            ("user", "Yine paket aldım."),
            ("assistant", "Ne oldu bugün?"),
            ("user", "Hep bir şey bitince bırakırım diyorum. Bandı mı denesem, "
                     "hap mı? Hangisi işe yarar, siz söyleyin."),
            ("assistant", None),
        ],
        "son": "Hangisinin işe yarayacağını bilmiyorum ve tahmin etmem — ikisi de "
               "hekimin değerlendireceği şeyler.\n\n"
               "Ama şunu duydum: yıllardır \"bir şey bitince\" diyorsun ve bugün "
               "hangisini deneyeceğini soruyorsun. Bu ikisi aynı cümlede "
               "durmuyor.\n\n"
               "Bugün seni bu soruyu sormaya getiren ne oldu?",
        "thinking": "İki seçenek arasında seçim yapmamı istiyor ve ikisi de ilaç. "
                    "Cevabı bende yok ve tahmin edersem tavsiye vermiş olurum.\n\n"
                    "Reddederken formül kullanmıyorum; bilmediğimi ve tahmin "
                    "etmeyeceğimi söylüyorum.\n\n"
                    "Asıl fark ettiğim şey başka: yıllardır erteleyen biri bugün "
                    "yöntem soruyor. Erteleme ile yöntem sorusu aynı cümlede "
                    "durmuyor ve bunu gösteriyorum.\n\n"
                    "Soruyu bugüne soruyorum.",
    },
    10: {  # tutun · kisa/duzgun · multi · planning · ozet
        "turns": [
            ("user", "Dün akşam kızım damadım torunumla geldiler."),
            ("assistant", "Kalabalık bir akşam olmuş."),
            ("user", "Oldu. Ben hep mutfak penceresini aralayıp içerim, kimseyi "
                     "rahatsız etmem diye düşünürdüm. Dün torun mutfağa geldi."),
            ("assistant", None),
        ],
        "son": "Yıllardır kurduğun bir düzen var: pencere aralık, mutfak, kimseyi "
               "rahatsız etmemek. Dün o düzene mutfağa giren biri eklendi.\n\n"
               "\"Düşünürdüm\" dedin — geçmiş zamanla.",
        "thinking": "Bir düzeni anlatıyor ve düzenin dayanağı bir varsayım: kimseyi "
                    "rahatsız etmediği. Dün o varsayıma bir şey değmiş.\n\n"
                    "Torunun mutfağa girmesinden bir sonuç çıkarmıyorum — ne olduğunu "
                    "söylemedi ve ben ekleyemem.\n\n"
                    "Ama kipini gösteriyorum: \"düşünürdüm\" dedi, \"düşünüyorum\" "
                    "değil. Bu değişimi o yaptı.\n\n"
                    "Soru sormuyorum, topluyorum. Kipi duyması yeterli.",
    },
}

def _serbest(m: str) -> str:
    return BLOK.sub("", m).strip()


def _bant(m: str) -> str:
    n = len(_serbest(m).split())
    return "kisa" if n <= 8 else "orta" if n <= 25 else "uzun"


def main() -> int:
    plan = {json.loads(l)["sira"]: json.loads(l)
            for l in PLAN.read_text(encoding="utf-8").splitlines() if l.strip()}
    kayitlar, hata = [], []
    for sira in SIRALAR:
        p, k = plan[sira], KAYIT[sira]
        ctx, blok = [], ""
        if "baglam" in k:
            b = k["baglam"]
            blok = f'<context kaynak="{b["kaynak"]}">\n{b["metin"]}\n</context>'
            ctx = [{"kaynak": b["kaynak"], "metin": b["metin"], "sentetik": True}]
        msgs = [{"role": "system", "content": CANON}]
        for rol, icerik in k["turns"]:
            t = (icerik if icerik is not None else k["son"]).replace("<CTX>", blok)
            msgs.append({"role": rol, "content": t})
        msgs[-1]["thinking"] = k["thinking"]
        son = msgs[-1]["content"]
        ilk = next(m["content"] for m in msgs if m["role"] == "user")

        if (b2 := _bant(ilk)) != p["bicim"]:
            hata.append(f"#{sira} bicim beyan {p['bicim']} ↔ ölçülen {b2} "
                        f"({len(_serbest(ilk).split())} kelime)")
        if bool(ctx) != bool(p["context"]):
            hata.append(f"#{sira} context beyan {p['context']} ↔ {bool(ctx)}")
        soru = son.count("?")
        if soru > 1:
            hata.append(f"#{sira} soru {soru} > 1")
        if p["turn_ending"] == "acik_uclu_soru" and soru != 1:
            hata.append(f"#{sira} `acik_uclu_soru` ama soru {soru}")
        if p["turn_ending"] in ("takdir", "ozet", "yalnizca_yansitma", "durur") and soru:
            hata.append(f"#{sira} `{p['turn_ending']}` sorusuz olmalı, soru {soru}")
        # ⭐ YENİ: beyan ↔ metin, iki yönde
        # ⛔⛔⛔ BU KAPI SERT REDDEN OKUMA KUYRUĞUNA ÇEVRİLDİ (2026-09-20) ve
        # sebebi ölçülmüş bir çelişki: şablonlaşma taraması bu partide
        # *«sana ben söyleyemem»*i %11,9'da buldu (`v0.0.14`: %1,2) — yani
        # kapıları geçmek için kullandığım red ve özerklik CÜMLELERİ şablona
        # dönüşmüştü. Cümlenin kuruluşunu değiştirince kapı *«hamle yok»* dedi.
        # ➡️⭐⭐⭐ *Sözlükle kurulmuş bir kapı, bir EDİMİ değil bir FORMÜLÜ
        #    tanır; formülü zorunlu kılan kapı, şablonu da zorunlu kılar.*
        # İki yanlış cevap vardı: eski hâle dönmek (şablonu korumak) ve deseni
        # kendi yazdığım cümlelerle genişletmek (kapı hep bir varyasyon geride
        # kalır, ve kendi metnime göre ölçüt yazmak olurdu). ⇒ Üçüncü yol:
        # desen görmezse kayıt DÜŞMEZ, **elle onaya** düşer ve onay gerekçesiyle
        # birlikte betikte yazılı durur (`_muafiyet.py`nin deseni).
        # ⛔⛔ Onaylar KAYDA yazılmıyordu; yalnız bu betikte duruyordu.
        # Sonuç: `beyan-metin-uyumu` deseni tek başına ölçtü ve HER İKİ
        # partide de bütün elle onayları geri aldı (parti1: 20 23 28 35
        # 37 53 · parti2: 19 onay). ➡️ *Yumuşak kapının kararı kayda
        # yazılmazsa, bir sonraki ölçüm onu yok sayar.*
        onaylar: list[str] = []
        for alan, desen, ad in ((p["ozerklik"], OZERKLIK, "ozerklik_vurgusu"),
                                (p["is_negative"], RED, "is_negative")):
            if alan and not desen.search(son):
                onay = ELLE_ONAY.get((sira, ad))
                if onay is None:
                    hata.append(f"#{sira} `{ad}` beyan edildi, desen görmedi ve "
                                f"ELLE ONAY yok")
                elif onay not in son:
                    hata.append(f"#{sira} `{ad}` elle onayı metinde bulunamadı: "
                                f"«{onay[:40]}»")
                else:
                    onaylar.append(ad)
        for m in msgs[1:-1]:
            if m.get("thinking"):
                hata.append(f"#{sira} ara turda thinking (K44)")
        o = len(k["thinking"]) / max(1, len(son))
        if o > 4:
            hata.append(f"#{sira} thinking {o:.1f}x > 4x")
        isk = re.findall(r"ızgara|kota|beyan|§\d|K\d{1,3}\b|T\d{2,3}\b|Kural \d|parti\d",
                         k["thinking"], re.I)
        if isk:
            hata.append(f"#{sira} thinking iskelesi: {set(isk)}")

        gm = {"generator": "claude-code", "generator_model": "claude-opus-5",
              "prompt_version": "uretim-v5", "date": betik_tarihi(__file__),
              "system_prompt_variant": "canon", "parti": "v6-parti2",
              "parti_sira": sira, "seed_id": p["seed_id"],
              "turn_ending": p["turn_ending"], "konusma_durumu": p["konusma_durumu"],
              "bicim": p["bicim"], "register": p["register"],
              "sinir_tipi": p["sinir_tipi"], "senaryo_hedefi": p["senaryo_hedefi"],
              "ozerklik_vurgusu": bool(p["ozerklik"]), "tohum_havuzu": "seeds",
              "motivasyon_tohum": p["motivasyon_tohum"]}
        if ctx:
            gm["baglam_davranisi"] = k["baglam_davranisi"]
            gm["baglam_bicimi"] = "v1"
        # ⛔⛔ BU SATIR blok3'ten türetilen betiklerde YOKTU ve sapma gerekçeleri
        # kaynakta yazılıp KAYDA GEÇMİYORDU (`#48 51 59`). §2a iskelenin
        # `gen_meta.izgara_sapmasi`'na yazılmasını söylüyor — `thinking`e değil —
        # yani kayıt onu taşımazsa gerekçe hiçbir yerde yok demektir.
        # ➡️ *Bir gerekçeyi betiğe yazmak, onu kayda yazmak değildir.*
        if onaylar:
            gm["elle_onay"] = onaylar
        if "sapma" in k:
            gm["izgara_sapmasi"] = k["sapma"]
        assert ("sapma" in k) == ("izgara_sapmasi" in gm), f"#{sira} sapma kaydı düştü"

        # ⛔⛔ Buradaki parti adı SABİTTİ ve parti2 betikleri sed ile
        # türetildiği için 60 kaydın 58'i parti1 ile AYNI id'yi aldı.
        # ➡️ *Türetilen betikte değişmesi gereken her yer, değişmediğinde
        #    sessiz kalan bir yerdir.* Artık kaydın kendi partisinden gelir.
        rec = {"id": hashlib.sha256(f'{gm["parti"]}-{sira}'.encode()).hexdigest()[:24],
               "slice": "rag_tek_tur" if p["turn_type"] == "single" else "cok_tur",
               "scenario": p["tohum_senaryo"], "addiction_type": p["tur"],
               "motivation": p["motivasyon"], "mi_process": p["mi_process"],
               "talk_type": "change" if p["senaryo_hedefi"] == "serbest" else "sustain",
               "age_group": p["yas"], "turn_type": p["turn_type"], "messages": msgs,
               "context": ctx, "source_ids": [p["source_id"]], "is_crisis": False,
               "is_negative": bool(p["is_negative"]), "has_thinking": True,
               "judge": None, "replay": False, "gen_meta": gm}
        c = run_checks(rec)
        if not c.get("passed"):
            hata.append(f"#{sira} run_checks: {json.dumps(c, ensure_ascii=False)[:260]}")
        kayitlar.append(rec)

    if hata:
        print("⛔ KAPI REDDETTİ:")
        for h in hata:
            print("   " + h)
        return 1
    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in kayitlar),
                     encoding="utf-8")
    print(f"✅ {len(kayitlar)} kayıt geçti → {CIKTI.relative_to(KOK)}")
    for r in kayitlar:
        g = r["gen_meta"]
        u = _serbest(next(m["content"] for m in r["messages"] if m["role"] == "user"))
        print(f"   #{g['parti_sira']:2d} {g['bicim']:5s}/{g['register']:6s} "
              f"{r['turn_type']:6s} {g['turn_ending']:17s} · {len(u.split()):2d} kelime"
              + (f" · bağlam[{g['baglam_davranisi']}]" if r["context"] else "")
              + (" · RED" if r["is_negative"] else "")
              + (" · özerklik" if g["ozerklik_vurgusu"] else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
