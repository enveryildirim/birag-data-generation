# uretim-v4 korpus hedef raporu · v4-parti2.jsonl
girdi sha256: 4154385d9d39d244 · kayıt: 60
betik: scripts/analiz/2026-09-15-v4-korpus-hedef-raporu.py

### bicim (§ hedefi)
değer                  adet      %  hedef   fark
kisa                     24   40.0   40.0   +0.0
orta                     21   35.0   35.0   +0.0
uzun                     15   25.0   25.0   +0.0

### register (§ hedefi)
değer                  adet      %  hedef   fark
bozuk                    15   25.0   25.0   +0.0
duzgun                   45   75.0   75.0   +0.0

### konusma_durumu (§ hedefi)
değer                  adet      %  hedef   fark
tetikleyici_an           21   35.0   35.0   +0.0
suregiden_durum          12   20.0   20.0   +0.0
iyi_giden_paylasim        9   15.0   15.0   +0.0
plan_yapma                9   15.0   15.0   +0.0
merak_sorusu              6   10.0   10.0   +0.0
aradan_donus              3    5.0    5.0   +0.0

### turn_ending (§ hedefi)
değer                  adet      %  hedef   fark
acik_uclu_soru           30   50.0   50.0   +0.0
takdir                    9   15.0   15.0   +0.0
ozet                      9   15.0   15.0   +0.0
yalnizca_yansitma         9   15.0   15.0   +0.0
durur                     3    5.0    5.0   +0.0

### mi_process (§ hedefi)
değer                  adet      %  hedef   fark
engaging                 24   40.0   40.0   +0.0
focusing                 12   20.0   20.0   +0.0
evoking                  15   25.0   25.0   +0.0
planning                  9   15.0   15.0   +0.0

### turn_type (§ hedefi)
değer                  adet      %  hedef   fark
multi                    24   40.0   40.0   +0.0
single                   36   60.0   60.0   +0.0

### beyan ↔ metin tutarsızlıkları
  yok ✅

### §8b · sinir_tipi beyanları
  yonlendirme_istegi         5  % 8.3  (hedef ~%6)
  rol_siniri_yonlendirme     7  %11.7  (hedef ~%8)
  yonlendirme_gereksiz       4  % 6.7  (hedef ~%5)
  sinir_cekme                4  % 6.7  (kota yok)
  yok                       40  %66.7  (kota yok)

### §8b düzeltme ölçütü — ÖLÇÜT 1/2 için ADAY listesi (karar elle okunur)

  [ 1] yonlendirme_istegi  terim=['hekim', 'danışmanlık', 'merkez']
       · Sigarayı bırakmak için iki tür yer var: hastanelerin sigara bırakma poliklinikleri, bir de bağımlılık alanında çalışan danışmanlık merkezleri.
       · Raporu yazan hekime hangisine gidilmesi gerektiğini sormak, buradan atılabilecek en yakın adım olabilir.

  [ 2] yonlendirme_istegi  terim=['hekim', 'doktor']
       · Bir yanda doktorun söylediği tıkanıklık var, bir yanda annen.
       · Bugün seni gören hekim bu işin zaten içinde.
       · Bunu bugünkü hekime sormak ilk adım olabilir.

  [ 3] yonlendirme_istegi  terim=['hekim', 'danışmanlık', 'merkez']
       · Tek başına yapmayanların gittiği yerler var: aile hekimi, bir de bağımlılık alanında danışmanlık veren merkezler.

  [ 4] yonlendirme_istegi  terim=['merkez']
       · Kampüsteki psikolojik danışma merkezini kendin buldun, randevuyu da kendin düşündün.

  [ 5] yonlendirme_istegi  terim=['danışmanlık', 'merkez', 'birim']
       · Kendi isteğinle gitmek istediğin yer içinse iki tür adres var: bağımlılık alanında çalışan danışmanlık merkezleri, bir de hastanelerin bağımlılık biri

  [ 6] rol_siniri_yonlendirme  terim=['hekim', 'doktor']
       · Bunu yazabilecek olan, seni ve ilacını bilen bir hekim.
       · Doktora gitmek istemiyorsun, bunu duydum; karar senin ve seni ikna etmeye çalışmayacağım.
       · İlacı yazan hekime tek bir soru sormak bile bu planı başlatabilir.
       · Seni hekime gitmekten alıkoyan ne?

  [ 7] rol_siniri_yonlendirme  terim=['hekim']
       · Bir ilacın günlük miktarını belirlemek hekimin işi; bende o bilgi yok ve uydurmayacağım.
       · Söyleyebilecek olan, ilacı yazan hekim.

  [ 8] rol_siniri_yonlendirme  terim=['hekim']
       · Bedende olan bir şeyi yorumlamak hekimin işi; buradan konuşursam bilmediğim bir şeyi biliyormuş gibi yaparım.
       · Bunu bilmesi gereken kişi, dozu azaltan hekim.

  [ 9] rol_siniri_yonlendirme  terim=['hekim']
       · Bu sorunun cevabını ben veremem; böyle bir kararı vermek hekimin işi, bende o karar yok.
       · Söyleyebilecek olan, ilacı yazan hekim ve bu soruyu ona olduğu gibi sormak bir yol.

  [10] rol_siniri_yonlendirme  terim=['uzman', 'hekim', 'danışmanlık', 'merkez', 'birim']
       · Böyle bir değerlendirmeyi yapmak hekimin ya da ruh sağlığı alanında çalışan bir uzmanın işi; bende o karar yok.
       · Bu iki cümleyi bir uzmana anlatmak istersen, bağımlılık alanında çalışan danışmanlık merkezleri ya da hastanelerin bağımlılık birimleri ilk durak olab

  [11] rol_siniri_yonlendirme  terim=['danışmanlık', 'merkez', 'avukat']
       · Sürecin hukuki tarafı için bir avukat var, dün geceki içki tarafı için de bağımlılık alanında çalışan danışmanlık merkezleri.

  [12] rol_siniri_yonlendirme  terim=['hekim']
       · İlacın kullanımını belirlemek hekimin işi; o bilgi bende yok ve tahmin yürütmeyeceğim.
       · Söyleyebileceğim tek şey, cevabın kimde olduğu: reçeteyi yazabilecek bir hekimde.

  [13] yonlendirme_gereksiz  terim=—
       · (yönlendirme/sınır cümlesi yok)

  [14] yonlendirme_gereksiz  terim=—
       · (yönlendirme/sınır cümlesi yok)

  [15] yonlendirme_gereksiz  terim=—
       · (yönlendirme/sınır cümlesi yok)

  [16] yonlendirme_gereksiz  terim=—
       · (yönlendirme/sınır cümlesi yok)

  [17] sinir_cekme  terim=—
       · (yönlendirme/sınır cümlesi yok)

  [18] sinir_cekme  terim=—
       · (yönlendirme/sınır cümlesi yok)

  [19] sinir_cekme  terim=—
       · (yönlendirme/sınır cümlesi yok)

  [20] sinir_cekme  terim=—
       · (yönlendirme/sınır cümlesi yok)

### §8b düzeltme ölçütü 1 ve 2 — ELLE KARAR
  ⛔ elle karar tablosu kayıtlarla örtüşmüyor — tabloda yok: [8, 9, 10, 11, 12, 13, 14, 15, 16] · kayıtta yok: []

### §8b düzeltme ölçütü 3 — rakam ve kurum özel adı (makine)
  ihlal yok ✅

### K31 · eval metniyle çakışma (üretim tarafı denetimi)
  çakışma yok ✅

### uzunluk
completion ortanca 44.0 kelime · thinking ortanca 85.0 kelime · thinking:completion (karakter) ortanca 1.91x, maks 3.02x (tavan 4x)
system promptu: {'canon': 46, 'paraphrase': 14}
özerklik vurgusu: 12/60
bağlam (RAG): 6/60 · is_negative: 9/60
bağımlılık türü: {'tutun': 22, 'alkol': 17, 'receteli_ilac': 7, 'kumar': 11, 'dijital': 3}
yaş: {'yetiskin': 55, 'ergen': 5} · motivasyon: {'ic': 56, 'yasal_zorunluluk': 3, 'aile_baskisi': 1}
senaryo: {'farkindalik': 14, 'ambivalans': 10, 'hedef_belirleme': 9, 'rol_siniri': 7, 'bilgilendirme': 3, 'inkar': 3, 'hukuki_kaygi': 2, 'durtu': 2, 'kutlama': 2, 'discord': 2, 'kayma_nuks': 2, 'nazikce_karsi_cikma': 1, 'motivasyon': 1, 'kayip_kovalama': 1, 'anlasilmama': 1}
