# Vahşi doğa dilimi — kaynak taraması ve engel kaydı

**Betik:** `scripts/analiz/2026-09-15-vahsi-dilim-kaynak-taramasi.py` · **Tarih:** 2026-09-15

---

## 0. Sonuç önce

⛔ **Bu dilim şu an ÜRETİLEMEZ ve sahtesi yapılmadı.** Gerekçe aşağıda ölçüldü.
Gereken karar teknik değil: **yürütücü + etik kurul** (§14).

## 1. Niye gerekli — ölçülmüş açık (K42)

| Ölçüt | Bizim korpus | Tohum havuzu |
|---|---:|---:|
| kullanıcı mesajı | 154 | 2240 |
| medyan kelime | 30 | 36 |
| ≤8 kelimelik mesaj | %2.6 | %0.5 |
| hiç noktalama içermeyen | %0.0 | %0.0 |

İnsanlar sohbet botuna üç cümle yazmaz. Bu dağılım **üretici artefaktı** ve
K42'nin uyarısı tam burada: model "zengin girdi → detaylı yansıtma" öğreniyor,
iki kelimelik girdide **detay uyduruyor**. Grounding skoru riskin en yüksek
olduğu yerde kör.

## 2. Aday kaynaklar ve her birinin düştüğü yer

| Kaynak | Lisans | İnsan yazımı mı | Alan uygun mu | Sonuç |
|---|---|---|---|---|
| `data/seeds.jsonl` (2.240) | proje içi | ⛔ hayır — sentetik | ✅ evet | ⛔ K42 bunları *artefakt* diye ölçtü; vahşi değil |
| `TFLai/Turkish-Alpaca` | apache-2.0 | ⛔ hayır — çeviri/sentetik | ⛔ hayır | ⛔ |
| `merve/turkish_instructions` | apache-2.0 | ⛔ hayır — çeviri/sentetik | ⛔ hayır | ⛔ |
| `OpenAssistant/oasst2` | apache-2.0 | ✅ **evet** | ⛔ hayır (genel amaçlı) | ⛔ **Türkçe prompter mesajı yalnızca 10 tane** |
| Forum (Reddit/Quora vb.) | — | ✅ evet | ✅ evet | 🔴 **etik kurul kararı** (§14) |
| İP5 pilot kullanıcıları | — | ✅ evet | ✅ evet | 🔴 rıza + pilot süreci |

`oasst2` ölçümü (10 mesaj): medyan **8** kelime · ≤8 kelime **%60** · noktalamasız **%0**.

⚠️ Bu sayılar **hiçbir şey kanıtlamaz** — n çok küçük. Buraya yazılmasının tek
sebebi aramanın yapıldığının kaydı olması (Kural 7).

## 3. Neden sahtesi yapılmadı

K42'nin register hedeflerini (kısa açılış ~%40, noktalamasız vb.) kendi
tohumlarımıza uygulayıp "vahşi" diye etiketlemek mümkündü. **Yapılmadı**, çünkü
bu dilimin var oluş sebebi tam olarak *"bizim üretmediğimiz"* olması. Kendi
üreticimizin register'ını kendimiz bozup vahşi demek, ölçmek istediğimiz şeyi
ölçmez — yalnızca ölçüyormuş gibi görünür. Bu, K47'nin (*bir aracın "yok" dediği
yerde "göremedim" mi demek istediği ayrıca gösterilmeli*) veri tarafındaki ikizi.

## 4. Karar için gereken tek şey

Aşağıdakilerden **biri** yeterli:

1. 🔴 **Etik kurul + yürütücü:** forum verisi *eval girdisi* olarak kullanılabilir mi?
   ⚠️ Not: §14'ün kendi önerisi forumları *eğitim verisi* değil **dil referansı**
   olarak kullanmaktı. Eval girdisi o ikisinin arasında ve ayrıca karara bağlanmalı.
2. **İP5 pilotundan rızalı örneklem** — doğru kaynak bu; pilot takvimine bağlı.
3. **Uzman korpusu B dilimi** (K20) — insan yazımı ama danışan mesajları;
   A/B/C duvarı ve PII riski var, uzman kararı.

Karar gelene kadar **Faz 3 bu maddede açık kalır** ve bu dosya o açığın kaydıdır.

