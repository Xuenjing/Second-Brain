/*
    Main application interface.

    Displays:
    - A chat for asking questions and viewing answers.
    - Options for adding, viewing, editing and deleting saved knowledge.

    Communicates with the Python backend through slots and signals.
*/

import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs

import "components"
import "dialogs"


// Main application window.
ApplicationWindow {
    id: root

    // Choose between dark and light mode.
    property bool darkMode: true

    // Shared colors for dark mode and the Ice Blue light theme.
    readonly property color windowColor: darkMode ? "#0B1220" : "#EFF6FF"
    readonly property color surfaceColor: darkMode ? "#152238" : "#FFFFFF"

    readonly property color textColor: darkMode ? "#F1F5F9" : "#0F172A"
    readonly property color secondaryTextColor: darkMode ? "#94A3B8" : "#475569"

    readonly property color borderColor: darkMode ? "#2B405C" : "#BFDBFE"
    readonly property color accentColor: darkMode ? "#38BDF8" : "#2563EB"

    readonly property color hoverColor: darkMode ? "#1E3350" : "#DBEAFE"
    readonly property color pressedColor: darkMode ? "#243B55" : "#BFDBFE"

    // Chat bubble backgrounds.
    readonly property color userBubbleColor: darkMode ? "#1E40AF" : "#BFDBFE"
    readonly property color assistantBubbleColor: darkMode ? "#243B55" : "#DBEAFE"

    // Colors for delete actions.
    readonly property color dangerColor: darkMode ? "#FCA5A5" : "#B91C1C"
    readonly property color dangerBorderColor: darkMode ? "#F87171" : "#DC2626"
    readonly property color dangerHoverColor: darkMode ? "#552020" : "#FEE2E2"
    readonly property color dangerPressedColor: darkMode ? "#7F1D1D" : "#FECACA"

    // Track whether a question is being processed.
    property bool isThinking: false

    // Store questions and answers displayed in the chat.
    ListModel {
        id: chatModel
    }

    visible: true
    width: 1000
    height: 700
    title: "Second Brain"
    color: root.windowColor

    Column {
        // Fill the window's content area with equal margins.
        anchors.fill: parent
        anchors.margins: 24
        anchors.bottomMargin: 36
        spacing: 16

        // Application name, logo and settings button.
        Header {
            width: parent.width

            textColor: root.textColor
            accentColor: root.accentColor
            hoverColor: root.hoverColor
            pressedColor: root.pressedColor
            surfaceColor: root.surfaceColor

            onSettingsClicked: settingsDialog.open()
        }

        // Place the knowledge buttons next to each other.
        Row {
            spacing: 12

            Button {
                id: addKnowledgeButton
                text: "Lägg till kunskap"
                height: 40
                leftPadding: 16
                rightPadding: 16
                hoverEnabled: true

                // Center the button text.
                contentItem: Text {
                    text: addKnowledgeButton.text
                    color: root.textColor
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                // Change background color when hovered or pressed.
                background: Rectangle {
                    radius: 8
                    color: addKnowledgeButton.down ? root.pressedColor
                        : addKnowledgeButton.hovered ? root.hoverColor
                        : root.surfaceColor
                    border.color: root.accentColor
                    border.width: 1
                }

                // Open the dialog for adding knowledge.
                onClicked: knowledgeDialog.open()
            }

            Button {
                id: viewKnowledgeButton
                text: "Visa kunskapsposter"
                height: 40
                leftPadding: 16
                rightPadding: 16
                hoverEnabled: true

                // Center the button text.
                contentItem: Text {
                    text: viewKnowledgeButton.text
                    color: root.textColor
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                // Change background color when hovered or pressed.
                background: Rectangle {
                    radius: 8
                    color: viewKnowledgeButton.down ? root.pressedColor
                        : viewKnowledgeButton.hovered ? root.hoverColor
                        : root.surfaceColor
                    border.color: root.accentColor
                    border.width: 1
                }

                // Open the dialog and load saved knowledge.
                onClicked: {
                    knowledgeViewDialog.open()
                    knowledgeViewDialog.requestRefresh()
                }
            }

            // Adds a dropdown menu for selection of LLM
            ComboBox {
                id: modelSelector

                width: 305
                height: 40

                model: [
                    "Qwen3 0.6B — Snabb",
                    "Qwen3 1.7B — Rekommenderas",
                    "Qwen3 4B — Långsam"
                ]

                currentIndex: 1

                // Show an arrow using the current theme color.
                indicator: Text {
                    x: modelSelector.width - width - 12
                    width: 16
                    height: modelSelector.height
                    text: "\u25BE"
                    color: root.textColor
                    font.pixelSize: 18
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                contentItem: Text {
                    text: modelSelector.displayText
                    color: root.textColor
                    font.pixelSize: 14

                    leftPadding: 12
                    rightPadding: 32

                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                }

                background: Rectangle {
                    color: root.surfaceColor
                    radius: 8
                    border.color: modelSelector.activeFocus
                        ? root.accentColor
                        : root.borderColor
                    border.width: 1
                }

                // Dictates how every row in dropdown should act
                delegate: ItemDelegate {
                    width: ListView.view.width
                    height: 40
                    hoverEnabled: true

                    contentItem: Text {
                        text: modelData
                        color: root.textColor
                        font.pixelSize: 14
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: 12
                    }

                    // Highlight rows when navigating or hovering.
                    background: Rectangle {
                        radius: 6
                        color: parent.highlighted ? root.pressedColor
                            : parent.hovered ? root.hoverColor
                            : root.surfaceColor
                    }
                }

                // The popup when the dropdown is clicked
                popup: Popup {
                    y: modelSelector.height + 4
                    width: modelSelector.width
                    padding: 1

                    contentItem: ListView {
                        implicitHeight: contentHeight
                        clip: true

                        model: modelSelector.popup.visible
                            ? modelSelector.delegateModel
                            : null

                        currentIndex: modelSelector.highlightedIndex
                    }

                    background: Rectangle {
                        color: root.surfaceColor
                        radius: 8
                        border.color: root.borderColor
                        border.width: 1
                    }
                }
            }

            // Add a load model button next to the dropdown menu.
            Button {
                id: loadModelButton
                text: "Ladda modell"
                height: 40
                leftPadding: 16
                rightPadding: 16
                hoverEnabled: true                

                // Center the button text.
                contentItem: Text {
                    text: loadModelButton.text
                    color: root.accentColor
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                // Change background color when hovered or pressed.
                background: Rectangle {
                    radius: 8
                    color: loadModelButton.down ? root.pressedColor
                        : loadModelButton.hovered ? root.hoverColor
                        : root.surfaceColor
                    border.width: 1
                }

                // Load the model when clicked.
                onClicked: {

                }
            }
        }


        // Conversation title.
        // Keep the chat heading and thinking indicator on the same line.
        Item {
            width: parent.width
            height: 32

            // Show an animated indicator while processing a question.
            Row {
                x: 16
                anchors.leftMargin: 16
                anchors.verticalCenter: parent.verticalCenter
                spacing: 8
                visible: root.isThinking

                // Show a rotating blue ring while processing.
                Item {
                    width: 24
                    height: 24

                    Rectangle {
                        id: thinkingRing
                        anchors.centerIn: parent
                        width: 20
                        height: 20
                        radius: 10
                        color: "transparent"
                        border.color: root.accentColor
                        border.width: 2

                        Rectangle {
                            width: 6
                            height: 6
                            radius: 3
                            color: root.windowColor
                            anchors.horizontalCenter: parent.horizontalCenter
                            y: -2
                        }

                        RotationAnimator on rotation {
                            from: 0
                            to: 360
                            duration: 1000
                            loops: Animation.Infinite
                            running: root.isThinking
                        }
                    }
                }

                Label {
                    text: "Tänker…"
                    color: root.textColor
                    font.pixelSize: 14
                    font.bold: true
                    anchors.verticalCenter: parent.verticalCenter
                }
            }
        }

// Show a welcome message or the conversation.
Rectangle {
    id: chatPanel
    width: parent.width
    height: Math.max(
        0,
        parent.height - y - questionRow.height - parent.spacing
    )
    color: root.surfaceColor
    radius: 10
    border.color: root.borderColor
    border.width: 1

    // Show the welcome view while the chat is empty.
    Column {
        anchors.centerIn: parent
        width: parent.width - 48
        spacing: 12
        visible: chatModel.count === 0

        // Display a muted logo in the empty chat.
        Image {
            anchors.horizontalCenter: parent.horizontalCenter
            source: "../assets/logo_chat.png"
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
            color: root.textColor
        }
    }

        // Display each message as a separate bubble.
        ListView {
            id: chatList
            anchors.fill: parent
            anchors.margins: 16
            spacing: 16
            clip: true
            model: chatModel
            visible: chatModel.count > 0

            ScrollBar.vertical: ScrollBar {}

            delegate: Item {
            id: messageItem

            required property string sender
            required property string message
            required property var sources
            required property int sourceCount

            property bool isUser: sender === "user"

            width: ListView.view.width
            height: Math.max(messageBubble.height, avatar.height)

            // Helper function that builds a unique list of popup-sources.
            function uniqueSources() {
                let seen = {}
                let result = []

                for (let i = 0; i <messageItem.sources.count; i++) {
                    let item = messageItem.sources.get(i)

                    if(!seen[item.source]) {
                        seen[item.source] = true

                        result.push({
                            source: item.source,
                            created_at: item.created_at
                        })
                    }
                }
                return result
            }

        // Dialog for opening the source-information.
        Dialog {
            id: sourceDialog

            property var sources: []

            parent: Overlay.overlay
            modal: true

            width: 700
            height: 600

            x: (parent.width - width) / 2
            y: (parent.height - height) / 2

            header: null

            background: Rectangle {
                color: root.surfaceColor
                radius: 10
            }

            // Listing the sources inside the dialogue.
            ListView {
                anchors.fill: parent
                anchors.margins: 16

                model: sourceDialog.sources
                spacing: 12
                clip: true

                delegate: Rectangle {
                    id: sourceItem

                    required property int id
                    required property string source
                    required property string text
                    required property real score
                    required property string created_at

                    width: ListView.view.width
                    height: contentColumn.implicitHeight + 20
                    radius: 8

                    color: root.assistantBubbleColor

                    // Makes the sources clickable.
                    TapHandler {
                        onTapped: {
                            sourceDialog.close()
                            backend.open_knowledge_entry(sourceItem.id)
                        }
                    }

                    Column {
                        id: contentColumn

                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.margins: 10
                        anchors.verticalCenter: parent.verticalCenter

                        spacing: 6

                        // Row containing source + created at
                        Row {
                            spacing: 10

                            Text {
                            text: sourceItem.source
                            color: root.textColor
                            font.bold: true
                            }

                            Text {
                                text: sourceItem.created_at
                                    .replace("T", " ")
                                    .slice(0, 16)
                                color: root.secondaryTextColor
                                font.pixelSize: 11
                            }
                        }

                        Text {
                            text: sourceItem.text
                            width: parent.width
                            wrapMode: Text.WordWrap
                            color: root.textColor
                        }

                        Text {
                            text: "Score: " + sourceItem.score.toFixed(3)
                            color: root.secondaryTextColor
                            font.pixelSize: 11
                        }

                    }

                }
            }
        }

            // Show assistant logo.
            Item {
                id: avatar
                width: 32
                height: 32

                x: messageItem.isUser
                    ? messageItem.width - width
                    : 0

                Image {
                    anchors.fill: parent
                    source: "../assets/logo4.png"
                    fillMode: Image.PreserveAspectFit
                    smooth: true
                    visible: !messageItem.isUser
                }

                Rectangle {
                    anchors.fill: parent
                    radius: 16
                    color: "#1E40AF"
                    border.color: "#38BDF8"
                    visible: messageItem.isUser

                    Text {
                        anchors.centerIn: parent
                        text: "Du"
                        color: "#F1F5F9"
                        font.pixelSize: 12
                        font.bold: true
                    }
                }
            }

            // Leave space between the bubble and the avatar.
            Rectangle {
                id: messageBubble

                width: Math.min(
                    messageText.implicitWidth + 28,
                    messageItem.width * 0.8,
                    messageItem.width - avatar.width - 12
                )
                height: messageText.height + 24
                radius: 10

                x: messageItem.isUser
                    ? avatar.x - width - 12
                    : avatar.width + 12

                color: messageItem.isUser
                    ? root.userBubbleColor
                    : root.assistantBubbleColor

                Text {
                    id: messageText
                    x: 14
                    y: 12
                    width: parent.width - 28

                    text: messageItem.message
                    textFormat: Text.PlainText
                    wrapMode: Text.Wrap
                    font.pixelSize: 14
                    color: root.textColor
                }

                // Button for showing sources.
                Button {
                    id: sourceButton

                    visible: messageItem.sender === "assistant"
                    && messageItem.sourceCount > 0

                    hoverEnabled: true

                    text: "i"

                    x: parent.width + 4
                    y: (parent.height - height) / 2

                    width: 24
                    height: 24

                    background: Rectangle {
                        radius: 12
                        color: sourceButton.down ? root.pressedColor
                            : sourceButton.hovered ? root.hoverColor
                            : root.assistantBubbleColor
                        border.color: root.accentColor
                        border.width: 1
                    }

                    contentItem: Text {
                        text: "i"
                        color: root.textColor
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    Timer {
                        id: sourceHoverTimer
                        interval: 1000
                        repeat: false

                        onTriggered: {
                            sourcePreview.open()
                        }
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
                        sourceDialog.sources = messageItem.sources
                        sourceDialog.open()
                    }
                }

                Popup {
                    id: sourcePreview

                    property var uniqueSourcesList: messageItem.uniqueSources()
                    
                    width: 300
                    height: previewContent.implicitHeight + 20


                    
                    x: sourceButton.x + sourceButton.width + 6
                    y: sourceButton.y - 20

                    padding: 10

                    background: Rectangle {
                        color: root.surfaceColor
                        radius: 8
                        border.color: root.accentColor
                        border.width: 1
                    }


                    contentItem: Column {
                        id: previewContent
                        spacing: 6

                        Text {
                            text: sourcePreview.uniqueSourcesList.length
                                + (sourcePreview.uniqueSourcesList.length === 1 ? " källa, " : " källor, ")
                                + messageItem.sourceCount
                                + (messageItem.sourceCount === 1 ? " post" : " poster")

                            color: root.textColor
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
                                    color: root.textColor
                                    font.pixelSize: 11
                                }

                                Text {
                                    text: sourceRow.created_at
                                        .replace("T", " ")
                                        .slice(0, 16)

                                    color: root.secondaryTextColor
                                    font.pixelSize: 10
                                }
                                



                            }
                        }

                        Text {
                            text: "Klicka för detaljer"
                            color: root.secondaryTextColor
                            font.pixelSize: 10
                            font.italic: true
                        }
                    }
                }
            }
        }

            // Scroll to the latest message after the list updates.
            onCountChanged: Qt.callLater(function() {
                chatList.positionViewAtEnd()
            })
        }
    }

        // Place the question field and send button next to each other.
        Row {
            id: questionRow
            width: parent.width
            spacing: 12

            TextField {
                id: inputField

                // Leave room for the buttons beside the input field.
                width: parent.width - sendButton.width -
                    (root.isThinking
                            ? cancelButton.width + 2 * parent.spacing
                            : parent.spacing)

                placeholderText: "Skriv din fråga här"

                // Text colors plus extra space inside the field.
                color: root.textColor
                placeholderTextColor: root.secondaryTextColor
                font.pixelSize: 14
                padding: 12
                height: 44

                // Highlight the border when the field has keyboard focus.
                background: Rectangle {
                    color: root.surfaceColor
                    radius: 8
                    border.color: inputField.activeFocus
                        ? root.accentColor
                        : root.borderColor
                    border.width: 1
                }
            }

            Button {
                id: cancelButton
                text: "Avbryt"
                width: 100
                height: 44
                visible: root.isThinking
                hoverEnabled: true

                contentItem: Text {
                    text: cancelButton.text
                    color: "#FFFFFF"
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    radius: 8
                    color: cancelButton.down ? "#991B1B"
                        : cancelButton.hovered ? "#EF4444"
                        : "#DC2626"
                }

                // onClicked: backend.cancel_question()
            }

            Button {
                id: sendButton
                text: "Skicka"

                // Prevent sending another question while processing.
                enabled: !root.isThinking

                height: 44
                width: 100
                hoverEnabled: true

                // Center the button's text.
                contentItem: Text {
                    text: sendButton.text
                    color: "#FFFFFF"
                    font.pixelSize: 14
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                // Change background color when hovered or pressed.
                background: Rectangle {
                    radius: 8
                    color: sendButton.down ? "#1D4ED8"
                        : sendButton.hovered ? "#3B82F6"
                        : "#2563EB"
                }

                onClicked: {
                    // Remove whitespace from the beginning and end.
                    const question = inputField.text.trim()

                    // Send only questions that contain text.
                    if (question.length > 0) {
                        // Add the question to the chat.
                        chatModel.append({
                            sender: "user",
                            message: question,
                            sources: [],
                            sourceCount: 0
                        })

                        // Send the question to Python and clear the input field.
                        backend.receive_text(question)
                        inputField.clear()
                    }
                }
            }
        }
    }

    // Dialog for application settings.
    SettingsDialog {
        id: settingsDialog

        parent: root.contentItem
        anchors.centerIn: parent

        width: Math.min(500, root.width - 48)
        height: Math.min(400, root.height - 48)

        darkMode: root.darkMode

        surfaceColor: root.surfaceColor
        borderColor: root.borderColor
        textColor: root.textColor
        secondaryTextColor: root.secondaryTextColor
        accentColor: root.accentColor
        hoverColor: root.hoverColor
        pressedColor: root.pressedColor

        onThemeToggleRequested: {
            root.darkMode = !root.darkMode
        }

        onExportRequested: {
            exportFileDialog.open()
        }
    }

    // Dialog for adding knowledge manually or importing files.
    KnowledgeDialog {
        id: knowledgeDialog

        parent: root.contentItem
        anchors.centerIn: parent

        surfaceColor: root.surfaceColor
        borderColor: root.borderColor
        textColor: root.textColor
        secondaryTextColor: root.secondaryTextColor
        accentColor: root.accentColor
        hoverColor: root.hoverColor
        pressedColor: root.pressedColor
        windowColor: root.windowColor

        onSaveRequested: function(text) {
            backend.add_manual_knowledge(text)
        }

        onTxtImportRequested: {
            textFileDialog.open()
        }

        onDocxImportRequested: {
            docxFileDialog.open()
        }

        onPdfImportRequested: {
            pdfFileDialog.open()
        }
    }

    // Dialog for viewing and managing saved knowledge.
    KnowledgeViewDialog {
        id: knowledgeViewDialog

        parent: root.contentItem
        anchors.centerIn: parent

        width: Math.min(800, root.width - 48)
        height: Math.min(600, root.height - 48)

        surfaceColor: root.surfaceColor
        borderColor: root.borderColor
        textColor: root.textColor
        secondaryTextColor: root.secondaryTextColor
        accentColor: root.accentColor
        hoverColor: root.hoverColor
        pressedColor: root.pressedColor
        windowColor: root.windowColor

        dangerColor: root.dangerColor
        dangerBorderColor: root.dangerBorderColor
        dangerHoverColor: root.dangerHoverColor
        dangerPressedColor: root.dangerPressedColor

        onRefreshRequested: function(
            searchText,
            sortOrder,
            txtFilterActive,
            docxFilterActive,
            pdfFilterActive,
            manualFilterActive
        ) {
            backend.load_filtered_knowledge(
                searchText,
                sortOrder,
                txtFilterActive,
                docxFilterActive,
                pdfFilterActive,
                manualFilterActive
            )
        }

        onEditRequested: function(id, text) {
            editKnowledgeDialog.loadKnowledge(id, text)
            editKnowledgeDialog.open()
        }

        onDeleteRequested: function(id, text) {
            deleteKnowledgeDialog.loadKnowledge(id, text)
            deleteKnowledgeDialog.open()
        }
    }

    // Dialog for editing a saved knowledge post.
    EditKnowledgeDialog {
        id: editKnowledgeDialog

        parent: root.contentItem
        anchors.centerIn: parent

        width: Math.min(500, root.width - 48)
        height: Math.min(380, root.height - 48)

        surfaceColor: root.surfaceColor
        borderColor: root.borderColor
        textColor: root.textColor
        secondaryTextColor: root.secondaryTextColor
        windowColor: root.windowColor
        hoverColor: root.hoverColor
        pressedColor: root.pressedColor

        onSaveRequested: function(id, text) {
            backend.edit_saved_knowledge(id, text)
        }
    }

    // Ask for confirmation before deleting a knowledge post.
    DeleteKnowledgeDialog {
        id: deleteKnowledgeDialog

        parent: root.contentItem
        anchors.centerIn: parent

        width: Math.min(500, root.width - 48)
        height: Math.min(320, root.height - 48)

        surfaceColor: root.surfaceColor
        borderColor: root.borderColor
        textColor: root.textColor
        secondaryTextColor: root.secondaryTextColor
        hoverColor: root.hoverColor
        pressedColor: root.pressedColor
        dangerColor: root.dangerColor

        onDeleteRequested: function(id) {
            backend.delete_saved_knowledge(id)
        }
    }    

    // File picker for importing a text file.
    FileDialog {
        id: textFileDialog
        title: "Välj en textfil"
        nameFilters: ["Textfiler (*.txt)"]

        // Send the selected file URL to Python.
        onAccepted: {
            knowledgeDialog.clearSaveStatus()
            backend.add_txt_knowledge(selectedFile.toString())
        }
    }

    // File picker for importing a docx file.
    FileDialog {
        id: docxFileDialog
        title: "Välj en DOCX-fil"
        nameFilters: ["Word-dokument (*.docx)"]

        // Send the selected file URL to Python.
        onAccepted: {
            knowledgeDialog.clearSaveStatus()
            backend.add_docx_knowledge(selectedFile)
        }
    }

    // File picker for importing a pdf file.
    FileDialog {
        id: pdfFileDialog
        title: "Välj en PDF-fil"
        nameFilters: ["PDF-dokument (*.pdf)"]

        // Send the selected file URL to python.
        onAccepted: {
            knowledgeDialog.clearSaveStatus()
            backend.add_pdf_knowledge(selectedFile)
        }
    }

    // Choose where to save the JSON backup.
    FileDialog {
        id: exportFileDialog
        title: "Spara säkerhetskopia"
        fileMode: FileDialog.SaveFile
        nameFilters: ["JSON-filer (*.json)"]
        defaultSuffix: "json"
        acceptLabel: "Spara"
        rejectLabel: "Avbryt"

        // Send the destination file URL to Python.
        onAccepted: {
            exportStatus.text = "Exporterar…"
            backend.export_knowledge(selectedFile.toString())
        }
    }

    // Listen for signals from the Python backend.
    Connections {
        target: backend

        // Add the answer to the chat.
        function onReplyReady(reply, sources) {
            
            chatModel.append({
                sender: "assistant",
                message: reply,
                sources: sources,
                sourceCount: sources.length
            })
        }

        // Show the result of saving or importing knowledge.
        function onKnowledgeSaveResult(message) {
            knowledgeDialog.setSaveStatus(message)
        }

        // Update the list with the received posts.
        function onKnowledgeLoaded(posts) {
            knowledgeViewDialog.setPosts(posts)
        }

        // Show the edit result and refresh the list if saving succeeded.
        function onKnowledgeEditResult(success, message) {
            editKnowledgeDialog.setStatus(message)

            if (success) {
                knowledgeViewDialog.requestRefresh()
            }
        }

        // Close the dialog and refresh the current search after deletion.
        function onKnowledgeDeleteResult(success, message) {
            if (success) {
                deleteKnowledgeDialog.close()
                knowledgeViewDialog.requestRefresh()
            } else {
                deleteKnowledgeDialog.setStatus(message)
            }
        }

        // Show or hide the thinking indicator.
        function onThinkingChanged(thinking) {
            root.isThinking = thinking
        }

        // Display an error message in the chat.
        function onReplyFailed(message) {
            chatModel.append({
                sender: "assistant",
                message: "Fel: " + message
            })
        }

        // Open knowledgeview for clicked entry
        function onKnowledgeEntryOpened(id, text, source, created_at) {
            editKnowledgeDialog.loadKnowledge(id, text)
            editKnowledgeDialog.open()
        }

        // Show whether the export succeeded or failed.
        function onExportResult(message) {
            settingsDialog.setExportStatus(message)
        }
    }
}