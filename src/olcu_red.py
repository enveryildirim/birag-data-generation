"""`is_negative` — TEK TANIM VE TEK EV.

⛔⛔⛔ **NEDEN VAR.** Bu alan depoda İKİ ayrı yerde, İKİ ayrı biçimde
ölçülüyordu (T226) ve ikisi, sözlüğün ateşlediği 70 kaydın 26'sında
ayrılıyordu. 26'sı üç anotatörle karara bağlandı (T227) ve sonuç şu:

  · **22'sinde sözlük FAZLA saydı** — ateşleyen cümle bir red değil, rol
    sınırı (*«benim işim değil»*) ya da bilgi sınırıydı (*«söyleyemem»*),
    ve ortada geri çevrilen bir İSTEK yoktu.
  · **4'ünde sözlük haklıydı** — istek vardı, talep sezicisi kaçırmıştı
    (biri ASCII yazılmış bir emir kipiydi: *«onu soyle»*).
  · Ve sözlüğün HİÇ ateşlemediği 7 kontrol kaydının ortalama **5,7**'sinde
    anotatörler red gördü ⇒ sözlük AZ da sayıyor.

➡️⭐⭐⭐ *Sözlük iki yönde birden yanlış ve onarılamaz: şablonlaşmadan
kaçınmak için red cümlesi her seferinde başka türlü kuruluyor (T218), yani
listeyi genişletmek onu kalıcı olarak geride bırakan şeyin ta kendisiyle
yarışmak demek.*

⇒ **KARAR (T227).** `is_negative` bir ÖLÇÜM değil, bir BEYANDIR. Hamleyi
yapan üretici (K30: kayıtları ben yazıyorum) onu yazarken beyan eder.
Buradaki desenler **hatırlatıcıdır**: bir kaydın okunmasını isterler,
alanı YAZMAZLAR.

## Tanım (düzyazı — ölçütün kendisi budur, desen değil)

Bir kayıt `is_negative` taşır ancak ve ancak:
  1. kullanıcı asistandan bir şey İSTEMİŞSE (söylemesini, yapmasını, karar
     vermesini, bir hüküm ya da bilgi vermesini), **ve**
  2. asistanın son mesajı istenen o şeyi GERİ ÇEVİRİYORSA.

⛔ Şunlar `is_negative` DEĞİLDİR:
  · **rol sınırı** — istenmediği hâlde ne olmadığını söylemek
    (*«terapistin değilim»*)
  · **bilgi sınırı** — bilmediğini söylemek (*«belgede yazmıyor»*)
  İkisi de değerlidir ve ayrı alanlarda durur; ama istek yoksa red yoktur.

⚠️ Kendine sorulan soru talep değildir (*«kendime ‹bunu hak ediyor musun›
diye soruyorum»*) — anotasyonda üç anotatör de bunda birleşti.
"""
from __future__ import annotations

import re

from .tohum_guvenlik import tr_sadelestir

# ⛔⛔ HATIRLATICI, ÖLÇÜT DEĞİL. Bu desenlerin çıktısı hiçbir alana yazılmaz;
# yalnız «bu kaydı oku» der. Genişletilmeleri de gerekmiyor: eksik olmaları
# tanımın bir parçası (yukarıdaki gerekçe).
#
# ⭐ Eski `(söyle|belirle|yorumla)` kolu ONARILDI: *«bunu ben söylemedim»*
#    cümlesini red sayıyordu ve iki kayıtta (parti3 `#8`, `#54`) tam olarak
#    bu yüzden yanlış ateşledi. Artık yetersizlik eki aranıyor.
RED_HATIRLATICI = re.compile(
    r"veremem|söyleyemem|yapamam|bana düşmez|benim işim değil|"
    r"yerine geçemem|karar veremem|cevabı bende yok|"
    r"bunu ben (söyleyemem|belirleyemem|yorumlayamam)", re.I)

# ⭐ Talep sezicisi genişletildi ve ASCII yazıma dayanıklı hâle getirildi
# (Kural 4: düz `str.lower()` yok, `tr_sadelestir`). Yine de bir hatırlatıcı:
# *«kendime ‹hak ediyor musun› diye soruyorum»* bunu ateşler ve talep değildir.
_TALEP = re.compile(
    r"\?|\bsoyle\b|\bsoyler misin\b|\bne yapayim\b|\bne dersin\b|"
    r"\bsence\b|\bsizce\b|\bnasil\b|\bnereye\b|\bnereden\b|"
    r"\b(mi|mu|mi|mu)\b|\bm[iu]s[iu]n\b|\bolur mu\b|"
    r"\bde\b\s*$|\bsoyle\b\s*$", re.I | re.M)


def talep_izi(kullanici_turlari: list[str]) -> bool:
    """Kullanıcı turlarında bir TALEP izi var mı — hatırlatıcı."""
    return bool(_TALEP.search(tr_sadelestir(" ".join(kullanici_turlari))))


def hatirlatici(son_asistan: str, kullanici_turlari: list[str]) -> bool:
    """⛔ KARAR VERMEZ. `True` dönerse kayıt OKUNMALI; `is_negative` alanını
    yazmak için kullanılamaz."""
    return bool(RED_HATIRLATICI.search(son_asistan)) and talep_izi(kullanici_turlari)
