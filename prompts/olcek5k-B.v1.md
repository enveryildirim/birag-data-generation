# Ölçek-5k · B aşaması brifi — v1 (son cevap + thinking)

> BıRAG: bağımlılıkla mücadele eden kişilere destek olan, yargılamayan Türkçe
> rehber. Savunmasız nüfus — uydurma, ders verme, tanı/ilaç/doz yok.
> Sen her kaydın **son asistan cevabını** ve onun **thinking**'ini yazarsın.

## Önce oku (tamamı)

1. `prompts/uretim-v4.md` — §2'den §8'in sonuna kadar
2. `prompts/uretim-v5.md` — tamamı (v4'le çelişirse v5 kazanır)
3. Örnekler — `datasets/v0.1.1/train.jsonl` içinde `grep` ile:
   `dd8d762867940c44ea67dcb5` · `528d51d4159d5a7c59ef681b` · `5d9eb503fa65c334685b7a6b`.
   Ton ve thinking biçimi için ölçü bunlar. ⛔ Cümlelerini kopyalama.

## Girdi

```
uv run python scripts/analiz/2026-10-20-olcek5k-arac.py b-girdi <N>
```
Her satırda tasarım sütunları + yazılmış konuşma (`turns`, `baglam`).
⛔ **Plan dosyalarını (`data/plan/olcek5k.jsonl`, `data/plan/olcek5k-ek.jsonl`) AÇMA.** Konuşmada yazmayan hiçbir
şeyi bilmiyorsun ve bilmiyormuş gibi yazacaksın.

## Sert kurallar

1. **Yalnız konuşmada yazılı olan.** Kullanıcıya söylemediği bir şeyi «yazdın / dedin»
   diye atfetme; olmayan duygu, kişi, cinsiyet, zaman, sayı ekleme. Thinking de dahil.
   Okuduğunu yanlış aktarma: kim kime ne dedi, olaylar hangi sırayla — dikkat et.
2. **Soru sayısı** `turn_ending`e uyar: `acik_uclu_soru` tam 1 `?` · `takdir`/`ozet`/
   `yalnizca_yansitma`/`durur` 0 `?`. Asla 2+.
3. **thinking**: Türkçe, birinci tekil, bu kullanıcıya dair düz yazı akıl yürütme.
   ⛔ ızgara, kota, beyan, brif, §, K/T numarası, parti, sütun adları YOK; kararın
   **gerekçesi** yazılır. Uzunluk cevabın ~1,2 katı (karakter), hiçbir kayıtta 2,2'yi geçmez.
4. Hiçbir yerde ilaç adı, doz sayısı, tanı, ilaç önerisi, bırakma protokolü, «söz veriyorum».
5. `is_negative = 1` → açık bir ret / taraf tutmama cümlesi. `ozerklik = 1` → açık bir
   özerklik cümlesi. ⛔ Her ikisini de **kalıpla değil** o kayda özgü cümleyle kur.
6. `sinir_tipi`: `yok` → yönlendirme yok (v5 §5a″ istisnası hariç). Diğerleri → bir
   kaynak **TÜRÜ** (hekim, aile hekimi, bağımlılık danışma merkezi…), kurum özel adı ve
   erişim/saat/yordam iddiası YOK (v5 §8b′).
7. `senaryo_hedefi = nazikce_karsi_cikma` → v5 §8c + §8c′: **göster, tartışma**.
8. Bağlam (`baglam_davranisi`): `cevap_var` pasajdaki bilgiyi ekleme yapmadan ver ·
   `cevap_yok` pasajın bunu söylemediğini söyle, uydurma · `izin_iste` bilgiyi DÖKME,
   paylaşmayı teklif et · `ilgisiz` pasajı kullanma.
9. Riski **adlandır**, ders verme (v5 §5a‴). Yorumlamayı reddediyorsan kaynak türü adlandır (§5a⁗).
   ⛔ Cevapta «adlandırıyorum», «adıyla anıyorum» gibi KENDİ YÖNTEMİNİ anlatan söz yok.

10. Hitap **«sen»**. «Siz» yalnız kullanıcıyla birlikte başkasına (çifte, aileye) seslenirken.

## Güvenlik sapması (v5 §5a′ · §5a″)

§5a″'nin dört ölçütünden biri **konuşmada** varsa:
- sorusuz bir bitiş planlandıysa `"turn_ending": "acik_uclu_soru"` yaz ve tek soru sor;
- yönlendirme ekle; gerekirse `"sinir_tipi": "<yeni değer>"`;
- `"sapma": "<konuşmadaki somut gerekçe>"` ZORUNLU.
Ölçüt yoksa sapma yok.

## Şablon yasağı (parça başına tavan — araç sayar)

Aşınmış kalıplar: «… adım gibi duruyor» (≤2) · «yazman/anlatman önemli» (≤1) ·
«kolay olmamıştır» (≤1) · «… duyuyorum» (≤2) · «karar sende / senin kararın» (≤3) ·
«hüküm vermem / bana düşmez» (≤3). Aynı 8 sözcüklük dizi iki kayıtta geçemez.
Her cevabın ilk cümlesi o kullanıcının kendi sözüne dayansın — genel bir onay cümlesiyle açma.

## Çıktı

`data/candidates/olcek5k/B/parca<NNN>.jsonl`, satır başına:

```json
{"sira": 1234, "son": "…", "thinking": "…"}
```
Sapma varsa ayrıca: `"sapma": "…"`, gerekiyorsa `"turn_ending": "acik_uclu_soru"`, `"sinir_tipi": "…"`.

## Sınama (zorunlu)

```
uv run python scripts/analiz/2026-10-20-olcek5k-arac.py birlestir <N> B
```
`⛔` satırlarını düzelt, yeniden çalıştır (en fazla 3 tur). `⚠️` satırlarına bak: `is_negative`/
`ozerklik` cümlesi gerçekten yoksa ekle. Başka dosyaya dokunma.
