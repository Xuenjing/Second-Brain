import QtQuick
import QtQuick.Controls

Dialog {
    id: helpDialog

    property color surfaceColor
    property color borderColor
    property color textColor
    property color secondaryTextColor
    property color accentColor
    property color hoverColor
    property color pressedColor

    title: "Användarguide"
    modal: true
    padding: 20
    closePolicy: Popup.CloseOnEscape

    background: Rectangle {
        color: helpDialog.surfaceColor
        radius: 12
        border.color: helpDialog.borderColor
        border.width: 1
    }

    header: Item {
        implicitHeight: 64

        Label {
            anchors.left: parent.left
            anchors.leftMargin: 20
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: closeButton.left
            anchors.rightMargin: 12

            text: helpDialog.title
            color: helpDialog.textColor
            font.pixelSize: 20
            font.bold: true
            elide: Text.ElideRight
        }

        Button {
            id: closeButton

            anchors.right: parent.right
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter

            width: 40
            height: 40
            hoverEnabled: true

            Accessible.name: "Stäng användarguiden"
            ToolTip.visible: hovered
            ToolTip.text: "Stäng"

            contentItem: Text {
                text: "×"
                color: helpDialog.secondaryTextColor
                font.pixelSize: 26
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            background: Rectangle {
                radius: 8
                color: closeButton.down
                    ? helpDialog.pressedColor
                    : closeButton.hovered
                        ? helpDialog.hoverColor
                        : "transparent"
            }

            onClicked: helpDialog.close()
        }
    }

    contentItem: ScrollView {
        id: guideScroll

        clip: true
        contentWidth: availableWidth

        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
        ScrollBar.vertical.policy: ScrollBar.AsNeeded

        Column {
            width: guideScroll.availableWidth - 20
            spacing: 24

            Label {
                width: parent.width
                text: "Second Brain hjälper dig att spara kunskap "
                    + "och ställa frågor om informationen."
                color: helpDialog.secondaryTextColor
                font.pixelSize: 14
                wrapMode: Text.WordWrap
                textFormat: Text.PlainText
            }

            Repeater {
                model: [
                    {
                        heading: "Lägg till kunskap",
                        body: "Öppna 'Lägg till kunskap'. Skriv eller "
                            + "klistra in information och klicka på "
                            + "disketten för att spara.\n\n"
                            + "Du kan också importera TXT-, PDF- och "
                            + "DOCX-filer med filknapparna, eller dra "
                            + "en fil till den markerade släppytan. "
                            + "Släpp en fil åt gången."
                    },
                    {
                        heading: "Importera och granska mejl",
                        body: "Importera en EML- eller MSG-fil med "
                            + "mejlknappen eller släpp den på släppytan. "
                            + "Mejlet visas för granskning före sparande.\n\n"
                            + "Du kan spara hela mejltexten eller låta "
                            + "AI:n föreslå fakta. Analysen använder "
                            + "den laddade språkmodellen och kan ta "
                            + "flera minuter.\n\n"
                            + "När analysen är klar öppnar du "
                            + "granskningen. Jämför förslagen med "
                            + "originalet, redigera vid behov och "
                            + "avmarkera sådant du inte vill spara. "
                            + "Spara de valda förslagen eller kasta "
                            + "granskningen. Ett mejl utan användbara "
                            + "fakta kan ge noll förslag."
                    },
                    {
                        heading: "Ställ frågor och granska källor",
                        body: "Skriv din fråga i chattfältet och "
                            + "klicka på Skicka. Vänta medan modellen "
                            + "arbetar.\n\n"
                            + "Öppna svarets källor för att granska "
                            + "kunskapsposterna som användes. Där kan "
                            + "du också söka och undersöka fler poster.\n\n"
                            + "AI:n kan missa eller misstolka "
                            + "information. Kontrollera viktiga "
                            + "uppgifter mot källorna."
                    },
                    {
                        heading: "Visa och hantera kunskap",
                        body: "Öppna Visa kunskap för att se sparade "
                            + "poster. Använd sökfältet och filtren "
                            + "för att hitta information.\n\n"
                            + "Antalet ovanför sökfältet visar hur "
                            + "många poster som matchar det aktuella "
                            + "urvalet. Använd pennan för att redigera "
                            + "en post och papperskorgen för att "
                            + "ta bort den."
                    },
                    {
                        heading: "Byt språkmodell",
                        body: "Välj en modell i modellistan och "
                            + "klicka på Ladda modell. Bekräfta "
                            + "modellbytet och vänta tills laddningen "
                            + "är klar.\n\n"
                            + "Första gången kan modellen behöva "
                            + "laddas ner. Tiden beror på modellens "
                            + "storlek och datorns prestanda."
                    },
                    {
                        heading: "Ändra RAG-inställningar",
                        body: "Öppna kugghjulet för inställningar.\n\n"
                            + "Top-K anger hur många kunskapsposter "
                            + "som högst väljs ut som underlag för "
                            + "ett svar.\n\n"
                            + "Threshold är likhetströskeln för "
                            + "urvalet, mellan 0 och 1. En högre "
                            + "tröskel gör urvalet striktare och kan "
                            + "ge färre träffar.\n\n"
                            + "Klicka på Spara RAG-inställningar för "
                            + "att spara ändringar. Återställ återgår "
                            + "till Top-K 5 och threshold 0.82. "
                            + "RAG-inställningarna finns kvar "
                            + "efter omstart."
                    },
                    {
                        heading: "Utseende och back-up",
                        body: "I inställningarna kan du växla mellan "
                            + "ljust och mörkt tema.\n\n"
                            + "Använd Exportera databas för att "
                            + "spara en säkerhetskopia som JSON-fil. "
                            + "Använd Importera databas för att "
                            + "läsa in en sådan fil."
                    },
                    {
                        heading: "Stäng och avsluta",
                        body: "När du stänger huvudfönstret fortsätter "
                            + "appen att köras i systemfältet vid "
                            + "klockan.\n\n"
                            + "Högerklicka på Second Brains ikon "
                            + "och välj Öppna för att visa fönstret "
                            + "igen, eller Avsluta för att "
                            + "stänga programmet helt."
                    }
                ]

                delegate: Column {
                    required property var modelData

                    width: parent.width
                    spacing: 8

                    Label {
                        width: parent.width
                        text: modelData.heading
                        color: helpDialog.accentColor
                        font.pixelSize: 17
                        font.bold: true
                        wrapMode: Text.WordWrap
                        textFormat: Text.PlainText
                    }

                    Label {
                        width: parent.width
                        text: modelData.body
                        color: helpDialog.textColor
                        font.pixelSize: 14
                        wrapMode: Text.WordWrap
                        textFormat: Text.PlainText
                    }
                }
            }
        }
    }
}