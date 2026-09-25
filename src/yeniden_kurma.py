"""`uretim-v6` yeniden kurma kapıları (K277) — `v0.1.0` kaydı → `v0.1.1` kaydı.

⭐ Yeniden kurma yalnız iki şeye dokunabilir: son asistan turunun `thinking`i ve
bitiş adayında cevabın **son cümlesi**. Bu modül bunu denetler:

  zarf(eski, yeni)             izinli alanlar dışında bayt bayt aynı mı
  dusunme_temizligi(th, kayit) ⛔/⭐ · biçim · üretim iskelesi · ritüel kalıp
  karar_eslemesi(...)          `korunan_kararlar` iki metinde birebir var mı
  son_cumle_uygula(...)        cevabın gövdesini koruyarak son cümleyi değiştirir

⛔ Kapılar yalnız **yeniden kurulmuş** kayıtlara uygulanır. `v0.1.0` kayıtlarının
%23'ü ⛔/⭐ taşıyor; bu kapıdan geçirilselerdi düşerlerdi — temizlik yeni
sürümün hedefidir, eski sürümün kusuru olarak geriye dönük uygulanmaz.
"""
from __future__ import annotations

import copy
import json
import re

from tohum_guvenlik import tr_fold, tr_sadelestir
from yansitma import _dizge, konusma_metni

ISARET = re.compile("[⛔⭐✅❌⚠️➡️]")
BICIM = re.compile(r"\*\*|^\s*#{1,6}\s|^\s*[*\-•]\s|^\s*\d+[.)]\s", re.M)
# ⛔⛔ Bu desen AKSANSIZ yazılmış ⇒ yalnız `tr_sadelestir` ile aranır, `tr_fold`
# ile DEĞİL. `tr_fold` aksanı düşürmez: «mesajdan çıkarıldı» → «mesajdan çikarildi»
# ve «üretimde» → «üretimde» kalır, ikisi de bu desene takılmaz. Faz 2 blok 1'de
# üç kayıt bu yüzden iskeleyle geçti (T75 · T84 ailesinin yeni bir örneği).
ISKELE = re.compile(r"tohum|izgara|\bkota|\bbeyan|§|\bparti\s?\d|\b[kt]\d{2,3}\b|"
                    r"mesajdan cikarildi|ilk yazimda|uretim(de| sirasinda)|"
                    # ⭐ 2026-09-25: yeniden kurma sürecinin kendisine atıf («bitişi değiştirmiyorum»,
                    # «bu kayıtta») — dağıtılmış modelde değiştirilecek bir «bitiş» yok
                    r"bitisi (bu yuzden )?degistir|bu kayitta")
RITUEL = re.compile(r"\bsoru(yu)?\s+(da\s+)?sormuyorum\b")
# ⭐ Faz 2 blok 4'te yakalandı: MI süreç adları ve bu repodaki üretim terimleri
# («evoking», «güvenlik sapması») düşünmeye sızıyordu; kapı görmüyordu, pilotta
# da bir tane vardı. AKSANSIZ desen ⇒ tr_sadelestir ile aranır. ⚠️ «mi» ya da
# «MI» eklenmez: Türkçe soru ekiyle çakışır.
JARGON = re.compile(r"\b(evoking|engaging|focusing|planning|sustain talk|change talk|"
                    r"karar dengesi|guvenlik sapmasi|izgara sapmasi|marlatt|miti|ave)\b")
KURAL_OKUMA = re.compile(r"tek seferde|\bkural|protokol")
# ⭐ 2026-09-25 (kullanıcı kararı): yaş ÜSTVERİDİR. age_group modele gitmez ⇒
# konuşmada açık yaş yoksa düşünme yaşı olgu gibi yazamaz (K51). Çekinceli kullanım
# meşru olabildiği için kapı İNCELEMEYE düşürür, sert değil; hükmü okuyucu verir.
YAS = re.compile(r"\bergen\w*|\bbu yaşta|\bgenç biri|\bçocuk yaşta")
# Cinsiyet de üstveri gibi davranır: konuşmada ipucu yoksa düşünme kişiye «adam»,
# «kadın» diyemez. ⚠️ Desenler tr_fold'dan GEÇİRİLİR — metin katlanmış, desen de
# katlanmalı (aynı oturumda «ı»lı bir desen katlanmış metinde iki kez ölü kaldı).
CINS = re.compile(tr_fold(r"\b(adam|kadın|erkek|genç kız|delikanlı|hanımefendi)\b"))
CINS_IPUCU = re.compile(tr_fold(r"\b(karım|hanımım|hanım|kocam|bir kadınım|bir erkeğim|annesiyim|"
                                r"babasıyım|emzir\w*|hamile\w*|lohusa|adam olamam|adam gibi|abi|abla)\b"))
ACIK_YAS = re.compile(r"\b(1[0-9]|on (bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz)) yaş|"
                      r"\byaşındayım|\blise|\blgs\b|\bortaokul|\byks\b")
BUYUK = re.compile(r"\b[A-ZÇĞİÖŞÜ]{3,}\b")
TIRNAK = re.compile(r'"([^"\n]{4,})"|«([^»\n]{4,})»|“([^”\n]{4,})”')
BITIS_KARARI = {"aday_degil", "degisti", "degismedi", "korunan_soru"}
KORUNAN_SORU = {"guvenlik", "izin", "sor_sun_sor", "seyrek_girdi"}


def _son_asistan(kayit: dict) -> dict:
    return [m for m in kayit["messages"] if m["role"] == "assistant"][-1]


def _nrm(s: str | None) -> str:
    return re.sub(r"\s+", " ", ISARET.sub("", tr_fold(s or ""))).strip()


def son_cumle_uygula(icerik: str, son_cumle: dict) -> str:
    """`eski` cevabın SONU olmak zorunda; gövde bayt bayt korunur."""
    eski, yeni = son_cumle["eski"], son_cumle["yeni"]
    govde = icerik.rstrip()
    if not eski or not govde.endswith(eski.rstrip()):
        raise ValueError("son_cumle.eski cevabın sonu değil")
    return govde[: len(govde) - len(eski.rstrip())] + yeni


def zarf(eski: dict, yeni: dict) -> list[str]:
    """İzinli alanlar dışında fark → ihlal listesi."""
    ihlal = []
    a, b = copy.deepcopy(eski), copy.deepcopy(yeni)
    for r in (a, b):
        r.pop("_checks", None)
        r.pop("judge", None)                      # bitişi değişende yeniden yargılanır
        r.get("gen_meta", {}).pop("yeniden_kurma", None)
    sa, sb = _son_asistan(a), _son_asistan(b)
    sa.pop("thinking", None)
    sb.pop("thinking", None)
    if sa["content"] != sb["content"]:
        yk = (yeni.get("gen_meta") or {}).get("yeniden_kurma") or {}
        sc = yk.get("son_cumle")
        if not sc:
            ihlal.append("cevap değişmiş ama son_cumle beyanı yok")
        else:
            try:
                if son_cumle_uygula(sa["content"], sc) != sb["content"]:
                    ihlal.append("yeni cevap = gövde + son_cumle.yeni değil")
            except ValueError as e:
                ihlal.append(str(e))
        sb["content"] = sa["content"]
    ga, gb = a.get("gen_meta", {}), b.get("gen_meta", {})
    if ga.get("turn_ending") != gb.get("turn_ending"):
        if sa["content"] == _son_asistan(yeni)["content"]:
            ihlal.append("turn_ending değişmiş ama cevap aynı")
        gb["turn_ending"] = ga.get("turn_ending")
    if json.dumps(a, sort_keys=True, ensure_ascii=False) != \
            json.dumps(b, sort_keys=True, ensure_ascii=False):
        ihlal.append("izinli alanlar dışında fark var")
    return ihlal


def dusunme_temizligi(th: str, kayit: dict, eski_th: str = "") -> tuple[list, list]:
    """(sert ihlaller, incelenecekler). Sert olan kaydı reddettirir."""
    sert, incele = [], []
    f = tr_fold(th)
    if ISARET.search(th):
        sert.append("işaret (⛔/⭐ vb.)")
    if BICIM.search(th):
        sert.append("başlık / madde / numara / kalın")
    # ⚠️ ISKELE aksansız desen ⇒ sadeleştirilmiş metinde aranır; konuşma tarafı da
    # aynı foldla karşılaştırılır, yoksa kullanıcının kendi sözcüğü muaf kalmaz.
    fs, konusma = tr_sadelestir(th), tr_sadelestir(konusma_metni(kayit))
    for m in ISKELE.finditer(fs):
        # ⚠️ «kota», «beyan», «üretimde» kullanıcının kendi konusu olabilir
        # (internet kotası, iş yerinde üretim) — konuşmada geçiyorsa iskele değil
        if m.group(0) == "§" or m.group(0) not in konusma:
            sert.append(f"üretim iskelesi: «{m.group(0)}»")
            break
    if RITUEL.search(f):
        sert.append("«soru sormuyorum» kalıbı")
    for m in JARGON.finditer(fs):
        if m.group(0) not in konusma:
            sert.append(f"yöntem/üretim terimi: «{m.group(0)}»")
            break
    kaynak = _dizge(konusma_metni(kayit) + " " + _son_asistan(kayit)["content"])
    for w in BUYUK.findall(th):
        if _dizge(w) not in kaynak:
            sert.append(f"büyük harfle vurgu: «{w}»")
    if m := KURAL_OKUMA.search(f):
        incele.append(f"kural okuma olabilir: «{m.group(0)}»")
    kul = tr_fold(" ".join(x["content"] for x in kayit["messages"] if x["role"] == "user"))
    if (m := YAS.search(f)) and not ACIK_YAS.search(kul):
        incele.append(f"yaş ifadesi ama konuşmada açık yaş yok: «{m.group(0)}» — çekinceli mi?")
    if (m := CINS.search(f)) and not CINS_IPUCU.search(kul):
        incele.append(f"cinsiyetli kişi sözcüğü ama konuşmada ipucu yok: «{m.group(0)}»")
    izinli = kaynak + " " + _dizge(eski_th)
    for g in TIRNAK.finditer(th):
        a = next(x for x in g.groups() if x)
        if _dizge(a) not in izinli:
            incele.append(f"tırnak konuşmada/eski düşünmede yok: «{a[:60]}»")
    return sert, incele


def karar_eslemesi(kararlar: list[dict], eski_th: str, yeni_th: str) -> list[str]:
    sorun = []
    if not kararlar:
        return ["korunan_kararlar boş"]
    ea, ya = _nrm(eski_th), _nrm(yeni_th)
    for i, k in enumerate(kararlar, 1):
        if _nrm(k.get("eski")) not in ea:
            sorun.append(f"#{i} eski parça eski düşünmede yok")
        if k.get("yeni") is None:
            if not (k.get("not") or "").strip():
                sorun.append(f"#{i} düşürülmüş ama not yok")
        elif _nrm(k["yeni"]) not in ya:
            sorun.append(f"#{i} yeni parça yeni düşünmede yok")
        # ⭐ Faz 2 blok 1'de yakalandı: üretim iskelesi «korunan karar» diye
        # listelenmiş ve üstelik anlamı kayarak taşınmıştı («hepsi mesajdan
        # çıkarıldı» → «hepsi kendi mesajından çıkarıldı»). İskele korunacak
        # bir karar değildir (karar-korunumu.v1 §1a); yeni tarafta hiç
        # görünmemeli. Eski tarafta görünebilir — orası temizlenecek metin.
        elif (m := ISKELE.search(tr_sadelestir(k["yeni"]))):
            sorun.append(f"#{i} yeni parçada üretim iskelesi: «{m.group(0)}»")
    return sorun


def _sina() -> None:
    k = {"messages": [{"role": "user", "content": "Bugün AMATEM'i aradım, iyi geldi."},
                      {"role": "assistant", "content": "Aradın. Nasıl geçti?",
                       "thinking": "⛔ Tohumda X vardı. Soru sormuyorum, duruyorum."}],
         "gen_meta": {"turn_ending": "acik_uclu_soru"}}
    y = copy.deepcopy(k)
    sc = {"eski": "Nasıl geçti?", "yeni": "Aramak için bir adım attın."}
    _son_asistan(y)["content"] = son_cumle_uygula(_son_asistan(k)["content"], sc)
    _son_asistan(y)["thinking"] = "Aradığını yazıyor; AMATEM adını o verdi."
    y["gen_meta"]["turn_ending"] = "takdir"
    y["gen_meta"]["yeniden_kurma"] = {"son_cumle": sc}
    assert _son_asistan(y)["content"] == "Aradın. Aramak için bir adım attın.", "uygula"
    assert zarf(k, y) == [], zarf(k, y)
    y2 = copy.deepcopy(y)
    y2["messages"][0]["content"] += " "
    assert "izinli alanlar dışında fark var" in zarf(k, y2), "kullanıcı turu korunmuyor"
    s, _ = dusunme_temizligi(_son_asistan(k)["thinking"], k)
    assert any("işaret" in x for x in s) and any("iskele" in x for x in s) and \
        any("kalıbı" in x for x in s), s
    s, _ = dusunme_temizligi(_son_asistan(y)["thinking"], y)
    assert s == [], f"konuşmadaki kısaltma vurgu sayılmamalı: {s}"
    s, _ = dusunme_temizligi("Bunu ANMIYORUM.", y)
    assert any("büyük harf" in x for x in s), s
    s, _ = dusunme_temizligi("Rakamı anmıyorum, mesajdan çıkarıldı.", y)
    assert any("iskele" in x for x in s), f"aksanlı iskele kaçtı: {s}"
    s, _ = dusunme_temizligi("Bunu üretimde konuşmuştuk.", y)
    assert any("iskele" in x for x in s), f"aksanlı «üretimde» kaçtı: {s}"
    s, _ = dusunme_temizligi("Evoking turu, güvenlik sapması yapmıyorum.", y)
    assert any("terim" in x for x in s), f"jargon kaçtı: {s}"
    s, _ = dusunme_temizligi("Bunu mi diye sormuyor, ama gelecek mi?", y)
    assert not any("terim" in x for x in s), f"Türkçe «mi» terim sayıldı: {s}"
    _, inc = dusunme_temizligi("Bir ergen ve bu yaşta kapanır.", y)
    assert any("yaş ifadesi" in x for x in inc), f"yaş sızıntısı kaçtı: {inc}"
    _, inc = dusunme_temizligi("Adam iki duygu arasında sıkışmış.", y)
    assert any("cinsiyet" in x for x in inc), f"cinsiyet varsayımı kaçtı: {inc}"
    kota = copy.deepcopy(y)
    kota["messages"][0]["content"] = "İnternet kotam bitti, telefonsuz kaldım."
    s, _ = dusunme_temizligi("Kotası bitince telefonsuz kalmış.", kota)
    assert s == [], f"kullanıcının kendi sözcüğü iskele sayılmamalı: {s}"
    kk = [{"eski": "Tohumda X vardı.", "yeni": None, "not": "yalnız iskele"}]
    assert karar_eslemesi(kk, _son_asistan(k)["thinking"], "a") == []
    assert karar_eslemesi([{"eski": "yok böyle", "yeni": "a"}], "b", "a") == \
        ["#1 eski parça eski düşünmede yok"]


if __name__ == "__main__":
    _sina()
    print("✅ yeniden_kurma sınaması geçti")
