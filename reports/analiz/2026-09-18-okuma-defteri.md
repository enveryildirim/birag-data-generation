# Okuma defteri — yapısal atıf yığını · `v0.0.12`

**Betik:** `scripts/analiz/2026-09-18-okuma-defteri.py` (yazıldı 2026-09-18) · **koşu tarihi:** 2026-09-19  
**Defter:** `reports/analiz/okuma-defteri-*.json` · hüküm kaynağı: T155 (2026-09-18) · 27 iddia elle okundu, 7'si yanlış çıktı ve düzeltildi

⛔⛔ **Neden var.** Yığın her sürümde insan okuması gerektiriyor ve bunu hatırlatan
bir mekanizma yoktu. Mekanizma yoksa ya yığın hiç okunmaz (T155'te olan buydu:
27 iddia hiç okunmamıştı ve **%26'sı yanlıştı**) ya da her sürümde baştan okunur.

➡️⭐⭐ *Elle verilmiş bir hüküm, verildiği METNE bağlıdır. Metin değişmediyse hüküm
de geçerlidir — ama bunu SÖYLEYEN bir şey yoksa, hükmün hâlâ geçerli olduğunu
kimse bilemez.*

| | |
|---|---:|
| yığındaki iddia | **20** |
| ⭐ hükmü TAŞINAN (metin değişmemiş) | **20** |
| ⛔ **YENİ/DEĞİŞMİŞ — okunmalı** | **0** |
| defterden düşen (artık yığında yok) | 0 |

⭐ **Okunacak yeni iddia yok** — yığındaki her iddianın hükmü defterde ve
metni değişmemiş. ⇒ Bu sürüm için elle okuma **yeniden gerekmiyor**.

## Bütün kapılar

| kapı | yığın | hükmü taşınan | ⛔ okunmalı |
|---|---:|---:|---:|
| `yapisal-atif` | 20 | 20 | **0** |
| `mekan-atfi` | 2 | 2 | **0** |

⭐ **Hiçbir kapıda okunacak yeni bulgu yok.**

## ⛔ Bu defterin söylemedikleri

| | |
|---|---|
| ⛔ **Defter HÜKÜM üretmez** | yalnız hangi hükmün hâlâ geçerli olduğunu söyler; hüküm elle verilir (K30) |
| ⛔ **İmza cümlenin kendisi** | aynı iddia başka bir kayda taşınırsa defter onu «bilinen» sayar; kayıt kimliği izlenmiyor |
| ⚠️ **İki kapı kapsanıyor** | yapısal atıf ve mekân; alıntı ve zaman kapılarının bulguları şu an **sıfır** olduğu için deftere gerek yok, ama sıfırdan çıkarlarsa defter onları kapsamıyor |
| ⚠️ Mekânda yalnız **etiketsiz** bulgular deftere giriyor | etiketliler okuma önceliği düşük diye işaretli (T170) ve hüküm gerektirmiyor |
