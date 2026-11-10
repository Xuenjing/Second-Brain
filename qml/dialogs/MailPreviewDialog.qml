import QtQuick
import QtQuick.Controls

// Preview an email before choosing how to import it.
Dialog {
    id: mailPreviewDialog

    property string emailText: ""
    property string sourceName: ""
    property string statusMessage: ""

    property bool isMailAnalyzing: false
    property bool isThinking: false
    property bool modelLoading: false
    property bool mailReviewPending: false

    property color surfaceColor
    property color borderColor
    property color textColor
    property color secondaryTextColor
    property color accentColor
    property color hoverColor
    property color pressedColor
    property color assistantBubbleColor

    signal saveRequested(string emailText)
    signal analyzeRequested(string emailText)
    signal reviewRequested()

    modal: true
    title: translator.text(
        "mail_preview.title",
        translator.language
    )

    footer: Item {
        implicitHeight: 90

        Label {
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.margins: 12

            text: mailPreviewDialog.statusMessage
            color: mailPreviewDialog.textColor
            wrapMode: Text.WordWrap
        }

        Button {
            id: saveWholeMailButton

            width: 40
            height: 40
            padding: 0
            hoverEnabled: true

            enabled: !mailPreviewDialog.isMailAnalyzing
            opacity: enabled ? 1.0 : 0.5

            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: 12

            Accessible.name: translator.text(
                "mail_preview.save_full",
                translator.language
            )
            ToolTip.visible: hovered
            ToolTip.text: translator.text(
                "mail_preview.save_full",
                translator.language
            )
            
            // Draw the same floppy-disk icon.
            contentItem: Item {
                Rectangle {
                    anchors.centerIn: parent
                    width: 22
                    height: 22
                    radius: 2
                    color: mailPreviewDialog.accentColor

                    // Upper label area with a visible outer border.
                    Rectangle {
                        x: 5
                        y: 2
                        width: 12
                        height: 7
                        radius: 1
                        color: mailPreviewDialog.surfaceColor

                        Rectangle {
                            x: 8
                            y: 1
                            width: 2
                            height: 5
                            color: mailPreviewDialog.accentColor
                        }
                    }

                    // Lower label area.
                    Rectangle {
                        x: 4
                        y: 13
                        width: 14
                        height: 7
                        radius: 1
                        color: mailPreviewDialog.surfaceColor

                        Rectangle {
                            x: 3
                            y: 2
                            width: 8
                            height: 1
                            color: mailPreviewDialog.accentColor
                        }

                        Rectangle {
                            x: 3
                            y: 4
                            width: 8
                            height: 1
                            color: mailPreviewDialog.accentColor
                        }
                    }
                }
            }

            background: Rectangle {
                radius: 8
                color: saveWholeMailButton.down
                    ? mailPreviewDialog.pressedColor
                    : saveWholeMailButton.hovered
                        ? mailPreviewDialog.hoverColor
                        : mailPreviewDialog.surfaceColor
                border.color: mailPreviewDialog.accentColor
                border.width: 1
            }

            onClicked: {
                mailPreviewDialog.statusMessage = ""
                mailPreviewDialog.saveRequested(mailPreviewInput.text)
            }
        }

        // Show a rotating indicator during email analysis.
        Item {
            anchors.left: parent.left
            anchors.bottom: parent.bottom
            anchors.margins: 16

            width: 32
            height: 32
            visible: mailPreviewDialog.isMailAnalyzing

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

                        color: mailPreviewDialog.accentColor
                        opacity: (index + 1) / 8
                    }
                }

                RotationAnimator on rotation {
                    from: 0
                    to: 360
                    duration: 1000
                    loops: Animation.Infinite
                    running: mailPreviewDialog.isMailAnalyzing
                }
            }
        }

        Button {
            id: reviewMailButton

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

            visible: mailPreviewDialog.mailReviewPending && !mailPreviewDialog.isMailAnalyzing

            contentItem: Text {
                text: reviewMailButton.text
                color: mailPreviewDialog.textColor
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            background: Rectangle {
                radius: 8
                color: reviewMailButton.down
                    ? mailPreviewDialog.pressedColor
                    : reviewMailButton.hovered
                        ? mailPreviewDialog.hoverColor
                        : mailPreviewDialog.assistantBubbleColor
                border.color: mailPreviewDialog.accentColor
                border.width: 1
            }

            onClicked: mailPreviewDialog.reviewRequested()
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

            enabled: !mailPreviewDialog.isMailAnalyzing
                && !mailPreviewDialog.isThinking
                && !mailPreviewDialog.modelLoading
                && !mailPreviewDialog.mailReviewPending

            opacity: enabled ? 1.0 : 0.5

            Accessible.name: translator.text(
                "mail_preview.suggest_facts",
                translator.language
            )
            ToolTip.visible: hovered
            ToolTip.text: translator.text(
                "mail_preview.suggest_facts",
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
                color: analyzeMailButton.down
                    ? mailPreviewDialog.pressedColor
                    : analyzeMailButton.hovered
                        ? mailPreviewDialog.hoverColor
                        : mailPreviewDialog.surfaceColor
                border.color: mailPreviewDialog.accentColor
                border.width: 1
            }

            onClicked: {
                mailPreviewDialog.statusMessage = ""
                mailPreviewDialog.analyzeRequested(mailPreviewInput.text)
            }
        }
    }

    background: Rectangle {
        color: mailPreviewDialog.surfaceColor
        radius: 12
        border.color: mailPreviewDialog.borderColor
    }

    header: Item {
        implicitHeight: 56

        Label {
            anchors.left: parent.left
            anchors.leftMargin: 16
            anchors.right: closeMailPreviewButton.left
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter

            text: translator.text(
                    "mail_preview.preview_prefix",
                    translator.language
                )
                + " "
                + mailPreviewDialog.sourceName
            color: mailPreviewDialog.textColor
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

            Accessible.name: translator.text(
                "mail_preview.close_preview",
                translator.language
            )
            ToolTip.visible: hovered
            ToolTip.text: translator.text(
                "common.close",
                translator.language
            )

            contentItem: Item {
                Rectangle {
                    anchors.centerIn: parent
                    width: 14
                    height: 2
                    radius: 1
                    rotation: 45
                    color: mailPreviewDialog.secondaryTextColor
                }

                Rectangle {
                    anchors.centerIn: parent
                    width: 14
                    height: 2
                    radius: 1
                    rotation: -45
                    color: mailPreviewDialog.secondaryTextColor
                }
            }

            background: Rectangle {
                radius: 6
                color: closeMailPreviewButton.down
                    ? mailPreviewDialog.pressedColor
                    : closeMailPreviewButton.hovered
                        ? mailPreviewDialog.hoverColor
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
            readOnly: mailPreviewDialog.isMailAnalyzing

            // Retain edits when the preview is closed and reopened.
            onTextChanged: mailPreviewDialog.emailText = text

            selectByMouse: true
            textFormat: TextEdit.PlainText
            wrapMode: TextEdit.Wrap

            color: mailPreviewDialog.textColor
            selectedTextColor: mailPreviewDialog.surfaceColor
            selectionColor: mailPreviewDialog.accentColor

            background: Rectangle {
                color: mailPreviewDialog.assistantBubbleColor
                radius: 8
            }
        }
    }
}