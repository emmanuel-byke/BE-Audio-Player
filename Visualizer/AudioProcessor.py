from pydub import AudioSegment
import numpy as np
from scipy import signal


from pydub.silence import detect_silence
from PyQt6.QtCore import QObject, pyqtSignal, QThread


class AudioLevel:
    def __init__(self, num_samples, channels=1, volume=100):
        self.num_samples = num_samples
        self.channels = channels
        self.volume = volume
        
    def load_audio(self, path):
        self.audio = AudioSegment.from_file(path)
        
    def is_loaded(self):
        return self.audio is not None
    
    def set_num_samples(self, num_samples):
        self.num_samples = num_samples
        
    def set_volume(self, volume):
        self.volume = volume

    def extract_audio_samples(self, position_ms):
        position_frames = int(position_ms * self.audio.frame_rate / 1000)
        samples = self.audio.get_sample_slice(position_frames, position_frames + self.num_samples)
        if self.channels > 1:
            channel_samples = samples.split_to_mono()
            return [list(channel.get_array_of_samples()) for channel in channel_samples]
        else:
            return samples.get_array_of_samples()
        
    def sample_values(self, position_ms):
        if self.channels > 1:
            result = list(self.extract_audio_samples(position_ms))
            result[0].extend(result[1])
            return [abs(d/400)*self.volume/100 for d in result[0]]
        else:
            result = list(self.extract_audio_samples(position_ms))
            return [abs(d/400)*self.volume/100 for d in result]
            
        

class AdvancedAudioLevel:
    def __init__(self, num_samples, channels=1, volume=100):
        self.num_samples = num_samples
        self.channels = channels
        self.volume = volume
        
    def load_audio(self, path):
        self.audio = AudioSegment.from_file(path)
        
    def is_loaded(self):
        return self.audio is not None
    
    def set_num_samples(self, num_samples):
        self.num_samples = num_samples
        
    def set_volume(self, volume):
        self.volume = volume

    def extract_audio_samples(self, position_ms):
        position_frames = int(position_ms * self.audio.frame_rate / 1000)
        samples = self.audio.get_sample_slice(position_frames, position_frames + self.num_samples)
        
        if self.channels > 1:
            channel_samples = samples.split_to_mono()
            return [channel.get_array_of_samples() for channel in channel_samples]
        else:
            return samples.get_array_of_samples()

    def apply_filter(self, b, a, samples):
        filtered_samples = signal.lfilter(b, a, samples)
        return AudioSegment(
            data=filtered_samples.tobytes(),
            frame_rate=self.audio.frame_rate,
            sample_width=self.audio.sample_width,
            channels=self.audio.channels
        )

    def extract_bass_treble_voice(self, position_ms):
        bass_cutoff = 200  # Adjust this value as needed
        treble_cutoff = 4000  # Adjust this value as needed
        
        b_bass, a_bass = signal.butter(4, bass_cutoff / (self.audio.frame_rate / 2), btype='low')
        b_treble, a_treble = signal.butter(4, treble_cutoff / (self.audio.frame_rate / 2), btype='high')
        
        audio_samples = self.extract_audio_samples(position_ms)
        
        bass_samples = self.apply_filter(b_bass, a_bass, audio_samples)
        treble_samples = self.apply_filter(b_treble, a_treble, audio_samples)
        # voice_samples = self.audio - bass_samples - treble_samples
        
        result = list(bass_samples.get_array_of_samples())
        result.extend(list(treble_samples.get_array_of_samples()))
        
        return [abs(r/400) for r in result] #, voice_samples



class SilenceDetector(QObject):
    start_silence_duration = pyqtSignal(int)
    end_silence_duration = pyqtSignal(int)
    
    def __init__(self, path):
        super().__init__()
        self.audio = AudioSegment.from_file(path)
        silence_threshold = -40
        min_silence_duration = 500

        silent_segments = detect_silence(self.audio, silence_thresh=silence_threshold, min_silence_len=min_silence_duration, seek_step=500)

        silent_durations_ms = [segment[1] - segment[0] for segment in silent_segments]
        
        self.start_silence_duration.emit(silent_durations_ms[0])
        self.end_silence_duration.emit(silent_durations_ms[1])
        

