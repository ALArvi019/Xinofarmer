
Func _CheckForUpdates()
	dim $headers[1][2]
	$headers[0][0] = "Content-Type"
	$headers[0][1] = "application/x-www-form-urlencoded"
	$sVersion = SendHTTPRequest("https", $XF_Domain, "/xf/version.txt", 443, "GET", $headers, 1)

	;~ delete all spaces
	$sVersion = StringRegExpReplace($sVersion, ' ', '')
	;~ execute replace
	$sVersion = StringRegExpReplace($sVersion, '{"version":"', '')
	$sVersion = StringRegExpReplace($sVersion, '"}', '')
	;~ check if the sVersion contains character "."
	If StringInStr($sVersion, ".") = 0 Then
		MsgBox(16, "Error", "Cannot check for updates, please try again later.")
		XF_2ndScript_CloseAndKill()
		Exit
	EndIf
	If $sVersion = $XF_Version Then
		Return True
	Else
		MsgBox(0, "Update", "There is a new version of XinoFarmer available, you have the version " & $XF_Version & " and the new version is " & $sVersion & ".")
		;~ delete MD5 from registry
		Local $aJson = Json_Decode($JSON_prepareFiles)
		Local $aFiles =  Json_Get($aJson, ".files")
		For $i = 0 To UBound($aFiles) - 1
			Local $sPath = Json_Get($aJson, ".files[" & $i & "].path")
			DeleteDataFromTheRegistry($sPath)
		Next
		_DownloadNewVersionNew($sVersion, "https://" & $XF_Domain & "/sites/all/modules/aaa_custom_diablo/src/XinoFarmer.exe", @ScriptDir & "\XinoFarmer_" & $sVersion & ".exe")
	EndIf
EndFunc

Func _DownloadNewVersionNew($sVersion, $url, $destino, $reintentos = 3)
    Local $intentosActuales = 0
    Local $archivoTemporal = @TempDir & "\tempfilexf.tmp"
    Local $tiempoInicio = TimerInit()
    Local $tiempoTranscurrido = 0
    Local $archivoDescargado = False
    Local $tamanoArchivo = 0
    Local $hdownload = 0
    
    $hGUIDownload = GUICreate("Downloading version " & $sVersion, 400, 120) 
    $hProgress = GUICtrlCreateProgress(10, 40, 380, 20)
	;~ show Label in te left
    $hLabelTiemporestante = GUICtrlCreateLabel("", 10, 70, 380, 20)
	;~ show Label in te right
	$hLabelTamanioRestante = GUICtrlCreateLabel("", 10, 90, 380, 20)

	;~ if  press X button, exit
	GUISetOnEvent($GUI_EVENT_CLOSE, "_ExitDownload")
    
    GUISetState(@SW_SHOW)

	; Obtener el tamaño del archivo
	$tamanoArchivo = InetGetSize($url, $INET_FORCERELOAD + $INET_IGNORESSL)
	If $tamanoArchivo = -1 Then
		MsgBox($MB_OK, "Error", "Cannot get the size of the file, please try again later.")
		Return
	EndIf
    ; Descargar el archivo usando InetGet
    $hdownload = InetGet($url, $archivoTemporal, $INET_FORCERELOAD, 1)
    
    ; Esperar hasta que la descarga se complete o falle
    While InetGetInfo($hDownload, 3) <> True
        Sleep(250)
        
        ; Obtener la información de la descarga actual
        Local $downloadBytes = InetGetInfo($hDownload, 0) ; Bytes read so far (this is updated while the download progresses).

		$tiempoTranscurrido = TimerDiff($tiempoInicio)
        
        ; Actualizar la barra de progreso, mostrar el tiempo estimado restantey mostar el tamaño restante
        If $downloadBytes > 0 Then
            Local $porcentaje = Round(($downloadBytes / $tamanoArchivo) * 100)
            If $porcentaje > 0 And $tiempoTranscurrido > 0 Then
                Local $tiempoRestante = ($tiempoTranscurrido / $porcentaje) * (100 - $porcentaje)
				$tamanioRestante = $tamanoArchivo - $downloadBytes
				GUICtrlSetData($hLabelTamanioRestante, "Size remaining: " & Round($tamanioRestante / 1024 / 1024, 2) & " MB")
				GUICtrlSetData($hProgress, $porcentaje)
                GUICtrlSetData($hLabelTiemporestante, "Time remaining: " & SegundosAHoras($tiempoRestante / 1000))
            EndIf
        EndIf

		; Verificar si el tamaño de la descarga es el mismo durante 2 minutos
		If $tiempoTranscurrido > 600000 Then
			If $downloadBytes = InetGetInfo($hDownload, 0) Then
				$intentosActuales += 1
				If $intentosActuales > $reintentos Then
					MsgBox($MB_OK, "Error", "The download of the new version has failed.")
					ExitLoop
				EndIf
			Else
				$intentosActuales = 0
			EndIf
		EndIf
        
        ; Verificar si la descarga se completó
        If InetGetInfo($hDownload, 2) Then
			$archivoDescargado = True
			ExitLoop
		EndIf
        
    WEnd
    
    ; Verificar si la descarga fue exitosa
    If FileExists($archivoTemporal) Then
        Local $tamanoDescargado = FileGetSize($archivoTemporal)
        If $tamanoDescargado = $tamanoArchivo Then
            FileMove($archivoTemporal, $destino, $FC_OVERWRITE)
        EndIf
    EndIf

	InetClose($hdownload)
    
    GUIDelete($hGUIDownload)
    
    If $archivoDescargado Then
        ;~ MsgBox($MB_OK, "Download completed", "The new version has been downloaded successfully, please run the new version if not run automatically. PLEASE BE PATIENT, THE FIRST RUN CAN TAKE A FEW MINUTES.")
		; Centre the single button
		_ExtMsgBoxSet(1, 4, -1 , 0xFF0000, 12)
		$sMsg = "The version " & $sVersion & " has been downloaded successfully and now will be extracted." & @CRLF & @CRLF
		$sMsg &= "PLEASE BE PATIENT, THE FIRST RUN CAN TAKE A FEW MINUTES !!!" & @CRLF & @CRLF
		$sMsg &= "If the bot doesn't start automatically in more than 5 minutes, please run it manually." & @CRLF & @CRLF
		$iRetValue = _ExtMsgBox($EMB_ICONSTOP, "Ok", "Download completed", $sMsg, 15)
		_ExtMsgBoxSet(Default)
    EndIf

	_RunNewVersion($sVersion)
EndFunc

Func _ExitDownload()
	MsgBox($MB_OK, "Error", "User has canceled the download.")
	XF_2ndScript_CloseAndKill()
	Exit
EndFunc

Func SegundosAHoras($segundos)
	Local $horas = Int($segundos / 3600)
	Local $minutos = Int(($segundos - ($horas * 3600)) / 60)
	$segundos = Int($segundos - ($horas * 3600) - ($minutos * 60))
	
	Return StringFormat("%02d:%02d:%02d", $horas, $minutos, $segundos)
EndFunc
	
Func _DownloadFile($sURL, $sFile)
	;~ get the directory of the script
	Local $sDir = @ScriptDir

	Local $sDestFile = $sDir & $sFile

	Local $hDownload = InetGet($sURL, $sDestFile, $INET_FORCERELOAD, 1)
	If @error Then
		ShowMsgBox("The download has failed, please try again later.", "Error", 16, $hGUIDownload)
		XF_2ndScript_CloseAndKill()
		Exit
	EndIf
	return $hDownload
EndFunc

Func FileGetMD5($sFile)
	Local $sCommand = @ScriptDir & '\inc\scripts\certutil.exe -hashfile "' & $sFile & '" MD5'
	Local $iPID = Run($sCommand, @ScriptDir, @SW_HIDE, $STDERR_CHILD + $STDOUT_CHILD)
	Local $sOutput = ""

	$actualtime = TimerInit()
	While 1
		$sTempOutput = StdoutRead($iPID)
		If Not @error Then $sOutput &= $sTempOutput
		If @error Then ExitLoop
		If TimerDiff($actualtime) > 5000 Then
			ProcessClose($iPID)
			ExitLoop
		EndIf
	WEnd

	_log4a_Debug("FileGetMD5: " & $sFile)
	_log4a_Debug("FileGetMD5: " & $sOutput)

	Local $aLines = StringSplit($sOutput, @LF)

	For $i = 1 To $aLines[0]
		If StringRegExp($aLines[$i], "^[0-9a-fA-F]*$", 0) = 1 Then
			;~ get the MD5
			$sOutput = $aLines[$i]
			;~ exit the loop
			ExitLoop
		EndIf
	Next

	$sOutput = StringRegExpReplace($sOutput, "[\s\r\n]+", "")
	 
	Return $sOutput

EndFunc

Func _RunNewVersion($sVersion)
	;~ check if @ScriptDir & "\inc" exists
	If FileExists(@ScriptDir & "\inc") Then
		;~ remove @ScriptDir & "\inc\ folder
		If DirRemove(@ScriptDir & "\inc", 1) = 0 Then
			MsgBox(16, "Error", "Cannot remove the /inc folder, please remove manually and restart the bot.")
			XF_2ndScript_CloseAndKill()
			Exit
		EndIf
	EndIf

	;~ run the new version and pass as parameter the old script path
	Run("XinoFarmer_" & $sVersion & ".exe" & " " & @ScriptFullPath)
	;~ exit the script
	Exit
EndFunc
#include <File.au3>

Func Explore_Main_LDPath()
	If $GUI_LDPath <> "" Then
		Local $initialDir = $GUI_LDPath
	Else
		Local $initialDir = @ScriptDir
	EndIf
    Local $sFile = FileOpenDialog("Seleccionar archivo ldconsole.exe", $initialDir, "Archivos ejecutables (*.exe)", 1, "ldconsole.exe")
    If Not @error Then
        GUICtrlSetData($GUI_LDPath, $sFile)
    EndIf
EndFunc
