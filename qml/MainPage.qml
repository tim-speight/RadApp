import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Page {
    id: root
    anchors.fill: parent
    background: Rectangle { color: "black" }

    header: Rectangle {
        height: 60
        color: "#222"
        RowLayout {
            anchors.fill: parent
            anchors.margins: 10

            Text {
                text: controller.roomId + ":" + controller.experimentId
                font.pixelSize: 32
                color: "white"
                Layout.alignment: Qt.AlignVCenter
            }

            Item { Layout.fillWidth: true }

            Text {
                text: controller.timeString
                font.pixelSize: 32
                color: "white"
            }
        }
    }

    footer: Rectangle {
        height: 60
        color: "#333"
        RowLayout {
            anchors.fill: parent
            anchors.margins: 10
            spacing: 20

            Button { text: "Help"; onClicked: controller.showHelp() }
            Button { text: "Admin"; onClicked: controller.showAdmin() }
            Button { text: "Export CSV"; onClicked: controller.exportCsv("/home/pi/targets.csv") }
        }
    }

    GridView {
        id: boxesView
        model: boxesModel
        anchors {
            top: header.bottom
            bottom: footer.top
            left: parent.left
            right: parent.right
            margins: 10
        }
        cellWidth: (width - 40) / 3
        cellHeight: 160
        interactive: true
        clip: true

        delegate: MouseArea {
            width: boxesView.cellWidth
            height: boxesView.cellHeight
            onClicked: controller.boxClicked(index)
            onDoubleClicked: controller.boxDoubleClicked(index)

            Rectangle {
                anchors.fill: parent
                radius: 6
                color: displayColour
                border.width: isBeingEdited ? 6 : 2
                border.color: isBeingEdited ? "blue" : "black"

                Column {
                    anchors.fill: parent
                    anchors.margins: 10
                    spacing: 4

                    Text { text: caption; font.pixelSize: 22; color: "white" }

                    Column {
                        visible: isNotEmpty
                        spacing: 4

                        Text { text: payload; font.pixelSize: 20; color: "white" }

                        Text {
                            text: doseRate + " µSv/hr"
                            font.pixelSize: 20
                            color: "white"
                        }

                        Rectangle {
                            width: parent.width
                            height: 10
                            color: "#444"
                            Rectangle {
                                anchors.left: parent.left
                                height: parent.height
                                width: parent.width * Math.min(1, remainingSeconds / 300) // 5 min scale
                                color: "lime"
                            }
                        }

                        Text {
                            text: remainingSeconds + " s"
                            font.pixelSize: 18
                            color: "white"
                        }

                        Text { text: debugInfo; font.pixelSize: 18; color: "white" }
                    }
                }
            }
        }
    }

    NumericKeypad {
        id: keypad
        onAccepted: controller.numericInputReceived(value)
        onCancelled: controller.numericInputCancelled()
    }

    AdminPinDialog {
        id: adminDialog
    }

    Connections {
        target: controller
        function onRequestNumericInput(index) {
            keypad.visible = true
        }
        function onRequestAdminPin() {
            adminDialog.visible = true
        }
    }
}