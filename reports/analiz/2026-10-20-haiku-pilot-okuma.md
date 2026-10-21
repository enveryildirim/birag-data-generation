# Haiku pilotu — okuma raporu (60 kayıt)

- Tarih: 2026-10-20 · Okuyan: Claude Code (Opus 5.5), K260 rejimi
- Plan: `data/plan/haiku-pilot.jsonl` (`scripts/analiz/2026-10-20-haiku-pilot-plan.py`, rapor `2026-10-20-haiku-pilot-plan.md`)
- Taslaklar: `data/candidates/haiku-pilot.taslak.blok{1,2,3}.jsonl` — yazar `claude-haiku-5-5`
  (Claude Code alt ajanı, brif `prompts/haiku-taslak-brifi.v1.md`), blok başına bir ajan, paralel
- Kapı: `scripts/analiz/2026-10-20-haiku-pilot-birlestir.py` · şablon sayımı: `2026-10-20-haiku-pilot-sablon.md`
- ⛔ Okuma **tek okuyucu** (K30'un bilinen sınırı); hükümler aşağıda kayıt kayıt yazılı ki yeniden okunabilsin.
- ⛔ **Revizyon YAPILMADI.** Bu rapor ham taslağın kusur oranını ölçer; kayıtlar korpusa girmedi.

## 1. Mekanik kapı

| blok | taslak | geçti | ret | ret sebebi |
|---|---:|---:|---:|---|
| 1 | 20 | 18 | 2 | #8 #10 — güvenlik sapması (§5a′) `turn_ending`i soruya çevirdi, betik plan değerini bekliyor |
| 2 | 20 | 20 | 0 | — |
| 3 | 20 | 17 | 3 | #41 #48 #58 — aynı sebep |

⭐ Beş reddin beşi de **betiğin eksiği**, kaydın değil: v5 §5a′ *«beyan `acik_uclu_soru`ya çevrilir»* diyor
ve betik sapma beyanında `turn_ending`in değişmesine izin vermiyor. Düzeltilecek.
⇒ Haiku mekanik kapıları **pratikte tamamen** geçiyor (ajanlar sınamayı kendileri koştu, 0–2 düzeltme turu).
Blok thinking/cevap oranları 1,25 · 1,17 · 1,19 (hedef 1,20 ± 0,20).

## 2. Okuma — kusur sınıfları

Kusur «ciddi» sayıldıysa kayıt bu hâliyle korpusa giremez.

| sınıf | kayıtlar | n |
|---|---|---:|
| **A. Tohum sızıntısı** — cevap/thinking, kırpılmış konuşmada OLMAYAN tohum ayrıntısına dayanıyor (v5 §3a′) | #1 #5ᵗ #14 #16 #24 #34 #41 #49 #55 #58 #59 | **11** |
| **B. Yanlış okuma** — kullanıcının söylediğini ters/yanlış aktarıyor | #15 #19 #32 | 3 |
| **C. Bağlam sınıfı ihlali** | #3 (pasaj durumla ilgisiz, `cevap_var` diye uygulanmış) · #50 (`izin_iste`: bilgiyi döküp sonra izin istiyor) | 2 |
| **D. İskele sızıntısı cevaba** — «bunu adlandırıyorum», «adıyla anıyorum» | #20 · (#25 #32 hafif) | 1 (+2) |
| **ciddi kusurlu kayıt (tekil)** | | **17 / 60** |

ᵗ yalnız thinking'de.

**A sınıfının en ağır örnekleri:**
- #58 — cevap *«emzirirken bu ilacı kullanıyor olman»* diyor; konuşmada emzirme YOK (tohumda var). Yönlendirmenin gerekçesi bu ayrıntı.
- #14 · #55 — kullanıcıya yazmadığı cümle *«yazdın / yazmışsın»* diye atfediliyor.
- #34 — kırpılmış mesaj yalnız *«Pazar gecesi uykum yok. Bu benim sorunum mu?»*; cevap bağımlılık danışma merkezine yönlendiriyor — alkol konuşmada hiç geçmiyor.
- #41 — thinking kullanıcıya *«kadın»* diyor; cinsiyet konuşmada yok.

**B sınıfı:**
- #32 — *«Annen öldükten sonra iki yıl içmemişsin»* — sıra ters (iki yıl ayıktı, anne öldü, sonra başladı).
- #19 — kullanıcı sevgilisi için *«haksız da değil»* diyor; cevap *«kendi haksızlığını kabul etmek mi»* diye soruyor. Thinking cevapla çelişiyor (*«onun elinde değil»* ↔ *«karar sende»*).
- #15 — *«son dönemde hep kuponla döndüm»* → *«bu sabah kuponla eve dönüşlerin»*.

## 3. Okuma — doğru olanlar

- **§5a″ sapmaları yerinde ve gerekçeli:** #8 (nefes), #10 (yardım isteği), #12 #30 #31 #36 (reçeteli ilaç kararı),
  #32 #37 #59 (titreme / dalma), #48 (alkol + ilaçla acil). Hiçbirinde sapma gereksiz değildi.
  ⚠️ Ama #58'in sapması A sınıfı sızıntıya dayanıyor.
- İlaç markası ve doz sayısı kullanıcı turlarından da temizlenmiş (Xanax → «sakinleştirici», Concerta → «reçeteli ilaç», 1 mg → «küçük bir miktar»).
- Kurum özel adı asistan turunda yok; YEDAM/AMATEM kullanıcı turunda da genelleştirilmiş.
- Temiz ve iyi kayıtlar: #11 #21 #23 #39 #42 #44 #45 #47 #48 #56 #60.

## 4. Şablon

`2026-10-20-haiku-pilot-sablon.md`: çok turlu kayıtların **%84**'ü ara turu «Dinliyorum / Buradayım» ile açıyor
(parti8 %10). «… adım gibi duruyor» %18 (parti8 %1), «… duyuyorum» %17 (%0), «hüküm / bana düşmez» %20 (%1).
8 sözcüklük kapı bunların hiçbirini görmüyor.

⚠️ Kıyas zemini adil değil: parti8 **revize edilmiş** metin (ve v0.1.1'de thinking'i yeniden kurulmuş);
burada ham taslak sayılıyor. Yön yine de açık.

## 5. Hüküm

- Ham taslakta ciddi kusur **17/60 (%28)**; en büyük sınıf (**11**) tohum sızıntısı — projenin en tehlikeli
  hata sınıfı (uydurulmuş dayanak) ve hiçbir mekanik kapı onu görmüyor.
- ⭐ A sınıfı **yapısal**: taslak yazarı tohumu görürken cevabı da yazıyor. v5 §3a′ *«mesaj yazıldıktan sonra
  tohum kapatılır»* diyor; tek ajanda bu bir talimattır, iki ajanda bir **yapı** olur.
- ⇒ Haiku bu hâliyle «okumayı örneklemeye indir» rejimine **uygun değil**: her dört kayıttan biri okuma olmadan
  korpusa kusurlu girer.
