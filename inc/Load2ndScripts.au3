Global $XF_2nd_process_name = "xf.exe"

Func XF_2ndScript_CloseAndKill()
	$aProcesses = ProcessList($XF_2nd_process_name)
	;~ $aProcesses = ProcessList('xf.exe')
	For $i = 1 To $aProcesses[0][0]
	  	ProcessClose($aProcesses[$i][1])
	Next
EndFunc

Func XF_2ndScript_CheckIfScriptIsRunnung()
	$aProcesses = ProcessList($XF_2nd_process_name)
	If $aProcesses[0][0] = 0 Then
		XF_2ndScript_Set_Path_variable()
		;~ Run(@ScriptDir & '\inc\scripts\xf.exe "fromXF"', "", @SW_HIDE)
		;~ Run(@ScriptDir & '\inc\scripts\' & $XF_2nd_process_name & ' "fromXF" "' & $XF_Username & '"', "")
		Run(@ScriptDir & '\inc\scripts\' & $XF_2nd_process_name & ' "fromXF" "' & $XF_Username & '"', "", @SW_HIDE)
		Return False
	EndIf
	Return True
EndFunc

Func XF_2ndScript_Set_Path_variable()
	$existingPath = EnvGet("PATH")
	$directoryToAdd = @ScriptDir & "\inc\data\dll"
	;~ check if directoryToAdd is in the PATH
	If StringInStr($existingPath, $directoryToAdd) = 0 Then
		$updatedPath = $existingPath & ";" & $directoryToAdd
		EnvSet("PATH", $updatedPath)
		EnvUpdate()
	EndIf
EndFunc

Func XF_2ndScript_Send($message, $retrys = 50)
	$protocol = "http"
	$domain = "127.0.0.1"
	$port = 9000
	$url = "/xf"

	; Definir las cabeceras
	dim $headers[1][2]
	$headers[0][0] = "Content-Type"
	$headers[0][1] = "text/plain"

	$response = SendHTTPRequest($protocol, $domain, $url, $port, "POST", $headers, $retrys, $message)

	; Mostrar la respuesta recibida desde Python
	;~ AddTextLog("Respuesta: " & $response)

	return $response
EndFunc