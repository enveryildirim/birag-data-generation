"""LLM çağrısı — content-hash cache zorunlu (Kural 4, K3). Bkz. plan.md §10.

Şu an tek kullanım: judge (Faz 2+). Üretim Claude Code ile yapıldığı için (K30)
burada bir "generate" çağrısı yok.
"""
from __future__ import annotations
import hashlib
import datetime
import json
import re
import time
import subprocess
from pathlib import Path

import litellm

CACHE_DIR = Path(__file__).parent.parent / ".cache" / "llm"


def _cache_key(model: str, messages: list[dict]) -> str:
    payload = json.dumps({"model": model, "messages": messages}, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode()).hexdigest()


# ⚠️ 2026-09-15: `agy` CLI'ın KENDİ 5 dakikalık sınırı var ve dolduğunda
# ÇIKIŞ KODU 0 ile KISMİ ÇIKTI döndürüyor:
#     [agy] print timeout after 5m0s with turn in progress; returning partial output
# Yani bizim `AGY_TIMEOUT`'umuzu 300'ün üstüne çıkarmak onu ÖLÜ KOD yapar: CLI önce
# kendi sınırına varır, temiz bir `TimeoutExpired` yerine yarım metin döner ve
# `returncode == 0` olduğu için başarı sanılır. Sınır bu yüzden CLI'ınkinin ALTINDA
# tutuluyor; ayrıca kısmi çıktı işareti aşağıda ayrıca yakalanıyor.
AGY_TIMEOUT = 280      # tek çağrı sınırı (sn) — CLI'ın 300 sn'lik sınırının altında
KISMI_ISARET = ("print timeout", "turn in progress; returning partial output")
AGY_DENEME = 3         # boş çıktı VE zaman aşımı için toplam deneme

# ⛔⛔ 2026-09-18: KOTA BİTİNCE CLI HATA DÖNDÜRMÜYOR, ASILI KALIYOR. Kendi günlüğüne
#     RESOURCE_EXHAUSTED (code 429): Individual quota reached. ... Resets in 1h55m0s.
# yazıp içeride yeniden denemeye giriyor; bize hiç dönmüyor. Bizim tarafta bu bir
# ZAMAN AŞIMI gibi görünüyor ⇒ 3 deneme × 280 sn = kayıt başına ~14 dakika boşa
# yanıyor ve sonunda «zaman aşımı» yazan, sebebi söylemeyen bir hata çıkıyor.
# ➡️ Zaman aşımında CLI'ın günlüğüne bakılır: kota hatası TAZEYSE hemen durulur.
# Bir hatanın yanlış adla görünmesi, hatanın kendisinden pahalıya mal olur.
AGY_GUNLUK = Path.home() / ".gemini" / "antigravity-cli" / "cli.log"
KOTA_ISARET = ("RESOURCE_EXHAUSTED", "quota reached")
KOTA_PENCERE = 300     # sn — günlükteki kota hatası bundan eskiyse dikkate alınmaz


def _kota_bitti() -> str | None:
    """CLI günlüğünde TAZE bir kota hatası varsa onu döndürür, yoksa None.

    ⚠️ Günlük bizim değil; biçimi değişirse bu sonda sessizce çalışmaz olur ve
    davranış eski hâline (3 deneme zaman aşımı) döner — bozulma güvenli yönde.
    """
    try:
        if time.time() - AGY_GUNLUK.stat().st_mtime > KOTA_PENCERE:
            return None
        kuyruk = AGY_GUNLUK.read_text(errors="replace").splitlines()[-40:]
    except Exception:
        return None
    for satir in reversed(kuyruk):
        if KOTA_ISARET[0] not in satir:
            continue
        # ⚠️ Dosyanın mtime'ı yetmez: hub günlüğe BAŞKA sebeplerle de yazar ve o zaman
        # ESKİ bir kota hatası taze görünür ⇒ gerçek bir zaman aşımı «kota» diye
        # maskelenirdi. Satırın KENDİ damgası okunur (`I0918 18:30:15.376492`).
        m = re.match(r"[IEWF](\d{2})(\d{2}) (\d{2}):(\d{2}):(\d{2})", satir)
        if not m:
            return satir.strip()[-200:]          # damga okunamadı ⇒ mtime'a güven
        ay, gun, sa, dk, sn = (int(x) for x in m.groups())
        simdi = datetime.datetime.now()
        try:
            t = datetime.datetime(simdi.year, ay, gun, sa, dk, sn)
        except ValueError:
            return satir.strip()[-200:]
        if abs((simdi - t).total_seconds()) <= KOTA_PENCERE:
            return satir.strip()[-200:]
        return None                              # kota hatası var ama ESKİ
    return None


def _call_agy(model: str, prompt: str) -> str:
    """Antigravity CLI üzerinden çağrı (Gemini vb.). `agy:` önekiyle seçilir.

    İki ayrı kararsızlığa karşı yeniden dener:
      · çıkış kodu 0 ile BOŞ stdout (2026-09-12 eval'de görüldü)
      · `TimeoutExpired` (2026-09-14: parti 3'te bir kayıt üç koşuda da sınırı aştı,
        sonra aynı prompt doğrudan çağrıldığında 65 sn'de döndü — yani kayıt değil
        çağrı kararsız). Eskiden zaman aşımı yeniden denenmiyordu, tek seferde
        `_judge_error` oluyordu.
    """
    son_hata = None
    for deneme in range(AGY_DENEME):
        try:
            proc = subprocess.run(
                ["agy", "--model", model, "--dangerously-skip-permissions", "-p", prompt],
                capture_output=True, text=True, timeout=AGY_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            kota = _kota_bitti()
            if kota:
                raise RuntimeError(f"agy KOTA BİTTİ — yeniden denemek boşa: {kota}")
            son_hata = f"zaman aşımı ({AGY_TIMEOUT} sn), deneme {deneme + 1}/{AGY_DENEME}"
            continue
        if proc.returncode != 0:
            raise RuntimeError(f"agy hata ({proc.returncode}): {proc.stderr[:400]}")
        cikti = proc.stdout.strip()
        if any(i in cikti[:400] for i in KISMI_ISARET):
            son_hata = (f"CLI kendi sınırına vardı ve kısmi çıktı döndürdü "
                        f"(çıkış kodu 0), deneme {deneme + 1}/{AGY_DENEME}")
            continue
        if cikti:
            return cikti
        son_hata = f"boş çıktı, deneme {deneme + 1}/{AGY_DENEME}"
    raise RuntimeError(f"agy {AGY_DENEME} denemede de başarısız — son: {son_hata}")


def call(model: str, messages: list[dict], api_base: str | None = None) -> str:
    """Cache'li tamamlama çağrısı. Aynı (model, messages) ikinci kez servise gitmez.

    `agy:<model>` -> antigravity CLI · diğerleri -> litellm.
    """
    key = _cache_key(model, messages)
    cache_file = CACHE_DIR / f"{key}.json"
    if cache_file.exists():
        onbellek = json.loads(cache_file.read_text())["content"]
        # ⚠️ BOŞ CACHE ZEHİRLİDİR: bir kez boş yazıldığında aynı prompt bir daha
        # servise hiç gitmez ve her koşuda aynı hatayı verir. 2026-09-15'te
        # havuzda böyle bir girdi bulundu. Boş girdi ISKA sayılır, yeniden çağrılır.
        if onbellek.strip():
            return onbellek
        cache_file.unlink(missing_ok=True)

    if model.startswith("agy:"):
        prompt = "\n\n".join(m["content"] for m in messages)
        content = _call_agy(model[4:], prompt)
    else:
        resp = litellm.completion(model=model, messages=messages, api_base=api_base)
        content = resp.choices[0].message.content

    if not content.strip():          # boş sonucu cache'e YAZMA (yukarıdaki gerekçe)
        raise RuntimeError("boş içerik döndü — cache'e yazılmadı")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps({"model": model, "messages": messages, "content": content}, ensure_ascii=False))
    return content


def gecersiz_kil(model: str, messages: list[dict]) -> bool:
    """Bir cache girdisini siler; bir sonraki çağrı servise gider.

    ⛔⛔⛔ BOŞ OLMAYAN AMA BOZUK CACHE DE ZEHİRLİDİR (2026-09-21). `call()`
    yalnız BOŞ içeriği ıska sayıyor; JSON içermeyen dolu bir yanıt ise
    yazılıyor ve her koşuda aynı `ValueError`ı veriyor. `v6-parti2 #9`
    böyle takıldı: judge modeli rubrik yerine *«I have started a search
    across the repository…»* döndürdü, yanıt cache'e girdi ve SÜRDÜRME
    mekanizması onu bir daha asla onaramadı — iki koşu, aynı hata, aynı
    bayt. ➡️⭐⭐ *Bir «geçici hatayı yeniden dene» mekanizması, hatanın
    kaynağı önbellekteyse hiçbir şeyi yeniden denemez; kalıcılık kararını
    veren yer, geçerlilik kararını veren yerden başkaysa onarım imkânsızdır.*
    ⛔ Bu bir YENİDEN ÇEKİLİŞ değildir (T174): geçerli bir puan hiç
    üretilmedi, dolayısıyla silinen şey bir ölçüm değil bir çöp.
    """
    f = CACHE_DIR / f"{_cache_key(model, messages)}.json"
    var = f.exists()
    f.unlink(missing_ok=True)
    return var


def parse_json(text: str) -> dict:
    """Judge çıktısı bazen ```json ... ``` içine sarılı geliyor ya da JSON'dan sonra
    ekstra metin/tekrar ekliyor. Metindeki İLK `{` karakterinden başlayıp yalnızca
    ilk geçerli JSON nesnesini çözer, çevresindeki her şeyi (fence, sonraki metin) yok sayar."""
    start = text.find("{")
    if start == -1:
        raise ValueError(f"JSON bulunamadı: {text[:200]!r}")
    obj, _ = json.JSONDecoder().raw_decode(text, start)
    return obj
