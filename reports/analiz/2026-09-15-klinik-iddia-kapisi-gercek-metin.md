# Klinik-iddia kapısı gerçek kurumsal metne uygulanınca ne oluyor?

**Girdi:** `docs/arastirma-notlari.md` (BÖLÜM K) · SHA256 `e7b4227d9d2a95b0b60ee24ba9eb7a24c0ad835fe665682d368403e74ccf7533`  
**Betik:** `scripts/analiz/2026-09-15-klinik-iddia-kapisi-gercek-metin.py` · **Tarih:** 2026-09-15

---

## 1. Soru

`uretim-v3` §7b-2 *"pasaj klinik iddia taşımaz"* diyor; `src/checks.py::KLINIK_IDDIA`
bunu anahtar kelimeyle denetliyor. Kural **sentetik** pasaj için yazıldı (K74).
A katmanı korpusu geldiğinde aynı kapı **gerçek** kurum belgelerine de uygulanacak:
`context_ok` yalnızca §7b-1'i (kaynak adı büyük harf) `sentetik` bayrağına göre ayırıyor,
§7b-2'yi **her bağlam girdisine** uyguluyor.

## 2. Ölçüm

- İncelenen içerik satırı: **22**
- Kapıya takılan: **7** (%32)

| eşleşen sözcük | kaç satırda |
|---|---|
| `tedavi` | 5 |
| `tanı` | 1 |
| `iyileşme` | 1 |

### Takılan satırlar

| eşleşen | satır |
|---|---|
| `tedavi` | \| **AMATEM** \| Alkol ve Madde Bağımlıları Tedavi Merkezi — yetişkin \| Yataklı ve ayaktan; hastane bünyesind |
| `tedavi` | \| **ÇEMATEM** \| Çocuk ve Ergen Madde Bağımlıları Tedavi Merkezi \| 18 yaş altı ayrı sistem \| |
| `tedavi` | \| **YEDAM** \| Yeşilay Danışmanlık Merkezi — STK \| Danışmanlık, tedavi değil. Erişimi daha kolay, damgalanma |
| `tedavi` | \| **Denetimli Serbestlik Müdürlüğü** \| Adalet Bakanlığı — zorunlu takip \| Tedavi değil, **denetim** \| |
| `tedavi` | Tedavi       : otomatik değil — savcı veya müdürlük "gerek görürse" AMATEM/ÇEMATEM'e sevk |
| `tanı` | \| Sistem kaygısı \| *"İmzaya gitmedim, ne olur?"* \| Yatıştırıcı yalan (*"bir şey olmaz"*) veya korkutma \| B |
| `iyileşme` | \| Performatif iyileşme \| Söylediği ile yaşadığı arasında fark \| Yüzeysel change talk'u gerçek sanmak \| Bas |

## 3. Okuma

Eşleşmelerin çoğu **klinik iddia değil**; kapının K65 ailesinden bir yanlış pozitifi:

- `tedavi` — kurumun **kendi adının** içinde geçiyor (*Alkol ve Madde Bağımlıları
  **Tedavi** Merkezi*). A katmanının her belgesi bu adı taşır.
- `tanı` — *"kaygıyı **tanı**"* buyruk kipi; teşhis değil, eşsesli.
- `iyileşme` — davranış tarifinde geçiyor (*performatif iyileşme*), iddia olarak değil.

## 4. Sonuç

Kapı **sentetik pasaj için doğru, gerçek belge için fazla geniş.** A katmanı
korpusu bugünkü hâliyle `context_ok`'tan geçirilirse kurum adı taşıyan her pasaj
elenir. Düzeltme yönü §7b-1'in deseniyle aynı: kapı `sentetik` bayrağına göre
ayrılmalı ve gerçek pasajda **iddia cümlesi** aranmalı (sözcük varlığı değil).

⚠️ **Sınır:** vekil ölçüm. Girdi markdown tablo satırı, kurum belgesi paragrafı
değil; **oran** gerçek korpusa taşınmaz. Taşınan şey kapının hangi sözcükten
ateşlediği. Gerçek oran, A katmanı pilotunun ilk partisinde ölçülmeli.
