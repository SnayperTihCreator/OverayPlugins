// BatteryItem.qml
import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: root
    property int level: 50
    property bool charging: false
    property color borderColor: "white"
    property color fillColor: level > 20 ? "green" : "red"
    property color chargingColor: "yellow"

    width: 100
    height: 50

    Rectangle {
        id: batteryBody
        width: parent.width - 10
        height: parent.height
        color: "transparent"
        border.color: root.borderColor
        border.width: 2
        radius: 3

        Rectangle {
            id: batteryFill
            width: (parent.width - 4) * (root.level / 100)
            height: parent.height - 4
            anchors {
                left: parent.left
                top: parent.top
                margins: 2
            }
            color: root.charging ? root.chargingColor : root.fillColor
            radius: 1

            Behavior on width {
                NumberAnimation { duration: 300 }
            }
        }
    }

    Rectangle {
        id: batteryTip
        width: 5
        height: parent.height / 2
        anchors {
            left: batteryBody.right
            verticalCenter: parent.verticalCenter
        }
        color: root.borderColor
        radius: 2
    }

    Image {
        anchors.centerIn: batteryBody
        source: "qrc:/power_widget/icons/lightning.png"
        width: parent.width * 0.4
        height: parent.height * 0.4
        visible: root.charging
    }
}