import QtQuick
import QtQuick.Controls

Item {
    id: header

    property color textColor
    property color accentColor
    property color hoverColor
    property color pressedColor
    property color surfaceColor

    signal settingsClicked()
    signal helpClicked()

    width: parent.width
    height: 76

    Row {
        spacing: 16
        anchors.left: parent.left
        anchors.verticalCenter: parent.verticalCenter

        Image {
            width: 76
            height: 76
            source: "../../assets/logo4.png"
            fillMode: Image.PreserveAspectFit
            smooth: true
        }

        Column {
            spacing: 0
            anchors.verticalCenter: parent.verticalCenter

            Label {
                text: "Second"
                font.pixelSize: 28
                font.bold: true
                color: header.textColor
            }

            Label {
                text: "Brain"
                font.pixelSize: 28
                font.bold: true
                color: "#38BDF8"
            }

            Rectangle {
                width: 64
                height: 4
                radius: 2
                color: "#FACC15"
            }
        }
    }

    // Open the user guide.
    Button {
        id: helpButton

        width: 44
        height: 44

        anchors.right: settingsButton.left
        anchors.rightMargin: 12
        anchors.top: parent.top

        hoverEnabled: true

        Accessible.name: translator.text(
            "header.user_guide",
            translator.language
        )
        ToolTip.visible: hovered
        ToolTip.text: translator.text(
            "header.user_guide",
            translator.language
        )

        contentItem: Text {
            text: "?"
            font.pixelSize: 26
            font.bold: true
            color: header.accentColor
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        background: Rectangle {
            radius: 8

            color: helpButton.down
                ? header.pressedColor
                : helpButton.hovered
                    ? header.hoverColor
                    : header.surfaceColor

            border.color: header.accentColor
            border.width: 1
        }

        onClicked: header.helpClicked()
    }

    Button {
        id: settingsButton

        width: 44
        height: 44

        anchors.right: parent.right
        anchors.top: parent.top

        hoverEnabled: true

        Accessible.name: translator.text(
            "settings.title",
            translator.language
        )
        ToolTip.visible: hovered
        ToolTip.text: translator.text(
            "settings.title",
            translator.language
        )

        contentItem: Item {
            Canvas {
                anchors.centerIn: parent
                width: 24
                height: 24

                property color iconColor: header.accentColor

                onIconColorChanged: requestPaint()

                onPaint: {
                    const ctx = getContext("2d")
                    ctx.clearRect(0, 0, width, height)

                    ctx.strokeStyle = iconColor
                    ctx.lineWidth = 2
                    ctx.lineJoin = "round"
                    ctx.beginPath()

                    for (let tooth = 0; tooth < 8; tooth++) {
                        const angles = [-22.5, -12, 12, 22.5]
                        const radii = [8.5, 11, 11, 8.5]

                        for (let point = 0; point < 4; point++) {
                            const angle =
                                (tooth * 45 + angles[point]) * Math.PI / 180

                            const px =
                                12 + Math.cos(angle) * radii[point]

                            const py =
                                12 + Math.sin(angle) * radii[point]

                            if (tooth === 0 && point === 0) {
                                ctx.moveTo(px, py)
                            } else {
                                ctx.lineTo(px, py)
                            }
                        }
                    }

                    ctx.closePath()
                    ctx.stroke()

                    ctx.beginPath()
                    ctx.arc(12, 12, 4, 0, 2 * Math.PI)
                    ctx.stroke()
                }
            }
        }

        background: Rectangle {
            radius: 8

            color: settingsButton.down
                ? header.pressedColor
                : settingsButton.hovered
                    ? header.hoverColor
                    : header.surfaceColor

            border.color: header.accentColor
            border.width: 1
        }

        onClicked: header.settingsClicked()
    }
}