import os
import sys
import subprocess
import youtube_dl
from moviepy.editor import *


def download_videos(singer, num_videos):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'max_downloads': num_videos,
        'default_search': 'ytsearch',
        'verbose': True,  # Add the verbose flag
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([f'{singer}'])
        except youtube_dl.DownloadError as e:
            print(f"Error occurred: {e}")
            print("Unable to download videos. Please try again later.")
            return
        except Exception as e:
            print(f"Error occurred: {e}")
            return

def convert_to_audio():
    for filename in os.listdir('.'):
        if filename.endswith('.webm'):
            audio = AudioFileClip(filename)
            audio.write_audiofile(f'{filename[:-5]}.mp3')
            os.remove(filename)

def cut_audio(duration):
    for filename in os.listdir('.'):
        if filename.endswith('.mp3'):
            audio = AudioFileClip(filename)
            audio = audio.subclip(0, duration)
            audio.write_audiofile(f'cut_{filename}')
            os.remove(filename)

def merge_audios(output_file):
    audio_files = [file for file in os.listdir('.') if file.startswith('cut_') and file.endswith('.mp3')]
    audio_clips = [AudioFileClip(file) for file in audio_files]
    final_clip = concatenate_audioclips(audio_clips)
    final_clip.write_audiofile(output_file)

def mashup(singer, num_videos, duration, output_file):
    try:
        download_videos(singer, num_videos)
        convert_to_audio()
        cut_audio(duration)
        merge_audios(output_file)
        print("Mashup completed successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python <program py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)
    
    singer = sys.argv[1]
    num_videos = int(sys.argv[2])
    duration = int(sys.argv[3])
    output_file = sys.argv[4]
    mashup(singer, num_videos, duration, output_file)
