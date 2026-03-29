# main.py
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from boxesmodel import BoxesModel
from controller import Controller
import sys

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    boxes_model = BoxesModel()
    controller = Controller(boxes_model)

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("controller", controller)
    engine.rootContext().setContextProperty("boxesModel", boxes_model)
    engine.load("qml/MainPage.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())