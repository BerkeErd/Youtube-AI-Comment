# YouTube Yorum Botu

Bu proje, YouTube videolarına otomatik olarak yorumlar yapan ve var olan yorumlara cevap veren gelişmiş bir bottur. Bot, Gemini API'yi kullanarak yapay zeka destekli yanıtlar üretir ve YouTube Data API aracılığıyla bu yanıtları yayınlar. Özellikle dikkat çeken yönü, çeşitli karakterlerde ve tarzlarda yorum üretmek için kullanılan yaratıcı prompt mühendisliğidir.

## Özellikler

- Son 3 ay içinde yayınlanan popüler YouTube videolarını bulma
- Seçilen videolara yeni yorumlar yapma
- Var olan yorumlara cevap verme
- Gemini API ile çeşitli karakterlerde ve tarzlarda yorum üretme
- Google Colab üzerinde çalışma imkanı
- Prompt mühendisliği ile çeşitli yorum tarzları

## Yorum Tarzları

Bu bot, çeşitli yorum tarzları oluşturmak için gelişmiş prompt mühendisliği tekniklerini kullanır. İşte bazı örnek prompt seçenekleri:

1. **Ciddi Yanlış Bilgi**: Yanlış bilgiler içeren, kendinden emin bir tarzda yazılmış yorumlar.
2. **Aşırı Heyecanlı Fan**: Abartılı ve heyecanlı bir tonda yazılmış yorumlar.
3. **Yanlış Anlayan Aptal**: Konuyu tamamen yanlış anlayan, yazım hataları içeren yorumlar.
4. **Komplo Teorisyeni**: Her şeyin arkasında gizli bir plan olduğunu düşünen yorumlar.
5. **Gizlice Söyle**: İma ve benzetmelerle mesajını gizlice ileten yorumlar.
6. **Anime Karakteri**: Anime dünyasından gelen, Japonca terimler içeren yorumlar.
7. **Şüpheci Dedektif**: Olayların iç yüzünü çözmeye çalışan, sorgulayıcı yorumlar.
8. **Aşırı Milliyetçi Türk**: Milliyetçi söylemler ve Türk bayrakları içeren yorumlar.
9. **Orta Çağ Şövalyesi**: Eski Türkçe kelimeler kullanan, destansı tarzda yorumlar.
10. **Gelecekten Gelen Birisi**: İleri bir tarihten gelmiş gibi yazılan, gelecek hakkında bilgiler içeren yorumlar.

... ve daha fazlası!

Örnek bir prompt:

```python
prompt = "'{video_title}' başlıklı video için bu yoruma, sanki bir anime karakteriymişsin ve burası bir anime dünyasıymış gibi cevap ver. Konuşmalarında Japonca kelimeler kullan ama romaji ile yaz bunları. Ayrıca bazı popüler animelere gönderme de yapabilirsin. (maksimum 200 karakter): {comment}"
```

Bu çeşitlilik, botun ürettiği yorumları daha ilginç ve eğlenceli hale getirir, aynı zamanda gerçek kullanıcı yorumlarına benzer bir çeşitlilik sağlar.

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

5. Notebook'u çalıştırın ve konsol çıktılarını takip edin.## Kurulum

1. Bu repository'yi klonlayın:
   ```
   git clone https://github.com/kullaniciadi/youtube-yorum-botu.git
   ```

2. Proje dizinine gidin:
   ```
   cd youtube-yorum-botu
   ```

3. (Opsiyonel) Bir sanal ortam oluşturun ve etkinleştirin:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux veya macOS
   # veya
   venv\Scripts\activate  # Windows
   ```

4. Gerekli kütüphaneleri yükleyin:
   ```
   pip install -r requirements.txt
   ```

5. Google Cloud Console'da bir proje oluşturun ve YouTube Data API'yi etkinleştirin.

6. OAuth 2.0 istemci kimlik bilgilerini indirin ve `client_secret.json` olarak kaydedin.

7. Gemini API anahtarınızı alın.

8. `bot.py` dosyasında `GEMINI_API_KEY` değişkenine API anahtarınızı girin.

## Google Colab Kullanımı

1. Google Colab'de yeni bir notebook oluşturun.

2. Bu repository'deki `bot.py` ve `ui.py` dosyalarının içeriğini Colab notebook'una kopyalayın.

3. Gerekli kütüphaneleri yüklemek için notebook'un başına şu komutu ekleyin:
   ```python
   !pip install -r requirements.txt
   ```

4. `client_secret.json` dosyasını Colab ortamına yükleyin.

5. Notebook'u çalıştırın ve oluşturulan kullanıcı arayüzünü kullanarak bot'u yönetin.

6. İstendiğinde yetkilendirme URL'sini açın ve kodu girin.

7. Bot'un talimatlarını izleyerek yorumları yönetin ve istediğiniz prompt tarzını seçin.

## Dikkat Edilmesi Gerekenler

- Bu bot, YouTube'un hizmet şartlarına aykırı olabilecek şekilde kullanılmamalıdır.
- Aşırı kullanım, hesabınızın kısıtlanmasına neden olabilir.
- Yapay zeka tarafından üretilen içerikleri dikkatle kontrol edin.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## Katkıda Bulunma

Katkılarınızı memnuniyetle karşılıyoruz! Yeni prompt fikirleri veya bot geliştirmeleri için lütfen bir pull request açın veya bir issue oluşturun.

---

**Not:** Bu bot eğitim ve deneysel amaçlar için tasarlanmıştır. Gerçek YouTube etkileşimlerinde dikkatli ve sorumlu kullanım önemlidir.
