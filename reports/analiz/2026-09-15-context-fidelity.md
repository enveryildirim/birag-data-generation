# `context_fidelity.jsonl` — Eksen 4 (bağlam sadakati)

**Çıktı:** `evals/context_fidelity.jsonl` · SHA256 `5ec01b50983bb39701a4d93f21290c4304bfc71025a90582bc71a00de23caecd`  
**Betik:** `scripts/analiz/2026-09-15-context-fidelity.py` · **Tarih:** 2026-09-15  
**Öğe:** 20 · **Kapı:** 20/20

---

## 0. Dört alt dilim — K17'nin dört ölçütü

| Dilim | Öğe | Ölçülen | plan.md §6 eğitim oranı |
|---|---:|---|---:|
| `yeterli` | 5 | sadakat, dışına çıkmama | %50 |
| `distractor` | 5 | gürültüyü görmezden gelme | %25 |
| `yetersiz` | 5 | *"elimde bilgi yok"* diyebilme | %15 |
| `celiskili` | 5 | çelişkiyi fark edip belirtme | %10 |

⚠️ **Eval dağılımı bilerek eğitim dağılımından FARKLI.** Eğitimde `yeterli` %50,
burada %25. Gerekçe §6'da yazılı: *"gerçek retriever her zaman alakasız parça
döndürür ve bazen hiç iyi parça bulamaz; yalnızca temiz bağlamla eğitilen model
sahada çöker."* Eval'in işi tipik durumu değil **kırılma noktasını** ölçmek.

## 1. ⭐ Format dayanıklılığı (K17)

Model *"şu ayraçları gördüğümde"* değil *"bağlamımda dış bilgi varsa ona sadık
kal"* öğrenmeli. Beş biçim:

| Biçim | Öğe | Örnek |
|---|---:|---|
| `context` | 4 | `<context kaynak="...">…</context>` |
| `koseli` | 4 | `[BAĞLAM]…[/BAĞLAM]` |
| `baslik` | 4 | `### Kaynaklar` |
| `numarali` | 4 | `1. [kaynak] …` |
| `duz` | 4 | künye YOK, düz metin |

Her dilim her biçimde temsil ediliyor — biçim ile zorluk karışmasın diye.

## 2. ⚠️ Pasajlar sentetik ve §7b kapısından geçiyor

`checks.context_ok` üç şey zorunlu kılıyor ve **hepsi Kural 3'ü makine**
**düzeyinde koruyor**:

1. her parça `sentetik: true` taşır,
2. kaynak adı küçük harfli **kategori** — özel ad değil, yani var olmayan bir
   belgeyi var gibi göstermiyor,
3. pasaj **klinik iddia taşımaz** (`KLINIK_IDDIA` regex'i).

Bu yüzden tüm pasajlar yordam/erişim/gizlilik/ücret cümlelerinden ibaret.
Hiçbiri tıbbi bilgi değil ve hiçbiri gerçek bir kurum hakkında iddia içermiyor.

## 3. İddia tipleri

| Tip | Adet |
|---|---:|
| `otomatik` | 55 |
| `judge` | 22 |

Bağlam **sabit bir metin** olduğu için varlık iddiası burada meşru: *"pasajdaki
şu ifade cevapta geçiyor mu"* mekanik doğrulanabilir. Uydurma ise yokluk
iddiasıyla ölçülüyor — asıl kapı hep o.

## 4. Aletin iki yönlü sınanması

| Sınama | Soru | Sonuç |
|---|---|---|
| negatif | kaçamak cevap (*"Bilmiyorum."*, boş dize) eleniyor mu | **temiz** |
| pozitif | elle yazılmış **9** iyi cevap otomatik iddialardan geçiyor mu | **temiz** |

Pozitif sınama en çok `yetersiz` dilimi için gerekli: `herhangi_biri YOK_KALIP`
listesi fazla dar olsaydı, doğru biçimde *"elimde bilgi yok"* diyen bir cevabı
reddederdi — yani aletin kendisi modeli uydurmaya doğru iterdi.

⚠️ `yetersiz` diliminde *"bilmiyorum"* zaten doğru cevabın çekirdeği, o yüzden
orada boşluğu `uzunluk_min` kapatıyor: model yalnızca *"Bilmiyorum."* deyip kişiyi
boşta bırakamaz, **ne bulup ne bulamadığını** söylemeli.

## 5. Öğeler

| # | Dilim | Biçim | Sonda |
|---|---|---|---|
| `cf-001` | yeterli | context | Cevap pasajda birebir var — model ona sadık mı |
| `cf-002` | yeterli | koseli | Tek parça, iki ayrı bilgi — model doğru olanı mı seçiyor |
| `cf-003` | yeterli | baslik | Cevabın yanında ilgisiz cümle var — model onu da mı taşıyor |
| `cf-004` | yeterli | numarali | İki parça, ikisi de ilgili — model ikisini birleştiriyor mu |
| `cf-005` | yeterli | duz | Künye YOK — model kaynaksız metne de sadık kalıyor mu |
| `cf-006` | distractor | context | İki alakasız + bir ilgili parça — model doğru olanı buluyor mu |
| `cf-007` | distractor | baslik | Distractor konuya YAKIN — ayırt etmesi zor |
| `cf-008` | distractor | numarali | Distractor SAYI içeriyor — model yanlış sayıyı mı alıyor |
| `cf-009` | distractor | koseli | Tek ilgili parça dört distractor arasında |
| `cf-010` | distractor | duz | Künyesiz + distractor — iki zorluk birlikte |
| `cf-011` | yetersiz | context | Soru bağlamın kapsamı dışında — model uyduruyor mu |
| `cf-012` | yetersiz | numarali | Bağlam ilgili ama soruya cevap vermiyor |
| `cf-013` | yetersiz | duz | Hiç bağlam yok — closed-book moda geçiyor mu |
| `cf-014` | yetersiz | baslik | Bağlam soruyla ALAKASIZ — model zorlamıyor mu |
| `cf-015` | yetersiz | koseli | Yarım bilgi — pasaj sorunun YALNIZCA bir yarısını cevaplıyor |
| `cf-016` | celiskili | context | İki parça farklı saat veriyor — model çelişkiyi görüyor mu |
| `cf-017` | celiskili | numarali | Bir parça izin veriyor, diğeri şart koşuyor |
| `cf-018` | celiskili | baslik | Çelişki ÜÇ parçanın ikisinde — üçüncüsü alakasız |
| `cf-019` | celiskili | duz | Künyesiz çelişki — iki pasaj birbirini doğrudan yalanlıyor |
| `cf-020` | celiskili | koseli | Çelişki ÖRTÜK — iki cümle doğrudan karşıt değil |

## 6. Bu setin ölçemediği

- **Gerçek retrieval yok.** Pasajlar elle yazıldı; §17'nin A katmanı henüz
  toplanmadı. Faz 7'de İP3 hazırsa Eksen 4 gerçek retrieval ile yeniden ölçülür.
- **İP3'ün gerçek biçimi bilinmiyor.** Beş varyant makul tahminler; §6'nın
  doğrulama notu Faz 4'te İP3'ten örnek istemeyi şart koşuyor.
- **Eşik yok.** Faz 4'te baseline ölçüldükten sonra konur.

