import os
import re

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem
import numpy as np


class PulseVisualizer(QtWidgets.QGraphicsView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setScene(QtWidgets.QGraphicsScene(self))
        self.init_ui()

    def set_opacity(self, value):
        self._opacity = value
        self.overlay.setOpacity(value)

    def init_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(110)

        self.now_playing_visual = NowPlayingVisual(self)
        self.main_layout.addWidget(self.now_playing_visual)

        self.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.black))

        self.video_item = QGraphicsVideoItem()
        self.video_item.setGraphicsEffect(QtWidgets.QGraphicsBlurEffect())
        self.video_item.setAspectRatioMode(QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.scene().addItem(self.video_item)

        self.overlay = QtWidgets.QGraphicsRectItem(0, 0, 0, 0, self.video_item)
        self.overlay.setBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.black))
        self.set_opacity(0.8)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setStyleSheet('border: 0px;')

        self.setLayout(self.main_layout)

    def change_title(self, title=''):
        self.now_playing_visual.set_title(title)

    def resizeEvent(self, event):
        self.video_item.setSize(QtCore.QSizeF(self.size()))
        rect = QtCore.QRectF(0, 0, self.video_item.size().width(),
                             self.video_item.size().height())
        self.overlay.setRect(rect)
        
    def setValues(self, amp):
        self.now_playing_visual.set_amplitudes(amp)


class NowPlayingVisual(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.amps = np.array([])
        self.colour = QtGui.QColor(255, 255, 255, 255)
        self.init_ui()
    
    def init_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.song_title = QtWidgets.QLabel()
        self.song_title.setFont(QtGui.QFont('Montserrat', 36))
        self.song_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.now_playing = QtWidgets.QLabel()
        self.now_playing.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.now_playing.setFont(QtGui.QFont('Karla', 14))

        self.main_layout.addWidget(self.song_title)
        self.main_layout.addWidget(self.now_playing)

        self.setStyleSheet('color: white;')

        self.setLayout(self.main_layout)

    def set_amplitudes(self, amps):
        self.amps = np.array(amps)
        self.repaint()

    def draw_polygon(self):
        poly = QtGui.QPolygonF()
        poly.append(QtCore.QPointF(0, self.height()))
        for n, amp in zip(np.linspace(0, self.width(), self.amps.size), self.amps):
            poly.append(QtCore.QPointF(n, self.height()-amp*self.height()))
        poly.append(QtCore.QPointF(self.width(), self.height()))
        return poly

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        poly = self.draw_polygon()
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(self.colour)
        painter.drawPolygon(poly)
        painter.drawRect(0, self.height()-5, self.width(), 5)
    
    def set_title(self, name):
        if len(name) > 35:
            name = name[:35].strip() + '...'
        self.song_title.setText(name)
        w = self.song_title.fontMetrics().boundingRect(name).width()
        self.parent().setMinimumWidth(w+200)