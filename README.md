# YouTube Yorum Botu

Bu proje, YouTube videolarına otomatik olarak yorumlar yapan ve var olan yorumlara cevap veren bir bottur. Bot, Gemini API'yi kullanarak yapay zeka destekli yanıtlar üretir ve YouTube Data API aracılığıyla bu yanıtları yayınlar.

## Özellikler

- Son 3 ay içinde yayınlanan popüler YouTube videolarını bulma
- Seçilen videolara yeni yorumlar yapma
- Var olan yorumlara cevap verme
- Gemini API ile çeşitli karakterlerde ve tarzlarda yorum üretme
- Google Colab üzerinde çalışma imkanı

## Gereksinimler

- Python 3.7+
- Google hesabı (YouTube Data API ve Gemini API erişimi için)
- Gerekli Python kütüphaneleri (requirements.txt dosyasında listelenmiştir)

## Kurulum

1. Bu repository'yi klonlayın:
   ```
   git clone https://github.com/kullaniciadi/youtube-yorum-botu.git
   ```

2. Gerekli kütüphaneleri yükleyin:
   ```
   pip install -r requirements.txt
   ```

3. Google Cloud Console'da bir proje oluşturun ve YouTube Data API'yi etkinleştirin.

4. OAuth 2.0 istemci kimlik bilgilerini indirin ve `client_secret.json` olarak kaydedin.

5. Gemini API anahtarınızı alın.

6. `bot.py` dosyasında `GEMINI_API_KEY` değişkenine API anahtarınızı girin.

## Kullanım

1. Google Colab'de yeni bir notebook oluşturun.

2. Bu repository'deki `bot.py` dosyasının içeriğini Colab notebook'una kopyalayın.

3. Gerekli kütüphaneleri yüklemek için notebook'un başına şu komutu ekleyin:
   ```python
   !pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client google-generativeai
   ```

4. `client_secret.json` dosyasını Colab ortamına yükleyin.

5. Notebook'u çalıştırın ve konsol çıktılarını takip edin.

6. İstendiğinde yetkilendirme URL'sini açın ve kodu girin.

7. Bot'un talimatlarını izleyerek yorumları yönetin.

## Dikkat Edilmesi Gerekenler

- Bu bot, YouTube'un hizmet şartlarına aykırı olabilecek şekilde kullanılmamalıdır.
- Aşırı kullanım, hesabınızın kısıtlanmasına neden olabilir.
- Yapay zeka tarafından üretilen içerikleri dikkatle kontrol edin.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## Katkıda Bulunma

Katkılarınızı memnuniyetle karşılıyoruz! Lütfen bir pull request açın veya bir issue oluşturun.

---

**Not:** Bu bot eğitim ve deneysel amaçlar için tasarlanmıştır. Gerçek YouTube etkileşimlerinde dikkatli ve sorumlu kullanım önemlidir.
