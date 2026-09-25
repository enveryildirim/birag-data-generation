# «Yönlendirmeme» refleksi — korpusta ne kadar var

**Betik:** `scripts/analiz/2026-09-17-yonlendirmeme-refleksi.py` · **Tarih:** 2026-09-17

⚠️ Kalıplar elle yazıldı (K30) ⇒ sayı bir **alt sınırdır**.

| sürüm | kayıt | ret_bilgi | ret_tavsiye | özerklik | **herhangi biri** | oran |
|---|---:|---:|---:|---:|---:|---:|
| `v0.0.2` | 117 | 22 | 1 | 11 | **26** | %22.2 |
| `v0.0.3` | 155 | 30 | 1 | 13 | **35** | %22.6 |
| `v0.0.5` | 155 | 30 | 1 | 13 | **35** | %22.6 |
| `v0.0.6` | 214 | 39 | 1 | 23 | **52** | %24.3 |
| `v0.0.7` | 272 | 51 | 2 | 34 | **74** | %27.2 |
| `v0.0.8` | 571 | 139 | 13 | 60 | **184** | %32.2 |

## ⭐ Yönlendirme ile karşılaştırma

| | yönlendirme adlandıran | **yönlendirmeme kalıbı** | oran |
|---|---:|---:|---:|
| `v0.0.5` | 30 (%19.4) | **35** (%22.6) | **1.2×** |
| `v0.0.8` | 96 (%16.8) | **184** (%32.2) | **1.9×** |

➡️⭐⭐ *Korpus, yönlendirmeyi öğrettiğinden kat kat fazla yönlendirMEMEYİ öğretiyor. İnce ayarın yönlendirme refleksini silmesi, verinin bir EKSİĞİYLE değil bir FAZLASIYLA açıklanabilir — ve bu ikisi taramada aynı görünür ama çareleri zıttır: eksiklik «daha çok yönlendirme ekle» der, fazlalık «bağlam ayrımını öğret» der.*

## ⛔⛔ Bugünkü düzeltmelerin payı

§8b′ gereği **16 kayda** *«hangi kapının açık olduğunu buradan bilemem»* biçiminde bir ret cümlesi eklendi; §5a⁗ bir kayda daha ret getirdi.

⭐ **Ve bu ölçüldü** — `v5-parti4..8`'in revizyon ÖNCESİ ve SONRASI hâli:

| | kayıt | eşleşme |
|---|---:|---:|
| revizyondan önce | **100**/300 | 132 |
| revizyondan sonra | **109**/300 | 150 |
| ⇒ **benim payım** | **+9** | **+18** |

➡️ Katkım gerçek ama küçük: 300 kayıtta **+3 puan**. Asıl sürükleyici `uretim-v5`'in kendi üslubu — revizyon öncesi bile **%33.3** (v0.0.7 %27.2). ⇒ *Dayanaksız iddiayı düzeltirken refleksi güçlendirdim, ama refleksi kuran ben değilim; üretim talimatı kuruyor ve `rol_siniri` dilimi v0.0.8'de **75 kayıt**.*

⚠️ Bu, v0.0.7 ↔ v0.0.8 eğitim karşılaştırmasında bir **karıştırıcıdır** ve CARD.md'deki 16 kayıtlık uyarıyla aynı kayıtlar değildir — ayrı bir kalemdir.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔ **Nedensellik yok** | eş görülme; karşı olgusal korpus yok |
| ⛔ **Kalıplar elle** | alt sınır; sözlükte olmayan biçimler görünmez |
| ⛔ **Bağlam ayrımı ölçülmedi** | kalıbın TERAPÖTİK bağlamda doğru olduğu sayılmıyor; sayı «kaç kayıtta geçiyor», «kaçında yanlış» değil |
| ⚠️ Tüm asistan turları taranıyor | son tur değil (ara turlar da modele gider) |
