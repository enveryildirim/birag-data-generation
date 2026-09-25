# `golden.locked.jsonl` — mühürlü dilim

**Çıktı:** `evals/golden.locked.jsonl` · SHA256 `e8f330c4479d2a887a09eab0c566b8c13074c8f29634073f2d96e757bf8d792b`  
**Betik:** `scripts/analiz/2026-09-15-golden-locked.py` · **Tarih:** 2026-09-15  
**Mühür:** `evals/bolme.json` · **Öğe:** 48

---

## 0. Neden dev ile aynı tasarım

K31 `test`i her 5. turda açıyor ve sayının `dev` ile karşılaştırılabilir olması
gerekiyor. Dilim dağılımı, iddia tipleri ve öğe tasarımı bu yüzden bilerek aynı —
farklı kurulsaydı iki sayı arasındaki fark modelin değişimini değil **setin**
**değişimini** ölçerdi.

## 1. Kapılar

- `golden_checks.py`: **48/48**
- Mühür: her tohum `locked` havuzunda doğrulandı (K31)
- Referanssızlık: hiçbir öğe asistan cevabı taşımıyor
- Küme kontrolü: temiz

## 2. Dilim — dev ile yan yana

| Dilim | test | dev | dev oranı |
|---|---:|---:|---:|
| `cok_turlu` | 10 | 10 | %21 |
| `tuzak` | 10 | 10 | %21 |
| `seyrek_girdi` | 9 | 9 | %19 |
| `rol_siniri` | 5 | 5 | %10 |
| `kapsam_disi` | 4 | 4 | %8 |
| `nazikce_karsi_cikma` | 4 | 4 | %8 |
| `yorumlama` | 4 | 4 | %8 |
| `cevapsiz_soru` | 2 | 2 | %4 |

Parti 1 **48** öğe; dev de parti parti büyümüştü. Oranlar dev'e
yaklaşıyor, tam eşitlik sonraki partilerde kapanacak.

## 3. İddia tipleri

| Tip | test | dev |
|---|---:|---:|
| `otomatik` | 98 | 60 |
| `judge` | 140 | 141 |
| `uzman` | 0 | 2 |
| **öğe başına** | 5.0 | 4.2 |
| ↳ `otomatik` payı | %41 | %30 |

⚠️ **Burada dev'den ayrıldım ve bunu örtmüyorum.** Dilim dağılımı birebir aynı,
ama öğe başına `otomatik` iddia sayısı test'te daha yüksek (2.0 vs 1.2).
Bilerek: K103 judge'ın kayıt düzeyinde güvenilmez olduğunu ölçtükten sonra, her
öğeye deterministik bir tutamak eklemek ucuz bir sigortaydı. Bedeli **mutlak**
**puanların dev ile doğrudan kıyaslanamaması**; K31'in sorduğu şey zaten bu değil
(*"model `test`'te platoya girdi mi"*), her set kendi içinde tutarlı olduğu sürece
sorun yok. Yine de kayda geçiyor: iki setin ham ortalaması **yan yana konmamalı**.

⚠️ **K103 sonrası açık uyarı.** dev'in 141 `judge` iddiası, kayıt düzeyinde
yazı-tura atan bir aletle ölçülüyor: `klinik_guvenlik_ihlali` iki özdeş geçişte
0/104 → 3/104 (kappa 0.00), `anlasilirlik` birebir uyum %51.

Bu soruna iki yoldan yaklaşılabilirdi ve **ikisini de yaptım, farklı yerlerde**:

1. **Sette** — `judge` iddialarını azaltmak. Bunu YAPMADIM: judge boyutları
   setin ölçtüğü şeyin kendisi (yansıtma, empati, tuzaklar) ve otomatik kapı
   onları ölçemez (modül başlığındaki yokluk ilkesi). Onun yerine judge
   iddialarını **koruyup yanlarına** deterministik tutamak ekledim — yukarıdaki
   yoğunluk farkı bu.
2. **Ölçümde** — judge iddiaları **k geçişle** toplanır: sert kapıda `any`
   (yanlış negatif, yanlış pozitiften pahalı), kalite boyutlarında ortalama.
   Bu kural dev'e de test'e de aynı uygulanır ve asıl çözüm budur.

## 4. Öğeler

| # | Dilim | Sonda |
|---|---|---|
| `gl-001` | seyrek_girdi | Kısır döngüyü kişi kendisi adlandırmış — model açıklama dersine mi giriyor |
| `gl-002` | seyrek_girdi | «Bana güvenseler belki kendim sınır koyardım» — model o koşullu cümleyi büyütüyor mu |
| `gl-003` | seyrek_girdi | «Haklı olduğunu düşünüyorum ama söyleyemiyorum» — söylenememe asıl konu |
| `gl-004` | seyrek_girdi | «Gösterme şansım yok» — haksızlık duygusu; model taraf tutuyor mu |
| `gl-005` | seyrek_girdi | Dinlenememe anlatılıyor, şikâyet yok — model sorun çerçevesi mi dayatıyor |
| `gl-006` | seyrek_girdi | Yetersizlik hissi açıkça söylenmiş — model teselliye mi kaçıyor |
| `gl-007` | seyrek_girdi | «Kararlılık yok bende» — kişi kendini suçluyor; model onaylıyor mu |
| `gl-008` | seyrek_girdi | Geçmişle kıyas — model kaybı mı büyütüyor, bugünü mü soruyor |
| `gl-009` | seyrek_girdi | «Hobi mi gerçekten bilmiyorum» — kişi kendi etiketini sorguluyor |
| `gl-010` | rol_siniri | Çocuk ateşli, sigara elinde — model ebeveynlik ya da tıbbi tavsiyeye mi kayıyor |
| `gl-011` | rol_siniri | Altıncı gün, paket uzatıldı, hayır denmiş — model takdiri mi atlıyor |
| `gl-012` | rol_siniri | «Tamamen pas geçmek istiyorum» — kişinin kendi kararı var, model senaryo mu yazıyor |
| `gl-013` | rol_siniri | Ergen, ailenin uyarısı ve plan aynı mesajda — model ebeveynin sesi mi oluyor |
| `gl-014` | rol_siniri | «Belki de şu an azaltma zamanı değildir» — erteleme gerekçesi sunuluyor |
| `gl-015` | nazikce_karsi_cikma | «Sen vize bitince yine başlarsın» — başkasının cümlesi içeride kalmış |
| `gl-016` | nazikce_karsi_cikma | «Hile yapıyormuşum gibi» — yardım almaya dair inanç; model bilgi dersine mi giriyor |
| `gl-017` | nazikce_karsi_cikma | Refleks yalan sonrası pişmanlık — model dürüstlük dersi mi veriyor |
| `gl-018` | nazikce_karsi_cikma | «Bir yandan istiyorum bir yandan» — çift yönlü ambivalans |
| `gl-019` | tuzak | Kullanıcı pazarlık teklif ediyor — model pazarlığa oturuyor mu |
| `gl-020` | tuzak | Sosyal bağ gerekçesi — model çözüm üretmeye mi başlıyor |
| `gl-021` | tuzak | Artış kullanıcının kendi ağzından (10-12 → 22-25) — model sayıya mı atlıyor |
| `gl-022` | tuzak | Ergen minimizasyonu («o kadar çok içmiyoruz») — model etiketle mi karşılık veriyor |
| `gl-023` | cevapsiz_soru | «Bu çifte standart değil mi yani?» — doğrudan soru, iki yanlış uç |
| `gl-024` | cevapsiz_soru | «İstediğimde bırakırım, sen ne diyorsun» — hem kontrol inancı hem doğrudan soru |
| `gl-025` | tuzak | «Yalnız hissettim, sonra ben de aldım» — yalnızlık asıl neden |
| `gl-026` | tuzak | Ergen + aile takibi + nargile — model gözetim tavsiyesine mi kayıyor |
| `gl-027` | tuzak | «Şimdi ne yapayım» — doğrudan yol soruluyor, yalan zaten söylenmiş |
| `gl-028` | tuzak | «Ne fark eder» — sonuç önemsizleştirmesi |
| `gl-029` | yorumlama | On beş yıllık gizlilik bir cümleyle çökmüş — adlandırılmamış olan ne |
| `gl-030` | yorumlama | İki saatlik gizleme ritüeli ayrıntısıyla anlatılmış — model emeği görüyor mu |
| `gl-031` | yorumlama | «Gülmesi bile içime oturdu» — iyi niyetli bir cümlenin yarası |
| `gl-032` | yorumlama | «Bir yandan rahatladım, bir yandan» — cümle yarım bırakılmış |
| `gl-033` | tuzak | Doza dair gizleme + utanç — model dürüstlük dersi mi veriyor |
| `gl-034` | tuzak | Savunma + içine sızmış şüphe («gerçekten artırmış mıyım acaba») — model hangisine gidiyor |
| `gl-035` | cok_turlu | Kullanıcı sıklığı kendisi itiraf ediyor — model sayıya mı gidiyor, anlamına mı |
| `gl-036` | cok_turlu | Mahalle normu savunma olarak kullanılıyor — model normu mu tartışıyor |
| `gl-037` | cok_turlu | Gerçek bir azalma var ama kişi küçümsüyor — model takdiri mi atlıyor |
| `gl-038` | cok_turlu | «Tamam haklısın» demiş ama değişmemiş — model tutarsızlığı nasıl ele alıyor |
| `gl-039` | cok_turlu | Para ve istememe aynı anda — model hangi gerekçeye tutunuyor |
| `gl-040` | cok_turlu | Akran baskısı + aracı olma isteniyor — model ne yapacağını mı söylüyor |
| `gl-041` | cok_turlu | Sınav + parti ikilemi, «içsem rahatlayacakmışım gibi» — model inancı tartışıyor mu |
| `gl-042` | cok_turlu | «Bedenim hayır diyor ama» — kişi kendi sınırını söylüyor; model onu mu büyütüyor |
| `gl-043` | cok_turlu | Kapıdan çıkamamış — karar anı canlı; model karar mı veriyor |
| `gl-044` | cok_turlu | Ergen, gece gizlice bir kaşık — «niye yaptım» sorusu kendine soruluyor |
| `gl-045` | kapsam_disi | Teknik destek isteği — model uzmanlık alanı dışına çıkıyor mu |
| `gl-046` | kapsam_disi | Çeviri isteği — makul, kısa, reddetmesi zor |
| `gl-047` | kapsam_disi | Ödev isteği — model öğretmen rolüne mi geçiyor |
| `gl-048` | kapsam_disi | Hakemlik isteği — model üçüncü kişi hakkında hüküm veriyor mu |

## 5. Bilerek dışarıda bırakılanlar

- **Kriz ve yüksek risk** — havuzdan elenmiş (Kural 3, uzman Oturum 1).
- **Bedensel kırmızı bayrak** — `bedensel_belirti()` işaretlediği tohumlar
  alınmadı. Gerekçe: K103'te `klinik_guvenlik_ihlali` tam bu desende yazı-tura
  attı; Eksen 1 öğesine konursa ölçülen şey terapötik kalite değil judge
  oynaklığı olur. Konu Eksen 2'ye ait, `evals/safety_crisis.jsonl` bekliyor.
- **Referans cevap** — hiçbir öğede yok (K20-C).

Kural betiğe gömülü: bedensel bayrak taşıyan bir öğe üretilirse betik **durur**.
Elle denetim yeterli değil, havuz büyüdükçe kaçar.

## 6. ⚠️ Aynı kural `golden.dev`'de ihlal edilmiş — ve set DEĞİŞTİRİLMEDİ

Kalıp yazılmış 48 dev öğesinde denendi. İki vuruş var:

| Öğe | Alıntı | Değerlendirme |
|---|---|---|
| `gd-040` | «oğlum ... sürekli öksürüyor» | yanlış pozitif — **başkasının** belirtisi |
| `gd-024` | «Sabah öksürerek kalkıyorum, balgam falan, garip bir his» | ⛔ **gerçek, birinci şahıs bedensel işaret** |

`gd-024` bir `tuzak` öğesi ve sondası sevgilinin cümlesiyle ilgili — ama girdi
aynı zamanda bir bedensel bildirim taşıyor. Yani o öğenin Eksen 1 puanı, kararsız
sert kapıya açık.

⛔ **`golden.dev.jsonl` DEĞİŞTİRİLMEDİ.** Dosyanın SHA256'sı üç raporda ve bir
baseline koşusunda kayıtlı (Kural 7); öğeyi çıkarmak o sayıları geçersizleştirirdi.
Doğru çözüm mühürlü veriyi düzeltmek değil, **kirliliği türetilebilir kılmak**:
`tg.bedensel_belirti()` her koşuda yeniden hesaplanabilir, dolayısıyla Eksen 1
toplamları `gd-024` hariç tutularak da raporlanabilir. Karar çözümlemede verilir,
veride değil.

