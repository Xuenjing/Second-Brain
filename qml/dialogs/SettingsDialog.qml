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

    signal themeToggleRequested()
    signal exportRequested()

    function setExportStatus(message) {
        exportStatus.text = message
    }

    function clearExportStatus() {
        exportStatus.text = ""
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
    
    

    contentItem: Column {
        spacing: 12

        Label {
            text: "Utseende"
            color: settingsDialog.textColor
            font.pixelSize: 16
            font.bold: true
        }
    }

    footer: Item {
        implicitHeight: 64

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

            Label {
                text: "Back-up"
                color: settingsDialog.textColor
                font.pixelSize: 16
                font.bold: true
            }

            Button {
                id: exportKnowledgeButton
                text: "Exportera databas"
                height: 40
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
                    settingsDialog.clearExportStatus()
                    settingsDialog.exportRequested()
                }
            }

            Label {
                id: exportStatus
                width: parent.width
                text: ""
                color: settingsDialog.textColor
                wrapMode: Text.WordWrap
            }

    }    

