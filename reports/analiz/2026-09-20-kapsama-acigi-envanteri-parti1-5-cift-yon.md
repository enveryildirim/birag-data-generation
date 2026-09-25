# Sıradaki parti neyi kapatmalı — kapsama açığı envanteri

**Betik:** `scripts/analiz/2026-09-20-kapsama-acigi-envanteri.py` · **Tarih:** 2026-09-20  
**Havuz:** `data/seeds.v2.jsonl` **2240** tohum · üretilmiş **927** (%41) · kalan **1313**

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
| `bagimlilik_turu=receteli_ilac` | %16.1 | %18.8 | **+2.7** | 271 |
| `bagimlilik_turu=kumar` | %20.6 | %23.2 | **+2.6** | 290 |
| `risk_seviyesi=orta` | %52.5 | %54.9 | **+2.4** | 743 |
| `evre=nuksetme` | %7.9 | %10.3 | **+2.4** | 157 |
| `senaryo=rol_siniri` | %19.1 | %21.4 | **+2.3** | 285 |
| `stres_tipi=yok` | %72.7 | %75.0 | **+2.2** | 986 |
| `motivasyon_evresi=hazirlik` | %9.9 | %12.1 | **+2.1** | 178 |
| `siddet_seviyesi=hafif` | %11.9 | %13.8 | **+2.0** | 200 |
| `stres_tipi=yalnizlik` | %1.5 | %3.5 | **+2.0** | 64 |
| `yas_grubu=ergen` | %9.5 | %11.4 | **+1.9** | 168 |
| `profil=yeni_ebeveyn` | %6.7 | %8.5 | **+1.8** | 128 |
| `bagimlilik_turu=dijital` | %7.2 | %8.9 | **+1.7** | 133 |
| `evre=birakma_cabasi` | %10.0 | %11.6 | **+1.6** | 167 |
| `evre=dibe_vurma` | %9.2 | %10.7 | **+1.5** | 116 |
| `profil=ev_kadini` | %7.0 | %8.5 | **+1.5** | 125 |
| `siddet_seviyesi=agir` | %21.0 | %22.5 | **+1.5** | 271 |
| `profil=lise_ergeni` | %11.2 | %12.5 | **+1.3** | 176 |
| `profil=emekli_yasli` | %12.3 | %13.4 | **+1.1** | 186 |
| `evre=merak_deneme` | %5.3 | %6.2 | **+1.0** | 91 |
| `risk_seviyesi=cok_yuksek` | %0.0 | %0.9 | **+0.9** | 0 |
| `yas_grubu=orta_yas` | %8.8 | %9.7 | **+0.9** | 136 |
| `profil=universite_ogrencisi` | %11.7 | %12.5 | **+0.8** | 162 |
| `profil=diger` | %1.0 | %1.8 | **+0.8** | 31 |
| `stres_tipi=saglik_kaygisi` | %1.9 | %2.6 | **+0.7** | 31 |
| `senaryo=kriz` | %1.3 | %1.8 | **+0.5** | 18 |
| `motivasyon_evresi=eylem` | %3.3 | %3.8 | **+0.5** | 44 |
| `yas_grubu=yasli` | %8.2 | %8.7 | **+0.5** | 119 |
| `senaryo=kayma_nuks` | %0.0 | %0.4 | **+0.4** | 0 |
| `stres_tipi=yas_kayip` | %0.5 | %0.9 | **+0.4** | 5 |
| `profil=kronik_issiz` | %8.0 | %8.0 | **+0.1** | 86 |
| `stres_tipi=aile_catismasi` | %3.0 | %3.2 | **+0.1** | 43 |
| `senaryo=discord` | %0.4 | %0.4 | **+0.0** | 6 |
| `senaryo=inkar` | %1.0 | %0.9 | **-0.1** | 11 |
| `senaryo=nazikce_karsi_cikma` | %14.1 | %14.1 | **-0.1** | 183 |
| `evre=sosyal_kullanim` | %5.0 | %4.9 | **-0.1** | 64 |
| `yas_grubu=genc_yetiskin` | %16.5 | %16.4 | **-0.1** | 205 |
| `stres_tipi=akran_baskisi` | %2.4 | %2.2 | **-0.1** | 28 |
| `stres_tipi=sosyal_karsilastirma` | %1.1 | %1.0 | **-0.1** | 13 |
| `stres_tipi=kronik_agri` | %0.5 | %0.4 | **-0.1** | 5 |
| `stres_tipi=fiziksel_yorgunluk` | %1.7 | %1.5 | **-0.2** | 18 |
| `stres_tipi=None` | %1.9 | %1.6 | **-0.4** | 17 |
| `risk_seviyesi=dusuk` | %6.5 | %5.8 | **-0.7** | 70 |
| `stres_tipi=akademik_stres` | %4.1 | %3.4 | **-0.7** | 38 |
| `senaryo=ambivalans` | %38.1 | %37.3 | **-0.8** | 481 |
| `stres_tipi=ekonomik_baski` | %1.6 | %0.8 | **-0.8** | 3 |
| `motivasyon_evresi=dusunme` | %68.2 | %67.2 | **-1.0** | 844 |
| `bagimlilik_turu=alkol` | %28.3 | %26.8 | **-1.5** | 338 |
| `stres_tipi=is_stresi` | %3.9 | %2.4 | **-1.5** | 18 |
| `stres_tipi=ritüel_bagimliligi` | %3.0 | %1.5 | **-1.5** | 5 |
| `motivasyon_evresi=on_dusunme` | %18.6 | %17.0 | **-1.6** | 208 |
| `evre=inkar` | %11.4 | %9.8 | **-1.6** | 114 |
| `senaryo=belirsiz` | %26.0 | %23.7 | **-2.3** | 290 |
| `profil=beyaz_yakali` | %27.0 | %24.6 | **-2.4** | 291 |
| `risk_seviyesi=yuksek` | %41.0 | %38.4 | **-2.6** | 461 |
| `yas_grubu=yetiskin` | %57.0 | %53.7 | **-3.3** | 646 |
| `siddet_seviyesi=orta` | %67.1 | %63.6 | **-3.5** | 803 |
| `evre=tolerans` | %51.2 | %46.4 | **-4.8** | 565 |
| `profil=mavi_yakali` | %15.2 | %10.3 | **-4.9** | 89 |
| `bagimlilik_turu=tutun` | %27.8 | %22.3 | **-5.5** | 242 |

⚠️ **6 satır ÇOĞUNLUK sınıfı** (`risk_seviyesi=orta`, `motivasyon_evresi=dusunme`, `evre=tolerans`, `yas_grubu=yetiskin`, `siddet_seviyesi=orta`, `stres_tipi=yok`): havuz payı %40'ın üstünde olan bir değerde 3-7 puanlık fark oransal olarak küçüktür ve hedeflemeye değmez. ➡️ *Mutlak puan eşiği büyük sınıflarda yanıltır; eylenebilir açıklar AZINLIK sınıflarındakilerdir.*

## 3. ⚠️ Üretilebilir havuzun kriz içeriği

| | |
|---|---:|
| kalan tohum | 1313 |
| ⛔ SERT (üretime giremez) | **39** |
| üretilebilir | **1274** |
| ⚠️ bunlardan kriz İÇERİĞİ işareti taşıyan | **50** (%3.9) |

⚠️ K52: *«kriz içeriği etikete güvenilerek elenemez»* ⇒ içerik taraması SERT sınıftan sonra da koşuluyor. Bu işaretler **elenmez, raporlanır** (PERSONA ayrımı, `tohum-beyan-kriz-kapisi` §2): eleme borç/tefeci eksenini tamamen kaybettirirdi ve §8b yönlendirmesi en çok orada önem taşıyor.

## ⛔ Bu envanterin söylemedikleri

| | |
|---|---|
| ⛔ **-100 puanlık eşik SEÇİLDİ** | türetilmedi; bu benim önerim |
| ⛔⛔ **Kapsama ≠ kalite** | bir eksenin payını havuza eşitlemek o eksende iyi kayıt üretileceğini göstermez |
| ⛔⛔ **T132 hâlâ geçerli** | kapsama açığını kapatmak da «daha çok veri»dir; güvenlik kapısını açacağına dair bir kanıt YOK |
| ⛔ **Eksenler bağımsız sayıldı** | birlikte dağılım (hücre düzeyi) bakılmadı; T94 tam bunun bedelini ölçmüştü ⇒ parti planı ızgarayı kısıtla kurmalı, marjinalleri ayrı ayrı değil |
