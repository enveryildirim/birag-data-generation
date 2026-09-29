# Makale notları — `v0.1.1` çalışmasından çıkabilecek yayınlar

> **Amaç:** `v0.1.1` (düşünmenin kararlar korunarak yeniden kurulması) boyunca ortaya çıkan
> bulgulardan hangilerinin makaleye dönüşebileceğini, **hangi kanıtın elde olduğunu** ve
> **neyin eksik olduğunu** tek yerde tutmak. Katkıların kendisi [katki-defteri.md](katki-defteri.md)'nde;
> bu dosya onları yayın adaylarına göre gruplar.
>
> ⛔ **Kural 7:** sohbette üretilen sayı tezde (ve makalede) kullanılamaz. Aşağıdaki her sayının
> yanında kaynağı yazılı; kaynağı yalnız defter olanlar **⚠️** ile işaretli ve kullanılmadan önce
> bir betikle yeniden üretilmeli (§5).
>
> ⭐ `tez-plani.md` §7 *«tezden makale çıkacak mı? (T1/T2/T10 buna uygun)»* diye soruyordu. O üç
> kalem (Türkçe ruh sağlığı NLP boşluğu · TCK 191/3 segmenti · bf16 LoRA ↔ QLoRA) burada
> değerlendirilmedi; bu dosya yalnız `v0.1.1`'den doğan adayları ekler.

**Tarih:** 2026-09-29 · **Durum göstergesi:** ✅ raporlu (betik + rapor dosyası var) · ⚠️ yalnız defter · 🔜 Faz 4'e bağlı

---

## 1. Aday A — ana makale: kararları değiştirmeden iç muhakemeyi yeniden kurmak

**Çalışma başlığı:** *Türkçe bir bağımlılık destek modelinin eğitim verisinde iç muhakemeyi klinik
kararları koruyarak yeniden kurmak: bir boru hattı, ölçülmüş kapılar ve önceden kayıtlı bir sınama.*

**İddia.** Var olan 1039 kaydın düşünmesi, kayıtlı klinik kararlar korunarak yeniden kurulabilir;
her kararın korunduğu bağımsız bir okumayla sınanabilir ve bunun modele geçip geçmediği önceden
kayıtlı bir kıyasla ölçülebilir.

**Katkı.** (i) Yeniden üretim yerine *yeniden kurma*: cevap, kullanıcı turları ve kararlar sabit,
yalnız düşünme değişir. (ii) Ölçülmüş kapılar: benzerlik (≥ 0,6 sert), karar eşlemesi (birebir alt
dize), bağımsız karar korunumu okuması, bitişi değişen kayıtta eski↔yeni aynı judge. (iii) Ön kayıt,
iki ek ve sonuç yokken yazılmış çözümleme.

| kanıt | değer | kaynak | durum |
|---|---|---|---|
| kabul | **1036/1039** (3 red: 0094 temizlik · 0840 · 0909 karar düştü) | `reports/analiz/2026-09-24-v011-faz2.md` | ✅ |
| eski ↔ yeni benzerlik, ortanca | **0,31** (≥ 0,6: 1 kayıt) | aynı | ✅ |
| düşünmede «sormuyorum» | **%30,6 → %3,1** | `reports/analiz/2026-09-29-v011-derleme.md` | ✅ |
| düşünmede ⛔/⭐ | **%22,8 → %0,2** | aynı | ✅ |
| düşünme ortanca sözcük | **72 → 112** | aynı | ✅ |
| son tur soruyla biten | **%50,3 → %49,4** (cevabı değişen yalnız **9** kayıt) | aynı | ✅ |
| bitiş adayları | 156 aday → `degisti` 9 · `korunan_soru` 9 · `degismedi` 138 | `reports/analiz/2026-09-24-v011-faz2.md` | ✅ |
| kıyas kolunun modeldeki değerleri (`v0.1.0`, MLX) | B1 %51,4 · B2 %13,0 · tek tur soruyla bitme 74,1 ± 1,8 | `reports/analiz/2026-09-29-v011-onkayit.md` (tam beyan) · `…-onkayit-ek1.md` | ✅ |
| **modele geçti mi** (B1 ↓ ∧ B2 ↓) | — | `reports/analiz/2026-09-29-v011-onkayit-ek2-sonuc.md` (henüz yok) | 🔜 |

**Önceden kayıtlı negatif sonuç — yayına değer.** K277'nin bitiş müdahalesi ~170 kayıt bekliyordu,
**9**'da kaldı (T300). Ön kayıt bunu sonuçtan önce yazdı: soruyla bitme ölçülerinde *«etki
beklenmez»* (`2026-09-29-v011-onkayit.md`). Demodaki *«her cevap soruyla bitiyor»* gözlemi bu
sürümle düzeltilemez — ve bunun nedeni veride gösterilebiliyor.

**Eksik.** Faz 4 (Colab). Onsuz makale bir **veri** makalesi; B1/B2 sonucuyla bir **model** makalesi.

**Aday C (§3) bu makaleye bir bölüm olarak girebilir.**

---

## 2. Aday B — kısa yöntem makalesi: LLM denetçinin güvenilirliği

**Çalışma başlığı:** *Bir LLM denetçi rubriğinin girdi tanımı, sadık yeniden kurmayı cezalandırabilir.*

**Bulgu 1 — rubrik boşluğu (T302 · T303).** `karar-korunumu.v1` girdiyi «Konuşma» (*önceki* asistan
turları) ve «Cevap» (*bu turun* cevabı) diye ayırıyor, uydurmayı ise *«konuşmada olmayan»* diye
tanımlıyordu ⇒ bu turun cevabı «konuşma»nın dışında kalıyor ⇒ **kendi cevabına tam sadık bir düşünme
sert kapıdan (`uydurma`) düşebiliyor.** İki bağımsız okuyucu, iki ayrı kayıtta, bunu kendi sözleriyle
yazdı. Tanım düzeltilince (v2) iki red geri döndü.

| kanıt | değer | kaynak | durum |
|---|---|---|---|
| v1 okumalarında `uydurma` | **7/1145** okuma · gerekçesinde cevabı anan **3** | `reports/analiz/2026-09-29-korunum-uydurma-dokumu.md` | ✅ |
| tanım düzeltmesinin etkisi | 1034 → **1036** kabul; #0920 ve #0991 v2 ile `korundu` | `reports/analiz/2026-09-24-v011-faz2.md` (rubrik dağılımı satırı) | ✅ |
| v1 ↔ v2 farkı | yalnız «konuşma» tanımı | `prompts/karar-korunumu.v1.md` ↔ `v2.md` | ✅ |

⚠️ Defterde (T302) *«6/1144 · 2»* yazıyor; aradaki fark tek okuma — #0920'nin v1 okuması o sayımdan
**sonra** depoya girdi. Yeniden üretilebilir değer yukarıdaki.

**Bulgu 2 — aynı metne zıt sert-kapı hükmü (T302).** #0920'nin `uydurma` işaretlenen 1. paragrafı
onarımdan önce ve sonra **birebir aynı**; iki okuma zıt hüküm verdi (`uydurma` 0 ↔ 1).
Kaynak: `reports/analiz/2026-09-29-korunum-uydurma-dokumu.md` §2 (git geçmişinden doğrulandı) ✅.
T300'de iki okuyucu aynı cümleye *«makul çıkarım»* ↔ `uydurma` dedi ⚠️ (yalnız defter).

**Eksik — bu makale onsuz yazılamaz.** Tasarlanmış bir **iki-kör-okuyucu gürültü tabanı deneyi**
(aynı kayıtları iki bağımsız okuyucu, önceden kayıtlı bir uyum ölçüsüyle). Şu anki kanıt tekil
örnekler; gürültü tabanı ölçülmedi (T291'den beri açık).

⚠️ **Denetçi yolu güvenilmez:** bu oturumda denetim okumalarının 10 denemesinden 4'ü güvenlik
sınıflandırıcısına takıldı, 1'i kısmi (T303 · T304) ⚠️ yalnız defter. Deney tasarımı bunu hesaba katmalı.

---

## 3. Aday C — çok belgeli talimatlarda çatışan tanımlar (A'ya bölüm olarak)

**Desen (T298 · T304).** Aynı boru hattında iki belge zıt yöne çekiyor ve aradaki kayıt cezalanıyor;
üç örnek aynı biçimde:

| çatışma | ne oldu | kaynak | durum |
|---|---|---|---|
| **Yaş** — `uretim-v6` §1b çekinceli yaşı serbest bırakıyor, taslak istemi satır 49 yasaklıyordu | iki belge blok 21'den (`d590658`) beri çelişiyordu; kullanıcı §1b'yi geçerli saydı, satır hizalandı | `prompts/v011-faz2-taslak.md` · T304 | ✅ (belgeler) · ⚠️ sayım |
| **Olumsuz pay ↔ ret** — olumsuz pay hedefi (T285) ile *reddi koru* (`karar-korunumu` §1) | 7 kayıtta birinci tekil ret atfa çevrildi (*«tek kelime etmiyorum»* → *«hekimin alanında kalıyor»*); geri konunca pay %14-17'de kaldı ⇒ hedef reddi silmeyi gerektirmiyordu | T298 §2 | ⚠️ |
| **Kök neden talimatın örneğiydi** | `uretim-v6`'nın benzerlik kuralı için verdiği tek örnek (*«Miktara girmiyorum»* ↔ *«Saydığını olduğu gibi geri veriyorum»*) reddi atfa çeviriyor | `prompts/uretim-v6.md` (örnek + 2026-09-29 şerhi) | ✅ |

**Çözüm biçimi — kapıların sırası:** sert kapı (karar düşmesi) yumuşak hedefin (olumsuz pay) üstünde;
`uretim-v6.md`'ye yazıldı (T304) ✅.

---

## 4. Destekleyici notlar — yöntem bölümü ya da tartışma

**4.1 Yanlış veri üstünde koşup başarı bildiren denetimler — beş örnek.** Her birinde tek işaret
*fazla temiz* bir sayıydı; hiçbiri kendini bildirmedi:

| # | ne oldu | kaynak |
|---|---|---|
| 1 | düzenleme betiği dışa aktarılmamış bir kabuk değişkeni yüzünden hiçbir şey yapmadı; `kontrol` değişmemiş dosyalara temiz dedi | T297 §6 ⚠️ |
| 2 | yaş taraması var olmayan bir alanı okudu ⇒ **0/965** | T298 §4 ⚠️ |
| 3 | yönlendirme taraması var olmayan `completion` alanını okudu ⇒ 38 kayıt koşulsuz «temiz» | T298 §4 ⚠️ |
| 4 | rubrik sürümü kayıt numarasından damgalandı ⇒ var olan v1 okumaları «v2» diye etiketlendi | T303 · `scripts/analiz/2026-09-24-v011-faz2.py` (düzeltme yorumu) |
| 5 | mühürlü çözümlemenin iki raporlanır ölçüsü puanlanmış dosyada olmayan alanları okuyordu ⇒ gecikme vekili **her zaman 0**; uçtan uca sınama yakalamadı çünkü iki kol da 0'dı | T308 · `reports/analiz/2026-09-29-v011-onkayit-ek2.md` ✅ |

⭐ **Makaleye girecek cümle:** *Δ = 0 veren bir sınama, iki tarafın da boş olduğu bir ölçüyü doğrulamaz.*
⭐ Çıkarılan ilke: kapının koştuğunu değil, **neyin üstünde koştuğunu** doğrula (girdi boşsa assert).

**4.2 Bir eleğin sayısı hata profili ölçülmeden anlamsızdır (T301 · T293 §4).** Düşünme ↔ cevap
eleğinin ilk sürümü **%37,1** işaret verdi; dört örnek okumak iddiayı on kat küçülttü. Bugünkü koşu
**97/1039 (%9,3)**; en önemli kategoride (*düşünme «yönlendirme yok» diyor, cevap yönlendiriyor*)
**7/7 yanlış olumlu**. Kaynak: `reports/analiz/2026-09-29-v011-dusunme-cevap.md` ✅ (ilk koşu 98'di;
fark #0920'nin onarımı, raporda açıklı).

**4.3 LLM ile üretilmiş veride ek'li ön kayıt (T305–T308).** Ölçümün bağlı olduğu her dosya SHA ile
mühürlü (üç mühürde 55 dosya); çözümleme sonuç yokken yazıldı ve iki kol aynıyken uçtan uca sınandı
(her Δ = 0); kazanç şartı (EK-1) ve platform değişikliği (EK-2) **ilk çıktıdan önce** ek olarak yazıldı;
ekleri yazan betikler çıktı varsa duruyor. Kaynak: `configs/deney/2026-09-29-v011-on-kayit*.json` ·
`reports/analiz/2026-09-29-v011-onkayit*.md` ✅.

**4.4 Bitiş müdahalesinin gücü önceden hesaplandı (T306).** `v0.1.0` kolunun tohum dağılımıyla
okunabilir en küçük düşüş: B1 **10,3 puan** (gerekli < %41,1) · B2 **8,0 puan** (gerekli < %5,0).
B2 şartın bağlayıcı yarısı. Kaynak: `reports/analiz/2026-09-29-v011-onkayit-ek1.md` ✅.

**4.5 MLX → PEFT/Unsloth aktarımının tuzakları (T308).** `mlx_lm` 0.31.3 kaynağından okundu:
LoRA `scale` 20 ⇒ `lora_alpha` 160; başlangıç dağılımları aynı; MLX AdamW `bias_correction=False`,
torch'ta hep açık (birebir aktarılamayan tek şey). ⚠️ Unsloth'un alışılmış `target_modules=['q_proj','o_proj']`
çağrısı, **Gemma benzeri sahte bir ağaçta** LoRA'yı 42 katmanın hepsine ve görü kulesine koydu — gerçek
Gemma 4'te sınanmadı. Kaynak: `reports/analiz/2026-09-29-v011-onkayit-ek2.md` ✅ (sınama betikleri depoda
değil ⚠️ §5).

**4.6 Taslağı kimin yazdığı (T300) — gözlem, sonuç değil.** Blok 39-40'ta Claude Code taslaklarının
sert-kapı onarımı alt ajanlarınkinden fazlaydı (b40: 24 kaydın 7'si onarım, 6'sı sert kapı; b39 alt
ajanların 16 kaydında 0). ⛔ **Karışık:** bitiş adaylarını Claude Code yazdı, alt ajanlar aday
olmayanları — kayıt zorluğu eşit değil. ⚠️ yalnız defter.

**4.7 Türkçeye özgü bir gözlem.** Bir düşünmenin *«kişi görüşmede yoktu»* çıkarımını dayandırabileceği
tek ipucu `-miş`'li kanıtsallıktı (*«Okul müdürü ailemle görüşmüş»*); çıkarım olarak kurulunca
denetçi geçirdi, olgu gibi kurulunca `uydurma` dedi (#0906, T304). Tekil örnek; dilbilim notu.

---

## 5. Hakemin soracakları — beyanı zorunlu olanlar

| | |
|---|---|
| ⛔ **Yazarlık ve bağımsızlık** | 1039 taslağın **206**'sı Claude Code'a ait (pilot 40 · bitiş adayı 144 · alt ajan yolu kapandıktan sonra 22); **bütün** revizyonlar Claude Code; denetçiler Claude alt ajanları — aynı model ailesi (`reports/analiz/2026-09-24-v011-faz2.md` başlığı ✅) |
| ⛔ **İnsan okuması yok** | pilotun 40 kaydı henüz insan tarafından okunmadı (K277'nin ikinci güvence katmanı); hiçbir klinik karar uzman onayından geçmedi |
| ⛔⛔ **Etik kurul kaydı yok** | `tez-plani.md` §5 *«en acil eksik»*; yayın için sert engel |
| ⛔ **Kriz dilimi hariç** | `v0.1.0` gibi (K275); güvenlik ekseni korpusa kördür (T259) |
| ⚠️ **Tek okuyucu** | kayıtların çoğunda tek korunum okuması; gürültü tabanı bilinmiyor (§2) |
| ⚠️ **İki rubrik sürümü** | 1143 okuma v1, 4 okuma v2 (rapor başlığında yazılı ✅) |
| ⚠️ **Model sonuçları iki çerçevede** | kayıtlı `v0.1.0` koşuları MLX; Faz 4 Colab/Unsloth — birbirleriyle doğrudan karşılaştırılamaz (EK-2) |

---

## 6. Sayı envanteri ve kapatılacak boşluklar (öncelik sırasıyla)

1. 🔜 **Faz 4 sonucu** — Aday A'nın model iddiası buna bağlı (`notebooks/v011-unsloth-egitim.ipynb`).
2. ⚠️ **Gürültü tabanı deneyi** — Aday B bunsuz yazılamaz. Tasarım: aynı kayıt kümesini iki kör okuyucu,
   önceden kayıtlı uyum ölçüsü (κ ya da sert-kapı uyuşma oranı), sınıflandırıcı kesintisi için kural.
3. ⚠️ **T298 §2'nin 7 kaydı** — «önce» hâli depoda yok (blok 38 yalnız onarımdan sonra commit'lendi);
   *«pay %14-17'de kaldı»* bugünkü dosyalardan yeniden hesaplanabilir, *«ret silinmişti»* ancak oturum
   dökümünden (ajanın ilk `Write` çağrısı — T304'te 0901/0906 için yapıldığı gibi) kurtarılabilir.
4. ⚠️ **Yaş çekincesi sayımı (T298 §1)** — tanımı kayıtlı değil; basit bir kalıpla bugün 7 kayıt
   bulunuyor, defterin sayımıyla (6, sonra +2) örtüşmüyor ⇒ tanım yazılıp betikle yeniden ölçülmeli.
5. ⚠️ **EK-2 sınama betikleri** — `reports/analiz/2026-09-29-v011-onkayit-ek2.md`'deki sınamalar
   (maske, bölme, LoRA hedefi, şablon, eğitim, puanlama) oturum çalışma alanında koşuldu; depoya
   betik olarak eklenmeli ki yeniden koşulabilsin.
6. ⚠️ **T300 taslak kalitesi, T297 §6 ve T298 §4'ün sayıları** — yalnız defter; kullanılacaksa yeniden üretilmeli.

✅ Bu dosya yazılırken kapatılan iki boşluk: T301 artık rapor yazıyor
(`reports/analiz/2026-09-29-v011-dusunme-cevap.md`) ve T302/T303'ün denetçi sayıları raporlandı
(`reports/analiz/2026-09-29-korunum-uydurma-dokumu.md`).
