
Func GoDungeon()
	;~ Set $Setup_Main_VMName to active window
	If $replay_dungeon = 'NO' Then
		WinActivate($Setup_Main_VMName)
		$windowPos = GetPositionOfWindow($Setup_Main_VMName)
		Sleep(2000)

		$oJson = Json_Decode($JSON_dungeons)
		Local $RUNJSON = Json_Get($oJson, '.dungeons')
		For $i = 0 To UBound($RUNJSON) - 1
			Local $JSONdungeon = Json_Get($oJson, '.dungeons[' & $i & '].name')
			If StringLower($JSONdungeon) = StringLower($Setup_Dungeon_name) Then
				Local $aMapname = Json_Get($oJson, '.dungeons[' & $i & '].mapname')
				Local $dungeonPosition = $i
			EndIf
		Next

		$aMapPosition = GetPositionOfMapInArray($aMapname)

		;~ ;~ ;~ Check actual map
		Local $actualMap = GetMap()
		If $actualMap = -1 Or Int($actualMap) <> Int($aMapPosition) Then
			Local $oJson = Json_Decode($JSON_runs)
			Local $mapName = Json_Get($oJson, '.maps[' & $actualMap & '].name')
			AddTextLog( "Actual map is " & $mapName)
			AddTextLog( "Traveling to " & $aMapname)
			GoToCorrectMap($aMapPosition)
			Return
		EndIf

		If $foundBlacksmithInsideDungeon <> True Then
			CheckInventory()
		EndIf
	EndIf
	goToEntranceNew()

EndFunc

Func finishdungeonfromxf()
	AddTextLog("Dungeon finished")
	$count_dungeon = $count_dungeon + 1
	GUICtrlSetData($text_count_dungeonLabel, "Number of dungeons completed: " & $count_dungeon)
	$dungeonRunning = False
	XF_2ndScript_Send("fromXF|stopfarmingspot|" & $Setup_Main_VMName, 20)
	XF_2ndScript_CheckIfScriptIsRunnung()
	$foundBlacksmithInsideDungeon = True
	$replay_dungeon = 'NO'
EndFunc

Func finishdungeonfromxfNF()
	AddTextLog("Dungeon finished")
	$count_dungeon = $count_dungeon + 1
	GUICtrlSetData($text_count_dungeonLabel, "Number of dungeons completed: " & $count_dungeon)
	$dungeonRunning = False
	XF_2ndScript_Send("fromXF|stopfarmingspot|" & $Setup_Main_VMName, 20)
	XF_2ndScript_CheckIfScriptIsRunnung()
	$foundBlacksmithInsideDungeon = False
	$replay_dungeon = 'NO'
EndFunc

Func finishdungeonfromxfRD()
	AddTextLog("Dungeon finished")
	$count_dungeon = $count_dungeon + 1
	GUICtrlSetData($text_count_dungeonLabel, "Number of dungeons completed: " & $count_dungeon)
	$dungeonRunning = False
	XF_2ndScript_Send("fromXF|stopfarmingspot|" & $Setup_Main_VMName, 20)
	XF_2ndScript_CheckIfScriptIsRunnung()
	$foundBlacksmithInsideDungeon = False
	$replay_dungeon = 'YES'
EndFunc

Func goToEntranceNew()
	$step = False
    While True
         If $dungeonRunning = True Then
             Sleep(1000)
 			$step = 1
             ContinueLoop
         EndIf
        
         If $step = 1 Then
             AddTextLog("Start dungeon again")
             ExitLoop
         EndIf
        
         Local $gameLanguage = TranslateLanguage($Setup_Main_Language)
        
         Local $response = XF_2ndScript_Send("fromXF|dungeon|" & $Setup_Main_VMName & "|" & $XF_image_folder & "|" & $Setup_Dungeon_name & "|" & $gameLanguage & "|" & $Setup_Dungeon_Team_solo & "|" & $Setup_Dungeon_Time_to_exit & "|" & $Setup_Dungeon_Time_to_wait_party & "|" & $replay_dungeon)
		;~  AddTextLog("SpotFarm response: " & $response)
         If $response = 'OK' Then
             $dungeonRunning = True
             ContinueLoop
         EndIf
        
         
    WEnd

EndFunc

;~ Func goToEntrance($dungeonPosition)
;~ 	AddTextLog( "Going to entrance of " & $Setup_Dungeon_name)

;~ 	$windowPos = GetPositionOfWindow($Setup_Main_VMName)

;~ 	$folder_dungeon = StringLower($Setup_Dungeon_name)
;~ 	Local $gameLanguage = TranslateLanguage($Setup_Main_Language)

;~ 	Sleep(1000)
;~ 	;~ Open map
;~ 	OpenMap()
;~ 	Sleep(1000)
;~ 	;~ click on the glass
;~ 	MouseClick("left", $windowPos[0] + 41, $windowPos[1] + 309)
;~ 	Sleep(1000)
;~ 	;~ move mouse in the itemList
;~ 	MouseMove($windowPos[0] + 119, $windowPos[1] + 223)
;~ 	Sleep(1000)

;~ 	Local $PositionOFBS_x = 0
;~ 	Local $PositionOFBS_y = 0
;~ 	Local $BSFoundIcon = False
;~ 	Local $Fails = 0
;~ 	While $BSFoundIcon = False
;~ 		If $Fails > 4 Then
;~ 			return False
;~ 		EndIf
;~ 		$findImage = FindImageInScreen("tower_entrance_icon_" & $gameLanguage, $XF_image_folder & "\dungeons\" & $folder_dungeon)
;~ 		If $findImage[0] = False Then
;~ 			MouseWheel("down", 1)
;~ 			Sleep(1000)
;~ 			$Fails = $Fails + 1
;~ 		Else
;~ 			$PositionOFBS_x = $findImage[1]
;~ 			$PositionOFBS_y = $findImage[2]
;~ 			$BSFoundIcon = True
;~ 		EndIf
;~ 	WEnd
;~ 	MouseClick("left",$windowPos[0] + $PositionOFBS_x, $windowPos[1] + $PositionOFBS_y)
;~ 	Sleep(1000)
;~ 	;~ click on the teleport button
;~ 	MouseClick("left", $windowPos[0] + 476, $windowPos[1] + 274)
;~ 	$aActualtime = TimerInit()
;~ 	While TimerDiff($aActualtime) < 20000
;~ 		Sleep(1000)
;~ 		AddTextLog("Seconds to arrive to " & $Setup_Dungeon_name & ": " & Int(20) - Int(TimerDiff($aActualtime) / 1000))
;~ 	WEnd
;~ 	Local $count = 0
;~ 	waitForTheArrivalToSpot()
;~ 	While FindImageInScreen("hand_up", $XF_image_folder & "\game_items")[0] = False
;~ 		Fight(0, True)
;~ 		Sleep(300)
;~ 		Fight(0, True)
;~ 		$count = $count + 1
;~ 		AddTextLog( "Waiting to arrive to entrance of " & $Setup_Dungeon_name & " (" & $count & "/100)")
;~ 		waitForTheArrivalToSpot()
;~ 		If $count = 100 Then
;~ 			AddTextLog( "We are stuck in the entrance of " & $Setup_Dungeon_name)
;~ 			CheckIsDead()
;~ 			return False
;~ 			ExitLoop
;~ 		EndIf
;~ 	WEnd
;~ 	Send("{f}")
;~ 	Sleep(2000)
;~ 	;~ TODO PARTY DUNGEON
;~ 	MouseClick("left", $windowPos[0] + 789, $windowPos[1] + 450)
;~ 	Sleep(1000)
;~ 	InsideDungeon($dungeonPosition)
;~ EndFunc

;~ Func InsideDungeon($dungeonPosition)
;~ 	$windowPos = GetPositionOfWindow($Setup_Main_VMName)

;~ 	$folder_dungeon = StringLower($Setup_Dungeon_name)

;~ 	$actualtime = TimerInit()
;~ 	While TimerDiff($actualtime) < 10000
;~ 		If FindImageInScreen("load_screen", $XF_image_folder & "\game_items")[0] = False Then
;~ 			ExitLoop
;~ 		EndIf
;~ 		AddTextLog("Waiting to load dungeon")
;~ 		Sleep(1000)
;~ 	WEnd

;~ 	$actualtime = TimerInit()
;~ 	While TimerDiff($actualtime) < 10000
;~ 		If FindImageInScreen("dungeon_intro", $XF_image_folder & "\game_items")[0] = False Then
;~ 			ExitLoop
;~ 		EndIf
;~ 		AddTextLog("Waiting to load intro of dungeon")
;~ 		Sleep(1000)
;~ 	WEnd
;~ 	StartDungeon($dungeonPosition)
;~ EndFunc

;~ Func StartDungeon($dungeonPosition)
;~ 	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
;~ 	$oJson = Json_Decode($JSON_dungeons)
;~ 	$dungeonName = Json_Get($oJson, '.dungeons[' & $dungeonPosition & '].name')
;~ 	$startCoord_x = Json_Get($oJson, '.dungeons[' & $dungeonPosition & '].startcoords[0]')
;~ 	$startCoord_y = Json_Get($oJson, '.dungeons[' & $dungeonPosition & '].startcoords[1]')

;~ 	AddTextLog( "Checking if we are inside " & $dungeonName & " and in the correct position")

;~ 	$actualPlayerCoords = GetPlayerCoords('dungeons', $dungeonName)
;~ 	AddTextLog( "Actual player coords0!!!!: " & $actualPlayerCoords[0])
;~ 	AddTextLog( "Actual player coords1!!!!: " & $actualPlayerCoords[1])
;~ 	If $actualPlayerCoords[0] = False Then
;~ 		AddTextLog( "We are stuck when we try to get player coords, restarting...")
;~ 		CheckIsDead()
;~ 		return
;~ 	EndIf

;~ 	$actualPlayerCoords_x = $actualPlayerCoords[1]
;~ 	$actualPlayerCoords_y = $actualPlayerCoords[2]
;~ 	AddTextLog( "Actual player coords: " & $actualPlayerCoords_x & " " & $actualPlayerCoords_y)

;~ 	;~ Local $firstMovementJSON = Json_Get($oJson, '.dungeons[' & $dungeonPosition & '].firstMovement')
;~ 	;~ For $i = 0 To UBound($firstMovementJSON) - 1 Step 1
;~ 	;~ 	$movement = Json_Get($oJson, '.dungeons[' & $dungeonPosition & '].firstMovement[' & $i & '].move')
;~ 	;~ 	If $movement <> "" Then
;~ 	;~ 		MoveRandom(1, $movement)
;~ 	;~ 	EndIf
;~ 	;~ Next

;~ 	DungeonGo('dungeons', $dungeonName)
;~ 	AddTextLog('END OF PYTON SCRIPT')
;~ 	Sleep(1000000)

;~ 	;~ Local $SETOPJSON = Json_Get($oJson, '.dungeons[' & $dungeonPosition & '].guion')
;~ 	;~ For $i = 0 To UBound($SETOPJSON) - 1 Step 1
;~ 	;~ 	Local $aAction = Json_Get($oJson, '.dungeons[' & $dungeonPosition & '].guion[' & $i & '].action')
;~ 	;~ 	Switch $aAction
;~ 	;~ 		Case "goto"
;~ 	;~ 			$aTargetCoords_x = Json_Get($oJson, '.dungeons[' & $dungeonPosition & '].guion[' & $i & '].targetcoords[0]')
;~ 	;~ 			$aTargetCoords_y = Json_Get($oJson, '.dungeons[' & $dungeonPosition & '].guion[' & $i & '].targetcoords[1]')
;~ 	;~ 			GoTo2ndScript($aTargetCoords_x, $aTargetCoords_y, 'dungeons', $dungeonName)
;~ 	;~ 			Fight()
;~ 	;~ 		Case "findpath"
;~ 	;~ 			$aTargetCoords_x = Json_Get($oJson, '.dungeons[' & $dungeonPosition & '].guion[' & $i & '].targetcoords[0]')
;~ 	;~ 			$aTargetCoords_y = Json_Get($oJson, '.dungeons[' & $dungeonPosition & '].guion[' & $i & '].targetcoords[1]')
;~ 	;~ 			$aPath = FindPath($actualPlayerCoords_x, $actualPlayerCoords_y, $aTargetCoords_x, $aTargetCoords_y, 'dungeons', $dungeonName)
;~ 	;~ 			If $aPath = "notfound" Then
;~ 	;~ 				AddTextLog( "We are stuck when we try to find the path, restarting...")
;~ 	;~ 				CheckIsDead()
;~ 	;~ 				return
;~ 	;~ 			EndIf
;~ 	;~ 			AddTextLog( "Path: " & $aPath)
;~ 	;~ 			$aPath = Json_Encode($aPath)
;~ 	;~ 			$oPath = Json_Decode($aPath)
;~ 	;~ 			$JOSNPath = Json_Get($oPath, '.path')
;~ 	;~ 			For $j = 0 To UBound($JOSNPath) - 1 Step 1
;~ 	;~ 				$aPath_x = Json_Get($oPath, '.path[' & $j & '].x')
;~ 	;~ 				$aPath_y = Json_Get($oPath, '.path[' & $j & '].y')
;~ 	;~ 				AddTextLog( "Moving to: " & $aPath_x & " " & $aPath_y)
;~ 	;~ 			Next
;~ 	;~ 	EndSwitch
;~ 	;~ Next



;~ EndFunc
