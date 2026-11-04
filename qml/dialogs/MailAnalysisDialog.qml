import QtQuick
import QtQuick.Controls

Dialog {
    id: mailAnalysisDialog

    property string emailText: ""

    property color surfaceColor
    property color borderColor
    property color textColor
    property color hoverColor
    property color pressedColor
    property color accentColor
    property color assistantBubbleColor

    signal analysisConfirmed(string emailText)

    title: "Analysera mejl med AI?"
    modal: true

    background: Rectangle {
        color: mailAnalysisDialog.surfaceColor
        radius: 12
        border.color: mailAnalysisDialog.borderColor
        border.width: 1
    }

    header: Label {
        text: mailAnalysisDialog.title
        color: mailAnalysisDialog.textColor
        font.pixelSize: 18
        font.bold: true
        padding: 16
    }

    contentItem: Rectangle {
        implicitHeight: warningText.implicitHeight + 24
        radius: 8
        color: mailAnalysisDialog.assistantBubbleColor

        Label {
            id: warningText

            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.margins: 12

            text: "AI-analysen kan ta flera minuter beroende på mejlets längd, den laddade modellen och datorns prestanda. Du får granska och redigera förslagen innan något sparas."

            color: mailAnalysisDialog.textColor
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
                model: ["Avbryt", "Analysera mejl"]

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
                        color: mailAnalysisDialog.textColor
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        radius: 8
                        color: actionButton.down
                            ? mailAnalysisDialog.pressedColor
                            : actionButton.hovered
                                ? mailAnalysisDialog.hoverColor
                                : mailAnalysisDialog.surfaceColor

                        border.color: actionButton.index === 1
                            ? mailAnalysisDialog.accentColor
                            : mailAnalysisDialog.borderColor
                        border.width: 1
                    }

                    onClicked: {
                        const textToAnalyze = mailAnalysisDialog.emailText
                        mailAnalysisDialog.close()

                        if (index === 1) {
                            mailAnalysisDialog.analysisConfirmed(
                                textToAnalyze
                            )
                        }
                    }
                }
            }
        }
    }

    onClosed: emailText = ""
}