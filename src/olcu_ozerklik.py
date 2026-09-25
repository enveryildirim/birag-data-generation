"""`ozerklik_vurgusu` — TEK TANIM VE TEK EV.

⭐⭐ **T228 SONUCU `is_negative`'İN TERSİ ÇIKTI ve bu kendi başına bir bulgu.**
Aynı yöntem (üç anotatör, karıştırılmış liste, tabaka bilgisi verilmeden)
iki alana uygulandı ve aynı tür araç iki ayrı davranış gösterdi:

  · `is_negative` sözlüğü **hem fazla hem az** saydı (T227) ⇒ ölçüm
    olmaktan çıkarıldı.
  · `ozerklik_vurgusu` deseni **fazla saymıyor** — desenin tek başına
    ateşlediği 24 kaydın TAMAMI okundu ve 23'ü doğrulandı (%96). Ama
    **az sayıyor**: hiçbir yolla işaretlenmemiş 323 kaydın 26'sı okundu,
    5'inde özerklik vardı (%19).

➡️⭐⭐⭐ *Fark, edimlerin dilbilgisinde: özerklik bırakmanın Türkçede
sayılı ve kalıplaşmış birkaç kuruluşu var (*«senin kararın»*, *«sana
kalmış»*, *«karışmam»*) — sözlük onları yakalar. Red ise sınırsız biçimde
kurulabiliyor VE sözlüğü üç ayrı edimle paylaşıyor (red / rol sınırı /
bilgi sınırı). ⇒ Bir sözlüğün işe yarayıp yaramayacağını belirleyen şey,
ölçtüğü edimin kaç türlü söylenebildiği ve kaç edimle kelime paylaştığı.*

⛔ **Anotatörler uyumu:** `ozerklik` κ **0,85-0,97** (ham %93-99).
⛔⛔ Ön şart sorusu (*«ortada verilecek bir karar var mı»*) κ **0,16-0,52**
çıktı ⇒ T227'deki `talep` şartının karşılığı BURADA KURULAMAZ. Özerklik
için ön şart aranmıyor; sebebi ölçülmüş bir güvenilmezlik.

## Tanım (düzyazı — ölçüt budur, desen değil)

Asistanın son mesajı, bir kararın kullanıcıya ait olduğunu AÇIKÇA söylüyorsa
`ozerklik_vurgusu` taşır: kendi yerine karar vermeyeceğini, bir yön/talimat/
tarih koymayacağını, seçimin onda olduğunu belirtmek.

⛔ Şunlar özerklik vurgusu DEĞİLDİR:
  · **bilgi sınırı** — yalnızca bilmediğini söylemek
  · **rol sınırı** — yalnızca ne olmadığını söylemek
  · **takdir** — kullanıcının GEÇMİŞTE bir şeyi kendisinin yaptığını
    söylemek; özerklik GELECEKTEKİ bir karara dairdir
  · **soru sormak / yansıtmak / özetlemek**

## Alanın durumu (T230 sonrası — TAM SAYIM)

Korpusta beyan edilen: **131/412 (%32)**. ⭐ **Kestirim bileşeni yok:**
`A` (24) + `B` (65) + `C` (323) = 412, üç tabakanın üçü de tam sayıldı ve
412 kaydın 412'sinde `gen_meta.ozerklik_kaynak` duruyor.

| tabaka | ne | sayım | sonuç |
|---|---|---:|---|
| `A` | yalnız desen | 24/24 | 23 doğrulandı (%96) — desen fazla saymıyor |
| `B` | yalnız elle onayım | 65/65 | 57 tuttu (%88) — 8 onayım düştü |
| `C` | hiçbiri | 323/323 | 51'inde özerklik vardı (%16) — desen az sayıyor |

⭐⭐ **Gizli tekrar testi İKİ KEZ %100:** T228'de okunan kayıtlar sonraki
listelere karıştırıldı ve anotatörlere söylenmedi (C turunda 26/26, B
turunda 20/20). T227 ve T228'in bütün sayıları bu ölçülmeden duruyordu.

⭐ T228'in 26 kayıtlık kestirimi (~%34) tam sayımla **%32-33** çıktı;
elle onay kestirimi (%85) tam sayımla **%88**. Dar örneklemler kötü değil,
belirsiz kestirim veriyordu.

## Ölçütün iki sınırı (ayrışmalardan çıktı)

⛔⛔ **KAÇINMAK ≠ DEVRETMEK.** Bir hüküm ya da talimat vermekten kaçınmak
(*«ölçü koymuyorum»*) özerklik vurgusu değildir.

⛔⛔ **DEVRETMEK ≠ BİLMENİN ONDA OLDUĞUNU SÖYLEMEK.** *«O inancı sınayacak
olan sensin»* bilgiyi ona verir, kararı değil.

⇒ 25 ayrışmanın (C'de 18, B'de 7) tamamı bu iki sınırdaydı; rastgele değil.
"""
from __future__ import annotations

import re

# ⭐ Desen KALDIRILMADI (T227'de red sözlüğü kaldırılmıştı): burada %96
# kesinlikle çalışıyor ve blok kapısının hatırlatıcısı olarak kalıyor.
# ⛔ Ama tek başına ölçüt değil — `gen_meta.ozerklik_kaynak` taşıyan
# kayıtlarda uzlaştırma kararı üstündür ve desen onları YAZMAZ.
OZERKLIK_HATIRLATICI = re.compile(
    r"senin kararın|sen karar ver|karar sende|bana düşmez|"
    r"senin yerine karar|bırak demeyeceğim|ne yapacağını sen|"
    r"senin bileceğin|sen bilirsin|bunu senin yerine (söyle|karar)|"
    r"önerecek bir şeyim yok", re.I)


def hatirlatici(son_asistan: str) -> bool:
    """⛔ Kesinliği yüksek (%96), duyarlılığı düşük (~%19 kaçırma)."""
    return bool(OZERKLIK_HATIRLATICI.search(son_asistan))
