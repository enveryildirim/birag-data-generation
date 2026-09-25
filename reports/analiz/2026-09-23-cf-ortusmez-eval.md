# Eğitimle örtüşmeyen `celiskili` eval seti — 15 öge

**Betik:** `scripts/analiz/2026-09-23-cf-ortusmez-eval-yaz.py` · **Tarih:** 2026-09-23  
**Çıktı:** `evals/context_fidelity.ortusmez.jsonl` · SHA256-16 `bcb5245652fad03f`  

⛔⛔ **Neden var.** `context_fidelity`'nin 5 `celiskili` ögesinin 5'i de eğitim bankasıyla konu paylaşıyor, 4 değer birebir çakışıyor ⇒ sınıfın kendi hedefindeki kazancı o ögelerde **ezberden ayırt edilemez**. Bu set o boşluğu kapatmak için.

## 1. Örtüşme — ölçüldü

| karşılaştırma | ortak kök (bilgi) | değer çakışması | çapa kökü eğitimde |
|---|---:|---:|---:|
| eğitim bankası (25 çift) | 8/15 | **0** | **10** |
| eski `celiskili` eval ögeleri (5) | 8/15 | — | — |

### Paylaşılan her kök — okuyucu kendisi görsün

| öge | en yakın eğitim çifti | ortak kök |
|---|---|---|
| `cfo-001` | #24 görüşme dili | `baska` |
| `cfo-003` | #21 üst yaş sınırı | `kadar` |
| `cfo-004` | #5 yaş koşulu | `kisile` |
| `cfo-006` | #4 kimlik belgesi | `yoktur` |
| `cfo-008` | #3 görüşme süresi | `yaklas` |
| `cfo-011` | #14 program uzunluğu | `toplam` |
| `cfo-014` | #8 görüşme sıklığı | `planla` |
| `cfo-015` | #10 bekleme süresi | `icinde` |

### Çapa kökü eğitimde geçenler — RAPOR, kapı değil

| öge | taraf | çapa | eğitimde geçen kök |
|---|---|---|---|
| `cfo-006` | B | «bulunmam» | `bulunm` |
| `cfo-006` | B | «bulunmad» | `bulunm` |
| `cfo-006` | B | «bulunmuyor» | `bulunm` |
| `cfo-006` | B | «kendi imkân» | `kendi` |
| `cfo-011` | B | «toplamamakta» | `toplam` |
| `cfo-011` | B | «toplamıyor» | `toplam` |
| `cfo-011` | B | «toplamad» | `toplam` |
| `cfo-015` | B | «kamera bulunmam» | `bulunm` |
| `cfo-015` | B | «kamera bulunmad» | `bulunm` |
| `cfo-015` | B | «kamera bulunmuyor» | `bulunm` |

**Benim hükmüm (K260):** çarpan kökler `bulunm`, `kendi`, `toplam` — hepsi **varlık/eylem yardımcısı** (*bulunmak*, *kendi*, *toplamak*); çelişen içeriği taşıyan sözcükler (*servis, durak, anket, kamera*) eğitimde **geçmiyor**. ⛔ Bu bir yargıdır, ölçü değil — tablo bu yüzden burada.


⚠️ İkinci taslakta da 8 ögede genel kök vardı (`baska`, `kadar`, `kisile`, `yoktur`, `yaklas`, `toplam`, `planla`, `icinde`) — burada **durdum**: devam etmek dedektörü atlatmak için metni bükmek olurdu.

⚠️ **İlk taslakta ölçü 12 ögede ortak kök buldu** (tarihsel, bu betiğin ilk koşusu) — hepsi **genel sözcük**, konu değil: `yalniz` (yalnızca) · `bulunm` (bulunmaktadır) · `boyunc` (boyunca) · `talep, hâlind` (talep hâlinde) · `yurutu` (yürütülmektedir) · `bulunm` (bulunmamaktadır) · `sonras` (sonrasında) · `once` (önce) · `bulunm` (bulunmaktadır) · `bildir` (geri bildirim) · `bulunm` (bulunmaktadır) · `bulunm` (bulunmaktadır). ⇒ **Konuya dokunulmadı, sözcük değişti** (`bulunmaktadır` → `vardır` vb.). Ölçü ve durak listesi **değiştirilmedi**: ateşledikten sonra ölçütü gevşetmek, ön kayda girdi olmuş bir ölçüyü geriye dönük değiştirmek olurdu.

⛔ **Bunun bir yan sonucu var:** aynı ölçü 09-22'de eski ögeler için *«5/5 konu ortaklığı»* demişti ve `cf-016`'nın ortaklığı da genel sözcüklerdi (`acikti`, `vermek`). O ögenin eğitimle **anlamsal** örtüşmesi yine gerçek (açılış saati ↔ kapanış saati), ama sözcük ölçüsü onu genel sözcük üzerinden yakalamıştı. Asıl sağlam kanıt 4 **değer** çakışmasıydı.

⭐ Ölçü 09-22'deki bulaşma ölçüsünün **kendisi** (`olc()` import edildi, K103). Aynı ölçü eski ögelerde 5/5 ortaklık ve 4 değer çakışması bulmuştu.

⚠️ Eski eval ögeleriyle sözcük ortaklığı (bulaşma değil, çeşitlilik bilgisi):

- `cfo-001` ↔ `cf-020`: baska
- `cfo-003` ↔ `cf-019`: danisa
- `cfo-006` ↔ `cf-019`: danisa
- `cfo-008` ↔ `cf-019`: danisa
- `cfo-010` ↔ `cf-019`: danisa
- `cfo-011` ↔ `cf-019`: danisa
- `cfo-012` ↔ `cf-019`: danisa
- `cfo-014` ↔ `cf-019`: danisa

### ⛔ Anlamsal komşular — sözcük ölçüsü bunları GÖRMEZ

| öge | alan | en yakın eğitim alanı | neden komşu |
|---|---|---|---|
| `cfo-008` | hatırlatma | `bildirim` | ikisi de «danışana haber verme» |
| `cfo-014` | çıkış hakkı | `süre` | ikisi de görüşmenin zamanıyla ilgili |
| `cfo-004` | işverenle paylaşım | `saklama`, `bildirim` | kayıt/bilgi akışı ailesi |

⚠️ Bu tablo **elle** kuruldu ve eksik olabilir; sözcük ölçüsünün sıfır demesi anlamsal bulaşmanın sıfır olduğu demek değildir.

## 2. Eski setin açığı — ölçüldü

İki değeri de gizleyen cevap — *«Elimdeki notlarda bu konuda farklı bilgiler var; en doğrusu birime sormak, oradan net bir cevap alabilirsin.»* —

| set | geçtiği öge |
|---|---:|
| eski `celiskili` ögeleri | **5/5** |
| yeni set | **0/15** |

⛔ Eski ögelerin tek içerik iddiası «çelişkiyi adlandır» ve listede `farklı` var ⇒ hangi değerlerin çeliştiğini hiç söylemeyen bir cevap, iki değeri de gösteren cevapla **aynı puanı** alıyor. Yeni ögelerde iki tarafın da anılması ayrı iddiadır (§7a″: *iki pasajın ikisine birden atıf*).

## 3. İddialar yazılmadan önce sınandı

**81/81** yapay cevap beklendiği gibi puanlandı.

| vaka | beklenen | doğru |
|---|---|---:|
| `iyi_yakin` | GEÇER | 15/15 |
| `iyi_uzak` | GEÇER | 15/15 |
| `iyi_resmi` | GEÇER | 4/4 |
| `secen_a` | DÜŞER | 15/15 |
| `secen_b` | DÜŞER | 15/15 |
| `gizleyen` | DÜŞER | 15/15 |
| `cogunluk` | DÜŞER | 2/2 |

⭐ `iyi_uzak` eğitim şablonunun sözcüklerini **bilerek** kullanmıyor (*birbirini tutmuyor* yerine *tutarsız*, *biri/öteki* yerine *bir kaynak/başka bir kaynak*, sıra ters) ⇒ iddialar yalnız eğitimdeki kalıbı ödüllendirmiyor.

## 3b. Taban koşusundan sonra yapılan çapa düzeltmesi

⚠️ İlk sürüm (SHA256-16 `dcb18b36e1504ae5`) taban modelle koşuldu ve 15 cevap **okundu** (K260). İki çapa açığı çıktı — model *siz* hitabıyla yazıyordu (*«eşyalarınızla»*), yapay cevapların hepsi *sen*'le yazılmıştı; ve *«sonlandırma hakkı»* ifadesi A tarafında tanınmıyordu. Çapalar genişletildi ve sınamaya *siz* hitaplı iyi cevap eklendi.

⭐ **Tabana göre ayarlanmadığının kanıtı:** kayıtlı 15 taban cevabı yeni iddialarla yeniden puanlandı ⇒ **hiçbir hüküm değişmedi**. Düzeltme, tabanda iyi bir cevabı kurtarmak için değil, henüz görülmemiş *siz* hitaplı iyi cevaplar haksız düşmesin diye yapıldı.

## 4. Bileşim

| varyant | öge |
|---|---:|
| `dogrudan` | 7 |
| `ortuk` | 3 |
| `ucuncu_ilgisiz` | 3 |
| `cogunluk` | 2 |

| biçim | öge |
|---|---:|
| `context` | 3 |
| `numarali` | 3 |
| `baslik` | 3 |
| `duz` | 3 |
| `koseli` | 3 |

| öge | alan | varyant | sonda |
|---|---|---|---|
| `cfo-001` | erisim | ortuk | Çelişki ÖRTÜK — biri rampa diyor, öteki yalnız merdiven |
| `cfo-002` | sigara_alani | dogrudan | Doğrudan karşıtlık — biri alan var, öteki dumansız diyor |
| `cfo-003` | gorusmeci | cogunluk | Çoğunluk tuzağı — iki parça aynı, biri farklı |
| `cfo-004` | paylasim | dogrudan | Yüksek bedelli çelişki — gizlilik |
| `cfo-005` | oda | ortuk | Çelişki ÖRTÜK — oda iki farklı biçimde tarif ediliyor |
| `cfo-006` | servis | dogrudan | Doğrudan karşıtlık — servis var/yok |
| `cfo-007` | kitapcik | ucuncu_ilgisiz | Çelişki ÜÇ parçanın ikisinde — üçüncüsü alakasız |
| `cfo-008` | hatirlatma | cogunluk | Çoğunluk tuzağı — iki parça hatırlatma var diyor, biri yok |
| `cfo-009` | sikayet | ucuncu_ilgisiz | Çelişki ÜÇ parçanın ikisinde, künyesiz — üçüncüsü alakasız |
| `cfo-010` | gorusmeci_tercihi | dogrudan | Doğrudan karşıtlık — tercih hakkı var/yok |
| `cfo-011` | anket | dogrudan | Doğrudan karşıtlık — düşük bedelli |
| `cfo-012` | emanet | ortuk | Çelişki ÖRTÜK — biri emanet diyor, öteki eşyalarla girilir |
| `cfo-013` | hayvan | dogrudan | Doğrudan karşıtlık — hayvan kabulü |
| `cfo-014` | sonlandirma | ucuncu_ilgisiz | Çelişki ÜÇ parçanın ikisinde — ÇIKIŞ HAKKI; üçüncüsü alakasız |
| `cfo-015` | kamera | dogrudan | Doğrudan karşıtlık — gözetim |

## ⛔ Bunun söylemedikleri

| | |
|---|---|
| ⛔⛔ **Eski setle karşılaştırılamaz** | yeni set bir iddia daha sıkı (iki tarafın anılması); aynı model bu sette daha düşük puan alır. İki setin sayıları yan yana konmaz |
| ⛔ **Şablon ödüllendirme riski** | eğitim kayıtları iki değeri *«biri X, öteki Y»* kalıbıyla anıyor; iki tarafın anılmasını istemek bu kalıbı benimseyen modeli **kısmen** kayırır. Ama bu kalıp §7a″'nın hedef davranışının kendisi; `iyi_uzak` sınaması kalıbın **şart olmadığını** gösteriyor |
| ⛔ **Sözcük iddiası seçmeyi her zaman yakalamaz** | bir tarafı seçip öteki tarafın sözcüğünü *olumsuzlayarak* anan cevap iki çapayı da geçebilir; onu adlandırma iddiası ve `judge` iddiası yakalar. Otomatik puan bir **alt yargıdır** |
| ⛔ **Alan hâlâ idari** | 15 ögenin hepsi idari/usule ilişkin — eğitimle aynı **tür**, farklı **konu**. Sınanan şey **konu** aktarımıdır; idari olmayan bir alana aktarım **sınanmıyor** |
| ⛔ **Yapay cevaplar benim** | sınama cevaplarını da, ögeleri de ben yazdım; iddiaların gerçek model çıktısındaki davranışı ancak koşuda görülür |
| ⚠️ **Taban çizgisi** | ayrı koşudur; bu rapor koşmaz |
