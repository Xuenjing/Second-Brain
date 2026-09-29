/*
    Huvudvy för applikationen.

    QML används för användargränssnittet.
    Exempel på komponenter som kan bli aktuella:
    - TextArea
    - Button
    - ScrollView
    - Connections

    Layout och funktionalitet bestäms under projektet.
*/

import QtQuick
import QtQuick.Controls


// Appens huvudfönster.
ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "Second Brain"

    Column {
        anchors.centerIn: parent
        spacing: 12

        TextField {
            id: inputField
            width: 300
            placeholderText: "Skriv ett meddelande"
        }
    
        Button {
            text: "Skicka"

            // Skicka textfältets innehåll till en slot i Python.
            onClicked: {
                backend.receive_text(inputField.text)
            }
        }

        Label {
            id: replyLabel
            text: ""
        }
    }

    Connections {
        target: backend

        // Ta emot Python-signalens svar och visa det i gränssittet.
        function onReplyReady(reply) {
            replyLabel.text = reply
        }
    }
}