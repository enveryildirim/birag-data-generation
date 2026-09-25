# `forgetting_smoke.jsonl` — Eksen 3 duman seti

**Çıktı:** `evals/forgetting_smoke.jsonl` · SHA256 `94b9b5fb31cd60d430db40f4f95aac882febb1937614f6c6cf9bf58ed7cb57ef`  
**Betik:** `scripts/analiz/2026-09-15-forgetting-smoke.py` · **Tarih:** 2026-09-15  
**Öğe:** 30 · **Kapı:** 30/30

---

## 0. Bu set ne ölçer, ne ölçmez

**Ölçer:** eğitim sonrası genel yeteneğin ÇÖKÜP çökmediği (§9).

**Ölçmez:** yetenek tavanı. Öğeler bilerek kolay — baz model zaten geçmeli ki
düşüş görünsün. Zor öğelerden kurulu bir set, baz modelin de düştüğü yerde
LoRA'nın etkisini gizler.

⚠️ **Bu bir kapı değil, bir alarm.** Kaç öğe düşerse durdurucu olduğu Faz 4'te
baseline ölçüldükten sonra konur; şimdi eşik koymak uydurma olur.

## 1. System prompt neden YOK

K19 promptu konsaydı bu öğelerin çoğunda doğru davranış **reddetmek** olurdu
(`golden.dev`'in `kapsam_disi` dilimi tam onu ölçüyor) ve set persona uyumunu
ölçmeye başlardı. Eksen 3'ün sorusu ağırlıklarla ilgili: *genel yetenek duruyor mu*.
Replay diliminin boş-system varyantıyla aynı gerekçe (K88/K89).

## 2. Neden burada VARLIK iddiası meşru

`golden_checks.py` otomatik iddiaların yalnızca **yokluk** iddia edebileceğini
söylüyor ve Eksen 1 için haklı: Türkçe serbest terapötik metinde "şu davranış
olsun" demek yanlış negatif üretir, çünkü davranışın sonsuz çok yazılışı var.

Eksen 3'te cevap uzayı **kapalı**: *"17×3"* tek cevaplı. Sınır açık yazılı
(`src/smoke_checks.py`): bir iddia ancak cevabın doğruluğu metinden **mekanik**
doğrulanabiliyorsa buraya yazılır. *"Özet iyi mi"* yazılamaz; *"özet şu özel adı
içeriyor mu"* yazılabilir.

## 3. Kategoriler

| Kategori | Öğe |
|---|---:|
| `talimat` | 5 |
| `genel_kultur` | 5 |
| `kod` | 4 |
| `ceviri` | 4 |
| `matematik` | 3 |
| `mantik` | 3 |
| `ozet` | 3 |
| `ingilizce` | 3 |

## 4. İddia kuralları

| Kural | Kullanım |
|---|---:|
| `herhangi_biri` | 17 |
| `uzunluk_maks` | 10 |
| `sayi` | 8 |
| `icerir` | 7 |
| `dil` | 6 |
| `icermez` | 3 |
| `madde_sayisi` | 3 |

Öğe başına ortalama **1.8** iddia. Hepsi deterministik — **bu sette judge yok**, dolayısıyla K103'ün ölçtüğü
oynaklık bu ekseni hiç etkilemiyor.

## 5. Öğeler

| # | Kategori | Sonda |
|---|---|---|
| `fs-001` | matematik | Tek adımlı çarpma — en temel aritmetik duruyor mu |
| `fs-002` | matematik | İki adımlı işlem — ara sonucu tutabiliyor mu |
| `fs-003` | matematik | Yüzde hesabı — günlük hayatta en sık kullanılan işlem |
| `fs-004` | mantik | Basit çıkarım — öncüllerden sonuç |
| `fs-005` | mantik | Sıralama — göreli ifadelerden düzen kurma |
| `fs-006` | mantik | Tuzak soru — modelin kabul etmeden düzeltmesi |
| `fs-007` | kod | Python temel sözdizimi — fonksiyon yazımı |
| `fs-008` | kod | Liste işlemi — döngü ya da comprehension |
| `fs-009` | kod | Hata okuma — mesajdan nedene |
| `fs-010` | kod | SQL — temel sorgu |
| `fs-011` | ozet | Kısa metinden özel adları koruyarak özet |
| `fs-012` | ozet | Uzunluk talimatına uyarak özet |
| `fs-013` | ozet | Bilgi çıkarma — metinde geçen sayı |
| `fs-014` | ceviri | Türkçe → İngilizce, basit cümle |
| `fs-015` | ceviri | İngilizce → Türkçe, basit cümle |
| `fs-016` | ceviri | Deyim çevirisi — birebir çeviri tuzağı |
| `fs-017` | ceviri | Teknik terim — alan dışı kelime dağarcığı |
| `fs-018` | ingilizce | İngilizce soruya İngilizce yanıt |
| `fs-019` | ingilizce | İngilizce talimat takibi — biçim + dil |
| `fs-020` | ingilizce | İngilizce akıl yürütme |
| `fs-021` | talimat | Sayılı liste — tam sayı |
| `fs-022` | talimat | Uzunluk sınırı |
| `fs-023` | talimat | Olumsuz talimat — bir şeyi YAPMAMA |
| `fs-024` | talimat | Biçim talimatı — JSON |
| `fs-025` | talimat | Çok adımlı talimat |
| `fs-026` | genel_kultur | Coğrafya — temel olgu |
| `fs-027` | genel_kultur | Bilim — temel olgu |
| `fs-028` | genel_kultur | Tarih — tarih bilgisi |
| `fs-029` | genel_kultur | Edebiyat — eser–yazar eşleşmesi |
| `fs-030` | genel_kultur | Birim dönüşümü |

## 6. Öz-sınama — iddialar doğru cevabı reddediyor mu

Bir eval öğesinin en tehlikeli kusuru **fazla katı iddia**dır: model doğru
davranır, alet "başarısız" der, veri o yöne revize edilir (K40, K65).

Bu yüzden her öğe için elle bir **doğru cevap örneği** yazıldı ve betik her
koştuğunda bunların tüm iddialardan geçtiğini doğruluyor. Geçmezse betik durur.

İlk yazımda sınama **5 yanlış negatif** buldu — hepsi `dil` iddiasıydı ve dil
sezimi kısa cümlelerde (*"It arrives at 17:00."*) çöküyordu. İki düzeltme:
Türkçeye özgü harf sinyali eklendi ve işlev sözcüğü listeleri genişletildi.
Beşincisi (`fs-019`, üç renk adı) gerçekten belirsizdi — orada `dil` iddiası
**yokluk** iddiasıyla değiştirildi.

### 6a. Negatif sınama — iddia gerçekten bir şey talep ediyor mu

Ters kusur da ölçülüyor: bir öğe **boş** olabilir, yani iddiaları hiçbir şey
talep etmeyebilir. Betik her öğeye kaçamak cevaplar veriyor (*"Bilmiyorum."*,
*"I don't know."*, *"Bu konuda yardımcı olamam."*, boş dize) ve hepsinin
elenmesini bekliyor.

İlk yazımda **`fs-023` boştu**: tek iddiası `icermez=[İstanbul]` olduğu için
*"Bilmiyorum."* de geçiyordu. Yokluk iddiası tek başına asla yeterli değil —
yanına içerik talep eden bir iddia gerekiyor.

## 7. Bilinen sınırlar

- **Dil sezimi frekans temelli.** Çok kısa cevaplarda (`belirsiz`) yanılabilir;
  bu yüzden `dil` iddiası hep başka bir iddiayla birlikte kullanıldı.
- **Özet kalitesi ölçülmüyor**, yalnızca ana özel adın korunması. Kalite
  ölçümü judge gerektirir ve bu setin amacı dışında.
- **Kod çalıştırılmıyor**, deyim içeriyor mu diye bakılıyor. Çalıştırmak
  sandbox gerektirir; duman seti için maliyet/fayda tutmuyor.

