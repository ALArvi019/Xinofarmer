Global $sDATAMAIN = ''

While 1
	Local $response = ConsoleRead()
	;~ check if response is empty

	If $sDATAMAIN = "" Then
		$sDATAMAIN = $response
	EndIf
	Sleep(1000)
	ConsoleWrite($sDATAMAIN & @CRLF)  ; Send progress to Main Process
WEnd