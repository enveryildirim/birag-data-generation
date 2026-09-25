"""Rapor şerhleri — TEK yerde yazılır, her rapor buradan ÇAĞIRIR.

⛔ Bu dosya rapor üretmez; `scripts/analiz/2026-09-16-rapor-serh-denetimi.py`
bu şerhlerin yazılıp yazılmadığını sınar. ⭐ Metnin tek bir yerde durmasının
sebebi T70: aynı kural iki ayrı yerde yazılınca **ikisi de tutulmayabilir** ve
hangisinin doğru olduğu sorulamaz.
"""

# T68 · Ş1 — güvenlik ekseninde bildirilen her ihlal sayısının yanına.
UST_SINIR = [
    "> ⚠️ **Standart şerh — bu sayılar ÜST SINIRDIR (T68).** Güvenlik judge'larının",
    "> **tek yönlü tedbirli sapma** gösterdiği bildiriliyor ve bizim asimetrik",
    "> doğrulamamız (doğrulanamayan *muafiyet* düşer, doğrulanamayan *suçlama*",
    "> yalnız kaydedilir) bu sapmayı azaltmaz — **aynı yöne ekler**. ⛔ Judge'ın",
    "> yanlış pozitif oranı **uzmana karşı hiç ölçülmedi**; ölçülene kadar buradaki",
    "> ihlal sayıları *«en çok bu kadar»* diye okunmalı, *«tam olarak bu kadar»* diye",
    "> değil. ➡️ Yön Kural 3 açısından **güvenli** taraftadır: hata payı ihlali",
    "> abartma yönünde, gözden kaçırma yönünde değil.",
    "",
]

# T63 · Ş2 — kol sırası kuran her tabloya.
TERS_CIFT = [
    "> ⚠️ **Standart şerh — sıra numarası tek başına okunmaz (T63).** Eşitliğin sık",
    "> olduğu bir kol kümesinde sıra, eşitlik bozucu ada duyarlıdır: ilk hesap",
    "> *«4 kolun sırası değişti»* demişti, **kesin ters dönen çiftlerle** ölçülen",
    "> doğru sayı **1**'di. ➡️ Sıra yazılıyorsa yanında eşitlik ve **ters çift**",
    "> sayısı da okunmalı.",
    "",
]
