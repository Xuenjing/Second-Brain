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
    color: root.windowColor

    Column {
        // Fill the window's content area with equal margins.
        anchors.fill: parent
        anchors.margins: 24
        anchors.bottomMargin: 36
        spacing: 16

        // Application name, logo and settings button.
        Item {
        width: parent.width
        height: 76

        // Application name and logo.
        Row {
            spacing: 16
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter

            Image {
                width: 76
                height: 76
                source: "../assets/logo4.png"
                fillMode: Image.PreserveAspectFit
                smooth: true
            }

            Column {
                spacing: 0
                anchors.verticalCenter: parent.verticalCenter

                Label {
                    text: "Second"
                    font.pixelSize: 28
                    font.bold: true
                    color: root.textColor
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

        // Open the settings dialog.
        Button {
            id: settingsButton
            width: 44
            height: 44
            anchors.right: parent.right
            anchors.top: parent.top
            hoverEnabled: true

            Accessible.name: "Inställningar"
            ToolTip.visible: hovered
            ToolTip.text: "Inställningar"

            // Draw an outlined gear icon.
            contentItem: Item {
                Canvas {
                    anchors.centerIn: parent
                    width: 24
                    height: 24

                    property color iconColor: root.accentColor

                    // Redraw when the theme changes.
                    onIconColorChanged: requestPaint()

                    onPaint: {
                        const ctx = getContext("2d")
                        ctx.clearRect(0, 0, width, height)

                        ctx.strokeStyle = iconColor
                        ctx.lineWidth = 2
                        ctx.lineJoin = "round"
                        ctx.beginPath()

                        // Draw eight teeth around the center.
                        for (let tooth = 0; tooth < 8; tooth++) {
                            const angles = [-22.5, -12, 12, 22.5]
                            const radii = [8.5, 11, 11, 8.5]

                            for (let point = 0; point < 4; point++) {
                                const angle =
                                    (tooth * 45 + angles[point]) * Math.PI / 180

                                const px = 12 + Math.cos(angle) * radii[point]
                                const py = 12 + Math.sin(angle) * radii[point]

                                if (tooth === 0 && point === 0) {
                                    ctx.moveTo(px, py)
                                } else {
                                    ctx.lineTo(px, py)
                                }
                            }
                        }

                        ctx.closePath()
                        ctx.stroke()

                        // Draw the center ring.
                        ctx.beginPath()
                        ctx.arc(12, 12, 4, 0, 2 * Math.PI)
                        ctx.stroke()
                    }
                }
            }

            background: Rectangle {
                radius: 8
                color: settingsButton.down ? root.pressedColor
                    : settingsButton.hovered ? root.hoverColor
                    : root.surfaceColor
                border.color: root.accentColor
                border.width: 1
            }

            onClicked: settingsDialog.open()
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
                    color: addKnowledgeButton.down ? root.pressedColor
                        : addKnowledgeButton.hovered ? root.hoverColor
                        : root.surfaceColor
                    border.color: root.accentColor
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
    Dialog {
        id: settingsDialog
        title: "Inställningar"
        modal: true
        parent: root.contentItem
        anchors.centerIn: parent

        width: Math.min(500, root.width - 48)
        height: Math.min(400, root.height - 48)

        background: Rectangle {
            color: root.surfaceColor
            radius: 12
            border.color: root.borderColor
            border.width: 1
        }

        header: Label {
            text: settingsDialog.title
            color: root.textColor
            font.pixelSize: 18
            font.bold: true
            padding: 16
        }

        // Arrange the settings vertically.
        contentItem: Column {
            spacing: 12

            Label {
                text: "Utseende"
                color: root.textColor
                font.pixelSize: 16
                font.bold: true
            }

            // Place the theme labels on each side of the toggle.
            Row {
                spacing: 12

                Label {
                    text: "Ljust"
                    anchors.verticalCenter: parent.verticalCenter
                    color: root.darkMode
                        ? root.secondaryTextColor
                        : root.textColor
                    font.pixelSize: 14
                    font.bold: !root.darkMode
                }

                // Toggle between light and dark mode.
                Button {
                    id: themeToggle
                    width: 100
                    height: 36
                    padding: 0
                    hoverEnabled: true

                    Accessible.name: "Byt mellan ljust och mörkt läge"
                    ToolTip.visible: hovered
                    ToolTip.text: root.darkMode
                        ? "Byt till ljust läge"
                        : "Byt till mörkt läge"

                    onClicked: root.darkMode = !root.darkMode

                    background: Rectangle {
                        radius: height / 2
                        color: root.darkMode ? "#0B1220" : "#E2E8F0"
                        border.color: themeToggle.activeFocus
                            ? root.accentColor
                            : root.borderColor
                        border.width: 1

                        // Highlight the current mode.
                        Rectangle {
                            width: 44
                            height: 28
                            y: 4
                            x: root.darkMode ? 52 : 4
                            radius: height / 2
                            color: root.darkMode ? "#334155" : "#FFFFFF"

                            Behavior on x {
                                NumberAnimation {
                                    duration: 180
                                    easing.type: Easing.InOutQuad
                                }
                            }
                        }
                    }

                    contentItem: Item {
                        // Sun symbol.
                        Text {
                            width: parent.width / 2
                            height: parent.height
                            text: "\u263C"
                            font.pixelSize: 24
                            color: root.darkMode ? "#94A3B8" : "#0F172A"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        // Moon symbol.
                        Text {
                            x: parent.width / 2
                            width: parent.width / 2
                            height: parent.height
                            text: "\u263D"
                            font.pixelSize: 24
                            color: root.darkMode ? "#F1F5F9" : "#64748B"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                    }
                }

                Label {
                    text: "Mörkt"
                    anchors.verticalCenter: parent.verticalCenter
                    color: root.darkMode
                        ? root.textColor
                        : root.secondaryTextColor
                    font.pixelSize: 14
                    font.bold: root.darkMode
                }
            }
        }

        // Footer with close button.
        footer: Item {
            implicitHeight: 64

            Button {
                id: closeSettingsButton
                text: "Stäng"
                width: 100
                height: 40
                hoverEnabled: true

                anchors.right: parent.right
                anchors.rightMargin: 16
                anchors.verticalCenter: parent.verticalCenter

                // Center the button text.
                contentItem: Text {
                    text: closeSettingsButton.text
                    color: root.textColor
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                // Change background color when hovered or pressed.
                background: Rectangle {
                    radius: 8
                    color: closeSettingsButton.down ? root.pressedColor
                        : closeSettingsButton.hovered ? root.hoverColor
                        : root.surfaceColor
                    border.color: root.accentColor
                    border.width: 1
                }

                // Close the settings dialog.
                onClicked: settingsDialog.close()
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
            color: root.surfaceColor
            radius: 12
            border.color: root.borderColor
            border.width: 1
        }

        // Display the dialog title.
        header: Label {
            text: knowledgeDialog.title
            color: root.textColor
            font.pixelSize: 18
            font.bold: true
            padding: 16
        }

        // Arrange the dialog content vertically.
        contentItem: Column {
            spacing: 12

            Label {
                text: "Skriv eller klistra in information:"
                color: root.textColor
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
                    color: root.textColor
                    placeholderTextColor: root.secondaryTextColor
                    font.pixelSize: 14
                    padding: 12

                    // Highlight the border when the field has keyboard focus.
                    background: Rectangle {
                        color: root.windowColor
                        radius: 8
                        border.color: knowledgeInput.activeFocus
                            ? root.accentColor
                            : root.borderColor
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
                    width: 40
                    height: 40
                    hoverEnabled: true

                    // Description when howered.
                    Accessible.name: "Spara kunskap"
                    ToolTip.visible: hovered
                    ToolTip.text: "Spara kunskap"

                    // Draw a save icon.
                    contentItem: Item {
                        Rectangle {
                            anchors.centerIn: parent
                            width: 22
                            height: 22
                            radius: 3
                            color: root.accentColor

                            // Upper inset.
                            Rectangle {
                                x: 5
                                y: 0
                                width: 12
                                height: 8
                                color: root.surfaceColor

                                Rectangle {
                                    x: 8
                                    y: 1
                                    width: 2
                                    height: 5
                                    color: root.accentColor
                                }
                            }

                            // Label area.
                            Rectangle {
                                x: 4
                                y: 12
                                width: 14
                                height: 8
                                radius: 1
                                color: root.surfaceColor
                            }
                        }
                    }

                    // Change background color when hovered or pressed.
                    background: Rectangle {
                        radius: 8
                        color: saveKnowledgeButton.down ? root.pressedColor
                            : saveKnowledgeButton.hovered ? root.hoverColor
                            : root.surfaceColor
                        border.color: root.accentColor
                        border.width: 1
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
                        color: root.textColor
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    // Change background color when hovered or pressed.
                    background: Rectangle {
                        radius: 8
                        color: importFileButton.down ? root.pressedColor
                            : importFileButton.hovered ? root.hoverColor
                            : root.surfaceColor
                        border.color: root.borderColor
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
                        color: root.textColor
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    // Change background color when hovered or pressed.
                    background: Rectangle {
                        radius: 8
                        color: importDocxButton.down ? root.pressedColor
                            : importDocxButton.hovered ? root.hoverColor
                            : root.surfaceColor
                        border.color: root.borderColor
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
                        color: root.textColor
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    // Change background color when hovered or pressed.
                    background: Rectangle {
                        radius: 8
                        color: importPdfButton.down ? root.pressedColor
                            : importPdfButton.hovered ? root.hoverColor
                            : root.surfaceColor
                        border.color: root.borderColor
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
                        color: root.textColor
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    // Change background color when hovered or pressed.
                    background: Rectangle {
                        radius: 8
                        color: closeKnowledgeButton.down ? root.pressedColor
                            : closeKnowledgeButton.hovered ? root.hoverColor
                            : root.surfaceColor
                        border.color: root.borderColor
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
                color: root.textColor
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
            color: root.surfaceColor
            radius: 12
            border.color: root.borderColor
            border.width: 1
        }

        // Display the dialog title.
        header: Label {
            text: knowledgeViewDialog.title
            color: root.textColor
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
                color: root.textColor
                placeholderTextColor: root.secondaryTextColor
                font.pixelSize: 14
                padding: 12

                // Highlight the border when the field has keyboard focus.
                background: Rectangle {
                    color: root.windowColor
                    radius: 8
                    border.color: knowledgeSearchField.activeFocus
                        ? root.accentColor
                        : root.borderColor
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
                            color: root.textColor
                            font.pixelSize: 14
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        // Change background color when hovered or toggled on/off.
                        background: Rectangle {
                            radius: 8
                            color: filterTxtButton.down ? root.pressedColor
                                : root.txtFilterActive || filterTxtButton.hovered
                                    ? root.hoverColor
                                    : root.surfaceColor
                            border.color: root.txtFilterActive
                                ? root.accentColor
                                : root.borderColor
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
                            color: root.textColor
                            font.pixelSize: 14
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        // Change background color when hovered or toggled on/off.
                        background: Rectangle {
                            radius: 8
                            color: filterDocxButton.down ? root.pressedColor
                                : root.docxFilterActive || filterDocxButton.hovered
                                    ? root.hoverColor
                                    : root.surfaceColor
                            border.color: root.docxFilterActive
                                ? root.accentColor
                                : root.borderColor
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
                            color: root.textColor
                            font.pixelSize: 14
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        // Change background color when hovered or toggled on/off.
                        background: Rectangle {
                            radius: 8
                            color: filterPdfButton.down ? root.pressedColor
                                : root.pdfFilterActive || filterPdfButton.hovered
                                    ? root.hoverColor
                                    : root.surfaceColor
                            border.color: root.pdfFilterActive
                                ? root.accentColor
                                : root.borderColor
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
                            color: root.textColor
                            font.pixelSize: 14
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter       
                        }

                        // Change background color when hovered or toggled on/off.
                        background: Rectangle {
                            radius: 8
                            color: filterManualButton.down ? root.pressedColor
                                : root.manualFilterActive || filterManualButton.hovered
                                    ? root.hoverColor
                                    : root.surfaceColor
                            border.color: root.manualFilterActive
                                ? root.accentColor
                                : root.borderColor
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
                            color: root.sortOrder === "asc"
                                ? root.accentColor
                                : root.secondaryTextColor 
                            font.pixelSize: 20
                            font.bold: true
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        // Highlight the background when hovered or toggled.
                        background: Rectangle {
                            radius: 8
                            color: sortAscendingButton.down ? root.pressedColor
                                : root.sortOrder === "asc" || sortAscendingButton.hovered
                                    ? root.hoverColor
                                    : root.surfaceColor
                            border.color: root.sortOrder === "asc"
                                ? root.accentColor
                                : root.borderColor
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
                            color: root.sortOrder === "desc"
                                ? root.accentColor
                                : root.secondaryTextColor
                            font.pixelSize: 20
                            font.bold: true
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        // Highlight the background when hovered or toggled.
                        background: Rectangle {
                            radius: 8
                            color: sortDescendingButton.down ? root.pressedColor
                                : root.sortOrder === "desc" || sortDescendingButton.hovered
                                    ? root.hoverColor
                                    : root.surfaceColor
                            border.color: root.sortOrder === "desc"
                                ? root.accentColor
                                : root.borderColor
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
                    color: root.windowColor
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
                            color: root.textColor
                        }

                        // Display the source and creation date.
                        Label {
                            width: parent.width
                            text: "Källa: " + postItem.modelData.source
                                + " | Skapad: " + postItem.modelData.created_at
                            textFormat: Text.PlainText
                            wrapMode: Text.WordWrap
                            color: root.secondaryTextColor
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
                                        color: root.accentColor

                                        // Line along the pencil.
                                        Rectangle {
                                            anchors.horizontalCenter: parent.horizontalCenter
                                            y: 2
                                            width: 1
                                            height: 9
                                            color: root.surfaceColor
                                        }
                                    }

                                    // Pencil cap.
                                    Rectangle {
                                        x: 9
                                        y: 1
                                        width: 6
                                        height: 3
                                        radius: 1
                                        color: root.accentColor
                                    }

                                    // Pencil tip.
                                    Rectangle {
                                        x: 10
                                        y: 17
                                        width: 4
                                        height: 4
                                        rotation: 45
                                        color: root.accentColor
                                    }
                                }
                            }

                            // Change background color when hovered or pressed.
                            background: Rectangle {
                                radius: 8
                                color: editPostButton.down ? root.pressedColor
                                    : editPostButton.hovered ? root.hoverColor
                                    : root.surfaceColor
                                border.color: root.accentColor
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
                                        border.color: root.dangerColor
                                        border.width: 2
                                    }

                                    // Lid.
                                    Rectangle {
                                        x: 2
                                        y: 5
                                        width: 16
                                        height: 2
                                        radius: 1
                                        color: root.dangerColor
                                    }

                                    // Bin.
                                    Rectangle {
                                        x: 4
                                        y: 9
                                        width: 12
                                        height: 14
                                        radius: 2
                                        color: root.dangerColor

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
                                                color: root.surfaceColor
                                            }
                                        }
                                    }
                                }
                            }

                            // Use red colors for the delete button.
                            background: Rectangle {
                                radius: 8
                                color: deletePostButton.down ? root.dangerPressedColor
                                    : deletePostButton.hovered ? root.dangerHoverColor
                                    : root.surfaceColor
                                border.color: root.dangerBorderColor
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
                    color: root.secondaryTextColor
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
                    color: root.textColor
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                // Change background color when hovered or pressed.
                background: Rectangle {
                    radius: 8
                    color: closeKnowledgeViewButton.down ? root.pressedColor
                        : closeKnowledgeViewButton.hovered ? root.hoverColor
                        : root.surfaceColor
                    border.color: root.borderColor
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
            color: root.surfaceColor
            radius: 12
            border.color: root.borderColor
            border.width: 1
        }

        // Display the dialog title.
        header: Label {
            text: editKnowledgeDialog.title
            color: root.textColor
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
                    color: root.textColor
                    placeholderTextColor: root.secondaryTextColor
                    padding: 12

                    // Use the current theme colors.
                    background: Rectangle {
                        color: root.windowColor
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
                color: root.textColor
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
                        color: root.textColor
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    // Change background color when hovered or pressed.
                    background: Rectangle {
                        radius: 8
                        color: cancelEditButton.down ? root.pressedColor
                            : cancelEditButton.hovered ? root.hoverColor
                            : root.surfaceColor
                        border.color: root.borderColor
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
            color: root.surfaceColor
            radius: 12
            border.color: root.borderColor
            border.width: 1
        }

        // Display the dialog title.
        header: Label {
            text: deleteKnowledgeDialog.title
            color: root.textColor
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
                color: root.textColor
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
                color: root.dangerColor
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
                        color: root.textColor
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    // Change background color when hovered or pressed.
                    background: Rectangle {
                        radius: 8
                        color: cancelDeleteButton.down ? root.pressedColor
                            : cancelDeleteButton.hovered ? root.hoverColor
                            : root.surfaceColor
                        border.color: root.borderColor
                        border.width: 1
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

        // Open knowledgeview for clicked entry
        function onKnowledgeEntryOpened(id, text, source, created_at) {
            editKnowledgeDialog.knowledgeId = id
            editKnowledgeInput.text = text
            editKnowledgeStatus.text = ""
            editKnowledgeDialog.open()
        }
    }
}