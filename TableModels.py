from PyQt6.QtCore import Qt
from PyQt6.QtCore import QAbstractTableModel
from Helper import res

from PyQt6.QtGui import QIcon, QStandardItem, QColor

class FirstModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data = []
        for d in data:
            self.data.append(['No Icon', d['playlist_name'], "Yes" if d['is_shared'] else "No"])
        
        # self.data = [['Alice', 25, 19], ['Bob', 30, 30], ["test", 90, 20]]

    def rowCount(self, parent):
        return len(self.data)

    def columnCount(self, parent):
        if len(self.data) > 0:
            return len(self.data[0])
        return 0

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.data[index.row()][index.column()]
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            if section == 0:
                return " "
            if section == 1:
                return "Playlist Name"
            elif section == 2:
                return "is sharable"

        return super().headerData(section, orientation, role)
    
class SecondModel(QAbstractTableModel):
    def __init__(self, data=[], current_row=None):
        super().__init__()
        self.data = []
        self.current_row = current_row
        icon_item = QStandardItem(QIcon(res()+"/Icons/activity.svg"), "Emmanuel")
        for d in data:
            self.data.append([icon_item, d['filename'], d['title'], d['artist'], d['path']])

    def rowCount(self, parent):
        return len(self.data)

    def columnCount(self, parent):
        if len(self.data) > 0:
            return len(self.data[0])
        return 0

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.data[index.row()][index.column()]
        
        if self.current_row is not None:
            if role == Qt.ItemDataRole.BackgroundRole:
                if index.row() == self.current_row:
                    return QColor(255, 0, 0)
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            if section == 0:
                return " "
            if section == 1:
                return "File Name"
            if section == 2:
                return "Title"
            if section == 3:
                return "Artist"
            if section == 4:
                return "Path"

        return super().headerData(section, orientation, role)

