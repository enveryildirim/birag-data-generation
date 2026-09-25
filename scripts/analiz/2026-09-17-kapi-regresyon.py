"""Bağlaçlı tür-adlandırma muafiyetinin regresyon sınaması.

⛔ İlk «regresyon» koşusu GEÇERSİZDİ: sınamak için kullandığım dosyada kusur
zaten düzeltilmişti, yani kapı sıfır bulguyu doğru olduğu için değil, kusur
orada olmadığı için verdi. ➡️ *Bir regresyon testi, testin ARADIĞI şeyin test
verisinde BULUNDUĞUNU önce kanıtlamalı.*
"""
import json, sys, tempfile
from pathlib import Path
KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "scripts/analiz"))
import importlib.util as iu
sp = iu.spec_from_file_location("kapi", KOK / "scripts/analiz/2026-09-17-zaman-kaynak-kapisi.py")
K = iu.module_from_spec(sp); sp.loader.exec_module(K)

ORNEK = [
 # (cevap, kullanıcı turu, BEKLENEN: işaretlenmeli mi, neden)
 ('Bu, ilacı yazan hekimin bilmesi gereken bir şey.', 'Doktor verdi diye alıyorum.',
  True,  'GERÇEK ATIF — belirli tamlayan, rol sözcüğü yok, bağlaç yok'),
 ('Böyle bir değerlendirmeyi yapmak hekimin ya da ruh sağlığı alanında çalışan bir uzmanın işi.',
  'bağımlı mıyım ben gerçekten ya',
  False, 'BAĞLAÇLI TÜR ADLANDIRMA — rol sözcüğü bağlacın öbür ucunda'),
 ('Bu değerlendirme hekimin işi.', 'bağımlı mıyım',
  False, 'BİTİŞİK TÜR ADLANDIRMA — eski muafiyet'),
 ('Bunu bir hekimin bilmesi gerekiyor.', 'ellerim titriyor',
  False, 'BELİRSİZ ARTİKEL MUAFİYETİ'),
 ('Eşinin sana söylediği şey orada duruyor.', 'bugün çok yoruldum',
  True,  'GERÇEK ATIF — konuşmada eş yok'),
]

hata = 0
for cevap, kul, bekle, neden in ORNEK:
    r = {"id": "x"*24, "gen_meta": {"parti_sira": 1},
         "messages": [{"role": "user", "content": kul},
                      {"role": "assistant", "content": cevap}]}
    yol = KOK / "data/candidates/_regresyon_gecici.jsonl"
    yol.write_text(json.dumps(r, ensure_ascii=False) + "\n", encoding="utf-8")
    yol = str(yol)
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        K.main(yol)
    ciktı = buf.getvalue()
    isaretli = "işaretli 1 kayıt" in ciktı
    ok = isaretli == bekle
    hata += 0 if ok else 1
    print(f"{'✅' if ok else '⛔'} bekle={bekle!s:<5} bulundu={isaretli!s:<5} — {neden}")
Path(KOK / "data/candidates/_regresyon_gecici.jsonl").unlink(missing_ok=True)
Path(KOK / "reports/analiz/2026-09-17-zaman-kaynak-_regresyon_gecici.json").unlink(missing_ok=True)
print(f"\n{'⭐ REGRESYON GEÇTİ' if not hata else f'⛔ {hata} SINAMA BAŞARISIZ'}")
sys.exit(1 if hata else 0)
