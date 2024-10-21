from PyQt6.QtWidgets import QGraphicsBlurEffect
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMenu
from player import Player
from Helper import Conversions
from create_update_db import Create
from read_db import Read
from update_db import Update
from settings import WidgetRemover, Skin
from Helper import Settings, retrive_current_audio_property, retrive_current_playlist_property, create_important_variables
from ThreeAudio import Customize
from PyQt6.QtGui import QAction
from PlaylistManager import PlaylistTools
from time import time
from AdditionWidgets import YesNo, MetadataEditor
from SVG import IconLoader
# from Visualizer.AudioProcessor import AudioLevel
# from Visualizer.pulse_visualiser import PulseVisualizer
from Visualizer.equalizer_bar import Bar
import threading
from Transition import Shrink
from Settings_Widget import SettingsWidget

class HandleWidgets():
    def __init__(self, parent, get_file):
        self.create = Create()
        self.update_db = Update()
        self.read = Read()
        create_important_variables() ## before running anything else
        self.parent = parent
        self.conversion = Conversions()
        self.slider_is_dragged = False
        self.get_file = get_file
        self.player = Player()
        self.widgetRemover = WidgetRemover(parent)
        self.settings_helper = Settings(parent, self.widgetRemover)
        self.threeAudioCustomize = Customize(parent)
        self.iconLoader = IconLoader(parent)
        self.skin = Skin(parent)
        self.shrink = Shrink(parent.mainFrame)
                
        # self.audio_array = AudioLevel(num_samples=8, channels=2)
        # # self.pulse_visualizer = PulseVisualizer(self.parent.visualizerFrame)
        # self.bar_visualizer = Bar(16, ['#0C0786', '#40039C', '#6A00A7', '#8F0DA3', '#B02A8F', '#CA4678', '#E06461',
        #                         '#F1824C', '#FCA635', '#FCCC25', '#EFF821'], self.parent.visualizerFrame)
        
        self.hide_volume_frame_timer = 1999999
        self.hide_status_frame_timer = 0
        self.play_pause_animation_counter = 0
        self.one_button_skin_counter = 0
        self.one_button_skin_current_state = ''
        self.start_playing_time = time()
        
                
        self.playlistTools = PlaylistTools(parent, self.settings_helper, get_file)
        self.key_bindings()
        self.customization()
        self.add_actions()
        self.addMenues()         
        
        self.load() # last thing to be done
        
    def set_bar_visualizer(self):
        # self.create.create_variable("current visualizer", "Bar")
        # # self.audio_array.set_num_bars(10)
        # self.bar_visualizer.setGeometry(5, 5, 471, 110)
        # # self.pulse_visualizer.setGeometry(0, 0, 0, 0)
        pass
        
    def set_pulse_visualizer(self):
        # self.create.create_variable("current visualizer", "Pulse")
        # # self.audio_array.set_num_bars(100)
        # # self.pulse_visualizer.setGeometry(5, 5, 471, 50)
        # self.bar_visualizer.setGeometry(0, 0, 0, 0)
        pass
        
    def playback_end(self):
        self.create.create_variable("playing", False)
        self.iconLoader.special_icons()
        self.save_current_audio_updates()
        self.change_audio_with_repeate_condition(forward_direction=True, forced_loop=False)
        self.load_player()
        
    def load_player(self, forced_play=False):
        if not self.read.get_variable("end of playlist", False) or self.isLoading or forced_play:
            details = self.read.get_current_file(self.read.get_variable("current playlist"), default=[]) if not self.read.get_variable('virtual playlist', False) else None
            if self.read.get_variable('virtual playlist', False):
                path = self.read.get_variable('virtual playing path')
                name = self.read.get_variable('virtual playlist')
                self.play_audio(name, path)
                
            elif len(details) > 0 and details['current_audio_path'] is not None:
                self.play_audio(details["playlist_name"], details['current_audio_path'], details["current_playing_time_milli"]) 
                self.isLoading = False
                self.create.create_variable("end of playlist", False) # find better place to update this variable
            else:
                text = "No playlist" if len(details) <= 0 else details['playlist_name'] + " has no audios" 
                self.parent.statusLabel.setText(text)
                self.hide_status_frame_timer = 0
                self.create.create_variable("end of playlist", True)
        else:
            self.parent.statusLabel.setText("End of your playlist")
            self.hide_status_frame_timer = 0
            self.isLoading = True
            self.create.create_variable("end of playlist", True)
        self.iconLoader.special_icons()
            
    def play_audio(self, playlist_name, path, start_time=0):
        self.save_current_audio_updates()
        if not self.read.get_variable('virtual playlist', False):
            self.create.create_variable("current playlist", playlist_name)
            self.update_db.update_current_audio(playlist_name, path, 0)
        
        details = self.read.get_file_details(path)
        if details['silence_array'] is None:
            worker_thread = threading.Thread(target=self.update_db.update_silence)
            worker_thread.start()
        self.player.load_audio(path, silence_array=details['silence_array'], auto_play=True)
        # self.audio_array.load_audio(path) 
        self.start_playing_time = time()
        self.create.create_variable("playing", True)
        self.iconLoader.like_love_star_updater()
        self.threeAudioCustomize.support_playlist_decider()
        self.threeAudioCustomize.main_playlist_decider()
        # self.player.play()  ### Auto play is doing similar work here
        self.player.seek(start_time)
        self.playlistTools.show_current_data()
        self.iconLoader.special_icons()
        
    def play(self):
        if self.player.isPlaying():
            self.player.pause()
            self.create.create_variable("playing", False)
            self.save_current_audio_updates()
            self.play_action.setText("Play")
        elif self.player.isPaused():
            self.player.play()
            self.create.create_variable("playing", True)
            self.start_playing_time = time()
            self.play_action.setText("Pause")
        else:
            self.load_player(forced_play=True)
            self.play_action.setText("Pause")
            
        self.iconLoader.special_icons()
        
    def stop_audio(self, save=True):
        if save:
            self.save_current_audio_updates()
        self.player.stop_audio(emit_signal=False)
        self.create.create_variable("playing", False)
        self.iconLoader.special_icons()
        self.play_action.setText("Pause" if self.player.isPlaying() else "Play")
        
        self.parent.skin_filename.setText("Playback Stopped")
        self.parent.skin_title.setText("Message From Basikolo himself")
                
    def next(self, save=True):
        if save:
            self.save_current_audio_updates()
        self.change_audio_with_repeate_condition(forward_direction=True, forced_loop=True)
        self.load_player(forced_play=True)
        
    def prev(self, save=True):
        if save:
            self.save_current_audio_updates()
        self.change_audio_with_repeate_condition(forward_direction=False, forced_loop=True)
        self.load_player(forced_play=True)

    def change_audio_with_repeate_condition(self, forward_direction, forced_loop=False):
        repeate = self.read.get_variable('Repeate')
        if repeate != "One" or forced_loop:
            if self.read.get_variable('virtual playlist', False):
                adjacent_audio = self.read.get_adjacent_virtual_path(self.read.get_variable('virtual playing path', False), 
                            forward=forward_direction, get_by_force=(repeate=="All" or forced_loop))
                self.create.create_variable('virtual playing path', adjacent_audio)
            else:
                adjacent_audio = self.read.get_adjacent_path(self.read.get_variable('current playlist'), 
                            forward=forward_direction, get_by_force=(repeate=="All" or forced_loop))
                if adjacent_audio is not None and len(adjacent_audio) > 0:
                    self.update_db.change_current_path(self.read.get_variable('current playlist'), adjacent_audio['path'])
                else:
                    self.create.create_variable("end of playlist", True)
                    
                    
        
        
    def repeate(self):
        repeate_var = self.read.get_variable("Repeate", None) # use None inorder to create the variable
        if repeate_var is None:
            self.create.create_variable("Repeate", False)
        else:
            self.create.create_variable("Repeate", False if repeate_var=="One" else "All" if not repeate_var else "One")
        self.iconLoader.repeate_shuffle_updater()
        
        repeate_var = self.read.get_variable("Repeate", False)
        self.repeate_action.setText("Repeate {}".format("Off" if repeate_var=="One" else "All" if not repeate_var else "One"))
        
    def shuffle(self):
        shuffle_var = self.read.get_variable("Shuffle", None) #use None to create variable if absent
        if shuffle_var is None:
            self.create.create_variable("Shuffle", False)
        else:
            self.create.create_variable("Shuffle", not shuffle_var)
        self.shuffle_action.setText("Turn Shuffle {}".format("On" if shuffle_var else "Off"))
        if self.read.get_variable("Shuffle"):
            self.playlistTools.show_shuffle()
        else:
            self.create.create_variable('virtual playlist', False)
            self.playlistTools.show_current_data()
            
        self.iconLoader.repeate_shuffle_updater()
        
             
        
    def add_actions(self):
        self.playback_menu = QMenu("Playback")
        self.play_action = QAction("Play", self.parent)
        self.next_action = QAction("Next", self.parent)
        self.prev_action = QAction("Prev", self.parent)
        self.repeate_action = QAction("Repeate all", self.parent)
        self.shuffle_action = QAction("Shuffle", self.parent)
        self.playback_menu.addActions([self.play_action, self.next_action, self.prev_action])
        self.playback_menu.addSeparator()
        self.playback_menu.addActions([self.repeate_action, self.shuffle_action])
        
        self.open_menu = QMenu("Open")
        self.open_file_action = QAction("Open File ", self.parent)
        self.open_folder_action = QAction("Open Folder ", self.parent)
        self.open_menu.addActions([self.open_file_action, self.open_folder_action])
                
        self.help_menu = QMenu("Help")
        self.help_menu.setDisabled(True)
        self.help_action = QAction("Help", self.parent)
        self.about_action = QAction("About", self.parent)
        self.sortcurts_action = QAction("Shortcurts", self.parent)
        self.update_action = QAction("Update", self.parent)
        self.help_menu.addActions([self.help_action, self.about_action])
        self.help_menu.addSeparator()
        self.help_menu.addActions([self.sortcurts_action, self.update_action])
        
        self.account_menu = QMenu("Account")
        self.account_menu.setDisabled(True)
        self.login_action = QAction("Login", self.parent)
        self.register_action = QAction("Register", self.parent)
        self.logout_action = QAction("Logout", self.parent)
        self.account_menu.addActions([self.login_action, self.register_action])
        self.account_menu.addSeparator()
        self.account_menu.addAction(self.logout_action)
        
        self.settings_action = QAction("Settings", self.parent)
        self.exit_action = QAction("Exit", self.parent)
        self.edit_metadata_action = QAction("Edit Metadata", self.parent)
     

        self.skin_menu = QMenu("Skin")
        for name in self.skin.skin_names():
            skin_action = QAction(name, self.parent)
            skin_action.triggered.connect(lambda: self.settings_helper.set_skin(self.skin, self.parent.sender().text()))
            skin_action.triggered.connect(self.iconLoader.load_icons)
            
            self.skin_menu.addAction(skin_action)
            

        self.visualizer_menu = QMenu("Visualizer")
        self.visualizer_menu.setDisabled(True)
        self.bar_visualizer_action = QAction("Bar", self.parent)
        self.pulse_visualizer_action = QAction("Pulse", self.parent)
        self.no_visualizer_action = QAction("Off", self.parent)
        self.visualizer_menu.addActions([self.bar_visualizer_action, self.pulse_visualizer_action])
        self.visualizer_menu.addSeparator()
        self.visualizer_menu.addAction(self.no_visualizer_action)                
        
        self.share_action = QAction("", self.parent)
        self.share_action.setText(self.share_name_decider()) # do it in two lines so that you can disable the action in decider
        self.current_playlist_action = QAction(self.update_current_playlist(), self.parent)
        self.create_playlist_action = QAction("Create Playlist", self.parent)
        self.select_playlist_action = QAction("Select Playlist", self.parent)
        
        self.view_menu = QMenu("View")
        self.view_menu.addAction(self.current_playlist_action)
        self.view_menu.addSeparator()
        self.view_menu.addMenu(self.visualizer_menu)
        
        self.load_playlist_menu_pop = QMenu("Load Your Likes")
        self.load_playlist_menu_pop_fav = QAction("Favourite", self.parent)
        self.load_playlist_menu_pop_his = QAction("History", self.parent)
        self.load_playlist_menu_pop_most = QAction("Most Played", self.parent)
        self.load_playlist_menu_pop_sugg = QAction("Suggested", self.parent)
        self.load_playlist_menu_pop.addAction(self.load_playlist_menu_pop_fav)
        self.load_playlist_menu_pop.addAction(self.load_playlist_menu_pop_his)
        self.load_playlist_menu_pop.addAction(self.load_playlist_menu_pop_most)
        self.load_playlist_menu_pop.addAction(self.load_playlist_menu_pop_sugg)
        
        self.new_menu = QMenu()
        self.new_menu.addActions([self.open_file_action, self.create_playlist_action])
        
        self.load_playlist_menu_pop_fav.triggered.connect(self.playlistTools.show_favourite)
        self.load_playlist_menu_pop_most.triggered.connect(self.playlistTools.show_most_played)
        self.load_playlist_menu_pop_his.setDisabled(True)
        self.load_playlist_menu_pop_sugg.setDisabled(True)
        
        # self.current_playlist_action.triggered.connect(self.playlistTools.create_playlist)
        self.create_playlist_action.triggered.connect(self.playlistTools.create_playlist)
        self.select_playlist_action.triggered.connect(self.playlistTools.load_playlist_names)
        
        self.current_playlist_action.triggered.connect(self.open_playlist)
        self.current_playlist_action.triggered.connect(lambda: self.current_playlist_action.setText(self.update_current_playlist()))
        self.parent.playlistAlt.clicked.connect(self.open_playlist)
        self.current_playlist_action.triggered.connect(self.playlistTools.show_current_data)
        self.parent.playlistAlt.clicked.connect(self.playlistTools.show_current_data)
        self.share_action.triggered.connect(self.share_playlist)
        
        self.play_action.triggered.connect(self.play)
        self.next_action.triggered.connect(self.next)
        self.prev_action.triggered.connect(self.prev)
        self.repeate_action.triggered.connect(self.repeate)
        self.shuffle_action.triggered.connect(self.shuffle)
        self.settings_action.triggered.connect(self.settings)
        self.edit_metadata_action.triggered.connect(self.edit_metadata)
        self.open_file_action.triggered.connect(self.get_file.get_file_btn)
        self.open_folder_action.triggered.connect(self.get_file.get_file_folder)
        self.login_action.triggered.connect(self.login_signup_decider)
        self.register_action.triggered.connect(self.login_signup_decider)
        self.bar_visualizer_action.triggered.connect(self.set_bar_visualizer)
        self.pulse_visualizer_action.triggered.connect(self.set_pulse_visualizer)
        self.exit_action.triggered.connect(self.before_quite_application)

        
     
    def edit_metadata(self):
        self.metadata_editor = MetadataEditor(self.parent, self.player.get_path())
        self.metadata_editor.metadata_changed.connect(self.metadata_changed)
        
    def metadata_changed(self, path):
        self.update_db.update_metadata(path)
        self.player.set_load_widgets(True)    
        self.change_widgets_after_play()
        
        
    def update_current_playlist(self):
        text = self.share_name_decider()
        self.share_action.setText(text)
        self.parent.sharePlaylist.setToolTip(text)
        
        name = self.read.get_variable("current playlist") if not self.read.get_variable("virtual playlist") else self.read.get_variable("virtual playlist")
        return "Show " +name.capitalize() + " Playlist"
        
    def key_bindings(self):        
        self.parent.exitBtn.clicked.connect(self.before_quite_application)
        self.parent.exitBtnAlt.clicked.connect(self.before_quite_application)
        self.parent.skin_power.clicked.connect(self.before_quite_application)
        self.parent.minimizeBtn.clicked.connect(self.parent.showMinimized)
        self.parent.minizeBtnAlt.clicked.connect(self.parent.showMinimized)
        self.parent.skin_minimize.clicked.connect(self.parent.showMinimized)
        self.parent.playPos.sliderPressed.connect(self.slider_pressed)
        self.parent.skin_progress.sliderPressed.connect(self.slider_pressed)
        self.parent.playPos.sliderReleased.connect(self.slider_released)
        self.parent.skin_progress.sliderReleased.connect(self.slider_released)
        self.player.playback_end.connect(self.playback_end)
        self.parent.open.clicked.connect(self.get_file.get_file_btn)
        self.parent.next.clicked.connect(self.next)
        self.parent.nextAlt.clicked.connect(self.next)
        self.parent.skin_next.clicked.connect(self.next)
        self.parent.prev.clicked.connect(self.prev)
        self.parent.prevAlt.clicked.connect(self.prev)
        self.parent.skin_prev.clicked.connect(self.prev)
        self.parent.shuffle.clicked.connect(self.shuffle)
        self.parent.repeate.clicked.connect(self.repeate)
        self.parent.settBtn.clicked.connect(self.settings)
        self.parent.settBtnAlt.clicked.connect(self.settings)
        
        self.parent.volumeSlider.sliderMoved.connect(self.change_volume)
        self.parent.volSliderAlt.sliderMoved.connect(lambda: self.change_volume(self.parent.volSliderAlt.value(), True, True))
        self.parent.skin_volume_slider.sliderMoved.connect(lambda: self.change_volume(self.parent.skin_volume_slider.value(), True, True))
        self.parent.volUpBtn.clicked.connect(lambda: self.change_volume(self.parent.volumeSlider.value()+5, True))
        self.parent.skin_add_volume_btn.clicked.connect(lambda: self.change_volume(self.parent.volumeSlider.value()+5, True))
        self.parent.volDownBtn.clicked.connect(lambda: self.change_volume(self.parent.volumeSlider.value()-5, True))
        self.parent.skin_minus_volume_btn.clicked.connect(lambda: self.change_volume(self.parent.volumeSlider.value()-5, True))
        
        
        self.parent.mute.clicked.connect(self.mute)
        
        self.threeAudioCustomize.play_signal.connect(self.load_player)
        self.get_file.play_signal.connect(self.file_added)
        self.parent.play.clicked.connect(self.play)
        self.parent.playAlt.clicked.connect(self.play)
        self.parent.skin_play.clicked.connect(self.play)
        self.playlistTools.reload_player.connect(self.load_playlist)
        self.playlistTools.play_next.connect(self.next)
        self.playlistTools.play_audio.connect(self.play_audio)
        self.playlistTools.stop_audio.connect(self.stop_audio)
        self.playlistTools.playlist_changed.connect(lambda: self.current_playlist_action.setText(self.update_current_playlist()))
        self.playlistTools.playlist_changed.connect(self.open_playlist)
        
        self.parent.showVolume.clicked.connect(self.show_volume_frame)
        self.parent.skin_show_volume.clicked.connect(self.show_skin_volume_frame)
        
        self.parent.loginBtn.clicked.connect(self.login_signup_decider)
        self.parent.loginBtnAlt.clicked.connect(self.login_signup_decider)
        self.parent.loginFromRegister.clicked.connect(self.settings_helper.open_login)
        self.parent.registerBtn.clicked.connect(self.register_user)
        self.parent.closeRegister.clicked.connect(self.open_defaults)
        self.parent.closeLogin.clicked.connect(self.open_defaults)
        self.parent.homeAlt.clicked.connect(self.open_defaults)
        self.parent.loginUser.clicked.connect(self.login_user)
        self.parent.signupFromRegister.clicked.connect(self.settings_helper.open_register)
        
        
        
        self.parent.likeAudio.clicked.connect(self.like_audio)
        self.parent.starAudio.clicked.connect(self.star_audio)
        self.parent.likePlaylist.clicked.connect(self.like_playlist)
        self.parent.lovePlaylist.clicked.connect(self.love_playlist)
        self.parent.sharePlaylist.clicked.connect(self.share_playlist)
                
        self.parent.destroyed.connect(self.save)
        
        self.parent.skin_expand_right.clicked.connect(self.maximize_one_button_skin)
        self.parent.skin_expand_left.clicked.connect(self.maximize_one_button_skin)
        self.parent.skin_menu.clicked.connect(self.open_playlist)
         
    def file_added(self, play_item=True):
        if self.read.get_variable('playing', False) and self.read.get_variable('virtual playlist', False):
            self.yes_no_window = YesNo(self.parent.geometry().x()+50, self.parent.geometry().y()+80)
            self.parent.destroyed.connect(self.yes_no_window.deleteLater)
            self.yes_no_window.yes_signal.connect(lambda: self.remove_virtual_playlist_and_play(play_item)) 
            self.yes_no_window.promptText.setText("Switch to {} playlist and play new added audio?".format(self.read.get_variable('current playlist', "").capitalize()))
        else:
            self.remove_virtual_playlist_and_play(play_item)
            
        text = self.share_name_decider()
        self.share_action.setText(text)
        self.parent.sharePlaylist.setToolTip(text)
        self.playlistTools.show_current_data()
            
    def remove_virtual_playlist_and_play(self, play_item):
        self.create.create_variable('virtual playlist', False)
        if play_item:
            self.load_player(forced_play=True)
        self.create.create_variable("Shuffle", False)
        self.iconLoader.repeate_shuffle_updater()
        
    def show_volume_frame(self):
        if self.parent.volFrameControls_2.isHidden():
            self.hide_volume_frame_timer = 0
        else:
            self.hide_volume_frame_timer = 181400
        self.parent.volFrameControls_2.setHidden(not self.parent.volFrameControls_2.isHidden())
        
    def show_skin_volume_frame(self):
        if self.parent.skin_volume_frame.isHidden():
            self.hide_volume_frame_timer = 0
        else:
            self.hide_volume_frame_timer = 181400
        self.parent.skin_volume_frame.setHidden(not self.parent.skin_volume_frame.isHidden())
        
    def addMenues(self):
        context_menu = QMenu()
        
        # self.create_playlist_action.setText(self.read.get_variable("current playlist"))
        
        context_menu.addAction(self.current_playlist_action)
        context_menu.addAction(self.create_playlist_action)
        context_menu.addSeparator()
        context_menu.addMenu(self.load_playlist_menu_pop)
        context_menu.addAction("friends playlist")
        context_menu.addAction(self.select_playlist_action)
        context_menu.addSeparator()
        context_menu.addAction(self.share_action)
        
        self.parent.newMenu.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.parent.newMenu.setMenu(self.new_menu)
        
        self.parent.togglePlaylist.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)  # Enable context menu
        self.parent.togglePlaylist.setMenu(context_menu)
        
    def update(self):
        if self.player.isPlaying():
            self.parent.startTime.setText(f"{self.conversion.from_milli(self.player.get_pos())}")
            self.parent.endTime.setText(f"{self.conversion.from_milli(self.player.get_total_length())}") #may count down might be implemented later
            self.parent.progressAlt.setValue(round(self.player.get_pos()))
            self.update_slider()
            
            self.change_widgets_after_play()
            
            # if self.audio_array.is_loaded and self.read.get_variable("Show Visualizer", True):
            #     if self.read.get_variable("current visualizer", "Bar") == "Bar":
            #         self.bar_visualizer.setValues(self.audio_array.sample_values(self.player.get_pos()))
                    
            #     # elif self.read.get_variable("current visualizer", "Bar") == "Pulse":
            #     #     self.pulse_visualizer.setValues(self.audio_array.calculate_amps(self.player.get_pos(), self.player.isPlaying()))
            
        if self.read.get_variable("file clicked") is not None:
            self.load_player(forced_play=True)
            self.create.create_variable("file clicked", None)
            
            
        if self.hide_volume_frame_timer < 1800:
            self.hide_volume_frame_timer += 1
        elif not self.parent.volFrameControls_2.isHidden():
            self.parent.volFrameControls_2.setHidden(True)
            
        if not self.parent.skin_volume_frame.isHidden() and self.hide_volume_frame_timer>60:
            self.parent.skin_volume_frame.setHidden(True)
            
        if self.hide_status_frame_timer < 90:
            self.hide_status_frame_timer += 1
        elif not self.parent.statusFrame.isHidden():
            self.parent.statusFrame.setHidden(True)
            
        if self.read.get_variable('current skin') in ['One Button', 'Simple']:
            self.parent.skin_pos_text.display(f"{self.conversion.from_milli(self.player.get_pos())}")
            if self.play_pause_animation_counter > 5:
                if self.player.get_total_length() > 0:
                    self.iconLoader.pause_play_animation(self.player.get_pos()/self.player.get_total_length())
                else:
                    self.iconLoader.pause_play_animation(0)
                self.play_pause_animation_counter = 0
            else:
                self.play_pause_animation_counter += 1  
        
        if self.read.get_variable('current skin') == 'One Button':
            if self.one_button_skin_current_state != self.read.get_variable('one btn auto switch skin', 'auto'):
                if self.read.get_variable('one btn auto switch skin', 'auto') in ['auto', False]:
                    self.one_button_skin_counter += 1
                    if self.one_button_skin_counter > 1200:
                        self.one_button_skin_current_state = self.read.get_variable('one btn auto switch skin', 'auto')
                        self.widgetRemover.one_button_min_state(maximize=False)
                        
                elif self.read.get_variable('one btn auto switch skin', 'auto') == 'min':
                    self.one_button_skin_current_state = self.read.get_variable('one btn auto switch skin', 'auto')
                    self.widgetRemover.one_button_min_state(maximize=False)
                elif self.read.get_variable('one btn auto switch skin', 'auto') == 'max':
                    self.one_button_skin_current_state = self.read.get_variable('one btn auto switch skin', 'auto')
                    self.widgetRemover.one_button_min_state(maximize=True)               
        
            
    def slider_pressed(self):
        self.slider_is_dragged = True
        
    def slider_released(self):
        self.slider_is_dragged = False
        self.player.seek(self.parent.playPos.value())
        self.player.seek(self.parent.skin_progress.value())
        
    def update_slider(self):
        if not self.slider_is_dragged:
            self.parent.playPos.setValue(round(self.player.get_pos()))
            self.parent.skin_progress.setValue(round(self.player.get_pos()))
            
                   
    def customization(self):
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(5)
        self.parent.backgroundPic.setGraphicsEffect(blur)
        
    def change_widgets_after_play(self):
        if self.player.get_load_widgets() and self.player.isPlaying():
            self.parent.playPos.setMaximum(round(self.player.get_total_length()))
            self.parent.skin_progress.setMaximum(round(self.player.get_total_length()))
            self.parent.progressAlt.setMaximum(round(self.player.get_total_length()))
            self.player.set_load_widgets(False)
            
            if self.read.get_variable('virtual playlist', False):
                path = self.read.get_variable('virtual playing path')
            else:
                path = self.read.get_playlistname_attr(self.read.get_variable('current playlist'))['current_audio_path']
            details = self.read.get_file_details(path)
            self.parent.skin_filename.setText(details['title'])
            self.parent.skin_title.setText(details['artist'])
            
        
    
    def change_volume(self, vol=None, unhide=False, is_alt_slider=False):
        if vol is None:
            vol = self.parent.volumeSlider.value()
            self.parent.volSliderAlt.setValue(vol)
            self.parent.skin_volume_slider.setValue(vol)
        else:
            self.parent.volumeSlider.setValue(vol)
            if not is_alt_slider:
                self.parent.volSliderAlt.setValue(vol)
                self.parent.skin_volume_slider.setValue(vol)
        if unhide:
            self.hide_volume_frame_timer=0
            
        if vol > 100:
            vol = 100
        elif vol < 0:
            vol = 0
        self.player.set_volume(vol)
        self.create.create_variable("volume", vol)
        self.parent.volLabel.setText(f"Volume is {vol}%")
        self.create.create_variable("mute", False)
        self.iconLoader.special_icons()
        
        
        
        
    def mute(self):
        self.create.create_variable("volume tmp", self.read.get_variable("volume"))
        if self.read.get_variable("mute") is None:
            self.create.create_variable("mute", False)
            
        if self.read.get_variable("mute"):
            self.create.create_variable("mute", False)
            self.player.set_volume(int(self.read.get_variable("volume tmp")))
            self.create.create_variable("volume", int(self.read.get_variable("volume tmp")))
            self.parent.volLabel.setText(f"Mute is off")
        else:
            self.create.create_variable("mute", True)
            self.player.set_volume(0)
            self.create.create_variable("volume", 0)
            self.parent.volLabel.setText(f"Mute is on")
        self.parent.volumeSlider.setValue(int(self.read.get_variable("volume", 100)))
        self.iconLoader.special_icons()
            
    
    def settings(self):
        if self.read.get_variable('current skin') == 'default':
            self.settings_helper.open_settings()
            
        self.settings_widget = SettingsWidget(self.parent)
        self.settings_widget.reload_skin.connect(lambda: self.skin.update_css(self.read.get_variable('current skin')))
        self.settings_widget.reload_skin.connect(self.iconLoader.load_icons)
        
        self.settings_widget.reset_settings_signal.connect(self.reset_settings)
        self.settings_widget.reset_files_signal.connect(self.reset_files)
        
    def reset_settings(self):
        create_important_variables()
        self.iconLoader.check_colors()
        self.settings_helper.set_skin(self.skin, self.read.get_variable('current skin'))
        self.iconLoader.load_icons()
        
        
    def reset_files(self):
        self.stop_audio(save=False)
        self.iconLoader.load_icons()
        
        
    def open_defaults(self):
        if self.read.get_variable('current skin') == 'default':
            self.settings_helper.open_defaults
        
    def open_playlist(self):
        if self.read.get_variable('current skin') == 'default':
            self.settings_helper.open_playlist()
        else:
            self.playlistTools.alternative_playlist()
        
    def load(self):
        self.isLoading = True
        self.change_volume(int(self.read.get_variable("volume")) if self.read.get_variable("volume") is not None else 100)
        self.iconLoader.load_icons()
        
        if self.read.get_variable("playing") and self.read.get_variable("file clicked") is None:
            self.load_player()
        self.threeAudioCustomize.load_defaults()
        self.threeAudioCustomize.main_playlist_decider()  
        self.threeAudioCustomize.support_playlist_decider()  
        self.open_defaults()
        
        self.load_playlist()
        
        # if self.read.get_variable("current visualizer", "Bar"):
        #     self.set_bar_visualizer()
        # else:
        #     self.set_pulse_visualizer()
        
        
        
        
            
        self.settings_helper.set_skin(self.skin, self.read.get_variable('current skin'))
        if self.read.get_variable('coordinates') is not None:
            val = self.read.get_variable('coordinates').replace('[', '').replace(']', '').replace(' ', '').split(',')
            val = [int(d) for d in val]
            self.parent.setGeometry(*val)
        
        
    def save(self):
        self.save_current_audio_updates()        
        if self.read.get_variable('current playlist'):
            if not self.read.get_variable('virtual playlist', False):
                current_audio = self.read.get_current_file(self.read.get_variable('current playlist'))
                if len(current_audio) > 0:
                    self.update_db.update_current_audio_time(current_audio['playlist_name'], self.player.get_pos())
                    
    def save_current_audio_updates(self):
        if self.read.get_variable('virtual playlist'):
            path = self.read.get_variable('virtual playing path')
            for name in self.read.get_playlistnames_attr():
                details = self.read.get_playlist_file_details(name, path, default=[])
                if len(details) > 0:
                    self.update_db.update_audio_played_times(details['playlist_name'], details['current_audio_path'])
                    self.update_db.update_audio_seconds_played(details['playlist_name'], details['current_audio_path'], time()-self.start_playing_time)
        else:     
            current_audio = self.read.get_current_file(self.read.get_variable('current playlist'))
            if len(current_audio) > 0:
                self.update_db.update_audio_played_times(current_audio['playlist_name'], current_audio['current_audio_path'])
                self.update_db.update_audio_seconds_played(current_audio['playlist_name'], current_audio['current_audio_path'], time()-self.start_playing_time)
        
        
        self.start_playing_time = time()
    
    ## main purpose is to update current playing audio and update playlist relying widgets
    def load_playlist(self):
        current_playlist = self.read.get_variable("current playlist", None)
        playlist_names = self.read.get_playlistnames_attr()
        if current_playlist is None and len(playlist_names) <= 0:
            create_important_variables()
            self.parent.statusLabel.setText("Default playlist has been created")
            self.hide_status_frame_timer = 0
        elif current_playlist is None and len(playlist_names) > 0:
            self.playlistTools.load_playlist_names()
        elif current_playlist is not None:
            details = self.read.get_playlistname_attr(current_playlist) 
            if len(details)>0:   
                self.parent.statusLabel.setText("Loading {} playlist ({}) audio{}"
                    .format(details['playlist_name'], details['files_counter'], "" if details['playlist_name']==1 else "s"))
                self.hide_status_frame_timer = 0
            if self.read.get_variable("playlist created"):
                self.isLoading = True
                self.load_player(forced_play=True)
                self.create.create_variable("playlist created", False)
                self.iconLoader.special_icons()
                
        self.current_playlist_action.setText(self.update_current_playlist())
            
    def login_signup_decider(self):
        self.settings_helper.open_login()
    
    def register_user(self):
        print("Registering ... ")

    def login_user(self):
        print("Login ... ")
                
    def like_audio(self):
        playlist_name, path, like = retrive_current_audio_property('like_audio')
        if like is not None:
            if like == 'Normal':
                like = 'High'
            elif like == 'High':
                like = 'Low'
            elif like == 'Low':
                like = 'Normal'
            else:
                like = 'Normal'
            self.update_db.update_audio_like(playlist_name, path, like)
            self.iconLoader.like_love_star_updater()
    
    def star_audio(self):
        playlist_name, path, star = retrive_current_audio_property('star')
        if star is not None:
            if star < 5:
                star += 1
            else:
                star = 0
            self.update_db.update_audio_star(playlist_name, path, star)
            self.iconLoader.like_love_star_updater()
    
    def like_playlist(self):
        playlist_name, like = retrive_current_playlist_property('like_playlist')
        if like is not None:
            if like == 'Normal':
                like = 'High'
            elif like == 'High':
                like = 'Low'
            elif like == 'Low':
                like = 'Normal'
            else:
                like = 'Normal'
            self.update_db.update_playlist_common_like(playlist_name, like)
            self.iconLoader.like_love_star_updater()
            
    def love_playlist(self):
        playlist_name, love = retrive_current_playlist_property('love_playlist')
        if love is not None:
            self.update_db.update_playlist_common_love(playlist_name, not love)
            self.iconLoader.like_love_star_updater()
        
    def share_playlist(self):
        playlist_name, shared = retrive_current_playlist_property('is_shared')
        if shared is not None:
            self.update_db.update_playlist_common_shared(playlist_name, not shared)
            text = self.share_name_decider()
            
            self.share_action.setText(text)
            self.parent.sharePlaylist.setToolTip(text)
            self.iconLoader.like_love_star_updater()
        
    def share_name_decider(self):
        if self.read.get_variable('virtual playlist'):
            self.share_action.setDisabled(True)
            self.parent.sharePlaylist.setHidden(True)
            return self.read.get_variable('virtual playlist').capitalize() + " Playlist"
        else:
            self.share_action.setDisabled(False)
            self.parent.sharePlaylist.setHidden(False)
            tmp = self.read.get_playlistname_attr(self.read.get_variable("current playlist"), None)
            if tmp is not None:
                name_tmp = tmp["playlist_name"]
                share_tmp = tmp["is_shared"]
                return f"Un-Share {name_tmp} Playlist" if share_tmp else f"Share {name_tmp} Playlist"
        return 'No playlist'
        
    def mouseEnter(self):
        if self.read.get_variable('current skin')=='One Button':
            # self.parent.skin_expand_left.setHidden(False)
            # self.parent.skin_expand_right.setHidden(False)
            # self.parent.skin_minimize.setHidden(False)
            # self.parent.skin_settings.setHidden(False)
            self.one_button_skin_counter=-2000
            if self.read.get_variable('one btn auto switch skin', 'auto') in ['auto', False]:
                self.maximize_one_button_skin()
    
    def mouseLeave(self):
        if self.read.get_variable('current skin')=='One Button':
            # self.parent.skin_expand_left.setHidden(True)
            # self.parent.skin_expand_right.setHidden(True)
            # self.parent.skin_minimize.setHidden(True)
            # self.parent.skin_settings.setHidden(True)
            if self.read.get_variable('one btn auto switch skin', 'auto') in ['auto', False]:
                self.maximize_one_button_skin()
            self.one_button_skin_counter = 800
            self.create.create_variable('coordinates', [self.parent.geometry().x(), self.parent.geometry().y(),
                                            self.parent.geometry().width(), self.parent.geometry().height()])
            
    def maximize_one_button_skin(self):
        if self.read.get_variable('current skin')=='One Button':
            self.widgetRemover.one_button_min_state(maximize=True)
    
    
    def before_quite_application(self):  
        self.create.create_variable('coordinates', [self.parent.geometry().x(), self.parent.geometry().y(),
                                            self.parent.geometry().width(), self.parent.geometry().height()]) 
        if self.read.get_variable('current skin')=='default':     
            self.settings_helper.remove_all()
            self.parent.statusLabel.setText("Exiting the application")
            self.hide_status_frame_timer = 0
        self.shrink.start_shrink(False, True)
        self.player.get_fade_obj().fade_out_complete.connect(self.parent.deleteLater)
        self.player.get_fade_obj().fade_out(800)
        