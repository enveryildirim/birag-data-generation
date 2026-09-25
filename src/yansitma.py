"""Yansıtma sadakati — cevabın kullanıcıya atfettiği şey konuşmada var mı?

⛔⛔ **Neden var (T265).** `celiskili` sınıfının 12 kaydının 3'ünde cevap,
kullanıcının **söylemediği** bir ayrıntıyı ona atfediyordu ("baş ağrısıyla
açıklıyorsun", "arkadaşın şaka gibi söylemiş", "«Güvensiz biriymişim
gibi» dedin"). Üçünde de ayrıntı **tohumda** vardı: cevabı tohumdan
yazdım, kullanıcı mesajı ise tohumun kısaltmasıydı.

T217 kapısı *«kullanıcı metni kendi tohumundan mı?»* diye soruyordu.
Bu modül **tersini** sorar: ***«cevap yalnız konuşmadan mı?»***

⭐ **İki ayrı sıkılıkta iki kural** — çünkü ikisinin ölçülen kesinliği
farklı (bkz. `reports/analiz/2026-09-22-yansitma-kalibrasyon.md`):

  **A — ALINTI (dar, kesin).** Cevap «…» ya da "…" içinde bir şeyi
  kullanıcıya atfediyorsa (yakınında `dedin`/`yazmışsın`/`demişsin`…),
  alıntının içeriği kullanıcı turlarında **bulunmalı**. Alıntı bir
  iddiadır: kullanıcı bunu *söyledi* demektir.

  **B — YANSITMA (geniş, gürültülü).** İkinci tekil şahıs eki taşıyan
  cümlelerde geçen içerik sözcükleri konuşmada (kullanıcı turları +
  `<context>`) aranır; bulunmayanlar **yeni** sayılır. ⛔ Bu kural
  yeniden ifadeyi (parafrazı) yeniden ifade olarak tanıyamaz ⇒ yanlış
  pozitif üretir ve **kapı değil rapordur** (K40 emsali).

⛔ Kök eşleme 5 harfe kısaltır (Türkçe ek sorunu, K40/T22 ailesi) ⇒ hem
yanlış pozitif hem yanlış negatif verebilir. Durak listesi **elle**
yazıldı.
"""
from __future__ import annotations

import re

from tohum_guvenlik import tr_fold, tr_sadelestir

# İkinci tekil şahıs: cevabın kullanıcı hakkında hüküm kurduğu yer.
# ⛔⛔ İlk sürüm `-sın|-sin|-tin|-dın` eklerini de arıyordu ve **isimleri fiil
#   sandı** (`hizmetin`, `kaydın`) ⇒ kalibrasyonda kural 1176 kaydın 1023'ünde
#   ateşledi, kesinlik tesadüf düzeyine düştü. Yalnız fiil olduğu **belirsiz
#   olmayan** biçimler bırakıldı.
_SAHIS = re.compile(
    r"\b\w{3,}(?:mışsın|mişsin|muşsun|müşsün|yorsun|acaksın|eceksin"
    r"|mıştın|miştin|muştun|müştün)\b", re.I)

# Alıntıyı kullanıcıya bağlayan eylemler.
_ATIF_EYLEM = re.compile(
    r"\b(dedin|demişsin|demiştin|diyorsun|söyledin|söylemişsin|söylüyorsun"
    r"|yazdın|yazmışsın|yazıyorsun|anlatmışsın|anlatıyorsun|belirtmişsin"
    r"|sormuşsun|soruyorsun)\b", re.I)

# ⛔⛔ Olumsuz atıf, atıf DEĞİLDİR. «Sana "haklısın" demeyeceğim» ve
#   «"kızgınım" gibi bir cümle kurmadın» kullanıcıya bir şey atfetmez —
#   tersini söyler. İlk sürüm bunları ihlal saydı (kalibrasyonda görüldü).
_OLUMSUZ = re.compile(
    r"\b\w{2,}(?:madın|medin|mamışsın|memişsin|mazsın|mezsin"
    r"|meyeceğim|mayacağım|miyorum|mıyorum|mem|mam|medim|madım)\b", re.I)

_ALINTI = re.compile(r"«([^»]{4,200})»|\"([^\"]{4,200})\"|“([^”]{4,200})”")
_CTX = re.compile(r"<context.*?</context>|<CTX>", re.S)
_CUMLE = re.compile(r"[^.!?\n]+[.!?]?")

# ⛔ Durak kökleri elle yazıldı — ölçümü DARALTIR (şişirmez).
_DURAK = {w[:5] for w in """
gibi şimdi yine ama için bunu şunu onun sonra önce kadar daha çok bir bu
şey olan olarak diye kendi ben sen biz siz biraz zaten şöyle böyle hem
yani hep hiç her bazı öyle nasıl neden niye eğer ise ile göre üzere
yan yana birlikte arada aynı başka öteki ikisi üçü hangi kim ne
duruyor duran olmak olan oldu olur var yok değil mi mu
senin sana seni bende bana beni onu ona onda
şunlar bunlar burada orada şurada
""".split()}


# ⛔⛔ İlk sürüm kökü «ilk 5 harf» sayıyordu ve **iyelik ekini tanımıyordu**:
#   `eşim` ↔ `eşinin`, `annem` ↔ `annen`, `ses` ↔ `sesin` ayrı kök çıkıyordu ⇒
#   kullanıcının SÖYLEDİĞİ şey «yeni» görünüyordu. Hafif ek soyucuyla
#   değiştirildi (T22 ailesinin Türkçe tuzağı).
_EK = ["larının", "lerinin", "larında", "lerinde", "ların", "lerin", "ları",
       "leri", "lar", "ler", "sının", "sinin", "nın", "nin", "nun", "nün",
       "ının", "inin", "unun", "ünün", "ndan", "nden", "tan", "ten", "dan",
       "den", "da", "de", "ta", "te", "yla", "yle", "la", "le", "sı", "si",
       "su", "sü", "ım", "im", "um", "üm", "ın", "in", "un", "ün",
       "ı", "i", "u", "ü", "a", "e", "m", "n"]


# ⛔⛔ Kural 4: düz `str.lower()` YASAK. İlk sürümde kullandım ve `İtiraf`
#   → `i̇tiraf` (birleşik nokta) olduğu için kök `tiraf` çıkıyordu; kullanıcının
#   yazdığı `itiraf` ile EŞLEŞMİYORDU ⇒ gerçek eşleşmeler «karşılıksız» sayıldı.
_EK_F = sorted({tr_fold(e) for e in _EK}, key=len, reverse=True)


def _soy(w: str, en_az: int = 3) -> str:
    w = tr_fold(w)
    degisti = True
    while degisti and len(w) > en_az:
        degisti = False
        for ek in _EK:
            if w.endswith(ek) and len(w) - len(ek) >= en_az:
                w, degisti = w[:-len(ek)], True
                break
    return w


def _kok(metin: str, n: int = 5) -> set[str]:
    return ({_soy(w) for w in re.findall(r"\w{4,}", tr_fold(metin))}
            - {_soy(d) for d in _DURAK})


def konusma_metni(record: dict) -> str:
    """Kullanıcının söyledikleri + `<context>` pasajları.

    ⛔ Asistan turları DAHİL DEĞİL: cevabın kendi önceki cümlesine
    dayanarak «sen dedin» demesi zaten kusurdur.
    """
    parca = []
    for m in record.get("messages", []):
        if m.get("role") == "user":
            parca.append(m.get("content") or "")
    for p in record.get("context") or []:
        parca.append(p.get("metin") or "" if isinstance(p, dict) else str(p))
    return "\n".join(parca)


def kullanici_turlari(record: dict) -> str:
    """Yalnız kullanıcının yazdıkları — `<context>` sökülmüş."""
    return "\n".join(_CTX.sub(" ", m.get("content") or "")
                     for m in record.get("messages", [])
                     if m.get("role") == "user")


def _son_cevap(record: dict) -> str:
    for m in reversed(record.get("messages", [])):
        if m.get("role") == "assistant":
            return m.get("content") or ""
    return ""


def _dizge(metin: str) -> str:
    """Aksan ve boşluk duyarsız karşılaştırma dizgesi.

    ⛔ Kalibrasyonda üç yanlış pozitifin **üçü de** buradan geldi:
    kullanıcı `universitede zaten icecegim` yazmıştı (aksansız), cevap
    `üniversitede zaten içeceğim`; bir başkası `hiç bir`, cevap `hiçbir`.
    `tr_sadelestir` aksanı, boşluk sökümü de yazım ayrımını kapatır.
    """
    return re.sub(r"\W+", "", tr_sadelestir(metin))


def alinti_ihlalleri(record: dict) -> list[tuple[str, list[str]]]:
    """A kuralı: kullanıcıya atfedilen ALINTI kullanıcı turlarında yok mu?

    Dönen: [(alıntı, konuşmada bulunmayan kökler), …]
    """
    cevap = _son_cevap(record)
    if not cevap:
        return []
    kul_ham = kullanici_turlari(record)
    kul, kul_dizge = _kok(kul_ham), _dizge(kul_ham)
    ihlal = []
    for m in _ALINTI.finditer(cevap):
        span = next(g for g in m.groups() if g)
        kuyruk = cevap[m.end():m.end() + 40]
        bas = cevap[max(0, m.start() - 40):m.start()]
        if not (_ATIF_EYLEM.search(kuyruk) or _ATIF_EYLEM.search(bas)):
            continue
        # ⛔ Olumsuz atıf atıf değildir — ve olumsuzluk eki alıntıdan SONRA
        #   gelir («…demeyeceğim», «…kurmadın»). İlk sürüm öncesine de
        #   bakıyordu ve uzaktaki bir «çıkaramıyorum» kapıyı susturuyordu:
        #   kapı asıl hedefini (T265 #11) BU YÜZDEN kaçırdı.
        if _OLUMSUZ.search(kuyruk):
            continue
        # ⛔ Karşıtlama: «…» demişsin, «…» değil — ikincisi atıf değildir.
        if re.match(r"\s*(değil|degil)\b", kuyruk):
            continue
        # Birebir (aksan/boşluk duyarsız) geçiyorsa zaten dayanaklıdır.
        if _dizge(span) and _dizge(span) in kul_dizge:
            continue
        yeni = sorted(_kok(span) - kul)
        if yeni:
            ihlal.append((span.strip(), yeni))
    return ihlal


def yansitma_yeni(record: dict) -> list[tuple[str, list[str]]]:
    """B kuralı: 2. tekil şahıslı cümlelerdeki YENİ içerik sözcükleri.

    ⛔ RAPOR — kapı değil. Parafrazı tanıyamaz.
    """
    cevap = _son_cevap(record)
    if not cevap:
        return []
    kon = _kok(konusma_metni(record))
    bulgu = []
    for c in _CUMLE.findall(cevap):
        if not _SAHIS.search(c):
            continue
        # Atıf eylemlerinin kendisi içerik değildir.
        temiz = _ATIF_EYLEM.sub(" ", _SAHIS.sub(" ", c))
        yeni = sorted(_kok(temiz) - kon)
        if yeni:
            bulgu.append((c.strip()[:90], yeni))
    return bulgu


def yansitma_ok(record: dict) -> tuple[bool, str | None]:
    """KAPI — yalnız A kuralı (alıntı). B kuralı raporda kalır.

    Alıntıyla kullanıcıya bir söz atfetmek en sert iddiadır ve en az
    parafraz riski taşır; kapı oraya kurulur.
    """
    ihlal = alinti_ihlalleri(record)
    if not ihlal:
        return True, None
    span, yeni = ihlal[0]
    return False, (f"kullanıcıya atfedilen alıntı kullanıcı turlarında yok: "
                   f"«{span[:60]}» (karşılıksız kök: {', '.join(yeni[:4])})")
