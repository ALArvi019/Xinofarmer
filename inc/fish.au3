Func GoFish()
	;~ Set $Setup_Main_VMName to active window
	WinActivate($Setup_Main_VMName)
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	Sleep(2000)

	;~ Check actual map
	Local $actualMap = GetMap()
	If $actualMap = -1 Then
		AddTextLog( "Traveling a known map before starting")
		GoToCorrectMap(0)
		CloseShitInvites()
		Return
	EndIf

	Fight(0, True)
	FishShit()
	CloseShitInvites()

	Local $oJson = Json_Decode($JSON_runs)
	Local $mapName = Json_Get($oJson, '.maps[' & $actualMap & '].name')

	$Setup_Fish_Maps = StringLower($Setup_Fish_Maps)
	If $mapName = $Setup_Fish_Maps Then
		AddTextLog( "We are in the correct map: " & $mapName)
		CloseShitInvites()
		CheckInventory()
		;~ Go to fish
		AddTextLog( "Going to fish")
		GoToFish($actualMap)
		CloseShitInvites()
	Else
		AddTextLog( "Actual map is " & $mapName)
		AddTextLog( "Going to " & $Setup_Fish_Maps)
		$positionOfArrayMap = GetPositionOfMapInArray($Setup_Fish_Maps)
		GoToCorrectMap($positionOfArrayMap)
		Return
	EndIf
EndFunc

Func GoToFish($actualMap)
	If 1 = 1 Then

		$windowPos = GetPositionOfWindow($Setup_Main_VMName)
		CloseShitInvites()
		OpenMap()
		Sleep(2000)
		MouseClick("left", $windowPos[0] + 34, $windowPos[1] + 310)
		Sleep(1000)
		MouseMove($windowPos[0] + 113, $windowPos[1] + 232)
		Sleep(1000)
		Local $PositionOFBS_x = 0
		Local $PositionOFBS_y = 0
		Local $BSFoundIcon = False
		Local $Fails = 0
		While $BSFoundIcon = False
			CloseShitInvites()
			If $Fails > 4 Then
				AddTextLog( "We are stuck found the fisherman")
				CheckIsDead()
				return True
			EndIf
			$findImage = FindImageInScreen("fisherman", $XF_image_folder & "\mapLegend")
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
		MouseClick("left", $windowPos[0] + $PositionOFBS_x, $windowPos[1] + $PositionOFBS_y)
		Sleep(2000)
		FindAndClickTeleportOrNavigate()
		
		$aActualtime = TimerInit()
		While TimerDiff($aActualtime) < 15000
			Sleep(1000)
			AddTextLog("Seconds to arrive to fisherman: " & Int(15) - Int(TimerDiff($aActualtime) / 1000))
			Fight(0, True)
			CloseShitInvites()
		WEnd
		Local $count = 0

		While CheckIfWeAreInStep() = False Or FindImageInScreen("talk", $XF_image_folder & "\game_items")[0] = False
			;~ AddTextLog("1 --> " & CheckIfWeAreInStep())
			;~ AddTextLog("2 --> " & CheckIfPositionContainsColor(690, 311, "0x693108"))
			;~ AddTextLog("3 --> " & CheckIfPositionContainsColor(707, 311, "0x5E2104"))
			;~ AddTextLog("4 --> " & CheckIfPositionContainsColor(699, 311, "0x6B2809"))
			AddTextLog( "Waiting to arrive to fisherman")
			Sleep(300)
			$count = $count + 1
			If $count = 100 Then
				AddTextLog( "We are stuck in the fisherman")
				CheckIsDead()
				return True
				ExitLoop
			EndIf
		WEnd
			;~ click on the fisherman
		CloseShitInvites()
		Fight(0, True)
		Send("f")
		Sleep(3000)
		CloseShitInvites()
		BuyLure()
		Fight(0, True)
		Send("f")
		CloseShitInvites()
		SellFish($actualMap)
		Sleep(3000)
		GoToRiver($actualMap)
	EndIf
	StarFish($actualMap)
EndFunc

Func StarFish($actualMap)
	$cont = 0
	While CheckIfPositionContainsColor(711, 317, "0xD09214") = False
		AddTextLog( "Waiting to fish option is available")
		CloseShitInvites()
		Sleep(300)
		$cont = $cont + 1
		If $cont = 100 Then
			AddTextLog( "We are stuck when we try to fish")
			CheckIsDead()
			CloseShitInvites()
			return True
			ExitLoop
		EndIf
	WEnd
	Sleep(1000)
	Local $oJson = Json_Decode($JSON_runs)
	local $randommove = Json_Get($oJson, '.maps[' & $actualMap & '].fishData[0].randommove')
	MoveRandom(1, $randommove)
	CloseShitInvites()
	FishBucle(0)
EndFunc

Func FishShit()
	CloseShitInvites()
	If CheckIfPositionContainsColor(320, 359, "0x41201B") = True And CheckIfPositionContainsColor(519, 359, "0x41211B") = True Then
		$windowPos = GetPositionOfWindow($Setup_Main_VMName)
		AddTextLog( "I don't want to cancel the fishing")
		MouseClick("left", $windowPos[0] + 320, $windowPos[1] + 359)
		sleep(1000)
		CheckIsDead()
		return True
	EndIf
EndFunc


Func FishBucle($step, $avoidTime = False)
	XF_2ndScript_CheckIfScriptIsRunnung()
	FishShit()
	NewLoot()
	Sleep(1000)
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	;~ bucle with 20 fishes
	If $step < $Setup_Fish_Fish_Iter Then
		$actualtime = TimerInit()
		$timemessage = TimerInit()
		If $avoidTime = False Then
			AddTextLog("Fishing " & $step + 1 & " of " & $Setup_Fish_Fish_Iter)
			Send("f")
			If $Setup_Fish_FishType = 'Gold' Then
				$timeFish = 170000;~ TIME TO WAIT FOR FISHING grey, blue, gold?? 3MIN
			ElseIf $Setup_Fish_FishType = 'Epic' Then
				$timeFish = 240000
			ElseIf $Setup_Fish_FishType = 'Legendary' Then
				$timeFish = 200000
			ElseIf $Setup_Fish_FishType = 'Blue' Then
				$timeFish = 58000
			ElseIf $Setup_Fish_FishType = 'White' Then
				$timeFish = 5000
			Else
				$timeFish = 180000
			EndIf
			While TimerDiff($actualtime) < $timeFish
				Sleep(30000)
				Local $atime = Int($timeFish / 1000) - Int(TimerDiff($actualtime) / 1000)
				If Int($atime) < 0 Then
					$atime = 0
				EndIf
				AddTextLog( "Waiting to fish " & $Setup_Fish_FishType & ". " & $atime & " seconds left")
				CloseShitInvites()
				FishShit()
			WEnd
		EndIf
		;~ Sleep(10000) ;~ TIME TO WAIT FOR FISHING grey, blue, gold?? 3MIN
		If CheckIfPositionContainsColor(711, 317, "0xD09214") = True Then
			AddTextLog( "We are stuck when we try to fish")
			CheckIsDead()
			return True
		EndIf
		While CheckIfPositionContainsColor(851, 454, "0x9B917D") = False
			Sleep(300)
			FishShit()
			;~ show "Waiting to fish" every 10 seconds
			If TimerDiff($timemessage) > 10000 Then
				AddTextLog( "Waiting to fish")
				$timemessage = TimerInit()
			EndIf
			If TimerDiff($actualtime) > 310000 Then
				AddTextLog( "We are stuck when we try to fish")
				CheckIsDead()
				return True
				ExitLoop
			EndIf
		WEnd
		$response = executefishScript($Setup_Fish_FishType, $step)
		NewLoot()
		If $response = 'failed' Then
			FishBucle($step, True)
		Else
			FishBucle($step + 1)
		EndIf
	Else
		AddTextLog( "We have finished fishing")
		Return
	EndIf
EndFunc

Func executefishScript($sFishType, $step = 0)
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	MouseClick("left", $windowPos[0] + 851, $windowPos[1] + 454)
	Sleep(100)
	Local $response = XF_2ndScript_Send("fromXF|fish|" & $Setup_Main_VMName & "|" & $XF_image_folder & "\fishing|" & $sFishType, 10)
	AddTextLog("fish response: " & $response)
	if $response = 'failed' Then
		return 'failed'
	EndIf
	;~ MouseClick("left", $windowPos[0] + 851, $windowPos[1] + 454)
	Sleep(100)
	;~ MouseClick("left", $windowPos[0] + 851, $windowPos[1] + 454)
	While CheckIfPositionContainsColor(882, 349, "0xC88C14") = True And CheckIfPositionContainsColor(884, 283, "0xA41B0D") = False 
		Sleep(100)
	WEnd
	AddTextLog( "We have finished fishing this round")
	FishShit()
	Return 'success'
EndFunc

Func GoToRiver($actualMap)
	Local $oJson = Json_Decode($JSON_runs)
	Local $scroll = Json_Get($oJson, '.maps[' & $actualMap & '].fishData[0].scroll')
	Local $leftoption_x = Json_Get($oJson, '.maps[' & $actualMap & '].fishData[0].leftoption[0]')
	Local $leftoption_y = Json_Get($oJson, '.maps[' & $actualMap & '].fishData[0].leftoption[1]')
	Local $river_x = Json_Get($oJson, '.maps[' & $actualMap & '].fishData[0].river[0]')
	Local $river_y = Json_Get($oJson, '.maps[' & $actualMap & '].fishData[0].river[1]')
	local $ctrlscroll = Json_Get($oJson, '.maps[' & $actualMap & '].fishData[0].ctrlscroll')
	Local $imgtofind = ''
	If $leftoption_x = 0 And $leftoption_y = 0 Then
		Local $imgtofind = Json_Get($oJson, '.maps[' & $actualMap & '].fishData[0].imgtofind')
	EndIf

	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	OpenMap()
	Sleep(2000)
	;~ glass
	MouseClick("left", $windowPos[0] + 35, $windowPos[1] + 307)
	Sleep(1000)
	MouseMove($windowPos[0] + 132, $windowPos[1] + 224)
	Sleep(1000)
	If $imgtofind <> '' Then
		Local $PositionOFBS_x = 0
		Local $PositionOFBS_y = 0
		Local $BSFoundIcon = False
		Local $Fails = 0
		While $BSFoundIcon = False
			If $Fails > 4 Then
				AddTextLog( "We are stuck found the fisherman")
				CheckIsDead()
				return True
			EndIf
			$findImage = FindImageInScreen($imgtofind, $XF_image_folder & "\mapLegend")
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
		MouseClick("left", $windowPos[0] + $PositionOFBS_x, $windowPos[1] + $PositionOFBS_y)
	Else
		MouseWheel("down", $scroll)
		Sleep(2000)	
		MouseClick("left", $windowPos[0] + $leftoption_x, $windowPos[1] + $leftoption_y)
	EndIf
	Sleep(1000)
	;~ 671, 127
	MouseClick("left", $windowPos[0] + 671, $windowPos[1] + 127)
	Sleep(1000)
	;~ move mouse ti center of the screen 482, 386
	MouseMove($windowPos[0] + 482, $windowPos[1] + 386)
	WinActivate($Setup_Main_VMName)
	_WinAPI_Keybd_Event(0x11, 0) ; CTRL Down
	MouseWheel("up", $ctrlscroll)
	Sleep(2000)
	While _IsPressed('11')
		ControlSend("", "", "", "text", 0)
		_WinAPI_Keybd_Event(0x11, 2) ; CTRL Up
		Sleep(200)
	WEnd
	MouseClick("left", $windowPos[0] + $river_x, $windowPos[1] + $river_y)
	Sleep(1000)
	MouseClick("left", $windowPos[0] + $river_x, $windowPos[1] + $river_y)
	Sleep(1000)
	FindAndClickTeleportOrNavigate()
	Sleep(6000)
EndFunc

Func BuyLure()
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	Sleep(2000)
	MouseClick("left", $windowPos[0] + 767, $windowPos[1] + 368)
	Sleep(2000)
	MouseClick("left", $windowPos[0] + 809, $windowPos[1] + 464)
	Sleep(2000)
	;~ 879, 341
	MouseClick("left", $windowPos[0] + 879, $windowPos[1] + 341)
	Sleep(1000)
	;~ 879, 341
	MouseClick("left", $windowPos[0] + 879, $windowPos[1] + 341)
	Sleep(2000)
	;~ 863, 404
	MouseClick("left", $windowPos[0] + 863, $windowPos[1] + 404)
	Sleep(2000)
	;~ 821, 514
	MouseClick("left", $windowPos[0] + 821, $windowPos[1] + 514)
	Sleep(2000)
	Send("{ESC}")
	Sleep(2000)
EndFunc

Func SellFish($actualMap)
	$windowPos = GetPositionOfWindow($Setup_Main_VMName)
	;~ 778, 318
	Sleep(2000)
	MouseClick("left", $windowPos[0] + 778, $windowPos[1] + 318)
	Sleep(2000)
	;~ 481, 526
	MouseClick("left", $windowPos[0] + 481, $windowPos[1] + 526)
	Sleep(2000)
	;~ 747, 512
	MouseClick("left", $windowPos[0] + 747, $windowPos[1] + 512)
	Sleep(2000)
	If FindImageInScreen("close", $XF_image_folder & "\game_items")[0] <> False Then
		AddTextLog( "We have no fish to sell")
		Send("{ESC}")
		Sleep(2000)
		Fight(0, True)
	Else
		Local $oJson = Json_Decode($JSON_runs)
		local $lootmove = Json_Get($oJson, '.maps[' & $actualMap & '].fishData[0].lootmove')
		$lootmove = StringSplit($lootmove, "|")
		;~ for every item in the loot
		For $i = 1 To $lootmove[0]
			AddTextLog("Moving to: " & $lootmove[$i])
			MovePlayerToLoot($lootmove[$i])
			Sleep(1000)
			FindLootNearPlayer()
			MovePlayerToLoot(getReverseDirection($lootmove[$i]))
			Sleep(1000)
		Next
		;~ MovePlayerToLoot()
		Fight(0, True)
		Sleep(2000)
		NewLoot()
		Sleep(2000)
		NewLoot()
		Sleep(2000)
		NewLoot()
		Sleep(2000)
	EndIf
EndFunc
