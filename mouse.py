from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QPoint
# from PyQt6.QtGui import QKeySequence

class HandleMouse():
    def __init__(self, parent, handler):
        self.parent = parent
        self.move_window_flag = None
        self.handler = handler
        
        # self.song_info = QAction(QtGui.QIcon(get_icon(54)), get_word(123), self)
        self.song_info = QAction("Test message", self.parent)
        # self.song_info.triggered.connect(self.song_info_fn)
        self.add_shortcuts()
        
    def add_shortcuts(self):
        self.handler.next_action.setShortcut("n")
        self.handler.prev_action.setShortcut("p")
        self.handler.repeate_action.setShortcut("r")
        self.handler.shuffle_action.setShortcut("Ctrl+s")
        self.handler.open_file_action.setShortcut("o")
        self.handler.open_folder_action.setShortcut("Ctrl+o")
        self.handler.exit_action.setShortcut("Ctrl+q")
        self.handler.bar_visualizer_action.setShortcut("Ctrl+b")
        self.handler.pulse_visualizer_action.setShortcut("Ctrl+p")
        self.handler.open_folder_action.setShortcut("Ctrl+o")
        
        # self.handler.play_action.setShortcut(QKeySequence("Space"))
        # self.handler.settings_action.setShortcut(QKeySequence("Return"))
        
    def get_shortcurts(self, event):
        key = event.key()
        if key == Qt.Key.Key_Space or key == Qt.Key.Key_MediaPause or key == Qt.Key.Key_MediaPlay:
            self.handler.play()
        elif key == Qt.Key.Key_Right:
            self.handler.player.seek(self.handler.player.get_pos()+5629)
        elif key == Qt.Key.Key_Left:
            self.handler.player.seek(self.handler.player.get_pos()-5629)
        elif key == Qt.Key.Key_Up:
            self.handler.change_volume(self.parent.volumeSlider.value()+5)
        elif key == Qt.Key.Key_Down:
            self.handler.change_volume(self.parent.volumeSlider.value()-5)
        elif key == Qt.Key.Key_M:
            self.handler.mute()
        elif key == Qt.Key.Key_N or key == Qt.Key.Key_MediaNext:
            self.handler.next()
        elif key == Qt.Key.Key_P or key == Qt.Key.Key_MediaPrevious:
            self.handler.prev()
        elif key == Qt.Key.Key_Escape:
            self.handler.before_quite_application()
        elif key == Qt.Key.Key_R:
            self.handler.repeate()
        elif key == Qt.Key.Key_S:
            self.handler.shuffle()
        elif key == Qt.Key.Key_L:
            self.handler.open_playlist()
        elif key == Qt.Key.Key_MediaStop:
            self.handler.stop_audio()
        # elif key == Qt.Key.Key_Shift:
        #     self.show_playlist_fn()
        # elif key == Qt.Key.Key_Control:
        #     self.hide_playlist_fn()
        elif key == Qt.Key.Key_Return:
            self.handler.settings()
        # elif key == Qt.Key.Key_Alt:
        #     self.btm_status.setText("")
        #     self.hide_status = 20
        # elif key == Qt.Key.Key_CapsLock:
        #     self.btm_status.setText("Emmanuel Basikolo")
        #     self.hide_status = -20
        # elif key == Qt.Key.Key_NumLock:
        #     self.btm_status.setText("Atsuko Basikolo")
        #     self.hide_status = -20
        elif key == Qt.Key.Key_Backspace:
            self.handler.player.seek(0)
        elif key == Qt.Key.Key_H:
            self.handler.open_defaults()
        # elif key == Qt.Key.Key_I:
        #     self.information()
        # elif key == Qt.Key.Key_C:
        #     self.shortcurts()
        # elif key == Qt.Key.Key_G:
        #     self.grabKeyboard()
        # elif key == Qt.Key.Key_X:
        #     self.releaseKeyboard()
        # elif key == Qt.Key.Key_U:
        #     self.player.song_info_update()
        #     self.new_song_played_fn()
        
        
    def getContextMenuMenu(self, event):
        contextMenu = QMenu(self.parent)
        contextMenu.addMenu(self.handler.open_menu)
        contextMenu.addSeparator()
        contextMenu.addAction(self.handler.play_action)
        contextMenu.addMenu(self.handler.playback_menu)
        contextMenu.addSeparator()
        contextMenu.addAction(self.handler.settings_action)
        contextMenu.addAction(self.handler.edit_metadata_action)
        contextMenu.addMenu(self.handler.view_menu)
        contextMenu.addSeparator()
        contextMenu.addAction(self.handler.select_playlist_action)
        contextMenu.addMenu(self.handler.load_playlist_menu_pop)
        contextMenu.addSeparator()
        contextMenu.addMenu(self.handler.account_menu)
        contextMenu.addMenu(self.handler.help_menu)
        contextMenu.addMenu(self.handler.skin_menu)
        contextMenu.addSeparator()
        contextMenu.addAction(self.handler.exit_action)
        contextMenu.setStyleSheet("background-color: white; color: black;")
        return contextMenu.exec(self.parent.mapToGlobal(event.pos()))
    
    def getMousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.move_window_flag = True
            self.m_position = event.globalPosition().toPoint() - self.parent.pos()
            event.accept()
            
    def getMouseMoveEvent(self, event):
        if Qt.MouseButton.LeftButton and self.move_window_flag:            
            self.parent.move(event.globalPosition().toPoint() - self.m_position)
            event.accept()

    def getMouseReleaseEvent(self, event):
        self.move_window_flag = False
        self.m_position = QPoint()
        