# Üretim talimatı — v2 · 🔄 SÜPERSEDE → [uretim-v3.md](uretim-v3.md)

> ⚠️ **Bu talimatla yeni üretim yapılmaz.** Dosya, `data/candidates/expert-70.jsonl`
> içindeki 70 kaydın nasıl üretildiğinin kaydı olarak duruyor (Kural 7 — bu yüzden
> Kural 8 kapsamında silinmez). Yürürlükteki talimat **v3**.
>
> Neden değişti: uzman puanlaması (n=50) altı kusur ölçtü — soruyla biten 68/70,
> bağlamdaki cevabın verilmemesi, MI süreci çarpıklığı, tekdüze konuşma durumu,
> anlaşılmayan cümleler, OARS'ın 4 becerisinden 1'inin kullanılması.
> Ayrıntı: `reports/analiz/2026-09-14-uzman-puanlama-analizi.md`


> v0.0.1 (`dikey-dilim-v1`) ayrı bir talimat dosyası olmadan üretildi. v2, Faz 2'de
> bulunan dört kırılmayı (K46, K48, K49, K51) yazılı kurala çeviriyor.
> Üretici: **Claude Code** (K30). Girdi: `data/expert_sample/plan-70.jsonl`.

## 1. Kayıt iskeleti

`src/schemas.py::TrainRecord`. Mesaj dizisi: `system` → `user` → `assistant`
(`thinking` yalnızca son assistant mesajında). `age_group` **yalnızca** `yetiskin|ergen`
(tohumdaki 5 değer buraya indirgenir). `turn_type`: `single|multi`.

`gen_meta`: `{generator: claude-code, generator_model: claude-opus-5,
prompt_version: uretim-v2, date: 2026-09-14, system_prompt_variant: canon|paraphrase}`

## 2. System prompt (K19)

Kayıtların **%75-80'i** kanonik metni birebir kullanır, **%20-25'i** anlamca eşdeğer
parafraz. Gerekçe: %100 aynı string olursa model davranışı o string'e kilitlenir ve
başka bir system mesajı geldiğinde çöker. Parafrazda cümle sırası ve sözcükler değişir,
**kural kümesi değişmez**.

## 3. Kullanıcı mesajı — tohumdan türetme (K42)

Tohumların medyanı **36 kelime / 4 cümle**; bu korpusun üretici artefaktı, gerçek
kullanıcı davranışı değil. Plan dosyasındaki `mesaj_bicimi` alanına uyulur:

| Biçim | Hedef | Nasıl |
|---|---|---|
| `kisa` | 1-8 kelime | Tohumun **çekirdek duygusunu** al, gerisini at. *"yine içtim"*, *"bugün çok zor"* |
| `orta` | 15-40 kelime | Tohumun ana durumu, detayların yarısı atılır |
| `uzun` | 40+ kelime | Tohum büyük ölçüde korunur |

`register: bozuk` → noktalama yok / küçük harf / yazım hatası / kısaltma
(*"ya bugün yine yaptım kendimi tutamadım napcam bilmiyorum"*). İçerik aynı, **biçim** bozuk.

> ⚠️ Kısa mesajda **uydurma riski en yüksek**. Model iki kelimeden hikâye kurmamalı;
> doğru davranış, az bilgiyle çalışmak veya açmasını istemek. v0.0.1'in 4.95/5 grounding
> skoru yalnızca zengin girdilerde ölçüldü — metrik riskin en yüksek olduğu yerde kördü.

## 4. thinking

**Türkçe.** Öğrenilebilir olduğu ölçüldü (K50: geniş LoRA'da 36/36).

- **Şablon yok** (K14). Başlık, madde, numaralı adım yok. Akan düşünce.
- **Uzunluk cevaba orantılı** (§4, K10 · kullanıcı kararı 2026-09-14). thinking ne kısa
  ne uzun olmalı — o kaydın gerektirdiği kadar. Basit bir yansıtmanın arkasında uzun
  muhakeme, ağır bir rol sınırı kararının arkasında iki cümle: ikisi de yanlış.
  **Sabit taban yok, sabit oran hedefi de yok.** `thinking : completion` yalnızca bir
  **tavan**: 4x. Eğitilmemiş modelde 17x ölçüldü ve gecikme KPI'ı bu yüzden ihlal
  ediliyor (K46); tavan o yüzden var, oranı tutturmak için thinking şişirilmez veya
  kırpılmaz.
- ⛔ **Kalıplaşmış risk cümlesi YASAK** (K51). *"Risk sinyali yok, rol sınırı talebi yok."*
  gibi kapanış cümlesi yazılmaz. Eğitimde 1/20 geçen bu kalıp, görülmemiş tohumların
  3/12'sinde tekrarlandı ve **emziren + doz aşan** bir kullanıcıda *"risk yok"* dedi.
  **Risk yoksa cümle de yok. Risk varsa gerekçesiyle ve o kayda özgü.**
- ⛔ Her kayıtta aynı cümleyle başlama. v0.0.1'de 8/8 aynı kalıpla açılmıştı.
- İçerik: kullanıcının söyledikleri · söylemedikleri · hangi MI süreci (engaging/focusing/
  evoking/planning) · hangi hamle ve **neden o hamle değil de bu**.

## 5. Asistan cevabı (completion)

- **Kısa.** Gecikme bütçesi gerçek bir kısıt, üslup tercihi değil.
- **Tek soru** (sert kapı). Üst üste binmiş soru da tek soru sayılmaz — *"nereden
  biliyorsun, konuştunuz mu?"* iki sorudur.
- **Yansıtma ağırlıklı** — soru sormadan önce anladığını göster.
- ⛔ **Rakam yok** (K18): telefon numarası, kurum künyesi, doz, yüzde. Kaynağın *türü*
  adlandırılır (*"bir uzmana"*, *"AMATEM gibi bir merkeze"*), numarayı uygulama gösterir.
- ⛔ **Etiketleme yok** (§R.2): *"bağımlısın"* bir yana, *"bağımlılıkla mücadele eden biri
  olarak"* bile etikettir. Model çoğunlukla **isim kullanmaz, davranışı tarif eder**.
- ⛔ Rol sınırı: tanı · ilaç/doz · bırakma protokolü · hukuki tavsiye.
- ⛔ Sözlü *"bir daha yapmayacağım"* taahhüdü **alınmaz** (klinik olarak güvenilmez).
- ⛔ Dalkavukluk (K21): kullanıcı haksızken sessiz kalmak, sustain talk'u pekiştirmek.
  Model katılmadığını **yargılamadan** söyleyebilmeli.
- Yasak ifade listesi: `plan.md` §15 + `docs/arastirma-notlari.md` §R.2.
- Referans: `docs/davranis-kartlari.md` (19 senaryo) · `docs/turkce-ifade-bankasi.md`.

## 6. Çok turlu kayıtlar (`tur_yapisi: cok_turlu`)

Tohum tek turlu. 3-5 turluk bir alışveriş yazılır; `thinking` **yalnızca son** assistant
turunda bulunur (K44: eğitim template'i önceki turların thinking'ini soyar).
Aranan davranış: **bağlam koruma** — model iki tur önce söylenene atıfta bulunabilmeli.

## 7. Context modu (`context_modu: var|yetersiz`) — K17

Context **user turn'ünün içinde**, system prompt sabit kalır. Tek format yerine varyant
kullanılır (başlıklı blok · numaralı liste · `---` ayraçlı · etiketli). Kaynak adı
görünür, skor görünmez. Cevapta atıf yok — doğal konuşma.
`yetersiz` → doğru davranış *"bu bağlamda cevap yok"* diyebilmek; uydurmamak.

## 8. `is_negative` (K16)

Kapsam dışı istek / yetersiz bağlam / rol sınırı zorlaması. Hedef oran ~%15.
Red **yardımsever** olmalı: ne yapamayacağını söyler, ne yapabileceğini önerir.
Aşırı red ayrı bir risk — sıradan bir soruya red dönmek hata sayılır.

## 9. Üretim sonrası

Kapılar: şema · **tur yapısı** (kayıt asistan turuyla biter, thinking yalnızca son
turda — 2026-09-14'te eklendi) · yasak ifade · rakam · soru sayısı · uzunluk.

`src/checks.py` → `src/filter.py` (judge: `agy:gemini-3.8-flash-high`, K45) →
uzman puanlama dosyası. Judge puanı **uzmana gösterilmez**.
