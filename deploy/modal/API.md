# BıRAG API

Bağımlılıkla mücadele eden kişilere destek olmak üzere ince ayar yapılmış **BıRAG** modelinin (Gemma 4 26B tabanlı) test API'si.
API **OpenAI uyumludur**: OpenAI SDK'sı veya OpenAI destekleyen herhangi bir kütüphane (LangChain, LlamaIndex, Vercel AI SDK…) ile çalışır.

> ⚠️ **Araştırma prototipidir, destek hizmeti değildir.** Kriz durumlarını güvenilir şekilde yönlendiremez ve bilgi uydurabilir. Gerçek kullanıcılara sunacaksanız kriz/acil durum yönlendirmesini uygulamanızda ayrıca sağlayın.

---

## Bağlantı bilgileri

| | |
|---|---|
| **Base URL** | `https://yildirim-developer34--birag-api-serve.modal.run/v1` |
| **Model** | `birag` |
| **Kimlik doğrulama** | `Authorization: Bearer <API_KEY>` (anahtar size ayrıca iletilir) |
| **Bağlam sınırı** | 16.384 token (girdi + çıktı) |

API anahtarını kodun içine yazmayın, ortam değişkeninde tutun:

```bash
export BIRAG_API_KEY="..."
```

---

## Hızlı başlangıç

### Python

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://yildirim-developer34--birag-api-serve.modal.run/v1",
    api_key=os.environ["BIRAG_API_KEY"],
    timeout=600,
)

resp = client.chat.completions.create(
    model="birag",
    messages=[{"role": "user", "content": "Sigarayı bırakmak istiyorum ama bir türlü başlayamıyorum."}],
)

print(resp.choices[0].message.content)
```

### JavaScript / TypeScript

```js
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://yildirim-developer34--birag-api-serve.modal.run/v1",
  apiKey: process.env.BIRAG_API_KEY,
  timeout: 600_000,
});

const resp = await client.chat.completions.create({
  model: "birag",
  messages: [{ role: "user", content: "Sigarayı bırakmak istiyorum ama bir türlü başlayamıyorum." }],
});

console.log(resp.choices[0].message.content);
```

### cURL

```bash
curl https://yildirim-developer34--birag-api-serve.modal.run/v1/chat/completions \
  -H "Authorization: Bearer $BIRAG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "birag",
    "messages": [{"role": "user", "content": "Merhaba"}]
  }'
```

---

## Parametreler

Standart OpenAI `chat.completions` parametreleri desteklenir. Yalnızca `model` ve `messages` zorunludur; diğerleri opsiyoneldir ve verilmezse varsayılan değer kullanılır.

| Parametre | Durum | Varsayılan | Açıklama |
|---|---|---|---|
| `model` | **Zorunlu** | — | Her zaman `"birag"` |
| `messages` | **Zorunlu** | — | Sohbet mesajları (`user` / `assistant`; `system` opsiyonel) |
| `max_tokens` | Opsiyonel | `8192` | Üretilecek en fazla token (düşünme dahil) |
| `temperature` | Opsiyonel | model varsayılanı | Daha tutarlı cevap için `0.3`–`0.7` |
| `stream` | Opsiyonel | `false` | `true` ile cevap parça parça gelir |
| `chat_template_kwargs.enable_thinking` | Opsiyonel | `true` | Düşünme modunu açar / kapatır |

---

## Ayrıntılar

### Sistem promptu (opsiyonel)
Sunucu, modelin eğitildiği **BıRAG sistem promptunu varsayılan olarak ekler**; yalnızca `user` / `assistant` mesajlarını göndermeniz yeterlidir.
İsterseniz kendi `system` mesajınızı gönderebilirsiniz; bu durumda sunucu sizinkini kullanır. Model en iyi sonucu varsayılan promptla verir.

### Sohbet geçmişi
API durumsuzdur (stateless). Çok turlu sohbette önceki mesajların tamamını her istekte gönderin:

```python
messages = [
    {"role": "user", "content": "Bu hafta üç gün içmedim."},
    {"role": "assistant", "content": "<önceki cevap>"},
    {"role": "user", "content": "Ama dün yine başladım."},
]
```

### Düşünme modu (opsiyonel, varsayılan: açık)
Model cevap vermeden önce düşünür. Düşünme metni cevaptan **ayrı** gelir ve son kullanıcıya genellikle **gösterilmemelidir**:

```python
msg = resp.choices[0].message
cevap   = msg.content                              # kullanıcıya gösterin
dusunme = getattr(msg, "reasoning_content", None)  # log / hata ayıklama için
```

Daha hızlı ama daha az özenli cevap için kapatabilirsiniz:

```python
client.chat.completions.create(..., extra_body={"chat_template_kwargs": {"enable_thinking": False}})
```

### `max_tokens` (opsiyonel, varsayılan: 8192)
Belirtilmezse sunucu **8192** kullanır. Kendiniz belirtecekseniz, düşünme de bu sınırdan harcadığı için **en az 2048** önerilir; daha düşük değerlerde cevap boş gelebilir.
Girdi ve çıktı birlikte **16.384 token** bağlam sınırını aşamaz; çok uzun sohbet geçmişlerinde eski mesajları kısaltın.

### Akış / streaming (opsiyonel)
Cevabı kelime kelime göstermek için:

```python
stream = client.chat.completions.create(model="birag", messages=messages, stream=True)
for chunk in stream:
    delta = chunk.choices[0].delta
    if delta.content:
        print(delta.content, end="", flush=True)
```

### İlk istek yavaş olabilir (soğuk başlangıç)
Sunucu kullanılmadığında kapanır. Uzun aradan sonraki ilk istek, model yüklenirken **1–3 dakika** sürebilir; sonrakiler hızlıdır.
İstemci zaman aşımını **en az 600 saniye** yapın ve kullanıcıya bir "yükleniyor" durumu gösterin. Uzun cevaplarda **streaming** kullanmanız önerilir: ilk kelimeler model hazır olur olmaz gelmeye başlar.

### Kapasite
Bu bir **test sunucusudur**: tek GPU üzerinde aynı anda bir istek işlenir, diğerleri sıraya girer. Yük testi veya toplu (batch) çağrı yapmayın.

---

## Hata kodları

| Kod | Anlamı | Ne yapmalı |
|---|---|---|
| `401` | API anahtarı eksik / hatalı | `Authorization: Bearer <API_KEY>` başlığını kontrol edin |
| `400` | Geçersiz istek veya bağlam sınırı aşıldı | İsteği kontrol edin / mesaj geçmişini kısaltın |
| `503` | Model yükleniyor | Birkaç saniye bekleyip tekrar deneyin |
| Zaman aşımı | Soğuk başlangıç veya çok uzun cevap | Zaman aşımını artırın (≥ 600 sn), streaming kullanın ve tekrar deneyin |

---

## Kullanım kuralları

- API anahtarını **paylaşmayın** ve istemci tarafı (tarayıcı / mobil uygulama) koduna gömmeyin; çağrıları kendi backend'iniz üzerinden yapın.
- Model tanı koymaz, ilaç/doz önermez ve profesyonel desteğin yerini tutmaz. Kullanıcıya bunu açıkça belirtin.
- Kişisel/hassas verileri test için göndermeyin.

Sorun veya geri bildirim için: proje sahibiyle iletişime geçin.
