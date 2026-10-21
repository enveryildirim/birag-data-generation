# Ölçek-5k — sonuç

- Betik: `scripts/analiz/2026-10-20-olcek5k-toplu.py` · plan `data/plan/olcek5k.jsonl` `922926a97588363c`
- Çıktı: `data/candidates/olcek5k.jsonl` `a78055098e7201a6` — **5680 kayıt**
- Planlanan 5700 · C'si bitmemiş parça 0
- Birleştirmede `run_checks` reddi: 0

## C kararları

| karar | satır |
|---|---:|
| aynen | 3982 |
| duzeltildi | 1698 |
| dusuruldu | 20 |

### C modeline göre (Sonnet 1–13 · Haiku 14–228)

| C modeli | parça | aynen | duzeltildi | dusuruldu | düzeltme+düşürme % |
|---|---:|---:|---:|---:|---:|
| claude-haiku-5-5 | 215 | 3860 | 1500 | 15 | %28.2 |
| claude-sonnet-5-5 | 13 | 122 | 198 | 5 | %62.5 |

## C düzeltme / düşürme sebepleri (ilk sözcük öbeği)

| sebep | n |
|---|---:|
| yanlış okuma | 241 |
| dil | 229 |
| uydurma | 149 |
| güvenlik | 110 |
| yanlis_okuma | 100 |
| guvenlik | 51 |
| yanlis okuma | 28 |
| rol sınırı | 21 |
| yöntem sızıntısı | 19 |
| sızıntı | 14 |
| atıf | 12 |
| thinking | 11 |
| yanlis | 11 |
| uydurma duygu | 10 |
| bağlam | 10 |
| sızıntı/uydurma | 9 |
| §8b′ | 9 |
| yontem_sizintisi | 9 |
| yorum | 8 |
| sızıntı/duygu | 8 |
| sizinti | 8 |
| atfetme | 8 |
| uzunluk | 8 |
| kriz içeriği | 7 |
| olmayan duygu | 7 |

## Dağılım

| alan | dağılım |
|---|---|
| turn_ending | acik_uclu_soru 3370 · yalnizca_yansitma 747 · ozet 676 · takdir 653 · durur 234 |
| sinir_tipi | yok 3774 · rol_siniri_yonlendirme 1171 · yonlendirme_istegi 388 · yonlendirme_gereksiz 191 · sinir_cekme 156 |
| güvenlik sapması | yok 4495 · var 1185 |
| sızıntı şüphesi kaldı | hayır 5528 · evet 152 |
| tur | alkol 1530 · tutun 1270 · kumar 1267 · receteli_ilac 1082 · dijital 531 |
| yas | yetiskin 4996 · ergen 684 |
| turn_type | single 3448 · multi 2232 |
| slice | terapotik_tek_tur 2320 · terapotik_cok_tur 1904 · rag_tek_tur 1128 · rag_cok_tur 328 |
| tohum önceden kullanılmış | True 5680 |

## Şablon (kayıt başına, bütün korpus)

| kalıp | n | % |
|---|---:|---:|
| «… adım gibi duruyor / adım olabilir» | 0 | %0.0 |
| «yazman / anlatman … önemli» | 16 | %0.3 |
| «kolay olmamıştır / kolay olmaz» | 1 | %0.0 |
| «… duyuyorum» | 20 | %0.4 |
| «karar sende / senin kararın» | 54 | %1.0 |
| «hüküm ver… / bana düşmez» | 310 | %5.5 |
| «adlandırıyorum / adıyla anıyorum» | 0 | %0.0 |

Çok turlu açılış: 2232 kayıtta 2229 farklı açılış; en sık: «bu alişkanlik ne zamandir sürü»×2 · «sevgilinin bu sözü seni nasil »×2 · «eşinin bu gece söylediği şey s»×2 · «oğlunun senin için baktiği yer»×1 · «hazirliğin iyi olduğu hâlde ka»×1

8 sözcüklük dizi tekrarı (parçalar arası): 795 dizi; en sık: «bir hekim ya da bağimlilik alaninda çalişan bir»×15 · «bir hekimle ya da bağimlilik alaninda çalişan bir»×15 · «bağimlilik alaninda çalişan bir danişmanlik merkezi ya da»×13 · «alaninda çalişan bir danişmanlik merkezi ya da bir»×10 · «ne yapacağina sen karar verirsin ben senin yerine»×8
