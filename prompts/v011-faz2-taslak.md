<!-- v0.1.1 Faz 2 taslak alt ajanı istemi (blok 10-11'de kullanıldı). {ISLER} ve {N} doldurulur; bitiş adayları Claude Code'a kalır. -->

Bu bir **metin düzenleme** işi. Kocaeli Üniversitesi'nin TÜBİTAK projesinde, Türkçe bir destek sohbet robotunun eğitim verisindeki kayıtların **iç muhakeme metni** (düşünme) yeniden yazılıyor. Kullanıcı mesajları ve robotun cevabı zaten onaylanmış; onlara dokunulmuyor. Sen yalnız düşünme metnini **yeniden kuruyorsun** ve içindeki kararları **aynen** koruyorsun. Yeni içerik üretmiyorsun.

Amaç yalnız temizlik değil, **yapının yeniden kurulması**: düşünme, o kişinin o mesajından başlayıp çerçeveye, oradan hamleye ve gerekçesine giden bir akıl yürütme olmalı; eski metnin işaretleri sökülüp cümleleri olduğu gibi bırakılmış hâli değil. Önceki bloklarda taslakların %37'si eski metni aynen taşıdı ve yeniden yazılmak zorunda kaldı; kontrol betiği artık bunu yakalıyor.

⛔⛔ **Kayıtları tek tek yaz ve her birini ayrı ayrı dosyaya kaydet.** Her kaydın konuşmasını oku, düşünmesini o konuşmaya bakarak kur, **Write aracıyla** o kaydın JSON dosyasını yaz, kontrol et, sonrakine geç. Metinleri bir Python betiğinde toplayıp topluca yazdırma.

## Adımlar

1. Önce `/Users/pc/projects/birag/data-finetuning/prompts/uretim-v6.md` dosyasını baştan sona oku — bağlayıcı talimat odur (§1 düşünme, §1b yaş ve cinsiyet, §1c ve oradaki **«Yeniden kur, taşıma»**, §1d paragraf, §3 çıktı biçimi ve **eşleme tablosu**). Başka proje dosyası açma. Biçim örneği gerekirse `sonuc/0213.json` dosyasına bakabilirsin (yalnız biçim için; içeriğini kopyalama).
2. İşlerin, sırayla: **{ISLER}.** ({N} kayıt. Diğer sonuc dosyaları **sana ait değil** — dokunma.)
   Kök: `/private/tmp/claude-501/-Users-pc-projects-birag-data-finetuning/0f56c31b-862e-4207-b30f-95714cb3de6a/scratchpad/v011-faz2/kurma/`
   Her iş: `istek/<no>.json` → sonuç `sonuc/<no>.json`. Hepsinde `bitis_adayi: false` ⇒ `bitis_karari: "aday_degil"`, `korunan_soru_turu: null`, `son_cumle: null`, `turn_ending` istek dosyasındaki eski değerin aynısı. (Bir istek dosyasında `bitis_adayi: true` görürsen o kaydı yazma, dönüşte bildir.)
3. Her kaydı yazdıktan hemen sonra sına:
   `cd /Users/pc/projects/birag/data-finetuning && BIRAG_SCRATCH=/private/tmp/claude-501/-Users-pc-projects-birag-data-finetuning/0f56c31b-862e-4207-b30f-95714cb3de6a/scratchpad uv run python scripts/analiz/2026-09-24-v011-faz2.py kontrol <no>`
   ⛔ satırı kalmayana kadar düzelt. Betik `benzerlik` değerini gösteriyor ve **≥ 0,6'da ⛔ veriyor**; hedefin 0,45'in altı. `olumsuz cümle %a→%b` değerinde **b, a'dan belirgin düşük** olmalı; ⚠️ çıkarsa kararların bir kısmını olumlu kur. Bu betiğe ve başka bir proje dosyasına yazma.

## Nasıl yeniden kurulur

- **Önce konuşmayı oku, eski düşünmeyi sonra.** Kendine sor: bu kişi ne yaşıyor, ne istiyor (kendi sözüyle); konuşmanın neresindeyiz; cevap ne yapıyor ve neden. Düşünmeyi bu sırayla yaz. Sonra eski düşünmedeki her kararın yeni metinde bulunduğunu denetle.
- **Kararlar korunur, cümleler korunmaz.**
- ⭐⭐ **Eşleme ortak sözcük gerektirmez.** `korunan_kararlar`'da `eski` eski metinden, `yeni` yeni metinden **birebir** alınmış **kısa** parçalardır (birkaç sözcük, bütün cümle değil); ikisinin aynı sözcükleri taşıması gerekmez. Örnek: `{"eski": "Miktara girmiyorum", "yeni": "saydığını olduğu gibi geri veriyorum"}`. Büyük/küçük harf ve boşluk farkı tolere ediliyor, **noktalama ve « » edilmiyor** — tırnak ya da özel işaret içeren parça seçme.
- ⭐⭐ **Olumsuz kararları olumluya çevir.** *«X demiyorum. Y'ye girmiyorum.»* dizisi yerine cevabın **ne yaptığını** ve neden onu seçtiğini yaz. Olumsuz cümleyi yalnız gerçek bir çekim varsa ve gerekçesiyle koru.
- **Paragraf çapası:** eski düşünmenin paragraf sayısına yakın kal (±1).
- ⛔⛔ **Yaş ve cinsiyet üstveridir** (§1b): `age_group` gibi alanları konuşma görmez. Yalnız konuşma açıkça söylüyorsa olgu gibi yaz; dolaylı ipucu varsa çekinceli kur ve ipucunu an; yoksa hiç anma — gerekçe olarak da anma (*«yaşı ne olursa olsun»* bile yazma).
- ⛔⛔ **Üretim iskelesi hiçbir yere giremez:** *tohum, ızgara, kota, beyan, parti, §, K/T numarası, kart numarası, «mesajdan çıkarıldı», «üretimde», «bu kayıtta», «bitişi değiştirmiyorum»*. Eski düşünmede *«X mesajda yok»* ya da *«tohumda vardı»* diye yalnız üretim ayrıntısına dair bir not varsa, onu yeni metne hiç taşıma — ne olgu olarak ne *«bilmiyorum»* olarak.
- ⛔ **Eski düşünmedeki uydurma da taşınmaz:** konuşmada geçmeyen bir yer, kişi, sayı, madde adı (nargile vb.), nesne (telefon, klavye, araba, masa), alıntı, duygu ya da niyet. Kişinin söylemediği bir sözü tırnakla ona yakıştırma.
- **Konuşmayı doğru aktar:** kimin ne yaptığını, sırayı, süreyi, hangi davranıştan söz edildiğini (içmek mi, bahis sitesine girmek mi) konuşmadaki gibi yaz. Yazdıktan sonra her olgu cümlesini konuşmayla bir kez karşılaştır; kişinin sözünü aktarırken fiili, olumsuzluğu ve sayıyı değiştirme (*«birlikte kurmayız»* ≠ *«kuramayız»*, *«haftada bir şişe»* ≠ *«bir haftalık şişe»*, *«önceki denemelerimde»* ≠ *«iki kez denemiş»*).
- **Düşünme bu cevaba çıkar:** cevabın yapmadığı bir şeyi söyleme (ör. cevap seçim sunmuyorsa «ona bırakıyorum» deme). Cevabın en önemli hamlesi (hekime söylemek, bir kaynağa yönlendirmek) gerekçesiyle bulunsun. Cevap soruyla bitiyorsa sorunun neden sorulduğunu anlat.
- ⛔ **Kararı ters çevirme:** cevap bir şeyi yapmıyorsa (*«seçim önüne koymayacağım»*) düşünme onu *«seçimi ona bırakıyorum»* diye yazamaz; *«yöntem önermiyorum»* ≠ *«yöntem önerip önermemek ona ait»*. Olumluya çevirirken anlamı koru.
- ⛔ Eski düşünmedeki *«X mesajda yok»* notunu *«X'ten söz etmedi, yazdığıyla sınırlı kalıyorum»* diye yeni metne **taşıma** — eşlemede `yeni: null` yap ve `not` alanına kısa gerekçe yaz.
- **Biçim:** düz, başlıksız Türkçe; madde imi, numara, kalın, ⛔/⭐, BÜYÜK HARF vurgusu yok. *«soru sormuyorum, X'liyorum»* kalıbı, system prompt kuralı okuma (*«yasak»*, *«kural gereği»*) ve MI jargonu (*evoking*, *engaging*, *focusing*, *discord*, *change talk*, *ambivalans*) yok.
- **Uzunluk:** ortanca 100-120 sözcük; düşünme karakteri cevabın 4 katını geçemez.
- **Kalıp yok:** açılışlar ve kapanışlar kayıtlar arasında birbirine benzemesin.

Bir kayıt bu çerçeveye sığmıyorsa yeniden yazma: eski düşünmeyi aynen bırak ve `bitis_gerekcesi`'ne kısa bir not düş.

## Dönüş

Kaç kayıt yazdın, her birinin son benzerlik ve olumsuz cümle değeri (tek satırda `no: benzerlik · olumsuz a→b`), emin olmadığın kayıtlar, yaş/cinsiyet ifadesini düşürdüğün ya da çekinceye çevirdiğin kayıtlar. Yarıda kaldıysan nerede kaldığını açıkça yaz.