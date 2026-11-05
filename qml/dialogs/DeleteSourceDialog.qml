import QtQuick
import QtQuick.Controls

Dialog {
    id: deleteSourceDialog

    title: "Ta bort källa"

    property string sourceName: ""
    property int entryCount: 0

    property color surfaceColor
    property color borderColor
    property color textColor
    property color secondaryTextColor
    property color hoverColor
    property color pressedColor
    property color dangerColor
    property color dangerBorderColor
    property color dangerHoverColor
    property color dangerPressedColor    

    signal deleteConfirmed(string source)

    modal: true
    standardButtons: Dialog.NoButton

    background: Rectangle {
        color: deleteSourceDialog.surfaceColor
        radius: 12
        border.color: deleteSourceDialog.borderColor
        border.width: 1
    }

    header: Rectangle {
        implicitHeight: 56
        color: deleteSourceDialog.surfaceColor

        Label {
            anchors.fill: parent
            anchors.leftMargin: 16

            text: deleteSourceDialog.title
            color: deleteSourceDialog.textColor
            font.pixelSize: 18
            font.bold: true

            verticalAlignment: Text.AlignVCenter
        }
    }

    contentItem: Column {
        spacing: 12

        Label {
            width: parent.width

            text: "Vill du ta bort alla kunskapsposter från den här källan?"

            color: deleteSourceDialog.textColor
            wrapMode: Text.WordWrap
        }

        Label {
            width: parent.width

            text: deleteSourceDialog.sourceName

            color: deleteSourceDialog.secondaryTextColor
            font.pixelSize: 14
            wrapMode: Text.WordWrap
        }

        Label {
            width: parent.width

            text: deleteSourceDialog.entryCount
                + " kunskapsposter kommer att tas bort."

            color: deleteSourceDialog.secondaryTextColor
            font.pixelSize: 12
            wrapMode: Text.WordWrap
        }

        Label {
            width: parent.width

            text: "Detta går inte att ångra."

            color: deleteSourceDialog.dangerColor
            wrapMode: Text.WordWrap
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
                id: confirmDeleteButton

                text: "Ta bort alla"
                width: 120
                height: 40
                hoverEnabled: true

                contentItem: Text {
                    text: confirmDeleteButton.text
                    color: "#FFFFFF"
                    font.pixelSize: 14

                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    radius: 8

                    color: confirmDeleteButton.down
                        ? "#991B1B"
                        : confirmDeleteButton.hovered
                            ? "#EF4444"
                            : "#DC2626"
                }

                onClicked: {
                    deleteSourceDialog.deleteConfirmed(
                        deleteSourceDialog.sourceName
                    )

                    deleteSourceDialog.close()
                }
            }

            Button {
                id: cancelDeleteButton

                text: "Avbryt"
                width: 100
                height: 40
                hoverEnabled: true

                contentItem: Text {
                    text: cancelDeleteButton.text
                    color: deleteSourceDialog.textColor
                    font.pixelSize: 14

                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    radius: 8

                    color: cancelDeleteButton.down
                        ? deleteSourceDialog.pressedColor
                        : cancelDeleteButton.hovered
                            ? deleteSourceDialog.hoverColor
                            : deleteSourceDialog.surfaceColor

                    border.color: deleteSourceDialog.borderColor
                    border.width: 1
                }

                onClicked: deleteSourceDialog.close()
            }
        }
    }
}