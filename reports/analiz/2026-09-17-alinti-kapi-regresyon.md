# Alıntı kapısı — regresyon sınaması

**Betik:** `scripts/analiz/2026-09-17-alinti-kapi-regresyon.py` · **Tarih:** 2026-09-17

⛔ Bir kapı gevşetildiğinde sorulacak soru *«yeni hâli sessiz mi»* değil,
**«eski yakaladıklarını hâlâ yakalıyor mu»**dur.

| # | vaka | beklenen bulgu | çıkan | muafiyet | |
|---:|---|---:|---:|---|---|
| 1 | temel yakalama — olumlu atıf, cümlede mastar yok | 1 | 1 | `—` | ✅ |
| 2 | gerçek karşı olgusal | 0 | 0 | `karsi_olgusal` | ✅ |
| 3 | anma çerçevesi | 0 | 0 | `anma_oneri` | ✅ |
| 4 | öneri çerçevesi | 0 | 0 | `anma_oneri` | ✅ |
| 5 | ⭐ ESKİ KAPININ KAÇIRDIĞI — alakasız mastar muafiyeti ateşliyordu | 1 | 1 | `—` | ✅ |
| 6 | ⭐ EŞLEME — kısa alıntı sonrakini kaydırıyordu | 1 | 1 | `kisa_alinti, karsi_olgusal` | ✅ |
| 7 | ⭐ ADFİİL + İYELİK — olumsuzluk değil (`söylemen` = «senin söylemen») | 1 | 1 | `—` | ✅ |
| 8 | ⭐ EŞGÜDÜMLÜ ANMA — araya bağlaçlı ikinci alıntı giriyor | 0 | 0 | `anma_oneri, anma_oneri` | ✅ |
| 9 | ⭐ OLUMSUZ YETERLİLİK — «diyemem» (de- → di- ses değişimi) | 0 | 0 | `olumsuz_yeterlilik` | ✅ |
| 10 | ⭐ ULAÇ ÇERÇEVESİ — «diyerek … almayacağım» | 0 | 0 | `anma_ulac` | ✅ |
| 11 | ⭐ KARŞILAŞTIRMA — «X ile Y aynı şey değil» | 0 | 0 | `karsilastirma, karsilastirma` | ✅ |
| 12 | ⭐ KARŞIT «değil» — olumsuzluğu söz fiili değil sıfat taşıyor | 0 | 0 | `karsit_degil` | ✅ |

⭐ **12 vakanın 12'ü de beklendiği gibi.**
