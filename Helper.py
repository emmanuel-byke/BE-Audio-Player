import os, psutil
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPixmap
from read_db import Read
from create_update_db import Create
from update_db import Update
import threading
from PyQt6.QtGui import QGuiApplication
from settings import Constants

def app_is_running():
        counter = 0
        for app in psutil.process_iter():
            if app.name().lower() == "be_audio_player.exe":
                counter += 1
            if counter > 1:
                return True
        return False
    
def get_widget_coordinates(parent_geo, obj_geo, position='center'):
    parent_x, parent_y, parent_width, parent_height = parent_geo.x(), parent_geo.y(), parent_geo.width(), parent_geo.height()
    obj_width, obj_height = obj_geo.width(), obj_geo.height()
    
    screen = QGuiApplication.primaryScreen()
    screen = screen.availableGeometry()
    screen_width, screen_height = screen.width(), screen.height()
    
    y_value = int(parent_y+parent_height-obj_height+parent_height)
    y_value = 0 if y_value < 0 else (screen_height-obj_height) if (y_value+obj_height) > screen_height else y_value
    if position=='center': 
        x_value = int(parent_x+parent_width-obj_width+parent_width/8)
        x_value = -50 if x_value < -50 else (screen_width-obj_width+50) if (x_value+obj_width) > screen_width+50 else x_value
    elif position=='side':
        x_value = parent_x+parent_width if parent_x+parent_width < screen_width-obj_width else parent_x-obj_width if parent_x-obj_width > 0 else parent_x
    else:
        x_value = parent_x
        y_value = parent_y
    
    return x_value, y_value, obj_width, obj_height
    
def get_cwd():
    # return os.getcwd().replace("\\", "/")
    path = os.path.abspath(__file__).replace("\\", "/")
    return path[:path.rfind("/")]

def res():
    # return os.getcwd().replace("\\", "/")
    path = os.path.abspath(__file__).replace("\\", "/")
    return path[:path.rfind("/")] + "/res"

def user_folder(path=""):
    return os.path.expanduser("~").replace("\\", "/") + path

def temp_folder(subdir=''):
    path = user_folder() + "/AppData/Local/BE Next Step/Player" + subdir
    os.makedirs(path, exist_ok=True)
    return path

def set_label_pixmap(label, pic_data, local_file=False):
    if pic_data is None:
        pixmap = QPixmap(res()+"/Images/red_gray_flower.jpg")
    elif local_file:
        pixmap = QPixmap(pic_data)
    else:
        pixmap = QPixmap()
        pixmap.loadFromData(pic_data)
    label.setPixmap(pixmap)
    
def retrive_current_audio_property(prop):
    read = Read()
    try: # you can also check if each prop searched is inside the array returned by db
        details = read.get_current_file(read.get_variable('current playlist'))
        if len(details) > 0:
            name = read.get_variable('current playlist')
            path = details['current_audio_path']
            
            prop = read.get_playlist_file_details(read.get_variable('current playlist'), details['current_audio_path'])[prop]
            return details['playlist_name'], details['current_audio_path'], prop
        else:
            return None, None, None
    except:
        return None, None, None
    
def retrive_current_playlist_property(prop):
    read = Read()
    try: # you can also check if each prop searched is inside the array returned by db
        details = read.get_current_file(read.get_variable('current playlist'), [])
        if len(details) > 0:
            return details['playlist_name'], details[prop]
        else:
            return None, None
    except:
        return None, None
    
def create_important_variables():
    read = Read()
    create = Create()
    if read.get_variable("current playlist", None) is None:
        create.create_variable("current playlist", "local")
    create.create_variable("Shuffle", False)
    create.create_variable("virtual playlist", False)
    
    if read.get_variable("current skin") is None:
        create.create_variable("current skin", "Simple")
    
    default_skin_colors(create, read)
        
def default_skin_colors(create, read):
    if read.get_variable("simple color 1") is None:
        create.create_variable("simple color 1", "rgb(13, 10, 5)")
    if read.get_variable("simple color 2") is None:
        create.create_variable("simple color 2", "rgb(12, 12, 12)")
    if read.get_variable("simple color 3") is None:
        create.create_variable("simple color 3", "rgb(0, 0, 0)")
    if read.get_variable("simple color 4") is None:
        create.create_variable("simple color 4", "rgb(0, 0, 0)")
    if read.get_variable("simple color 5") is None:
        create.create_variable("simple color 5", "rgb(12, 12, 12)")
    if read.get_variable("simple color 6") is None:
        create.create_variable("simple color 6", "rgb(13, 10, 5)")
    if read.get_variable("simple border color") is None:
        create.create_variable("simple border color", "#1FFF6B")
    if read.get_variable("simple lcd color") is None:
        create.create_variable("simple lcd color", "#1FFF6B")
    if read.get_variable("simple label color") is None:
        create.create_variable("simple label color", "#1FFF6B")
    if read.get_variable("simple progress groove color 1") is None:
        create.create_variable("simple progress groove color 1", "rgb(81, 83, 84)")
    if read.get_variable("simple progress groove color 2") is None:
        create.create_variable("simple progress groove color 2", "rgb(50, 52, 61)")
    if read.get_variable("simple progress groove border color") is None:
        create.create_variable("simple progress groove border color", "#bbb")
    if read.get_variable("simple progress handle color 1") is None:
        create.create_variable("simple progress handle color 1", "#EEE")
    if read.get_variable("simple progress handle color 2") is None:
        create.create_variable("simple progress handle color 2", "#999")
    if read.get_variable("simple progress sub-page color 1") is None:
        create.create_variable("simple progress sub-page color 1", "rgb(252, 255, 253)")
    if read.get_variable("simple progress sub-page color 2") is None:
        create.create_variable("simple progress sub-page color 2", "rgba(26, 210, 89, 255)")
    if read.get_variable("simple progress sub-page background color") is None:
        create.create_variable("simple progress sub-page background color", "gray")
    if read.get_variable("simple mask-label color") is None:
        create.create_variable("simple mask-label color", "rgb(36, 36, 48)")
    if read.get_variable("simple btn color") is None:
        create.create_variable("simple btn color", "#1FFF6B")
    
    if read.get_variable("rounded-bar color 1") is None:
        create.create_variable("rounded-bar color 1", "#E5EEF8")
    if read.get_variable("rounded-bar color 2") is None:
        create.create_variable("rounded-bar color 2", "#287AD1")
    if read.get_variable("rounded bar progress groove color 1") is None:
        create.create_variable("rounded bar progress groove color 1", "#B1B1B1")
    if read.get_variable("rounded bar progress groove color 2") is None:
        create.create_variable("rounded bar progress groove color 2", "#c4c4c4")
    if read.get_variable("rounded bar progress groove border color") is None:
        create.create_variable("rounded bar progress groove border color", "#999999")
    if read.get_variable("rounded bar progress handle color 1") is None:
        create.create_variable("rounded bar progress handle color 1", "#ffdfce")
    if read.get_variable("rounded bar progress handle color 2") is None:
        create.create_variable("rounded bar progress handle color 2", "#ff9a9a")
    if read.get_variable("rounded bar btn color") is None:
        create.create_variable("rounded bar btn color", "#287AD1")
    
    if read.get_variable("one button label color") is None:
        create.create_variable("one button label color", "#1FFF6B")
    if read.get_variable("one button mask-label color") is None:
        create.create_variable("one button mask-label color", "rgb(36, 36, 48)")
    if read.get_variable("one button btn color") is None:
        create.create_variable("one button btn color", "#FF3647")
    if read.get_variable("one button progress groove color 1") is None:
        create.create_variable("one button progress groove color 1", "rgb(81, 83, 84)")
    if read.get_variable("one button progress groove color 2") is None:
        create.create_variable("one button progress groove color 2", "rgb(50, 52, 61)")
    if read.get_variable("one button progress groove border color") is None:
        create.create_variable("one button progress groove border color", "#bbb")
    if read.get_variable("one button progress handle color 1") is None:
        create.create_variable("one button progress handle color 1", "#EEE")
    if read.get_variable("one button progress handle color 2") is None:
        create.create_variable("one button progress handle color 2", "#999")
    if read.get_variable("one button progress sub-page color 1") is None:
        create.create_variable("one button progress sub-page color 1", "rgb(252, 255, 253)")
    if read.get_variable("one button progress sub-page color 2") is None:
        create.create_variable("one button progress sub-page color 2", "rgb(26, 210, 89)")
    if read.get_variable("one button progress sub-page background color") is None:
        create.create_variable("one button progress sub-page background color", "gray")
        
    if read.get_variable("default background color") is None:
        create.create_variable("default background color", "rgb(36, 36, 48)")

    
class Conversions:
    def from_seconds(self, seconds):
        seconds = round(seconds)
        m, s = divmod(seconds, 60)
        # h, m = divmod(m, 60)  ### removing hours
        # result = f"{self.add_zero(h)}:" if h>0 else ""
        # result += f"{self.add_zero(m)}:" if m>0 or h>0 else ""
        
        result = f"{self.add_zero(m)}:" if m>0 else ""
        result += self.add_zero(s)
        return result
    
    def from_milli(self, milli):
        return self.from_seconds(milli/1000)
    
    def add_zero(self, val):
        if val < 10:
            return f"0{val}"
        return f"{val}"
    
    def from_bytes(self, size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
    
class PositionCalculator():
    def __init__(self, start_time=0):
        self.start_time = self.start(start_time)
        self.difference = 0
        self.pause_time = 0
        self.pauseFirst = False
    
    def start(self, start):
        self.start_time = start
        
    def pause(self, pause_time):
        if not self.pauseFirst:
            self.pause_time = pause_time
            self.pauseFirst = True
        
    def play(self, play_time):
        if self.pauseFirst:
            self.difference += (self.pause_time - play_time)
            self.pauseFirst = False
        
    def get_pos(self, current):
        duration = (current - self.start_time) + self.difference
        return duration
    
class GetFile(QObject):
    play_signal = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.create = Create()
        self.read = Read()
        self.update_db = Update()    
        self.constants = Constants()   
         
    def get_allowed_formats(self)->list:
        audio_formats = self.constants.audio_formats()
        if self.read.get_variable('popular Video', True):
            audio_formats.extend(self.constants.video_formats()['popular'])
        if self.read.get_variable('un-popular Video', True):
            audio_formats.extend(self.constants.video_formats()['less_popular'])
        return audio_formats
    
    def join_string_in_list(self, arr):
        result = ''
        for d in arr:
            result += " "
            result += d
        return result
       
    def get_file_btn(self):
        folder = user_folder("/Music")
        try:
            if self.read.get_variable("virtual playlist", False):
                path = self.read.get_variable('virtual playing path')
            elif self.read.get_variable('current playlist', None) is not None:
                path = self.read.get_current_file(self.read.get_variable('current playlist'))['current_audio_path']
            folder = os.path.dirname(path)
        except:
            pass
        
        new_files = QFileDialog.getOpenFileNames(QMainWindow(), "Select File to Play", folder, 
                    self.join_string_in_list(["*."+d for d in self.get_allowed_formats()]))[0]
        self.add_to_playlist(new_files)
        
    def get_file_folder(self):
        folder = user_folder("/Music")
        try:
            if self.read.get_variable("virtual playlist", False):
                path = self.read.get_variable('virtual playing path')
            elif self.read.get_variable('current playlist', None) is not None:
                path = self.read.get_current_file(self.read.get_variable('current playlist'))['current_audio_path']
            folder = os.path.dirname(os.path.dirname(path))
        except:
            pass
        
        folder_path = QFileDialog.getExistingDirectory(QMainWindow(), "Select Folder", folder)
        if folder_path:
            self.add_to_playlist([folder_path])
        
    def get_file_drag(self, event):
        if event.mimeData().hasUrls():
            file_url = event.mimeData().urls()
            result = []
            for f in file_url:
                result.append(f.toLocalFile())
            self.add_to_playlist(result)
    
    def add_to_playlist(self, files_arr, initial_add=False):
        if len(files_arr) <= 0:
            return
        
        if self.read.get_variable("current playlist", None) is None:
            create_important_variables()
            
        audio_formats = self.get_allowed_formats()
            
        file_to_play = None
        playlist_created = False
        break_loops = False
        max_main_thread_files = 20
        for f in files_arr: 
            if break_loops:
                break
            if os.path.isdir(f):
                if len(files_arr) == 1:
                    playlist_name = os.path.basename(f).capitalize()
                    playlist_name = playlist_name if playlist_name.strip() != "" else self.read.get_variable("current playlist")
                    self.create.create_playlist_commons(playlist_name, is_shared=True, picture=None)
                    self.create.create_variable('current playlist', playlist_name)
                elif len(files_arr) > 1 and not playlist_created:
                    playlist_name = os.path.basename(os.path.dirname(f)).capitalize() 
                    playlist_name = playlist_name if playlist_name.strip() != "" else self.read.get_variable("current playlist")
                    self.create.create_playlist_commons(playlist_name, is_shared=True, picture=None)
                    self.create.create_variable('current playlist', playlist_name)
                    playlist_created = False
                    
                for root_, dirs, files in os.walk(f):
                    for files_ in files:
                        if files_[files_.rfind(".")+1:].lower() in audio_formats:
                            self.create.create_playlist(playlist_name, (root_ + "/" + files_))
                            if file_to_play is None:
                                file_to_play = (root_ + "/" + files_)
                                self.update_db.update_current_audio(playlist_name, (root_ + "/" + files_), 0)
                                if not initial_add:    
                                    self.play_signal.emit(True)
                                if len(files_arr) > max_main_thread_files or len(files) > max_main_thread_files: 
                                    worker_thread = threading.Thread(target=lambda: self.add_file_thread(files_arr, (root_ + "/" + files_), playlist_name, audio_formats))
                                    worker_thread.start()
                                    break_loops = True
                                    break
                    if break_loops:
                        break
            else:
                if f[f.rfind(".")+1:].lower() in audio_formats:
                    self.create.create_playlist(self.read.get_variable("current playlist"), f)
                    if file_to_play is None:
                        file_to_play = f
                        self.update_db.update_current_audio(self.read.get_variable("current playlist"), f, 0)
                        if not initial_add:
                            self.play_signal.emit(True)
                        if len(files_arr)>max_main_thread_files:
                            worker_thread = threading.Thread(target=lambda: self.add_file_thread(files_arr, f, self.read.get_variable("current playlist"), audio_formats))
                            worker_thread.start()    
                            break_loops = True                    
                            break
                    
        if initial_add and len(files_arr) > 0: ### it should be done after loops to avoid loading wrong audio
            self.create.create_variable("file clicked", True)
                    
        if not break_loops and not initial_add:
            self.play_signal.emit(False)
                    
    def add_file_thread(self, files_arr, file_to_play, playlist_name, audio_formats):
        if len(files_arr) > 0:
            for f in files_arr:
                if os.path.isdir(f):
                    for root_, dirs, files in os.walk(f):
                        for files_ in files:
                            if len(files) > 0 and files_ != file_to_play and files_[files_.rfind(".")+1:].lower() in audio_formats:
                                self.create.create_playlist(playlist_name, (root_ + "/" + files_))                                
                else:
                    if f[f.rfind(".")+1:].lower() in audio_formats and f != file_to_play:
                        self.create.create_playlist(playlist_name, f)
        update_db = Update()   
        update_db.update_silence()
                    
                
        
    # def read_from_playlist(self, playlistname=None):
    #     if playlistname is not None:
    #         return self.read.get_playlistname_attr(playlistname)
        
    # def get_save_path(self, path="", extensions=""):
    #     file_path = os.path.expanduser("~").replace("\\", "/") + path
    #     result = QFileDialog.getSaveFileName(self, "Save playlist", file_path, f" (*{extensions})")
    #     return result


class DefaultVariables():
    
    def logo(self):
        path = res() + "/Labels/"
        return {
            'Logo 1': path + "cooltext441067353539699.png",
            'Logo 2': path + "cooltext441067491928042.png",
            'Logo 3': path + "cooltext441067566572119.png",
            'Logo 4': path + "cooltext441067602838032.png",
            'Logo 5': path + "cooltext441067678798419.png",
        }    
            
class Settings:
    def __init__(self, parent, remover):
        self.parent = parent
        self.remover = remover
        self.create = Create()
        self.read = Read()
        self.binding()
        self.load_settings()
        self.update_header_logo()
                
    def binding(self):
        self.parent.settingsRemoveCurrent.clicked.connect(self.remove_current_audio)
        self.parent.settingsRemoveUnavailable.clicked.connect(self.remove_unavailable_audio)
        self.parent.settingsAddAll.clicked.connect(self.add_all)
        self.parent.settingsReset.clicked.connect(self.reset)
        self.parent.settingsChangeBackground.clicked.connect(self.change_bg)
        self.parent.settingsChangeSkin.clicked.connect(self.change_skin)
        self.parent.settingBackBtn.clicked.connect(self.open_defaults)
        self.parent.settingsAddLastItem.clicked.connect(lambda checked: self.create.create_variable("Adding Files", "Last"))
        self.parent.settingsAddFistItem.clicked.connect(lambda checked: self.create.create_variable("Adding Files", "First"))
        self.parent.settingsPlayFromPlaylist.clicked.connect(lambda checked: self.create.create_variable("Adding Files", "Playlist"))
        self.parent.settingsClearList.clicked.connect(lambda checked: self.create.create_variable("Adding Files", "Clear"))
        self.parent.settingsWaitCurrentAudio.clicked.connect(lambda checked: self.create.create_variable("Wait Current Audio", checked))
        self.parent.settingsSortPlaylist.clicked.connect(lambda checked: self.create.create_variable("Auto Sort", checked))
        self.parent.settingsSortFileName.clicked.connect(lambda checked: self.create.create_variable("Sortby", "File Name"))
        self.parent.settingsSortTitle.clicked.connect(lambda checked: self.create.create_variable("Sortby", "Title"))
        self.parent.settingsSortArtist.clicked.connect(lambda checked: self.create.create_variable("Sortby", "Artist"))
        self.parent.settingsSortAlbum.clicked.connect(lambda checked: self.create.create_variable("Sortby", "Album"))
        self.parent.settingsSortPath.clicked.connect(lambda checked: self.create.create_variable("Sortby", "Path"))
        self.parent.settingsSortSize.clicked.connect(lambda checked: self.create.create_variable("Sortby", "Size"))
        self.parent.settingsSortDuration.clicked.connect(lambda checked: self.create.create_variable("Sortby", "Duration"))
        self.parent.settingSortDescending.clicked.connect(lambda checked: self.create.create_variable("Descending", checked))
        self.parent.settingsFilterSmall.clicked.connect(lambda checked: self.create.create_variable("filter", checked))
        self.parent.settingsAutoLoad.clicked.connect(lambda checked: self.create.create_variable("Auto Load", checked))
        self.parent.settingsFadeIn.clicked.connect(lambda checked: self.create.create_variable("FadeIn", checked))
        self.parent.settingsFadeInSpin.valueChanged.connect(lambda value: self.create.create_variable("FadeIn Time", value))
        self.parent.settingsFadeOut.clicked.connect(lambda checked: self.create.create_variable("FadeOut", checked))
        self.parent.settingsFadeOutSpin.valueChanged.connect(lambda value: self.create.create_variable("FadeOut Time", value))
        self.parent.settingsIncreaseSpeed.clicked.connect(lambda checked: self.create.create_variable("Increase Speed", checked))
        self.parent.settingsIncreaseSpeedSpin.valueChanged.connect(lambda value: self.create.create_variable("Increase Speed Time", value))
        self.parent.settingsReduceSpeed.clicked.connect(lambda checked: self.create.create_variable("Reduce Speed", checked))
        self.parent.settingsReduceSpeedSpin.valueChanged.connect(lambda value: self.create.create_variable("Reduce Speed Time", value))
        self.parent.settingsEndForceLoop.clicked.connect(lambda checked: self.create.create_variable("End Loop", "Loop"))
        self.parent.settingsEndLoopRules.clicked.connect(lambda checked: self.create.create_variable("End Loop", "Normal"))
        self.parent.settingsShuffleForceLoop.clicked.connect(lambda checked: self.create.create_variable("Shuffle Loop", "Loop"))
        self.parent.settingsShuffleLoopRules.clicked.connect(lambda checked: self.create.create_variable("Shuffle Loop", "Normal"))
        self.parent.settingsShowVisualizer.clicked.connect(lambda checked: self.create.create_variable("Show Visualizer", checked))
        self.parent.settingsShowControls.clicked.connect(lambda checked: self.create.create_variable("Show Controls", checked))
        self.parent.settingsShowVolumeControl.clicked.connect(lambda checked: self.create.create_variable("Show Volume Controls", checked))
        self.parent.settingsShowSeek.clicked.connect(lambda checked: self.create.create_variable("Show Seek", checked))
        self.parent.settingsShowVolumeControl.clicked.connect(self.disable_move_seek)
        self.parent.settingsShowSeek.clicked.connect(self.disable_move_seek)
        self.parent.settingsMoveSeekDown.clicked.connect(lambda checked: self.create.create_variable("Move Seek", checked))
        self.parent.settingsShowAudioSelector.clicked.connect(lambda checked: self.create.create_variable("Show Audio Selector", checked))
        self.parent.settingsShowHeader.clicked.connect(lambda checked: self.create.create_variable("Show Header", checked))
        self.parent.settingsShowHeader.clicked.connect(self.update_header_logo)
        self.parent.settingsRoundCorners.clicked.connect(lambda checked: self.create.create_variable("Round Corner", checked))
        
        self.parent.logoCombobox.currentIndexChanged.connect(self.change_header_logo_handler)
        
    def change_header_logo_handler(self):
        self.create.create_variable("logo", self.parent.logoCombobox.currentText())
        self.update_header_logo()
        
    def update_header_logo(self):
        logo_paths = DefaultVariables().logo()
        logo_name = self.read.get_variable("logo", 'Logo 1')
        self.parent.appName.setPixmap(QPixmap(logo_paths[logo_name]))
        self.parent.logoCombobox.setCurrentText(logo_name)
        self.parent.logoCombobox.setHidden(not self.read.get_variable("Show Header", True))
        

    def remove_all(self):
        self.remover.removeVisualizerFrame()
        self.remover.removeSettingsFrame()
        self.remover.removeVolControlFrame()
        self.remover.removeVolControlFrameAlt()
        self.remover.removeThreeAudioFrame()
        self.remover.removeHeaderFrame()
        self.remover.removeHeaderFrameAlt()
        self.remover.removeLoginFrame()
        self.remover.removeRegisterFrame()
        self.remover.removeSeekFrameNew()
        self.remover.removePlaylistFrame()
        self.remover.removeControlFrame()
        self.remover.removeOtherSkinItems()
        
    def open_settings(self):
        if self.read.get_variable('current skin')=='default':
            self.remove_all()
            self.remover.removeHeaderFrameAlt(True)
            self.remover.removeSettingsFrame(True)
            self.remover.removeSeekFrameNew(True)
            self.remover.removeControlFrame(True)
        
    def open_login(self):
        if self.read.get_variable('current skin')=='default':
            self.remove_all()
            self.remover.removeHeaderFrameAlt(True)
            self.remover.removeLoginFrame(True)
            self.remover.removeSeekFrameNew(True)
            self.remover.removeControlFrame(True)
        
    def open_register(self):
        if self.read.get_variable('current skin')=='default':
            self.remove_all()
            self.remover.removeRegisterFrame(True)
            self.remover.removeHeaderFrameAlt(True)
            self.remover.removeSeekFrameNew(True)
            self.remover.removeControlFrame(True)
        
    def open_playlist(self):
        if self.read.get_variable('current skin')=='default':
            self.remove_all()
            self.remover.removePlaylistFrame(True)
            self.remover.removeHeaderFrameAlt(True)
            self.remover.removeSeekFrameNew(True)
            self.remover.removeControlFrame(True)
        
    def open_defaults(self):
        self.remove_all()
        self.seek_decider()
        self.remover.removeVisualizerFrame(self.read.get_variable("Show Visualizer", True))
        self.remover.removeVolControlFrame(self.read.get_variable("Show Volume Controls", True))
        self.remover.removeVolControlFrameAlt(True)
        self.remover.removeThreeAudioFrame(self.read.get_variable("Show Audio Selector", True))
        self.remover.removePlaylistFrame(self.read.get_variable("playlist", False))
        self.remover.removeHeaderFrame(self.read.get_variable("Show Header", True))
        self.remover.removeHeaderFrameAlt(not self.read.get_variable("Show Header", True))
        self.remover.removeControlFrame(self.read.get_variable("Show Controls", True))
        
    def seek_decider(self):
        if self.read.get_variable("Show Seek", True):
            if self.read.get_variable("Move Seek", False):
                if not self.read.get_variable("Show Volume Controls", True):
                    self.remover.removeSeekFrameNew(True)
                    return
            else:
                self.remover.removeSeekFrame(True)
                return
        self.remover.removeSeekFrame()
        
    def disable_move_seek(self):
        self.parent.settingsMoveSeekDown.setDisabled(
            self.read.get_variable("Show Volume Controls", True) or not self.read.get_variable("Show Seek", True)
        )
        
    def set_skin(self, skin, name):
        self.create.create_variable('current skin', name)
        self.remove_all()
        self.remover.removeHeaderFrameForce()
        
        if name=='default':
            self.open_defaults()
        elif name=='One Button':
            self.remover.restore_one_btn_skin()
        elif name == "Rounded Bar":
            self.remover.restore_rounded_bar_skin()
        elif name == "Simple":
            self.remover.restore_simple_skin()
        skin.set_skin(name)
        
        
        
    def load_settings(self):
        self.parent.settingsAddLastItem.setChecked(self.read.get_variable("Adding Files", "Playlist")=="Last")
        self.parent.settingsAddFistItem.setChecked(self.read.get_variable("Adding Files", "Playlist")=="First")
        self.parent.settingsPlayFromPlaylist.setChecked(self.read.get_variable("Adding Files", "Playlist")=="Playlist")
        self.parent.settingsClearList.setChecked(self.read.get_variable("Adding Files", "Playlist")=="Clear")
        self.parent.settingsSortFileName.setChecked(self.read.get_variable("Sortby", False)=='File Name')
        self.parent.settingsSortTitle.setChecked(self.read.get_variable("Sortby", False)=='Title')
        self.parent.settingsSortArtist.setChecked(self.read.get_variable("Sortby", False)=='Artist')
        self.parent.settingsSortAlbum.setChecked(self.read.get_variable("Sortby", False)=='Album')
        self.parent.settingsSortPath.setChecked(self.read.get_variable("Sortby", False)=='Path')
        self.parent.settingsSortSize.setChecked(self.read.get_variable("Sortby", False)=='Size')
        self.parent.settingsSortDuration.setChecked(self.read.get_variable("Sortby", False)=='Duration')
        self.parent.settingsEndForceLoop.setChecked(self.read.get_variable("End Loop", False))
        self.parent.settingsEndLoopRules.setChecked(self.read.get_variable("End Loop", True))
        self.parent.settingsShuffleForceLoop.setChecked(self.read.get_variable("Shuffle Loop", True))
        self.parent.settingsShuffleLoopRules.setChecked(self.read.get_variable("Shuffle Loop", False))
        self.parent.settingSortDescending.setChecked(self.read.get_variable("Sort Descending Order", False))
        self.parent.settingsWaitCurrentAudio.setChecked(self.read.get_variable("Wait Current Audio", False))
        self.parent.settingsSortPlaylist.setChecked(self.read.get_variable("Auto Sort", True))
        self.parent.settingsFilterSmall.setChecked(self.read.get_variable("Filter Small", True))
        self.parent.settingsAutoLoad.setChecked(self.read.get_variable("Auto Load", True))
        self.parent.settingsFadeIn.setChecked(self.read.get_variable("FadeIn", False))
        self.parent.settingsFadeOut.setChecked(self.read.get_variable("FadeOut", False))
        self.parent.settingsIncreaseSpeed.setChecked(self.read.get_variable("Increase Speed", False))
        self.parent.settingsReduceSpeed.setChecked(self.read.get_variable("Reduce Speed", False))
        self.parent.settingsShowVisualizer.setChecked(self.read.get_variable("Show Visualizer", True))
        self.parent.settingsShowControls.setChecked(self.read.get_variable("Show Controls", True))
        self.parent.settingsShowVolumeControl.setChecked(self.read.get_variable("Show Volume Controls", True))
        self.parent.settingsShowSeek.setChecked(self.read.get_variable("Show Seek", True))
        self.parent.settingsMoveSeekDown.setChecked(self.read.get_variable("Move Seek", False))
        self.parent.settingsRoundCorners.setChecked(self.read.get_variable("Round Corner", True))
        self.parent.settingsShowAudioSelector.setChecked(self.read.get_variable("Show Audio Selector", True))
        self.parent.settingsShowHeader.setChecked(self.read.get_variable("Show Header", True))
    
    def remove_current_audio(self):
        pass
    def remove_unavailable_audio(self):
        pass
    def add_all(self):
        pass
    def reset(self):
        pass
    def change_bg(self):
        pass
    def change_skin(self):
        pass
    
        
   
        
    