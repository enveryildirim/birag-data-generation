#!/usr/bin/env python3
"""v6-parti4 üretim öncesi kriz taraması — 60 plan satırı, yazmadan ÖNCE.

⛔⛔ **Bu taramanın gerekçesi bir kaçırmadır.** T192: `v6-parti1 #29`'un tohumu
(*«belki herkesi rahatlatmak için ortadan çekilsem»*) **dört kapının dördünü
de** geçmişti; üretilmedi ve süzgeç genişletildi. T199: `v6-parti2 #54`'ü
yakalayan şey sınıfı değil **mesajıydı**. ➡️ *Bir süzgeç yalnız kendi
sözlüğünü tanır; tohum metni okunmadan üretime girmez.*

⭐ Hiçbir süzgeç yeniden tanımlanmadı (K97): beyan sınıfları
`2026-09-17-tohum-beyan-kriz-kapisi`ten, dolaylı desen
`2026-09-17-kriz-suzgeci-yanlis-negatif`ten, içerik taraması
`tohum_guvenlik.kriz_icerigi`ten, çıplak sınıf `...-v6-parti4-plan`dan gelir.

⛔ **Bu betik ELEMİYOR, İŞARETLİYOR.** Eleme kararı Kural 3 gereği elle verilir
ve gerekçesiyle birlikte rapora yazılır.

Çıktı: reports/analiz/2026-09-20-v6-parti4-on-tarama.md
"""
from __future__ import annotations

import json
import sys
from importlib import util as _iu
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
TARIH = Path(__file__).name[:10]
sys.path.insert(0, str(KOK / "src"))
PLAN = KOK / "data/plan/v6-parti4.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-v6-parti4-on-tarama.md"

# ⛔ ELLE VERİLEN HÜKÜM — her satır okunarak yazıldı, desenle değil.
#    Boş bırakılan satır «okundu, kriz yok» demektir; anahtar yalnız üretim
#    talimatı gerektirenlerde vardır.
# ⛔ ÜRETİLMEYECEK — Kural 3, gerekçesiyle.
ELENEN: dict[int, str] = {
    16: "⛔⛔⛔ Dün gece **mide yıkanmış**, bu sabah *«başka bir hap kaldı mı diye "
        "bakıyorum»* diyor; buna *«ben kötü bir anneyim»*, çocuğun ondan korkması "
        "ve *«nefes alamıyorum»* eşlik ediyor. Mide yıkamasının ertesi günü hap "
        "aranması, sürmekte olan bir kendine zarar riskinin biçimi. ⛔ Bu kaydın "
        "cevabını yazmak klinik/etik bir karardır (Kural 3) ⇒ ÜRETİLMEDİ, "
        "`gd-023` açıldı.",
}

# ⛔ ELLE VERİLEN HÜKÜM — her satır okunarak yazıldı, desenle değil.
OKUMA: dict[int, str] = {
    29: "⚠️ ÜRETİM NOTU — acilden taburcu, psikiyatri kontrolü iki hafta sonra, "
        "**titreme** sürüyor. §5a″ md.1 + md.3 ateşler: *«nasıl idare edeceğim»* "
        "bir idare yöntemi istiyor. Yöntem verilmeyecek; randevu tarihi yordamsal "
        "ve sorulabilir (parti2 `#59`'un hamlesi).",
    32: "⚠️ ÜRETİM NOTU — iki gündür ilaç yok + birkaç kadeh + baş dönmesi, "
        "bulantı, ve *«yatıp uyusam geçer mi»*. md.1 + md.3. «Geçer» de «geçmez» "
        "de hüküm olur; söylenecek tek şey bunun bugün bakılması gerektiği.",
    33: "⚠️ ÜRETİM NOTU — reçeteli uyarıcı + **arkadaştan alınan beta bloker** + "
        "çarpıntı, üstüne *«bu kombinasyon güvenli, araştırdım»*. md.1 + md.2. "
        "İtiraz kombinasyonun etkisine değil, *«araştırdım»*ın yeterli sayılmasına "
        "yapılacak (epistemik, `#19`/`#23`'ün biçimi).",
    38: "⚠️ ÜRETİM NOTU — lohusa, gece bebeğe kalkarken **şiddetli baş dönmesi**, "
        "*«düşersem onu nasıl tutarım»*. md.1 ateşler. ⛔ Ders verilmeyecek: "
        "zaten kendini yiyip bitirmiş ve kimseye söyleyememiş.",
    46: "⚠️ ÜRETİM NOTU — **elleri titriyor**, evde kalan tablet var ve *«yarım "
        "tane alsam belirtiler geçer mi»* diye soruyor. md.1 + md.2 + md.3; "
        "parti1 `#51` ve parti3 `#30` ile aynı aile ama orada belirti YOKTU.",
    53: "⚠️ ÜRETİM NOTU — **göğüs sıkışması ve nefes alamama**, kimseye "
        "söylememiş. md.1'in en açık hâli. Yarınki sunum ve ailenin bilmemesi "
        "ikinci planda kalacak.",
    10: "⛔⛔ ÜRETİM NOTU — alkolü ve reçeteli bir ilacı **aynı gün, birlikte, "
        "tamamen** kesme planı; üstüne *«mantıklı bir plan mı sizce»*. Partideki "
        "en tehlikeli plan ve doğrudan onay isteniyor. md.3. ⛔ Planın NEDEN "
        "riskli olduğu SÖYLENMEYECEK — o klinik içerik; söylenecek olan, böyle "
        "bir planın ilacı yazan hekimle kurulması gerektiği.",
    50: "⛔⛔ ÜRETİM NOTU — üç gündür sokakta, bu gece köprü altı, battaniye yok, "
        "sığınmaevini koğuş olduğu için reddediyor, ısınmak için içmiş. "
        "⭐ §5a″'nın dördü de KLİNİK; **barınma/maruz kalma gibi akut refah "
        "acilleri hiçbir maddeye girmiyor** ve bunu gösteren ilk tohum bu ⇒ "
        "`gd-022` açıldı. ⛔ Alkolün ısı üzerindeki etkisine dair bir şey "
        "SÖYLENMEYECEK (üretilmiş sağlık iddiası olur); reddettiği sığınmaevinin "
        "gerekçesi ciddiye alınacak ve başka barınma/sosyal hizmet yolları "
        "adlandırılacak.",
    12: "⚠️ ÜRETİM NOTU — yönlendirmeyi ÖNCEDEN yasaklıyor (*«beni hemen "
        "oraya geri yollamaya çalışmayın, yeni çıktım»*) ve ortada akut bedensel "
        "olay yok ⇒ parti3 `#47`'nin ölçütü: **yasağa uyulacak**. Kurum adı "
        "genelleştirilecek.",
    15: "⚠️ ÜRETİM NOTU — randevudan önce bir-iki gün bırakıp sonra söyleme planı; "
        "parti1 `#57` ile aynı hamle. Plana itiraz edilecek, yalana değil.",
    19: "⚠️ ÜRETİM NOTU — *«Stoklamak bağımlılık mı oldu şimdi?»* retorik ama "
        "klinik bir soru. Cevaplanmayacak; konuşulacak olan oğlunun telefonu.",
    24: "⚠️ ÜRETİM NOTU — kızı bilişsel bulanıklık fark etmiş, kullanıcı "
        "*«alakası yok»* diyor. İlacın bunu yapıp yapmadığı SÖYLENMEYECEK; "
        "itiraz *«yıllardır kullanıyorum, dün başlamadı»* çıkarımına.",
    27: "⚠️ ÜRETİM NOTU — *«Ben deli miyim?»* Psikiyatrinin gerekli olup olmadığı "
        "tartışılmayacak; karşılanacak şey damga.",
    31: "⚠️ ÜRETİM NOTU — elinde bardakla yazıyor ve *«babalığımı rakı söndürdü»* "
        "diyor. Şu an içiyor olması bir ders konusu yapılmayacak.",
    49: "⚠️ ÜRETİM NOTU — üç ay temizken kazanmış, kupon ekranda, KARAR ANINDA "
        "yazıyor. Kurum adı genelleştirilecek. ⛔ «Oynama» da «oyna» da "
        "denmeyecek; konuşulacak olan *«kazanmış olmak bir başarı gibi geliyor»*.",
    56: "⚠️⚠️ ÜRETİM NOTU — yalnızlık kümesi: sponsor üç gündür sessiz, kardeş "
        "iki haftadır konuşmuyor, *«herkes yoruldu benden, ben de kendimden "
        "yoruldum»*. ⛔ Okundu: ortada kaybolma isteği, yöntem ya da plan YOK; "
        "*«kendimden yoruldum»* Türkçede tükenmişlik deyimi ⇒ elenmedi. Ama "
        "cevaba **bir kişi daha eklenmeyecek** — üç kişi zaten susmuş durumda. "
        "Kurum adı genelleştirilecek.",
    36: "⚠️ Tohumun senaryo etiketi `kriz` ama METİNDE kriz yok: yarınki tedavi "
        "randevusuna gitmeme kararsızlığı. ⭐ Etiket değil metin okundu (T199'un "
        "dersi). Kurum özel adı genelleştirilecek (K110).",
    5: "⚠️ Kurum özel adı var (K110) — genelleştirilecek. İçerik temiz: kendini "
       "bir komşuyla karşılaştırıyor.",
    7: "⚠️ Kurum özel adı var (K110) — genelleştirilecek. *«Eşime söyleyeyim mi "
       "sence»* — bu kararı vermeyeceğim.",
}


def _modul(ad: str, yol: str):
    sp = _iu.spec_from_file_location(ad, KOK / yol)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def main() -> int:
    KRIZ = _modul("kriz", "scripts/analiz/2026-09-17-tohum-beyan-kriz-kapisi.py")
    DOL = _modul("dol", "scripts/analiz/2026-09-17-kriz-suzgeci-yanlis-negatif.py")
    # ⭐ Çıplak sınıfın TANIMI parti3 planlayıcısında yaşıyor (K97); parti4
    # planlayıcısı onu yeniden tanımlamıyor, çağırıyor. Tarama da öyle yapar.
    P3 = _modul("p3", "scripts/analiz/2026-09-20-v6-parti3-plan.py")
    import tohum_guvenlik as TG

    tohum = KRIZ._tohumlar()
    plan = [json.loads(l) for l in PLAN.read_text(encoding="utf-8").splitlines() if l.strip()]
    bulgu = []
    for r in plan:
        d = tohum[r["seed_id"]]
        meta = d.get("meta", {}) or {}
        v = []
        if (s := KRIZ._sinif(d)):
            v.append(f"beyan:{s}")
        if P3.ciplak_kriz(d):
            v.append("⛔ ÇIPLAK")
        if (tg := TG.kriz_icerigi(d)):
            v.append("TG:" + ",".join(tg))
        if DOL.DOLAYLI.search(r["tohum_metin"]):
            v.append("DOLAYLI")
        if (rs := meta.get("risk_seviyesi")) in ("yuksek", "cok_yuksek"):
            v.append(f"risk:{rs}")
        if v:
            bulgu.append((r["sira"], v, r["tohum_metin"], r["tur"], r["tohum_senaryo"]))

    icerik = [b for b in bulgu if any(not x.startswith("risk:") for x in b[1])]
    sat = [f"# v6-parti4 — üretim öncesi kriz taraması", "",
           f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
           f"**Girdi:** `{PLAN.relative_to(KOK)}` · **{len(plan)}** satır", "",
           "⛔⛔ T192: `v6-parti1 #29` **dört kapının dördünü de** geçmişti. "
           "T199: `#54`'ü yakalayan şey sınıfı değil **mesajıydı**. "
           "➡️ *Bir süzgeç yalnız kendi sözlüğünü tanır; tohum metni okunmadan "
           "üretime girmez.*", "",
           "| | |", "|---|---:|",
           f"| işaret taşıyan satır | **{len(bulgu)}** / {len(plan)} |",
           f"| — yalnız `risk_seviyesi` alanından | {len(bulgu) - len(icerik)} |",
           f"| ⛔ **içerik/beyan süzgeci ateşleyen** | **{len(icerik)}** |",
           f"| ⛔ **üretilmeyecek satır** | **{len(ELENEN)}** {sorted(ELENEN) or ''} |", "",
           # ⛔⛔ DEVRALINAN ŞERH YANLIŞ ÇIKTI. parti3'ün raporu «hiçbir süzgeç
           # ateşlemedi» ve «on dördünün tam metni okundu» diyordu; parti4'te
           # üçü ateşledi ve otuz dört satır var. ➡️ *Devralınan bir cümle,
           # devralan bağlamda sessizce yanlış olur* (T198'in aynısı).
           (f"⭐ **İçerik/beyan süzgeci ateşlemedi**; işaretlerin hepsi "
            "`risk_seviyesi` alanından geliyor ve o alan tek başına eleme ölçütü "
            "değil (SERT eşiği `cok_yuksek`)."
            if not icerik else
            f"⛔ **{len(icerik)} satır içerik/beyan süzgeci ateşledi** ve her biri "
            "aşağıda ayrı ayrı hükme bağlandı. Kalan işaretler "
            "`risk_seviyesi` alanından geliyor; o alan tek başına eleme ölçütü "
            "değil (SERT eşiği `cok_yuksek`)."),
           "",
           f"⛔ **İşaretli {len(bulgu)} satırın tam metni okundu.** Bu bir BETİK "
           "çıktısı değil, benim beyanımdır (K30); betik yalnız hangi satırların "
           "okunması gerektiğini söyler.", "",
           "## İşaretli satırlar", "",
           "| # | tür / senaryo | işaret | hüküm |", "|---:|---|---|---|"]
    for sira, v, _m, tur, sen in bulgu:
        # ⛔⛔ İLK SÜRÜM OKUNMAMIŞ SATIRA «okundu, kriz yok» DİYORDU — yani
        # olmayan bir insan hükmünü rapora yazıyordu. ➡️ *Bir raporun
        # varsayılan etiketi bir iddia taşıyorsa, o iddia hiç yapılmamış
        # olabilir.* Artık okunmamış satır açıkça öyle yazılır ve içerik/beyan
        # süzgeci ateşleyen bir satır okunmamışsa betik REDDEDER.
        if sira in ELENEN:
            h = "⛔⛔ **ÜRETİLMEYECEK**"
        elif sira in OKUMA:
            h = "⚠️ okundu, **üretim notu var**"
        elif any(not x.startswith("risk:") for x in v):
            h = "⛔ **OKUNMADI**"
        else:
            h = "⭐ okundu, kriz yok"
        sat.append(f"| {sira} | `{tur}` / `{sen}` | {' + '.join(v)} | {h} |")
    sat += ["", "## ⚠️ Üretim notları — eleme değil, talimat", ""]
    for sira, not_ in sorted(ELENEN.items()):
        sat += [f"**`#{sira}`** — {not_}", ""]
    for sira, not_ in sorted(OKUMA.items()):
        sat += [f"**`#{sira}`** — {not_}", ""]
    sat += ["## ⛔ Bu taramanın söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **«0 eleme» süzgeçlerin temiz olduğunu göstermez** | T192 tam "
            "tersini ölçtü: dördü de temiz derken kaçırmışlardı. Buradaki güvence "
            "süzgeç değil, **on dört metnin okunmuş olması** |",
            "| ⛔ **Okuma BENİM okumam** | K30 gereği üretimi ben yapıyorum ve "
            "hükümleri de ben veriyorum; uzman okuması değil |",
            "| ⛔ **`gd-021` açık** | çıplak *«İntihar düşüncesi»* sınıfı bu partiye "
            "düşmedi (havuzda 6 var); karar hâlâ verilmedi |",
            "| ⚠️ **Yalnız tohum metni okundu** | üretilecek konuşmanın kendisi "
            "üretim anında ayrıca kapılardan geçer |"]
    okunmamis = [b[0] for b in icerik if b[0] not in OKUMA and b[0] not in ELENEN]
    if okunmamis:
        print(f"⛔ İçerik/beyan süzgeci ateşleyen ve OKUNMAMIŞ satır: {okunmamis}")
        print("   Rapor yazılmadı — bu satırlar okunmadan parti planlanmış sayılmaz.")
        return 1
    RAPOR.write_text("\n".join(sat) + "\n", encoding="utf-8")
    print(f"✅ {len(plan)} satır tarandı · işaretli {len(bulgu)} · "
          f"içerik/beyan süzgeci {len(icerik)} · ⛔ elenen {len(ELENEN)} "
          f"{sorted(ELENEN) if ELENEN else ''} · üretim notu {len(OKUMA)}")
    print(f"→ {RAPOR.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
