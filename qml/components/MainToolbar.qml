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

        text: translator.text(
            "toolbar.add_knowledge",
            translator.language
        )
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

        text: translator.text(
            "toolbar.view_knowledge",
            translator.language
        )
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
            translator.text(
                "toolbar.model_fast",
                translator.language
            ),
            translator.text(
                "toolbar.model_recommended",
                translator.language
            ),
            translator.text(
                "toolbar.model_slow",
                translator.language
            )
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

        text: translator.text(
            "toolbar.load_model",
            translator.language
        )
        height: 40
        leftPadding: 16
        rightPadding: 16
        hoverEnabled: true

        enabled: !mainToolbar.modelLoading

        contentItem: Text {
            text: mainToolbar.modelLoading
                ? translator.text(
                    "toolbar.loading_model",
                    translator.language
                )
                : translator.text(
                    "toolbar.load_model",
                    translator.language
                )

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