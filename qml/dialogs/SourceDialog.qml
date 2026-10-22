import QtQuick
import QtQuick.Controls

Dialog {
    id: sourceDialog

    property var sources: []

    property color surfaceColor
    property color textColor
    property color secondaryTextColor
    property color assistantBubbleColor

    signal knowledgeEntryRequested(int id)

    modal: true
    header: null

    background: Rectangle {
        color: sourceDialog.surfaceColor
        radius: 10
    }

    contentItem: ListView {
        anchors.fill: parent
        anchors.margins: 16

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