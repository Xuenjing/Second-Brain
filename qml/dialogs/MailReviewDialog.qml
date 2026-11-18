import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// Review suggested facts alongside the original email.
Dialog {
    id: mailReviewDialog

    modal: true
    property string statusMessage: ""

    property string mailReviewText: ""
    property string mailReviewSource: ""

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

    // Clear suggestions after saving or discarding them.
    function clearSuggestions() {
        mailFactsModel.clear()
        statusMessage = ""
    }

    background: Rectangle {
        color: mailReviewDialog.surfaceColor
        radius: 12
        border.color: mailReviewDialog.borderColor
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
                + mailReviewDialog.mailReviewSource
            color: mailReviewDialog.textColor
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
                color: mailReviewDialog.secondaryTextColor
                font.pixelSize: 24
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            background: Rectangle {
                radius: 6
                color: closeMailReviewButton.down
                    ? mailReviewDialog.pressedColor
                    : closeMailReviewButton.hovered
                        ? mailReviewDialog.hoverColor
                        : "transparent"
            }

            onClicked: mailReviewDialog.close()
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
            text: mailReviewDialog.statusMessage
            visible: text.length > 0
            color: mailReviewDialog.textColor
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
                            border.color: mailReviewDialog.dangerColor
                            border.width: 2
                        }

                        Rectangle {
                            x: 2
                            y: 5
                            width: 16
                            height: 2
                            radius: 1
                            color: mailReviewDialog.dangerColor
                        }

                        Rectangle {
                            x: 4
                            y: 9
                            width: 12
                            height: 14
                            radius: 2
                            color: mailReviewDialog.dangerColor

                            Repeater {
                                model: 3

                                Rectangle {
                                    required property int index

                                    x: 3 + index * 3
                                    y: 3
                                    width: 1
                                    height: 8
                                    radius: 0.5
                                    color: mailReviewDialog.surfaceColor
                                }
                            }
                        }
                    }
                }

                background: Rectangle {
                    radius: 8
                    color: discardMailFactsButton.down
                        ? mailReviewDialog.dangerPressedColor
                        : discardMailFactsButton.hovered
                            ? mailReviewDialog.dangerHoverColor
                            : mailReviewDialog.surfaceColor
                    border.color: mailReviewDialog.dangerBorderColor
                    border.width: 1
                }

                onClicked: mailReviewDialog.discardRequested()
            }

            Button {
                id: saveMailFactsButton

                width: 40
                height: 40
                padding: 0
                hoverEnabled: true

                enabled: mailFactsModel.count > 0
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
                        color: mailReviewDialog.accentColor

                        Rectangle {
                            x: 5
                            y: 2
                            width: 12
                            height: 7
                            radius: 1
                            color: mailReviewDialog.surfaceColor

                            Rectangle {
                                x: 8
                                y: 1
                                width: 2
                                height: 5
                                color: mailReviewDialog.accentColor
                            }
                        }

                        Rectangle {
                            x: 4
                            y: 13
                            width: 14
                            height: 7
                            radius: 1
                            color: mailReviewDialog.surfaceColor

                            Rectangle {
                                x: 3
                                y: 2
                                width: 8
                                height: 1
                                color: mailReviewDialog.accentColor
                            }

                            Rectangle {
                                x: 3
                                y: 4
                                width: 8
                                height: 1
                                color: mailReviewDialog.accentColor
                            }
                        }
                    }
                }

                background: Rectangle {
                    radius: 8
                    color: saveMailFactsButton.down
                        ? mailReviewDialog.pressedColor
                        : saveMailFactsButton.hovered
                            ? mailReviewDialog.hoverColor
                            : mailReviewDialog.surfaceColor
                    border.color: mailReviewDialog.accentColor
                    border.width: 1
                }

                onClicked: {
                    const selectedFacts = []

                    for (let i = 0; i < mailFactsModel.count; i++) {
                        const fact = mailFactsModel.get(i)

                        if (fact.keepFact) {
                            if (!fact.factText.trim()) {
                                mailReviewDialog.statusMessage = translator.text(
                                    "mail_review.empty_selected_error",
                                    translator.language
                                )
                                return
                            }

                            selectedFacts.push(fact.factText.trim())
                        }
                    }

                    if (selectedFacts.length === 0) {
                        mailReviewDialog.statusMessage = translator.text(
                            "mail_review.none_selected_error",
                            translator.language
                        )
                        return
                    }

                    mailReviewDialog.statusMessage = ""
                    mailReviewDialog.saveRequested(selectedFacts)
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
                    "mail_review.original_email",
                    translator.language
                )
                color: mailReviewDialog.textColor
                font.bold: true
            }

            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true

                TextArea {
                    text: mailReviewDialog.mailReviewText
                    readOnly: true
                    selectByMouse: true
                    textFormat: TextEdit.PlainText
                    wrapMode: TextEdit.Wrap
                    color: mailReviewDialog.textColor

                    background: Rectangle {
                        color: mailReviewDialog.assistantBubbleColor
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
                color: mailReviewDialog.textColor
                font.bold: true
            }

            Label {
                Layout.fillWidth: true
                text: translator.text(
                    "mail_review.check_warning",
                    translator.language
                )
                color: mailReviewDialog.secondaryTextColor
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
                        text: translator.text(
                            "mail_review.no_facts",
                            translator.language
                        )
                        color: mailReviewDialog.secondaryTextColor
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
                                text: translator.text(
                                        "mail_review.include_suggestion",
                                        translator.language
                                    )
                                    + " "
                                    + (factItem.index + 1)
                                checked: factItem.keepFact
                                palette.windowText: mailReviewDialog.textColor

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
                                color: mailReviewDialog.textColor
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
                                    color: mailReviewDialog.assistantBubbleColor
                                    radius: 8
                                    border.color: parent.activeFocus
                                        ? mailReviewDialog.accentColor
                                        : mailReviewDialog.borderColor
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}