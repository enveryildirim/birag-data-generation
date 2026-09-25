# -*- coding: utf-8 -*-
"""v4-parti2 Blok 1 — §8b'nin ÖNCE YAZILMIŞ düzeltme ölçütünün denetimi (T24).

⛔ Ölçüt üretimden önce yazıldı (`prompts/uretim-v4.md` §8b), burada gevşetilmiyor:
  1. `yonlendirme_istegi` + `rol_siniri_yonlendirme` kayıtlarının **hepsinde** son
     cevapta kaynağın **türünü** adlandıran ve bir **adım** gösteren cümle bulunur.
  2. `yonlendirme_gereksiz` kayıtlarının **hiçbirinde** yönlendirme cümlesi bulunmaz.
  3. Hiçbir kayıtta rakam yok ve model kurum **özel adını** kendisi atmaz.
  4. Sayım envanter betiğinin **aynı ayrımını** kullanır (sınır çekme ≠ yönlendirme)
     ve sonuç **elle okunarak** doğrulanır. Terim sayısı tek başına kanıt değildir.

⭐ Betiğin rolü: ADAY LİSTELEMEK ve SERT taramaları yapmak (rakam, kurum özel adı).
   Sınıf kararı `ELLE` sözlüğünde, cümle numarasıyla ve gerekçesiyle yazılıdır —
   aynı desen: `2026-09-15-v002-yonlendirme-envanteri.py::ETIKET`.

⚠️ Terim listesi o betikten **import edilir**, kopyalanmaz. Tek fark katlama:
   orası düz `.lower()` kullanıyor (2026-09-15, yasaktan önce), burası `tr_fold`
   (Kural 4). tr_fold i-sınıfını çökerttiği için **daha kapsayıcı**; yani buradaki
   terim sayısı o betiğinkinden küçük ÇIKAMAZ.
"""
from __future__ import annotations

import hashlib
from collections import Counter
import importlib.util
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(KOK / "src"))

from checks import _last_assistant, _sentences, detect_number_candidates  # noqa: E402
from tohum_guvenlik import tr_fold  # noqa: E402

GIRDI = KOK / "data/candidates/v4-parti2.jsonl"
CIKTI = KOK / "reports/analiz/2026-09-16-parti2-blok1-8b-denetimi.json"
ENVANTER = KOK / "scripts/analiz/2026-09-15-v002-yonlendirme-envanteri.py"
RAPOR = KOK / "scripts/analiz/2026-09-15-v4-korpus-hedef-raporu.py"


def _yukle(yol: Path, ad: str):
    spec = importlib.util.spec_from_file_location(ad, yol)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# K18/K110 — model bu ÖZEL adları kendisi atmaz. Kullanıcı andıysa yansıtabilir,
# o yüzden tarama SON ASİSTAN CEVABINDA yapılır ve kullanıcı turlarıyla karşılaştırılır.
KURUM_OZEL_AD = [
    "amatem", "çematem", "cematem", "yedam", "alo 191", "yeşilay", "yesilay",
    "adsız alkolikler", "anonim alkolikler", "kumarbazlar anonim",
    "sağlık bakanlığı", "kızılay", "türkiye bağımlılıkla mücadele",
]

# ─── ELLE OKUNMUŞ. parti_sira -> (tür_adı cümlesi, adım cümlesi, not) ───
# None = o öge YOK. Sayılar `_sentences()` indeksidir; betik cümleyi rapora basar,
# yani numara boşa yazılamaz.
ELLE: dict[int, tuple[int | None, int | None, str]] = {
    1:  (1, 3, "iki tür yer sayılıyor (poliklinik · danışmanlık merkezi); adım «raporu yazan hekime sormak»"),
    2:  (4, 5, "tür: «sigara bırakma üzerine çalışan poliklinikler»; adım: bugünkü hekime sormak"),
    3:  (2, 4, "tür: aile hekimi + danışmanlık merkezleri; adım kullanıcının KENDİ cümlesini söylemek"),
    4:  (4, 6, "⚠️ türü kullanıcı andı («psikolojik danışma merkezi»), model yansıttı ve adımı O ekledi"),
    5:  (4, 5, "tür: danışmanlık merkezleri + hastane bağımlılık birimleri; adım: ilk imzada sormak"),
    6:  (7, 9, "tür: «seni ve ilacını bilen bir hekim»; adım: ilacı yazan hekime TEK soru"),
    7:  (2, 3, "tür: «ilacı yazan hekim»; adım: soruyu olduğu gibi sormak"),
    8:  (3, 4, "tür: «dozu azaltan hekim»; adım: cümlenin kendisi veriliyor"),
    9:  (1, 1, "tek cümlede hem tür hem adım — kısa kayıt, bölünmedi"),
    10: (1, 3, "tür: hekim / ruh sağlığı uzmanı, sonra merkez+birim; adım: iki cümleyi anlatmak"),
    11: (7, 7, "İKİ ayrı tür, iki ayrı sorun için: avukat (hukuk) · danışmanlık merkezi (içki)"),
    12: (5, 7, "tür: reçete yazabilecek hekim + poliklinik; adım: kutuyu yanına alıp götürmek. "
               "⚠️ [6] «böyle sorular için var» amaç cümlesi — yordam (sıra/ücret/süre) DEĞİL, sınırda kabul"),
    13: (None, None, "talep yok; yalnız yansıtma. Hiçbir yer anılmıyor"),
    14: (None, None, "«bana bir şey söyleme, sadece dinle» — kural aynen uygulandı"),
    15: (None, None, "⚠️ [1] terapisti ANIYOR ama model bir yer ÖNERMİYOR: kullanıcının "
                     "kendi kurduğu düzenin yansıtılması. Yeni kaynak yok, adım yok"),
    16: (None, None, "kullanıcı zaten destekte; model yeni yer önermiyor"),
    17: (None, None, "yalnız sınır: «eşine ne diyeceğini benim yazmam doğru olmaz»"),
    18: (None, None, "yalnız sınır: «o soru sana soruldu, bana değil»"),
    19: (None, None, "yalnız sınır + özerklik; kadeh kararına dair cümle YOK (ergen)"),
    20: (None, None, "yalnız sınır: «benim ne dediğim o masada bir şey değiştirmez»"),
    # ── Blok 2 (sira 21-38) · `sinir_tipi: yok` ──────────────────────────────
    # ⭐ `yok` beyanı da SINANIR: yönlendirme içeren bir kayıt `yok` diye beyan
    # edilirse beyan yanlıştır ve §8b'nin dilim sayımı bozulur.
    21: (None, None, "yalnız MI; hiçbir kaynak anılmıyor"),
    22: (None, None, "ergen; «normal mi» sorusu cevaplanıyor, yönlendirme yok"),
    23: (None, None, "yalnızca yansıtma"),
    24: (None, None, "durur — «buradayım»; kaynak anılmıyor"),
    25: (None, None, "takdir + özerklik; kaynak anılmıyor"),
    26: (None, None, "durur; ergen, kapı açık bırakılıyor"),
    27: (None, None, "özet; eşin bırakmış olması anlatılıyor, yer önerilmiyor"),
    28: (None, None, "planlama sorusu; kaynak anılmıyor"),
    29: (None, None, "takdir + özerklik"),
    30: (None, None, "⚠️ «doktor» geçiyor — KULLANICININ kendi doktoru, yansıtma; model yönlendirmiyor"),
    31: (None, None, "nazik itiraz + takdir; yer önerilmiyor, borcun rakamına girilmiyor"),
    32: (None, None, "⚠️ «doktor» üç kez geçiyor, üçü de kullanıcının kendi doktoru; yönlendirme yok"),
    33: (None, None, "kullanıcının çizdiği sınır kabul ediliyor + takdir"),
    34: (None, None, "«hazır bir cevabım yok» bilgi sınırı; yer önerilmiyor"),
    35: (None, None, "planlama sorusu; kaynak anılmıyor"),
    36: (None, None, "korkuya dönülüyor; hekim/ilaç yönlendirmesi YOK"),
    37: (None, None, "özet, tek tur; kaynak anılmıyor"),
    38: (None, None, "kayma sonrası takdir; kaynak anılmıyor"),
    # ── Blok 3 (sira 39-60) · `sinir_tipi: yok`, 6'sı bağlamlı ──────────────
    # ⭐ Bağlamlı kayıtlarda ayrım 2026-09-15 envanterinin `baglam_siniri`
    # sınıfıdır: terim/kaynak PASAJIN içinden gelir ve kullanıcı SORMUŞTUR;
    # model kendi inisiyatifiyle bir kaynak önermez. Kural: `yok` beyanı,
    # modelin KENDİ İNİSİYATİFİYLE tür adlandırıp adım göstermemesidir.
    39: (None, None, "ültimatom anı; yalnız MI, kaynak anılmıyor"),
    40: (None, None, "⚠️ §7a izin_iste — model PASAJI paylaşmayı öneriyor, kendi "
                     "kaynağını önermiyor; adım yok, izin bekleniyor"),
    41: (None, None, "soru cevaplanmıyor + takdir; kaynak anılmıyor"),
    42: (None, None, "planlama sorusu; ilaç/hekim yönlendirmesi YOK"),
    43: (None, None, "⚠️ bağlamdan aktarım (`baglam_siniri`) — kullanıcı SORDU, "
                     "cevap panodaki metinde; model kendi kaynağını önermiyor"),
    44: (None, None, "özet; kaynak anılmıyor, borç rakamına girilmiyor"),
    45: (None, None, "planlama sorusu; kaynak anılmıyor"),
    46: (None, None, "ergen, okul yönlendirmesi anlatılıyor; model yönlendirmiyor"),
    47: (None, None, "hakemlik reddi + takdir; kaynak anılmıyor"),
    48: (None, None, "ergen, özet; kaynak anılmıyor"),
    49: (None, None, "özet + özerklik; tarih/adım KONMUYOR"),
    50: (None, None, "⚠️ §7a cevap_yok — «bu metinde yazmıyor» deniyor, yerine "
                     "kaynak önerilmiyor (uydurma da yok)"),
    51: (None, None, "iki ses arasında seçim reddi + özerklik"),
    52: (None, None, "⚠️ §7a ilgisiz — pasaj hiç anılmıyor, MI sürüyor"),
    53: (None, None, "özet; kaynak anılmıyor"),
    54: (None, None, "«içme demeyeceğim» + takdir; kaynak anılmıyor"),
    55: (None, None, "⚠️ bağlamdan aktarım — iki yordam sorusu SORULDU, cevap "
                     "pasajda; model kendi kaynağını önermiyor"),
    56: (None, None, "aradan dönüş özeti; kaynak anılmıyor"),
    57: (None, None, "etiket reddi; kaynak anılmıyor"),
    58: (None, None, "durur; kaynak anılmıyor"),
    59: (None, None, "⚠️ bağlamdan aktarım — iki yordam sorusu SORULDU, cevap "
                     "panodaki yazıda; model kendi kaynağını önermiyor"),
    60: (None, None, "yalnızca yansıtma; kaynak anılmıyor"),
}

GEREKLI = {"yonlendirme_istegi", "rol_siniri_yonlendirme"}
YASAK = {"yonlendirme_gereksiz", "yok"}
YALNIZ_SINIR = {"sinir_cekme"}


def main() -> None:
    # ⭐⭐ İKİ ayrı liste, ikisi de repoda, ikisi de "yönlendirme"yi ölçüyor:
    #   · EVAL listesi (16 terim) — `evals/safety_crisis.jsonl` sk-013/sk-020'nin
    #     `herhangi_biri` alanı. Faz 5'te PUANI bu belirleyecek.
    #   · RAPOR listesi (21 terim) — üretim tarafının kendi aday listesi; 5 terim
    #     fazlası var ve beşi de tam olarak KURUM KATEGORİSİ sözcükleri
    #     (danışmanlık · merkez · birim · avukat · müdürlük).
    # İkisi import edilir, kopyalanmaz.
    env = _yukle(ENVANTER, "envanter_0915")
    rap = _yukle(RAPOR, "rapor_0915")
    ham = GIRDI.read_bytes()
    kayitlar = [json.loads(s) for s in ham.decode("utf-8").splitlines() if s.strip()]

    satirlar, hata = [], []
    for k in kayitlar:
        gm = k["gen_meta"]
        sira, st = gm["parti_sira"], gm["sinir_tipi"]
        cevap = _last_assistant(k)["content"]
        cumleler = _sentences(cevap)
        kullanici = " ".join(m["content"] for m in k["messages"] if m["role"] == "user")

        # --- SERT taramalar (makine) ---
        rakam = detect_number_candidates(cevap)
        c_fold, u_fold = tr_fold(cevap), tr_fold(kullanici)
        ozel = [a for a in KURUM_OZEL_AD if tr_fold(a) in c_fold]
        ozel_modelden = [a for a in ozel if tr_fold(a) not in u_fold]

        # --- terim sayımı: KANIT DEĞİL, karşılaştırma için ---
        terim = [t for t in env.TERIMLER if tr_fold(t) in c_fold]
        terim_genis = [t for t in rap.TERIMLER if tr_fold(t) in c_fold]

        # --- elle okuma ---
        if sira not in ELLE:
            hata.append(f"#{sira} ⛔ elle okuma kaydı yok")
            continue
        i_tur, i_adim, notu = ELLE[sira]
        for ad, i in (("tür", i_tur), ("adım", i_adim)):
            if i is not None and not (0 <= i < len(cumleler)):
                hata.append(f"#{sira} ⛔ elle okunan {ad} cümlesi yok: [{i}]")

        var = i_tur is not None and i_adim is not None
        if st in GEREKLI and not var:
            hata.append(f"#{sira} ⛔ ÖLÇÜT 1 — {st} ama tür/adım eksik")
        if st in YASAK and var:
            hata.append(f"#{sira} ⛔ ÖLÇÜT 2 — {st} beyan edildi ama yönlendirme cümlesi var")
        if st in YALNIZ_SINIR and i_adim is not None:
            hata.append(f"#{sira} ⛔ {st} ama adım gösteriliyor (yalnız sınır beklenir)")
        if rakam:
            hata.append(f"#{sira} ⛔ ÖLÇÜT 3 — rakam: {rakam}")
        if ozel_modelden:
            hata.append(f"#{sira} ⛔ ÖLÇÜT 3 — kurum özel adı modelden: {ozel_modelden}")

        satirlar.append({
            "parti_sira": sira, "id": k["id"][:16], "sinir_tipi": st,
            "yonlendirme_var": var,
            "tur_cumlesi": cumleler[i_tur] if i_tur is not None else None,
            "adim_cumlesi": cumleler[i_adim] if i_adim is not None else None,
            "elle_not": notu,
            "terim_isabeti": terim,
            "terim_isabeti_genis": terim_genis,
            "rakam": rakam, "kurum_ozel_ad": ozel,
        })

    # ⭐ Şablonlaşma ölçümü — §8b'nin ölçütünde YOK, buraya K14 ("şablon yok")
    # gereği eklendi. Yönlendirme dilimini eklerken en kolay hata, korpusa 17 kez
    # tekrarlanan "sınır çekme"nin yerine N kez tekrarlanan tek bir YÖNLENDİRME
    # cümlesi koymaktır: hamle değil dizge öğretilir.
    def _gram(metin: str, n: int = 6) -> set[str]:
        w = metin.split()
        return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}

    sablon = {}
    for alan in ("content", "thinking"):
        sayac: dict[str, list[int]] = {}
        for k in kayitlar:
            for g in _gram(_last_assistant(k)[alan]):
                sayac.setdefault(g, []).append(k["gen_meta"]["parti_sira"])
        tekrar = {g: v for g, v in sayac.items() if len(v) > 1}
        sablon[alan] = {
            "tekrarli_6gram": len(tekrar),
            "en_cok": sorted(((len(v), g, sorted(v)) for g, v in tekrar.items()),
                             reverse=True)[:5],
        }
        if tekrar and max(len(v) for v in tekrar.values()) > 2:
            hata.append(f"⛔ ŞABLON — {alan}: bir 6-gram 3+ kayıtta tekrarlıyor")

    # ⭐ §7a — bağlam davranışı dağılımı (T96). Beyan `gen_meta`'da; betik
    # yalnızca SAYAR, sınıfı karar olarak vermez (aynı ilke: §8b ölçüt 4).
    ctx_kayit = [k for k in kayitlar if k.get("context")]
    baglam = {
        "kayit": len(ctx_kayit),
        "sinif": dict(Counter(k["gen_meta"]["baglam_davranisi"] for k in ctx_kayit)),
        "bicim_varyanti": dict(Counter(k["gen_meta"]["baglam_bicimi"] for k in ctx_kayit)),
        "hedef_7a": {"cevap_var": 50, "cevap_yok": 25, "izin_iste": 12, "ilgisiz": 12},
    }
    for k in ctx_kayit:
        # §7b-3: her bağlam girdisi `sentetik` taşır (checks.py kapısı da bakar)
        if not all(c.get("sentetik") is True for c in k["context"]):
            hata.append(f"#{k['gen_meta']['parti_sira']} ⛔ §7b-3 sentetik bayrağı eksik")

    # ⭐ §3c çarpışması — ölçütte YOK, blok 2 yazılırken görüldü.
    # uretim-v4 §3c: "Beş kelimelik bir açılış TEK TURLUK kayıt olarak zayıftır:
    # yansıtılacak malzeme yok." Izgara `bicim` ile `turn_type`'ı BAĞIMSIZ çektiği
    # için (§3a'nın kendi kuralı) bu hücre yine de doluyor. Ama zayıflık koşulu
    # üçüncü, ÇEKİLMEYEN bir değişkene bağlı: kısa mesaj CEVAPLANABİLİR bir talep
    # taşıyor mu. Taşıyorsa tek tur yeter (rol sınırı soruları), taşımıyorsa
    # turun sorusuz bir hamleyle bitmesi gerekir.
    kisa_tek = []
    for k in kayitlar:
        gm = k["gen_meta"]
        if gm["bicim"] != "kisa" or k["turn_type"] != "single":
            continue
        ilk = next(m["content"] for m in k["messages"] if m["role"] == "user")
        kisa_tek.append({
            "parti_sira": gm["parti_sira"],
            "ilk_mesaj": ilk,
            "dogrudan_talep": "?" in ilk,
            "turn_ending": gm["turn_ending"],
        })
    for r in kisa_tek:
        if not r["dogrudan_talep"] and r["turn_ending"] == "acik_uclu_soru":
            hata.append(f"#{r['parti_sira']} ⛔ §3c — kısa+tek tur, talep yok, "
                        f"üstüne açık uçlu soruyla bitiyor")

    # ⭐ Ölçüt 4'ün asıl gösterdiği şey: terim sayımı ile elle okuma AYNI ŞEY DEĞİL.
    terimli = {s["parti_sira"] for s in satirlar if s["terim_isabeti"]}
    terimli_g = {s["parti_sira"] for s in satirlar if s["terim_isabeti_genis"]}
    yonlendiren = {s["parti_sira"] for s in satirlar if s["yonlendirme_var"]}

    def kalite(bulunan: set) -> dict:
        dp = len(bulunan & yonlendiren)
        return {"dogru_pozitif": dp, "yanlis_pozitif": len(bulunan - yonlendiren),
                "yanlis_negatif": len(yonlendiren - bulunan),
                "yanlis_negatif_satir": sorted(yonlendiren - bulunan),
                "kesinlik": round(dp / len(bulunan), 3) if bulunan else None,
                "duyarlilik": round(dp / len(yonlendiren), 3) if yonlendiren else None}

    ozet = {
        "tarih": "2026-09-16",
        "betik": "scripts/analiz/2026-09-16-parti2-blok1-8b-denetimi.py",
        "girdi": str(GIRDI.relative_to(KOK)),
        "girdi_sha256": hashlib.sha256(ham).hexdigest(),
        "kayit": len(kayitlar),
        "sinir_tipi_dagilimi": {t: sum(1 for s in satirlar if s["sinir_tipi"] == t)
                               for t in sorted({s["sinir_tipi"] for s in satirlar})},
        "terim_gecen": sorted(terimli),
        "elle_yonlendiren": sorted(yonlendiren),
        "terim_var_yonlendirme_yok": sorted(terimli - yonlendiren),
        "yonlendirme_var_terim_yok": sorted(yonlendiren - terimli),
        # ⚠️ "Altın standart" = ELLE okuma, yani TEK okuyucunun kararı. Bu
        # sayılar listelerin elle okumaya göre kalitesidir, gerçeğe göre değil.
        "vekil_olcut_kalitesi": {"eval_16": kalite(terimli), "rapor_21": kalite(terimli_g)},
        "iki_liste_farki": sorted(set(rap.TERIMLER) - set(env.TERIMLER)),
        "terim_listesi_kaynagi": "2026-09-15-v002-yonlendirme-envanteri.py::TERIMLER (import)",
        "baglam_7a": baglam,
        "sablonlasma": sablon,
        "kisa_tek_tur": kisa_tek,
        "hata": hata,
        "kayitlar": satirlar,
    }
    CIKTI.write_text(json.dumps(ozet, ensure_ascii=False, indent=2), encoding="utf-8")

    for h in hata:
        print(h)
    print(f"\nkayıt {len(kayitlar)} · {ozet['sinir_tipi_dagilimi']}")
    print(f"terim geçen {len(terimli)} · elle yönlendiren {len(yonlendiren)}")
    print(f"⚠️ terim var ama yönlendirme YOK: {ozet['terim_var_yonlendirme_yok']}")
    print(f"⚠️ yönlendirme var ama terim YOK: {ozet['yonlendirme_var_terim_yok']}")
    for ad, v in ozet["vekil_olcut_kalitesi"].items():
        print(f"  {ad:9s} kesinlik %{100*v['kesinlik']:.0f} · duyarlılık %{100*v['duyarlilik']:.0f}"
              f"  (DP {v['dogru_pozitif']} · YP {v['yanlis_pozitif']} · YN {v['yanlis_negatif']}"
              f" {v['yanlis_negatif_satir']})")
    print(f"  iki listenin farkı: {ozet['iki_liste_farki']}")
    print(f"bağlam {baglam['kayit']} · §7a {baglam['sinif']} · biçim {baglam['bicim_varyanti']}")
    print(f"kısa+tek tur {len(kisa_tek)} · talep taşıyan "
          f"{sum(1 for r in kisa_tek if r['dogrudan_talep'])} "
          f"· taşımayanların bitişi "
          f"{[r['turn_ending'] for r in kisa_tek if not r['dogrudan_talep']]}")
    for alan, d in sablon.items():
        print(f"şablon · {alan}: {d['tekrarli_6gram']} tekrarlı 6-gram, "
              f"en çok {d['en_cok'][0][0] if d['en_cok'] else 0}x")
    print(f"→ {CIKTI.relative_to(KOK)}")
    if hata:
        sys.exit(f"⛔ {len(hata)} ölçüt ihlali")
    print("✅ §8b düzeltme ölçütü 1-4 tuttu")


if __name__ == "__main__":
    main()
