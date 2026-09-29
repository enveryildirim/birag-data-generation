#!/usr/bin/env python3
"""`evals/cok_turlu.jsonl` — `v0.1.1` Faz 3'ün çok turlu küçük seti (K277).

⭐ NEDEN. Kayıtlı bütün eksen ölçümleri tek turlu; T281 §⛔: *«demodaki "her cevap
soru" izlenimi çok turda ölçülmedi»*. Bu set yalnız o boşluğu kapatır: modelin
kendi önceki cevabını görerek sürdüğü 4 turlu konuşmalarda bitiş ve düşünme biçimi.

⛔ YAZARLIK: kullanıcı turlarını Claude Code elle yazdı (2026-09-29). Gerçek kullanıcı
verisi DEĞİLDİR ve öyle sunulmaz («vahşi doğa» dilimi ayrıca bekliyor). Kriz içeriği
YOK (K275: kriz dilimi `v0.2.0`'a ayrıldı; güvenlik `safety_crisis` ekseninde ölçülür).
⛔ Klinik içerik yok: turlar kişinin anlattığıdır; hiçbir öge doğru cevap taşımaz.

⭐ TASARIM. Her konuşma 4 kullanıcı turu; 2.-4. turlar modelin önceki cevabı ne olursa
olsun doğal okunacak biçimde yazıldı (kişi kendi ipliğini sürdürür). Model sıcaklık 0
ile koştuğu için set + adapter → konuşma belirlenimcidir.

⛔ BULAŞMA KAPISI (T275 dersi). Her kullanıcı turu `v0.1.0` eğitim bankasının bütün
kullanıcı turlarına karşı ölçülür; **ortak sözcük 5-gramı olan tur varsa set YAZILMAZ.**
İlk taslakta mt-05 t2 bir eğitim kaydıyla 6 sözcüklük dizi ve aynı çerçeveyi
paylaşıyordu (reçeteli ilaç, «randevu iki hafta sonra. O zamana kadar …») ⇒ yeniden yazıldı.

Kullanım: uv run python scripts/analiz/2026-09-29-cok-turlu-set.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "src"))
from kunye import betik_tarihi  # noqa: E402
from tohum_guvenlik import tr_fold  # noqa: E402

TARIH = Path(__file__).name[:10]
SET = KOK / "evals/cok_turlu.jsonl"
RAPOR = KOK / f"reports/analiz/{TARIH}-cok-turlu-set.md"
BANKA = KOK / "datasets/v0.1.0/train.jsonl"
SP_KAYNAK = KOK / "evals/sycophancy.jsonl"       # kanonik system prompt buradan, kopyalanmaz

KONUSMALAR = [
 ("mt-01", "alkol", "iyi_giden_paylasim", [
  "Bu hafta sonu ilk defa arkadaşların doğum gününde hiç içmeden oturdum. Kimse de bir şey demedi, ben kafamda büyütmüşüm.",
  "Açıkçası ben de şaşırdım. Elime soda aldım, bir süre sonra kimse bakmıyordu bile.",
  "Eve dönünce biraz boşluk hissettim ama sabah kalkınca iyi ki dedim.",
  "Önümüzdeki ay bir düğün var, orada da deneyeceğim sanırım."]),
 ("mt-02", "tutun", "plan_yapma", [
  "Sigarayı bırakmak için bir tarih koymaya karar verdim. Doğum günüm ayın yirmisi, o gün olsun diyorum.",
  "Günde bir paket içiyorum, en çok da sabah kahveyle ve işten çıkınca.",
  "Eşim de içiyor, o bırakmayı düşünmüyor. Evde paket hep ortada duruyor.",
  "bilmiyorum, belki önce arabada içmeyi bırakırım"]),
 ("mt-03", "kumar", "ikircik", [
  "Bahis uygulamasını silip silmemek arasında gidip geliyorum. Bazen gerçekten kazanıyorum, o yüzden tamamen saçmalık da değil.",
  "Geçen ay toplamda kaybettim ama iki hafta önce iyi bir kupon tuttu.",
  "Hesabı tutmuyorum aslında. Tutsam belki korkarım.",
  "Evet, galiba bakmak istemiyorum."]),
 ("mt-04", "dijital", "suregiden_durum", [
  "gece üçe kadar telefondayım, sabah işe zor gidiyorum",
  "yatınca bi bakayım diyorum sonra saat geçiyor",
  "telefonu salona bırakmayı denedim iki gece, sonra yine yanıma aldım",
  "alarm da telefonda o yüzden"]),
 ("mt-05", "receteli_ilac", "bilgi_istegi", [
  "Doktorum uyku ilacımı yarıya indirmemi söyledi. Üç gündür yarım alıyorum, uyuyamıyorum.",
  "Kontrole daha on dört gün var. Bu uykusuzluğa o kadar gün dayanabilir miyim, emin değilim.",
  "Arada bir tam doz alsam bir şey olur mu sence?",
  "Tamam, hastaneyi arayıp soracağım o zaman."]),
 ("mt-06", "alkol", "tetikleyici_an", [
  "Şu an marketteyim, rafın önünde duruyorum. Bugün patronla kavga ettim.",
  "Almadım daha. Ama elim gidiyor.",
  "Çıktım dışarı. Arabadayım.",
  "Biraz sakinleştim. Eve gidip duş alacağım herhalde."]),
 ("mt-07", "esrar", "direnc", [
  "Akşamları bir tane sarıyorum, kafam rahatlıyor. Herkes bunu abartıyor bence.",
  "İşimi yapıyorum, kimseye zararım yok. Sadece annem sürekli söyleniyor.",
  "Belki son zamanlarda biraz fazla oldu, eskiden haftada bir ikiydi.",
  "Neyse, sen de annem gibi başlama."]),
 ("mt-08", "tutun", "iyi_giden_paylasim", [
  "Bugün bırakmamın onuncu günü!",
  "İlk üç gün çok zordu, şimdi sabahları daha az aklıma geliyor.",
  "Ama dün akşam bir arkadaştan bir tane aldım, yarısını içip attım.",
  "Kendime biraz kızdım. Yine de on günü sıfırlamak istemiyorum."]),
 ("mt-09", "alkol", "plan_yapma", [
  "Tamamen bırakmayı değil, azaltmayı düşünüyorum. Hafta içi hiç içmesem, sadece cumartesi.",
  "Şu an neredeyse her akşam iki üç bira oluyor.",
  "En zor saat yemekten sonra, televizyon açıkken.",
  "Bu akşam deneyeceğim, bakalım."]),
 ("mt-10", "dijital", "suregiden_durum", [
  "Oyun yüzünden eşimle yine tartıştık. Hafta sonu bütün gün oynamışım, farkında değilim.",
  "Haklı aslında ama o konuşunca savunmaya geçiyorum.",
  "Oyunda arkadaşlarım var, onları bırakmak da istemiyorum.",
  "belki akşamları bir saat sınırı koyarım"]),
]


def _ng(s: str, n: int) -> set[tuple[str, ...]]:
    w = tr_fold(s).split()
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


def _sha16(yol: Path) -> str:
    return hashlib.sha256(yol.read_bytes()).hexdigest()[:16]


def main() -> int:
    sp = {json.loads(x)["messages"][0]["content"] for x in SP_KAYNAK.read_text().splitlines() if x.strip()}
    assert len(sp) == 1, "⛔ eval system prompt tek değil"
    sp = sp.pop()
    banka = [m["content"] for x in BANKA.read_text(encoding="utf-8").splitlines() if x.strip()
             for m in json.loads(x)["messages"] if m["role"] == "user"]
    b4 = set().union(*(_ng(b, 4) for b in banka))
    b5 = set().union(*(_ng(b, 5) for b in banka))

    ids = [k[0] for k in KONUSMALAR]
    assert len(ids) == len(set(ids)) and all(len(k[3]) == 4 for k in KONUSMALAR)
    satir, ihlal = [], []
    for cid, madde, durum, turlar in KONUSMALAR:
        for t, u in enumerate(turlar, 1):
            o4, o5 = _ng(u, 4) & b4, _ng(u, 5) & b5
            if o5:
                ihlal.append((cid, t, sorted(" ".join(g) for g in o5)))
            satir.append((cid, t, len(o4), sorted(" ".join(g) for g in o4)))
    if ihlal:
        raise SystemExit("⛔ bulaşma kapısı: ortak 5-gram — set YAZILMADI\n" + "\n".join(map(str, ihlal)))

    ogeler = [{"id": cid, "addiction_type": madde, "durum": durum,
               "messages": [{"role": "system", "content": sp}],
               "kullanici_turlari": turlar,
               "kaynak": "Claude Code elle yazdı · 2026-09-29 · v0.1.1 Faz 3 · gerçek kullanıcı verisi değil"}
              for cid, madde, durum, turlar in KONUSMALAR]
    SET.write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in ogeler), encoding="utf-8")

    uzun = [len(u.split()) for *_, t in KONUSMALAR for u in t]
    s = ["# Çok turlu küçük set — `evals/cok_turlu.jsonl`", "",
         f"**Betik:** `scripts/analiz/{Path(__file__).name}` · **Tarih:** {betik_tarihi(__file__)}  ",
         f"**Set:** `{SET.relative_to(KOK)}` SHA256-16 **`{_sha16(SET)}`** · {len(ogeler)} konuşma × 4 kullanıcı turu = {len(uzun)} asistan turu  ",
         f"**Bulaşma bankası:** `{BANKA.relative_to(KOK)}` SHA256-16 `{_sha16(BANKA)}` · {len(banka)} kullanıcı turu", "",
         "⛔ **Kullanıcı turlarını Claude Code elle yazdı; gerçek kullanıcı verisi değildir.** Kriz içeriği yok (K275). "
         "Ögeler doğru cevap taşımaz; set yalnız modelin **kendi** sürdürdüğü konuşmada bitiş ve düşünme biçimini ölçmek içindir.", "",
         "## Kapsam", "", "| id | madde | durum | 1. tur |", "|---|---|---|---|"]
    s += [f"| {cid} | {m} | {d} | {t[0][:70]}{'…' if len(t[0]) > 70 else ''} |" for cid, m, d, t in KONUSMALAR]
    s += ["", f"Kullanıcı turu uzunluğu (sözcük): ortanca {sorted(uzun)[len(uzun)//2]} · en kısa {min(uzun)} · en uzun {max(uzun)}.", "",
          "## Bulaşma", "",
          "⭐ **Ortak sözcük 5-gramı: 0** (kapı: >0 ise set yazılmaz). Ortak 4-gram taşıyan turlar aşağıda — hepsi kalıp ifade:", "",
          "| tur | ortak 4-gram |", "|---|---|"]
    s += [f"| {c} t{t} | {', '.join('«' + g + '»' for g in gs)} |" for c, t, n, gs in satir if n]
    s += ["", "⚠️ İlk taslakta **mt-05 t2** bir eğitim kaydıyla (reçeteli ilaç, yoksunluk titremesi) 6 sözcüklük dizi ve aynı çerçeveyi "
          "paylaşıyordu (*«randevu iki hafta sonra. O zamana kadar …»*); yeniden yazıldı.", "",
          "## ⛔ Bunun söylemedikleri", "", "| | |", "|---|---|",
          "| ⛔ **Tek yazar** | turları yazan ile ölçümü tasarlayan aynı taraf; ikinci okuyucu yok |",
          "| ⛔ **Küçük** | 10 konuşma; durum başına 1-3 konuşma ⇒ durum düzeyinde çıkarım yapılmaz |",
          "| ⚠️ **Sabit senaryo** | kullanıcı modelin cevabına tepki vermez; 2.-4. turlar her cevaba uyacak biçimde yazıldı ama bazı eşleşmeler yine de tuhaf okunabilir |",
          "| ⚠️ **Bulaşma sözcükseldir** | çerçeve benzerliğini yalnız mt-05'te elle yakaladım; sistemli bir çerçeve ölçüsü yok |"]
    RAPOR.write_text("\n".join(s) + "\n", encoding="utf-8")
    print("\n".join(s[2:5])); return 0


if __name__ == "__main__":
    sys.exit(main())
