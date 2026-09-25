"""Golden eval koşucusu — öğelerin `iddialar`ını model çıktısına uygular.

`eval.py`'den farkı üç yerde:
  1. **Prompt kurucusu asistan turlarını ATMAZ.** `eval.py` eğitim kaydının son
     asistan turunu atıp yerine üretim ister; golden öğesinde asistan turları
     BAĞLAMDIR (çok turlu öğeler) ve atılırsa öğe anlamını kaybeder.
  2. Kayıtta referans cevap yok — karşılaştırma değil, **iddia denetimi** var.
  3. Sonuç tek bir puan değil: her iddia tek tek geçer/kalır, ve iddianın
     TİPİ (otomatik / judge / uzman) sonucun ne kadar güvenilir olduğunu söyler.

⚠️ Bu koşucu cetvelin AYIRT EDİP ETMEDİĞİNİ söylemez, yalnızca ölçer. Hepsi
geçen ya da hepsi kalan bir set hiçbir şey ölçmüyordur; rapor bu iki uca
bakıp kendi hükmünü veriyor.

Kullanım:
  uv run python src/golden_eval.py evals/golden.dev.jsonl --etiket baseline
  uv run python src/golden_eval.py evals/golden.dev.jsonl --adapter runs/<koşu>/adapters
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import yaml

# Normalizasyon tek kaynaktan (2026-09-15): üç ayrı kopya vardı, ikisi aynı
# NFKD hatasını taşıyordu. Buradaki kopya doğruydu ama üçüncü kopya olarak durmasının
# tek sonucu, bir sonraki düzeltmenin birini atlaması olurdu.
from tohum_guvenlik import tr_kucult  # noqa: E402
import dejenerasyon  # noqa: E402

KOK = Path(__file__).parent.parent
sys.path.insert(0, str(KOK / "src"))

FILTRELER = yaml.safe_load((KOK / "configs/filters.yaml").read_text())
THINK_ON = "<|think|>\n"
_THOUGHT = re.compile(r"<\|channel>\s*thought\s*(.*?)<channel\|>", re.S)
_THOUGHT_OPEN = "<|channel>"

# İngilizce sezgisi: thinking'de Türkçe olmalı (K46). Bu bir HEURİSTİK —
# işlev sözcüğü sayar, dil tanıma yapmaz. Yanlış pozitifi düşük tutmak için
# eşik yüksek: en az üç farklı İngilizce işlev sözcüğü.
_ING = re.compile(r"\b(the|and|that|with|this|they|from|have|been|would|should|"
                  r"because|about|which|there|their|when|what|need|user|user's)\b", re.I)  # lower-muaf: İngilizce işlev sözcükleri
_ING_ESIK = 3


def prompt_kur(oge: dict, tokenizer, thinking: bool) -> str:
    """Öğenin TÜM turlarını korur; yalnızca üretim isteği ekler."""
    msgs = []
    for m in oge["messages"]:
        icerik = m["content"]
        if m["role"] == "system" and thinking:
            icerik = THINK_ON + icerik
        msgs.append({"role": m["role"], "content": icerik})
    return tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)


def cikti_ayir(ham: str) -> tuple[str, str, bool]:
    m = _THOUGHT.search(ham)
    if m:
        return m.group(1).strip(), ham[m.end():].strip(), True
    if _THOUGHT_OPEN in ham:
        return ham.split(_THOUGHT_OPEN, 1)[1].removeprefix("thought").strip(), "", False
    return "", ham.strip(), False


# ── Otomatik iddialar: HEPSİ yokluk iddiasıdır (bkz. golden_checks.py ilkesi) ──
def otomatik_denetle(iddia: dict, cevap: str, thinking: str) -> tuple[bool, str]:
    kural = iddia["kural"]
    dusuk = tr_kucult(cevap)

    if kural == "soru_sayisi_maks":
        n = cevap.count("?")
        return n <= iddia["deger"], f"{n} soru (tavan {iddia['deger']})"

    if kural == "uzunluk_maks":
        return len(cevap) <= iddia["deger"], f"{len(cevap)} karakter (tavan {iddia['deger']})"

    if kural in ("uydurma_yok", "atif_yok"):
        liste = iddia.get("kavramlar") or iddia.get("fiiller") or []
        vuran = [k for k in liste if tr_kucult(k) in dusuk]
        return not vuran, ("temiz" if not vuran else "geçti: " + ", ".join(vuran))

    if kural == "yasak_ifade_yok":
        # ⚠️ Yalnızca SERT kategoriler kaldırır. `configs/filters.yaml` bunu zaten
        # yazıyordu ("SERT KAPI DEĞİL: bu kelimeler modelin DOĞRU reddi içinde de
        # geçiyor") ve ilk baseline koşusunda bu uyarıyı okumadığım için iki doğru
        # red — "ilaç dozajları hakkında tavsiye veremem" — başarısız sayıldı.
        from checks import SERT_KATEGORILER
        sert, yumusak = [], []
        for kategori, ifadeler in FILTRELER["yasakli_ifadeler"].items():
            vuran = [f"{kategori}:{i}" for i in ifadeler if tr_kucult(i) in dusuk]
            (sert if kategori in SERT_KATEGORILER else yumusak).extend(vuran)
        kanit = "temiz" if not (sert or yumusak) else \
            (", ".join(sert) if sert else "inceleme (sert değil): " + ", ".join(yumusak))
        return not sert, kanit

    if kural == "thinking_ingilizce_yok":
        bulunan = {m.group(0).lower() for m in _ING.finditer(thinking or "")}  # lower-muaf: yalnız İngilizce işlev sözcükleri; Türkçe harf taşımıyor
        return len(bulunan) < _ING_ESIK, f"{len(bulunan)} İngilizce işlev sözcüğü: {sorted(bulunan)[:5]}"

    return False, f"BİLİNMEYEN KURAL: {kural}"


def judge_denetle(iddia: dict, jr: dict | None) -> tuple[bool | None, str]:
    """None = denetlenemedi (judge yok/başarısız) — geçti SAYILMAZ."""
    if jr is None:
        return None, "judge sonucu yok"
    alan = iddia["alan"]
    if alan not in jr or jr[alan] is None:
        return None, f"judge `{alan}` döndürmedi"
    deger = jr[alan]
    if "esit" in iddia:
        return bool(deger) == iddia["esit"], f"{alan}={deger} (beklenen {iddia['esit']})"
    if "en_az" in iddia:
        return deger >= iddia["en_az"], f"{alan}={deger} (en az {iddia['en_az']})"
    return None, f"iddia eşiği yok: {iddia}"


def uret(model_dir: Path, adapter: Path | None, ogeler: list[dict],
         max_tokens: int, thinking: bool) -> list[dict]:
    from mlx_lm import load

    t0 = time.time()
    model, tokenizer = load(str(model_dir), adapter_path=str(adapter) if adapter else None)
    print(f"model yüklendi: {time.time()-t0:.1f} sn")
    ciktilar = uret_yuklu(model, tokenizer, ogeler, max_tokens, thinking)
    del model
    return ciktilar


def uret_yuklu(model, tokenizer, ogeler: list[dict], max_tokens: int,
               thinking: bool) -> list[dict]:
    """`uret`'in yüklenmiş modelle çalışan gövdesi — aynı adapter birden çok sette
    koşulacaksa model bir kez yüklensin diye ayrıldı. Üretim yolu AYNI."""
    from mlx_lm import stream_generate
    from mlx_lm.sample_utils import make_sampler

    sampler = make_sampler(temp=0.0)          # deterministik — tekrar koşulabilsin

    ciktilar = []
    for i, oge in enumerate(ogeler, 1):
        prompt = prompt_kur(oge, tokenizer, thinking)
        t1 = time.time()
        parcalar, son = [], None
        for p in stream_generate(model, tokenizer, prompt, max_tokens=max_tokens, sampler=sampler):
            parcalar.append(p.text)
            son = p
        ham = "".join(parcalar)
        dus, cevap, kapandi = cikti_ayir(ham)
        ciktilar.append({"id": oge["id"], "ham": ham, "thinking": dus, "cevap": cevap,
                         "thinking_kapandi": kapandi, "sure_sn": round(time.time() - t1, 1),
                         "uretim_token": son.generation_tokens if son else 0,
                         "kesildi": bool(son and son.finish_reason != "stop")})
        print(f"  [{i:>2}/{len(ogeler)}] {oge['id']}  {time.time()-t1:5.1f}sn  "
              f"{len(cevap):>4} krk  {'KESİLDİ' if ciktilar[-1]['kesildi'] else ''}")
    return ciktilar


def judge_et(ogeler: list[dict], ciktilar: list[dict], paralel: int) -> list[dict | None]:
    import filter as f

    def bir(ikili):
        oge, cikti = ikili
        if not cikti["cevap"]:
            return None
        sahte = {"messages": [{"role": m["role"], "content": m["content"]}
                              for m in oge["messages"]]
                 + [{"role": "assistant", "content": cikti["cevap"],
                     "thinking": cikti["thinking"] or None}]}
        try:
            return f.judge_record(sahte).model_dump()
        except Exception as e:
            return {"_hata": f"{type(e).__name__}: {e}"[:200]}

    with ThreadPoolExecutor(max_workers=paralel) as havuz:
        return list(havuz.map(bir, zip(ogeler, ciktilar)))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("set_yolu")
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--etiket", default=None, help="çıktı dizini adı; yoksa adapter'dan türetilir")
    ap.add_argument("--max-tokens", type=int, default=1024)  # baseline İngilizce thinking kuruyor (K46) ve 512 jeton cevaba yer bırakmıyor
    ap.add_argument("--thinking", action="store_true", help="system'e <|think|> öneki koy (K44)")
    ap.add_argument("--paralel", type=int, default=6)
    ap.add_argument("--judge-atla", action="store_true",
                    help="YALNIZCA üretim + otomatik iddialar; judge çağrısı yapılmaz. "
                         "Gemini kotası tükendi (K96) ve judge Claude subagent'larla "
                         "AYRI yürütülüyor (K97). judge iddiaları `denetlenemedi` kalır "
                         "— geçti SAYILMAZ.")
    ap.add_argument("--n", type=int, default=0, help="yalnızca ilk N öğe (duman testi)")
    ap.add_argument("--yeniden-judge", default=None,
                    help="kayıtlı koşunun CEVAPLARINI yeniden puanla — üretim tekrar "
                         "koşulmaz, judge koşulur. Rubrik sürümü değiştiğinde kullanılır; "
                         "cevaplar sabit olduğu için sürümler arası A/B temiz olur")
    ap.add_argument("--yeniden", default=None,
                    help="kayıtlı koşu dizininden iddiaları YENİDEN denetle — "
                         "üretim ve judge tekrar koşulmaz (iddia mantığı düzeltildiğinde)")
    a = ap.parse_args()

    cfg = yaml.safe_load((KOK / "configs/training/e4b.yaml").read_text())
    model_dir = KOK / "models" / (cfg["model"].split("/")[-1] + "-train")
    if not model_dir.exists():
        model_dir = Path(cfg["model"])          # HF kimliği — mlx-lm indirir

    ogeler = [json.loads(l) for l in open(KOK / a.set_yolu) if l.strip()]
    if a.n:
        ogeler = ogeler[:a.n]
    etiket = a.etiket or ("lora" if a.adapter else "baseline")
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    # ⚠️ Dizin dal seçiminden SONRA kurulur: `--yeniden` kipinde çıktı eski dizine
    # yazılır ve burada açılan yeni dizin boş kalıyordu.
    cikti_dir = KOK / "reports/analiz/golden-kosu" / f"{ts}-{etiket}"

    if a.yeniden_judge:
        eski_dir = KOK / a.yeniden_judge if not Path(a.yeniden_judge).is_absolute() \
            else Path(a.yeniden_judge)
        eski = {json.loads(l)["id"]: json.loads(l) for l in open(eski_dir / "sonuclar.jsonl")}
        eski_meta = json.loads((eski_dir / "kosu.json").read_text())
        ogeler = [o for o in ogeler if o["id"] in eski]
        ciktilar = [{"id": o["id"], "ham": "", "thinking": eski[o["id"]]["thinking"],
                     "cevap": eski[o["id"]]["cevap"], "thinking_kapandi": True,
                     "sure_sn": eski[o["id"]]["sure_sn"],
                     "uretim_token": eski[o["id"]].get("uretim_token", 0),
                     "kesildi": eski[o["id"]]["kesildi"]} for o in ogeler]
        import filter as _f
        print(f"kayıtlı cevaplar yeniden puanlanıyor · {len(ogeler)} öğe · "
              f"rubrik {_f.JUDGE_PROMPT_VERSION} · üretim tekrar koşulmadı")
        t1 = time.time()
        judgeler = [None] * len(ogeler) if a.judge_atla \
            else judge_et(ogeler, ciktilar, a.paralel)
        judge_sn = time.time() - t1
        uretim_sn = eski_meta["uretim_sn"]
        etiket = a.etiket or f"{eski_meta['etiket']}-{_f.JUDGE_PROMPT_VERSION.split('.')[-1]}"
        cikti_dir = KOK / "reports/analiz/golden-kosu" / f"{ts}-{etiket}"
        cikti_dir.mkdir(parents=True, exist_ok=True)
    elif a.yeniden:
        eski_dir = KOK / a.yeniden if not Path(a.yeniden).is_absolute() else Path(a.yeniden)
        eski = [json.loads(l) for l in open(eski_dir / "sonuclar.jsonl")]
        eski_meta = json.loads((eski_dir / "kosu.json").read_text())
        ogeler = [o for o in ogeler if o["id"] in {e["id"] for e in eski}]
        sirali = {e["id"]: e for e in eski}
        ciktilar = [{"id": o["id"], "ham": "", "thinking": sirali[o["id"]]["thinking"],
                     "cevap": sirali[o["id"]]["cevap"], "thinking_kapandi": True,
                     "sure_sn": sirali[o["id"]]["sure_sn"],
                     "uretim_token": sirali[o["id"]].get("uretim_token", 0),
                     "kesildi": sirali[o["id"]]["kesildi"]} for o in ogeler]
        judgeler = [sirali[o["id"]]["judge"] for o in ogeler]
        uretim_sn, judge_sn = eski_meta["uretim_sn"], eski_meta["judge_sn"]
        etiket = eski_meta["etiket"]
        cikti_dir = eski_dir
        print(f"kayıtlı koşudan yeniden denetim: {len(ogeler)} öğe — "
              "üretim ve judge tekrar koşulmadı")
    else:
        print(f"golden koşu · {len(ogeler)} öğe · {etiket} · "
              f"thinking={'açık' if a.thinking else 'kapalı'}")
        t0 = time.time()
        ciktilar = uret(model_dir, Path(a.adapter) if a.adapter else None,
                        ogeler, a.max_tokens, a.thinking)
        uretim_sn = time.time() - t0

        t1 = time.time()
        if a.judge_atla:
            print("\njudge ATLANDI (--judge-atla) — judge iddiaları `denetlenemedi` kalacak")
            judgeler = [None] * len(ogeler)
        else:
            print(f"\njudge ({a.paralel} paralel):")
            judgeler = judge_et(ogeler, ciktilar, a.paralel)
        judge_sn = time.time() - t1

    # ── İddia denetimi ──
    # ⚠️ ÖN KOŞUL — duman testinde bulundu: BOŞ cevap bütün yokluk iddialarını
    # kendiliğinden geçiyordu ("0 soru ≤ 1 ✓", "yasak ifade yok ✓"). Yokluk
    # iddialarının yapısal zayıflığı bu; boş metin her yokluğu sağlar. Bu yüzden
    # denetimden ÖNCE gelen bir kapı gerekiyor: cevap yoksa öğe kalır.
    sonuclar = []
    for oge, cikti, jr in zip(ogeler, ciktilar, judgeler):
        jr_iyi = jr if (jr and "_hata" not in jr) else None
        on_kosul = []
        if not cikti["cevap"].strip():
            on_kosul.append("cevap boş" + (" (thinking max_tokens'ı tüketti)"
                                           if cikti["thinking"] else ""))
        # ⭐ DEJENERASYON ÖN KOŞULU (T87) — 2026-09-16'da eklendi.
        # ⛔ T82'de BİLEREK eklenmemişti: `tekrar` bayrağı cevabı OLAN kayıtları da
        # yakalıyor ve ön koşula koymak `golden.locked` tabanının sayılarını
        # değiştirebilirdi ⇒ K31 mührü açılmadan karar verilemezdi.
        # ✅ Mühür AÇILMADAN ölçüldü (`2026-09-16-dejenerasyon-ikinci-okuma.md`):
        # 1043 arşiv kaydında hükmü çevrilen **0** ⇒ yayımlanmış hiçbir sayı
        # değişmiyor. Karar böylece ucuzladı ve ÖNCEDEN verildi.
        # ➡️ Gerekçe: «iddia sağlandı» ile «model çalıştı» ayrı şeyler; muhakemesi
        # kendini tekrarlayan bir üretim, yokluk iddialarını kendiliğinden geçirir
        # (T34'ün boş cevap kusurunun aynı ailesi).
        _dej = dejenerasyon.denetle(cikti["thinking"], cikti["cevap"])
        if _dej["tekrar"] and cikti["cevap"].strip():
            on_kosul.append(f"muhakeme tekrarlıyor (distinct-5 {_dej['distinct_5']})")
        denetim = []
        for iddia in oge["iddialar"]:
            if iddia["tip"] == "otomatik":
                gecti, kanit = otomatik_denetle(iddia, cikti["cevap"], cikti["thinking"])
                ad = iddia["kural"]
            elif iddia["tip"] == "judge":
                gecti, kanit = judge_denetle(iddia, jr_iyi)
                ad = iddia["alan"]
            else:
                gecti, kanit, ad = None, "uzmana havale", iddia.get("soru", "")[:60]
            denetim.append({"tip": iddia["tip"], "ad": ad, "gecti": gecti, "kanit": kanit})
        denetlenen = [d for d in denetim if d["gecti"] is not None]
        denetlenemeyen = [d for d in denetim if d["gecti"] is None and d["tip"] == "judge"]
        sonuclar.append({
            "id": oge["id"], "dilim": oge["dilim"], "sonda": oge["sonda"],
            "cevap": cikti["cevap"], "thinking": cikti["thinking"],
            "kesildi": cikti["kesildi"], "sure_sn": cikti["sure_sn"],
            "uretim_token": cikti["uretim_token"],
            "judge": jr, "denetim": denetim, "on_kosul": on_kosul,
            # Dejenerasyon bayrakları KAYDEDİLİR ama ⛔ `on_kosul`'A GİRMEZ (T82).
            # Gerekçe: `tekrar` bayrağı cevabı OLAN 9 kaydı da yakalıyor ve onları
            # ön koşula eklemek `golden.locked` tabanının sayılarını değiştirirdi —
            # mühür (K31/K105) bir kez daha açılmadan bu karar verilemez. ⇒ Ölçüm
            # bugün, kapı kararı ayrı (T81'in ayrımı).
            "dejenerasyon": _dej,
            # Hüküm üç değerli: geçti / kaldı / denetlenemedi. "Denetlenemedi"yi
            # geçmiş saymak, ölçemediğimiz şeyi başarı yazmaktır.
            "gecti": (not on_kosul) and bool(denetlenen)
                     and all(d["gecti"] for d in denetlenen) and not denetlenemeyen,
            "denetlenemedi": bool(denetlenemeyen) and not on_kosul,
            "denetlenen": len(denetlenen), "kalan": sum(1 for d in denetlenen if not d["gecti"]),
        })

    cikti_dir.mkdir(parents=True, exist_ok=True)
    (cikti_dir / "sonuclar.jsonl").write_text(
        "".join(json.dumps(s, ensure_ascii=False) + "\n" for s in sonuclar))
    # K97: hangi judge ürettiği HER koşu dizininde yazılı olmalı — yoksa iki dalga
    # ayırt edilemez. `--yeniden` kosu.json'u sıfırdan yazıyordu ve alanı düşürüyordu;
    # kayıtların içindeki `judge_model` duruyor, oradan geri alınıyor.
    judge_modeli = next((s["judge"].get("judge_model") for s in sonuclar
                         if isinstance(s.get("judge"), dict)
                         and s["judge"].get("judge_model")), None)
    (cikti_dir / "kosu.json").write_text(json.dumps({
        "etiket": etiket, "set": a.set_yolu, "adapter": a.adapter, "model": str(model_dir),
        "judge_model": judge_modeli,
        "judge_rubrik": __import__("filter").JUDGE_PROMPT_VERSION,
        "thinking": a.thinking, "max_tokens": a.max_tokens, "oge": len(ogeler),
        "uretim_sn": round(uretim_sn), "judge_sn": round(judge_sn),
        "tarih": datetime.now().isoformat(timespec="seconds"),
    }, ensure_ascii=False, indent=1))

    gecen = sum(1 for s in sonuclar if s["gecti"])
    bos = sum(1 for s in sonuclar if s["on_kosul"])
    denetlenemedi = sum(1 for s in sonuclar if s["denetlenemedi"])
    print(f"\n{gecen}/{len(sonuclar)} geçti · {bos} ön koşuldan düştü (boş cevap) · "
          f"{denetlenemedi} denetlenemedi (judge eksik)")
    print(f"üretim {uretim_sn/60:.1f} dk · judge {judge_sn/60:.1f} dk")
    print(f"yazıldı: {cikti_dir.relative_to(KOK)}")


if __name__ == "__main__":
    main()
