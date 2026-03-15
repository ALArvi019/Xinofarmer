Func GoCyrangar()
	Sleep(2000)

	Fight(0, True)

	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	Local $language = TranslateLanguage($Setup_Main_Language)
	
	;~ click on menu 943, 67
	MouseClick("left", $windowPos[0] + 943, $windowPos[1] + 67)
	Sleep(2000)

	;~ check if menu is open
	If FinfImageAndClic("\" & $language & "\cyrangar", "warband_" & $language) = False Then
		AddTextLog( "We are stuck when we try to open warband menu")
		AddTextLog( "You are in a warband?")
		CheckIsDead()
		;~ press esc
		Send("{ESC}")
		Sleep(2000)
		;~ 367, 355
		MouseClick("left", $windowPos[0] + 367, $windowPos[1] + 355)
		return
	EndIf

	Sleep(2000)

	$response1 = FindImageInScreen('go_to_cyrangar_on_' & $language, $XF_image_folder & "\" & $language & "\cyrangar", 0.8, "False")
	$response2 = FindImageInScreen('go_to_cyrangar_off_' & $language, $XF_image_folder & "\" & $language & "\cyrangar", 0.8, "False")

	If $response1[0] <> False And $response2[0] <> False Then
		$response1[3] = Int(StringReplace($response1[3], '.', ''))
		$response2[3] = Int(StringReplace($response2[3], '.', ''))
		If $response1[3] > $response2[3] Then
			AddTextLog( "We are going to cyrangar")
			MouseClick("left", $windowPos[0] + $response1[1], $windowPos[1] + $response1[2])
			;~ for 20 seconds
			$aActualtime = TimerInit()
			While TimerDiff($aActualtime) < 20000
				Sleep(1000)
				AddTextLog("Seconds to arrive to cyrangar: " & Int(20) - Int(TimerDiff($aActualtime) / 1000))
			WEnd
		Else
			AddTextLog( "We already are in cyrangar")
			;~ send esc
			Send("{ESC}")
			Sleep(2000)
		EndIf
	Else
		AddTextLog( "You are in a warband?")
		CheckIsDead()
		;~ press esc
		Send("{ESC}")
		Sleep(2000)
		;~ 367, 355
		MouseClick("left", $windowPos[0] + 367, $windowPos[1] + 355)
		return
	EndIf

	;~ CheckInventory(True)

	If $Setup_Cyrangar_Mode = "Endless" Then
		GoToEndless()
	Else
		AddTextLog("Not implemented mode " & $Setup_Cyrangar_Mode)
	EndIf
EndFunc

Func GoToEndless()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	Local $language = TranslateLanguage($Setup_Main_Language)
	OpenMapCyrangar()
	Sleep(2000)
	If FinfImageAndClic("\" & $language & "\cyrangar", "endless_gate") = False Then
		AddTextLog( "Not found the endless gate")
		CheckIsDead()
		;~ press esc
		Send("{ESC}")
		Sleep(2000)
		;~ 367, 355
		MouseClick("left", $windowPos[0] + 367, $windowPos[1] + 355)
		MoveRandom(2, "NorthEast")
		return
	EndIf
	Sleep(2000)
	FinfImageAndClic("\" & $language & "\cyrangar", "enter_" & $language)
	Sleep(1000)
	If FinfImageAndClic("\" & $language & "\cyrangar", "endless_" & $language) = False Then
		If FinfImageAndClic("\" & $language & "\cyrangar", "endless_2_" & $language) = False Then
			AddTextLog( "Not found the endless button")
			CheckIsDead()
			;~ press esc
			Send("{ESC}")
			Sleep(2000)
			;~ 367, 355
			MouseClick("left", $windowPos[0] + 367, $windowPos[1] + 355)
			MoveRandom(2, "NorthEast")
			return
		EndIf
	EndIf
	Sleep(1000)
	FinfImageAndClic("\" & $language & "\cyrangar", "create_raid_" & $language)
	Sleep(1000)
	FinfImageAndClic("\" & $language & "\cyrangar", "enter_" & $language)
	Sleep(1000)
	$aActualtime = TimerInit()
	While FindImageInScreen("life_door_icon1", $XF_image_folder & "\" & $language & "\cyrangar")[0] = False And FindImageInScreen("life_door_icon2", $XF_image_folder & "\" & $language & "\cyrangar")[0] = False
		Sleep(1000)
		AddTextLog("Waiting for the endless to start")
		AddTextLog("Seconds to abort the endless: " & Int(20) - Int(TimerDiff($aActualtime) / 1000))
		If TimerDiff($aActualtime) > 20000 Then
			AddTextLog("We are stuck when we try to start the endless")
			CheckIsDead()
			;~ press esc
			Send("{ESC}")
			Sleep(2000)
			;~ 367, 355
			MouseClick("left", $windowPos[0] + 367, $windowPos[1] + 355)
			MoveRandom(2, "NorthEast")
			return
		EndIf
	WEnd
	AddTextLog("Endless started")
	executeendlessScript()

EndFunc

Func finishedendlessfromxf()
	AddTextLog("Endless finished")
	$endlessRunning = False
	MoveRandom(2, "NorthEast")
	XF_2ndScript_Send("fromXF|stopfarmingspot|" & $Setup_Main_VMName, 20)
	XF_2ndScript_CheckIfScriptIsRunnung()
EndFunc

Func executeendlessScript()
	$step = False
	While True
		If $endlessRunning = True Then
			Sleep(1000)
			$step = 1
			ContinueLoop
		EndIf
	   
		If $step = 1 Then
			AddTextLog("Start Endless again")
			ExitLoop
		EndIf
	   
		Local $gameLanguage = TranslateLanguage($Setup_Main_Language)
	   
		Local $response = XF_2ndScript_Send("fromXF|endless|" & $Setup_Main_VMName & "|" & $XF_image_folder & "|" & $gameLanguage & "|" & $Setup_Telegram_IsConfig & "|" & $XF_Username)
	   ;~  AddTextLog("endless response: " & $response)
		If $response = 'OK' Then
			$endlessRunning = True
			ContinueLoop
		EndIf
	   
		
	WEnd
EndFunc