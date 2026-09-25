# R0 — İP3 tarafındaki mevcut belge korpusu: var, ama bizim katmanımız yok

**Girdi:** `birag-tubitak/` (dizin taraması; belge içeriği OKUNMADI) · **Betik:** `scripts/analiz/2026-09-15-rag-mevcut-korpus-envanteri.py` · **Tarih:** 2026-09-15

---

## 1. Ne var

**`3005-Bagımlılık-Knowledge-base` — 171 belge · 401 MB**

| klasör | belge | boyut | tahmini katman (§17.2) |
|---|---|---|---|
| `türkce/YOK_TEZ` | 104 | 268 MB | **B** — akademik tez — klinik/psikoeğitim |
| `ingilizce/Makale` | 30 | 22 MB | **B** — akademik makale |
| `türkce/Blog` | 24 | 8 MB | **C / B** — blog ve deneyim anlatısı; YEDAM yazıları kurumun ama yordam metni değil |
| `ingilizce` | 7 | 26 MB | **B** — terapist el kitabı |
| `türkce` | 6 | 77 MB | **B** — kitap ve klinik görüşme metni |

**Ayrıca dönüştürülmüş markdown:** `datasets/md_rag_ressources/` **74** dosya · `turkce/` **1** dosya

## 2. Üç bulgu

### 2.1 Türkçe taraf dönüştürülmemiş — ve K90 tam tersini istiyor

Arşivde **134** Türkçe PDF var; dönüştürülmüş Türkçe markdown **1**. Buna karşılık İngilizce taraf **74** markdown'a dönüştürülmüş.

K90 çeviri Türkçesinde kusur oranını %80-83, elle yazılanda %16 ölçmüştü. Yani
hazırlık emeği, **düşük değerli** tarafa harcanmış: 104 YÖK tezi Türkçe-özgün
akademik metindir ve bu korpusun en değerli, en el değmemiş parçasıdır.

### 2.2 A katmanı içeriği yok

YEDAM/Yeşilay adı geçen **9** belgenin tamamı **blog yazısı**:

- Bağımlılıkla Mücadelede Başarının Sırrı_ Tedaviye Devam Etmek _ YEDAM - Yeşilay Danışmanlık Merkezi.pdf
- Dengeli Yaşamayı Öğrenmek İyileştirir _ YEDAM - Yeşilay Danışmanlık Merkezi.pdf
- Gizlilik bağımlılığı besler _ YEDAM - Yeşilay Danışmanlık Merkezi.pdf
- OrnekOlaylarYeşilay Danışmanlık Merkezi.pdf
- Sadece keyif için içmeye devam edebileceğimi sanmıştım… _ YEDAM - Yeşilay Danışmanlık Merkezi.pdf
- YEDAM - Yeşilay Danışmanlık Merkezi.pdf
- Yarınlar aydınlık… _ YEDAM - Yeşilay Danışmanlık Merkezi.pdf
- Ödenmeyen her borç yeni bir bahis oyununun tetikleyicisidir _ YEDAM - Yeşilay Danışmanlık Merkezi.pdf
- İş’te Benim Senfonim _ YEDAM - Yeşilay Danışmanlık Merkezi.pdf

Bunlar deneyim anlatısı ve psikoeğitim; **başvuru yordamı, gizlilik politikası,
ücret, uygunluk metni değil.** R1'in tek gerçek cevheri tam da orasıydı:
*"kayıt aileme gider mi, sicilime düşer mi"*, *"siz aileme söylemezsiniz değil mi"*.
**Bu korpus o soruyu cevaplayamaz.**

### 2.3 Dönüşüm kalitesi ve negatif alan

İki örnek dosya açıldı:

- `md_rag_ressources/.../gambling1.md` (644 KB) — YAML künyesi **var** (`source_file`, `folder`, `date`; lisans alanı **yok**), ama metin ham PDF çıkarımı: `(Page 2)` işaretleri ve sözcük başına satır kırılması. Kitap başına **tek dosya**, chunk yok.
- `turkce/alkol/1.md` — Yeşilay sayfası, **temiz Türkçe**. Ama içeriği yoksunluk belirtileri, *"6-8 saat sonra"* zaman çizelgesi, *"ölüm riski"*: §17.3'ün **negatif alanı**. Mevcut malzemenin bir kısmı RAG havuzuna **olduğu gibi giremez**.

## 3. Sonuç — plan değişmiyor, R2 netleşiyor

| Katman | Durum |
|---|---|
| **A — yordam/kurum** | ⛔ korpusta **yok**. R2 için hâlâ dışarı çıkmak gerekiyor |
| **B — klinik/psikoeğitim** | ✅ bol miktarda var (104 tez + 37 kitap/makale). Toplama işi bitmiş, **tasnif ve negatif alan ayıklaması** işi başlıyor |
| **C — deneyim/dil** | ✅ 24 blog. §17.2 gereği RAG havuzuna girmez; kullanıcı register'ı için değerli |

⚠️ **Sınır:** katman ataması dosya adından yapıldı, **içerik okunmadı**. Bir
belgenin gerçekten hangi katmana düştüğü ancak açılınca bilinir; bu envanter
hangisinin açılmaya değer olduğunu söyler, ne içerdiğini değil.
