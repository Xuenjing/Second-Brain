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
    id: root
    visible: true
    width: 800
    height: 600
    title: "Second Brain"

    Column {
        anchors.centerIn: parent
        spacing: 12
        width: parent.width - 80

        Button{
            text: "Lägg till kunskap"

            // Öppna dialogen där användaren kan skriva information."
            onClicked: knowledgeDialog.open()
        }

        Label {
            text: "Ställ en fråga"
        }

        TextField {
            id: inputField
            width: parent.width
            placeholderText: "Skriv din fråga här"
        }
    
        Button {
            text: "Skicka"

            onClicked: {
                const question = inputField.text.trim()

                // Skicka endast frågor som innehåller text.
                if (question.length > 0) {
                    chatDisplay.append("Du: " + question)

                    // Skicka frågan till en slot i Python.
                    backend.receive_text(question)
                    inputField.clear()
                }
            }
        }

        Label {
            text: "Konversation"
        }

        ScrollView {
            width: parent.width
            height: 300

            TextArea {
                id: chatDisplay
                readOnly: true
                wrapMode: TextArea.Wrap
                textFormat: TextEdit.PlainText
                placeholderText: "Dina frågor och svar visas här"
            }
        }
    }

    Dialog {
        id: knowledgeDialog
        title: "Lägg till kunskap"
        modal: true
        width: 500
        height: 350

        anchors.centerIn: parent
        parent: root.contentItem

        contentItem: Column {
            spacing: 12

            Label {
                text: "Skriv eller klistra in information:"
            }

            ScrollView {
                width: parent.width
                height: 200

                TextArea {
                    id: knowledgeInput
                    placeholderText: "Information till kunskapsbasen"
                    wrapMode: TextArea.Wrap
                    textFormat: TextEdit.PlainText
                }
            }
            Row {
                spacing: 12

                Button {
                    text: "Spara"

                    // Kopplar den till databasen senare.
                }

                Button {
                    text: "Importera .txt-fil"

                    // Koppar den senare.
                }

                Button {
                    text: "Stäng"
                    onClicked: knowledgeDialog.close()
                }
            }
        }
    }

    Connections {
        target: backend

        // Lägg till Python-svaret efter användarens fråga.
        function onReplyReady(reply) {
            chatDisplay.append("Assistent: " + reply + "\n")
        }
    }
}