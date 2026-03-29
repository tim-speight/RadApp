import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: adminDialog
    anchors.fill: parent
    color: "#80000000"
    visible: false
    z: 1000

    property string buffer: ""

    Rectangle {
        width: 320
        height: 420
        radius: 12
        color: "#222"
        anchors.centerIn: parent

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 12
            spacing: 12

            Text {
                text: "Enter Admin PIN"
                color: "white"
                font.pixelSize: 24
                Layout.fillWidth: true
            }

            Text {
                text: buffer.replace(/./g, "•")
                font.pixelSize: 40
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                Layout.fillWidth: true
                Layout.preferredHeight: 60
            }

            GridLayout {
                columns: 3
                rowSpacing: 10
                columnSpacing: 10
                Layout.fillWidth: true
                Layout.fillHeight: true

                Repeater {
                    model: ["1","2","3","4","5","6","7","8","9","←","0","OK"]

                    delegate: Button {
                        text: modelData
                        font.pixelSize: 28
                        Layout.preferredWidth: 90
                        Layout.preferredHeight: 70

                        onClicked: {
                            if (text === "←") {
                                buffer = buffer.slice(0, -1)
                            } else if (text === "OK") {
                                adminDialog.visible = false
                                controller.adminPinEntered(buffer)
                                buffer = ""
                            } else {
                                buffer += text
                            }
                        }
                    }
                }
            }

            Button {
                text: "Cancel"
                font.pixelSize: 22
                Layout.fillWidth: true
                onClicked: {
                    adminDialog.visible = false
                    buffer = ""
                }
            }
        }
    }
}