from pydub import AudioSegment, silence
import numpy as np

def remove_silence(audio_path, output_path, min_silence_duration=1000, silence_threshold=-50):
    audio = AudioSegment.from_file(audio_path)
    silent_ranges = silence.detect_silence(audio, min_silence_duration=min_silence_duration, silence_thresh=silence_threshold)

    if not silent_ranges:
        print("No silence detected.")
        return

    # Calculate the start and end points of the non-silent audio
    non_silent_start = max(silent_ranges[0][0] - 100, 0)  # Ensure a bit of audio before the first detected silence
    non_silent_end = min(silent_ranges[-1][1] + 100, len(audio))  # Ensure a bit of audio after the last detected silence

    non_silent_audio = audio[non_silent_start:non_silent_end]

    non_silent_audio.export(output_path, format="wav")

if __name__ == "__main__":
    input_audio_path = "C:/Users/Byke/Downloads/music/Piksy-Ole Mp3 Download - Nyasa Vibes.mp3"
    output_audio_path = "output_audio.wav"
    remove_silence(input_audio_path, output_audio_path)
