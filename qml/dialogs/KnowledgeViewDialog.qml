import QtQuick
import QtQuick.Controls

Dialog {
    id: knowledgeViewDialog

    property color surfaceColor
    property color borderColor
    property color textColor
    property color secondaryTextColor
    property color accentColor
    property color hoverColor
    property color pressedColor
    property color windowColor

    property color dangerColor
    property color dangerBorderColor
    property color dangerHoverColor
    property color dangerPressedColor

    // Reusable document icon within this dialog.
    component DocumentIcon: Item {
        id: documentIcon

        property string label: ""
        property color iconColor
        property color labelColor

        implicitWidth: 24
        implicitHeight: 26

        Item {
            anchors.centerIn: parent
            width: 24
            height: 26

            Canvas {
                anchors.fill: parent

                property color iconColor: documentIcon.iconColor

                // Redraw when the theme or filter changes.
                onIconColorChanged: requestPaint()

                onPaint: {
                    const ctx = getContext("2d")
                    ctx.clearRect(0, 0, width, height)
                    ctx.strokeStyle = iconColor
                    ctx.lineWidth = 1.8
                    ctx.lineJoin = "round"
                    ctx.lineCap = "round"

                    // Document outline.
                    ctx.beginPath()
                    ctx.moveTo(6, 1)
                    ctx.lineTo(16, 1)
                    ctx.lineTo(23, 8)
                    ctx.lineTo(23, 25)
                    ctx.lineTo(6, 25)
                    ctx.closePath()
                    ctx.stroke()

                    // Folded corner.
                    ctx.beginPath()
                    ctx.moveTo(16, 1)
                    ctx.lineTo(16, 8)
                    ctx.lineTo(23, 8)
                    ctx.stroke()

                    // Text lines.
                    ctx.beginPath()
                    ctx.moveTo(10, 18)
                    ctx.lineTo(19, 18)
                    ctx.moveTo(10, 21)
                    ctx.lineTo(19, 21)
                    ctx.stroke()
                }
            }

            // File type label.
            Rectangle {
                x: 0
                y: 8
                width: 20
                height: 10
                radius: 2
                color: documentIcon.iconColor

                Text {
                    anchors.centerIn: parent
                    text: documentIcon.label
                    font.pixelSize: 7
                    font.bold: true
                    color: documentIcon.labelColor
                }
            }
        }
    }

    property bool txtFilterActive: true
    property bool docxFilterActive: true
    property bool pdfFilterActive: true
    property bool manualFilterActive: true
    property bool mailFilterActive: true

    property string sortOrder: "desc"

    signal refreshRequested(
        string searchText,
        string sortOrder,
        bool txtFilterActive,
        bool docxFilterActive,
        bool pdfFilterActive,
        bool manualFilterActive,
        bool mailFilterActive
    )

    
    signal editRequested(int id, string text)
    signal deleteRequested(int id, string text)

    function requestRefresh() {
        refreshRequested(
            knowledgeSearchField.text,
            sortOrder,
            txtFilterActive,
            docxFilterActive,
            pdfFilterActive,
            manualFilterActive,
            mailFilterActive
        )
    }

    function setPosts(posts) {
        knowledgeList.model = posts
    }    

    title: "Kunskapsbas"
    modal: true

    background: Rectangle {
        color: knowledgeViewDialog.surfaceColor
        radius: 12
        border.color: knowledgeViewDialog.borderColor
        border.width: 1
    }

    header: Item {
        implicitHeight: 56
     
    
        Label {
            text: knowledgeViewDialog.title
            color: knowledgeViewDialog.textColor
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
                    color: knowledgeViewDialog.secondaryTextColor
                }

                Rectangle {
                    anchors.centerIn: parent
                    width: 14
                    height: 2
                    radius: 1
                    rotation: -45
                    color: knowledgeViewDialog.secondaryTextColor
                }
            }

            background: Rectangle {
                radius: 6

                color: closeKnowledgeButton.down
                    ? knowledgeViewDialog.pressedColor
                    : closeKnowledgeButton.hovered
                        ? knowledgeViewDialog.hoverColor
                        : "transparent"
            }

            onClicked: knowledgeViewDialog.close()
        }
    }            

    contentItem: Item {
        TextField {
            id: knowledgeSearchField

            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right

            height: 44
            placeholderText: "Sök bland sparad kunskap"

            color: knowledgeViewDialog.textColor
            placeholderTextColor: knowledgeViewDialog.secondaryTextColor
            font.pixelSize: 14
            padding: 12

            background: Rectangle {
                color: knowledgeViewDialog.windowColor
                radius: 8

                border.color: knowledgeSearchField.activeFocus
                    ? knowledgeViewDialog.accentColor
                    : knowledgeViewDialog.borderColor

                border.width: 1
            }

            onTextEdited: {
                knowledgeViewDialog.requestRefresh()
            }
        }

        Row {
            id: sortButtons

            anchors.top: knowledgeSearchField.bottom
            anchors.topMargin: 6
            anchors.right: parent.right

            spacing: 30

            Row {
                id: filterButtons
                spacing: 6

                Button {
                    id: filterTxtButton
                    text: "TXT"
                    width: 40
                    height: 40
                    hoverEnabled: true

                    contentItem: DocumentIcon {
                        label: filterTxtButton.text
                        iconColor: knowledgeViewDialog.txtFilterActive
                            ? knowledgeViewDialog.accentColor
                            : knowledgeViewDialog.secondaryTextColor
                        labelColor: knowledgeViewDialog.surfaceColor
                    }

                    background: Rectangle {
                        radius: 8

                        color: filterTxtButton.down
                            ? knowledgeViewDialog.pressedColor
                            : knowledgeViewDialog.txtFilterActive
                                || filterTxtButton.hovered
                                ? knowledgeViewDialog.hoverColor
                                : knowledgeViewDialog.surfaceColor

                        border.color: knowledgeViewDialog.txtFilterActive
                            ? knowledgeViewDialog.accentColor
                            : knowledgeViewDialog.borderColor

                        border.width: 1
                    }

                    onClicked: {
                        knowledgeViewDialog.txtFilterActive =
                            !knowledgeViewDialog.txtFilterActive

                        knowledgeViewDialog.requestRefresh()
                    }

                    ToolTip.visible: hovered
                    ToolTip.text: "TXT-filer"
                }

                Button {
                    id: filterDocxButton
                    text: "DOCX"
                    width: 40
                    height: 40
                    hoverEnabled: true

                    contentItem: DocumentIcon {
                        label: filterDocxButton.text
                        iconColor: knowledgeViewDialog.docxFilterActive
                            ? knowledgeViewDialog.accentColor
                            : knowledgeViewDialog.secondaryTextColor
                        labelColor: knowledgeViewDialog.surfaceColor
                    }

                    background: Rectangle {
                        radius: 8

                        color: filterDocxButton.down
                            ? knowledgeViewDialog.pressedColor
                            : knowledgeViewDialog.docxFilterActive
                                || filterDocxButton.hovered
                                ? knowledgeViewDialog.hoverColor
                                : knowledgeViewDialog.surfaceColor

                        border.color: knowledgeViewDialog.docxFilterActive
                            ? knowledgeViewDialog.accentColor
                            : knowledgeViewDialog.borderColor

                        border.width: 1
                    }

                    onClicked: {
                        knowledgeViewDialog.docxFilterActive =
                            !knowledgeViewDialog.docxFilterActive

                        knowledgeViewDialog.requestRefresh()
                    }

                    ToolTip.visible: hovered
                    ToolTip.text: "DOCX-filer"
                }

                Button {
                    id: filterPdfButton
                    text: "PDF"
                    width: 40
                    height: 40
                    hoverEnabled: true

                    contentItem: DocumentIcon {
                        label: filterPdfButton.text
                        iconColor: knowledgeViewDialog.pdfFilterActive
                            ? knowledgeViewDialog.accentColor
                            : knowledgeViewDialog.secondaryTextColor
                        labelColor: knowledgeViewDialog.surfaceColor
                    }

                    background: Rectangle {
                        radius: 8

                        color: filterPdfButton.down
                            ? knowledgeViewDialog.pressedColor
                            : knowledgeViewDialog.pdfFilterActive
                                || filterPdfButton.hovered
                                ? knowledgeViewDialog.hoverColor
                                : knowledgeViewDialog.surfaceColor

                        border.color: knowledgeViewDialog.pdfFilterActive
                            ? knowledgeViewDialog.accentColor
                            : knowledgeViewDialog.borderColor

                        border.width: 1
                    }

                    onClicked: {
                        knowledgeViewDialog.pdfFilterActive =
                            !knowledgeViewDialog.pdfFilterActive

                        knowledgeViewDialog.requestRefresh()
                    }

                    ToolTip.visible: hovered
                    ToolTip.text: "PDF-filer"
                }

                // Filter imported emails.
                Button {
                    id: filterMailButton
                    width: 40
                    height: 40
                    hoverEnabled: true

                    Accessible.name: "Filtrera mejl"
                    ToolTip.visible: hovered
                    ToolTip.text: "Mejl (.eml och .msg)"

                    // Draw an envelope icon.
                    contentItem: Item {
                        Canvas {
                            anchors.centerIn: parent
                            width: 24
                            height: 20

                            property color iconColor:
                                knowledgeViewDialog.mailFilterActive
                                    ? knowledgeViewDialog.accentColor
                                    : knowledgeViewDialog.secondaryTextColor

                            // Redraw when the theme or filter changes.
                            onIconColorChanged: requestPaint()

                            onPaint: {
                                const ctx = getContext("2d")
                                ctx.clearRect(0, 0, width, height)
                                ctx.strokeStyle = iconColor
                                ctx.lineWidth = 2
                                ctx.lineJoin = "round"
                                ctx.lineCap = "round"

                                // Envelope outline.
                                ctx.beginPath()
                                ctx.moveTo(2, 2)
                                ctx.lineTo(22, 2)
                                ctx.lineTo(22, 18)
                                ctx.lineTo(2, 18)
                                ctx.closePath()
                                ctx.stroke()

                                // Lower folds.
                                ctx.beginPath()
                                ctx.moveTo(2, 18)
                                ctx.lineTo(9, 11)
                                ctx.moveTo(22, 18)
                                ctx.lineTo(15, 11)
                                ctx.stroke()

                                // Envelope flap.
                                ctx.beginPath()
                                ctx.moveTo(2, 2)
                                ctx.lineTo(12, 12)
                                ctx.lineTo(22, 2)
                                ctx.stroke()
                            }
                        }
                    }

                    // Highlight the button when the filter is active.
                    background: Rectangle {
                        radius: 8

                        color: filterMailButton.down
                            ? knowledgeViewDialog.pressedColor
                            : (knowledgeViewDialog.mailFilterActive
                                || filterMailButton.hovered)
                                ? knowledgeViewDialog.hoverColor
                                : knowledgeViewDialog.surfaceColor

                        border.color: knowledgeViewDialog.mailFilterActive
                            ? knowledgeViewDialog.accentColor
                            : knowledgeViewDialog.borderColor

                        border.width: 1
                    }

                    // Toggle the email filter and refresh the list.
                    onClicked: {
                        knowledgeViewDialog.mailFilterActive =
                            !knowledgeViewDialog.mailFilterActive

                        knowledgeViewDialog.requestRefresh()
                    }
                }

                Button {
                    id: filterManualButton
                    text: "M"
                    width: 40
                    height: 40
                    hoverEnabled: true
                    Accessible.name: "Filtrera manuella poster"

                    // Draw a document with a pencil for manual entries.
                    contentItem: Item {
                        Canvas {
                            anchors.centerIn: parent
                            width: 26
                            height: 26

                            property color iconColor:
                                knowledgeViewDialog.manualFilterActive
                                    ? knowledgeViewDialog.accentColor
                                    : knowledgeViewDialog.secondaryTextColor

                            // Redraw when the theme or filter changes.
                            onIconColorChanged: requestPaint()

                            onPaint: {
                                const ctx = getContext("2d")
                                ctx.clearRect(0, 0, width, height)
                                ctx.strokeStyle = iconColor
                                ctx.lineWidth = 1.8
                                ctx.lineJoin = "round"
                                ctx.lineCap = "round"

                                // Document outline.
                                ctx.beginPath()
                                ctx.moveTo(12, 24)
                                ctx.lineTo(3, 24)
                                ctx.lineTo(3, 2)
                                ctx.lineTo(14, 2)
                                ctx.lineTo(20, 8)
                                ctx.lineTo(20, 12)
                                ctx.stroke()

                                // Folded corner.
                                ctx.beginPath()
                                ctx.moveTo(14, 2)
                                ctx.lineTo(14, 8)
                                ctx.lineTo(20, 8)
                                ctx.stroke()

                                // Text lines.
                                ctx.beginPath()
                                ctx.moveTo(7, 12)
                                ctx.lineTo(14, 12)
                                ctx.moveTo(7, 16)
                                ctx.lineTo(12, 16)
                                ctx.stroke()

                                // Pencil body and pointed tip.
                                ctx.beginPath()
                                ctx.moveTo(13, 24)
                                ctx.lineTo(14, 19)
                                ctx.lineTo(22, 11)
                                ctx.lineTo(25, 14)
                                ctx.lineTo(17, 22)
                                ctx.closePath()
                                ctx.stroke()

                                // Pencil tip and end.
                                ctx.beginPath()
                                ctx.moveTo(14, 19)
                                ctx.lineTo(17, 22)
                                ctx.moveTo(20, 13)
                                ctx.lineTo(23, 16)
                                ctx.stroke()
                            }
                        }
                    }

                    background: Rectangle {
                        radius: 8

                        color: filterManualButton.down
                            ? knowledgeViewDialog.pressedColor
                            : knowledgeViewDialog.manualFilterActive
                                || filterManualButton.hovered
                                ? knowledgeViewDialog.hoverColor
                                : knowledgeViewDialog.surfaceColor

                        border.color: knowledgeViewDialog.manualFilterActive
                            ? knowledgeViewDialog.accentColor
                            : knowledgeViewDialog.borderColor

                        border.width: 1
                    }

                    onClicked: {
                        knowledgeViewDialog.manualFilterActive =
                            !knowledgeViewDialog.manualFilterActive

                        knowledgeViewDialog.requestRefresh()
                    }

                    ToolTip.visible: hovered
                    ToolTip.text: "Manuella poster"
                }
            }

            Row {
                id: dateSortButtons
                spacing: 6

                Button {
                    id: sortAscendingButton
                    width: 40
                    height: 40
                    hoverEnabled: true

                    contentItem: Text {
                        text: "↑"

                        color: knowledgeViewDialog.sortOrder === "asc"
                            ? knowledgeViewDialog.accentColor
                            : knowledgeViewDialog.secondaryTextColor

                        font.pixelSize: 20
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        radius: 8

                        color: sortAscendingButton.down
                            ? knowledgeViewDialog.pressedColor
                            : knowledgeViewDialog.sortOrder === "asc"
                                || sortAscendingButton.hovered
                                ? knowledgeViewDialog.hoverColor
                                : knowledgeViewDialog.surfaceColor

                        border.color: knowledgeViewDialog.sortOrder === "asc"
                            ? knowledgeViewDialog.accentColor
                            : knowledgeViewDialog.borderColor

                        border.width: 1
                    }

                    onClicked: {
                        knowledgeViewDialog.sortOrder = "asc"
                        knowledgeViewDialog.requestRefresh()
                    }

                    ToolTip.visible: hovered
                    ToolTip.text: "Äldst först"
                }

                Button {
                    id: sortDescendingButton
                    width: 40
                    height: 40
                    hoverEnabled: true

                    contentItem: Text {
                        text: "↓"

                        color: knowledgeViewDialog.sortOrder === "desc"
                            ? knowledgeViewDialog.accentColor
                            : knowledgeViewDialog.secondaryTextColor

                        font.pixelSize: 20
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        radius: 8

                        color: sortDescendingButton.down
                            ? knowledgeViewDialog.pressedColor
                            : knowledgeViewDialog.sortOrder === "desc"
                                || sortDescendingButton.hovered
                                ? knowledgeViewDialog.hoverColor
                                : knowledgeViewDialog.surfaceColor

                        border.color: knowledgeViewDialog.sortOrder === "desc"
                            ? knowledgeViewDialog.accentColor
                            : knowledgeViewDialog.borderColor

                        border.width: 1
                    }

                    onClicked: {
                        knowledgeViewDialog.sortOrder = "desc"
                        knowledgeViewDialog.requestRefresh()
                    }

                    ToolTip.visible: hovered
                    ToolTip.text: "Nyast först"
                }
            }
        }

        ListView {
            id: knowledgeList

            anchors.top: sortButtons.bottom
            anchors.topMargin: 6
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom

            clip: true
            spacing: 12
            model: []

            ScrollBar.vertical: ScrollBar {}

            delegate: Rectangle {
                id: postItem

                required property var modelData

                width: knowledgeList.width

                height: Math.max(
                    postContent.height,
                    postActions.height
                ) + 24

                color: knowledgeViewDialog.windowColor
                radius: 8

                Column {
                    id: postContent

                    x: 12
                    y: 12

                    width: parent.width - postActions.width - 36
                    spacing: 8

                    Label {
                        width: parent.width

                        text: postItem.modelData.text
                        textFormat: Text.PlainText
                        wrapMode: Text.WordWrap

                        color: knowledgeViewDialog.textColor
                    }

                    Label {
                        width: parent.width

                        text: "Källa: "
                            + postItem.modelData.source
                            + " | Skapad: "
                            + postItem.modelData.created_at

                        textFormat: Text.PlainText
                        wrapMode: Text.WordWrap

                        color: knowledgeViewDialog.secondaryTextColor
                        font.pixelSize: 12
                    }
                }

                Row {
                    id: postActions

                    spacing: 8

                    anchors.right: parent.right
                    anchors.rightMargin: 12
                    anchors.verticalCenter: parent.verticalCenter

                    Button {
                        id: editPostButton
                        text: "Redigera"
                        width: 40
                        height: 40
                        hoverEnabled: true

                        Accessible.name: "Redigera kunskapspost"
                        ToolTip.visible: hovered
                        ToolTip.text: "Redigera kunskapspost"

                        contentItem: Item {
                            Item {
                                anchors.centerIn: parent
                                width: 24
                                height: 24
                                rotation: 45

                                Rectangle {
                                    x: 9
                                    y: 5
                                    width: 6
                                    height: 13
                                    radius: 1
                                    color: knowledgeViewDialog.accentColor

                                    Rectangle {
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        y: 2
                                        width: 1
                                        height: 9
                                        color: knowledgeViewDialog.surfaceColor
                                    }
                                }

                                Rectangle {
                                    x: 9
                                    y: 1
                                    width: 6
                                    height: 3
                                    radius: 1
                                    color: knowledgeViewDialog.accentColor
                                }

                                Rectangle {
                                    x: 10
                                    y: 17
                                    width: 4
                                    height: 4
                                    rotation: 45
                                    color: knowledgeViewDialog.accentColor
                                }
                            }
                        }

                        background: Rectangle {
                            radius: 8

                            color: editPostButton.down
                                ? knowledgeViewDialog.pressedColor
                                : editPostButton.hovered
                                    ? knowledgeViewDialog.hoverColor
                                    : knowledgeViewDialog.surfaceColor

                            border.color: knowledgeViewDialog.accentColor
                            border.width: 1
                        }

                        onClicked: {
                            knowledgeViewDialog.editRequested(
                                postItem.modelData.id,
                                postItem.modelData.text
                            )
                        }
                    }

                    Button {
                        id: deletePostButton
                        text: "Ta bort"
                        width: 40
                        height: 40
                        hoverEnabled: true

                        Accessible.name: "Ta bort kunskapspost"
                        ToolTip.visible: hovered
                        ToolTip.text: "Ta bort kunskapspost"

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
                                    border.color: knowledgeViewDialog.dangerColor
                                    border.width: 2
                                }

                                Rectangle {
                                    x: 2
                                    y: 5
                                    width: 16
                                    height: 2
                                    radius: 1
                                    color: knowledgeViewDialog.dangerColor
                                }

                                Rectangle {
                                    x: 4
                                    y: 9
                                    width: 12
                                    height: 14
                                    radius: 2
                                    color: knowledgeViewDialog.dangerColor

                                    Repeater {
                                        model: 3

                                        Rectangle {
                                            required property int index

                                            x: 3 + index * 3
                                            y: 3
                                            width: 1
                                            height: 8
                                            radius: 0.5
                                            color: knowledgeViewDialog.surfaceColor
                                        }
                                    }
                                }
                            }
                        }

                        background: Rectangle {
                            radius: 8

                            color: deletePostButton.down
                                ? knowledgeViewDialog.dangerPressedColor
                                : deletePostButton.hovered
                                    ? knowledgeViewDialog.dangerHoverColor
                                    : knowledgeViewDialog.surfaceColor

                            border.color: knowledgeViewDialog.dangerBorderColor
                            border.width: 1
                        }

                        onClicked: {
                            knowledgeViewDialog.deleteRequested(
                                postItem.modelData.id,
                                postItem.modelData.text
                            )
                        }
                    }

                }
            }

            Label {
                anchors.centerIn: parent
                visible: knowledgeList.count === 0
                text: "Inga kunskapsposter att visa."
                color: knowledgeViewDialog.secondaryTextColor
            }
        }
        
    }

    footer: Item {
        implicitHeight: 64

    }

}