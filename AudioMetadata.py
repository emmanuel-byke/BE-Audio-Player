from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TCON
from tinytag import TinyTag
import os
from settings import Constants

def is_audio(extension):
    return extension in Constants().audio_formats()

class ExtractMetadata():
    def __init__(self, path):
        self.path = path
        if is_audio(self.get_filename()[1]):
            try:
                self.audio = EasyID3(path)
                self.using_mutagen = True
            except:
                self.using_mutagen = False
            try:
                self.tag = TinyTag.get(path) # used to get duration
            except:
                self.tag = None
        else:
            pass
        
            
    def get_artwork(self):
        if is_audio(self.get_filename()[1]):
            if self.using_mutagen:
                id3_tags = ID3(self.path)
                artwork = id3_tags.getall("APIC")
                if artwork:
                    return artwork[0].data
                else:
                    return self.tag.get_image()
            elif self.tag is not None:
                return self.tag.get_image()
        return None
        
    def get_folder_pic(self):
        pass
        
    def get_artist(self):
        if is_audio(self.get_filename()[1]):
            if self.using_mutagen:
                return self.audio.get("artist", ["Unknown Artist"])[0]
            elif self.tag is not None:
                return self.tag.artist if self.tag.artist else "Unknown Artist"
            return "Unknown Artist"
        return "Video"
    
    def get_album(self):
        if is_audio(self.get_filename()[1]):
            if self.using_mutagen:
                return self.audio.get("album", ["Unknown Album"])[0]
            elif self.tag is not None:
                return self.tag.album if self.tag.album else "Unknown Album"
        return "Unknown Album"
    
    def get_title(self):
        if is_audio(self.get_filename()[1]):
            if self.using_mutagen:
                return self.audio.get("title", [self.get_filename()[0]])[0]
            elif self.tag is not None:
                return self.tag.title if self.tag.title else self.get_filename()[0]
        return self.get_filename()[0]
    
    def get_genre(self):
        if is_audio(self.get_filename()[1]):
            if self.tag is not None:
                return self.tag.genre
        return ""
    
    def get_path(self):
        return self.path
    
    def get_filename(self):
        if self.path.count('.') > 0:
            return os.path.basename(self.path).rsplit(".", 1)
        return (os.path.basename(self.path), "")
    
    def get_size(self):
        try:
            import Helper
            conv = Helper.Conversions()
            return conv.from_bytes(os.path.getsize(self.path))
        except:
            return "0"
    
    def get_duration(self):
        try:
            return self.tag.duration * 1000
        except:
            return 0
    

class MetadataWriter:
    def __init__(self, path):
        self.path = path
        if is_audio(self.get_filename()[1]):
            self.audio = ID3(path)   
        
    def modify_title(self, title):
        if is_audio(self.get_filename()[1]):
            self.audio["TIT2"] = TIT2(encoding=3, text=title)
    
    def modify_artist(self, artist):
        if is_audio(self.get_filename()[1]):
            self.audio["TPE1"] = TPE1(encoding=3, text=artist)
    
    def modify_album(self, album):
        if is_audio(self.get_filename()[1]):
            self.audio["TALB"] = TALB(encoding=3, text=album)
    
    def modify_genre(self, genre):
        if is_audio(self.get_filename()[1]):
            self.audio["TCON"] = TCON(encoding=3, text=genre)
            
    def modify_artwork(self, path):
        if is_audio(self.get_filename()[1]):
            with open(path, "rb") as albumart_file:
                albumart = albumart_file.read()
                self.audio["APIC"] = APIC(
                    encoding=3,
                    mime="image/jpeg",
                    type=3,
                    desc=u"Cover",
                    data=albumart,
                )
    
    def save(self):
        if is_audio(self.get_filename()[1]):
            self.audio.save()
            
    def get_filename(self):
        if self.path.count('.') > 0:
            return os.path.basename(self.path).rsplit(".", 1)
        return (os.path.basename(self.path), "")
    
    
    
