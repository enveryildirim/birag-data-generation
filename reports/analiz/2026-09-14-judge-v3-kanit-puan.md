# Judge v3 — kanıt → puan müdahalesi ölçüldü

**Betik:** `scripts/analiz/2026-09-14-judge-v3-kanit-puan.py` · **Tarih:** 2026-09-14  
**v1:** `data/judged/expert-70.jsonl` · SHA256 `c5e179ee0992ca64622078907f6e83f51378f3ca7fddffb81235bddd82ce82d4`  
**v2:** `data/judged/expert-70.v2.jsonl` · SHA256 `8988a94e7be238c4a71a538638601fd3b41c821dd5e8f5a9355d0efad409850a`  
**v3:** `data/judged/expert-70.v3.jsonl` · SHA256 `1973c8398ccdebe684929d3ae757a1e74e54c4523b3edeeb8f22092846379602`  
**Uzman:** `data/expert_sample/uzman-puanlari.json` · SHA256 `d9d36c10691157a90173da8452ceffc47c3d88782b91bd7a8e4ecf11e492263c`  
**Üç sürümde de puanlanan ve uzmanın değerlendirdiği kayıt:** 48

> **Hipotez:** v2'de judge kusuru görüyor ama saymıyordu. `anlasilirlik` puanı LLM'den alınıp beş ikili cevaptan **kod** hesaplarsa ayrım gücü artar.

> **Kontrol aynı çağrının içinde:** v3 hem hesaplanan puanı hem judge'ın kendi `anlasilirlik_holistik`'ini üretti. İkisi aynı modelin aynı okumasından geliyor; fark **yalnızca puanlama mekanizması**.

> ⚠️ **Kalibrasyon testi, genelleme testi değil — v2 ile aynı sınır.** Beş kusur türü (`kurulmamis_mecaz`, `belirsiz_gonderge`, …) bu uzmanın reddettiği cümlelerden çıkarıldı (`uretim-v3.md` §5d) ve test aynı korpusta yapılıyor. Uzmanın reddettiği 5 gerçek cümle prompt'a konulmadı, ama kusur taksonomisi onlardan türedi. Sonuç en fazla şunu söyler: **mekanizma değişikliği bu korpusta fark yaratıyor mu.** Yeni korpusta genellenip genellenmediği ikinci bir uzman turu gerektirir.

> ⚠️ **v3-holistik kontrolü de kusursuz değil:** judge, holistik puanı verirken beş ikili soruyu **zaten cevaplamış** oluyor (aynı çağrı, A3 → A4 sırası). Yani holistik puan bağımsız bir kontrol değil, *bayrakları gördükten sonraki* kanaat. Fark çıkarsa mekanizmaya atfedilebilir; **çıkmazsa** bunun bir kısmı bulaşma olabilir.

---

## 1. Bayraklar ateşledi mi

Müdahalenin ön koşulu: ikili sorular gerçekten `true` dönebilmeli. Hiç ateşlemiyorlarsa puan da hep 5 çıkar ve mekanizma değişmemiş olur.

| Bayrak | `true` | Oran |
|---|---:|---:|
| `kurulmamis_mecaz` | 20/68 | %29 |
| `belirsiz_gonderge` | 21/68 | %31 |
| `ust_uste_yan_cumle` | 18/68 | %26 |
| `devrik_eksiltili` | 4/68 | %6 |
| `soyut_adlastirma` | 2/68 | %3 |

**Kayıt başına kusur sayısı:** `{0: 25, 1: 26, 2: 13, 3: 3, 4: 1}`  
**`duz_turkce` = ÇEVİREMEDİM:** 0/68

## 2. Dil boyutunun dağılımı — dört yöntem

| Yöntem | n | Ort. | s | Dağılım | Tam puan |
|---|---:|---:|---:|---|---:|
| v1 · `dil_butunlugu` | 70 | 5.00 | 0.00 | `{5: 70}` | %100 |
| v2 · `anlasilirlik` | 68 | 4.26 | 0.44 | `{4: 50, 5: 18}` | %26 |
| v3 · `anlasilirlik` | 68 | 4.04 | 0.93 | `{1: 1, 2: 3, 3: 13, 4: 26, 5: 25}` | %37 |
| v3-holistik · `anlasilirlik_holistik` | 68 | 4.07 | 0.58 | `{3: 9, 4: 45, 5: 14}` | %21 |

## 3. Ayrım gücü

Mann-Whitney uyum oranı: rastgele bir (kötü, iyi) çiftinde judge'ın **kötüye daha düşük** puan verme olasılığı. **0.50 = tesadüf.** İki hedef var — ikincisi doğrudan dil boyutunu sınadığı için bu rubrik açısından daha yerinde.

### Uzmanın genel kararı — `ret` vs `kabul`  ·  n = 5 / 32

| Yöntem | kötü ort. | iyi ort. | uyum oranı | %95 aralık |
|---|---:|---:|---:|:---:|
| v1 · `dil_butunlugu` | 5.00 | 5.00 | 0.50 ❌ | 0.22 – 0.78 |
| v2 · `anlasilirlik` | 4.20 | 4.25 | 0.53 ❌ | 0.25 – 0.80 |
| v3 · `anlasilirlik` | 2.80 | 4.22 | 0.87 ✅ | 0.66 – 1.00 |
| v3-holistik · `anlasilirlik_holistik` | 3.40 | 4.22 | 0.82 ✅ | 0.58 – 1.00 |

### Uzmanın dil puanı — dil ≤ 2 vs dil = 5  ·  n = 5 / 37

| Yöntem | kötü ort. | iyi ort. | uyum oranı | %95 aralık |
|---|---:|---:|---:|:---:|
| v1 · `dil_butunlugu` | 5.00 | 5.00 | 0.50 ❌ | 0.23 – 0.77 |
| v2 · `anlasilirlik` | 4.20 | 4.24 | 0.52 ❌ | 0.25 – 0.80 |
| v3 · `anlasilirlik` | 2.60 | 4.11 | 0.82 ✅ | 0.59 – 1.00 |
| v3-holistik · `anlasilirlik_holistik` | 3.40 | 4.14 | 0.79 ✅ | 0.54 – 1.00 |

> ✅ ≥ 0.75 · ⚠️ ≥ 0.60 · ❌ < 0.60 — **bizim konvansiyonumuz** (Kural 6).

## 4. Karar cümleleri — v2'nin bulup da cezalandırmadığı üç cümle

v2 raporu §6: judge bu üç cümleyi uzmanla **aynı** seçmişti; uzman 2/1/2 verdi, v2 üçüne de 4 verdi. v3 aynı cümlelerde ne yaptı?

| Form | Uzmanın dil puanı | v2 | v3 hesaplanan | v3 holistik | Ateşleyen bayraklar | v3'ün seçtiği cümle |
|---|---:|---:|---:|---:|---|---|
| 25 | 2 | 4 | **4** | 4 | ust_uste_yan_cumle | Uykuya ihtiyacın olduğunu biliyorsun ve yine de duramıyorsun |
| 27 | 1 | 4 | **2** | 3 | belirsiz_gonderge, devrik_eksiltili, soyut_adlastirma | O söylenene dair elimdekini paylaşmamı ister misin? |
| 33 | 2 | 4 | **1** | 3 | kurulmamis_mecaz, belirsiz_gonderge, ust_uste_yan_cumle, soyut_adlastirma | Kendin fark etmişsin: ölçüyü dışarıya bırakmışsın ve o ölçü  |

## 5. Kanıt adımı kararlı mı

v2 ve v3 aynı kayıtta **aynı cümleyi** seçti: **41/48**. Kanıt adımı iki farklı rubrik altında aynı yere işaret ediyorsa, ölçtüğü şey rubriğin değil metnin özelliğidir.

## 6. Uzmanın dil puanıyla korelasyon

| Yöntem | n | r |
|---|---:|---:|
| v1 · `dil_butunlugu` | 44 | — |
| v2 · `anlasilirlik` | 44 | +0.00 |
| v3 · `anlasilirlik` | 44 | +0.42 |
| v3-holistik · `anlasilirlik_holistik` | 44 | +0.30 |

## 7. Kazanç nereden geldi — ayrıştırma mı, aritmetik mi

Üç kol, tek değişkenli fark:

| Kol | Beş ikili soru | Puanı kim verdi |
|---|---|---|
| `v2` | ❌ yok | LLM |
| `v3-holistik` | ✅ var (aynı çağrıda cevaplandı) | LLM |
| `v3` | ✅ var | **kod** |

| Hedef | v2 | v3-holistik | v3 | ayrıştırmanın katkısı | aritmetiğin katkısı |
|---|---:|---:|---:|---:|---:|
| `ret` vs `kabul` | 0.53 | 0.82 | 0.87 | **+0.29** | +0.05 |
| dil ≤ 2 vs dil = 5 | 0.52 | 0.79 | 0.82 | **+0.26** | +0.04 |

**Kazancın büyük kısmı ayrıştırmadan geliyor, aritmetikten değil.** Beş somut soruyu sormak, judge'ın okumasını değiştirdi; puanı ondan almak bunun üstüne küçük bir katkı koydu. Yani hipotezimin *yönü* doğruydu ama *mekanizması* farklı: sorun LLM'in puan vermesi değil, ondan **soyut bir yargı** istenmesiydi.

⚠️ `v3-holistik` kolu bağımsız bir kontrol değil: judge o puanı verirken beş soruyu zaten cevaplamıştı. Bu yüzden ayrıştırmanın katkısı bu tabloda bir **üst sınır** olarak okunmalı — soruları sorup holistik puanı ayrı bir çağrıda istemek gerçek ayrımı verirdi; o koşu yapılmadı.

## 8. Sonuç

### Ne değişti

1. **İlk kez bir judge boyutu uzmanın kararını ayırıyor.** `ret` vs `kabul` uyum oranı v1'de 0.50, v2'de 0.53, **v3'te 0.87**; dil puanı hedefinde 0.50 → 0.52 → **0.82**. Her iki testte de %95 aralığın alt sınırı 0.50'nin üstünde.
2. **Uzmanla korelasyon** v2'de +0.00 iken v3'te **+0.42**.
3. **Karar cümlelerinin ikisi düzeldi:** form 27 (uzman 1 → v2 4 → **v3 2**), form 33 (uzman 2 → v2 4 → **v3 1**).

### Ne düzelmedi, ne bilmiyoruz

- **Form 25 düzelmedi** (uzman 2, v3 4). Sebep puanlama değil **kanıt seçimi**: v3 bu kayıtta uzmanın şikâyet ettiği *"O saat sana ne veriyor"* cümlesini değil başka bir cümleyi seçti. En zayıf cümleyi tek seçmek, cevabın tamamını ölçmüyor.
- **İki bayrak neredeyse hiç ateşlemiyor:** `devrik_eksiltili`, `soyut_adlastirma`. Mekanizma pratikte üç bayrakla çalışıyor; beşinin de gerekli olduğu gösterilmedi.
- **`duz_turkce = ÇEVİREMEDİM` hiç tetiklenmedi** (0/68). O emniyet kuralı bu korpusta hiçbir şey yapmadı; katkısı **ölçülmemiştir**, iddia edilemez.
- **n = 5.** Kötü grupta beş kayıt var; aralıklar geniş. Güçlü bir ayrım gösterilebiliyor ama büyüklüğü kesin değil.
- **Kalibrasyon, genelleme değil.** Kusur taksonomisi bu uzmanın şikâyetlerinden türedi ve test aynı korpusta yapıldı.

### Karar

`anlasilirlik` boyutu için **v3 mekanizması benimsenir**: tek soyut yargı yerine somut ikili sorular + kodla hesaplanan puan. Aynı desen diğer boyutlara (`dogallik`, `mi_uyumu`) da uygulanabilir — **denenmedi**. ⚠️ Judge çıktısının bütünü hâlâ kalite kanıtı değildir: yalnızca bir boyut ayrım kazandı, diğerleri v2'deki gibi. `uretim-v3.md` §9 güncellenmeli ama kaldırılmamalı.

