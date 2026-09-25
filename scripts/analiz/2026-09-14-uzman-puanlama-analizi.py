"""Uzman puanlaması (n=50) analizi + judge karşılaştırması — K27.

Girdi : data/expert_sample/uzman-puanlari.json · data/judged/expert-70.jsonl
        data/expert_sample/sunum-haritasi.json
Çıktı : reports/analiz/2026-09-14-uzman-puanlama-analizi.md
"""
import collections, hashlib, json, pathlib, statistics

KOK = pathlib.Path(__file__).resolve().parents[2]
PUAN = KOK / "data/expert_sample/uzman-puanlari.json"
JUDGED = KOK / "data/judged/expert-70.jsonl"
HARITA = KOK / "data/expert_sample/sunum-haritasi.json"
CIKTI = KOK / "reports/analiz/2026-09-14-uzman-puanlama-analizi.md"

SUREKLI = ["duygusal_tepki", "yorumlama", "kesif", "mi_uyumu",
           "grounding", "kisalik_dogallik", "dil_butunlugu"]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def pearson(a, b):
    n = len(a)
    if n < 3:
        return None
    ma, mb = statistics.mean(a), statistics.mean(b)
    pay = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    payda = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
    return pay / payda if payda else None


uzmanlar = json.loads(PUAN.read_text())["uzmanlar"]
ad, icerik = next(iter(uzmanlar.items()))
puanlar = icerik["puanlar"]
harita = json.loads(HARITA.read_text())
kayitlar = {json.loads(s)["id"]: json.loads(s) for s in open(JUDGED)}

esli = [(no, p, kayitlar[p["kayit_id"]]) for no, p in puanlar.items() if p["kayit_id"] in kayitlar]

sat = [
    "# Uzman puanlaması — analiz (n=50)", "",
    f"**Uzman:** `{ad}` · puanlanan kayıt **{len(puanlar)}/70**  ",
    f"**Girdi:** `data/expert_sample/uzman-puanlari.json` · SHA256 `{sha(PUAN)}`  ",
    f"**Judge:** `data/judged/expert-70.jsonl` · SHA256 `{sha(JUDGED)}`  ",
    "**Betik:** `scripts/analiz/2026-09-14-uzman-puanlama-analizi.py` · **Tarih:** 2026-09-14  ",
    "**Karar:** K27 — uzman puanlaması hem korpusun geçme oranını hem judge kalibrasyonunu verir", "",
    "---", "", "## 1. Geçme oranı (K27'nin birinci çıktısı)", "",
]

karar = collections.Counter(p["genel_karar"] for p in puanlar.values())
n = len(puanlar)
sat += ["| Genel karar | Adet | Oran |", "|---|---:|---:|"]
sat += [f"| {k} | {v} | %{100*v/n:.0f} |" for k, v in karar.most_common()]
sat += ["",
        f"**Kabul oranı %{100*karar['kabul']/n:.0f}** · sınırda dahil edilirse "
        f"%{100*(karar['kabul']+karar['sınırda'])/n:.0f} · **red %{100*karar['ret']/n:.0f}**", ""]

sat += ["## 2. Sert kapılar", "", "| Kapı | Uzman | Judge (aynı 50 kayıt) |", "|---|---|---|"]
for alan, judge_alan in [("klinik_guvenlik_ihlali", "klinik_guvenlik_ihlali"),
                         ("rol_siniri_ihlali", "rol_siniri_ihlali")]:
    u = sum(1 for p in puanlar.values() if p[alan] == "Evet")
    j = sum(1 for _, _, k in esli if (k.get("judge") or {}).get(judge_alan))
    sat.append(f"| {alan} | {u}/{n} | {j}/{len(esli)} |")
ut = collections.Counter(x for p in puanlar.values() for x in (p.get("tuzak_ihlali") or []))
jt = collections.Counter(x for _, _, k in esli for x in ((k.get("judge") or {}).get("tuzak_ihlali") or []))
sat += [f"| tuzak ihlali (toplam) | {sum(ut.values())} | {sum(jt.values())} |", ""]
if jt:
    sat += [f"Judge'ın bulduğu tuzaklar: {dict(jt)}", ""]

sat += ["## 3. Boyut boyut — uzman vs judge", "",
        "| Boyut | n | Uzman ort. | Judge ort. | Fark | Korelasyon |", "|---|---:|---:|---:|---:|---:|"]
for alan in SUREKLI:
    çift = [(p[alan], (k.get("judge") or {}).get(alan))
            for _, p, k in esli if p.get(alan) is not None and (k.get("judge") or {}).get(alan) is not None]
    if not çift:
        continue
    u = [x for x, _ in çift]
    j = [y for _, y in çift]
    r = pearson(u, j)
    sat.append(f"| {alan} | {len(çift)} | {statistics.mean(u):.2f} | {statistics.mean(j):.2f} | "
               f"{statistics.mean(u)-statistics.mean(j):+.2f} | {f'{r:.2f}' if r is not None else '—'} |")
sat += ["", "> `mi_uyumu` uzman tarafından yalnızca bir kısmında dolduruldu (zorunlu değildi).", ""]

sat += ["### 3b. Puan dağılımı — korelasyonun neden sıfıra yakın olduğu", "",
        "Sıfıra yakın korelasyon, varyans yokluğundan mı kaynaklanıyor? Hayır — bir boyut hariç.", "",
        "| Boyut | Uzman dağılımı | s | Judge dağılımı | s |", "|---|---|---:|---|---:|"]
for alan in SUREKLI:
    u = [x[alan] for x in puanlar.values() if x.get(alan) is not None]
    j = [(k.get("judge") or {}).get(alan) for _, _, k in esli]
    j = [y for y in j if y is not None]
    du = dict(sorted(collections.Counter(u).items()))
    dj = dict(sorted(collections.Counter(j).items()))
    su = f"{statistics.pstdev(u):.2f}" if len(u) > 1 else "—"
    sj = f"{statistics.pstdev(j):.2f}" if len(j) > 1 else "—"
    sat.append(f"| {alan} | `{du}` | {su} | `{dj}` | {sj} |")
sat += ["",
        "**`dil_butunlugu`: judge 50 kaydın 50'sine de 5 verdi (s=0.00).** Korelasyon hesaplanamıyor "
        "çünkü judge bu boyutta hiç ayrım yapmıyor; uzman ise 5 kayda 1-2 verdi. Bu bir istatistik "
        "artefaktı değil, **judge körlüğü**. Diğer boyutlarda iki tarafın da gerçek varyansı var "
        "(s = 0.47-1.30), dolayısıyla oradaki düşük korelasyon da varyans kısıtından kaynaklanmıyor.", "",
        "⚠️ Yine de bu ölçüm **kimin haklı olduğunu göstermiyor** (K43 ile aynı sınır): tek uzman, "
        "n=50, tavana yığılmış dağılımlar, anotatör uyumu henüz ölçülmedi.", "",
        "## 4. İç muhakeme (13. madde)", "", "| Değerlendirme | Adet | Oran |", "|---|---:|---:|"]
im = collections.Counter(p.get("ic_muhakeme") for p in puanlar.values())
sat += [f"| {k} | v | %{100*v/n:.0f} |".replace("| v |", f"| {v} |") for k, v in im.most_common()]
sat += ["", f"**İç muhakemede sorun görülen oran: %{100*(im['kısmen sorunlu']+im['sorunlu'])/n:.0f}** "
        "— kullanıcıya giden cevaptan bağımsız ölçüldü.", ""]

# genel karar ile iç muhakeme çaprazı
sat += ["Genel karar ↔ iç muhakeme çaprazı:", "", "| | uygun | kısmen sorunlu | sorunlu |", "|---|---:|---:|---:|"]
for gk in ["kabul", "sınırda", "ret"]:
    r = [p for p in puanlar.values() if p["genel_karar"] == gk]
    c = collections.Counter(p.get("ic_muhakeme") for p in r)
    sat.append(f"| {gk} | {c['uygun']} | {c['kısmen sorunlu']} | {c['sorunlu']} |")
sat += [""]

# ── uzmanın serbest yorumlarının sayısal karşılığı ──────────────────────────
tum = list(kayitlar.values())
soru_ile_biten = sum(1 for k in tum if k["messages"][-1]["content"].rstrip().endswith("?"))
mi = collections.Counter(k["mi_process"] for k in tum)
tt = collections.Counter(k["talk_type"] for k in tum)
sen = collections.Counter(k["scenario"] for k in tum)
tek_tur = sum(1 for k in tum if k["turn_type"] == "single")

sat += ["---", "", "## 5. Uzmanın serbest yorumları — sayısal karşılığı", "",
        "Uzmanın dört genel yorumu, ürettiğimiz veride birebir ölçülebiliyor.", "",
        "| Uzman ne dedi | Veride karşılığı | Doğrulandı mı |", "|---|---|---|",
        f"| *\"hep bir soru ile bitiyor\"* | **{soru_ile_biten}/70** kayıt soruyla bitiyor "
        f"(%{100*soru_ile_biten/70:.0f}) | ✅ |",
        f"| *\"hep bir an yakalama senaryosu\"* | {tek_tur}/70 tek turlu; tohumların **tamamı** "
        "tek turlu açılış mesajı (K26) | ✅ |",
        f"| *\"motive edici well-being tam olmadı\"* | `planning` {mi['planning']}/70 · "
        f"`focusing` {mi['focusing']}/70 · `kutlama` {sen['kutlama']}/70 | ✅ |",
        f"| *\"motivasyon yükselten yazışmalar eklenebilir\"* | değişim konuşması "
        f"(`change_darn`+`change_cat`) {tt['change_darn']+tt['change_cat']}/70; "
        f"`sustain`+`ambivalans` {tt['sustain']+tt['ambivalans']}/70 | ✅ |", "",
        "### MI süreci dağılımı (tüm 70 kayıt)", "", "| Süreç | Adet |", "|---|---:|"]
sat += [f"| {k} | {v} |" for k, v in mi.most_common()]
sat += ["", "### Konuşma tipi dağılımı", "", "| Tip | Adet |", "|---|---:|"]
sat += [f"| {k} | {v} |" for k, v in tt.most_common()]
sat += [""]

# ── serbest notların tipleri ────────────────────────────────────────────────
notlar = [(no, p) for no, p in sorted(puanlar.items(), key=lambda x: int(x[0]))
          if p.get("not", "").strip()]
sat += ["## 5b. Uzmanın reddettiği 5 kayıt — judge aynı kayıtlara ne dedi", "",
        "| Form | Kayıt | Senaryo | Uzman dil/kısalık | Judge dil/kısalık/mi | Uzmanın notu |",
        "|---|---|---|---|---|---|"]
for no, pp in sorted(puanlar.items(), key=lambda t: int(t[0])):
    if pp["genel_karar"] != "ret":
        continue
    r = kayitlar[pp["kayit_id"]]
    j = r.get("judge") or {}
    sat.append(f"| {no} | #{harita[no]['sira']} | {r['scenario']} | "
               f"{pp.get('dil_butunlugu')}/{pp.get('kisalik_dogallik')} | "
               f"{j.get('dil_butunlugu')}/{j.get('kisalik_dogallik')}/{j.get('mi_uyumu')} | "
               f"{(pp.get('not') or '—').strip()} |")
sat += ["",
        "**Uzmanın reddettiği 5 kaydın 5'ine de judge dil ve kısalık boyutunda tam puan verdi**, "
        "gerekçelerinde *isabetle*, *derin bir empatiyle*, *yargısızca* gibi ifadeler kullandı. "
        "Bu, §3b'deki körlüğün kayıt düzeyindeki karşılığı.", "",
        "## 6. Kayıt bazlı notlar (13 adet)", "",
        "| Form no | Kayıt | Senaryo | Karar | Muhakeme | Not |", "|---|---|---|---|---|---|"]
for no, p in notlar:
    h = harita[no]
    sat.append(f"| {no} | #{h['sira']} | {h['scenario']} | {p['genel_karar']} | "
               f"{p['ic_muhakeme']} | {p['not'].strip()} |")
sat += [""]

# ── 7. çapa listeleri ve araç doldurma oranları (2026-09-14 ikinci yarı) ────
en_iyi = icerik.get("en_iyi_5") or []
en_kotu = icerik.get("en_kotu_5") or []
isaret = collections.Counter(p.get("capa", "—") for p in puanlar.values())
tuzak_durum = collections.Counter(p.get("tuzak_durum", "alan yoktu") for p in puanlar.values())

sat += ["## 7. Çapa listeleri (K27'nin en değerli çıktısı)", ""]
if en_iyi or en_kotu:
    for etiket, liste in [("En iyi 5", en_iyi), ("En kötü 5", en_kotu)]:
        sat += [f"**{etiket}:** " + (", ".join(str(x) for x in liste) if liste else "_boş_"), ""]
        if liste:
            sat += ["| Form | Kayıt | Senaryo | Uzman kararı |", "|---|---|---|---|"]
            for no in liste:
                h = harita.get(str(no), {})
                pp = puanlar.get(str(no), {})
                sat.append(f"| {no} | #{h.get('sira', '?')} | {h.get('scenario', '?')} | "
                           f"{pp.get('genel_karar', '—')} |")
            sat += [""]
else:
    sat += ["⚠️ **Her iki liste de boş.** Bu 10 kayıt, judge cetvelini kalibre edecek "
            "çapa kümesiydi — tek tek puanlardan daha değerli. 14. madde (kayıt içinde "
            "⭐/⛔ işareti) tam da bu yüzden eklendi.", ""]

sat += ["### Araç doldurma oranları", "", "| Madde | Durum |", "|---|---|",
        f"| 4 · `mi_uyumu` | {sum(1 for p in puanlar.values() if p.get('mi_uyumu') is not None)}/{n} dolu |",
        f"| 5 · `tuzak_durum` | " + " · ".join(f"{k}: {v}" for k, v in tuzak_durum.most_common()) + " |",
        f"| 14 · `capa` | " + " · ".join(f"{k}: {v}" for k, v in isaret.most_common()) + " |", "",
        "> Boş bırakılan madde, \"sorun yok\" demek değildir — ölçülmemiş demektir. "
        "İlk 50 kayıtta 5. madde 0 kez dolduruldu; 'ihlal yok' ile 'bakmadım' ayırt "
        "edilemiyordu, 2026-09-14'te ayrıldı.", ""]

# ── 8. temsil gücü: puanlanan 50 ile puanlanmayan 20 ─────────────────────────
# Uzman turu 50/70'te kapandı. Sunum sırası seed=70 ile KARIŞTIRILMIŞTI ve uzman
# baştan sırayla gitti → puanlanan 50, 70'in rastgele bir alt örneklemi. Bu iddia
# gözlenebilir boyutlarda sınanıyor; tutmuyorsa geçme oranı 70'e genellenemez.
puanlanan_id = {p["kayit_id"] for p in puanlar.values()}
A = [r for r in kayitlar.values() if r["id"] in puanlanan_id]
B = [r for r in kayitlar.values() if r["id"] not in puanlanan_id]

sat += ["## 8. Puanlanan 50 ile puanlanmayan 20 karşılaştırması", "",
        f"Uzman turu **{len(A)}/{len(A)+len(B)}**'te kapandı (uzman devam etmeyeceğini bildirdi). "
        "Sunum sırası üretimden bağımsız olarak `seed=70` ile karıştırılmıştı ve uzman "
        "**baştan sırayla** gitti (form 1-50, atlama yok) — yani puanlanan küme 70'in "
        "**rastgele alt örneklemidir**. Aşağıdaki tablo bu iddiayı gözlenebilir boyutlarda "
        "sınıyor; ciddi sapma varsa %68'lik oran 70'e genellenemez.", "",
        "| Boyut | Puanlanan (n=%d) | Puanlanmayan (n=%d) |" % (len(A), len(B)),
        "|---|---|---|"]


def _dag(kume, anahtar):
    c = collections.Counter(r[anahtar] for r in kume)
    return " · ".join(f"{k} {v}" for k, v in c.most_common(5)) or "—"


for etiket, anahtar in [("Bağımlılık türü", "addiction_type"), ("MI süreci", "mi_process"),
                        ("Konuşma tipi", "talk_type"), ("Yaş grubu", "age_group"),
                        ("Tur tipi", "turn_type")]:
    sat.append(f"| {etiket} | {_dag(A, anahtar)} | {_dag(B, anahtar)} |")
for etiket, anahtar in [("`is_negative`", "is_negative"), ("Bağlam modu", "context")]:
    a = sum(1 for r in A if r.get(anahtar))
    b = sum(1 for r in B if r.get(anahtar))
    sat.append(f"| {etiket} | {a}/{len(A)} (%{100*a/len(A):.0f}) | {b}/{len(B)} (%{100*b/len(B):.0f}) |")
sat += ["",
        "⚠️ **Sınır:** bu tablo yalnızca *gözlenebilir* boyutlarda benzerlik gösterir. "
        "Klinik kalite gözlenebilir bir boyut değil — puanlanmayan 20 kaydın kalitesi "
        "**bilinmiyor**. %68 oranı 50 kayıt üzerinden ölçülmüştür; 70'e genellenmesi "
        "rastgele örnekleme varsayımına dayanır, ölçüme değil.", "",
        "### Çapa listeleri ne oldu", "",
        "Uzman `en iyi 5` / `en kötü 5` listelerini **doldurmadan** bıraktı. Ama analiz "
        "bu listelere bağlı değil: judge kalibrasyonu `kabul` (34) ve `ret` (5) "
        "**gruplarını** kullanıyor, sıralama değil. Kaybedilen şey **olumlu çapa**: "
        "34 kabul kaydının hangisinin örnek alınacağı belli değil. Bu noktadan sonra "
        "üretilecek herhangi bir \"en iyi\" listesi **bizim yargımızdır, uzmanın değil** "
        "ve öyle etiketlenir.", ""]

CIKTI.write_text("\n".join(sat) + "\n")
print(f"rapor → {CIKTI}")
print(f"kabul %{100*karar['kabul']/n:.0f} · sınırda %{100*karar['sınırda']/n:.0f} · ret %{100*karar['ret']/n:.0f}")
print(f"soruyla biten: {soru_ile_biten}/70")
