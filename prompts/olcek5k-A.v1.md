# Ölçek-5k · A aşaması brifi — v1 (kullanıcı tarafı)

> Üç aşamalı üretimin ilki. Sen yalnız **kullanıcının söylediklerini** (ve çok
> turluda kısa bir asistan açılışını, bağlam kaydında pasajı) yazarsın. Son
> cevabı bir başka ajan, **tohumu görmeden** yazacak: senin yazdığın konuşma
> onun elindeki TEK bilgidir.

## Önce oku

`prompts/uretim-v4.md` içinde yalnız şu bölümler: **§3 (3a, 3b, 3c)**, **§6**, **§7b**.
`prompts/uretim-v5.md` içinde: **§3a′** (kırpma kuralı), **§7a″** yalnız «pasaj çifti nasıl yazılır».

## Girdi

```
uv run python scripts/analiz/2026-10-20-olcek5k-arac.py a-girdi <N>
```
25 satır. Her satırda `tohum_metin` (gerçek kullanıcı mesajı) ve tasarım sütunları.

## Her satır için yaz

1. **Kullanıcı mesajı(ları)** — `tohum_metin`den türet; konuşmada kalacak her ayrıntı
   tohumdan gelir, **yeni olay/kişi/sayı uydurma**.
   - `bicim`: İLK kullanıcı mesajı `kisa` ≤ 8 kelime · `orta` 9–25 · `uzun` ≥ 26.
   - `register`: `duzgun` düzgün Türkçe · `bozuk` küçük harf, Türkçe harfler ASCII (ş→s, ğ→g, ı→i, ö→o, ü→u, ç→c), gevşek noktalama.
   - `turn_type = multi`: `[user, assistant, user]` — ilk mesaj kısa bir giriş, ikinci
     mesaj asıl anlatı (v4 §3c). Kırptığın tohum ayrıntısını **ikinci mesaja** koy; cevap
     ancak konuşmada yazılı olana dayanabilir.
   - `konusma_durumu` mesajın hangi anda yazıldığını belirler (v4 §3b).
   - İlaç markası, kurum özel adı (AMATEM, YEDAM…), doz sayısı (mg/ml) → genelleştir:
     «sakinleştirici», «reçeteli ilacım», «bağımlılık merkezi», «yarım tane».
2. **Asistan açılışı** (yalnız `multi`): bir cümle, ilk kullanıcı mesajına **özgü** — ⛔ ilk
   mesajda YAZMAYAN bir ayrıntıyı (tohumda olsa bile) anamaz, soramaz.
   ⛔ «Dinliyorum», «Buradayım», «Anlat», «Devam et» ile BAŞLAMAZ. Parçadaki 25 kayıtta
   iki açılış aynı olamaz. En fazla bir soru. ⛔ Hitap **«sen»** — «siz», «sizi», «-sınız»,
   «-nız» YOK (BıRAG kullanıcıya «sen» der). Örnek: *«Broşür hâlâ masada mı?»* ·
   *«Aramadan önce ne oldu?»* · *«Kahve faslı nasıl geçti?»*
3. **Bağlam** (yalnız `context = 1`): `{"kaynak": "...", "metin": "..."}`
   - `kaynak` küçük harfle başlayan bir **kategori**: «bir belediye aile destek birimi duyurusu».
   - 1–3 cümle yordamsal bilgi. ⛔ Bu sohbeti / uygulamayı / BıRAG'ı anlatamaz.
   - Kullanıcı mesajı `baglam_davranisi`yla UYUMLU olmalı:
     `cevap_var` → kullanıcı pasajın cevapladığı yordamsal bir şey SORAR ·
     `cevap_yok` → kullanıcı bir şey sorar, pasaj aynı alandadır ama O SORUYU cevaplamaz ·
     `izin_iste` → pasaj işe yarar ama kullanıcı sormaz ·
     `ilgisiz` → pasaj konuyla ilgisizdir.
4. **Tasarımın kullanıcıya düşen payı:**
   - `sinir_tipi = yonlendirme_istegi` → kullanıcı açıkça «kime / nereye sorabilirim» der.
   - `sinir_tipi = rol_siniri_yonlendirme` → kullanıcı tanı/ilaç/hukuk gibi BıRAG'ın cevaplayamayacağı bir şey sorar.
   - `senaryo_hedefi = nazikce_karsi_cikma` → kullanıcı mesajında itiraz edilebilir, yanlış ya da kendini kandıran bir İDDİA bulunur (tohumda varsa onu koru).
   - `yas = ergen` → reşit olmayan biri gibi yaz (okul, aile, harçlık).

## Çıktı

`data/candidates/olcek5k/A/parca<NNN>.jsonl` (NNN üç haneli: 7 → `007`). Satır başına bir JSON:

```json
{"sira": 1234, "turns": [["user", "…"], ["assistant", "…"], ["user", "…"]], "baglam": null}
```
`single` → `"turns": [["user", "…"]]`. Bağlam yoksa `"baglam": null`.

## Sınama (zorunlu)

```
uv run python scripts/analiz/2026-10-20-olcek5k-arac.py a-kontrol <N>
```
`⛔` satırlarını düzelt, yeniden çalıştır (en fazla 3 tur). Başka dosyaya dokunma.
