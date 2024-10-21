import xml.etree.ElementTree as ET
from Helper import res, temp_folder, retrive_current_audio_property, retrive_current_playlist_property
from PyQt6.QtGui import QIcon
from create_update_db import Create
from read_db import Read
from update_db import Update
from settings import NeonColors
import os
import svgwrite
import math
import svgwrite

# def create_repeat_one_svg(filename, width, height):
#     dwg = svgwrite.Drawing(filename, profile='tiny', size=(width, height))

#     # Draw the main circle
#     circle = dwg.circle(center=(width / 2, height / 2), r=width / 2 - 2, fill="none", stroke="black", stroke_width=2)
#     dwg.add(circle)

#     # Draw the "1" inside the circle
#     text = dwg.text("1", insert=(width / 2, height / 2), font_size=width * 0.5, font_family="Arial",
#                     text_anchor="middle", alignment_baseline="middle", fill="black")
#     dwg.add(text)

#     dwg.save()


def create_pause_button(filename, circle_radius, start_angle, end_angle):
    dwg = svgwrite.Drawing(filename, profile='tiny', size=(100, 100))

    center = (50, 50)

    # Draw the circle
    circle = dwg.circle(center=center, r=circle_radius, fill='none', stroke='black', stroke_width=2)
    dwg.add(circle)

    # Calculate the arc endpoints
    start_x = center[0] + circle_radius * math.cos(math.radians(start_angle))
    start_y = center[1] - circle_radius * math.sin(math.radians(start_angle))

    end_x = center[0] + circle_radius * math.cos(math.radians(end_angle))
    end_y = center[1] - circle_radius * math.sin(math.radians(end_angle))

    # Draw the arc
    arc = dwg.path(d=f"M {start_x},{start_y} A {circle_radius},{circle_radius} 0 0,1 {end_x},{end_y}")
    dwg.add(arc)

    dwg.save()
    print(filename)
    return filename





def create_pie_chart(filename, value, radius, fill='none', stroke='black'):
    dwg = svgwrite.Drawing(filename, profile='tiny', size=(2*radius, 2*radius))
    start_angle = 0
    center = (radius, radius)
    
    end_angle = value * (2 * 3.141592653589793)
    
    start_x = center[0] + radius * math.sin(start_angle)
    start_y = center[1] - radius * math.cos(start_angle)
    
    end_x = center[0] + radius * math.sin(end_angle)
    end_y = center[1] - radius * math.cos(end_angle)
    
    # Draw the arc
    path = dwg.path(d=f'M {center[0]},{center[1]} L {start_x},{start_y} A {radius},{radius} 0 {int(value > 0.5)} 1 {end_x},{end_y} Z', fill=fill, stroke=stroke)
    dwg.add(path)
    
    dwg.save()
    return filename

def change_color(path, fill='none', stroke='currentColor', name_prefix=""):
    tree = ET.parse(path)
    root = tree.getroot()
    for elem in root.iter():
        if "fill" in elem.attrib:
            elem.attrib["fill"] = fill 
            
        if "stroke" in elem.attrib:
            elem.attrib["stroke"] = stroke
    name = os.path.basename(path).rsplit(".")[0]
    saved_path = temp_folder("/icon_tmp")+f"/{name_prefix}_{name}_tmp.svg"
    tree.write(saved_path)
    return saved_path

class IconLoader:
    def __init__(self, parent):
        self.parent = parent
        self.update_db = Update()
        self.create = Create()
        self.read = Read()
        self.grad = GradientColorConvertor()
        self.color = NeonColors()
        self.play_pause_orientation_counter = 0
        self.play_pause_orientation_direction = True
        self.skin_icon_color = '#FF3647'
        
        self.check_colors()
        self.like_love_star_updater()
        self.repeate_shuffle_updater()
    
    def load_icons(self):
        # self.parent.repeate.setIcon(QIcon(change_color(res()+"/Icons/repeat.svg", fill=self.read.get_variable("control fill color", 'none'), stroke=self.read.get_variable("control stroke color", 'black'))))
        # self.parent.starAudio.setIcon(QIcon(self.grad.change_color(res()+"/Icons/star.svg", gradient_stroke=self.color.neon_3(), gradient_fill=None)))        
        # self.parent.likeAudio.setIcon(QIcon(self.grad.change_color(res()+"/Icons/thumbs-up.svg", gradient_stroke=self.color.neon_3(), gradient_fill=None)))

        self.parent.play.setIcon(QIcon(self.grad.change_color(res()+"/Icons/play-circle.svg", gradient_stroke=self.color.neon_6(), gradient_fill=None)))
        self.parent.playAlt.setIcon(QIcon(self.grad.change_color(res()+"/Icons/play.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
        self.parent.prev.setIcon(QIcon(self.grad.change_color(res()+"/Icons/arrow-left-circle.svg", gradient_stroke=self.color.neon_6(), gradient_fill=None)))
        self.parent.next.setIcon(QIcon(self.grad.change_color(res()+"/Icons/arrow-right-circle.svg", gradient_stroke=self.color.neon_6(), gradient_fill=None)))
        self.parent.togglePlaylist.setIcon(QIcon(self.grad.change_color(res()+"/Icons/menu.svg", gradient_stroke=self.color.neon_2(), gradient_fill=None)))
        self.parent.shuffle.setIcon(QIcon(change_color(res()+"/Icons/shuffle.svg", fill=self.read.get_variable("control fill color", 'none'), stroke=self.read.get_variable("control stroke color", 'black'))))
        self.parent.open.setIcon(QIcon(self.grad.change_color(res()+"/Icons/music.svg", gradient_stroke=self.color.neon_4(), gradient_fill=None)))
        self.parent.mute.setIcon(QIcon(self.grad.change_color(res()+"/Icons/volume-1.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
        self.parent.showVolume.setIcon(QIcon(self.grad.change_color(res()+"/Icons/volume-1.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
        self.parent.skin_show_volume.setIcon(QIcon(self.grad.change_color(res()+"/Icons/volume-1.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
        self.parent.settBtn.setIcon(QIcon(self.grad.change_color(res()+"/Icons/settings.svg", gradient_stroke=self.color.neon_6(), gradient_fill=None)))
        self.parent.loginBtn.setIcon(QIcon(self.grad.change_color(res()+"/Icons/log-in.svg", gradient_stroke=self.color.neon_6(), gradient_fill=None)))
        self.parent.minimizeBtn.setIcon(QIcon(change_color(res()+"/Icons/minus.svg", fill=self.read.get_variable("exit fill color"), stroke=self.read.get_variable("exit stroke color"))))
        self.parent.exitBtn.setIcon(QIcon(change_color(res()+"/Icons/power.svg", fill=self.read.get_variable("exit fill color"), stroke=self.read.get_variable("exit stroke color"))))
        
        
        
        
        self.skin_color_decider()
        self.parent.skin_prev.setStyleSheet(self.additional_css("skin_prev", 'rgba(0, 250, 0, 10)'))
        self.parent.skin_minimize.setStyleSheet(self.additional_css("skin_minimize", 'rgba(0, 250, 0, 10)'))
        self.parent.skin_next.setStyleSheet(self.additional_css("skin_next", 'rgba(0, 250, 0, 10)'))
        self.parent.skin_menu.setStyleSheet(self.additional_css("skin_menu", 'rgba(0, 250, 0, 10)'))
        self.parent.skin_power.setStyleSheet(self.additional_css("skin_power", 'rgba(250, 250, 0, 7)'))
        
        self.parent.skin_power.setIcon(QIcon(change_color(res()+"/Icons/power.svg", stroke=self.skin_icon_color, fill='none', name_prefix='big_btn_skin')))
        self.parent.skin_minimize.setIcon(QIcon(change_color(res()+"/Icons/minus.svg", stroke=self.skin_icon_color, fill='none', name_prefix='big_btn_skin')))
        self.parent.skin_prev.setIcon(QIcon(change_color(res()+"/Icons/skip-back.svg", stroke=self.skin_icon_color, fill='none', name_prefix='big_btn_skin')))
        self.parent.skin_next.setIcon(QIcon(change_color(res()+"/Icons/skip-forward.svg", stroke=self.skin_icon_color, fill='none', name_prefix='big_btn_skin')))
        self.parent.skin_menu.setIcon(QIcon(change_color(res()+"/Icons/menu.svg", stroke=self.skin_icon_color, fill='none', name_prefix='big_btn_skin')))
        self.parent.skin_play.setIcon(QIcon(self.grad.change_color(res()+"/Icons/play-circle.svg", gradient_stroke=self.color.neon_6(), gradient_fill=None, name_prefix='big_btn_skin')))
        self.parent.skin_circle.setIcon(QIcon(change_color(create_pie_chart(temp_folder("/dynamic/Icons")+"/circle_alt.svg", 0.0, 10), fill=self.skin_icon_color, stroke='none', name_prefix='big_btn_skin')))
        
        self.like_love_star_updater()
        self.repeate_shuffle_updater()
        self.special_icons()

    def additional_css(self, btn_name, color):
        return "#"+btn_name+":hover{background-color:"+color+"}"
        
    def special_icons(self):
        if self.read.get_variable("playing"):
            self.parent.play.setIcon(QIcon(self.grad.change_color(res()+"/Icons/pause-circle.svg", gradient_stroke=self.color.neon_6(), gradient_fill=self.color.fill_green_quater())))
            self.parent.playAlt.setIcon(QIcon(self.grad.change_color(res()+"/Icons/pause.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
            self.parent.skin_play.setIcon(QIcon(self.grad.change_color(res()+"/Icons/pause-circle.svg", gradient_stroke=self.color.neon_6(), gradient_fill=None, name_prefix='big_btn_skin')))
        else:
            self.parent.play.setIcon(QIcon(self.grad.change_color(res()+"/Icons/play-circle.svg", gradient_stroke=self.color.neon_6(), gradient_fill=None)))
            self.parent.playAlt.setIcon(QIcon(self.grad.change_color(res()+"/Icons/play.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
            self.parent.skin_play.setIcon(QIcon(self.grad.change_color(res()+"/Icons/play-circle.svg", gradient_stroke=self.color.neon_6(), gradient_fill=None, name_prefix='big_btn_skin')))

        if self.read.get_variable("volume") is not None and int(self.read.get_variable("volume")) <= 0:
            self.parent.mute.setIcon(QIcon(self.grad.change_color(res()+"/Icons/volume-x.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
            self.parent.showVolume.setIcon(QIcon(self.grad.change_color(res()+"/Icons/volume-x.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
            self.parent.skin_show_volume.setIcon(QIcon(self.grad.change_color(res()+"/Icons/volume-x.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
        elif self.read.get_variable("volume") is not None and int(self.read.get_variable("volume")) <= 10:
            self.parent.mute.setIcon(QIcon(self.grad.change_color(res()+"/Icons/volume.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
            self.parent.showVolume.setIcon(QIcon(self.grad.change_color(res()+"/Icons/volume.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
            self.parent.skin_show_volume.setIcon(QIcon(self.grad.change_color(res()+"/Icons/volume.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
        elif self.read.get_variable("volume") is not None and int(self.read.get_variable("volume")) <= 50:
            self.parent.mute.setIcon(QIcon(self.grad.change_color(res()+"/Icons/volume-1.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
            self.parent.showVolume.setIcon(QIcon(self.grad.change_color(res()+"/Icons/volume-1.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
            self.parent.skin_show_volume.setIcon(QIcon(self.grad.change_color(res()+"/Icons/volume-1.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
        else:
            self.parent.mute.setIcon(QIcon(self.grad.change_color(res()+"/Icons/volume-2.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
            self.parent.showVolume.setIcon(QIcon(self.grad.change_color(res()+"/Icons/volume-2.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
            self.parent.skin_show_volume.setIcon(QIcon(self.grad.change_color(res()+"/Icons/volume-2.svg", gradient_stroke=self.color.neon_1(), gradient_fill=None)))
    
    def like_love_star_updater(self):
        _, _, like_audio = retrive_current_audio_property('like_audio')
        _, _, star_audio = retrive_current_audio_property('star')
        _, like_playlist = retrive_current_playlist_property('like_playlist')
        _, love_playlist = retrive_current_playlist_property('love_playlist')
        _, shared = retrive_current_playlist_property('is_shared')
        
        if love_playlist:
            self.parent.lovePlaylist.setIcon(QIcon(self.grad.change_color(res()+"/Icons/heart.svg", gradient_stroke=self.color.neon_5(), gradient_fill=self.color.color_1())))
        else:
            self.parent.lovePlaylist.setIcon(QIcon(change_color(res()+"/Icons/heart.svg", fill='none', stroke='black')))

        if shared:
            self.parent.sharePlaylist.setIcon(QIcon(self.grad.change_color(res()+"/Icons/share-2.svg", gradient_stroke=self.color.neon_5(), gradient_fill=self.color.color_1())))
        else:
            self.parent.sharePlaylist.setIcon(QIcon(change_color(res()+"/Icons/share-2.svg", fill='none', stroke='black')))
        
        if like_playlist == "High":
            self.parent.likePlaylist.setIcon(QIcon(self.grad.change_color(res()+"/Icons/thumbs-up.svg", gradient_stroke=self.color.neon_5(), gradient_fill=self.color.color_1(), name_prefix="playlist")))
        elif like_playlist == "Low":
            self.parent.likePlaylist.setIcon(QIcon(change_color(res()+"/Icons/thumbs-down.svg", fill=self.read.get_variable("dislike fill color"), stroke=self.read.get_variable("control stroke color", 'black'), name_prefix="playlist")))
        else:
            self.parent.likePlaylist.setIcon(QIcon(change_color(res()+"/Icons/thumbs-up.svg", stroke='black', fill='none', name_prefix="playlist")))
        
        if like_audio == "High":
            self.parent.likeAudio.setIcon(QIcon(self.grad.change_color(res()+"/Icons/thumbs-up.svg", gradient_stroke=self.color.neon_5(), gradient_fill=self.color.color_1(), name_prefix="audio")))
        elif like_audio == "Low":
            self.parent.likeAudio.setIcon(QIcon(change_color(res()+"/Icons/thumbs-down.svg", fill=self.read.get_variable("dislike fill color"), stroke=self.read.get_variable("control stroke color", 'black'), name_prefix="audio")))
        else:
            self.parent.likeAudio.setIcon(QIcon(change_color(res()+"/Icons/thumbs-up.svg", stroke='black', fill='none', name_prefix="audio")))
        
        if star_audio == 0:
            self.parent.starAudio.setIcon(QIcon(self.grad.change_color(res()+"/Icons/star.svg", gradient_stroke=self.color.neon_3(), gradient_fill=None)))
        elif star_audio == 1:
            self.parent.starAudio.setIcon(QIcon(self.grad.change_color(res()+"/Icons/star.svg", gradient_stroke=self.color.neon_3(), gradient_fill=self.color.color_2())))        
        elif star_audio == 2:
            self.parent.starAudio.setIcon(QIcon(self.grad.change_color(res()+"/Icons/star.svg", gradient_stroke=self.color.neon_1(), gradient_fill=self.color.color_2())))        
        elif star_audio == 3:
            self.parent.starAudio.setIcon(QIcon(self.grad.change_color(res()+"/Icons/star.svg", gradient_stroke=self.color.neon_2(), gradient_fill=self.color.color_1())))        
        elif star_audio == 4:
            self.parent.starAudio.setIcon(QIcon(self.grad.change_color(res()+"/Icons/star.svg", gradient_stroke=self.color.neon_7(), gradient_fill=self.color.color_3())))        
        elif star_audio == 5:
            self.parent.starAudio.setIcon(QIcon(self.grad.change_color(res()+"/Icons/star.svg", gradient_stroke=self.color.neon_5(), gradient_fill=self.color.neon_7())))        
        
    def repeate_shuffle_updater(self):
        if not self.read.get_variable("Repeate"):
            self.parent.repeate.setIcon(QIcon(change_color(res()+"/Icons/repeat.svg", fill=self.read.get_variable("control fill color", 'none'), stroke=self.read.get_variable("control stroke color", 'black'))))
        elif self.read.get_variable("Repeate") == "All":
            self.parent.repeate.setIcon(QIcon(self.grad.change_color(res()+"/Icons/repeat.svg", gradient_stroke=self.color.neon_6(), gradient_fill=None)))
        else:
            self.parent.repeate.setIcon(QIcon(res()+"/Icons/repeat-one-svgrepo-com.svg"))
        
        
        if self.read.get_variable("Shuffle"):
            self.parent.shuffle.setIcon(QIcon(self.grad.change_color(res()+"/Icons/shuffle.svg", gradient_stroke=self.color.neon_6(), gradient_fill=None)))
        else:
            self.parent.shuffle.setIcon(QIcon(change_color(res()+"/Icons/shuffle.svg", fill=self.read.get_variable("control fill color", 'none'), stroke=self.read.get_variable("control stroke color", 'black'))))
        
        
        
    def pause_play_animation(self, progress):
        # self.parent.play.setIcon(QIcon(self.grad.change_color(res()+"/Icons/pause-circle.svg", gradient_stroke=self.color.neon_6(), gradient_fill=self.color.fill_green(progress*100, self.play_pause_orientation_counter))))
        
        # if self.play_pause_orientation_direction:
        #     self.play_pause_orientation_counter += 1
        # else:
        #     self.play_pause_orientation_counter -= 1
            
        # if self.play_pause_orientation_counter > 2 or self.play_pause_orientation_counter < -2:
        #     self.play_pause_orientation_direction = not self.play_pause_orientation_direction
        if self.read.get_variable('current skin') == 'One Button':
            self.parent.skin_circle.setIcon(QIcon(change_color(create_pie_chart(temp_folder("/dynamic/Icons")+"/circle_alt.svg", progress, 10), fill=self.skin_icon_color, stroke='none', name_prefix='big_btn_skin')))
        
        if self.read.get_variable('current skin') == 'Simple':
            self.parent.skin_circle.setIcon(QIcon(change_color(create_pie_chart(temp_folder("/dynamic/Icons")+"/circle_alt.svg", progress, 1), fill=self.skin_icon_color, stroke='none', name_prefix='big_btn_skin')))
        
        
    def skin_color_decider(self):
        if self.read.get_variable('current skin') == 'One Button':
            self.skin_icon_color = self.read.get_variable("one button btn color")
        elif self.read.get_variable('current skin') == 'Simple':
            self.skin_icon_color = self.read.get_variable("simple btn color")
        elif self.read.get_variable('current skin') == 'Rounded Bar':
            self.skin_icon_color = self.read.get_variable("rounded bar btn color")
        
    def change_colors(self, fill="none", stroke="red"):
        self.create.create_variable("Fill Color", fill)
        self.create.create_variable("Stroke Color", stroke)
        self.load_icons()
            
    def check_colors(self):
        if self.read.get_variable("control fill color") is None:
            self.create.create_variable("control fill color", 'none')
        if self.read.get_variable("control stroke color") is None:
            self.create.create_variable("control stroke color", 'black')
            
        if self.read.get_variable("dislike fill color") is None:
            self.create.create_variable("dislike fill color", 'none')
        if self.read.get_variable("dislike stroke color") is None:
            self.create.create_variable("dislike stroke color", 'red')
            
        if self.read.get_variable("other fill color") is None:
            self.create.create_variable("other fill color", 'none')
        if self.read.get_variable("other stroke color") is None:
            self.create.create_variable("other stroke color", 'rgb(255, 0, 51)')
            
        if self.read.get_variable("exit fill color") is None:
            self.create.create_variable("exit fill color", 'none')
        if self.read.get_variable("exit stroke color") is None:
            self.create.create_variable("exit stroke color", 'rgb(127, 48, 255)')
            
        
            
class GradientColorConvertor:
    # # Example input string: "0,0;100,0;0,#ffff00,1,#ff0000"
    def numbers_to_svg(self, qlinear_gradient_str):
        gradient_info = qlinear_gradient_str.split(';')
        start_x, start_y = map(float, gradient_info[0].split(','))
        end_x, end_y = map(float, gradient_info[1].split(','))
        color_stops = gradient_info[2].split(',')
        
        # Construct the SVG linear gradient element
        svg_gradient = '<linearGradient x1="{}" y1="{}" x2="{}" y2="{}">'.format(
            start_x, start_y, end_x, end_y
        )
        
        for i in range(0, len(color_stops), 2):
            offset = float(color_stops[i])
            color = color_stops[i+1]
            svg_stop = '<stop offset="{}%" stop-color="{}"/>'.format(offset * 100, color)
            svg_gradient += svg_stop
        
        svg_gradient += '</linearGradient>'
        return svg_gradient
    

    def string_to_svg(self, str_color, id):
        if str_color is None:
            return ""
        headers = str_color[str_color.find('x1'):str_color.find('stop')]
        body = str_color[str_color.find('stop'):]
        
        
        result = f"<linearGradient id='{id}' {self.header_decoder(headers)}>\n"
        result += f"{self.body_generator(body)}\n"
        result += "</linearGradient>\n"
        
        return result

    def header_decoder(self, val):
        val = val.split(",")
        val.pop()
        result = ""
        for v in val:
            v=v.strip()
            v= v.split(":")
            result += " {}=\"{}%\"".format(v[0], float(v[1])*100)
        return result
        
    
    def body_generator(self, val):
        val = val.split("stop")
        result = ""
        for v in val:
            v=v.strip()
            if v != "":
                result += "<stop offset=\"{}%\"".format(float(v[v.find(':')+1:v.find('rgb')])*100)
                rgba = v[v.find('(')+1:v.find(')')].split(",")
                result += " style=\"stop-color:rgb({}, {}, {});".format(int(rgba[0]), int(rgba[1]), int(rgba[2]))
                result += " stop-opacity:{}\" />".format(float(rgba[3])/255)
        return result
    
    def change_color(self, path, gradient_fill=None, gradient_stroke=None, name_prefix=""):
        tree = ET.parse(path)
        root = tree.getroot()
        for elem in root.iter():
            if gradient_fill is not None and "fill" in elem.attrib:
                elem.attrib["fill"] = 'url(#fillgradient)'
                
            if gradient_stroke is not None and "stroke" in elem.attrib:
                elem.attrib["stroke"] = 'url(#strokegradient)'
        
        name = os.path.basename(path).rsplit(".")[0]
        saved_path = temp_folder("/icon_tmp")+f"/{name_prefix}_{name}_tmp.svg" 
        tree.write(saved_path)
        
        with open(saved_path, "r") as svg_file:
            svg_content = svg_file.read()
            text = "<defs>\n"
            text += self.string_to_svg(gradient_stroke, "strokegradient") + self.string_to_svg(gradient_fill, "fillgradient")
            text += '</defs>'
            if gradient_stroke is not None or gradient_fill is not None:
                svg_content = svg_content[:svg_content.find(">")+1] +text+svg_content[svg_content.find(">")+1:]
                svg_content = svg_content.replace("ns0:", "")
                svg_content = svg_content.replace(":ns0", "")
            
        with open(saved_path, "w") as svg_file:
            svg_file.write(svg_content)
            
        return saved_path







