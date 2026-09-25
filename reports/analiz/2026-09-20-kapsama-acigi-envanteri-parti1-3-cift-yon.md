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

Eşik: sette payı havuzdakinden **≥ -100 puan** düşük olan değerler. «Üretilebilir kalan» SERT sınıf düşüldükten sonradır.

| eksen = değer | sette | havuz | fark | üretilebilir kalan |
|---|---:|---:|---:|---:|
| `stres_tipi=yok` | %70.2 | %75.0 | **+4.8** | 1093 |
| `bagimlilik_turu=receteli_ilac` | %15.2 | %18.8 | **+3.5** | 297 |
| `bagimlilik_turu=kumar` | %19.9 | %23.2 | **+3.3** | 320 |
| `senaryo=rol_siniri` | %18.7 | %21.4 | **+2.7** | 311 |
| `siddet_seviyesi=agir` | %19.8 | %22.5 | **+2.7** | 306 |
| `evre=nuksetme` | %7.7 | %10.3 | **+2.6** | 168 |
| `profil=yeni_ebeveyn` | %5.9 | %8.5 | **+2.5** | 142 |
| `risk_seviyesi=orta` | %52.5 | %54.9 | **+2.4** | 806 |
| `motivasyon_evresi=hazirlik` | %9.8 | %12.1 | **+2.3** | 191 |
| `evre=birakma_cabasi` | %9.3 | %11.6 | **+2.3** | 185 |
| `siddet_seviyesi=hafif` | %11.5 | %13.8 | **+2.3** | 217 |
| `evre=dibe_vurma` | %8.7 | %10.7 | **+2.1** | 131 |
| `stres_tipi=yalnizlik` | %1.4 | %3.5 | **+2.1** | 67 |
| `profil=ev_kadini` | %6.4 | %8.5 | **+2.0** | 138 |
| `bagimlilik_turu=dijital` | %7.1 | %8.9 | **+1.9** | 143 |
| `yas_grubu=ergen` | %9.7 | %11.4 | **+1.8** | 178 |
| `profil=lise_ergeni` | %10.8 | %12.5 | **+1.7** | 193 |
| `evre=merak_deneme` | %4.8 | %6.2 | **+1.4** | 101 |
| `profil=universite_ogrencisi` | %11.3 | %12.5 | **+1.2** | 179 |
| `profil=diger` | %0.7 | %1.8 | **+1.0** | 34 |
| `risk_seviyesi=cok_yuksek` | %0.0 | %0.9 | **+0.9** | 0 |
| `motivasyon_evresi=eylem` | %2.8 | %3.8 | **+0.9** | 52 |
| `senaryo=ambivalans` | %36.5 | %37.3 | **+0.8** | 539 |
| `profil=emekli_yasli` | %12.6 | %13.4 | **+0.8** | 198 |
| `yas_grubu=orta_yas` | %8.9 | %9.7 | **+0.8** | 146 |
| `yas_grubu=genc_yetiskin` | %15.7 | %16.4 | **+0.7** | 231 |
| `senaryo=kriz` | %1.2 | %1.8 | **+0.5** | 20 |
| `profil=kronik_issiz` | %7.5 | %8.0 | **+0.5** | 99 |
| `stres_tipi=saglik_kaygisi` | %2.1 | %2.6 | **+0.5** | 32 |
| `senaryo=kayma_nuks` | %0.0 | %0.4 | **+0.4** | 0 |
| `yas_grubu=yasli` | %8.3 | %8.7 | **+0.4** | 128 |
| `senaryo=nazikce_karsi_cikma` | %13.7 | %14.1 | **+0.3** | 203 |
| `stres_tipi=yas_kayip` | %0.6 | %0.9 | **+0.3** | 5 |
| `senaryo=discord` | %0.5 | %0.4 | **-0.0** | 6 |
| `stres_tipi=aile_catismasi` | %3.2 | %3.2 | **-0.0** | 45 |
| `senaryo=inkar` | %1.1 | %0.9 | **-0.2** | 11 |
| `stres_tipi=sosyal_karsilastirma` | %1.2 | %1.0 | **-0.2** | 13 |
| `stres_tipi=kronik_agri` | %0.6 | %0.4 | **-0.2** | 5 |
| `evre=sosyal_kullanim` | %5.2 | %4.9 | **-0.3** | 68 |
| `stres_tipi=None` | %2.0 | %1.6 | **-0.4** | 19 |
| `stres_tipi=akran_baskisi` | %2.7 | %2.2 | **-0.5** | 28 |
| `stres_tipi=fiziksel_yorgunluk` | %2.0 | %1.5 | **-0.5** | 18 |
| `stres_tipi=akademik_stres` | %4.2 | %3.4 | **-0.8** | 42 |
| `risk_seviyesi=dusuk` | %6.8 | %5.8 | **-1.0** | 75 |
| `stres_tipi=ekonomik_baski` | %1.9 | %0.8 | **-1.1** | 3 |
| `motivasyon_evresi=on_dusunme` | %18.3 | %17.0 | **-1.4** | 232 |
| `evre=inkar` | %11.6 | %9.8 | **-1.8** | 126 |
| `bagimlilik_turu=alkol` | %28.6 | %26.8 | **-1.8** | 369 |
| `motivasyon_evresi=dusunme` | %69.1 | %67.2 | **-1.9** | 918 |
| `stres_tipi=is_stresi` | %4.5 | %2.4 | **-2.0** | 18 |
| `stres_tipi=ritüel_bagimliligi` | %3.5 | %1.5 | **-2.0** | 5 |
| `risk_seviyesi=yuksek` | %40.7 | %38.4 | **-2.3** | 512 |
| `profil=beyaz_yakali` | %27.7 | %24.6 | **-3.2** | 317 |
| `yas_grubu=yetiskin` | %57.4 | %53.7 | **-3.7** | 710 |
| `senaryo=belirsiz` | %28.2 | %23.7 | **-4.5** | 303 |
| `siddet_seviyesi=orta` | %68.7 | %63.6 | **-5.1** | 870 |
| `evre=tolerans` | %52.7 | %46.4 | **-6.3** | 614 |
| `profil=mavi_yakali` | %17.0 | %10.3 | **-6.7** | 93 |
| `bagimlilik_turu=tutun` | %29.2 | %22.3 | **-6.9** | 264 |

⚠️ **6 satır ÇOĞUNLUK sınıfı** (`risk_seviyesi=orta`, `motivasyon_evresi=dusunme`, `evre=tolerans`, `yas_grubu=yetiskin`, `siddet_seviyesi=orta`, `stres_tipi=yok`): havuz payı %40'ın üstünde olan bir değerde 3-7 puanlık fark oransal olarak küçüktür ve hedeflemeye değmez. ➡️ *Mutlak puan eşiği büyük sınıflarda yanıltır; eylenebilir açıklar AZINLIK sınıflarındakilerdir.*

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
| ⛔ **-100 puanlık eşik SEÇİLDİ** | türetilmedi; bu benim önerim |
| ⛔⛔ **Kapsama ≠ kalite** | bir eksenin payını havuza eşitlemek o eksende iyi kayıt üretileceğini göstermez |
| ⛔⛔ **T132 hâlâ geçerli** | kapsama açığını kapatmak da «daha çok veri»dir; güvenlik kapısını açacağına dair bir kanıt YOK |
| ⛔ **Eksenler bağımsız sayıldı** | birlikte dağılım (hücre düzeyi) bakılmadı; T94 tam bunun bedelini ölçmüştü ⇒ parti planı ızgarayı kısıtla kurmalı, marjinalleri ayrı ayrı değil |
