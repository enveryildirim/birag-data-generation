# Tasarım önerileri — 2026-09-22 ölçümlerinden

> **Ne bu belge:** döngünün beşinci adımı (*tasarımı iyileştir*). Bugün
> üret→yargıla→derle→ince ayar→**ölç** zinciri ilk kez baştan sona döndü;
> bu belge ölçümlerin **üretim tasarımına** ne dediğini toplar.
>
> ⛔⛔ **Hiçbiri uygulanmadı.** Her madde bir **öneridir** ve kararı
> yürütücünündür. Her önerinin başında **hangi ölçüme dayandığı** yazılıdır;
> dayanağı olmayan öneri bu belgeye girmez.
>
> ⚠️ *«Bu benim önerim»* ile *«ölçüldü»* ayrımı her maddede korunur (Kural 6).

---

## ⭐ Ö1 — §7a'ya beşinci bağlam sınıfı: `celiskili`

**Dayanak:** T259 (kapsama matrisi) · T254 (ölçülebilir tek kazanç).

`context_fidelity`, ince ayarın **ölçülebilir kazanç verdiği tek eksen**
(`.real` üzerinde **+1,33**, okunabilir). Kapsama matrisi o eksenin dört
kategorisinden **üçünün** korpusta karşılığı olduğunu, **birinin
olmadığını** buldu:

| eval kategorisi | korpustaki karşılığı | kayıt |
|---|---|---:|
| `yeteri` | `baglam_davranisi = cevap_var` | 89 |
| `yetersiz` | `cevap_yok` | 59 |
| `distractor` | `ilgisiz` | 40 |
| ⛔ **`celiskili`** | **yok** | **0** |

⭐⭐ **Ve bu boşluk korpusun en büyük sorununa değiyor.** Eval ögesinin kendi
notu: *«Model birini seçip diğerini yok sayarsa çelişkiyi gizlemiş olur;
**ikisini birleştirmeye çalışırsa uydurur**.»* ⇒ Çelişkiyi adlandırmayı
öğretmek aynı zamanda **uydurma karşıtı** bir eğitimdir (uydurma %12, T238).

### Önerilen tanım — *bu benim önerim*

```
soruldu + iki pasaj AYNI KONUDA FARKLI şey söylüyor  → çelişkiyi ADLANDIR,
                                                        birini seçme, birleştirme
```

| alan | değer |
|---|---|
| `baglam_davranisi` | `celiskili` (§1b sözlüğüne eklenir) |
| doğru davranış | çelişkinin **varlığını** söyler · **hangi ikisi** olduğunu gösterir · **birini doğru ilan etmez** · **birleştirmez** |
| ⛔ yasak | sessizce birini seçmek · ortalama/uzlaştırma uydurmak · *«muhtemelen şu doğrudur»* |
| kapı | cevap, çelişkiye işaret eden bir ifade taşımalı **ve** iki pasajın **ikisine de** atıf yapmalı |

⚠️ **Kota açık soru.** Mevcut dağılım `cevap_var` %50 · `cevap_yok` %25 ·
`izin_iste` %12 · `ilgisiz` %12. Beşinci sınıf eklenince bunlar **yeniden
bölüşülmeli** ve hangisinden alınacağı bir **tasarım kararıdır**. Öneri:
`celiskili` ~%10, `cevap_var`dan alınarak (%50 → %40) — çünkü `cevap_var`
zaten en kalabalık ve T254'ün kazancı ondan da geliyor olabilir, azaltmanın
etkisi ölçülmeli.

⛔ **Bu öneri içerik yazmıyor.** Çelişkili pasaj çiftleri §7b'nin sentetik
pasaj kurallarına uymak zorunda (kaynak adı kategori, küçük harf, gerçek
belge taklidi yasak).

---

## ⚠️ Ö2 — kısa girdide uydurma: korpus şu an yanlış şeyi öğretiyor

**Dayanak:** T261 (6,4 kat fark) · K42 (kısa girdi **bilerek** var).

| girdi | uydurma |
|---|---:|
| kısa (≤8 sözcük) | %6,5 |
| orta (≤26) | %8,2 |
| **uzun (>26)** | **%1,1** |

⛔⛔ **Gerilim tasarımın içinde:** K42 kısa ve noktalamasız girdiyi
**gerçekçilik** gereği koyuyor (gerçek kullanıcı kısa yazar). Ama korpus şu
an kısa girdide **uydurmayı** öğretiyor.

⇒ Çözüm *«kısa girdiyi azalt»* **değildir** — o gerçekçiliği bozar. Çözüm
**kısa girdide doğru davranışı öğretmektir**: az bilgi varken **az söylemek**,
boşluğu doldurmamak.

### Öneri — *bu benim önerim, ölçülmedi*

Kısa girdili kayıtlar için ek bir üretim kuralı: *cevap, kullanıcının
söylediği **somut öğe sayısını aşamaz**.* Kullanıcı bir şey söylediyse cevap
iki şeye atıfta bulunamaz.

⛔⛔ **Ama T261'in kendi şerhi burada da geçerli:** ölçülen fark, uydurmanın
azalması kadar **sondanın kolaylaşması** da olabilir (uzun metinde ayrıntı
rastlantısal olarak daha kolay bulunur). ⇒ Bu öneri, **ayırıcı ölçüm
koşulmadan** uygulanmamalıdır: aynı cevaplar, kullanıcı metni kısaltılmış
kopyayla yeniden puanlanır.

---

## ⚠️ Ö3 — alan dışı sinyal: karar ürün kararıdır, mekanizma ölçüldü

**Dayanak:** T256 · T257 · T253.

**Ölçülen:** dar dağılımlı korpus genel yeteneği bozuyor; kayıp sinyalinin
**%5'i** kadar alan dışı içerik bunu **tamamen** geri alıyor
(`forgetting_smoke` 26,75 → **28,00** = taban) ve terapötik güvenlik ekseni de
düzeliyor (8,75 → 12,33). **LoRA kapsamı bu etkiyi üretmiyor** (modül 8→48,
r = −0,28).

⛔⛔ **Ama `v0.0.20`'nin %25,9'u alan dışıdır** ve terapötik kalite
**ölçülmedi** (eklenen kayıtlar judge'a girmiyor). ⇒ *«Korpusa aritmetik
ekleyelim»* **sonucu çıkmaz**.

### Karar için gereken üç şey — *öneri*

1. **Ne ekleneceği** bir ürün kararıdır: aritmetik bir **vekildi**, amaç
   dağılımı genişletmekti. Alan dışı ama **zararsız** başka içerik de olabilir.
2. **Sinyal payı ölçülerek** seçilmeli, kayıt sayısıyla değil (T256: %3,7
   kayıt = %0,034 gradyan).
3. Eklendikten sonra **terapötik eksenler yeniden ölçülmeli** — bu kez
   judge'la, çünkü `otomatik_gecti` kalite ölçmez (K57).

---

## ⛔ Ö4 — değiştirilmemesi gereken: korpus BÜYÜKLÜĞÜ

**Dayanak:** T246 · T248.

Korpusu **571 → 1033**'e çıkarmak (%81 artış) dereceli puanda **ölçülebilir
kazanç vermedi** — ve sebebi ölçüm gücü değil **yapısaldı**: o eksen kriz
yönlendirmesi ölçüyor, korpusta `is_crisis` kaydı **0**.

➡️ **Sıradaki iş veri ÜRETMEK değildir.** Üretim, ancak yukarıdaki
boşluklardan biri (Ö1 gibi) kapatılacaksa anlamlıdır — *«daha çok aynı
şeyden»* değil.

---

## Öncelik — *öneri*

| # | öneri | maliyet | dayanağı ne kadar sağlam |
|---|---|---|---|
| 1 | **Ö1** `celiskili` sınıfı | orta (yeni pasaj çiftleri) | ⭐ sağlam — ölçülen boşluk, ölçülen kazanç ekseninde |
| 2 | **Ö2**'nin ayırıcı ölçümü | düşük (yeniden puanlama) | ⭐ önce bu, öneri sonra |
| 3 | **Ö3** alan dışı sinyal | yüksek (ürün kararı) | ⭐ mekanizma sağlam, **içerik kararı açık** |
| — | **Ö4** üretimi durdurmak | sıfır | ⭐ sağlam |

⛔ Hepsinin önünde üç engel duruyor ve **hiçbiri tasarımla çözülmez**:
ikinci uzman (κ yok) · bağımsız judge erişimi · kriz diliminin uzman onayı.
