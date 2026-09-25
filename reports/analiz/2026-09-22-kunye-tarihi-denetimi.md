# Künye tarihi denetimi — `gen_meta.date` betik adından mı

**Betik:** `scripts/analiz/2026-09-22-kunye-tarihi-denetimi.py` · **Tarih:** 2026-09-22  
**Eşleşen blok:** 47 · **uyuşmayan kayıt (benzersiz):** 0  
**Kip:** yalnız denetim  

⭐ Ölçüt: kaydın `gen_meta.date`'i, onu üreten blok betiğinin **adındaki** tarihe eşit olmalı (K126'nın künyeye uygulanışı).

⭐ **Uyuşmazlık yok.** Bütün kayıtların künye tarihi, kendilerini üreten betiğin adıyla eşleşiyor.

## ⛔ Bu denetimin söylemedikleri

| | |
|---|---|
| ⛔ **Kapı DEĞİL, denetimdir** | bir kaydın hangi betikten geldiği kayıtta yazmıyor; bağ yalnız blok dosyası adından kuruluyor ⇒ `checks.py`'ye kayıt düzeyli kapı olarak konulamaz |
| ⛔ **Betik adı da bir BEYANDIR** | yalnız daha dayanıklı bir beyan: dosya adı commit'te görünür ve K126 onu zaten ölçüt saymıştı. Gerçek üretim anını ölçen şey **git zaman damgasıdır** ve bu denetim onu kullanmıyor |
| ⚠️ **`datasets/` düzeltilmez** | IMMUTABLE; `v0.0.15` ve `v0.0.16` eski tarihleri taşımayı sürdürür |
