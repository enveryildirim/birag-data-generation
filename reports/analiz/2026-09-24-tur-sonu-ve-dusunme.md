# Tur sonu ve düşünme — «hep soru» ve «dar düşünme» ölçüldü

**Betik:** `scripts/analiz/2026-09-24-tur-sonu-ve-dusunme.py` · **Tarih:** 2026-09-24  
**Girdi:** `datasets/v0.1.0/train.jsonl` SHA256-16 `6fcb6b1e16290575` (1058 kayıt; son asistan turu = eğitim hedefi, `mask_prompt`) · kayıtlı eksen koşuları: taban tek koşu, `d1` (v0.0.18) / `e3` (v0.1.0) 8 tohum, `forget` hariç 5 eksen. **Yeni koşu yok.** Tohumlu değerler ort ± 2·SE.

## 1. Veri tur sonunu nasıl öğretiyor

### 1a. Beyan ve metin

| beyan (`gen_meta.turn_ending`) | kayıt | metni `?` ile biten |
|---|---:|---:|
| `acik_uclu_soru` | 525 (49.6%) | 523 |
| `takdir` | 160 (15.1%) | 0 |
| `ozet` | 151 (14.3%) | 0 |
| `yalnizca_yansitma` | 150 (14.2%) | 0 |
| `durur` | 54 (5.1%) | 0 |
| `None` | 18 (1.7%) | 1 |

Son tur soruyla biten: **524/1058 (50%)**.

### 1b. Bitiş bağlama göre değişiyor mu — `konusma_durumu` × `turn_ending` (satır %)

| bağlam | kayıt | `acik_uclu_soru` | `takdir` | `ozet` | `yalnizca_yansitma` | `durur` | en sık |
|---|---:|---:|---:|---:|---:|---:|---|
| `tetikleyici_an` | 359 | 50 | 13 | 16 | 17 | 4 | `acik_uclu_soru` |
| `suregiden_durum` | 219 | 52 | 13 | 14 | 16 | 5 | `acik_uclu_soru` |
| `iyi_giden_paylasim` | 155 | 42 | 28 | 15 | 9 | 6 | `acik_uclu_soru` |
| `plan_yapma` | 154 | 56 | 12 | 14 | 11 | 7 | `acik_uclu_soru` |
| `merak_sorusu` | 102 | 52 | 17 | 10 | 18 | 4 | `acik_uclu_soru` |
| `aradan_donus` | 51 | 55 | 14 | 16 | 8 | 8 | `acik_uclu_soru` |

En sık bitişin `acik_uclu_soru` olduğu bağlam: **6 / 6**.

### 1c. Çok turlu kayıtlar — geçmiş, son turun bitişini belirliyor mu

| son turdan hemen önceki ardışık soru-sonu | kayıt | son tur soruyla biten |
|---:|---:|---:|
| 0 | 198 | 102/198 (52%) |
| 1 | 188 | 100/188 (53%) |
| 2 | 17 | 6/17 (35%) |
| 3 | 2 | 2/2 (100%) |

## 2. Model ne yapıyor — tek turlu eval ögeleri

### 2a. Soruyla biten cevap (%, dolu cevaplar)

| eksen | taban | `d1` | `e3` |
|---|---:|---:|---:|
| `safety` | 80.0 | 72.8 ± 8.0 | 69.6 ± 6.2 |
| `context_fidelity` | 90.0 | 69.3 ± 5.3 | 71.9 ± 8.2 |
| `sycophancy` | 100.0 | 85.0 ± 5.6 | 86.2 ± 2.5 |
| `cfreal` | 93.3 | 84.5 ± 4.2 | 80.2 ± 5.9 |
| `cfo` | 80.0 | 56.6 ± 7.7 | 58.0 ± 9.5 |
| **hepsi** | 89.4 | 74.5 ± 2.7 | 74.1 ± 1.8 |

### 2b. Cevabın şekli

| | ortanca sözcük | ortanca cümle | soru cümlesi payı (ort.) |
|---|---:|---:|---:|
| veri (son tur) | 48 | 5 | 11% |
| `taban` | 22 | 3 | 39% |
| `d1` | 19 | 2 | 35% |
| `e3` | 18 | 2 | 34% |

## 3. Düşünme tur sonunu belirliyor mu

Düşünmede «sormuyorum» geçen ve geçmeyen dolu cevapların soruyla bitme payı.

| | «sormuyorum» geçen düşünme | bunların soruyla biten cevabı | geçmeyenlerin soruyla biten cevabı | fark (puan) | okuma |
|---|---:|---:|---:|---:|---|
| veri | 318/1040 (31%) | 27/318 (8%) | 496/722 (69%) | -60 | tek küme |
| `d1` | 340/691 (49%) | 256/340 (75%) | 259/351 (74%) | 2 ± 8 | sıfırdan ayırt edilemiyor |
| `e3` | 364/709 (51%) | 267/364 (73%) | 258/345 (75%) | -1 ± 7 | sıfırdan ayırt edilemiyor |

Taban satırı yok: taban İngilizce düşünüyor, «sormuyorum» hiç geçmiyor.

## 4. Düşünmenin içeriği

### 4a. Uzunluk ve biçim (% düşünme)

| | veri | taban | `d1` | `e3` |
|---|---:|---:|---:|---:|
| ortanca sözcük | 72 | 312 | 102 | 97 |
| madde / başlık biçimi (`**`, madde imi, numara) | 0 | 100 | 55 | 57 |
| sistem kuralını anıyor (*tek seferde* · *kural* · *protokol*) | 3 | 0 | 33 | 32 |
| «sormuyorum» | 31 | 0 | 47 | 51 |
| ⛔ / ⭐ işareti | 23 | 0 | 17 | 12 |

### 4b. Veride olumsuz karar cümleleri

* Olumsuz birinci tekil fiil (*-mıyorum*, *-mayacağım*) içeren düşünme cümlesi: **2769/7225 (38%)**
* Kayıt başına ortanca: **3** · hiç olmayan kayıt: 26/1040 (2%)
* Korpusta **≥ 5 kayıtta** birebir geçen düşünme cümlesi (≥ 3 sözcük, noktalamasız): **9**

| cümle | kayıt |
|---|---:|
| *Soru sormuyorum, özetlemiyorum.* | 11 |
| *⛔ Miktara hüküm vermiyorum.* | 10 |
| *Soru sormuyorum, topluyorum.* | 6 |
| *Kararı ona bırakıyorum.* | 5 |
| *Soru sormuyorum, duruyorum.* | 5 |
| *⛔ Eşine söylemesini önermiyorum.* | 5 |
| *⛔ Sorduğu şey metinde yok; uydurmuyorum.* | 5 |
| *⛔ Rakamı ANMIYORUM; mesajdan çıkarıldı.* | 5 |
| *İlaç adını anmıyorum.* | 5 |

### 4c. Modelin döngüleri neyin etrafında dönüyor

| kol | döngülü düşünme (T279 tanımı) | en çok tekrarlanan cümlesinde «soru» geçen |
|---|---:|---:|
| `d1` | 142/752 (19%) | 44/142 (31%) |
| `e3` | 115/752 (15%) | 43/115 (37%) |

## ⛔ Bunun söylemedikleri

| | |
|---|---|
| ⛔ **Anahtar sözcük vekildir** | «sormuyorum» karşıtlık cümlesinde de geçer (veride bu kayıtların 27'i yine soruyla bitiyor); olumsuz fiil deseni yalnız iki kip yakalar; *kural* başka anlamda da geçebilir |
| ⛔ **Nedeni ölçülmedi** | §3 bağın koptuğunu gösterir; neden koptuğunu (bağdaştırıcı kapasitesi, taban eğilimi, açgözlü çözme) ayırmaz |
| ⚠️ **Eval ögeleri eğitim konuşması değil** | tek turlu, ögenin kendi istemi, 1024 jeton; demo çok turlu ve kanonik system prompt ⇒ demodaki «her cevap soru» izlenimi **çok turda ölçülmedi** |
| ⚠️ **Bitiş = son karakter** | soru ortada, son cümle yansıtmaysa soru sayılmaz |
| ⚠️ **Taban tek koşu ve İngilizce düşünüyor** | yüzdeleri dağılım değil; Türkçe vekil satırlarında taban karşılaştırılamaz |
