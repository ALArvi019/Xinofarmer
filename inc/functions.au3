Func Terminate()
	XF_2ndScript_CloseAndKill()
	ShowMsgBox("Terminating.", "Exit", $MB_SYSTEMMODAL, $hGUI)
    Exit
EndFunc

Func Start()
	;~ focus on the emulator window $Setup_Main_VMName
	WinActivate($Setup_Main_VMName)
	;~ create timer
	$XF_Timer = TimerInit()
	;~ hidde startButton and show stopButton 
	GUICtrlSetState(Eval("Button_start"), $GUI_HIDE)
	GUICtrlSetState(Eval("Button_stop"), $GUI_SHOW)
	If $isPaused = True Then
		$isPaused = False
	Else
		If $isStarted = False Then
			;~ start the script
			$isStarted = True
			Main()
		Else
			AddTextLog( "Script is already running.")
		EndIf
	EndIf
EndFunc

Func Pause()
	If $spotFarmRunning = True Or $endlessRunning = True  Or $dungeonRunning = True Or $fishingRunning = True Then
		$spotFarmRunning = False
		$endlessRunning = False
		$dungeonRunning = False
		$fishingRunning = False
		XF_2ndScript_Send("fromXF|stopfarmingspot|" & $Setup_Main_VMName, 20)
		XF_2ndScript_CheckIfScriptIsRunnung()
	EndIf
	If $isPaused = False Then
		$isPaused = True
		While 1
			Sleep(10)
			If $isPaused <> True Then
				ExitLoop
			EndIf
		WEnd
	EndIf
EndFunc

Func Stop()
	GUICtrlSetState(Eval("Button_stop"), $GUI_HIDE)
	GUICtrlSetState(Eval("Button_start"), $GUI_SHOW)
	Pause()
EndFunc

Func Save()
	OverWriteFileINI()
	ShowMsgBox("Configuration saved successfully.", "Save", $MB_SYSTEMMODAL, $hGUI)
EndFunc

Func HELP_Main_Player()
	HELPSHowInfo("image", '', @ScriptDir & "\inc\help\img\HelpPlayerSelect.jpg")
EndFunc

Func HELP_Fish_zones()
	HELPSHowInfo("image", '', @ScriptDir & "\inc\help\img\HelpFishV2.jpg")
EndFunc

Func HELPSHowInfo( $type = 'text', $text = '', $sImagePath = '')
	Switch $type
		Case "image"
			Local $sDestination = $sImagePath

			;~ get the size of the image
			_GDIPlus_Startup ()

			Local $hImage = _GDIPlus_ImageLoadFromFile($sDestination)
			If @error Then
				MsgBox(16, "Error", "Does the file exist?")
				XF_2ndScript_CloseAndKill()
				Exit 1
			EndIf

			Local $sOriginaWidth = _GDIPlus_ImageGetWidth($hImage)
			Local $sOriginaHeight = _GDIPlus_ImageGetHeight($hImage)

			_GDIPlus_ImageDispose ($hImage)

			_GDIPlus_ShutDown ()

			Local $sizeWidth = $sOriginaWidth
			Local $sizeHeight = $sOriginaHeight

			While @DesktopWidth < $sOriginaWidth Or @DesktopHeight < $sOriginaHeight
				$sizeWidth = $sOriginaWidth / 2
				$sizeHeight = $sOriginaHeight / 2
			WEnd


			SplashImageOn("Splash Screen", $sDestination, $sizeWidth, $sizeHeight,-1, -1, $DLG_NOTITLE)
			Sleep(5000)

			SplashOff()
		Case "text"
			MsgBox(0, "Help", $text)
			Return			
	EndSwitch
	
EndFunc

Func CheckProgramIsOpenByTitle($program)
	 If WinExists($program) Then
	   Return 1
	 Else
	   Return 0
	 EndIf
EndFunc

Func CheckProgramIsOpenByNameProcess($sProcessName)

	If ProcessExists($sProcessName) Then
		Return True
	Else
		Return False
	EndIf

EndFunc

Func AddTextLog($text, $color=False)
	;~ check if the $cEdit have more than 14000 characters, then clear the first 1000 lines
	If _GUICtrlRichEdit_GetLineCount($cEdit) > 14000 Then
		$allText = _GUICtrlRichEdit_GetText($cEdit)
		$allText = StringSplit($allText, @CRLF)
		$newText = ""
		For $i = 0 To UBound($allText) - 1
			If $i > 1000 Then
				$newText = $newText & $allText[$i] & @CRLF
			EndIf
		Next
		;~ delete the last @CRLF
		$newText = StringTrimRight($newText, 2)
		_GUICtrlRichEdit_SetText($cEdit, $newText)
		;~ remove variables
		$allText = ""
		$newText = ""
	EndIf
	_GUICtrlRichEdit_AppendText($cEdit, $text & @CRLF)
	dim $aColor[3]
	If $color = "red" Then
		$aColor[0] = 0xff
		$aColor[1] = 0x00
		$aColor[2] = 0x00
	ElseIf $color = "green" Then
		$aColor[0] = 0x41
		$aColor[1] = 0x7c
		$aColor[2] = 0x42
	ElseIf $color = "blue" Then
		$aColor[0] = 0x00
		$aColor[1] = 0x00
		$aColor[2] = 0xff
	ElseIf $color = "yellow" Then
		;~ c49f33
		$aColor[0] = 0xc4
		$aColor[1] = 0x9f
		$aColor[2] = 0x33
	ElseIf $color = "orange" Then
		$aColor[0] = 0xff
		$aColor[1] = 0x7f
		$aColor[2] = 0x00
	ElseIf $color = "purple" Then
		$aColor[0] = 0x7f
		$aColor[1] = 0x00
		$aColor[2] = 0x7f
	ElseIf $color = "pink" Then
		$aColor[0] = 0xff
		$aColor[1] = 0x00
		$aColor[2] = 0xff
	ElseIf $color = "brown" Then
		$aColor[0] = 0x7f
		$aColor[1] = 0x00
		$aColor[2] = 0x00
	Else
		$aColor[0] = 0x00
		$aColor[1] = 0x00
		$aColor[2] = 0x00
	EndIf
	$nColor = _ColorSetCOLORREF($aColor)
	;~ get the position of the first character of the last line
	$lastLine = _GUICtrlRichEdit_GetLineCount($cEdit)
	$lastLine = $lastLine - 1
	$firstChar = _GUICtrlRichEdit_GetFirstCharPosOnLine($cEdit, $lastLine)
	;~ select the last text position
	_GUICtrlRichEdit_SetSel($cEdit, $firstChar, -1)
	;~ change the color
	_GUICtrlRichEdit_SetCharColor($cEdit, $nColor)
	;~ desselect
	_GUICtrlRichEdit_Deselect($cEdit)
	
EndFunc

Func ShowMsgBox($text, $title, $type, $actualGui, $timeout = 0)
	WinSetOnTop($actualGui, "", 0)
	MsgBox($type, $title, $text, $timeout)
	WinSetOnTop($actualGui, "", 1)
EndFunc

Func Main()
	OverWriteFileINI()
	CheckingGUISetupParameters()
	AddTextLog( "Press F9 to terminate script.", "orange")
	AddTextLog( "VMName (LDPlayer windows name): " & $Setup_Main_VMName, "blue")
	AddTextLog( "Action: " & $Setup_Main_Action, "blue")

	Switch $Setup_Main_Action
		;~ Case "Farm"
		;~ 	AddTextLog( "FarmMap: " & $Setup_Farm_FarmMap)
		Case "Rift"
			Return			
		Case "Fish"
			AddTextLog( "FishType: " & $Setup_Fish_Fishtype, "blue")
			AddTextLog( "FishMap: " & $Setup_Fish_Maps, "blue")
		Case "Fish2.0"
			AddTextLog( "FishType: " & $Setup_Fish2_Fish2Type, "blue")
			AddTextLog( "IterationsMin: " & $Setup_Fish2_Fish2_IterMin, "blue")
			AddTextLog( "IterationsMax: " & $Setup_Fish2_Fish2_IterMax, "blue")
			AddTextLog( "FishMap: " & $Setup_Fish2_Maps, "blue")
			AddTextLog( "FishZone: " & $Setup_Fish2_Zones, "blue")
		Case "SpotFarm"
			AddTextLog( "SpotFarmMap: " & $Setup_SpotFarm_SpotFarmMap, "blue")
		Case "Dungeon"
			AddTextLog( "Dungeon: " & $Setup_Dungeon_name, "blue")
			AddTextLog( "Time to exit: " & $Setup_Dungeon_Time_to_exit & " (seconds)", "blue")
			AddTextLog( "Team/solo: " & $Setup_Dungeon_Team_solo, "blue")
		Case "Cyrangar"
			AddTextLog( "Cyrangar Mode: " & $Setup_Cyrangar_Mode, "blue")
			AddTextLog( "Cyrangar StayAtTheDoor: " & $Setup_Cyrangar_StayAtTheDoor, "blue")
			AddTextLog( "Cyrangar Time_to_exit: " & $Setup_Cyrangar_Time_to_exit, "blue")

	EndSwitch
	While 1
		;~ Check if the launcher is open
		AddTextLog( "Open the emulator")
		CheckIfEmulatorIsOpen()
		ExecuteMainGameLoop()
	WEnd
EndFunc

Func CheckingGUISetupParameters()
	Local $oJson = Json_Decode($JSON_setup)
	Local $SETOPJSON = Json_Get($oJson, '.setup')
	For $i = 0 To UBound($SETOPJSON) - 1 Step 1
		Local $SETOPJSON2 = Json_Get($oJson, '.setup[' & $i & '].values')
		For $j = 0 To UBound($SETOPJSON2) - 1 Step 1
			Local $iniGroup = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].iniGroup')
			Local $iniProp = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].iniProp')
			Local $GUILabel = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUILabel')
			Local $GUITypeField = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUITypeField')
			Local $GUIVariable = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUIVariable')
			Local $GUIValue = GUICtrlRead(Eval($GUIVariable))
			Switch $GUITypeField
				Case "text"
				Case "combo"
					If $GUIValue = "" Then
						If $iniGroup = "SpotFarm" And $iniProp = "SpotFarmCustomModelMap" Then
							$GUIValue = "Cementery"
						Else
							ShowMsgBox("The field " & $GUILabel & " is empty.", "Error", $MB_SYSTEMMODAL, $hGUI)
							Terminate()
						EndIf
					EndIf
				Case "textExplore"
					If $GUIValue = "" Then
						ShowMsgBox("The field " & $GUILabel & " is empty.", "Error", $MB_SYSTEMMODAL, $hGUI)
						Terminate()
					EndIf
					;~ check if the file exist
					If Not FileExists($GUIValue) Then
						ShowMsgBox("The file " & $GUIValue & " not exist.", "Error", $MB_SYSTEMMODAL, $hGUI)
						Terminate()
					EndIf
			EndSwitch
		Next
	Next
EndFunc

Func CapitalLetter($string)
	$firstChar = StringUpper(StringLeft($string, 1))
	$restOfString = StringMid($string, 2)
	Return $firstChar & $restOfString
EndFunc

Func game_main_screen()
	WinActivate($Setup_Main_VMName)
	;~ click in the center of the screen
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	;~ click in the center of the window
	MouseClick("left", $windowPos[0] + 480, $windowPos[1] + 277, 1, 0)
	;~ wait 5 seconds
	Sleep(5000)
EndFunc

Func game_blizzard_message_shit()
	;~ click in the center of the screen
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	MouseClick("left", $windowPos[0] + 448, $windowPos[1] + 356, 1, 0)
	;~ wait 5 seconds
	Sleep(5000)
EndFunc

Func game_blizz_support_web()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	;~ 922, 532
	MouseClick("left", $windowPos[0] + 922, $windowPos[1] + 532, 1, 0)
	;~ wait 5 seconds
	Sleep(5000)
EndFunc

Func game_blizzard_message_events()
	;~ click in the center of the screen
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	MouseClick("left", $windowPos[0] + 924, $windowPos[1] + 105, 1, 0)
	;~ wait 5 seconds
	Sleep(5000)
EndFunc

Func game_disconnect()
	;~ click in the center of the screen
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	MouseClick("left", $windowPos[0] + 459, $windowPos[1] + 352, 1, 0)
	;~ wait 5 seconds
	Sleep(5000)
EndFunc

Func game_fishing()
	;~ click in the center of the screen
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	executefishScript("Gold")
EndFunc

Func game_blizzard_message_local_events()
	;~ click in the center of the screen
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	MouseClick("left", $windowPos[0] + 889, $windowPos[1] + 121, 1, 0)
	;~ wait 5 seconds
	Sleep(5000)
EndFunc

Func game_select_character()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	
;~ 5 cases and default
	;~ 86, 92
	;~ 79, 197
	;~ 79, 296
	;~ 72, 383
	;~ 77, 477
	;~ MsgBox(0, "Select character", $Setup_Main_Player)
	Switch $Setup_Main_Player
		Case 1
			MouseClick("left", $windowPos[0] + 86, $windowPos[1] + 92, 1, 10)
		Case 2
			MouseClick("left", $windowPos[0] + 79, $windowPos[1] + 197, 1, 10)
		Case 3
			MouseClick("left", $windowPos[0] + 79, $windowPos[1] + 296, 1, 10)
		Case 4
			MouseClick("left", $windowPos[0] + 72, $windowPos[1] + 383, 1, 10)
		Case 5
			MouseClick("left", $windowPos[0] + 77, $windowPos[1] + 477, 1, 10)
		Case Else
			MouseClick("left", $windowPos[0] + 86, $windowPos[1] + 92, 1, 10)
	EndSwitch
	;~ wait 2 seconds
	Sleep(2000)
	MouseClick("left", $windowPos[0] + 795, $windowPos[1] + 526, 1, 10)
	;~ wait 5 seconds
	Sleep(10000)
EndFunc

Func game_any_open_screen_last_property()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	MouseClick("left", $windowPos[0] + 938, $windowPos[1] + 75)
	;~ wait 5 seconds
	Sleep(5000)
EndFunc

Func game_in_game()
	AddTextLog( "Game is running...")
	;~ left menu is open
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
;~ 	0xB71404
;~ 238, 179
	If $firstRun Then
		;~ turn OFF GPS
		MouseClick("left", $windowPos[0] + 599, $windowPos[1] + 163)
		;~ close left menu
		MouseClick("left", $windowPos[0] + 262, $windowPos[1] + 173)
		$firstRun = False
	EndIf

	Sleep(1000)
	Switch $Setup_Main_Action
		Case "Farm"
			GoFarm()
		Case "Rift"
			GoRift()
		Case "Fish"
			GoFish()
		Case "Fish2.0"
			GoFishNew()
		Case "SpotFarm"
			GoSpotFarm()
		Case "Dungeon"
			GoDungeon()
		Case "Cyrangar"
			GoCyrangar()
	EndSwitch
EndFunc

Func game_die()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	AddTextLog( "Player is dead...")
	;~ MouseClick("left", $windowPos[0] + 646, $windowPos[1] + 424)
	MouseClick("left", $windowPos[0] + 260, $windowPos[1] + 432)
EndFunc

Func special_event()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	AddTextLog( "Special event detected...")
	FinfImageAndClic("\game_items", "dungeon_special_event")
	$replay_dungeon = 'NO'
	Sleep(2000)
	MouseClick("left", $windowPos[0] + 713, $windowPos[1] + 134)
	Sleep(2000)
	MouseClick("left", $windowPos[0] + 576, $windowPos[1] + 357)
	Sleep(10000)
EndFunc

Func game_elder_rift()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	AddTextLog( "Close rift menu")
	;~ 931, 61
	MouseClick("left", $windowPos[0] + 931, $windowPos[1] + 61)
EndFunc

Func game_ldpayer_stuck()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	AddTextLog( "wait APP")
	;~ 880, 554
	MouseClick("left", $windowPos[0] + 335, $windowPos[1] + 397)
EndFunc

Func game_ldpayer_stuck2()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	AddTextLog( "wait APP")
	;~ 363, 292
	MouseClick("left", $windowPos[0] + 363, $windowPos[1] + 292)
EndFunc

Func CheckIfPositionContainsColor($x, $y, $color, $debug = 0, $tolerance = 3)
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	;~ get the color of the pixel inside window
	$pixelColor = PixelGetColor($x + $windowPos[0], $y + $windowPos[1], 0)
	;~ $pixelColor = "0x" & Hex(PixelGetColor($x + $windowPos[0], $y + $windowPos[1], 0), 6)
	If $debug = 1 Then
		AddTextLog( "----------------------------------------")
		AddTextLog( "Fullx: " & $x + $windowPos[0] & " Fully: " & $y + $windowPos[1])
		AddTextLog( "JSON color: " & Dec($color))
		AddTextLog( "Pixel color: " & $pixelColor)
		AddTextLog( "----------------------------------------")
	EndIf
	For $i = 0 To $tolerance
		$pixelToleranceplus = "0x" & Hex($pixelColor + $i, 6)
		$pixelToleranceminus = "0x" & Hex($pixelColor - $i, 6)
		If $debug = 1 Then
			AddTextLog( "Pixel JSON color: " & $color)
			AddTextLog( "Pixel color plus:   " & $pixelToleranceplus)
			AddTextLog( "Pixel color minus: " & $pixelToleranceminus)
		EndIf
		If $pixelToleranceplus = $color Then
			Return True
		EndIf
		If $pixelToleranceminus = $color Then
			Return True
		EndIf
	Next
	Return False
EndFunc

Func GetPositionOfWindow($windowTitle)
	;~ get handle for window
	$handle = WinGetHandle($windowTitle)
	;~ get the position of the window
	$windowPos = WinGetPos($handle)
	Return $windowPos
EndFunc

;====================================================================================
; Decode JSON from a given local file
;
; @param $jsonfilePath (string)
; @return $object (object), instance return by json_decode
;====================================================================================
Func json_decode_from_file($filePath)
    Local $fileOpen, $fileContent, $object
 
    $fileOpen = FileOpen($filePath, $FO_READ)
    If $fileOpen = -1 Then
        Return SetError(1, 0, "An error occurred when reading the file " & $filePath)
    EndIf
    $fileContent = FileRead($fileOpen)
    FileClose($fileOpen)
    $object = Json_Decode($fileContent)
 
    Return $object
EndFunc

Func _Send($text, $milliseconds)
    $time = TimerInit()
    Do
        Send($text)
		Sleep(500)
    Until TimerDiff($time) > $milliseconds
EndFunc

;~ IN GAME FUNCTIONS
Func GetMap()
	AddTextLog( "Checking map")
	;~ check if we are in the right map
	$oJson = Json_Decode($JSON_runs)
	Local $RUNJSON = Json_Get($oJson, '.maps')

	If OpenMap() = False Then
		Return
	EndIf
	Sleep(2000)

	Local $gameLanguage = TranslateLanguage($Setup_Main_Language)

	$MapFound = False
	For $i = 0 To UBound($RUNJSON) - 1 Step 1
		Local $mapname = Json_Get($oJson, '.maps[' & $i & '].name')
		$response = FindImageInScreen($mapname & '_' & $gameLanguage, $XF_image_folder & '\' & $gameLanguage & '\maps\')
		If $response[0] = False Then
			$MapFound = False
		Else
			$MapFound = True
		EndIf
		If $MapFound Then
			Send("{ESCAPE}")
			Sleep(2000)
			Return $i
		EndIf
	Next
	AddTextLog( "No map found")
	Send("{ESCAPE}")
	Sleep(2000)
	Return -1
EndFunc

Func TranslateLanguage($lang)
	Switch $lang
		Case "Spanish"
			Return "es"
		Case "English"
			Return "en"
	EndSwitch
EndFunc

Func GetPositionOfMapInArray($mapName)
	$oJson = Json_Decode($JSON_runs)
	Local $RUNJSON = Json_Get($oJson, '.maps')
	For $i = 0 To UBound($RUNJSON) - 1
		Local $mapNameTmp = Json_Get($oJson, '.maps[' & $i & '].name')
		If StringLower($mapNameTmp) = StringLower($mapName) Then
			Return $i
		EndIf
	Next
EndFunc

Func GoToCorrectMap($actualMapVar)
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	;~ Open map
	OpenMap()
	Sleep(2000)
	MouseClick("left", $windowPos[0] + 46, $windowPos[1] + 84)
	Sleep(2000)
	MouseMove($windowPos[0] + 485, $windowPos[1] + 275)
	Sleep(2000)
	WinActivate($Setup_Main_VMName)
	_WinAPI_Keybd_Event(0x11, 0) ; CTRL Down
	MouseWheel("down", 200)
	Sleep(2000)
	While _IsPressed('11')
		ControlSend("", "", "", "text", 0)
		_WinAPI_Keybd_Event(0x11, 2) ; CTRL Up
		Sleep(200)
	WEnd
	$oJson = Json_Decode($JSON_runs)
	Local $mapCoords_direction = Json_Get($oJson, '.maps[' & $actualMapVar & '].WorldMapCoords[0]')
	If $mapCoords_direction = "down" Then
		MouseClickDrag("left", $windowPos[0] + 458, $windowPos[1] + 496, $windowPos[0] + 458, $windowPos[1] + 147)
	Else
		MouseClickDrag("left", $windowPos[0] + 458, $windowPos[1] + 147, $windowPos[0] + 458, $windowPos[1] + 496)
	EndIf
	Sleep(2000)
	
	Local $mapCoords_x = Json_Get($oJson, '.maps[' & $actualMapVar & '].WorldMapCoords[1]')
	Local $mapCoords_y = Json_Get($oJson, '.maps[' & $actualMapVar & '].WorldMapCoords[2]')
	Local $mapSafeCoords_x = Json_Get($oJson, '.maps[' & $actualMapVar & '].SafeZone[0]')
	Local $mapSafeCoords_y = Json_Get($oJson, '.maps[' & $actualMapVar & '].SafeZone[1]')
	MouseClick("left", $windowPos[0] + $mapCoords_x, $windowPos[1] + $mapCoords_y)
	Sleep(2000)
	MouseClick("left", $windowPos[0] + $mapSafeCoords_x, $windowPos[1] + $mapSafeCoords_y)
	Sleep(2000)
	FindAndClickTeleportOrNavigate()
	Sleep(2000)
	Return
EndFunc

Func FindAndClickTeleportOrNavigate()
    Local $language = TranslateLanguage($Setup_Main_Language)
    Local $buttons[3] = ["navigate_" & $language, "teleport_" & $language]
	Local $windowPos = GetPositionOfWindow($Setup_Main_VMName)
	Local $last_scroll = False
	Local $win_position = 0

    For $i = 1 To 6
        For $j = 0 To UBound($buttons) - 1
            Local $response = FinfImageAndClic("\game_items", $buttons[$j])
            If $response Then
                Return True
            EndIf
        Next
		AddTextLog("No teleport or navigate found, try again (" & $i & "/6)") 
		MouseMove($windowPos[0] + 485, $windowPos[1] + 275)
		Sleep(2000)
		WinActivate($Setup_Main_VMName)
		If $last_scroll = False Then
			MouseWheel("down", 200)
			$last_scroll = 'down'
			$win_position = $win_position + 200
		ElseIf $last_scroll = 'down' And $win_position > 399 Then
			;~ go to initial position
			MouseWheel("up", $win_position + 200)
			$last_scroll = 'up'
			$win_position = 200
		ElseIf $last_scroll = 'up' And $win_position > 399 Then
			;~ go to initial position
			MouseWheel("down", $win_position + 200)
			$last_scroll = False
			$win_position = 0
		ElseIf $last_scroll = 'up' Then
			MouseWheel("up", 200)
			$last_scroll = 'up'
			$win_position = $win_position + 200
		ElseIf $last_scroll = 'down' Then
			MouseWheel("down", 200)
			$last_scroll = 'down'
			$win_position = $win_position + 200
		EndIf

			

		Sleep(2000)
    Next

    Return False
EndFunc

Func OpenMap()
	;~ open the map
	Local $count = 0
	While CheckIfPositionContainsColor(57, 78, "0x732709") = False And CheckIfPositionContainsColor(40, 306, "0x78423B") = False And CheckIfPositionContainsColor(945, 76, "0x7D3012") = False
		AddTextLog("Try to open map (" & $count & "/100)")
		If $count = 100 Then
			AddTextLog( "cannt open map " & $count)
			ExitToTheActualMap()
			Sleep(20000)
			Return False
		EndIf
		If $count = 4 And $Setup_Main_Action = "Rift" Then
			AddTextLog( "Exit to the actual map")
			ExitToTheActualMap()
			Sleep(20000)
			Return False
		EndIf
		$count = $count + 1
		Send("{m}")
		Sleep(500)
	WEnd
	Return True
EndFunc

Func OpenMapCyrangar()
	Local $count = 0
	While FindImageInScreen("close", $XF_image_folder & "\game_items")[0] = False
		If $count = 100 Then
			AddTextLog( "cannt open map " & $count)
			ExitToTheActualMap()
			Sleep(20000)
			Return False
		EndIf
		$count = $count + 1
		Send("{m}")
		Sleep(500)
	WEnd
EndFunc

Func ExitToTheActualMap()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	;~ 715, 137
	sleep(2000)
	MouseClick("left", $windowPos[0] + 715, $windowPos[1] + 137)
	sleep(2000)
	;~ 567, 357
	MouseClick("left", $windowPos[0] + 567, $windowPos[1] + 357)
	sleep(2000)
EndFunc

Func CheckIfWeAreInStep()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	Local $inStep = PixelSearch(290 + $windowPos[0], 152 + $windowPos[1], 690 + $windowPos[0], 181 + $windowPos[1], 0xEBD6AF, 1, 1)
	If $inStep <> 0 Then
		;~ AddTextLog( "We are not in the step")
		;~ check if we are in the middle of the step
		Local $inthemiddle = PixelSearch(353 + $windowPos[0], 363 + $windowPos[1], 707 + $windowPos[0], 407 + $windowPos[1], 0x572A23, 1, 1)
		If $inthemiddle <> 0 Then
			;~ AddTextLog( "We are in the middle of the step")
			MouseClick("left", $inthemiddle[0], $inthemiddle[1])
			AvoidTeleport()
		EndIf
		Fight()
		Return False
	Else
		If CheckIsDead() = True Then
			Return False
		EndIf
		AddTextLog( "We are in the step")
		Return True
	EndIf
EndFunc

Func waitForTheArrivalToSpot()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	Local $language = TranslateLanguage($Setup_Main_Language)
	Local $PositionOFBS_x = 0
	Local $PositionOFBS_y = 0
	Local $BSFoundIcon = False
	Local $Fails = 0
	$findImage = FindImageInScreen("navto_" & $language, $XF_image_folder & "\" & $language & "\farm")
    $aActualtime = TimerInit()
	While $findImage[0] = False And TimerDiff($aActualtime) < 150000
		AddTextLog( "Waiting to arrive to spot, time left: " & (150000 - TimerDiff($aActualtime)))
		Sleep(1000)
		$findImage = FindImageInScreen("navto_" & $language, $XF_image_folder & "\" & $language & "\farm")
		$findImage2 = FindImageInScreen("nav_arrow", $XF_image_folder & "\" & $language & "\farm")
		$BSFoundIcon = False
		If $findImage2[0] <> False Then
			$PositionOFBS_x = $findImage2[1]
			$PositionOFBS_y = $findImage2[2]
			$BSFoundIcon = True
		EndIf
		If $BSFoundIcon = True Then
			MouseClick("left",  $windowPos[0] + $PositionOFBS_x - 9, $windowPos[1] + $PositionOFBS_y - 5)
		EndIf
	WEnd
EndFunc

Func AvoidTeleport()
	Local $cont = 0
	;~  send s to avoid teleport and go walking
	;~ 342, 414
	;~ 612, 456
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	For $i = 0 To 10 Step 1
		;~ AddTextLog( "Send key to avoid teleport")
		Local $pixel = PixelSearch(342 + $windowPos[0], 414 + $windowPos[1], 612 + $windowPos[0], 456 + $windowPos[1], 0x0A7CD4, 1, 1)
		;~ AddTextLog( "Pixel: " & $pixel)
		If $pixel <> 0 Then
			Send("{s}")
		Else
			;~ sum 1 to cont
			$cont = $cont + 1
		EndIf
		If $cont = 3 Then
			ExitLoop
		EndIf
		Sleep(500)
	Next
EndFunc


;~ Fight life an loot----------------------------------------------->
Func Fight($step = 0, $lightFight = False)
	AvoidTeleport()
	CheckLife()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	$pixelMonster = PixelSearch($windowPos[0] + 116, $windowPos[1] + 90, $windowPos[0] + 731, $windowPos[1] + 540, 0xB10000, 1, 1)
	$pixelDamageInPlayer = PixelSearch($windowPos[0] + 388, $windowPos[1] + 201, $windowPos[0] + 571, $windowPos[1] + 352, 0xC70000, 1, 1)
	If $lightFight = True Then
		$tmpStep = $step
		$step = 3
	EndIf
	If $pixelMonster <> 0 Or $pixelDamageInPlayer <> 0 Then
		Switch $step
			Case 0
				AddTextLog( "Monster found")
				;~ Send 5
				Send("5")
				Send("k")
				Sleep(300)
				Send("l")
			Case 1
				Send("1")
				Sleep(300)
				Send("3")
			Case 3
				Send("k")
				Sleep(300)
				Send("l")
			Case 4
				Send("3")
				Sleep(300)
				Send("3")
				Sleep(200)
				Send("4")
			Case Else
				Send("k")
				Sleep(300)
				Send("l")
				$step = -1
		EndSwitch
		If $lightFight = True Then
			$step = $tmpStep
		EndIf
		if $step > 70 Then
			AddTextLog( "We are stuck in the fight")
			CheckIsDead()
			return True
		EndIf
		Fight($step + 1, $lightFight)
	Else
		;~ If $step > 0 And $step < 5 Then
			;~ Sleep(1000)
			;~ Fight($step + 1)
			CheckIsDead()
		;~ EndIf
	EndIf
	If $lightFight = False Then
		Loot()
	EndIf
EndFunc

Func CheckLife()
	;~ revisar la vida y si esta baja pulsar la tecla q para curarse
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	$pixelLife = PixelSearch($windowPos[0] + 23, $windowPos[1] + 104, $windowPos[0] + 61, $windowPos[1] + 111, 0x000000, 0, 1)
	$pixelLife2 = PixelSearch($windowPos[0] + 23, $windowPos[1] + 104, $windowPos[0] + 61, $windowPos[1] + 111, 0x4C1211, 0, 1)
	$pixelLife3 = PixelSearch($windowPos[0] + 23, $windowPos[1] + 104, $windowPos[0] + 61, $windowPos[1] + 111, 0x4B1211, 0, 1)
	$pixelLife4 = PixelSearch($windowPos[0] + 23, $windowPos[1] + 104, $windowPos[0] + 61, $windowPos[1] + 111, 0x45100F, 0, 1)
	If $pixelLife <> 0 Or $pixelLife2 <> 0 Or $pixelLife3 <> 0 Or $pixelLife4 <> 0 Then
		Send("{q}")
		Send("{q}")
		Send("{q}")
		Send("{q}")
		Send("{q}")
	EndIf
EndFunc

Func CheckLotPixels($type, $size)
 	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
 	Select
 		Case $size = 'small'
 			Local $x1 = $windowPos[0] + 184
 			Local $y1 = $windowPos[1] + 140
 			Local $x2 = $windowPos[0] + 707
 			Local $y2 = $windowPos[1] + 458
 		Case $size = 'big'
 			Local $x1 = $windowPos[0] + 110
 			Local $y1 = $windowPos[1] + 89
 			Local $x2 = $windowPos[0] + 832
 			Local $y2 = $windowPos[1] + 524
 	EndSelect
 	Select
 		Case $type = 'yellow'
 			return PixelSearch($x1, $y1, $x2, $y2, 0xF0EE4F, 1, 1)
 		Case $type = 'blue'
 			return PixelSearch($x1, $y1, $x2, $y2, 0x575EEC, 1, 1)
 		Case $type = 'gold'
 			return PixelSearch($x1, $y1, $x2, $y2, 0xDED390, 1, 1)
 		Case $type = 'gold2'
 			return PixelSearch($x1, $y1, $x2, $y2, 0xE6DF86, 1, 1)
 		Case $type = 'white'
 			return PixelSearch($x1, $y1, $x2, $y2, 0xFFFFFF, 1, 1)
 		Case $type = 'legendary'
 			return PixelSearch($x1, $y1, $x2, $y2, 0xF38F24, 1, 1)
 	EndSelect
EndFunc

Func FindLootNearPlayer()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	Local $PositionOFBS_x = 0
	Local $PositionOFBS_y = 0
	Local $BSFoundIcon = False
	Local $Fails = 0
	$findImage = FindImageInScreen("hand_down", $XF_image_folder & "\game_items")
	While $findImage[0] = False Or $Fails <= 4
		;~ AddTextLog($findImage[0])
		;~ AddTextLog($findImage[1])
		;~ AddTextLog($findImage[2])
		If $Fails > 4 Then
			AddTextLog( "Not found loot near the player")
			CheckIsDead()
			return True
		EndIf
		If $findImage[0] = False Then
			Sleep(1000)
			$Fails = $Fails + 1
		Else
			$PositionOFBS_x = $findImage[1]
			$PositionOFBS_y = $findImage[2]
			$BSFoundIcon = True
			MouseClick("left", $windowPos[0] + $PositionOFBS_x, $windowPos[1] + $PositionOFBS_y)
			Sleep(2000)
			$PositionOFBS_x = 0
			$PositionOFBS_y = 0
			$BSFoundIcon = False
			$Fails = 0
			$findImage = FindImageInScreen("hand_down", $XF_image_folder & "\game_items")
		EndIf
	WEnd
EndFunc

Func FinfImageAndClic($path, $file, $retries = 4, $threshold = 0.8, $x_diff = 0, $y_diff = 0)
    $windowPos = GetPositionOfWindow($Setup_Main_VMName)
    Local $PositionOFBS_x = 0
    Local $PositionOFBS_y = 0
    Local $BSFoundIcon = False
    Local $Fails = 0

    ; Realiza hasta $retries intentos de búsqueda de la imagen
    While $Fails <= $retries
        $findImage = FindImageInScreen($file, $XF_image_folder & $path, $threshold)

        If $findImage[0] = False Then
            ; Incrementa el contador de intentos fallidos
            $Fails += 1
            ; Espera 1 segundo antes de intentar nuevamente
            Sleep(1000)
        Else
            ; Si se encontró la imagen, realiza el clic
            $PositionOFBS_x = $findImage[1] + $x_diff
            $PositionOFBS_y = $findImage[2] + $y_diff
            $BSFoundIcon = True
            MouseClick("left", $windowPos[0] + $PositionOFBS_x, $windowPos[1] + $PositionOFBS_y)
            ; Espera 1 segundo después del clic 
            Sleep(1000)
            ExitLoop ; Sale del bucle una vez que se hizo el clic
        EndIf
    WEnd

    ; Si después de todos los intentos no se encontró la imagen, muestra un mensaje de error
    If Not $BSFoundIcon Then
        AddTextLog("Not found " & $file)
        CheckIsDead()
        Return False
    EndIf
	Return True
EndFunc


Func getReverseDirection($actualDIrection)
	Select
		Case $actualDIrection = "North"
			Return "South"
		Case $actualDIrection = "South"
			Return "North"
		Case $actualDIrection = "East"
			Return "West"
		Case $actualDIrection = "West"
			Return "East"
		Case $actualDIrection = "NorthEast"
			Return "SouthWest"
		Case $actualDIrection = "NorthWest"
			Return "SouthEast"
		Case $actualDIrection = "SouthEast"
			Return "NorthWest"
		Case $actualDIrection = "SouthWest"
			Return "NorthEast"
	EndSelect
EndFunc

Func NewLoot($step = 0)
	Fight(0, True)
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	;~ revisar si hay un cofre y si lo hay abrirlo
	;~ Local $pixelLootBlue = CheckLotPixels('blue', 'big')


	;~ get the loot near the player first 
	FindLootNearPlayer()
	Sleep(1000)


	$resp = FindLoot()

	$lootOrange = False
	$lootYellow = False
	$lootBlue = False
	$lootGold = False
	$lootEssence = False
	$lootGlobe = False
	$lootmonstrous_essence = False

	

	If $resp[0][0] <> False Then
		For $i = 0 To UBound($resp) - 1
			$typeOfLoot = $resp[$i][0]
			$loot_x = $resp[$i][1]
			$loot_y = $resp[$i][2]
			If $typeOfLoot = 'orange' Then
				$lootOrange = True
				$positionOrange = $i
			ElseIf $typeOfLoot = 'yellow' Then
				$lootYellow = True
				$positionYellow = $i
			ElseIf $typeOfLoot = 'blue' Then
				$lootBlue = True
				$positionBlue = $i
			ElseIf StringInStr($typeOfLoot, "gold_label_") Then
				$lootGold = True
				$positionGold = $i
			ElseIf StringInStr($typeOfLoot, "essence_label_") Then
				$lootEssence = True
				$positionEssence = $i
			ElseIf $typeOfLoot = 'monstrous_essence' Then
				$lootmonstrous_essence = True
				$positionmonstrous_essence = $i
			ElseIf StringInStr($typeOfLoot, "globe_label_") Then
				$lootGlobe = True
				$positionGlobe = $i
			EndIf
		Next
		Local $loot_x = 0
		Local $loot_y = 0
		Local $typeOfLoot = 0
		If $lootOrange = True Then
			AddTextLog( "Loot orange found " & $step)
			$loot_x = $resp[$positionOrange][1]
			$loot_y = $resp[$positionOrange][2]
			$typeOfLoot = 'orange'
		ElseIf $lootmonstrous_essence = True Then
			AddTextLog( "Loot monstrous_essence found " & $step)
			$loot_x = $resp[$positionmonstrous_essence][1]
			$loot_y = $resp[$positionmonstrous_essence][2]
			$typeOfLoot = 'monstrous_essence'
		ElseIf $lootYellow = True Then
			AddTextLog( "Loot yellow found " & $step)
			$loot_x = $resp[$positionYellow][1]
			$loot_y = $resp[$positionYellow][2]
			$typeOfLoot = 'yellow'
		ElseIf $lootEssence = True Then
			AddTextLog( "Loot essence found " & $step)
			$loot_x = $resp[$positionEssence][1]
			$loot_y = $resp[$positionEssence][2]
			$typeOfLoot = 'essence'
		ElseIf $lootBlue = True Then
			AddTextLog( "Loot blue found " & $step)
			$loot_x = $resp[$positionBlue][1]
			$loot_y = $resp[$positionBlue][2]
			$typeOfLoot = 'blue'
		ElseIf $lootGold = True Then
			AddTextLog( "Loot gold found " & $step)
			$loot_x = $resp[$positionGold][1]
			$loot_y = $resp[$positionGold][2]
			$typeOfLoot = 'gold'
		ElseIf $lootGlobe = True Then
			AddTextLog( "Loot globe found " & $step)
			$loot_x = $resp[$positionGlobe][1]
			$loot_y = $resp[$positionGlobe][2]
			$typeOfLoot = 'globe'
		EndIf

		If $loot_x <> 0 And $loot_y <> 0 Then
			Local $playerPosScreen_x = 480
			Local $playerPosScreen_y = 331
			;~ find out where the loot is in relation to the player's position (North, NorthEast, East, SouthEast, South, SouthWest, West, NorthWest)
			Local $lootPos = GetLootPosNew($loot_x, $loot_y, $playerPosScreen_x, $playerPosScreen_y)
			MovePlayerToLoot($lootPos)
			If $step = 50 Then
				AddTextLog( "Loot not found")
				Return
			EndIf
			If FindImageInScreen("hand_down", $XF_image_folder & "\game_items") <> False Then
				Send("{f}")
			EndIf
			Loot($step + 1)
		EndIf
	EndIf
EndFunc

Func Loot($step = 0)
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	;~ revisar si hay un cofre y si lo hay abrirlo
	Local $pixelLootBlue = CheckLotPixels('blue', 'big')
	Local $pixelLootYellow = CheckLotPixels('yellow', 'big')
	Local $pixelLootGold = CheckLotPixels('gold', 'big')
	Local $pixelLootGold2 = CheckLotPixels('gold2', 'big')
	;~ Local $pixelLootWhite = CheckLotPixels('white', 'small')
	Local $pixelLootWhite = 0 ;~ no loot white bug stuck
	Local $pixelLootLegendary = CheckLotPixels('legendary', 'big')

		
	Local $loot_x = 0
	Local $loot_y = 0
	Local $typeOfLoot = 0
	Select
		Case $pixelLootLegendary <> 0
			AddTextLog( "Loot legendary found " & $step)
			$loot_x = $pixelLootLegendary[0]
			$loot_y = $pixelLootLegendary[1]
			$typeOfLoot = 'legendary'
		Case $pixelLootYellow <> 0
			AddTextLog( "Loot yellow found " & $step)
			$loot_x = $pixelLootYellow[0]
			$loot_y = $pixelLootYellow[1]
			$typeOfLoot = 'yellow'
		Case $pixelLootBlue <> 0
			AddTextLog( "Loot blue found " & $step)
			$loot_x = $pixelLootBlue[0]
			$loot_y = $pixelLootBlue[1]
			$typeOfLoot = 'blue'
		Case $pixelLootWhite <> 0
			AddTextLog( "Loot white found " & $step)
			$loot_x = $pixelLootWhite[0]
			$loot_y = $pixelLootWhite[1]
			$typeOfLoot = 'white'
		Case $pixelLootGold <> 0
			AddTextLog( "Loot gold found " & $step)
			$loot_x = $pixelLootGold[0]
			$loot_y = $pixelLootGold[1]
			$typeOfLoot = 'gold'
		Case $pixelLootGold2 <> 0
			AddTextLog( "Loot gold found " & $step)
			$loot_x = $pixelLootGold2[0]
			$loot_y = $pixelLootGold2[1]
			$typeOfLoot = 'gold2'
		
	EndSelect
	If $loot_x <> 0 And $loot_y <> 0 Then
		Local $playerPosScreen_x = $windowPos[0] + 489
		Local $playerPosScreen_y = $windowPos[1] + 324
		;~ find out where the loot is in relation to the player's position (North, NorthEast, East, SouthEast, South, SouthWest, West, NorthWest)
		Local $lootPos = GetLootPos($loot_x, $loot_y, $playerPosScreen_x, $playerPosScreen_y)
		AddTextLog( "Loot position: " & $lootPos)
		Local $size = 'big'
		If $typeOfLoot = 'white' Then
			$size = 'small'
		EndIf
		If CheckLotPixels($typeOfLoot, $size) <> 0 Then
			;~ move the player to the loot
			MovePlayerToLoot($lootPos)
			Sleep(800)
		EndIf
		If $step = 50 Then
			AddTextLog( "Loot not found")
			Return
		EndIf
		If CheckIfPositionContainsColor(706, 308, "0xEBD311") = True And CheckIfPositionContainsColor(713, 301, "0xB88E08") = True Then
			Send("{f}")
		EndIf
		Loot($step + 1)
	EndIf
EndFunc
Func MovePlayerToLoot($lootPos)
	;~ move the player to the loot
	Local $speed = 10
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	Select
		Case $lootPos = "NorthWest"
			MouseClickDrag("right", $windowPos[0] + 100, $windowPos[1] + 470, $windowPos[0] + 50, $windowPos[1] + 420, $speed)
			Sleep(100)
		Case $lootPos = "North"
			MouseClickDrag("right", $windowPos[0] + 100, $windowPos[1] + 470, $windowPos[0] + 100, $windowPos[1] + 420, $speed)
			Sleep(100)
		Case $lootPos = "NorthEast"
			MouseClickDrag("right", $windowPos[0] + 100, $windowPos[1] + 470, $windowPos[0] + 150, $windowPos[1] + 420, $speed)
			Sleep(100)
		Case $lootPos = "East"
			MouseClickDrag("right", $windowPos[0] + 100, $windowPos[1] + 470, $windowPos[0] + 150, $windowPos[1] + 470, $speed)
			Sleep(100)
		Case $lootPos = "SouthEast"
			MouseClickDrag("right", $windowPos[0] + 100, $windowPos[1] + 470, $windowPos[0] + 150, $windowPos[1] + 520, $speed)
			Sleep(100)
		Case $lootPos = "South"
			MouseClickDrag("right", $windowPos[0] + 100, $windowPos[1] + 470, $windowPos[0] + 100, $windowPos[1] + 520, $speed)
			Sleep(100)
		Case $lootPos = "SouthWest"
			MouseClickDrag("right", $windowPos[0] + 100, $windowPos[1] + 470, $windowPos[0] + 50, $windowPos[1] + 520, $speed)
			Sleep(100)
		Case $lootPos = "West"
			MouseClickDrag("right", $windowPos[0] + 100, $windowPos[1] + 470, $windowPos[0] + 50, $windowPos[1] + 470, $speed)
			Sleep(100)
	EndSelect
EndFunc

Func GetLootPosNew($lootPos_x, $lootPos_y, $playerPos_x, $playerPos_y)
    Local $diff_x = $lootPos_x - $playerPos_x
    Local $diff_y = $lootPos_y - $playerPos_y
    Local $direction
    
    If $diff_x > 0 Then
        If $diff_y > 0 Then
            $direction = "SouthEast"
        ElseIf $diff_y < 0 Then
            $direction = "NorthEast"
        Else
            $direction = "East"
        EndIf
    ElseIf $diff_x < 0 Then
        If $diff_y > 0 Then
            $direction = "SouthWest"
        ElseIf $diff_y < 0 Then
            $direction = "NorthWest"
        Else
            $direction = "West"
        EndIf
    Else
        If $diff_y > 0 Then
            $direction = "South"
        ElseIf $diff_y < 0 Then
            $direction = "North"
        Else
            $direction = "North"
        EndIf
    EndIf
    Return $direction
EndFunc

Func GetLootPos($lootPos_x, $lootPos_y, $playerPos_x, $playerPos_y)
	;~ find out where the loot is in relation to the player's position (North, NorthEast, East, SouthEast, South, SouthWest, West, NorthWest)
	Local $lootPos = ""
	If $lootPos_x < $playerPos_x And $lootPos_y < $playerPos_y Then
		$lootPos = "NorthWest"
	ElseIf $lootPos_x = $playerPos_x And $lootPos_y < $playerPos_y Then
		$lootPos = "North"
	ElseIf $lootPos_x > $playerPos_x And $lootPos_y < $playerPos_y Then
		$lootPos = "NorthEast"
	ElseIf $lootPos_x > $playerPos_x And $lootPos_y = $playerPos_y Then
		$lootPos = "East"
	ElseIf $lootPos_x > $playerPos_x And $lootPos_y > $playerPos_y Then
		$lootPos = "SouthEast"
	ElseIf $lootPos_x = $playerPos_x And $lootPos_y > $playerPos_y Then
		$lootPos = "South"
	ElseIf $lootPos_x < $playerPos_x And $lootPos_y > $playerPos_y Then
		$lootPos = "SouthWest"
	ElseIf $lootPos_x < $playerPos_x And $lootPos_y = $playerPos_y Then
		$lootPos = "West"
	EndIf
	Return $lootPos
EndFunc

Func MoveRandom($numberOfMovements = 1, $movements = "NorthWest|North|NorthEast|East|SouthEast|South|SouthWest|West")
	Local $validMovements = StringSplit($movements, "|")
	;~ check if $validMovements[0] is empty
	If $validMovements[0] = "" Then
		dim $validMovements[0]
		$validMovements[0] = $movements
	EndIf
	For $i = 1 To $numberOfMovements
		$windowPos = GetPositionOfWindow($Setup_Main_VMName)
		Local $speed = 10
		Local $random = Random(1, $validMovements[0])
		$random = Int($random)
		Select
			Case $validMovements[$random] = "NorthWest"
				MouseClickDrag("right", $windowPos[0] + 100, $windowPos[1] + 470, $windowPos[0] + 50, $windowPos[1] + 420, $speed)
				Sleep(100)
			Case $validMovements[$random] = "North"
				MouseClickDrag("right", $windowPos[0] + 100, $windowPos[1] + 470, $windowPos[0] + 100, $windowPos[1] + 420, $speed)
				Sleep(100)
			Case $validMovements[$random] = "NorthEast"
				MouseClickDrag("right", $windowPos[0] + 100, $windowPos[1] + 470, $windowPos[0] + 150, $windowPos[1] + 420, $speed)
				Sleep(100)
			Case $validMovements[$random] = "East"
				MouseClickDrag("right", $windowPos[0] + 100, $windowPos[1] + 470, $windowPos[0] + 150, $windowPos[1] + 470, $speed)
				Sleep(100)
			Case $validMovements[$random] = "SouthEast"
				MouseClickDrag("right", $windowPos[0] + 100, $windowPos[1] + 470, $windowPos[0] + 150, $windowPos[1] + 520, $speed)
				Sleep(100)
			Case $validMovements[$random] = "South"
				MouseClickDrag("right", $windowPos[0] + 100, $windowPos[1] + 470, $windowPos[0] + 100, $windowPos[1] + 520, $speed)
				Sleep(100)
			Case $validMovements[$random] = "SouthWest"
				MouseClickDrag("right", $windowPos[0] + 100, $windowPos[1] + 470, $windowPos[0] + 50, $windowPos[1] + 520, $speed)
				Sleep(100)
			Case $validMovements[$random] = "West"
				MouseClickDrag("right", $windowPos[0] + 100, $windowPos[1] + 470, $windowPos[0] + 50, $windowPos[1] + 470, $speed)
				Sleep(100)
		EndSelect
	Next
EndFunc



Func CheckInventory($isCyrangar = False)
	;~ check if we have space in inventory
	;~ if not, go to inventory and sell items
	;~ if yes, continue
	Send("{b}")
	;~ countdown 10 seconds
	$countdown = 10
	While ( true )
		AddTextLog( "Checking inventory in " & $countdown & " seconds")
		$countdown = $countdown - 1
		If $countdown = 0 Then
			ExitLoop
		EndIf
		Sleep(1000)
	WEnd
	If CheckIfPositionContainsColor(678, 514, "0x422F25") Then
		AddTextLog( "Inventory not full, continuing")
		;~ continue
		Send("{ESC}")
		Sleep(1000)
	Else
		AddTextLog( "Inventory is full")
		$windowPos = GetPositionOfWindow($Setup_Main_VMName)
		;~ close inventory
		Send("{ESC}")
		Sleep(1000)
		If $isCyrangar Then
			AddTextLog( "Going to sell items to cyrangar blacksmith")
			OpenMapCyrangar()
			Sleep(1000)
			If FinfImageAndClic("\mapLegend", "essence_cyrangar", 4, 0.8, 8, -0.7) = False Then
				AddTextLog( "Blacksmith not found")
				CheckIsDead()
				return True
			EndIf
			Sleep(1000)
			FindAndClickTeleportOrNavigate()
			AddTextLog( "Going to sell items")
		Else
			If $Setup_Main_IHavePetWithBlacksmith = "Yes" Then
				AddTextLog("Using pet to sell items")
			Else
				;~ Open map
				OpenMap()
				Sleep(1000)
				;~ click on the glass
				MouseClick("left", $windowPos[0] + 41, $windowPos[1] + 309)
				Sleep(1000)
				;~ move mouse in the itemList
				MouseMove($windowPos[0] + 119, $windowPos[1] + 223)
				Sleep(1000)
				
				Local $PositionOFBS_x = 0
				Local $PositionOFBS_y = 0
				Local $BSFoundIcon = False
				Local $Fails = 0
				While $BSFoundIcon = False
					If $Fails > 4 Then
						AddTextLog( "We are stuck in the blacksmith")
						CheckIsDead()
						return True
					EndIf
					$findImage = FindImageInScreen("blacksmith", $XF_image_folder & "\mapLegend")
					If $findImage[0] = False Then
						MouseWheel("down", 1)
						Sleep(1000)
						$Fails = $Fails + 1
					Else
						$PositionOFBS_x = $findImage[1]
						$PositionOFBS_y = $findImage[2]
						$BSFoundIcon = True
					EndIf
				WEnd
				;~ MsgBox(0, "Blacksmith", "Blacksmith found at " & $PositionOFBS_x & " " & $PositionOFBS_y)
				;~ click on the blacksmithss
				MouseClick("left",$windowPos[0] + $PositionOFBS_x, $windowPos[1] + $PositionOFBS_y)
				Sleep(2000)
				;~ click on the teleport button
				FindAndClickTeleportOrNavigate()
			EndIf
		EndIf
		If $Setup_Main_IHavePetWithBlacksmith = "Yes" And $isCyrangar = False Then
			Send("{b}")
			Sleep(5000)
			Local $response = FinfImageAndClic("\game_items", "pet_icon")
            If $response Then
                Local $response = FinfImageAndClic("\game_items", "pet_recycle")
				If $response Then 
					Sleep(2000)
					MouseClick("left", $windowPos[0] + 822, $windowPos[1] + 525)
					Sleep(1000)
					MouseClick("left", $windowPos[0] + 870, $windowPos[1] + 525)
					Sleep(1000)
					MouseClick("left", $windowPos[0] + 925, $windowPos[1] + 525)
					Sleep(3000)
					MouseClick("left", $windowPos[0] + 296, $windowPos[1] + 505)
					Sleep(3000)
					Send("{ESC}")
					Sleep(1000)
				Else
					AddTextLog( "Pet recycle not found1")
					CheckIsDead()
					return True
				EndIf
			Else
				AddTextLog( "We are stuck in pet blacksmith")
				CheckIsDead()
				return True
            EndIf
		Else
			;~ for while 15 seconds
			$aActualtime = TimerInit()
			While TimerDiff($aActualtime) < 15000
				Sleep(1000)
					AddTextLog("Seconds to arrive to blacksmith: " & Round((15000 - TimerDiff($aActualtime)) / 1000))
			WEnd
			If $isCyrangar Then
				MoveRandom(2, "South")
			EndIf
			Local $count = 0
			While CheckIfWeAreInStep() = False Or FindImageInScreen("talk", $XF_image_folder & "\game_items")[0] = False
				AddTextLog( "Waiting to arrive to blacksmith")
				Sleep(300)
				$count = $count + 1
				If $count = 100 Then
					AddTextLog( "We are stuck in the blacksmith")
					CheckIsDead()
					return True
					ExitLoop
				EndIf
			WEnd
			;~ click on the blacksmith
			Send("f")
			Sleep(3000)
			;~ click on services
			MouseClick("left", $windowPos[0] + 731, $windowPos[1] + 374)
			Sleep(2000)
			If FindImageInScreen("bs_button3_en", $XF_image_folder & "\en\blacksmith")[0] <> False Then
				;~ click on sell items
				MouseClick("left", $windowPos[0] + 394, $windowPos[1] + 519)
				Sleep(1000)
				;~ # YESS ALL --->
					MouseClick("left", $windowPos[0] + 528, $windowPos[1] + 357)
					Sleep(1000)
				;~ # ---->
				MouseClick("left", $windowPos[0] + 440, $windowPos[1] + 520)
				Sleep(1000)
				;~ # YESS ALL --->
					MouseClick("left", $windowPos[0] + 528, $windowPos[1] + 357)
					Sleep(1000)
				;~ # ---->
				MouseClick("left", $windowPos[0] + 482, $windowPos[1] + 519)
				Sleep(1000)
				;~ # YESS ALL --->
					MouseClick("left", $windowPos[0] + 528, $windowPos[1] + 357)
					Sleep(1000)
				;~ # ---->
			EndIf
			MouseClick("left", $windowPos[0] + 640, $windowPos[1] + 510)
			Send("{ESC}")
			Sleep(1000)
		EndIf
	EndIf
EndFunc


Func FindImageInScreen($templateImage, $imageFolder = '', $threshold = 0.8, $gray="True")
	If $imageFolder = '' Then
		$imageFolder = $XF_image_folder
	Else
		$imageFolder = $imageFolder
	EndIf
	;~ AddTextLog("fromXF|findimage|" & $Setup_Main_VMName & "|" & $XF_image_folder & "|" & $templateImage & "|" & $threshold)
	Local $response = XF_2ndScript_Send("fromXF|findimage|" & $Setup_Main_VMName & "|" & $imageFolder & "|" & $templateImage & "|" & $threshold & "|" & $gray)

	$oJsonGood = ProcessScriptResponse($response)

	$foundImage = False
	For $i = 0 To Json_ObjGetKeys($oJsonGood) - 1
		$key = Json_ObjGetKeys($oJsonGood)[$i]
		$value = Json_ObjGet($oJsonGood, Json_ObjGetKeys($oJsonGood)[$i])
		If $value <> "notfound" Then
			$foundImage = True
		EndIf
	Next

	If $foundImage = False Then
		Dim $aResponse[1]
		$aResponse[0] = False
		Return $aResponse
	EndIf

	If Json_ObjGetCount($oJsonGood) = 1 Then
		Local $aResponse = StringSplit(Json_ObjGet($oJsonGood, Json_ObjGetKeys($oJsonGood)[0]), "|")
	Else
		Local $aResponse[Json_ObjGetCount($oJsonGood)]
		For $i = 0 To Json_ObjGetKeys($oJsonGood) - 1
			$aResponse[$i] = Json_ObjGet($oJsonGood, Json_ObjGetKeys($oJsonGood)[$i])
		Next
	EndIf

	return $aResponse
EndFunc

Func FindLoot($templateImage = '')
	Local $language = TranslateLanguage($Setup_Main_Language)
	Local $imageFolder = $XF_image_folder & "\" & $language & "\loot_items"
	If $templateImage = '' Then
		$templateImage = "None"
	Else
		$templateImage = $templateImage
	EndIf
	Local $response = XF_2ndScript_Send("fromXF|findloot|" & $Setup_Main_VMName & "|" & $imageFolder & "|" & $templateImage)
	;~ $response = "{'orange': [(399, 112), (411, 96), (390, 85)],'yellow': [(610, 139), (626, 139)]}"
	;~ $response = "notfound"
	;~ MsgBox(0, "response", $response)

	$oJsonGood = ProcessScriptResponse($response)
	
	$foundImage = False
	Dim $aResponse[Json_ObjGetCount($oJsonGood)][3]
	For $i = 0 To UBound(Json_ObjGetKeys($oJsonGood)) - 1
		$key = Json_ObjGetKeys($oJsonGood)[$i]
		$value = Json_ObjGet($oJsonGood, Json_ObjGetKeys($oJsonGood)[$i])
		If $value <> "notfound" Then
			$foundImage = True
		EndIf
	Next

	If $foundImage = False Then
		Dim $aResponse[1][1]
		$aResponse[0][0] = False
		Return $aResponse
	EndIf

	For $i = 0 To UBound(Json_ObjGetKeys($oJsonGood)) - 1
		$firstResponse = StringSplit(Json_ObjGet($oJsonGood, Json_ObjGetKeys($oJsonGood)[$i]), ",")
		$firstResponse = StringSplit($firstResponse[1], "|")
		$aResponse[$i][0] = $key
		$aResponse[$i][1] = $firstResponse[1]
		$aResponse[$i][2] = $firstResponse[2]
	Next

	return $aResponse
EndFunc

Func CheckIsDead()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)

	Local $gameLanguage = TranslateLanguage($Setup_Main_Language)

	If FindImageInScreen("dead_player_" & $gameLanguage, $XF_image_folder & "\game_items")[0] <> False Then
	;~ If (CheckIfPositionContainsColor(259, 442, "0x652711") = True And CheckIfPositionContainsColor(345, 441, "0x5D2610") = True And CheckIfPositionContainsColor(576, 233, "0x91472D") = True) Or (CheckIfPositionContainsColor(259, 442, "0x652711") = True And CheckIfPositionContainsColor(345, 441, "0x5D2610") = True And CheckIfPositionContainsColor(576, 233, "0x91472D") = True) Then
		AddTextLog( "The player is dead")
		MouseClick("left", $windowPos[0] + 260, $windowPos[1] + 432)
		Sleep(3000)
		return True
	EndIf
	If  FindImageInScreen("dead_player_by_" & $gameLanguage, $XF_image_folder & "\game_items")[0] <> False Then
		AddTextLog( "The player is dead")
		MouseClick("left", $windowPos[0] + 564, $windowPos[1] + 360)
		Sleep(3000)
		return True
	EndIf
	;~ AddTextLog( "CheckDEAD")
	;~ AddTextLog( "0x" & Hex(PixelGetColor(199 + $windowPos[0], 439 + $windowPos[1]), 6) & "-->0x5B210F")
	;~ AddTextLog( "0x" & Hex(PixelGetColor(345 + $windowPos[0], 441 + $windowPos[1]), 6) & "-->0x5D2610")
	;~ AddTextLog( "0x" & Hex(PixelGetColor(576 + $windowPos[0], 233 + $windowPos[1]), 6) & "-->0x91472D")
	return False
EndFunc

Func ProcessScriptResponse($response)
	;~ delete all bank spaces and new lines
	;~ AddTextLog("FindImage " & ' : ' & $response)
	$response = StringReplace($response, @LF, "")
	$response = StringReplace($response, @CRLF, "")
	$response = StringReplace($response, @CR, "")
	$response = StringReplace($response, " ", "")
	;~ AddTextLog("FindImage1 "  & ' : ' & $response)
	$oJson = Json_Decode($response)
	;~ delete ' character from the response
	$oJsonGood = Json_ObjCreate()
	For $i = 0 To UBound(Json_ObjGetKeys($oJson)) - 1
		$key = Json_ObjGetKeys($oJson)[$i]
		$key = StringReplace($key, "'", "")
		$value = Json_ObjGet($oJson, Json_ObjGetKeys($oJson)[$i])
		;~ check if value is an array
		If VarGetType($value) = "Array" Then
			;~ if $value division /2 is 0 then it is a tuple
			If UBound($value) / 2 = Int(UBound($value) / 2) Then
				$resultVale = ''
				For $j = 0 To UBound($value) - 1 Step 2
					$value[$j] = StringReplace($value[$j], "'", "")
					$value[$j] = StringReplace($value[$j], "(", "")
					$value[$j] = StringReplace($value[$j], ")", "")
					$value[$j] = StringReplace($value[$j], "'", "")
					$value[$j + 1] = StringReplace($value[$j + 1], "'", "")
					$value[$j + 1] = StringReplace($value[$j + 1], "(", "")
					$value[$j + 1] = StringReplace($value[$j + 1], ")", "")
					$value[$j + 1] = StringReplace($value[$j + 1], "'", "")
					$resultVale = $resultVale & $value[$j] & "|" & $value[$j + 1] & ","
				Next
				$resultVale = StringTrimRight($resultVale, 1)
				Json_ObjPut($oJsonGood, $key, $resultVale)
			Else
				;~ if $value division /2 is not 0 then it is a list
				For $j = 0 To UBound($value) - 1
					$resultVale = ''
					$value[$j] = StringReplace($value[$j], "'", "")
					$value[$j] = StringReplace($value[$j], "(", "")
					$value[$j] = StringReplace($value[$j], ")", "")
					$value[$j] = StringReplace($value[$j], "'", "")
					$resultVale = $resultVale & $value[$j] & ","
				Next
				$resultVale = StringTrimRight($resultVale, 1)
				Json_ObjPut($oJsonGood, $key, $resultVale)
			EndIf
		Else
			$value = StringReplace($value, "'", "")
			Json_ObjPut($oJsonGood, $key, $value)
		EndIf
	Next
	Return $oJsonGood
EndFunc

Func CloseShitInvites($decline=True)
	Local $language = TranslateLanguage($Setup_Main_Language)
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	$findImage = FindImageInScreen("party_invite_" & $language, $XF_image_folder & "\" & $language & "\farm")
	If $findImage[0] <> False Then
			$PositionOFBS_x = $findImage[1]
			$PositionOFBS_y = $findImage[2]
			If $decline = True Then
				AddTextLog( "Declining Party invite", "red")
				MouseClick("left", $windowPos[0] + $PositionOFBS_x - 40, $windowPos[1] + $PositionOFBS_y + 10)
			Else
				AddTextLog( "Accepting Party invite", "red")
				MouseClick("left", $windowPos[0] + $PositionOFBS_x + 85, $windowPos[1] + $PositionOFBS_y + 10)
		EndIf
	EndIf
EndFunc