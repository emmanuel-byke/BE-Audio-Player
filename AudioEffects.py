from PyQt6.QtCore import QObject, pyqtSignal, QTimer

class Fade(QObject):
    fade_in_complete = pyqtSignal(bool)
    fade_out_complete = pyqtSignal(bool)
    fade_in_started = pyqtSignal(bool)
    fade_out_started = pyqtSignal(bool)
    volume = pyqtSignal(int)
    
    
    def __init__(self, volume=100, fade_duration=10000) -> None:
        super().__init__()
        self.set_master_volume(volume)
        self.tmp_volume = 0
        self._fade_duration_ = fade_duration
        
        self._fade_in_timer = None
        self._fade_out_timer = None
        
    def set_master_volume(self, volume):
        if volume <= 0:
            self.master_volume = 1 # avoid division by zero
        else:
            self.master_volume = volume
        
    def set_fade_duration(self, duration):
        if duration > 0:
            self._fade_duration_ = duration
        else: # avoid setting timer to 0 milliseconds or negative number
            self._fade_duration_ = 1
        
    def fade_out(self, duration=None):
        if duration is not None:
            self.set_fade_duration(duration)
            
        if self._fade_in_timer is not None:
            self._fade_in_timer.stop()
        else:
            self.tmp_volume = self.master_volume
        self.fade_out_started.emit(True)
        self._fade_out_timer = QTimer()
        self._fade_out_timer.setInterval(int(self._fade_duration_/self.master_volume))
        self._fade_out_timer.timeout.connect(self.__fade_out_algorithm__)
        self._fade_out_timer.start()
    
    def fade_in(self, duration=None):
        if duration is not None:
            self.set_fade_duration(duration)
            
        if self._fade_out_timer is not None:
            self._fade_out_timer.stop()
        else:
            self.tmp_volume = 0
        self.volume.emit(0)
        self.fade_in_started.emit(True)
        self._fade_in_timer = QTimer()
        self._fade_in_timer.setInterval(int(self._fade_duration_/self.master_volume))
        self._fade_in_timer.timeout.connect(self.__fade_in_algorithm__)
        self._fade_in_timer.start()
            
    def __fade_in_algorithm__(self):
        if self.tmp_volume >= self.master_volume:
            self._fade_in_timer.stop()
            self.fade_in_complete.emit(True)
        self.volume.emit(self.tmp_volume)
        self.tmp_volume += 1  
            
    def __fade_out_algorithm__(self):
        self.volume.emit(self.tmp_volume)
        self.tmp_volume -= 1
        if self.tmp_volume <= 0:
            self._fade_out_timer.stop()
            self.fade_out_complete.emit(True)
