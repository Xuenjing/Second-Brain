/*
    Huvudvy för applikationen.

    QML används för användargränssnittet.
    Exempel på komponenter som kan bli aktuella:
    - TextArea
    - Button
    - ScrollView
    - Connections

    Layout och funktionalitet bestäms under projektet.
*/

import QtQuick
import QtQuick.Controls


// Appens huvudfönster.
ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "Second Brain"

// Tillfällig rubrik.
    Label {
        anchors.centerIn: parent
        text: "Second Brain"
        font.pixelSize: 32

    }

}