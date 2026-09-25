# Yayılım mı derinlik mi — ölçüt koşudan önce ilan edilmişti

**Betik:** `scripts/analiz/2026-09-20-yayilim-mi-derinlik-mi.py` · **Tarih:** 2026-09-20  
**İlan:** `configs/training/z-h9-k8qo-v014-t*.yaml` başlığı, koşudan önce  
**Kollar:** aynı veri (`v0.0.14`), aynı bölme, tohum 7/13/23

## 1. ⭐⭐⭐ İlan edilen ölçüt ve çıkan sonuç

| kol | kapsam | katman | modül | dereceli | otomatik |
|---|---|---:|---:|---:|---:|
| **h1** | 8 kat · q | 8 | 8 | **16.33** | 10.67 |
| **h9** | 8 kat · **q+o** | 8 | 16 | **7.67** | 8.67 |
| **h2** | **16 kat** · q | 16 | 16 | **2.00** | 6.00 |
| **h8** | 24 kat · q+o · r16 · s10 | 24 | 48 | **4.00** | 9.00 |

⭐⭐⭐ **İlan edilen ÜÇÜNCÜ şık: ikisi birlikte.** h9 = 7.67, ilan edilen ara bölgede (5-13) ve **hem h1'den hem h2'den ayırt ediliyor** ⇒ ne derinlik ne modül sayısı tek başına açıklıyor.

· h9 ↔ h1: fark **-8.67**, eşik 4.7 ⇒ **ayırt ediliyor**  
· h9 ↔ h2: fark **+5.67**, eşik 4.1 ⇒ **ayırt ediliyor**

## 2. ⭐⭐⭐ İki temiz tek-değişkenli karşılaştırma

| karşılaştırma | sabit tutulan | değişen | fark | hüküm |
|---|---|---|---:|---|
| **h1 ↔ h9** | katman (8) | modül 8 → 16 | -8.67 | ⭐ modül sayısı TEK BAŞINA etkiliyor |
| **h9 ↔ h2** | modül (16) | katman 8 → 16 | +5.67 | ⭐ derinlik TEK BAŞINA etkiliyor |

⭐⭐⭐ **İki etken de, öteki sabit tutulduğunda, ayrı ayrı doğrulandı.** Merdiven boyunca iç içe giden iki şey burada ilk kez ayrıldı.

## 3. ⭐⭐ Eşit enerji, artan yayılım — üç nokta

T187'nin post-hoc çifti artık üçlü bir seri: **toplam güncelleme enerjisi neredeyse aynı** olan üç kol, modül sayısına göre sıralanıyor.

| kol | modül | ‖ΔW‖ toplam | modül başına | **dereceli** |
|---|---:|---:|---:|---:|
| h1 | 8 | **10.4** | 3.67 | **16.33** |
| h9 | 16 | **10.6** | 2.63 | **7.67** |
| h8 | 48 | **10.5** | 1.50 | **4.00** |

⭐⭐⭐ **Toplam enerji 10.4-10.6 arasında sabitken (yayılım %1), modül sayısı 8 → 48 çıkarken puan 16.33 → 4.00 diye **tekdüze düşüyor**.** ➡️ *Aynı miktarda değişikliği daha çok yere dağıtmak, kriz davranışına daha çok zarar veriyor.*

⛔ **Üç noktanın ikisi (h1, h8) T187'de POST-HOC seçilmişti**; yeni ve önceden ilan edilmiş olan yalnız **h9**. Seri bu yüzden bir doğrulama değil, *önceden ilan edilmiş bir noktayla güçlenmiş* bir hipotez.

## ⛔ Bu ölçümün söylemedikleri

| | |
|---|---|
| ⛔⛔ **Tasarım 2×2 DEĞİL** | modül sayısı = katman × anahtar ⇒ «16 katman · 8 modül» hücresi **var olamaz**; iki tek-değişkenli karşılaştırma var, tam bir faktöriyel yok |
| ⛔⛔ **n=3 tohum** | eşikler 4,1-4,7; küçük etkiler görünmez |
| ⛔ **Tek veri sürümü, tek ölçüt ailesi** | dereceli puan doğrulanmış değil (T186: anahtar sözcük listesi) |
| ⛔ **`‖ΔW‖` Frobenius** | başka norm başka sıralama verebilir (T187) |
| ⚠️ **Mekanizma yok** | *«neden yayılım zarar veriyor»* bu ölçümde YOK |
