import QtQuick
import QtQuick.Controls

Dialog {
    id: sourceDialog

    property var sources: []
    property var additionalSources: []
    property var lessRelevantSources: []

    property bool showAdditionalSources: false

    property color surfaceColor
    property color textColor
    property color secondaryTextColor
    property color assistantBubbleColor
    property color hoverColor
    property color pressedColor
    property color accentColor

    signal knowledgeEntryRequested(int id)

    modal: true
    title: translator.text(
        "source_dialog.title",
        translator.language
    )

    ListModel {
        id: visibleSourcesModel
    }

    ListModel {
        id: filteredSourcesModel
    }

    function appendSources(sourceModel) {
        if (!sourceModel) {
            return
        }

        // QML ListModel
        if (sourceModel.count !== undefined && sourceModel.get) {
            for (let i = 0; i < sourceModel.count; i++) {
                visibleSourcesModel.append(sourceModel.get(i))
            }

            return
        }

        // Normal JavaScript array
        if (sourceModel.length !== undefined) {
            for (let i = 0; i < sourceModel.length; i++) {
                visibleSourcesModel.append(sourceModel[i])
            }
        }
    }

    function refreshVisibleSources() {
        visibleSourcesModel.clear()

        appendSources(sourceDialog.sources)

        if (sourceDialog.showAdditionalSources) {
            appendSources(sourceDialog.additionalSources)
        }

        filterSources()
    }

    function filterSources() {
        filteredSourcesModel.clear()

        const query = searchField.text.trim().toLowerCase()

        for (let i = 0; i < visibleSourcesModel.count; i++) {
            const item = visibleSourcesModel.get(i)

            const sourceText = item.source
                ? item.source.toLowerCase()
                : ""

            const contentText = item.text
                ? item.text.toLowerCase()
                : ""

            if (query === ""
                    || sourceText.includes(query)
                    || contentText.includes(query)) {

                filteredSourcesModel.append(item)
            }
        }
    }

    function hasAdditionalSources() {
        if (!sourceDialog.additionalSources) {
            return false
        }

        if (sourceDialog.additionalSources.count !== undefined) {
            return sourceDialog.additionalSources.count > 0
        }

        if (sourceDialog.additionalSources.length !== undefined) {
            return sourceDialog.additionalSources.length > 0
        }

        return false
    }

    onOpened: {
        searchField.clear()
        refreshVisibleSources()
    }

    onClosed: {
        showAdditionalSources = false
        searchField.clear()
        visibleSourcesModel.clear()
        filteredSourcesModel.clear()
    }

    header: Item {
        implicitHeight: 56

        Label {
            anchors.left: parent.left
            anchors.leftMargin: 16
            anchors.right: closeSourceButton.left
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter

            text: sourceDialog.title
            color: sourceDialog.textColor
            font.pixelSize: 18
            font.bold: true
            elide: Text.ElideRight
        }

        Button {
            id: closeSourceButton

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
                    color: sourceDialog.secondaryTextColor
                }

                Rectangle {
                    anchors.centerIn: parent
                    width: 14
                    height: 2
                    radius: 1
                    rotation: -45
                    color: sourceDialog.secondaryTextColor
                }
            }

            background: Rectangle {
                radius: 6

                color: closeSourceButton.down
                    ? sourceDialog.pressedColor
                    : closeSourceButton.hovered
                        ? sourceDialog.hoverColor
                        : "transparent"
            }

            onClicked: sourceDialog.close()
        }
    }

    background: Rectangle {
        color: sourceDialog.surfaceColor
        radius: 10
    }

    contentItem: Column {
        spacing: 12

        Label {
            id: sourceCountLabel

            width: parent.width

            text: searchField.text.trim() !== ""
                ? translator.text(
                    "source_dialog.showing",
                    translator.language
                )
                    + " "
                    + filteredSourcesModel.count
                    + " "
                    + translator.text(
                        "source_dialog.of",
                        translator.language
                    )
                    + " "
                    + visibleSourcesModel.count
                    + " "
                    + translator.text(
                        "source_dialog.source_entries",
                        translator.language
                    )
                : visibleSourcesModel.count === 1
                    ? translator.text(
                        "source_dialog.showing",
                        translator.language
                    )
                        + " 1 "
                        + translator.text(
                            "source_dialog.source_entry",
                            translator.language
                        )
                    : translator.text(
                        "source_dialog.showing",
                        translator.language
                    )
                        + " "
                        + visibleSourcesModel.count
                        + " "
                        + translator.text(
                            "source_dialog.source_entries",
                            translator.language
                        )

            color: sourceDialog.secondaryTextColor
            font.pixelSize: 12
        }

        TextField {
            id: searchField

            width: parent.width - 16
            height: 40

            placeholderText: translator.text(
                "source_dialog.search",
                translator.language
            )

            color: sourceDialog.textColor
            placeholderTextColor: sourceDialog.secondaryTextColor

            leftPadding: 12
            rightPadding: 12

            selectByMouse: true

            background: Rectangle {
                radius: 8

                color: sourceDialog.assistantBubbleColor

                border.color: searchField.activeFocus
                    ? sourceDialog.accentColor
                    : sourceDialog.secondaryTextColor

                border.width: searchField.activeFocus ? 1.5 : 1
            }

            onTextChanged: {
                sourceDialog.filterSources()
            }
        }

        ListView {
            id: sourceList

            width: parent.width

            height: parent.height
                - sourceCountLabel.height
                - searchField.height
                - (showMoreButton.visible
                    ? showMoreButton.height
                    : 0)
                - parent.spacing * (
                    showMoreButton.visible ? 3 : 2
                )

            model: filteredSourcesModel

            spacing: 12
            clip: true

            ScrollBar.vertical: ScrollBar {
                policy: ScrollBar.AsNeeded
                width: 14
            }

            delegate: Rectangle {
                id: sourceItem

                required property int id
                required property string source
                required property string text
                required property real score
                required property string created_at

                width: ListView.view.width
                    - (sourceList.ScrollBar.vertical.visible ? 16 : 0)

                height: contentColumn.implicitHeight + 20
                radius: 8

                color: sourceDialog.assistantBubbleColor

                TapHandler {
                    onTapped: {
                        sourceDialog.close()
                        sourceDialog.knowledgeEntryRequested(sourceItem.id)
                    }
                }

                Column {
                    id: contentColumn

                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.margins: 10
                    anchors.verticalCenter: parent.verticalCenter

                    spacing: 6

                    Row {
                        spacing: 10

                        Text {
                            text: sourceItem.source
                            color: sourceDialog.textColor
                            font.bold: true
                        }

                        Text {
                            text: sourceItem.created_at
                                .replace("T", " ")
                                .slice(0, 16)

                            color: sourceDialog.secondaryTextColor
                            font.pixelSize: 11
                        }
                    }

                    Text {
                        text: sourceItem.text
                        width: parent.width
                        wrapMode: Text.WordWrap
                        color: sourceDialog.textColor
                    }

                    Text {
                        text: translator.text(
                                "source_dialog.score",
                                translator.language
                            )
                            + ": "
                            + sourceItem.score.toFixed(3)
                        color: sourceDialog.secondaryTextColor
                        font.pixelSize: 11
                    }
                }
            }

            Label {
                anchors.centerIn: parent

                visible: searchField.text.trim() !== ""
                    && filteredSourcesModel.count === 0

                text: translator.text(
                    "source_dialog.no_search_results",
                    translator.language
                )
                color: sourceDialog.secondaryTextColor
                font.pixelSize: 13
            }
        }

        Button {
            id: showMoreButton

            anchors.horizontalCenter: parent.horizontalCenter

            height: 40
            leftPadding: 18
            rightPadding: 18
            hoverEnabled: true

            visible: sourceDialog.hasAdditionalSources()

            text: sourceDialog.showAdditionalSources
                ? translator.text(
                    "source_dialog.show_used_only",
                    translator.language
                )
                : translator.text(
                    "source_dialog.show_more_relevant",
                    translator.language
                )

            contentItem: Text {
                text: showMoreButton.text

                color: sourceDialog.textColor
                font.pixelSize: 13

                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            background: Rectangle {
                radius: 8

                color: showMoreButton.down
                    ? sourceDialog.pressedColor
                    : showMoreButton.hovered
                        ? sourceDialog.hoverColor
                        : sourceDialog.surfaceColor

                border.color: sourceDialog.accentColor
                border.width: 1
            }

            onClicked: {
                sourceDialog.showAdditionalSources =
                    !sourceDialog.showAdditionalSources

                sourceDialog.refreshVisibleSources()
            }
        }
    }
}