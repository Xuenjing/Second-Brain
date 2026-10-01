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
    // Mörkblå bakgrund för huvudfönstret.
    color: "#0B1220"

    Column {
        // Samma marginal upptill och på sidorna.
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 24
        spacing: 16

        // Appens namn och beskrivning.
        Label {
            text: "Second Brain"
            font.pixelSize: 28
            font.bold: true
            color: "#F1F5F9"
        }

        Label {
            text: "Ställ frågor om din sparade kunskap"
            font.pixelSize: 14
            color: "#94A3B8"
        }

        Row {
            spacing: 12

            Button {
                id: addKnowledgeButton
                text: "Lägg till kunskap"
                height: 40
                leftPadding: 16
                rightPadding: 16
                hoverEnabled: true

                contentItem: Text {
                    text: addKnowledgeButton.text
                    color: "#F1F5F9"
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    radius: 8
                    color: addKnowledgeButton.down ? "#243B55"
                        : addKnowledgeButton.hovered ? "#1E3350"
                        : "#152238"
                    border.color: "#38BDF8"
                    border.width: 1
                }
                // Öppna dialogen där användaren kan skriva information.
                onClicked: knowledgeDialog.open()
            }

            Button {
                id: viewKnowledgeButton
                text: "Visa kunskapsbas"
                height: 40
                leftPadding: 16
                rightPadding: 16
                hoverEnabled: true

                contentItem: Text {
                    text: viewKnowledgeButton.text
                    color: "#F1F5F9"
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    radius: 8
                    color: viewKnowledgeButton.down ? "#243B55"
                        : viewKnowledgeButton.hovered ? "#1E3350"
                        : "#152238"
                    border.color: "#38BDF8"
                    border.width: 1
                }

                // Öppna dialogen för sparad kunskap.
                onClicked: knowledgeViewDialog.open()
            }
        }

        Label {
            text: "Konversation"
            font.pixelSize: 16
            font.bold: true
            color: "#F1F5F9"
        }

        ScrollView {
            width: parent.width
            height: 220

            TextArea {
                id: chatDisplay
                readOnly: true
                wrapMode: TextArea.Wrap
                textFormat: TextEdit.PlainText
                placeholderText: "Dina frågor och svar visas här"

                // Ljus text mot en mörk bakgrund.
                color: "#F1F5F9"
                placeholderTextColor: "#94A3B8"
                font.pixelSize: 14
                padding: 16

                // Rundad bakgrund med en diskret kant.
                background: Rectangle {
                    color: "#152238"
                    radius: 10
                    border.color: "#2B405C"
                    border.width: 1
                }  
            }
        }

        Row {
            width: parent.width
            spacing: 12

            TextField {
                id: inputField
                width: parent.width - sendButton.width - parent.spacing
                placeholderText: "Skriv din fråga här"

                // Textfärg och luft runt frågan.
                color: "#F1F5F9"
                placeholderTextColor: "#94A3B8"
                font.pixelSize: 14
                padding: 12
                height: 44

                // Visa en blå kant när användaren skriver i fältet.
                background: Rectangle {
                    color: "#152238"
                    radius: 8
                    border.color: inputField.activeFocus ? "#38BDF8" : "#2B405C"
                    border.width: 1
                }
            }

            Button {
                id: sendButton
                text: "Skicka"
                height: 44
                width: 100
                hoverEnabled: true

                // Knappens text.
                contentItem: Text {
                    text: sendButton.text
                    color: "#FFFFFF"
                    font.pixelSize: 14
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                // Byt färg när muspekaren ligger över knappen eller den trycks ned.
                background: Rectangle {
                    radius: 8
                    color: sendButton.down ? "#1D4ED8"
                        : sendButton.hovered ? "#3B82F6"
                        : "#2563EB"
                }

                onClicked: {
                    const question = inputField.text.trim()

                    // Skicka endast frågor som innehåller text.
                    if (question.length > 0) {
                        chatDisplay.append("Du: " + question)

                        // Skicka frågan till Python.
                        backend.receive_text(question)
                        inputField.clear()
                    }
                }
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

        // Dialogens bakgrund.
        background: Rectangle {
            color: "#152238"
            radius: 12
            border.color: "#2B405C"
            border.width: 1
        }

        // Dialogens rubrik.
        header: Label {
            text: knowledgeDialog.title
            color: "#F1F5F9"
            font.pixelSize: 18
            font.bold: true
            padding: 16
        }

        contentItem: Column {
            spacing: 12

            Label {
                text: "Skriv eller klistra in information:"
                color: "#F1F5F9"
            }

            ScrollView {
                width: parent.width
                height: 200

                TextArea {
                    id: knowledgeInput
                    placeholderText: "Information till kunskapsbasen"
                    wrapMode: TextArea.Wrap
                    textFormat: TextEdit.PlainText

                    // Textfält för ny kunskap.
                    color: "#F1F5F9"
                    placeholderTextColor: "#94A3B8"
                    font.pixelSize: 14
                    padding: 12

                    background: Rectangle {
                        color: "#0B1220"
                        radius: 8
                        border.color: knowledgeInput.activeFocus ? "#38BDF8" : "#2B405C"
                        border.width: 1
                    }
                }
            }
            Row {
                spacing: 12

                Button {
                    id: saveKnowledgeButton
                    text: "Spara"
                    width: 90
                    height: 40
                    hoverEnabled: true

                    contentItem: Text {
                        text: saveKnowledgeButton.text
                        color: "#FFFFFF"
                        font.pixelSize: 14
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        radius: 8
                        color: saveKnowledgeButton.down ? "#1D4ED8"
                            : saveKnowledgeButton.hovered ? "#3B82F6"
                            : "#2563EB"
                    }

                    // Kopplas till databasen senare.
                }

                Button {
                    id: importFileButton
                    text: "Importera .txt-fil"
                    width: 160
                    height: 40
                    hoverEnabled: true

                    contentItem: Text {
                        text: importFileButton.text
                        color: "#F1F5F9"
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        radius: 8
                        color: importFileButton.down ? "#243B55"
                            : importFileButton.hovered ? "#1E3350"
                            : "#152238"
                        border.color: "#2B405C"
                        border.width: 1
                    }

                    // Kopplas senare.
                }

                Button {
                    id: closeKnowledgeButton
                    text: "Stäng"
                    width: 90
                    height: 40
                    hoverEnabled: true

                    contentItem: Text {
                        text: closeKnowledgeButton.text
                        color: "#F1F5F9"
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        radius: 8
                        color: closeKnowledgeButton.down ? "#243B55"
                            : closeKnowledgeButton.hovered ? "#1E3350"
                            : "#152238"
                        border.color: "#2B405C"
                        border.width: 1
                    }

                    // Stäng dialogen.
                    onClicked: knowledgeDialog.close()
                }
            }
        }
    }

    Dialog {
        id: knowledgeViewDialog
        title: "Kunskapsbas"
        modal: true
        width: Math.min(600, root.width - 48)
        height: Math.min(450, root.height - 48)
        parent: root.contentItem
        anchors.centerIn: parent

        background: Rectangle {
            color: "#152238"
            radius: 12
            border.color: "#2B405C"
            border.width: 1
        }

        header: Label {
            text: knowledgeViewDialog.title
            color: "#F1F5F9"
            font.pixelSize: 18
            font.bold: true
            padding: 16
        }

        // Scrollbar yta för poster som senare skickas från Python.
        contentItem: ScrollView {
            clip: true
            contentWidth: availableWidth

            TextArea {
                id: knowledgeDisplay
                readOnly: true
                wrapMode: TextArea.Wrap
                textFormat: TextEdit.PlainText
                placeholderText: "Sparad kunskap visas här när backend är inkopplad."
                color: "#F1F5F9"
                placeholderTextColor: "#94A3B8"
                font.pixelSize: 14
                padding: 12

                background: Rectangle {
                    color: "#0B1220"
                    radius: 8
                }
            }
        }

        // Standardknapp som stänger dialogen.
        footer: Item {
            implicitHeight: 64

            Button {
                id: closeKnowledgeViewButton
                text: "Stäng"
                width: 90
                height: 40

                anchors.right: parent.right
                anchors.rightMargin: 12
                anchors.verticalCenter: parent.verticalCenter
                hoverEnabled: true

                contentItem: Text {
                    text: closeKnowledgeViewButton.text
                    color: "#F1F5F9"
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    radius: 8
                    color: closeKnowledgeViewButton.down ? "#243B55"
                        : closeKnowledgeViewButton.hovered ? "#1E3350"
                        : "#152238"
                    border.color: "#2B405C"
                    border.width: 1
                }

                onClicked: knowledgeViewDialog.close()
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