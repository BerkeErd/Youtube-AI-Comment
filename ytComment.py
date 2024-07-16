# 1. Gerekli Kütüphanelerin Kurulumu
!pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client google-generativeai

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import google.generativeai as genai
import random
import os
import time

# OAuth 2.0 istemci kimlik bilgilerinizi içeren JSON dosyasının yolunu belirleyin
CLIENT_SECRETS_FILE = "client_secret.json"

# Google API erişim kapsamları
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# OAuth 2.0 kimlik doğrulama akışını başlatın
flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'  # Bu satırı ekledik
)

# Yetkilendirme URL'sini alın
auth_url, _ = flow.authorization_url(prompt='consent')

print(f"Lütfen bu URL'yi tarayıcınızda açın ve yetkilendirmeyi tamamlayın: {auth_url}")

# Kullanıcıdan yetkilendirme kodunu isteyin
auth_code = input("Yetkilendirme kodunu buraya yapıştırın: ")

# Yetkilendirme kodunu kullanarak kimlik bilgilerini alın
flow.fetch_token(code=auth_code)
credentials = flow.credentials

# Yetkili API istemcisini oluşturun
youtube = build('youtube', 'v3', credentials=credentials)

# Gemini API anahtarını ayarlayın
GEMINI_API_KEY = 'AIzaSyB4B7qLCOmef7_Npw_jD7O9Hf9y26OzrsY'
genai.configure(api_key=GEMINI_API_KEY)


# Botun çalıştırılması kısmı da aynı kalacak...

# ... (önceki kodlar aynı kalacak)

# 4. Video Yorumlarını Çekme Fonksiyonu
def get_video_comments(video_id):
    comments = []
    results = youtube.commentThreads().list(part='snippet', videoId=video_id, textFormat='plainText').execute()
    for item in results['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comment_id = item['snippet']['topLevelComment']['id']
        comments.append({'text': comment, 'id': comment_id})
    return comments

# 5. Gemini API ile Yorum Oluşturma Fonksiyonu
def generate_comment(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

# 6. Yoruma Cevap Yayınlama Fonksiyonu
def post_reply(comment_id, reply):
    request = youtube.comments().insert(
        part="snippet",
        body={
            "snippet": {
                "parentId": comment_id,
                "textOriginal": reply
            }
        }
    )
    response = request.execute()
    return response


# Prompt seçeneklerini güncelleyelim
prompt_options = [
    {"title": "Ciddi Yanlış Bilgi", "prompt": "Bu YouTube videosunun başlığı '{video_title}'. Şu yoruma yanlış bilgili bir açıklama getir, ama olmayan şeyler uydur, kelimeler bile uydur. Hatta bazı alakasız sayısal hesaplamalar da yapabilirsin ama kendinden çok emin yazacaksın. YouTube kullanan normal bir insan gibi yaz. Yazım kurallarına tamamen uyma (maksimum 200 karakter): {comment}"},
    {"title": "Aşırı Heyecanlı Fan", "prompt": "Video başlığı şu olan: '{video_title}'. Bu yoruma çok heyecanlı ve abartılı bir şekilde cevap ver, sanki hayatında duyduğun en ilginç şeymiş gibi. O kadar heyecanlı yaz ki harfleri fazla falan bas ve yorumun sonuna gelmeden ortada bir yerde kesilsin  (maksimum 200 karakter): {comment}"},
    {"title": "Yanlış Anlayan Aptal", "prompt": "'{video_title}' başlıklı video hakkındaki. Yorumdaki yazıyı tamamen aptal gibi yorumla ve ona göre cevap yaz, yazım yanlışları yap ve tüm mesajı küçük harflerle yaz. (maksimum 200 karakter): {comment}"},
    {"title": "Komplo Teorisyeni", "prompt": "Video başlığı şu olan '{video_title}'. Bu yoruma bir komplo teorisyeni gibi cevap ver. Her şeyin arkasında gizli bir plan olduğunu düşünen biri gibi yanıtla ama çok da ciddi olma. YouTube kullanan bir insan gibi cevap ver, yazım yanlışları yapabilirsin (maksimum 200 karakter): {comment}"},
    {"title": "Gizlice Söyle", "prompt": "Video başlığı şu olan '{video_title}'. Bu yoruma, sanki herkes senin ne dediğini dinliyormuş gibi düşünüp çaktırmadan ne demek istediğini imalar ve benzetmelerde bulunarak kimse anlamadan anlatmaya çalış (maksimum 200 karakter): {comment}"},
    {"title": "Anime Karakteri", "prompt": "'{video_title}' başlıklı video için bu yoruma, sanki bir anime karakteriymişsin ve burası bir anime dünyasıymış gibi cevap ver. Konuşmalarında Japonca kelimeler kullan ama romaji ile yaz bunları. Ayrıca bazı popüler animelere gönderme de yapabilirsin. (maksimum 200 karakter): {comment}"},
    {"title": "Şüpheci Dedektif", "prompt": "Video başlığı şu olan '{video_title}'. Bu yoruma, sanki bir dedektifmişsin ve olayın iç yüzünü çözmeye çalışıyormuşsun gibi cevap ver. Yorumun birçok soru içersin ve şüpheler uyandırsın. Çelişkiler bulmaya çalış ve bunları yüzlerine çarp mesajında (maksimum 200 karakter): {comment}"},
    {"title": "Aşırı Milliyetçi Türk", "prompt": "'{video_title}' başlıklı video için bu yoruma, aşırı milliyetçi bir Türk gibi cevap ver. Bol bol Türk bayrakları koy ve çok ciddi ol. Asla virgül kullanma (maksimum 200 karakter): {comment}"},
    {"title": "Orta Çağ Şövalyesi", "prompt": "'{video_title}' başlıklı videoya yapılan bu yoruma, sanki Orta Çağ'dan gelmiş bir şövalyesin ve her şeyi çok eski bir dille ve destansı bir şekilde cevaplıyormuşsun gibi yaz. Eski Türkçe kelimeler kullan (maksimum 200 karakter): {comment}"},
    {"title": "Gelecekten Gelen Birisi", "prompt": "'{video_title}' başlıklı videoya yapılan bu yoruma, sanki çok ileri bir yıldan geliyormuşsun gibi cevap ver. Anlaşılmayan ileri yıllara ait detaylarda bulun ve hatta daha olmamış olan olayları olmuş gibi söyle. İnsanlara ileride olacaklar hakkında bilgiler ver. (maksimum 200 karakter): {comment}"},
    {"title": "Yazım Kuralları Bilmeyen", "prompt": "'{video_title}' başlıklı videoya yapılan bu yoruma, yazım kurallarını hiç bilmeyen birisiymişsin gibi cevap ver. Noktalama işaretlerini yanlış kullan, kelimeleri yanlış yaz ve cümleleri garip bir şekilde kur (maksimum 200 karakter): {comment}"},
    {"title": "Aşırı Şüpheci", "prompt": "'{video_title}' başlıklı videoya yapılan bu yoruma, sanki her şeyden aşırı derecede şüpheleniyorsun ve sürekli komplolar arıyormuşsun gibi cevap ver. Herkese güvenmeyen bir ton kullan (maksimum 200 karakter): {comment}"},
    {"title": "Ukala", "prompt": "'{video_title}' başlıklı videoya yapılan bu yoruma, sanki en zeki insanıymışsın ve her şeyi çok biliyormuşsun gibi cevap ver. Çok ukala ol ve çok bilinmeyen terimler ve kelimeler kullan. Ayrıca noktalama işaretlerinden sadece noktayı kullan ve baş harf dışında küçük harf yaz (maksimum 200 karakter): {comment}"},
    {"title": "League of Legends oyuncusu", "prompt": "'{video_title}' başlıklı videoya yapılan bu yoruma, bronz bir LoL oyuncusunun takım arkadaşına yazışı gibi cevap ver. Bütün mesajı küçük harfler ile yaz ve noktalama işaretleri kullanma (maksimum 200 karakter): {comment}"},
    {"title": "Fıkracı", "prompt": "'{video_title}' başlıklı videoya yapılan bu yoruma, yorumdan yola çıkarak bir fıkra uydur ve o fıkrayı yaz. Fıkra oldukça yaratıcı ve saçma olsun. Hatta sonunu öyle saçma bağla ki absürdlüğü bizi güldürsün. (maksimum 200 karakter): {comment}"},
    {"title": "Gereksiz Detaycı", "prompt": "'{video_title}' başlıklı bu videoya yapılmış olan bu yoruma aşırı gereksiz detaylar ekleyerek cevap yaz. Mesela 'iPhone 15 Pro Max 512 Gb siyah akıllı telefonumla videoyu izlerken bu yorumu gördüm' gibi ama direkt aynısını yazma, bunun gibi başka şeyler üret (maksimum 200 karakter): {comment}"},
    {"title": "Kendini Beğenmiş", "prompt": "'{video_title}' başlıklı bu videoya yapılmış olan bu yoruma cevap yazarken sürekli kendini öv ve gülücük gibi ifadeler kullan, bulduğun her fırsatta kendini öv. (maksimum 200 karakter): {comment}"},
    {"title": "AI Müzik Kanalı Reklamı", "prompt": "Video başlığı şu olan '{video_title}'. Bu yoruma AI Müzik kanalının reklamını yapar gibi cevap yaz, ama gerçekten bir insan gibi görünsün. Yazarken kesme işaretlerini, büyük harfleri ve küçük harfleri hatalı kullan çok az emoji kullan ve yazım kurallarını pek umursama. Özellikle 'Yapay Zeka İş Başında' diye bir şarkı olduğunu söyle, bu şarkıda yapay zekanın işleri aldığını ve bunun ilginç ve komik olduğunu belirt ama bunları bir bronz küme lol oyuncusuymuşsun gibi yaz lol chatte yazan lol oyuncuları gibi yaz(maksimum 200 karakter): {comment}"}
    ]







def get_recent_videos():
    try:
        # Son üç ayın tarihini hesapla
        three_months_ago = (datetime.utcnow() - timedelta(days=90)).isoformat() + 'Z'

        # Popüler arama terimleri
        search_terms = ["Yapay zeka müziği", "Müzik", "Yapay zekalı müzik", "Suno ile müzik yapmak", "Udio ile müzik", "Yapay zeka müzik yapıyor", "AI Müzik türkçe", "Türkçe yapay zeka müziği", "Yapay zekaya yaptırdım", "Yapay zeka yapıyor", "Lol TR", "çekiliş"]

        # Rastgele bir arama terimi seç
        search_query = random.choice(search_terms)

        # Son üç ay içinde yayınlanan videoları ara
        search_response = youtube.search().list(
            q=search_query,
            type='video',
            part='id,snippet',
            maxResults=50,
            publishedAfter=three_months_ago,
            order='date'
        ).execute()

        videos = []
        for item in search_response.get('items', []):
            video_id = item['id']['videoId']
            # Videonun yorum durumunu kontrol et
            video_response = youtube.videos().list(
                part='statistics',
                id=video_id
            ).execute()
            if video_response['items'][0]['statistics'].get('commentCount') is not None:
                videos.append(video_id)

        if not videos:
            return None

        return random.choice(videos)

    except Exception as e:
        print(f"Video arama hatası: {e}")
        return None

def get_recent_comments(video_id):
    try:
        comments = []

        results = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=100
        ).execute()

        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'text': comment['textDisplay'],
                'id': item['snippet']['topLevelComment']['id']
            })

        return comments

    except HttpError as e:
        if e.resp.status == 403 and 'commentsDisabled' in str(e):
            print(f"Bu video için yorumlar devre dışı bırakılmış: {video_id}")
        else:
            print(f"Yorum alma hatası: {e}")
        return []

def get_video_details(video_id):
    try:
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]['snippet']['title']
        else:
            return "Video başlığı bulunamadı"
    except Exception as e:
        print(f"Video detayları alınırken hata oluştu: {e}")
        return "Video başlığı alınamadı"

def post_comment(video_id, comment):
    try:
        youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": comment
                        }
                    }
                }
            }
        ).execute()
        print("Yorum başarıyla gönderildi.")
    except Exception as e:
        print(f"Yorum gönderirken hata oluştu: {e}")

def main():
    while True:
        video_id = get_recent_videos()
        if video_id:
            video_title = get_video_details(video_id)
            try:
                comments = get_recent_comments(video_id)
                comment_count = len(comments)

                print(f"\nSeçilen video ID: {video_id}")
                print(f"Video Başlığı: {video_title}")
                print(f"Yorum Sayısı: {comment_count}")

                action_choice = input("Ne yapmak istersiniz? (1: Yorum yanıtla, 2: Yeni yorum bırak, 3: Bu videoyu geç): ")

                if action_choice == '1':
                    if comments:
                        while comments:
                            random_comment = random.choice(comments)
                            print(f"\nSeçilen yorum: {random_comment['text']}")

                            print("\nPrompt seçenekleri:")
                            for i, prompt in enumerate(prompt_options, 1):
                                print(f"{i}. {prompt['title']}")
                            print("0. Bu yorumu geç")

                            prompt_choice = input("Hangi prompt'u kullanmak istersiniz? (0-15): ")

                            if prompt_choice == '0':
                                comments.remove(random_comment)
                                print("Yorum geçildi. Yeni bir yorum seçiliyor...")
                                continue

                            try:
                                prompt_choice = int(prompt_choice)
                                if 1 <= prompt_choice <= len(prompt_options):
                                    chosen_prompt = prompt_options[prompt_choice - 1]['prompt'].format(
                                        comment=random_comment['text'],
                                        video_title=video_title
                                    )
                                    response_comment = generate_comment(chosen_prompt)

                                    print(f"\nOluşturulan yanıt: {response_comment}")

                                    confirmation = input("Bu yanıtı göndermek istiyor musunuz? (E/H): ")
                                    if confirmation.lower() == 'e':
                                        post_reply(random_comment['id'], response_comment)
                                        print("Yanıt başarıyla gönderildi.")
                                    else:
                                        print("Yanıt gönderilmedi.")
                                    break
                                else:
                                    print("Geçersiz seçim. Lütfen 0 ile 15 arasında bir sayı girin.")
                            except ValueError:
                                print("Geçersiz giriş. Lütfen bir sayı girin.")

                        if not comments:
                            print("Bu video için tüm yorumlar geçildi veya uygun yorum bulunamadı.")
                    else:
                        print("Seçilen video için uygun yorum bulunamadı.")

                elif action_choice == '2':
                    print("\nYeni yorum için prompt seçenekleri:")
                    for i, prompt in enumerate(prompt_options, 1):
                        print(f"{i}. {prompt['title']}")

                    prompt_choice = input("Hangi prompt'u kullanmak istersiniz? (1-15): ")

                    try:
                        prompt_choice = int(prompt_choice)
                        if 1 <= prompt_choice <= len(prompt_options):
                            chosen_prompt = prompt_options[prompt_choice - 1]['prompt'].format(
                                comment="",
                                video_title=video_title
                            )
                            new_comment = generate_comment(chosen_prompt)

                            print(f"\nOluşturulan yorum: {new_comment}")

                            confirmation = input("Bu yorumu göndermek istiyor musunuz? (E/H): ")
                            if confirmation.lower() == 'e':
                                post_comment(video_id, new_comment)
                                print("Yorum başarıyla gönderildi.")
                            else:
                                print("Yorum gönderilmedi.")
                        else:
                            print("Geçersiz seçim. Lütfen 1 ile 15 arasında bir sayı girin.")
                    except ValueError:
                        print("Geçersiz giriş. Lütfen bir sayı girin.")

                elif action_choice == '3':
                    print("Bu video geçildi. Yeni bir video seçiliyor...")
                    continue

                else:
                    print("Geçersiz seçim. Lütfen 1, 2 veya 3 girin.")

            except Exception as e:
                print(f"Bu video için yorumlar alınamadı: {e}")
                print("Yeni bir video seçiliyor...")
                continue

        else:
            print("Uygun video bulunamadı.")

        continue_choice = input("\nBaşka bir video için devam etmek istiyor musunuz? (E/H): ")
        if continue_choice.lower() != 'e':
            break

        print("10 saniye bekleniyor...")
        time.sleep(10)


if __name__ == "__main__":
    main()