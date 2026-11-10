import QtQuick
import QtQuick.Controls

Dialog {
    id: documentAnalysisDialog

    property string documentText: ""

    property color surfaceColor
    property color borderColor
    property color textColor
    property color hoverColor
    property color pressedColor
    property color accentColor
    property color assistantBubbleColor

    signal analysisConfirmed(string documentText)

    title: translator.text(
        "document_analysis.title",
        translator.language
    )
    modal: true

    background: Rectangle {
        color: documentAnalysisDialog.surfaceColor
        radius: 12
        border.color: documentAnalysisDialog.borderColor
        border.width: 1
    }

    header: Label {
        text: documentAnalysisDialog.title
        color: documentAnalysisDialog.textColor
        font.pixelSize: 18
        font.bold: true
        padding: 16
    }

    contentItem: Rectangle {
        implicitHeight: warningText.implicitHeight + 24
        radius: 8
        color: documentAnalysisDialog.assistantBubbleColor

        Label {
            id: warningText

            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.margins: 12

            text: translator.text(
                "document_analysis.warning",
                translator.language
            )

            color: documentAnalysisDialog.textColor
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

            Repeater {
                model: [
                    translator.text(
                        "common.cancel",
                        translator.language
                    ),
                    translator.text(
                        "document_analysis.analyze",
                        translator.language
                    )
                ]

                delegate: Button {
                    id: actionButton

                    required property int index
                    required property string modelData

                    text: modelData
                    width: 130
                    height: 40
                    hoverEnabled: true

                    contentItem: Text {
                        text: actionButton.text
                        color: documentAnalysisDialog.textColor
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        radius: 8
                        color: actionButton.down
                            ? documentAnalysisDialog.pressedColor
                            : actionButton.hovered
                                ? documentAnalysisDialog.hoverColor
                                : documentAnalysisDialog.surfaceColor

                        border.color: actionButton.index === 1
                            ? documentAnalysisDialog.accentColor
                            : documentAnalysisDialog.borderColor
                        border.width: 1
                    }

                    onClicked: {
                        const textToAnalyze = documentAnalysisDialog.documentText
                        documentAnalysisDialog.close()

                        if (index === 1) {
                            documentAnalysisDialog.analysisConfirmed(
                                textToAnalyze
                            )
                        }
                    }
                }
            }
        }
    }

    onClosed: documentText = ""
}