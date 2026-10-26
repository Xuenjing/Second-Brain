import QtQuick
import QtQuick.Controls

Dialog {
    id: sourceDialog

    property var sources: []

    property color surfaceColor
    property color textColor
    property color secondaryTextColor
    property color assistantBubbleColor
    property color hoverColor
    property color pressedColor

    signal knowledgeEntryRequested(int id)

    modal: true
    title: "Källor"


    header: Item {
        implicitHeight: 56

        Label {
            anchors.left: parent.left
            anchors.leftMargin: 16
            anchors.right: closeSourceButton.left
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter

            text: sourceDialog.title
            color: sourceDialog.textColor
            font.pixelSize: 18
            font.bold: true
            elide: Text.ElideRight
        }

        Button {
            id: closeSourceButton

            width: 28
            height: 28
            padding: 0
            hoverEnabled: true

            anchors.right: parent.right
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter

            Accessible.name: "Stäng"
            ToolTip.visible: hovered
            ToolTip.text: "Stäng"

            contentItem: Item {
                Rectangle {
                    anchors.centerIn: parent
                    width: 14
                    height: 2
                    radius: 1
                    rotation: 45
                    color: sourceDialog.secondaryTextColor
                }

                Rectangle {
                    anchors.centerIn: parent
                    width: 14
                    height: 2
                    radius: 1
                    rotation: -45
                    color: sourceDialog.secondaryTextColor
                }
            }

            background: Rectangle {
                radius: 6

                color: closeSourceButton.down
                    ? sourceDialog.pressedColor
                    : closeSourceButton.hovered
                        ? sourceDialog.hoverColor
                        : "transparent"
            }

            onClicked: sourceDialog.close()
        }
    }

    background: Rectangle {
        color: sourceDialog.surfaceColor
        radius: 10
    }

    contentItem: ListView {
        anchors.fill: parent

        anchors.leftMargin: 16
        anchors.rightMargin: 16
        anchors.bottomMargin: 16
        anchors.topMargin: 48

        model: sourceDialog.sources
        spacing: 12
        clip: true

        delegate: Rectangle {
            id: sourceItem

            required property int id
            required property string source
            required property string text
            required property real score
            required property string created_at

            width: ListView.view.width
            height: contentColumn.implicitHeight + 20
            radius: 8

            color: sourceDialog.assistantBubbleColor

            TapHandler {
                onTapped: {
                    sourceDialog.close()
                    sourceDialog.knowledgeEntryRequested(sourceItem.id)
                }
            }

            Column {
                id: contentColumn

                anchors.left: parent.left
                anchors.right: parent.right
                anchors.margins: 10
                anchors.verticalCenter: parent.verticalCenter

                spacing: 6

                Row {
                    spacing: 10

                    Text {
                        text: sourceItem.source
                        color: sourceDialog.textColor
                        font.bold: true
                    }

                    Text {
                        text: sourceItem.created_at
                            .replace("T", " ")
                            .slice(0, 16)

                        color: sourceDialog.secondaryTextColor
                        font.pixelSize: 11
                    }
                }

                Text {
                    text: sourceItem.text
                    width: parent.width
                    wrapMode: Text.WordWrap
                    color: sourceDialog.textColor
                }

                Text {
                    text: "Score: " + sourceItem.score.toFixed(3)
                    color: sourceDialog.secondaryTextColor
                    font.pixelSize: 11
                }
            }
        }
    }

}