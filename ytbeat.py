import librosa
import pydub
import youtube_dl
import os
import soundfile as sf

def download_and_split_audio(youtube_link):
    # Download the video as an mp3 file
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_link])

    # Convert the mp3 file to a wav file
    sound = pydub.AudioSegment.from_mp3("audio.mp3")
    sound.export("audio.wav", format="wav")

    # Load the wav file and detect the beats
    y, sr = librosa.load("audio.wav")
    tempo, beat_frames = librosa.beat.beat_track(y, sr=sr)

    # Create a subfolder to save the split audio files
    os.makedirs("samples", exist_ok=True)

    # Split the audio into multiple files based on 16 beat frames
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    for i in range(len(beat_times) - 16):
        start = beat_times[i]
        end = beat_times[i + 16]
        sf.write("samples/audio_%d.wav" % i, y[int(start * sr):int(end * sr)], sr, 'PCM_24')


if __name__ == "__main__":
    download_and_split_audio("https://www.youtube.com/watch?v=XXXXXXXXXXXX")