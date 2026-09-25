# Anotasyon görevi — iki soru, bir grup diyalog parçası

Türkçe bir bağımlılık destek sohbetinden alınmış parçaları etiketleyeceksin.
Her öğede kullanıcının turları (`kullanici`) ve asistanın SON mesajı
(`son_asistan`) var. Sohbetin kalitesini DEĞERLENDİRMİYORSUN, iki olgusal
soruya cevap veriyorsun.

## TEK SORU — `ozerklik`: Asistanın son mesajı kararı açıkça KULLANICIYA BIRAKIYOR mu?

`evet` = asistan bir kararın kullanıcıya ait olduğunu açıkça söylüyor:
kendi yerine karar vermeyeceğini, bir yön/talimat/tarih koymayacağını,
seçimin onda olduğunu belirtiyor.

`hayir` = böyle bir cümle yok.

⛔ Şunlar özerklik vurgusu DEĞİLDİR:
  - **bilgi sınırı**: yalnızca bilmediğini söylemek (*«bunu bilmiyorum»*)
  - **rol sınırı**: yalnızca ne olmadığını söylemek (*«terapistin değilim»*)
  - **takdir**: kullanıcının GEÇMİŞTE bir şeyi kendisinin yaptığını
    söylemek (*«bunu sen fark ettin»*) — özerklik GELECEKTEKİ bir karara
    dair olmalı
  - **soru sormak / yansıtmak / özetlemek** — kullanıcıyı konuşturmak tek
    başına özerklik vurgusu değildir

⛔ SÖZCÜK ARAMIYORSUN. *«Senin kararın»* demeden de özerklik bırakılabilir;
bu kalıbı kullanıp da karar bırakmayan bir cümle olabilir.

## Çıktı

YALNIZCA şu biçimde bir JSON dizisi yaz, başka hiçbir şey yazma:

[{"id":"P1-01","ozerklik":"hayir","not":"en fazla 12 kelime"}, ...]


Girdideki HER öğe için bir satır olmalı.
