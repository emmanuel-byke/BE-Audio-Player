from PyQt6.QtCore import QObject, pyqtSignal, QTimer

class Shrink(QObject):
    shrink_start = pyqtSignal()
    shrink_end = pyqtSignal()
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.coordinates = [parent.pos().x(), parent.pos().y(), parent.width(), parent.height()]
        
    def start_shrink(self, horizontal=False, vertical=False):
        self.shrink_start.emit()

        self.shrink_timer = QTimer()
        self.shrink_timer.timeout.connect(lambda: self._shrink_algorithm_(horizontal, vertical))
        self.shrink_timer.setInterval(10)
        self.shrink_timer.start()
        
        
    def _shrink_algorithm_(self, horizontal, vertical):
        try:
            if horizontal:
                self.coordinates[2] = self.coordinates[2]-6
                self.coordinates[0] = self.coordinates[0]+3
            if vertical:
                self.coordinates[3] = self.coordinates[3]-6
                self.coordinates[1] = self.coordinates[1]+3
                
            if (not horizontal and not vertical) or self.coordinates[2] <= 0 or self.coordinates[3] <= 0:
                self.shrink_end.emit()
                self.shrink_timer.stop()
            else:
                self.parent.setGeometry(self.coordinates[0], self.coordinates[1], self.coordinates[2], self.coordinates[3])
                if self.coordinates[2] <= 6 or self.coordinates[3] <= 6:
                    self.parent.setStyleSheet('background-color: white;')
        except:
            pass
        
    
        
        
        