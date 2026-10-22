import QtQuick
import QtQuick.Controls

Rectangle {
    id: chatView

    property var chatModel

    property color surfaceColor
    property color borderColor
    property color textColor
    property color secondaryTextColor
    property color userBubbleColor
    property color assistantBubbleColor
    property color accentColor
    property color hoverColor
    property color pressedColor

    signal sourcesRequested(var sources)

    radius: 10
    border.width: 1
    border.color: chatView.borderColor
    color: chatView.surfaceColor

    Column {
        anchors.centerIn: parent
        width: parent.width - 48
        spacing: 12

        visible: chatView.chatModel.count === 0

        Image {
            anchors.horizontalCenter: parent.horizontalCenter
            source: "../../assets/logo_chat.png"
            width: 200
            height: 200
            fillMode: Image.PreserveAspectFit
            smooth: true
            opacity: 1.0
        }

        Label {
            width: parent.width
            text: "Vad vill du veta?"
            horizontalAlignment: Text.AlignHCenter
            font.pixelSize: 22
            font.bold: true
            color: chatView.textColor
        }
    }

    ListView {
        id: chatList

        anchors.fill: parent
        anchors.margins: 16

        spacing: 16
        clip: true

        model: chatView.chatModel
        visible: chatView.chatModel.count > 0

        ScrollBar.vertical: ScrollBar {}

        delegate: Item {
            id: messageDelegate

            required property string sender
            required property string message
            required property var sources
            required property int sourceCount

            width: ListView.view.width
            height: chatMessage.height

            ChatMessage {
                id: chatMessage

                width: messageDelegate.width

                sender: messageDelegate.sender
                message: messageDelegate.message
                sources: messageDelegate.sources
                sourceCount: messageDelegate.sourceCount

                textColor: chatView.textColor
                secondaryTextColor: chatView.secondaryTextColor
                userBubbleColor: chatView.userBubbleColor
                assistantBubbleColor: chatView.assistantBubbleColor
                accentColor: chatView.accentColor
                surfaceColor: chatView.surfaceColor
                hoverColor: chatView.hoverColor
                pressedColor: chatView.pressedColor

                onSourcesRequested: function(sources) {
                    chatView.sourcesRequested(sources)
                }
            }
        }

        onCountChanged: Qt.callLater(function() {
            chatList.positionViewAtEnd()
        })
    }

}