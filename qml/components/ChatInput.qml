import QtQuick
import QtQuick.Controls

Row {
    id: chatInput

    property bool isThinking: false

    property color textColor
    property color secondaryTextColor
    property color surfaceColor
    property color borderColor
    property color accentColor
    property color hoverColor
    property color pressedColor

    signal questionSubmitted(string question)
    signal cancelRequested()

    spacing: 12

    TextField {
        id: inputField

        width: chatInput.width - sendButton.width - chatInput.spacing

        placeholderText: translator.text(
            "chat_input.placeholder",
            translator.language
        )

        color: chatInput.textColor
        placeholderTextColor: chatInput.secondaryTextColor
        font.pixelSize: 14
        padding: 12
        height: 44

        background: Rectangle {
            color: chatInput.surfaceColor
            radius: 8
            border.color: inputField.activeFocus
                ? chatInput.accentColor
                : chatInput.borderColor
            border.width: 1
        }
    }

    Button {
        id: cancelButton

        text: "Avbryt"
        width: 100
        height: 44

        visible: false
        hoverEnabled: true

        contentItem: Text {
            text: translator.text(
                "common.cancel",
                translator.language
            )
            color: "#FFFFFF"
            font.pixelSize: 14
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        background: Rectangle {
            radius: 8
            color: cancelButton.down
                ? "#991B1B"
                : cancelButton.hovered
                    ? "#EF4444"
                    : "#DC2626"
        }

        onClicked: {
            chatInput.cancelRequested()
        }
    }

    Button {
        id: sendButton

        text: "Skicka"
        width: 100
        height: 44
        hoverEnabled: true

        enabled: !chatInput.isThinking

        contentItem: Text {
            text: translator.text(
                "chat_input.send",
                translator.language
            )
            color: "#FFFFFF"
            font.pixelSize: 14
            font.bold: true
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        background: Rectangle {
            radius: 8
            color: sendButton.down
                ? "#1D4ED8"
                : sendButton.hovered
                    ? "#3B82F6"
                    : "#2563EB"
        }

        onClicked: {
            const question = inputField.text.trim()

            if (question.length > 0) {
                chatInput.questionSubmitted(question)
                inputField.clear()
            }
        }
    }

}