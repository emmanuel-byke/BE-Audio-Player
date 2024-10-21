from settings import Constants

class Skin:
    def __init__(self):
        self.name = 'Skin'
        self.description = 'change colors, behaviours'
        self.path = 'default skin.png'
        self.group = 'skin'
        self.subclasses = [Skin_Simple, Skin_OneBtn, Skin_Default, Skin_Rounded_Bar]
        self.items = [
            {'name': 'transparent', 'widget': 'checkbox', 'save_value': 'one btn transparent', 'save_name':'transparent'},
            
            ]
        
class Skin_OneBtn:
    def __init__(self):
        self.name = 'One Button Skin'
        # self.description = 'change colors, behaviours'
        self.path = 'one btn skin.png'
        self.group = 'skin'
        self.subclasses = [Skin, Skin_OneBtn_Colors]
        self.items = [
            {'name': 'auto switch skin', 'widget': 'checkbox', 'save_value': 'auto', 'save_name': 'one btn auto switch skin'},
            {'name': 'stay mini skin', 'widget': 'checkbox', 'save_value': 'min', 'save_name': 'one btn auto switch skin'},
            {'name': 'stay max skin', 'widget': 'checkbox', 'save_value': 'max', 'save_name': 'one btn auto switch skin'},
        ]
        
class Skin_OneBtn_Colors:
    def __init__(self):
        self.name = 'Change Colors'
        self.path = 'change colors.png'
        self.group = 'skin'
        self.subclasses = [Skin, Skin_OneBtn]
        self.items = [
            {'name': 'Font Color', 'widget': 'btn', 'args': {'save_name':'one button label color', 'type': 'color'}},
            {'name': 'inside Play btn Color', 'widget': 'btn', 'args': {'save_name':'one button mask-label color', 'type': 'color'}},
            {'name': 'Widget colors', 'widget': 'btn', 'args': {'save_name':'one button btn color', 'type': 'color'}},
            {'name': 'Progress Handle Inner Color', 'widget': 'btn', 'args': {'save_name':'one button progress handle color 1', 'type': 'color'}},
            {'name': 'Progress Handle Outer Color', 'widget': 'btn', 'args': {'save_name':'one button progress handle color 2', 'type': 'color'}},
            {'name': 'Progress left-groove Start Color', 'widget': 'btn', 'args': {'save_name':'one button progress sub-page color 1', 'type': 'color'}},
            {'name': 'Progress left-groove End Color', 'widget': 'btn', 'args': {'save_name':'one button progress sub-page color 2', 'type': 'color'}},
            {'name': 'Progress left-groove Border Color', 'widget': 'btn', 'args': {'save_name':'one button progress sub-page background color', 'type': 'color'}},
            {'name': 'Progress right-groove Start Color', 'widget': 'btn', 'args': {'save_name':'one button progress groove color 1', 'type': 'color'}},
            {'name': 'Progress right-groove End Color', 'widget': 'btn', 'args': {'save_name':'one button progress groove color 2', 'type': 'color'}},
            {'name': 'Progress right-groove Border Color', 'widget': 'btn', 'args': {'save_name':'one button progress groove border color', 'type': 'color'}},
        ]
        
class Skin_Default:
    def __init__(self):
        self.name = 'Default Skin'
        # self.description = 'change colors, behaviours'
        self.path = 'default skin.png'
        self.group = 'skin'
        self.subclasses = [Skin, Skin_Default_Colors]
        self.items = [
            {'name': 'Default Header', 'widget': 'checkbox', 'save_name': 'Show Header', 'save_value':True},
            {'name': 'Visualizer', 'widget': 'checkbox', 'save_name': 'Show Visualizer', 'save_value':True},
            {'name': 'Controls', 'widget': 'checkbox', 'save_name': 'Show Controls', 'save_value':True},
            {'name': 'Seek Controls', 'widget': 'checkbox', 'save_name': 'Show Seek Controls', 'save_value':True},
            {'name': 'Move Seek Controls', 'widget': 'checkbox', 'save_name': 'Move Seek Controls', 'save_value':True},
            {'name': 'Audio Selector', 'widget': 'checkbox', 'save_name': 'Show Audio Selector', 'save_value':True},
            {'name': 'Volume Controls', 'widget': 'checkbox', 'save_name': 'Show Volume Controls', 'save_value':True},
            {'name': 'space', 'widget': 'space'},
            {'name': 'Logo 1', 'widget': 'checkbox', 'save_name': 'logo', 'save_value':'Logo 1'},
            {'name': 'Logo 2', 'widget': 'checkbox', 'save_name': 'logo', 'save_value':'Logo 2'},
            {'name': 'Logo 3', 'widget': 'checkbox', 'save_name': 'logo', 'save_value':'Logo 3'},
            {'name': 'Logo 4', 'widget': 'checkbox', 'save_name': 'logo', 'save_value':'Logo 4'},
            {'name': 'Logo 5', 'widget': 'checkbox', 'save_name': 'logo', 'save_value':'Logo 5'},
        ]
        
class Skin_Default_Colors:
    def __init__(self):
        self.name = 'Change Colors'
        self.path = 'change colors.png'
        self.group = 'skin'
        self.subclasses = [Skin, Skin_Default]
        self.items = [
            {'name': 'Background Color', 'widget': 'btn', 'args': {'save_name':'default background color', 'type': 'color'}},
        ]
        
        
class Skin_Rounded_Bar:
    def __init__(self):
        self.name = 'Rounded Bar Skin'
        self.path = 'Rounded Skin.png'
        self.group = 'skin'
        self.subclasses = [Skin, Skin_Rounded_Bar_Colors]
        self.items = [
            
        ]
        
class Skin_Rounded_Bar_Colors:
    def __init__(self):
        self.name = 'Change Colors'
        self.path = 'change colors.png'
        self.group = 'skin'
        self.subclasses = [Skin, Skin_Default]
        self.items = [
            {'name': 'Frame Color', 'widget': 'btn', 'args': {'save_name':'rounded-bar color 1', 'type': 'color'}},
            {'name': 'Border Color', 'widget': 'btn', 'args': {'save_name':'rounded-bar color 2', 'type': 'color'}},
            {'name': 'Progress Groove Start Color', 'widget': 'btn', 'args': {'save_name':'rounded bar progress groove color 1', 'type': 'color'}},
            {'name': 'Progress Groove End Color', 'widget': 'btn', 'args': {'save_name':'rounded bar progress groove color 2', 'type': 'color'}},
            {'name': 'Progress Groove Border Color', 'widget': 'btn', 'args': {'save_name':'rounded bar progress groove border color', 'type': 'color'}},
            {'name': 'Progress Handle Start Color', 'widget': 'btn', 'args': {'save_name':'rounded bar progress handle color 1', 'type': 'color'}},
            {'name': 'Progress Handle End Color', 'widget': 'btn', 'args': {'save_name':'rounded bar progress handle color 2', 'type': 'color'}},
            {'name': 'Widget Color', 'widget': 'btn', 'args': {'save_name':'rounded bar btn color', 'type': 'color'}},
        ]
        
class Skin_Simple:
    def __init__(self):
        self.name = 'Simple Skin'
        self.path = 'simple skin.png'
        self.group = 'skin'
        self.subclasses = [Skin, Skin_Simple_Colors]
        self.items = [
            
        ]
        
class Skin_Simple_Colors:
    def __init__(self):
        self.name = 'Change Colors'
        self.path = 'change colors.png'
        self.group = 'skin'
        self.subclasses = [Skin, Skin_Simple]
        self.items = [
            {'name': 'Frame Top Left Color', 'widget': 'btn', 'args': {'save_name':'simple color 1', 'type': 'color'}},
            {'name': 'Frame Inner Top Left Color', 'widget': 'btn', 'args': {'save_name':'simple color 2', 'type': 'color'}},
            {'name': 'Frame Top Diagonal Color', 'widget': 'btn', 'args': {'save_name':'simple color 3', 'type': 'color'}},
            {'name': 'Frame Bottom Diagonal Color', 'widget': 'btn', 'args': {'save_name':'simple color 4', 'type': 'color'}},
            {'name': 'Frame Inner Bottom Right Color', 'widget': 'btn', 'args': {'save_name':'simple color 5', 'type': 'color'}},
            {'name': 'Frame Bottom Right Color', 'widget': 'btn', 'args': {'save_name':'simple color 6', 'type': 'color'}},
            {'name': 'Border Color', 'widget': 'btn', 'args': {'save_name':'simple border color', 'type': 'color'}},
            {'name': 'LCD Font Color', 'widget': 'btn', 'args': {'save_name':'simple lcd color', 'type': 'color'}},
            {'name': 'Font Color', 'widget': 'btn', 'args': {'save_name':'simple label color', 'type': 'color'}},
            {'name': 'Handle Inner Color', 'widget': 'btn', 'args': {'save_name':'simple progress handle color 1', 'type': 'color'}},
            {'name': 'Handle Outer Color', 'widget': 'btn', 'args': {'save_name':'simple progress handle color 2', 'type': 'color'}},
            {'name': 'Inside Play Button Color', 'widget': 'btn', 'args': {'save_name':'simple mask-label color', 'type': 'color'}},
            {'name': 'Widget Color', 'widget': 'btn', 'args': {'save_name':'simple btn color', 'type': 'color'}},
            {'name': 'Progress Left-Groove Start Color', 'widget': 'btn', 'args': {'save_name':'simple progress sub-page color 1', 'type': 'color'}},
            {'name': 'Progress Left-Groove End Color', 'widget': 'btn', 'args': {'save_name':'simple progress sub-page color 2', 'type': 'color'}},
            {'name': 'Progress Left-Groove Boorder Color', 'widget': 'btn', 'args': {'save_name':'simple progress sub-page background color', 'type': 'color'}},
            {'name': 'Progress Right-Groove Start Color', 'widget': 'btn', 'args': {'save_name':'simple progress groove color 1', 'type': 'color'}},
            {'name': 'Progress Right-Groove End Color', 'widget': 'btn', 'args': {'save_name':'simple progress groove color 2', 'type': 'color'}},
            {'name': 'Progress Right-Groove Border Color', 'widget': 'btn', 'args': {'save_name':'simple progress groove border color', 'type': 'color'}},
        ]
        
        
        
        
        
        
class Files:
    def __init__(self):
        self.name = 'Files'
        self.description = 'sort, playlist behaviours'
        self.path = 'folder.png'
        self.group = 'files'
        self.subclasses = [Files_Formats, Files_Adding, Files_Sort]
        self.items = [
            {'name': 'filter small files', 'widget': 'checkbox', 'save_name': 'filter', 'save_value':True},
            {'name': 'Auto Play Last File', 'widget': 'checkbox', 'save_name': 'Auto Load', 'save_value':True},
            {'name': 'add all files', 'widget': 'button'},
            ]       
        
class Files_Adding:
    def __init__(self):
        self.name = 'Adding Files'
        # self.description = 'change colors, behaviours'
        self.path = 'filenew.png'
        self.group = 'skin'
        self.subclasses = [Files]
        self.items = [
            {'name': 'As Last Item', 'widget': 'checkbox', 'save_name': "Adding Files", 'save_value':'Last'},
            {'name': 'As First Item', 'widget': 'checkbox', 'save_name': "Adding Files", 'save_value':'First'},
            {'name': 'Play from playlist', 'widget': 'checkbox', 'save_name': "Adding Files", 'save_value':'Playlist'},
            {'name': 'Clear Old List', 'widget': 'checkbox', 'save_name': "Adding Files", 'save_value':'Clear'},
        ]
        
class Files_Sort:
    def __init__(self):
        self.name = 'Sorting Files'
        # self.description = 'change colors, behaviours'
        self.path = 'sort_2.png'
        self.group = 'skin'
        self.subclasses = [Files]
        self.items = [
            {'name': 'File Name', 'widget': 'checkbox', 'save_name': "Sortby", 'save_value':'File Name'},
            {'name': 'Title', 'widget': 'checkbox', 'save_name': "Sortby", 'save_value':'Title'},
            {'name': 'Artist', 'widget': 'checkbox', 'save_name': "Sortby", 'save_value':'Artist'},
            {'name': 'Album', 'widget': 'checkbox', 'save_name': "Sortby", 'save_value':'Album'},
            {'name': 'Path', 'widget': 'checkbox', 'save_name': "Sortby", 'save_value':'Path'},
            {'name': 'Size', 'widget': 'checkbox', 'save_name': "Sortby", 'save_value':'Size'},
            {'name': 'Duration', 'widget': 'checkbox', 'save_name': "Sortby", 'save_value':'Duration'},
            {'name': 'space', 'widget': 'space'},
            {'name': 'Descending', 'widget': 'checkbox', 'save_name': "Order", 'save_value':True},
        ]
        
class Files_Formats:
    def __init__(self):
        self.name = 'Allowed Formats'
        self.path = 'mp3_format.jpg'
        self.group = 'skin'
        self.subclasses = [Files]
        self.items = [
            {'name': 'Un-popular Audio', 'widget': 'checkbox', 'save_name': 'Unpopular Audio', 'save_value':True},
            {'name': 'popular Video', 'widget': 'checkbox', 'save_name': 'popular Video', 'save_value':True},
            {'name': 'un-popular Video', 'widget': 'checkbox', 'save_name': 'un-popular Video', 'save_value':True},
        ]
        
        
        
        
class Player:
    def __init__(self):
        self.name = 'Player'
        self.description = 'fade, effects'
        self.path = 'player.png'
        self.group = 'files'
        self.subclasses = [Player_Output]
        self.items = [
                {'name': 'Fade In', 'widget': 'checkbox', 'save_name': 'FadeIn', 'save_value':True},
                {'name': 'Increase Speed', 'widget': 'checkbox', 'save_name': 'Increase Speed', 'save_value':True},
                {'name': 'Fade Out', 'widget': 'checkbox', 'save_name': 'FadeOut', 'save_value':True},
                {'name': 'Reduce Speed', 'widget': 'checkbox', 'save_name': 'Reduce Speed', 'save_value':True},
            ]   

class Player_Output:
    def __init__(self):
        self.name = 'Output Options'
        self.path = 'player_out.png'
        self.group = 'skin'
        self.subclasses = [Player]
        self.items = []
        const = Constants()
        for key in const.sound_output().keys():
            self.items.append({'name': key, 'widget': 'checkbox', 'save_name': "Sound output", 'save_value':key})



class Reset:
    def __init__(self):
        self.name = 'Reset'
        self.description = 'restore configurations to defaults'
        self.path = 'reset.png'
        self.group = 'files'
        self.subclasses = []
        self.items = [
                {'name': 'Reset Configurations', 'widget': 'btn', 'args': {'save_name':'settings', 'type': 'reset'}},
                {'name': 'Remove all Files', 'widget': 'btn', 'args': {'save_name':'files', 'type': 'reset'}},
                {'name': 'Reset All', 'widget': 'btn', 'args': {'save_name':'all', 'type': 'reset'}},
            ]   


        