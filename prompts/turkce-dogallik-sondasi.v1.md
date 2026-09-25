# Türkçe doğallık sondası — v1

Sana **tek bir Türkçe metin** verilecek. Görevin onu puanlamak DEĞİL.

Tek soru şu: metinde **ana dili Türkçe olan birinin yazmayacağı** bir yapı var mı?

Kural:
- Varsa, o parçayı **metinden birebir alıntıla** ve doğal karşılığını yaz.
- Yoksa `dogal_olmayan: false` de ve alıntı alanını boş bırak.
- **Üslup tercihi kusur değildir.** Resmî/samimi, uzun/kısa, diyalog/açıklama —
  hiçbiri tek başına sorun sayılmaz. Yalnızca Türkçenin kurallarına ya da
  yerleşik kullanımına aykırı olan şeyi işaretle.
- Konu, doğruluk, bilgi düzeyi seni ilgilendirmiyor. **Yalnızca dil.**
- Emin değilsen `false` de. Şüpheli olanı işaretleme.

Örnekler:
- `"Sana özledim"` → kusur. Doğalı: `"Seni özledim"` (özlemek belirtme hâli ister).
- `"Bir kitap okumayı seviyorum"` → kusur değil, doğal.
- `"Üç gündür içmiyorum."` → kusur değil.

Yalnızca şu JSON'u döndür, başka hiçbir şey yazma:

```json
{
  "dogal_olmayan": true,
  "alinti": "metinden birebir alınmış parça",
  "dogal_hali": "aynı şeyin doğal Türkçesi",
  "tur": "ek_hatasi | sozcuk_secimi | soz_dizimi | ceviri_kokusu | diger"
}
```

METİN:
