Func XF_Timers()
	XF_TimeLeft()
	XF_Timer()
	XF_ShutdowBot()
EndFunc

Func XF_TimeLeft()
	WinSetTitle($hGUI, "", "XinoFarmer - " & $XF_Username & " - " & XF_TimeLeft_Decrement($XF_LefTime) & " time left")
	;~ pingtoserver()
EndFunc

Func pingtoserver()
	dim $headers[1][2]
	$headers[0][0] = "Content-Type"
	$headers[0][1] = "application/x-www-form-urlencoded"
	return SendHTTPRequest("https", $XF_Domain, "/xf/register", 443, "POST", $headers, 3, "username=" & $username & "&password=" & $password)
EndFunc

Func XF_ShutdowBot()
	If $Setup_Main_StopBotAfter = 0 Then Return

	If TimerDiff($logEvery30Minutes) > 30 * 60 * 1000 Then
		$logEvery30Minutes = TimerInit()
		;~ ShowMsgBox("The bot will be stopped in " & $Setup_Main_StopBotAfter - Int(TimerDiff($StopBotAfter) / 60 / 60 / 1000) & " hours.", "Stop", $MB_SYSTEMMODAL, $hGUI)
		AddTextLog("The bot will be stopped in " & $Setup_Main_StopBotAfter - Int(TimerDiff($StopBotAfter) / 60 / 60 / 1000) & " hours.")
	EndIf

	;~ if the timer is expired, we stop the bot
	If TimerDiff($StopBotAfter) > $Setup_Main_StopBotAfter * 60 * 60 * 1000 Then
		$StopBotAfter = 0
		Stop()
		ShowMsgBox("The bot has been stopped because the time limit has been reached.", "Stop", $MB_SYSTEMMODAL, $hGUI)
		XF_2ndScript_CloseAndKill()
		Exit
	EndIf
EndFunc

Func XF_Timer()

	If $XF_Timer = 0 And $isStarted = True And $isPaused = False Then
		$XF_Timer = TimerInit()
		$XF_Timer = $XF_Timer + $XF_Last_Timer
	EndIf
	If $XF_Timer <> 0 And $isStarted = True And $isPaused = False Then
		; Obtener el tiempo transcurrido desde el inicio en milisegundos
		$timeInMilliseconds = TimerDiff($XF_Timer)

		; Convertir el tiempo a formato HH:MM:SS
		$timeInSeconds = Int($timeInMilliseconds / 1000)
		$hours = Int($timeInSeconds / 3600)
		$minutes = Int(($timeInSeconds - ($hours * 3600)) / 60)
		$seconds = $timeInSeconds - ($hours * 3600) - ($minutes * 60)
		$timeString = StringFormat("%02d:%02d:%02d", $hours, $minutes, $seconds)
	
		; Actualizar el label con el tiempo actualizado
		GUICtrlSetData($XF_Label_Running_Time, "Running time: " & $timeString)
	
		; Esperar un momento antes de continuar
		Sleep(50)
	EndIf
	If $XF_Timer <> 0 And $isStarted = True And $isPaused = True Then
		$XF_Last_Timer = TimerDiff($XF_Timer)
	 	$XF_Timer = 0
	EndIf
EndFunc

Func XF_TimeLeft_Decrement($XF_LefTime)
	$XF_LefTime = StringReplace($XF_LefTime, "-", "/")
	Local $difference = _DateDiff('s',_NowCalc(), $XF_LefTime)
	;~ if the difference is negative, return 0 days 00:00:00
	If $difference < 0 Then Return "0 days 00:00:00"
    Local $days = Int($difference / (24 * 60 * 60))
    Local $hours = Int(Mod($difference, (24 * 60 * 60)) / (60 * 60))
    Local $minutes = Int(Mod($difference, (60 * 60)) / 60)
    Local $seconds = Mod($difference, 60)
	Local $sFormatDays = StringFormat("%02i", $days)
	Local $sFormatHours = StringFormat("%02i", $hours)
	Local $sFormatMinutes = StringFormat("%02i", $minutes)
	Local $sFormatSeconds = StringFormat("%02i", $seconds)
	If $days = 0 And $hours = 0 And $minutes = 0 Then
		;~ Your period of use has expired, please renew your subscription
		ShowMsgBox("Your period of use has expired, please renew your subscription", "Error", $MB_SYSTEMMODAL, $hGUI)
		XF_2ndScript_CloseAndKill()
		Exit
	EndIf
    Return $sFormatDays & " days " & $sFormatHours & ":" & $sFormatMinutes & ":" & $sFormatSeconds
EndFunc

