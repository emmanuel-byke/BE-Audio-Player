from PyQt6.QtCore import QObject, pyqtSignal, QTimer
import os
from AudioEffects import Fade
from Helper import get_cwd
os.environ['PYTHON_VLC_MODULE_PATH'] = "{}/res".format(get_cwd())
os.environ['PYTHON_VLC_LIB_PATH'] = "{}/res/VLC/libvlc.dll".format(get_cwd())
import vlc
import json

class Player(QObject):
    playback_end = pyqtSignal()
    next_playback = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_audio_status)
        self.vlc_instance = vlc.Instance('--no-xlib', "--aout=spdif")
        
        self.vlc_player_1 = self.vlc_instance.media_player_new()
        self.vlc_player_2 = self.vlc_instance.media_player_new()
        self.player_1_turn = False  #### Most important variable when working with 2 players (don't change it's value any how)
        self.paused = False
        self.cross_fade_time = 1500
        
        self.player_1_fade = Fade(volume=100, fade_duration=self.cross_fade_time)
        self.player_1_fade.fade_in_started.connect(self.player_1_play)
        self.player_1_fade.fade_out_complete.connect(self.player_1_pause)
        self.player_1_fade.volume.connect(self.vlc_player_1.audio_set_volume)
        
        self.player_2_fade = Fade(volume=100, fade_duration=self.cross_fade_time)
        self.player_2_fade.fade_in_started.connect(self.player_2_play)
        self.player_2_fade.fade_out_complete.connect(self.player_2_pause)
        self.player_2_fade.volume.connect(self.vlc_player_2.audio_set_volume)
        
        self.path = None
                
    def load_audio(self, path, silence_array=None, auto_play=False):
        self.load_widgets = True # loading audio resets number of times it has been played  
        self.player_1_turn = not self.player_1_turn  
        self.path = path
        
        if silence_array is not None:
            self.silence_array = json.loads(silence_array)
        else:
            self.silence_array = [[0, 0], [0, 0]]
        
        if self.player_1_turn:
            self.vlc_player_1.set_media(self.vlc_instance.media_new(path, ':no-video'))
            # self.vlc_player_1.audio_output_set("spdif")
            if auto_play:
                self.play()
            self.player_2_fade.fade_out()
        else:
            self.vlc_player_2.set_media(self.vlc_instance.media_new(path, ':no-video'))
            # self.vlc_player_2.audio_output_set("spdif")
            if auto_play:
                self.play()
            self.player_1_fade.fade_out()
        
        self.seek(self.silence_array[0][1]) # Skip initial silence
        
        #### Redundance to prevent 2 players playing at same time
        if self.player_1_turn and self.vlc_player_2.get_state()==vlc.State.Playing:
            self.player_2_fade.fade_out()
        elif not self.player_1_turn and self.vlc_player_1.get_state()==vlc.State.Playing:
            self.player_1_fade.fade_out()
            
    def play(self):
        if self.player_1_turn:
            self.player_1_fade.fade_in()
        else:
            self.player_2_fade.fade_in()
        
    def player_1_play(self):
        self.vlc_player_1.play()
        self.post_play()
        
    def player_2_play(self):
        self.vlc_player_2.play()
        self.post_play()
        
    def post_play(self):
        self.timer.start(1000)
        self.paused = False
            
    def pause(self):
        if self.player_1_turn:
            self.player_1_fade.fade_out()
        else:
            self.player_2_fade.fade_out()
        self.paused = True

    def player_1_pause(self):
        self.vlc_player_1.pause()
        if self.vlc_player_2.get_state() in [vlc.State.NothingSpecial, vlc.State.Paused, vlc.State.Stopped, vlc.State.Ended, vlc.State.Error]:
            self.timer.stop()
        
        
    def player_2_pause(self):
        self.vlc_player_2.pause()
        if self.vlc_player_1.get_state() in [vlc.State.NothingSpecial, vlc.State.Paused, vlc.State.Stopped, vlc.State.Ended, vlc.State.Error]:
            self.timer.stop()
            
    def seek(self, pos):
        if pos < self.silence_array[0][1]:
            pos = self.silence_array[0][1]
        if self.player_1_turn:
            self.vlc_player_1.set_time(pos)
        else:
            self.vlc_player_2.set_time(pos)
            
    def update_audio_status(self):
        silence = self.silence_array[1][0]-self.cross_fade_time-4_000        
        if self.audio_reach_end() or (silence > 0 and self.get_pos() > silence and 
                                      self.get_pos() > 0 and self.player_state()==vlc.State.Playing):
            self.pause()
            self.stop_audio(emit_signal=True)
                        
    def stop_audio(self, emit_signal=True):
        self.load_widgets = False
        self.paused = False
        self.timer.stop()
        self.path = None
        
        if emit_signal:
            self.playback_end.emit()
        else:
            if self.player_1_turn:
                self.vlc_player_1.release()
                self.vlc_player_1 = self.vlc_instance.media_player_new()
                self.player_1_fade.volume.connect(self.vlc_player_1.audio_set_volume)
            else:
                self.vlc_player_2.release()
                self.vlc_player_2 = self.vlc_instance.media_player_new()
                self.player_1_fade.volume.connect(self.vlc_player_2.audio_set_volume)
                
    def get_pos(self):
        if self.player_1_turn:
            val = self.vlc_player_1.get_time()
        else:
            val = self.vlc_player_2.get_time()
        return val if val is not None else 0
    
    def get_total_length(self):
        if self.player_1_turn:
            return self.vlc_player_1.get_length()
        else:
            return self.vlc_player_2.get_length()
        
    def audio_reach_end(self):
        if self.player_1_turn:
            return self.vlc_player_1.get_state() == vlc.State.Ended
        else:
            return self.vlc_player_2.get_state() == vlc.State.Ended
        
    def player_state(self):
        if self.player_1_turn:
            return self.vlc_player_1.get_state()
        else:
            return self.vlc_player_2.get_state()
    
    def isPlaying(self):
        if self.player_1_turn:
            return self.vlc_player_1.get_state() == vlc.State.Playing
        else:
            return self.vlc_player_2.get_state() == vlc.State.Playing
        
    
    def isPaused(self):
        return self.paused
    
    def get_load_widgets(self):
        return self.load_widgets
    
    def set_load_widgets(self, val):
        self.load_widgets = val
        
    def set_volume(self, value):
        ### All players should have same volume ###
        if value <= 0:
            value = 0
        elif value > 100:
            value = 100
        
        self.vlc_player_1.audio_set_volume(value)   
        self.vlc_player_2.audio_set_volume(value)   
        self.player_1_fade.set_master_volume(value)
        self.player_2_fade.set_master_volume(value)
                
    def get_fade_obj(self):
        if self.player_1_turn:
            return self.player_1_fade
        else:
            return self.player_2_fade
      
    def get_path(self):
        return self.path