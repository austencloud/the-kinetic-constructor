// Button.qml
import QtQuick 2.15
import QtQuick.Controls 2.15

Button {
    id: customButton
    text: 'Click Me'
    hoverEnabled: true

    // Normal state style
    background: Rectangle {
        color: customButton.hovered ? '#e0e0e0' : 'white'
        border.color: '#a0a0a0'
        radius: 25
    }

    // Pressed state style
    contentItem: Text {
        text: customButton.text
        font: customButton.font
        color: customButton.pressed ? '#c0c0c0' : '#000000'
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
}
