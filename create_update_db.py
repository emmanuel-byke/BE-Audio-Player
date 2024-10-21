from PyQt6.QtCore import QObject, pyqtSignal
from schema import variable_db, playlist_db, Variables, PlaylistSpecificAtrributes, PlaylistCommonAtrributes, VirtualPlaylist
from AudioMetadata import ExtractMetadata
import math
import random

# os.remove("variables.db")
# os.remove("playlist.db")

class Create(QObject):
    file_added = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        try:
            variable_db.connect()
            playlist_db.connect()
            variable_db.create_tables([Variables])
            playlist_db.create_tables([PlaylistSpecificAtrributes, PlaylistCommonAtrributes, VirtualPlaylist])
        except:
            # print("Create connection error")
            pass

    def create_variable(self, name, value):
        variable, created = Variables.get_or_create(name=name)
        variable.value = value # repeation was done to correct error when updating the value
        variable.save()
        
    def create_playlist(self, name, path):
        path = path.replace('\\', '/')
        playlist_common_attr, _ = PlaylistCommonAtrributes.get_or_create(name=name)
        playlist, created = PlaylistSpecificAtrributes.get_or_create(path=path, name=playlist_common_attr)
        if created:            
            metadata = ExtractMetadata(path)
            playlist.album = metadata.get_album()
            playlist.artist = metadata.get_artist()
            playlist.filename, playlist.extension = metadata.get_filename() # it returns a tuple
            playlist.title = metadata.get_title()
            playlist.size = metadata.get_size()
            playlist.duration = metadata.get_duration()
            
        playlist_common_attr.files_counter = len(playlist_common_attr.files)
        playlist.save()     
        playlist_common_attr.save()   
        # self.file_added.emit(path)
        return path      
    
    def create_playlist_commons(self, name, is_shared, picture):
        playlist_common_attr, _ = PlaylistCommonAtrributes.get_or_create(
            name=name,
            is_shared = is_shared,
            picture = picture
        )
        playlist_common_attr.save()
        
    def create_virtual_playlist(self, name, files=[]):
        with playlist_db.atomic():
            VirtualPlaylist.delete().execute()
            
        if name.lower() == 'favourite':
            for specific_attr in self._favourite_decider_():
                VirtualPlaylist.create(
                    name=name,
                    playlist_item = specific_attr
                )
                
        elif name.lower() == 'most played':
            for specific_attr in self._most_played_decider_():
                VirtualPlaylist.create(
                    name=name,
                    playlist_item = specific_attr
                )
                
        elif name.lower() == 'shuffle':
            for specific_attr in self._shuffle_decider_(files):
                VirtualPlaylist.create(
                    name=name,
                    playlist_item = specific_attr
                )
        
        
    def _favourite_decider_(self):
        seconds_played_weight = 0.00001
        number_of_plays_weight = 0.567 * math.pi
        like_weight = 50 * math.pi  * 5 
        star_weight = 30 * math.pi ** 2
        return PlaylistSpecificAtrributes.select().where(
            (
                (
                    (PlaylistSpecificAtrributes.seconds_played * seconds_played_weight) + 
                    (PlaylistSpecificAtrributes.star * star_weight) + 
                    (PlaylistSpecificAtrributes.played_times * number_of_plays_weight) + 
                    (like_weight * 5 if (PlaylistSpecificAtrributes.like_audio == "High") else 1)
                ) >= 1000) 
                &   (
                        PlaylistSpecificAtrributes.hide_in_auto_play == False
                    ) 
                &   (
                        PlaylistSpecificAtrributes.like_audio != 'Low'
                    )
            )

    def _most_played_decider_(self):
        return PlaylistSpecificAtrributes.select().where((PlaylistSpecificAtrributes.played_times>20) & (PlaylistSpecificAtrributes.hide_in_auto_play==False))
        
    
    def _shuffle_decider_(self, files):
        random.shuffle(files)
        return files
    
    

