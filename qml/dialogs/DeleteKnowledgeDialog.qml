import QtQuick
import QtQuick.Controls

Dialog {
    id: deleteKnowledgeDialog

    property int knowledgeId: -1
    property string postText: ""

    property color surfaceColor
    property color borderColor
    property color textColor
    property color secondaryTextColor
    property color hoverColor
    property color pressedColor
    property color dangerColor
    property color assistantBubbleColor

    signal deleteRequested(int id)

    function loadKnowledge(id, text) {
        knowledgeId = id
        postText = text
        deleteKnowledgeStatus.text = ""
    }

    function setStatus(message) {
        deleteKnowledgeStatus.text = message
    }    

    title: "Ta bort kunskap"
    modal: true

    background: Rectangle {
        color: deleteKnowledgeDialog.surfaceColor
        radius: 12
        border.color: deleteKnowledgeDialog.borderColor
        border.width: 1
    }

    header: Label {
        text: deleteKnowledgeDialog.title
        color: deleteKnowledgeDialog.textColor
        font.pixelSize: 18
        font.bold: true
        padding: 16
    }

    contentItem: Item {
        Label {
            id: deleteQuestion

            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right

            text: "Vill du ta bort den här kunskapsposten?"
            color: deleteKnowledgeDialog.textColor
            wrapMode: Text.WordWrap
        }

        ScrollView {
            anchors.top: deleteQuestion.bottom
            anchors.topMargin: 12

            anchors.left: parent.left
            anchors.right: parent.right

            anchors.bottom: deleteKnowledgeStatus.top
            anchors.bottomMargin: 12

            contentWidth: availableWidth
            clip: true

            TextArea {
                id: deleteKnowledgePreview

                text: deleteKnowledgeDialog.postText
                readOnly: true

                wrapMode: TextArea.Wrap
                textFormat: TextEdit.PlainText

                color: deleteKnowledgeDialog.textColor
                padding: 12

                background: Rectangle {
                    color: deleteKnowledgeDialog.assistantBubbleColor
                    radius: 8
                }
            }
        }

        Label {
            id: deleteKnowledgeStatus

            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom

            text: ""
            color: deleteKnowledgeDialog.dangerColor
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
                text: "Ta bort"
                width: 100
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
                    deleteKnowledgeStatus.text = ""

                    deleteKnowledgeDialog.deleteRequested(
                        deleteKnowledgeDialog.knowledgeId
                    )
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
                    color: deleteKnowledgeDialog.textColor
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    radius: 8

                    color: cancelDeleteButton.down
                        ? deleteKnowledgeDialog.pressedColor
                        : cancelDeleteButton.hovered
                            ? deleteKnowledgeDialog.hoverColor
                            : deleteKnowledgeDialog.surfaceColor

                    border.color: deleteKnowledgeDialog.borderColor
                    border.width: 1
                }

                onClicked: deleteKnowledgeDialog.close()
            }
        }
    }        
}