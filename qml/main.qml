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
import QtQuick.Layouts

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

    // Track email analysis and retain suggestions for review.
    property bool isMailAnalyzing: false
    property bool mailReviewPending: false
    property string mailReviewText: ""
    property var mailReviewFacts: []
    property string mailReviewSource: ""

    // Track state of model loading.
    property bool modelLoading: false
    property string modelLoadStatus: ""

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
        MainToolbar {
            width: parent.width

            textColor: root.textColor
            accentColor: root.accentColor
            surfaceColor: root.surfaceColor
            borderColor: root.borderColor
            hoverColor: root.hoverColor
            pressedColor: root.pressedColor

            modelLoading: root.modelLoading

            onAddKnowledgeRequested: {
                knowledgeDialog.open()
            }

            onViewKnowledgeRequested: {
                knowledgeViewDialog.open()
                knowledgeViewDialog.requestRefresh()
            }

            onModelLoadConfirmationRequested: function(modelIndex, modelName) {
                modelLoadDialog.modelIndex = modelIndex
                modelLoadDialog.modelName = modelName
                modelLoadDialog.open()
            }

            
            // onLoadModelRequested: function(modelIndex) {
            //     backend.load_model(modelIndex)
            // }
        }

        // Show email-analysis status and reopen pending suggestions.
        Button {
            id: openMailReviewButton

            visible: root.isMailAnalyzing || root.mailReviewPending
            enabled: !root.isMailAnalyzing
            height: 40
            hoverEnabled: true

            text: root.isMailAnalyzing
                ? "Analyserar mejl…"
                : "Mejlanalysen är klar – Granska förslag"

            contentItem: Text {
                text: openMailReviewButton.text
                color: root.textColor
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            background: Rectangle {
                radius: 8
                color: openMailReviewButton.down
                    ? root.pressedColor
                    : openMailReviewButton.hovered
                        ? root.hoverColor
                        : root.surfaceColor
                border.color: root.accentColor
            }

            onClicked: mailReviewDialog.open()
        }

        // Conversation title.
        // Keep the chat heading and thinking indicator on the same line.
        ThinkingIndicator {
            width: parent.width
            height: 32

            isThinking: root.isThinking

            textColor: root.textColor
            accentColor: root.accentColor
            windowColor: root.windowColor
        }

        // Show a welcome message or the conversation.
        ChatView {
            id: chatPanel

            width: parent.width

            height: Math.max(
                0,
                parent.height - y - questionRow.height - parent.spacing
            )

            chatModel: chatModel

            surfaceColor: root.surfaceColor
            borderColor: root.borderColor
            textColor: root.textColor
            secondaryTextColor: root.secondaryTextColor
            userBubbleColor: root.userBubbleColor
            assistantBubbleColor: root.assistantBubbleColor
            accentColor: root.accentColor
            hoverColor: root.hoverColor
            pressedColor: root.pressedColor

            onSourcesRequested: function(sources) {
                sourceDialog.sources = sources
                sourceDialog.open()
            }
        }

        // Place the question field and send button next to each other.
        ChatInput {
            id: questionRow

            width: parent.width

            isThinking: root.isThinking

            textColor: root.textColor
            secondaryTextColor: root.secondaryTextColor
            surfaceColor: root.surfaceColor
            borderColor: root.borderColor
            accentColor: root.accentColor
            hoverColor: root.hoverColor
            pressedColor: root.pressedColor

            onQuestionSubmitted: function(question) {
                chatModel.append({
                    sender: "user",
                    message: question,
                    sources: [],
                    sourceCount: 0
                })

                backend.receive_text(question)
            }

            onCancelRequested: {
                // backend.cancel_question()
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

        onImportRequested: {
            importBackupFileDialog.open()
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
        assistantBubbleColor: root.assistantBubbleColor

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

        onMailImportRequested: {
            mailFileDialog.open()
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
        assistantBubbleColor: root.assistantBubbleColor

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
            manualFilterActive,
            mailFilterActive
        ) {
            backend.load_filtered_knowledge(
                searchText,
                sortOrder,
                txtFilterActive,
                docxFilterActive,
                pdfFilterActive,
                manualFilterActive,
                mailFilterActive
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
        assistantBubbleColor: root.assistantBubbleColor
        accentColor: root.accentColor

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
        assistantBubbleColor: root.assistantBubbleColor
        dangerBorderColor: root.dangerBorderColor
        dangerHoverColor: root.dangerHoverColor
        dangerPressedColor: root.dangerPressedColor

        onDeleteRequested: function(id) {
            backend.delete_saved_knowledge(id)
        }
    }

    SourceDialog {
        id: sourceDialog

        parent: root.contentItem

        width: 700
        height: 600

        x: (parent.width - width) / 2
        y: (parent.height - height) / 2

        surfaceColor: root.surfaceColor
        textColor: root.textColor
        secondaryTextColor: root.secondaryTextColor
        assistantBubbleColor: root.assistantBubbleColor
        hoverColor: root.hoverColor
        pressedColor: root.pressedColor

        onKnowledgeEntryRequested: function(id) {
            backend.open_knowledge_entry(id)
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

    // Review suggested facts alongside the original email.
    Dialog {
        id: mailReviewDialog

        parent: root.contentItem
        anchors.centerIn: parent

        width: Math.min(900, root.width - 48)
        height: Math.min(600, root.height - 48)
        modal: true
        property string statusMessage: ""

        // Keep edits when the dialog is closed and reopened.
        ListModel {
            id: mailFactsModel
        }

        function loadSuggestions(facts) {
            mailFactsModel.clear()

            for (let i = 0; i < facts.length; i++) {
                mailFactsModel.append({
                    factText: facts[i],
                    keepFact: true
                })
            }
        }

        background: Rectangle {
            color: root.surfaceColor
            radius: 12
            border.color: root.borderColor
        }

        header: Item {
            implicitHeight: 56

            Label {
                anchors.left: parent.left
                anchors.leftMargin: 16
                anchors.right: closeMailReviewButton.left
                anchors.rightMargin: 12
                anchors.verticalCenter: parent.verticalCenter

                text: "Granska fakta: " + root.mailReviewSource
                color: root.textColor
                font.pixelSize: 18
                font.bold: true
                elide: Text.ElideRight
            }

            Button {
                id: closeMailReviewButton

                width: 28
                height: 28
                padding: 0
                hoverEnabled: true

                anchors.right: parent.right
                anchors.rightMargin: 12
                anchors.verticalCenter: parent.verticalCenter

                Accessible.name: "Stäng granskningen"
                ToolTip.visible: hovered
                ToolTip.text: "Stäng och behåll förslagen"

                contentItem: Text {
                    text: "×"
                    color: root.secondaryTextColor
                    font.pixelSize: 24
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    radius: 6
                    color: closeMailReviewButton.down
                        ? root.pressedColor
                        : closeMailReviewButton.hovered
                            ? root.hoverColor
                            : "transparent"
                }

                onClicked: mailReviewDialog.close()
            }
        }

        footer: Column {
            spacing: 8
            padding: 12

            Label {
                width: parent.width - 24
                text: mailReviewDialog.statusMessage
                visible: text.length > 0
                color: root.textColor
                wrapMode: Text.WordWrap
            }

            Row {
                spacing: 12

                Button {
                    id: discardMailFactsButton

                    width: 40
                    height: 40
                    padding: 0
                    hoverEnabled: true

                    Accessible.name: "Kasta förslagen"
                    ToolTip.visible: hovered
                    ToolTip.text: "Kasta förslagen"

                    // Draw a trash-can icon.
                    contentItem: Item {
                        Item {
                            anchors.centerIn: parent
                            width: 20
                            height: 24

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

                            Rectangle {
                                x: 2
                                y: 5
                                width: 16
                                height: 2
                                radius: 1
                                color: root.dangerColor
                            }

                            Rectangle {
                                x: 4
                                y: 9
                                width: 12
                                height: 14
                                radius: 2
                                color: root.dangerColor

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

                    background: Rectangle {
                        radius: 8
                        color: discardMailFactsButton.down
                            ? root.dangerPressedColor
                            : discardMailFactsButton.hovered
                                ? root.dangerHoverColor
                                : root.surfaceColor
                        border.color: root.dangerBorderColor
                        border.width: 1
                    }

                    onClicked: backend.discard_mail_review()
                }

                Button {
                    id: saveMailFactsButton

                    width: 40
                    height: 40
                    padding: 0
                    hoverEnabled: true

                    enabled: mailFactsModel.count > 0
                    opacity: enabled ? 1.0 : 0.5

                    Accessible.name: "Spara valda fakta"
                    ToolTip.visible: hovered
                    ToolTip.text: "Spara valda fakta"

                    // Draw a floppy-disk icon.
                    contentItem: Item {
                        Rectangle {
                            anchors.centerIn: parent
                            width: 22
                            height: 22
                            radius: 2
                            color: root.accentColor

                            Rectangle {
                                x: 5
                                y: 2
                                width: 12
                                height: 7
                                radius: 1
                                color: root.surfaceColor

                                Rectangle {
                                    x: 8
                                    y: 1
                                    width: 2
                                    height: 5
                                    color: root.accentColor
                                }
                            }

                            Rectangle {
                                x: 4
                                y: 13
                                width: 14
                                height: 7
                                radius: 1
                                color: root.surfaceColor

                                Rectangle {
                                    x: 3
                                    y: 2
                                    width: 8
                                    height: 1
                                    color: root.accentColor
                                }

                                Rectangle {
                                    x: 3
                                    y: 4
                                    width: 8
                                    height: 1
                                    color: root.accentColor
                                }
                            }
                        }
                    }

                    background: Rectangle {
                        radius: 8
                        color: saveMailFactsButton.down
                            ? root.pressedColor
                            : saveMailFactsButton.hovered
                                ? root.hoverColor
                                : root.surfaceColor
                        border.color: root.accentColor
                        border.width: 1
                    }

                    onClicked: {
                        const selectedFacts = []

                        for (let i = 0; i < mailFactsModel.count; i++) {
                            const fact = mailFactsModel.get(i)

                            if (fact.keepFact) {
                                if (!fact.factText.trim()) {
                                    mailReviewDialog.statusMessage =
                                        "Valda faktauppgifter får inte vara tomma."
                                    return
                                }

                                selectedFacts.push(fact.factText.trim())
                            }
                        }

                        if (selectedFacts.length === 0) {
                            mailReviewDialog.statusMessage =
                                "Välj minst en faktauppgift att spara."
                            return
                        }

                        mailReviewDialog.statusMessage = ""
                        backend.save_reviewed_mail_facts(selectedFacts)
                    }
                }
            }
        }

        contentItem: RowLayout {
            spacing: 16

            ColumnLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.preferredWidth: 1

                Label {
                    text: "Originalmejl"
                    color: root.textColor
                    font.bold: true
                }

                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true

                    TextArea {
                        text: root.mailReviewText
                        readOnly: true
                        selectByMouse: true
                        textFormat: TextEdit.PlainText
                        wrapMode: TextEdit.Wrap
                        color: root.textColor

                        background: Rectangle {
                            color: root.assistantBubbleColor
                            radius: 8
                        }
                    }
                }
            }

            ColumnLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.preferredWidth: 1

                Label {
                    text: "Välj och redigera fakta"
                    color: root.textColor
                    font.bold: true
                }

                Label {
                    Layout.fillWidth: true
                    text: "Kontrollera förslagen mot originalet. "
                        + "AI:n kan missa eller misstolka information."
                    color: root.secondaryTextColor
                    wrapMode: Text.WordWrap
                }

                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    contentWidth: availableWidth
                    clip: true

                    Column {
                        width: parent.width
                        spacing: 12

                        Label {
                            width: parent.width
                            visible: mailFactsModel.count === 0
                            text: "AI:n föreslog inga faktauppgifter."
                            color: root.secondaryTextColor
                            wrapMode: Text.WordWrap
                        }

                        Repeater {
                            model: mailFactsModel

                            delegate: Column {
                                id: factItem

                                required property int index
                                required property string factText
                                required property bool keepFact

                                width: parent.width
                                spacing: 4

                                CheckBox {
                                    text: "Ta med förslag "
                                        + (factItem.index + 1)
                                    checked: factItem.keepFact
                                    palette.windowText: root.textColor

                                    onToggled: {
                                        mailFactsModel.setProperty(
                                            factItem.index,
                                            "keepFact",
                                            checked
                                        )
                                    }
                                }

                                TextArea {
                                    width: parent.width
                                    text: factItem.factText
                                    textFormat: TextEdit.PlainText
                                    wrapMode: TextEdit.Wrap
                                    selectByMouse: true
                                    color: root.textColor
                                    opacity: factItem.keepFact ? 1.0 : 0.5

                                    onTextChanged: {
                                        if (activeFocus) {
                                            mailFactsModel.setProperty(
                                                factItem.index,
                                                "factText",
                                                text
                                            )
                                        }
                                    }

                                    background: Rectangle {
                                        color: root.assistantBubbleColor
                                        radius: 8
                                        border.color: parent.activeFocus
                                            ? root.accentColor
                                            : root.borderColor
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    // Preview an email before choosing how to import it.
    Dialog {
        id: mailPreviewDialog

        property string emailText: ""
        property string sourceName: ""
        property string statusMessage: ""

        parent: root.contentItem
        anchors.centerIn: parent

        width: Math.min(800, root.width - 48)
        height: Math.min(550, root.height - 48)

        modal: true
        title: "Förhandsgranska mejl"

        footer: Item {
            implicitHeight: 90

            Label {
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.margins: 12

                text: mailPreviewDialog.statusMessage
                color: root.textColor
                wrapMode: Text.WordWrap
            }

            Button {
                id: saveWholeMailButton

                width: 40
                height: 40
                padding: 0
                hoverEnabled: true

                enabled: !root.isMailAnalyzing
                opacity: enabled ? 1.0 : 0.5

                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.margins: 12

                Accessible.name: "Spara hela mejlet"
                ToolTip.visible: hovered
                ToolTip.text: "Spara hela mejlet"

                // Draw the same floppy-disk icon.
                contentItem: Item {
                    Rectangle {
                        anchors.centerIn: parent
                        width: 22
                        height: 22
                        radius: 2
                        color: root.accentColor

                        // Upper label area with a visible outer border.
                        Rectangle {
                            x: 5
                            y: 2
                            width: 12
                            height: 7
                            radius: 1
                            color: root.surfaceColor

                            Rectangle {
                                x: 8
                                y: 1
                                width: 2
                                height: 5
                                color: root.accentColor
                            }
                        }

                        // Lower label area.
                        Rectangle {
                            x: 4
                            y: 13
                            width: 14
                            height: 7
                            radius: 1
                            color: root.surfaceColor

                            Rectangle {
                                x: 3
                                y: 2
                                width: 8
                                height: 1
                                color: root.accentColor
                            }

                            Rectangle {
                                x: 3
                                y: 4
                                width: 8
                                height: 1
                                color: root.accentColor
                            }
                        }
                    }
                }

                background: Rectangle {
                    radius: 8
                    color: saveWholeMailButton.down
                        ? root.pressedColor
                        : saveWholeMailButton.hovered
                            ? root.hoverColor
                            : root.surfaceColor
                    border.color: root.accentColor
                    border.width: 1
                }

                onClicked: {
                    mailPreviewDialog.statusMessage = ""
                    backend.save_previewed_mail(mailPreviewInput.text)
                }
            }

            // Show a rotating indicator during email analysis.
            Item {
                anchors.left: parent.left
                anchors.bottom: parent.bottom
                anchors.margins: 16

                width: 32
                height: 32
                visible: root.isMailAnalyzing

                Item {
                    id: mailSpinner
                    anchors.fill: parent

                    Repeater {
                        model: 8

                        Rectangle {
                            required property int index

                            width: 4
                            height: 4
                            radius: 2

                            x: 14 + 11 * Math.cos(index * Math.PI / 4)
                            y: 14 + 11 * Math.sin(index * Math.PI / 4)

                            color: root.accentColor
                            opacity: (index + 1) / 8
                        }
                    }

                    RotationAnimator on rotation {
                        from: 0
                        to: 360
                        duration: 1000
                        loops: Animation.Infinite
                        running: root.isMailAnalyzing
                    }
                }
            }

            Button {
                id: reviewMailButton

                anchors.left: parent.left
                anchors.bottom: parent.bottom
                anchors.margins: 12

                text: "Granska förslag"
                height: 40
                leftPadding: 16
                rightPadding: 16
                hoverEnabled: true

                visible: root.mailReviewPending && !root.isMailAnalyzing

                contentItem: Text {
                    text: reviewMailButton.text
                    color: root.textColor
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    radius: 8
                    color: reviewMailButton.down
                        ? root.pressedColor
                        : reviewMailButton.hovered
                            ? root.hoverColor
                            : root.assistantBubbleColor
                    border.color: root.accentColor
                    border.width: 1
                }

                onClicked: {
                    mailPreviewDialog.close()
                    mailReviewDialog.open()
                }
            }

            Button {
                id: analyzeMailButton

                anchors.right: saveWholeMailButton.left
                anchors.rightMargin: 12
                anchors.verticalCenter: saveWholeMailButton.verticalCenter

                width: 40
                height: 40
                padding: 0
                hoverEnabled: true

                enabled: !root.isMailAnalyzing
                    && !root.isThinking
                    && !root.modelLoading
                    && !root.mailReviewPending

                opacity: enabled ? 1.0 : 0.5

                Accessible.name: "Föreslå fakta med AI"
                ToolTip.visible: hovered
                ToolTip.text: "Föreslå fakta med AI"

                contentItem: Item {
                    Image {
                        anchors.centerIn: parent
                        width: 28
                        height: 28
                        source: "../assets/logo4.png"
                        fillMode: Image.PreserveAspectFit
                        smooth: true
                    }
                }

                background: Rectangle {
                    radius: 8
                    color: analyzeMailButton.down
                        ? root.pressedColor
                        : analyzeMailButton.hovered
                            ? root.hoverColor
                            : root.surfaceColor
                    border.color: root.accentColor
                    border.width: 1
                }

                onClicked: {
                    mailPreviewDialog.statusMessage = ""
                    backend.analyze_previewed_mail(mailPreviewInput.text)
                }
            }
        }

        background: Rectangle {
            color: root.surfaceColor
            radius: 12
            border.color: root.borderColor
        }

        header: Item {
            implicitHeight: 56

            Label {
                anchors.left: parent.left
                anchors.leftMargin: 16
                anchors.right: closeMailPreviewButton.left
                anchors.rightMargin: 12
                anchors.verticalCenter: parent.verticalCenter

                text: "Förhandsgranska: " + mailPreviewDialog.sourceName
                color: root.textColor
                font.pixelSize: 18
                font.bold: true
                elide: Text.ElideRight
            }

            Button {
                id: closeMailPreviewButton

                width: 28
                height: 28
                padding: 0
                hoverEnabled: true

                anchors.right: parent.right
                anchors.rightMargin: 12
                anchors.verticalCenter: parent.verticalCenter

                Accessible.name: "Stäng förhandsgranskningen"
                ToolTip.visible: hovered
                ToolTip.text: "Stäng"

                contentItem: Item {
                    Rectangle {
                        anchors.centerIn: parent
                        width: 14
                        height: 2
                        radius: 1
                        rotation: 45
                        color: root.secondaryTextColor
                    }

                    Rectangle {
                        anchors.centerIn: parent
                        width: 14
                        height: 2
                        radius: 1
                        rotation: -45
                        color: root.secondaryTextColor
                    }
                }

                background: Rectangle {
                    radius: 6
                    color: closeMailPreviewButton.down
                        ? root.pressedColor
                        : closeMailPreviewButton.hovered
                            ? root.hoverColor
                            : "transparent"
                }

                // Close the preview without saving the email.
                onClicked: mailPreviewDialog.close()
            }
        }

        contentItem: ScrollView {
            clip: true

            TextArea {
                id: mailPreviewInput

                text: mailPreviewDialog.emailText

                // Prevent editing while this email is being analyzed.
                readOnly: root.isMailAnalyzing

                // Retain edits when the preview is closed and reopened.
                onTextChanged: mailPreviewDialog.emailText = text

                selectByMouse: true
                textFormat: TextEdit.PlainText
                wrapMode: TextEdit.Wrap

                color: root.textColor
                selectedTextColor: root.surfaceColor
                selectionColor: root.accentColor

                background: Rectangle {
                    color: root.assistantBubbleColor
                    radius: 8
                }
            }
        }
    }

    // File picker for importing a mail file.
    FileDialog {
        id: mailFileDialog

        title: "Välj ett mejl"
        nameFilters: ["Mejlfiler (*.eml *.msg)"]
        fileMode: FileDialog.OpenFile

        onAccepted: {
            knowledgeDialog.clearSaveStatus()
            backend.preview_mail(selectedFile.toString())
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
            settingsDialog.setBackupStatus("Exporterar…")
            backend.export_knowledge(selectedFile.toString())
        }
    }

    // Choose where to import JSON file from.
    FileDialog {
        id: importBackupFileDialog

        title: "Importera backup"
        nameFilters: ["JSON-filer (*.json)"]

        onAccepted: {
            backend.import_knowledge(selectedFile.toString())
        }
    }    

    // Choose to load model or cancel.
    ModelLoadDialog {
        id: modelLoadDialog

        surfaceColor: root.surfaceColor
        borderColor: root.borderColor
        textColor: root.textColor
        secondaryTextColor: root.secondaryTextColor
        hoverColor: root.hoverColor
        pressedColor: root.pressedColor
        accentColor: root.accentColor
        assistantBubbleColor: root.assistantBubbleColor

        onLoadConfirmed: function(modelIndex) {
            backend.load_model(modelIndex)
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

            if (mailPreviewDialog.visible) {
                mailPreviewDialog.statusMessage = message
            }

            if (mailReviewDialog.visible) {
                mailReviewDialog.statusMessage = message
            }
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
            settingsDialog.setBackupStatus(message)
        }

        // Show error messages on faulty imports.
        function onImportResult(message) {
            settingsDialog.setBackupStatus(message)
        }        

        // Track whether a model is being loaded.
        function onModelLoadingChanged(loading) {
            root.modelLoading = loading
        }

        // Status for models being loaded
        function onModelLoadStatus(message) {
            root.modelLoadStatus = message
        }

        // Show the selected email without saving it.
        function onMailPreviewReady(emailText, sourceName) {
            mailPreviewDialog.emailText = emailText
            mailPreviewDialog.sourceName = sourceName
            mailPreviewDialog.statusMessage = ""
            mailPreviewDialog.open()
        }

        // Show whether email analysis is running.
        function onMailAnalysisChanged(analyzing) {
            root.isMailAnalyzing = analyzing
        }

        // Keep suggestions until the user reviews them.
        function onMailReviewReady(emailText, facts, source) {
            root.mailReviewText = emailText
            root.mailReviewFacts = facts
            root.mailReviewSource = source
            root.mailReviewPending = true
            

            mailPreviewDialog.statusMessage =
                "Analysen är klar. " + facts.length + " förslag att granska."

            mailReviewDialog.loadSuggestions(facts)
        }

        // Clear suggestions after saving or discarding them.
        function onMailReviewFinished() {
            mailReviewDialog.close()
            mailFactsModel.clear()
            mailReviewDialog.statusMessage = ""

            root.mailReviewPending = false
            root.mailReviewText = ""
            root.mailReviewFacts = []
            root.mailReviewSource = ""

            if (knowledgeViewDialog.visible) {
                knowledgeViewDialog.requestRefresh()
            }
        }
    }
}