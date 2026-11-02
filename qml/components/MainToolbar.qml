import QtQuick
import QtQuick.Controls

Row {
    id: mainToolbar

    property color textColor
    property color accentColor
    property color surfaceColor
    property color borderColor
    property color hoverColor
    property color pressedColor

    signal addKnowledgeRequested()
    signal viewKnowledgeRequested()
    signal modelLoadConfirmationRequested(
        int modelIndex,
        string modelName
    )

    property bool modelLoading: false
    

    spacing: 12

    Button {
        id: addKnowledgeButton

        text: "Lägg till kunskap"
        height: 40
        leftPadding: 16
        rightPadding: 16
        hoverEnabled: true

        contentItem: Text {
            text: addKnowledgeButton.text
            color: mainToolbar.textColor
            font.pixelSize: 14
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        background: Rectangle {
            radius: 8

            color: addKnowledgeButton.down
                ? mainToolbar.pressedColor
                : addKnowledgeButton.hovered
                    ? mainToolbar.hoverColor
                    : mainToolbar.surfaceColor

            border.color: mainToolbar.accentColor
            border.width: 1
        }

        onClicked: {
            mainToolbar.addKnowledgeRequested()
        }
    }

    Button {
        id: viewKnowledgeButton

        text: "Visa kunskapsposter"
        height: 40
        leftPadding: 16
        rightPadding: 16
        hoverEnabled: true

        contentItem: Text {
            text: viewKnowledgeButton.text
            color: mainToolbar.textColor
            font.pixelSize: 14
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        background: Rectangle {
            radius: 8

            color: viewKnowledgeButton.down
                ? mainToolbar.pressedColor
                : viewKnowledgeButton.hovered
                    ? mainToolbar.hoverColor
                    : mainToolbar.surfaceColor

            border.color: mainToolbar.accentColor
            border.width: 1
        }

        onClicked: {
            mainToolbar.viewKnowledgeRequested()
        }
    }

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

        indicator: Text {
            x: modelSelector.width - width - 12
            width: 16
            height: modelSelector.height

            text: "\u25BE"
            color: mainToolbar.textColor
            font.pixelSize: 18

            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        contentItem: Text {
            text: modelSelector.displayText
            color: mainToolbar.textColor
            font.pixelSize: 14

            leftPadding: 12
            rightPadding: 32

            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
        }

        background: Rectangle {
            color: mainToolbar.surfaceColor
            radius: 8

            border.color: modelSelector.activeFocus
                ? mainToolbar.accentColor
                : mainToolbar.borderColor

            border.width: 1
        }

        delegate: ItemDelegate {
            width: ListView.view.width
            height: 40
            hoverEnabled: true

            contentItem: Text {
                text: modelData
                color: mainToolbar.textColor
                font.pixelSize: 14
                verticalAlignment: Text.AlignVCenter
                leftPadding: 12
            }

            background: Rectangle {
                radius: 6

                color: parent.highlighted
                    ? mainToolbar.pressedColor
                    : parent.hovered
                        ? mainToolbar.hoverColor
                        : mainToolbar.surfaceColor
            }
        }

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
                color: mainToolbar.surfaceColor
                radius: 8
                border.color: mainToolbar.borderColor
                border.width: 1
            }
        }
    }

    Button {
        id: loadModelButton

        text: "Ladda modell"
        height: 40
        leftPadding: 16
        rightPadding: 16
        hoverEnabled: true

        enabled: !mainToolbar.modelLoading

        contentItem: Text {
            text: mainToolbar.modelLoading
                ? "Laddar..."
                : "Ladda modell"
            color: mainToolbar.accentColor
            font.pixelSize: 14
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        background: Rectangle {
            radius: 8

            color: loadModelButton.down
                ? mainToolbar.pressedColor
                : loadModelButton.hovered
                    ? mainToolbar.hoverColor
                    : mainToolbar.surfaceColor

            border.width: 1
        }

        onClicked: {
            mainToolbar.modelLoadConfirmationRequested(
                modelSelector.currentIndex,
                modelSelector.currentText
            )
        }
    }        

}