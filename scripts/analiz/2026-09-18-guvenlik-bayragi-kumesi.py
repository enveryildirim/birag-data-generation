#!/usr/bin/env python3
"""Pozitifçe zengin küme — `klinik_guvenlik_ihlali` bayrağının kararlılığını
ölçebilmek için.

⛔ T175 bayrağın çevrilebildiğini gösterdi ama örneklemde pozitif sayısı **1**di:
«tek pozitif çevrildi» ile «bayrak oynak» aynı şey değil. `gd-019` bu yüzden
bekletmede (K214). Bekletmeyi bitirecek ölçüm pozitifçe zengin bir küme ister.

**Kümenin kuruluşu — iki grup, ikisi de zorunlu:**
  · **P (pozitif)**: `data/judged/*.jsonl` havuzlarının TAMAMINDA bayrağı en az bir
    kez ateşlemiş tekil `source_id`'ler, GÜNCEL metinleriyle
  · **K (kontrol)**: hiçbir havuzda hiç ateşlememiş, aynı korpus ailesinden,
    cevap uzunluğu en yakın kayıtlar — pozitif başına bir tane

⭐ **Kontrol grubu pazarlık konusu değil (K116):** yalnız pozitifleri yeniden
yargılamak pozitifleri **tek yönlü eritir** ve yanlış negatif oranını hiç ölçmez.
Bayrağın oynaklığı iki yönlüdür: pozitif → negatif kadar negatif → pozitif de
sayılmalıdır.

⛔⛔ **Örnekleme çerçevesinin yanlılığı yazılı:** 19 pozitifin 19'unu da
`claude-sonnet-subagent` işaretledi; havuzlarda **tek bir Gemini pozitifi yok**.
Dolayısıyla bu küme *«Gemini, Claude'un kusur gördüğü yerde kararlı mı»* sorusunu
sorar — *«Gemini kendi ateşlediği yerde kararlı mı»* sorusunu SORMAZ. İkincisi
için Gemini ile geniş bir tarama gerekir ve bu küme onu yapmıyor.

⚠️ Çerçevenin Claude'dan gelmesi K43/K97'yi ihlal etmez: burada Claude'un çıktısı
bir **metriğe** değil, hangi kayıtların okunacağına giriyor — K43'ün Claude'a
verdiği rol tam olarak budur (aday işaretlemek). Ölçümün kendisi Gemini ↔ Gemini.

Girdi : data/judged/*.jsonl
Çıktı : reports/analiz/2026-09-18-guvenlik-bayragi-kumesi.{md,json}
Kullanım: uv run python scripts/analiz/2026-09-18-guvenlik-bayragi-kumesi.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
TARIH = Path(__file__).name[:10]
HAVUZ = KOK / "data/judged"
BAYRAK = "klinik_guvenlik_ihlali"
# ⭐ Güncel metin önceliği: yayımlanmış havuz > parti dosyaları. Bir kaydın metni
# sürümler boyunca revize edildiği için ölçüm GÜNCEL metne yapılmalı; eski
# havuzdaki metni yargılamak artık var olmayan bir kaydı ölçer.
# ⛔ İlk sürüm, yayımlanmış havuzda OLMAYAN kayıtlar için metni dosya SIRASINA
# göre seçiyordu (alfabetik) — oysa `v5-parti3.v2.v9` ile `v5-parti3.v9` arasında
# sıra bir şey söylemez. Düzeltildi: en son DEĞİŞTİRİLMİŞ havuz kazanır ve her
# kaydın metninin hangi havuzdan geldiği kümeye YAZILIR.
GUNCEL = "v0.0.14.jsonl"


def _sid(r) -> str:
    return (r.get("source_ids") or ["?"])[0]


def _korpus(sid: str) -> str:
    return sid.split(":")[0]


def _aile(sid: str) -> str:
    p = sid.split(":")
    return ":".join(p[:2]) if len(p) >= 2 else sid


def _cevap_uz(r) -> int:
    a = [m for m in r.get("messages", []) if m["role"] == "assistant"]
    return len(a[-1]["content"]) if a else 0


def main() -> int:
    havuzlar = sorted(HAVUZ.glob("*.jsonl"))
    poz_kanit: dict[str, list] = collections.defaultdict(list)
    hic_atesleme: set[str] = set()
    guncel: dict[str, dict] = {}

    yargi_say: collections.Counter = collections.Counter()
    poz_say: collections.Counter = collections.Counter()
    gordu: dict[str, set] = collections.defaultdict(set)
    sira = {f.name: (f.name == GUNCEL, f.stat().st_mtime) for f in havuzlar}
    nereden: dict[str, str] = {}
    for f in havuzlar:
        for s in f.read_text(encoding="utf-8").splitlines():
            if not s.strip():
                continue
            r = json.loads(s)
            sid, j = _sid(r), (r.get("judge") or {})
            yargi_say[j.get("judge_model") or "YOK"] += 1 if j else 0
            if j.get("judge_model"):
                gordu[j["judge_model"]].add(sid)
            if j.get(BAYRAK):
                poz_say[j.get("judge_model") or "YOK"] += 1
                poz_kanit[sid].append({"havuz": f.name, "tip": j.get("guvenlik_tipi"),
                                       "judge": j.get("judge_model"),
                                       "rubrik": j.get("prompt_version")})
            else:
                hic_atesleme.add(sid)
            # yayımlanmış havuz her zaman kazanır; yoksa en son değiştirilen havuz
            if sid not in guncel or sira[f.name] > sira[nereden[sid]]:
                guncel[sid], nereden[sid] = r, f.name

    P = sorted(poz_kanit)
    hic_atesleme -= set(P)               # bir kez bile ateşlemişse kontrol olamaz

    # ⭐ Eşleştirme: aynı korpus ailesi, cevap uzunluğu en yakın, DETERMİNİST.
    kullanilmis: set[str] = set()
    eslesme: dict[str, str] = {}
    for sid in P:
        hedef = _cevap_uz(guncel[sid])
        for olcut in (lambda x: _aile(x) == _aile(sid), lambda x: _korpus(x) == _korpus(sid)):
            aday = sorted((x for x in hic_atesleme
                           if x not in kullanilmis and olcut(x) and x in guncel),
                          key=lambda x: (abs(_cevap_uz(guncel[x]) - hedef), x))
            if aday:
                eslesme[sid] = aday[0]
                kullanilmis.add(aday[0])
                break

    K = [eslesme[s] for s in P if s in eslesme]
    eksik = [s for s in P if s not in eslesme]
    kume = [{"grup": "P", "source_id": s, "id": guncel[s]["id"], "metin_havuzu": nereden[s],
             "korpusta": nereden[s] == GUNCEL,
             "kanit": poz_kanit[s], "esi": eslesme.get(s)} for s in P]
    kume += [{"grup": "K", "source_id": s, "id": guncel[s]["id"], "metin_havuzu": nereden[s],
              "korpusta": nereden[s] == GUNCEL, "esi": None} for s in K]
    korpus_disi = [k["source_id"] for k in kume if not k["korpusta"]]
    gunceldeki = sum(1 for s in P if any(
        json.loads(l).get("source_ids", ["?"])[0] == s and (json.loads(l).get("judge") or {}).get(BAYRAK)
        for l in (HAVUZ / GUNCEL).read_text(encoding="utf-8").splitlines() if l.strip()))

    tipler = collections.Counter(k["tip"] for s in P for k in poz_kanit[s])
    korpus = collections.Counter(_korpus(s) for s in P)
    judge_ler = collections.Counter(k["judge"] for s in P for k in poz_kanit[s])

    sat = [
        "# Pozitifçe zengin küme — güvenlik bayrağının kararlılığı için", "",
        f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {TARIH}  ",
        f"**Taranan:** `data/judged/` altındaki **{len(havuzlar)}** havuzun tamamı · "
        f"güncel metin kaynağı `{GUNCEL}`  ",
        f"**Küme:** **{len(P)} pozitif + {len(K)} kontrol = {len(P) + len(K)} kayıt** "
        f"(bunların **{sum(1 for k in kume if k['korpusta'])}**'i yayımlanmış korpusta)", "",
        "⭐ Kontrol grubu pazarlık konusu değil (K116): yalnız pozitifleri yeniden "
        "yargılamak pozitifleri **tek yönlü eritir** ve yanlış negatif oranını hiç ölçmez. "
        "Bayrağın oynaklığı iki yönlüdür.", "",
        "## 1. Pozitifler nereden geliyor", "", "| | |", "|---|---:|",
        f"| tekil pozitif `source_id` | **{len(P)}** |",
        f"| bunlardan **güncel havuzda hâlâ ateşleyen** | **{gunceldeki}** |",
        f"| yalnız eski havuzlarda ateşlemiş | {len(P) - gunceldeki} |", "",
        "| `guvenlik_tipi` | adet |", "|---|---:|"]
    sat += [f"| `{t}` | {n} |" for t, n in tipler.most_common()]
    sat += ["", "| korpus | pozitif |", "|---|---:|"]
    sat += [f"| `{k}` | {n} |" for k, n in korpus.most_common()]
    sat += ["", "| işaretleyen judge | işaret |", "|---|---:|"]
    sat += [f"| `{m}` | {n} |" for m, n in judge_ler.most_common()]
    sat += ["",
            f"⛔⛔ **Örnekleme çerçevesi TEK YANLI:** {len(P)} pozitifin hepsini "
            f"`{judge_ler.most_common(1)[0][0]}` işaretledi; havuzlarda **Gemini pozitifi yok**. "
            "⇒ Bu küme *«Gemini, Claude'un kusur gördüğü yerde kararlı mı»* sorusunu sorar; "
            "*«Gemini kendi ateşlediği yerde kararlı mı»* sorusunu **sormaz**. ⚠️ Çerçevenin "
            "Claude'dan gelmesi K43/K97'yi ihlal etmez — Claude'un çıktısı metriğe değil, "
            "hangi kayıtların okunacağına giriyor; K43'ün ona verdiği rol budur.", "",
            f"⭐ **{len(P) - gunceldeki}/{len(P)} pozitif güncel havuzda artık ateşlemiyor.** "
            "İki açıklama var ve bu küme onları **ayırmak için** kuruldu: ya metin revize "
            "edildi (gerçek düzelme), ya bayrak zaten oynaktı (T175). ➡️ *Bir kapının "
            "«temizlendi» dediği yerde, temizlenen şeyin metin mi ölçüm mü olduğu "
            "sorulmadıkça bilinmez.*", "",
            "## 2. ⛔⛔⛔ Bu kapı kimin kapısı — judge başına ateşleme oranı", "",
            "| judge | yargı | pozitif | oran |", "|---|---:|---:|---:|"]
    for m, n in yargi_say.most_common():
        sat.append(f"| `{m}` | {n} | {poz_say[m]} | %{100 * poz_say[m] / max(1, n):.2f} |")
    claude = "claude-sonnet-subagent"
    gem = "agy:gemini-3.8-flash-high"
    oran = poz_say[claude] / max(1, yargi_say[claude])
    import math
    olasilik = math.exp(-oran * yargi_say[gem]) if yargi_say[gem] else float("nan")
    kesisim = sorted(set(P) & gordu[gem])
    sat += ["",
            f"⛔⛔ **Bayrağın bütün pozitifleri tek judge'dan geliyor.** `{gem}` "
            f"**{yargi_say[gem]}** yargıda **{poz_say[gem]}** kez ateşledi. Claude'un "
            f"oranı (%{100 * oran:.2f}) geçerli olsaydı o kadar yargıda sıfır görme "
            f"olasılığı ≈ **%{100 * olasilik:.1f}** ⇒ fark yalnız örneklem azlığıyla "
            "açıklanmıyor; iki judge bu bayrakta **farklı oranda** ateşliyor.", "",
            f"⭐ **Doğrudan örtüşme:** Gemini {len(gordu[gem])} tekil kaydı yargıladı; "
            f"bunların **{len(kesisim)}**'i Claude-pozitifi ve Gemini **hepsinde** "
            f"«ihlal yok» dedi: {kesisim}", "",
            "➡️⭐⭐⭐ *`build.py`'nin kayıt elediği tek judge ölçütü bu bayrak. Bugüne kadar "
            "eleme yapan bütün pozitifleri Claude üretti; K45'in puanlayan judge olarak "
            "atadığı Gemini ise örtüşen her kayıtta aksini söyledi. Yani korpusun tek "
            "otomatik klinik güvenlik kapısı, kuralın puanlayan olamaz dediği judge'ın "
            "kapısıdır.*", "",
            f"⚠️ **n={len(kesisim)}** ve Gemini'nin {yargi_say[gem]} yargısı rastgele bir "
            "örneklem değil (revize edilmiş kayıtlar + erken havuzlar) ⇒ oran farkı "
            "**ölçüldü**, nedeni ölçülmedi.", "",
            "## 3. Küme", "", "| grup | source_id | tip | eşlendiği kontrol |", "|---|---|---|---|"]
    for s in P:
        sat.append(f"| P | `{s}` | {sorted({k['tip'] for k in poz_kanit[s]})} | "
                   f"{'`' + eslesme[s] + '`' if s in eslesme else '⛔ eşlenemedi'} |")
    sat += ["", "## ⛔ Bu kümenin söylemedikleri", "", "| | |", "|---|---|",
            "| ⛔⛔ **Oran farkının nedeni bilinmiyor** | rubrik sürümü, örneklem "
            "bileşimi ya da judge'ın kendisi — bu ölçüm ayırmıyor |",
            f"| ⛔⛔ **n={len(P)} pozitif hâlâ küçük** | korpusun tamamında bayrak seyrek "
            "ateşliyor; bu bir ölçüm sınırı değil, **korpusun özelliği** |",
            "| ⛔⛔ **Çerçeve Claude'dan** | yukarıda; Gemini'nin kendi pozitifleri "
            "bilinmiyor |",
            f"| ⛔ **{len(eksik)} pozitif eşlenemedi** | aynı aileden hiç ateşlememiş aday "
            f"bulunamadı: {eksik or '—'} |",
            f"| ⛔⛔ **{len(korpus_disi)}/{len(kume)} kayıt yayımlanmış korpusta YOK** | "
            f"{korpus_disi} — metinleri parti havuzlarından alındı (en son değiştirilen "
            "havuz kazanır ve her kaydın havuzu kümeye yazılıdır). Bunlar judge'ın "
            "davranışını ölçmek için geçerli uyaranlardır (aynı boru hattının ürünü) ama "
            "**bugün sevk edilen korpusu temsil etmezler** ⇒ rapor iki oranı AYRI verir |",
            "| ⚠️ **Bu küme bir ÖLÇÜM DEĞİL** | yalnız ölçümün girdisi; kararlılık henüz "
            "ölçülmedi |", "",
            "## ⭐ Sıradaki adım", "",
            f"Bu {len(P) + len(K)} kayda **aynı gün iki taze çekiliş** (önbellek atlanarak, "
            "T174'ün yöntemi) ⇒ bayrağın iki yönlü oynaklığı. Sonuç `gd-019`'un uzmana "
            "hangi biçimde gideceğini belirler (K214): kararlıysa **tasarım** sorusu, "
            "oynaksa önce **ölçüm** sorusu.", ""]

    ham = hashlib.sha256(b"".join(f.read_bytes() for f in havuzlar)).hexdigest()[:16]
    (KOK / f"reports/analiz/{TARIH}-guvenlik-bayragi-kumesi.json").write_text(
        json.dumps({"tarih": TARIH, "havuz_sayisi": len(havuzlar), "havuz_sha256_16": ham,
                    "guncel_kaynak": GUNCEL, "n_pozitif": len(P), "n_kontrol": len(K),
                    "guncelde_atesleyen": gunceldeki, "eslenemeyen": eksik,
                    "kume": kume}, ensure_ascii=False, indent=2), encoding="utf-8")
    (KOK / f"reports/analiz/{TARIH}-guvenlik-bayragi-kumesi.md").write_text(
        "\n".join(sat), encoding="utf-8")
    print("\n".join(sat[5:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
