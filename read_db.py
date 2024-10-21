from PyQt6.QtCore import QObject, pyqtSignal
from schema import variable_db, playlist_db, Variables, PlaylistSpecificAtrributes, PlaylistCommonAtrributes, VirtualPlaylist
from peewee import Case

class Read(QObject):
    file_read = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        try:
            playlist_db.connect()
            variable_db.connect()
        except:
            # print("Error occur during connecting read cursor")
            pass
    
    def get_variable(self, name, default=None):
        try:
            var = Variables.get(Variables.name==name)
        except:
            return default
        
        if var.value == "True":
            return True
        elif var.value == "False":
            return False 
        return var.value if var.value is not None else default
        
    def get_playlistnames_attr(self):
        return [self.common_attr_to_json(common_attr) for common_attr in PlaylistCommonAtrributes.select()]
    
    def get_playlistname_attr(self, name, default={}):
        try:
            common_attr = PlaylistCommonAtrributes.get(name=name)
            if common_attr.name is None:
                return default
            return self.common_attr_to_json(common_attr)
        except:
            return default
    
    def get_playlist_file_details(self, name, path, default={}):
        try:
            playlist_common_attr = PlaylistCommonAtrributes.get(name=name)
            details = PlaylistSpecificAtrributes.get(name=playlist_common_attr, path=path)
            return self.specific_attr_to_json(details)
        except:
            return default
        
    def get_file_details(self, path):
        specific_attr = PlaylistSpecificAtrributes.get(path=path)
        return self.specific_attr_to_json(specific_attr)
            
    def get_playlist_files(self, name, default=[]):
        return [self.specific_attr_to_json(specific_attr) for specific_attr in self.get_playlist_files_specific_attr(name, default=default)]
        
    def get_playlist_files_specific_attr(self, name, default=[]):
        try:
            playlist_common_attr = PlaylistCommonAtrributes.get(name=name)
            # files = playlist_common_attr.files
            return [d for d in self.__specific_item_sort__(PlaylistSpecificAtrributes.select().where(PlaylistSpecificAtrributes.name==playlist_common_attr))]
        except:
            return default
    
    def get_current_file(self, name, default=[]): # current file in any given playlist
            return self.get_playlistname_attr(name, default)
        
    def select_specific_playlist(self, name):
        common_attr = PlaylistCommonAtrributes.get(PlaylistCommonAtrributes.name == name)
        specific_attr = PlaylistSpecificAtrributes.select().where(PlaylistSpecificAtrributes.name==common_attr)
        return common_attr, self.__specific_item_sort__(specific_attr) 
      
    def get_adjacent_path(self, name, forward=True, get_by_force=False, default=[]):
        common_attr, specific_attr = self.select_specific_playlist(name)
        if common_attr.files_counter > 0:
            current_audio_path = common_attr.current_audio_path
            for i, audio_file in enumerate(specific_attr):
                if audio_file.path == current_audio_path:
                    selected_index = self._selector(i, len(specific_attr), forward, get_by_force)
                    if selected_index is None:
                        return default
                    return self.specific_attr_to_json(specific_attr[selected_index])
        return default
            
    def _selector(self, db_index, db_len, forward, get_by_force): #return integer or None
        if db_len <= 0:
            return None
        if forward:
            return self._forward_selector(db_index=db_index, db_len=db_len, get_by_force=get_by_force)
        else:
            return self._backward_selector(db_index=db_index, db_len=db_len, get_by_force=get_by_force)
    
    def _forward_selector(self, db_index, db_len, get_by_force):
        if db_index+1 < db_len:
            return db_index+1
        elif get_by_force:
            return 0
        return None
    
    def _backward_selector(self, db_index, db_len, get_by_force):
        if db_index > 0:
            return db_index-1
        elif get_by_force:
            return db_len-1
        return None

    def common_attr_to_json(self, common_attr):
        return {
            "playlist_name": common_attr.name,
            "current_audio_path": common_attr.current_audio_path,
            "current_playing_time_milli": common_attr.current_playing_time_milli,
            "is_shared": common_attr.is_shared,
            "picture": common_attr.picture,
            "created_at": common_attr.created_at,
            "created_on": common_attr.created_on,
            "files_counter": common_attr.files_counter,
            "love_playlist": common_attr.love_playlist,
            "like_playlist": common_attr.like_playlist,
        }
        
    def specific_attr_to_json(self, specific_attr):
        return {
            "playlist_name": specific_attr.name.name,
            "path": specific_attr.path,
            "album": specific_attr.album,
            "artist": specific_attr.artist,
            "filename": specific_attr.filename,
            "title": specific_attr.title,
            "size": specific_attr.size,
            "duration": specific_attr.duration,
            "extension": specific_attr.extension,
            "star": specific_attr.star,
            "seconds_played": specific_attr.seconds_played,
            "like_audio": specific_attr.like_audio,
            "hide_in_auto_play": specific_attr.hide_in_auto_play,
            "played_times": specific_attr.played_times,
            "silence_array": specific_attr.silence_array,
        }
        
        
    def get_adjacent_virtual_path(self, path, forward=True, get_by_force=False):
        fav = self.get_virtual_playlist()        
        if not path and len(fav) > 0:
            path = fav[0]['path']
        for i, audio_file in enumerate(fav):
            if audio_file['path'] == path:
                selected_index = self._selector(i, len(fav), forward, get_by_force)
                if selected_index is None:
                    return fav[0]['path'] if len(fav) > 0 else "C:"
                return (fav[selected_index]['path'])
        return fav[0]['path'] if len(fav) > 0 else "C:"
    
    
    def get_virtual_playlist(self):
        ## for loop to select virtual playlist item and get a specific_attr item after that convert it to json format then create a list and return the result
        return [self.specific_attr_to_json(PlaylistSpecificAtrributes.get(PlaylistSpecificAtrributes.id==fav.playlist_item)) for fav in VirtualPlaylist.select()]
    
    def get_virtual_playlist_specific_attr(self):
        ## for loop to select virtual playlist item and get a specific_attr item after that return the result
        return [PlaylistSpecificAtrributes.get(PlaylistSpecificAtrributes.id==fav.playlist_item) for fav in VirtualPlaylist.select()]

    def __specific_item_sort__(self, specific):
        if self.get_variable('Sortby') == "File Name":
            sorted_list = specific.order_by(PlaylistSpecificAtrributes.filename.asc())
        elif self.get_variable('Sortby') == "Title":
            sorted_list = specific.order_by(PlaylistSpecificAtrributes.title.asc())
        elif self.get_variable('Sortby') == "Artist":
            sorted_list = specific.order_by(PlaylistSpecificAtrributes.artist.asc())
        elif self.get_variable('Sortby') == "Album":
            sorted_list = specific.order_by(PlaylistSpecificAtrributes.album.asc())
        elif self.get_variable('Sortby') == "Path":
            sorted_list = specific.order_by(PlaylistSpecificAtrributes.path.asc())
        elif self.get_variable('Sortby') == "Size":
            sorted_list = specific.order_by(PlaylistSpecificAtrributes.size.asc())
        elif self.get_variable('Sortby') == "Duration":
            sorted_list = specific.order_by(PlaylistSpecificAtrributes.duration.asc())
        else:
            sorted_list = specific.order_by(PlaylistSpecificAtrributes.created_at.asc())
            
        if self.get_variable('Descending', False):
            sorted_list = reversed(sorted_list)
        return sorted_list


