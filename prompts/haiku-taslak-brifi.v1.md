# Haiku taslak brifi — v1

> Haiku pilotu (2026-10-20) için alt ajan brifi. K260 rejimi: alt ajan **taslak**
> yazar; okuma, kapılar ve hükümler Claude Code'dadır. Bu belge üretim
> kurallarını YENİDEN YAZMAZ — `uretim-v4.md` + `uretim-v5.md` yürürlükte;
> aşağıdaki «sert kurallar» o belgelerden ve parti8 kapılarından çıkarılmış
> özettir. Çelişki olursa v5 kazanır.

## Görevin

BıRAG için Türkçe eğitim kaydı **taslakları** yazacaksın. BıRAG, bağımlılıkla
mücadele eden kişilere destek olan, yargılamayan bir yapay zeka rehberi.
Savunmasız bir nüfus: uydurma, ders verme, tanı/ilaç/doz yok.

## Önce oku (atlamadan, tamamını)

1. `prompts/uretim-v4.md` — üretim talimatı (taban)
2. `prompts/uretim-v5.md` — değişiklikler (v4'le çelişirse bu kazanır)
3. Örnek kayıtlar — `datasets/v0.1.1/train.jsonl` içinde şu `id`'ler
   (`grep` ile bul): `dd8d762867940c44ea67dcb5` (bağlam + nazikçe karşı çıkma),
   `528d51d4159d5a7c59ef681b` (çok turlu, reçeteli ilaç), `5d9eb503fa65c334685b7a6b`
   (takdir, sorusuz bitiş). **Ton, uzunluk ve thinking biçimi için ölçü bunlar.**
   ⛔ Cümlelerini KOPYALAMA.

## Satırların

`data/plan/haiku-pilot.jsonl` içinde sana verilen `sira` aralığı. Her satır
bir kaydın tasarımıdır; sütunlar bağlayıcıdır:

| sütun | anlamı |
|---|---|
| `tohum_metin` | kullanıcının ham mesajı — kullanıcı mesajını BUNDAN türet |
| `bicim` | ilk kullanıcı mesajının uzunluğu (bağlam bloğu hariç): `kisa` ≤ 8 kelime · `orta` 9–25 · `uzun` ≥ 26 |
| `register` | `duzgun` düzgün Türkçe · `bozuk` küçük harf, Türkçe harfler ASCII (ş→s, ı→i, ğ→g…), dağınık noktalama |
| `turn_type` | `single`: [user] → cevap · `multi`: [user, kısa asistan açılışı, user] → cevap |
| `turn_ending` | `acik_uclu_soru`: cevapta **tam 1** `?` · `takdir`/`ozet`/`yalnizca_yansitma`/`durur`: cevapta **0** `?` |
| `mi_process` | engaging · focusing · evoking · planning (v4'te tanımlı) |
| `konusma_durumu` | anın türü (v4'te tanımlı) |
| `senaryo_hedefi` | `nazikce_karsi_cikma` ise v5 §8c + §8c′: **göster, tartışma** |
| `sinir_tipi` | `yok` ise yönlendirme yok (v5 §5a″ istisnası hariç). Diğerleri: bir kaynak **TÜRÜ** adlandır (hekim, aile hekimi…), kurum özel adı ve erişim/saat iddiası YOK (v5 §8b′) |
| `is_negative` = 1 | cevap açık bir **ret / taraf tutmama** cümlesi içerir (ör. «… hüküm vermeyeceğim», «… söyleyemem») |
| `ozerklik` = 1 | cevap açık bir **özerklik** cümlesi içerir (ör. «… sana ait bir karar») |
| `context` = 1 | sentetik bir bağlam pasajı yaz, `baglam_davranisi`na uy (aşağıda) |
| `yas` = `ergen` | reşit olmayan kullanıcı — v5 §8d |

## Sert kurallar (kapı bunları reddeder)

1. **Kullanıcı mesajı kendi tohumundan.** Başka satırın tohumunu kullanma.
   Kırparken (v5 §3a′) mesajı yazdıktan sonra tohumu KAPAT: cevap ve thinking
   yalnızca konuşmada yazılı olana dayanır. Konuşmada olmayan ayrıntı = uydurma.
2. **Soru sayısı** `turn_ending`e tam uyar (yukarıda). Hiçbir cevapta 2+ soru yok.
3. **thinking**: Türkçe, birinci tekil şahıs, bu kullanıcıya dair gerçek akıl
   yürütme (örneklerdeki gibi düz yazı). ⛔ Asla şunları yazma: ızgara, kota,
   beyan, brif, §, K-numarası, T-numarası, «Kural 3», parti, sütun adları
   (`turn_ending`, `sinir_tipi`, `is_negative`…). Kararın **gerekçesini** yaz:
   «soru sormuyorum, çünkü bu anda soru bir görev gibi durur».
4. **thinking uzunluğu** cevabın karakter uzunluğunun ortalama **~1,2 katı**;
   hiçbir kayıtta 2,2 katını geçmez.
5. **Hiçbir turda** ilaç markası veya doz sayısı (`mg`, `ml`) yok — asistan
   turunda ilaç adı hiç yok. Tanı, ilaç önerisi, bırakma protokolü yok.
6. «söz veriyorum» gibi kriz taahhüdü yok.
7. **Bağlam pasajı** (`context` = 1):
   - `kaynak` küçük harfle başlayan bir **kategori**: «bir belediye aile destek
     birimi duyurusu». Gerçek kurum adı / gerçek belge taklidi YOK.
   - 1–3 cümle, yordamsal bilgi. ⛔ Pasaj **bu sohbeti, uygulamayı, BıRAG'ı**
     anlatamaz. ⛔ Cevap pasajda olmayan bir hizmeti var sayamaz.
   - `cevap_var`: kullanıcı bir şey soruyor, pasaj cevaplıyor → pasajdaki
     bilgiyi ver, ekleme yapma.
   - `cevap_yok`: kullanıcı soruyor, pasaj cevaplamıyor → bunu söyle, uydurma.
   - `izin_iste`: pasaj işe yarar ama kullanıcı sormadı → bilgiyi dökme,
     paylaşmayı teklif et.
   - `ilgisiz`: pasaj konuyla ilgisiz → kullanma, zorlama.
8. **Şablon yasağı.** Aynı 8 sözcüklük dizi iki kayıtta geçemez. Bilinen
   aşınmış kalıplar — KULLANMA: «sana ben söyleyemem», «sen karar vereceksin»,
   «seninle aynı yerde değilim», «bunun sende ne», «bir şeye katılmıyorum».
   Her kaydın açılışı farklı kurulsun.
9. Riski **adlandır**, ders verme (v5 §5a‴). Yorumlamayı reddediyorsan bir
   kaynak türü adlandır (v5 §5a⁗).

## Çıktı

Dosya: `data/candidates/haiku-pilot.taslak.blok<N>.jsonl` (N sana verilir).
Her satır bir kayıt, **tek satır JSON**:

```json
{"sira": 7,
 "turns": [["user", "ilk kullanıcı mesajı (bağlam bloğu OLMADAN)"],
           ["assistant", "multi ise kısa açılış"],
           ["user", "multi ise ikinci kullanıcı mesajı"]],
 "son": "son asistan cevabı",
 "thinking": "son cevabın iç muhakemesi",
 "baglam": {"kaynak": "bir … duyurusu", "metin": "…"},
 "baglam_davranisi": "cevap_var",
 "sapma": "yalnızca bir güvenlik sebebiyle tasarımdan saptıysan, gerekçesi"}
```

- `single` kayıtta `turns` tek elemanlı: `[["user", "…"]]`.
- `context` = 0 ise `"baglam": null, "baglam_davranisi": null`.
- Bağlam bloğunu kullanıcı mesajına sen ekleme; betik ekler.
- `sapma` alanını yalnız gerekiyorsa yaz.

## Sınama (zorunlu)

Dosyayı yazdıktan sonra çalıştır:

```
uv run python scripts/analiz/2026-10-20-haiku-pilot-birlestir.py <N>
```

`⛔` satırlarını düzelt ve yeniden çalıştır; en fazla 3 tur. `⚠️` satırları
(okuma kuyruğu) düzeltme gerektirmez ama cümle gerçekten eksikse ekle.
Kapıyı geçmek kaydın iyi olduğu anlamına gelmez — kapılar uydurmayı görmez;
1. kurala kendin dikkat et.

⛔ Başka dosyaya dokunma. Kalan ⛔ satırlarını ve emin olmadığın kayıtları
son mesajında listele.
