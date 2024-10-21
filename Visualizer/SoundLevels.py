from pydub import AudioSegment
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

class AudioArray:
    def __init__(self, num_bars=10, delta_threshold=1000, sensitivity=5) -> None:
        self.resolution = num_bars
        self.visual_delta_threshold = delta_threshold
        self.sensitivity = sensitivity
        
    def set_num_bars(self, num_bar):
        self.resolution = num_bar
        
    def load_media(self, path):
        self.audio_path = path
        self.song = AudioSegment.from_file(self.audio_path).set_channels(2)
        self.samples = np.array(self.song.get_array_of_samples())
        self.max_sample = self.samples.max()
        self.points = np.zeros(self.resolution)
        
    def is_loaded(self):
        return self.song is not None
        
    def calculate_amps(self, position, playing=True):
        """Calculates the amplitudes used for visualising the media."""
        if self.song is None:
            return np.zeros(self.resolution)

        sample_count = int(self.song.frame_rate * 0.05)
        start_index = int((position/1000) * self.song.frame_rate)
        v_sample = self.samples[start_index:start_index+sample_count]  # samples to analyse

        # use FFTs to analyse frequency and amplitudes
        fourier = np.fft.fft(v_sample)
        freq = np.fft.fftfreq(fourier.size, d=0.05)
        amps = 2/v_sample.size * np.abs(fourier)
        data = np.array([freq, amps]).T

        point_range = 1 / self.resolution
        point_samples = []

        if not data.size:
            return

        for n, f in enumerate(np.arange(0, 1, point_range), start=1):
            # get the amps which are in between the frequency range
            amps = data[(f - point_range < data[:, 0]) & (data[:, 0] < f)]
            if not amps.size:
                point_samples.append(0)
            else:
                point_samples.append(amps.max()*((1+self.sensitivity/10+(self.sensitivity-1)/10)**(n/50)))

        # Add the point_samples to the self.points array, the reason we have a separate
        # array (self.bars) is so that we can fade out the previous amplitudes from
        # the past
        for n, amp in enumerate(point_samples):

            amp *= 2

            if abs(self.points[n] - amp) > self.visual_delta_threshold:
                self.points[n] = amp
            if self.points[n] < 1:
                self.points[n] = 0

        # interpolate points
        rs = gaussian_filter1d(self.points, sigma=2)

        # Mirror the amplitudes, these are renamed to 'rs' because we are using them
        # for polar plotting, which is plotted in terms of r and theta
        rs = np.concatenate((rs, np.flip(rs)))

        # they are divided by the highest sample in the song to normalise the
        # amps in terms of decimals from 0 -> 1
        return (rs / self.max_sample)

    # def run(self):
    #     """Runs the animate function depending on the song."""
    #     while True:
    #         if self.start_animate:
    #             try:
    #                 self.calculate_amps()
    #             except ValueError:
    #                 self.calculated_visual.emit(np.zeros(self.resolution))
    #                 self.start_animate = False
    #         # time.sleep(0.025)