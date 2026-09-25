# RAG kaynak haritası — A katmanı öncelikli

> **Rol:** `plan.md` §17'nin kaynak tarafı (R2 çıktısı). Karar belgesi: hangi kaynak,
> hangi katman, hangi lisans, **hangi soruyu kapatıyor.**
> **Onay kapısı:** yürütücü (lisans/telif) · uzman (B katmanı kesiti, Kural 3)
> **Durum:** 2026-09-15 · **A1 + A2 ÇEKİLDİ** — 7 sayfa, 23 chunk, `data/rag/a-katmani/`
> · telifli kitaplar elendi (§5) · sonuç: [A katmanı pilotu](../reports/analiz/2026-09-15-rag-a-katmani-pilot.md)

Dayanak ölçümler:
[R0 envanteri](../reports/analiz/2026-09-15-rag-mevcut-korpus-envanteri.md) ·
[R1 soru envanteri](../reports/analiz/2026-09-15-rag-soru-envanteri.md) ·
[klinik-iddia kapısı](../reports/analiz/2026-09-15-klinik-iddia-kapisi-gercek-metin.md)

---

## 0. Üç katman — nerede duruyoruz

| Katman | Ne | Toplama | Sıradaki iş |
|---|---|---|---|
| **A** yordam/kurum | başvuru · gizlilik · ücret · uygunluk · kurum farkı · TCK 191/3 yordamı | ⛔ **yok** | §3'teki satırların çekilmesi |
| **B** klinik/psikoeğitim | MI · BDT · nüks · çarpıtma | ✅ **141 belge** | tasnif + negatif alan ayıklaması + Türkçe dönüşüm |
| **C** deneyim/dil | blog · tanıklık · forum · video | ✅ 24 blog | RAG havuzuna **girmez**; kullanıcı register'ı (K42) |

---

## 1. Hedef soru listesi — haritanın kapatması gereken şey

R1 dar eleğinden çıkan, **dış bilgi gerektiren** sorular. Haritanın başarı ölçütü bu
liste; belge sayısı değil.

| # | Soru (korpustan birebir) | Kim cevaplar | Belge türü | Durum |
|---|---|---|---|---|
| S1 | *"Bir şey soracağım, siz aileme söylemezsiniz değil mi bunu?"* | YEDAM · AMATEM | gizlilik politikası | ⛔ kaynak yok |
| S2 | *"…kayıt aileme gider mi, ileride işe girersem sicilime düşer mi?"* | kurum + adli sicil mevzuatı | kayıt/gizlilik yordamı | ⛔ kaynak yok |
| S3 | *"…söylersem dosyama işlenir mi bilmiyorum"* | kurum | kayıt tutma yordamı | ⛔ kaynak yok |
| S4 | *"Kurumsal sigortamız davranışsal sağlık notlarını görüyor mu?"* | — | — | ⚠️ **geçersiz, aşağıya bak** |
| S5 | *"Bir daha AMATEM'e gitsem yine boş çıkar mı?"* | AMATEM | başvuru/kabul yordamı | ⛔ kaynak yok |
| S6 | *"Aile hekimine gitmeyi düşündüm ama oraya 'içki yüzünden' diye nasıl giderim?"* | ASM / aile hekimliği | sevk ve başvuru yolu | ⛔ kaynak yok |
| S7 | *"Bu test pozitif çıkarsa … denetimli serbestlik dosyam çok kötü etkilenir"* | Denetimli Serbestlik Md. | TCK 191/3 yükümlülük metni | ⛔ kaynak yok |
| S8 | *"Avukata gidilecek bir şey mi bu?"* | — (rol sınırı) | — | ✅ belge gerekmez: model hukuki tavsiye vermez, yönlendirir |

> ⚠️ **S4 Türkiye sisteminde karşılıksız.** Tohum metni *"kurumsal psikologla görüşeceğim…
> EAP üzerinden… kurumsal sigortamız davranışsal sağlık notlarını görüyor mu"* diyor —
> bu bir **ABD işveren sigortası** çerçevesi. Ölçüldü: 2.240 tohumda bu tür işaret
> **16 tohum (%0,7)** — dar bir artefakt, korpus geneli değil. Ama S4 için **çekilecek
> belge yoktur**; doğru model davranışı §7a'nın `yetersiz` dalıdır.
>
> **Kural:** hedef soru listesine giren her satır, önce *"Türkiye'de bunun bir kurumsal
> karşılığı var mı"* denetiminden geçer. Yoksa belge aranmaz, `yetersiz` örneği yazılır.

---

## 2. Arşivde olan — tasnif kararı

`birag-tubitak/3005-Bagımlılık-Knowledge-base` · 171 belge · 420 MB
Çalışma listesi: [`…-mevcut-korpus-envanteri.tsv`](../reports/analiz/2026-09-15-rag-mevcut-korpus-envanteri.tsv) (246 satır)

| klasör | belge | dil | katman | karar |
|---|---|---|---|---|
| `türkce/YOK_TEZ` | 104 | tr | B | **Öncelik 1 — dokunulmamış ve Türkçe-özgün.** Aşağıdaki 6 satır A'ya yakın |
| `ingilizce/Makale` | 30 | en | B | Öncelik 3 — çeviri riski (K90), İngilizce kalırsa retrieval dili bozar |
| `türkce/Blog` | 24 | tr | C / B | **Havuza girmez.** Register malzemesi olarak ayrılır |
| `ingilizce` | 7 | en | B | Öncelik 3 — terapist el kitabı; dolaylı, üstelik §3'e göre *davranış* bizim tarafımız |
| `türkce` (kök) | 6 | tr | B | Öncelik 2 — kumar kitabı ve klinik görüşme metni |
| `md_rag_ressources` | 74 | en | B | ⚠️ **olduğu gibi kullanılmaz** — `(Page 2)` artığı, sözcük başına satır kırılması, kitap başına tek dosya, **lisans alanı yok** |

### ⭐ A katmanına yakın altı tez — ikincil kaynak

Tez başlıkları kurumsal ve hukuksal sistemi anlatıyor; **A katmanının ikamesi değil ama
kurum haritasını Türkçe-özgün metinle besleyebilir:**

```
858857  Madde bağımlılığıyla mücadele: Kurumsal ve hukuksal yöntemler
560098  Türkiye'de madde bağımlılığı ile mücadelede uygulanan sosyal politikaların analizi
794059  Madde bağımlılığının tedavisi ve mücadele politikaları — Türkiye ve ABD örnekleri
839242  Uyuşturucu ve uyarıcı madde bağımlılığı ile mücadele stratejileri
936603  Uyuşturucu madde bağımlılığı ve mücadele stratejisi — Türkiye ve Azerbaycan örneği
585922  Sosyal politika boyutu ile madde bağımlılığı sorunu
```

⚠️ **İki sınır.** (1) Tez kurum **hakkında** yazar, kurumun **kendi** yordam metni değildir;
*"kayıt aileme gider mi"* sorusunu bağlayıcı biçimde cevaplayamaz. (2) **Tazelik**: tez
tarihi sabittir, mevzuat değişir → `gecerlilik_tarihi` tez tarihi olarak yazılır.
Sayı prefiksi YÖK tez numarasıdır; künye doğrulanabilir.

---

## 3. Çekilecek — A katmanı *(onay bekliyor)*

⛔ **Hiçbiri çekilmedi.** Bu tablo onay içindir; satır satır işaretle.

⚠️ URL sütunu: yalnızca **repoda kayıtlı** adresler yazıldı (`docs/arastirma-notlari.md`
kaynakçası). Kalanlar `doğrulanacak` — adres uydurmuyorum.

| # | Kurum | Kapattığı soru | Beklenen belge | URL | Öncelik |
|---|---|---|---|---|---|
| A1 ✅ | **YEDAM / Yeşilay** | S1, S3 | danışan gizliliği · başvuru yordamı · ücret · randevu | `yedam.org.tr` — tedavi merkezleri sayfası kayıtlı: `/bagimlilik-tedavi-merkezleri`; gizlilik/başvuru sayfaları **doğrulanacak** | **1** |
| A2 ✅ | **YEDAM / Yeşilay** | kurum haritası | YEDAM nedir, AMATEM'den farkı, kimler başvurabilir | doğrulanacak | **1** |
| A3 | **ALO 191** | kriz/yönlendirme yordamı | hattın kapsamı, kimler arayabilir, gizlilik | doğrulanacak | 2 |
| A4 | **AMATEM / ÇEMATEM** | S5, S6 | başvuru, kabul, yataklı/ayaktan, yaş sınırı | hastane bazında dağınık — **temsilci bir üniversite hastanesi seçilecek** | 2 |
| A5 | **Denetimli Serbestlik Md.** | S7 | TCK 191/3 yükümlülük ve süreç metni | resmî mevzuat tercih edilir; repodaki kayıt bir **avukatlık blogu** (`kultavukatlik.com.tr/tck-191-3/`) — ⚠️ ikincil, bağlayıcı değil | 2 |
| A6 | **SBB** | kurum haritası | Bağımlılıkla Mücadele ÇG Raporu — kayıtlı PDF | `sbb.gov.tr/…/Bagimlikla-Mucadele-CG-Raporu_01082025.pdf` | 3 |

**Pilot kararı (K101):** A1 + A2 ile başlanır. Gerekçe: STK, erişimi açık, yayımlanmış
yordam metni var, §7b-2'nin *"yordam/erişim/gizlilik/uygunluk/sınır cümlesi"* tanımıyla
birebir uyuşuyor.

---

## 4. Havuza girmeyecekler

```
NEGATİF ALAN (§17.3) — girdi kapısı
  doz · ilaç adı · detoks/bırakma protokolü
  telefon numarası / rakam                     (K18)
  DSM/ICD tanı kriteri madde listesi
  hukuki tavsiye cümlesi                       (yordam metni EVET, tavsiye HAYIR)

C KATMANI — 24 blog + video/podcast/forum
  grounding'e girmez; kullanıcı register'ı ve senaryo tohumu için ayrılır
```

⚠️ **Mevcut malzemede negatif alan zaten var:** `turkce/alkol/1.md` (Yeşilay sayfası,
temiz Türkçe) yoksunluk belirtileri, *"6-8 saat sonra"* zaman çizelgesi ve *"ölüm riski"*
içeriyor. Kaynağın kurumsal olması içeriği meşrulaştırmıyor.

---

## 5. Lisans ve KVKK

| Katman | Örnek | Not |
|---|---|---|
| Kurumsal kamuya açık | YEDAM sayfaları, SBB raporu | Kaynak künyesi zorunlu; ticari kullanım ayrıca sorulmalı |
| Akademik açık erişim | YÖK tezleri | YÖK tez numarası künyeye yazılır; erişim kısıtlı tezler **alınmaz** |
| Telifli kitap | `ingilizce/` terapist el kitapları | ⛔ **KARAR 2026-09-15: HAVUZA GİRMEZ.** Telifli · İngilizce · üstelik içerdiği şey *davranış*, o da §3'e göre İP2'nin tarafı. Arşivde durur, RAG'e alınmaz |
| Kullanıcı üretimi | forum, yorum | KVKK — C katmanı zaten havuza girmiyor |

Her chunk şu alanları taşır (§17.4): `kaynak_url · alinma_tarihi · gecerlilik_tarihi ·
lisans · icerik_hash · belge_id`. **`lisans` boş bırakılamaz**; bilinmiyorsa `belirsiz`
yazılır ve o chunk pilota alınmaz.

---

## 6. Onay kapısı

- [ ] **Yürütücü** — §3 tablosunda çekilecek satırlar · §5 telifli kitap kararı
- [ ] **Uzman** — B katmanı kesiti (Kural 3) · negatif alan listesi eksiksiz mi
- [ ] **Teknik** — `context_ok` §7b-2 gerçek pasaja ayrılmadan (R3) hiçbir chunk kapıdan geçmez
