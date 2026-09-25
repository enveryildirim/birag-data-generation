# Sıradaki parti neyi kapatmalı — kapsama açığı envanteri

**Betik:** `scripts/analiz/2026-09-20-kapsama-acigi-envanteri.py` · **Tarih:** 2026-09-20  
**Havuz:** `data/seeds.v2.jsonl` **2240** tohum · üretilmiş **867** (%39) · kalan **1373**

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
| `stres_tipi=yok` | %71.5 | %75.0 | **+3.4** | 1040 |
| `risk_seviyesi=orta` | %51.7 | %54.9 | **+3.2** | 782 |
| `bagimlilik_turu=receteli_ilac` | %15.6 | %18.8 | **+3.2** | 285 |
| `bagimlilik_turu=kumar` | %20.3 | %23.2 | **+2.9** | 305 |
| `siddet_seviyesi=hafif` | %11.3 | %13.8 | **+2.5** | 212 |
| `evre=nuksetme` | %8.0 | %10.3 | **+2.3** | 161 |
| `evre=dibe_vurma` | %8.5 | %10.7 | **+2.2** | 127 |
| `motivasyon_evresi=hazirlik` | %9.9 | %12.1 | **+2.1** | 184 |
| `senaryo=rol_siniri` | %19.4 | %21.4 | **+2.0** | 294 |
| `evre=birakma_cabasi` | %9.6 | %11.6 | **+2.0** | 177 |
| `profil=yeni_ebeveyn` | %6.5 | %8.5 | **+2.0** | 134 |
| `siddet_seviyesi=agir` | %20.5 | %22.5 | **+2.0** | 288 |
| `yas_grubu=ergen` | %9.6 | %11.4 | **+1.9** | 173 |
| `stres_tipi=yalnizlik` | %1.6 | %3.5 | **+1.9** | 64 |
| `profil=ev_kadini` | %6.7 | %8.5 | **+1.8** | 132 |
| `bagimlilik_turu=dijital` | %7.2 | %8.9 | **+1.8** | 138 |
| `profil=lise_ergeni` | %10.8 | %12.5 | **+1.7** | 186 |
| `evre=merak_deneme` | %4.7 | %6.2 | **+1.5** | 99 |
| `profil=universite_ogrencisi` | %11.1 | %12.5 | **+1.4** | 174 |
| `risk_seviyesi=cok_yuksek` | %0.0 | %0.9 | **+0.9** | 0 |
| `profil=emekli_yasli` | %12.5 | %13.4 | **+0.9** | 192 |
| `profil=diger` | %0.9 | %1.8 | **+0.9** | 32 |
| `yas_grubu=genc_yetiskin` | %15.6 | %16.4 | **+0.9** | 223 |
| `motivasyon_evresi=eylem` | %3.0 | %3.8 | **+0.8** | 49 |
| `stres_tipi=saglik_kaygisi` | %2.0 | %2.6 | **+0.7** | 32 |
| `senaryo=nazikce_karsi_cikma` | %13.6 | %14.1 | **+0.5** | 196 |
| `yas_grubu=orta_yas` | %9.2 | %9.7 | **+0.5** | 138 |
| `yas_grubu=yasli` | %8.2 | %8.7 | **+0.5** | 124 |
| `senaryo=kriz` | %1.4 | %1.8 | **+0.4** | 18 |
| `senaryo=kayma_nuks` | %0.0 | %0.4 | **+0.4** | 0 |
| `senaryo=ambivalans` | %37.0 | %37.3 | **+0.3** | 513 |
| `profil=kronik_issiz` | %7.7 | %8.0 | **+0.3** | 93 |
| `stres_tipi=yas_kayip` | %0.6 | %0.9 | **+0.3** | 5 |
| `stres_tipi=aile_catismasi` | %3.1 | %3.2 | **+0.1** | 44 |
| `senaryo=discord` | %0.5 | %0.4 | **-0.0** | 6 |
| `senaryo=inkar` | %1.0 | %0.9 | **-0.1** | 11 |
| `stres_tipi=sosyal_karsilastirma` | %1.2 | %1.0 | **-0.1** | 13 |
| `stres_tipi=kronik_agri` | %0.6 | %0.4 | **-0.1** | 5 |
| `evre=sosyal_kullanim` | %5.2 | %4.9 | **-0.3** | 65 |
| `stres_tipi=akran_baskisi` | %2.5 | %2.2 | **-0.3** | 28 |
| `stres_tipi=fiziksel_yorgunluk` | %1.8 | %1.5 | **-0.3** | 18 |
| `stres_tipi=None` | %2.0 | %1.6 | **-0.4** | 18 |
| `stres_tipi=akademik_stres` | %4.0 | %3.4 | **-0.6** | 41 |
| `risk_seviyesi=dusuk` | %6.6 | %5.8 | **-0.8** | 73 |
| `stres_tipi=ekonomik_baski` | %1.7 | %0.8 | **-0.9** | 3 |
| `motivasyon_evresi=dusunme` | %68.5 | %67.2 | **-1.3** | 882 |
| `motivasyon_evresi=on_dusunme` | %18.6 | %17.0 | **-1.6** | 219 |
| `evre=inkar` | %11.5 | %9.8 | **-1.7** | 120 |
| `bagimlilik_turu=alkol` | %28.5 | %26.8 | **-1.7** | 353 |
| `stres_tipi=is_stresi` | %4.2 | %2.4 | **-1.7** | 18 |
| `stres_tipi=ritüel_bagimliligi` | %3.2 | %1.5 | **-1.8** | 5 |
| `profil=beyaz_yakali` | %27.6 | %24.6 | **-3.0** | 302 |
| `senaryo=belirsiz` | %27.1 | %23.7 | **-3.4** | 296 |
| `risk_seviyesi=yuksek` | %41.8 | %38.4 | **-3.4** | 479 |
| `yas_grubu=yetiskin` | %57.4 | %53.7 | **-3.7** | 676 |
| `siddet_seviyesi=orta` | %68.2 | %63.6 | **-4.6** | 834 |
| `profil=mavi_yakali` | %16.3 | %10.3 | **-6.0** | 89 |
| `evre=tolerans` | %52.5 | %46.4 | **-6.1** | 585 |
| `bagimlilik_turu=tutun` | %28.5 | %22.3 | **-6.2** | 253 |

⚠️ **6 satır ÇOĞUNLUK sınıfı** (`risk_seviyesi=orta`, `motivasyon_evresi=dusunme`, `evre=tolerans`, `yas_grubu=yetiskin`, `siddet_seviyesi=orta`, `stres_tipi=yok`): havuz payı %40'ın üstünde olan bir değerde 3-7 puanlık fark oransal olarak küçüktür ve hedeflemeye değmez. ➡️ *Mutlak puan eşiği büyük sınıflarda yanıltır; eylenebilir açıklar AZINLIK sınıflarındakilerdir.*

## 3. ⚠️ Üretilebilir havuzun kriz içeriği

| | |
|---|---:|
| kalan tohum | 1373 |
| ⛔ SERT (üretime giremez) | **39** |
| üretilebilir | **1334** |
| ⚠️ bunlardan kriz İÇERİĞİ işareti taşıyan | **53** (%4.0) |

⚠️ K52: *«kriz içeriği etikete güvenilerek elenemez»* ⇒ içerik taraması SERT sınıftan sonra da koşuluyor. Bu işaretler **elenmez, raporlanır** (PERSONA ayrımı, `tohum-beyan-kriz-kapisi` §2): eleme borç/tefeci eksenini tamamen kaybettirirdi ve §8b yönlendirmesi en çok orada önem taşıyor.

## ⛔ Bu envanterin söylemedikleri

| | |
|---|---|
| ⛔ **-100 puanlık eşik SEÇİLDİ** | türetilmedi; bu benim önerim |
| ⛔⛔ **Kapsama ≠ kalite** | bir eksenin payını havuza eşitlemek o eksende iyi kayıt üretileceğini göstermez |
| ⛔⛔ **T132 hâlâ geçerli** | kapsama açığını kapatmak da «daha çok veri»dir; güvenlik kapısını açacağına dair bir kanıt YOK |
| ⛔ **Eksenler bağımsız sayıldı** | birlikte dağılım (hücre düzeyi) bakılmadı; T94 tam bunun bedelini ölçmüştü ⇒ parti planı ızgarayı kısıtla kurmalı, marjinalleri ayrı ayrı değil |
