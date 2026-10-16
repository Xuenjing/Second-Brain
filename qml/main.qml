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


// Main application window.
ApplicationWindow {
    id: root

    // Track whether a question is being processed.
    property bool isThinking: false

    // Track whether sort buttons are active.
    property bool pdfFilterActive: true
    property bool docxFilterActive: true
    property bool txtFilterActive: true
    property bool manualFilterActive: true
    property string sortOrder: "desc"

    // Refresh filter state.
    function refreshKnowledge() {
        backend.load_filtered_knowledge(
            knowledgeSearchField.text,
            root.sortOrder,
            root.txtFilterActive,
            root.docxFilterActive,
            root.pdfFilterActive,
            root.manualFilterActive
        )
    }

    // Store questions and answers displayed in the chat.
    ListModel {
        id: chatModel
    }

    visible: true
    width: 1000
    height: 700
    title: "Second Brain"
    color: "#0B1220"

    Column {
        // Fill the window's content area with equal margins.
        anchors.fill: parent
        anchors.margins: 24
        anchors.bottomMargin: 36
        spacing: 16

        // Application name and logo
        Row {
            spacing: 16

            Image {
                width: 76
                height: 76
                source: "../assets/logo4.png"
                fillMode: Image.PreserveAspectFit
                smooth: true
                anchors.verticalCenter: parent.verticalCenter
            }

            Column {
                spacing: 0
                anchors.verticalCenter: parent.verticalCenter

                Label {
                    text: "Second"
                    font.pixelSize: 28
                    font.bold: true
                    color: "#F1F5F9"
                }

                Label {
                    text: "Brain"
                    font.pixelSize: 28
                    font.bold: true
                    color: "#38BDF8"
                }

                // Yellow accent matching the lightning bolt.
                Rectangle {
                    width: 64
                    height: 4
                    radius: 2
                    color: "#FACC15"
                }
            }
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
                    color: "#F1F5F9"
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                // Change background color when hovered or pressed.
                background: Rectangle {
                    radius: 8
                    color: addKnowledgeButton.down ? "#243B55"
                        : addKnowledgeButton.hovered ? "#1E3350"
                        : "#152238"
                    border.color: "#38BDF8"
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
                    color: "#F1F5F9"
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                // Change background color when hovered or pressed.
                background: Rectangle {
                    radius: 8
                    color: viewKnowledgeButton.down ? "#243B55"
                        : viewKnowledgeButton.hovered ? "#1E3350"
                        : "#152238"
                    border.color: "#38BDF8"
                    border.width: 1
                }

                // Open the dialog and load saved knowledge.
                onClicked: {
                    knowledgeViewDialog.open()
                    root.refreshKnowledge()
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

                contentItem: Text {
                    text: modelSelector.displayText
                    color: "#F1F5F9"
                    font.pixelSize: 14

                    leftPadding: 12
                    rightPadding: 32

                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                }

                background: Rectangle {
                    color: "#152238"
                    radius: 8
                    border.color: modelSelector.activeFocus ? "#38BDF8" : "#2B405C"
                    border.width: 1
                }

                // Dictates how every row in dropdown should act
                delegate: ItemDelegate {
                    width: ListView.view.width
                    height: 40
                    hoverEnabled: true

                    contentItem: Text {
                        text: modelData
                        color: "#F1F5F9"
                        font.pixelSize: 14
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: 12
                    }

                    // if/elif/else for marked and hover
                    background: Rectangle {
                        radius: 6
                        
                        color: parent.highlighted
                            ? "#1E3350"
                            : parent.hovered
                                ? "#1A2C45"
                                : "#152238"
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
                        color: "#152238"
                        radius: 8
                        border.color: "#2B405C"
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
                    color: "#F1F5F9"
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                // Change background color when hovered or pressed.
                background: Rectangle {
                    radius: 8
                    color: loadModelButton.down ? "#243B55"
                        : loadModelButton.hovered ? "#1E3350"
                        : "#152238"
                    border.color: "#38BDF8"
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
                        border.color: "#38BDF8"
                        border.width: 2

                        Rectangle {
                            width: 6
                            height: 6
                            radius: 3
                            color: "#F1F5F9"
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
                    color: "#94A3B8"
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
    color: "#152238"
    radius: 10
    border.color: "#2B405C"
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
            color: "#F1F5F9"
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

                width: ListView.view.width
                height: messageBubble.height

                Rectangle {
                    id: messageBubble

                    // Place questions on the right and answers on the left.
                    x: messageItem.sender === "user"
                        ? parent.width - width
                        : 0

                    width: Math.min(
                        messageText.implicitWidth + 28,
                        messageItem.width * 0.8
                    )
                    height: messageText.height + 24
                    radius: 10

                    color: messageItem.sender === "user"
                        ? "#1E40AF"
                        : "#243B55"

                    Text {
                        id: messageText
                        x: 14
                        y: 12
                        width: parent.width - 28
                        text: messageItem.message
                        textFormat: Text.PlainText
                        wrapMode: Text.Wrap
                        font.pixelSize: 14
                        color: "#F1F5F9"
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
                color: "#F1F5F9"
                placeholderTextColor: "#94A3B8"
                font.pixelSize: 14
                padding: 12
                height: 44

                // Highlight the border when the field has keyboard focus.
                background: Rectangle {
                    color: "#152238"
                    radius: 8
                    border.color: inputField.activeFocus ? "#38BDF8" : "#2B405C"
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
                            message: question
                        })

                        // Send the question to Python and clear the input field.
                        backend.receive_text(question)
                        inputField.clear()
                    }
                }
            }
        }
    }

    // Dialog for adding knowledge manually or importing a text file.
    Dialog {
        id: knowledgeDialog
        title: "Lägg till kunskap"

        // Block interaction with the main window while the dialog is open.
        modal: true
        width: 800
        height: 400

        // Center the dialog in the main window's content area.
        anchors.centerIn: parent
        parent: root.contentItem

        // Rounded background with a subtle border.
        background: Rectangle {
            color: "#152238"
            radius: 12
            border.color: "#2B405C"
            border.width: 1
        }

        // Display the dialog title.
        header: Label {
            text: knowledgeDialog.title
            color: "#F1F5F9"
            font.pixelSize: 18
            font.bold: true
            padding: 16
        }

        // Arrange the dialog content vertically.
        contentItem: Column {
            spacing: 12

            Label {
                text: "Skriv eller klistra in information:"
                color: "#F1F5F9"
            }

            // Allow scrolling through longer text.
            ScrollView {
                width: parent.width
                height: 200

                // Input field for new knowledge.
                TextArea {
                    id: knowledgeInput
                    placeholderText: "Information till kunskapsbasen"
                    wrapMode: TextArea.Wrap
                    textFormat: TextEdit.PlainText

                    // Text colors and space inside the field.
                    color: "#F1F5F9"
                    placeholderTextColor: "#94A3B8"
                    font.pixelSize: 14
                    padding: 12

                    // Highlight the border when the field has keyboard focus.
                    background: Rectangle {
                        color: "#0B1220"
                        radius: 8
                        border.color: knowledgeInput.activeFocus ? "#38BDF8" : "#2B405C"
                        border.width: 1
                    }
                }
            }

            // Place the dialog buttons next to each other.
            Row {
                spacing: 12

                Button {
                    id: saveKnowledgeButton
                    text: "Spara"
                    width: 90
                    height: 40
                    hoverEnabled: true

                    // Center the button text.
                    contentItem: Text {
                        text: saveKnowledgeButton.text
                        color: "#FFFFFF"
                        font.pixelSize: 14
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    // Change background color when hovered or pressed.
                    background: Rectangle {
                        radius: 8
                        color: saveKnowledgeButton.down ? "#1D4ED8"
                            : saveKnowledgeButton.hovered ? "#3B82F6"
                            : "#2563EB"
                    }

                    // Clear the previous status and send the text to Python.
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

                    // Center the button text.
                    contentItem: Text {
                        text: importFileButton.text
                        color: "#F1F5F9"
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    // Change background color when hovered or pressed.
                    background: Rectangle {
                        radius: 8
                        color: importFileButton.down ? "#243B55"
                            : importFileButton.hovered ? "#1E3350"
                            : "#152238"
                        border.color: "#2B405C"
                        border.width: 1
                    }

                    // Open the file picker to select a text file.
                    onClicked: textFileDialog.open() 
                }

                // Button for importing docx files.
                Button {
                    id: importDocxButton
                    text: "Importera .docx-fil"
                    width: 160
                    height: 40
                    hoverEnabled: true
                

                    // Center the button text.
                    contentItem: Text {
                        text: importDocxButton.text
                        color: "#F1F5F9"
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    // Change background color when hovered or pressed.
                    background: Rectangle {
                        radius: 8
                        color: importDocxButton.down ? "#243B55"
                            : importDocxButton.hovered ? "#1E3350"
                            : "#152238"
                        border.color: "#2B405C"
                        border.width: 1
                    }

                    onClicked: docxFileDialog.open()
                }

                // Button for importing PDF files.
                Button {
                    id: importPdfButton
                    text: "Importera .pdf-fil"
                    width: 160
                    height: 40
                    hoverEnabled: true

                    // Center the button text.
                    contentItem: Text {
                        text: importPdfButton.text
                        color: "#F1F5F9"
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    // Change background color when hovered or pressed.
                    background: Rectangle {
                        radius: 8
                        color: importPdfButton.down ? "#243B55"
                            : importPdfButton.hovered ? "#1E3350"
                            : "#152238"
                        border.color: "#2B405C"
                        border.width: 1
                    }

                    onClicked: pdfFileDialog.open()
                }

                Button {
                    id: closeKnowledgeButton
                    text: "Stäng"
                    width: 90
                    height: 40
                    hoverEnabled: true

                    // Center the button text.
                    contentItem: Text {
                        text: closeKnowledgeButton.text
                        color: "#F1F5F9"
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    // Change background color when hovered or pressed.
                    background: Rectangle {
                        radius: 8
                        color: closeKnowledgeButton.down ? "#243B55"
                            : closeKnowledgeButton.hovered ? "#1E3350"
                            : "#152238"
                        border.color: "#2B405C"
                        border.width: 1
                    }

                    // Close the dialog.
                    onClicked: knowledgeDialog.close()
                }
            }
            
            // Display feedback from Python about saving or importing knowledge.
            Label {
                id: knowledgeSaveStatus
                width: parent.width
                text: ""
                color: "#F1F5F9"
                wrapMode: Text.WordWrap
            }
        }
    }

    // Dialog for viewing and managing saved knowledge.
    Dialog {
        id: knowledgeViewDialog
        title: "Kunskapsbas"

        // Block interaction with the main window while the dialog is open.
        modal: true

        // Limit the dialog size to fit within the main window.
        width: Math.min(800, root.width - 48)
        height: Math.min(600, root.height - 48)

        // Center the dialog in the main window's content area.
        parent: root.contentItem
        anchors.centerIn: parent

        // Rounded background with a subtle border.
        background: Rectangle {
            color: "#152238"
            radius: 12
            border.color: "#2B405C"
            border.width: 1
        }

        // Display the dialog title.
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

                // Text colors and space inside the field.
                color: "#F1F5F9"
                placeholderTextColor: "#94A3B8"
                font.pixelSize: 14
                padding: 12

                // Highlight the border when the field has keyboard focus.
                background: Rectangle {
                    color: "#0B1220"
                    radius: 8
                    border.color: knowledgeSearchField.activeFocus
                        ? "#38BDF8" : "#2B405C"
                    border.width: 1
                }

                // Search saved knowledge as the user types.
                onTextEdited: root.refreshKnowledge()
            }

            // Row containing sort and filter buttons.
            Row {
                id: sortButtons
                anchors.top: knowledgeSearchField.bottom
                anchors.topMargin: 6
                anchors.right: parent.right
                spacing: 30

                Row {
                    id: filterButtons
                    spacing: 6
                

                    // Button for displaying sort by TXT.
                    Button {
                        id: filterTxtButton
                        text: "TXT"
                        width: 40
                        height: 40
                        hoverEnabled: true

                        // Center the button text.
                        contentItem: Text {
                            text: filterTxtButton.text
                            color: "#F1F5F9"
                            font.pixelSize: 14
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        // Change background color when hovered or toggled on/off.
                        background: Rectangle {
                            radius: 8
                            color: root.txtFilterActive ? "#1E3350" 
                                : filterTxtButton.down ? "#243B55"
                                : filterTxtButton.hovered ? "#1E3350"
                                : "#152238"
                            border.color: root.txtFilterActive ? "#38BDF8" : "#2B405C"
                            border.width: 1
                        }

                        // Toggle.
                        onClicked: {
                            root.txtFilterActive = !root.txtFilterActive
                            root.refreshKnowledge()
                        }

                        // Tooltip.
                        ToolTip.visible: hovered
                        ToolTip.text: "TXT-filer"
                    }

                    // Button for displaying filter by DOCX.
                    Button {
                        id: filterDocxButton
                        text: "DOCX"
                        width: 40
                        height: 40
                        hoverEnabled: true

                        // Center the button text.
                        contentItem: Text {
                            text: filterDocxButton.text
                            color: "#F1F5F9"
                            font.pixelSize: 14
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        // Change background color when hovered or toggled on/off.
                        background: Rectangle {
                            radius: 8
                            color: root.docxFilterActive ? "#1E3350" 
                                : filterDocxButton.down ? "#243B55"
                                : filterDocxButton.hovered ? "#1E3350"
                                : "#152238"
                            border.color: root.docxFilterActive ? "#38BDF8" : "#2B405C"
                            border.width: 1
                        }

                        // Toggle.
                        onClicked: {
                            root.docxFilterActive = !root.docxFilterActive
                            root.refreshKnowledge()
                        }

                        // Tooltip.
                        ToolTip.visible: hovered
                        ToolTip.text: "DOCX-filer"
                    }

                    // Button for displaying sort by PDF.
                    Button {
                        id: filterPdfButton
                        text: "PDF"
                        width: 40
                        height: 40
                        hoverEnabled: true

                        // Center the button text.
                        contentItem: Text {
                            text: filterPdfButton.text
                            color: "#F1F5F9"
                            font.pixelSize: 14
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        // Change background color when hovered or toggled on/off.
                        background: Rectangle {
                            radius: 8
                            color: root.pdfFilterActive ? "#1E3350" 
                                : filterPdfButton.down ? "#243B55"
                                : filterPdfButton.hovered ? "#1E3350"
                                : "#152238"
                            border.color: root.pdfFilterActive ? "#38BDF8" : "#2B405C"
                            border.width: 1
                        }

                        // Toggle.
                        onClicked: {
                            root.pdfFilterActive = !root.pdfFilterActive
                            root.refreshKnowledge()
                        }

                        // Tooltip.
                        ToolTip.visible: hovered
                        ToolTip.text: "PDF-filer"
                    }


                    // Button for filtering by manual posts.
                    Button {
                        id: filterManualButton
                        text: "M"
                        width: 40
                        height: 40
                        hoverEnabled: true

                        // Center the button text.
                        contentItem: Text {
                            text: filterManualButton.text
                            color: "#F1F5F9"
                            font.pixelSize: 14
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter       
                        }

                        // Change background color when hovered or toggled on/off.
                        background: Rectangle {
                            radius: 8
                            color: root.manualFilterActive ? "#1E3350" 
                                : filterManualButton.down ? "#243B55"
                                : filterManualButton.hovered ? "#1E3350"
                                : "#152238"
                            border.color: root.manualFilterActive ? "#38BDF8" : "#2B405C"
                            border.width: 1
                        }

                        // Toggle.
                        onClicked: {
                            root.manualFilterActive = !root.manualFilterActive
                            root.refreshKnowledge()
                        }

                        // Tooltip.
                        ToolTip.visible: hovered
                        ToolTip.text: "Manuella poster"
                    }
                }

                // Row for sort by date buttons.
                Row {
                    id: dateSortButtons
                    spacing: 6
                

                    Button {
                        id: sortAscendingButton
                        width: 40
                        height: 40
                        hoverEnabled: true

                        // Display an upward arrow.
                        contentItem: Text {
                            text: "↑"
                            // old color: sortAscendingButton.hovered ? "#F1F5F9" : "#94A3B8"
                            color: root.sortOrder === "asc" ? "#FFFFFF" : "#94A3B8" 
                            font.pixelSize: 20
                            font.bold: true
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        // Highlight the background when hovered or toggled.
                        background: Rectangle {
                            radius: 8
                            color: root.sortOrder === "asc" ? "#1E3350"
                                : sortAscendingButton.down ? "#243B55"
                                : sortAscendingButton.hovered ? "#1E3350"
                                : "#152238"
                            border.color: root.sortOrder === "asc"
                                ? "#38BDF8"
                                : "#2B405C"

                            border.width: 1
                        }

                        // Request all posts in ascending date order.
                        onClicked: {
                            root.sortOrder = "asc"
                            root.refreshKnowledge()
                        }

                        // Explain the sorting order when hovered.
                        ToolTip.visible: hovered
                        ToolTip.text: "Äldst först"
                    }

                    Button {
                        id: sortDescendingButton
                        width: 40
                        height: 40
                        hoverEnabled: true

                        // Display a downward arrow.
                        contentItem: Text {
                            text: "↓"
                            color: root.sortOrder === "desc" ? "#FFFFFF" : "#94A3B8"
                            font.pixelSize: 20
                            font.bold: true
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        // Highlight the background when hovered or toggled.
                        background: Rectangle {
                            radius: 8
                            color: root.sortOrder === "desc" ? "#1E3350"
                                : sortDescendingButton.down ? "#243B55"
                                : sortDescendingButton.hovered ? "#1E3350"
                                : "#152238"
                            border.color: root.sortOrder === "desc"
                                ? "#38BDF8"
                                : "#2B405C"
                            border.width: 1
                        }

                        // Request all posts in descending date order.
                        onClicked: {
                            root.sortOrder = "desc"
                            root.refreshKnowledge()
                        }

                        // Explain the sorting order when hovered.
                        ToolTip.visible: hovered
                        ToolTip.text: "Nyast först"
                    }
                }
            }

            // Display saved knowledge below the sorting buttons.
            ListView {
                id: knowledgeList
                anchors.top: sortButtons.bottom
                anchors.topMargin: 6
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                clip: true
                spacing: 12
                model: []

                ScrollBar.vertical: ScrollBar {}

                // Show each knowledge post.
                delegate: Rectangle {
                    id: postItem
                    required property var modelData

                    width: knowledgeList.width

                    // Fit both the text and action buttons, with vertical padding.
                    height: Math.max(postContent.height, postActions.height) + 24
                    color: "#0B1220"
                    radius: 8

                    // Leave space on the right for the action buttons.
                    Column {
                        id: postContent
                        x: 12
                        y: 12
                        width: parent.width - postActions.width - 36
                        spacing: 8

                        // Display the saved text.
                        Label {
                            width: parent.width
                            text: postItem.modelData.text
                            textFormat: Text.PlainText
                            wrapMode: Text.WordWrap
                            color: "#F1F5F9"
                        }

                        // Display the source and creation date.
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

                    // Place the action buttons next to each other on the right.
                    Row {
                        id: postActions
                        spacing: 8
                        anchors.right: parent.right
                        anchors.rightMargin: 12
                        anchors.verticalCenter: parent.verticalCenter

                        Button {
                            id: editPostButton
                            text: "Redigera"
                            width: 40
                            height: 40
                            hoverEnabled: true

                            // Description when howered.
                            Accessible.name: "Redigera kunskapspost"
                            ToolTip.visible: hovered
                            ToolTip.text: "Redigera kunskapspost"

                            // Draw a pencil icon.
                            contentItem: Item {
                                Item {
                                    anchors.centerIn: parent
                                    width: 24
                                    height: 24
                                    rotation: 45

                                    // Pencil body.
                                    Rectangle {
                                        x: 9
                                        y: 5
                                        width: 6
                                        height: 13
                                        radius: 1
                                        color: "#38BDF8"

                                        // Line along the pencil.
                                        Rectangle {
                                            anchors.horizontalCenter: parent.horizontalCenter
                                            y: 2
                                            width: 1
                                            height: 9
                                            color: "#152238"
                                        }
                                    }

                                    // Pencil cap.
                                    Rectangle {
                                        x: 9
                                        y: 1
                                        width: 6
                                        height: 3
                                        radius: 1
                                        color: "#38BDF8"
                                    }

                                    // Pencil tip.
                                    Rectangle {
                                        x: 10
                                        y: 17
                                        width: 4
                                        height: 4
                                        rotation: 45
                                        color: "#38BDF8"
                                    }
                                }
                            }

                            // Change background color when hovered or pressed.
                            background: Rectangle {
                                radius: 8
                                color: editPostButton.down ? "#243B55"
                                    : editPostButton.hovered ? "#1E3350"
                                    : "#152238"
                                border.color: "#38BDF8"
                                border.width: 1
                            }

                            // Fill the edit dialog with the selected post.
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
                            width: 40
                            height: 40
                            hoverEnabled: true

                            // Description when hovered.
                            Accessible.name: "Ta bort kunskapspost"
                            ToolTip.visible: hovered
                            ToolTip.text: "Ta bort kunskapspost"

                            // Draw a trash can icon.
                            contentItem: Item {
                                Item {
                                    anchors.centerIn: parent
                                    width: 20
                                    height: 24

                                    // Handle.
                                    Rectangle {
                                        x: 7
                                        y: 1
                                        width: 6
                                        height: 5
                                        radius: 1
                                        color: "transparent"
                                        border.color: "#FCA5A5"
                                        border.width: 2
                                    }

                                    // Lid.
                                    Rectangle {
                                        x: 2
                                        y: 5
                                        width: 16
                                        height: 2
                                        radius: 1
                                        color: "#FCA5A5"
                                    }

                                    // Bin.
                                    Rectangle {
                                        x: 4
                                        y: 9
                                        width: 12
                                        height: 14
                                        radius: 2
                                        color: "#FCA5A5"

                                        // Vertical lines inside the bin.
                                        Repeater {
                                            model: 3

                                            Rectangle {
                                                required property int index
                                                x: 3 + index * 3
                                                y: 3
                                                width: 1
                                                height: 8
                                                radius: 0.5
                                                color: "#152238"
                                            }
                                        }
                                    }
                                }
                            }

                            // Use red colors for the delete button.
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

                // Show a message when there are no posts to display.
                Label {
                    anchors.centerIn: parent
                    visible: knowledgeList.count === 0
                    text: "Inga kunskapsposter att visa."
                    color: "#94A3B8"
                }
            }
        }

        // Button that closes the dialog.
        footer: Item {
            implicitHeight: 64

            Button {
                id: closeKnowledgeViewButton
                text: "Stäng"
                width: 90
                height: 40

                // Place the button on the right and center it vertically.
                anchors.right: parent.right
                anchors.rightMargin: 12
                anchors.verticalCenter: parent.verticalCenter
                hoverEnabled: true

                // Center the button text.
                contentItem: Text {
                    text: closeKnowledgeViewButton.text
                    color: "#F1F5F9"
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                // Change background color when hovered or pressed.
                background: Rectangle {
                    radius: 8
                    color: closeKnowledgeViewButton.down ? "#243B55"
                        : closeKnowledgeViewButton.hovered ? "#1E3350"
                        : "#152238"
                    border.color: "#2B405C"
                    border.width: 1
                }

                // Close the knowledge dialog.
                onClicked: knowledgeViewDialog.close()
            }
        }
    }

    // Dialog for editing a saved knowledge post.
    Dialog {
        id: editKnowledgeDialog
        title: "Redigera kunskap"

        // Store the selected post's ID. -1 means no post is selected.
        property int knowledgeId: -1

        // Block interaction with the main window while the dialog is open.
        modal: true

        // Limit the dialog size to fit within the main window.
        width: Math.min(500, root.width - 48)
        height: Math.min(380, root.height - 48)

        // Center the dialog in the main window's content area.
        parent: root.contentItem
        anchors.centerIn: parent

        // Rounded background with a subtle border.
        background: Rectangle {
            color: "#152238"
            radius: 12
            border.color: "#2B405C"
        }

        // Display the dialog title.
        header: Label {
            text: editKnowledgeDialog.title
            color: "#F1F5F9"
            font.pixelSize: 18
            font.bold: true
            padding: 16
        }

        contentItem: Item {
            // Leave room below the text field for status messages.
            ScrollView {
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: editKnowledgeStatus.top
                anchors.bottomMargin: 12

                // Fit the text to the available width.
                contentWidth: availableWidth
                clip: true

                // Show the selected post's text and allow editing.
                TextArea {
                    id: editKnowledgeInput
                    placeholderText: "Ändra kunskapspostens text"
                    wrapMode: TextArea.Wrap
                    textFormat: TextEdit.PlainText

                    // Text colors and space inside the field.
                    color: "#F1F5F9"
                    placeholderTextColor: "#94A3B8"
                    padding: 12

                    // Dark background with rounded corners.
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

        // Bottom area with save and cancel buttons.
        footer: Item {
            implicitHeight: 64

            // Place the buttons next to each other on the right.
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

                    // Center the button text.
                    contentItem: Text {
                        text: saveEditButton.text
                        color: "#FFFFFF"
                        font.pixelSize: 14
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    // Change background color when hovered or pressed.
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

                    // Center the button text.
                    contentItem: Text {
                        text: cancelEditButton.text
                        color: "#F1F5F9"
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    // Change background color when hovered or pressed.
                    background: Rectangle {
                        radius: 8
                        color: cancelEditButton.down ? "#243B55"
                            : cancelEditButton.hovered ? "#1E3350"
                            : "#152238"
                        border.color: "#2B405C"
                        border.width: 1
                    }

                    // Close the dialog without saving pending changes.
                    onClicked: editKnowledgeDialog.close()
                }
            }
        }
    }

    // Ask for confirmation before deleting a knowledge post.
    Dialog {
        id: deleteKnowledgeDialog
        title: "Ta bort kunskap"

        // Store the selected post's ID and text.
        property int knowledgeId: -1
        property string postText: ""

        // Block interaction with the main window while the dialog is open.
        modal: true

        // Limit the dialog size to fit within the main window.
        width: Math.min(500, root.width - 48)
        height: Math.min(320, root.height - 48)

        // Center the dialog in the main window's content area.
        parent: root.contentItem
        anchors.centerIn: parent

        // Rounded background with a subtle border.
        background: Rectangle {
            color: "#152238"
            radius: 12
            border.color: "#2B405C"
        }

        // Display the dialog title.
        header: Label {
            text: deleteKnowledgeDialog.title
            color: "#F1F5F9"
            font.pixelSize: 18
            font.bold: true
            padding: 16
        }

        // Place the question, post text and status message below each other.
        contentItem: Column {
            spacing: 12

            // Ask the user to confirm deletion.
            Label {
                width: parent.width
                text: "Vill du ta bort den här kunskapsposten?"
                color: "#F1F5F9"
                wrapMode: Text.WordWrap
            }

            // Show a preview of the selected post.
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

        // Bottom area with delete and cancel buttons.
        footer: Item {
            implicitHeight: 64

            // Place the buttons next to each other on the right.
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

                    // Center the button text.
                    contentItem: Text {
                        text: confirmDeleteButton.text
                        color: "#FFFFFF"
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    // Change the red background when hovered or pressed.
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

                    // Center the button text.
                    contentItem: Text {
                        text: cancelDeleteButton.text
                        color: "#F1F5F9"
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    // Change background color when hovered or pressed.
                    background: Rectangle {
                        radius: 8
                        color: cancelDeleteButton.down ? "#243B55"
                            : cancelDeleteButton.hovered ? "#1E3350"
                            : "#152238"
                        border.color: "#2B405C"
                    }

                    // Close the dialog without deleting the post.
                    onClicked: deleteKnowledgeDialog.close()
                }
            }
        }
    }

    // File picker for importing a text file.
    FileDialog {
        id: textFileDialog
        title: "Välj en textfil"
        nameFilters: ["Textfiler (*.txt)"]

        // Send the selected file URL to Python.
        onAccepted: {
            knowledgeSaveStatus.text = ""
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
            knowledgeSaveStatus.text = ""
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
            knowledgeSaveStatus.text = ""
            backend.add_pdf_knowledge(selectedFile)
        }
    }

    // Listen for signals from the Python backend.
    Connections {
        target: backend

        // Add the answer to the chat.
        function onReplyReady(reply) {
            chatModel.append({
                sender: "assistant",
                message: reply
            })
        }

        // Show the result of saving or importing knowledge.
        function onKnowledgeSaveResult(message) {
            knowledgeSaveStatus.text = message
        }

        // Update the list with the received posts.
        function onKnowledgeLoaded(posts) {
            knowledgeList.model = posts
        }

        // Show the edit result and refresh the list if saving succeeded.
        function onKnowledgeEditResult(success, message) {
            editKnowledgeStatus.text = message

            if (success) {
                root.refreshKnowledge()
            }
        }

        // Close the dialog and refresh the current search after deletion.
        function onKnowledgeDeleteResult(success, message) {
            if (success) {
                deleteKnowledgeDialog.close()
                root.refreshKnowledge()
            } else {
                deleteKnowledgeStatus.text = message
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
    }
}