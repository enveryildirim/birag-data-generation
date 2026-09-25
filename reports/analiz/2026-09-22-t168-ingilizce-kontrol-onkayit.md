# T168 İngilizce kontrol deneyi — ÖN KAYIT (koşudan önce)

**Betik:** `scripts/analiz/2026-09-22-t168-kontrol-hazirlik.py` · **Tarih:** 2026-09-22  
**Ön kayıt:** `configs/deney/2026-09-22-t168-ingilizce-kontrol.yaml`  
**Öge kümesi:** `data/deney/2026-09-22-t168-ogeler.jsonl` SHA256 `af09a27e2c42be05` · **48 öge**

⛔ Bu belge **üretimden önce** yazıldı ve commit edildi. Ölçüt ve hüküm kuralları sonradan değiştirilmeyecek.

---

## 1. Tasarım — üç ihtimali ikiye indirmemek için 2×2

*«Türkçe'ye özgü»* ile *«ekleşik ögeye özgü»* **aynı şey değil** ve tek
dilli bir karşılaştırma ikisini ayıramaz. Bu yüzden 2×2:

| | `klitik_benzeri` | `serbest_belirtec` |
|---|---|---|
| **tr** | `de` / `da` (12) | `biraz` / `aslında` (12) |
| **en** | `too` / `also` (12) | `a bit` / `actually` (12) |

⭐ **Serbest belirteç hücresi bir iç kontroldür:** TR ve EN'de yapıca **eşleşiktir** (ikisi de serbest sözcük). Eğer düşme yalnız `tr_klitik`'te yüksekse olgu **dile** değil **ekleşikliğe** bağlıdır.

---

## 2. ⛔ Ayırt etme gücü — ÖNCEDEN hesaplandı

T245/T246'nın dersi: *bir eşiği ilan etmek onu doğru kılmaz.* Bu yüzden eşikle birlikte **görülebilirlik** de ilan ediliyor.

Fisher kesin testi, iki yönlü, α = 0,05, **n = 12/hücre**:

| Bir hücrede düşme | Ötekinde anlamlı olmak için gereken | p |
|---:|---:|---:|
| 0/12 | **5/12** | 0.0373 |
| 1/12 | **7/12** | 0.0272 |
| 2/12 | **8/12** | 0.0361 |
| 3/12 | **9/12** | 0.0391 |

➡️ ⛔⛔ **Bu tasarım ancak ÇOK BÜYÜK bir farkı görebilir.** Karşı hücre sıfırken bile anlamlılık için **5/12** düşme gerekiyor (%42). ⇒ **Null sonuç «fark yok» DEĞİL, «bu tasarımla gösterilemiyor» demektir.**

⚠️ Bu, deneyi koşmamak için bir gerekçe değil: T168 *«%100'e yakın bir üslup»* iddiası taşıyor (16/16 bulgu tek örüntü) ⇒ iddia doğruysa etki zaten bu büyüklükte olmalı. Değilse, iddia zaten zayıftır.

---

## 3. Hüküm kuralları (değiştirilemez)

| Gözlenen | Hüküm |
|---|---|
| `tr_klitik` ≫ `en_klitik` **ve** `tr_serbest` ≈ `en_serbest` | (b) **EKLEŞİKLİĞE** özgü |
| `tr`'nin **iki** hücresi de yüksek | (a) **DİLE** özgü — T168'in ucu ayakta |
| dört hücre de benzer ve **yüksek** | (c) **GENEL** işlev-sözcüğü düşmesi ⇒ T168'in «Türkçe'ye özgü» ucu **DÜŞER** |
| dört hücre de benzer ve **düşük** | ⛔ olgu bu kurulumda **yeniden üretilemedi** — T168'in kendisi sorgulanır |
| hiçbiri anlamlı değil | ⛔ **SONUÇSUZ** — yokluk kanıtı değil |

---

## 4. ⛔ Koşudan önce yazılan karıştırıcılar

| | |
|---|---|
| ⛔ **`de/da` klitik, `too` serbest** | iki klitik hücresi yapıca eşit DEĞİL — sorunun kendisi bu, ama *«dile özgü»* hükmü tek başına bu hücreden kurulamaz |
| ⛔ **Ögeleri ben yazdım** (K30) | çeviri denkliği benim okumam; ikinci okuyucu yok |
| ⛔ **Tek üretici ailesi** | Claude; Gemini/GPT koşulmadı (agy kotası dolu, OPENAI_API_KEY yok) |
| ⛔ **Blok üretimi** | 12 öge tek çağrıda ⇒ üretici kendi içinde tutarlılaşabilir; öge bağımsızlığı tam değil |
| ⚠️ **Körlük** | üreticiye edat/vurgu/düşme hiç söylenmiyor; görev yalnız «kullanıcının sözünü anarak destek cevabı yaz» |
| ⚠️ **Kriz yok** | ögeler günlük sıkıntı; kriz içeriği Kural 3 gereği dışarıda |
