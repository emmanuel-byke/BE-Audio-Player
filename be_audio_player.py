from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QTimer, QEvent
from PyQt6 import uic
import sys, argparse
import resources_qrc #important to be imported and not used

from widgets_initializer import HandleWidgets
from mouse import HandleMouse
from Helper import app_is_running, GetFile, res, get_cwd

# AttributeError: 'HandleMouse' object has no attribute 'move_window_flag'
get_file = GetFile()

class Ui(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(get_cwd() + '/simple.ui', self)
        self.setWindowFlags( Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowIcon(QIcon(res() + "/compact-disk-free-png.png"))
        self.setWindowTitle("BE Next Step")
        self.skin_window_title.setText('BE Next Step')
        self.setAcceptDrops(True)
        self.get_file = get_file
        self.setMouseTracking(True)
        self.mainFrame.setMouseTracking(True)
        
        self.handle_widgets = HandleWidgets(self, get_file=get_file)
        self.mouse = HandleMouse(self, self.handle_widgets)
        self.show()
        
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_widgets)
        self.update_timer.start(100)
        
        
        self.grabbed_keyboard = False
        self.grab_keyboard()
        
        # self.skin_play.clicked.connect(self.clicked)
        # self.skin_play.mousePressEvent = self.mousePressEvent
        # self.skin_play.mouseMoveEvent = self.mouseMoveEvent
        # self.skin_play.mouseReleaseEvent = self.mouseReleaseEvent
        
        

    
        
    def grab_keyboard(self):
        if not self.grabbed_keyboard:
            self.grabKeyboard()
            self.grabbed_keyboard = True

    def release_keyboard(self):
        if self.grabbed_keyboard:
            self.releaseKeyboard()
            self.grabbed_keyboard = False

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress:
            if self.grabbed_keyboard:
                # Handle the key event here while keyboard is grabbed
                print("Key pressed while keyboard is grabbed:", event.key())
                return True  # Event handled
        return super().eventFilter(obj, event)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        self.get_file.get_file_drag(event)
                
    def contextMenuEvent(self, event):
        self.contextMenuAction = self.mouse.getContextMenuMenu(event)

    def mousePressEvent(self, event):
        self.mouse.getMousePressEvent(event)
            
    def mouseMoveEvent(self, event):
        self.mouse.getMouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.mouse.getMouseReleaseEvent(event)
        
    def enterEvent(self, event):
        # This method is called when the mouse enters the main window
        self.handle_widgets.mouseEnter()

    def leaveEvent(self, event):
        # This method is called when the mouse leaves the main window
        self.handle_widgets.mouseLeave()
        
    def closeEvent(self, event):
        self.handle_widgets.before_quite_application()
        
    def update_widgets(self):
        self.handle_widgets.update()
        
    def keyPressEvent(self, event):
        self.mouse.get_shortcurts(event)
        event.accept()

    ##### , creationflags=subprocess.CREATE_NO_WINDOW >>> added following argument to subprocess.Popen in pydub.AudioSement
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="*", default=[], type=str)
    arg = parser.parse_args()
    get_file.add_to_playlist([d.replace("\\", '/') for d in arg.path], initial_add=True)
    
    
    if not app_is_running():
        app = QApplication(sys.argv)
        window = Ui()
        app.exec()



