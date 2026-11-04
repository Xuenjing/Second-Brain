import QtQuick
import QtQuick.Controls

Dialog {
    id: settingsDialog

    property bool darkMode

    property color surfaceColor
    property color borderColor
    property color textColor
    property color secondaryTextColor
    property color accentColor
    property color hoverColor
    property color pressedColor
    property color successColor: "#22C55E"
    property color errorColor: "#EF4444"

    signal themeToggleRequested()
    signal exportRequested()
    signal importRequested()
    signal ragSettingsRequested(int topK, real similarityThreshold)
    signal ragSettingsLoadRequested()

    function setBackupStatus(message) {
        backupStatus.text = message
    }

    function clearBackupStatus() {
        backupStatus.text = ""
    }

    function showRagStatus(success, message) {
        ragStatus.text = message
        ragStatus.color = success
            ? settingsDialog.accentColor
            : settingsDialog.errorColor
    }

    function loadRagSettings(topK, similarityThreshold) {
        topKInput.value = topK
        thresholdInput.text = similarityThreshold.toFixed(2)
    }

    onOpened: {
        settingsDialog.ragSettingsLoadRequested()
    }

    onClosed: {
        ragStatus.text = ""
    }    

    title: "Inställningar"
    modal: true

    background: Rectangle {
        color: settingsDialog.surfaceColor
        radius: 12
        border.color: settingsDialog.borderColor
        border.width: 1
    }

    header: Item {
        implicitHeight: 56

        Label {
                text: settingsDialog.title
                color: settingsDialog.textColor
                font.pixelSize: 18
                font.bold: true
                padding: 16
        }

        Button {
            id: closeKnowledgeButton

            width: 28
            height: 28
            padding: 0
            hoverEnabled: true

            anchors.right: parent.right
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter

            Accessible.name: "Stäng"
            ToolTip.visible: hovered
            ToolTip.text: "Stäng"

            contentItem: Item {
                Rectangle {
                    anchors.centerIn: parent
                    width: 14
                    height: 2
                    radius: 1
                    rotation: 45
                    color: settingsDialog.secondaryTextColor
                }

                Rectangle {
                    anchors.centerIn: parent
                    width: 14
                    height: 2
                    radius: 1
                    rotation: -45
                    color: settingsDialog.secondaryTextColor
                }
            }

            background: Rectangle {
                radius: 6

                color: closeKnowledgeButton.down
                    ? settingsDialog.pressedColor
                    : closeKnowledgeButton.hovered
                        ? settingsDialog.hoverColor
                        : "transparent"
            }

            onClicked: settingsDialog.close()
        }        
                    
    }
    
    

        contentItem: ScrollView {
        clip: true

        Column {
            width: settingsDialog.availableWidth
            spacing: 16

            // Appearance
            Label {
                text: "Utseende"
                color: settingsDialog.textColor
                font.pixelSize: 16
                font.bold: true
            }

            Row {
                spacing: 12

                Label {
                    text: "Ljust"
                    anchors.verticalCenter: parent.verticalCenter

                    color: settingsDialog.darkMode
                        ? settingsDialog.secondaryTextColor
                        : settingsDialog.textColor

                    font.pixelSize: 14
                    font.bold: !settingsDialog.darkMode
                }

                Button {
                    id: themeToggle

                    width: 100
                    height: 36
                    padding: 0
                    hoverEnabled: true

                    Accessible.name: "Byt mellan ljust och mörkt läge"

                    ToolTip.visible: hovered
                    ToolTip.text: settingsDialog.darkMode
                        ? "Byt till ljust läge"
                        : "Byt till mörkt läge"

                    onClicked: settingsDialog.themeToggleRequested()

                    background: Rectangle {
                        radius: height / 2

                        color: settingsDialog.darkMode
                            ? "#0B1220"
                            : "#E2E8F0"

                        border.color: themeToggle.activeFocus
                            ? settingsDialog.accentColor
                            : settingsDialog.borderColor

                        border.width: 1

                        Rectangle {
                            width: 44
                            height: 28
                            y: 4
                            x: settingsDialog.darkMode ? 52 : 4
                            radius: height / 2

                            color: settingsDialog.darkMode
                                ? "#334155"
                                : "#FFFFFF"

                            Behavior on x {
                                NumberAnimation {
                                    duration: 180
                                    easing.type: Easing.InOutQuad
                                }
                            }
                        }
                    }

                    contentItem: Item {
                        Text {
                            width: parent.width / 2
                            height: parent.height
                            text: "\u263C"
                            font.pixelSize: 24

                            color: settingsDialog.darkMode
                                ? "#94A3B8"
                                : "#0F172A"

                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        Text {
                            x: parent.width / 2
                            width: parent.width / 2
                            height: parent.height
                            text: "\u263D"
                            font.pixelSize: 24

                            color: settingsDialog.darkMode
                                ? "#F1F5F9"
                                : "#64748B"

                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                    }
                }

                Label {
                    text: "Mörkt"
                    anchors.verticalCenter: parent.verticalCenter

                    color: settingsDialog.darkMode
                        ? settingsDialog.textColor
                        : settingsDialog.secondaryTextColor

                    font.pixelSize: 14
                    font.bold: settingsDialog.darkMode
                }
            }

            // RAG
            Label {
                text: "RAG-inställningar"
                color: settingsDialog.textColor
                font.pixelSize: 16
                font.bold: true
                topPadding: 8
            }

            Grid {
                columns: 2
                columnSpacing: 16
                rowSpacing: 12

                Label {
                    text: "Antal källor (Top-K)"
                    color: settingsDialog.textColor
                    font.pixelSize: 14
                }

            Item {
                id: topKInput

                property int value: 5
                property int from: 1
                property int to: 20

                width: 140
                height: 42

                Rectangle {
                    anchors.fill: parent
                    radius: 8
                    color: settingsDialog.surfaceColor
                    border.color: settingsDialog.borderColor
                    border.width: 1
                }

                Row {
                    anchors.fill: parent
                    spacing: 0

                    Rectangle {
                        id: decrementButton

                        width: 42
                        height: parent.height
                        radius: 8

                        color: decrementArea.pressed
                            ? settingsDialog.pressedColor
                            : decrementArea.containsMouse
                                ? settingsDialog.hoverColor
                                : "transparent"

                        Text {
                            anchors.centerIn: parent
                            text: "−"
                            color: settingsDialog.textColor
                            font.pixelSize: 24
                        }

                        MouseArea {
                            id: decrementArea
                            anchors.fill: parent
                            hoverEnabled: true

                            onClicked: {
                                if (topKInput.value > topKInput.from) {
                                    topKInput.value--
                                }
                            }
                        }
                    }

                    Rectangle {
                        width: topKInput.width - 84
                        height: parent.height
                        color: "transparent"

                        Text {
                            anchors.centerIn: parent
                            text: topKInput.value
                            color: settingsDialog.textColor
                            font.pixelSize: 15
                        }
                    }

                    Rectangle {
                        id: incrementButton

                        width: 42
                        height: parent.height
                        radius: 8

                        color: incrementArea.pressed
                            ? settingsDialog.pressedColor
                            : incrementArea.containsMouse
                                ? settingsDialog.hoverColor
                                : "transparent"

                        Text {
                            anchors.centerIn: parent
                            text: "+"
                            color: settingsDialog.textColor
                            font.pixelSize: 22
                        }

                        MouseArea {
                            id: incrementArea
                            anchors.fill: parent
                            hoverEnabled: true

                            onClicked: {
                                if (topKInput.value < topKInput.to) {
                                    topKInput.value++
                                }
                            }
                        }
                    }
                }
            }

                Label {
                    text: "Likhetströskel (Threshold)"
                    color: settingsDialog.textColor
                    font.pixelSize: 14
                }

                TextField {
                    id: thresholdInput

                    width: 120
                    text: "0.82"
                    color: settingsDialog.textColor

                    background: Rectangle {
                        radius: 6
                        color: settingsDialog.surfaceColor

                        border.color: thresholdInput.activeFocus
                            ? settingsDialog.accentColor
                            : settingsDialog.borderColor

                        border.width: 1
                    }
                }
            }

            Row {
                spacing: 12

                Button {
                    id: saveRagSettingsButton

                    text: "Spara RAG-inställningar"
                    height: 40
                    width: 180
                    leftPadding: 16
                    rightPadding: 16
                    hoverEnabled: true

                    contentItem: Text {
                        text: saveRagSettingsButton.text
                        color: settingsDialog.textColor
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    

                    background: Rectangle {
                        radius: 8

                        color: saveRagSettingsButton.down
                            ? settingsDialog.pressedColor
                            : saveRagSettingsButton.hovered
                                ? settingsDialog.hoverColor
                                : settingsDialog.surfaceColor

                        border.color: settingsDialog.accentColor
                        border.width: 1
                    }

                    // Normalize "," and ".".
                    onClicked: {
                        const normalizedThreshold =
                            thresholdInput.text.trim().replace(",", ".")

                        const thresholdValue = Number(normalizedThreshold)

                        if (normalizedThreshold === ""
                                || !Number.isFinite(thresholdValue)
                                || thresholdValue < 0
                                || thresholdValue > 1) {

                            settingsDialog.showRagStatus(
                                false,
                                "Threshold måste vara ett giltigt tal mellan 0 och 1."
                            )
                            return
                        }

                        settingsDialog.ragSettingsRequested(
                            topKInput.value,
                            thresholdValue
                        )
                    }
                }

                Button {
                    id: resetRagSettingsButton
                    text: "Återställ standard"
                    height: 40
                    width: 180
                    leftPadding: 16
                    rightPadding: 16
                    hoverEnabled: true

                    contentItem: Text {
                        text: resetRagSettingsButton.text
                        color: settingsDialog.textColor
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        radius: 8

                        color: resetRagSettingsButton.down
                            ? settingsDialog.pressedColor
                            : resetRagSettingsButton.hovered
                                ? settingsDialog.hoverColor
                                : settingsDialog.surfaceColor

                        border.color: settingsDialog.accentColor
                        border.width: 1
                    }                    

                    onClicked: {
                        topKInput.value = 5
                        thresholdInput.text = "0.82"

                        settingsDialog.ragSettingsRequested(
                            5,
                            0.82
                        )
                    }
                }
            }

            

            // Backup
            Label {
                text: "Back-up"
                color: settingsDialog.textColor
                font.pixelSize: 16
                font.bold: true
                topPadding: 8
            }

            Row {
                spacing: 12

                Button {
                    id: exportKnowledgeButton

                    text: "Exportera databas"
                    height: 40
                    width: 180
                    leftPadding: 16
                    rightPadding: 16
                    hoverEnabled: true

                    contentItem: Text {
                        text: exportKnowledgeButton.text
                        color: settingsDialog.textColor
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        radius: 8

                        color: exportKnowledgeButton.down
                            ? settingsDialog.pressedColor
                            : exportKnowledgeButton.hovered
                                ? settingsDialog.hoverColor
                                : settingsDialog.surfaceColor

                        border.color: settingsDialog.accentColor
                        border.width: 1
                    }

                    onClicked: {
                        settingsDialog.clearBackupStatus()
                        settingsDialog.exportRequested()
                    }
                }

                Button {
                    id: importKnowledgeButton

                    text: "Importera databas"
                    height: 40
                    width: 180
                    leftPadding: 16
                    rightPadding: 16
                    hoverEnabled: true

                    contentItem: Text {
                        text: importKnowledgeButton.text
                        color: settingsDialog.textColor
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        radius: 8

                        color: importKnowledgeButton.down
                            ? settingsDialog.pressedColor
                            : importKnowledgeButton.hovered
                                ? settingsDialog.hoverColor
                                : settingsDialog.surfaceColor

                        border.color: settingsDialog.accentColor
                        border.width: 1
                    }

                    onClicked: {
                        settingsDialog.clearBackupStatus()
                        settingsDialog.importRequested()
                    }
                }
            }

            Label {
                id: backupStatus

                width: parent.width
                text: ""
                color: settingsDialog.textColor
                wrapMode: Text.WordWrap
            }
        }
    }

    footer: Item {
        implicitHeight: ragStatus.text ? 52 : 24

        Label {
            id: ragStatus

            anchors {
                left: parent.left
                right: parent.right
                verticalCenter: parent.verticalCenter
                leftMargin: 16
                rightMargin: 16
            }

            text: ""
            color: settingsDialog.accentColor
            font.pixelSize: 13
            wrapMode: Text.WordWrap
        }
    }

}