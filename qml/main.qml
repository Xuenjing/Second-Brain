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
import QtQuick.Dialogs 


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

                // Öppna dialogen och hämta aktuella poster från databasen.
                onClicked: {
                    knowledgeViewDialog.open()
                    backend.load_all_knowledge()
                }
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
        height: 400

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

                    // Skicka texten till Python för att spara den.
                    onClicked: {
                        knowledgeSaveStatus.text = ""
                        backend.add_manual_knowledge(knowledgeInput.text)
                    }
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

                    onClicked: textFileDialog.open() 
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
            // Visa besked från Python om sparandet.
            Label {
                id: knowledgeSaveStatus
                width: parent.width
                text: ""
                color: "#F1F5F9"
                wrapMode: Text.WordWrap
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

        // Keep the search field separate from the results list.
        contentItem: Item {
            TextField {
                id: knowledgeSearchField
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
                height: 44
                placeholderText: "Sök bland sparad kunskap"

                color: "#F1F5F9"
                placeholderTextColor: "#94A3B8"
                font.pixelSize: 14
                padding: 12

                background: Rectangle {
                    color: "#0B1220"
                    radius: 8
                    border.color: knowledgeSearchField.activeFocus
                        ? "#38BDF8" : "#2B405C"
                    border.width: 1
                }

                // Update the results without replacing the search field.
                onTextEdited: backend.search_saved_knowledge(text)
            }

            ListView {
                id: knowledgeList
                anchors.top: knowledgeSearchField.bottom
                anchors.topMargin: 16
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                clip: true
                spacing: 12
                model: []

                ScrollBar.vertical: ScrollBar {}

                delegate: Rectangle {
                    id: postItem
                    required property var modelData

                    width: knowledgeList.width
                    height: Math.max(postContent.height, postActions.height) + 24
                    color: "#0B1220"
                    radius: 8

                    Column {
                        id: postContent
                        x: 12
                        y: 12
                        width: parent.width - postActions.width - 36
                        spacing: 8

                        Label {
                            width: parent.width
                            text: postItem.modelData.text
                            textFormat: Text.PlainText
                            wrapMode: Text.WordWrap
                            color: "#F1F5F9"
                        }

                        Label {
                            width: parent.width
                            text: "Källa: " + postItem.modelData.source
                                + " | Skapad: " + postItem.modelData.created_at
                            textFormat: Text.PlainText
                            wrapMode: Text.WordWrap
                            color: "#94A3B8"
                            font.pixelSize: 12
                        }
                    }

                    Column {
                        id: postActions
                        width: 100
                        spacing: 8

                        // Place the button to the right of the post text.
                        anchors.right: parent.right
                        anchors.rightMargin: 12
                        anchors.verticalCenter: parent.verticalCenter

                        Button {
                            id: editPostButton
                            text: "Redigera"
                            width: 100
                            height: 40

                            hoverEnabled: true

                            contentItem: Text {
                                text: editPostButton.text
                                color: "#F1F5F9"
                                font.pixelSize: 14
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }

                            // Match the other buttons with rounded corners and hover feedback.
                            background: Rectangle {
                                radius: 8
                                color: editPostButton.down ? "#243B55"
                                    : editPostButton.hovered ? "#1E3350"
                                    : "#152238"
                                border.color: "#38BDF8"
                                border.width: 1
                            }

                            onClicked: {
                                editKnowledgeDialog.knowledgeId = postItem.modelData.id
                                editKnowledgeInput.text = postItem.modelData.text
                                editKnowledgeStatus.text = ""
                                editKnowledgeDialog.open()
                            }
                        }

                        Button {
                            id: deletePostButton
                            text: "Ta bort"
                            width: 100
                            height: 40
                            hoverEnabled: true

                            contentItem: Text {
                                text: deletePostButton.text
                                color: "#FCA5A5"
                                font.pixelSize: 14
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }

                            background: Rectangle {
                                radius: 8
                                color: deletePostButton.down ? "#7F1D1D"
                                    : deletePostButton.hovered ? "#552020"
                                    : "#152238"
                                border.color: "#F87171"
                                border.width: 1
                            }

                            // Ask for confirmation before deleting the selected post.
                            onClicked: {
                                deleteKnowledgeDialog.knowledgeId = postItem.modelData.id
                                deleteKnowledgeDialog.postText = postItem.modelData.text
                                deleteKnowledgeStatus.text = ""
                                deleteKnowledgeDialog.open()
                            }
                        }
                    }
                }

                Label {
                    anchors.centerIn: parent
                    visible: knowledgeList.count === 0
                    text: "Inga kunskapsposter att visa."
                    color: "#94A3B8"
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

    Dialog {
        id: editKnowledgeDialog
        title: "Redigera kunskap"
        property int knowledgeId: -1

        modal: true
        width: Math.min(500, root.width - 48)
        height: Math.min(380, root.height - 48)
        parent: root.contentItem
        anchors.centerIn: parent

        background: Rectangle {
            color: "#152238"
            radius: 12
            border.color: "#2B405C"
        }

        header: Label {
            text: editKnowledgeDialog.title
            color: "#F1F5F9"
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
                    color: "#F1F5F9"
                    placeholderTextColor: "#94A3B8"
                    padding: 12

                    background: Rectangle {
                        color: "#0B1220"
                        radius: 8
                    }
                }
            }

            // Display feedback from the backend.
            Label {
                id: editKnowledgeStatus
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                text: ""
                color: "#F1F5F9"
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
                        color: saveEditButton.down ? "#1D4ED8"
                            : saveEditButton.hovered ? "#3B82F6"
                            : "#2563EB"
                    }

                    // Send the post id and updated text to Python.
                    onClicked: {
                        editKnowledgeStatus.text = ""
                        backend.edit_saved_knowledge(
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
                        color: "#F1F5F9"
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        radius: 8
                        color: cancelEditButton.down ? "#243B55"
                            : cancelEditButton.hovered ? "#1E3350"
                            : "#152238"
                        border.color: "#2B405C"
                        border.width: 1
                    }

                    onClicked: editKnowledgeDialog.close()
                }
            }
        }
    }

    Dialog {
        id: deleteKnowledgeDialog
        title: "Ta bort kunskap"
        property int knowledgeId: -1
        property string postText: ""

        modal: true
        width: Math.min(500, root.width - 48)
        height: Math.min(320, root.height - 48)
        parent: root.contentItem
        anchors.centerIn: parent

        background: Rectangle {
            color: "#152238"
            radius: 12
            border.color: "#2B405C"
        }

        header: Label {
            text: deleteKnowledgeDialog.title
            color: "#F1F5F9"
            font.pixelSize: 18
            font.bold: true
            padding: 16
        }

        contentItem: Column {
            spacing: 12

            Label {
                width: parent.width
                text: "Vill du ta bort den här kunskapsposten?"
                color: "#F1F5F9"
                wrapMode: Text.WordWrap
            }

            Label {
                width: parent.width
                text: deleteKnowledgeDialog.postText
                textFormat: Text.PlainText
                maximumLineCount: 4
                elide: Text.ElideRight
                wrapMode: Text.WordWrap
                color: "#94A3B8"
            }

            // Show feedback if the post could not be deleted.
            Label {
                id: deleteKnowledgeStatus
                width: parent.width
                text: ""
                color: "#FCA5A5"
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
                    id: confirmDeleteButton
                    text: "Ta bort"
                    width: 100
                    height: 40
                    hoverEnabled: true

                    contentItem: Text {
                        text: confirmDeleteButton.text
                        color: "#FFFFFF"
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        radius: 8
                        color: confirmDeleteButton.down ? "#991B1B"
                            : confirmDeleteButton.hovered ? "#EF4444"
                            : "#DC2626"
                    }

                    // Delete only after the user confirms.
                    onClicked: {
                        deleteKnowledgeStatus.text = ""
                        backend.delete_saved_knowledge(
                            deleteKnowledgeDialog.knowledgeId
                        )
                    }
                }

                Button {
                    id: cancelDeleteButton
                    text: "Avbryt"
                    width: 100
                    height: 40
                    hoverEnabled: true

                    contentItem: Text {
                        text: cancelDeleteButton.text
                        color: "#F1F5F9"
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        radius: 8
                        color: cancelDeleteButton.down ? "#243B55"
                            : cancelDeleteButton.hovered ? "#1E3350"
                            : "#152238"
                        border.color: "#2B405C"
                    }

                    onClicked: deleteKnowledgeDialog.close()
                }
            }
        }
    }

    FileDialog {
        id: textFileDialog
        title: "Välj en textfil"
        nameFilters: ["Text files (*.txt)"]

        onAccepted: {
            backend.add_txt_knowledge(selectedFile.toString())
        }
    }

    Connections {
        target: backend

        // Lägg till Python-svaret efter användarens fråga.
        function onReplyReady(reply) {
            chatDisplay.append("Assistent: " + reply + "\n")
        }

        // Ta emot beskedet om kunskapen sparades.
        function onKnowledgeSaveResult(message) {
            knowledgeSaveStatus.text = message
        }

        // Keep all post data, including the id, in the list model.
        function onKnowledgeLoaded(posts) {
            knowledgeList.model = posts
        }

        // Show the edit result and refresh the current search on success.
        function onKnowledgeEditResult(success, message) {
            editKnowledgeStatus.text = message

            if (success) {
                backend.search_saved_knowledge(knowledgeSearchField.text)
            }
        }

        // Close the dialog and refresh the current search after deletion.
        function onKnowledgeDeleteResult(success, message) {
            if (success) {
                deleteKnowledgeDialog.close()
                backend.search_saved_knowledge(knowledgeSearchField.text)
            } else {
                deleteKnowledgeStatus.text = message
            }
        }
    }
}