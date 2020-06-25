import QtQuick 2.0
import Mycroft 1.0 as Mycroft

//
// This is designed and built for a 7" screen, but should resize pretty well regardless of screensize.
// I doubt this would work very well on a Mark2 screen. :(
//
Mycroft.Delegate {
    id: root
    visible: true

    Item {
        id: item1
        property alias item1: item1
        BorderImage {
            id: borderImage
            x: 0
            y: 0
            width: 800
            height: 480
            z: -1
            source: "bg.png"
        }
    
        Image {
            id: image1
            x: 385
            y: 98
            width: 359
            height: 343
            z: 1
            source: "list.png"
    
            Text {
                id: listName
                x: 8
                y: 8
                width: 343
                height: 69
                text: sessionData.listName
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: 24
            }
        }
    
        Image {
            id: image
            x: 59
            y: 54
            width: 250
            height: 250
            source: "logo.jpg"
        }
    
        Text {
            id: text1
            x: 59
            y: 343
            width: 250
            height: 69
            text: qsTr("Todoist")
            font.bold: true
            font.family: "Verdana"
            horizontalAlignment: Text.AlignHCenter
            font.pixelSize: 45
        }
    
        Text {
            id: itemText
            x: 451
            y: 325
            text: sessionData.itemToAdd
            z: 2
            font.family: "Verdana"
            font.pixelSize: 17
        }
    
    
    
    }
}
