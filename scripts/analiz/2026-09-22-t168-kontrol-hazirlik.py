"""T168 İngilizce kontrol deneyi — öge kümesi + ayırt etme gücü (KOŞUDAN ÖNCE).

Bu betik üretimden ÖNCE koşar ve iki şey yapar:
  1. 48 ögelik eşleşmiş küme (2×2: dil × öge türü) yazılır — sonradan değişmez
  2. Fisher kesin testiyle bu tasarımın AYIRT EDEBİLECEĞİ en küçük fark
     hesaplanıp ilan edilir (T245/T246'nın dersi: eşik ilan etmek yetmez,
     eşiğin görülebilir olup olmadığı da ilan edilmeli)

Çıktı: data/deney/2026-09-22-t168-ogeler.jsonl
       reports/analiz/2026-09-22-t168-ingilizce-kontrol-onkayit.md
"""

from __future__ import annotations

import hashlib
import json
from math import comb
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
OGELER = KOK / "data" / "deney" / "2026-09-22-t168-ogeler.jsonl"
ONKAYIT = KOK / "reports" / "analiz" / "2026-09-22-t168-ingilizce-kontrol-onkayit.md"
CONFIG = KOK / "configs" / "deney" / "2026-09-22-t168-ingilizce-kontrol.yaml"

# ─── Öge kümesi: BİREBİR çeviri çiftleri, her ögede tek hedef ──────────────
# tr_klitik ↔ en_klitik aynı sırada eşleşir; tr_serbest ↔ en_serbest de öyle.

TR_KLITIK = [
    ("de", "Akşamları artık içmiyorum, ama içim de bir tuhaf oluyor."),
    ("de", "Abim aradı, annem de aynı şeyi söyledi."),
    ("de", "İşe gidiyorum, eve de düzenli dönüyorum."),
    ("de", "Sigarayı bıraktım, kahveyi de azalttım."),
    ("da", "Eşim kızgın, çocuklar da benden uzak duruyor."),
    ("de", "Param yok, iş de bulamıyorum."),
    ("da", "Doktora gittim, ilaçları da düzenli kullanıyorum."),
    ("da", "Uyuyamıyorum, iştahım da kapandı."),
    ("de", "Arkadaşlarım aramıyor, ben de aramıyorum."),
    ("de", "O gün çok kötüydüm, ertesi gün de kalkamadım."),
    ("de", "Bıraktığımı kimseye söylemedim, eşime de söylemedim."),
    ("da", "Sabah yürüyüşe çıktım, akşam da çıkacağım."),
]

EN_KLITIK = [
    ("too", "I don't drink in the evenings anymore, but I feel strange inside too."),
    ("too", "My brother called, and my mother said the same thing too."),
    ("too", "I go to work, and I come home regularly too."),
    ("too", "I quit smoking, and I cut down on coffee too."),
    ("too", "My wife is angry, and the kids keep away from me too."),
    ("also", "I have no money, and I also can't find a job."),
    ("too", "I went to the doctor, and I take my medication regularly too."),
    ("too", "I can't sleep, and my appetite is gone too."),
    ("also", "My friends don't call, and I also don't call them."),
    ("also", "I was very bad that day, and the next day I also couldn't get up."),
    ("also", "I didn't tell anyone I quit, and I also didn't tell my wife."),
    ("too", "I went for a walk in the morning, and I'll go in the evening too."),
]

TR_SERBEST = [
    ("biraz", "Bugün biraz daha iyiyim."),
    ("aslında", "Aslında bırakmak istiyorum."),
    ("biraz", "Toplantıdan sonra biraz rahatladım."),
    ("aslında", "Aslında kimseye kızgın değilim."),
    ("biraz", "Akşamları biraz huzursuz oluyorum."),
    ("aslında", "Aslında bu ilk denemem değil."),
    ("biraz", "Ailemle aram biraz düzeldi."),
    ("aslında", "Aslında yalnız kalmaktan korkuyorum."),
    ("biraz", "Uyku düzenim biraz oturdu."),
    ("aslında", "Aslında yardım istemeye utanıyorum."),
    ("biraz", "İştahım biraz açıldı."),
    ("aslında", "Aslında o gün gitmek istememiştim."),
]

EN_SERBEST = [
    ("a bit", "I'm a bit better today."),
    ("actually", "Actually, I want to quit."),
    ("a bit", "I relaxed a bit after the meeting."),
    ("actually", "Actually, I'm not angry at anyone."),
    ("a bit", "I get a bit restless in the evenings."),
    ("actually", "Actually, this isn't my first attempt."),
    ("a bit", "Things with my family got a bit better."),
    ("actually", "Actually, I'm afraid of being alone."),
    ("a bit", "My sleep schedule settled a bit."),
    ("actually", "Actually, I'm ashamed to ask for help."),
    ("a bit", "My appetite opened up a bit."),
    ("actually", "Actually, I didn't want to go that day."),
]

HUCRELER = {
    "tr_klitik": ("tr", "klitik_benzeri", TR_KLITIK),
    "en_klitik": ("en", "klitik_benzeri", EN_KLITIK),
    "tr_serbest": ("tr", "serbest_belirtec", TR_SERBEST),
    "en_serbest": ("en", "serbest_belirtec", EN_SERBEST),
}


def fisher_iki_yonlu(a: int, b: int, c: int, d: int) -> float:
    """2x2 Fisher kesin testi, iki yönlü (p'lerin toplamı yöntemi)."""
    n = a + b + c + d
    satir1, satir2 = a + b, c + d
    sutun1 = a + c

    def olasilik(x: int) -> float:
        return comb(satir1, x) * comb(satir2, sutun1 - x) / comb(n, sutun1)

    gozlenen = olasilik(a)
    alt = max(0, sutun1 - satir2)
    ust = min(satir1, sutun1)
    return sum(
        olasilik(x) for x in range(alt, ust + 1) if olasilik(x) <= gozlenen * (1 + 1e-9)
    )


def guc_taramasi(n: int) -> list[tuple[int, int, float]]:
    """Bir hücrede 0 düşme varken, ötekinde kaç düşme anlamlı olur?"""
    sonuc = []
    for taban in (0, 1, 2, 3):
        for k in range(taban, n + 1):
            p = fisher_iki_yonlu(k, n - k, taban, n - taban)
            if p < 0.05:
                sonuc.append((taban, k, p))
                break
        else:
            sonuc.append((taban, -1, 1.0))
    return sonuc


def main() -> None:
    OGELER.parent.mkdir(parents=True, exist_ok=True)
    satirlar = []
    for hucre, (dil, tur, ogeler) in HUCRELER.items():
        for i, (hedef, metin) in enumerate(ogeler, 1):
            assert hedef.lower() in metin.lower(), f"{hucre}#{i}: hedef metinde yok"
            satirlar.append(
                json.dumps(
                    {
                        "id": f"{hucre}-{i:02d}",
                        "hucre": hucre,
                        "dil": dil,
                        "oge_turu": tur,
                        "hedef": hedef,
                        "metin": metin,
                    },
                    ensure_ascii=False,
                )
            )
    OGELER.write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    sha = hashlib.sha256(OGELER.read_bytes()).hexdigest()[:16]

    n = 12
    tarama = guc_taramasi(n)

    s = ["# T168 İngilizce kontrol deneyi — ÖN KAYIT (koşudan önce)\n\n"]
    s.append(
        f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** 2026-09-22  \n"
        f"**Ön kayıt:** `configs/deney/2026-09-22-t168-ingilizce-kontrol.yaml`  \n"
        f"**Öge kümesi:** `data/deney/2026-09-22-t168-ogeler.jsonl` "
        f"SHA256 `{sha}` · **{len(satirlar)} öge**\n\n"
        "⛔ Bu belge **üretimden önce** yazıldı ve commit edildi. Ölçüt ve hüküm "
        "kuralları sonradan değiştirilmeyecek.\n\n---\n\n"
    )
    s.append("## 1. Tasarım — üç ihtimali ikiye indirmemek için 2×2\n\n")
    s.append(
        "*«Türkçe'ye özgü»* ile *«ekleşik ögeye özgü»* **aynı şey değil** ve tek\n"
        "dilli bir karşılaştırma ikisini ayıramaz. Bu yüzden 2×2:\n\n"
    )
    s.append("| | `klitik_benzeri` | `serbest_belirtec` |\n|---|---|---|\n")
    s.append("| **tr** | `de` / `da` (12) | `biraz` / `aslında` (12) |\n")
    s.append("| **en** | `too` / `also` (12) | `a bit` / `actually` (12) |\n\n")
    s.append(
        "⭐ **Serbest belirteç hücresi bir iç kontroldür:** TR ve EN'de yapıca "
        "**eşleşiktir** (ikisi de serbest sözcük). Eğer düşme yalnız `tr_klitik`'te "
        "yüksekse olgu **dile** değil **ekleşikliğe** bağlıdır.\n\n---\n\n"
    )
    s.append("## 2. ⛔ Ayırt etme gücü — ÖNCEDEN hesaplandı\n\n")
    s.append(
        "T245/T246'nın dersi: *bir eşiği ilan etmek onu doğru kılmaz.* Bu yüzden "
        "eşikle birlikte **görülebilirlik** de ilan ediliyor.\n\n"
        f"Fisher kesin testi, iki yönlü, α = 0,05, **n = {n}/hücre**:\n\n"
    )
    s.append("| Bir hücrede düşme | Ötekinde anlamlı olmak için gereken | p |\n|---:|---:|---:|\n")
    for taban, k, p in tarama:
        gerekli = f"**{k}/{n}**" if k >= 0 else "⛔ hiçbir değer yetmiyor"
        s.append(f"| {taban}/{n} | {gerekli} | {p:.4f} |\n")
    s.append(
        f"\n➡️ ⛔⛔ **Bu tasarım ancak ÇOK BÜYÜK bir farkı görebilir.** Karşı hücre "
        f"sıfırken bile anlamlılık için **{tarama[0][1]}/{n}** düşme gerekiyor "
        f"(%{100 * tarama[0][1] / n:.0f}). ⇒ **Null sonuç «fark yok» DEĞİL, «bu "
        f"tasarımla gösterilemiyor» demektir.**\n\n"
    )
    s.append(
        "⚠️ Bu, deneyi koşmamak için bir gerekçe değil: T168 *«%100'e yakın bir "
        "üslup»* iddiası taşıyor (16/16 bulgu tek örüntü) ⇒ iddia doğruysa etki "
        "zaten bu büyüklükte olmalı. Değilse, iddia zaten zayıftır.\n\n---\n\n"
    )
    s.append("## 3. Hüküm kuralları (değiştirilemez)\n\n")
    s.append(
        "| Gözlenen | Hüküm |\n|---|---|\n"
        "| `tr_klitik` ≫ `en_klitik` **ve** `tr_serbest` ≈ `en_serbest` | (b) **EKLEŞİKLİĞE** özgü |\n"
        "| `tr`'nin **iki** hücresi de yüksek | (a) **DİLE** özgü — T168'in ucu ayakta |\n"
        "| dört hücre de benzer ve **yüksek** | (c) **GENEL** işlev-sözcüğü düşmesi ⇒ T168'in «Türkçe'ye özgü» ucu **DÜŞER** |\n"
        "| dört hücre de benzer ve **düşük** | ⛔ olgu bu kurulumda **yeniden üretilemedi** — T168'in kendisi sorgulanır |\n"
        "| hiçbiri anlamlı değil | ⛔ **SONUÇSUZ** — yokluk kanıtı değil |\n\n"
    )
    s.append("---\n\n## 4. ⛔ Koşudan önce yazılan karıştırıcılar\n\n")
    s.append(
        "| | |\n|---|---|\n"
        "| ⛔ **`de/da` klitik, `too` serbest** | iki klitik hücresi yapıca eşit DEĞİL — sorunun kendisi bu, ama *«dile özgü»* hükmü tek başına bu hücreden kurulamaz |\n"
        "| ⛔ **Ögeleri ben yazdım** (K30) | çeviri denkliği benim okumam; ikinci okuyucu yok |\n"
        "| ⛔ **Tek üretici ailesi** | Claude; Gemini/GPT koşulmadı (agy kotası dolu, OPENAI_API_KEY yok) |\n"
        "| ⛔ **Blok üretimi** | 12 öge tek çağrıda ⇒ üretici kendi içinde tutarlılaşabilir; öge bağımsızlığı tam değil |\n"
        "| ⚠️ **Körlük** | üreticiye edat/vurgu/düşme hiç söylenmiyor; görev yalnız «kullanıcının sözünü anarak destek cevabı yaz» |\n"
        "| ⚠️ **Kriz yok** | ögeler günlük sıkıntı; kriz içeriği Kural 3 gereği dışarıda |\n"
    )

    ONKAYIT.parent.mkdir(parents=True, exist_ok=True)
    ONKAYIT.write_text("".join(s), encoding="utf-8")
    print(f"öge kümesi: {OGELER.relative_to(KOK)} ({len(satirlar)} öge, SHA {sha})")
    print(f"ön kayıt   : {ONKAYIT.relative_to(KOK)}")
    print(f"güç: karşı hücre 0 iken anlamlılık için gereken = {tarama[0][1]}/{n}")
    for taban, k, p in tarama:
        print(f"   taban {taban}/{n} → gereken {k}/{n} (p={p:.4f})")


if __name__ == "__main__":
    main()
