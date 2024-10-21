import PyInstaller.__main__

PyInstaller.__main__.run([
    'be_audio_player.py', 
    # '--onefile',
    # '--noconsole',  
    '--icon=res/Images/Compact Disk.ico'
])
