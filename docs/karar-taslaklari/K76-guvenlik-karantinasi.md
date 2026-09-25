# K76 — güvenlik karantinası kararı · **TASLAK, HÜKÜM YAZILMADI**

> ⛔ **Bu dosya bir karar DEĞİLDİR.** Kararın doğrulanabilir malzemesi aşağıda
> türetilmiştir; **hüküm bölümü boştur ve yürütücü tarafından doldurulur.**
>
> ⚠️ Hangi kaydın neden silinmeyip karantinaya alındığı bir **klinik güvenlik
> kararıdır** (Kural 3). Bunu yazmak bir izin sorunu değil, **yetkinlik ve kurum**
> sorunudur: uydurulmuş bir gerekçe tezde gerçek bir karar gibi okunur.

## 1. Kararın doğrulanabilir kısmı *(türetilir — elle düzenlenmez)*

<!-- TÜRETİLEN:kanit başlangıç — elle düzenleme; `scripts/analiz/2026-09-16-k76-taslagi.py` üretir -->

**Üretildi:** `scripts/analiz/2026-09-16-k76-taslagi.py` · 2026-09-16  
**Artefakt:** `data/guvenlik-karantinasi.jsonl` SHA256 `a5658c0d02326a2b` — **8** kayıt

### Kayıtlar — yalnızca META (klinik metin karantinada kalır)

| # | korpus | parti | tarih | durum | öncelik | eşdurum sayısı |
|---:|---|---:|---|---|---|---:|
| 1 | `v3-parti2-baglam` | 8 | 2026-09-14 | `uzman_karari_bekliyor` | yuksek | 5 |
| 2 | `v3-parti1` | 2 | 2026-09-14 | `uzman_karari_bekliyor` | orta | 7 |
| 3 | `v3-kumulatif` | None | 2026-09-15 | `uzman_karari_bekliyor` | yuksek | 0 |
| 4 | `v3-kumulatif` | None | 2026-09-15 | `uzman_karari_bekliyor` | yuksek | 0 |
| 5 | `v3-kumulatif` | None | 2026-09-15 | `uzman_karari_bekliyor` | yuksek | 0 |
| 6 | `expert-70` | None | 2026-09-15 | `uzman_karari_bekliyor` | yuksek | 0 |
| 7 | `None` | 34 | 2026-09-15 | `uzman_karari_bekliyor` | None | 0 |
| 8 | `None` | 39 | 2026-09-15 | `uzman_karari_bekliyor` | None | 0 |

### Dağılımlar

| | |
|---|---|
| durum | `uzman_karari_bekliyor` ×8 |
| öncelik | `None` ×2, `orta` ×1, `yuksek` ×5 |
| en sık eşdurum | Sirozis erken bulgu ×1, Sarılık ×1, Sokağa düşme riski ×1, Akraba reddi ×1, İntihar düşüncesi sinyali ×1, Borç ×1 |

### K76'ya atıf verenler

| dosya | satır |
|---|---|
| `PROJECT_MEMORY.md` | `—` |
| `PROJECT_MEMORY.md` | `—` |
| `PROJECT_MEMORY.md` | `K78` |
| `PROJECT_MEMORY.md` | `K112` |
| `PROJECT_MEMORY.md` | `K138` |
| `PROJECT_MEMORY.md` | `K153` |
| `PROJECT_MEMORY.md` | `K162` |
| `docs/tez/katki-defteri.md` | `T23` |
| `docs/tez/katki-defteri.md` | `T64` |
| `docs/tez/katki-defteri.md` | `T79` |
| `docs/tez/katki-defteri.md` | `T80` |
| `docs/tez/katki-defteri.md` | `T89` |

⛔ **12 yerden atıf alıyor, kendisi yok.** Numaralandırma K75→K77 atlıyor.

<!-- TÜRETİLEN:kanit bitiş -->

## 2. ⛔ HÜKÜM — yürütücü doldurur

Aşağıdaki üç soru `PROJECT_MEMORY.md`'ye `K76` satırı olarak yazılacak metni
belirler. ⚠️ Boş bırakılan her satır, tezin §11 (Etik) ve §9 (Hata analizi)
bölümlerinde **eksik** kalır.

**(a) Neden silinmedi?** Kayıtlar `klinik_guvenlik_ihlali` aldı ve eğitim setine
girmedi; ama dosyadan da çıkarılmadı. Gerekçe:

> _(yazılacak)_

**(b) Karantinadan çıkış ölçütü nedir?** `durum: uzman_karari_bekliyor` — hangi
uzman, hangi ölçütle, hangi sonuçlar mümkün (`uzman_onayladi` / kalıcı ret /
yeniden yazım)?

> _(yazılacak)_

**(c) Tezde nasıl raporlanacak?** Bu 8 kayıt bir **veri kaybı** mı, bir
**güvenlik kapısının çalıştığının kanıtı** mı, yoksa ikisi birden mi?

> _(yazılacak)_

## 3. Bu taslağın söylemedikleri

| | |
|---|---|
| ⛔ **Hüküm** | yazılmadı ve bu betikle yazılamaz (Kural 3) |
| ⛔ **Klinik metinler** | taslağa girmiyor; yalnızca meta türetildi (K18) |
| ⚠️ Atıf taraması | `\bK76\b` dizgesi; düzyazı içinde başka biçimde anılmışsa görünmez |
| ⚠️ Bu dosya `docs/karar-taslaklari/` altında | ⛔ karar kaydı **değil**; `PROJECT_MEMORY.md` tek karar kaydıdır (Kural 2) |
