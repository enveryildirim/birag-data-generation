# Sıradaki parti neyi kapatmalı — kapsama açığı envanteri

**Betik:** `scripts/analiz/2026-09-20-kapsama-acigi-envanteri.py` · **Tarih:** 2026-09-20  
**Havuz:** `data/seeds.v2.jsonl` **2240** tohum · üretilmiş **985** (%44) · kalan **1255**

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
| `senaryo=rol_siniri` | %19.1 | %21.4 | **+2.3** | 274 |
| `bagimlilik_turu=receteli_ilac` | %16.4 | %18.8 | **+2.3** | 258 |
| `bagimlilik_turu=kumar` | %20.9 | %23.2 | **+2.3** | 275 |
| `yas_grubu=ergen` | %9.4 | %11.4 | **+2.0** | 163 |
| `stres_tipi=yalnizlik` | %1.6 | %3.5 | **+1.9** | 62 |
| `siddet_seviyesi=agir` | %20.8 | %22.5 | **+1.7** | 261 |
| `motivasyon_evresi=hazirlik` | %10.5 | %12.1 | **+1.6** | 167 |
| `evre=dibe_vurma` | %9.1 | %10.7 | **+1.6** | 111 |
| `profil=ev_kadini` | %6.9 | %8.5 | **+1.6** | 122 |
| `bagimlilik_turu=dijital` | %7.3 | %8.9 | **+1.6** | 128 |
| `evre=birakma_cabasi` | %10.2 | %11.6 | **+1.5** | 160 |
| `stres_tipi=yok` | %73.6 | %75.0 | **+1.4** | 935 |
| `risk_seviyesi=orta` | %53.6 | %54.9 | **+1.3** | 702 |
| `profil=lise_ergeni` | %11.2 | %12.5 | **+1.3** | 170 |
| `evre=nuksetme` | %9.1 | %10.3 | **+1.1** | 140 |
| `profil=yeni_ebeveyn` | %7.4 | %8.5 | **+1.1** | 117 |
| `profil=emekli_yasli` | %12.4 | %13.4 | **+1.0** | 178 |
| `risk_seviyesi=cok_yuksek` | %0.0 | %0.9 | **+0.9** | 0 |
| `profil=diger` | %0.9 | %1.8 | **+0.9** | 31 |
| `stres_tipi=saglik_kaygisi` | %1.8 | %2.6 | **+0.8** | 31 |
| `yas_grubu=yasli` | %8.0 | %8.7 | **+0.7** | 116 |
| `siddet_seviyesi=hafif` | %13.1 | %13.8 | **+0.7** | 181 |
| `senaryo=kriz` | %1.2 | %1.8 | **+0.6** | 18 |
| `motivasyon_evresi=eylem` | %3.1 | %3.8 | **+0.6** | 44 |
| `yas_grubu=orta_yas` | %9.1 | %9.7 | **+0.6** | 128 |
| `senaryo=kayma_nuks` | %0.0 | %0.4 | **+0.4** | 0 |
| `stres_tipi=yas_kayip` | %0.5 | %0.9 | **+0.4** | 5 |
| `evre=merak_deneme` | %6.0 | %6.2 | **+0.3** | 81 |
| `profil=universite_ogrencisi` | %12.4 | %12.5 | **+0.1** | 148 |
| `stres_tipi=aile_catismasi` | %3.0 | %3.2 | **+0.1** | 41 |
| `senaryo=inkar` | %0.9 | %0.9 | **-0.0** | 11 |
| `senaryo=discord` | %0.4 | %0.4 | **+0.0** | 6 |
| `stres_tipi=akran_baskisi` | %2.2 | %2.2 | **-0.0** | 28 |
| `stres_tipi=sosyal_karsilastirma` | %1.0 | %1.0 | **+0.0** | 13 |
| `evre=sosyal_kullanim` | %5.0 | %4.9 | **-0.1** | 61 |
| `stres_tipi=fiziksel_yorgunluk` | %1.6 | %1.5 | **-0.1** | 18 |
| `stres_tipi=kronik_agri` | %0.5 | %0.4 | **-0.1** | 5 |
| `profil=kronik_issiz` | %8.2 | %8.0 | **-0.2** | 79 |
| `stres_tipi=None` | %1.8 | %1.6 | **-0.3** | 17 |
| `senaryo=nazikce_karsi_cikma` | %14.5 | %14.1 | **-0.5** | 171 |
| `yas_grubu=genc_yetiskin` | %17.2 | %16.4 | **-0.7** | 189 |
| `stres_tipi=akademik_stres` | %4.1 | %3.4 | **-0.7** | 36 |
| `stres_tipi=ekonomik_baski` | %1.5 | %0.8 | **-0.7** | 3 |
| `risk_seviyesi=dusuk` | %6.6 | %5.8 | **-0.8** | 65 |
| `motivasyon_evresi=on_dusunme` | %17.9 | %17.0 | **-0.9** | 204 |
| `evre=inkar` | %10.9 | %9.8 | **-1.0** | 113 |
| `bagimlilik_turu=alkol` | %28.0 | %26.8 | **-1.2** | 324 |
| `motivasyon_evresi=dusunme` | %68.5 | %67.2 | **-1.3** | 801 |
| `stres_tipi=is_stresi` | %3.8 | %2.4 | **-1.3** | 17 |
| `senaryo=ambivalans` | %38.7 | %37.3 | **-1.4** | 453 |
| `risk_seviyesi=yuksek` | %39.8 | %38.4 | **-1.4** | 449 |
| `stres_tipi=ritüel_bagimliligi` | %2.8 | %1.5 | **-1.4** | 5 |
| `senaryo=belirsiz` | %25.2 | %23.7 | **-1.5** | 283 |
| `profil=beyaz_yakali` | %26.2 | %24.6 | **-1.6** | 283 |
| `yas_grubu=yetiskin` | %56.2 | %53.7 | **-2.5** | 620 |
| `siddet_seviyesi=orta` | %66.1 | %63.6 | **-2.5** | 774 |
| `evre=tolerans` | %49.7 | %46.4 | **-3.3** | 550 |
| `profil=mavi_yakali` | %14.4 | %10.3 | **-4.1** | 88 |
| `bagimlilik_turu=tutun` | %27.3 | %22.3 | **-5.0** | 231 |

⚠️ **6 satır ÇOĞUNLUK sınıfı** (`risk_seviyesi=orta`, `motivasyon_evresi=dusunme`, `evre=tolerans`, `yas_grubu=yetiskin`, `siddet_seviyesi=orta`, `stres_tipi=yok`): havuz payı %40'ın üstünde olan bir değerde 3-7 puanlık fark oransal olarak küçüktür ve hedeflemeye değmez. ➡️ *Mutlak puan eşiği büyük sınıflarda yanıltır; eylenebilir açıklar AZINLIK sınıflarındakilerdir.*

## 3. ⚠️ Üretilebilir havuzun kriz içeriği

| | |
|---|---:|
| kalan tohum | 1255 |
| ⛔ SERT (üretime giremez) | **39** |
| üretilebilir | **1216** |
| ⚠️ bunlardan kriz İÇERİĞİ işareti taşıyan | **50** (%4.1) |

⚠️ K52: *«kriz içeriği etikete güvenilerek elenemez»* ⇒ içerik taraması SERT sınıftan sonra da koşuluyor. Bu işaretler **elenmez, raporlanır** (PERSONA ayrımı, `tohum-beyan-kriz-kapisi` §2): eleme borç/tefeci eksenini tamamen kaybettirirdi ve §8b yönlendirmesi en çok orada önem taşıyor.

## ⛔ Bu envanterin söylemedikleri

| | |
|---|---|
| ⛔ **-100 puanlık eşik SEÇİLDİ** | türetilmedi; bu benim önerim |
| ⛔⛔ **Kapsama ≠ kalite** | bir eksenin payını havuza eşitlemek o eksende iyi kayıt üretileceğini göstermez |
| ⛔⛔ **T132 hâlâ geçerli** | kapsama açığını kapatmak da «daha çok veri»dir; güvenlik kapısını açacağına dair bir kanıt YOK |
| ⛔ **Eksenler bağımsız sayıldı** | birlikte dağılım (hücre düzeyi) bakılmadı; T94 tam bunun bedelini ölçmüştü ⇒ parti planı ızgarayı kısıtla kurmalı, marjinalleri ayrı ayrı değil |
