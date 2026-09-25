#!/usr/bin/env python3
"""Judge ve kapıların v5-parti4'te bulduğu 12 uydurma dayanağı düzeltir.

⛔⛔ **Neden var (T123).** Kör bir judge 60 kayıtta **8 uydurma dayanak** buldu;
üç kapı (zaman/kaynak · alıntı birebirlik · mekân), delikleri kapatıldıktan
sonra bunların 6'sını ve **4 tane daha** gösterdi. Toplam **12 kayıt**.

⭐ **Düzeltme ilkesi:** uydurulmuş ayrıntı SİLİNİR ya da kullanıcının kendi
sözüyle DEĞİŞTİRİLİR. Cümlenin işlevi korunur; ayrıntı uydurulmuşsa işlev
başka bir dayanağa taşınır.

⛔ Orijinal `v5-parti4.v2.arinmis.jsonl` DEĞİŞTİRİLMEZ (Kural 7); çıktı yeni
sürüme yazılır. ⛔ Değişen 12 kaydın `judge` alanı BOŞALTILIR: eski puan yeni
metni tarif etmez.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
GIRDI = KOK / "data/candidates/v5-parti4.v2.arinmis.jsonl"
CIKTI = KOK / "data/candidates/v5-parti4.v3.jsonl"

D = {
 3: ("İkisi de aynı hafta içinde.",
     "İkisi de arka arkaya oldu: düşünmek ve vazgeçmek."),
 5: ('Söyleyebilecek olan da o: azaltmayı yapan hekime "belki abartıyorum" dediğin şeyi olduğu gibi anlatmak buradan atılabilecek en yakın adım.',
     'Söyleyebilecek olan da o: doktoruna "Belki ben abartıyorum" dediğin şeyi olduğu gibi anlatmak buradan atılabilecek en yakın adım.'),
 19: ('Bir şeye katılmıyorum ama: "nasıl geçireceğim bilmiyorum" derken sanki üç günü tek parça hâlinde taşıyacakmışsın gibi kuruyorsun cümleyi.',
      'Bir şeye katılmıyorum ama: "üç günü nasıl geçiricem bilmiyorum" derken sanki üç günü tek parça hâlinde taşıyacakmışsın gibi kuruyorsun cümleyi.'),
 20: ('"İş çıkışı" dediğin şeye hafta içi bahane diyorsun; demek ki o da bir açıklamaydı, sebep değil.',
      '"Hafta içi bahanem oluyor" dedin; bahane bir açıklamadır, sebep değil.'),
 21: ("Bugün bir odada durup bunu sesli söyledin.",
      "Bugün onların yanında durup bunu sesli söyledin."),
 26: ("Ne yapacağını bilmen gerekmiyor; sayıyı on dakika önce öğrendin.",
      "Ne yapacağını bilmen gerekmiyor; hesabı kafandan sen yaptın."),
 29: ('"Hiç hazır olmayacağım" bir tahmin, üç ertelemeden çıkarılmış.',
      '"galiba hiç hazır olmuycam" bir tahmin, üç ertelemeden çıkarılmış.'),
 # ⛔ #36'nın TÜM KAPANIŞI uydurma: kullanıcının tek turu «Sence o adam
 # gerçekten kazanıyor mu?» — ne abi var, ne hesap, ne «iki deneme». Kapanış
 # kullanıcının kendi sorusuna bağlanıyor (ızgara `acik_uclu_soru` istiyor).
 36: ("Abinin hesabıyla denemiştin. O iki denemede ne oldu?",
      "O adamın kazandığını sana ne gösterdi?"),
 47: ("İkiniz de aynı mutfakta duruyorsunuz.",
      "İkiniz de aynı sessizliğin içindesiniz."),
 49: ('"Sosyal içici" ile "bağımlılık yok" arasına bir eşittir koydun ve ben oraya katılmıyorum — birincisi ne zaman içtiğini anlatıyor, ikincisi bambaşka bir şey.',
      '"sosyal içiciyim" ile "önemli değil" arasına bir eşittir koydun ve ben oraya katılmıyorum — birincisi ne zaman içtiğini anlatıyor, ikincisi bir hüküm.'),
 54: ("Bilmiyor olman bugün bir eksiklik değil; sayıyı dün bilmiyordun.",
      "Bilmiyor olman bir eksiklik değil; bilmediğini söyleyebilmişsin."),
 60: ('Sorduğun soru "kim sürecek" idi; metnin cevabı "sen değil".',
      "Sorduğun şey kimin sürebileceğiydi ve metin bunu belge koşuluna bağlıyor."),
}


def main() -> int:
    n = 0
    out = []
    for s in GIRDI.read_text(encoding="utf-8").splitlines():
        if not s.strip():
            continue
        r = json.loads(s)
        sira = r["gen_meta"]["parti_sira"]
        if sira in D:
            eski, yeni = D[sira]
            son = [m for m in r["messages"] if m["role"] == "assistant"][-1]
            assert eski in son["content"], f"#{sira}: eski metin bulunamadı"
            son["content"] = son["content"].replace(eski, yeni).strip()
            r["judge"] = None          # ⛔ eski puan yeni metni tarif etmez
            n += 1
        out.append(json.dumps(r, ensure_ascii=False))
    CIKTI.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"→ {CIKTI.relative_to(KOK)} ({len(out)} kayıt) · düzeltilen {n}/{len(D)}")
    return 0 if n == len(D) else 1


if __name__ == "__main__":
    raise SystemExit(main())
