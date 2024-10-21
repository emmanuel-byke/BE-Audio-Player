from PyQt6.QtCore import QObject, pyqtSignal
from schema import PlaylistSpecificAtrributes, PlaylistCommonAtrributes, Variables, playlist_db, variable_db
from pydub.silence import detect_silence
from pydub import AudioSegment
from AudioMetadata import ExtractMetadata


class Update(QObject):
    updated = pyqtSignal()
    
    def __init__(self):
        super().__init__()
    
    def change_current_path(self, playlist_name, path):
        try:
            if len(PlaylistSpecificAtrributes.select().where(PlaylistSpecificAtrributes.path==path)) > 0: ## playlist contains the given path
                self.update_current_audio(playlist_name, path, time_milli=0)
                return True
            return False
        except:
            return False
            
    def update_current_audio(self, name, path, time_milli=0):
        self.update_current_audio_path(name, path)
        self.update_current_audio_time(name, time_milli)
        
    def update_current_audio_path(self, name, path):
        try:
            playlist_common_attr = PlaylistCommonAtrributes.get(name=name)        
            playlist_common_attr.current_audio_path = path
            playlist_common_attr.save()
        except:
            pass
        
    def update_current_audio_time(self, name, time_milli):
        # try:
            playlist_common_attr = PlaylistCommonAtrributes.get(name=name)
            playlist_common_attr.current_playing_time_milli = time_milli
            playlist_common_attr.save()
        # except:
        #     pass
        
    def update_playlist_common_like(self, name, like):
        try:
            playlist_common_attr = PlaylistCommonAtrributes.get(name=name)
            playlist_common_attr.like_playlist = like
            playlist_common_attr.save() 
        except:
            pass
           
    def update_playlist_common_shared(self, name, shared):
        try:
            playlist_common_attr = PlaylistCommonAtrributes.get(name=name)
            playlist_common_attr.is_shared = shared
            playlist_common_attr.save()    
        except:
            pass

    def update_playlist_common_love(self, name, love):
        try:
            playlist_common_attr = PlaylistCommonAtrributes.get(name=name)
            playlist_common_attr.love_playlist = love
            playlist_common_attr.save()    
        except:
            pass
        
        
    def update_audio_like(self, name, path, like):
        try:
            playlist_common_attr = PlaylistCommonAtrributes.get(name=name)
            playlist_audio = PlaylistSpecificAtrributes.get(path=path, name=playlist_common_attr)
            playlist_audio.like_audio = like
            playlist_audio.save()  
        except:
            pass
        
    def update_audio_star(self, name, path, star):
        try:
            playlist_common_attr = PlaylistCommonAtrributes.get(name=name)
            playlist_audio = PlaylistSpecificAtrributes.get(path=path, name=playlist_common_attr)
            playlist_audio.star = star
            playlist_audio.save()  
        except:
            pass
        
    def update_audio_hide_auto_play(self, name, path, hide):
        try:
            playlist_common_attr = PlaylistCommonAtrributes.get(name=name)
            playlist_audio = PlaylistSpecificAtrributes.get(path=path, name=playlist_common_attr)
            playlist_audio.hide_in_auto_play = hide
            playlist_audio.save()  
        except:
            pass
        
    def update_audio_seconds_played(self, name, path, seconds):
        try:
            playlist_common_attr = PlaylistCommonAtrributes.get(name=name)
            playlist_audio = PlaylistSpecificAtrributes.get(path=path, name=playlist_common_attr)
            playlist_audio.seconds_played += seconds
            playlist_audio.save()  
        except:
            pass
        
    def update_audio_played_times(self, name, path): # call it when audio has been played (manually or automatically)
        try:
            playlist_common_attr = PlaylistCommonAtrributes.get(name=name)
            playlist_audio = PlaylistSpecificAtrributes.get(path=path, name=playlist_common_attr)
            playlist_audio.played_times += 1
            playlist_audio.save()  
        except:
            pass
        
    def update_playlist_name(self, old_name, new_name):
        playlist_common_attr = PlaylistCommonAtrributes.get(name=old_name)
        playlist_common_attr.name = new_name
        playlist_common_attr.save()
        
    def update_silence(self):
        for specific_attr in PlaylistSpecificAtrributes.select():
            if specific_attr.silence_array is None:
                self.silence_detector(specific_attr, specific_attr.path)
    
    def update_silence_file_force(self, path):
        self.silence_detector(PlaylistSpecificAtrributes.get(path=path), path)
        
    def silence_detector(self, specific_attr, path):
        audio = AudioSegment.from_file(path)
        silent_segments = detect_silence(audio, silence_thresh=-1000, min_silence_len=50, seek_step=50)
        specific_attr.silence_array = self.get_formatted_silence_array(silent_segments)
        specific_attr.save()
        
        
    def get_formatted_silence_array(self, array):
        if len(array) <= 0:
            return [[0, 0], [0, 0]]
        elif len(array) == 1:
            if array[0][0] == 0:
                return [array[0], [0, 0]]
            else:
                return [[0, 0], array[0]]
        elif len(array) >= 2:
            if array[0][0] == 0:
                return [array[0], array[-1]]
            else:
                return [[0, 0], array[-1]]
        else:
            return [array[0], array[-1]]
        
    def update_playlist_name(self, old_name, new_name):
        common = PlaylistCommonAtrributes.get(name=old_name)
        common.name = new_name
        common.save()
        
    def update_metadata(self, path):
        path = path.replace('\\', '/')
        metadata = ExtractMetadata(path)
        for item in PlaylistSpecificAtrributes.select().where(PlaylistSpecificAtrributes.path==path):
            item.album = metadata.get_album()
            item.artist = metadata.get_artist()
            item.filename, item.extension = metadata.get_filename() # it returns a tuple
            item.title = metadata.get_title()
            item.size = metadata.get_size()
            item.duration = metadata.get_duration()
            item.save()
        
    def update_files_counter(self, playlist_name):
        common = PlaylistCommonAtrributes.get(name=playlist_name)
        common.files_counter = len(common.files)
        common.save()
        
    def remove_audio(self, playlist_name, path):
        common = PlaylistCommonAtrributes.get(name=playlist_name)
        specific = PlaylistSpecificAtrributes.get(name=common, path=path)
        specific.delete_instance()
        
    def clear_playlist(self, playlist_name):
        try:
            common = PlaylistCommonAtrributes.get(name=playlist_name)
            specific = common.files
            common.delete_instance()
            
            for item in specific:
                item.delete_instance()
        except:
            pass

    def remove_playlist(self, playlist_name):
        try:
            common = PlaylistCommonAtrributes.get(name=playlist_name)
            specific = common.files
            common.delete_instance()
            
            for item in specific:
                item.delete_instance()
            common.delete_instance()    
        except:
            pass        
            
    def remove_playlist_table(self):
        try:
            with playlist_db.atomic():
                PlaylistSpecificAtrributes.delete().execute()
            with playlist_db.atomic():
                PlaylistCommonAtrributes.delete().execute()
        except:
            pass
        
    def remove_variable_table(self):
        try:
            with variable_db.atomic():
                Variables.delete().execute()
        except:
            pass
        
            
    
    
    

