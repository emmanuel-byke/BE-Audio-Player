from PyQt6.QtCore import QObject, pyqtSignal
from Helper import set_label_pixmap, res, Conversions
from read_db import Read
from create_update_db import Create
from update_db import Update
from AudioMetadata import ExtractMetadata

class Customize(QObject):
    play_signal = pyqtSignal(bool)
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.rotation_angle = 0
        self.read = Read()
        self.create = Create()
        self.update_db = Update()
        self.playlist_tmp = []
        self.support_playlist_middle_index = 0
        self.support_playlist_middle_index_tmp = 0
        self.middle_item_index = 0
        self.support_playlistLabels= [
            self.parent.supportPlaylistItem1,
            self.parent.supportPlaylistItem2,
            self.parent.supportPlaylistItem3,
            self.parent.supportPlaylistItem4,
            self.parent.supportPlaylistItem5,
            self.parent.supportPlaylistItem6,
            self.parent.supportPlaylistItem7,
        ]
        
        self.playlist_items = [
            self.parent.firstAudio,
            self.parent.secondAudio,
            self.parent.thirdAudio,
        ]
        self.parent.nextList.clicked.connect(self.next_list_handler)
        self.parent.prevList.clicked.connect(self.prev_list_handler)
        self.conversions = Conversions()
        
        self.support_playlistLabels[0].mouseDoubleClickEvent = self.support_playlist_handler0
        self.support_playlistLabels[1].mouseDoubleClickEvent = self.support_playlist_handler1
        self.support_playlistLabels[2].mouseDoubleClickEvent = self.support_playlist_handler2
        self.support_playlistLabels[3].mouseDoubleClickEvent = self.support_playlist_handler3
        self.support_playlistLabels[4].mouseDoubleClickEvent = self.support_playlist_handler4
        self.support_playlistLabels[5].mouseDoubleClickEvent = self.support_playlist_handler5
        self.support_playlistLabels[6].mouseDoubleClickEvent = self.support_playlist_handler6
        
        self.default_pic = self.read.get_variable("Default Audio Artwork", None)
        if self.default_pic is None:
            self.default_pic = f"{res()}/Images/compact-disk-free-png.png"
            self.create.create_variable("Default Audio Artwork", self.default_pic)
            
        self.bind()
        
        
        self.support_playlist_decider() 
        self.main_playlist_decider()
        
    def bind(self):
        if self.read.get_variable('single click', False):
            self.parent.firstAudio.mousePressEvent = self.first_frame
            self.parent.secondAudio.mousePressEvent = self.second_frame
            self.parent.thirdAudio.mousePressEvent = self.third_frame
        else:
            self.parent.firstAudio.mouseDoubleClickEvent = self.first_frame
            self.parent.secondAudio.mouseDoubleClickEvent = self.second_frame
            self.parent.thirdAudio.mouseDoubleClickEvent = self.third_frame 
        
    def load_defaults(self):
        self.parent.fArtist.setText("")
        self.parent.fTitle.setText("")
        set_label_pixmap(self.parent.fPic, self.default_pic, True)
        self.parent.sArtist.setText("")
        self.parent.sTitle.setText("")
        set_label_pixmap(self.parent.sPic, self.default_pic, True)
        self.parent.tArtist.setText("")
        self.parent.tTitle.setText("")
        set_label_pixmap(self.parent.tPic, self.default_pic, True)
        
    def first_frame(self, event):
        calc_index = self.middle_item_index-1
        self.play_audio(self.playlist_tmp[calc_index]['path'], self.playlist_tmp[calc_index]['playlist_name'])
        
    def second_frame(self, event):
        calc_index = self.middle_item_index
        self.play_audio(self.playlist_tmp[calc_index]['path'], self.playlist_tmp[calc_index]['playlist_name'])
        
    def third_frame(self, event):
        calc_index = self.middle_item_index+1
        self.play_audio(self.playlist_tmp[calc_index]['path'], self.playlist_tmp[calc_index]['playlist_name'])
        
    def main_playlist_decider(self):
        playlist = self.read.get_playlist_files(self.read.get_variable('current playlist'))
        self.playlist_tmp = playlist
        current_audio = self.read.get_current_file(self.read.get_variable('current playlist'))
                
        self.middle_item_index = self.current_audio_index(current_audio, playlist)
        if self.middle_item_index >= 0:
            if self.middle_item_index-1 > 0:
                self.main_playlist_writer(self.parent.fTitle, self.parent.fArtist, self.parent.fPic, playlist[self.middle_item_index-1])
                
            if self.middle_item_index > 0:
                self.main_playlist_writer(self.parent.sTitle, self.parent.sArtist, self.parent.sPic, playlist[self.middle_item_index])
                
            if self.middle_item_index+1 < len(playlist):
                self.main_playlist_writer(self.parent.tTitle, self.parent.tArtist, self.parent.tPic, playlist[self.middle_item_index+1])
                
    def main_playlist_writer(self, title_label, artist_label, pic_label, playlist_details=None):
        if playlist_details is not None:
            title_label.setHidden(False)
            artist_label.setHidden(False)
            pic_label.setHidden(False)
            metadata = ExtractMetadata(playlist_details['path'])
            set_label_pixmap(pic_label, metadata.get_artwork(), local_file=False)
            pic_label.setToolTip("File Name: {}\nTitle: {}\nArtist: {}\nAlbum: {}\nDuration: {}\nFile Type: {}".format(playlist_details['filename'],
                playlist_details['title'], playlist_details['artist'], playlist_details['album'], self.conversions.from_milli(float(playlist_details['duration'])), playlist_details['extension']))            
            artist_label.setText(playlist_details['artist'])
            title_label.setText(playlist_details['title'])
        else:
            title_label.setHidden(True)
            artist_label.setHidden(True)
            pic_label.setHidden(True)
            
    def support_playlist_decider(self):
        playlist = self.read.get_playlist_files(self.read.get_variable('current playlist'))
        self.playlist_tmp = playlist
        current_audio = self.read.get_current_file(self.read.get_variable('current playlist'))
                
        self.support_playlist_middle_index = self.current_audio_index(current_audio, playlist)
        if self.support_playlist_middle_index >= 0:
            for i, label in enumerate(self.support_playlistLabels):
                calc_index = self.support_playlist_middle_index + i - 3 + self.support_playlist_middle_index_tmp
                if ((calc_index >= 0) and (calc_index < len(playlist))):
                    self.support_playlist_writer(label, playlist[calc_index])
                else:
                    self.support_playlist_writer(label, None)  ###  hide labels with no audio
        
    def support_playlist_writer(self, label, playlist_details=None):
        if playlist_details is not None:
            label.setHidden(False)
            metadata = ExtractMetadata(playlist_details['path'])
            set_label_pixmap(label, metadata.get_artwork(), local_file=False)
            label.setToolTip("File Name: {}\nTitle: {}\nArtist: {}\nAlbum: {}\nDuration: {}\nFile Type: {}".format(playlist_details['filename'],
                playlist_details['title'], playlist_details['artist'], playlist_details['album'], self.conversions.from_milli(float(playlist_details['duration'])), playlist_details['extension']))            
        else:
            label.setHidden(True)
        
    def support_playlist_handler0(self, event):
        calc_index = self.support_playlist_middle_index + self.support_playlist_middle_index_tmp + 0 - 3
        self.play_audio(self.playlist_tmp[calc_index]['path'], self.playlist_tmp[calc_index]['playlist_name'])
        
    def support_playlist_handler1(self, event):
        calc_index = self.support_playlist_middle_index + self.support_playlist_middle_index_tmp + 1 - 3
        self.play_audio(self.playlist_tmp[calc_index]['path'], self.playlist_tmp[calc_index]['playlist_name'])
        
    def support_playlist_handler2(self, event):
        calc_index = self.support_playlist_middle_index + self.support_playlist_middle_index_tmp + 2 - 3
        self.play_audio(self.playlist_tmp[calc_index]['path'], self.playlist_tmp[calc_index]['playlist_name'])
        
    def support_playlist_handler3(self, event):
        calc_index = self.support_playlist_middle_index + self.support_playlist_middle_index_tmp + 3 - 3
        self.play_audio(self.playlist_tmp[calc_index]['path'], self.playlist_tmp[calc_index]['playlist_name'])
        
    def support_playlist_handler4(self, event):
        calc_index = self.support_playlist_middle_index + self.support_playlist_middle_index_tmp + 4 - 3
        self.play_audio(self.playlist_tmp[calc_index]['path'], self.playlist_tmp[calc_index]['playlist_name'])
        
    def support_playlist_handler5(self, event):
        calc_index = self.support_playlist_middle_index + self.support_playlist_middle_index_tmp + 5 - 3
        self.play_audio(self.playlist_tmp[calc_index]['path'], self.playlist_tmp[calc_index]['playlist_name'])
        
    def support_playlist_handler6(self, event):
        calc_index = self.support_playlist_middle_index + self.support_playlist_middle_index_tmp + 6 - 3
        self.play_audio(self.playlist_tmp[calc_index]['path'], self.playlist_tmp[calc_index]['playlist_name'])
        
    def play_audio(self, path, playlist_name):
        self.create.create_variable("current playlist", playlist_name)
        self.update_db.update_current_audio(playlist_name, path, 0)        
        self.play_signal.emit(True)
        self.support_playlist_middle_index_tmp = 0
        self.support_playlist_decider()
        
    def next_list_handler(self):
        if self.support_playlist_middle_index+1 < len(self.playlist_tmp):
            self.support_playlist_middle_index_tmp += 1
            self.support_playlist_decider()
        
    def prev_list_handler(self):
        if self.support_playlist_middle_index-1 > 0:
            self.support_playlist_middle_index_tmp -= 1
            self.support_playlist_decider()
      
    def current_audio_index(self, current_audio, playlist):
        if len(current_audio) > 0 and len(playlist) > 0:
            for i, audio in enumerate(playlist):
                if current_audio['current_audio_path'] == audio['path']:
                    return i
        return -1
        
    def title_decider(self, title, filename):
        if len(title) <= 0 or title.toLower() == "unknwon title":
            return filename
        return title
        
        
     
        
    