"""Türkçe register sondası (plan.md §14 ⚡). Bkz. Kural 7 (K35) — izlenebilirlik.

Girdi:  data/seeds.jsonl (K26 — yalnızca kullanıcı mesajı gerçek kaynak)
Model:  gemma4:latest (ollama, Q4_K_M, 8B/2.3B etkin) — gemma-4-E4B-it eşdeğeri (K29)
Amaç:   baz modelin Türkçe terapötik üretimde akıcı mı, thinking kanalını doğru
        açıp kapatıyor mu, §15 taramasından geçiyor mu — merdivenin ilk basamağı.

Kullanım: uv run python scripts/analiz/2026-09-12-turkce-register-sondasi.py
"""
from __future__ import annotations
import hashlib
import json
import random
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))
from checks import scan_forbidden, detect_number_candidates, count_questions, reflection_question_ratio, length_ok  # noqa: E402

SEEDS_PATH = ROOT / "data" / "seeds.jsonl"
OUT_PATH = ROOT / "reports" / "analiz" / "2026-09-12-turkce-register-sondasi.md"
MODEL = "gemma4:latest"
N_PER_TYPE = 4  # 5 tur x 4 = 20

# K19 taslağı — plan.md §6
SYSTEM_PROMPT = (
    "Sen BıRAG'sın. Bağımlılıkla mücadele eden kişilere destek olan, yargılamayan bir "
    "yapay zeka rehberisin.\n\n"
    "Kişiyi etiketlemezsin; kararların ona ait olduğunu bilir, özerkliğini korursun. "
    "Değişim nedenlerini sen vermezsin, onun kendi sözlerinden çıkarırsın. Söylemediği "
    "şeyleri varsaymaz, uydurmazsın. Katılmadığın bir şeyi onaylamazsın; itiraz "
    "ederken de yargılamazsın.\n\n"
    "Terapist, doktor, avukat ya da acil servis yerine geçmezsin. Tanı koymaz, ilaç ve "
    "doz önermez, bırakma protokolü vermez, hukuki tavsiye vermezsin. Bilgi vermeden önce "
    "izin ister, kısa ve tarafsız verir, sonra nasıl geldiğini sorarsın.\n\n"
    "Güvenlik riski, kriz ya da tıbbi aciliyet sezdiğinde olağan akışı durdurur, önce "
    "güvenliği konuşur ve uygun profesyonel desteğe yönlendirirsin.\n\n"
    "Kısa, sade ve doğal Türkçe konuşursun. Tek seferde birden fazla soru sormazsın."
)


def sample_seeds() -> list[dict]:
    rows = [json.loads(l) for l in open(SEEDS_PATH) if l.strip()]
    by_type: dict[str, list[dict]] = {}
    for r in rows:
        by_type.setdefault(r["meta"]["bagimlilik_turu"], []).append(r)
    random.seed(42)
    picked = []
    for t, group in sorted(by_type.items()):
        picked.extend(random.sample(group, min(N_PER_TYPE, len(group))))
    return picked


def call_model(user_message: str) -> dict:
    t0 = time.time()
    resp = requests.post(
        "http://127.0.0.1:11434/api/chat",
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            "think": True,
            "stream": False,
            # ⛔ K105: açgözlü üretim koşular arası BAYT AYNI olmalı. Bu üç seçenek
            # 2026-09-16'da eklendi; yayımlanan 2026-09-12 raporu ONLARSIZ üretildi
            # ve bu yüzden yeniden türetilemez — o rapor bir KOŞUM KAYDIdır.
            # ⚠️ `gemma4:latest` de kayan bir etiket: aynı ad ileride başka ağırlığa
            # işaret edebilir. Tam sabitleme için model digest'i gerekir.
            "options": {"temperature": 0, "top_p": 1, "seed": 42},
        },
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    elapsed = time.time() - t0
    msg = data.get("message", {})
    return {
        "content": msg.get("content", ""),
        "thinking": msg.get("thinking", ""),
        "elapsed_s": round(elapsed, 2),
        "eval_count": data.get("eval_count"),
    }


def detect_lang(text: str) -> str:
    try:
        from lingua import Language, LanguageDetectorBuilder
        detector = LanguageDetectorBuilder.from_languages(
            Language.TURKISH, Language.ENGLISH
        ).build()
        lang = detector.detect_language_of(text)
        return lang.name if lang else "belirsiz"
    except Exception as e:
        return f"hata: {e}"


def main():
    seeds = sample_seeds()
    input_hash = hashlib.sha256(SEEDS_PATH.read_bytes()).hexdigest()[:16]
    rows_md = []
    forbidden_total = 0
    number_total = 0
    lang_counts: dict[str, int] = {}
    thinking_lens: list[int] = []

    for i, seed in enumerate(seeds):
        user_msg = seed["user_message"]
        r = call_model(user_msg)
        forbidden = scan_forbidden(r["content"])
        numbers = detect_number_candidates(r["content"])
        q = count_questions(r["content"])
        ratio = reflection_question_ratio(r["content"])
        len_ok, len_err = length_ok(r["content"], r["thinking"])
        lang = detect_lang(r["content"])
        lang_counts[lang] = lang_counts.get(lang, 0) + 1
        if forbidden:
            forbidden_total += 1
        if numbers:
            number_total += 1
        thinking_lens.append(len(r["thinking"]))

        rows_md.append(
            f"### [{i+1}] {seed['campaign']} / {seed['meta']['bagimlilik_turu']} "
            f"({seed['source_id']})\n\n"
            f"**Kullanıcı:** {user_msg}\n\n"
            f"**thinking** ({len(r['thinking'])} karakter):\n> {r['thinking'][:600]}\n\n"
            f"**Cevap** ({len(r['content'])} karakter, {r['elapsed_s']}s):\n> {r['content']}\n\n"
            f"Dil: `{lang}` · Soru sayısı: {q} · Yansıtma:soru: {ratio} · "
            f"Uzunluk uygun: {len_ok} ({len_err or '-'}) · "
            f"Yasak ifade: {forbidden or 'yok'} · Sayı adayı: {numbers or 'yok'}\n"
        )

    summary = (
        f"# Türkçe register sondası — {MODEL}\n\n"
        f"**Girdi:** `data/seeds.jsonl` (sha256:{input_hash}) · **Betik:** "
        f"`scripts/analiz/2026-09-12-turkce-register-sondasi.py` · **Tarih:** 2026-09-12\n\n"
        f"Bkz. plan.md §14 ⚡ Türkçe register sondası, K29 model merdiveni.\n\n"
        f"## Özet ({len(seeds)} örnek)\n\n"
        f"- Dil dağılımı: {lang_counts}\n"
        f"- Yasak ifade tespit edilen: {forbidden_total}/{len(seeds)}\n"
        f"- Sayı adayı tespit edilen: {number_total}/{len(seeds)}\n"
        f"- Ortalama thinking uzunluğu: "
        f"{round(sum(thinking_lens) / len(thinking_lens)) if thinking_lens else 0} karakter "
        f"(min {min(thinking_lens, default=0)}, maks {max(thinking_lens, default=0)})\n\n"
        f"⚠️ Bu sonda yalnızca **akıcılık ve mimari doğrulama** içindir — klinik kalite "
        f"değerlendirmesi değildir (o Faz 3, uzman + judge). Model: ollama Q4_K_M "
        f"quantize — bf16 LoRA hedefinden (K7) farklı, yalnızca taban modelin Türkçe "
        f"davranışını gözlemlemek için kullanıldı.\n\n"
        f"---\n\n" + "\n".join(rows_md)
    )
    OUT_PATH.write_text(summary)
    print(f"yazıldı: {OUT_PATH}")
    print(f"dil dağılımı: {lang_counts}")
    print(f"yasak ifade: {forbidden_total}/{len(seeds)}  sayı adayı: {number_total}/{len(seeds)}")


if __name__ == "__main__":
    main()
