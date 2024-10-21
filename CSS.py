from read_db import Read

class SkinCss:
    def __init__(self):
        self.read_db = Read()
    
    def main_frame(self, name):
        val = ''
        if name.lower() in ['one button', 'default']:
            val = """background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.830727, y2:0.938, stop:0 rgba(164, 17, 49, 37), 
                stop:0.506266 rgba(164, 17, 107, 51), stop:0.729323 rgba(127, 49, 183, 70), stop:1 rgba(42, 33, 175, 24));
                border-bottom-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(0, 0, 0, 255), stop:0.05 
                rgba(14, 8, 73, 255), stop:0.36 rgba(28, 17, 145, 255), stop:0.6 rgba(126, 14, 81, 255), stop:0.75 rgba(234, 11, 11, 255), 
                stop:0.79 rgba(244, 70, 5, 255), stop:0.86 rgba(255, 136, 0, 255), stop:0.935 rgba(239, 236, 55, 255)); border-right-color: 
                qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(0, 0, 0, 255), stop:0.05 rgba(14, 8, 73, 255), stop:0.36 
                rgba(28, 17, 145, 255), stop:0.6 rgba(126, 14, 81, 255), stop:0.75 rgba(234, 11, 11, 255), stop:0.79 rgba(244, 70, 5, 255), 
                stop:0.86 rgba(255, 136, 0, 255), stop:0.935 rgba(239, 236, 55, 255)); border-left-color: qlineargradient(spread:pad, 
                x1:0.0229121, y1:0.142, x2:1, y2:0, stop:0 rgba(233, 12, 12, 77), stop:0.0769231 rgba(255, 0, 62, 71), stop:0.372253 
                rgba(255, 0, 164, 71), stop:1 rgba(255, 255, 255, 54)); border-radius: 70px;border-width: 1;border-style: solid;"""    
        
        elif name.lower() == 'rounded bar':
            val = f"""background-color: {self.read_db.get_variable("rounded-bar color 1")}; border-radius: 15px; border: 2px solid 
            {self.read_db.get_variable("rounded-bar color 2")};"""
            
        elif name.lower() == 'simple':
            val = f"""background-color: qlineargradient(spread:pad, x1:0.168048, y1:0.085, x2:0.886685, y2:0.932, stop:0 
            {self.read_db.get_variable("simple color 1")}, stop:0.34598 {self.read_db.get_variable("simple color 2")}, stop:0.485998 
            {self.read_db.get_variable("simple color 3")}, stop:0.566396 {self.read_db.get_variable("simple color 4")}, stop:0.706414 
            {self.read_db.get_variable("simple color 5")}, stop:1 {self.read_db.get_variable("simple color 6")}); border-radius: 15px; 
            border: 2px dotted {self.read_db.get_variable("simple border color")};"""
        if val == '':
            return ""
        return f"#mainFrame {self.__add_paranthesis__(val)}"
    
    def lcd(self, name):
        val = ""
        if name.lower() == 'simple':
            val = f"""color: {self.read_db.get_variable("simple lcd color")};"""
            
        elif name.lower() == 'one button':
            val = f"""border: 1px dotted {self.read_db.get_variable("one button btn color")}; color: 
                {self.read_db.get_variable("one button label color")};"""
            
        if val == '':
            return ""
        return f"QLCDNumber {self.__add_paranthesis__(val)}"
    
    def label(self, name):
        val = ''
        if name.lower() == 'simple':
            val = f"""color: {self.read_db.get_variable("simple label color")};"""
        elif name.lower() == 'one button':
            val = f"""color: {self.read_db.get_variable("one button label color")};"""
        if val == '':
            return ""
        return f"QLabel {self.__add_paranthesis__(val)}"
    
    def progress_slider(self, name):
        val = ''
        if name.lower() == 'simple':
            val = "#skin_progress::groove:horizontal "
            val += self.__add_paranthesis__(
                f"""background: qlineargradient(spread:pad, x1:0, y1:0.477273, x2:1, y2:0.443, stop:0 
                {self.read_db.get_variable("simple progress groove color 1")}, stop:1 
                {self.read_db.get_variable("simple progress groove color 2")}); border: 1px solid 
                {self.read_db.get_variable("simple progress groove border color")}; height: 10px;  margin: 1px; border-radius: 5px;"""
            )
            val += "\n#skin_progress::handle:horizontal "
            val += self.__add_paranthesis__(
                f"""background: qradialgradient(cx:0.5, cy:0.5, radius: 1, fx:0.5, fy:0.5, stop:0 
                {self.read_db.get_variable("simple progress handle color 1")}, stop:1 
                {self.read_db.get_variable("simple progress handle color 2")}); width: 16px; height: 8px; margin: -5px 0; border-radius: 8px;"""
            )
            val += "\n#skin_progress::sub-page:horizontal"
            val += self.__add_paranthesis__(
                f"""background: qlineargradient(spread:pad, x1:0, y1:0.477273, x2:1, y2:0.443, stop:0 
                {self.read_db.get_variable("simple progress sub-page color 1")}, stop:1 
                {self.read_db.get_variable("simple progress sub-page color 2")}); border: 1px solid 
                {self.read_db.get_variable("simple progress sub-page background color")}; height: 4px;"""
            )
            
        elif name.lower() == 'one button':
            val = "#skin_progress::groove:horizontal "
            val += self.__add_paranthesis__(
                f"""background: qlineargradient(spread:pad, x1:0, y1:0.477273, x2:1, y2:0.443, stop:0 
                {self.read_db.get_variable("one button progress groove color 1")}, stop:1 
                {self.read_db.get_variable("one button progress groove color 2")}); border: 1px solid 
                {self.read_db.get_variable("one button progress groove border color")}; height: 10px;  margin: 1px; border-radius: 5px;"""
            )
            val += "\n#skin_progress::handle:horizontal "
            val += self.__add_paranthesis__(
                f"""background: qradialgradient(cx:0.5, cy:0.5, radius: 1, fx:0.5, fy:0.5, stop:0 
                {self.read_db.get_variable("one button progress handle color 1")}, stop:1 
                {self.read_db.get_variable("one button progress handle color 2")}); width: 16px; height: 8px; margin: -5px 0; border-radius: 8px;"""
            )
            val += "\n#skin_progress::sub-page:horizontal"
            val += self.__add_paranthesis__(
                f"""background: qlineargradient(spread:pad, x1:0, y1:0.477273, x2:1, y2:0.443, stop:0 
                {self.read_db.get_variable("one button progress sub-page color 1")}, stop:1 
                {self.read_db.get_variable("one button progress sub-page color 2")}); border: 1px solid 
                {self.read_db.get_variable("one button progress sub-page background color")}; height: 4px;"""
            )
            
        elif name.lower() == 'rounded bar':
            val = "#skin_progress::groove:horizontal "
            val += self.__add_paranthesis__(
                f"""border: 1px solid {self.read_db.get_variable("rounded bar progress groove border color")};height: 10px; background: 
                qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {self.read_db.get_variable("rounded bar progress groove color 1")}, stop:1 
                {self.read_db.get_variable("rounded bar progress groove color 2")});"""
            )
            val += "\n#skin_progress::handle:horizontal "
            val += self.__add_paranthesis__(
                f"""background: qradialgradient(cx:0.3, cy:0.3, radius: 1.5, fx:0.3, fy:0.3, stop:0 {self.read_db.get_variable
                ("rounded bar progress handle color 1")}, stop:1 {self.read_db.get_variable("rounded bar progress handle color 2")});
                width: 20px;height: 20px;margin: -5px 0;border-radius: 10px;"""
            )
        return val
        
    def mask_label(self, name):
        val = ''
        if name.lower()=='simple':
            val = f"""border-radius: 23px; background-color: {self.read_db.get_variable("simple mask-label color")};"""
        elif name.lower() == 'one button':
            val = f"""border-radius: 57px; background-color: {self.read_db.get_variable("one button mask-label color")};"""

        if val == '':
            return ""
        return f"#skin_mask_label {self.__add_paranthesis__(val)}"
    
    def background(self, name):
        val = ''
        if name.lower() in ['one button', 'default']:
            val = self.__add_paranthesis__(f"""background-color: {self.read_db.get_variable("default background color")};""")
        if val == '':
            return ""
        return f"#skin_background {val}"
    
    def __add_paranthesis__(self, val):
        if val == '':
            return ""
        return "{" + val + "}"
    