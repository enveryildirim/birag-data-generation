#!/usr/bin/env python3
"""datasets/v0.0.4 ve v0.0.5 için CARD.md üretir. Her sayı buradan hesaplanır."""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

KOK = Path(__file__).parent.parent.parent
V3 = KOK / "datasets/v0.0.3/train.jsonl"

METIN = {
    "v0.0.4": ("%10,2", "ORTA nokta", "7"),
    "v0.0.5": ("%24,1", "ÜST nokta", "26"),
}


def say(rs, alan):
    return dict(collections.Counter(r[alan] for r in rs).most_common())


def kart(surum: str) -> str:
    yol = KOK / f"datasets/{surum}/train.jsonl"
    R = [json.loads(l) for l in yol.open()]
    ter = [r for r in R if not r.get("replay")]
    rep = [r for r in R if r.get("replay")]
    yama = [r for r in ter if "doz_yamasi" in (r.get("gen_meta") or {})]
    yon = len(yama) + 7
    oran, rol, nyama = METIN[surum]
    V3R = [json.loads(l) for l in V3.open()]
    ayni = sum(1 for a, b in zip(R, V3R) if a["id"] == b["id"])
    havuz = collections.Counter((r["gen_meta"]["doz_yamasi"]["havuz"]) for r in yama)
    bag = say(yama, "addiction_type")
    yeni_karne = sum(1 for r in ter if (r.get("judge") or {}).get("prompt_version") == "judge-eksen1.v7"
                     and "doz_yamasi" in (r.get("gen_meta") or {}))
    sha = hashlib.sha256(yol.read_bytes()).hexdigest()[:16]
    man = json.loads((KOK / f"datasets/{surum}/manifest.json").read_text())

    return f"""# BıRAG talimat veri seti — {surum}

*Datasheets for Datasets* yapısında (Gebru ve ark.). Bkz. `docs/tez/tez-plani.md` §3.5.

## Motivasyon

**Bu bir sürüm değil, T30'un DOZ-YANIT EĞRİSİ için üretilmiş deney kolu.**

T30 negatif bir sonuç kaydetti: yönlendirme hamlesini korpusa geri koymak ince ayarlı
modelde refleksi geri getirmedi. İki açıklama **ayırt edilemedi** — (a) doz yetersizdi,
(b) ilişki yapısal olarak asimetrik. Ayıracak tek deney doz-yanıt eğrisi. Bu set eğrinin
**{rol}sı**: yönlendirme hamlesi taşıyan kayıt **{yon}/{len(ter)} = {oran}**.

| Nokta | Set | Yönlendirme | Ölçüldü mü |
|---|---|---|---|
| taban | `v0.0.2` | 2/99 = **%2,0** | ✅ (T30) |
| alt | `v0.0.3` | 7/137 = **%5,1** | ✅ (T30/K113) |
| orta | `v0.0.4` | 14/137 = **%10,2** | ⏳ |
| üst | `v0.0.5` | 33/137 = **%24,1** | ⏳ |

⚠️ Taban oranları **T32'de düzeltildi** (0 → 2 ve 5 → 7): K110'un envanteri tarayıcı
olarak eval'in **tıbbi** terim listesini kullanıyordu, *avukat* içinde yoktu ve hukuki
yönlendirme yapan iki kayıt hiç elle okunmadı. Tıbbi eksende v0.0.2 yine **0**'dır.

## ⭐ Tasarım — neden korpus BÜYÜTÜLMEDİ

K113'ün kontrol kolu şunu ölçtü: `A-dar`/v0.0.2/**280** → 2 · `A-dar`/v0.0.3/**280** → 2 ·
`A-dar`/v0.0.3/**372** → 4. Yani **adım sayısı metriği veriden daha çok oynattı.** Korpus
büyüseydi §9'un 3-epoch kuralı adımı da büyütürdü ve eğri okunamazdı.

Bu yüzden **N sabit**: {len(R)} kayıt, üç doz noktasında da aynı. {ayni}/{len(R)} kaydın
`id`'si v0.0.3 ile **aynı sırada aynı**. Replay payı da sabit (**{100*len(rep)/len(R):.1f}%**),
yani Eksen 3'ün ikinci değişkeni donduruldu. **Adım sayısı 372 olarak DEĞİŞMEZ** — doz
kolları `f4b` ailesiyle aynı adımda koşulabilir.

### Manipülasyon: eşleştirilmiş EKLEME, silme yok

{nyama} kaydın son asistan cevabının **içine tek bir yönlendirme cümlesi eklendi**.
Kullanıcı turları, `context`, `source_ids` ve cevabın geri kalanı **bayt bayt aynı**.
Makineyle denetlenen değişmezler (`2026-09-15-doz-yanit-yamala.py`):

| | Değişmez |
|---|---|
| I1 | Kayıt sayısı, id'ler, kullanıcı mesajları, context, source_ids birebir aynı |
| I2 | Eklenen cümle çıkarılınca cevap **orijinaliyle bayt bayt aynı** |
| I3 | Orijinal cevabın **son cümlesi** yeni cevabın da son cümlesi (§5a `turn_ending` korunur) |
| I4 | Eklenen cümlede soru işareti yok → soru sayısı kapısı hiç oynamadı |
| I5 | Rakam yok · kurum özel adı yok · yordam iddiası yok (K18) |
| I6 | `v0.0.4`'ün ekleme kümesi `v0.0.5`'inkinin **öz alt kümesi** — eğri yapıca monoton |

⭐ Bunun ölçüm açısından sonucu: **sınır çekme metninin korpustaki maruziyeti üç dozda da
birebir aynı.** Silinen davranış yok; değişen tek şey, sınırın ardından bir **adım**
gösterilip gösterilmediği — T29'un ayrımı tam olarak budur.

## Bileşim

| Alan | Dağılım |
|---|---|
| Kayıt sayısı | **{len(R)}** (v0.0.3 ile aynı; manifest: {man['n_kept']}/{man['n_total']}) |
| Terapötik / replay | {len(ter)} / {len(rep)} (**{100*len(rep)/len(R):.1f}%**) |
| Yönlendirme hamlesi taşıyan | **{yon}** (**{oran}**) — {len(yama)} yama + 7 mevcut |
| Yamanın havuzu | `sinir_cekme` {havuz.get('sinir',0)} · alan dışı {havuz.get('ek',0)} |
| Yamanın bağımlılık dağılımı | {' · '.join(f'{k} {v}' for k, v in bag.items())} |
| Bağımlılık türü (korpus) | {' · '.join(f'{k} {v}' for k, v in say(ter, 'addiction_type').items())} |
| Senaryo | {' · '.join(f'{k} {v}' for k, v in list(say(ter, 'scenario').items())[:6])} … |
| Kriz | **0** — Kural 3, uzman onayı bekliyor |

## ⚠️ Bilinen açıklar — bu setin ölçtüğü şeyi sınırlar

1. ⚠️ **Yönlendirme dilimi KONUYA ÇARPIK.** Yamanın {bag.get('receteli_ilac',0)}/{len(yama)}'i
   `receteli_ilac`, oysa korpustaki payı %14. Rol sınırı konuşmaları doğal olarak ilaç ve
   hukuk etrafında kümeleniyor. **Bilerek düzeltilmedi:** dengelemek, yönlendirmeyi yeri
   olmayan konuşmalara sokmak (U1'i çiğnemek) demekti. Çarpıklık iki dozda da benzer
   olduğu için *doz* karşılaştırmasını bozmaz, ama **genellemeyi sınırlar**.
2. ⚠️ **Üst nokta %25 değil %24,1.** Uygunluk ölçütü (U1-U7) uygulanınca havuzdan
   {nyama} kayıt çıktı, 27 değil. Sayıyı tutturmak ölçütü sonradan gevşetmek olurdu (T24).
   Elenenlerin hepsi gerekçeli; **üçü**, kaydın KENDİ `thinking`'i yönlendirmeyi bilerek
   yapmadığını yazdığı için elendi.
3. ⚠️ **`sinir_tipi` etiketi kayıyor.** {len(yama)} kayıt `sinir_cekme`'den
   `rol_siniri_yonlendirme`'ye geçti. Defter kaydı değişti, **korpustaki metin değişmedi**
   (I2) — ama etiket üzerinden yapılacak sayımlarda bu akılda tutulmalı.
4. ⚠️ **Eklenen cümleler tek bir elden çıktı ve kalıplaşma riski taşıyor.** Bitiş kalıbı
   dağılımı üretimde denetlendi (hiçbir kalıp {len(yama)//3}'ü aşmıyor), ama üslup
   çeşitliliği yine de {len(yama)} cümlelik bir örnekle sınırlı. Model kalıbı öğrenirse
   `safety_crisis`'in alt-dizge ölçütü bunu **başarı** sayar (T31 ailesi).
5. ⚠️ **Karşı kutup büyütülmedi.** `yonlendirme_gereksiz` iki kayıtta kaldı; doz {oran}'e
   çıkarken karşı kutup sabit. Aşırı yönlendirme bu setle ölçülemez — eval tarafında
   kontrol kutbuna bakılmalı (ve §8b onun kanıt gücünün düştüğünü yazmıştı).
6. **Kriz dilimi yok · vahşi doğa yok · yasadışı madde dilimi yok** (v0.0.3 ile aynı).
7. **Hacim.** {len(R)} kayıt v0.1.0 hedefinin (~800-1.200, K34) beşte biri.

## Toplama süreci

- **Taban korpus:** `datasets/v0.0.3/train.jsonl`
  sha256[:16] `{hashlib.sha256(V3.read_bytes()).hexdigest()[:16]}` — hiçbir kaydı silinmedi.
- **Tasarım ve ölçüt:** `scripts/analiz/2026-09-15-doz-yanit-plan.py` — uygunluk ölçütü
  (U1-U7) ve düzeltme ölçütü (D1-D5) **üretimden önce** yazıldı; elenen 21 adayın hepsi
  gerekçesiyle betikte.
- **Eklemeler:** `data/candidates/doz-yonlendirme-ekleri.jsonl` — {len(yama)} cümle, elle
  yazıldı (K30), bağlamı içinde elle okundu (D5).
- **Judge:** {yeni_karne} yamalı kayıt **yeniden** puanlandı (cevap değiştiği için eski
  karne geçersiz); rubrik **v7**, puanlayan `claude-sonnet-subagent` (K97). Yamasız
  {len(ter)-len(yama)} terapötik kaydın karnesi K112'den **aynen taşındı** — metinleri
  bayt bayt aynı (I2).
- **Kapılar:** `src/checks.py` iki set için de yeniden koşuldu — **{len(R)}/{len(R)} geçti**.

```
scripts/analiz/2026-09-15-yonlendirme-genis-tarama.py   # T32: taban düzeltildi
scripts/analiz/2026-09-15-doz-yanit-plan.py             # ızgara + ölçüt (üretimden ÖNCE)
  -> data/plan/doz-yanit-ekler.jsonl
  (eklemeler elle yazıldı — K30)
  data/candidates/doz-yonlendirme-ekleri.jsonl
scripts/analiz/2026-09-15-doz-yanit-yamala.py           # I1-I6 + kapılar
  -> data/candidates/{surum}-doz{'10' if surum == 'v0.0.4' else '25'}.jsonl
scripts/analiz/2026-09-15-judge-isleri-hazirla.py --korpus <yamalı 26> --etiket doz-yama-v7
scripts/analiz/2026-09-15-judge-sonuclari-topla.py doz-yama-v7 ...
scripts/analiz/2026-09-15-doz-yanit-derleme.py          # karneleri birleştirir
  -> data/judged/{surum}.jsonl
uv run python src/build.py data/judged/{surum}.jsonl {surum}
  datasets/{surum}/train.jsonl                          sha256[:16] {sha}
```

## Kullanım

**Kullanılır:** yalnızca **T30'un doz-yanıt eğrisi**. `v0.0.3` ile **aynı config, aynı
tohum, aynı adım sayısı (372)** koşulur ve `safety_crisis`'te profesyonel desteği hiç
adlandırmayan öğe sayısına bakılır. Üç nokta aynı eksende okunur.
**Kullanılmaz:** kalite iddiası, yayın, judge kalibrasyonu, altın küme, Eksen 3 yorumu.
⚠️ Yönlendirme sayıları **yukarı yönlü güvenilmez** olabilir: `safety_crisis` kabul
listesi düzeltilmeden (T31) kurum özel adı içeren bir cevap da geçer.

## Bakım

`datasets/` IMMUTABLE (Kural 4). Bu dizin bir daha yazılmaz.
"""


def main() -> None:
    for surum in ("v0.0.4", "v0.0.5"):
        d = KOK / "datasets" / surum
        if not d.is_dir():
            raise SystemExit(f"⛔ {d.relative_to(KOK)} yok — önce src/build.py koşulmalı")
        (d / "CARD.md").write_text(kart(surum), encoding="utf-8")
        print(f"yazıldı: datasets/{surum}/CARD.md")


if __name__ == "__main__":
    main()
