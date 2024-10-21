from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6 import uic
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon
from SVG import change_color
from Helper import res, get_cwd, get_widget_coordinates, set_label_pixmap, user_folder
from read_db import Read
from create_update_db import Create
from update_db import Update
from AudioMetadata import ExtractMetadata, MetadataWriter


class ConfirmPlaylist(QMainWindow, QObject):
    data = pyqtSignal(dict)
    
    def __init__(self, parent):
        super().__init__()
        uic.loadUi(get_cwd() + '/confirm_playlist.ui', self)
        self.setWindowFlags( Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(*get_widget_coordinates(parent.geometry(), self.geometry(), 'center'))
        self.picture_path = ""
        self.isShared = False
        self.read = Read()
        self.accept_name = False
        self.parent = parent
        self.parent.release_keyboard()
        
        self.destroyed.connect(self.parent.grab_keyboard)
        self.back.clicked.connect(self.deleteLater)
        self.create.clicked.connect(self.commit)
        self.playlistname.returnPressed.connect(self.commit)
        self.shared.clicked.connect(self.shared_handler)
        self.playlistname.textChanged.connect(self.typingEvent)
        self.create.setDisabled(not self.accept_name)
        self.message.setText("")
        self.render_icons()
        
        
        self.show()
        
        
    def commit(self):
        if self.playlistname.text().strip() != "" and self.accept_name:
            self.data.emit({
                "name": self.playlistname.text(),
                "isShared": self.isShared,
                "picture": self.picture_path
            }) 
            self.deleteLater() 
        elif not self.accept_name:
            self.message.setText("Forbidden name")
        else:
            self.message.setText("Playlist name cannot be empty")
        
    def typingEvent(self):
        if self.playlistname.text().lower().strip() in  [entry['playlist_name'].lower().strip() for entry in self.read.get_playlistnames_attr()]:
            self.message.setText("Playlist already exist")
            self.accept_name = False
        else:
            self.accept_name = True
            self.message.setText("")
        self.accept_name = False if self.playlistname.text().strip() == "" else self.accept_name
        self.create.setDisabled(not self.accept_name)

    def shared_handler(self):
        self.isShared = not self.isShared
        self.render_icons()

    def render_icons(self):
        if self.isShared:
            self.shared.setIcon(QIcon(change_color(res()+"/Icons/toggle-right.svg", fill='green', stroke='red')))
        else:
            self.shared.setIcon(QIcon(change_color(res()+"/Icons/toggle-left.svg", fill='transparent', stroke='rgb(30, 21, 38)')))
        self.create.setIcon(QIcon(change_color(res()+"/Icons/check.svg", fill='transparent', stroke='rgb(98, 63, 117)')))
        self.back.setIcon(QIcon(change_color(res()+"/Icons/arrow-left.svg", fill='transparent', stroke='rgb(211, 78, 42)')))
        self.pic.setIcon(QIcon(change_color(res()+"/Icons/image.svg", fill='transparent', stroke='rgb(178, 82, 191)')))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.move_window_flag = True
            self.m_position = event.globalPosition().toPoint() - self.pos()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if Qt.MouseButton.LeftButton and self.move_window_flag:            
            self.move(event.globalPosition().toPoint() - self.m_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.move_window_flag = False
        self.m_position = QPoint()
        
        
        
class ShowList(QMainWindow, QObject):
    data = pyqtSignal(dict)
    selected_item = pyqtSignal(str)
    remove_item_signal = pyqtSignal(str)
    
    def __init__(self, parent, get_model, args, get_file=None):
        super().__init__()
        uic.loadUi(get_cwd() + '/load_playlist.ui', self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(*get_widget_coordinates(parent.geometry(), self.geometry(), 'side'))
        self.create = Create()
        self.read = Read()
        self.update_db = Update()
        self.parent = parent
        self.get_model = get_model
        self.args = args
        if get_file is not None:
            self.get_file = get_file
        
        self.back.clicked.connect(self.deleteLater)
        self.add.clicked.connect(self.add_item)
        self.load.clicked.connect(self.commit)
        self.removeItem.clicked.connect(self.remove_item)
        self.renameItem.clicked.connect(self.rename_item)
        self.table.doubleClicked.connect(self.commit)
        
        self.show_data()
        # self.render_icons()
        
        self.show()
    
    def show_data(self):
        self.table_model = self.get_model()
        self.table.setModel(self.table_model)
        
    def add_item(self):
        if self.args['mode'] == 'playlist':
            self.create_playlist_window = ConfirmPlaylist(self.parent)
            self.destroyed.connect(self.create_playlist_window.deleteLater)
            self.create_playlist_window.data.connect(lambda data: self.data.emit(data))
            self.create_playlist_window.data.connect(lambda data: self.add_new_playlist_to_same_table(data))
        elif self.args['mode'] == 'audio':
            self.get_file.get_file_btn()
        
            
    def add_new_playlist_to_same_table(self, data):
        self.show_data()
        
    def get_selected_item(self):
        selected_indexes = self.table.selectionModel().selectedIndexes()
        if selected_indexes:
            selected_rows = [index.row() for index in selected_indexes]
            if selected_rows is not None:
                return self.table_model.data[selected_rows[self.args['row']]][self.args['col']]
            else:
                return None
        else:
            return None
        
    def commit(self):
        selected = self.get_selected_item()
        if selected is not None:
            self.selected_item.emit(selected)
            self.deleteLater()
            self.parent.grabKeyboard()
        
    def remove_item(self):
        selected = self.get_selected_item()
        if selected is not None:
            if self.args['mode'] == 'playlist':
                self.update_db.remove_playlist(selected)
            else:
                self.remove_item_signal.emit(selected)
            self.show_data()
        
    def rename_item(self):
        selected = self.get_selected_item()
        if selected is not None:
            if self.args['mode'] == 'playlist':
                self.line_edit_window = LineEditValue(self.parent, self)
                self.parent.destroyed.connect(self.line_edit_window.deleteLater)
                self.destroyed.connect(self.line_edit_window.deleteLater)
                self.line_edit_window.text.connect(lambda txt: self.update_db.update_playlist_name(selected, txt))
                self.line_edit_window.text.connect(self.show_data)
     
    def render_icons(self):
        if self.isShared:
            self.shared.setIcon(QIcon(change_color(res()+"/Icons/toggle-right.svg", fill='green', stroke='red')))
        else:
            self.shared.setIcon(QIcon(change_color(res()+"/Icons/toggle-left.svg", fill='transparent', stroke='rgb(30, 21, 38)')))
        self.create.setIcon(QIcon(change_color(res()+"/Icons/check.svg", fill='transparent', stroke='rgb(98, 63, 117)')))
        self.back.setIcon(QIcon(change_color(res()+"/Icons/arrow-left.svg", fill='transparent', stroke='rgb(211, 78, 42)')))
        self.pic.setIcon(QIcon(change_color(res()+"/Icons/image.svg", fill='transparent', stroke='rgb(178, 82, 191)')))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.move_window_flag = True
            self.m_position = event.globalPosition().toPoint() - self.pos()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if Qt.MouseButton.LeftButton and self.move_window_flag:            
            self.move(event.globalPosition().toPoint() - self.m_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.move_window_flag = False
        self.m_position = QPoint()
        
        
        
        
        
        
        
        
        

class YesNo(QMainWindow, QObject):
    yes_signal = pyqtSignal()
    no_signal = pyqtSignal()
    is_yes_signal = pyqtSignal(bool)
    
    def __init__(self, x_coor, y_coor):
        super().__init__()
        uic.loadUi(get_cwd() + '/confirm_box.ui', self)
        self.setWindowFlags( Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.move(x_coor, y_coor)
        
        self.no.clicked.connect(self.no_clicked)
        self.yes.clicked.connect(self.yes_clicked)        
        self.show()        
        
    def no_clicked(self):
        self.deleteLater()
        self.no_signal.emit()
        self.is_yes_signal.emit(False)
        
    def yes_clicked(self):
        self.deleteLater()
        self.yes_signal.emit()
        self.is_yes_signal.emit(True)
        
    def render_icons(self):
        if self.isShared:
            self.shared.setIcon(QIcon(change_color(res()+"/Icons/toggle-right.svg", fill='green', stroke='red')))
        else:
            self.shared.setIcon(QIcon(change_color(res()+"/Icons/toggle-left.svg", fill='transparent', stroke='rgb(30, 21, 38)')))
        self.create.setIcon(QIcon(change_color(res()+"/Icons/check.svg", fill='transparent', stroke='rgb(98, 63, 117)')))
        self.back.setIcon(QIcon(change_color(res()+"/Icons/arrow-left.svg", fill='transparent', stroke='rgb(211, 78, 42)')))
        self.pic.setIcon(QIcon(change_color(res()+"/Icons/image.svg", fill='transparent', stroke='rgb(178, 82, 191)')))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.move_window_flag = True
            self.m_position = event.globalPosition().toPoint() - self.pos()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if Qt.MouseButton.LeftButton and self.move_window_flag:            
            self.move(event.globalPosition().toPoint() - self.m_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.move_window_flag = False
        self.m_position = QPoint()
        
        
        
class LineEditValue(QMainWindow, QObject):
    text = pyqtSignal(str)
    
    def __init__(self, parent, parent_coord, names=[]):
        super().__init__()
        uic.loadUi(get_cwd() + '/entername.ui', self)
        self.setWindowFlags( Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(*get_widget_coordinates(parent_coord.geometry(), self.geometry(), 'side'))
        self.parent = parent
        self.names = names
        
        self.back.clicked.connect(self.deleteLater)
        self.check.clicked.connect(self.commit)
        self.nameValue.returnPressed.connect(self.commit)
        self.nameValue.textChanged.connect(self.typing_event)
        
        self.check.setDisabled(not self.is_valid_text())
        self.destroyed.connect(self.parent.grab_keyboard)
        self.parent.release_keyboard()
               
        self.show()  
        
    def commit(self):
        if self.is_valid_text():
            self.text.emit(self.nameValue.text().strip())
            self.deleteLater()
            
        
            
        
    def is_valid_text(self):
        return self.nameValue.text().strip() != "" or self.nameValue.text().strip().lower() not in [d.lower().strip() for d in self.names]
    
    def typing_event(self):
        if self.is_valid_text():
            self.message.setText("")
        elif self.nameValue.text().strip() != "":
            self.message.setText("Enter Something Please")
        elif self.nameValue.text.strip().lower() not in [d.lower().strip() for d in self.names]:
            self.message.setText("Select another word")
        else:
            self.message.setText("Invalid Text Used")
        self.check.setDisabled(not self.is_valid_text())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.move_window_flag = True
            self.m_position = event.globalPosition().toPoint() - self.pos()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if Qt.MouseButton.LeftButton and self.move_window_flag:            
            self.move(event.globalPosition().toPoint() - self.m_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.move_window_flag = False
        self.m_position = QPoint()




class MetadataEditor(QMainWindow, QObject):
    metadata_changed = pyqtSignal(str)
    
    def __init__(self, parent, path):
        super().__init__()
        uic.loadUi(get_cwd() + '/metadata_editor.ui', self)
        self.setWindowTitle("BE Metadata Editor")
        self.setWindowFlags( Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAcceptDrops(True)
        self.setGeometry(*get_widget_coordinates(parent.geometry(), self.geometry(), 'side'))
        self.accept_name = False
        self.parent = parent
        self.parent.release_keyboard()
        
        self.destroyed.connect(self.parent.grab_keyboard)
        parent.destroyed.connect(self.deleteLater)
        self.closeBtn.clicked.connect(self.deleteLater)
        self.minimizeBtn.clicked.connect(self.showMinimized)
        self.saveBtn.clicked.connect(self.commit)
        self.artwork.mousePressEvent = self.choose_artwork
        # self.playlistname.returnPressed.connect(self.commit)
        # self.playlistname.textChanged.connect(self.typingEvent)
        # self.create.setDisabled(not self.accept_name)
        
        self.message.setText("")
        self.render_icons()
        self.metadata_writer = None
        self.path = path
        
        if path is not None:
            self.metadata = ExtractMetadata(path)
            self.metadata_writer = MetadataWriter(path)
            self.filename.setText(self.metadata.get_filename()[0])
            self.title.setText(self.metadata.get_title())
            self.artist.setText(self.metadata.get_artist())
            self.album.setText(self.metadata.get_album())
            self.genre.setText(self.metadata.get_genre())
            if self.metadata.get_artwork() is not None:
                set_label_pixmap(self.artwork, self.metadata.get_artwork(), False)
            else:
                set_label_pixmap(self.artwork, res()+"/Images/compact-disk-free-png.png", True)
        else:
            self.filename.setText("No File Found")
        
        
        self.show()
    def choose_artwork(self, event):
        folder = user_folder("/Pictures")
        path = QFileDialog.getOpenFileName(QMainWindow(), "Select Artwork", folder, 
                    "*.jpg *.jpeg")[0]
        if self.path is not None:
            self.metadata_writer.modify_artwork(path)
            self.metadata_writer.save()
            set_label_pixmap(self.artwork, self.metadata.get_artwork(), False)
    
    def commit(self):
        self.metadata_writer.modify_title(self.title.text())
        self.metadata_writer.modify_artist(self.artist.text())
        self.metadata_writer.modify_album(self.album.text())
        self.metadata_writer.modify_genre(self.genre.text())
        self.metadata_writer.save()
        
        self.metadata_changed.emit(self.path)
        
        
    def typingEvent(self):
        if self.playlistname.text().lower().strip() in  [entry['playlist_name'].lower().strip() for entry in self.read.get_playlistnames_attr()]:
            self.message.setText("Playlist already exist")
            self.accept_name = False
        else:
            self.accept_name = True
            self.message.setText("")
        self.accept_name = False if self.playlistname.text().strip() == "" else self.accept_name
        self.create.setDisabled(not self.accept_name)


    def render_icons(self):
        self.closeBtn.setIcon(QIcon(change_color(res()+"/Icons/x-circle.svg", fill='transparent', stroke='#FF2929')))
        self.minimizeBtn.setIcon(QIcon(change_color(res()+"/Icons/minus.svg", fill='transparent', stroke='#2495FF')))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.move_window_flag = True
            self.m_position = event.globalPosition().toPoint() - self.pos()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if Qt.MouseButton.LeftButton and self.move_window_flag:            
            self.move(event.globalPosition().toPoint() - self.m_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.move_window_flag = False
        self.m_position = QPoint()
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_url = event.mimeData().urls()
            for f in file_url:
                if self.path is not None and f.toLocalFile().rsplit('.')[1].lower() in ['jpeg', 'jpg']:
                    self.metadata_writer.modify_artwork(f.toLocalFile())
                    self.metadata_writer.save()
                    set_label_pixmap(self.artwork, self.metadata.get_artwork(), False)
                    
        
        




