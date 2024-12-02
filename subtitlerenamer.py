import os
import glob
import re
import sys
import chardet
import codecs

def main(folder_path, video_extensions, language_code="tr"):
    # Klasör yolunu normalize et ve güvenli şekilde işleme hazırla
    folder_path = os.path.abspath(folder_path)

    # Klasördeki tüm dosyaları listele
    all_files = glob.glob(os.path.join(folder_path, '*'))

    # Video dosyalarını ve altyazı dosyalarını ayır
    video_files = [f for f in all_files if os.path.splitext(f)[1] in video_extensions]
    subtitle_files = [f for f in all_files if os.path.splitext(f)[1] == '.srt']

    # Sezon ve bölüm numaralarını ayıklamak için regex deseni
    pattern = re.compile(r'[Ss](\d+)[Ee](\d+)')

    def get_season_episode(filename):
        match = pattern.search(filename)
        if match:
            return int(match.group(1)), int(match.group(2))
        return None, None

    def convert_to_utf8(file_path):
        try:
            # Dosyanın kodlamasını tespit et
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                confidence = result['confidence']
                print(f"Kodlama tespit ediliyor {os.path.basename(file_path)}: {encoding} ({confidence * 100:.2f}% güven)")

            # UTF-8 with BOM kontrolü
            if raw_data.startswith(codecs.BOM_UTF8):
                encoding = 'utf-8-sig'
                print(f"{os.path.basename(file_path)} dosyası UTF-8 with BOM içeriyor. Kodlama ayarlandı: {encoding}")

            # Kodlama tespit edilemezse veya güven düşükse varsayılan kodlama kullan
            if encoding is None or confidence < 0.8:
                encoding = 'windows-1254'
                print(f"Kodlama tespit edilemedi veya güven düşük. Varsayılan kodlama kullanılıyor: {encoding}")

            # Dosyayı oku ve UTF-8 olarak yeniden yaz
            with codecs.open(file_path, 'r', encoding=encoding) as file:
                data = file.read()

            with codecs.open(file_path, 'w', encoding='utf-8') as file:
                file.write(data)
            print(f"Başarıyla UTF-8 olarak kaydedildi {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Kaydedilirken hata oluştu {os.path.basename(file_path)}: {e}")

    # Her video dosyası için ilgili altyazı dosyasını bul ve adını değiştir
    for video_file in video_files:
        video_name, _ = os.path.splitext(video_file)
        season_video, episode_video = get_season_episode(video_name)

        for subtitle_file in subtitle_files:
            subtitle_name, _ = os.path.splitext(subtitle_file)
            season_subtitle, episode_subtitle = get_season_episode(subtitle_name)

            if season_video == season_subtitle and episode_video == episode_subtitle:
                new_subtitle_name = os.path.join(folder_path, f"{os.path.basename(video_name)}.{language_code}.srt")
                try:
                    os.rename(subtitle_file, new_subtitle_name)
                    convert_to_utf8(new_subtitle_name)
                    print(f"İsimlendirildi ve kodlaması UTF-8 yapıldı: {os.path.basename(subtitle_file)} -> {os.path.basename(new_subtitle_name)}")
                except Exception as rename_error:
                    print(f"Yeniden adlandırma hatası: {rename_error}")
                break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python script.py <folder_path> [<video_extensions>] [<language_code>]")
        print("Örnek: python script.py '/path/to/your/folder' .mp4,.mkv en")
    else:
        folder_path = sys.argv[1]
        if len(sys.argv) >= 3 and len(sys.argv[2]) == 2:
            language_code = sys.argv[2]  # Dil kodu belirtilmiş
            video_extensions = ['.mkv']  # Varsayılan değer
        elif len(sys.argv) >= 3:
            video_extensions = sys.argv[2].split(',')
            language_code = "tr"  # Varsayılan dil kodu
        else:
            video_extensions = ['.mkv']
            language_code = "tr"
        main(folder_path, video_extensions, language_code)
