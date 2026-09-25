# Alıntıda edat düşmesi — 21 bulgu elle okundu

**Betik:** `scripts/analiz/2026-09-18-alinti-edat-dusmesi.py` · **Tarih:** 2026-09-18  
**Girdi:** `datasets/v0.0.11/train.jsonl` · bulgu **16**

⭐ Üç yeni ANMA çerçevesi kapıya eklendikten sonra 21 → **16**; kalan 16'sı
tek bir örüntü. Her bulgu için kullanıcının en yakın parçası `difflib` ile
bulundu.

| benzerlik | alıntı | kullanıcının yazdığı | düşen |
|---:|---|---|---|
| 0.94 | *«Gerçeği söylemek mümkün değil»* | *«gerçeği söylemek de mümkün değil.»* | `de, değil.` |
| 0.92 | *«Benim bildiğim bir şey var ki onlar bilmiy»* | *«Ama benim bildiğim bir şey var ki onlar bilmiyor»* | `ama, bilmiyor,, o` |
| 0.88 | *«yanlış mı bilmiyorum, garip hissediyorum»* | *«Yanlış mı bilmiyorum, biraz garip hissediyorum b»* | `biraz, bunu` |
| 0.87 | *«icra dosyasına bir nefes olur, kimsenin ha»* | *«'icra dosyasına bir nefes olur, eşim duymaz, kim»* | `'icra, eşim, duymaz,, olmaz'` |
| 0.86 | *«Ortada büyük bir şey yok»* | *«ortada büyük bir şey de yok. İlk»* | `de, yok., ilk` |
| 0.85 | *«Kumardan diyemezsin di mi»* | *«kumardan diyemezsin ki di mi? bide»* | `ki, mi?, bide` |
| 0.83 | *«hiçbir işe yaramıyor»* | *«hiç bir işe yaramıyor galiba»* | `hiç, bir, galiba` |
| 0.78 | *«İçim bir tuhaf»* | *«ama içim de bir tuhaf,»* | `ama, de, tuhaf,` |
| 0.77 | *«İçim buna razı değil»* | *«içim de buna razı değil aslında.»* | `de, aslinda.` |
| 0.77 | *«eşim bilse zaten anlamaz.»* | *«eşim de bilse zaten anlamaz. Bilmiyorum,»* | `de, bilmiyorum,` |
| 0.77 | *«hak etmiyorum bu cümleyi.»* | *«bir yandan 'hak etmiyorum bu cümleyi'»* | `bir, yandan, 'hak, cümleyi'` |
| 0.74 | *«niye hep yalnızım»* | *«'niye ben hep yalnızım' vardı»* | `'niye, ben, yalnizim', vardi` |
| 0.73 | *«ben de katılıyorum»* | *«ben de aslında buna katılıyorum»* | `aslinda, buna` |
| 0.71 | *«Hak ettim galiba»* | *«kadeh. Hak ettim bunu galiba.»* | `kadeh., bunu, galiba.` |
| 0.60 | *«nasıl uzak dururum»* | *«Bu fikirden nasıl uzak durabilirim?»* | `bu, fikirden, durabilirim?` |
| 0.53 | *«Babam da idare etti»* | *«etti. Ben de idare ederim.»* | `etti., ben, de, ederim.` |

⭐⭐ **6 bulguda düşen şey Türkçenin «de/da» edatı.**

➡️⭐⭐⭐ *Bu bir «yanlış alıntı» değil, bir ÜSLUP: alıntı kısaltılırken cümlenin
vurgusunu taşıyan öge atılıyor. «içim DE bir tuhaf» ile «içim bir tuhaf» aynı şeyi
söylemez — «de» başka bir şeyin daha olduğunu ima eder ve alıntıdan silinince
kullanıcının söylediğinden BAŞKA bir cümle tırnak içine alınmış olur.*

## ⛔⛔ Biri daha ağır — yan cümle elenmiş

*«icra dosyasına bir nefes olur, kimsenin haberi olmaz»* — kullanıcı
*«…bir nefes olur, **eşim duymaz**, kimsenin haberi…»* yazmış ⇒ alıntı ortadaki
yan cümleyi atıp iki ucu **bitiştiriyor**. Bu T104'ün özgün kırpma kusurudur ve
öteki on beşten farklı bir sınıftır.

## ⛔ Bu okumanın söylemedikleri

| | |
|---|---|
| ⛔ **Hiçbiri düzeltilmedi** | `datasets/` IMMUTABLE ⇒ 16 kayıt bir sonraki derlemenin kalemi. Düzeltme ölçütü verilebilir: düzeltmeden sonra kapı o kayıtlar için **0** demeli |
| ⛔ **Benzerlik bir SINIF değil** | `difflib` oranı bir sezgidir; hangi düşmenin anlamı değiştirdiğine **elle okuma** karar verdi |
| ⛔ **Anma çerçevesi listesi kapanmıyor** | üç biçim daha eklendi ve her biri ancak elle okumayla görüldü ⇒ kapı bu sınıfta hep bir adım geride |
| ⚠️ Kullanıcının «en yakın parçası» pencere kaydırarak bulundu | yanlış hizalama olabilir; oran düşükse tablo yanıltır |
