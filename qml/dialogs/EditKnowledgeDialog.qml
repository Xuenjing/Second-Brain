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
    property color assistantBubbleColor
    property color accentColor

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

    header: Item {
        implicitHeight: 56

        Label {
            anchors.left: parent.left
            anchors.leftMargin: 16
            anchors.right: closeEditButton.left
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter

            text: editKnowledgeDialog.title
            color: editKnowledgeDialog.textColor
            font.pixelSize: 18
            font.bold: true
            elide: Text.ElideRight
        }

        Button {
            id: closeEditButton

            width: 28
            height: 28
            padding: 0
            hoverEnabled: true

            anchors.right: parent.right
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter

            Accessible.name: "Stäng utan att spara"
            ToolTip.visible: hovered
            ToolTip.text: "Stäng utan att spara"

            contentItem: Item {
                Rectangle {
                    anchors.centerIn: parent
                    width: 14
                    height: 2
                    radius: 1
                    rotation: 45
                    color: editKnowledgeDialog.secondaryTextColor
                }

                Rectangle {
                    anchors.centerIn: parent
                    width: 14
                    height: 2
                    radius: 1
                    rotation: -45
                    color: editKnowledgeDialog.secondaryTextColor
                }
            }

            background: Rectangle {
                radius: 6
                color: closeEditButton.down
                    ? editKnowledgeDialog.pressedColor
                    : closeEditButton.hovered
                        ? editKnowledgeDialog.hoverColor
                        : "transparent"
            }

            onClicked: editKnowledgeDialog.close()
        }
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
                    color: editKnowledgeDialog.assistantBubbleColor
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

        Button {
            id: saveEditButton

            anchors.right: parent.right
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter

            width: 40
            height: 40
            padding: 0
            hoverEnabled: true

            Accessible.name: "Spara ändringar"
            ToolTip.visible: hovered
            ToolTip.text: "Spara ändringar"

            // Draw a floppy-disk icon.
            contentItem: Item {
                Rectangle {
                    anchors.centerIn: parent
                    width: 22
                    height: 22
                    radius: 2
                    color: editKnowledgeDialog.accentColor

                    Rectangle {
                        x: 5
                        y: 2
                        width: 12
                        height: 7
                        radius: 1
                        color: editKnowledgeDialog.surfaceColor

                        Rectangle {
                            x: 8
                            y: 1
                            width: 2
                            height: 5
                            color: editKnowledgeDialog.accentColor
                        }
                    }

                    Rectangle {
                        x: 4
                        y: 13
                        width: 14
                        height: 7
                        radius: 1
                        color: editKnowledgeDialog.surfaceColor

                        Rectangle {
                            x: 3
                            y: 2
                            width: 8
                            height: 1
                            color: editKnowledgeDialog.accentColor
                        }

                        Rectangle {
                            x: 3
                            y: 4
                            width: 8
                            height: 1
                            color: editKnowledgeDialog.accentColor
                        }
                    }
                }
            }

            background: Rectangle {
                radius: 8
                color: saveEditButton.down
                    ? editKnowledgeDialog.pressedColor
                    : saveEditButton.hovered
                        ? editKnowledgeDialog.hoverColor
                        : editKnowledgeDialog.surfaceColor

                border.color: editKnowledgeDialog.accentColor
                border.width: 1
            }

            onClicked: {
                editKnowledgeStatus.text = ""

                editKnowledgeDialog.saveRequested(
                    editKnowledgeDialog.knowledgeId,
                    editKnowledgeInput.text
                )
            }
        }
    }    
}