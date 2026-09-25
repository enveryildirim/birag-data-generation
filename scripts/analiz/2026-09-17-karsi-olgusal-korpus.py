#!/usr/bin/env python3
"""KARŞI OLGUSAL korpus — «yönlendirmeme refleksi» hipotezini sınamak için.

⛔⛔ **Bu bir VERİ SETİ DEĞİL, bir ABLASYON korpusudur.** `datasets/` altına
yazılmaz, yayımlanmaz, eğitim için aday değildir. Tek amacı **tek bir
değişkeni** yalıtmak. MI ekseninde daha KÖTÜ bir korpustur ve bilerek öyledir.

## Hipotez (T132)

Üç kapsam taraması (17 kol) ince ayarın yönlendirme refleksini sildiğini
gösterdi ve çapa kol *«veride yönlendirme az»* açıklamasını çürüttü (veri 3,7
kat büyüdü, sonuç değişmedi). Geriye kalan aday: **korpus yönlendirmeyi az
öğretmiyor, yönlendirMEMEYİ çok öğretiyor.**

## ⭐ Neden SİLME, yeniden yazma değil

*Bir ablasyonda silinir, yeniden yazılmaz.* Yeniden yazmak İKİ şeyi birden
değiştirir — hedef değişkeni ve yeni metnin getirdiği her şeyi. Bugün bunun
bedeli ölçüldü: §8b′ düzeltmem bir uydurmayı koşul kipine alarak taşıdı
(`v5-parti8 #26`). ⇒ Yalnız **tam ilan cümleleri/parçaları** silinir.

## ⛔ Neyin silinmediği ve NEDEN

| sınıf | sayı | karar |
|---|---:|---|
| `ret_bilgi` (*«ne olduğunu ben söyleyemem»*) | 159 | ⛔ **DOKUNULMAZ** — Kural 3: silinirse veri, modele yorumlayabileceğini öğretir |
| §8b′ erişilebilirlik reddi | (ret_bilgi içinde) | ⛔ **DOKUNULMAZ** — silinirse kurum yordamı uydurması geri gelir |
| klinik sözcük taşıyan ilan | 2 | ⛔ dokunulmaz |
| bileşik ilan (>12 kelime) | 6 | ⚠️ atlanır — ikinci yan cümle içerik taşıyor |
| ⭐ **saf ilan** (≤12 kelime, klinik sözcük yok) | **64** | ✅ **silinir** |

➡️⭐⭐ *Ve bu tablonun kendisi bir bulgu: hipotezin suçladığı şeyin büyük kısmı
Kural 3'ün ZORUNLU kıldığı şeyle aynı. Ablasyon ancak azınlığa dokunabiliyor
⇒ negatif sonuç «hipotez yanlış» demek olmayacak, «bu manipülasyon zayıftı»
demek olabilecek. Bu, koşudan ÖNCE yazılıyor.*

## Plasebo kolu

⭐ Silmenin kendisinin etkisini ayırmak için ikinci bir korpus: **aynı sayıda,
benzer uzunlukta, hedef DIŞI** cümle silinir. Plasebo da bozulursa fark
«yönlendirmeme»den değil «cümle silmek»ten gelir.
"""
from __future__ import annotations
import json, random, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
import importlib.util as _iu
_sp = _iu.spec_from_file_location("y", KOK / "scripts/analiz/2026-09-17-yonlendirmeme-refleksi.py")
Y = _iu.module_from_spec(_sp); _sp.loader.exec_module(Y)

GIRDI = KOK / "datasets/v0.0.8/train.jsonl"          # ⛔ DEĞİŞMEZ, yalnız okunur
DIZIN = KOK / "data/ablasyon"
HEDEF = {k: Y.DERLENMIS[k] for k in ("ret_tavsiye", "ozerklik")}
KLINIK = re.compile(r"hekim|doktor|ilac|ilaç|doz|hukuk|avukat|acil|uzman|poliklinik|eczane", re.I)
AZAMI_KELIME = 12


# ⛔⛔ **İLK YAZIMDA PARAGRAF YAPISI YOK EDİLİYORDU.** Cümleler `\n\n`
# üzerinden de bölünüyor, sonra hepsi tek boşlukla birleştiriliyordu ⇒ 63 cümle
# silinmesine rağmen **556 kayıt** değişmiş görünüyordu: ablasyon, hedef
# değişkenin yanında BÜTÜN KORPUSUN BİÇİMİNİ de değiştiriyordu.
# ➡️ *Bir ablasyonda «kaç kayıt değişti» sayısı, «kaç şey sildim» sayısıyla
#    tutarlı olmalı; tutmuyorsa değişen şey sandığınız şey değildir.*
# ⇒ Paragraflar KORUNUR; bölme ve birleştirme paragraf İÇİNDE yapılır.
def _paragraflar(metin: str) -> list[str]:
    return metin.split("\n\n")


def _parcala(metin: str) -> list[str]:
    """Bir PARAGRAF içinde cümlelere ayır."""
    return re.split(r"(?<=[.!?])\s+", metin)


def _saf_mi(parca: str) -> bool:
    if not any(p.search(parca) for pats in HEDEF.values() for p in pats):
        return False
    return not KLINIK.search(parca) and len(parca.split()) <= AZAMI_KELIME


def _sil(metin: str, sayac: dict) -> str:
    """Saf ilanları siler. ⭐ Paragraf yapısı KORUNUR; boşalan paragraf düşer."""
    yeni_par = []
    for par in _paragraflar(metin):
        yeni_cumleler = []
        for c in _parcala(par):
            if not c.strip():
                continue
            if _saf_mi(c):
                sayac["cumle"] += 1
                continue
            if ";" in c:
                parcalar = re.split(r"\s*;\s*", c)
                kalan = [p for p in parcalar if not _saf_mi(p)]
                if len(kalan) != len(parcalar):
                    sayac["yan_cumle"] += len(parcalar) - len(kalan)
                    if not kalan:
                        sayac["cumle"] += 1
                        continue
                    c = "; ".join(kalan)
                    if not c.rstrip().endswith((".", "!", "?")):
                        c = c.rstrip(" ,;") + "."
                    c = c[0].upper() + c[1:] if c else c
            yeni_cumleler.append(c)
        if yeni_cumleler:
            yeni_par.append(" ".join(yeni_cumleler))
        else:
            sayac["paragraf"] = sayac.get("paragraf", 0) + 1
    return "\n\n".join(yeni_par)


def _uygula(kayitlar: list[dict], fn) -> tuple[list[dict], dict]:
    sayac = {"cumle": 0, "yan_cumle": 0, "kayit": 0}
    out = []
    for r in json.loads(json.dumps(kayitlar)):          # derin kopya
        degisti = False
        for m in r["messages"]:
            if m["role"] != "assistant" or not m.get("content"):
                continue
            # ⭐⭐ SİLME OLMAYAN MESAJA DOKUNULMAZ. Bölüp yeniden birleştirmek,
            # hiçbir şey silinmese bile boşlukları normalize ediyordu (satır sonu
            # boşluğu, fazla boş satır) ⇒ 2 kayıt hedef dışı değişmişti.
            # ➡️ *Bir ablasyonda «değiştirmedim» ile «değiştirip aynı yazdım»
            #    aynı şey değildir; ikincisi hedef dışı bir fark üretir.*
            once = dict(sayac)
            yeni = fn(m["content"], sayac)
            silindi = any(sayac.get(k, 0) != once.get(k, 0) for k in ("cumle", "yan_cumle"))
            if silindi and yeni.strip():
                m["content"] = yeni
                degisti = True
            elif silindi:
                for k in ("cumle", "yan_cumle"):          # ⛔ boş cevap ASLA: geri al
                    sayac[k] = once.get(k, 0)
        sayac["kayit"] += degisti
        out.append(r)
    return out, sayac


def main() -> int:
    DIZIN.mkdir(parents=True, exist_ok=True)
    kayitlar = [json.loads(s) for s in GIRDI.read_text(encoding="utf-8").splitlines() if s.strip()]

    # ── A kolu: saf ilanlar silinir ─────────────────────────────────────────
    a, sa = _uygula(kayitlar, _sil)
    hedef_adet = sa["cumle"] + sa["yan_cumle"]

    # ── Plasebo: aynı sayıda, HEDEF DIŞI, benzer uzunlukta cümle silinir ────
    rng = random.Random(7)
    aday = []
    for i, r in enumerate(kayitlar):
        for j, m in enumerate(r["messages"]):
            if m["role"] != "assistant" or not m.get("content"):
                continue
            cs = [c for par in _paragraflar(m["content"]) for c in _parcala(par) if c.strip()]
            if len(cs) < 2:                       # ⛔ tek cümlelik cevaptan silinmez
                continue
            for c in cs:
                if _saf_mi(c) or any(p.search(c) for pats in Y.DERLENMIS.values() for p in pats):
                    continue
                if len(c.split()) <= AZAMI_KELIME:
                    aday.append((i, j, c))
    rng.shuffle(aday)

    # ⛔⛔ **PLASEBO, SİLİNMESİ KAYDI BOZAN CÜMLELERİ SEÇİYORDU** ve üç kayıt
    # `checks`ten düştü (dayanak cümlesi, bağlam sert kapısı). Bozuk bir plasebo
    # kolu kontrol olmaktan çıkar: A ile P arasındaki fark «yönlendirmeme»den
    # değil «P bozuk»tan gelirdi.
    # ➡️ *Bir kontrol kolu, deney kolunun geçtiği her kapıdan geçmelidir; yoksa
    #    kontrol değil ikinci bir müdahaledir.*
    # ⇒ Aday, silindikten sonra `checks` geçerse kabul edilir; geçmezse atlanır.
    from checks import run_checks as _rc

    def _dene(kayit: dict, j: int, c: str) -> bool:
        k2 = json.loads(json.dumps(kayit))
        m = k2["messages"][j]
        yp = []
        for par in _paragraflar(m["content"]):
            kalan = [x for x in _parcala(par) if x.strip() and x != c]
            if kalan:
                yp.append(" ".join(kalan))
        if not yp:
            return False
        m["content"] = "\n\n".join(yp)
        return _rc(k2)["passed"]

    sec, elenen = {}, 0
    for i, j, c in aday:
        if sum(len(v) for v in sec.values()) >= hedef_adet:
            break
        if not _dene(kayitlar[i], j, c):
            elenen += 1
            continue
        sec.setdefault((i, j), set()).add(c)

    p = json.loads(json.dumps(kayitlar))
    sp_ = {"cumle": 0, "yan_cumle": 0, "kayit": 0, "checks_elendi": elenen}
    for (i, j), cset in sec.items():
        m = p[i]["messages"][j]
        yeni_par, silinen = [], 0
        for par in _paragraflar(m["content"]):
            cs = [c for c in _parcala(par) if c.strip()]
            kalan = [c for c in cs if c not in cset]
            silinen += len(cs) - len(kalan)
            if kalan:
                yeni_par.append(" ".join(kalan))
        if not yeni_par:
            continue
        m["content"] = "\n\n".join(yeni_par)
        sp_["cumle"] += silinen
    sp_["kayit"] = len({i for i, _ in sec})

    s_map = {"A-ilan-seyreltilmis": sa, "P-plasebo": sp_}
    for ad, veri, s in (("A-ilan-seyreltilmis", a, sa), ("P-plasebo", p, sp_)):
        yol = DIZIN / f"v0.0.8-{ad}.jsonl"
        yol.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in veri),
                       encoding="utf-8")
        print(f"{ad:<22} {len(veri)} kayıt · {s['cumle']} cümle + {s.get('yan_cumle',0)} yan cümle "
              f"silindi · {s['kayit']} kayıt değişti → {yol.relative_to(KOK)}")

    # ── Doğrulama ───────────────────────────────────────────────────────────
    print("\n─── doğrulama ───")
    for ad in ("A-ilan-seyreltilmis", "P-plasebo"):
        v = [json.loads(s) for s in (DIZIN / f"v0.0.8-{ad}.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
        ayni_id = [x["id"] for x in v] == [x["id"] for x in kayitlar]
        bos = sum(1 for x in v for m in x["messages"]
                  if m["role"] == "assistant" and m.get("content") is not None and not m["content"].strip())
        deg = sum(1 for x, o in zip(v, kayitlar)
                  if json.dumps(x["messages"], ensure_ascii=False)
                  != json.dumps(o["messages"], ensure_ascii=False))
        bek = s_map[ad]["cumle"] + s_map[ad].get("yan_cumle", 0)
        tutarli = deg <= bek and deg > 0
        print(f"  {ad:<22} kayıt {len(v)}=={len(kayitlar)} · id sırası "
              f"{'✅' if ayni_id else '⛔'} · boş cevap {bos} · değişen kayıt {deg} "
              f"(silinen {bek}) {'✅' if tutarli else '⛔ TUTARSIZ'}")
        if not tutarli:
            print("     ⛔ «kaç kayıt değişti» > «kaç şey sildim» ⇒ hedef dışı bir şey de değişti")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
