#Include <WinAPI.au3>
#Include <AutoItConstants.au3>

Func GoFarm()
	;~ Set $Setup_Main_VMName to active window
	WinActivate($Setup_Main_VMName)
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	Sleep(2000)

	;~ Check actual map
	Local $actualMap = GetMap()
	If $actualMap = -1 Then
		AddTextLog( "Traveling a known map before starting")
		GoToCorrectMap(0)
		Return
	EndIf

	Fight()

	$oJson = Json_Decode($JSON_runs)
	Local $mapName = Json_Get($oJson, '.maps[' & $actualMap & '].name')

	If $Setup_Farm_FarmMap = 'All' Then
		
		If $Setup_LastRun_mapName = "init" And $Setup_LastRun_step = "init" And $Setup_LastRun_position = "init" Then
			;~ first time running the script
			;~ go to the first map
			AddTextLog( "First time running the script")

			If $mapName = "westmarch" Then
				GoToCorrectMap(0)
			Else
				Farm($actualMap, $Setup_LastRun_step)
			EndIf
		Else
			;~ check if actual map is the same as the one in the setup file
			If $mapName = $Setup_LastRun_mapName Then
				Farm($actualMap, $Setup_LastRun_step)
			Else
				;~ Go to Correct Map
				AddTextLog( "Actual map is " & $mapName)
				AddTextLog( "Going to " & $Setup_LastRun_mapName)
				;~ Local $MOVEMAP = Json_Get($oJson, '.maps[' & $actualMap & '].runs[' & $i & '].moveMap')
				GoToCorrectMap($Setup_LastRun_position)
				Return
			EndIf
		EndIf
	Else
		;~ set farmMap to lower case
		$Setup_Farm_FarmMapTmp = StringLower($Setup_Farm_FarmMap)
		If $mapName = $Setup_Farm_FarmMapTmp Then
		;~ check if stepNameSetup exist in the actual map
			Local $RUNJSONNAME = Json_Get($oJson, '.maps[' & $actualMap & '].runs')
			For $i = 0 To UBound($RUNJSONNAME) - 1
				Local $stepNameTmp = Json_Get($oJson, '.maps[' & $actualMap & '].runs[' & $i & '].name')
				If $stepNameTmp = $Setup_LastRun_step Then
					;~ stepNameSetup exist, go to farm
					Farm($actualMap, $Setup_LastRun_step)
					Return
				EndIf
			Next
			;~ stepNameSetup doesn't exist, set stepNameSetup to 0	
			AddTextLog( "StepName" & $Setup_LastRun_step & " doesn't exist in " & $mapName)
			AddTextLog( "Going to step 0")
			$Setup_LastRun_step = 0
			Farm($actualMap, $Setup_LastRun_step)
		Else
			;~ Go to Correct Map
			AddTextLog( "Actual map is " & $mapName)
			AddTextLog( "Going to " & $Setup_Farm_FarmMap)
			;~ get the position of the map $Setup_Farm_FarmMap in the array
			Local $Setup_LastRun_position = GetPositionOfMapInArray($Setup_Farm_FarmMap)
			GoToCorrectMap($Setup_LastRun_position)
			Return	
		EndIf
	EndIf
EndFunc


Func Farm($actualMapVar, $stepName)
	$oJson = Json_Decode($JSON_runs)
	Local $RUNJSON = Json_Get($oJson, '.maps[' & $actualMapVar & '].runs')
	Local $mapName = Json_Get($oJson, '.maps[' & $actualMapVar & '].name')
	;~ print Starting farm in map " & $mapName & @CRLF in color green
	AddTextLog( "Starting farm in map " & $mapName)
	For $i = 0 To UBound($RUNJSON) - 1 Step 1
		Local $x = Json_Get($oJson, '.maps[' & $actualMapVar & '].runs[' & $i & '].coords[0]')
		Local $y = Json_Get($oJson, '.maps[' & $actualMapVar & '].runs[' & $i & '].coords[1]')
		Local $MapCoords_x = Json_Get($oJson, '.maps[' & $actualMapVar & '].runs[' & $i & '].mapCoords[0]')
		Local $MapCoords_y = Json_Get($oJson, '.maps[' & $actualMapVar & '].runs[' & $i & '].mapCoords[1]')
		Local $runName = Json_Get($oJson, '.maps[' & $actualMapVar & '].runs[' & $i & '].name')
		Local $MOVEMAP = Json_Get($oJson, '.maps[' & $actualMapVar & '].runs[' & $i & '].moveMap')
		If $runName <> $stepName Or $stepName <> 0 Then
			ContinueLoop
		EndIf
		CheckIsDead()
		CheckLife()
		;~ get the total of RUNJSON and check if we need to check inventory
		Local $totalRuns = UBound($RUNJSON) - 1
		If $totalRuns < 5 And $i = $totalRuns Then
			CheckBestiary()
			CheckInventory()
		Else
			If Mod($i, 5) = 0 Then
				CheckBestiary()
				CheckInventory()
			EndIf
		EndIf

		;~ go to step
		AddTextLog( "Going to " & $runName)
		$windowPos = GetPositionOfWindow($Setup_Main_VMName)

		;~ Open map
		OpenMap()
		Sleep(2000)
		CheckIsDead()
		;~ click on the glass
		MouseClick("left", $windowPos[0] + 41, $windowPos[1] + 309)
		Sleep(1000)
		;~ click on the MapCoords element
		MouseClick("left", $windowPos[0] + $MapCoords_x, $windowPos[1] + $MapCoords_y)
		Sleep(1000)
		;~ close glass
		MouseClick("left", $windowPos[0] + 298, $windowPos[1] + 306)
		;~ check if needed move map
		For $ii = 0 To UBound($MOVEMAP) - 1 Step 1
			Local $x1 = Json_Get($oJson, '.maps[' & $actualMapVar & '].runs[' & $i & '].moveMap[' & $ii & '].x1')
			Local $y1 = Json_Get($oJson, '.maps[' & $actualMapVar & '].runs[' & $i & '].moveMap[' & $ii & '].y1')
			Local $x2 = Json_Get($oJson, '.maps[' & $actualMapVar & '].runs[' & $i & '].moveMap[' & $ii & '].x2')
			Local $y2 = Json_Get($oJson, '.maps[' & $actualMapVar & '].runs[' & $i & '].moveMap[' & $ii & '].y2')
			;~ check if variables is not empty
			If $x1 <> "" And $y1 <> "" And $x2 <> "" And $y2 <> "" Then
				;~ AddTextLog( "Moving map")
				MouseClickDrag("left", $windowPos[0] + $x1, $windowPos[1] + $y1, $windowPos[0] + $x2, $windowPos[1] + $y2)
				Sleep(1000)
			EndIf
		Next
		;~ click on the step
		MouseClick("left", $windowPos[0] + $x, $windowPos[1] + $y)
		Sleep(1000)
		MouseClick("left", $windowPos[0] + $x, $windowPos[1] + $y)
		Sleep(2000)
		Local $count = 0
		;~ AddTextLog( "x: " & $x & " y: " & $y)
		;~ AddTextLog( "x: " & $x & " y: " & $y - 41)
		While (PixelSearch($windowPos[0] + $x - 69, $windowPos[1] + $y - 64, $windowPos[0] + $x + 66, $windowPos[1] + $y - 40, 0x622F22) = 0)
		;~ AddTextLog( "x: " & $x & " y: " & $y)
		;~ AddTextLog( "x: " & $x & " y: " & $y - 41)
			$count = $count + 1
			If $count > 10 Then
				AddTextLog( "Error: Can't go to " & $runName)
				ExitLoop
				Return
			EndIf
			MouseClick("left", $windowPos[0] + $x, $windowPos[1] + $y)
			Sleep(2000)
		WEnd
		FindAndClickTeleportOrNavigate()
		Sleep(3000)
		AvoidTeleport()
		While CheckIfWeAreInStep() = False
			Sleep(300)
		WEnd
		CheckIsDead()

		;~ hold random key a,s,d,w 1 second
		Local $random = Random(1, 4, 1)
		If $random = 1 Then
			Send("{a}")
			Send("{a}")
		ElseIf $random = 2 Then
			Send("{s}")
			Send("{s}")
		ElseIf $random = 3 Then
			Send("{d}")
			Send("{d}")
		ElseIf $random = 4 Then
			Send("{w}")
			Send("{w}")
		EndIf
		;~ execute function Fight() 4 seconds
		Local $start = TimerInit()
		While TimerDiff($start) < 4000
			Fight()
			Sleep(100)
		WEnd

		CheckIsDead()
		AddTextLog( "Finished " & $runName)
		If Json_Get($oJson, '.maps[' & $actualMapVar & '].runs[' & $i + 1  & '].name') <> "" Then
			$stepName = Json_Get($oJson, '.maps[' & $actualMapVar & '].runs[' & $i + 1  & '].name')
		Else
			If  Json_Get($oJson, '.maps[' & $actualMapVar + 1 & '].runs[0].name') <> "" Then
				$stepName = Json_Get($oJson, '.maps[' & $actualMapVar + 1 & '].runs[0].name')
				$mapName = Json_Get($oJson, '.maps[' & $actualMapVar + 1 & '].name')
				$actualMapVar = $actualMapVar + 1
			Else
				$stepName = Json_Get($oJson, '.maps[0].runs[0].name')
				$mapName = Json_Get($oJson, '.maps[0].name')
				$actualMapVar = 0
			EndIf
		EndIf
		AddTextLog( "Next step is " & $stepName)
		AddTextLog( "Next map is " & $mapName)
		AddTextLog( "Next map number is " & $actualMapVar)
		WriteSetupFile('LastRun_mapName', $mapName)
		WriteSetupFile('LastRun_step', $stepName)
		WriteSetupFile('LastRun_position', $actualMapVar)
	Next
EndFunc

Func CheckBestiary()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	AddTextLog( "Checking bestiary")
	MouseClick("left", $windowPos[0] + 31, $windowPos[1] + 214)
	Sleep(3000)
	Local $bestiary = PixelSearch(88 + $windowPos[0], 165 + $windowPos[1], 323 + $windowPos[0], 452 + $windowPos[1], 0x07C823, 1, 1)
	If $bestiary <> 0 Then
		AddTextLog( "Going to bestiary")
		MouseClick("left", $bestiary[0], $bestiary[1])
		Sleep(50000)
		Local $count = 0
		While CheckIfWeAreInStep() = False Or CheckIfPositionContainsColor(703, 316, "0xE4C60F") = False
			Sleep(300)
			$count = $count + 1
			If $count = 100 Then
				AddTextLog( "We are stuck in the bestiary")
				CheckIsDead()
				return True
				ExitLoop
			EndIf
		WEnd
		AddTextLog( "We are in the bestiary")
		Send("{f}")
		Sleep(60000)
		MouseClick("left", 928 + $windowPos[0], 60 + $windowPos[1])
		Sleep(5000)
		Loot()
	Else
		MouseClick("left", $windowPos[0] + 31, $windowPos[1] + 214)
		Sleep(1000)
	EndIf
EndFunc

