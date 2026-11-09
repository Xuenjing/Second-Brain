import QtQuick
import QtQuick.Controls

Item {
    id: thinkingIndicator

    property bool isThinking: false

    property color textColor
    property color accentColor
    property color windowColor

    visible: true

    Row {
        x: 16
        anchors.leftMargin: 16
        anchors.verticalCenter: parent.verticalCenter
        spacing: 8

        visible: thinkingIndicator.isThinking

        Item {
            width: 24
            height: 24

            Rectangle {
                id: thinkingRing

                anchors.centerIn: parent

                width: 20
                height: 20
                radius: 10

                color: "transparent"
                border.color: thinkingIndicator.accentColor
                border.width: 2

                Rectangle {
                    width: 6
                    height: 6
                    radius: 3

                    color: thinkingIndicator.windowColor

                    anchors.horizontalCenter: parent.horizontalCenter
                    y: -2
                }

                RotationAnimator on rotation {
                    from: 0
                    to: 360
                    duration: 1000
                    loops: Animation.Infinite
                    running: thinkingIndicator.isThinking
                }
            }
        }

        Label {
            text: translator.text(
                "thinking.status",
                translator.language
            )

            color: thinkingIndicator.textColor
            font.pixelSize: 14
            font.bold: true

            anchors.verticalCenter: parent.verticalCenter
        }
    }

}