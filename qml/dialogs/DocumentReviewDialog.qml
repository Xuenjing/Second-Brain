import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// Review suggested facts alongside the document text.
Dialog {
    id: documentReviewDialog

    modal: true
    property string statusMessage: ""

    property string documentReviewText: ""
    property string documentReviewSource: ""

    property color surfaceColor
    property color borderColor
    property color textColor
    property color secondaryTextColor
    property color accentColor
    property color hoverColor
    property color pressedColor
    property color assistantBubbleColor

    property color dangerColor
    property color dangerBorderColor
    property color dangerHoverColor
    property color dangerPressedColor

    signal discardRequested()
    signal saveRequested(var selectedFacts)
    

    // Keep edits when the dialog is closed and reopened.
    ListModel {
        id: documentFactsModel
    }

    function loadSuggestions(facts) {
        documentFactsModel.clear()

        for (let i = 0; i < facts.length; i++) {
            documentFactsModel.append({
                factText: facts[i],
                keepFact: true
            })
        }
    }

    // Clear suggestions after saving or discarding them.
    function clearSuggestions() {
        documentFactsModel.clear()
        statusMessage = ""
    }

    background: Rectangle {
        color: documentReviewDialog.surfaceColor
        radius: 12
        border.color: documentReviewDialog.borderColor
    }

    header: Item {
        implicitHeight: 56

        Label {
            anchors.left: parent.left
            anchors.leftMargin: 16
            anchors.right: closeMailReviewButton.left
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter

            text: translator.text(
                    "mail_review.title_prefix",
                    translator.language
                )
                + " "
                + documentReviewDialog.documentReviewSource
            color: documentReviewDialog.textColor
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

            Accessible.name: translator.text(
                "mail_review.close",
                translator.language
            )
            ToolTip.visible: hovered
            ToolTip.text: translator.text(
                "mail_review.close_keep",
                translator.language
            )


            contentItem: Text {
                text: "×"
                color: documentReviewDialog.secondaryTextColor
                font.pixelSize: 24
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            background: Rectangle {
                radius: 6
                color: closeMailReviewButton.down
                    ? documentReviewDialog.pressedColor
                    : closeMailReviewButton.hovered
                        ? documentReviewDialog.hoverColor
                        : "transparent"
            }

            onClicked: documentReviewDialog.close()
        }
    }

    footer: Control {
        padding: 12

        implicitHeight: contentItem.implicitHeight
            + topPadding + bottomPadding

        contentItem: Column {
            spacing: 8

        Label {
            width: parent.width
            text: documentReviewDialog.statusMessage
            visible: text.length > 0
            color: documentReviewDialog.textColor
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

                Accessible.name: translator.text(
                    "mail_review.discard",
                    translator.language
                )
                ToolTip.visible: hovered
                ToolTip.text: translator.text(
                    "mail_review.discard",
                    translator.language
                )


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
                            border.color: documentReviewDialog.dangerColor
                            border.width: 2
                        }

                        Rectangle {
                            x: 2
                            y: 5
                            width: 16
                            height: 2
                            radius: 1
                            color: documentReviewDialog.dangerColor
                        }

                        Rectangle {
                            x: 4
                            y: 9
                            width: 12
                            height: 14
                            radius: 2
                            color: documentReviewDialog.dangerColor

                            Repeater {
                                model: 3

                                Rectangle {
                                    required property int index

                                    x: 3 + index * 3
                                    y: 3
                                    width: 1
                                    height: 8
                                    radius: 0.5
                                    color: documentReviewDialog.surfaceColor
                                }
                            }
                        }
                    }
                }

                background: Rectangle {
                    radius: 8
                    color: discardMailFactsButton.down
                        ? documentReviewDialog.dangerPressedColor
                        : discardMailFactsButton.hovered
                            ? documentReviewDialog.dangerHoverColor
                            : documentReviewDialog.surfaceColor
                    border.color: documentReviewDialog.dangerBorderColor
                    border.width: 1
                }

                onClicked: documentReviewDialog.discardRequested()
            }

            Button {
                id: saveMailFactsButton

                width: 40
                height: 40
                padding: 0
                hoverEnabled: true

                enabled: documentFactsModel.count > 0
                opacity: enabled ? 1.0 : 0.5

                Accessible.name: translator.text(
                    "mail_review.save_selected",
                    translator.language
                )
                ToolTip.visible: hovered
                ToolTip.text: translator.text(
                    "mail_review.save_selected",
                    translator.language
                )

                // Draw a floppy-disk icon.
                contentItem: Item {
                    Rectangle {
                        anchors.centerIn: parent
                        width: 22
                        height: 22
                        radius: 2
                        color: documentReviewDialog.accentColor

                        Rectangle {
                            x: 5
                            y: 2
                            width: 12
                            height: 7
                            radius: 1
                            color: documentReviewDialog.surfaceColor

                            Rectangle {
                                x: 8
                                y: 1
                                width: 2
                                height: 5
                                color: documentReviewDialog.accentColor
                            }
                        }

                        Rectangle {
                            x: 4
                            y: 13
                            width: 14
                            height: 7
                            radius: 1
                            color: documentReviewDialog.surfaceColor

                            Rectangle {
                                x: 3
                                y: 2
                                width: 8
                                height: 1
                                color: documentReviewDialog.accentColor
                            }

                            Rectangle {
                                x: 3
                                y: 4
                                width: 8
                                height: 1
                                color: documentReviewDialog.accentColor
                            }
                        }
                    }
                }

                background: Rectangle {
                    radius: 8
                    color: saveMailFactsButton.down
                        ? documentReviewDialog.pressedColor
                        : saveMailFactsButton.hovered
                            ? documentReviewDialog.hoverColor
                            : documentReviewDialog.surfaceColor
                    border.color: documentReviewDialog.accentColor
                    border.width: 1
                }

                onClicked: {
                    const selectedFacts = []

                    for (let i = 0; i < documentFactsModel.count; i++) {
                        const fact = documentFactsModel.get(i)

                        if (fact.keepFact) {
                            if (!fact.factText.trim()) {
                                documentReviewDialog.statusMessage = translator.text(
                                    "mail_review.empty_selected_error",
                                    translator.language
                                )
                                return
                            }

                            selectedFacts.push(fact.factText.trim())
                        }
                    }

                    if (selectedFacts.length === 0) {
                        documentReviewDialog.statusMessage = translator.text(
                            "mail_review.none_selected_error",
                            translator.language
                        )
                        return
                    }

                    documentReviewDialog.statusMessage = ""
                    documentReviewDialog.saveRequested(selectedFacts)
                }
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
                text: translator.text(
                    "document_review.original_text",
                    translator.language
                )
                color: documentReviewDialog.textColor
                font.bold: true
            }

            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true

                TextArea {
                    text: documentReviewDialog.documentReviewText
                    readOnly: true
                    selectByMouse: true
                    textFormat: TextEdit.PlainText
                    wrapMode: TextEdit.Wrap
                    color: documentReviewDialog.textColor

                    background: Rectangle {
                        color: documentReviewDialog.assistantBubbleColor
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
                text: translator.text(
                    "mail_review.select_edit",
                    translator.language
                )
                color: documentReviewDialog.textColor
                font.bold: true
            }

            Label {
                Layout.fillWidth: true
                text: translator.text(
                    "document_review.check_warning",
                    translator.language
                )
                color: documentReviewDialog.secondaryTextColor
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
                        visible: documentFactsModel.count === 0
                        text: translator.text(
                            "mail_review.no_facts",
                            translator.language
                        )
                        color: documentReviewDialog.secondaryTextColor
                        wrapMode: Text.WordWrap
                    }

                    Repeater {
                        model: documentFactsModel

                        delegate: Column {
                            id: factItem

                            required property int index
                            required property string factText
                            required property bool keepFact

                            width: parent.width
                            spacing: 4

                            CheckBox {
                                text: translator.text(
                                        "mail_review.include_suggestion",
                                        translator.language
                                    )
                                    + " "
                                    + (factItem.index + 1)
                                checked: factItem.keepFact
                                palette.windowText: documentReviewDialog.textColor

                                onToggled: {
                                    documentFactsModel.setProperty(
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
                                color: documentReviewDialog.textColor
                                opacity: factItem.keepFact ? 1.0 : 0.5

                                onTextChanged: {
                                    if (activeFocus) {
                                        documentFactsModel.setProperty(
                                            factItem.index,
                                            "factText",
                                            text
                                        )
                                    }
                                }

                                background: Rectangle {
                                    color: documentReviewDialog.assistantBubbleColor
                                    radius: 8
                                    border.color: parent.activeFocus
                                        ? documentReviewDialog.accentColor
                                        : documentReviewDialog.borderColor
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}