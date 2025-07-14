import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import QtQml 2.15

Item {
    id: root
    width: 300
    height: 100
    
    // Форматы из Python
    property string timeFormat: timeFormat
    property string dateFormat: dateFormat
    
    // Дни недели
    property var weekDays: [
        "Понедельник", "Вторник", "Среда", 
        "Четверг", "Пятница", "Суббота", "Воскресенье"
    ]
    
    // Текущее время и дата
    property variant currentDateTime: new Date()

    Rectangle {
        anchors.fill: parent
        color: "#805f5f5f"
        radius: 10
    }

    GridLayout{
        columns: 2  // два столбца
        rows: 2     // две строки
        anchors.fill: parent
        anchors.margins: 5

        Item{
            Layout.columnSpan: 2
            Layout.fillHeight: true
            Layout.fillWidth: true
            
            Text {
                id: timeLabel
                text: Qt.formatDateTime(currentDateTime, root.timeFormat)
                anchors.centerIn: parent
                color: mainTextColor
            }
        }

        Item{
            Layout.fillHeight: true
            Layout.fillWidth: true

            Text {
                id: weekdayLabel
                text: weekDays[currentDateTime.getDay() - 1]
                anchors.centerIn: parent
                color: mainTextColor
            }
        }

        Item{
            Layout.fillHeight: true
            Layout.fillWidth: true
            Text {
                id: dateLabel
                text: Qt.formatDateTime(currentDateTime, root.dateFormat)
                anchors.centerIn: parent
                color: mainTextColor
            }
        }
    }
}