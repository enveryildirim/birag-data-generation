# Dilim kapsaması — `plan.md` §6'ya karşı

**Girdi:** `data/candidates/v3-kumulatif.jsonl` (SHA256 `5867e31fc49e3dbf…`)  
**Betik:** `scripts/analiz/2026-09-14-dilim-kapsama-raporu.py` · **Tarih:** 2026-09-14 · **Kayıt:** 104

---

> Bu rapor `uretim-v3.md` hedeflerini DEĞİL, `plan.md` §6'nın **dilim karışımını** ölçüyor. İkisi ayrı belgeler; §6 bugüne kadar hiç ölçülmemişti.

## 1. §6 dilim karışımı

| Dilim | Var | Oran | Hedef | Sapma | |
|---|---:|---:|---:|---:|:--:|
| Terapötik diyalog, tek tur | 63 | %61 | %35 | +26 p | ❌ |
| Çok turlu diyalog | 32 | %31 | %15 | +16 p | ❌ |
| Kriz + rol sınırı | 12 | %12 | %10 | +2 p | ✅ |
| Direnç / inkâr / discord | 10 | %10 | %5 | +5 p | ✅ |
| Nazikçe karşı çıkma | 9 | %9 | %5 | +4 p | ✅ |
| RAG modu — context sadakati | 10 | %10 | %10 | -0 p | ✅ |
| Kapsam dışı / sınır | 16 | %15 | %5 | +10 p | ❌ |
| Replay (genel amaçlı) | 0 | %0 | %15 | -15 p | ❌ |

## 2. ⚠️ Çok turlu kayıtların DERİNLİĞİ

§6 *"3-5 turluk alışveriş"* diyor ve §5c çok turlu kayıtların **MI süreci geçişini** öğretmesini istiyor. Ölçüm:

| Kullanıcı turu | Kayıt |
|---:|---:|
| 1 | 72 |
| 2 | 18 |
| 3 | 10 |
| 4 | 4 |

**3+ turlu kayıt: 14/104 (%13).** Çok turlu 32 kaydın **18**'i iki turlu (tek alışveriş), **14**'ü 3-5 turlu. §6'nın istediği derinlik artık korpusta var ama çoğunluk hâlâ iki turlu.

## 3. Davranış kartı kapsaması

19 karttan **17**'i üretildi.

| Kart | Kayıt |
|---|---:|
| `motivasyon` | 6 |
| `kriz` | 0  ⛔ uzman onayı bekliyor |
| `farkindalik` | 19 |
| `kutlama` | 3 |
| `bilgilendirme` | 4 |
| `hedef_belirleme` | 6 |
| `kayma_nuks` | 7 |
| `ambivalans` | 18 |
| `inkar` | 7 |
| `discord` | 2 |
| `rol_siniri` | 9 |
| `durtu` | 3 |
| `hukuki_kaygi` | 3 |
| `borc_finansal` | 2 |
| `kayip_kovalama` | 1 |
| `nazikce_karsi_cikma` | 9 |
| `anlasilmama` | 1 |
| `bilmiyorum_cikmazi` | 4 |
| `sanrili_soylem` | 0  ⛔ uzman onayı bekliyor |

## 4. Okuma

- ❌ **Replay 0/104.** §6 bu dilimi *"açık genel amaçlı setlerden örneklenir"* diye tanımlıyor — Claude Code üretimi değil. Ayrı bir iş kalemi (catastrophic forgetting savunması, §9).
- ❌ **Terapötik tek tur %61**, hedef %35. Diğer dilimler eksik olduğu sürece bu pay mekanik olarak şişer; kendi başına bir kusur değil.
- ⚠️ **Kapsam dışı / sınır %15**, `plan.md` §6 %5 diyor — ama `uretim-v3.md` §8 aynı şey için **%15** diyor. **İki belge çelişiyor**; hangisinin geçerli olduğu kararlaştırılmalı (işaretlenen tutarsızlıktır, çözümü değil).
- ✅ **Nazikçe karşı çıkma %9**, hedef %5. K21 bu dilimi *"eğitilmezse ortaya çıkmaz"* diye işaretliyor.
- ⛔ Hiç üretilmemiş davranış kartı: `kriz`, `sanrili_soylem`. `kriz` ve `sanrili_soylem` uzman onayı bekliyor (Kural 3).
- Derin çok turlu (3-5 tur): **14/104**. §6'nın "3-5 turluk alışveriş" beklentisi için ölçülen tek sayı budur; `turn_type=multi` iki turlu kayıtları da sayar ve tek başına yanıltıcıdır.

