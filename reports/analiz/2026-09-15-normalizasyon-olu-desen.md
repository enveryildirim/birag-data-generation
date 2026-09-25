# Normalizasyon kaynaklı ölü desenler — güvenlik kalıplarında sessiz açık

**Kalıp kaynağı:** `src/tohum_guvenlik.py` · SHA256 `c7531ab9b1f393e3`  
**Girdi:** `data/seeds.jsonl` · SHA256 `0631c02ec7510af35bcd5b229c306c1688afbe1d4471c0c2de5c176ed7b42485`  
**Betik:** `scripts/analiz/2026-09-15-olu-desen-taramasi.py` · **Tarih:** 2026-09-15  
**Düzeltilen:** `src/tohum_guvenlik.py`

---

## 1. Mekanizma

`tr_kucult` NFKD uyguluyor ve yalnızca birleşen NOKTAyı (U+0307) siliyor:

```
tr_kucult("Çarpıntı") == "c" + U+0327 + "arpıntı"   # ç ayrıştı, ime dokunulmadı
assert "çarpıntı" not in tr_kucult("Çarpıntı")           # bileşik iğne, ayrıştırılmış saman
```

Yani **ç ö ü ş ğ içeren her bileşik kalıp**, `tr_kucult`'tan geçmiş metinde
hiç eşleşemez. Hata yok, uyarı yok — kalıp sessizce hiçbir şey yapmaz.

Bulunuşu: K103'te sert kapının yazı-tura attığı üç kayıt bedensel belirti
taşıyordu; kararı deterministik ön-taramaya taşımak isterken regex `öksürük`'ü
bulamadı.

## 2. Etkilenen listeler

| Liste | Kalıp | Karşılaştırma | Ölü kalıp | Etkisi |
|---|---:|---|---:|---|
| `KRIZ_ANAHTAR` | 34 | `tr_kucult(a) in metin` — **iki taraf da** | 0 | ✅ etkilenmedi |
| `RISKLI_ESDURUM` | 11 | `k in tr_kucult(e)` — **ham iğne** | 4 | ⚠️ gizli: bugün kayıp yok |
| `BEDENSEL` (analiz betiği) | 22 | `re.compile(ham).search(tr_kucult(m))` | 9 | ⛔ **kayıp verdi** |
| `KAPALI_KUME` (golden_checks) | 25 | `tr_kucult(k) in KUME` — **bileşik küme** | 4 | ⛔ **ters yönde: meşru öğeyi reddederdi** |

Ölü eşdurum kalıpları: `öz kıyım`, `özkıyım`, `nöbet`, `aşırı doz`. Bugünkü 2.240
tohumda ek yakalama üretmiyor (ölçüldü) — ama yeni veride sessizce kaçırırdı.

### 2b. `KAPALI_KUME` — aynı hatanın TERS yüzü

`golden_checks.py`'de üyelik `tr_kucult(k) in KAPALI_KUME` ile sınanıyordu:
iğne ayrıştırılmış, küme bileşik. Burada sonuç kaçırmak değil **yanlış**
**reddetmek**: bu kavramlarla yazılan her `uydurma_yok` iddiası kapıdan düşer.

Kullanılamaz kavramlar (4/25): `içki`, `tütün`, `uyuşturucu`, `yeşilay`

`golden.dev`'in fiilen kullandığı 7 kavram: `alkol`, `amatem`, `bahis`, `kumar`, `madde`, `rehabilitasyon`, `sigara` — **hiçbiri accent taşımıyor**.

⚠️ Bu, hatanın yazarı o kelimelerden uzaklaştırdığının **kanıtı değil**
(yazar zaten bunları seçmiş olabilir); kesin olan, dört kavramın kullanılamaz
olduğu ve kimsenin fark etmediğidir. Yazılmış hiçbir öğe geçersiz değil —
düzeltmeden sonra `golden.dev` **48/48** geçmeye devam ediyor.

Ayrıca `golden_checks.py` kendi `tr_kucult` **kopyasını** taşıyordu; iki kopya
aynı hatayı taşıyınca biri unutulur. Artık `tohum_guvenlik`'ten alınıyor ve
modülün kendi `_kume_oz_sinamasi()`'sı import anında koşuyor.

## 3. ⭐ Bedensel eksende ölçülen kayıp

⚠️ Burada **iki ayrı değişiklik** var ve karıştırılmamalı: (1) ölü desen hatasının
düzeltilmesi — bir hata onarımı, (2) kalıp listesinin genişletilmesi — benim kararım.
Tablo ikisini ayrı satırda gösteriyor.

| | Tohum | Ne oldu |
|---|---:|---|
| golden havuzu | 1233 | |
| **A** · eski desen, ham | **19** | `2026-09-14-kriz-filtresi-bedensel-acik.md`'deki sayı |
| **B** · eski desen, normalize | **25** | ⛔ **hata onarımı: +6** |
| **C** · yeni desen | **61** | ⚠️ +36 — **iki sebep birden**: kalıp eklendi *ve* desen literal biçimden Türkçe KÖKE çevrildi (`öksürüyor` → `öksür{EK}`). İkisi de benim kararım |

⚠️ 2026-09-14 raporundaki **19** sayısı, ölü desen yüzünden **25** olmalıydı.
Yön değişmiyor (açık gerçekti) ama büyüklüğü eksik ölçülmüştü.

### 3a. Ölü desen yüzünden kaçanlar (A → B)

| Tohum | Dilim | Eşleşen | Mesaj |
|---|---|---|---|
| `3bfe5acbef966f4b` | test | «çarpıntı» | İki haftadır geceleri uyuyamıyorum, kalp çarpıntısı oluyor sabaha karşı. Ama K… |
| `4e0c94a5f4d769fe` | locked | «göğsüm sıkış» | Az önce göğsüm sıkıştı, kalbim deli gibi attı, böyle bir dakika sürdü. Bir kad… |
| `8fbc22c3b78d7a29` | dev | «çarpıntı» | Vizede bir kere oda arkadaşımın Ritalin'inden almıştım, çarpıntım oldu açıkças… |
| `abf29120517d17fd` | locked | «çarpıntı» | şu an telefonda iki sekme açık. birinde oda arkadaşımın 'sınavdan iki saat önc… |
| `b1a741f15df8f951` | dev | «çarpıntı» | merhaba, biraz garip bir şey soracağım. oda arkadaşım finallerden önce bana bi… |
| `de21c622d22fd781` | dev | «göremiyorum» | TikTok'ta herkes çok güzel, bakımlı görünüyor. Ben kendime bakınca hiç öyle gö… |

Dilim dağılımı: dev 3 · locked 2 · test 1

⛔ `4e0c94a5f4d769fe` **`locked` havuzunda** ve metni *«Az önce göğsüm sıkıştı,
kalbim deli gibi attı, böyle bir dakika sürdü»* — settteki en güçlü bedensel işaret
ve filtre onu hiç görmemişti.

⚠️ **Bu sayı "kaçırılan kriz" DEĞİL** (Kural 3). `de21c622d22fd781`'deki
*«kendime bakınca hiç öyle göremiyorum»* beden değil benlik algısı — regex bilerek
geniş. Hangisinin tıbbi aciliyet taşıdığı uzmanın kararı.

### 3b. ⚠️ Benim eklediğim kalıplar (B → C) — Kural 6

Bunlar hata onarımı DEĞİL, bir genişletme kararı. Gerekçe: K103'te sert kapının
yazı-tura attığı üç kaydın belirtileri (sabah bulantısı · geçmeyen öksürük ·
Juul sonrası çarpıntı) eski listede **yoktu**. Eklenen kökler:

`kalbim (deli gibi/hızlı) at` · `titriyor` · `mide(m) bulan` · `bulantı` · `nefes(im) zor/daral` · `göğsüm ağırlaş` · `göğsümde ağırlık` · `öksürük` · `öksürüyor` · `kan tükür` · `kan geliyor` · `kan gelmiş`

Etki: havuzda **+36** tohum — ⚠️ bunun bir kısmı yeni kök değil, **eski köklerin kaçırdığı çekimler** (`öksürerek`, `öksürdüğümü`). Listenin doğru kesiti klinik karardır ve
uzman Oturum 1'e aittir (Kural 3) — bu genişletme *kapsamı*, *eşiği* değil değiştirir.

### 3c. ⭐ Yanlış pozitif — neden OTOMATİK KAPI olamaz

Aynı kalıp yazılmış **48** golden.dev öğesinde denendi. Düzeltme öncesi **2** vuruş vardı ve **ikisi de yanlış pozitifti**:

| Öğe | Alıntı | Neden yanlış | Ayrılabilir mi |
|---|---|---|---|
| `gd-011` | «içim hâlâ titriyor» | duygusal deyim, beden değil | ✅ evet — dilbilgisel, kalıptan düşüldü |
| `gd-040` | «oğlum sürekli öksürüyor» | **başkasının** belirtisi | ⛔ hayır — özne çözümü gerekir |

Düzeltmeden sonra kalan vuruş: **2** (`gd-024`, `gd-040`).

⚠️ **«Kalan vuruş» ≠ «kalan yanlış pozitif».** Desen literal biçimlerden Türkçe köke çevrildikten sonra (`öksürüyor` → `öksür{EK}`) listeye birinci tekil, kendi bedenine ait bir vuruş da girdi — yukarıdaki iki vakayla aynı sınıfta değil. Hangisinin tıbbi aciliyet taşıdığı **klinik karardır** ve uzmana aittir (Kural 3); bu betik sınıflandırmaz.

⛔ **Sonuç: bu kalıp otomatik dışlama kapısı olarak KULLANILAMAZ.** İkinci
sınıfı regex ayıramaz. Fonksiyon "bakılacak yer" işaretler; öğe yazarken
elle denetlenir. Bu, K40'ın (cümle sayan oran kapısı yanlış eliyordu) ve
K65'in (anahtar kelime kelime içinde eşleşiyordu) aynı dersi: **Türkçe serbest
metinde anahtar kelime kapısı karar veremez, yalnızca aday gösterir.**

## 4. Düzeltmenin geriye dönük etkisi

| Kontrol | Sonuç |
|---|---|
| golden havuzunda `kriz_icerigi` işareti | 0 (değişmedi — havuz zaten önceden süzülmüş) |
| `golden.dev`'de kullanılmış tohum | 40, **hiçbiri** yeni işaret almadı |
| `evals/bolme.json` mührü | dokunulmadı (K31) |
| korpus `checks.run_checks` | 104/104 geçmeye devam ediyor |

Yani düzeltme **hiçbir yazılmış öğeyi geçersizleştirmiyor**; yalnızca bundan
sonra yazılacak `safety_crisis` ve `golden.{test,locked}` öğelerinin havuzunu
doğru gösteriyor.

## 5. Kalıcı savunma — `_olu_desen_taramasi()`

Tek tek kalıp düzeltmek bu hatayı bir daha önlemez; liste büyüdükçe geri gelir.
Bu yüzden `src/tohum_guvenlik.py` **import anında** her güvenlik kalıbını kendi
metninde arıyor ve bulamazsa `AssertionError` atıyor.

Sınama **şekil değil davranış** ölçüyor: bileşik yazılmış olmak tek başına hata
değil (`kriz_icerigi` iki tarafı da normalize ediyor). Hata, tüketen kodun HAM
kalıbı normalize metinle karşılaştırmasıdır — ve o ancak kalıbı gerçek arama
yolundan geçirerek görülür.

Kapsanan tarihsel tuzaklar: `İntihar` (K76, büyük-İ) · `Nöbet` ve `Aşırı doz`
(bugün, ö ve ş) · altı bedensel kalıp.

## 6. Aile kaydı

| # | Sessizce yanlış çalışan katman |
|---|---|
| K44 | eğitim template'i thinking'i siliyordu |
| K47 | eval regex'i kapanış etiketi bekliyordu, "thinking yok" diyordu |
| K49 | LoRA hedef anahtarı hiçbir modülle eşleşmiyordu |
| K52 | kriz filtresi etikete bakıyordu, içeriğe değil |
| K65 | anahtar kelime kelime İÇİNDE eşleşiyordu ("belirtilmez" → "belirti") |
| **bugün** | **güvenlik kalıbı normalizasyon yüzünden hiç eşleşemiyordu** |

