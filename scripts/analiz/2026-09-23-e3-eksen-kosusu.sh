#!/bin/bash
# ⛔⛔ SÜPERSEDE (2026-09-23, EK-1 · K273): bu betik yalnız e3'ün beş eski
#   eksenini koşar — yeni baş ölçü B1'i (örtüşmez set) ve d1'in eksik
#   tohumlarını KOŞMAZ. Yerine:
#     uv run python scripts/analiz/2026-09-23-onkayit-ek1-olcum.py
#   Bu dosya T273'te anıldığı için silinmedi.
# `e3-celiskili-k8qo-v022` kolunun eksen ölçümü — KALDIĞI YERDEN DEVAM EDER.
#
# ⛔⛔ Ölçüm 2026-09-23'te 5/40'ta KULLANICI KARARIYLA durduruldu (K272,
#   T273). Bu betik tamamlanmış (tohum, eksen) çiftlerini ATLAR: bir çiftin
#   `reports/analiz/eksen-kosu/*-e3-v022-t{T}-{eksen}/sonuclar.jsonl` dosyası
#   eksen setinin öge sayısı kadar satır taşıyorsa bitmiş sayılır. Yarım
#   kalmış dizin varsa ATLANMAZ, yeniden koşulur (eski dizin silinmez —
#   Kural 7; karşılaştırma betiği en son dizini okur).
#
# ⛔ Ön kayıt: configs/deney/2026-09-22-v0022-celiskili-on-kayit.json
#   (commit 65a50c3). Bitince okunacak sıra oradadır; baş sonuç
#   `context_fidelity`'nin BULAŞMAMIŞ 15 ögesidir, `celiskili` alt puanı
#   DEĞİLDİR (bulaşma: reports/analiz/2026-09-22-celiskili-eval-bulasma.md).
#
# Kullanım:  bash scripts/analiz/2026-09-23-e3-eksen-kosusu.sh
#            KURU=1 bash … ⇒ hiçbir şey koşmaz, yalnız ne koşacağını basar
# Süre:      tohum başına ~12,5 dk (ölçüldü: t7, 06:45:20 → 06:57:50)
set -u
cd "$(dirname "$0")/../.."

EKSENLER="safety_crisis:safety forgetting_smoke:forget context_fidelity:context_fidelity sycophancy:sycophancy context_fidelity.real:cfreal"

bitti_mi() {   # $1 tohum, $2 kısa ad, $3 set yolu
  local n d
  n=$(grep -c . "$3")
  for d in reports/analiz/eksen-kosu/*-e3-v022-t$1-$2; do
    [ -f "$d/sonuclar.jsonl" ] || continue
    [ "$(grep -c . "$d/sonuclar.jsonl")" -eq "$n" ] && return 0
  done
  return 1
}

toplam=0; atlanan=0
for t in 7 13 23 31 37 41 43 47; do
  A=$(ls -d runs/*e3-celiskili-k8qo-v022-t${t}/adapters 2>/dev/null | head -1)
  if [ -z "$A" ]; then echo "⛔ adapter yok: t${t}"; exit 1; fi
  for pair in $EKSENLER; do
    s="${pair%%:*}"; k="${pair##*:}"; set_yolu="evals/${s}.jsonl"
    toplam=$((toplam+1))
    if bitti_mi "$t" "$k" "$set_yolu"; then
      atlanan=$((atlanan+1)); echo "   atlandı (bitmiş): t${t} ${s}"; continue
    fi
    echo "── t${t} ${s} $(date +%H:%M:%S)"
    [ "${KURU:-0}" = "1" ] && continue
    uv run python src/eksen_eval.py "$set_yolu" \
      --adapter "$A" --etiket "e3-v022-t${t}-${k}" 2>&1 | tail -2
  done
done
echo "EKSEN KOŞUSU BİTTİ $(date +%H:%M:%S) · $toplam çiftin $atlanan'i önceden bitmişti"
