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
    property color dangerBorderColor
    property color dangerHoverColor
    property color dangerPressedColor

    signal deleteRequested(int id)

    function loadKnowledge(id, text) {
        knowledgeId = id
        postText = text
        deleteKnowledgeStatus.text = ""
    }

    function setStatus(message) {
        deleteKnowledgeStatus.text = message
    }    

    title: translator.text(
        "delete_knowledge.title",
        translator.language
    )
    modal: true

    background: Rectangle {
        color: deleteKnowledgeDialog.surfaceColor
        radius: 12
        border.color: deleteKnowledgeDialog.borderColor
        border.width: 1
    }

    header: Item {
        implicitHeight: 56

        Label {
            anchors.left: parent.left
            anchors.leftMargin: 16
            anchors.right: closeDeleteButton.left
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter

            text: deleteKnowledgeDialog.title
            color: deleteKnowledgeDialog.textColor
            font.pixelSize: 18
            font.bold: true
            elide: Text.ElideRight
        }

        Button {
            id: closeDeleteButton

            width: 28
            height: 28
            padding: 0
            hoverEnabled: true

            anchors.right: parent.right
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter

            Accessible.name: translator.text(
                "common.cancel",
                translator.language
            )
            ToolTip.visible: hovered
            ToolTip.text: translator.text(
                "common.cancel",
                translator.language
            )

            contentItem: Item {
                Rectangle {
                    anchors.centerIn: parent
                    width: 14
                    height: 2
                    radius: 1
                    rotation: 45
                    color: deleteKnowledgeDialog.secondaryTextColor
                }

                Rectangle {
                    anchors.centerIn: parent
                    width: 14
                    height: 2
                    radius: 1
                    rotation: -45
                    color: deleteKnowledgeDialog.secondaryTextColor
                }
            }

            background: Rectangle {
                radius: 6
                color: closeDeleteButton.down
                    ? deleteKnowledgeDialog.pressedColor
                    : closeDeleteButton.hovered
                        ? deleteKnowledgeDialog.hoverColor
                        : "transparent"
            }

            onClicked: deleteKnowledgeDialog.close()
        }
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

        Button {
            id: confirmDeleteButton

            anchors.right: parent.right
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter

            width: 40
            height: 40
            padding: 0
            hoverEnabled: true

            Accessible.name: translator.text(
                "common.delete",
                translator.language
            )
            ToolTip.visible: hovered
            ToolTip.text: translator.text(
                "common.delete",
                translator.language
            )

            // Draw a trash-can icon.
            contentItem: Item {
                Item {
                    anchors.centerIn: parent
                    width: 20
                    height: 24

                    Rectangle {
                        x: 7
                        y: 1
                        width: 6
                        height: 5
                        radius: 1
                        color: "transparent"
                        border.color: deleteKnowledgeDialog.dangerColor
                        border.width: 2
                    }

                    Rectangle {
                        x: 2
                        y: 5
                        width: 16
                        height: 2
                        radius: 1
                        color: deleteKnowledgeDialog.dangerColor
                    }

                    Rectangle {
                        x: 4
                        y: 9
                        width: 12
                        height: 14
                        radius: 2
                        color: deleteKnowledgeDialog.dangerColor

                        Repeater {
                            model: 3

                            Rectangle {
                                required property int index

                                x: 3 + index * 3
                                y: 3
                                width: 1
                                height: 8
                                radius: 0.5
                                color: deleteKnowledgeDialog.surfaceColor
                            }
                        }
                    }
                }
            }

            background: Rectangle {
                radius: 8
                color: confirmDeleteButton.down
                    ? deleteKnowledgeDialog.dangerPressedColor
                    : confirmDeleteButton.hovered
                        ? deleteKnowledgeDialog.dangerHoverColor
                        : deleteKnowledgeDialog.surfaceColor

                border.color: deleteKnowledgeDialog.dangerBorderColor
                border.width: 1
            }

            onClicked: {
                deleteKnowledgeStatus.text = ""

                deleteKnowledgeDialog.deleteRequested(
                    deleteKnowledgeDialog.knowledgeId
                )
            }
        }
    }        
}