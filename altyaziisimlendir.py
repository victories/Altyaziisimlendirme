import os
import glob
import re
import sys
import chardet

def main(folder_path, video_extensions):
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
                print(f"Kodlama tespit ediliyor {os.path.basename(file_path)}: {encoding}")

            # Kodlama tespit edilemezse veya UTF-8 değilse Windows-1254 kullan
            if encoding is None or encoding.lower() != 'utf-8':
                encoding = 'windows-1254'

            with open(file_path, 'r', encoding=encoding) as file:
                data = file.read()

            with open(file_path, 'w', encoding='utf-8') as file:
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
                new_subtitle_name = f"{video_name}.tr.srt"
                os.rename(subtitle_file, new_subtitle_name)
                convert_to_utf8(new_subtitle_name)
                print(f"İsimlendirildi ve kodlaması utf8 yapıldı: {os.path.basename(subtitle_file)} -> {os.path.basename(new_subtitle_name)}")
                break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python script.py <folder_path> [<video_extensions>]")
        print("Örnek: python script.py /path/to/your/folder .mp4,.mkv,.avi")
    else:
        folder_path = sys.argv[1]
        if len(sys.argv) >= 3:
            video_extensions = sys.argv[2].split(',')
        else:
            video_extensions = ['.mkv']  # Varsayılan değer .mkv
        main(folder_path, video_extensions)
