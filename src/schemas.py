"""Veri şemaları. Bkz. plan.md §12 (TrainRecord) ve §5/K26 (SeedMeta).

SeedMeta, normalize.py'nin normalize() çıktısıyla birebir uyumludur —
data/seeds.jsonl (Faz 1) bu şemayla doğrulanır.
"""
from __future__ import annotations
from typing import Literal

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str
    thinking: str | None = None  # yalnızca eğitilen son assistant mesajında


class TrainRecord(BaseModel):
    id: str                              # sha256(normalize(user_content + mode))
    slice: str                           # §6 dilimi
    scenario: str                        # §5, 16 tipten biri
    addiction_type: str                  # tütün | alkol | kumar | madde | yok
    motivation: str                      # ic | aile_baskisi | yasal_zorunluluk (K22)
    mi_process: str                      # engaging | focusing | evoking | planning
    talk_type: str                       # change_darn | change_cat | sustain | ambivalans | discord
    age_group: Literal["yetiskin", "ergen"]
    turn_type: Literal["single", "multi"]
    messages: list[Message]              # template UYGULANMADAN
    context: list[dict] | None = None    # RAG modunda dolu (K17)
    source_ids: list[str] = Field(default_factory=list)
    is_crisis: bool = False
    is_negative: bool = False            # kapsam dışı / yetersiz bağlam / sınır
    has_thinking: bool = False
    judge: dict | None = None
    replay: bool = False
    # ⚠️ `gen_meta` serbest sözlük ama BEYANLARI zorunlu (uretim-v4 §1):
    #   generator · generator_model · prompt_version · date · system_prompt_variant
    #   turn_ending · konusma_durumu · bicim · register · sinir_tipi
    #   tohum_havuzu  -> `seeds` | `seeds.v2`  (T88: iki havuz karışımı kayıttan
    #                    okunabilsin diye; hangi havuzun kullanılacağı AYRI karar)
    #   baglam_davranisi -> YALNIZ bağlamlı kayıtta: §7a'nın hangi sınıfı
    #                    uygulandı — cevap_var | cevap_yok | izin_iste | ilgisiz
    #                    (T96: §7a'nın yüzdesi vardı, alanı yoktu = T25 hatası)
    gen_meta: dict = Field(default_factory=dict)


class JudgeResult(BaseModel):
    """Eksen 1 judge çıktısı. Bkz. arastirma-notlari §H.5.

    İki rubrik sürümünü de doğrular; sürüme özgü alanlar opsiyoneldir, `prompt_version`
    hangisinin geçerli olduğunu söyler.
      v1 (`judge-eksen1.v1`): kisalik_dogallik + dil_butunlugu
      v2 (`judge-eksen1.v2`): anlasilirlik + dogallik + cevapsiz_soru + kanıt alanları
    v1'in dil_butunlugu boyutu ölçmediği için (50/50 tam puan, s=0.00) v2'de
    yeniden tanımlandı — reports/analiz/2026-09-14-uzman-puanlama-analizi.md §3b.
    """
    duygusal_tepki: int
    yorumlama: int
    kesif: int
    mi_uyumu: int
    tuzak_ihlali: list[str] = Field(default_factory=list)
    klinik_guvenlik_ihlali: bool
    rol_siniri_ihlali: bool
    grounding: int
    gerekce: str = ""
    judge_model: str = ""
    prompt_version: str = ""
    # v1'e özgü
    kisalik_dogallik: int | None = None
    dil_butunlugu: int | None = None
    # v2'ye özgü
    anlasilirlik: int | None = None
    dogallik: int | None = None
    cevapsiz_soru: bool | None = None
    en_belirsiz_cumle: str | None = None      # puandan ÖNCE çıkarılan kanıt
    cevapsiz_soru_metni: str | None = None
    # v3'e özgü — `anlasilirlik` artık LLM'den GELMEZ, aşağıdaki beş bayraktan
    # kod hesaplar (bkz. filter.py::anlasilirlik_hesapla). `anlasilirlik_holistik`
    # judge'ın kendi kanaati; hesaba girmez, yalnızca iki yöntem karşılaştırılsın diye.
    duz_turkce: str | None = None
    kurulmamis_mecaz: bool | None = None
    belirsiz_gonderge: bool | None = None
    ust_uste_yan_cumle: bool | None = None
    devrik_eksiltili: bool | None = None
    soyut_adlastirma: bool | None = None
    anlasilirlik_holistik: int | None = None
    # v4'e özgü — aynı desen dogallik ve mi_uyumu'na da uygulandı (K61).
    # Holistik puanlar artık sorulardan ÖNCE isteniyor: v3'te sonda isteniyordu ve
    # kontrol kirliydi (judge soruları görmüş oluyordu).
    dogallik_holistik: int | None = None
    mi_uyumu_holistik: int | None = None
    siz_kaymasi: bool | None = None
    klise_acilis: bool | None = None
    terapi_jargonu: bool | None = None
    bos_guvence: bool | None = None
    ovgu_tonu: bool | None = None
    yansitma_var: bool | None = None
    karmasik_yansitma: bool | None = None
    takdir_var: bool | None = None
    ozet_var: bool | None = None
    ozerklik_vurgusu: bool | None = None
    tuzak_uzman: bool | None = None
    tuzak_etiketleme: bool | None = None
    tuzak_soru_cevap: bool | None = None
    tuzak_erken_odak: bool | None = None
    tuzak_suclama: bool | None = None
    tuzak_erken_tavsiye: bool | None = None

    # --- judge-eksen1.v5 Bölüm F: zorunlu çıkarım (K94) ---
    # v4 bu altı boyutta 48 cevapta hiç varyans üretmedi; soyut soru judge'ı
    # bakmaya zorlamıyor, varsayılana oturtuyordu. v5 önce cevaptan parça
    # çıkartıyor, sonra yalnızca o parça hakkında karar soruyor.
    en_somut_ayrinti: str | None = None
    ayrinti_konusmada_var: bool | None = None
    ayrinti_hipotez_olarak_isaretli: bool | None = None
    rol_sinirina_en_yakin: str | None = None
    rol_alani: str | None = None
    rol_reddediyor: bool | None = None
    guvenlige_en_yakin: str | None = None
    guvenlik_tipi: str | None = None
    kisiye_dair_en_genel: str | None = None
    genelleme_kategori_mi: bool | None = None
    etiket_kullanicinin: bool | None = None
    sorumluluga_en_yakin: str | None = None
    kusur_kullanicida_ima: bool | None = None
    utanc_buyutuyor: bool | None = None
    kullanicinin_kendi_sucu: bool | None = None
    en_teselli_edici: str | None = None
    teselli_dayanakli: bool | None = None          # v5; v6'da ikiye bölündü
    teselli_kullanicinin_sozunden: bool | None = None  # v6
    teselli_kalip: bool | None = None                  # v6

    # --- judge-eksen1.v7: ikinci adım da kanıta bağlandı ---
    # v6'da judge bir cümleye ihlal diyebiliyor ama ihlali KURAN ögeyi yazmak
    # zorunda değildi; rol sınırında 5 sistematik yanlış pozitif buradan çıktı
    # (reports/analiz/2026-09-15-v7-gerekce.md §D). Üçü alanın aşırı atanması,
    # ikisi RAG aktarımının tavsiye sanılmasıydı.
    # ⚠️ Alanlar OPSİYONEL kalmalı: v6 kayıtlarında yoklar ve türetme onları
    # yalnızca VARSA uyguluyor — eski koşuların sayıları geriye dönük değişmesin.
    rol_iddiasi: str | None = None            # alana ait somut iddia; yoksa YOK
    rol_bilgi_baglamdan: bool | None = None   # bilgi verilen bağlam belgesinden mi
    rol_baglam_alintisi: str | None = None    # o belgeden birebir alıntı; yoksa YOK
    teselli_ozgu_oge: str | None = None       # cümleyi BU konuşmaya bağlayan öge

    # --- judge-eksen1.v8: dışlama da bir karardır, alanı vardır ---
    # v7 ilk kez Eksen 2'de koştu ve iki sistematik kusur çıktı; ikisi de DOĞRU
    # davranışı cezalandırıyordu (reports/analiz/2026-09-15-eksen2-judge-ayiklama.md).
    # ⚠️ Hepsi OPSİYONEL: v5-v7 kayıtlarında yoklar ve türetme onları yalnızca VARSA
    # uyguluyor — eski koşuların sayıları geriye dönük değişmesin (v7 ile aynı kural).
    rol_risk_olasilik_olarak: bool | None = None  # risk olasılık olarak mı söylendi
    rol_kaynak_turu: str | None = None            # kararın devredildiği kaynak TÜRÜ
    teselli_islevi: str | None = None             # rahatlatma|bilgi|soru|yonlendirme|
    #                                               asistan_kendine_dair
    teselli_kullanici_alintisi: str | None = None  # v8: ikili değil ALINTI
    kurum_yordam_en_yakin: str | None = None      # F7 — K18/K110
    kurum_adi: str | None = None                  # kurum ÖZEL adı; tür adıysa YOK
    kurum_adi_kullanicidan: bool | None = None    # adı kullanıcı mı andı (K110 muafiyeti)
    yordam_iddiasi: str | None = None             # ücret/süre/sıra/yetki iddiası
    yordam_baglamdan: bool | None = None          # bağlam belgesinden mi
    yordam_baglam_alintisi: str | None = None     # o belgeden birebir alıntı
    kurum_yordam_ihlali: bool | None = None       # TÜRETİLİR (filter.f_bolumu_turet)

    # --- judge-eksen1.v9: kanıt KAYNAĞA bağlanır; muafiyet de bir iddiadır ---
    # v8 koşusunun 803 alıntısı kaynak metne karşı denetlendi (reports/analiz/
    # 2026-09-15-v9-kanit-denetimi.md): judge alıntı UYDURMUYOR (0/803), ama ihlali
    # düşüren 11 koşulun 6'sı hiçbir dizgeye dayanmıyordu ve kalan 5'inde de kod
    # yalnızca "alan dolu mu" diye bakıyordu. `E-genis`/`sk-020` bu boşluktan geçti:
    # `teselli_ozgu_oge` doluydu, içeriği konuşmada HİÇ GEÇMİYORDU.
    # ⚠️ v8'in üç F6 alanı (`teselli_ozgu_oge` · `teselli_kalip` ·
    # `teselli_kullanici_alintisi`) ve `kurum_adi_kullanicidan` v9'da SORULMUYOR ama
    # şemadan SİLİNMEZ — eski kayıtlar okunabilmeli (Kural 7).
    teselli_dayanak_alintisi: str | None = None   # konuşmadan birebir parça; yoksa YOK
    teselli_dayanak_dogrulandi: bool | None = None  # TÜRETİLİR — parça konuşmada bulundu mu
    # TÜRETİLİR — doğrulama kaynakla mı koştu. ⚠️ Kaynaksız çağrı v9 kapısını SESSİZCE
    # kapatır; bu alan olmadan bir sayının doğrulanmış mı ölçüldüğü rapordan görülemez.
    alinti_dogrulama: str | None = None           # "yapildi" | "kaynaksiz"
    # TÜRETİLİR — kaynağında bulunamayan alıntı alanlarının adları. Hüküm DEĞİŞTİRMEZ
    # (suçlama yönünde ölçüm 0/803 çıktı); kayıt, sonraki sürümlerin ölçebilmesi için.
    alinti_dogrulanmadi: list[str] | None = None


class SeedMeta(BaseModel):
    """Faz 1 — data/seeds.jsonl. Kaynak: src/normalize.py normalize()."""
    bagimlilik_turu: str
    bagimlilik_alt_turu: str | None = None
    senaryo: str
    stres_tipi: str | None = None
    profil: str
    yas_grubu: str | None = None
    evre: str | None = None
    motivasyon_evresi: str | None = None
    motivasyon: str | None = None
    risk_seviyesi: str | None = None
    siddet_seviyesi: str | None = None
    egitim: str
    kullanim_suresi: str
    onceki_tedavi: str
    cinsiyet: str
    notlar: dict = Field(default_factory=dict)
