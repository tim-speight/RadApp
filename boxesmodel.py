# boxesmodel.py
from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray

class BoxItem:
    def __init__(self, caption, payload, dose_rate, end_time):
        self.caption = caption
        self.payload = payload
        self.doseRate = dose_rate
        self.end_time = end_time
        self.displayColour = "green"
        self.doseRateBarWidth = 80
        self.debugInfo = ""
        self.isNotEmpty = True
        self.isBeingEdited = False
        self.remainingSeconds = 0

class BoxesModel(QAbstractListModel):
    CaptionRole = Qt.UserRole + 1
    PayloadRole = Qt.UserRole + 2
    DoseRateRole = Qt.UserRole + 3
    EndTimeRole = Qt.UserRole + 4
    DisplayColourRole = Qt.UserRole + 5
    DoseRateBarWidthRole = Qt.UserRole + 6
    DebugInfoRole = Qt.UserRole + 7
    IsNotEmptyRole = Qt.UserRole + 8
    IsBeingEditedRole = Qt.UserRole + 9
    RemainingSecondsRole = Qt.UserRole + 10

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = [
            BoxItem("Box 1", "Target A", 3.2, 0),
            BoxItem("Box 2", "Target B", 5.0, 0),
            BoxItem("Box 3", "Target C", 1.5, 0),
        ]

    @property
    def items(self):
        return self._items

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        item = self._items[index.row()]
        if role == self.CaptionRole:
            return item.caption
        if role == self.PayloadRole:
            return item.payload
        if role == self.DoseRateRole:
            return item.doseRate
        if role == self.EndTimeRole:
            return item.end_time
        if role == self.DisplayColourRole:
            return item.displayColour
        if role == self.DoseRateBarWidthRole:
            return item.doseRateBarWidth
        if role == self.DebugInfoRole:
            return item.debugInfo
        if role == self.IsNotEmptyRole:
            return item.isNotEmpty
        if role == self.IsBeingEditedRole:
            return item.isBeingEdited
        if role == self.RemainingSecondsRole:
            return item.remainingSeconds
        return None

    def roleNames(self):
        return {
            self.CaptionRole: QByteArray(b"caption"),
            self.PayloadRole: QByteArray(b"payload"),
            self.DoseRateRole: QByteArray(b"doseRate"),
            self.EndTimeRole: QByteArray(b"endTime"),
            self.DisplayColourRole: QByteArray(b"displayColour"),
            self.DoseRateBarWidthRole: QByteArray(b"doseRateBarWidth"),
            self.DebugInfoRole: QByteArray(b"debugInfo"),
            self.IsNotEmptyRole: QByteArray(b"isNotEmpty"),
            self.IsBeingEditedRole: QByteArray(b"isBeingEdited"),
            self.RemainingSecondsRole: QByteArray(b"remainingSeconds"),
        }

    def setItemData(self, row):
        idx = self.index(row)
        self.dataChanged.emit(idx, idx, list(self.roleNames().keys()))

    def setEndTime(self, row, end_time):
        self._items[row].end_time = end_time
        self.setItemData(row)

    def setDisplayColour(self, row, colour):
        self._items[row].displayColour = colour
        self.setItemData(row)

    def setRemainingSeconds(self, row, seconds):
        self._items[row].remainingSeconds = seconds
        self.setItemData(row)