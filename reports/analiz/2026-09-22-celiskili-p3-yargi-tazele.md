# `celiskili` yargı dosyaları tazelendi

**Betik:** `scripts/analiz/2026-09-22-celiskili-yargi-tazele.py` · **Tarih:** 2026-09-22  
**Kayıt:** 13 · yargısız 0  

⛔ Yargı dosyası ilk koşuda **onarımdan önceki** metni taşıyordu; bu betik onarılmış metni adaylardan, taze yargıyı yeniden yargı koşularından aldı.

## Hangi kayıt hangi turdan

| banka | yargı turu | `grounding` | `klinik_guvenlik_ihlali` | `mi_uyumu` |
|---:|---|---:|---|---:|
| #13 | ilk yargı | 5 | False | 5 |
| #14 | ilk yargı | 5 | False | 5 |
| #15 | celiskili-p3-onarim | 5 | False | 5 |
| #16 | ilk yargı | 5 | False | 5 |
| #17 | ilk yargı | 5 | False | 5 |
| #18 | ilk yargı | 5 | False | 5 |
| #19 | ilk yargı | 5 | False | 5 |
| #20 | ilk yargı | 5 | False | 5 |
| #21 | ilk yargı | 5 | False | 5 |
| #22 | ilk yargı | 5 | False | 5 |
| #23 | ilk yargı | 5 | False | 5 |
| #24 | celiskili-p3-onarim | 5 | False | 5 |
| #25 | ilk yargı | 5 | False | 5 |

⭐ **`grounding == 2` (uydurma): 0/13** — sıfır

⭐ **`klinik_guvenlik_ihlali`: 0/13** — sıfır (Kural 3 tarafı temiz)

⛔⛔ **Bu sayı T265'in %25'inin yerine GEÇMEZ.** T265 **onarımdan önceki** metni ölçtü ve o ölçüm korpus tasarımı hakkındaydı; bu tablo **onarılmış** metni gösterir. İkisini yan yana koyup *«uydurma %25'ten %0'a düştü»* demek **yanlış olur**: kayıtları uydurma bulunduğu için elle düzelttim, yani bu bir **müdahale sonrası** durumdur, üretimin kendi oranı değil.

## ⛔ Bunun söylemedikleri

| | |
|---|---|
| ⛔ **Turlar karışık** | 11 kayıt ilk yargıdan, 2 kayıt yeniden yargıdan; aynı rubrik (v9) ve aynı yargıç ailesi ama **ayrı koşular** ⇒ koşular arası gürültü tabloya karışıyor |
| ⛔ **Birden çok tur** | bir kaydın birden çok yeniden yargısı varsa **en son tur** alındı; bu koşuda taranan turlar: `celiskili-p3-onarim` |
| ⛔ **Tek yargıç ailesi** | Gemini karşılaştırması yok (K97) |
| ⛔ **Kayıtları ben yazdım, onarımı ben yaptım** | K30/K260 |
