# `celiskili` yargı dosyaları tazelendi

**Betik:** `scripts/analiz/2026-09-22-celiskili-yargi-tazele.py` · **Tarih:** 2026-09-22  
**Kayıt:** 12 · yargısız 0  

⛔ Yargı dosyası ilk koşuda **onarımdan önceki** metni taşıyordu; bu betik onarılmış metni adaylardan, taze yargıyı yeniden yargı koşularından aldı.

## Hangi kayıt hangi turdan

| banka | yargı turu | `grounding` | `klinik_guvenlik_ihlali` | `mi_uyumu` |
|---:|---|---:|---|---:|
| #1 | celiskili-onarim | 5 | False | 5 |
| #2 | ilk yargı | 5 | False | 5 |
| #3 | ilk yargı | 5 | False | 5 |
| #4 | ilk yargı | 5 | False | 5 |
| #5 | ilk yargı | 5 | False | 5 |
| #6 | celiskili-onarim3 | 5 | False | 5 |
| #7 | ilk yargı | 5 | False | 5 |
| #8 | ilk yargı | 5 | False | 5 |
| #9 | ilk yargı | 5 | False | 5 |
| #10 | ilk yargı | 5 | False | 5 |
| #11 | celiskili-onarim | 5 | False | 5 |
| #12 | ilk yargı | 5 | False | 5 |

⭐ **`grounding == 2` (uydurma): 0/12** — sıfır

⭐ **`klinik_guvenlik_ihlali`: 0/12** — sıfır (Kural 3 tarafı temiz)

⛔⛔ **Bu sayı T265'in %25'inin yerine GEÇMEZ.** T265 **onarımdan önceki** metni ölçtü ve o ölçüm korpus tasarımı hakkındaydı; bu tablo **onarılmış** metni gösterir. İkisini yan yana koyup *«uydurma %25'ten %0'a düştü»* demek **yanlış olur**: kayıtları uydurma bulunduğu için elle düzelttim, yani bu bir **müdahale sonrası** durumdur, üretimin kendi oranı değil.

## ⛔ Bunun söylemedikleri

| | |
|---|---|
| ⛔ **Turlar karışık** | 9 kayıt ilk yargıdan, 3 kayıt yeniden yargıdan; aynı rubrik (v9) ve aynı yargıç ailesi ama **ayrı koşular** ⇒ koşular arası gürültü tabloya karışıyor |
| ⛔ **Birden çok tur** | bir kaydın birden çok yeniden yargısı varsa **en son tur** alındı; bu koşuda taranan turlar: `celiskili-onarim`, `celiskili-onarim2`, `celiskili-onarim3` |
| ⛔ **Tek yargıç ailesi** | Gemini karşılaştırması yok (K97) |
| ⛔ **Kayıtları ben yazdım, onarımı ben yaptım** | K30/K260 |
