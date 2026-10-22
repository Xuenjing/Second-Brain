import QtQuick
import QtQuick.Controls

Dialog {
    id: editKnowledgeDialog

    property int knowledgeId: -1

    property color surfaceColor
    property color borderColor
    property color textColor
    property color secondaryTextColor
    property color windowColor
    property color hoverColor
    property color pressedColor

    signal saveRequested(int id, string text)

    function loadKnowledge(id, text) {
    knowledgeId = id
    editKnowledgeInput.text = text
    editKnowledgeStatus.text = ""
    }

    function setStatus(message) {
        editKnowledgeStatus.text = message
    }

    title: "Redigera kunskap"
    modal: true

    background: Rectangle {
        color: editKnowledgeDialog.surfaceColor
        radius: 12
        border.color: editKnowledgeDialog.borderColor
        border.width: 1
    }

    header: Label {
        text: editKnowledgeDialog.title
        color: editKnowledgeDialog.textColor
        font.pixelSize: 18
        font.bold: true
        padding: 16
    }

    contentItem: Item {
        ScrollView {
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: editKnowledgeStatus.top
            anchors.bottomMargin: 12

            contentWidth: availableWidth
            clip: true

            TextArea {
                id: editKnowledgeInput

                placeholderText: "Ändra kunskapspostens text"
                wrapMode: TextArea.Wrap
                textFormat: TextEdit.PlainText

                color: editKnowledgeDialog.textColor
                placeholderTextColor: editKnowledgeDialog.secondaryTextColor
                padding: 12

                background: Rectangle {
                    color: editKnowledgeDialog.windowColor
                    radius: 8
                }
            }
        }

        Label {
            id: editKnowledgeStatus

            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom

            text: ""
            color: editKnowledgeDialog.textColor
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
                id: saveEditButton
                text: "Spara"
                width: 100
                height: 40
                hoverEnabled: true

                contentItem: Text {
                    text: saveEditButton.text
                    color: "#FFFFFF"
                    font.pixelSize: 14
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    radius: 8

                    color: saveEditButton.down
                        ? "#1D4ED8"
                        : saveEditButton.hovered
                            ? "#3B82F6"
                            : "#2563EB"
                }

                onClicked: {
                    editKnowledgeStatus.text = ""

                    editKnowledgeDialog.saveRequested(
                        editKnowledgeDialog.knowledgeId,
                        editKnowledgeInput.text
                    )
                }
            }

            Button {
                id: cancelEditButton
                text: "Avbryt"
                width: 100
                height: 40
                hoverEnabled: true

                contentItem: Text {
                    text: cancelEditButton.text
                    color: editKnowledgeDialog.textColor
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    radius: 8

                    color: cancelEditButton.down
                        ? editKnowledgeDialog.pressedColor
                        : cancelEditButton.hovered
                            ? editKnowledgeDialog.hoverColor
                            : editKnowledgeDialog.surfaceColor

                    border.color: editKnowledgeDialog.borderColor
                    border.width: 1
                }

                onClicked: editKnowledgeDialog.close()
            }
        }
    }    
}