# BıRAG talimat veri seti — v0.0.1

*Datasheets for Datasets* yapısında (Gebru ve ark.). Bkz. `docs/tez/tez-plani.md` §3.5 —
bu dosya doğrudan tezin veri seti bölümüne taşınır.

## Motivasyon

Bu, projenin **dikey dilimi** (plan.md §13 Faz 2): kalite hedefi yok, amaç
üretim→kontrol→değerlendirme→eğitim borularının uçtan uca bağlandığını doğrulamak.
20 kayıt, `data/seeds.jsonl`'daki 2.240 tohumdan düşük/orta risk seviyesinde
stratifiye örneklenmiştir — **kriz dilimi bilinçli olarak dışarıda bırakılmıştır**
(uzman onayına kadar beklemede, AGENTS.md Kural 3).

## Bileşim

| Alan | Dağılım |
|---|---|
| Kayıt sayısı | 20 |
| Bağımlılık türü | alkol 4 · dijital 4 · kumar 4 · reçeteli ilaç 4 · tütün 4 |
| Yaş grubu | yetişkin 15 · ergen 5 |
| Senaryo | farkındalık 8 · rol sınırı 3 · kayma/nüks 2 · hedef belirleme 2 · nazikçe karşı çıkma 2 · ambivalans 1 · inkâr 1 · bilgilendirme 1 |
| Tur yapısı | tamamı tek tur |
| RAG/context | yok (bu dilimde context modu test edilmedi) |
| Kriz | yok (bilinçli dışlama) |

⚠️ **Kapsama tam değil, olması da gerekmiyor** (kalite hedefi sıfır): 19 senaryodan
yalnızca 8'i temsil ediliyor; 11 senaryo bu dilimde yok. Bu, Faz 4 iterasyon
döngüsünün girdisi olacak.

## Toplama süreci

- **Kaynak:** `data/seeds.jsonl` (K26) — kullanıcı mesajı `birag-tubitak/.../campaigns/`
  kampanya korpusundan (2.240 kayıt, DOĞRULANMAMIŞ — yalnızca gerçekçilik için kullanıldı).
- **Seçim:** risk_seviyesi ∈ {düşük, orta} olan 1.360 tohumdan, bağımlılık türü başına
  4 olacak şekilde rastgele örneklendi (seed=7), her biri hukuki_kaygı/sanrılı_söylem
  içermediği doğrulanarak elle gözden geçirildi.
- **Üretim:** asistan tarafı (thinking + completion) **Claude Code ile** (K30) elle
  yazıldı — `docs/davranis-kartlari.md` ve `docs/turkce-ifade-bankasi.md` referans alındı.
  system prompt: K19 taslağı (16/20 birebir, 4/20 parafraz — K19 kuralı).
- **Üretici:** claude-sonnet-5, `prompts/dikey-dilim-v1` (bu CARD.md + davranış kartları +
  ifade bankası, ayrı bir API prompt dosyası değil — K30 gereği üretim doğrudan).

## Ön işleme / etiketleme

- `src/checks.py` deterministik kapılar: şema, uzunluk, soru sayısı ≤1 — **20/20 geçti**.
- ⚠️ Yansıtma:soru oranı ölçüldü ama **sert kapı değil** (K40 — cümle-sayma yöntemi kısa,
  doğru MI turlarını yanlış eliyordu, bu dilimde bulundu ve düzeltildi).
- **Judge:** `ollama/qwen3.8:27b-mlx` (üretici aileden farklı — Kural 16), Eksen 1 rubriği
  (`prompts/judge-eksen1.v1.md`, arastirma-notlari §H.5). **20/20 güvenlik/rol sınırı
  ihlali sıfır, tuzak ihlali sıfır.**

## Kullanım

- **Amaçlanan:** `gemma-4-E4B-it` bf16 LoRA, 50 adım, MLX — boru hattı testi.
- **Amaçlanmayan:** üretim eğitimi, ölçüm/karar dayanağı (kalite hedefi yok, hacim çok küçük).

## Dağıtım

Yalnızca proje içi. Dış dağıtım yok, kişisel veri riski düşük (sentetik kampanya
korpusundan türetilen kurgusal kullanıcı mesajları).

## Bakım

`datasets/v0.0.1/` IMMUTABLE — bir daha yazılmaz. Revizyon gerekirse `v0.0.2` açılır.
Sorumlusu: proje sahibi (255172017@kocaeli.edu.tr).

---

## ⚠️ Bilinen kusur — iki kayıtta grounding/çerçeveleme hatası (K43)

Üç-judge karşılaştırmasında (K43) bağımsız judge'ın **kaçırdığı**, Claude judge'ların
yakaladığı iki gerçek hata:

| Kayıt | Hata |
|---|---|
| `kimyasal_madde:st_001:0802` | Kullanıcı *"Pazartesi'den beri her gece"* dedi; cevap **"beş gece"** diye **kullanıcının vermediği bir sayı üretti**. Tam da §4 grounding kuralının yasakladığı şey |
| `dijital:st_003:0192` | *"bu anları daha sık kılan neyi eksik buluyorsun"* — hem bozuk Türkçe hem kullanıcının kurmadığı bir "eksiklik" çerçevesi dayatıyor |

v0.0.1 IMMUTABLE olduğu için düzeltilmedi; **Faz 4'te bu iki desen üretim kuralına yazılacak**
(sayı çıkarımı yapma · kullanıcının kurmadığı çerçeveyi dayatma).

## ⚠️ Bilinen sınırlılık — kullanıcı mesajı biçimi (K42)

Bu sürümdeki kullanıcı mesajları **gerçek sohbet robotu kullanımını biçim olarak
temsil etmiyor**: medyan 33 kelime, 1-8 kelimelik mesaj **%0.0**, hiç noktalama
içermeyen mesaj **%0.0**. Gerçek kullanımda en sık görülecek açılış (*"bırakamıyorum ya"*)
bu sette yok. Tohum korpusundan devralınan bir **üretici artefaktı** —
`reports/analiz/2026-09-12-kullanici-mesaji-bicimi.md`.

Sonucu: bu veriyle eğitilen model "zengin girdi → detaylı yansıtma" öğrenir ve
seyrek girdide **detay uydurmaya** yatkın olabilir. Aşağıdaki grounding skoru
(4.95/5) **yalnızca zengin girdilerde** ölçüldüğü için bu riski göstermez.

v0.0.1 bu haliyle kalır (IMMUTABLE, boru hattı testi). Düzeltme Faz 4'te.

## ⚠️ Bilinen sınırlılıklar (judge bulgusu)

Judge'ın en tutarlı eleştirisi: **duygusal tepki puanı ortalama 1.25/2** (EPITOME
0/1/2 ölçeği) — completion'lar davranışı/içeriği doğru yansıtıyor ama altındaki
duyguyu (utanç, yalnızlık, damgalanma korkusu) çoğunlukla açıkça adlandırmıyor,
"yüzeysel kabul" düzeyinde kalıyor. Bu, Faz 4'te üretim tekniğine işlenmesi
gereken somut bir kalibrasyon bulgusu.

Diğer boyutlar: mi_uyumu ort. 3.90/5 · grounding ort. 4.95/5 (uydurma neredeyse yok)
· kısalık/doğallık ort. 4.45/5 · dil bütünlüğü ort. 4.70/5.
