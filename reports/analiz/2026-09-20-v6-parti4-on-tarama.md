# v6-parti4 — üretim öncesi kriz taraması

**Betik:** `scripts/analiz/2026-09-20-v6-parti4-on-tarama.py` · **Tarih:** 2026-09-20  
**Girdi:** `data/plan/v6-parti4.jsonl` · **60** satır

⛔⛔ T192: `v6-parti1 #29` **dört kapının dördünü de** geçmişti. T199: `#54`'ü yakalayan şey sınıfı değil **mesajıydı**. ➡️ *Bir süzgeç yalnız kendi sözlüğünü tanır; tohum metni okunmadan üretime girmez.*

| | |
|---|---:|
| işaret taşıyan satır | **34** / 60 |
| — yalnız `risk_seviyesi` alanından | 31 |
| ⛔ **içerik/beyan süzgeci ateşleyen** | **3** |
| ⛔ **üretilmeyecek satır** | **1** [16] |

⛔ **3 satır içerik/beyan süzgeci ateşledi** ve her biri aşağıda ayrı ayrı hükme bağlandı. Kalan işaretler `risk_seviyesi` alanından geliyor; o alan tek başına eleme ölçütü değil (SERT eşiği `cok_yuksek`).

⛔ **İşaretli 34 satırın tam metni okundu.** Bu bir BETİK çıktısı değil, benim beyanımdır (K30); betik yalnız hangi satırların okunması gerektiğini söyler.

## İşaretli satırlar

| # | tür / senaryo | işaret | hüküm |
|---:|---|---|---|
| 1 | `kumar` / `ambivalans` | risk:yuksek | ⭐ okundu, kriz yok |
| 3 | `kumar` / `rol_siniri` | risk:yuksek | ⭐ okundu, kriz yok |
| 5 | `alkol` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 6 | `kumar` / `ambivalans` | risk:yuksek | ⭐ okundu, kriz yok |
| 7 | `kumar` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 10 | `alkol` / `nazikce_karsi_cikma` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 11 | `tutun` / `ambivalans` | risk:yuksek | ⭐ okundu, kriz yok |
| 12 | `alkol` / `kriz` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 14 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⭐ okundu, kriz yok |
| 15 | `alkol` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 16 | `receteli_ilac` / `belirsiz` | TG:doz aşımı + risk:yuksek | ⛔⛔ **ÜRETİLMEYECEK** |
| 17 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, kriz yok |
| 19 | `receteli_ilac` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 23 | `kumar` / `rol_siniri` | risk:yuksek | ⭐ okundu, kriz yok |
| 24 | `receteli_ilac` / `nazikce_karsi_cikma` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 25 | `alkol` / `ambivalans` | risk:yuksek | ⭐ okundu, kriz yok |
| 26 | `kumar` / `ambivalans` | risk:yuksek | ⭐ okundu, kriz yok |
| 27 | `receteli_ilac` / `nazikce_karsi_cikma` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 29 | `receteli_ilac` / `rol_siniri` | TG:taburcu + risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 31 | `alkol` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 32 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 33 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 35 | `alkol` / `ambivalans` | risk:yuksek | ⭐ okundu, kriz yok |
| 36 | `receteli_ilac` / `kriz` | TG:taburcu + risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 38 | `alkol` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 44 | `kumar` / `rol_siniri` | risk:yuksek | ⭐ okundu, kriz yok |
| 45 | `dijital` / `belirsiz` | risk:yuksek | ⭐ okundu, kriz yok |
| 46 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 48 | `kumar` / `rol_siniri` | risk:yuksek | ⭐ okundu, kriz yok |
| 49 | `kumar` / `ambivalans` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 50 | `alkol` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 53 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 56 | `kumar` / `rol_siniri` | risk:yuksek | ⚠️ okundu, **üretim notu var** |
| 58 | `receteli_ilac` / `rol_siniri` | risk:yuksek | ⭐ okundu, kriz yok |

## ⚠️ Üretim notları — eleme değil, talimat

**`#16`** — ⛔⛔⛔ Dün gece **mide yıkanmış**, bu sabah *«başka bir hap kaldı mı diye bakıyorum»* diyor; buna *«ben kötü bir anneyim»*, çocuğun ondan korkması ve *«nefes alamıyorum»* eşlik ediyor. Mide yıkamasının ertesi günü hap aranması, sürmekte olan bir kendine zarar riskinin biçimi. ⛔ Bu kaydın cevabını yazmak klinik/etik bir karardır (Kural 3) ⇒ ÜRETİLMEDİ, `gd-023` açıldı.

**`#5`** — ⚠️ Kurum özel adı var (K110) — genelleştirilecek. İçerik temiz: kendini bir komşuyla karşılaştırıyor.

**`#7`** — ⚠️ Kurum özel adı var (K110) — genelleştirilecek. *«Eşime söyleyeyim mi sence»* — bu kararı vermeyeceğim.

**`#10`** — ⛔⛔ ÜRETİM NOTU — alkolü ve reçeteli bir ilacı **aynı gün, birlikte, tamamen** kesme planı; üstüne *«mantıklı bir plan mı sizce»*. Partideki en tehlikeli plan ve doğrudan onay isteniyor. md.3. ⛔ Planın NEDEN riskli olduğu SÖYLENMEYECEK — o klinik içerik; söylenecek olan, böyle bir planın ilacı yazan hekimle kurulması gerektiği.

**`#12`** — ⚠️ ÜRETİM NOTU — yönlendirmeyi ÖNCEDEN yasaklıyor (*«beni hemen oraya geri yollamaya çalışmayın, yeni çıktım»*) ve ortada akut bedensel olay yok ⇒ parti3 `#47`'nin ölçütü: **yasağa uyulacak**. Kurum adı genelleştirilecek.

**`#15`** — ⚠️ ÜRETİM NOTU — randevudan önce bir-iki gün bırakıp sonra söyleme planı; parti1 `#57` ile aynı hamle. Plana itiraz edilecek, yalana değil.

**`#19`** — ⚠️ ÜRETİM NOTU — *«Stoklamak bağımlılık mı oldu şimdi?»* retorik ama klinik bir soru. Cevaplanmayacak; konuşulacak olan oğlunun telefonu.

**`#24`** — ⚠️ ÜRETİM NOTU — kızı bilişsel bulanıklık fark etmiş, kullanıcı *«alakası yok»* diyor. İlacın bunu yapıp yapmadığı SÖYLENMEYECEK; itiraz *«yıllardır kullanıyorum, dün başlamadı»* çıkarımına.

**`#27`** — ⚠️ ÜRETİM NOTU — *«Ben deli miyim?»* Psikiyatrinin gerekli olup olmadığı tartışılmayacak; karşılanacak şey damga.

**`#29`** — ⚠️ ÜRETİM NOTU — acilden taburcu, psikiyatri kontrolü iki hafta sonra, **titreme** sürüyor. §5a″ md.1 + md.3 ateşler: *«nasıl idare edeceğim»* bir idare yöntemi istiyor. Yöntem verilmeyecek; randevu tarihi yordamsal ve sorulabilir (parti2 `#59`'un hamlesi).

**`#31`** — ⚠️ ÜRETİM NOTU — elinde bardakla yazıyor ve *«babalığımı rakı söndürdü»* diyor. Şu an içiyor olması bir ders konusu yapılmayacak.

**`#32`** — ⚠️ ÜRETİM NOTU — iki gündür ilaç yok + birkaç kadeh + baş dönmesi, bulantı, ve *«yatıp uyusam geçer mi»*. md.1 + md.3. «Geçer» de «geçmez» de hüküm olur; söylenecek tek şey bunun bugün bakılması gerektiği.

**`#33`** — ⚠️ ÜRETİM NOTU — reçeteli uyarıcı + **arkadaştan alınan beta bloker** + çarpıntı, üstüne *«bu kombinasyon güvenli, araştırdım»*. md.1 + md.2. İtiraz kombinasyonun etkisine değil, *«araştırdım»*ın yeterli sayılmasına yapılacak (epistemik, `#19`/`#23`'ün biçimi).

**`#36`** — ⚠️ Tohumun senaryo etiketi `kriz` ama METİNDE kriz yok: yarınki tedavi randevusuna gitmeme kararsızlığı. ⭐ Etiket değil metin okundu (T199'un dersi). Kurum özel adı genelleştirilecek (K110).

**`#38`** — ⚠️ ÜRETİM NOTU — lohusa, gece bebeğe kalkarken **şiddetli baş dönmesi**, *«düşersem onu nasıl tutarım»*. md.1 ateşler. ⛔ Ders verilmeyecek: zaten kendini yiyip bitirmiş ve kimseye söyleyememiş.

**`#46`** — ⚠️ ÜRETİM NOTU — **elleri titriyor**, evde kalan tablet var ve *«yarım tane alsam belirtiler geçer mi»* diye soruyor. md.1 + md.2 + md.3; parti1 `#51` ve parti3 `#30` ile aynı aile ama orada belirti YOKTU.

**`#49`** — ⚠️ ÜRETİM NOTU — üç ay temizken kazanmış, kupon ekranda, KARAR ANINDA yazıyor. Kurum adı genelleştirilecek. ⛔ «Oynama» da «oyna» da denmeyecek; konuşulacak olan *«kazanmış olmak bir başarı gibi geliyor»*.

**`#50`** — ⛔⛔ ÜRETİM NOTU — üç gündür sokakta, bu gece köprü altı, battaniye yok, sığınmaevini koğuş olduğu için reddediyor, ısınmak için içmiş. ⭐ §5a″'nın dördü de KLİNİK; **barınma/maruz kalma gibi akut refah acilleri hiçbir maddeye girmiyor** ve bunu gösteren ilk tohum bu ⇒ `gd-022` açıldı. ⛔ Alkolün ısı üzerindeki etkisine dair bir şey SÖYLENMEYECEK (üretilmiş sağlık iddiası olur); reddettiği sığınmaevinin gerekçesi ciddiye alınacak ve başka barınma/sosyal hizmet yolları adlandırılacak.

**`#53`** — ⚠️ ÜRETİM NOTU — **göğüs sıkışması ve nefes alamama**, kimseye söylememiş. md.1'in en açık hâli. Yarınki sunum ve ailenin bilmemesi ikinci planda kalacak.

**`#56`** — ⚠️⚠️ ÜRETİM NOTU — yalnızlık kümesi: sponsor üç gündür sessiz, kardeş iki haftadır konuşmuyor, *«herkes yoruldu benden, ben de kendimden yoruldum»*. ⛔ Okundu: ortada kaybolma isteği, yöntem ya da plan YOK; *«kendimden yoruldum»* Türkçede tükenmişlik deyimi ⇒ elenmedi. Ama cevaba **bir kişi daha eklenmeyecek** — üç kişi zaten susmuş durumda. Kurum adı genelleştirilecek.

## ⛔ Bu taramanın söylemedikleri

| | |
|---|---|
| ⛔⛔ **«0 eleme» süzgeçlerin temiz olduğunu göstermez** | T192 tam tersini ölçtü: dördü de temiz derken kaçırmışlardı. Buradaki güvence süzgeç değil, **on dört metnin okunmuş olması** |
| ⛔ **Okuma BENİM okumam** | K30 gereği üretimi ben yapıyorum ve hükümleri de ben veriyorum; uzman okuması değil |
| ⛔ **`gd-021` açık** | çıplak *«İntihar düşüncesi»* sınıfı bu partiye düşmedi (havuzda 6 var); karar hâlâ verilmedi |
| ⚠️ **Yalnız tohum metni okundu** | üretilecek konuşmanın kendisi üretim anında ayrıca kapılardan geçer |
