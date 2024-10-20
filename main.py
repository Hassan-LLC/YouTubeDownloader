import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled

def list_formats(url):
    try:
        ydl_opts = {
            'listformats': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])
            print("\nAvailable formats for this video:\n")
            for f in formats:
                print(f"Format code: {f['format_id']} - {f['ext']} - {f['resolution']} - {f['fps']}fps - {f['vcodec']}")
    except Exception as e:
        print(f"Error listing formats: {e}")

def download_video(url, format_code):
    try:
        ydl_opts = {
            'format': format_code,  # Download the selected format by the user
            'outtmpl': '%(title)s.%(ext)s',  # Save the video with its title as the file name
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  # Ensure output format is mp4
            }]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Video downloaded successfully!")
    except Exception as e:
        print(f"Error downloading video: {e}")

def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        print("\nTranscript available. Displaying transcript:")
        for item in transcript:
            print(f"{item['text']}")
    except NoTranscriptFound:
        print("No transcript available for this video.")
    except TranscriptsDisabled:
        print("Transcripts are disabled for this video.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    url = input("Enter the YouTube video URL: ")

    # Extract the video ID from the URL
    try:
        video_id = url.split("v=")[-1]
        if "&" in video_id:
            video_id = video_id.split("&")[0]
    except IndexError:
        print("Invalid YouTube URL. Please check the format.")
        exit()

    # List available formats
    list_formats(url)

    # Ask the user to choose a format (resolution, etc.)
    format_code = input("\nEnter the format code for the desired resolution: ")

    # Download the video using the selected format
    download_video(url, format_code)

    # Check for a transcript
    fetch_transcript(video_id)
