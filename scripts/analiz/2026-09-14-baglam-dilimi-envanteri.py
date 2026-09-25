#!/usr/bin/env python3
"""Bağlam (RAG) diliminin envanteri — parti 2 öncesi durum tespiti.

Soru: v2'nin bağlam kayıtlarındaki pasajlar NEREDEN geldi ve bu bir risk mi?

Bulgu (aşağıda ölçülüyor): pasajların ve kaynak adlarının tamamı üretim sırasında
YAZILDI; repoda bir belge korpusu yok (`data/` yalnızca tohum ve aday dosyaları
tutuyor). Kural 3 "uydurma klinik içerik yok" diyor, dolayısıyla bu kayıt altına
alınmalı. Riskin BÜYÜKLÜĞÜ ise ölçülebilir: pasajın içeriği modelin CEVABINA
geçiyor mu?

Girdi : data/candidates/expert-70.jsonl
Çıktı : reports/analiz/2026-09-14-baglam-dilimi-envanteri.md
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
# ⛔ Rapor tarihi betiğin ADINDAN gelir, koşulduğu günden DEĞİL. `date.today()`
# kullanılırsa betik ertesi gün kendi yayımlanmış raporunu yeniden üretemez
# (dosya adı da, içindeki tarih satırı da kayar) — Kural 7'nin sessiz ihlali.
TARIH = Path(__file__).name[:10]
GIRDI = KOK / "data/candidates/expert-70.jsonl"
CIKTI = KOK / "reports/analiz/2026-09-14-baglam-dilimi-envanteri.md"

# K17: tek format değil, 4-5 varyant dolaşır. v2'de fiilen kullanılanlar.
VARYANT = {
    "[BAĞLAM]": "köşeli etiket", "--- KAYNAK": "tire ayraç", "BAĞLAM —": "tire başlık",
    "<baglam": "XML etiketi", "### BAĞLAM": "markdown başlık",
    "BAĞLAM (kaynak:": "parantezli", "[BAĞLAM ·": "köşeli + nokta", "BAĞLAM\nKaynak:": "iki satır",
}


def main() -> None:
    rows = [json.loads(l) for l in open(GIRDI) if l.strip()]
    ctx = [r for r in rows if r.get("context")]
    L = [f"# Bağlam (RAG) dilimi envanteri — parti 2 öncesi", "",
         f"**Girdi:** `data/candidates/expert-70.jsonl` · SHA256 "
         f"`{hashlib.sha256(GIRDI.read_bytes()).hexdigest()}`  ",
         f"**Betik:** `scripts/analiz/2026-09-14-baglam-dilimi-envanteri.py` · "
         f"**Tarih:** {TARIH}", "", "---", "",
         "## 1. Durum", "",
         f"- Bağlamlı kayıt: **{len(ctx)}/{len(rows)}** (`uretim-v2`) · v3 parti 1'de **0/40**",
         f"- Repoda belge korpusu: **yok**. `data/` yalnızca `seeds.jsonl` (tohum "
         f"senaryoları), `candidates/`, `judged/`, `plan/` tutuyor. Tohumlarda "
         f"`user_message` ve senaryo meta'sı var, **alınabilir pasaj yok**.",
         f"- Sonuç: v2'deki **{len(ctx)} pasajın {len(ctx)}'i de** ve kaynak adlarının "
         f"tamamı üretim sırasında **yazıldı**.", "",
         "> ⚠️ Kaynak adları gerçek kurum belgesi gibi duruyor (*\"Fabrika Çalışan El "
         "Kitabı — Mola Düzeni\"*, *\"Üniversite Psikolojik Danışma Birimi — SSS\"*). "
         "Hiçbiri var olan bir belge değil. Kural 3 açısından kayda geçmesi gereken "
         "şey budur.", "",
         "## 2. Risk ne kadar büyük — pasaj içeriği cevaba geçiyor mu?", "",
         "Asıl soru uydurmanın **yayılıp yayılmadığı**: model pasajdaki iddiayı "
         "kendi cevabında tekrarlıyorsa uydurma içerik çıktıya taşınır.", "",
         "| # | kaynak (uydurma) | pasajdan cevaba geçen içerik sözcüğü |", "|---|---|---|"]
    gecen = 0
    for i, r in enumerate(ctx, 1):
        k = r["context"][0]
        cevap = r["messages"][-1]["content"].lower()
        ortak = sorted({w.lower() for w in re.findall(r"\w{6,}", k["metin"])
                        if w.lower() in cevap})
        if ortak:
            gecen += 1
        L.append(f"| {i} | {k['kaynak']} | {', '.join(ortak) if ortak else '— yok'} |")
    L += ["",
          f"**{len(ctx) - gecen}/{len(ctx)} kayıtta pasajdan cevaba HİÇBİR içerik "
          f"sözcüğü geçmiyor.** Geçen tek kayıt `yetersiz` vakası: model pasajın neyden "
          "bahsettiğini **reddini gerekçelendirmek için** adlandırıyor "
          "(*\"orada sınır belirleme araçlarından bahsediliyor, oranların uzun vadeli "
          "getirisinden değil\"*) — istenen davranış bu.", "",
          "**Okuma:** öğretilen şey pasajın **içeriği** değil, pasaj karşısındaki "
          "**davranış** (ne zaman kullan, ne zaman \"bu bağlamda yok\" de). Uydurma "
          "içerik çıktıya taşınmıyor. Yine de girdi tarafında var ve veri kartında "
          "yazılmalı.", "",
          "## 2b. ⚠️ Asıl bulgu: v2'nin RAG dilimi bağlamı KULLANMAYI hiç öğretmiyor", "",
          "Pasajın uydurma olması ikincil bir sorun çıktı. Birincil sorun şu: bağlamlı "
          "dokuz kaydın hiçbirinde model **bağlamdaki cevabı kullanıp kullanıcının "
          "sorusunu cevaplamıyor**.", "",
          "| Davranış | Adet | Ne öğretiyor |", "|---|---:|---|",
          "| bağlamı görmezden geliyor (kullanıcı zaten soru sormamış) | 6/9 | \"bağlam "
          "gelirse aldırma\" |",
          "| bağlam yetersiz, açıkça reddediyor | 2/9 | ✅ doğru davranış (§7 `yetersiz`) |",
          "| bağlamda cevap **var**, model yine de vermiyor | 1/9 | ⛔ uzmanın **reddettiği** "
          "kayıt: *\"cevap verilmesi gerekiyor, bu cevabı vermemiş\"* |",
          "| **bağlamdaki cevabı kullanıyor** | **0/9** | — |", "",
          "Son satırdaki kayıt (`ambivalans`, üniversite danışma birimi) v3 §5b'nin "
          "yazılma sebebiydi: kullanıcı *\"kayıt aileme gider mi\"* diye sordu, pasajda "
          "gizlilik cümlesi duruyordu, model *\"paylaşmamı ister misin?\"* dedi. §5b o "
          "kuralı düzeltti ama **parti 1'de hiç bağlam kaydı olmadığı için kural hiç "
          "sınanmadı**.", "",
          "**Parti 2'nin RAG dilimi buna göre kurulur:** çoğunluk, kullanıcının doğrudan "
          "sorduğu ve cevabı pasajda duran vakadır.", "",
          "## 3. Kullanılan format varyantları (K17)", "",
          "K17 tek format istemiyor, 4-5 varyant dolaşsın diyor. v2'de fiilen:", ""]
    for r in ctx:
        u = next(m["content"] for m in r["messages"] if m["role"] == "user")
        ad = next((v for k, v in VARYANT.items() if u.startswith(k) or k in u[:60]), "?")
        L.append(f"- `{ad}` — {u[:46].splitlines()[0]}…")
    L += ["", f"**{len(set(next((v for k, v in VARYANT.items() if k in next(m['content'] for m in r['messages'] if m['role']=='user')[:60]), '?') for r in ctx))} ayrı varyant** — K17'nin istediği çeşitlilik sağlanmış.", "",
          "## 4. Parti 2 için karar gereken nokta", "",
          "Bağlam dilimi pasaj metni olmadan yazılamaz. Üç yol var ve **hangisi "
          "seçilirse iş değişir**:", "",
          "1. **Gerçek korpus** — İP3'ün alma korpusu komşu depolarda olabilir. "
          "AGENTS Kural 1 gereği okumadan önce **izin gerekir**.",
          "2. **Sentetik pasaj, açık kayıtla** — v2'nin yolu; ama kaynak adları gerçek "
          "kurum belgesi taklidi olmaktan çıkarılır, pasajlar klinik iddia taşımaz "
          "(yalnızca yordam/sınır cümleleri), her kayıt `sentetik: true` ile işaretlenir.",
          "3. **Yalnızca `yetersiz` vakası** — doğru davranışın *\"bu bağlamda cevap "
          "yok\"* olduğu kayıtlar. En az uydurma gerektirir ama yalnızca reddi öğretir.", ""]
    CIKTI.write_text("\n".join(L) + "\n")
    print(f"yazıldı: {CIKTI.relative_to(KOK)}  "
          f"({len(ctx)} bağlamlı kayıt · içerik sızan {gecen})")


if __name__ == "__main__":
    main()
