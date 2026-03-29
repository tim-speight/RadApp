from PySide6.QtCore import QObject, Signal, Slot, Property, QTimer
import csv
import time

class Controller(QObject):
    requestNumericInput = Signal(int)
    boxUpdated = Signal()
    requestAdminPin = Signal()
    timeStringChanged = Signal()

    def __init__(self, boxes_model):
        super().__init__()
        self._boxes = boxes_model
        self._roomId = "R1"
        self._experimentId = "EXP-001"
        self._timeString = ""
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.updateTimers)
        self._timer.start(1000)
        self.USB_PATH = "/media/swdev/RADAPP/data"

    @Property(str, notify=timeStringChanged)
    def timeString(self):
        return self._timeString

    @Property(str, constant=True)
    def roomId(self):
        return self._roomId

    @Property(str, constant=True)
    def experimentId(self):
        return self._experimentId

    @Slot(int)
    def boxClicked(self, index):
        self.requestNumericInput.emit(index)

    @Slot(int)
    def boxDoubleClicked(self, index):
        # e.g. mark as being edited
        self._boxes.items[index].isBeingEdited = not self._boxes.items[index].isBeingEdited
        self._boxes.setItemData(index)

    @Slot(str)
    def numericInputReceived(self, value):
        # interpret as seconds for timer
        try:
            seconds = int(value)
        except ValueError:
            return
        now = time.time()
        # for simplicity, apply to all boxes being edited
        for i, box in enumerate(self._boxes.items):
            if box.isBeingEdited:
                self._boxes.setEndTime(i, now + seconds)

    @Slot()
    def numericInputCancelled(self):
        pass

    @Slot()
    def showHelp(self):
        print("Help requested")

    @Slot()
    def showAdmin(self):
        self.requestAdminPin.emit()

    @Slot()
    def test(self):
        print("Test pressed")

    @Slot(str)
    def adminPinEntered(self, pin):
        if pin == "111111":
            print("Admin unlocked")
        else:
            print("Bad PIN")

    @Slot()
    def updateTimers(self):
        now = time.time()
        for i, box in enumerate(self._boxes.items):
            if box.end_time > 0:
                remaining = int(box.end_time - now)
                if remaining < 0:
                    remaining = 0
                self._boxes.setRemainingSeconds(i, remaining)
                # traffic light
                if remaining == 0:
                    colour = "red"
                elif remaining < 60:
                    colour = "orange"
                else:
                    colour = "green"
                self._boxes.setDisplayColour(i, colour)
        self._timeString = time.strftime("%H:%M:%S")
        self.timeStringChanged.emit()
        self.boxUpdated.emit()

    @Slot()
    def exportToUsb(self):
        usb_path = self.USB_PATH

        if not os.path.isdir(usb_path):
            print(f"USB path not found: {usb_path}")
            return

        filename = os.path.join(usb_path, "irradiated_targets.csv")
        self.exportCsv(filename)
        print("Exported to:", filename)