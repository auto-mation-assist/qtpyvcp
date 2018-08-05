import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2

ApplicationWindow {
    visible: true
    width: 600
    height: 400
    title: qsTr("Dyn ATC")
    color: "whitesmoke"

    GridLayout {
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 9

        columns: 4
        rows: 4
        rowSpacing: 10
        columnSpacing: 10

        Text {
            text: qsTr("Angle")
        }

        // Input field of the first number
        TextField {
            id: firstNumber
        }

        Button {
            height: 40
            Layout.fillWidth: true
            text: qsTr("Do it")

            Layout.columnSpan: 2

            onClicked: {
                // Invoke the calculator slot to sum the numbers
                calculator.sum(firstNumber.text)
            }
        }
    }

    BorderImage {
        id: atc_holder
        x: 137
        y: 43
        width: 314
        height: 314
        rotation: 0
        transformOrigin: Item.Center
        source: "images/carousel_12.png"
    }

    // Here we take the result of sum or subtracting numbers
    Connections {
        target: calculator

        // Sum signal handler
        onSumResult: {
            // sum was set through arguments=['sum']
            atc_holder.rotation = sum
        }
    }
}