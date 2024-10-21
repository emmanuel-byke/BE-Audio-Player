from AudioProcessor import AudioLevel, AdvancedAudioLevel, SilenceDetector
from equalizer_bar import Bar
from PyQt6 import QtCore, QtWidgets

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.position = 0
        # audio_path = "C:/Users/Byke/Music/Converted/Burna Boy - Anybody.mp3"
        # audio_path = "C:/Users/Byke/Music/zimbabwe/12 Track 12.mp3"
        # audio_path = "C:/Users/Byke/Music/Cathoric Gospel/Yosefe Bambo Wathu.mp3"
        audio_path = "C:/Users/Byke/Music/sd/music/i_want_it_to_be_you_tatiana_manaois_ft_mac_mase_official_music_video_aac_748.mp3"
        self.audio_level = AudioLevel(15, 2)
        self.audio_level.load_audio(audio_path)
        
        self.advanced_audio = AdvancedAudioLevel(2, 1, 100)
        self.advanced_audio.load_audio(audio_path)
        
        self.bar = Bar(32, ['#0C0786', '#40039C', '#6A00A7', '#8F0DA3', '#B02A8F', '#CA4678', '#E06461',
                                          '#F1824C', '#FCA635', '#FCCC25', '#EFF821'])

        self.setCentralWidget(self.bar)

        # self._timer = QtCore.QTimer()
        # self._timer.setInterval(100)
        # self._timer.timeout.connect(self.update_values)
        # self._timer.start()
        
        # self.update_values()
        
        # print(self.advanced_audio.extract_bass_treble_voice(1000))
        
        silence = SilenceDetector(audio_path)
        silence.start_silence_duration.connect(self.start_silence)
        silence.end_silence_duration.connect(self.end_silence)
    
    def end_silence(self, val):
        print("End of Silence", val)
        
    def start_silence(self, val):
        print("Start silence", val)
        
        
       
        

    def update_values(self):
        self.bar.setValues(self.advanced_audio.extract_bass_treble_voice(self.position))
        self.position += 100
        

app = QtWidgets.QApplication([])
w = Window()
w.show()
app.exec()


