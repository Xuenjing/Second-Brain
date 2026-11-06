import QtQuick
import QtQuick.Controls

Dialog {
    id: knowledgeDialog

    title: translator.text(
        "knowledge.add_title",
        translator.language
    )

    property color surfaceColor
    property color borderColor
    property color textColor
    property color secondaryTextColor
    property color accentColor
    property color hoverColor
    property color pressedColor
    property color windowColor
    property color assistantBubbleColor

    signal saveRequested(string text)
    signal txtImportRequested()
    signal docxImportRequested()
    signal pdfImportRequested()
    signal mailImportRequested()
    signal documentDropped(url fileUrl)

    function setSaveStatus(message) {
    knowledgeSaveStatus.text = message
    }

    function clearSaveStatus() {
        knowledgeSaveStatus.text = ""
    }    

    modal: true
    width: 800
    height: 480

    background: Rectangle {
        color: knowledgeDialog.surfaceColor
        radius: 12
        border.color: knowledgeDialog.borderColor
        border.width: 1
    }

    header: Item {
        implicitHeight: 56

        Label {
            anchors.left: parent.left
            anchors.leftMargin: 16
            anchors.right: closeKnowledgeButton.left
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter

            text: knowledgeDialog.title

            color: knowledgeDialog.textColor
            font.pixelSize: 18
            font.bold: true
            elide: Text.ElideRight
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

            Accessible.name: translator.text(
                "common.close",
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
                    color: knowledgeDialog.secondaryTextColor
                }

                Rectangle {
                    anchors.centerIn: parent
                    width: 14
                    height: 2
                    radius: 1
                    rotation: -45
                    color: knowledgeDialog.secondaryTextColor
                }
            }

            background: Rectangle {
                radius: 6

                color: closeKnowledgeButton.down
                    ? knowledgeDialog.pressedColor
                    : closeKnowledgeButton.hovered
                        ? knowledgeDialog.hoverColor
                        : "transparent"
            }

            onClicked: knowledgeDialog.close()
        }
    }

    contentItem: Column {
        spacing: 12

        Label {
            text: translator.text(
                "knowledge.input_label",
                translator.language
            )
            color: knowledgeDialog.textColor
        }

        ScrollView {
            width: parent.width
            height: 200

            TextArea {
                id: knowledgeInput

                placeholderText: translator.text(
                    "knowledge.input_placeholder",
                    translator.language
                )
                wrapMode: TextArea.Wrap
                textFormat: TextEdit.PlainText

                color: knowledgeDialog.textColor
                placeholderTextColor: knowledgeDialog.secondaryTextColor
                font.pixelSize: 14
                padding: 12

                background: Rectangle {
                    color: knowledgeDialog.assistantBubbleColor
                    radius: 8

                    border.color: knowledgeInput.activeFocus
                        ? knowledgeDialog.accentColor
                        : knowledgeDialog.borderColor

                    border.width: 1
                }
            }
        }

        Rectangle {
            width: parent.width
            height: 56
            radius: 8

            color: documentDropArea.containsDrag
                ? knowledgeDialog.hoverColor
                : knowledgeDialog.surfaceColor

            border.color: documentDropArea.containsDrag
                ? knowledgeDialog.accentColor
                : knowledgeDialog.borderColor

            border.width: documentDropArea.containsDrag ? 2 : 1

            Label {
                anchors.centerIn: parent

                text: documentDropArea.containsDrag
                    ? translator.text(
                        "knowledge.drop_here",
                        translator.language
                    )
                    : translator.text(
                        "knowledge.drop_files",
                        translator.language
                    )

                color: knowledgeDialog.textColor
            }

            DropArea {
                id: documentDropArea
                anchors.fill: parent

                onEntered: function(drag) {
                    drag.accepted = drag.hasUrls
                }

                onDropped: function(drop) {
                    if (!drop.hasUrls) {
                        return
                    }

                    if (drop.urls.length !== 1) {
                        knowledgeDialog.setSaveStatus(
                            "Släpp en fil åt gången."
                        )
                        return
                    }

                    const fileUrl = drop.urls[0]
                    const fileName = fileUrl.toString().toLowerCase()

                    if (!/\.(txt|pdf|docx|eml|msg)$/.test(fileName)) {
                        knowledgeDialog.setSaveStatus(
                            "Filtypen stöds inte. Välj TXT, PDF, DOCX, EML eller MSG."
                        )
                        return
                    }

                    // Accept copying the document into the knowledge base.
                    drop.accept(Qt.CopyAction)

                    knowledgeDialog.clearSaveStatus()
                    knowledgeDialog.documentDropped(fileUrl)
                }
            }
        }

        Row {
            spacing: 12

            Button {
                id: saveKnowledgeButton
                text: translator.text(
                    "common.save",
                    translator.language
                )
                width: 40
                height: 40
                hoverEnabled: true

                Accessible.name: translator.text(
                    "knowledge.save",
                    translator.language
                )
                ToolTip.visible: hovered
                ToolTip.text: translator.text(
                    "knowledge.save",
                    translator.language
                )

                contentItem: Item {
                    Rectangle {
                        anchors.centerIn: parent
                        width: 22
                        height: 22
                        radius: 3
                        color: knowledgeDialog.accentColor

                        Rectangle {
                            x: 5
                            y: 0
                            width: 12
                            height: 8
                            color: knowledgeDialog.surfaceColor

                            Rectangle {
                                x: 8
                                y: 1
                                width: 2
                                height: 5
                                color: knowledgeDialog.accentColor
                            }
                        }

                        Rectangle {
                            x: 4
                            y: 12
                            width: 14
                            height: 8
                            radius: 1
                            color: knowledgeDialog.surfaceColor
                        }
                    }
                }

                background: Rectangle {
                    radius: 8

                    color: saveKnowledgeButton.down
                        ? knowledgeDialog.pressedColor
                        : saveKnowledgeButton.hovered
                            ? knowledgeDialog.hoverColor
                            : knowledgeDialog.surfaceColor

                    border.color: knowledgeDialog.accentColor
                    border.width: 1
                }

                onClicked: {
                    knowledgeSaveStatus.text = ""
                    knowledgeDialog.saveRequested(knowledgeInput.text)
                }
            }

            Button {
                id: importFileButton
                width: 40
                height: 40
                hoverEnabled: true

                Accessible.name: translator.text(
                    "knowledge.import_txt",
                    translator.language
                )
                ToolTip.visible: hovered
                ToolTip.text: translator.text(
                    "knowledge.import_txt",
                    translator.language
                )

                contentItem: Item {
                    Item {
                        anchors.centerIn: parent
                        width: 24
                        height: 26

                        Canvas {
                            anchors.fill: parent

                            property color iconColor: knowledgeDialog.accentColor

                            onIconColorChanged: requestPaint()

                            onPaint: {
                                const ctx = getContext("2d")
                                ctx.clearRect(0, 0, width, height)
                                ctx.strokeStyle = iconColor
                                ctx.lineWidth = 1.8
                                ctx.lineJoin = "round"
                                ctx.lineCap = "round"

                                ctx.beginPath()
                                ctx.moveTo(6, 1)
                                ctx.lineTo(16, 1)
                                ctx.lineTo(23, 8)
                                ctx.lineTo(23, 25)
                                ctx.lineTo(6, 25)
                                ctx.closePath()
                                ctx.stroke()

                                ctx.beginPath()
                                ctx.moveTo(16, 1)
                                ctx.lineTo(16, 8)
                                ctx.lineTo(23, 8)
                                ctx.stroke()

                                ctx.beginPath()
                                ctx.moveTo(10, 18)
                                ctx.lineTo(19, 18)
                                ctx.moveTo(10, 21)
                                ctx.lineTo(19, 21)
                                ctx.stroke()
                            }
                        }

                        Rectangle {
                            x: 0
                            y: 8
                            width: 20
                            height: 10
                            radius: 2
                            color: knowledgeDialog.accentColor

                            Text {
                                anchors.centerIn: parent
                                text: "TXT"
                                font.pixelSize: 8
                                font.bold: true
                                color: knowledgeDialog.surfaceColor
                            }
                        }
                    }
                }

                background: Rectangle {
                    radius: 8

                    color: importFileButton.down
                        ? knowledgeDialog.pressedColor
                        : importFileButton.hovered
                            ? knowledgeDialog.hoverColor
                            : knowledgeDialog.surfaceColor

                    border.color: knowledgeDialog.accentColor
                    border.width: 1
                }

                onClicked: knowledgeDialog.txtImportRequested()
            }

            Button {
                id: importDocxButton
                width: 40
                height: 40
                hoverEnabled: true

                Accessible.name: translator.text(
                    "knowledge.import_docx",
                    translator.language
                )
                ToolTip.visible: hovered
                ToolTip.text: translator.text(
                    "knowledge.import_docx",
                    translator.language
                )

                contentItem: Item {
                    Item {
                        anchors.centerIn: parent
                        width: 24
                        height: 26

                        Canvas {
                            anchors.fill: parent

                            property color iconColor: knowledgeDialog.accentColor

                            onIconColorChanged: requestPaint()

                            onPaint: {
                                const ctx = getContext("2d")
                                ctx.clearRect(0, 0, width, height)
                                ctx.strokeStyle = iconColor
                                ctx.lineWidth = 1.8
                                ctx.lineJoin = "round"
                                ctx.lineCap = "round"

                                ctx.beginPath()
                                ctx.moveTo(6, 1)
                                ctx.lineTo(16, 1)
                                ctx.lineTo(23, 8)
                                ctx.lineTo(23, 25)
                                ctx.lineTo(6, 25)
                                ctx.closePath()
                                ctx.stroke()

                                ctx.beginPath()
                                ctx.moveTo(16, 1)
                                ctx.lineTo(16, 8)
                                ctx.lineTo(23, 8)
                                ctx.stroke()

                                ctx.beginPath()
                                ctx.moveTo(10, 18)
                                ctx.lineTo(19, 18)
                                ctx.moveTo(10, 21)
                                ctx.lineTo(19, 21)
                                ctx.stroke()
                            }
                        }

                        Rectangle {
                            x: 0
                            y: 8
                            width: 20
                            height: 10
                            radius: 2
                            color: knowledgeDialog.accentColor

                            Text {
                                anchors.centerIn: parent
                                text: "DOCX"
                                font.pixelSize: 7
                                font.bold: true
                                color: knowledgeDialog.surfaceColor
                            }
                        }
                    }
                }

                background: Rectangle {
                    radius: 8

                    color: importDocxButton.down
                        ? knowledgeDialog.pressedColor
                        : importDocxButton.hovered
                            ? knowledgeDialog.hoverColor
                            : knowledgeDialog.surfaceColor

                    border.color: knowledgeDialog.accentColor
                    border.width: 1
                }

                onClicked: knowledgeDialog.docxImportRequested()
            }

            Button {
                id: importPdfButton
                width: 40
                height: 40
                hoverEnabled: true

                Accessible.name: translator.text(
                    "knowledge.import_pdf",
                    translator.language
                )
                ToolTip.visible: hovered
                ToolTip.text: translator.text(
                    "knowledge.import_pdf",
                    translator.language
                )


                contentItem: Item {
                    Item {
                        anchors.centerIn: parent
                        width: 24
                        height: 26

                        Canvas {
                            anchors.fill: parent

                            property color iconColor: knowledgeDialog.accentColor

                            onIconColorChanged: requestPaint()

                            onPaint: {
                                const ctx = getContext("2d")
                                ctx.clearRect(0, 0, width, height)
                                ctx.strokeStyle = iconColor
                                ctx.lineWidth = 1.8
                                ctx.lineJoin = "round"
                                ctx.lineCap = "round"

                                ctx.beginPath()
                                ctx.moveTo(6, 1)
                                ctx.lineTo(16, 1)
                                ctx.lineTo(23, 8)
                                ctx.lineTo(23, 25)
                                ctx.lineTo(6, 25)
                                ctx.closePath()
                                ctx.stroke()

                                ctx.beginPath()
                                ctx.moveTo(16, 1)
                                ctx.lineTo(16, 8)
                                ctx.lineTo(23, 8)
                                ctx.stroke()

                                ctx.beginPath()
                                ctx.moveTo(10, 18)
                                ctx.lineTo(19, 18)
                                ctx.moveTo(10, 21)
                                ctx.lineTo(19, 21)
                                ctx.stroke()
                            }
                        }

                        Rectangle {
                            x: 0
                            y: 8
                            width: 20
                            height: 10
                            radius: 2
                            color: knowledgeDialog.accentColor

                            Text {
                                anchors.centerIn: parent
                                text: "PDF"
                                font.pixelSize: 8
                                font.bold: true
                                color: knowledgeDialog.surfaceColor
                            }
                        }
                    }
                }

                background: Rectangle {
                    radius: 8

                    color: importPdfButton.down
                        ? knowledgeDialog.pressedColor
                        : importPdfButton.hovered
                            ? knowledgeDialog.hoverColor
                            : knowledgeDialog.surfaceColor

                    border.color: knowledgeDialog.accentColor
                    border.width: 1
                }

                onClicked: knowledgeDialog.pdfImportRequested()
            }

            Button {
                id: importMailButton
                width: 40
                height: 40
                hoverEnabled: true

                Accessible.name: translator.text(
                    "knowledge.import_mail",
                    translator.language
                )
                ToolTip.visible: hovered
                ToolTip.text: translator.text(
                    "knowledge.import_mail",
                    translator.language
                )


                contentItem: Item {
                    Canvas {
                        anchors.centerIn: parent
                        width: 24
                        height: 20

                        property color iconColor: knowledgeDialog.accentColor

                        onIconColorChanged: requestPaint()

                        onPaint: {
                            const ctx = getContext("2d")
                            ctx.clearRect(0, 0, width, height)
                            ctx.strokeStyle = iconColor
                            ctx.lineWidth = 2
                            ctx.lineJoin = "round"
                            ctx.lineCap = "round"

                            ctx.beginPath()
                            ctx.moveTo(2, 2)
                            ctx.lineTo(22, 2)
                            ctx.lineTo(22, 18)
                            ctx.lineTo(2, 18)
                            ctx.closePath()
                            ctx.stroke()

                            ctx.beginPath()
                            ctx.moveTo(2, 18)
                            ctx.lineTo(9, 11)
                            ctx.moveTo(22, 18)
                            ctx.lineTo(15, 11)
                            ctx.stroke()

                            ctx.beginPath()
                            ctx.moveTo(2, 2)
                            ctx.lineTo(12, 12)
                            ctx.lineTo(22, 2)
                            ctx.stroke()
                        }
                    }
                }

                background: Rectangle {
                    radius: 8

                    color: importMailButton.down
                        ? knowledgeDialog.pressedColor
                        : importMailButton.hovered
                            ? knowledgeDialog.hoverColor
                            : knowledgeDialog.surfaceColor

                    border.color: knowledgeDialog.accentColor
                    border.width: 1
                }

                onClicked: {
                    knowledgeDialog.mailImportRequested()
                }
            }
        }

        Label {
            id: knowledgeSaveStatus
            width: parent.width
            text: ""
            color: knowledgeDialog.textColor
            wrapMode: Text.WordWrap
        }
    }
}