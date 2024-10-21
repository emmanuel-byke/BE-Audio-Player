from PyQt6.QtCore import QObject, pyqtSignal
from create_update_db import Create
from read_db import Read
from update_db import Update
from AdditionWidgets import ConfirmPlaylist, ShowList, YesNo
from TableModels import FirstModel, SecondModel

class PlaylistTools(QObject):
    reload_player = pyqtSignal()
    stop_audio = pyqtSignal()
    play_audio = pyqtSignal(str, str, int)
    playlist_changed = pyqtSignal()
    play_next = pyqtSignal(bool)

    def __init__(self, parent, remover_helper, get_file):
        super().__init__()
        self.parent = parent
        self.create = Create()
        self.read = Read()
        self.update_db = Update()    
        self.remover_helper = remover_helper 
        self.table_model = None
        self.get_file = get_file
        self.audio_playlist_window_is_open = False
       
        
        
        self.parent.playlistTable.horizontalHeader().setStyleSheet(
            "QHeaderView::section {"
            "    background-color: rgba(40, 50, 60, 30);"
            "    border: none;"
            "}"
        )
        parent.playlistTable.verticalHeader().setVisible(False) # it introduces a white point at top left corner
        self.parent.playlistTable.verticalHeader().setStyleSheet(
            "QHeaderView::section {"
            "    background-color: rgba(0, 0, 0, 0);"
            "    border: none;"
            "}"
        )   
        self.parent.playlistTable.setStyleSheet(
            "QTableView::item:selected {"
            "    background-color: qlineargradient(spread:pad, x1:0, y1:0.477273, x2:1, y2:0.443, stop:0 rgba(220, 36, 36, 255), stop:1 rgba(74, 86, 157, 255));"
            "    color: white;"
            "}"
        )
        
        self.parent.removeSelectedSong.clicked.connect(lambda: self.remove_selected_item(self.get_selected_item()))
        self.parent.clearPlaylist.clicked.connect(self.clear_playlist)
        self.parent.deletePlaylist.clicked.connect(self.delete_playlist)
      
    def create_playlist(self):
        self.confirm_window = ConfirmPlaylist(self.parent)
        self.confirm_window.data.connect(self.commit)
        self.parent.destroyed.connect(self.confirm_window.deleteLater)
        self.confirm_window.setWindowTitle("BE Next Step: Create Playlist")
        
        self.parent.releaseKeyboard()
        
    def commit(self, data):
        self.create.create_playlist_commons(name=data['name'], is_shared=data['isShared'], picture=data['picture'])
        self.create.create_variable("playlist created", True)
        self.switch_playlist(data['name'])  
        
    def current_playlist_index(self):
        name = self.read.get_variable('current playlist')
        for i, d in enumerate(self.read.get_playlistnames_attr()):
            if name == d['playlist_name']:
                return i
        return None
    
    def get_load_playlist_names(self):
        data = self.read.get_playlistnames_attr()
        index = self.current_playlist_index()
        if not self.read.get_variable('virtual playlist', False) and index is not None:
            data.pop(index)
        return FirstModel(data)        
        
    def load_playlist_names(self):
        self.my_window = ShowList(self.parent, self.get_load_playlist_names, {'row':0, 'col':1, 'mode':'playlist'})
        self.parent.destroyed.connect(self.my_window.deleteLater)
        self.my_window.data.connect(self.commit)
        self.my_window.selected_item.connect(self.handle_selected_playlist) ### different from one in commit function
        self.my_window.setWindowTitle("BE Next Step: Load Playlist")
                
    def handle_selected_playlist(self, new_playlist_name):
        self.switch_playlist(new_playlist_name) 
        
    # check and determines whether to stop playback (and switch playlist) but it always creates new playlist
    def switch_playlist(self, new_playlist_name):
        if self.read.get_variable('playing', False):
            self.yes_no_window = YesNo(self.parent.geometry().x()+50, self.parent.geometry().y()+80)
            self.parent.destroyed.connect(self.yes_no_window.deleteLater)
            self.yes_no_window.yes_signal.connect(lambda: self.switch_playlist_events(new_playlist_name)) 
            self.yes_no_window.promptText.setText(f"Switching to {new_playlist_name.capitalize()} playlist will stop the playback,\
                \nDo you want to continue?")
            self.yes_no_window.setWindowTitle("BE Next Step: Respond")
        else:
            self.switch_playlist_events(new_playlist_name)
            
        self.create.create_variable("playlist changed", True)
        self.create.create_variable("current playlist", new_playlist_name)
            
    def switch_playlist_events(self, new_playlist_name):
        self.create.create_variable('virtual playlist', False)
        self.create.create_variable("current playlist", new_playlist_name)
        self.stop_audio.emit()
        self.reload_player.emit()
        self.playlist_changed.emit()
        self.show_current_data()
        
    def show_favourite(self):
        self.create.create_virtual_playlist('favourite')
        self.create.create_variable('virtual playlist', 'favourite')
        self.show_current_data()
    
    def show_most_played(self):
        self.create.create_virtual_playlist('Most Played')
        self.create.create_variable('virtual playlist', 'Most Played')
        self.show_current_data()

    def show_shuffle(self):
        if self.read.get_variable('virtual playlist', False):
            files = self.read.get_virtual_playlist_specific_attr()
        else:
            files = self.read.get_playlist_files_specific_attr(self.read.get_variable('current playlist'))
        self.create.create_virtual_playlist('shuffle', files)
        self.create.create_variable('virtual playlist', 'shuffle')
        self.show_current_data()
        
    def current_audio_playlist_index(self, data, current_path):
        for i, d in enumerate(data):
            if current_path == d['path']:
                return i
        return None
    
    def get_audio_list_model(self):
        if self.read.get_variable('virtual playlist', False):
            data = self.read.get_virtual_playlist() 
            current_path = self.read.get_variable('virtual playing path')
        else:
            playlist = self.read.get_variable("current playlist")
            data = self.read.get_playlist_files(playlist) 
            current_path = self.read.get_current_file(playlist)['current_audio_path']
        return SecondModel(data, self.current_audio_playlist_index(data, current_path))
        
    def show_current_data(self):
        if self.read.get_variable('current skin', 'default') != 'default':
            if self.audio_playlist_window_is_open:
                self.alternative_playlist()
        else:
            if self.read.get_variable('virtual playlist', False):
                self.parent.playlistName.setText(self.read.get_variable("virtual playlist").capitalize() + " Playlist") 
            else:
                self.parent.playlistName.setText(self.read.get_variable("current playlist").capitalize() + " Playlist") 
            
            connect = False if self.table_model is not None else True  
            self.table_model = self.get_audio_list_model()
            self.parent.playlistTable.setModel(self.table_model)
                
            if connect and self.table_model is not None:
                self.parent.playlistTable.setColumnWidth(0, 20)
                self.parent.playlistTable.setColumnWidth(1, 158)
                self.parent.playlistTable.setColumnWidth(2, 158)
                self.parent.playlistTable.setColumnWidth(3, 158)
                self.parent.playlistTable.doubleClicked.connect(self.__open_selected_decider__)
            
    def __open_selected_decider__(self):
        selected = self.get_selected_item()
        if selected is not None:
            self.__open_selected_audio__(selected[0], selected[1])
        
        
    def __open_selected_audio__(self, playlist=None, path=None): 
        if playlist is None:
            if self.read.get_variable('virtual playlist', False):
                playlist = self.read.get_variable("virtual playlist") 
                self.create.create_variable('virtual playing path', path)
            else:
                playlist = self.read.get_variable("current playlist") 
        if playlist is not None and path is not None:
            self.play_audio.emit(playlist, path, 0)
            
        
    def get_selected_item(self):
        selected_indexes = self.parent.playlistTable.selectionModel().selectedIndexes()
        if selected_indexes:
            selected_rows = [index.row() for index in selected_indexes]
            if selected_rows is not None:
                path = self.table_model.data[selected_rows[0]][4]  ### Each row has path data at index 4
                if self.read.get_variable('virtual playlist', False):
                    playlist = self.read.get_variable("virtual playlist") 
                    self.create.create_variable('virtual playing path', path)
                else:
                    playlist = self.read.get_variable("current playlist") 
                return playlist, path
            else:
                return None
        else:
            return None
        
        
        
        
        
        
        
        
        
    def  alternative_playlist(self):
        self.audio_playlist_window = ShowList(self.parent, self.get_audio_list_model, {'row':0, 'col':4, 'mode':'audio'}, self.get_file)
        self.parent.destroyed.connect(self.audio_playlist_window.deleteLater)
        self.audio_playlist_window.back.setText("Close")
        self.audio_playlist_window.load.setText("Play")
        self.audio_playlist_window.renameItem.setHidden(True)
        self.audio_playlist_window.destroyed.connect(self.alternative_playlist_destroyed)
        self.audio_playlist_window.remove_item_signal.connect(lambda path: self.remove_selected_item((None, path)))
        self.audio_playlist_window.selected_item.connect(lambda path: self.__open_selected_audio__(path=path))
        self.audio_playlist_window.setWindowTitle("BE Next Step: Audio Playlist")
        self.audio_playlist_window_is_open = True
        
    def alternative_playlist_destroyed(self):
        self.audio_playlist_window_is_open = False
        
        
        
        
        
    def remove_selected_item(self, selected):
        if selected is not None and not self.read.get_variable('virtual playlist', False):
            if selected[0] is None:
                selected = (self.read.get_variable("current playlist"), selected[1])
            playlist_details = self.read.get_playlistname_attr(selected[0])
            if playlist_details['current_audio_path']==selected[1]:
                if playlist_details['files_counter'] > 1:
                    self.play_next.emit(False) ## False arguments disables saving of data when next is pressed
                else:
                    self.update_db.update_current_audio(selected[0], None, 0)
                    self.stop_audio.emit() 
                    
            self.update_db.remove_audio(selected[0], selected[1])
            self.update_db.update_files_counter(selected[0])
            self.show_current_data()
            
    def clear_playlist(self):
        playlist = self.read.get_variable('current playlist')
        self.yes_no_window = YesNo(self.parent.geometry().x()+50, self.parent.geometry().y()+80)
        self.parent.destroyed.connect(self.yes_no_window.deleteLater)
        self.yes_no_window.yes_signal.connect(lambda: self.update_db.clear_playlist(playlist)) 
        self.yes_no_window.yes_signal.connect(self.show_current_data) 
        self.yes_no_window.yes_signal.connect(self.stop_audio.emit) 
        self.yes_no_window.promptText.setText(f"Do you want to remove all items from \"{playlist.capitalize()}\" Playlist?")
        self.yes_no_window.setWindowTitle("BE Next Step: Clear Playlist")
        
    def delete_playlist(self):
        playlist = self.read.get_variable('current playlist')
        self.yes_no_window = YesNo(self.parent.geometry().x()+50, self.parent.geometry().y()+80)
        self.parent.destroyed.connect(self.yes_no_window.deleteLater)
        self.yes_no_window.yes_signal.connect(lambda: self.update_db.remove_playlist(playlist)) 
        self.yes_no_window.yes_signal.connect(self.show_current_data) 
        self.yes_no_window.yes_signal.connect(self.stop_audio.emit) 
        self.yes_no_window.promptText.setText(f"Do you want to delete \"{playlist.capitalize()}\" Playlist?")
        self.yes_no_window.setWindowTitle("BE Next Step: Delete Playlist")
        
        
        
        
        
        