import QtQuick
import QtQuick.Controls

Item {
    id: chatMessage

    property string sender
    property string message
    property var sources: []
    property int sourceCount

    property color textColor
    property color userBubbleColor
    property color assistantBubbleColor
    property color accentColor
    property color surfaceColor
    property color hoverColor
    property color pressedColor
    property color secondaryTextColor
    property bool isPending: false

    property bool isUser: sender === "user"

    // Helper function. 
    function uniqueSources() {
        let seen = {}
        let result = []

        if (!chatMessage.sources) {
            return result
        }

        for (let i = 0; i < chatMessage.sourceCount; i++) {
            let item = chatMessage.sources.get
                ? chatMessage.sources.get(i)
                : chatMessage.sources[i]

            if (item && !seen[item.source]) {
                seen[item.source] = true

                result.push({
                    source: item.source,
                    created_at: item.created_at
                })
            }
        }

        return result
    }

    signal sourcesRequested(var sources)

    height: Math.max(messageBubble.height, avatar.height)

    Item {
        id: avatar

        width: 32
        height: 32

        x: chatMessage.isUser
            ? chatMessage.width - width
            : 0

        Image {
            anchors.fill: parent
            source: "../../assets/logo4.png"
            fillMode: Image.PreserveAspectFit
            smooth: true
            visible: !chatMessage.isUser
        }

        Rectangle {
            anchors.fill: parent
            radius: 16
            color: "#1E40AF"
            border.color: "#38BDF8"
            visible: chatMessage.isUser

            Text {
                anchors.centerIn: parent
                text: "Du"
                color: "#F1F5F9"
                font.pixelSize: 12
                font.bold: true
            }
        }
    }

    Rectangle {
        id: messageBubble
        radius: 10

        width: Math.min(
            chatMessage.isPending
                ? thinkingRow.implicitWidth + 28
                : messageText.implicitWidth + 28,
            chatMessage.width * 0.8,
            chatMessage.width - avatar.width - 12
        )

        height: chatMessage.isPending
            ? thinkingRow.implicitHeight + 24
            : messageText.height + 24

        x: chatMessage.isUser
            ? avatar.x - width - 12
            : avatar.width + 12

        color: chatMessage.isUser
            ? chatMessage.userBubbleColor
            : chatMessage.assistantBubbleColor

        Text {
            id: messageText

            x: 14
            y: 12
            width: parent.width - 28

            visible: !chatMessage.isPending
            text: chatMessage.message
            textFormat: Text.PlainText
            wrapMode: Text.Wrap
            font.pixelSize: 14
            color: chatMessage.textColor
        }

        // Show an animated indicator while waiting for the answer.
        Row {
            id: thinkingRow

            x: 14
            y: 12
            spacing: 8
            visible: chatMessage.isPending

            Item {
                width: 20
                height: 20

                Item {
                    anchors.fill: parent

                    Repeater {
                        model: 8

                        Rectangle {
                            required property int index

                            width: 3
                            height: 3
                            radius: 1.5

                            x: 8.5 + 7 * Math.cos(index * Math.PI / 4)
                            y: 8.5 + 7 * Math.sin(index * Math.PI / 4)

                            color: chatMessage.accentColor
                            opacity: (index + 1) / 8
                        }
                    }

                    RotationAnimator on rotation {
                        from: 0
                        to: 360
                        duration: 1000
                        loops: Animation.Infinite
                        running: chatMessage.isPending
                    }
                }
            }

            Text {
                text: "Tänker…"
                color: chatMessage.textColor
                font.pixelSize: 14
                anchors.verticalCenter: parent.verticalCenter
            }
        }

        Button {
            id: sourceButton

            visible: chatMessage.sender === "assistant"
                && chatMessage.sourceCount > 0

            hoverEnabled: true
            text: "i"

            x: parent.width + 4
            y: (parent.height - height) / 2

            width: 24
            height: 24

            background: Rectangle {
                radius: 12

                color: sourceButton.down
                    ? chatMessage.pressedColor
                    : sourceButton.hovered
                        ? chatMessage.hoverColor
                        : chatMessage.assistantBubbleColor

                border.color: chatMessage.accentColor
                border.width: 1
            }

            contentItem: Text {
                text: "i"
                color: chatMessage.textColor
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            Timer {
                id: sourceHoverTimer
                interval: 1000
                repeat: false

                onTriggered: sourcePreview.open()
            }

            onHoveredChanged: {
                if (hovered) {
                    sourceHoverTimer.start()
                } else {
                    sourceHoverTimer.stop()
                    sourcePreview.close()
                }
            }

            onClicked: {
                chatMessage.sourcesRequested(chatMessage.sources)
            }
        }

        Popup {
            id: sourcePreview

            property var uniqueSourcesList: chatMessage.uniqueSources()

            width: 300
            height: previewContent.implicitHeight + 20

            x: sourceButton.x + sourceButton.width + 6
            y: sourceButton.y - 20

            padding: 10

            background: Rectangle {
                color: chatMessage.surfaceColor
                radius: 8
                border.color: chatMessage.accentColor
                border.width: 1
            }

            contentItem: Column {
                id: previewContent
                spacing: 6

                Text {
                    text: sourcePreview.uniqueSourcesList.length
                        + (sourcePreview.uniqueSourcesList.length === 1
                            ? " källa, "
                            : " källor, ")
                        + chatMessage.sourceCount
                        + (chatMessage.sourceCount === 1
                            ? " post"
                            : " poster")

                    color: chatMessage.textColor
                    font.pixelSize: 12
                    font.bold: true
                }

                Repeater {
                    model: sourcePreview.uniqueSourcesList

                    delegate: Row {
                        id: sourceRow

                        required property string source
                        required property string created_at

                        spacing: 8

                        Text {
                            text: sourceRow.source
                            color: chatMessage.textColor
                            font.pixelSize: 11
                        }

                        Text {
                            text: sourceRow.created_at
                                .replace("T", " ")
                                .slice(0, 16)

                            color: chatMessage.secondaryTextColor
                            font.pixelSize: 10
                        }
                    }
                }

                Text {
                    text: "Klicka för detaljer"
                    color: chatMessage.secondaryTextColor
                    font.pixelSize: 10
                    font.italic: true
                }
            }
        }

    }
}