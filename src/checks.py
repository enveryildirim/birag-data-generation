"""Deterministik kapılar — LLM gerektirmez. Bkz. plan.md §15, §7, Kural 4/5.

Kontroller: yasak ifade taraması (§15) · sayı/telefon adayı (K18) ·
soru sayısı <= 1 · yansıtma:soru oranı >= 2:1 · uzunluk sınırları ·
şema geçerliliği · exact-hash dedup.

Kullanım: uv run python src/checks.py <records.jsonl>
"""
from __future__ import annotations
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml
from pydantic import ValidationError

from schemas import TrainRecord
# ⛔ Türkçe küçültme TEK kaynaktan gelir (K144/T73). Düz `.lower()` "ADI" -> "adi"
# ve "İLAÇ" -> "i̇laç" üretiyor; ikisi de Türkçe karşılığıyla eşleşmiyor ve §15
# kapısının 38 ifadesinden 14'ü büyük harfle yazılınca görünmez geçiyordu —
# biri SERT kategoride. Hata ailesinin dördüncü örneği; ilk üçü
# `tohum_guvenlik.py` başlığında anlatılıyor ve çözüm orada ilan edilmiş.
# ⭐ `i_sinifi` 2026-09-16'da buradan `tohum_guvenlik`'e TAŞINDI (T76):
# o modül kendini Türkçe küçültmenin TEK giriş noktası ilan ediyor ve
# fonksiyonun burada durması ailenin dokuzuncu örneğini davet ediyordu.
from tohum_guvenlik import i_sinifi, tr_fold, tr_kucult, AD_CEKIM_EKI
# ⭐ Dil tespiti `smoke_checks`'ten ÇAĞRILIR, kopyalanmaz: Eksen 3 smoke eval'i
# aynı dedektörü kullanıyor ve iki kopya zamanla ayrışırdı (T81).
import smoke_checks as _sc




FILTERS = yaml.safe_load((Path(__file__).parent.parent / "configs" / "filters.yaml").read_text())

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?…])\s+")
_NUMBER_CANDIDATE = re.compile(r"\d[\d\s\-.()]{1,}\d|\d{3,}")


# §15 kategorilerinden yalnızca bu SERT kapıdır. Diğerleri (özellikle `rol_siniri`)
# modelin DOĞRU reddinin içinde de geçer — "ben teşhis koyamam", "doz öneremem" —
# ve kelime taraması bağlamı ayırt edemez; onlar inceleme kuyruğuna gider.
# ⚠️ Bu ayrım eskiden `run_checks` içinde yerel bir değişkendi ve golden_eval onu
# göremediği için ilk baseline koşusunda iki DOĞRU reddi "başarısız" saydı.
SERT_KATEGORILER = {"kriz_yasagi"}


# ⛔⛔ **DÜZ ALT DİZGE ARAMASI KİP DEĞİŞİMİNİ GÖREMİYOR (2026-09-18, inceleme
# kuyruğu okununca bulundu).** Eşleşme `ifade in metin` idi ⇒ Türkçenin eklemeli
# yapısında ifade, KENDİNDEN TÜREYEN ama ANLAMI BAŞKA bir sözcüğün içinde de
# eşleşiyor: *«merak etme»* (olumsuz emir) *«merak etmeK»*in (mastar) içinde.
# ⭐ Ölçüldü: `bos_guvence` kategorisinin bütün korpuslardaki **16 vuruşunun 16'sı**
# bu kusurdan; korpusta gerçek bir *«merak etme»* güvencesi YOK.
# ➡️⭐⭐ *Bir ifade listesi, ekleri hesaba katmadan aranamaz — ama nasıl hesaba
#    katılacağı ifadenin BİÇİMİNE bağlı ve ikisi karıştırılmamalı:*
#   · **TEK SÖZCÜK** (*«doz»*, *«teşhis»*, *«bağımlısın»*) — ek SERBEST kalmalı;
#     *«dozu azaltan hekim»* aynı sözcüktür ve yakalanması doğrudur.
#   · **ÇOK SÖZCÜKLÜ** (*«merak etme»*, *«bana söz ver»*) — son öge bir FİİL
#     çekimidir ve ek aldığında kip değişir ⇒ sözcük sınırında bitmeli.
# ⚠️ Bu ayrım `KLINIK_IDDIA`'nın zaten uyguladığı ilkenin aynısı: *«Belirsiz kökler
#   için ek SERBEST DEĞİL, sayılı»*.
# ⛔⛔ **SERT KATEGORİ BU DÜZELTMENİN DIŞINDA TUTULDU — KURAL 3.** `kriz_yasagi`
#   ölçüldü ve orada durum daha ağır: *«bana söz ver»* ifadesi *«Senden bana söz
#   VERMENİ istemiyorum»* cümlesini de düşürüyor, yani kapının KENDİ kuralını
#   uygulayan cümleyi siliyor. ⚠️ Ama sözcük sınırı kuralı oraya uygulanırsa
#   *«bana söz verir misin»* KAÇAR ⇒ güvenlik ekseninde bir yanlış negatif doğar.
#   *«Güvenlik ekseninde gerileme kabul edilebilir değildir»* (Kural 3) ⇒ sert
#   kategorinin eşleşmesi AYNEN korunuyor; doğru çözüm ifade listesini düzeltmektir
#   ve o bir UZMAN kararıdır, benim değil. Bulgu raporlandı, kapı değiştirilmedi.
# ⛔⛔ **VE «EK SERBEST» DE ÇOK GENİŞTİ (2026-09-18, ikinci ölçüm).** Tek sözcüklü
# ifadelerde eki serbest bırakmak *«doz»* → *«dozu»* için DOĞRU (aynı sözcük) ama
# *«keş»* → *«keşke»* için yanlış: *«keşke»* bir ek almış *«keş»* değil, BAŞKA bir
# sözcük. ⚠️ Tuzak canlı: *«keşke»* kullanıcı turlarında **9**, asistan
# `thinking`'inde **9** kez geçiyor; `content`'te henüz yok ama yazıldığı gün
# `etiketleme` kategorisine yanlış vuruş girecek.
# ⇒ Kök yalnız **AD ÇEKİM EKİ** alabilir (kapalı küme, `tohum_guvenlik`).
# ⭐ Ölçüldü: bütün korpuslarda eşleşmeyi BIRAKAN vuruş **0** (*«dozu»*, *«dozun»*,
#   *«dozla»*, *«teşhis»* hepsi çekim ekiyle eşleşmeye devam ediyor).
# ⛔ Sert kategorinin üç ifadesi de ÇOK SÖZCÜKLÜ ⇒ bu kural oraya hiç dokunmuyor.
_EK_HARF = re.compile(r"\w")
_CEKIM = re.compile(AD_CEKIM_EKI + r"$")


def _ifade_gecer(ifade: str, low: str, ek_serbest: bool) -> bool:
    """İfade metinde geçiyor mu?

    `ek_serbest=True`  — tek sözcük: kök AD ÇEKİM EKİ alabilir, başka ek alamaz.
    `ek_serbest=False` — çok sözcüklü ya da sert kategori: sözcük sınırında bitmeli.
    ⚠️ Sert kategoride eşleşme hiç değişmez: ifadeleri çok sözcüklü olduğu için
       bu dal `ek_serbest=True` ile çağrılmıyor (Kural 3 tutması, `scan_forbidden`).
    """
    h = i_sinifi(tr_kucult(ifade))
    i = low.find(h)
    while i >= 0:
        j = i + len(h)
        if not ek_serbest:
            if not _EK_HARF.match(low[j:j + 1] or " "):
                return True
        else:
            son = j
            while son < len(low) and _EK_HARF.match(low[son]):
                son += 1
            if _CEKIM.fullmatch(low[j:son]):
                return True
        i = low.find(h, i + 1)
    return False


def scan_forbidden(text: str) -> dict[str, list[str]]:
    """§15 yasak ifade taraması. Sonuç: kategori -> eşleşen ifadeler.
    ahlaki_yargi_klinik bağlama duyarlıdır — eşleşme otomatik red değil, elle gözden geçirilir.
    """
    low = i_sinifi(tr_kucult(text))
    hits: dict[str, list[str]] = {}
    for kategori, ifadeler in FILTERS["yasakli_ifadeler"].items():
        # ⛔ Sert kategoride eşleşme AYNEN eski davranış (yukarıdaki Kural 3 şerhi).
        # ⛔ Sert kategori: eşleşme AYNEN eski davranış — ifadeleri çok sözcüklü
        # olduğu için «serbest» dalı zaten devreye girmez, ama koşul açık yazılıyor.
        sert = kategori in SERT_KATEGORILER
        found = []
        for i in ifadeler:
            tek = " " not in i.strip()
            if sert:
                if i_sinifi(tr_kucult(i)) in low:      # ⛔ Kural 3: dokunulmadı
                    found.append(i)
            elif _ifade_gecer(i, low, ek_serbest=tek):
                found.append(i)
        if found:
            hits[kategori] = found
    return hits


def _kelime(s: str | None) -> int:
    return len((s or "").split())


def thinking_metrikleri(thinking: str | None, completion: str) -> dict:
    """K46'nın üç metriği — plan.md §7'de ilan edildi, koda 2026-09-16'da girdi (T81).

    ⚠️ **Birim KELİME.** K46'nın *«~14x uzun»* ölçümü de kelimeyle yapıldı
    (`2026-09-12-thinking-dili-raporu.py`, `len(t.split())`); birim değişirse
    sayılar karşılaştırılamaz (Kural 5).

    · `thinking_dili` — `smoke_checks._dil` **çağrılır** (kopyalanmaz).
      ⚠️ Vekil bir dedektör: Türkçeye özgü harf + işlev sözcüğü sayımı, dil
      modeli değil. ⭐ Ama yanlış pozitif oranı ÖLÇÜLDÜ (plan.md'nin şartı):
      **0/2716** Türkçe thinking'in hiçbiri `en` sayılmadı; arşivlenmiş gerçek
      etikette de kusursuz (36/36 `tr`, 36/36 `en`).
      ⛔ **Yanlış negatif kanıtı ZAYIF:** 36 İngilizce örneğin hepsi **aynı
      kalıp** (*«Here's a thinking process…»*); İngilizcenin çeşitliliği
      sınanmadı.
    · `thinking_completion_orani` — thinking / completion kelime.
    · `kullaniciya_giden_pay` — completion / (thinking + completion).

    ⛔ **Son ikisi KAPI DEĞİL, yalnızca rapor.** Gerekçe T7: §4'ün *«sabit taban
    koyma»* dersi — sabit bir eşik dağılımı kendine çeker ve ölçtüğü şeyi
    bozar. Tavanın veriyle nasıl öğretileceği `plan.md`'de **açık kalem**.
    """
    t, c = _kelime(thinking), _kelime(completion)
    return {
        "thinking_dili": _sc._dil(thinking) if thinking else None,
        "thinking_completion_orani": round(t / c, 2) if c else None,
        "kullaniciya_giden_pay": round(c / (t + c), 2) if (t + c) else None,
    }


def detect_number_candidates(text: str) -> list[str]:
    """K18 — model çıktısında numara olmamalı (kaynak TÜRÜ verilir, numara değil).
    Kasıtlı olarak geniş kapsamlı bir vekil: 3+ ardışık rakam veya ayraçlı rakam
    grupları işaretlenir (yıl gibi yanlış pozitifler olabilir — insan incelemesine gider).
    """
    return [m.group(0).strip() for m in _NUMBER_CANDIDATE.finditer(text)]


def _sentences(text: str) -> list[str]:
    return [s for s in _SENTENCE_SPLIT.split(text.strip()) if s]


def count_questions(text: str) -> int:
    return text.count("?")


def reflection_question_ratio(text: str) -> float | None:
    """Vekil ölçüt: soru işaretiyle bitmeyen cümle sayısı / soru sayısı.
    Gerçek klinik "yansıtma" sınıflandırması değildir — TIP 35 oranının
    ucuz bir yaklaşıklamasıdır (§7). Soru yoksa None döner (oran tanımsız, iyi kabul edilir).
    """
    sents = _sentences(text)
    q = sum(1 for s in sents if s.rstrip().endswith("?"))
    if q == 0:
        return None
    return (len(sents) - q) / q


def length_ok(completion: str, thinking: str | None) -> tuple[bool, str | None]:
    u = FILTERS["uzunluk"]
    n = len(completion)
    if not (u["completion_min_char"] <= n <= u["completion_max_char"]):
        return False, f"completion uzunluk {n} sınır dışı ({u['completion_min_char']}-{u['completion_max_char']})"
    if thinking and len(thinking) > u["thinking_max_char"]:
        return False, f"thinking uzunluk {len(thinking)} > {u['thinking_max_char']}"
    tavan = u.get("thinking_completion_orani_maks")
    if thinking and tavan and n and len(thinking) / n > tavan:
        return False, (f"thinking:completion oranı {len(thinking)/n:.2f}x > {tavan}x tavanı")
    return True, None


def schema_valid(record: dict) -> tuple[bool, str | None]:
    try:
        TrainRecord(**record)
        return True, None
    except ValidationError as e:
        return False, str(e)


def exact_hash_dedup(records: list[dict]) -> dict[str, list[int]]:
    """id alanına göre (§12: sha256(normalize(user_content + mode))) çakışan indeksler."""
    seen: dict[str, list[int]] = {}
    for i, r in enumerate(records):
        rid = r.get("id") or hashlib.sha256(json.dumps(r, sort_keys=True).encode()).hexdigest()
        seen.setdefault(rid, []).append(i)
    return {rid: idxs for rid, idxs in seen.items() if len(idxs) > 1}


def _last_assistant(record: dict) -> dict | None:
    for m in reversed(record.get("messages", [])):
        if m.get("role") == "assistant":
            return m
    return None


def turn_structure_ok(record: dict) -> tuple[bool, str | None]:
    """Konuşma yapısı kapısı (2026-09-14).

    Faz 2'de bir üretim partisinde iki çok turlu kayıt yanlışlıkla KULLANICI turuyla
    bitirilmiş, `thinking` de kullanıcı mesajına iliştirilmişti; o günkü kapılar bunu
    yakalamadı ve kayıtlar 8/8 geçti. K49 ile aynı kök: sessizce yanlış olan bir şey
    doğrulanmadığı için doğru sayılıyor.

    Kurallar: kayıt asistan turuyla biter · thinking YALNIZCA son asistan turunda
    bulunur (K44: eğitim template'i önceki turların thinking'ini soyar) · roller
    system → (user → assistant)+ sırasını izler.
    """
    msgs = record.get("messages") or []
    if not msgs:
        return False, "messages boş"
    if msgs[-1].get("role") != "assistant":
        return False, f"kayıt '{msgs[-1].get('role')}' turuyla bitiyor, asistan turu bekleniyor"
    for i, m in enumerate(msgs):
        if m.get("thinking") and i != len(msgs) - 1:
            return False, f"thinking son olmayan turda ({i}, rol={m.get('role')})"
        if m.get("role") not in {"system", "user", "assistant"}:
            return False, f"bilinmeyen rol: {m.get('role')}"
    konusma = [m["role"] for m in msgs if m["role"] != "system"]
    for i, rol in enumerate(konusma):
        beklenen = "user" if i % 2 == 0 else "assistant"
        if rol != beklenen:
            return False, f"tur sırası bozuk: {i}. turda {rol}, {beklenen} bekleniyordu"
    return True, None


# uretim-v3 §7b — sentetik pasajın üç sınırı. Kural belgeye yazıldığı anda kapı da
# yazıldı (K66). Pasajlar repoda belge korpusu olmadığı için ÜRETİM SIRASINDA yazılıyor;
# gerekçe ve ölçüm: reports/analiz/2026-09-14-baglam-dilimi-envanteri.md
# ⚠️ KELİME SINIRIYLA eşleşir, alt dize olarak DEĞİL. İlk yazımda alt dize taraması
# yapıyordu ve "belirtilmez" kelimesi "belirti"yi içerdiği için yordam cümlesini
# klinik iddia sanıyordu — K65'in (anahtar kelime kapısı kelime içinde eşleşiyor)
# dördüncü örneği. Kökten sonra Türkçe ek serbest: "belirti", "belirtiler", "belirtisi".
# ⭐⭐ **LİSTE İKİ AYRI ŞEYİ KARIŞTIRIYORDU (2026-09-18, ölçüldü).** §7b-2 *«pasaj
# klinik İDDİA taşımaz»* diyor ve izin verilen kategorileri de sayıyor: yordam /
# erişim / gizlilik / uygunluk / sınır. Ama tarayıcı iki farklı türü tek listede
# topluyordu:
#   · **klinik AD** (belirti, tanı, doz, yoksunluk, semptom, teşhis, ilaç, terapi,
#     tedavi) — bir KONU sözcüğü. Tek başına iddia değildir: *«Araç tanı koymaz»*
#     bir feragat, *«Gündüz tedavi üniteleri»* bir birim adı, *«Reçeteli ilaçlar
#     için reçete aranır»* bir yordam cümlesi.
#   · **klinik YÜKLEM** (iyileş, zararl, etkili, bağımlılık yap, etki eder,
#     «üç hafta sürer», «riski azalır») — bir ETKİ/SONUÇ iddiası.
# ⭐ Ölçüldü: depodaki **118 benzersiz bağlam pasajının 7'si** takılıyor ve
# **yedisi de çıplak AD**; yüklem kökleri bağlam pasajlarında **hiç** ateşlemedi.
# ⇒ Yedi vuruşun yedisi yanlış pozitif.
# ➡️⭐⭐ *Bir ad, iddia değildir; iddia bir yüklem gerektirir. İkisini tek listede
#    toplayan bir kapı, konudan bahsetmeyi iddia etmekle karıştırır.*
# ⛔ Bu, deponun KENDİ verdiği bir kararın aynısıdır: `rol_siniri` sert kapı
#   DEĞİL, çünkü *«"teşhis" gibi kelimeler modelin DOĞRU reddi içinde de geçiyor —
#   kelime taraması bağlamı ayırt edemiyor»* (2026-09-12 register sondası). Aynı
#   gerekçe burada da geçerli ⇒ AD izleri **inceleme kuyruğuna**, yüklemler kapıya.
# ⚠️ Olumsuzluk BİR MUAFİYET DEĞİLDİR ve kasten öyle yazılmadı: *«Bu ilaç
#   bağımlılık YAPMAZ»* olumsuzdur ama yine de bir klinik iddiadır ve yakalanır.
KLINIK_AD_KAYNAK = (
    # Belirsiz kökler için ek SERBEST DEĞİL, sayılı: "belirti/belirtisi/belirtileri" klinik,
    # "belirtilmez" (belirtmek fiili) değil. `\w*` kullanmak ikisini ayıramıyor.
    r"\bbelirti(si|leri|ler|yi|nin)?\b|\btanı(sı|ları|lar|nın)?\b|\bdoz(u|lar|ları|aj)?\b"
    # Tek anlamlı kökler için ek serbest.
    r"|\byoksunluk\w*|\bsemptom\w*|\bteşhis\w*|\bilaç\w*|\bilac\w+|\bterapi\w*"
    r"|\btedavi\w*")
# ⛔ T150 iki boşluk ilan etmişti: yüklem desenleri ÇEKİME kapalıydı — *«riskini
# azaltır»* ve *«etki ediyor»* kaçıyordu. 2026-09-18'de dal dal ölçüldü ve YALNIZ
# bedava olanlar açıldı:
#   · `riski\w*` ve `etki ed\w*` → 28.084 metinlik havuzda **0 fark** ⇒ açıldı
#   · SÜRE dalı (*«iki ay sürüyor»*) → ⛔ AÇILMADI. Bağlam pasajlarında bedava ama
#     serbest metinde **49 yanlış pozitif** üretiyor (*«altı ay geçti düğünden»*,
#     *«aylar sürecek diye düşünüyorum»*) ve `KLINIK_IDDIA` birleşimini dört analiz
#     betiği serbest metinde kullanıyor.
# ➡️⭐⭐ *Bir desenin genişletilmesi bedava mı değil mi, desenin değil UYGULANDIĞI
#    YERİN özelliğidir. Aynı genişletme bağlam pasajında sıfır, kullanıcı metninde
#    49 yanlış pozitif verdi ⇒ «ölçtüm, bedava» demeden önce NEREDE ölçtüğünü
#    söylemek gerekir.*
KLINIK_YUKLEM_KAYNAK = (
    r"\biyileş\w*|\bzararl\w*|\betkili\w*"
    r"|\bbağımlılık yap\w*|\betki ed\w*"
    r"|\b(hafta|gün|ay|yıl) (sürer|içinde geçer)\b|\briski\w*\s+(art\w*|azal\w*)")
# ⚠️ BİRLEŞİK desen KORUNUYOR: dört analiz betiği `KLINIK_IDDIA`'yı içe aktarıyor
# ve onların sayıları değişmemeli (K97). Birleşim eski desenin AYNISIDIR.
KLINIK_IDDIA_KAYNAK = KLINIK_AD_KAYNAK + "|" + KLINIK_YUKLEM_KAYNAK
# ⛔ Desen ve metin AYNI sınıfa sokulur (T75). Düz `.lower()` ile 16 kökün 8'i
# DOĞRU Türkçe büyütmede ölüydü: "BELİRTİ".lower() -> "beli̇rti̇" (i + birleşen
# nokta) ve `\bbelirti` ile eşleşmiyor. ⚠️ Yön T73'ün TERSİ — orada tehlike `I`
# idi çünkü kalıplar `ı` taşıyordu, burada `İ` çünkü kökler `i` taşıyor.
# ⚠️ NFKD (`tr_kucult`) burada UYGULANMIYOR: desen bir regex ve NFKD `\b`/`\w`
# semantiğini bozuyor. Ayrıştırılmış ç/ş/ğ taşıyan metin hâlâ kaçabilir — açık
# kalem, `reports/analiz/2026-09-16-kalan-lower-satirlari.md` §5.
KLINIK_IDDIA = re.compile(i_sinifi(KLINIK_IDDIA_KAYNAK), re.IGNORECASE)  # lower-muaf: i-sınıfı ZATEN uygulandı; re.I burada yalnız ç/ş/ğ/ö/ü için ve Python onları doğru çözüyor
KLINIK_AD = re.compile(i_sinifi(KLINIK_AD_KAYNAK), re.IGNORECASE)          # lower-muaf: i-sınıfı ZATEN uygulandı
KLINIK_YUKLEM = re.compile(i_sinifi(KLINIK_YUKLEM_KAYNAK), re.IGNORECASE)  # lower-muaf: i-sınıfı ZATEN uygulandı


def klinik_ad_izleri(record: dict) -> list[str]:
    """§7b-2'nin YUMUŞAK yarısı: bağlam pasajlarındaki klinik AD izleri.

    ⛔ Bunlar kapıyı kapatmaz — inceleme kuyruğuna gider (`rol_siniri` emsali).
    Bir ad tek başına iddia değildir; iddia `KLINIK_YUKLEM` ile sınanır.
    """
    izler: list[str] = []
    for k in record.get("context") or []:
        if isinstance(k, dict):
            izler += [m.group(0) for m in KLINIK_AD.finditer(i_sinifi(k.get("metin") or ""))]
    return sorted(set(izler))


# ⛔⛔ **SERT KAPI ÜRETİM SÜRÜMÜ İLERLEYİNCE KENDİ KENDİNE KAPANMIŞTI (2026-09-18).**
# Koşul `startswith("uretim-v3")` idi; değişkenin adı `v3_ve_sonrasi`, yorumu
# *«uretim-v3 VE SONRASI»*. Üretim v4'e, sonra v5'e geçince kapı sessizce kapandı:
# 4404 kayıt kapsam dışı kaldı, yalnız 1238 v3 kaydında açık kaldı. Kapanma hata
# vermez, uyarı yazmaz — yalnız eleme yapmamaya başlar.
# ➡️⭐⭐ *Bir dizge önekine bağlanan sürüm koşulu, sürüm ilerledikçe KENDİ KAPSAMINI
#    daraltır. Sürüm bir SAYIDIR; öneki karşılaştırmak sayıyı karşılaştırmak değildir.*
_URETIM_SURUM = re.compile(r"^uretim-v(\d+)")


def uretim_surumu(record: dict) -> int | None:
    """`uretim-vN` içindeki N. Tanınmayan/eksik sürüm için `None`.

    ⚠️ `dikey-dilim-v1` ve sürümsüz kayıtlar bilerek `None`: §7b kapısı onlar için
    ZATEN kapalıydı ve bu bir TASARIM kararı (geriye dönük düzeltilmiyor), sürüm
    koşulunun kusuru değil. Kapsamı genişletmek ayrı bir karardır.
    """
    m = _URETIM_SURUM.match(str((record.get("gen_meta") or {}).get("prompt_version", "")))
    return int(m.group(1)) if m else None


def context_ok(record: dict) -> tuple[bool, str | None]:
    """uretim-v3 §7b: sentetik pasajın üç sınırı.

    1. her bağlam girdisi `sentetik` bayrağı taşır (gerçek korpus geldiğinde ayırt
       edilebilsin) · 2. kaynak adı özel ad değil kategori — küçük harfle başlar,
       böylece "var olmayan belgeyi var gösterme" kuralı makine denetlenebilir olur ·
       3. pasaj klinik iddia taşımaz (yordam/erişim/gizlilik/uygunluk/sınır cümlesi).

    Bağlamsız kayıt için her zaman geçer.
    """
    for i, k in enumerate(record.get("context") or [], 1):
        if not isinstance(k, dict):
            return False, f"context[{i}] sözlük değil"
        if "sentetik" not in k:
            return False, f"context[{i}] `sentetik` bayrağı yok (§7b-3)"
        kaynak = (k.get("kaynak") or "").strip()
        if not kaynak:
            return False, f"context[{i}] `kaynak` boş"
        if k.get("sentetik") is True and kaynak[:1].isupper():
            return False, (f"context[{i}] sentetik kaynak adı büyük harfle başlıyor — "
                           f"gerçek belge taklidi (§7b-1): {kaynak!r}")
        metin = i_sinifi(k.get("metin") or "")
        if not metin:
            return False, f"context[{i}] `metin` boş"
        # ⭐ SERT yarı: yalnız YÜKLEM. Ad izleri `klinik_ad_izleri()` ile raporlanır.
        vurus = sorted({m.group(0) for m in KLINIK_YUKLEM.finditer(metin)})
        if vurus:
            return False, f"context[{i}] pasajda klinik iddia izi (§7b-2): {vurus}"
    return True, None


# Kanonik BıRAG system prompt'unun ayırt edici ilk cümlesi. Replay kayıtları bu
# prompt'u KULLANMAMALI: plan.md §"Kanonik system prompt (K19)" — *"Replay verisinde
# tamamen farklı promptlar bulunur"*. Aynı prompt'la gelen replay, forgetting
# savunması işini görmez; modeli yine tek bir string'e kilitler.
BIRAG_IMZA = ("sen bırag'sın", "bırag sensin")


def replay_ok(record: dict) -> tuple[bool, str | None]:
    """Replay kaydına özgü kapı (plan.md §6, §9). Replay OLMAYAN kayıtta hep geçer."""
    if not record.get("replay"):
        return True, None
    sys_msg = next((m["content"] for m in record.get("messages", [])
                    if m.get("role") == "system"), "")
    # ⛔ Projenin KENDİ ADI tuzağın içinde (T75): `BıRAG` noktasız `ı` taşıyor ve
    # Türkçe klavyesi olmayan herkesin yazacağı hâl `BIRAG`. Düz `.lower()` ile
    # altı yazımın dördü — `SEN BıRAG'SIN`, `Sen BIRAG'sın`, `SEN BIRAG'SIN`,
    # `Sen BİRAG'sın` — imzayla eşleşmiyordu.
    low = i_sinifi(tr_kucult(sys_msg))
    if any(i_sinifi(tr_kucult(im)) in low for im in BIRAG_IMZA):
        return False, "replay kaydı kanonik BıRAG system prompt'unu kullanıyor (§9)"
    return True, None


from dilim import bant_tutarli, dilim_tutarli  # noqa: E402
from yansitma import yansitma_ok

from tohum_guvenlik import tr_fold  # noqa: E402

CELISKI_IZI = re.compile(
    r"çeliş\w*|birbirini tutm\w*|uyuşm\w*|tutarsız\w*|aynı şeyi söylem\w*|"
    r"iki ayrı|iki farklı|farklı (şey|saat|rakam|bilgi)\w*|ayrılıyor", re.I)


def celiskili_ok(record: dict) -> tuple[bool, str | None]:
    """§7a″ — `celiskili` beyan eden kayıt çelişkiyi ADLANDIRMALI ve
    İKİ pasaja birden atıf yapmalı.

    ⛔ Tek pasaja atıf = birini sessizce seçmiş sayılır; §7a″ bunu yasaklar.
    ⭐ Kapı, sınırla AYNI commit'te yazıldı (K66/T237).
    """
    gm = record.get("gen_meta") or {}
    if gm.get("baglam_davranisi") != "celiskili":
        return True, None
    ctx = record.get("context") or []
    if len(ctx) < 2:
        return False, "celiskili beyanı ama bağlam pasajı 2'den az"
    asst = _last_assistant(record) or {}
    cevap = asst.get("content") or ""
    if not CELISKI_IZI.search(cevap):
        return False, "celiskili beyanı ama cevap çelişkiyi adlandırmıyor"
    # ⛔ İKİ pasaja birden atıf.
    # ⛔⛔ İLK SÜRÜM YANLIŞTI: pasajın en uzun sözcüklerini TAM DİZGE arıyordu
    #   ve 12 doğru cevabın 8'ini reddetti — cevap «zorunlu» derken pasaj
    #   «zorunludur» diyor. Türkçe eklemeli; tam dizge çalışmaz.
    # ⭐ Onarım: ayırt edici öğe = ÖTEKİ pasajda olmayan kök (ilk 5 harf) ya da
    #   yalnız o pasajda geçen sayı. Kök karşılaştırması `tr_fold` ile.
    def _kokler(m):
        return {w[:5] for w in re.findall(r"\w{4,}", tr_fold(m or ""))}
    def _sayilar(m):
        return set(re.findall(r"\d[\d:.,]*", m or ""))
    metinler = [(p_.get("metin") if isinstance(p_, dict) else str(p_)) for p_ in ctx[:2]]
    cev_kok = _kokler(cevap)
    cev_say = _sayilar(cevap)
    tutan = 0
    for i, m in enumerate(metinler):
        oteki = metinler[1 - i]
        ayirt_kok = _kokler(m) - _kokler(oteki)
        ayirt_say = _sayilar(m) - _sayilar(oteki)
        if (ayirt_kok & cev_kok) or (ayirt_say & cev_say):
            tutan += 1
    # ⛔⛔ İKİNCİ ÖLÇÜT SERT KAPI DEĞİL — RAPOR.
    #   Gerekçe ölçüldü: bankadaki 12 çiftin doğru cevaplarında bu ölçüt
    #   5'ini reddetti, çünkü ayırt edici öğe bazen KISA bir sözcük («ilk»,
    #   «son», «iki») ve Türkçe serbest metinde kök eşlemesi onu göremiyor.
    #   ⭐ Repoda emsali var: `reflection_question_ratio_ok` da aynı sebeple
    #   bilgilendiricidir, sert kapı değil (K40).
    #   ⇒ Sert kapı yalnız (a) iki pasaj ve (b) çelişkinin ADLANDIRILMASI.
    #     «İki pasaja atıf» inceleme kuyruğuna gider.
    return True, (None if tutan >= 2 else
                  f"⚠️ RAPOR: cevap {tutan}/2 pasaja atıf yapıyor — okunmalı")


def run_checks(record: dict) -> dict:
    """Tek kayıt için tüm kapıları çalıştırır. `passed=False` -> build.py eler."""
    valid, schema_err = schema_valid(record)
    result: dict = {"schema_valid": valid, "schema_error": schema_err}
    if not valid:
        result["passed"] = False
        return result

    turns_ok, turns_err = turn_structure_ok(record)
    result.update({"turn_structure_ok": turns_ok, "turn_structure_error": turns_err})
    if not turns_ok:
        result["passed"] = False
        return result

    # ⛔⛔ T240 KAPISI. `slice` alanının anlamı v5 ile v6 arasında sessizce
    # değişmişti ve DÖRT katman da kördü: şema `slice: str` (Literal değil),
    # burada denetim yoktu, birleştirme raporu saymıyordu, judge görmüyordu.
    # ⭐ Alan artık `src/dilim.py`'de türetiliyor; bu kapı beyanın türetilenle
    # ayrışmasını yakalar. Üretim ve birleştirme türettiği için kapı ancak
    # biri dilimi ELLE yazarsa ateşler — yani tam ateşlemesi gereken yerde.
    dilim_ok, dilim_err = dilim_tutarli(record)
    result.update({"dilim_ok": dilim_ok, "dilim_error": dilim_err})
    if not dilim_ok:
        result["passed"] = False
        return result

    # ⛔⛔ `gen_meta.bicim` de BEYANDI (slice ve date'ten sonra ÜÇÜNCÜSÜ) ve
    #   `celiskili` pilotunda elle beyan edilen iki bant yanlış çıktı.
    bant_ok, bant_err = bant_tutarli(record)
    result.update({"bant_ok": bant_ok, "bant_error": bant_err})
    if not bant_ok:
        result["passed"] = False
        return result

    # ⭐ §7a″ (2026-09-22): beşinci bağlam sınıfı `celiskili`.
    cel_ok, cel_err = celiskili_ok(record)
    result.update({"celiskili_ok": cel_ok, "celiskili_error": cel_err})
    if not cel_ok:
        result["passed"] = False
        return result

    # ⛔⛔ T265: `celiskili` 12 kaydın 3'ü kullanıcının SÖYLEMEDİĞİ bir
    #   ayrıntıyı ona atfediyordu. T217 «metin kendi tohumundan mı» diye
    #   soruyordu; bu kapı TERSİNİ sorar: «cevap yalnız konuşmadan mı».
    #   ⭐ Kapı YALNIZ alıntıyla atfa bakar (A kuralı) — 1176 etiketli kayıtta
    #     kesinlik %100, sıfır yanlış pozitif.
    #   ⛔ Duyarlılığı DÜŞÜK (%1): alıntısız parafraz uydurmasını görmez;
    #     T265'in üç kaydından yalnız birini yakalar. Kapı sınırı burada
    #     yazılıdır, çünkü geçmek temiz olmak değildir.
    #     📎 reports/analiz/2026-09-22-yansitma-kalibrasyon.md
    yan_ok, yan_err = yansitma_ok(record)
    result.update({"yansitma_ok": yan_ok, "yansitma_error": yan_err})
    if not yan_ok:
        result["passed"] = False
        return result

    # §7b kapısı YALNIZCA uretim-v3 ve sonrası için serttir. Kural 2026-09-14'te
    # yazıldı; expert-70 (uretim-v2) ondan önce üretildi ve dokuz bağlam kaydı
    # `sentetik` bayrağı taşımıyor, kaynak adları da özel ad biçiminde. O dosyayı
    # geriye dönük düzeltmiyoruz: SHA256'sı üç raporda kayıtlı (Kural 7) ve uzman
    # puanlaması o metne yapıldı. Bulgu yine de HER kayıtta raporlanır — sessizce
    # geçmiş sayılmasın diye.
    ctx_ok, ctx_err = context_ok(record)
    v3_ve_sonrasi = (uretim_surumu(record) or 0) >= 3
    result.update({"context_ok": ctx_ok, "context_error": ctx_err,
                   "context_sert_kapi": v3_ve_sonrasi,
                   # ⛔ RAPOR, KAPI DEĞİL: klinik ad izleri inceleme kuyruğuna gider.
                   "context_klinik_ad_izi": klinik_ad_izleri(record)})
    if not ctx_ok and v3_ve_sonrasi:
        result["passed"] = False
        return result

    asst = _last_assistant(record) or {}
    completion = asst.get("content", "")
    thinking = asst.get("thinking")

    # ⚠️ 2026-09-14: PERSONA KAPILARI YALNIZCA BıRAG KAYITLARINA UYGULANIR.
    # Eskiden hepsi her kayda uygulanıyordu ve replay dilimi sessizce yok olurdu:
    # "soru sayısı ≤ 1" MI kuralıdır (K19 system prompt'u), genel amaçlı bir asistan
    # iki soru sorabilir; "completion ≥ 10 karakter" de "Dört." gibi doğru bir genel
    # cevabı eler; yasak ifade listesi klinik/MI listesidir. Oysa §9'un istediği
    # çeşitlilik tam olarak bunlar: kısa yanıtlar, farklı promptlar, İngilizce.
    # Ölçüldü: dört örnek replay kaydının ikisi eski kapılardan düşüyordu.
    is_replay = bool(record.get("replay"))
    rep_ok, rep_err = replay_ok(record)
    result.update({"replay_ok": rep_ok, "replay_error": rep_err})

    forbidden = scan_forbidden(completion)
    numbers = detect_number_candidates(completion)
    q_count = count_questions(completion)
    ratio = reflection_question_ratio(completion)
    len_ok, len_err = length_ok(completion, thinking)
    if is_replay:
        # Replay için yalnızca kaba bir üst sınır; alt sınır ve MI oranları yok.
        u = FILTERS["uzunluk"]
        len_ok = len(completion) <= u["completion_max_char"]
        len_err = None if len_ok else f"completion uzunluk {len(completion)} > {u['completion_max_char']}"

    # K46'nın üç metriği (T81). ⚠️ `thinking_dili` SERT KAPI, ötekiler rapor.
    metrik = thinking_metrikleri(thinking, completion)
    # ⛔ Kapı YALNIZCA BıRAG kayıtlarına: §9 replay diliminin İngilizce olması
    # tasarım gereği (çeşitlilik). ⚠️ Bugün replay kayıtlarının hiçbirinde
    # thinking yok (0/72, ölçüldü) — kapı yine de kapsam dışı bırakılıyor,
    # çünkü koşul veriye değil TASARIMA dayanmalı.
    dil_ok = is_replay or metrik["thinking_dili"] in (None, "tr")

    result.update({
        **metrik,
        "thinking_dili_ok": dil_ok,
        "forbidden_hits": forbidden,
        "number_candidates": numbers,
        "question_count": q_count,
        "question_count_ok": is_replay or q_count <= FILTERS["soru_sayisi_maks"],
        "reflection_question_ratio": ratio,
        "reflection_question_ratio_ok": ratio is None or ratio >= FILTERS["yansitma_soru_orani_min"],
        "length_ok": len_ok,
        "length_error": len_err,
        "persona_kapilari_uygulandi": not is_replay,
    })
    # sert kapı: yalnızca kriz_yasagi (sözlü taahhüt ifadeleri, bağlamdan bağımsız her zaman yanlış).
    # rol_siniri SERT KAPI DEĞİL (2026-09-12 register sondası bulgusu): "teşhis" gibi kelimeler
    # modelin *doğru* reddi içinde de geçiyor ("ben teşhis koyamam") — kelime taraması bağlamı
    # ayırt edemiyor. Bu kategori de inceleme kuyruğuna gider (filter.py, Faz 2+).
    # kriz_yasagi sözlü taahhüt ifadeleri — BıRAG kuralı. Replay kaydında
    # "söz veriyorum" geçmesi olağan bir Türkçe cümledir, persona ihlali değil.
    hard_categories = SERT_KATEGORILER
    hard_forbidden_hit = (not is_replay) and any(k in forbidden for k in hard_categories)
    # reflection_question_ratio_ok SERT KAPI DEĞİL (2026-09-12 dikey dilim bulgusu, K40):
    # 20 kayıtlık ilk gerçek üretimde 17/20 yalnızca bu yüzden elendi — kısa, tek bileşik
    # yansıtma cümlesi + tek soru yapısı (doğru MI kalıbı, K28'in kısa completion bulgusuyla
    # tutarlı) cümle-sayma yöntemiyle 1:1 çıkıyor. Cümle içi virgül/tire ile ayrılan birden
    # fazla yansıtma fikri tek cümle sayılıyor. Bilgilendirici, sert kapı değil.
    # `thinking_dili_ok` SERT KAPI — plan.md'nin şartı (yanlış pozitif oranı önce
    # ölçülsün) 2026-09-16'da karşılandı: **0/2716**, ve bu kapı bugünkü korpusta
    # **0 kayıt** eliyor (ölçüldü). ⚠️ Yani bir tuzak teli: bugün hiçbir şey
    # yapmıyor, İngilizce thinking üretildiği gün yakalıyor.
    result["passed"] = (
        len_ok and result["question_count_ok"] and not hard_forbidden_hit
        and (ctx_ok or not v3_ve_sonrasi) and rep_ok and dil_ok
    )
    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("kullanım: uv run python src/checks.py <records.jsonl>")
        sys.exit(1)
    rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
    reports = [run_checks(r) for r in rows]
    dups = exact_hash_dedup(rows)
    passed = sum(1 for r in reports if r["passed"])
    print(f"kayıt: {len(rows)}  geçti: {passed}  elendi: {len(rows) - passed}  yinelenen id: {len(dups)}")
    for i, r in enumerate(reports):
        if not r["passed"]:
            print(f"[{i}] {r}")
