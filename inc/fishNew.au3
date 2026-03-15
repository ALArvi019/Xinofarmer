Func GoFishNew()
	;~ Set $Setup_Main_VMName to active window
	WinActivate($Setup_Main_VMName)
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	Sleep(2000)

	;~ Check actual map
	Local $actualMap = GetMap()
	If $actualMap = -1 Then
		AddTextLog( "Traveling a known map before starting")
		CloseShitInvites()
		GoToCorrectMap(0)
		CloseShitInvites()
		Return
	EndIf

	Fight(0, True)
	FishShit()
	CloseShitInvites()

	Local $oJson = Json_Decode($JSON_runs)
	Local $mapName = Json_Get($oJson, '.maps[' & $actualMap & '].name')

	$Setup_Fish2_Maps = StringLower($Setup_Fish2_Maps)
	If $mapName = $Setup_Fish2_Maps Then
		AddTextLog( "We are in the correct map: " & $mapName)
		CloseShitInvites()
		;~ Go to fish
		AddTextLog( "Going to fish")
		GoToFish2($actualMap)
	Else
		AddTextLog( "Actual map is " & $mapName)
		AddTextLog( "Going to " & $Setup_Fish2_Maps)
		$positionOfArrayMap = GetPositionOfMapInArray($Setup_Fish2_Maps)
		GoToCorrectMap($positionOfArrayMap)
		Return
	EndIf
EndFunc

Func GoToFish2($actualMap)
	executefishScript2()
EndFunc

Func sendyellowdust($sData)
	$count_yellow_dust = $count_yellow_dust + $sData
	GUICtrlSetData($text_count_yellow_dustLabel, "Yellow dust: " & $count_yellow_dust)
	GUICtrlSetData($text_count_yellow_dust2Label, "Yellow dust: " & $count_yellow_dust)
EndFunc

Func sendscrap($sData)
	$count_scrap = $count_scrap + $sData
	GUICtrlSetData($text_count_scrapLabel, "Scrap: " & $count_scrap)
	GUICtrlSetData($text_count_scrap2Label, "Scrap: " & $count_scrap)
EndFunc

Func sendactualiter($sData)
	$actual_iter = $sData
	GUICtrlSetData($text_actual_iterLabel, "Actual iteration: " & $actual_iter)
EndFunc

Func executefishScript2()
	$step = False
	While True
		If $fishingRunning = True Then
			Sleep(1000)
			$step = 1
			ContinueLoop
		EndIf
	   
		If $step = 1 Then
			AddTextLog("Start Fishing Again")
			ExitLoop
		EndIf
	   
		Local $response = XF_2ndScript_Send("fromXF|fishingNew|" & $Setup_Main_VMName & "|" & $XF_image_folder)
	   ;~  AddTextLog("SpotFarm response: " & $response)
		If $response = 'OK' Then
			$fishingRunning = True
			ContinueLoop
		EndIf
	WEnd
EndFunc
