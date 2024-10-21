from PyQt6.QtWidgets import QMainWindow, QApplication, QFrame, QPushButton, QGraphicsDropShadowEffect, QColorDialog
import sys
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6 import uic
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon, QColor
from SVG import change_color
from Helper import res, get_cwd, get_widget_coordinates, set_label_pixmap
from read_db import Read
from create_update_db import Create
from update_db import Update
from CheckBox import AnimatedToggle
import os

from Settings_Classes import Skin, Files, Player, Reset

class SettingsBtn(QFrame):
    clicked = pyqtSignal(str)
    def __init__(self, parent, name, desc, path, x, y, width, height):
        super().__init__()
        self.name = name
        self.setGeometry(x, y, width, height)
        uic.loadUi(get_cwd() + '/settings_btn.ui', self)
        self.setParent(parent)
        self.show()
        
        self.title.setText(name)
        self.desc.setText(desc)
        path = f"{res()}/Images/{path}"
        if os.path.exists(path):
            set_label_pixmap(self.picture, path, True)
        
        
    def mousePressEvent(self, event):
        self.clicked.emit(self.name)
        
class Button(QPushButton):
    render_signal = pyqtSignal()
    reset_settings_signal = pyqtSignal()
    reset_files_signal = pyqtSignal()
    def __init__(self, parent, text, x, y, args={}):
        super().__init__()
        self.setText(text)
        self.setGeometry(x, y, 220, 40)
        self.setParent(parent)
        self.parent = parent
        self.args = args
        self.read = Read()
        self.create_db = Create()
        self.update_db = Update()
        self.styles()
        self.shadow()
        self.show()
        self.clicked.connect(self.save_data)
        
    def shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(shadow)

    def styles(self):
        val = 'border-radius: 20px;'
        if self.args['type'] in ['color']:
            color = QColor(self.read.get_variable(self.args['save_name'], '#08B1F0'))
            val += ('background-color:'+self.read.get_variable(self.args['save_name'], '#08B1F0')+';')
            if color.red()+color.green()+color.blue() < 200:
                val += 'color: white;'
            else:
                val += 'color: #121212;'
        elif self.args['type'] in ['reset']:
            val += 'background-color:red; color: black;'
        else:
            val += ('background-color: #08B1F0;')
            val += 'color: #121212;'
        hover = "background-color: transparent; color:#DD0808; border: 1px solid #DD0808;"
        pressed = "background-color: #08F383; color:#121212; border: 1px solid #121212;"
        self.setStyleSheet(
            f"""
            QPushButton {self.paran(val)}
            QPushButton:hover {self.paran(hover)}
            QPushButton:pressed {self.paran(pressed)}
            """
        )
    def paran(self, val):
        return "{"+val+"}"
        
    def save_data(self):
        if self.args['type'] == 'color':
            self.choose_color()
        elif self.args['type'] == 'reset':
            self.reset()
    
    def reset(self):
        if self.args['save_name']=='settings':
            self.update_db.remove_variable_table()
            self.reset_settings_signal.emit()
        elif self.args['save_name']=='files':
            self.update_db.remove_playlist_table()
            self.reset_files_signal.emit()
        elif self.args['save_name']=='all':
            self.update_db.remove_playlist_table()
            self.update_db.remove_variable_table()
            
            self.reset_settings_signal.emit()
            self.reset_files_signal.emit()
    
    
    def choose_color(self):
        current_color = QColor(self.read.get_variable(self.args['save_name'], '#08B1F0'))
        if not current_color.isValid():
            current_color = QColor("#08B1F0")
            
        color_dialog = QColorDialog(self)
        color = color_dialog.getColor(current_color, self.parent, "Choose Color")
        
        if color.isValid():
            self.create_db.create_variable(self.args['save_name'], color.name())
            self.render_signal.emit()
        
class LeftWidgetBtn(QFrame):
    clicked = pyqtSignal(str)
    def __init__(self, parent, name, path, x, y, width, height):
        super().__init__()
        self.name = name
        self.setGeometry(x, y, width, height)
        uic.loadUi(get_cwd() + '/settings_btn_2.ui', self)
        self.setParent(parent)
        self.show()
        
        self.title.setText(name)
        path = f"{res()}/Images/{path}"
        if os.path.exists(path):
            set_label_pixmap(self.picture, path, True)
        
        
    def mousePressEvent(self, event):
        self.clicked.emit(self.name)
    

class SettingsWidget(QMainWindow, QObject):
    reload_skin = pyqtSignal()
    reset_settings_signal = pyqtSignal()
    reset_files_signal = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__()
        self.move_window_flag = None # to avoid errors
        uic.loadUi(get_cwd() + '/settings_frame.ui', self)
        self.setWindowFlags( Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.create_db = Create()
        self.read_db = Read()
        self.update_db = Update()
        self.parent = parent
        self.displaying_items = []
        self.init_buttons()
        self.show()
        
        self.all_categories = [Skin, Files, Player, Reset]
        self.current_item = None
        self.home()
        if parent is not None:
            self.setGeometry(*get_widget_coordinates(parent.geometry(), self.geometry(), 'side'))
            parent.destroyed.connect(self.deleteLater)
        

    def __open_clicked_btn__(self, name):
        all_items = self.all_categories if self.current_item is None else self.current_item.subclasses
        for item in all_items:
            item = item()
            if item.name==name:
                self.current_item = item
                self.setWindowTitle(name.capitalize()+' Settings')
                self.titleLabel.setText(name.capitalize()+' Settings')
                break
            
        self.render()
        
    def render(self):
        self.clear_display()
        if self.current_item is None:
            x, y = 10, 100
            for item in self.all_categories:
                if item == 'space':
                    x=10
                    y+=60
                else:
                    item = item()
                    btn = SettingsBtn(self, item.name, item.description, item.path, x, y, 301, 51)
                    btn.clicked.connect(self.__open_clicked_btn__)
                    self.displaying_items.append(btn)
                    if x>=311:
                        y+=60
                        x=10
                    else:
                        x+=311
                
            
        else:
            y = 100
            for item in self.current_item.subclasses:
                if item == 'space':
                    y+=40
                else:
                    item = item()
                    btn = LeftWidgetBtn(self, item.name, item.path, 10, y, 181, 31)
                    btn.clicked.connect(self.__open_clicked_btn__)
                    self.displaying_items.append(btn)
                    y+=40
                
            x, y = 200, 100
            for item in self.current_item.items:
                if item['widget'] == 'checkbox':
                    toggler = AnimatedToggle(self, checked_color="#00DD63", pulse_checked_color="#44FFB000", name=item['name'], 
                                            x=x, y=y, save_name=item['save_name'], save_value=item['save_value'])
                    toggler.setFixedSize(toggler.sizeHint())
                    toggler.clicked.connect(lambda: self.save_item(self.sender().save_name, self.sender().save_value, self.sender().isChecked()))
                    toggler.setChecked(self.read_db.get_variable(item['save_name'], False)==item['save_value'])
                    self.displaying_items.append(toggler)
                    self.displaying_items.append(toggler.label)
                elif item['widget'] == 'btn':
                    btn = Button(self, item['name'], x, y, item['args'])
                    btn.render_signal.connect(self.render)
                    if item['args']['type'] == 'color':
                        btn.render_signal.connect(self.reload_skin.emit)
                    elif item['args']['type'] == 'reset':
                        btn.reset_settings_signal.connect(self.reset_settings_signal.emit)
                        btn.reset_files_signal.connect(self.reset_files_signal.emit)
                    self.displaying_items.append(btn)
                    
                if x>=400:
                    y+=50
                    x=200
                else:
                    x=430
                if item['widget'] == 'space':
                    y+=40
                    x=200
                
        self.__main_widgets__()
        
    def clear_display(self):
        for item in self.displaying_items:
            item.close()
            item.deleteLater()
        self.displaying_items.clear()
    
    def __main_widgets__(self):
        if self.current_item is None:
            self.leftLabel.setHidden(True)
            self.backBtn.setHidden(True)
            self.titleLabel.setText("BE Player Settings")
            self.titleLabel.setGeometry(10, 50, 640, 41)
        else:
            self.leftLabel.setHidden(False)
            self.backBtn.setHidden(False)
            self.titleLabel.setGeometry(200, 50, 451, 41)
            
    def home(self):
        self.current_item = None
        self.render()
        
    def save_item(self, save_name, save_value, checked):
        if checked:
            self.create_db.create_variable(save_name, save_value)
        else:
            self.create_db.create_variable(save_name, False)
        self.render()
     
    def init_buttons(self):
        self.backBtn.clicked.connect(self.home)
        self.closeBtn.clicked.connect(self.deleteLater)
        self.minBtn.clicked.connect(self.showMinimized)
        
        self.backBtn.setIcon(QIcon(change_color(res()+"/Icons/home.svg", fill='transparent', stroke='#0F0E15')))
        self.closeBtn.setIcon(QIcon(change_color(res()+"/Icons/x.svg", fill='transparent', stroke='#C2242D')))
        self.minBtn.setIcon(QIcon(change_color(res()+"/Icons/minus.svg", fill='transparent', stroke='#487DFC')))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.move_window_flag = True
            self.m_position = event.globalPosition().toPoint() - self.pos()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if Qt.MouseButton.LeftButton and self.move_window_flag:            
            self.move(event.globalPosition().toPoint() - self.m_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.move_window_flag = False
        self.m_position = QPoint()
       
       
       
       

if __name__ == "__main__":   
    app = QApplication(sys.argv)
    window = SettingsWidget()
    app.exec()