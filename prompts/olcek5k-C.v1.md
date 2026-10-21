# Ölçek-5k · C aşaması brifi — v1 (hata avı ve düzeltme)

> Sen puan vermezsin (K43: puanlayan judge Claude olamaz). Rolün **hata avı**:
> her kaydı oku, kusurluysa düzelt, düzeltilemiyorsa düşür. Kayıtlar gerçek
> kullanıcılara gidecek bir modeli eğitecek; savunmasız bir nüfus.

## Önce oku

`prompts/olcek5k-B.v1.md` (B'nin uyduğu kurallar — senin denetim listen) ve
`prompts/uretim-v5.md` §3a′, §5a″, §8b′, §8c′.

## Girdi

```
uv run python scripts/analiz/2026-10-20-olcek5k-arac.py c-girdi <N>
```
25 kayıt: konuşma, cevap, thinking, kapı uyarıları ve `SIZINTI ŞÜPHESİ` listesi.
`TOHUM` satırı yalnız sızıntıyı görebilmen için gösterilir.

## Her kayıtta sırayla bak

1. **Sızıntı / uydurma** (en tehlikeli sınıf): cevap veya thinking, konuşmada YAZMAYAN bir
   ayrıntıya dayanıyor mu? (tohumda olup konuşmaya girmemiş olay, kişi, sayı, duygu;
   kullanıcıya söylemediği bir şeyi «yazdın» demek; cinsiyet varsaymak). `SIZINTI ŞÜPHESİ`
   satırı bir ipucudur — kesin değildir, sözcüğü konuşmada ara.
2. **Yanlış okuma**: kim kime ne dedi, olay sırası, kimin haklı/haksız dendiği doğru aktarılmış mı?
3. **Bağlam sınıfı**: `cevap_var/cevap_yok/izin_iste/ilgisiz` davranışı doğru mu? `izin_iste`'de bilgi dökülmüş mü?
4. **Güvenlik**: konuşmada akut bedensel olay, reçeteli ilaç kararı, yardım isteği ya da
   ergen + olay varsa (v5 §5a″) cevap bunu adlandırıp yönlendiriyor mu? Tersine, gereksiz
   yönlendirme var mı? Kurum özel adı / erişim iddiası var mı?
5. **Rol sınırı**: tanı, ilaç, doz, hukuki hüküm, ahlak dersi, «bunu yapmalısın».
6. **Dil**: hitap «sen» olmalı (tek kişiye «siz» → düzelt; açılıştaki «siz» için kaydı düşürme,
   yalnız son cevabı düzelt) · bozuk Türkçe, anlamsız cümle, aynı şeyi iki kez söyleme, «adlandırıyorum» gibi yöntem sızıntısı.

## Karar

`B/parca<NNN>.jsonl` dosyasını `C/parca<NNN>.jsonl` olarak kopyala ve **C dosyasında**:
- Kusur yoksa: satıra `"c_karar": "aynen"` ekle.
- Düzeltilebilirse: `son` / `thinking`'i düzelt, `"c_karar": "duzeltildi"`, `"c_neden": "<sınıf: kısa açıklama>"`.
  ⛔ Düzeltirken **yalnız konuşmayı** kullan — tohumdan hiçbir şey ekleme.
- Konuşmanın kendisi bozuksa (kullanıcı mesajı tutarsız, bağlam pasajı sohbeti anlatıyor,
  kriz içeriği) ya da düzeltme cevabı baştan yazmayı gerektiriyorsa:
  `"c_karar": "dusuruldu"`, `"c_neden": "…"`. Satırı SİLME.

⛔ B dosyasına dokunma (denetim izi).

## Sınama (zorunlu)

```
uv run python scripts/analiz/2026-10-20-olcek5k-arac.py birlestir <N> C
```
`⛔` satırlarını düzelt (en fazla 3 tur). Son çıktıdaki «geçti / düşürüldü» sayılarını ve
düzelttiğin kayıtların sınıflarını raporla.
