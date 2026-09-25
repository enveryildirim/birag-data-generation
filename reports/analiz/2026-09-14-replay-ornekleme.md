# Replay dilimi — örnekleme raporu

**Çıktı:** `data/candidates/replay-v1.jsonl` · SHA256 `d543e8c66edbb855a59077968013a96e90ad918615808dbcb5da068b04809be4`  
**Betik:** `scripts/analiz/2026-09-14-replay-ornekleme.py` · **Tarih:** 2026-09-14 · **Rastgele tohum:** 915  

**Kayıt:** 18 — mevcut korpus 104 kayıt, karışımda replay payı **%15** (plan.md §6 hedefi %15)

---

## 1. Kaynaklar ve köken

> Kullanıcı kararı (2026-09-14): **yalnızca Apache-2.0**. Lisanslar HF etiketinden değil **kart verisinden** doğrulandı.

| Kaynak | Dosya | Lisans | Dil | Ham kayıt | Kalite süzgecinden geçen | Dosya SHA256 |
|---|---|---|---|---:|---:|---|
| `TFLai/Turkish-Alpaca` | `data.json` | apache-2.0 | tr | 51914 | 50509 | `f1aed098ae68849a…` |
| `merve/turkish_instructions` | `instructions.csv` | apache-2.0 | tr | 51563 | 49727 | `3e44fcbd3cc00dff…` |
| `OpenAssistant/oasst2` | `2023-11-05_oasst2_ready.messages.jsonl.gz` | apache-2.0 | en | 5411 | 5216 | `a9f240c4c77aa137…` |

## 2. plan.md §"Replay çeşitlilik ekseni" karşılanıyor mu

| Eksen | Durum |
|---|---|
| genel kültür ve mantık | ✅ üç kaynak da talimat-cevap |
| kısa / thinking'siz yanıtlar | ✅ `has_thinking` **hepsi False**; kısa bant 4/18 |
| İngilizce örnekler | ✅ 5/18 (oasst2, insan yazımı) |
| uzun-form yanıtlar | ✅ uzun bant 6/18 |
| farklı system prompt'lar | ✅ 8 farklı (biri BOŞ — system mesajı olmayan varyant) |

## 3. Dağılımlar

| Ölçüm | Değer | Hedef |
|---|---|---|
| Türkçe | 13 (%72) | %70 *(bizim önerimiz)* |
| İngilizce | 5 (%28) | %30 *(bizim önerimiz)* |
| kısa (<80 kr) | 4 | %25 |
| orta (80-400) | 8 | %50 |
| uzun (400+) | 6 | %25 |

## 4. ⚠️ Bilinen kalite sorunları — veri kartına girmeli

- **Türkçe kaynakların ikisi de makine çevirisi Alpaca türevi.** Ölçüldü: iki kümenin talimatları yalnızca **%13** örtüşüyor (farklı çeviriler), yani birbirinin kopyası değiller; ama ikisi de aynı İngilizce kaynaktan geliyor.
- **Çeviri kusurları elenemiyor.** Girdisi düşmüş (cevaplanamaz) kayıtlar süzüldü (kaynakta %3-4), ama *"Sana özledim"* gibi hatalı Türkçe otomatik ayıklanamıyor. Bu projede dil doğallığı ana kalite ekseni (K48, §5d) olduğu için bu bir **gerilim**: replay genel yeteneği korurken Türkçe doğallığa zarar verebilir. Ölçülmedi.
- **oasst2'de Türkçe pratikte yok:** 135.174 mesajın **37'si** Türkçe. Bu yüzden oasst2 yalnızca İngilizce ekseni için kullanıldı.
- **System prompt'lar kaynakta yok, bu betikte üretildi.** Beşinci çeşitlilik ekseni başka türlü karşılanamıyordu.

