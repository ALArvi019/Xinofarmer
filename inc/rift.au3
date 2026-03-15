Func GoRift()
	;~ Set $Setup_Main_VMName to active window
	WinActivate($Setup_Main_VMName)
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	Sleep(2000)
	Local $insideRift = False

	If CheckIfWeAreInTheRift() = True Then
		AddTextLog( "We are in the rift")
		InsideRift()
		Return
	EndIf

	;~ Check actual map
	Local $actualMap = GetMap()
	If $actualMap = -1 Then
		AddTextLog( "Traveling a known map before starting")
		GoToCorrectMap(0)
		Return
	EndIf

	Fight()

	Local $oJson = Json_Decode($JSON_runs)
	Local $mapName = Json_Get($oJson, '.maps[' & $actualMap & '].name')

	If $mapName <> 'westmarch' Then
		AddTextLog( "Not in westmarch")
		AddTextLog( "Going to westmarch")
		;~ Go to westmarch
		$positionOfArrayWestmarch = GetPositionOfMapInArray('westmarch')
		GoToCorrectMap($positionOfArrayWestmarch)
		Return
	EndIf

	;~ Go to rift
	AddTextLog( "Going to rift")
	GoToRift()
	Local $time = TimerInit()	
	While CheckIfWeAreInStep() = False Or CheckIfPositionContainsColor(703, 314, "0xE6CA10") = False
		Sleep(10000)	
		AddTextLog( "Waiting for arriving to rift")	
		;~ drag mouse from 104, 467 to 70, 433
		If CheckIfWeAreInStep() = True And TimerDiff($time) > 30000 Then
			MouseClickDrag("right", $windowPos[0] + 104, $windowPos[1] + 467, $windowPos[0] + 70, $windowPos[1] + 433)
			Sleep(1000)
		EndIf
		If TimerDiff($time) > 60000 Then
			AddTextLog( "Can't arrive to rift")
			Return
		EndIf
	WEnd	
	Send("{f}")
	sleep(2000)
	If CheckIfPositionContainsColor(403, 452, "0x5A1F0D") = True Then
		AddTextLog( "Get the diary reward")
		MouseClick("left", $windowPos[0] + 403, $windowPos[1] + 452)
		Sleep(1000)
	EndIf

	;~ check if actual screen is the rift
	AddTextLog( "Checking if we are in the rift")
	Local $time = TimerInit()
	While CheckIfPositionContainsColor(543, 491, "0x5D240D") = False And CheckIfPositionContainsColor(787, 503, "0x5B200C") = False And CheckIfPositionContainsColor(917, 62, "0x66260F") = False
		AddTextLog( "We are not in the rift menu")
		If TimerDiff($time) > 60000 Then
			AddTextLog( "Can't arrive to rift menu")
			Return
		EndIf
		Sleep(10000)
	WEnd

	;~ Enter in the rift
	AddTextLog( "Entering in the rift")
	;~ 831, 506
	MouseClick("left", $windowPos[0] + 831, $windowPos[1] + 506)
	Sleep(10000)
	InsideRift()
EndFunc

Func GoToRift()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	OpenMap()
	Sleep(2000)
	MouseMove($windowPos[0] + 485, $windowPos[1] + 275)
	Sleep(1000)
	_WinAPI_Keybd_Event(0x11, 0) ; CTRL Down
	MouseWheel("down", 200)
	Sleep(2000)
	While _IsPressed('11')
		ControlSend("", "", "", "text", 0)
		_WinAPI_Keybd_Event(0x11, 2) ; CTRL Up
		Sleep(200)
	WEnd
	MouseClickDrag("left", $windowPos[0] + 458, $windowPos[1] + 147, $windowPos[0] + 458, $windowPos[1] + 496)
	MouseClickDrag("left", $windowPos[0] + 458, $windowPos[1] + 147, $windowPos[0] + 458, $windowPos[1] + 496)
	MouseClickDrag("left", $windowPos[0] + 64, $windowPos[1] + 376, $windowPos[0] + 898, $windowPos[1] + 376)
	MouseClickDrag("left", $windowPos[0] + 64, $windowPos[1] + 376, $windowPos[0] + 898, $windowPos[1] + 376)
	Sleep(1000)
	;~ 846, 533
	MouseClick("left", $windowPos[0] + 846, $windowPos[1] + 533)
	Sleep(1000)
	FindAndClickTeleportOrNavigate()
	Sleep(1000)
	AvoidTeleport()
EndFunc

Func CheckIfWeAreInTheRift()
	If CheckIfPositionContainsColor(27, 177, "0x925BAB") = True Or CheckIfPositionContainsColor(28, 172, "0xA967C4") = True Or CheckIfPositionContainsColor(27, 177, "0x925CAC") = True Then
		AddTextLog( "We are in the rift")
		Return True
	EndIf
	Return False
EndFunc

Func InsideRift()
	;~ Set $Setup_Main_VMName to active window
	WinActivate($Setup_Main_VMName)
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)

	Local $time = TimerInit()
	While CheckIfWeAreInTheRift() = False
		AddTextLog( "We are not inside the rift")
		If TimerDiff($time) > 60000 Then
			AddTextLog( "you are inside the rift?")
			;~ 716, 137
			ExitToTheActualMap()
			Return
		EndIf
		Sleep(10000)
		CheckRiftModifiers()
	WEnd

	AddTextLog( "We are in the rift")
	If  CheckIfPositionContainsColor(29, 171, "0xAB71C7") = True Then
		AddTextLog( "Close left panel")
		;~ 260, 259
		MouseClick("left", $windowPos[0] + 260, $windowPos[1] + 259)
		Sleep(1000)
	EndIf

	AddTextLog( "Start rift")

	;~ drag and draw a crcle with the mouse in the position 119, 452
	MouseClickDrag("left", $windowPos[0] + 119, $windowPos[1] + 452, $windowPos[0] + 119, $windowPos[1] + 452)
	Sleep(1000)
	MouseClickDrag("left", $windowPos[0] + 119, $windowPos[1] + 452, $windowPos[0] + 119, $windowPos[1] + 452)
	Sleep(1000)

	;~ Check if the rift is ended
	While CheckIfPositionContainsColor(128, 171, "0x02EB28") = False
		Fight()
		MoveToNextPosition()
	WEnd

	;~ Go to sell
	;~ TODO

	;~ Exit The rift
	ExitToTheActualMap()
	Sleep(20000)

EndFunc

Func CheckRiftModifiers()
	If CheckIfPositionContainsColor(375, 501, "0x63240F") = True And CheckIfPositionContainsColor(599, 503, "0x5D240F") = True Then
		;~ click to avoid moifiers
		;~ 375, 501
		$windowPos = GetPositionOfWindow($Setup_Main_VMName)
		MouseClick("left", $windowPos[0] + 375, $windowPos[1] + 501)
		Sleep(1000)
	EndIf
EndFunc

Func OpenRiftMap()
	While CheckIfPositionContainsColor(914, 70, "0x592713") = False And CheckIfPositionContainsColor(915, 46, "0xB3673D") = False
		AddTextLog( "Open Map")
		Send("{m}")
		Sleep(300)
	WEnd
EndFunc

Func CloseRiftMap()
	While CheckIfPositionContainsColor(914, 70, "0x592713") = True And CheckIfPositionContainsColor(915, 46, "0xB3673D") = True
		AddTextLog( "Close Map")
		Send("{m}")
		Sleep(300)
	WEnd
EndFunc

Func MoveToNextPosition()
	CaptureMap()
	AddTextLog( "Move to next position")
EndFunc

Func CaptureMap()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	OpenRiftMap()
	_ScreenCapture_CaptureWnd(@TempDir & "\Rift_Map.jpg", $Setup_Main_VMName)
	CloseRiftMap()
	CropTheFile()
	processFile()
	Sleep(2000)
	;~ $position can be (0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)
	;~ AddTextLog( "Move to " & $position)
EndFunc

Func CropTheFile()
	;~ execute python file to crop the image
	;~ 746, 40
	;~ 910, 120
	;~ AddTextLog( "python " & @ScriptDir & "\inc\scripts\crop.py " & @TempDir & "\Rift_Map.jpg " & @TempDir & "\Rift_Map_Cropped.jpg 746 40 910 120")
	RunWait("python " & @ScriptDir & "\inc\scripts\crop.py " & @TempDir & "\Rift_Map.jpg " & @TempDir & "\Rift_Map_Cropped.jpg 28 47 900 545") 
EndFunc

Func processFile()
	;~ execute python file to process the image
	;~ AddTextLog( "python " & @ScriptDir & "\inc\scripts\process.py " & @TempDir & "\Rift_Map_Cropped.jpg " & @TempDir & "\Rift_Map_Processed.jpg")
	Local $test = RunWait("python " & @ScriptDir & "\inc\scripts\process.py " & @TempDir & "\Rift_Map_Cropped.jpg " & @TempDir & "\Rift_Map_Processed.jpg")
	AddTextLog( "result: " & $test)
EndFunc