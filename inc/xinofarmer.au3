Func XF_Openbot()

	GUIDelete($hGUILogin)

	;~ XF_2ndScript_CheckIfScriptIsRunnung()

	XF_CreateGUI()

	AdlibRegister('XF_Timers', 1000)

	CustomModelActive()

	AddTextLog('Checking computer vision script...')
	If XF_2ndScript_Send('XF_2ndScript_Start') = 'XF_2ndScript_Start' Then
		AddTextLog('Computer vision script is running OK.', "green")
		enableOrDisableButtons('enable')
		killProcessInPort(9001)
		StartWebServer()
	Else
		AddTextLog('Computer vision script is not running.', "red")
		ShowMsgBox("Computer vision script is not running. Is the port 9000 free?", "Error", 16, $hGUI)
		XF_2ndScript_CloseAndKill()
		Exit
	EndIf
	If XF_2ndScript_Send('XF_2ndScript_Version') = $XF_Version Then
		AddTextLog('Version of computer vision script is OK.', "green")
	Else
		AddTextLog('Version of computer vision script is not OK. Restart the bot.', "red")
		ShowMsgBox("Version of computer vision script is not OK. Restart the bot.", "Error", 16, $hGUI)
		If FileExists(@ScriptDir & "\inc") Then
			If @compiled Then
				If DirRemove(@ScriptDir & "\inc", 1) = 0 Then
					ShowMsgBox("Cannot remove the /inc folder, please remove manually and restart the bot.", "Error", 16, $hGUI)
					XF_2ndScript_CloseAndKill()
					Exit
				EndIf
			Else
				ShowMsgBox("Cannot remove the /inc folder, please remove manually and restart the bot.", "Error", 16, $hGUI)
				XF_2ndScript_CloseAndKill()
				Exit
			EndIf
		EndIf
		Exit
	EndIf
	If XF_2ndScript_Send('XF_2ndScript_chUser|' & $XF_Username) = 'OK' Then
		AddTextLog('Username is OK.', "green")
	EndIf

	telegram_CheckUserIsConfig()
	FishZonesSelect()

	While 1
		
	Wend

EndFunc