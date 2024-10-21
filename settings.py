from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QSize
from CSS import SkinCss

class Skin():
    def __init__(self, parent) -> None:
        self.parent = parent
        
    def set_skin(self, name):
        constants = Constants()
        self.parent.setGeometry(*constants.skin(name)['start_pos'], *constants.skin(name)['frame'])
        self.parent.mainFrame.setGeometry(0, 0, *constants.skin(name)['frame'])
        self.parent.backgroundPic.setGeometry(0, 0, *constants.skin(name)['background_pic'])
        self.parent.backgroundPicMask.setGeometry(0, 0, *constants.skin(name)['background_mask'])
        self.update_css(name, constants)
        
        self.parent.show()
        
    def update_css(self, name, constants=None):
        if constants is None:
            constants = Constants()
        self.parent.mainFrame.setStyleSheet(constants.get_skin_css(name))
        
    def skin_names(self):
        return ['default', 'One Button', 'Rounded Bar', "Simple"]
        
class Constants:
    def __init__(self):
        self.skin_css = SkinCss()
    
    def get_skin_css(self, name):
        if name.lower() == 'default':
            val =  self.skin_css.main_frame(name)
        elif name.lower() == 'one button':
            val =  f"{self.skin_css.main_frame(name)} {self.skin_css.label(name)} {self.skin_css.progress_slider(name)}\
                {self.skin_css.mask_label(name)} {self.skin_css.background(name)} {self.skin_css.lcd(name)}"
        elif name.lower() == 'rounded bar':
            val =  f"{self.skin_css.main_frame(name)} {self.skin_css.progress_slider(name)}"
        elif name.lower() == 'simple':
            val = f"{self.skin_css.main_frame(name)} {self.skin_css.lcd(name)} {self.skin_css.label(name)} \
                {self.skin_css.progress_slider(name)} {self.skin_css.mask_label(name)}" 
        return val
        
    def audio_formats(self):
        return ["mp3", "aiff", "wav", "aac", "alac", "amr", "midi", "opus", "ape", "wv", 'mpc', 'spx', 'mod', 's3m', 'it', 'xm', 
                 "au","flac", "ogg", "wma", "mp2", "ac3", "caf", "dts", "mmf", "mid"]
        
    def video_formats(self):
        return {
            'popular': ['mp4', 'mkv', 'avi'],
            'less_popular': ['mov', 'wmv', 'flv', 'webm', '3gp', 'ogg', 'mpeg', 'asf', 'vob', 'mts', 'm2ts', 'rm', 'divx', 'xvid']
            }
        
    def sound_output(self):
        return{'auto': 'default', 'sdl': 'Simple DirectMedia Layer',
               'waveout': 'Windows WaveOut audio output', 'directx': 'DirectX audio output', 'wasapi': 'Windows Audio Session API',
               'spdif': 'Sony/Philips Digital Interface for DTS audio'}
    
    def skin(self, name):
        screen = QGuiApplication.primaryScreen()
        screen = screen.availableGeometry()
        screen_width, screen_height = screen.width(), screen.height()
        
        start_pos = (0, 0)
        frame = (501, 501)
        background_pic = (0, 0)
        background_mask = (0, 00)
        if name=='One Button':
            frame = (381, 141)
            start_pos = (screen_width-frame[0], screen_height-frame[1])
        elif name=='default':
            background_pic = (500, 500)
            background_mask = (500, 500)
        elif name == "Rounded Bar":
            frame = (451, 31)
            start_pos = (screen_width-frame[0], screen_height-frame[1])
        elif name == "Simple":
            frame = (391, 171)
            start_pos = (screen_width-frame[0], screen_height-frame[1])
        
            
        return {
            'start_pos': start_pos,
            'frame': frame,
            'background_pic': background_pic,
            'background_mask': background_mask,
        }
        
    def controlFrame(self):
        return {
            "frame": (0, 420, 501, 51)
        }
        
    def headerFrame(self):
        return {
            "frame": (10, 0, 491, 52)
        }

    def headerFrameAlt(self):
        return {
            "frame": (10, 2, 481, 51)
        }
        
    def loginFrame(self):
        return {
            "frame": (0, 50, 461, 361)
        }
        
    def registerFrame(self):
        return {
            "frame": (20, 59, 451, 351)
        }
        
    def seekFrame(self):
        return {
            "frame": (10, 385, 440, 26),
            "startTime": (0, 3, 51, 20),
            "playPos": (60, 3, 301, 22),
            "endTime": (370, 3, 51, 20)
        }
        
    def seekFrameNew(self):
        return {
            "frame": (30, 470, 421, 31),
            "startTime": (10, 3, 51, 16),
            "playPos": (70, 3, 300, 22),
            "endTime": (380, 3, 51, 20)
        }
        
    def settingsFrame(self):
        return {
            "frame": (0, 50, 501, 351)
        }
        
    def threeAudioFrame(self):
        return {
            "frame": (10, 200, 481, 178)
        }
        
    def visualizerFrame(self):
        return {
            "frame": (10, 70, 481, 121)
        }
        
    def volControlFrame(self):
        return {
            "frame": (30, 470, 451, 31),
        }
        
    def volControlFrameAlt(self):
        return {
            "frame": (448, 220, 51, 195),
        }

    def playlistFrame(self):
        return {
            "frame": (10, 60, 481, 351),
        }
        

class NeonColors():
    
    def neon_1 (self):
        return "qlineargradient(spread:pad, x1:0.476, y1:0, x2:0.483925, y2:1, stop:0 rgba(37, 81, 96, 255), stop:0.309912 \
                rgba(207, 234, 245, 255), stop:0.688833 rgba(207, 234, 245, 255), stop:1 rgba(37, 81, 96, 255))"
                
    def neon_2(self):
        return "qlineargradient(spread:pad, x1:0.505, y1:0.0453182, x2:0.509589, y2:1, stop:0 rgba(74, 15, 10, 255), \
            stop:0.223289 rgba(255, 176, 176, 255), stop:0.776711 rgba(255, 176, 176, 255), stop:1 rgba(74, 15, 10, 255))"
            
    def neon_3(self):
        return "qlineargradient(spread:pad, x1:0.476, y1:0, x2:0.483925, y2:1, stop:0 rgba(122, 244, 236, 255), stop:0.425926\
            rgba(244, 246, 243, 255), stop:0.567901 rgba(244, 246, 243, 255), stop:1 rgba(122, 244, 236, 255))"
            
    def neon_4(self):
        return "qlineargradient(spread:pad, x1:0.476, y1:0, x2:0.483925, y2:1, stop:0 rgba(29, 52, 170, 68), stop:0.226166 \
            rgba(155, 194, 247, 255), stop:0.309912 rgba(250, 255, 255, 255), stop:0.688833 rgba(250, 255, 255, 255), stop:0.778905 \
            rgba(155, 194, 247, 255), stop:1 rgba(29, 52, 170, 68))"
            
    def neon_5(self):
        return "qlineargradient(spread:pad, x1:0.476, y1:0, x2:0.483925, y2:1, stop:0 rgba(121, 0, 0, 255), stop:0.318937 \
            rgba(247, 21, 0, 178), stop:0.418605 rgba(255, 217, 217, 255), stop:0.549834 rgba(255, 217, 217, 255), stop:0.647841 \
            rgba(247, 21, 0, 255), stop:1 rgba(121, 0, 0, 178))"
            
    def neon_6(self):
        return "qlineargradient(spread:pad, x1:0.476, y1:0, x2:0.483925, y2:1, stop:0 rgba(5, 77, 0, 255), stop:0.313905 rgba(0, 247, 16, 178),\
            stop:0.418605 rgba(137, 255, 141, 255), stop:0.549834 rgba(137, 255, 141, 255), stop:0.647841 rgba(0, 247, 16, 255), stop:1\
            rgba(5, 77, 0, 178))"
            
    def neon_7(self):
        return "qlineargradient(spread:pad, x1:0.476, y1:0, x2:0.483925, y2:1, stop:0 rgba(80, 0, 106, 179), stop:0.327039 rgba(247, 0, 255, 255), \
            stop:0.418605 rgba(255, 226, 255, 255), stop:0.549834 rgba(255, 226, 255, 255), stop:0.638627 rgba(247, 0, 255, 255), stop:1 rgba(80, 0, 106, 178))"
    
    def color_1(self):
        return "qlineargradient(spread:pad, x1:0, y1:0.568182, x2:1, y2:0.499, stop:0 rgba(3, 0, 30, 255), stop:0.302486 \
                rgba(115, 3, 192, 255), stop:0.68232 rgba(236, 56, 188, 255), stop:1 rgba(253, 239, 249, 255))"
    def color_2(self):
        return "qlineargradient(spread:pad, x1:0.457, y1:0, x2:0.309, y2:1, stop:0 rgba(222, 88, 88, 255), stop:1 rgba(37, 22, 72, 255))"
    
    def color_3(self):
        return "qlineargradient(spread:pad, x1:0.653, y1:0, x2:0.461, y2:1, stop:0 rgba(92, 53, 207, 255), stop:1 rgba(230, 46, 120, 255))"
    
    def fill_green_quater(self):
        return "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 0, 0, 0), stop:0.329167 rgba(255, 0, 0, 0), stop:0.3475\
            rgba(255, 255, 255, 0), stop:0.6525 rgba(55, 159, 27, 25), stop:0.700833 rgba(82, 216, 102, 55), stop:0.878333 \
            rgba(72, 209, 111, 89), stop:0.9625 rgba(29, 198, 85, 255), stop:1 rgba(0, 255, 103, 148))"
            
    def fill_green(self, percentage, oriantation):
        if percentage <= 0:
            return 
        elif percentage <= 15:
            return 
        elif percentage <= 30:
            return 
        elif percentage <= 45:
            return 
        elif percentage <= 60:
            return 
        elif percentage <= 75:
            return 
        elif percentage <= 90:
            return 
        elif percentage <= 100:
            if oriantation == 0:
                return "qlineargradient(spread:pad, x1:0.5, y1:0.00278552, x2:0.508, y2:0.994429, stop:0 rgba(121, 0, 0, 93), stop:0.318937 \
                    rgba(247, 21, 0, 178), stop:0.429637 rgba(255, 217, 217, 117), stop:0.549834 rgba(255, 217, 217, 138), stop:0.647841 \
                    rgba(247, 21, 0, 172), stop:1 rgba(121, 0, 0, 211))"
            elif oriantation==1:
                return "qlineargradient(spread:pad, x1:0.339, y1:0.252786, x2:0.508, y2:0.994429, stop:0 rgba(121, 0, 0, 93), stop:0.318937 \
                    rgba(247, 21, 0, 178), stop:0.429637 rgba(255, 217, 217, 117), stop:0.549834 rgba(255, 217, 217, 138), stop:0.647841 \
                    rgba(247, 21, 0, 172), stop:1 rgba(121, 0, 0, 211))"
            
            elif oriantation==2:
                return "qlineargradient(spread:pad, x1:0.0463423, y1:0.508, x2:0.508, y2:0.994429, stop:0 rgba(121, 0, 0, 93), stop:0.318937 \
                    rgba(247, 21, 0, 178), stop:0.429637 rgba(255, 217, 217, 117), stop:0.549834 rgba(255, 217, 217, 138), stop:0.647841 \
                    rgba(247, 21, 0, 172), stop:1 rgba(121, 0, 0, 211))"
            elif oriantation==-1:
                return "qlineargradient(spread:pad, x1:0.77, y1:0.297727, x2:0.508, y2:0.994429, stop:0 rgba(121, 0, 0, 93), stop:0.318937 \
                    rgba(247, 21, 0, 178), stop:0.429637 rgba(255, 217, 217, 117), stop:0.549834 rgba(255, 217, 217, 138), stop:0.647841 \
                    rgba(247, 21, 0, 172), stop:1 rgba(121, 0, 0, 211))"
            else:
                return "qlineargradient(spread:pad, x1:0.920129, y1:0.701, x2:0.508, y2:0.994429, stop:0 rgba(121, 0, 0, 93), stop:0.318937 \
                    rgba(247, 21, 0, 178), stop:0.429637 rgba(255, 217, 217, 117), stop:0.549834 rgba(255, 217, 217, 138), stop:0.647841 \
                    rgba(247, 21, 0, 172), stop:1 rgba(121, 0, 0, 211))"                
            
class WidgetRemover():
    def __init__(self, parent):
        self.constants = Constants()
        self.parent = parent
    
    def removeControlFrame(self, restore=False):
        if restore or restore is None:
            a, b, c, d = self.constants.controlFrame()['frame']
            self.parent.controlFrame.setGeometry(a, b, c, d)
        else:
            self.parent.controlFrame.setGeometry(0, 0, 0, 0)
        
    def removeHeaderFrame(self, restore=False):
        if restore or restore is None:
            a, b, c, d = self.constants.headerFrame()['frame']
            self.parent.headerFrame.setGeometry(a, b, c, d)
        else:
            self.parent.headerFrame.setGeometry(0, 0, 0, 0)
            
    def removeHeaderFrameAlt(self, restore=False):
        if restore or restore is None:
            a, b, c, d = self.constants.headerFrameAlt()['frame']
            self.parent.headerFrameAlt.setGeometry(a, b, c, d)
        else:
            self.parent.headerFrameAlt.setGeometry(0, 0, 0, 0)
            
    def removeHeaderFrameForce(self):
        self.parent.headerFrameAlt.setGeometry(0, 0, 0, 0)
        self.parent.headerFrame.setGeometry(0, 0, 0, 0)
        
    def removeLoginFrame(self, restore=False):
        if restore or restore is None:
            a, b, c, d = self.constants.loginFrame()['frame']
            self.parent.loginFrame.setGeometry(a, b, c, d)
        else:
            self.parent.loginFrame.setGeometry(0, 0, 0, 0)
        
    def removeRegisterFrame(self, restore=False):
        if restore or restore is None:
            a, b, c, d = self.constants.registerFrame()['frame']
            self.parent.registerFrame.setGeometry(a, b, c, d)
        else:
            self.parent.registerFrame.setGeometry(0, 0, 0, 0)
        
    def removeSeekFrame(self, restore=False):
        if restore or restore is None:
            a, b, c, d = self.constants.seekFrame()['frame']
            self.parent.seekFrame.setGeometry(a, b, c, d)
            a, b, c, d = self.constants.seekFrame()['startTime']
            self.parent.startTime.setGeometry(a, b, c, d)
            a, b, c, d = self.constants.seekFrame()['playPos']
            self.parent.playPos.setGeometry(a, b, c, d)
            a, b, c, d = self.constants.seekFrame()['endTime']
            self.parent.endTime.setGeometry(a, b, c, d)
        else:
            self.parent.seekFrame.setGeometry(0, 0, 0, 0)
        
    def removeSeekFrameNew(self, restore=False):
        if restore or restore is None:
            a, b, c, d = self.constants.seekFrameNew()['frame']
            self.parent.seekFrame.setGeometry(a, b, c, d)
            a, b, c, d = self.constants.seekFrameNew()['startTime']
            self.parent.startTime.setGeometry(a, b, c, d)
            a, b, c, d = self.constants.seekFrameNew()['playPos']
            self.parent.playPos.setGeometry(a, b, c, d)
            a, b, c, d = self.constants.seekFrameNew()['endTime']
            self.parent.endTime.setGeometry(a, b, c, d)
        else:
            self.parent.seekFrame.setGeometry(0, 0, 0, 0)
            
        
    def removeSettingsFrame(self, restore=False):
        if restore or restore is None:
            a, b, c, d = self.constants.settingsFrame()['frame']
            self.parent.settingsFrame.setGeometry(a, b, c, d)
        else:
            self.parent.settingsFrame.setGeometry(0, 0, 0, 0)
        
    def removeThreeAudioFrame(self, restore=False):
        if restore == False:
            self.parent.threeAudioFrame.setGeometry(0, 0, 0, 0)
        else:
            a, b, c, d = self.constants.threeAudioFrame()['frame']
            self.parent.threeAudioFrame.setGeometry(a, b, c, d)
        
        
    def removeVisualizerFrame(self, restore=False):
        if restore is True or restore is None:
            a, b, c, d = self.constants.visualizerFrame()['frame']
            self.parent.visualizerFrame.setGeometry(a, b, c, d)
        else:
            self.parent.visualizerFrame.setGeometry(0, 0, 0, 0)
            
        
    def removeVolControlFrame(self, restore=False):
        if restore or restore is None:
            a, b, c, d = self.constants.volControlFrame()['frame']
            self.parent.volControlFrame.setGeometry(a, b, c, d)
        else:
            self.parent.volControlFrame.setGeometry(0, 0, 0, 0)
            
    def removeVolControlFrameAlt(self, restore=False):
        if restore or restore is None:
            a, b, c, d = self.constants.volControlFrameAlt()['frame']
            self.parent.volFrame_2.setGeometry(a, b, c, d)
        else:
            self.parent.volFrame_2.setGeometry(0, 0, 0, 0)
            
    def removePlaylistFrame(self, restore=False):
        if restore or restore is None:
            a, b, c, d = self.constants.playlistFrame()['frame']
            self.parent.playlistFrame.setGeometry(a, b, c, d)
        else:
            self.parent.playlistFrame.setGeometry(0, 0, 0, 0)
            
    def removeOtherSkinItems(self):
        self.parent.skin_background.setGeometry(0, 0, 0, 0)
        self.parent.skin_circle.setGeometry(0, 0, 0, 0)
        self.parent.skin_filename.setGeometry(0, 0, 0, 0)
        self.parent.skin_mask_label.setGeometry(0, 0, 0, 0)
        self.parent.skin_menu.setGeometry(0, 0, 0, 0)
        self.parent.skin_next.setGeometry(0, 0, 0, 0)
        self.parent.skin_play.setGeometry(0, 0, 0, 0)
        self.parent.skin_power.setGeometry(0, 0, 0, 0)
        self.parent.skin_prev.setGeometry(0, 0, 0, 0)
        self.parent.skin_progress.setGeometry(0, 0, 0, 0)
        self.parent.skin_title.setGeometry(0, 0, 0, 0)
        self.parent.skin_pos_text.setGeometry(0, 0, 0, 0)

        self.parent.skin_expand_left.setGeometry(0, 0, 0, 0)
        self.parent.skin_expand_right.setGeometry(0, 0, 0, 0)
        self.parent.skin_minimize.setGeometry(0, 0, 0, 0)
        self.parent.skin_settings.setGeometry(0, 0, 0, 0)
        self.parent.skin_window_title.setGeometry(0, 0, 0, 0)
        self.parent.skin_volume_frame.setGeometry(0, 0, 0, 0)
        self.parent.skin_show_volume.setGeometry(0, 0, 0, 0)
        
    def restore_rounded_bar_skin(self):
        self.parent.skin_menu.setGeometry(340, 0, 31, 31)
        self.parent.skin_menu.setIconSize(QSize(31, 31))
        self.parent.skin_next.setGeometry(300, 0, 31, 31)
        self.parent.skin_next.setIconSize(QSize(31, 31))
        self.parent.skin_power.setGeometry(400, 0, 31, 35)
        self.parent.skin_power.setIconSize(QSize(31, 35))
        self.parent.skin_prev.setGeometry(10, 0, 31, 31)
        self.parent.skin_prev.setIconSize(QSize(31, 31))
        self.parent.skin_progress.setGeometry(50, 0, 241, 31)
        
    def restore_simple_skin(self):
        self.parent.skin_circle.setGeometry(150, 110, 61, 61)
        self.parent.skin_circle.setIconSize(QSize(50, 50))
        self.parent.skin_filename.setGeometry(120, 30, 261, 21)
        self.parent.skin_mask_label.setGeometry(157, 117, 46, 46)
        self.parent.skin_menu.setGeometry(10, 124, 31, 31)
        self.parent.skin_menu.setIconSize(QSize(31, 31))
        self.parent.skin_minimize.setGeometry(325, 6, 31, 16)
        self.parent.skin_minimize.setIconSize(QSize(31, 16))
        self.parent.skin_next.setGeometry(211, 124, 31, 31)
        self.parent.skin_next.setIconSize(QSize(31, 31))
        self.parent.skin_play.setGeometry(160, 120, 41, 41)
        self.parent.skin_play.setIconSize(QSize(41, 41))
        self.parent.skin_pos_text.setGeometry(10, 30, 101, 41)
        self.parent.skin_power.setGeometry(360, 0, 24, 24)
        self.parent.skin_power.setIconSize(QSize(24, 24))
        self.parent.skin_prev.setGeometry(117, 124, 31, 31)
        self.parent.skin_prev.setIconSize(QSize(31, 31))
        self.parent.skin_progress.setGeometry(10, 90, 361, 21)
        self.parent.skin_title.setGeometry(120, 50, 261, 20)
        self.parent.skin_window_title.setGeometry(10, 0, 271, 16)
        
        self.parent.skin_volume_frame.setGeometry(350, 0, 31, 131)
        self.parent.skin_show_volume.setGeometry(350, 131, 31, 31)
        
    def restore_one_btn_skin(self):
        self.parent.skin_background.setGeometry(0, 0, 381, 141)
        self.parent.skin_circle.setGeometry(-1, -1, 142, 142)
        self.parent.skin_circle.setIconSize(QSize(142, 142))
        self.parent.skin_filename.setGeometry(150, 10, 191, 20)
        self.parent.skin_mask_label.setGeometry(13, 13, 116, 116)
        self.parent.skin_menu.setGeometry(320, 90, 31, 31)
        self.parent.skin_menu.setIconSize(QSize(31, 31))
        self.parent.skin_next.setGeometry(250, 90, 31, 31)
        self.parent.skin_next.setIconSize(QSize(31, 31))
        self.parent.skin_play.setGeometry(0, 0, 142, 142)
        self.parent.skin_play.setIconSize(QSize(142, 142))
        self.parent.skin_power.setGeometry(160, 90, 31, 35)
        self.parent.skin_power.setIconSize(QSize(31, 35))
        self.parent.skin_prev.setGeometry(210, 90, 31, 31)
        self.parent.skin_prev.setIconSize(QSize(31, 31))
        self.parent.skin_progress.setGeometry(150, 60, 221, 22)
        self.parent.skin_title.setGeometry(148, 30, 201, 20)
        self.parent.skin_pos_text.setGeometry(300, 30, 64, 23)
        self.parent.skin_expand_left.setGeometry(120, 240, 21, 41)
        self.parent.skin_expand_right.setGeometry(280, 240, 21, 41)
        self.parent.skin_minimize.setGeometry(280, 280, 31, 16)
        self.parent.skin_settings.setGeometry(280, 210, 31, 31)
        self.one_button_min_state(maximize=True)
        
            
            
    def one_button_min_state(self, maximize=False):
        if maximize:
            # self.parent.skin_expand_left.setHidden(True)
            # self.parent.skin_expand_right.setHidden(True)
            # self.parent.skin_minimize.setHidden(True)
            # self.parent.skin_settings.setHidden(True)
            self.parent.skin_background.setGeometry(0, 0, 381, 141)
            self.parent.mainFrame.setGeometry(0, 0, 381, 141)
            # self.parent.move(self.parent.geometry().x()-141, self.parent.geometry().y())
        else:
            self.parent.skin_background.setGeometry(0, 0, 141, 141)
            self.parent.mainFrame.setGeometry(0, 0, 141, 141)
            # self.parent.move(self.parent.geometry().x()+141, self.parent.geometry().y())
            
            
            self.parent.skin_expand_left.setGeometry(120, 240, 21, 41)
            self.parent.skin_expand_right.setGeometry(280, 240, 21, 41)
            self.parent.skin_minimize.setGeometry(280, 280, 31, 16)
            self.parent.skin_settings.setGeometry(280, 210, 31, 31)
        
            
        
        
        
    