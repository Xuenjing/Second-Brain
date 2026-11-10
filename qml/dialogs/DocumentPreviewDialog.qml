import QtQuick
import QtQuick.Controls

// Preview and edit document text before saving.
Dialog {
    id: documentPreviewDialog

    property string sourceName: ""
    property alias documentText: documentInput.text

    property string statusKey: ""

    signal saveRequested(string text, string source)
    signal analyzeRequested(string text, string source)

    property color surfaceColor
    property color borderColor
    property color textColor
    property color secondaryTextColor
    property color accentColor
    property color hoverColor
    property color pressedColor
    property color assistantBubbleColor

    property bool isAnalyzing: false
    property bool modelBusy: false
    property bool reviewPending: false
    property int statusCount: 0

    signal reviewRequested()

    modal: true
    padding: 16
    closePolicy: Popup.CloseOnEscape

    // Replace the text when a new document is opened.
    function loadDocument(text, source) {
        sourceName = source
        documentInput.text = text
        documentInput.cursorPosition = 0
        statusKey = ""
        statusCount = 0
    }

    background: Rectangle {
        color: documentPreviewDialog.surfaceColor
        radius: 12
        border.color: documentPreviewDialog.borderColor
        border.width: 1
    }

    header: Item {
        implicitHeight: 56

        Label {
            anchors.left: parent.left
            anchors.leftMargin: 16
            anchors.right: closeButton.left
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter

            text: translator.text(
                    "document_preview.title",
                    translator.language
                )
                + ": " + documentPreviewDialog.sourceName

            color: documentPreviewDialog.textColor
            font.pixelSize: 18
            font.bold: true
            elide: Text.ElideRight
            textFormat: Text.PlainText
        }

        Button {
            id: closeButton

            anchors.right: parent.right
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter

            width: 28
            height: 28
            padding: 0
            hoverEnabled: true

            Accessible.name: translator.text(
                "common.close",
                translator.language
            )
            ToolTip.visible: hovered
            ToolTip.text: Accessible.name

            contentItem: Item {
                Rectangle {
                    anchors.centerIn: parent
                    width: 14
                    height: 2
                    radius: 1
                    rotation: 45
                    color: documentPreviewDialog.secondaryTextColor
                }

                Rectangle {
                    anchors.centerIn: parent
                    width: 14
                    height: 2
                    radius: 1
                    rotation: -45
                    color: documentPreviewDialog.secondaryTextColor
                }
            }

            background: Rectangle {
                radius: 6
                color: closeButton.down
                    ? documentPreviewDialog.pressedColor
                    : closeButton.hovered
                        ? documentPreviewDialog.hoverColor
                        : "transparent"
            }

            onClicked: documentPreviewDialog.close()
        }
    }

    contentItem: ScrollView {
        clip: true
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

        TextArea {
            id: documentInput

            readOnly: documentPreviewDialog.isAnalyzing
                || documentPreviewDialog.reviewPending

            selectByMouse: true
            textFormat: TextEdit.PlainText
            wrapMode: TextEdit.Wrap
            padding: 12

            color: documentPreviewDialog.textColor
            selectedTextColor: documentPreviewDialog.surfaceColor
            selectionColor: documentPreviewDialog.accentColor

            background: Rectangle {
                color: documentPreviewDialog.assistantBubbleColor
                radius: 8
            }
        }
    }

    footer: Item {
        implicitHeight: Math.max(90, documentStatus.implicitHeight + 76)

        Label {
            id: documentStatus
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.margins: 12

            text: documentPreviewDialog.statusKey
                ? translator.text(
                    documentPreviewDialog.statusKey,
                    translator.language
                ).replace("{count}", documentPreviewDialog.statusCount.toString())
                : ""
            color: documentPreviewDialog.textColor
            wrapMode: Text.WordWrap
            textFormat: Text.PlainText
        }

        Button {
            id: saveDocumentButton

            width: 40
            height: 40
            padding: 0
            hoverEnabled: true

            enabled: !documentPreviewDialog.isAnalyzing
                && !documentPreviewDialog.reviewPending
            opacity: enabled ? 1.0 : 0.5

            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: 12

            Accessible.name: translator.text(
                "document_save.save_full",
                translator.language
            )
            ToolTip.visible: hovered
            ToolTip.text: translator.text(
                "document_save.save_full",
                translator.language
            )
            
            // Draw the same floppy-disk icon.
            contentItem: Item {
                Rectangle {
                    anchors.centerIn: parent
                    width: 22
                    height: 22
                    radius: 2
                    color: documentPreviewDialog.accentColor

                    // Upper label area with a visible outer border.
                    Rectangle {
                        x: 5
                        y: 2
                        width: 12
                        height: 7
                        radius: 1
                        color: documentPreviewDialog.surfaceColor

                        Rectangle {
                            x: 8
                            y: 1
                            width: 2
                            height: 5
                            color: documentPreviewDialog.accentColor
                        }
                    }

                    // Lower label area.
                    Rectangle {
                        x: 4
                        y: 13
                        width: 14
                        height: 7
                        radius: 1
                        color: documentPreviewDialog.surfaceColor

                        Rectangle {
                            x: 3
                            y: 2
                            width: 8
                            height: 1
                            color: documentPreviewDialog.accentColor
                        }

                        Rectangle {
                            x: 3
                            y: 4
                            width: 8
                            height: 1
                            color: documentPreviewDialog.accentColor
                        }
                    }
                }
            }

            background: Rectangle {
                radius: 8
                color: saveDocumentButton.down
                    ? documentPreviewDialog.pressedColor
                    : saveDocumentButton.hovered
                        ? documentPreviewDialog.hoverColor
                        : documentPreviewDialog.surfaceColor
                border.color: documentPreviewDialog.accentColor
                border.width: 1
            }

            onClicked: {
                documentPreviewDialog.statusKey = ""
                documentPreviewDialog.saveRequested(
                    documentPreviewDialog.documentText,
                    documentPreviewDialog.sourceName
                )
            }
        }

        // Show a rotating indicator during document analysis.
        Item {
            anchors.left: parent.left
            anchors.bottom: parent.bottom
            anchors.margins: 16

            width: 32
            height: 32
            visible: documentPreviewDialog.isAnalyzing

            Item {
                id: documentSpinner
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

                        color: documentPreviewDialog.accentColor
                        opacity: (index + 1) / 8
                    }
                }

                RotationAnimator on rotation {
                    from: 0
                    to: 360
                    duration: 1000
                    loops: Animation.Infinite
                    running: documentPreviewDialog.isAnalyzing
                }
            }
        }

        Button {
            id: reviewDocumentButton

            anchors.left: parent.left
            anchors.bottom: parent.bottom
            anchors.margins: 12

            text: translator.text(
                "mail_preview.review_suggestions",
                translator.language
            )
            height: 40
            leftPadding: 16
            rightPadding: 16
            hoverEnabled: true

            visible: documentPreviewDialog.reviewPending && !documentPreviewDialog.isAnalyzing

            contentItem: Text {
                text: reviewDocumentButton.text
                color: documentPreviewDialog.textColor
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            background: Rectangle {
                radius: 8
                color: reviewDocumentButton.down
                    ? documentPreviewDialog.pressedColor
                    : reviewDocumentButton.hovered
                        ? documentPreviewDialog.hoverColor
                        : documentPreviewDialog.assistantBubbleColor
                border.color: documentPreviewDialog.accentColor
                border.width: 1
            }

            onClicked: documentPreviewDialog.reviewRequested()
        }

        Button {
            id: analyzeDocumentButton

            anchors.right: saveDocumentButton.left
            anchors.rightMargin: 12
            anchors.verticalCenter: saveDocumentButton.verticalCenter

            width: 40
            height: 40
            padding: 0
            hoverEnabled: true

            enabled: !documentPreviewDialog.isAnalyzing
                && !documentPreviewDialog.modelBusy
                && !documentPreviewDialog.reviewPending

            opacity: enabled ? 1.0 : 0.5

            Accessible.name: translator.text(
                "document_preview.suggest_facts",
                translator.language
            )
            ToolTip.visible: hovered
            ToolTip.text: translator.text(
                "document_preview.suggest_facts",
                translator.language
            )
            
            contentItem: Item {
                Image {
                    anchors.centerIn: parent
                    width: 28
                    height: 28
                    source: "../../assets/logo4.png"
                    fillMode: Image.PreserveAspectFit
                    smooth: true
                }
            }

            background: Rectangle {
                radius: 8
                color: analyzeDocumentButton.down
                    ? documentPreviewDialog.pressedColor
                    : analyzeDocumentButton.hovered
                        ? documentPreviewDialog.hoverColor
                        : documentPreviewDialog.surfaceColor
                border.color: documentPreviewDialog.accentColor
                border.width: 1
            }

            onClicked: {
                if (!documentPreviewDialog.documentText.trim()) {
                    documentPreviewDialog.statusKey = "document_save.empty_text"
                    return
                }
                documentPreviewDialog.statusKey = ""
                documentPreviewDialog.analyzeRequested(
                    documentPreviewDialog.documentText,
                    documentPreviewDialog.sourceName
                )
            }
        }
    }

}