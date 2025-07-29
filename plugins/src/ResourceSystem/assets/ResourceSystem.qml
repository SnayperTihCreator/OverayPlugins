import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import QtQml 2.15

Item {
    id: root
    width: 300
    height: 100

    
    property real total_cpu: 0
    property real mem_total: 0
    

    Rectangle {
        anchors.fill: parent
        color: "#805f5f5f"
        radius: 10
    }

    ColumnLayout{
        anchors.fill: parent
        anchors.margins: 5

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true

            Text {
                text: "CPU: " + root.total_cpu.toFixed(2) + "%"
                color: mainTextColor
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            
            Text {
                text: "Current/MAX/MIN: " + current_speed_cpu + "/" + max_speed_cpu + "/" + min_speed_cpu + "MHz"
                color: mainTextColor
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true

            Text {
                text: "Total RAM " + root.mem_total.toFixed(2)+ "GB"
                color: mainTextColor
            }
            
        }



        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true

            Text {
                text: "Available RAM " + mem_available.toFixed(2) + "GB"
                color: mainTextColor
            }
        }




        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            
            Text {
                text: "Used RAM " + mem_used.toFixed(2) + "GB"
                color: mainTextColor
            }
        }




        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            
            Text {
                text: "Percentage usege RAM " + mem_percentage_usege.toFixed(2) + "%"
                color: mainTextColor
            }
        }
    }
}