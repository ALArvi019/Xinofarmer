Global $g_bServerRunning = False

Func StartWebServer()
    ; Verifica si el servidor web ya está en ejecución
    If $g_bServerRunning Then
        AddTextLog("El servidor web ya está en ejecución.")
        Return
    EndIf

    ; First we set the callback functions for the three events (none of them is mandatory)
    _TCPServer_OnConnect("connected")
    _TCPServer_OnDisconnect("disconnect")
    _TCPServer_OnReceive("received")

    ; And some parameters
    _TCPServer_DebugMode(False)
    _TCPServer_SetMaxClients(10)

    ; Finally we start the server at port 9001 at any interface
    _TCPServer_Start(9001)

    $g_bServerRunning = True

    AddTextLog("The input log server is running OK.", "green")
EndFunc   ;==>StartWebServer

Func StopWebServer()
    ; Verifica si el servidor web no está en ejecución
    If Not $g_bServerRunning Then
        AddTextLog("El servidor web no está en ejecución.")
        Return
    EndIf

    ; Detiene el servidor web
    _TCPServer_Stop()

    $g_bServerRunning = False

    AddTextLog("El servidor web se ha detenido correctamente.")
EndFunc   ;==>StopWebServer

Func connected($iSocket, $sIP)
    ;~ AddTextLog( "Client " & $sIP & " connected1!")
    ;~ _TCPServer_Broadcast('new client connected guys', $iSocket)
    ;~ _TCPServer_Send($iSocket, "Hey! Write something ;)" & @CRLF)
    ;~ _TCPServer_SetParam($iSocket, "will write")
EndFunc   ;==>connected

Func received($iSocket, $sIP, $sData, $sPar)
    ;~ AddTextLog("Data received from " & $sIP & $sData & @CRLF & "Parameter: " & $sPar)
		;~ Data received from 127.0.0.1POST / HTTP/1.1
		;~ Host: 127.0.0.1:9001
		;~ User-Agent: python-requests/2.30.0
		;~ Accept-Encoding: gzip, deflate
		;~ Accept: */*
		;~ Connection: keep-alive
		;~ Content-Length: 36
		;~ Content-Type: application/x-www-form-urlencoded

		;~ message=aaaaa+bbbb+ccccc+ddddd+eeeee
		;~ Parameter: 0

	;~ get the message from request
	Local $aLines = StringSplit($sData, @CRLF, 1)
	; Recorrer cada línea y verificar si comienza con "message"
	For $i = 1 To $aLines[0]
		If StringLeft($aLines[$i], 6) = 'fromxf' Then
			;~ delete fromxf= from the string
			$sData = StringTrimLeft($aLines[$i], 7)
			;~ replace + to ' '
			$sData = StringReplace($sData, '+', ' ')
			;~ replace %20 to ' '
			$sData = StringReplace($sData, '%20', ' ')
			;~ replace %3A to ':'
			$sData = StringReplace($sData, '%3A', ':')
			;~ replace %2C to ','
			$sData = StringReplace($sData, '%2C', ',')
			;~ replace %2F to '/'
			$sData = StringReplace($sData, '%2F', '/')
			;~ replace %28 to '('
			$sData = StringReplace($sData, '%28', '(')
			;~ replace %29 to ')'
			$sData = StringReplace($sData, '%29', ')')
			;~ replace %7C to '|'
			$sData = StringReplace($sData, '%7C', '|')
			;~ replace %21 to '!'
			$sData = StringReplace($sData, '%21', '!')
			;~ replace %E2%86%91 to '↑'
			$sData = StringReplace($sData, '%E2%86%91', '↑')
			;~ replace %E2%86%93 to '↓'
			$sData = StringReplace($sData, '%E2%86%93', '↓')
			;~ replace %E2%86%90 to '←'
			$sData = StringReplace($sData, '%E2%86%90', '←')
			;~ replace %E2%86%92 to '→'
			$sData = StringReplace($sData, '%E2%86%92', '→')
			;~ replace %E2%86%96 to '↖'
			$sData = StringReplace($sData, '%E2%86%96', '↖')
			;~ replace %E2%86%97 to '↗'
			$sData = StringReplace($sData, '%E2%86%97', '↗')
			;~ replace %E2%86%99 to '↙'
			$sData = StringReplace($sData, '%E2%86%99', '↙')
			;~ replace %E2%86%98 to '↘'
			$sData = StringReplace($sData, '%E2%86%98', '↘')
			;~ replace %5B to '['
			$sData = StringReplace($sData, '%5B', '[')
			;~ replace %5D to ']'
			$sData = StringReplace($sData, '%5D', ']')
			;~ replace %27 to '''
			$sData = StringReplace($sData, '%27', "'")
			;~ replace %3E to '>'
			$sData = StringReplace($sData, '%3E', '>')
			;~ replace %3C to '<'
			$sData = StringReplace($sData, '%3C', '<')
			;~ replace %2D to '-'
			$sData = StringReplace($sData, '%2D', '-')
			;~ replace %3F to '?'
			$sData = StringReplace($sData, '%3F', '?')
			;~ replace %25 to '%'
			$sData = StringReplace($sData, '%25', '%')


			;~ AddTextLog($sData, 'blue')

			;~ if string contains 'command|', get the command and execute it
			If StringInStr($sData, 'command|') Then
				;~ delete 'command|' from the string
				$sData = StringTrimLeft($sData, 8)
				;~ if $sData contains sendyellowdust or sendscrap
				If StringInStr($sData, 'sendyellowdust') Or StringInStr($sData, 'sendscrap') Or StringInStr($sData, 'sendactualiter') Then
					;~ split the string by '|'
					Local $aArray = StringSplit($sData, '|', 1)
					;~ set the command
					$sCommand = $aArray[1]
					;~ set the text
					$sData = $aArray[2]
					;~ call the function
					Call($sCommand, $sData)
				Else
					$sData = Call($sData)
				EndIf
			;~ {'fromxf': 'color|' + color + '|' + text}	
			ElseIf StringInStr($sData, 'color|') Then
				;~ delete 'color|' from the string
				$sData = StringTrimLeft($sData, 6)
				;~ split the string by '|'
				Local $aArray = StringSplit($sData, '|', 1)
				;~ set the color
				$sColor = $aArray[1]
				;~ set the text
				$sData = $aArray[2]
				;~ call the function
				AddTextLog($sData, $sColor)
				
			EndIf
		EndIf
	Next
    _TCPServer_Send($iSocket, "HTTP/1.0 200 OK" & @CRLF & _
                    "Content-Type: text/html" & @CRLF & @CRLF & _
                    "<h1>Xinofarmer server Works!</h1>")
    _TCPServer_Close($iSocket)
EndFunc   ;==>received

Func killProcessInPort($port)
	$Pid = GetprocessByPort($port)
	ProcessClose($Pid)
EndFunc

Func exitXFlisto()
	ShowMsgBox("You only can have one instance of XinoFarmer running at the same time.", "WARNING", $MB_SYSTEMMODAL, $hGUI)
	XF_2ndScript_CloseAndKill()
	Exit
EndFunc

Func GetprocessByPort($port)
	Local $iPID = Run(@ComSpec & " /c " & "netstat -aon | findstr :9001", @SystemDir, @SW_HIDE, $STDERR_CHILD + $STDOUT_CHILD)
    Local $sStdOut
    While 1
        $sStdOut &= StdoutRead($iPID)
        If @error Then ExitLoop
    WEnd
	Local $aArray = StringSplit($sStdOut, @CRLF, 1)
	Local $aArray2 = StringSplit($aArray[1], " ", 1)
	Local $iPID2 = $aArray2[UBound($aArray2) - 1]
	return $iPID2
EndFunc
