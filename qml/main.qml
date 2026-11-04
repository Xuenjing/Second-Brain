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

    // Track the assistant bubble waiting for a reply.
    property int pendingReplyIndex: -1

    function finishPendingReply(
        message, 
        sources,
        additionalSources,
        lessRelevantSources) {
        if (pendingReplyIndex < 0
                || pendingReplyIndex >= chatModel.count) {
            return
        }

        const replyIndex = pendingReplyIndex
        const replySources = sources || []
        const replyAdditionalSources = additionalSources || []
        const replyLessRelevantSources = lessRelevantSources || []

        // Update the existing nested source model.
        const sourceModel = chatModel.get(replyIndex).sources
        sourceModel.clear()

        for (let i = 0; i < replySources.length; i++) {
            sourceModel.append(replySources[i])
        }

        const additionalSourceModel = 
            chatModel.get(replyIndex).additionalSources
        
        additionalSourceModel.clear()

        for (let i = 0; i < replyAdditionalSources.length; i++) {
            additionalSourceModel.append(replyAdditionalSources[i])
        }

        const lessRelevantSourceModel =
            chatModel.get(replyIndex).lessRelevantSources

        lessRelevantSourceModel.clear()

        for (let i = 0; i < replyLessRelevantSources.length; i++) {
            lessRelevantSourceModel.append(replyLessRelevantSources[i])
        }        

        chatModel.setProperty(replyIndex, "message", message)
        chatModel.setProperty(
            replyIndex,
            "sourceCount",
            replySources.length
        )
        chatModel.setProperty(replyIndex, "isPending", false)

        pendingReplyIndex = -1
        chatPanel.scrollToBottom()
    }

    // Track email analysis and retain suggestions for review.
    property bool isMailAnalyzing: false
    property bool mailReviewPending: false
    property string mailReviewText: ""
    property var mailReviewFacts: []
    property string mailReviewSource: ""

    // Track the email-analysis bubble separately from chat replies.
    property int mailAnalysisIndex: -1

    function updateMailAnalysisBubble(message, isPending) {
        if (mailAnalysisIndex < 0
                || mailAnalysisIndex >= chatModel.count) {
            return
        }

        chatModel.setProperty(mailAnalysisIndex, "message", message)
        chatModel.setProperty(mailAnalysisIndex, "isPending", isPending)

        chatPanel.scrollToBottom()
    }

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
        }

        // Show a welcome message or the conversation.
        ChatView {
            id: chatPanel

            width: parent.width

            height: Math.max(
                0,
                parent.height - y - questionRow.height - parent.spacing
            )

            onMailReviewRequested: {
                if (root.mailReviewPending) {
                    mailPreviewDialog.close()
                    mailReviewDialog.open()
                }
            }

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

            onSourcesRequested: function(
                sources,
                additionalSources,
                lessRelevantSources
            ) {
                sourceDialog.sources = sources
                sourceDialog.additionalSources = additionalSources
                sourceDialog.lessRelevantSources = lessRelevantSources
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
                // Allow only one unanswered question at a time.
                if (root.isThinking || root.pendingReplyIndex !== -1) {
                    return
                }

                chatModel.append({
                    sender: "user",
                    message: question,
                    sources: [],
                    additionalSources: [],
                    lessRelevantSources: [],
                    sourceCount: 0,
                    canReviewMail: false,
                    isPending: false
                })

                root.pendingReplyIndex = chatModel.count

                chatModel.append({
                    sender: "assistant",
                    message: "Tänker…",
                    sources: [],
                    additionalSources: [],
                    lessRelevantSources: [],
                    sourceCount: 0,
                    canReviewMail: false,
                    isPending: true
                })

                backend.receive_text(question)
            }
        }
    }
    

    // Dialog for application settings.
    SettingsDialog {
        id: settingsDialog

        parent: root.contentItem
        anchors.centerIn: parent

        width: Math.min(500, root.width - 48)
        height: Math.min(550, root.height - 48)

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

        onRagSettingsRequested: function(topK, similarityThreshold) {
            backend.set_rag_settings(topK, similarityThreshold)
        }

        onRagSettingsLoadRequested: {
            backend.get_rag_settings()
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

        onDocumentDropped: function(fileUrl) {
            backend.import_dropped_document(fileUrl.toString())
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

        width: Math.min(820, parent.width - 80)
        height: Math.min(700, parent.height - 80)

        x: (parent.width - width) / 2
        y: (parent.height - height) / 2

        surfaceColor: root.surfaceColor
        textColor: root.textColor
        secondaryTextColor: root.secondaryTextColor
        assistantBubbleColor: root.assistantBubbleColor
        hoverColor: root.hoverColor
        pressedColor: root.pressedColor
        accentColor: root.accentColor

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
    MailReviewDialog {
        id: mailReviewDialog

        parent: root.contentItem
        anchors.centerIn: parent

        width: Math.min(900, root.width - 48)
        height: Math.min(600, root.height - 48)

        mailReviewText: root.mailReviewText
        mailReviewSource: root.mailReviewSource

        surfaceColor: root.surfaceColor
        borderColor: root.borderColor
        textColor: root.textColor
        secondaryTextColor: root.secondaryTextColor
        accentColor: root.accentColor
        hoverColor: root.hoverColor
        pressedColor: root.pressedColor
        assistantBubbleColor: root.assistantBubbleColor

        dangerColor: root.dangerColor
        dangerBorderColor: root.dangerBorderColor
        dangerHoverColor: root.dangerHoverColor
        dangerPressedColor: root.dangerPressedColor

        onDiscardRequested: backend.discard_mail_review()

        onSaveRequested: function(selectedFacts) {
            backend.save_reviewed_mail_facts(selectedFacts)
        }
    }

    // Preview an email before choosing how to import it.
    MailPreviewDialog {
        id: mailPreviewDialog

        parent: root.contentItem
        anchors.centerIn: parent

        width: Math.min(800, root.width - 48)
        height: Math.min(550, root.height - 48)

        isMailAnalyzing: root.isMailAnalyzing
        isThinking: root.isThinking
        modelLoading: root.modelLoading
        mailReviewPending: root.mailReviewPending

        surfaceColor: root.surfaceColor
        borderColor: root.borderColor
        textColor: root.textColor
        secondaryTextColor: root.secondaryTextColor
        accentColor: root.accentColor
        hoverColor: root.hoverColor
        pressedColor: root.pressedColor
        assistantBubbleColor: root.assistantBubbleColor

        onSaveRequested: function(emailText) {
            backend.save_previewed_mail(emailText)
        }

        onAnalyzeRequested: function(emailText) {
            if (!emailText.trim()) {
                mailPreviewDialog.statusMessage =
                    "Det finns inget mejl att analysera."
                return
            }

            mailAnalysisDialog.emailText = emailText
            mailAnalysisDialog.open()
        }

        onReviewRequested: {
            mailPreviewDialog.close()
            mailReviewDialog.open()
        }
    }

    // Confirm before starting the email analysis.
    MailAnalysisDialog {
        id: mailAnalysisDialog

        parent: root.contentItem
        anchors.centerIn: parent
        width: Math.min(520, root.width - 48)

        surfaceColor: root.surfaceColor
        borderColor: root.borderColor
        textColor: root.textColor
        hoverColor: root.hoverColor
        pressedColor: root.pressedColor
        accentColor: root.accentColor
        assistantBubbleColor: root.assistantBubbleColor

        onAnalysisConfirmed: function(emailText) {
            backend.analyze_previewed_mail(emailText)
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

        // Replace the waiting bubble with the answer.
        function onReplyReady(
            reply, 
            sources,
            additionalSources,
            lessRelevantSources) {
            root.finishPendingReply(
                reply, 
                sources || [],
                additionalSources || [],
                lessRelevantSources || [])
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

        // Replace the waiting bubble with an error message.
        function onReplyFailed(message) {
            root.finishPendingReply("Fel: " + message, [], [], [])
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

        // Create and update the email-analysis status bubble.
        function onMailAnalysisChanged(analyzing) {
            root.isMailAnalyzing = analyzing

            if (analyzing) {
                knowledgeDialog.setSaveStatus("Analyserar mejl…")
                mailPreviewDialog.statusMessage = "Analyserar mejl…"

                root.mailAnalysisIndex = chatModel.count

                chatModel.append({
                    sender: "assistant",
                    message: "Analyserar mejl…",
                    sources: [],
                    additionalSources: [],
                    lessRelevantSources: [],
                    sourceCount: 0,
                    canReviewMail: false,
                    isPending: true
                })

                chatPanel.scrollToBottom()
            } else if (root.mailAnalysisIndex >= 0
                    && chatModel.get(root.mailAnalysisIndex).isPending) {
                // Successful analysis updates the bubble in onMailReviewReady.
                root.updateMailAnalysisBubble(
                    "Mejlet kunde inte analyseras. Försök igen.",
                    false
                )
                root.mailAnalysisIndex = -1
            }
        }

        // Keep suggestions until the user reviews them.
        function onMailReviewReady(emailText, facts, source) {
            root.mailReviewText = emailText
            root.mailReviewFacts = facts
            root.mailReviewSource = source
            root.mailReviewPending = true
            

            const reviewMessage = facts.length > 0
                ? "Mejlanalysen är klar. " + facts.length
                    + " förslag att granska."
                : "Mejlanalysen är klar. Inga faktauppgifter föreslogs."

            knowledgeDialog.setSaveStatus(reviewMessage)
            mailPreviewDialog.statusMessage = reviewMessage

            mailReviewDialog.loadSuggestions(facts)

            root.updateMailAnalysisBubble(
                "Analysen av mejlet ”" + source + "” är klar. "
                    + facts.length + " förslag att granska.",
                false
            )

            if (root.mailAnalysisIndex >= 0) {
                chatModel.setProperty(
                    root.mailAnalysisIndex,
                    "canReviewMail",
                    true
                )
            }
        }

        // Clear suggestions after saving or discarding them.
        function onMailReviewFinished() {
            knowledgeDialog.clearSaveStatus()
            mailPreviewDialog.statusMessage = ""
            if (root.mailAnalysisIndex >= 0) {
                chatModel.setProperty(
                    root.mailAnalysisIndex,
                    "canReviewMail",
                    false
                )
            }

            root.updateMailAnalysisBubble(
                "Mejlgranskningen är avslutad.",
                false
            )
            root.mailAnalysisIndex = -1

            mailReviewDialog.close()
            mailReviewDialog.clearSuggestions()

            root.mailReviewPending = false
            root.mailReviewText = ""
            root.mailReviewFacts = []
            root.mailReviewSource = ""

            if (knowledgeViewDialog.visible) {
                knowledgeViewDialog.requestRefresh()
            }
        }

        // Signal from backend whether rag settings were saved or not
        function onRagSettingsResult(success, message) {
            settingsDialog.showRagStatus(success, message)
        }

        function onRagSettingsLoaded(
            top_k,
            similarityThreshold
        ) {
            settingsDialog.loadRagSettings(
                top_k,
                similarityThreshold
            )
        }
    }
}