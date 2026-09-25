#!/usr/bin/env python3
"""Alt ajana verilecek BLOK TASLAK BRİFİ'ni üretir (K260).

⛔⛔ **K260'ın sınırı:** alt ajan TASLAK yazar. Okuma, kapılar, elle
onaylar, §5a″ sapma hükümleri ve ön tarama Claude Code'da kalır. Bu betik
yalnız brifi kurar; taslağı kayda çeviren ve kapılardan geçiren şey blok
üretim betiğidir.

⭐ Brif KENDİ KENDİNE YETERLİ olmak zorunda: alt ajanın bu depoya dair
hiçbir bağlamı yok. ⇒ Kapılar düzyazıyla, satır verileri tam, yasaklar
açık yazılıyor.

⛔ Brife GİRMEYEN iki şey var ve bilerek:
  · `ELLE_ONAY` — desenin göremediği hamleyi onaylamak bir İNSAN kararıdır
    (T196) ve bende kalır;
  · §5a″ sapma gerekçesi — sapma kararı ön taramada verilmiştir, alt ajan
    yeniden vermez; brife *«şunu yapma»* biçiminde talimat olarak girer.

Kullanım:
  uv run python ... --parti=v6-parti8 --siralar=1-20 [--on-tarama=<betik>]
Çıktı: scratchpad'e `brif-<parti>-<aralık>.md`
"""
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# Çıktı dizini: depoda. Scratchpad oturumla kaybolur ve brif,
# bir sonraki partide yeniden üretilebilir olmalı.
SP = KOK / "data/brifler"

_ap = argparse.ArgumentParser()
_ap.add_argument("--parti", required=True)
_ap.add_argument("--siralar", required=True, help="ör. 1-20 ya da 1,3,4")
_ap.add_argument("--on-tarama", default=None)
A = _ap.parse_args()

KURALLAR = """\
# Blok taslağı — kurallar

⛔⛔⛔ **ÖNCE ŞU BELGELERİ OKU.** Bu brif onların YERİNE GEÇMEZ, özetidir;
ve özetin yetmediği ÖLÇÜLDÜ (T234): yalnız brifle çalışan blok 39 kayıtta
10 kusur verdi, aynı gün proje belgelerini okuyan blok 2 verdi — fark en
çok bağlam pasajlarında ve uydurulmuş hizmetlerde çıktı (7→1 ve 4→0).

- `prompts/uretim-v5.md` — özellikle **§7** (bağlam blokları ve sınıfları),
  **§5a″** (md.1-4 sapma ölçütleri), **§2a** (thinking yasakları)
- `docs/davranis-kartlari.md` — hamlelerin nasıl kurulduğu
- `AGENTS.md` — Kural 3 (klinik sınırlar)
- `scripts/analiz/2026-09-21-uretim-v6-parti7-blok*.py` — ÜSLUP ÖRNEĞİ:
  `KAYIT` sözlüğündeki kayıtlar bu işin bitmiş hâlidir, onlara bak

⭐ Taslağı yazdıktan sonra kendi doğrulama betiğini yazıp sert kapıları
mekanik olarak denetlemen beklenir (bant, soru sayısı, thinking oranı,
marka/doz taraması, bağlam sınıfı). Blok 3'ün ajanı bunu yaptı ve fark
ölçümde göründü.

Türkçe bir bağımlılık destek sohbeti veri kümesi için **taslak kayıtlar**
yazacaksın. Taslakların tamamı sonradan okunacak, revize edilecek ve
mekanik kapılardan geçirilecek; senden beklenen bitmiş ürün değil, kapıları
geçebilecek sağlam bir ilk hâl.

## Kaydın yapısı

Her satır bir konuşma. `turn_type`:
- `single` → 1 kullanıcı mesajı + 1 asistan cevabı
- `multi`  → kullanıcı, KISA asistan sorusu, kullanıcı, asistan cevabı

Son asistan cevabı `son` alanına yazılır; ara asistan turu `turns` içinde.

## ⛔ SERT KAPILAR — biri bile geçmezse blok reddedilir

1. **`bicim` İLK kullanıcı mesajının sözcük sayısıdır** (bağlam bloğu
   sayılmaz): `kisa` ≤8 · `orta` 9-25 · `uzun` >25.
2. **`turn_ending` soru sayısını belirler** — SON asistan mesajındaki `?`:
   - `acik_uclu_soru` → tam **1**
   - `takdir`, `ozet`, `yalnizca_yansitma`, `durur` → **0**
3. **Bağlam.** `baglam_var` işaretli satırlarda bir `baglam` bloğu olacak
   (`kaynak` + `metin`, 1-2 cümle) ve ilk kullanıcı mesajı bağlam bloğuyla
   başlayacak. Pasaj yalnız yordam / erişim / gizlilik / uygunluk / sınır
   cümlesi içerir.
   ⛔⛔ **PASAJ DIŞ BİR KURUMUN YAZISIDIR, BU SOHBETİN DEĞİL.** Kaynak bir
   poliklinik bilgilendirmesi, danışma birimi notu, muhtarlık duyurusu ya
   da işyeri yönergesi gibi bir şeydir. ⛔ *«Bu sohbet…»*, *«Uygulama içi
   bildirimler…»*, *«Profil bilgileri…»*, *«Görüşme kayıtları sistemde
   tutulur…»* gibi SOHBETİN KENDİSİNİ anlatan pasajlar YASAK.
   ⛔⛔ **PASAJDA OLMAYAN BİR HİZMETİ VAR SAYMA.** *«Kısa yazılı destek
   hattı»*, *«uygulamanın yardım bölümü»*, *«haftalık grup buluşmaları»*
   uydurma; pasaj ne diyorsa o kadarı vardır. `cevap_yok` sınıfında cevabı
   uydurmak yerine *«bu notta yazmıyor, onu ancak şu yer söyler»* denir.
   - `cevap_var` → kullanıcı yordamsal bir şey sorar, pasaj cevabı taşır
   - `cevap_yok` → sorar, pasaj cevabı TAŞIMAZ (uydurma yok, soracağı yeri söyle)
   - `izin_iste`  → pasajı sunmadan önce izin iste (soru işareti olmadan da olur)
   - `ilgisiz`    → pasajın konuyla ilgisi yok, bir cümleyle geç
4. **Kayıt her zaman KENDİ tohumundan yazılır.** Tohum metninin ayırt edici
   sözcükleri kullanıcı turunda görünmeli. Başka satırın sahnesini yazma.
5. **Şablon yok.** Başka kayıtlarla 8 sözcüklük birebir aynı dizi kurma;
   red ve özerklik cümlelerini her seferinde başka türlü kur.
6. **Şu kalıpları KULLANMA** (bütçesi dolu): *«dikkatimi çekti»*,
   *«dikkatimi çeken»*, *«şunu fark ettim»*, *«bir şeye takıldım»*,
   *«şunu gördüm»*, *«katılmıyorum»*, *«aynı fikirde değilim»*.

## ⛔⛔ KLİNİK YASAKLAR — istisnasız

- ⛔⛔ **ASİSTAN AĞZINDAN MARKA VE İLAÇ ADI YOK.** Kullanıcı yazabilir, sen
  TEKRARLAYAMAZSIN. Yasak örnekleri: `Tekel 2000`, `Samsun`, `Marlboro`,
  `Lark`, `Slim`, `Parliament`, `Xanax`, `Rivotril`, `Stilnox`, `Ritalin`,
  `Cipram`, `Prozac`, `Efexor`, `sertralin`, `sibutramin`. Yerine:
  *«sigaran»*, *«ilacın»*, *«ilacı yazan hekim»*.
- Teşhis koyma, **doz sayısı** verme, bırakma/azaltma **protokolü** ya da
  takvimi yazma.
- Kurum ÖZEL ADI ve telefon numarası yazma. Genel ad kullan
  (*«bir danışma birimi»*, *«ilacı yazan hekim»*, *«acil servis»*).
- Kullanıcının kendi klinik iddiasını ne doğrula ne çürüt.
- Bir yakını ikna etme yöntemi verme.
- Kullanıcı bir hüküm isterse (*«haklı mıyım»*, *«ayıp mı»*, *«doğru karar
  mı»*) VERME; reddi gerekçesiz bırakma, soracağı yeri söyle.

## `thinking` alanı

Her kaydın son asistan turunda Türkçe bir `thinking` olacak: hangi kolay
hamleyi yapmadığını ve neden yapmadığını anlatan kısa paragraflar.

- ⛔ **Uzunluk hedefi: cevabın ~1,2 katı.** Blok ortalaması 1,40'ı aşarsa
  blok reddedilir; tek bir kayıt 2,20'yi aşamaz. Taban yok.
- ⛔ İçinde şu sözcükler GEÇMEYECEK: `ızgara`, `kota`, `beyan`, `§`,
  `Kural`, `parti`, `K` + sayı, `T` + sayı. Thinking bir üretim notu değil,
  cevabı veren kişinin muhakemesidir.

## Çıktı biçimi

YALNIZCA bir JSON dizisi yaz, başka hiçbir şey yazma:

```
[{"sira": 1,
  "baglam": {"kaynak": "...", "metin": "..."},        // yalnız bağlamlı satırlarda
  "baglam_davranisi": "cevap_yok",                     // yalnız bağlamlı satırlarda
  "turns": [["user", "..."], ["assistant", "..."], ["user", "..."]],
  "son": "son asistan cevabı",
  "thinking": "..."}]
```

`single` satırlarda `turns` yalnız bir `user` öğesi içerir.
Her satır için bir nesne olmalı.
"""


def _dict_cek(betik: Path, ad: str):
    """Ön tarama betiğinden bir sözlük değişmezini güvenle çeker."""
    s = betik.read_text(encoding="utf-8")
    m = re.search(rf"^{ad}(?::[^=]+)?\s*=\s*(\{{)", s, re.M)
    if not m:
        return {}
    i = m.start(1)
    derinlik = 0
    for j in range(i, len(s)):
        derinlik += (s[j] == "{") - (s[j] == "}")
        if derinlik == 0:
            return ast.literal_eval(s[i:j + 1])
    return {}


def main() -> int:
    plan = {json.loads(l)["sira"]: json.loads(l)
            for l in (KOK / f"data/plan/{A.parti}.jsonl").read_text(
                encoding="utf-8").splitlines() if l.strip()}
    if "-" in A.siralar:
        a, b = A.siralar.split("-")
        sir = list(range(int(a), int(b) + 1))
    else:
        sir = [int(x) for x in A.siralar.split(",")]

    ot = Path(A.on_tarama) if A.on_tarama else next(
        iter(sorted(KOK.glob(f"scripts/analiz/*{A.parti}-on-tarama.py"))), None)
    okuma = _dict_cek(ot, "OKUMA") if ot else {}
    elenen = _dict_cek(ot, "ELENEN") if ot else {}
    if isinstance(elenen, dict):
        elenen = set(elenen)

    sat = [KURALLAR, "", "---", "", f"# Yazılacak satırlar — `{A.parti}`", ""]
    yazilacak = [s for s in sir if s in plan and s not in elenen]
    atlanan = [s for s in sir if s in elenen]
    if atlanan:
        sat.append(f"⛔ Bu satırlar ÜRETİLMEYECEK, atla: {atlanan}\n")
    sat.append(f"Toplam **{len(yazilacak)}** satır.\n")

    for s in yazilacak:
        r = plan[s]
        sat += [f"## Satır {s}", "",
                f"- **biçim:** `{r['bicim']}` · **kayıt düzeyi:** "
                f"`{r['register']}` · **tur:** `{r['turn_type']}`",
                f"- **son hamle:** `{r['turn_ending']}` "
                + ("(son cevapta TAM 1 soru işareti)"
                   if r["turn_ending"] == "acik_uclu_soru"
                   else "(son cevapta SORU İŞARETİ YOK)"),
                f"- **MI evresi:** `{r['mi_process']}` · **konuşma durumu:** "
                f"`{r['konusma_durumu']}`",
                f"- **bağımlılık türü:** `{r['tur']}` · **yaş:** `{r['yas']}`",
                f"- **sınır tipi:** `{r['sinir_tipi']}` · **senaryo hedefi:** "
                f"`{r['senaryo_hedefi']}`",
                f"- **red hamlesi:** {'VAR — kullanıcı bir şey istiyor ve asistan onu geri çeviriyor' if r['is_negative'] else 'yok'}",
                f"- **özerklik hamlesi:** {'VAR — kararın kullanıcıya ait olduğu AÇIKÇA söylenecek' if r['ozerklik'] else 'yok'}",
                f"- **bağlam:** " + (f"VAR, sınıf `{r.get('baglam_davranisi')}`"
                                     if r["context"] else "yok"),
                "", f"**Tohum metni** (kayıt bundan yazılacak):", "",
                f"> {r['tohum_metin']}", ""]
        if s in okuma:
            sat += [f"⛔ **ÜRETİM NOTU — bağlayıcı:** {okuma[s]}", ""]

    y = SP / f"brif-{A.parti}-{A.siralar}.md"
    y.write_text("\n".join(sat), encoding="utf-8")
    print(f"{len(yazilacak)} satır · {len(atlanan)} atlandı · üretim notu "
          f"{sum(1 for s in yazilacak if s in okuma)}")
    print(f"→ {y}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
