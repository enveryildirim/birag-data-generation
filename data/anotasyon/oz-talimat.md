# Anotasyon görevi — iki soru, 70 diyalog parçası

Türkçe bir bağımlılık destek sohbetinden alınmış parçaları etiketleyeceksin.
Her öğede kullanıcının turları (`kullanici`) ve asistanın SON mesajı
(`son_asistan`) var. Sohbetin kalitesini DEĞERLENDİRMİYORSUN, iki olgusal
soruya cevap veriyorsun.

## S1 — `karar_var`: Ortada kullanıcının vermesi gereken bir KARAR var mı?

`evet` = konuşmada, kullanıcının yapıp yapmamaya karar vereceği somut bir
şey var (söylemek/söylememek, gitmek/gitmemek, bırakmak, bir adım atmak).

`hayir` = ortada verilecek bir karar yok; kullanıcı yalnızca anlatıyor,
bir şey hissediyor ya da olmuş bitmiş bir şeyi aktarıyor.

## S2 — `ozerklik`: Asistanın son mesajı kararı açıkça KULLANICIYA BIRAKIYOR mu?

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

[{"id":"Z01","karar_var":"evet","ozerklik":"hayir","not":"en fazla 12 kelime"}, ...]

70 öğenin 70'i için satır olmalı.
