import QtQuick
import QtQuick.Controls

Dialog {
    id: modelLoadDialog

    property int modelIndex: -1
    property string modelName: ""

    property color surfaceColor
    property color borderColor
    property color textColor
    property color secondaryTextColor
    property color hoverColor
    property color pressedColor
    property color accentColor
    property color assistantBubbleColor

    signal loadConfirmed(int modelIndex)

    title: translator.text(
        "model_load.title",
        translator.language
    )
    modal: true

    width: Math.max(parent.width * 0.45, 480)
    height: Math.max(parent.height * 0.30, 240)

    x: parent ? (parent.width - width) / 2 : 0
    y: parent ? (parent.height - height) / 2 : 0
    // anchors.centerIn: parent

    background: Rectangle {
        color: modelLoadDialog.surfaceColor
        radius: 12
        border.color: modelLoadDialog.borderColor
        border.width: 1
    }

    header: Label {
        text: modelLoadDialog.title
        color: modelLoadDialog.textColor
        font.pixelSize: 18
        font.bold: true
        padding: 16
    }

    contentItem: Column {
        spacing: 12

        Label {
            width: parent.width

            text: modelLoadDialog.modelName

            color: modelLoadDialog.textColor
            font.bold: true
            wrapMode: Text.WordWrap
        }

        Rectangle {
            width: parent.width
            height: warningText.implicitHeight + 24
            radius: 8
            color: modelLoadDialog.assistantBubbleColor

            Label {
                id: warningText

                anchors.fill: parent
                anchors.margins: 12

                text: translator.text(
                    "model_load.warning",
                    translator.language
                )

                color: modelLoadDialog.textColor
                wrapMode: Text.WordWrap
            }
        }
    }

    footer: Item {
        implicitHeight: 64

        Row {
            anchors.right: parent.right
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter
            spacing: 12

            Button {
                id: cancelButton

                text: translator.text(
                    "common.cancel",
                    translator.language
                )
                width: 100
                height: 40
                hoverEnabled: true

                contentItem: Text {
                    text: cancelButton.text
                    color: modelLoadDialog.textColor
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    radius: 8

                    color: cancelButton.down
                        ? modelLoadDialog.pressedColor
                        : cancelButton.hovered
                            ? modelLoadDialog.hoverColor
                            : modelLoadDialog.surfaceColor

                    border.color: modelLoadDialog.borderColor
                    border.width: 1
                }

                onClicked: modelLoadDialog.close()
            }

            Button {
                id: confirmButton

                text: "Ladda modell"
                width: 120
                height: 40
                hoverEnabled: true

                contentItem: Text {
                    text: translator.text(
                        "model_load.confirm",
                        translator.language
                    )
                    color: "#FFFFFF"
                    font.pixelSize: 14
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    radius: 8

                    color: confirmButton.down
                        ? "#1D4ED8"
                        : confirmButton.hovered
                            ? "#3B82F6"
                            : "#2563EB"
                }

                onClicked: {
                    modelLoadDialog.loadConfirmed(
                        modelLoadDialog.modelIndex
                    )

                    modelLoadDialog.close()
                }
            }
        }
    }
}