# `anaforik_demir` — 13 bağışın hepsi elle okundu

**Betik:** `scripts/analiz/2026-09-18-anaforik-demir-elle-okuma.py` · **Tarih:** 2026-09-18

⛔ T141'in son açık kalemi: muafiyet 13 kez ateşliyordu, yalnız 6'sı okunmuştu.

| | |
|---|---:|
| okunan bağış | **13** |
| ⭐ yerinde | **12** |
| ⛔ kusurlu | **1** |

| kayıt | öge | karar | kullanıcının çıpası |
|---|---|---|---|
| `v4-parti2.v2 #33` | *«o hafta»* | ⭐ yerinde | *«Bu hafta yarıya indirdim»* |
| `v4-parti2.v2 #41` | *«aynı gün»* | ⭐ yerinde | *«Bu sabah kızıma astım tanısı kondu»* |
| `v4-parti2.v2 #56` | *«aynı gece»* | ⭐ yerinde | *«Gece nöbetindeyim»* |
| `v5-parti3 #32` | *«aynı hafta»* | ⭐ yerinde | *«bu hafta sabahları öksürüyorum … parmak ucum da sararmış»* |
| `v5-parti3 #43` | *«aynı sabah»* | ⭐ yerinde | *«Sabah torunu okula götüremedim … İlaç zamanım vardı»* |
| `v5-parti4 #3` | *«aynı hafta»* | ⛔ **kusur** | ⛔ **kusur** — *«bir hafta içmesem mi diye DÜŞÜNMÜŞTÜM»* bir plan süresi; kullanıcı hiçbir hafta çıpası koymamış |
| `v5-parti4 #13` | *«aynı gün»* | ⭐ yerinde | *«Bugün dayanamayıp bir tane içtim»* |
| `v5-parti4 #32` | *«aynı akşam»* | ⭐ yerinde | *«bu akşam yine çocukları yatırdım … bi an durdum»* |
| `v5-parti5 #7` | *«o akşam»* | ⭐ yerinde | kullanıcının turunda *«akşam»* demiri var |
| `v5-parti6 #28` | *«aynı gün»* | ⭐ yerinde | *«dördüncü gün oldu sigarayı bıraktığımdan beri»* |
| `v5-parti6 #30` | *«aynı gün»* | ⭐ yerinde | *«Bugün eve dönerken … Beşinci gündeyim»* |
| `v5-parti6 #59` | *«aynı sabah»* | ⭐ yerinde | *«Sabah duraktayım … Az önce komşunun çocuğu geçti»* |
| `v5-parti7 #46` | *«aynı hafta»* | ⭐ yerinde | *«geçen hafta yine bir maç tutturdum»* |

## ⛔⛔ Önerdiğim düzeltme ölçüldü, çürüdü, UYGULANMADI

Kapı *«bir hekimin»*i belirsiz sayıp atıf saymıyor. Aynı ayrımı zamana taşımayı
önerdim: *«bir hafta»* çıpa sayılmasın. Ölçüm **8 vuruşu**, tekilleştirince
**2 kaydı** etkiliyordu:

| kayıt | kuralın hükmü | elle okuma |
|---|---|---|
| `v5-parti4 #3` | bulgu | ⭐ **doğru** — plan süresi, çıpa değil |
| `v3-parti1 #9` | bulgu | ⛔ **YANLIŞ POZİTİF** — *«bir hafta boyunca instagramı sildim gayet iyi oldum»*; burada *«bir hafta»* gerçekten yaşanmış bir haftadır ve cevabın *«o hafta iyi geçti»*si doğru bir geri göndermedir |

➡️⭐⭐⭐ *Ayrım **belirsizlikte** değil, **gerçekleşmişlikte**: «bir hafta boyunca
sildim» OLMUŞ bir haftadır (çıpalanabilir), «bir hafta içmesem mi diye düşünmüştüm»
DÜŞÜNÜLMÜŞ bir haftadır (çıpalanamaz). Bu bir **kip** ayrımıdır ve anahtar kelimeyle
yakalanmaz — rol tarafında işe yarayan «belirsiz artikel» sezgisi zamana
taşınamıyor.* ⇒ 1 doğru, 1 yanlış pozitif ⇒ **kural benimsenmedi.**

⭐ Muafiyetin geri kalanı sağlam: 80 vuruş kuralın etkilemediği yerde ve 12/13
bağış elle doğrulandı.

## ⛔ Bu okumanın söylemedikleri

| | |
|---|---|
| ⛔ **Kusurlu kayıt DÜZELTİLMEDİ** | `v5-parti4 #3`in *«İkisi de aynı hafta içinde»* cümlesi dayanaksız; `datasets/` IMMUTABLE ⇒ bir sonraki derlemeye kalem |
| ⛔ **Kip ayrımı için kapı yok** | gerçekleşmiş ↔ düşünülmüş zaman ayrımını yakalayan bir sezgi yazılmadı; muafiyet bugünkü hâliyle bu sınıfta kör kalıyor |
| ⚠️ **Kararlar elle** (K30) | ölçüt yazılı — cevap *«aynı X»* diyorsa kullanıcının o X'i bir ÇIPA olarak anmış olması gerekir — ama hüküm bana ait |
| ⚠️ 13 bağış küçük bir küme | oran (1/13) bir eğilim değil |
