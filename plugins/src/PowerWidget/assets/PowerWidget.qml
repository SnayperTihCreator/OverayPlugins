// PowerWidget.qml
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: root
    property int powerLevel: 0
    property string timeLeft: ""
    property bool charging: false

    Rectangle {
        anchors.fill: parent
        color: alphaBaseColor
        radius: 10
    }

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        spacing: 10

        Item {
            Layout.fillHeight: true
            Layout.preferredWidth: 100

            BatteryItem {
                id: battery
                level: root.powerLevel
                charging: root.charging
                anchors.fill: parent
                anchors.margins: 5
            }
        }

        Item {
            Layout.fillHeight: true
            Layout.preferredWidth: 50

            Label {
                id: powerLabel
                text: powerLevel + "%"
                color: mainTextColor
                anchors.centerIn: parent
            }
        }

        Item {
            Layout.fillHeight: true
            Layout.fillWidth: true

            Label {
                id: timeLabel
                text: root.timeLeft
                color: mainTextColor
                anchors.centerIn: parent
            }
        }

        

        


        /*Rectangle {
            color: "#00f"
            Layout.fillHeight: true
            Layout.fillWidth: true 
        }

        BatteryItem {
            id: battery
            level: root.powerLevel
            Layout.preferredWidth: 50
            Layout.preferredHeight: 25
        }

        Label {
            id: powerLabel
            text: powerLevel + "%"
            color: "white"
            Layout.alignment: Qt.AlignVCenter
        }

        Label {
            id: timeLabel
            text: root.timeLeft
            color: "white"
            Layout.alignment: Qt.AlignVCenter
        }*/
    }
}