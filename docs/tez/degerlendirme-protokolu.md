# Değerlendirme Protokolü — taban ↔ ince ayar

> **Amaç:** makalede/tezde *«ince ayar ne değiştirdi»* sorusunun hangi
> metriklerle, hangi istatistikle ve hangi şerhlerle cevaplanacağını
> **koşudan önce** sabitlemek.
>
> **Kural:** her metriğin yanında üç şey yazılı olmalı — **kaynağı**,
> **bugün hesaplanabilir mi**, ve **hangi şerhle raporlanır**. Şerhsiz sayı
> bu protokolde geçersizdir.
>
> ⚠️ *«Bu benim önerim»* işaretli satırlar ölçülmemiş tasarım kararlarıdır.

**Son güncelleme:** 2026-09-22

---

## 0. Neden bu belge var — dört ölçülmüş sebep

| | bulgu | sonucu |
|---|---|---|
| ⛔⛔ | **T247** — ölçüt kriz yönlendirmesini ölçüyor, korpusta `is_crisis` kaydı **0** | metrik seçilmeden **kapsama** denetlenmeli |
| ⛔⛔ | **T248** — eksen puanı davranışı, uzunluğu ve *cevap vermiş olmayı* birlikte ölçüyor (boş cevap tabanda 0/15, kollarda 3,2) | her puanın yanında **boş/uzunluk/kesilme** |
| ⛔⛔ | **T246** — 3 tohumda −4,67 görünen fark 8 tohumda −1,25'e düştü (%73'ü gürültü) | **çoklu tohum + güç analizi** zorunlu |
| ⛔⛔ | **judge-v7-uzman raporu** — 7 boyutun 5'i insan çapasına karşı **AUC ≈ 0,5** | boyut puanları kalite iddiası olarak **kullanılamaz** |

---

## 1. Üç ayak

Protokol üç bağımsız ayak üstünde durur. Hiçbiri tek başına yeterli değildir.

| ayak | ne söyler | durum |
|---|---|---|
| **A. Eşli kör tercih** | *«hangisi daha iyi»* | ⛔ kurulmadı |
| **B. Alan standardı sayımlar** (EPITOME + MI/OARS) | *«hangi davranış ne sıklıkta»* | ✅ mevcut yargılardan çıkar |
| **C. Judge doğrulama** | *«bu alet ne ölçüyor, nerede kör»* | ✅ büyük kısmı ölçülü |

---

## 2. Ayak A — eşli kör tercih (manşet metrik)

**Ne:** aynı girdiye taban ve ince ayarlı modelin cevapları yan yana; judge
hangisinin daha iyi olduğunu **hangisinin hangi model olduğunu bilmeden**
seçer. Raporlanan: **kazanma oranı · beraberlik · %95 GA**.

**Neden manşet:** mutlak puan ölçeğimiz tohumlar arasında **3–11** arası
zıplıyor (T246/T247). Eşli karşılaştırma aynı girdide iki çıktıyı kıyasladığı
için bu oynaklığın büyük kısmını düşürür.

**Kaynak:** MT-Bench / Chatbot Arena çizgisi (Zheng vd. 2023). ⚠️ Künye
doğrulanacak.

**Zorunlu kontroller:**

| | |
|---|---|
| ⛔ **Konum yanlılığı** | A/B sırası yarı yarıya çevrilir; ters sırada kararı değişen çiftler **tutarsız** sayılır ve ayrı raporlanır |
| ⛔ **Uzunluk yanlılığı** | kazanma oranı, uzunluk dilimine göre de kırılır (T248: kollar 20-31, taban 59 sözcük) |
| ⛔⛔ **Öz-yüceltme yanlılığı** | judge Claude **olamaz** — üreticiyle aynı aile, K45 +6/+11 öz-şişirme ölçtü |
| ⚠️ **Judge erişimi** | Gemini kotası kapalı (K45). Bu ayak **bir judge kaynağı açılmadan koşulamaz** — protokolün en sert kısıtı |

---

## 3. Ayak B — alan standardı sayımlar

### 3.1 EPITOME (empati) — ✅ zaten gömülü

`duygusal_tepki` · `yorumlama` · `kesif`, her biri 0/1/2.

**Kaynak:** Sharma vd. 2020, *A Computational Approach to Understanding
Empathy* — `docs/arastirma-notlari.md` §A, tam metin okunmuş.

⭐ **Özgün açı:** EPITOME İngilizce veri üzerine kurulu; buradaki **Türkçe
uyarlaması** tezin kendi katkısı.

⛔⛔ **Zorunlu şerh:** bu üç boyutun insan çapasına karşı AUC'si
**0,36–0,46** (kör). ⇒ *«empati iyileşti»* **yazılamaz**. Yazılabilecek olan:
*«EPITOME Türkçeye uyarlandı ve bu çapaya karşı ayırt etmedi»* — bu da bir
sonuçtur ve çürüyen iddia tezde değerlidir.

### 3.2 MI / OARS — ✅ zaten gömülü

**Kaynak:** SAMHSA TIP 35, Bölüm 3 — `docs/arastirma-notlari.md` §C.

| OARS | alan |
|---|---|
| **O**pen questions | soru sayımı · `turn_ending` |
| **A**ffirmations | `takdir_var` |
| **R**eflections | `yansitma_var` · `karmasik_yansitma` |
| **S**ummaries | `ozet_var` |
| MI-uyumsuz davranış | `tuzak_ihlali` (uzman · etiketleme · soru-cevap · erken odak · suçlama · erken tavsiye) |

### 3.3 MITI türevi oranlar — ✅ hesaplanabilir

Yansıtma/soru oranı · karmaşık yansıtma yüzdesi · MI-uyumlu ÷ MI-uyumsuz.

⚠️ **MITI bir İNSAN kodlama sistemidir** ve yayımlanmış eşikleri vardır.
Bizimki **MITI-esinli otomatik sayımlardır**; makalede böyle adlandırılmalı ve
MITI eşikleriyle doğrudan kıyaslanmamalı. ⚠️ Künye (Moyers vd.) doğrulanacak.

### 3.4 Çeşitlilik — ⭐ *bu benim önerim*, hesaplanabilir

distinct-1/2/3 · self-BLEU · tekrar oranı.

**Neden:** projede **ölçülmüş** bir şablonlaşma sorunu var — K193 korpusun
ikinci büyük kalıbını 43 kayıtta (%7,5) buldu ve T139 *«her yeni kural bir
sonraki şablonun tohumu»* dedi. Çeşitlilik metrikleri bu olguyu literatürde
tanınan bir ölçüye bağlar.

### 3.5 Uzunluk ve thinking bütçesi — ✅ hesaplanabilir

Cevap uzunluğu dağılımı · thinking:completion oranı · thinking dili.

**Neden:** T16 (thinking bütçesi ↔ gecikme SLA'sı) ve K46/K50 (thinking dili
veriyle Türkçeye dönüyor) bu projenin kendi bulguları. T248 ayrıca ölçtü:
taban **59** sözcük, ince ayarlı **20-31**.

---

## 4. Ayak C — judge doğrulama (⭐ metodoloji katkısı)

Bu ayak, *«hangi metrik»* sorusunun cevabı değil; *«metriklere ne kadar
güvenilir»* sorusunun cevabı. **Çoğu LLM-as-judge çalışmasında üçü birden
yoktur.**

| # | ölçüm | durum |
|---|---|---|
| 1 | **Tekrar-test gürültü tabanı**, boyut boyut | ✅ K98 (v6) **ve** 2026-09-22 (v9, 24 gizli çift) — neredeyse birebir yinelendi |
| 2 | **Aile yanlılığı, EŞLİ** | ✅ T241: aynı 42 kayıt, Claude↔Gemini; sapma **tek yönlü değil** (`yorumlama` +0,38 ↔ `anlasilirlik` −0,86) |
| 3 | **İnsan çapasına karşı AUC** | ✅ `reports/analiz/2026-09-15-judge-v7-uzman.md` |
| 4 | **Anotatörler arası uyum (κ/α)** | ⛔ **YOK** — tek uzman |

**Kaynak karşılaştırması:** MT-Bench judge bölümü (konum · uzunluk ·
öz-yüceltme yanlılığı + insan uyumu) bu işin yayımlanmış öncülüdür. ⭐ Bu
protokol onun üstüne **(1)** ve **(2)**'yi ekliyor.

⛔⛔ **Ayak C'nin sonucu Ayak B'yi sınırlar:** AUC'si ~0,5 olan bir boyut,
iyileşme iddiası için kullanılamaz. Şu an yalnız **`anlasilirlik`** (0,66)
bu eşiği geçiyor.

---

## 5. Gerileme ve genel yetenek

| eksen | durum | şerh |
|---|---|---|
| `forgetting_smoke` | ✅ taban 28/30 · kollar 27,6 / 26,8 | gerileme yok |
| `safety_crisis` | ✅ ölçülü | ⛔⛔ **T247: korpusta kriz kaydı 0** ⇒ bu eksen korpus büyütmenin etkisini ölçemez |
| `context_fidelity` · `sycophancy` | ✅ taban var | kollarda yeniden koşulmalı |
| **MT-Bench** | ⛔ koşulmadı | ⭐ *bu benim önerim*: katastrofik unutma iddiasını literatürde tanınan bir ölçüye bağlar. ⚠️ İngilizce ⇒ Türkçe varyantı gerekir ya da yalnız İngilizce yeteneği ölçer |
| held-out perplexity | ⛔ koşulmadı | ucuz ama kaliteyle zayıf ilişkili ⇒ ikincil |

---

## 6. İstatistik raporlama — zorunlu

| | kural | dayanağı |
|---|---|---|
| 1 | **Çoklu tohum** ve tohum sayısı yazılı | K213: tek koşu bir çekiliştir |
| 2 | **Güç analizi koşudan ÖNCE**; ayırt edilebilir en küçük fark ilan edilir | T246: 3 tohumda −4,67 → 8 tohumda −1,25 |
| 3 | **Eşik ithal edilmez** — koşunun kendi yayılımından hesaplanır | T245: ±2,4 başka bağlamdan taşındı ve yanlış çıktı |
| 4 | **Etki büyüklüğü + GA**, yalnız p değil | — |
| 5 | **Doğru BİRİM** seçilir | T242: kayıt düzeyli p=0,02, küme düzeyinde p=0,17 |
| 6 | Her eksen puanı **Δ(taban)** olarak | T248: tabanı 21 olan eksende 6,38'i iyileşme sanmak mümkün |
| 7 | Her eksen puanının yanında **boş cevap · uzunluk · kesilme** | T248 |
| 8 | ⛔ **K97:** iki judge'ın sayıları aynı tabloya konmaz | T176/T241 |
| 9 | ⛔ **K137:** rubrik sürümü değişirse eski sayılarla kıyas geçersiz | — |

---

## 7. Kullanılmayacaklar

| | neden |
|---|---|
| ⛔ **BLEU / ROUGE** | açık uçlu terapötik diyalogda referans cevap tek değil |
| ⛔ **AUC ≈ 0,5 olan boyutun ortalaması** | kalite iddiası olarak sunulamaz |
| ⛔ **Tek tohumlu kol karşılaştırması** | K213 |
| ⛔ **`safety_crisis` ile korpus büyüklüğü etkisi** | T247: yapısal uyumsuzluk |

---

## 8. Açık boşluklar — öncelik sırasıyla

1. ⛔⛔ **İkinci uzman + varyans üretecek biçimde tasarlanmış puanlama
   görevi.** Şu an tek uzman, n=48, üç boyutta dağılım %75+ tek değerde ve
   `mi_uyumu` 30/48 boş. κ hesaplanamıyor ⇒ **bütün judge sayıları
   doğrulanmamış bir aletin çıktısı.** En yüksek getirili eksik.
2. ⛔⛔ **Bağımsız aileden judge erişimi** — Ayak A bunsuz koşulamaz.
3. ⛔ **Kapsama matrisi** (eksen ↔ korpus): her eval ekseni için korpusta o
   davranışı taşıyan kayıt sayısı. T247 bu tablo olsaydı koşudan önce
   yakalanırdı. ⭐ *Bu benim önerim.*
4. ⛔ `golden.test` / `golden.locked` hiç kullanılmadı; `dev` üstünde
   yinelenen ölçüm **aşırı uyum** riski taşıyor (K31 mührü bu yüzden var).
5. ⚠️ **İzlenebilirlik:** golden koşularının `kosu.json`'unda `adapter: None`
   yazıyor, ince ayarlı koşuda bile — hangi adaptörle üretildiği yalnız
   etikette. Makale için düzeltilmeli.
