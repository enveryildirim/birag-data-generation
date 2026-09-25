#!/usr/bin/env python3
"""§7a″ `celiskili` — ÜÇÜNCÜ PARTİ, 13 kayıt (banka no 13-25).

⛔⛔ **Neden 13.** `v0.0.21`'de sınıfın payı bağlamlı 234 kaydın **%5,1**'i;
§7a″ kotası **~%10**. 13 kayıt payı **25/247 = %10,1** yapar. Sayı
seçilmedi, **hesaplandı**.

⭐⭐ **T265'in dersi bu partinin yazım kuralıdır.** İlk 12 kaydın 3'ü
uydurmuştu ve mekanizma ölçülmüştü: *cevabı tohumdan yazmıştım, kullanıcı
mesajı ise tohumun kısaltmasıydı.* ⇒ Burada cevap **yalnız kendi yazdığım
kullanıcı mesajından ve iki pasajdan** kuruldu; tohum **kullanıcı mesajını**
yazmak için okundu, cevabı yazmak için **değil**.

⭐ **Üretim anında ÜÇ denetim:**
  1. `run_checks` — `celiskili_ok`, `bant_ok`, `yansitma_ok` dahil (sert).
  2. **T217** — her metin kendi tohumundan (parti içi karşılaştırmalı, sert).
  3. **B kuralı raporu** — 2. tekil şahıslı cümlelerdeki «yeni» kökler
     basılır. ⛔ Bu bir KAPI DEĞİL (kesinliği taban oranla aynı, T266);
     **ben okuyayım diye** basılır (K260: okuma bende).

⛔ Hedef bant bir NİYETtir; türetilenle uyuşmazsa kayıt düşer (T263/T264).

⛔ Güvenlik süzgeci öncekilerle aynı (Kural 3): risk ∈ {dusuk, orta} ·
`senaryo ≠ kriz` · `siddet_seviyesi ≠ agir`.

⛔ Klinik sınır: #22'de kullanıcı bir arkadaşının ilaç verdiğini ve
*«doktor olarak söylüyorum güvenli»* dediğini aktarıyor. Cevap ilacı
**adlandırmaz**, güvenli olup olmadığını **söylemez**, kullanılıp
kullanılmayacağına dair **hiçbir şey** demez (Kural 3).

Çıktı: data/candidates/celiskili-parti3.jsonl
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
from yansitma import yansitma_yeni  # noqa: E402

CIKTI = KOK / "data/candidates/celiskili-parti3.jsonl"
BANKA = {c["no"]: c for c in json.loads(
    (KOK / "data/celiskili-pasaj-bankasi.v2.json").read_text())["ciftler"]}
SISTEM = next(m["content"] for m in
              json.loads(open(KOK / "datasets/v0.0.18/train.jsonl").readline())["messages"]
              if m["role"] == "system")
# ⚠️ Tohum sözlüğü ile korpus alan adları birebir DEĞİL; eşleme AÇIK yazılır.
#   `tetikleyici_olay` korpusta da aynı adla var (9 kayıt).
# ⭐ Tek gerçek ayrım `ic_motivasyon` → `ic`; kalanlar korpusta aynı adla
#   geçiyor. Ama geçirmeden önce KORPUSTA VAR MI diye denetlenir — sessiz
#   yeni bir değer sokmak T240 ailesinin biçimidir.
MOT_AD = {"ic_motivasyon": "ic"}
MOT_GECERLI = {"ic", "aile_baskisi", "yasal_zorunluluk", "tetikleyici_olay",
               "duygusal_regulasyon"}


def mot(deger: str) -> str:
    v = MOT_AD.get(deger, deger)
    if v not in MOT_GECERLI:
        raise SystemExit(f"⛔ korpusta olmayan motivation değeri: {deger!r}")
    return v

YAS = {"ergen": "ergen", "yetiskin": "yetiskin", "orta_yas": "yetiskin",
       "genc_yetiskin": "yetiskin", "yasli": "yetiskin"}

# banka_no → tohum ön eki (K105: seçim deterministik betikte yapıldı,
#   sonucu BURAYA yazıldı ki üretim yeniden koşulabilsin)
TOHUM = {13: "c4fd4462be1a", 14: "deebd2c02c21", 15: "78454c484228",
         16: "8d2858fc8c37", 17: "ee736258f41e", 18: "071e0e04327a",
         19: "8cce0fb21d34", 20: "165292809f0a", 21: "c1db68573fde",
         22: "52b4ae9f2319", 23: "3a3dc6e66456", 24: "941a74afce31",
         25: "447dd8894b34"}

KAYITLAR = {
 13: dict(tur="tutun", senaryo="ambivalans", mi="engaging", talk="ambivalans",
          hedef_bant="uzun", turn_ending="yalnizca_yansitma",
          durum="suregiden_durum", sinir="yok", register="duzgun",
          user=("Merhaba. Çocuğum uyuduktan sonra balkona çıkıp sigara "
                "içiyorum, eşim bilmiyor. Sonra ağzıma sakız atıyorum. Bunu "
                "birine söylemek zor ama söyleyebileceğim kimse yok. Danışma "
                "birimine gitmeyi düşünüyorum, elimdeki iki yazı nerede "
                "yapıldığı konusunda ayrı şeyler söylüyor. Nereye gitmem "
                "gerekiyor?"),
          cevap=("Yer konusunda elimdeki iki not birbirini tutmuyor: biri "
                 "görüşmelerin birimin kendi binasında yapıldığını, öteki "
                 "bağlı bulunulan semt biriminde yürütüldüğünü yazıyor. İkisi "
                 "aynı anda geçerli olamaz ve hangisinin güncel olduğunu "
                 "buradan bilemem; bunu birime sorarak öğrenebilirsin.\n\n"
                 "«Söyleyebileceğim kimse yok» diye yazmışsın — ama bunu "
                 "şimdi yazdın."),
          thk=("İki pasaj yer konusunda çelişiyor; birini seçmiyorum, "
               "ortasını bulmuyorum, ikisini de adlandırıp birime "
               "yönlendiriyorum.\n\n"
               "Gizlemeyi yorumlamıyorum; eşine söylemesi gerektiğini "
               "söylemiyorum, o benim kararım değil.\n\n"
               "Sakız ayrıntısını yorumlamıyorum, sigara miktarına hiç "
               "girmiyorum.\n\n"
               "Yalnız kendi yazdığı cümleyi ona geri veriyorum; mesajda "
               "olmayan hiçbir şey eklemiyorum.")),

 14: dict(tur="alkol", senaryo="tetikleyici", mi="evoking", talk="ambivalans",
          hedef_bant="uzun", turn_ending="ozet",
          durum="tetikleyici_an", sinir="yok", register="duzgun",
          user=("Bugün öğleden sonra mülakattan olumsuz mail geldi. Hemen "
                "mutfağa indim, normalde akşam açtığım birayı öğleden sonra "
                "açtım. Programa katılmayı düşünüyorum ama ne kadar sürdüğünü "
                "çıkaramadım; elimdeki iki yazı ayrı şey söylüyor. Kaç hafta?"),
          cevap=("Süre konusunda elimdeki iki not çelişiyor: biri programın "
                 "toplam sekiz hafta sürdüğünü, öteki on iki hafta olarak "
                 "uygulandığını yazıyor. İkisinin arasını bulmuyorum; "
                 "hangisinin geçerli olduğunu birime sormak gerekiyor.\n\n"
                 "Yazdıklarını toparlayayım: olumsuz mail öğleden sonra "
                 "geldi, normalde akşam açtığın birayı öğleden sonra açtın — "
                 "ve aynı mesajda programa katılmayı düşündüğünü yazıyorsun."),
          thk=("İki pasaj süre konusunda çelişiyor. «Yaklaşık on hafta» "
               "demek ikisini birleştirip uydurmak olurdu; yapmıyorum.\n\n"
               "İçmesine tanı koymuyorum, «tetiklendin» demiyorum, miktar "
               "yorumu yapmıyorum, azaltma takvimi vermiyorum.\n\n"
               "Yalnız mesajda duran üç şeyi toparlıyorum: mailin saati, "
               "biranın normalden erken açılması, programa katılma düşüncesi. "
               "Üçü de onun cümlesi.\n\n"
               "Soru sormuyorum; özetle bitiriyorum.")),

 15: dict(tur="kumar", senaryo="ambivalans", mi="focusing", talk="change",
          hedef_bant="orta", turn_ending="takdir",
          durum="suregiden_durum", sinir="yok", register="bozuk",
          user=("abi 3 hafta önce 200 koydum 900 çıkardım, o günden beri her "
                "gece oranlara bakıyorum. görüşmelere başlasam kaç kere "
                "gelmezsem kaydım kapanır?"),
          cevap=("Devamsızlık konusunda elimdeki iki not birbirini tutmuyor: "
                 "biri iki görüşmeye katılmayanların kaydının kapatıldığını, "
                 "öteki sınırın dört görüşme olduğunu yazıyor. Hangisinin "
                 "geçerli olduğunu buradan bilemem; bunu birime sormak "
                 "gerekiyor.\n\n"
                 "Şunu da söyleyeyim: o günden beri her gece oranlara "
                 "baktığını yazacak kadar açık yazmışsın."),
          thk=("İki pasaj devamsızlık sınırında çelişiyor; ortalamasını "
               "almıyorum, birini seçmiyorum.\n\n"
               "Kazandığı tutara yorum yapmıyorum, «şanslıymışsın» ya da "
               "«bu tuzak» demiyorum; sayıyı hiç ele almıyorum.\n\n"
               "Sınavına ve uykusuna girmiyorum — mesajda var ama soru "
               "oraya değil, ve ben buradan bir şey kuramam.\n\n"
               "Açık yazmasını takdir edip bırakıyorum, soru sormuyorum.")),

 16: dict(tur="dijital", senaryo="belirsiz", mi="engaging", talk="change",
          hedef_bant="kisa", turn_ending="durur",
          durum="merak_sorusu", sinir="yok", register="duzgun",
          user="Gece bebeği beslerken bakıyorum. Kayıtlar ne kadar saklanıyor?",
          cevap=("Saklama konusunda elimdeki iki not çelişiyor: biri görüşme "
                 "kayıtlarının bir yıl, öteki beş yıl süreyle saklandığını "
                 "yazıyor. İkisi aynı anda doğru olamaz ve hangisinin geçerli "
                 "olduğunu bilmiyorum — bunu birime sormak gerekiyor.\n\n"
                 "«Gece bebeği beslerken» diye yazmışsın. Onu duydum."),
          thk=("İki pasaj saklama süresinde çelişiyor; «muhtemelen bir "
               "yıldır» demiyorum, ikisini de adlandırıyorum.\n\n"
               "Kaydın ne içerdiğine ya da kimin göreceğine dair hiçbir şey "
               "söylemiyorum — bunu da bilmiyorum ve uydurmam.\n\n"
               "Bebeği ve gece saatini yorumlamıyorum, uyku önerisi "
               "vermiyorum.\n\n"
               "Sorusu kısa ve tek bir şey soruyor; cevabı kısa tutup soru "
               "sormadan duruyorum.")),

 17: dict(tur="dijital", senaryo="ambivalans", mi="evoking", talk="ambivalans",
          hedef_bant="orta", turn_ending="durur",
          durum="plan_yapma", sinir="yok", register="duzgun",
          user=("Arkadaşım TikTok'u bıraktı, ben de düşünüyorum ama "
                "«bırakınca ne yapacağım» diye de düşünüyorum. Gruplar kaç "
                "kişi?"),
          cevap=("Grup mevcudu konusunda elimdeki iki not çelişiyor: biri "
                 "grupların en çok sekiz kişiden oluştuğunu, öteki mevcudun "
                 "on beş kişi olduğunu yazıyor. Hangisinin geçerli olduğunu "
                 "bilmiyorum; bunu birime sormak gerekiyor.\n\n"
                 "Kendi cümlende iki şey yan yana duruyor: bırakmayı "
                 "düşünüyorsun, ve «bırakınca ne yapacağım» diye "
                 "düşünüyorsun."),
          thk=("İki pasaj mevcutta çelişiyor; aradan bir sayı "
               "uydurmuyorum.\n\n"
               "Arkadaşının bırakmasını örnek göstermiyorum, «sen de "
               "yaparsın» demiyorum — kıyas baskı olurdu.\n\n"
               "«Bırakınca ne yapacağım» sorusuna cevap vermiyorum; o soruyu "
               "çözmek benim işim değil.\n\n"
               "İki ucu yan yana bırakıp duruyorum.")),

 18: dict(tur="tutun", senaryo="belirsiz", mi="engaging", talk="ambivalans",
          hedef_bant="orta", turn_ending="acik_uclu_soru",
          durum="merak_sorusu", sinir="yok", register="bozuk",
          user=("ben gerçekten grupta denemeyen tek kişiyim şu an, ortada "
                "kalıyorum bi şekilde. okuldan sonra uğrasam birim kaça kadar "
                "açık?"),
          cevap=("Kapanış saati konusunda elimdeki iki not çelişiyor: biri "
                 "birimin saat on yediye kadar açık olduğunu, öteki akşam "
                 "saat yirmiye kadar hizmet verdiğini yazıyor. Hangisinin "
                 "geçerli olduğunu bilmiyorum; bunu birime sormak "
                 "gerekiyor.\n\n"
                 "«Ortada kalıyorum» diye yazmışsın. Orası tam olarak neye "
                 "benziyor senin için?"),
          thk=("İki pasaj kapanış saatinde çelişiyor; birini seçmiyorum.\n\n"
               "Denemeyen tek kişi olmasını ne övüyorum ne de «dayan» "
               "diyorum; ikisi de baskı olurdu.\n\n"
               "Gruptaki arkadaşları hakkında hiçbir şey söylemiyorum, "
               "onlara dair yorum yapmıyorum.\n\n"
               "Kendi sözcüğünü alıp açık uçlu soruyorum.")),

 19: dict(tur="alkol", senaryo="rol_siniri", mi="planning", talk="change",
          hedef_bant="uzun", turn_ending="ozet",
          durum="plan_yapma", sinir="yok", register="duzgun",
          user=("Merhaba. Oğlum geçen hafta benimle oturup konuştu, içtiğimi "
                "fark etmiş, terapiye gitmemi istedi. Eşim de öğrendi ama "
                "«sen bilirsin» deyip uzaklaştı. Ben gerçekten bırakmak "
                "istiyorum. Sık sık şehir dışındayım; görüşmeler telefonla "
                "olur mu? İki yazı ayrı şey diyor."),
          cevap=("Görüşmenin biçimi konusunda elimdeki iki not birbirini "
                 "tutmuyor: biri görüşmelerin yalnızca yüz yüze yapıldığını, "
                 "öteki telefon üzerinden de yürütülebildiğini yazıyor. İkisi "
                 "aynı anda geçerli olamaz ve hangisinin güncel olduğunu "
                 "bilmiyorum; bunu birime sormak gerekiyor.\n\n"
                 "Yazdıklarını toparlayayım: oğlun oturup konuşmuş, eşin «sen "
                 "bilirsin» deyip uzaklaşmış, sen de gerçekten bırakmak "
                 "istediğini yazıyorsun."),
          thk=("İki pasaj görüşme biçiminde çelişiyor; «çoğunlukla yüz "
               "yüzedir» demiyorum, ikisini de adlandırıyorum.\n\n"
               "Bırakma planı kurmuyorum, takvim vermiyorum, hedef "
               "koymuyorum — istekli olması bunu istememi gerektirmiyor.\n\n"
               "Eşinin uzaklaşmasını yorumlamıyorum, taraf tutmuyorum.\n\n"
               "Yalnız mesajda duran üç şeyi toparlıyorum ve soru "
               "sormuyorum.")),

 20: dict(tur="kumar", senaryo="nazikce_karsi_cikma", mi="focusing",
          talk="sustain", hedef_bant="orta", turn_ending="yalnizca_yansitma",
          durum="suregiden_durum", sinir="sinir_cekme", register="bozuk",
          user=("ya kız arkadaşım son üç gündür bir tuhaf, mesajlara geç "
                "dönüyor. iddia yüzünden değil bence. birime gitsem sevk "
                "falan gerekiyor mu?"),
          cevap=("Sevk konusunda elimdeki iki not çelişiyor: biri başvuru "
                 "için hekim sevki gerektiğini, öteki başvuruların sevk "
                 "olmaksızın doğrudan alındığını yazıyor. Hangisinin geçerli "
                 "olduğunu buradan bilemem; bunu birime sormak gerekiyor.\n\n"
                 "Kız arkadaşının neden geç döndüğünü ben bilemem — onu "
                 "ancak o söyleyebilir.\n\n"
                 "Sen «iddia yüzünden değil bence» diye yazmışsın. «Bence» "
                 "demişsin."),
          thk=("İki pasaj sevkte çelişiyor; birini seçmiyorum.\n\n"
               "Kız arkadaşının davranışını yorumlamıyorum, sebep "
               "atamıyorum; bilmiyorum ve uydurmam. Bu bir sınır.\n\n"
               "«İddia yüzünden değil» demesine karşı çıkmıyorum da "
               "onaylamıyorum; kendi «bence»sini geri veriyorum.\n\n"
               "Soru sormuyorum.")),

 21: dict(tur="receteli_ilac", senaryo="ambivalans", mi="engaging",
          talk="ambivalans", hedef_bant="uzun",
          turn_ending="yalnizca_yansitma", durum="suregiden_durum",
          sinir="yok", register="duzgun",
          user=("Bugün çocuklar yine geldi, yemekten sonra «baba seninle "
                "gurur duyuyoruz, plana sadık kal» dediler. Ben gülümsedim "
                "ama içimden «sanki ben hasta bir çocuğum» dedim. Bu yaşta "
                "benim gibi birini alıyorlar mı oraya? Elimdeki iki yazı ayrı "
                "şey diyor."),
          cevap=("Yaş konusunda elimdeki iki not birbirini tutmuyor: biri "
                 "hizmet için üst yaş sınırı bulunmadığını, öteki hizmetin "
                 "altmış beş yaşına kadar verildiğini yazıyor. Hangisinin "
                 "geçerli olduğunu buradan bilemem; bunu birime sorarak "
                 "öğrenebilirsin.\n\n"
                 "İki cümleni yan yana koyayım: «gülümsedim» diye yazmışsın, "
                 "hemen ardından da içinden «sanki ben hasta bir çocuğum» "
                 "dediğini. İkisi de senin."),
          thk=("İki pasaj yaş sınırında çelişiyor; «yaşın sorun değil» demek "
               "uydurma olurdu çünkü hangisinin geçerli olduğunu "
               "bilmiyorum.\n\n"
               "Plandan söz ediyor ama plana dair hiçbir şey söylemiyorum: "
               "ne sadık kalmasını ne de değiştirmesini öneriyorum. İlaç, "
               "doz, miktar hiç geçmiyor.\n\n"
               "Çocuklarının sözünü yorumlamıyorum, «iyi niyetliler» "
               "demiyorum.\n\n"
               "İki cümlesini yan yana bırakıyorum, soru sormuyorum.")),

 22: dict(tur="receteli_ilac", senaryo="rol_siniri", mi="engaging",
          talk="sustain", hedef_bant="orta", turn_ending="durur",
          durum="tetikleyici_an", sinir="rol_siniri_yonlendirme",
          register="duzgun",
          user=("Arkadaşım kendi ilacından veriyor, «doktor olarak "
                "söylüyorum güvenli» diyor. Başka ilçede oturuyorum, oradan "
                "yararlanabilir miyim?"),
          cevap=("İkamet konusunda elimdeki iki not çelişiyor: biri "
                 "hizmetten ilçede ikamet edenlerin yararlanabildiğini, öteki "
                 "ikamet şartı aranmadığını yazıyor. Hangisinin geçerli "
                 "olduğunu bilmiyorum; bunu birime sormak gerekiyor.\n\n"
                 "Arkadaşının verdiğinin güvenli olup olmadığını ben "
                 "söyleyemem; kullanılıp kullanılmayacağı hakkında da bir şey "
                 "söylemem. Onu ancak seni gören bir hekim söyleyebilir.\n\n"
                 "Şunu fark ettim: «doktor olarak söylüyorum» cümlesini sen "
                 "aktarmışsın."),
          thk=("İki pasaj ikamette çelişiyor; birini seçmiyorum.\n\n"
               "⛔ İlacı adlandırmıyorum, ne olduğunu sormuyorum, güvenli "
               "olup olmadığını söylemiyorum, kullan ya da kullanma "
               "demiyorum. Miktar, süre, etki — hiçbiri geçmiyor.\n\n"
               "Arkadaşının yetkisini de tartışmıyorum; «o doktor değil» ya "
               "da «doktorsa haklıdır» demiyorum. İkisi de benim işim "
               "değil.\n\n"
               "Yalnız cümlenin kime ait olduğunu geri veriyorum ve "
               "duruyorum.")),

 23: dict(tur="tutun", senaryo="belirsiz", mi="evoking", talk="ambivalans",
          hedef_bant="uzun", turn_ending="acik_uclu_soru",
          durum="suregiden_durum", sinir="yok", register="duzgun",
          user=("Yağmurlu bir salı. Çocuklar gitti, ben çayımla sigaramla "
                "buradayım. Dün de aynıydı, önceki gün de. Bazen "
                "düşünüyorum, ben günlerimi mi geçiriyorum yoksa günler beni "
                "mi. Randevu alsam, gelemezsem kaç saat önce haber vermem "
                "gerekir?"),
          cevap=("İptal bildirimi konusunda elimdeki iki not çelişiyor: biri "
                 "görüşme iptalinin en az yirmi dört saat önce bildirilmesi "
                 "gerektiğini, öteki kırk sekiz saat önceden haber verilmesi "
                 "gerektiğini yazıyor. İkisinin arasını bulmuyorum; "
                 "hangisinin geçerli olduğunu birime sormak gerekiyor.\n\n"
                 "«Ben günlerimi mi geçiriyorum yoksa günler beni mi» diye "
                 "yazmışsın — ve aynı mesajda randevudan söz ediyorsun. Bu "
                 "ikisi sende nasıl yan yana duruyor?"),
          thk=("İki pasaj iptal süresinde çelişiyor; «otuz altı saat» gibi "
               "bir orta yol uydurmuyorum.\n\n"
               "Cümlesini şiirsel bulup övmüyorum, yorumlamıyorum, "
               "«depresyon» gibi hiçbir ad koymuyorum.\n\n"
               "Sigarasına ve çayına yorum yapmıyorum, bırakma önermiyorum."
               "\n\n"
               "Kendi cümlesiyle kendi sorusunu yan yana koyup ona "
               "soruyorum.")),

 24: dict(tur="alkol", senaryo="tetikleyici", mi="focusing", talk="change",
          hedef_bant="orta", turn_ending="takdir",
          durum="tetikleyici_an", sinir="yok", register="duzgun",
          user=("Dönüş yolunda kendimi şişeyi düşünürken yakaladım, henüz eve "
                "varmamıştım. O an korktum kendimden. Annem Türkçe bilmiyor; "
                "görüşme hangi dilde yapılıyor?"),
          cevap=("Dil konusunda elimdeki iki not birbirini tutmuyor: biri "
                 "görüşmelerin yalnızca Türkçe yürütüldüğünü, öteki talep "
                 "hâlinde başka dillerde de yapılabildiğini yazıyor. "
                 "Hangisinin geçerli olduğunu buradan bilemem; bunu birime "
                 "sormak gerekiyor.\n\n"
                 "Şunu da söyleyeyim: «O an korktum kendimden» diye yazacak "
                 "kadar açık yazmışsın."),
          thk=("İki pasaj dilde çelişiyor; birini seçmiyorum.\n\n"
               "Korkusunu hafifletmiyorum, «normaldir» demiyorum; bu onun "
               "cümlesi ve öyle duruyor.\n\n"
               "Şişeyi düşünmesine tanı koymuyorum, evre adı vermiyorum, "
               "bırakma önerisi kurmuyorum.\n\n"
               "Annesinin gelip gelmeyeceğine dair bir şey söylemiyorum — "
               "onu bilmiyorum.\n\n"
               "Açık yazmasını takdir edip bırakıyorum.")),

 25: dict(tur="kumar", senaryo="ambivalans", mi="engaging", talk="sustain",
          hedef_bant="kisa", turn_ending="durur",
          durum="aradan_donus", sinir="yok", register="duzgun",
          user="Dün yazdıklarım için abartmışım galiba. Sonuç nasıl bildiriliyor?",
          cevap=("Bildirim konusunda elimdeki iki not çelişiyor: biri görüşme "
                 "sonucunun yazılı olarak bildirildiğini, öteki bildirimin "
                 "sözlü yapıldığını yazıyor. İkisi aynı anda geçerli olamaz "
                 "ve hangisinin doğru olduğunu bilmiyorum; bunu birime sormak "
                 "gerekiyor.\n\n"
                 "«Abartmışım galiba» demişsin. Dün yazdıkların da duruyor."),
          thk=("İki pasaj bildirimde çelişiyor; birini seçmiyorum.\n\n"
               "«Abartmamışsın» demiyorum, «haklısın abartmışsın» da "
               "demiyorum — ikisi de onun yerine karar vermek olurdu.\n\n"
               "Dün ne yazdığını bilmiyorum ve tahmin etmiyorum; yalnız "
               "kendi andığı şeyi anıyorum.\n\n"
               "Kısa soruya kısa cevap, soru sormadan duruyorum.")),
}

DURAK = set("""bir bu ve de da ama için ne mi mu mı diye ben sen o var yok
gibi çok daha en ile göre sonra önce kadar şey bunu şu olarak yine ki
merhaba abi ya""".split())


def _ayirt(metin: str) -> set[str]:
    return {w for w in re.findall(r"\w{4,}", metin.lower()) if w not in DURAK}


def main() -> int:
    ham = [json.loads(l) for l in open(KOK / "data/seeds.v2.jsonl")]
    onceki = set()
    for f in ("celiskili-pilot", "celiskili-parti2"):
        for l in open(KOK / f"data/candidates/{f}.jsonl"):
            onceki.add(json.loads(l)["gen_meta"]["seed_id"])

    tohum = {}
    for no, on_ek in TOHUM.items():
        aday = [t for t in ham if t["seed_id"].startswith(on_ek)]
        if len(aday) != 1:
            raise SystemExit(f"⛔ #{no}: tohum ön eki tekil değil ({len(aday)})")
        t = aday[0]
        m = t["meta"]
        # ⛔⛔ Güvenlik süzgeci burada TEKRAR koşar (seçim betiğine güvenilmez)
        if not (m.get("risk_seviyesi") in {"dusuk", "orta"}
                and m.get("senaryo") != "kriz"
                and m.get("siddet_seviyesi") != "agir"):
            raise SystemExit(f"⛔ #{no}: tohum güvenlik süzgecinden geçmiyor")
        if t["seed_id"] in onceki:
            raise SystemExit(f"⛔ #{no}: tohum önceki partilerde kullanılmış")
        tohum[no] = t

    kayitlar, hata = [], []
    for i, (no, k) in enumerate(sorted(KAYITLAR.items()), 1):
        t, c = tohum[no], BANKA[no]
        m = t["meta"]
        ctx = "\n\n".join(f'<context kaynak="{p["kaynak"]}">\n{p["metin"]}\n</context>'
                          for p in c["context"])
        r = {
            "id": hashlib.sha256(f"celiskili3-{t['seed_id']}-{no}".encode()).hexdigest()[:24],
            "messages": [
                {"role": "system", "content": SISTEM},
                {"role": "user", "content": f"{ctx}\n\n{k['user']}"},
                {"role": "assistant", "content": k["cevap"], "thinking": k["thk"]}],
            "context": c["context"],
            "scenario": k["senaryo"], "addiction_type": k["tur"],
            "motivation": mot(m["motivasyon"]), "mi_process": k["mi"],
            "talk_type": k["talk"], "age_group": YAS[m["yas_grubu"]],
            "turn_type": "single", "is_crisis": False, "is_negative": True,
            "has_thinking": True, "replay": False,
            "source_ids": [t.get("source_id") or t["seed_id"]],
            "gen_meta": {
                "generator": "claude-code", "generator_model": "claude-opus-5",
                "prompt_version": "uretim-v5", "date": betik_tarihi(__file__),
                "system_prompt_variant": "canon", "parti": "celiskili-parti3",
                "parti_sira": i, "seed_id": t["seed_id"],
                "baglam_davranisi": "celiskili", "baglam_bicimi": "v1",
                "turn_ending": k["turn_ending"], "konusma_durumu": k["durum"],
                "sinir_tipi": k["sinir"], "register": k["register"],
                "tohum_havuzu": "seeds", "celiskili_banka_no": no},
            "judge": None,
        }
        r["slice"] = dilim(r)
        r["gen_meta"]["bicim"] = bant(r)      # ⭐ T263: türetme, beyan değil

        if r["gen_meta"]["bicim"] != k["hedef_bant"]:
            hata.append((no, f"niyet={k['hedef_bant']} ≠ türetilen="
                             f"{r['gen_meta']['bicim']}"))
        chk = run_checks(r)
        if not chk["passed"]:
            hata.append((no, str([f"{a}={v}" for a, v in chk.items()
                                  if a.endswith("_error") and v][:3])))
        kayitlar.append((no, t, r))

    # ⛔ T217 KAPISI — parti içi karşılaştırmalı
    for no, t, r in kayitlar:
        benim = _ayirt(t["user_message"] + " " + (t.get("scenario_context") or ""))
        metin = _ayirt(KAYITLAR[no]["user"])
        kendi = len(metin & benim)
        baska = max((len(metin & _ayirt(t2["user_message"] + " "
                                        + (t2.get("scenario_context") or "")))
                     for n2, t2, _ in kayitlar if n2 != no), default=0)
        if kendi == 0 or kendi <= baska:
            hata.append((no, f"T217: kendi tohumuyla {kendi}, başkasıyla {baska}"))

    if hata:
        for no, h in hata:
            print(f"⛔ banka#{no}: {h}")
        raise SystemExit(f"⛔ {len(hata)} kusur — HİÇBİR KAYIT YAZILMADI")

    CIKTI.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n"
                             for _, _, r in kayitlar), encoding="utf-8")
    assert CIKTI.exists() and sum(1 for _ in open(CIKTI)) == len(kayitlar)

    s = lambda f: dict(collections.Counter(f(r) for _, _, r in kayitlar))
    print(f"⭐ {len(kayitlar)} kayıt · kapılar {len(kayitlar)}/{len(kayitlar)} GEÇTİ")
    print(f"   banka: {sorted(no for no, _, _ in kayitlar)}")
    print(f"   tür:        {s(lambda r: r['addiction_type'])}")
    print(f"   bicim:      {s(lambda r: r['gen_meta']['bicim'])} (türetildi)")
    print(f"   turn_ending:{s(lambda r: r['gen_meta']['turn_ending'])}")
    print(f"   mi_process: {s(lambda r: r['mi_process'])}")
    print(f"   yaş:        {s(lambda r: r['age_group'])}")
    print(f"→ {CIKTI.relative_to(KOK)}")

    # ── ⛔ B KURALI RAPORU — KAPI DEĞİL, BEN OKUYAYIM DİYE (K260) ──
    print("\n── B kuralı (rapor, kapı değil): 2. tekil şahıslı cümlelerde "
          "konuşmada bulunmayan kökler ──")
    for no, _, r in kayitlar:
        for cumle, yeni in yansitma_yeni(r):
            print(f"  #{no:2} {yeni} ← «{cumle[:70]}»")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
