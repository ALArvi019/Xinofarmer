Global $CBS_DROPDOWNLIST= 3
Global $ES_READONLY= 2048
Global $LBS_STANDARD= 10485763
$GUI_EVENT_CLOSE= -3

GUICreate("test", 200, 100)

$combo=GUICtrlCreateCombo("", 10, 10, 100, 80, BitOR($CBS_DROPDOWNLIST, $LBS_STANDARD))
GUICtrlSetData($combo,"item1|item2|item3", "item1")
GUISetState()

While 1
   $msg= GUIGetMsg()
  
   If $msg = $GUI_EVENT_CLOSE Then Exit
  
Wend
Exit