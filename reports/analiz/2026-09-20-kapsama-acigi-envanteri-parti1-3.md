# Sıradaki parti neyi kapatmalı — kapsama açığı envanteri

**Betik:** `scripts/analiz/2026-09-20-kapsama-acigi-envanteri.py` · **Tarih:** 2026-09-20  
**Havuz:** `data/seeds.v2.jsonl` **2240** tohum · üretilmiş **808** (%36) · kalan **1432**

⛔⛔ **Parti sırayla değil kanıtla seçiliyor.** T132: *«veriyi 3,7 kat, yönlendirme kaydını 3,2 kat büyütmek aynı kapsamda hiçbir şeyi değiştirmedi»* ⇒ aynı türden üretmek tıkanan şeyi açmaz.

## 1. ⛔⛔⛔ «Hiç üretilmemiş» değerler bir ihmal değil

| değer | havuzdaki tohum | bunlardan SERT | durum |
|---|---:|---:|---|
| `risk_seviyesi=cok_yuksek` | 20 | 20 | ⛔ tamamı SERT |
| `senaryo=kayma_nuks` | 10 | 10 | ⛔ tamamı SERT |

Hiç üretilmemiş **2** değerin **2**'i tamamen **SERT** sınıfın içinde (`2026-09-17-tohum-beyan-kriz-kapisi.py`) ⇒ Kural 3 gereği etik kurul + uzman onayı olmadan üretime giremezler. Kalanı başka bir sebeple boş kalmış ve **üretilebilir**.

➡️⭐⭐ *Kapsama açığı diye görünen şey kapının ÇALIŞMASIYDI. Bir boşluğu kapatmadan önce onu kimin açtığını sormak gerekiyor — yoksa «eksik» diye kapatılan şey, bilerek konmuş bir sınır olabilir.*

## 2. ⭐ Gerçek açıklar — üretilebilir bölgede

Eşik: sette payı havuzdakinden **≥ 3 puan** düşük olan değerler. «Üretilebilir kalan» SERT sınıf düşüldükten sonradır.

| eksen = değer | sette | havuz | fark | üretilebilir kalan |
|---|---:|---:|---:|---:|
| `stres_tipi=yok` | %70.2 | %75.0 | **+4.8** | 1093 |
| `bagimlilik_turu=receteli_ilac` | %15.2 | %18.8 | **+3.5** | 297 |
| `bagimlilik_turu=kumar` | %19.9 | %23.2 | **+3.3** | 320 |

⚠️ **1 satır ÇOĞUNLUK sınıfı** (`stres_tipi=yok`): havuz payı %40'ın üstünde olan bir değerde 3-7 puanlık fark oransal olarak küçüktür ve hedeflemeye değmez. ➡️ *Mutlak puan eşiği büyük sınıflarda yanıltır; eylenebilir açıklar AZINLIK sınıflarındakilerdir.*

## 3. ⚠️ Üretilebilir havuzun kriz içeriği

| | |
|---|---:|
| kalan tohum | 1432 |
| ⛔ SERT (üretime giremez) | **39** |
| üretilebilir | **1393** |
| ⚠️ bunlardan kriz İÇERİĞİ işareti taşıyan | **55** (%3.9) |

⚠️ K52: *«kriz içeriği etikete güvenilerek elenemez»* ⇒ içerik taraması SERT sınıftan sonra da koşuluyor. Bu işaretler **elenmez, raporlanır** (PERSONA ayrımı, `tohum-beyan-kriz-kapisi` §2): eleme borç/tefeci eksenini tamamen kaybettirirdi ve §8b yönlendirmesi en çok orada önem taşıyor.

## ⛔ Bu envanterin söylemedikleri

| | |
|---|---|
| ⛔ **3 puanlık eşik SEÇİLDİ** | türetilmedi; bu benim önerim |
| ⛔⛔ **Kapsama ≠ kalite** | bir eksenin payını havuza eşitlemek o eksende iyi kayıt üretileceğini göstermez |
| ⛔⛔ **T132 hâlâ geçerli** | kapsama açığını kapatmak da «daha çok veri»dir; güvenlik kapısını açacağına dair bir kanıt YOK |
| ⛔ **Eksenler bağımsız sayıldı** | birlikte dağılım (hücre düzeyi) bakılmadı; T94 tam bunun bedelini ölçmüştü ⇒ parti planı ızgarayı kısıtla kurmalı, marjinalleri ayrı ayrı değil |
