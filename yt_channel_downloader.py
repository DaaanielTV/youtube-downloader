import sys
import re
import yt_dlp

def sanitize_channel_input(input_str):
    """Bereinigt die Channel-Eingabe"""
    clean_str = re.sub(r'^[\'"\[\]()]+|[\'"\[\]()]+$', '', input_str)
    
    if clean_str.startswith(('http://', 'https://')):
        return clean_str
    
    if clean_str.startswith('UC'):
        return f'https://www.youtube.com/channel/{clean_str}'
    
    if clean_str.startswith('@'):
        return f'https://www.youtube.com/{clean_str}'
    
    raise ValueError(f'Ungültige Channel-ID: {clean_str}')

def main():
    if len(sys.argv) != 2:
        print("Verwendung: python yt_channel_downloader.py <Channel-URL/ID>")
        sys.exit(1)

    try:
        channel_url = sanitize_channel_input(sys.argv[1])
        print(f"Aktive Channel-URL: {channel_url}")
    except ValueError as e:
        print(f"Fehler: {str(e)}")
        sys.exit(1)

    ydl_opts = {
        # Format-Auswahl für direkte MP4-Dateien
        'format': 'best[height=720][ext=mp4]/bestvideo[height=720]+bestaudio',
        
        # Merge-Einstellungen
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
        
        # FFmpeg-Konfiguration
        'ffmpeg_location': '/usr/bin/ffmpeg',  # Pfad bei Windows: 'C:/ffmpeg/bin/ffmpeg.exe'
        
        # Basis-Einstellungen
        'outtmpl': 'downloads/%(title)s [%(id)s].%(ext)s',
        'download_archive': 'downloaded.txt',
        'retries': 10,
        'ignoreerrors': True,
        'writethumbnail': False,
        'writeinfojson': False,
        'keepvideo': False  # Löscht die temporären Dateien nach dem Merge
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([channel_url])
        print("\nDownload erfolgreich - Nur .mp4 Dateien erstellt!")
    except Exception as e:
        print(f"\nFehler: {str(e)}")

if __name__ == "__main__":
    main()
