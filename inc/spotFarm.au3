#Include <WinAPI.au3>
#Include <AutoItConstants.au3>

Func GoSpotFarm()
	telegram_CheckUserIsConfig()
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

	Local $oJson = Json_Decode($JSON_runs)
	Local $mapName = Json_Get($oJson, '.maps[' & $actualMap & '].name')

	$Setup_SpotFarm_SpotFarmMap = StringLower($Setup_SpotFarm_SpotFarmMap)
	;~ check if the las character is a number to delete it
	If StringIsDigit(StringRight($Setup_SpotFarm_SpotFarmMap, 1)) Then
		$mapName = $mapName & StringRight($Setup_SpotFarm_SpotFarmMap, 1)
	EndIf

	If StringLeft($Setup_SpotFarm_SpotFarmMap, 6) = "model_" Then
		$modelname = StringLower($Setup_SpotFarm_SpotFarmMap)
		$real_map_name = StringLower($Setup_SpotFarm_SpotFarmCustomModelMap)
	Else
		$modelname = "default"
		$real_map_name = StringLower($Setup_SpotFarm_SpotFarmMap)
	EndIf

	If $mapName = $real_map_name Then
		AddTextLog( "We are in the correct map: " & $mapName)
		GoToSpotFarm($modelname, $real_map_name)
	Else
		AddTextLog( "Actual map is " & $mapName)
		AddTextLog( "Going to " & $real_map_name)
		$positionOfArrayMap = GetPositionOfMapInArray($real_map_name)
		GoToCorrectMap($positionOfArrayMap)
		Return
	EndIf
EndFunc

Func GoToSpotFarm($modelname, $real_map_name)
	AddTextLog("Going to spot farm")
	executeSpotFarmScript($modelname, $real_map_name)
EndFunc

;~ Func executeSpotFarmScript($step = False)
;~  	If $spotFarmRunning = True Then
;~  		Sleep(1000)
;~  		executeSpotFarmScript(True)
;~  		Return
;~  	EndIf
;~  	If $step = 1 Then
;~  		AddTextLog("Start spot again")
;~  		Return
;~  	EndIf

;~  	Local $gameLanguage = TranslateLanguage($Setup_Main_Language)

;~  	Local $response = XF_2ndScript_Send("fromXF|farmingspot|" & $Setup_Main_VMName & "|" & $XF_image_folder & "\..|" & $Setup_SpotFarm_SpotFarmMap & "|" & $gameLanguage & "|" & $Setup_SpotFarm_AcceptPartyInvites& "|" & $Setup_Telegram_IsConfig & "|" & $XF_Username)
;~  	AddTextLog("SpotFarm response: " & $response)
;~  	If $response = 'OK' Then
;~  		;~ AddTextLog("SpotFarm response is OKk4kkkkkk")
;~  		$spotFarmRunning = True
;~  		executeSpotFarmScript(True)
;~ 	EndIf
;~ EndFunc

Func executeSpotFarmScript($modelname, $real_map_name)
 	$step = False
     While True
         If $spotFarmRunning = True Then
             Sleep(1000)
 			$step = 1
             ContinueLoop
         EndIf
        
         If $step = 1 Then
             AddTextLog("Start spot again")
             ExitLoop
         EndIf
        
         Local $gameLanguage = TranslateLanguage($Setup_Main_Language)

		 Local $response = XF_2ndScript_Send("fromXF|farmingspot|" & $Setup_Main_VMName & "|" & $XF_image_folder & "\..|" & $real_map_name & "|" & $gameLanguage & "|" & $Setup_SpotFarm_AcceptPartyInvites & "|" & $Setup_Telegram_IsConfig & "|" & $XF_Username & "|" & $Setup_SpotFarm_CheckPartyLeader & "|" & $Setup_SpotFarm_CheckBestyaryEveryIfNotification & "|" & $Setup_SpotFarm_CheckBestyaryEveryIfNotificationNotFound & "|" & $modelname)
		;~  AddTextLog("SpotFarm response: " & $response)
         If $response = 'OK' Then
             $spotFarmRunning = True
             ContinueLoop
         EndIf
        
         
     WEnd
 EndFunc
