from create_update_db import Create
from read_db import Read
from update_db import Update
from Visualizer.AudioProcessor import SilenceDetector
import time
from Helper import Conversions
from pydub.silence import detect_silence
from pydub import AudioSegment, silence
import threading

createDB = Create()
readDB = Read()
update_db = Update()


# createDB.create_virtual_playlist('fav')
# print(readDB.get_virtual_playlist())
# print("="*150)
# print(readDB.get_adjacent_virtual_path(None, True, True))
# print("="*150)
# print(readDB.get_adjacent_virtual_path(None, False, True))

start = time.time()
# to_formatted = Conversions()
print("... Starting-----")
audio_path = "C:/Users/Byke/Music/sd/music/i_want_it_to_be_you_tatiana_manaois_ft_mac_mase_official_music_video_aac_748.mp3"
# silence = SilenceDetector(audio_path)
# print("Fetching Duration:", to_formatted.from_seconds(time.time()-start), end="\t")
# print(to_formatted.from_milli(silence.get_silence_duration()[0]), to_formatted.from_milli(silence.get_silence_duration()[1]))



print(readDB.get_file_details(audio_path, createDB))

