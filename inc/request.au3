Func SendHTTPRequest($protocol, $domain, $url, $port, $type, $headers, $retry, $body="")
    Local $requestType = StringUpper($type)
    If $requestType <> "GET" And $requestType <> "POST" Then
		ShowMsgBox("Invalid request type: " & $requestType, "Error", 16, $hGUI)
        Return ""
    EndIf

    If $protocol <> "http" And $protocol <> "https" Then
		ShowMsgBox("Invalid protocol: " & $protocol, "Error", 16, $hGUI)
        Return ""
    EndIf

    Local $httpRequest = 0
    Local $httpConnect = 0
    Local $httpSession = _WinHttpOpen("AutoIt", $WINHTTP_ACCESS_TYPE_DEFAULT_PROXY, $WINHTTP_NO_PROXY_NAME, $WINHTTP_NO_PROXY_BYPASS)
    If Not $httpSession Then
		ShowMsgBox("Failed to open WinHTTP session: " & @error, "Error", 16, $hGUI)
        Return ""
    EndIf

    Local $requestFlags = BitOR($WINHTTP_FLAG_REFRESH, $WINHTTP_FLAG_SECURE)
    If $protocol = "http" Then
        $requestFlags = BitAND($requestFlags, BitNot($WINHTTP_FLAG_SECURE))
    EndIf

    $httpConnect = _WinHttpConnect($httpSession, $domain, $port)
    If Not $httpConnect Then
        ;~ ConsoleWrite("Failed to connect to " & $protocol & "://" & $domain & ":" & $port & ": " & @error & @CRLF)
		ShowMsgBox("Failed to connect to httpSession : " & @error, "Error", 16, $hGUI)
        _WinHttpCloseHandle($httpSession)
        Return ""
    EndIf

    Local $retryCount = 0
    While $retryCount < $retry
        $httpRequest = _WinHttpOpenRequest($httpConnect, $requestType, $url, Default, Default, Default, $requestFlags)
        If Not $httpRequest Then
			ShowMsgBox("Failed to open WinHTTP request : " & @error, "Error", 16, $hGUI)
            ExitLoop
        EndIf

        If $headers <> "" Then
			For $i = 0 To UBound($headers) - 1
				_WinHttpAddRequestHeaders($httpRequest, $headers[$i][0] & ": " & $headers[$i][1], $WINHTTP_ADDREQ_FLAG_ADD)
			Next
		EndIf

		GenerateHttpTimezoneHeader($httpRequest)

		Local $sendResult = _WinHttpSendRequest($httpRequest, Default, $body)

        Local $recvResult = _WinHttpReceiveResponse($httpRequest)
        If Not $recvResult Then
			If $domain = "127.0.0.1" Then
				If $retryCount = 20 Or $retryCount = 40 Then
					XF_2ndScript_CloseAndKill()
				EndIf
				XF_2ndScript_CheckIfScriptIsRunnung()
				AddTextLog("Retrying to connect to the server. ( " & $retryCount + 1 & "/" & $retry & " )", "red")
				_WinHttpCloseHandle($httpRequest)
				$httpRequest = 0
				$retryCount += 1
				Sleep(5000)
				ContinueLoop
			Else
				ShowMsgBox("Failed to receive WinHTTP response : " & @error, "Error", 16, $hGUI)
				ExitLoop
			EndIf
        EndIf

        Local $status = _WinHttpQueryHeaders($httpRequest, $WINHTTP_QUERY_STATUS_CODE)
        If $status <> 200 Then
			If $status = 423 And $domain = "127.0.0.1" Then
				XF_2ndScript_CloseAndKill()
				XF_2ndScript_CheckIfScriptIsRunnung()
				AddTextLog("Retrying to connect to the server. ( " & $retryCount + 1 & "/" & $retry & " )")
				Sleep(5000)
			Else
				ShowMsgBox("HTTP status code " & $status & " received", "Error", 16, $hGUI)
			EndIf
            _WinHttpCloseHandle($httpRequest)
            $httpRequest = 0
            $retryCount += 1
			Sleep(5000)
		Else
			ExitLoop
		EndIf

	WEnd

	If $retryCount >= $retry Then
			AddTextLog("Can't connect to the server, please try again later.")
			ShowMsgBox("Can't connect to the server, please try again later.", "Error", 16, $hGUI)
			_WinHttpCloseHandle($httpRequest)
			_WinHttpCloseHandle($httpConnect)
			_WinHttpCloseHandle($httpSession)
			XF_2ndScript_CloseAndKill()
			Exit
	EndIf

	Local $response = _WinHttpReadData($httpRequest)
	_WinHttpCloseHandle($httpRequest)
	_WinHttpCloseHandle($httpConnect)
	_WinHttpCloseHandle($httpSession)
	Return $response
EndFunc


Func GenerateHttpTimezoneHeader($httpRequest)
	$year = @YEAR
	$month = StringFormat("%02d", @MON)
	$day = StringFormat("%02d", @MDAY)
	$hour = StringFormat("%02d", @HOUR)
	$minute = StringFormat("%02d", @MIN)
	$second = StringFormat("%02d", @SEC)

	; Combine the date and time into a string
	$datetime = $year & $month & $day & $hour & $minute & $second

	; Generate the signature
	Local $EncryptedSignature = _Cryptshun($datetime)

	; Obtener la información de la zona horaria actual
	$timezoneInfo = _Date_Time_GetTimeZoneInformation()
	If $timezoneInfo[0] = -1 Then
		ShowMsgBox("Can't get the timezone information. Please check your system.", "Error", 16, $hGUI)
		XF_2ndScript_CloseAndKill()
		Exit
	EndIf

	; Calcular la zona horaria actual a partir de la información obtenida
	$timezoneOffset = -($timezoneInfo[1] / 60)
	If $timezoneOffset >= 0 Then
		$timezoneOffset = "+" & $timezoneOffset
	EndIf
	$timezoneName = $timezoneInfo[2]
	$timezone = "GMT" & $timezoneOffset

	_WinHttpAddRequestHeaders($httpRequest, "X-Auth: " & $EncryptedSignature, $WINHTTP_ADDREQ_FLAG_ADD)
	_WinHttpAddRequestHeaders($httpRequest, "X-Timezone: " & $timezone, $WINHTTP_ADDREQ_FLAG_ADD)

	Return True
EndFunc