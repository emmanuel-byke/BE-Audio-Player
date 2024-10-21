from peewee import PostgresqlDatabase, Model, TextField, DateField, IntegerField, ForeignKeyField, BooleanField, DateTimeField, CharField
import datetime

variable_db = PostgresqlDatabase('BE_Player_Variables', user='postgres', password='1234', host='localhost', port='5432')
playlist_db = PostgresqlDatabase('BE_Player_Playlist', user='postgres', password='1234', host='localhost', port='5432')



# variable_db = SqliteDatabase("variables.db")
# playlist_db = SqliteDatabase("playlist.db")
# playlist_auto_db = SqliteDatabase("playlist_auto_created.db")

class Variables(Model):
    name = TextField(null=False, index=True)
    value = TextField(null=True, index=False)
    
    class Meta:
        database = variable_db
        
class PlaylistCommonAtrributes(Model):
    name = TextField(null=False, index=True)
    current_audio_path = TextField(null=True, index=False)    
    current_playing_time_milli = IntegerField(default=0)
    files_counter = IntegerField(default=0)
    is_shared = BooleanField(default=False)
    picture = TextField(null=True) # Use BlobField
    
    love_playlist = BooleanField(default=False)
    like_playlist = TextField(default='Normal') # Low, Normal, High
    
    
    
    created_at = DateTimeField(default=datetime.datetime.now)
    created_on = DateField(default=datetime.date.today)
    
    class Meta:
        database = playlist_db
        
class PlaylistSpecificAtrributes(Model):
    name = ForeignKeyField(PlaylistCommonAtrributes, backref='files', null=False, index=True, on_delete='CASCADE')
    path = TextField(null=False, index=False)
    album = TextField(null=True, index=True)
    artist = TextField(null=True, index=True)
    filename = TextField(null=True, index=True)
    title = TextField(null=True, index=True)
    size = TextField(null=True, index=True)
    duration = TextField(null=True, index=True)
    extension = TextField(null=True, index=True)
    silence_array = TextField(null=True, index=False)
    
    star = IntegerField(default=0) # 0 - 5
    seconds_played = IntegerField(default=0)
    like_audio = TextField(default='Normal') # Low, Normal, High
    hide_in_auto_play = BooleanField(default=False)
    played_times = IntegerField(default=0)
    
    
    created_at = DateTimeField(default=datetime.datetime.now)
    created_on = DateField(default=datetime.date.today)
    
    class Meta:
        database = playlist_db
        
class VirtualPlaylist(Model):
    name = TextField(null=False)
    playlist_item = ForeignKeyField(PlaylistSpecificAtrributes, backref='files', null=True, index=True, on_delete='CASCADE')
    
    class Meta:
        database = playlist_db
    

    