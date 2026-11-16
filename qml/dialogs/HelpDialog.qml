import QtQuick
import QtQuick.Controls

Dialog {
    id: helpDialog

    property color surfaceColor
    property color borderColor
    property color textColor
    property color secondaryTextColor
    property color accentColor
    property color hoverColor
    property color pressedColor

    title: translator.text(
        "help.title",
        translator.language
    )
    modal: true
    padding: 20
    closePolicy: Popup.CloseOnEscape

    background: Rectangle {
        color: helpDialog.surfaceColor
        radius: 12
        border.color: helpDialog.borderColor
        border.width: 1
    }

    header: Item {
        implicitHeight: 64

        Label {
            anchors.left: parent.left
            anchors.leftMargin: 20
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: closeButton.left
            anchors.rightMargin: 12

            text: helpDialog.title
            color: helpDialog.textColor
            font.pixelSize: 20
            font.bold: true
            elide: Text.ElideRight
        }

        Button {
            id: closeButton

            anchors.right: parent.right
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter

            width: 40
            height: 40
            hoverEnabled: true

            Accessible.name: translator.text(
                "help.close",
                translator.language
            )
            ToolTip.visible: hovered
            ToolTip.text: translator.text(
                "common.close",
                translator.language
            )

            contentItem: Text {
                text: "×"
                color: helpDialog.secondaryTextColor
                font.pixelSize: 26
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            background: Rectangle {
                radius: 8
                color: closeButton.down
                    ? helpDialog.pressedColor
                    : closeButton.hovered
                        ? helpDialog.hoverColor
                        : "transparent"
            }

            onClicked: helpDialog.close()
        }
    }

    contentItem: ScrollView {
        id: guideScroll

        clip: true
        contentWidth: availableWidth

        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
        ScrollBar.vertical.policy: ScrollBar.AsNeeded

        Column {
            width: guideScroll.availableWidth - 20
            spacing: 24

            Label {
                width: parent.width
                text: translator.text(
                    "help.intro",
                    translator.language
                )
                color: helpDialog.secondaryTextColor
                font.pixelSize: 14
                wrapMode: Text.WordWrap
                textFormat: Text.PlainText
            }

            Button {
                id: onlineManualButton

                width: parent.width
                height: manualButtonText.implicitHeight + 28
                padding: 14
                hoverEnabled: true

                text: translator.text(
                    "help.online_manual",
                    translator.language
                )

                Accessible.name: text

                contentItem: Text {
                    id: manualButtonText

                    text: onlineManualButton.text
                    color: helpDialog.accentColor
                    font.pixelSize: 14
                    font.bold: true
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    radius: 8

                    color: onlineManualButton.down
                        ? helpDialog.pressedColor
                        : onlineManualButton.hovered
                            ? helpDialog.hoverColor
                            : helpDialog.surfaceColor

                    border.color: helpDialog.accentColor
                    border.width: onlineManualButton.visualFocus ? 2 : 1
                }

                onClicked: {
                    Qt.openUrlExternally(
                        "https://xuenjing.github.io/Second-Brain/"
                    )
                }
            }

            Repeater {
                model: [
                    {
                        heading: "help.add_heading",
                        body: "help.add_body"
                    },
                    {
                        heading: "help.documents_heading",
                        body: "help.documents_body"
                    },
                    {
                        heading: "help.mail_heading",
                        body: "help.mail_body"
                    },
                    {
                        heading: "help.chat_heading",
                        body: "help.chat_body"
                    },
                    {
                        heading: "help.knowledge_heading",
                        body: "help.knowledge_body"
                    },
                    {
                        heading: "help.model_heading",
                        body: "help.model_body"
                    },
                    {
                        heading: "help.rag_heading",
                        body: "help.rag_body"
                    },
                    {
                        heading: "help.settings_heading",
                        body: "help.settings_body"
                    },
                    {
                        heading: "help.tray_heading",
                        body: "help.tray_body"
                    }
                ]

                delegate: Column {
                    required property var modelData

                    width: parent.width
                    spacing: 8

                    Label {
                        width: parent.width
                        text: translator.text(
                            modelData.heading,
                            translator.language
                        )
                        color: helpDialog.accentColor
                        font.pixelSize: 17
                        font.bold: true
                        wrapMode: Text.WordWrap
                        textFormat: Text.PlainText
                    }

                    Label {
                        width: parent.width
                        text: translator.text(
                            modelData.body,
                            translator.language
                        )
                        color: helpDialog.textColor
                        font.pixelSize: 14
                        wrapMode: Text.WordWrap
                        textFormat: Text.PlainText
                    }
                }
            }
        }
    }
}