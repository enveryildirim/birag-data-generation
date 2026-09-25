# Özgünlük taraması — kanıta bağlı LLM-judge rubriği

> **Amaç:** T43/T46/T51/T58'in özgünlük iddialarını **daraltmak**. Bu taramanın işi
> iddiayı doğrulamak değil; aksi çıkarsa aksini yazmak.
>
> **Tarama tarihi:** 2026-09-16 · **Tarayan:** Claude Code (kullanıcı onayıyla, Kural 1)
> · Kayıt: `PROJECT_MEMORY.md` K141 · `katki-defteri.md` T67

---

## ⛔ Özet — iddiaların çoğu daraldı

| Kalem | Ne iddia ediliyordu | Tarama sonucu |
|---|---|---|
| **T43** çekirdeği | rubrik alıntı ister, **kod** alıntıyı kaynakta doğrular | ⛔ **ÖZGÜN DEĞİL** — yayımlanmış |
| **Rubrik mühürleme** (K31 hattı) | rubrik sürümü kilitlenir, değişiklik ikinci set olur | ⛔ **ÖZGÜN DEĞİL** — *«locked rubrics»* |
| **Asimetrik doğrulama** | doğrulanamayan **muafiyet düşer**, doğrulanamayan **suçlama yalnız kaydedilir** | ◐ **şimdilik ayakta** |
| **T46** caydırıcılık | kapı ilan edilince judge davranışı değişiyor, kapı hiç ateşlemiyor | ◐ **daraldı** — genel olgunun örneği |
| **T58** bozma deneyi | kusuru üret, kapının gücünü ölç | ⛔ **YÖNTEM ÖZGÜN DEĞİL** — mutasyon testi |
| **T51** hat denetimi | alıntı zorunluluğu **ölçüm hattını** geriye dönük denetlenebilir kılıyor | ◐ **doğrudan eşleşme bulunamadı** |

---

## 1. ⛔ T43'ün çekirdeği yayımlanmış — ve BİZDEN ÖNCE

**Hong, Yao, Shen, Xu, Wei, Dong** — *From Rubrics to Reliable Scores:
Evidence-Grounded Text Evaluation with LLM Judges* · arXiv:2601.08654
(ilk sürüm **13 Ocak 2026**, başlığı *«Rulers: Locked Rubrics and Evidence-Anchored
Scoring for Robust LLM Evaluation»*).

Kaynağından doğrulanan içerik:

| Rulers'ın yaptığı | BıRAG'ın v7→v9 hattında karşılığı |
|---|---|
| **extractive quote verification** — alıntı kaynakta **deterministik dizge eşlemesiyle** doğrulanıyor (§3.3'teki `V_τ(e, U_x)` işleci; LLM ile değil) ✅*doğrulandı* | `_dogrula()` + `alinti_nrm()` — **aynı fikir** |
| **locked rubrics** — ölçüt sürümlenip **değişmez paketlere** derleniyor, her puan için denetlenebilir kanıt isteniyor | K31 mührü + `judge-eksen1.v1…v9` sürümleri — **aynı fikir** |
| *«unverifiable score attribution»* zaten adlandırılmış bir kusur sınıfı | T43'ün teşhisi — **aynı teşhis** |

⛔ **Sonuç açıkça yazılmalı:** *«LLM-judge rubriğinde alıntı istemek yetmez, alıntının
kaynakta bulunduğunu KOD doğrulamalı»* iddiası **özgün değildir**; bizden sekiz ay
önce yayımlanmıştır. T43'ün ve T46'nın bu kısmı tezde **bağımsız yeniden keşif**
olarak yazılmalı, katkı olarak değil.

### ⭐ Ama üç şey Rulers'ta **yok** — kaynağından tek tek soruldu

| Soru | Rulers |
|---|---|
| Doğrulama **asimetrik** mi (kanıt hükmü kurduğunda mı düşürdüğünde mi sert)? | ⛔ **hayır** — tek biçimli uygulanıyor |
| Doğrulama gerçek veride **kaç kez ateşliyor**? | ⛔ **bildirilmiyor** |
| Kapının varlığını judge'a söylemek **davranışını değiştiriyor mu**? | ⛔ **ele alınmıyor** |

➡️ *Daralan iddia şu olur: mekanizma özgün değil, ama mekanizmanın **yönü**
(asimetri) ve **ateşlememesinin okunması** ele alınmamış.*

---

## 2. ⛔ Alıntı doğrulamasının daha eski kökü: atıflandırılabilirlik

**Rashkin ve ark.** — *Measuring Attribution in Natural Language Generation Models*
· arXiv:2112.12870 · *Computational Linguistics* 49(4), 2023. **AIS** çerçevesi
üretimi bağımsız bir kaynağa karşı doğrulamayı biçimselleştiriyor; **alıntı
(quotation)**, modelin kaynaktan **birebir** parça üretmesi olarak atıflandırmanın
dar bir biçimi diye tanımlanıyor.

➡️ Yani *«birebir alıntı = denetlenebilir dayanak»* fikri 2021-2023 hattında zaten
var. BıRAG'ın yaptığı, onu **judge'ın kendi çıktısına** uygulamak — bu kaydırma
küçük ama gerçek; Rulers da aynı kaydırmayı yapmış.

---

## 3. ◐ T46 daraldı — *«değerlendirme farkındalığı»* zaten bir literatür

*«Kapıyı ilan etmek judge'ın davranışını değiştiriyor, bu yüzden kapı hiç
ateşlemiyor ve sınanmamış kalıyor»* (T46) bulgusu, adlandırılmış iki alanın
kesişiminde duruyor:

| Alan | İlgisi |
|---|---|
| **Evaluation awareness** — modelin değerlendirildiğini fark edip davranış değiştirmesi (arXiv:2605.05835 · 2608.21766) | T46'nın mekanizması bunun **judge tarafındaki** örneği |
| **Guardrail Fallacy** (arXiv:2603.20320) | dış korumalar zararı engellediği için sistem güvenli **görünüyor**; sonuç tabanlı ölçüm gizli riski olduğundan az gösteriyor |
| **Phantom Guardrails** (arXiv:2607.13083) | hiç gerçekleşmeyen bir kusur sınıfı için konmuş korumanın sınanması |

➡️ *Daralan iddia: T46'nın olgusu yeni değil; yeni olabilecek şey onun bir
**LLM-judge rubriğinde** ve **ölçülmüş bir sıfırla** (0/162) gösterilmesi.*

---

## 4. ⛔ T58'in yöntemi özgün değil — mutasyon testi

*«Kapı ateşlemiyorsa kusuru ÜRET ve yakalayıp yakalamadığını ölç»* yöntemi,
yazılım mühendisliğinin **mutasyon testi**dir: yapay kusur enjekte edilip tespit
oranı ölçülür. LLM bağlamında da yaygın olarak kullanılıyor (ör. arXiv:2406.09843).

⚠️ Mutasyon testi literatürünün kendi uyarısı bizim raporumuzdakiyle **aynı**:
yüksek mutasyon skoru, mutantların gerçek kusurlara benzemesinden değil
**kolay yakalanmasından** gelebilir. T58 bunu bağımsız olarak yazmıştı
(*«metni DEĞİŞTİREN dört kipte %100 yapı gereği»*) — ⭐ tutarlılık lehte, ama
özgünlük iddiası değil.

➡️ *Daralan iddia: yöntem ödünç; özgün olabilecek tek şey onun bir LLM-judge
kanıt kapısına uygulanması ve kiplerin **gözlenmiş kusur sınıflarından**
türetilmesi.*

---

## 5. ◐ T51 — doğrudan eşleşme **bulunamadı**

*«Alıntı isteyen bir rubrik, judge'ı disipline etmenin yanında ÖLÇÜM HATTINI
geriye dönük denetlenebilir kılar; alıntı istemeyen rubrikle puanlanmış koşularda
sonuç-kayıt kayması bugün de gelecekte de görünmez»* iddiası için aranan sorgular:

- *«detecting misaligned results record mismatch evaluation pipeline annotation swap quotes audit LLM evaluation integrity»*
- *«LLM judge quote hallucination check deterministic string match evidence gate ablation how often fires»*

Çıkanlar veri denetimi (HH-RLHF/HelpSteer2'deki yapısal çelişkiler), etiketleyici
tutarlılığı ve konum değiştirme (position swap) sınamalarıydı; ⛔ **sonucun yanlış
kayda yazılmasını alıntılar üzerinden yakalama** fikrine rastlanmadı.

⚠️ **Ama bu iki sorguya dayanıyor.** *«Bulunamadı» ≠ «yok»* — ve bu, defterdeki
diğer dört kalemin hepsinin ilk aramada çıktığı düşünülünce **zayıf** bir negatif
değil, ama yeterli de değil.

---

## 6. ⭐ Tarama sonrası ayakta kalanlar — ve nasıl yazılmalı

| Kalem | Tezde nasıl yazılmalı |
|---|---|
| **Asimetrik doğrulama** (muafiyet düşer / suçlama kaydedilir) | ⭐ katkı olarak; gerekçesi **alan gereği** (Kural 3: güvenlik ekseninde yanılma yönü seçilir) ve Rulers'ta yok |
| **T51 hat denetimi** | ◐ katkı adayı; ⚠️ *«bir tarama turunda bulunamadı»* kaydıyla |
| **Sağlama bütünlüğü kusurunun bulunması** (T49/T50: sonucun yanlış dosyaya yazılması, iki ayrı partide) | ⭐ **olgu katkısı** — literatürde aranmadı bile; bir ölçüm hattı kusurunun belgelenmesi |
| T43/T46 çekirdeği | ⛔ **bağımsız yeniden keşif** olarak; öncelik Rulers'ta |
| T58 yöntemi | ⛔ **uygulama** olarak; yöntem mutasyon testinden ödünç |

---

## 7. ⛔ Bu taramanın sınırı

| | |
|---|---|
| ⛔ **Sekiz sorgu** | sistematik derleme değil; ACL/EMNLP bildiri taraması yapılmadı |
| ⛔ **Rulers tek sürümden okundu** | v2 HTML; v1 ile farkları karşılaştırılmadı |
| ⚠️ **Asimetri sığ arandı** | tek sorgu; hukuk/tıp değerlendirme literatüründe karşılığı olabilir |
| ⛔ **Türkçe literatür bu turda aranmadı** | ayrı belge: `benzer-calismalar.md` |
| ⭐ **Yön dürüst tutuldu** | tarama iddiayı daraltmak için yapıldı ve **daralttı**; lehte çıkan tek şey Rulers'ın üç boşluğu |

---

# EK — Asimetri, hukuk ve tıp literatüründe arandı (2026-09-16, ikinci tur)

§6'da *«şimdilik ayakta»* denen tek kalem — **asimetrik doğrulama** — üç ayrı
alanda arandı. ⛔ **Üçünde de karşılığı var.**

## E1. Hukuk — asimetrik ispat yükü kurucu bir ilke

Ceza hukukunda yük **zaten asimetriktir**: iddia makamı suçun her unsurunu
*«makul şüphenin ötesinde»* ispatlamakla yükümlüdür; buna karşılık **olumlu
savunma** (affirmative defense) — fiil sabit olsa bile sorumluluğu **kaldıran**
savunma — ileri süren tarafa bir **ispat ya da gösterme yükü** düşer (ör.
zorunluluk hâli *«delillerin üstünlüğü»*, akıl hastalığı *«açık ve inandırıcı
delil»* ölçüsüyle).

➡️ **Yapı birebir bizimki:** bir **muafiyet** ileri sürülüyorsa dayanağı
**gösterilmelidir**; gösterilemezse muafiyet düşer.

⛔ **Ama yön TERS.** Ceza hukukunun asimetrisi **sanığı** korur (haksız mahkûmiyet
daha pahalıdır). Bizim asimetrimiz **kullanıcıyı** korur: doğrulanamayan muafiyet
düşer *ve* doğrulanamayan suçlama da hükmü değiştirmez — iki yol da ihlali
**arttırır**. ➡️ *Asimetrinin VARLIĞI hukukun en eski kurumlarından biri;
seçilen YÖN alanın kayıp işlevine bağlı ve bizimki ceza hukukunun tersi.*

## E2. İstatistik — Neyman-Pearson bunu biçimselleştirmiş

**Neyman-Pearson sınıflandırma paradigması** tam olarak *«hangi hatada yanılmaya
razısın»*ı biçimselleştirir: I. tip hatayı kullanıcının belirlediği bir α
sınırının altında **tutar**, II. tip hatayı o kısıt altında en aza indirir.
Alanın kendi motive edici örneği kanser tanısıdır: hastayı sağlıklı saymak,
sağlıklıyı hasta saymaktan daha ağırdır.

➡️ ⛔ *«Yanılma yönü seçilir»* ilkesi **ders kitabı**dır. Kural 3'ün
*«güvenlik ekseninde gerileme kabul edilebilir değildir»* cümlesi bunun alanımıza
çevrilmiş hâli — özgün bir ilke değil, **doğru uygulanmış** bir ilke.

## E3. Tıp — SpPin / SnNout: amaca göre asimetrik eşik

Kanıta dayalı tıbbın onyıllardır öğrettiği ayrım: **tarama**da duyarlılık
(vakayı kaçırmamak), **doğrulama**da özgüllük (yanlış alarm vermemek) öncelenir.
⚠️ Literatürün kendi uyarısı da kayda değer: SpPin/SnNout kuralı naif
uygulandığında **güvenilir değildir** ve olabilirlik oranlarıyla değiştirilmesi
önerilmektedir.

➡️ Bizim kapımız da bir *«tarama»* aracıdır (ihlali kaçırmamak önceliklidir) ve
aynı uyarı bize de geçerlidir: **kapı bir tarama, hüküm değil.**

## E4. LLM değerlendirmesinde de yeni değil

*«Emin değilsen tedbirli davran ve işaretle»* yönergesi LLM-judge pratiğinde
yaygın bir kalıptır. ⛔ Yani asimetrik yönlendirme bu alanda da bilinmektedir.

## E5. ⛔⭐ Tasarımımız ALEYHİNE bir bulgu

Güvenlik judge'larının **tek yönlü tedbirli sapma** gösterdiği — yani ihlali
olduğundan çok işaretlediği — alan yazısında bildirilen bir eğilimdir. Bunun
sonucu bizim için doğrudan:

> ⛔ **Bizim ihlal sayılarımız ÜST SINIRDIR** ve asimetrimiz bu sapmayı
> **azaltmaz, aynı yöne ekler.**

⚠️ **Sayı verilmiyor:** arama özetinde geçen bir yanlış-pozitif/yanlış-negatif
oranı, iddia edildiği kaynakta **doğrulanamadı** ve bu belgeye **alınmadı**.
Bulgunun **türü** kayıtlı, **büyüklüğü** değil.

⛔ **Ve bizim ölçmediğimiz şey tam burada:** kapının yanlış pozitif oranı
ölçüldü (T58: 162/162 gerçek dayanak geçiyor), ama **judge'ın** yanlış pozitif
oranı **uzman kararına karşı** hiç ölçülmedi. Asimetriyi savunmak için o ölçüm
gerekir.

## E6. ⭐ Yan bulgu — T63'ün ölçtüğü şeyin literatürdeki adı: *policy invariance*

**Weng, Feng, Xie** — *Beyond Accuracy: Policy Invariance as a Reliability Test
for {LLM} Safety Judges* · arXiv:2605.06161 (7 Mayıs 2026). Değerlendirme
ölçütü **yeniden ifade edildiğinde** judge hükümleri **%9,1'e varan oranda**
değişiyor ve değişimlerin çoğu **belirsiz olmayan** vakalarda gerçekleşiyor
✅*doğrulandı*.

➡️ T63'ün *«hangi kol çiftinin ters döndüğü rubrik sürümüne bağlı»* bulgusu bu
özelliğin **bir örneği**. ⛔ T63'ün olgusu da özgün değil — ama ölçüsü (kesin
ters dönen çiftler, kesişim boş) bu çerçeveye **bağımsız** bir kanıt ekliyor.

## E7. ⛔ İkinci turun sonucu

| Kalem | Tarama öncesi | Tarama sonrası |
|---|---|---|
| Asimetrik doğrulama | ◐ *«şimdilik ayakta»* | ⛔ **kavram olarak ÖZGÜN DEĞİL** — hukuk · Neyman-Pearson · SpPin/SnNout · LLM pratiği |
| Ayakta kalan kırıntı | — | ◐ asimetrinin **judge'ın kendi alıntısına** ve **deterministik türetmeye** taşınması: dar bir mühendislik uygulaması, kavramsal katkı değil |
| T63 | ⭐ ölçüm | ◐ olgunun adı **policy invariance**; ölçüsü bağımsız kanıt |
| ⭐ **Yeni risk** | — | ⛔ asimetrimiz güvenlik judge'larının **bilinen tek yönlü sapmasına ekleniyor**; judge'ın uzmana karşı yanlış pozitif oranı **hiç ölçülmedi** |

➡️ *İkinci tur, birinci turun bıraktığı tek kalemi de aldı. Defterde kavramsal
katkı olarak ayakta kalan: **T51** (bulunamadı, iki sorgu) ve **T49/T50'nin
vaka katkısı**. Geri kalan her şey uygulama.*

---

# EK-2 — Türk hukuku (2026-09-16, üçüncü tur)

> ⚠️ **Yazan hukukçu değildir.** Aşağısı mevzuat metni ve ikincil kaynak okumasıdır,
> hukuki görüş değildir. Tezde kullanılmadan önce bir hukukçuya **okutulmalıdır**.

## E8. ⛔ E1'deki cümlem Türk hukuku için YANLIŞ

E1'de ABD ceza hukukunun **olumlu savunma** (affirmative defense) kurumuna bakıp
*«yapı birebir bizimki»* yazmıştım. ⛔ **Türk ceza muhakemesinde bu yapı yok.**

| | ABD (E1'de yazdığım) | Türkiye |
|---|---|---|
| İspat yükü | iddia makamında; **olumlu savunmada sanığa geçer** | ⛔ **hiçbir süjede değildir** — medeni muhakemenin aksine ceza muhakemesinde taraflara ispat yükü yüklenmez |
| Sanığın konumu | olumlu savunmayı **ispatla yükümlü** olabilir | ⛔ **suçsuzluğunu ispatla yükümlü değildir**; böyle bir yükümlülük getirilmesi mümkün görülmez |
| Mahkemenin rolü | taraf muhakemesi | ⭐ **re'sen araştırma ilkesi** — maddi gerçeği mahkeme arar |

➡️ **Düzeltme:** *«Muafiyeti ileri süren onu ispatlar»* yapısı **common law'a özgü**dür.
Türk ceza muhakemesinde muafiyet (hukuka uygunluk sebebi, kusurluluğu kaldıran hâl)
ileri sürüldüğünde de araştırma **mahkemenin** işidir. ⛔ T68'in *«yapı birebir»*
cümlesi bu yüzden **yalnızca ABD hukuku için** doğrudur.

## E9. ⭐⭐ Ama Türk hukukunda DAHA İYİ bir karşılaştırma var — ve yönü tam tersi

**Anayasa m.38/6:** kanuna aykırı olarak elde edilmiş bulgular delil olarak kabul
edilemez. Somutlaşması: **CMK m.206/2-a** (kanuna aykırı elde edilen delil
reddolunur) ve **CMK m.217/2** (yüklenen suç **hukuka uygun** elde edilmiş her
türlü delille ispat edilebilir).

⭐ Bu, bizim kapımızla **aynı türden** bir düzenek: *bir geçerlilik sınamasından
geçemeyen kanıt, hüküm kuramaz.* İkisi de kanıtın **içeriğine** değil
**geçerliliğine** bakar ve ikisi de deterministik bir kapıdır.

⛔ **Ama yön tam ters:**

| | Anayasa 38/6 · CMK 217/2 | BıRAG'ın kapısı |
|---|---|---|
| Geçersiz kanıt neyi kuramaz | **mahkûmiyeti** | **muafiyeti** |
| Kimi korur | **sanığı** | **kullanıcıyı** |
| Yanılma yönü | haksız mahkûmiyet daha pahalı | kaçırılmış ihlal daha pahalı |

➡️⭐⭐ *Türk anayasa hukuku, «geçerliliği sınanamayan kanıt hüküm kuramaz» kuralının
en sert biçimini zaten taşıyor — ve yönünü alanın kayıp işlevine göre seçmiş.
BıRAG'ın kapısı aynı kuralı **ters yöne** kuruyor ve gerekçesi de aynı biçimde
alan gereğidir (Kural 3). ➡️ Yani tezde savunulacak şey «asimetriyi biz bulduk»
değil, **«yönü neden böyle seçtik»**dir — ve o gerekçe yazılıdır.*

## E10. ⭐ *Şüpheden sanık yararlanır* — şüphenin yönü olduğunun kanonik ifadesi

Masumiyet karinesinin muhakeme hukukundaki karşılığı **in dubio pro reo**:
şüphe giderilemiyorsa **sanık lehine** karar verilir. ⛔ Bu, *«belirsizlik bir
tarafa yazılır»* ilkesinin en bilinen hukuki ifadesidir ve BıRAG'ın *«doğrulanamayan
muafiyet düşer»* kuralı onun **aynadaki görüntüsüdür**: bizde şüphe **kullanıcı
lehine** yazılır.

## E11. ⛔ Üçüncü turun sonucu

| | |
|---|---|
| ⛔ T68'in *«yapı birebir bizimki»* cümlesi | **yalnızca ABD hukuku için** doğru; Türk ceza muhakemesinde sanığa ispat yükü yüklenmez |
| ⭐ Daha iyi karşılaştırma bulundu | **Anayasa m.38/6 + CMK m.206/2-a, 217/2** — aynı tür kapı, **ters yön** |
| ⛔ Özgünlük | **değişmedi** — asimetri hâlâ özgün değil; ama karşılaştırma artık **Türk okuyucunun bildiği** bir kurala dayanıyor |
| ⭐ Tezde nasıl yazılmalı | *«asimetriyi biz bulmadık; **yönünü** biz seçtik ve gerekçesi Kural 3'tür»* |
| ⚠️ Güvenilirlik | kaynaklar ağırlıkla **hukuk bürosu yazıları** + bir DergiPark makalesi; ⛔ **hukukçu onayı gerekir** |

---

# EK-3 — İkinci tur: T146–T245 (2026-09-22, dördüncü tur)

> **Neden:** birinci tur (E1-E11) defterde **115 satır** varken yapıldı. Defter
> bugün **245** satır. Aradaki kayıtlar hiç taranmamıştı.
>
> **Kapsam ölçüldü:** aralıktaki **100** katkının **52**'si tarandı, **48**'i
> **taranmadı** — taranmayanların tek tek listesi ve kapsam sayıları
> `reports/analiz/2026-09-22-ozgunluk-ikinci-tur-kapsam.md`'de. Küme eşlemesi
> **editoryaldir** (Kural 6), türetilmedi.
>
> **Doğrulama imi:** ✅ kaynağın kendi sayfasından okundu · ⚠️ yalnız dizin
> kaydından (tam metin açılamadı). Doğrulanamayan hiçbir sayı bu belgeye girmedi.
>
> **On dört sorgu** §E24'te birebir yazılı — *«bulunamadı» ile «aramadım»*
> ayırt edilebilsin diye (T140'ın kuralı).

## ⛔ Özet — birinci turun sonucu yinelendi: daralma

| Küme | Ne iddia ediliyordu | Tarama sonucu |
|---|---|---|
| **Gürültü tabanı** (T159/T160/T241) | ölçütün gürültü tabanı **ölçütün** özelliğidir, koşunun değil | ⛔ **ÖZGÜN DEĞİL** — yayımlanmış, bizden ~5 ay önce |
| **Güç analizi** (T245) | koşu kendi ayırt etme gücünü ölçer | ⛔ **ÖZGÜN DEĞİL** — pilot → D-study |
| **Ön kayıtlı eşiğin yanlışlığı** (T245) | ilan edilmiş eşik **yanlış olabilir** ve koşu onu düzeltir | ◐ **ayakta** — kaynağa soruldu, yok |
| **Sıfır müdahale** (T159) | hiçbir şeyi değiştirmeyen müdahaleyle taban ölçümü | ◐ **daraldı** — komşusu var, tasarım farklı |
| **Tohum yayılımı** (T182/T183) | fark tohum gürültüsünün içinde kalabilir | ⛔ **DERS KİTABI** |
| **LoRA yayılımı ↔ güvenlik** (T187/T188) | belirleyici olan büyüklük değil **yayılım** | ⛔ **ÖZGÜN DEĞİL** — bütün bir hat var |
| **Sözlük kapısı → şablon** (T196/T201/T206) | kapı formülü zorunlu kılar, şablonu da | ⛔ **GOODHART** — adı konmuş |
| **«Alan dolu, değeri yanlış»** (T236/T237) | biçim denetimi değeri denetlemez | ⛔ **ADI VAR** — data cascade · silent defect |
| **Anotatör bağımsızlığı** (T227-T230) | aynı model ailesi uyumu yukarı çeker | ⛔ **YAYIMLANMIŞ** — kendi şerhimiz bir literatür |
| **Kapıyı denetleyen kopya** (T147/T151) | denetim kapının koşulunu kopyalıyor | ⛔ **TEST ORAKL SORUNU** |
| **Kapı bileşimi / aşırı red** (T189) | iki tutarlı kapı makul cevabı puanlanamaz kılıyor | ◐ **daraldı** — klinik yanlış pozitif literatürü var |
| **İç muhakemeyi cevaba karşı denetleyen KAPI** (T239) | üretim kabul kapısı olarak | ⭐ **bulunamadı** — olgu yayımlanmış, **kapı değil** |
| **Türkçe biçimbilim × sert güvenlik kapısı** (T153/T154) | çekim eki kapıyı deliyor | ⭐⭐ **bulunamadı** — iki literatür var, **kesişimi yok** |

---

## E12. ⛔⛔ GÜRÜLTÜ TABANI HATTININ ÇEKİRDEĞİ YAYIMLANMIŞ — VE YİNE BİZDEN ÖNCE

✅ **Messing, S. — «Hidden Measurement Error in LLM Pipelines Distorts Annotation,
Evaluation, and Benchmarking», arXiv:2604.11581** (ilk sürüm **13 Nisan 2026**,
v6 13 Mayıs 2026). Kaynağın kendi sayfasından okundu.

T159/T160/T241'in çekirdeği bu makalede duruyor:

| Bizim iddiamız | Makalede |
|---|---|
| *«gürültü tabanı ölçütün özelliğidir, koşunun değil»* | judge modeli · sıcaklık · prompt ifadesi **ayrı varyans bileşenleri**; *«design sensitivity»* ile *«sampling variance»* ayrılıyor |
| *«eski sayıların yarısı okunamaz hâle geldi»* (T159) | *«naive standard errors are 40-60% smaller than the TEE-corrected SE»* |
| *«bu koşu bir sonuç değil bir GÜÇ ANALİZİDİR»* (T245) | *«a small pilot recovers honest CIs and projects which design changes most improve precision»* — pilot → D-study izdüşümü |

➡️ **T159/T160/T241'in çekirdeği ve T245'in «güç analizi» katkısı tezde KATKI
değil, BAĞIMSIZ YENİDEN KEŞİF olarak yazılacak** — E1'de T43/T46 için verilen
hükmün aynısı. ⭐ Kuram adı da hazır: bu, **genellenebilirlik kuramının** (G/D
çalışması) LLM hattına uygulanmasıdır; tezde o adla anılmalı.

### ⭐ Ama bir şey soruldu ve yok

Kaynağa **ön kayıtlı eşik** soruldu: makale eşik *doğrulamasını* değil, tasarım
duyarlılığını ele alıyor — *«does not explicitly address pre-registered thresholds
or their re-derivation»*. ⇒ **T245'in asıl cümlesi ayakta:** *bir eşiğin önceden
ilan edilmiş olması onu doğru kılmaz; koşu kendi gürültüsünü ölçtüğünde ilan
DÜZELTİLİR.* ⚠️ Bu, klinik araştırmadaki **iç pilot / kör örneklem yeniden
kestirimi** kurumuna çok benziyor ve **o literatür bu turda aranmadı** (§E24).

## E13. ◐ SIFIR MÜDAHALE TASARIMI AYRI DURUYOR — AMA KOMŞUSU VAR

✅ **Khomiakov, M. & Frellsen, J. — «Noise-Response Calibration: A Causal
Intervention Protocol for LLM-Judges», arXiv:2603.17172** (17 Mart 2026).

Aynı soruyu soruyor (*«bu judge gerçekten ayırt ediyor mu»*) ama **ters
tasarımla**: aşamalı **gürültü EKLİYOR** ve bozulma eğiminin anlamlılığına
bakıyor. T159/T178'in tasarımı bunun tersidir — **hiçbir şeyi değiştirmeyen**
bir müdahale koşulur ve ölçütün yine de ürettiği fark taban sayılır.

⛔ **Ama özgünlük iddiası kurulmuyor:** çevrimiçi deney pratiğinde bu tasarımın
adı **A/A testi**dir ve ders kitabıdır; bulunamayan şey yalnızca *LLM-judge
hattına uygulanmış yayımlanmış bir örnek*. ⚠️ Tek sorgu ile arandı ⇒ **zayıf
negatif**; iddia edilmeden önce daha iyi aranmalı.

## E14. ⛔ TOHUM YAYILIMI DERS KİTABI — T182/T183/T245 BURAYA YASLANMALI

✅ **Bouthillier, X. ve ark. — «Accounting for Variance in Machine Learning
Benchmarks», MLSys 2021, arXiv:2103.03098.** Varyans kaynakları (veri örneklemesi,
ilklendirme, hiperparametre) ve *«corners are cut to reach conclusions»*.

✅ **Bui, N., Savova, G., Wang, L. — «Assessing the Macro and Micro Effects of
Random Seeds on Fine-Tuning Large Language Models», IJCNLP 2025, arXiv:2503.07329.**
**Makro** (toplam metrik) ve **mikro** (kayıt düzeyinde tutarlılık) ayrımı.

⭐ **Yan kazanç — T181'in adı buymuş:** *«aynı davranış öğeler arasında yer
değiştiriyor»* dediğimiz şey bu makalenin **mikro düzey tutarlılığı**dır;
toplam sabitken kayıt düzeyi oynar. T181 tezde **o adla** anılmalı.

## E15. ⛔ LoRA YAYILIMI ↔ GÜVENLİK: BİR HAT VAR, VE İÇİNDEYİZ

✅ **Hsu, C.-Y., Tsai, Y.-L., Lin, C.-H., Chen, P.-Y., Yu, C.-M., Huang, C.-Y. —
«Safe LoRA: The Silver Lining of Reducing Safety Risks when Finetuning Large
Language Models», NeurIPS 2024** (proceedings sayfasından okundu):
*«the projection of LoRA weights from **selected layers** to the safety-aligned
subspace»*. ⇒ **hangi/kaç modülün güncellendiği güvenlik kaybını yönetiyor** —
T187/T188'in mekanizması.

⚠️ Aynı hat (yalnız dizin kaydından): **SafeMERGE** arXiv:2503.17239 · **SPLoRA**
arXiv:2506.18931 · **SaLoRA** ICLR 2025 · **CSULoRA** arXiv:2605.30640.

⛔ **T187/T188 tezde «katkı» diye yazılamaz** — olsa olsa *bu hattın Türkçe
terapötik kriz davranışı üzerinde bir örneği*. ⛔ Zaten K226'nın kendi şerhi
kanıtı **çift post-hoc** ilan etmişti; şimdi özgünlüğü de düştü.

⭐ **Kaynağa soruldu, orada YOK:** Safe LoRA sayfası modül **sayısı** ile güvenlik
kaybı arasında nicel bir ilişki kurmuyor (*«no quantitative relationship between
the number of layers modified and the degree of safety degradation»*). ⇒ T188'in
**eşit enerji, farklı yayılım** doğal deneyi bir *ölçüm boşluğuna* denk geliyor
olabilir; ⛔ ama bizim n=8 kolluk, çift post-hoc kanıtımız onu doldurmaz.

## E16. ⛔ SÖZLÜK KAPISI → ŞABLON: BUNUN ADI GOODHART

T196'nın cümlesi (*«formülü zorunlu kılan kapı, şablonu da zorunlu kılar»*) ve
T201/T206 (*«şablonu azaltmak ölçümü gerileme gibi gösterir»*) **Goodhart yasasının**
sentetik veri üretimindeki hâlidir: ölçü hedef olunca ölçü olmaktan çıkar.

⚠️ (dizin kaydından) **Thomas, R. & Uminsky, D. — «The Problem with Metrics is a
Fundamental Problem for AI», arXiv:2002.08512** · sentetik veride çeşitlilik
çöküşü için **arXiv:2505.17390** (persona ile üretimde sözcüksel çeşitlilik ölçümü).

⇒ **Özgün olan iddia değil, olgunun bir ÜRETİM HATTINDA iki yönde birden
ölçülmüş olması** (T206: kapsama sözcük ölçüsü ↑, şablon dizi ölçüsü ↓). Bu bir
**vaka katkısı**dır, kavramsal katkı değil.

## E17. ⛔ «ALAN DOLU, BİÇİMİ DOĞRU, DEĞERİ YANLIŞ» — İKİ AYRI ADI VAR

✅ **Sambasivan, N., Kapania, S., Highfill, H., Akrong, D., Paritosh, P., Aroyo, L. M. —
«"Everyone wants to do the model work, not the data work": Data Cascades in
High-Stakes AI», CHI 2021** (Google Research sayfasından okundu). Tanım:
*«compounding events causing negative, downstream effects from data issues»* —
ve bu olaylar **görünmez ve gecikmeli** olarak niteleniyor; 53 uygulayıcı,
%92 yaygınlık.

✅ **Besanson, G. — «SARC-DQ: Runtime Data-Quality Gating for Agentic AI: Silent
Evidence Defects…», arXiv:2607.26313** (28 Temmuz 2026): *«a stale price or a
superseded record, **perfectly well-formed in the payload** and betrayed only by
freshness, lineage, or provenance»* + **eylem öncesi kapı** önerisi.

➡️ T236'nın vaka serisi (*«alan dolu, biçimi doğru, değeri yanlış»*) ve T237'nin
(*«kural yazılı, kapı yok»*) **teşhisi de çaresi de adlandırılmış.** ⛔ Tezde
katkı olarak değil, **yüksek riskli bir alanda belgelenmiş bir kaskad serisi**
olarak yazılmalı — ki bu Sambasivan'ın çağrısının tam olarak istediği şeydir.

⚠️ **Fark duruyor:** SARC-DQ'nun kusuru **tazelik/soy** kaynaklı; bizimki
**yazma anında** yanlış değer (T217: iki kayıt başka satırların tohumundan
yazıldı). Aynı sınıfın iki ayrı üyesi ⇒ örtüşme kısmi.

## E18. ⛔ ANOTATÖR BAĞIMSIZLIĞI: KENDİ ŞERHİMİZ ZATEN BİR LİTERATÜR

✅ **Panickssery, A., Bowman, S. R., Feng, S. — «LLM Evaluators Recognize and
Favor Their Own Generations», NeurIPS 2024, arXiv:2404.13076** (15 Nisan 2024):
*«a **linear correlation** between self-recognition capability and the strength
of self-preference bias»*.

T227-T230'un kendi şerhi (*«üç anotatörde de Claude; aynı model ailesinin ortak
yanlılığı uyumu yukarı çeker ⇒ bu bir bağımsızlık kanıtı DEĞİLDİR»*) doğruydu —
ve **bir olgunun adıdır.** ⛔ T229'un *«%100 tekrar güvenilirliği»* sayısı bu
yüzden **bağımsızlık değil, ailenin kendi kararlılığı** olarak okunmalı.

⚠️ Kaynağa soruldu: makale **aynı aile içi anotatörler arası** korelasyonu
doğrudan ele **almıyor** (kendi üretimini kayırma ile sınırlı) ⇒ *«aynı aile ⇒
şişmiş κ»* için **doğrudan atıf hâlâ yok**; ⚠️ arXiv:2601.02370
(*Variance-Aware LLM Annotation*) bu turda **açılmadı**, üçüncü tura kaldı.

## E19. ⛔ KAPIYI DENETLEYEN BETİK KAPININ KOPYASINI DENETLİYOR — TEST ORAKL SORUNU

T151 (*«denetim betiği sürüm koşulunu kopyaladı»*) ve T147 (*«denklik sınaması
dosyayı kendisiyle karşılaştırıp ✅ verdi»*) yazılım sınamasının kanonik
**test orakl sorunudur**: oraklın bağımsız bir belirtimden gelmesi gerekir,
sınanan gerçeklemenin kendisinden değil.

⚠️ **Barr, E., Harman, M., McMinn, P., Shahbaz, M., Yoo, S. — «The Oracle Problem
in Software Testing: A Survey», IEEE TSE 2015, DOI 10.1109/TSE.2014.2372785** —
⛔ **tam metin açılamadı** (IEEE 403, UCL kopyası erişilemedi); atıf yalnız dizin
kaydından. Tezde kullanılmadan önce **açılıp okunmalı**.

⇒ T147/T151 tezde **vaka** olarak durur; kavramsal katkı değildir.

## E20. ◐ KAPI BİLEŞİMİ VE AŞIRI RED — DARALDI

T189 (*«iki kapı, her biri kendi içinde tutarlı, birlikte klinik olarak makul bir
cevabı puanlanamaz kılıyor»*) klinik LLM literatüründe adlandırılmış bir
gerilimin örneğidir: koruma katmanları *«safety for safe helpfulness»* takası
yapar ve **iyi huylu klinik sorguları da bloke eder** (yüksek yanlış pozitif).

⚠️ Bu turda yalnız arama özetlerinden görüldü; hiçbir kaynak açılmadı ⇒ **atıf
verilmiyor**, yalnız yön kaydediliyor. Üçüncü turda XSTest ve aşırı-red ölçütleri
adıyla aranmalı.

⭐ **Ayakta kalan sivri uç:** T176/T177'nin sorusu bundan farklı ve daha keskin —
*korpusun tek otomatik klinik güvenlik kapısı, kuralın «puanlayan olamaz» dediği
judge'ın kendisidir.* Bu bir **yönetişim döngüselliği**dir, aşırı red değil, ve
bu turda **aranmadı**.

## E21. ⭐ İÇ MUHAKEMEYİ CEVABA KARŞI DENETLEYEN BİR *KAPI* — BULUNAMADI

Olgu yayımlanmış, hem de fazlasıyla:

- ⚠️ **Turpin ve ark., arXiv:2305.04388** — *«Language Models Don't Always Say
  What They Think»* (dizin kaydından)
- ⚠️ **arXiv:2503.08679** — *«Chain-of-Thought Reasoning In The Wild Is Not
  Always Faithful»* (dizin kaydından)
- ✅ **Young, R. J. — «Why Models Know But Don't Say: Chain-of-Thought Faithfulness
  Divergence Between Thinking Tokens and Answers in Open-Weight Reasoning Models»,
  arXiv:2603.26410** (27 Mart 2026): olgunun adı **thinking-answer divergence**;
  vakaların **%55,4**'ünde thinking'de olan ipucu cevapta hiç geçmiyor.

⭐ **Ama kaynağa soruldu ve yok:** Young **yalnız ölçüyor** — *«does not propose
using the reasoning channel as a filter or gate to accept/reject outputs»*.

➡️ **T239'un ayakta kalan kısmı şudur:** iç muhakeme–cevap sapmasını bir
**eğitim verisi kabul kapısı** olarak kullanmak (kaydın kendi thinking'i cevabın
yaptığını yapmadığını söylüyorsa kayıt düşer). ⛔ Bizde de **kapı yok** — T239
kapının yokluğunu kaydetti, kapıyı kurmadı ⇒ katkı **şimdilik bir öneridir**,
kurulup ölçülmeden iddia edilmemeli.

## E22. ⭐⭐ TÜRKÇE BİÇİMBİLİM × SERT GÜVENLİK KAPISI — İKİ LİTERATÜR VAR, KESİŞİMİ YOK

Aranan: Türkçe'nin eklemeli yapısının **düz alt dizge aramasıyla kurulmuş
güvenlik kapılarını** delmesi (T153: *«§15 taraması kip değişimini göremiyor»*;
T154: *«kökü ekle aramak, ekin ne olduğunu söylemeyi gerektirir»*; ve daha eski
`str.lower()` ailesi T73/T75/T84).

**Bulunan iki ayrı literatür:**
1. Türkçe biçimbilim ve NLP'de seyreklik — eklemeli yapı, bir fiilde 8-9 çekim
   ulamı, aynı anda 6 türetme eki, ünlü uyumu/ünsüz benzeşmesi kaynaklı yüzey
   değişimi (⚠️ dizin kayıtlarından: arXiv:1703.03200 · arXiv:2002.10416).
2. İçerik denetimi / güvenlik süzgeçleri — ama **Türkçe'ye özgü değil.**

⛔ **Kesişimi bulunamadı:** *«Türkçe çekim eki bir güvenlik kapısını deliyor»*
biçiminde yayımlanmış bir iş çıkmadı.

➡️ ⭐⭐ **Bu, ikinci turun en güçlü ayakta kalan kalemidir** — ve T1'in Türkçe
iddiasıyla aynı yere basıyor: alan Türkçe olduğu için kusur da Türkçe'ye özgü.
⛔ **Ama iddia bir turda kurulmaz:** tek sorgu ile arandı, Türkçe dizinler
(TR Dizin · YÖK Tez · ULAKBİM) **yine taranmadı** ⇒ iddia **ikinci bir tur
aranmadan yazılmamalı.**

## E23. ⭐ İKİNCİ TURUN SONUCU

| Kalem | Hüküm | Tezde nasıl yazılmalı |
|---|---|---|
| **Türkçe biçimbilim × sert kapı** (T153/T154 + T73/T75/T84) | ⭐⭐ ayakta | ⭐ katkı adayı; ⛔ Türkçe dizinler taranmadan **iddia edilmeyecek** |
| **İç muhakeme–cevap kapısı** (T239) | ⭐ ayakta, ama **kurulmadı** | öneri olarak; kapı kurulup ölçülürse katkı |
| **Ön kayıtlı eşiğin yanlışlığı** (T245) | ◐ ayakta | ⭐ katkı adayı; ⚠️ iç pilot literatürü aranmadı |
| **T176/T177 yönetişim döngüselliği** | ◐ **aranmadı** | üçüncü tur |
| Gürültü tabanı · güç analizi (T159/T160/T241/T245) | ⛔ düştü | **bağımsız yeniden keşif**; G/D kuramı adıyla |
| Tohum yayılımı (T181/T182/T183) | ⛔ düştü | ders kitabı; T181 = **mikro tutarlılık** |
| LoRA yayılımı (T184-T188) | ⛔ düştü | Safe LoRA hattının bir örneği |
| Sözlük kapısı → şablon (T196/T201/T206) | ⛔ düştü | **Goodhart**; vaka katkısı |
| «Değeri yanlış» serisi (T217/T236/T237) | ⛔ düştü | **data cascade** + silent defect; vaka katkısı |
| Anotatör bağımsızlığı (T227-T230) | ⛔ düştü | self-preference bias; şerh **doğruydu** |
| Kapı kopyası (T147/T151) | ⛔ düştü | **test orakl sorunu**; vaka |
| Kapı bileşimi (T189) | ◐ daraldı | klinik yanlış pozitif takası |

➡️ **Birinci turun dersi ikinci turda yinelendi:** *iddiayı DARALTMAK için yapılan
tarama bilgi üretir.* Bu turda **on kalem düştü ya da daraldı, üç kalem ayakta kaldı** ve
ayakta kalanların ikisi **Türkçe** ya da **alan** kaynaklı — kavramsal değil.
⭐ Bu, T1/T2'nin (Türkçe + alan) tezin gerçek omurgası olduğu yönündeki okumayı
**üçüncü kez** destekliyor.

## E24. ⛔ BU TURUN SINIRI

| | |
|---|---|
| ⛔ **Aralığın %48'i hiç taranmadı** | 100 kayıttan 48'i; listesi `reports/analiz/2026-09-22-ozgunluk-ikinci-tur-kapsam.md` §3 |
| ⛔ **On dört sorgu** | sistematik derleme değil; ACL/EMNLP/NeurIPS bildiri taraması yapılmadı |
| ⛔ **Türkçe dizinler yine taranmadı** | TR Dizin · YÖK Tez · ULAKBİM — E22'nin iddiası **buna bağlı** |
| ⛔ **Sekiz kaynak açıldı, gerisi dizin kaydından** | ✅/⚠️ imleri hangisinin hangisi olduğunu söylüyor |
| ⛔ **Üç kaynak hiç açılamadı** | IEEE TSE 403 · UCL kopyası erişilemedi · ACM DL 403 |
| ⛔ **Aranmayan iki hat ilan ediliyor** | (a) iç pilot / kör örneklem yeniden kestirimi (E12) · (b) T176/T177 yönetişim döngüselliği (E20) |
| ⭐ **Yön dürüst tutuldu** | tarama **daraltmak** için yapıldı ve daralttı; lehte çıkan üç kalemin ikisi Türkçe/alan kaynaklı |

**Aranan on dört sorgu (2026-09-22), birebir:**

```
1  null intervention A/A test measuring noise floor of an evaluation metric machine learning seed variance
2  random seed variance fine-tuning LLM minimum detectable effect accounting for variance in machine learning benchmarks
3  "A/A test" OR "sham intervention" OR "placebo intervention" evaluation pipeline LLM detect metric variance before claiming effect
4  Bouthillier "Accounting for Variance in Machine Learning Benchmarks" how many seeds detectable difference
5  LoRA target module placement which layers safety alignment degradation fine-tuning breaks safety adapter spread vs rank
6  "Safe LoRA" NeurIPS 2024 projecting LoRA weights safety subspace which layers selected arXiv
7  number of LoRA target modules breadth of adaptation more modules worse safety forgetting same update magnitude concentrated vs distributed
8  lexical keyword gate causes template collapse synthetic data generation Goodhart's law metric becomes target LLM generated training data homogenization
9  LLM annotators same model family correlated bias inflates inter-annotator agreement self-preference bias LLM evaluators recognize own generations
10 schema validation checks field presence not correctness silent metadata corruption data cascades high-stakes AI Sambasivan
11 test that duplicates the implementation logic tautological test self-fulfilling oracle problem software testing verifying a copy of the gate not the gate
12 composing two safety guardrails each internally consistent makes a clinically appropriate response unscoreable over-refusal conflicting constraints mental health LLM evaluation
13 Turkish agglutinative morphology defeats substring keyword matching safety filter content moderation suffix inflection missed matches
14 chain-of-thought faithfulness reasoning does not match final answer no gate audits reasoning against answer Turpin language models don't always say what they think
```

---

# EK-4 — Üçüncü tur: ikinci turun bıraktığı 48 kayıt (2026-09-22, beşinci tur)

> **Evren türetildi:** ikinci turun (§EK-3) taranmamış bıraktığı **48** kayıt,
> betik tarafından o raporun §3'ünden **okundu** — elle kopyalanmadı.
> **15'i tarandı, 33'ü hâlâ taranmadı.** Sayılar ve liste:
> `reports/analiz/2026-09-22-ozgunluk-ucuncu-tur-kapsam.md`.
> T146-T245 aralığının toplam kapsamı **%67** (52 + 15).
>
> **Doğrulama imi:** ✅ kaynağın kendi sayfasından okundu · ⚠️ yalnız dizin kaydından.
> **On sorgu** §E33'te birebir yazılı; küme sayısı **sekiz**.

## ⛔ Özet

| Küme | Ne iddia ediliyordu | Sonuç |
|---|---|---|
| **Çeşitlilik ölçütünün tabanı** (T146) | `distinct_n` kısa metinde *«ölçülemez = temiz»* diyor | ⛔ **ÖZGÜN DEĞİL** — ACL 2022, üstelik **hazır düzeltmesiyle** |
| **Etiket bayatlaması** (T156/T171/T240) | metin düzeltilince yargı geçersizleşir; alanın anlamı kayar | ◐ **daraldı** — adlandırılmış, ama hakemli kaynak açılmadı |
| **Kayıp mekanizması** (T179) | kaybın rastgeleliği kayıttan anlaşılmaz | ⛔ **DERS KİTABI** — Rubin'in MAR/MNAR ayrımı |
| **Erken tespit** (T218) | değer *ne zaman* bulunduğunda | ⛔ **DERS KİTABI** + alanımıza birebir bir bildiri |
| **Yakın-tekrarın yeri** (T231) | tehlikeyi örtüşmenin **yeri** söyler | ◐ **daraldı** — ⚠️ zayıf negatif |
| **Alıntıda vurgu düşmesi** (T168) | model tırnağa alırken vurgu ögesini atıyor | ⭐⭐ **AYAKTA** — iki literatür var, **kesişimi yok** |
| **Örtük eşik** (T208/T210) | eşiği söylemeyen ölçütün eşiğini uygulayan koyar | ⛔ **YAYIMLANMIŞ** — RIPD + rater drift |
| **Okunmayan sinyal** (T152/T195/T209/T213) | hatırlatma kapı değildir | ⛔ **ALARM YORGUNLUĞU** — kanonik |

---

## E25. ⛔ ÇEŞİTLİLİK ÖLÇÜTÜNÜN UZUNLUK YANLILIĞI — VE BİZ ONU TERS UÇTAN GÖRDÜK

✅ **Liu, S., Sabour, S., Zheng, Y., Ke, P., Zhu, X., Huang, M. — «Rethinking and
Refining the Distinct Metric», ACL 2022, arXiv:2202.13587.** Kaynağından okundu:
Distinct-n'in *«evident biases that tend to assign higher penalties to longer
sequences»* kusuru var; önerilen düzeltme **EAD** (*Expectation-Adjusted Distinct*),
*«scaling the number of distinct tokens based on their expectations»*.

T146 aynı yanlılığı **kısa uçtan** gördü: ~24 kelimenin altında `distinct_5` zaten
1,000 döndürüyor ⇒ *«ölçülemez»* sessizce *«temiz»* diye okunuyor.

⚠️ **Dürüstlük şerhi:** kaynağa soruldu ve **kısa metinde şişme** açıkça
doğrulanmıyor — makale uzun uç yanlılığını anlatıyor. İkisi aynı eğrinin iki ucu
ama *«makale bizim gördüğümüzü de söylüyor»* denemez.

➡️ ⭐ **Asıl kazanç özgünlük değil, çözüm:** T146 *«kural uzunluk koşullu olmalı»*
diye bir öneri bırakmıştı; literatürde **uzunluk-düzeltilmiş bir ölçüt zaten var**
(EAD, ve `PATTR`). ⇒ Öneri yeniden icat edilmeyecek, **EAD denenecek.**

## E26. ◐ ETİKET BAYATLAMASI — ADI VAR, HAKEMLİ KAYNAĞI BU TURDA AÇILMADI

T156 (*«bir metin düzeltmesi ona verilmiş yargıyı da geçersiz kılar»*), T171
(*«elle verilmiş hüküm verildiği metne bağlıdır»*) ve T240 (*«`slice` alanının
anlamı v5 ile v6 arasında sessizce değişti»*) endüstri pratiğinde adlandırılmış
üç olgudur: **annotation schema drift** · **ontology versioning** · **label
provenance** (hangi satır, ne zaman, **hangi rubrik sürümüne** karşı etiketlendi).

⚠️ **Bu turda hiçbir hakemli kaynak açılmadı.** Bulunan tek hakemli aday —
*«Analyzing Dataset Annotation Quality Management in the Wild»*, **Computational
Linguistics 50(3)** — okunmadı. ⛔ Bu yüzden **atıf verilmiyor**, yalnız yön
kaydediliyor ve dördüncü tura bırakılıyor.

⭐ **Ayakta kalabilecek ince uç:** T156'nın *«ve bu İLAN EDİLEBİLİR bir şeydir»*
kısmı — yani düzeltilen metnin yargısını **kayıtta bayat işaretlemek**. Endüstri
kaynakları *«effective_from tarihi sakla»* diyor; bizimki **yargıyı bayat ilan
eden bir alan**. Fark ince, ⛔ ve aranmadan iddia edilmeyecek.

## E27. ⛔ KAYIP MEKANİZMASI — T179'UN CÜMLESİ RUBIN'İN KURAMI

T179: *«bir örneklem kaybının rastgele mi olduğu kaydın özelliklerine bakarak
anlaşılmaz — kayıp boru hattının özelliğinden doğabilir.»*

Bu, **Rubin ve Little**'ın kayıp veri sınıflandırmasının (MCAR / MAR / MNAR)
doğrudan sonucudur ve kanonik biçimi şudur: **MAR ile MNAR ayrımı gözlenen
veriden sınanamaz** — hangi rejimin geçerli olduğu verinin dışında, *mekanizma
bilgisiyle* savunulur.

⇒ ⛔ **T179 tezde katkı değil, doğru uygulama olarak yazılmalı** — ve doğru terimle:
*«kaybın MCAR olduğu gösterilemez; boru hattı MNAR üretiyor olabilir.»*
⚠️ Kaynaklar ders kitabı düzeyinde tarandı; Rubin 1976 açılmadı.

## E28. ⛔ ERKEN TESPİT — HEM DERS KİTABI HEM DE ALANIMIZA BİREBİR BİR BİLDİRİ

T218 (*«bir ölçümün değeri bulduğu şeyde değil, ne zaman bulduğundadır»*):

- ⚠️ **Boehm, B. — *Software Engineering Economics* (1981)** ve **Boehm & Basili,
  *Software Defect Reduction Top 10 List*, IEEE Computer, Ocak 2001** (dizin
  kaydından): teslimden sonra düzeltmek, gereksinim/tasarım aşamasında
  düzeltmekten ~**100 kat** pahalı; küçük projelerde oran ~5:1.
- ✅ **Kothari, S. ve ark. — «Position: Early-Stage Quality Assurance in Annotation
  Pipelines Is More Cost-Effective Than Late-Stage Validation», arXiv:2605.15714**
  (15 Mayıs 2026, kaynağından okundu): *«errors caught before annotation begins
  cost a fraction of those discovered after review cycles complete»*; yazılım
  yazınından **4-100×** çarpan aktarılıyor.

⇒ ⛔ **T218 özgün değil** — ve ikincisi **tam bizim alanımızda** (anotasyon hattı),
dört ay önce. ⭐ Tezde bu bir **doğrulama**dır: bizim *«otuz kayıt yerine on kayıt
sonra»* gözlemimiz o bildirinin savunduğu konumun ölçülmüş bir örneği.

## E29. ◐ YAKIN-TEKRARIN YERİ — DARALDI, AMA NEGATİF ZAYIF

Yakın-tekrar ve bulaşma literatürü geniş: ⚠️ **Lee ve ark., arXiv:2107.06499**
(*Deduplicating Training Data Makes Language Models Better*; **tam alt dizge
eşlemesi** örneğin yalnız bir **parçasının** tekrarlandığı durumları buluyor) ·
⚠️ **arXiv:2311.04850** (*Rethinking Benchmark and Contamination … Rephrased
Samples*; n-gram'ın kaçırdığı başka-sözcüklü aynı-yapı vakaları).

⛔ T231'in çerçevesi — *«tehlikeyi örtüşmenin **büyüklüğü** değil **YERİ** söyler»* —
bu biçimde bulunamadı; ama *«parçanın hangi parça olduğu»* fikri Lee ve ark.'ın
alt dizge yaklaşımının içinde zımnen var. ⚠️ **İki sorgu ⇒ zayıf negatif**;
iddia edilmeyecek.

## E30. ⭐⭐ ALINTIDA VURGU DÜŞMESİ — İKİ LİTERATÜR VAR, KESİŞİMİ YOK

T168: *model kullanıcının cümlesini tırnağa alırken, cümlenin **vurgusunu taşıyan
ögeyi** atıyor.*

**Bulunan iki ayrı hat (ikisi de ⚠️ dizin kaydından):**
1. **Alıntı sadakati** — *Mind the Quote: Enabling Quotation-Aware Dialogue in
   LLMs* (arXiv:2505.24292) · *Verifiable by Design: Aligning Language Models to
   Quote from Pre-Training Data* (arXiv:2404.03862). İkisi de **alıntının
   kaynağında bulunup bulunmadığıyla** ilgileniyor.
2. **Türkçe edim belirleyicileri** — `yani` · `işte` · `şey` · `ya` · `hani` ·
   `zaten` üzerine yerleşik bir edimbilim yazını var.

⛔ **Kesişimi bulunamadı:** *«model alıntılarken edim/vurgu ögesini düşürüyor»*
biçiminde yayımlanmış bir iş, iki farklı sorguda da çıkmadı.

➡️ ⭐⭐ **Bu, E22 ile aynı yere basan ikinci Türkçe kalemdir** ve ondan daha
keskindir: E22 bir **kapının** Türkçe'yi göremediğini söylüyor, E30 **modelin
kendisinin** Türkçe'de bir anlam taşıyıcısını attığını. ⛔ **Ama aynı şerh:**
iki sorgu, Türkçe dizinler **yine taranmadı**, ve olgunun dile özgü mü yoksa
genel bir işlev-sözcüğü düşmesi mi olduğu **ayrıştırılmadı** — İngilizce muadili
aranmadan iddia edilmeyecek.

## E31. ⛔ ÖRTÜK EŞİK — RUBRİĞİN YÖNLÜ KAYMASI YAYIMLANMIŞ

✅ **Ding, R., Pang, Y., Sun, H., Wang, Y., Wu, Z. S., Deng, Z. — «Rubrics as an
Attack Surface: Stealthy Preference Drift in LLM Judges», arXiv:2602.13576**
(14 Şubat 2026; v2 14 Eylül 2026). Olgunun adı **RIPD** (*Rubric-Induced
Preference Drift*): ölçüt düzenlemeleri kıyas sınamasını geçse bile hükümlerde
**sistematik ve yönlü** kayma üretiyor — hedef alanda doğruluk **%9,5**
(helpfulness) ve **%27,9** (harmlessness) düşüyor.

T210 (*«ölçüt eşiğini söylemiyorsa, eşiği uygulayan koyar»*) ve T208 (*«devralınan
şerh devralan bağlamda sessizleşir»*) bunun **insan/uygulayıcı tarafıdır**; insan
değerlendirmesinde karşılığı **rater drift**tir.

⚠️ İnce fark duruyor ve kayda geçiyor: RIPD **rubriğin değiştirilmesinin** kayma
ürettiğini gösteriyor; T210 **hiç değişmeyen ama eşiksiz** bir rubriğin uygulayıcıyı
ölçütün yerine geçirdiğini. ⛔ Ayrı bir iddia kuracak kadar değil.

⭐ **Kullanılabilir sonuç:** T210'un *«altı kez üst üste aynı yöne karar verdim»*
gözlemi, RIPD'nin ölçtüğü **yönlülüğün** bizim hattımızdaki karşılığıdır ve
tezde o adla anılmalı.

## E32. ⛔ OKUNMAYAN SİNYAL — ALARM YORGUNLUĞU

T152 (*«okunmayan bir sinyal, sinyal değildir»*), T213 (*«ön tarama yalnız
işaretlediği satırı okutur»*), T209 (*«hatırlatma değil kapı gerekir»*) ve
T195 (*«kayıt kayıt denetim, eksik kaydı göremez»*):

⚠️ (dizin kaydından) Statik çözümlemede uyarıların **%35-91**'i yanlış pozitif ve
sonuç **alert fatigue**: geliştirici uyarılara duyarsızlaşıyor (arXiv:2604.18525,
*Towards Better Static Code Analysis Reports…*). Tıpta karşılığı **alarm fatigue**
olarak kanoniktir. T209'un *«hatırlatma değil kapı»* çözümü ise **shift-left /
pre-commit enforcement**tir — kodun girdiği yere koy, teslim kapısına değil.

⇒ ⛔ Dördü de **vaka** olarak durur. ⭐ T195'in ucu (*«denetim eksik kaydı göremez»*)
alarm yorgunluğundan farklı — o bir **yokluk körlüğü**dür — ⛔ ama bu turda
ayrıca aranmadı.

## E33. ⛔ BU TURUN SINIRI

| | |
|---|---|
| ⛔ **48'in 33'ü hâlâ taranmadı** | okuyarak verilen hüküm: ağırlıkla depoya özgü mühendislik/vaka kayıtları — ⚠️ **bu bir okuma, ölçüm değil** |
| ⛔ **On sorgu, sekiz küme** | sistematik derleme değil |
| ⛔ **Hakemli kaynak açılmadan bırakılan iki hat** | E26 (Computational Linguistics 50(3)) ve E27 (Rubin 1976) |
| ⛔ **Türkçe dizinler ÜÇÜNCÜ kez taranmadı** | E30 ve E22'nin ikisi de buna bağlı |
| ⚠️ **İki zayıf negatif** | E29 (iki sorgu) ve E30 (İngilizce muadili aranmadı) |
| ⭐ **Evren türetildi** | 48'lik liste ikinci turun raporundan **betikle okundu**, elle kopyalanmadı |

**Aranan on sorgu (2026-09-22), birebir:**

```
1 distinct-n diversity metric length bias short texts returns 1.0 unreliable below threshold n-gram repetition detection
2 annotation becomes stale when underlying text is edited label provenance invalidate judgments dataset versioning semantic drift of a field between versions
3 missing data mechanism MCAR MAR MNAR cannot be determined from observed record attributes missingness arises from the pipeline not the data
4 cost of a defect depends on when it is detected shift left testing Boehm curve earlier detection cheaper empirical evidence
5 near-duplicate train test contamination what matters is where the overlap falls not how much n-gram overlap deduplication benchmark leakage location
6 duplicate training examples danger depends on which span overlaps not overlap size same seed two records differ only in the behaviour-bearing part
7 LLM quoting user text drops function words particles when placing in quotation marks verbatim quote fidelity failure extractive quote alters emphasis
8 paraphrase omits function words discourse particles emphasis loss agglutinative language quotation extraction fidelity Turkish "bile" "de da" pragmatic marker dropped
9 rubric without explicit threshold the rater supplies it implicit cutoff annotator drift same direction repeatedly criterion underspecified
10 warnings nobody reads alert fatigue static analysis unactioned findings a reminder is not a gate enforcement must block not notify
```

---

# EK-5 — Dördüncü tur: Türkçe dizinler (2026-09-22, altıncı tur)

> **Neden bu tur:** üç tur boyunca *«Türkçe dizinler taranmadı»* diye ilan edildi
> ve **ayakta kalan iki kalemin ikisi de** (E22/T153, E30/T168) tam buna bağlıydı.
> Bu tur o borcu ödemeye çalıştı — **kısmen ödedi.**
>
> **Doğrulama imi:** ✅ kaynağından okundu · ⚠️ dizin kaydından.
> Altı sorgu §E38'de birebir.

## ⛔ Özet — ayakta kalan kalemlerden biri daraldı, biri güçlendi

| Kalem | Dördüncü turun sonucu |
|---|---|
| **E22 / T153-T154** — Türkçe çekim eki sert kapıyı deliyor | ⛔ **DARALDI** — Türkçe içerik denetiminde **kök eşleme** hem pratikte hem akademik olarak yerleşik |
| **E30 / T168** — alıntıda vurgu ögesinin düşmesi | ⭐ **Türkçe tarafta da bulunamadı** — ayakta |
| **T1** — Türkçe, bağımlılık alanına özgü terapötik veri seti | ⭐⭐ **BOŞLUK DOĞRULANDI VE KANITI GÜÇLENDİ** |
| **YÖK Tez · TR Dizin · ULAKBİM** | ⛔ **ERİŞİLEMEDİ** — borç kapanmadı, ama artık **nedeni** belgeli |

---

## E34. ⛔ TÜRKÇE BİÇİMBİLİM × KAPI: KÖK EŞLEME ZATEN STANDART

E22 *«iki literatür var, kesişimi yok»* demişti. **Türkçe kaynaklara bakılınca
kesişim çıktı** — hem de tam bizim kusurumuzun çözümü olarak.

⚠️ **Üslup** (`github.com/EgeSoft1/uslup`, kaynağından okundu) — cihaz üzerinde
çalışan Türkçe nezaket katmanı. Sözlük eşleştirme satırı birebir şöyle:
*«Türkçe eklemeli yapı: kök eşleşmesi»*; normalleştirme örnekleri
(`$3r3fsiz`→`serefsiz`, `aptaaaal`→`aptal`) düz alt dizge eşlemesinin neden
yetmediğini gösteriyor. ⛔ **Akademik değil** — hiçbir kaynağa atıf yok, bir
sosyal inovasyon yarışması işi.

⚠️ **Akademik taraf da var:** **SemEval-2020 Task 12 (OffensEval)** beş dilde
saldırgan dil tespiti yaptı ve **Türkçe** o beş dilden biriydi; Türkçe
*«morphologically rich language requiring language specific segmentation
techniques»* olarak anılıyor. Türkçe korpus (**OffensCorpus**, 36.232 tweet,
Nis 2018–Eyl 2019) ve `SU-NLP` gibi Türkçe takım bildirileri var.

➡️ ⛔ **E22'nin *«kesişim yok»* hükmü YANLIŞTI ve geri alınıyor.** *«Türkçe
eklemeli yapı düz eşlemeyi deler, kök/biçimbirim farkında eşleme gerekir»*
Türkçe içerik denetiminde **bilinen ve çözülmüş** bir sorundur.

### ⭐ Ayakta kalan ince uç — ve neden ince

T153/T154'ün kusuru saldırgan dil **tespiti** değil: kapı **modelin kendi
çıktısında klinik bir kuralı** uyguluyordu ve bulunan şey kapının
**kuralı uygulayan cümlenin kendisini silmesiydi** (yanlış pozitif, doğru
davranışı yok ediyor).

⚠️ Bunun kuzeni **pratikte belgeli**: nefret söylemi süzgeçlerinde korunan
grubun adını yasak listeye koymak geri teper ve korumak istediği grubu
susturur. ⛔ **Akademik kaynak bulunamadı** ve ⛔ bizim vakamız klinik bir
kuralda; ⇒ kalem **◐**'e iner: *vaka katkısı olabilir, kavramsal katkı değil.*

## E35. ⭐ ALINTIDA VURGU DÜŞMESİ — TÜRKÇE TARAFTA DA BULUNAMADI

T168 için Türkçe kaynaklarda arandı. Çıkanların tamamı **Türkçe öğretimi ve
özetleme pedagojisi** (ders kitaplarında özetleme etkinlikleri, öğretmen
adaylarının dinlediğini özetlemesi) ve **otomatik özetleme yöntemleri**;
*modelin alıntılarken vurgu taşıyan ögeyi düşürmesi* üzerine bir iş **yok**.

➡️ ⭐ **T168 dördüncü turdan da sağ çıktı** ve artık **üç ayrı yönde** arandı:
İngilizce alıntı sadakati · Türkçe edimbilim · Türkçe özetleme.
⛔ **Ama hâlâ eksik olan aynı sınama:** olgunun **dile özgü mü** yoksa genel bir
işlev-sözcüğü düşmesi mi olduğu **ölçülmedi**. İngilizce muadili koşulmadan
*«Türkçe'ye özgü»* denemez — bu artık bir **deney borcudur**, tarama borcu değil.

## E36. ⭐⭐ T1'İN BOŞLUĞU DOĞRULANDI — VE EN İYİ KANITI BİR TÜRK ÇALIŞMASI

✅ **Türk, M. N., Akın, R., Şahin, D. Ö., Demirci, S. — «Büyük Dil Modellerinin
Ruh Sağlığı Uygulamaları İçin Performans ve Tutarlılık Analizi», Black Sea
Journal of Engineering and Science, 9(3), Mayıs 2026,
DOI 10.34248/bsengineering.1913122** (kaynağından okundu).

Bulduğumuz **ilk Türkçe LLM × ruh sağlığı** çalışması. Dokuz model (GPT-4o,
GPT-3.5 Turbo, Claude, Gemini, LLaMA 3.3 ve diğerleri) aynı koşullarda
karşılaştırılmış; GPT-4o en yüksek anlamsal başarım (COMET 0,7277).

⭐⭐ **Ama üç şey tam bizim boşluğumuzu çiziyor:**

| | |
|---|---|
| Veri | **İngilizce** Kaggle *«Mental Health FAQ for Chatbot»* — **Türkçe veri kümesi yok, yayımlanmamış** |
| Alan | **Bağımlılık yok** |
| Ölçülen | **bilgi ve tutarlılık** — *«generated responses were compared with reference answers»*; **davranış/terapötik duruş değil** |

➡️ ⭐⭐ **`benzer-calismalar.md` §6'nın 2. boşluğu (*«Türkçe tıp NLP'si bilgi
ölçüyor, davranış ölçmüyor»*) artık ruh sağlığı alanında da doğrudan kanıtlı** —
ve kanıt bir varsayım değil, Türk yazarların 2026 tarihli çalışması.
⛔ Bu **T1'i özgün yapmaz**, ama boşluğun **var olduğunu** gösterir; T1 zaten
*«boşluk»* iddiasıydı, *«kimse denemedi»* değil.

## E37. ⛔ YÖK TEZ · TR DİZİN · ULAKBİM — ÜÇÜNCÜ KEZ TARANAMADI, AMA ARTIK NEDENİ BELGELİ

| | |
|---|---|
| **YÖK Ulusal Tez Merkezi** | `tez.yok.gov.tr` arama ekranı **oturum gerektiriyor**; arama motorları tez **içeriğini** indekslemiyor ⇒ dışarıdan taranamıyor |
| **TR Dizin · ULAKBİM** | doğrudan sorgulanamadı |
| **DergiPark** | ⭐ **açık ve tarandı** — E36 oradan çıktı |

➡️ ⛔ Borç **kapanmadı** ama niteliği değişti: bu bir **arama** eksiği değil
**erişim** eksiğidir ve çözümü üniversite ağıdır. ⚠️ Tezde sınırlılık olarak
böyle yazılmalı; *«aranmadı»* demek artık yanlış olur, *«erişilemedi»* doğrudur.

⭐ **Yan envanter (⚠️ dizin kayıtlarından):** Türkçe LLM ekosisteminde
**Mukayese** (arXiv:2203.01215) · Türkçe dil modelleri başarım karşılaştırması
(arXiv:2404.17010) · Türkçe verisetleriyle eğitim ve ince ayar (arXiv:2306.03978)
· **TurkEmbed4Retrieval** (arXiv:2511.07595) var — **hiçbiri klinik değil**,
`benzer-calismalar.md` §1'in Cetvel bulgusunu destekliyor.

## E38. ⛔ BU TURUN SINIRI

| | |
|---|---|
| ⛔ **Altı sorgu** | sistematik derleme değil |
| ⛔ **YÖK Tez / TR Dizin / ULAKBİM erişilemedi** | E37 |
| ⚠️ **E34'ün kanıtının bir ayağı akademik değil** | Üslup bir yarışma projesi, atıfsız |
| ⛔ **OffensEval Türkçe bildirileri açılmadı** | yalnız görev tanımı ve dizin kaydı okundu |
| ⛔ **T168 için artık tarama değil DENEY gerekiyor** | İngilizce muadili koşulmadan «Türkçe'ye özgü» denemez |
| ⭐ **Bir hüküm geri alındı** | E22'nin *«kesişim yok»*u yanlıştı; tarama kendi önceki turunu düzeltti |

**Aranan altı sorgu (2026-09-22), birebir:**

```
1 dergipark.org.tr Türkçe bağımlılık madde kullanımı doğal dil işleme yapay zeka veri seti çalışma
2 YÖK Ulusal Tez Merkezi yüksek lisans tezi Türkçe psikolojik destek sohbet robotu büyük dil modeli ince ayar veri kümesi
3 Türkçe küfür hakaret içerik denetimi filtre eklemeli yapı çekim eki kaçırma normalizasyon sorunu makale
4 Turkish offensive language detection OffensEval 2020 Turkish subtask morphology-aware normalization inflection suffix stemming dataset academic
5 Türkçe özetleme metin üretimi sadakat kaybı edim belirleyici vurgu ögesi düşmesi değerlendirme çalışması dergipark
6 Türkçe ruh sağlığı psikolojik danışma diyalog veri kümesi bağımlılık AMATEM yapay zeka model tez dergipark akademik çalışma
```

---

# EK-6 — E30/E35'in kalemi kontrol deneyiyle düştü (2026-09-22)

> Bu ek bir **tarama turu değildir.** E30 ve E35 T168'i *«ayakta kalan kalem»*
> ilan etmiş ve borcunu *«tarama değil DENEY»* diye bırakmıştı. Deney koşuldu
> (**T252**, K269) ve kalemi **literatür değil kendi kontrolü** düşürdü.

## E39. ⛔⛔ T168 — «ÜSLUP» İDDİASI KURULAMADI

**Ön kayıt üretimden önce mühürlendi** (`configs/deney/2026-09-22-t168-ingilizce-kontrol.yaml`,
commit `07ce8d8`): 2×2 tasarım (dil × öge türü), hüküm kuralları ve **ayırt etme
gücü** önceden ilan edildi.

| | |
|---|---:|
| Öge | 96 (iki tur × 48) |
| Sayılan fırsat | **37** |
| Düşme | **1** (%2,7) |
| `tr_klitik` ↔ `en_klitik` | Fisher **p = 1,00** |

➡️ ⛔ **Ön kayıtlı hüküm mekanik uygulandı:** *«dört hücre de düşük ⇒ olgu
yeniden üretilemedi.»*

### ⭐⭐⭐ Asıl bulgu sonuç değil, iddianın yapısı

T168 *«21 bulgu → 16'sı tek örüntü»* diyordu. Bu bir **oran değil**: kapının
**işaretlediği kümenin** betimlemesidir ve **paydası hiç hesaplanmamıştı.**
Kontrol paydayı sağladı ve taban oran düşük çıktı.

> ➡️ *Bir kapının bulgularını okuyup «hepsi aynı örüntü» demek, o örüntünün
> yaygın olduğunu göstermez — yalnız kapının ne yakaladığını gösterir.*

⚠️ **Kurulamayan şey ORAN iddiasıdır**, olgunun varlığı değil: kontrol üretim
istemini (`uretim-v5`, 455 satır) kullanmadı, tek model ailesinde koştu ve n
küçüktü ⇒ olgu **üretim koşullarında hâlâ olabilir.**

## E40. ⭐ Özgünlük tablosunun bugünkü hâli

| | |
|---|---|
| Kavramsal katkı iddiaları | ⛔ **hepsi düştü** — dördü tarama, sonuncusu (T168) **kendi deneyi** ile |
| T1/T2 — Türkçe + bağımlılık alanı **boşluğu** | ⭐⭐ **ayakta ve artık kanıtlı** (§E36) |
| T49/T50 · T168'in **vaka** ucu | ⭐ vaka katkısı olarak durur |

➡️ ⭐⭐⭐ *Beş turun ve bir deneyin ortak sonucu: **bu tezin özgünlüğü bir yöntem
iddiasında değil, bir ALAN ve DİL boşluğunda.** Yöntem tarafında söylenebilecek
şey «bağımsız yeniden keşif» ve «vaka»dır.*
