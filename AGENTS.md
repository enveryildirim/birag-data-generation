# AGENTS.md

BıRAG talimat veri üretimi ve LLM ince ayarlama projesi. Bu dosya, bu repoda
çalışan yapay zeka ajanları için bağlayıcı kurallardır.

---

## Kural 1 — Doküman disiplini (en önemli kural)

**Yalnızca kullanıcının açıkça verdiği dokümanları oku.**

Bu repo, içinde eskimiş ve terk edilmiş dosyalar bulunan daha büyük bir çalışmanın
parçası (`birag-tubitak/`, `birag-tubitak-data-generation/` altında `tasks_old/`,
`*_old.jsonl` gibi). Hangi dosyanın güncel olduğunu **bilemezsin.**

```
✅ Kullanıcının verdiği / işaret ettiği dosya
✅ Bu repodaki kendi dosyalarımız (plan.md, docs/, src/, configs/)
❌ Komşu klasörlerdeki dosyalar — önce SOR
❌ "Yardımcı olur" diye kendi inisiyatifinle açılan dosya
```

Bir dosyaya bakman gerektiğini düşünüyorsan **önce sor.** Bu kural 2026-09-11'de
gerçek bir hata sonrası kondu: izinsiz okunan 4 dosyaya dayanan analizin tamamı
geri çekilmek zorunda kaldı.

Yeni bir kaynak onaylanırsa `plan.md` §0'a ve `PROJECT_MEMORY.md` oturum kaydına yazılır.

---

## Kural 2 — Dosyaların rolleri

| Dosya | Rol | Ne zaman güncellenir |
|---|---|---|
| [plan.md](plan.md) | **Planlama.** Kararlar, mimari, fazlar, kabul kriterleri | Karar değiştiğinde |
| [PROJECT_MEMORY.md](PROJECT_MEMORY.md) | **Kayıt.** Karar kaydı, oturum günlüğü, açık sorular | **Her oturum sonunda** |
| [docs/arastirma-notlari.md](docs/arastirma-notlari.md) | **Referans.** Terapötik çerçeve, rubrikler, yasak listeleri | Yeni araştırma yapıldığında |
| `AGENTS.md` | **Kurallar.** Bu dosya | Nadiren |

**Oturum başında:** `PROJECT_MEMORY.md` "Şu anki durum" + "Karar kaydı" okunur.
**Oturum sonunda:** oturum kaydı ve varsa yeni kararlar eklenir; gereksiz dosyalar
temizlenir (Kural 8).

Kapalı kararlar yeniden tartışılmaz. Değişmesi gerekiyorsa yeni karar satırı eklenir,
eskisi `SÜPERSEDE` işaretlenir.

---

## Kural 3 — Alan hassasiyeti

Bu proje **bağımlılıkla mücadele eden bireyler** için. Savunmasız nüfus, klinik komşu alan.

- **Klinik içerik uydurma.** Terapötik davranış kuralları `docs/arastirma-notlari.md`'de
  kaynağıyla birlikte yazılı. Oradan dayanağı olmayan bir kural ekleme.
- **Kriz davranışı** üzerinde kendi başına karar verme — uzman ve etik kurul onayı gerekir.
- **Tanı, ilaç, doz, bırakma protokolü** üretme. Rol sınırı ihlali.
- Yasak ifade listesi: `docs/arastirma-notlari.md` §H.6. Üretilen her örnek bu taramadan geçer.
- Üretilen veri gerçek kullanıcılara ulaşacak bir modeli eğitecek. **Güvenlik ekseninde
  gerileme "kabul edilebilir" değildir** — sert kapı.

---

## Kural 4 — Teknik sözleşmeler

Gerekçeleri `plan.md` ve `PROJECT_MEMORY.md` karar kaydında.

```
Python 3.12          (3.14 DEĞİL — mlx-lm/torch wheel sorunları)
uv                   (pip/conda değil)
bf16 LoRA            (QLoRA DEĞİL — K7)
Chat template        daima tokenizer.apply_chat_template, elle string YOK
Eval                 OpenAI-uyumlu HTTP endpoint üzerinden, backend-agnostik
Hiper-parametre      tek YAML; mlx ve cuda runner'ları aynı dosyayı okur
LLM çağrısı          content-hash cache zorunlu — her aşama idempotent
datasets/vX.Y.Z/     IMMUTABLE, bir kez yazılır
data/seeds*.jsonl    IMMUTABLE — üzerine yazılmaz, SÜRÜMLENİR (T78)
Türkçe küçültme      str.lower() YASAK — tohum_guvenlik'ten tr_fold/tr_sadelestir
```

**`data/seeds*.jsonl` neden IMMUTABLE (T78, 2026-09-16 eklendi).** Kural bu tarihe
kadar yazılı değildi ve tohum havuzunun üzerine yazıldı; `ilan-edilen-sha-denetimi`
hemen yakaladı çünkü **8 geçmiş rapor** o dosyanın hash'ini ilan ediyordu ve bir
kısmının çıktısı dondurulmuştu (`data/plan/v3-parti*.jsonl` — üretime girmiş
örneklem planları). Dosya bayt bayt geri alındı, düzeltilmiş havuz
`data/seeds.v2.jsonl` olarak yazıldı.

> ⭐ **Ölçüt:** bir artefaktın dokunulabilir olup olmadığını kural listesi değil,
> **hash'ine atıf veren kayıt sayısı** söyler. Kural yoksa serbest demek değildir;
> `grep -l "<sha>" reports/analiz/*.md` sıfırdan büyükse o dosya fiilen mühürlüdür.

**Düz `str.lower()` neden YASAK (T73 · T75 · T84, 2026-09-16).** Ailenin **on**
örneği sayıldı ve beşi **kapı/dönüştürücünün içindeydi**: §15 sert kapısı 38
ifadenin 26'sını kaçırıyordu (ikisi `kriz_yasagi`), `BIRAG_IMZA` 6 yazımın 4'ünü,
`norm_sure` *«3 YILDAN FAZLA»*yı sessizce `1_3_yil` yapıyordu. ⛔ Öldüren vektör
her sitede **farklı** (`I` mi `İ` mi — kalıbın harfine bağlı), bu yüzden *«doğru
yöne normalize et»* çalışmaz; **sınıf** gerekir.

```
tr_fold(s)        i/ı/İ/I tek sınıfa iner  — genel hâl
tr_sadelestir(s)  + aksan da düşer          — yalnız GENİŞLEMESİ güvenli yerlerde
```

> ⚠️ `tr_sadelestir` her yere uygulanmaz: `normalize._keyword`'de aksansız `iş`
> → `is` ve **`isolation`** içinde eşleşiyor. **Bir foldun ne kadar
> genişleyebileceğini, o çağrı yerinin HATA YÖNÜ belirler** (T80/T84).
> `scripts/analiz/2026-09-16-lower-denetimi.py` yeni kullanımları yakalar.

**Kod hedefi: ~8 dosya, ~700 satır.** Yeni bağımlılık eklemeden önce, o bağımlılığın
*kaliteyi* mi yoksa sadece *altyapıyı* mı iyileştirdiğini sor. İkincisiyse ekleme.

**MLX adapter'ı doğrudan vLLM'e taşınmaz.** MLX = keşif, CUDA = üretim.

---

## Kural 5 — Ölçüm disiplini

- `evals/golden.jsonl` **elle yazılır**, üretim pipeline'ından geçmez, değişmez.
  Model ile üretme, "hızlandırmak" için otomatikleştirme.
- **Baseline fine-tune'dan ÖNCE ölçülür.** Yoksa unutma ölçülemez.
- Checkpoint seçimi: en düşük loss değil, **Pareto noktası**
  (güvenlik gerilemesi = 0 · genel yetenek düşüşü ≤ %3 · içlerinde domain'i en yüksek olan).
- Quantize sonrası eval **atlanmaz**.
- Bir sayı raporlanıyorsa nasıl ölçüldüğü yazılı olmalı.

---

## Kural 6 — Çalışma biçimi

- **Dil:** Türkçe. Kod, değişken ve dosya adları İngilizce.
- **Kaynak göster.** Terapötik veya metodolojik bir iddia, `docs/arastirma-notlari.md`
  kaynakçasına bağlanabilmeli. Bağlanamıyorsa "bu benim önerim" diye işaretle.
- **Emin değilsen söyle.** Bu projede uydurulmuş bir kural, geri çekilmesi haftalar süren
  bir veri setine dönüşür.
- **Faz atlanmaz.** Pilot koşmadan tam üretime, tam üretim bitmeden prod eğitime geçilmez.
- Geçici dosyalar scratchpad'e; projeye değil.

---

## Kural 7 — Tez kaydı (K35)

Bu çalışma aynı zamanda **yüksek lisans bitirme tezi**. Tez malzemesi sonradan
üretilemez; çalışırken kaydedilir. Ayrıntı: `docs/tez/tez-plani.md`.

- **Sohbette üretilen sayı tezde kullanılamaz.** Bir rapor sayısı üretildiyse onu
  üreten betik `scripts/analiz/` altına, çıktı `reports/analiz/` altına yazılır.
  Çıktının başlığında **girdi dosyası + SHA256 · betik · tarih**.
- **`runs/` asla silinmez, üzerine yazılmaz.** Başarısız koşu da saklanır —
  tezin negatif sonuç bölümüdür.
- **Özgün olabilecek her iddia ortaya çıktığı anda** `docs/tez/katki-defteri.md`'ye
  yazılır. Sonra hatırlanmıyor.
- **Karar gerekçesi teknik olmalı.** `PROJECT_MEMORY.md`'nin Gerekçe sütunu
  doğrudan tezin yöntem bölümü olacak; "kullanıcı istedi" yeterli değil.
- **Elenen alternatif de kayda geçer.** Tez "neden bu, neden şu değil"le değerlendirilir.

---

## Kural 8 — Dosya hijyeni (oturum sonu)

**Oturum sonunda, o oturumda üretilmiş ve bir daha kullanılmayacak dosyalar silinir.**

Gerekçe: dosya sayısı arttıkça hangisinin güncel olduğu kaybolur. Kural 1'i doğuran
sorun tam olarak buydu — eskimiş dosyaların arasında doğruyu seçememek. Aynı karmaşayı
bu repoda kendi elimizle üretmeyelim.

**Silinir:**
- Ara ve geçici çıktılar, deneme betikleri, yarım kalmış JSONL'ler
- Yerine yenisi geçmiş rapor/plan dosyaları
- Bir daha okunmayacak log ve döküm dosyaları

**Silinmez — Kural 7 bunları korur:**
```
runs/                          başarısız koşu dahil, asla
datasets/vX.Y.Z/               IMMUTABLE
scripts/analiz/ · reports/analiz/   raporlanan her sayının üreticisi ve çıktısı
docs/ · plan.md · PROJECT_MEMORY.md · prompts/ · configs/ · data/seeds.jsonl
```

Geçici dosya zaten scratchpad'e yazılır, projeye değil (Kural 6).
**Emin değilsen silme, sor.** Silinen dosya `PROJECT_MEMORY.md` oturum kaydına tek
satır yazılır — neyin neden silindiği, sonradan aranmasın diye.

---

## Hızlı bağlam

**Proje:** BıRAG — bağımlılıkla mücadelede çoklu-ajan RAG destekli Türkçe sohbet robotu.
TÜBİTAK/SBB projesi, Kocaeli Üniversitesi, yürütücü Doç. Dr. Süleyman EKEN.

**Bu repo:** İP1 (talimat veri kümesi) + İP2 (ince ayar). Hacim aşamalı, ölçekleme
eğrisine bağlı (K34). **İkincil çıktı: yüksek lisans tezi** (K35).

**Modelin öğreneceği:** terapötik duruş, MI/BDT teknikleri, kriz tanıma, rol sınırı,
çok turlu bağlam koruma, verilen context'e sadakat, iç muhakeme.

**Modelin öğrenmeyeceği:** bağımlılıkla ilgili olgusal bilgi ezberi — o İP3'ün (RAG) işi.

**Model merdiveni (K29):** `gemma-4-E4B-it` döngü → `12B-it` transfer → **`26B-A4B-it` prod**
→ `31B-it` tavan · `Qwen3.8-27B` genelleme kapısı. Üretici: **yalnızca Claude Code** (K30).

**Onaylı kaynaklar:** `plan.md` §0. Başka doküman açılmaz — Kural 1.
