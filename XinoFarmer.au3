
#include ".\inc\includes.au3"

Global $XF_Version = "1.7.6"

 	;~ _log4a_SetEnable()
 	;~ _log4a_SetErrorStream()
 	;~ _log4a_SetMinLevel($LOG4A_LEVEL_TRACE)
 	;~ If @compiled Then _log4a_SetMinLevel($LOG4A_LEVEL_WARN) ; Change the min level if the script is compiled
 	;~ _log4a_SetFormat("${date} | ${host} | ${level} | ${message}")
 	;~ _log4a_SetOutput($LOG4A_OUTPUT_FILE)


;~ _log4a_Trace("A TRACE message", True) ; overrides filters
;~ _log4a_Debug("A DEBUG message")
;~ _log4a_Info("A INFO message")
;~ _log4a_Warn("A WARN message")
;~ _log4a_Error("A ERROR message", True) ; overrides filters
;~ _log4a_Fatal("A FATAL message")


;~ check if the script is running from the new version
If $CmdLine[0] = 1 And $CmdLine[1] <> "" Then
	;~ if the script is running from the new version, then delete the old version
	FileDelete($CmdLine[1])
EndIf

XF_2ndScript_CloseAndKill()

;~ XF_CheckIfScriptIsRunnung()
If _CheckForUpdates() = True Then
	_CheckForFiles()
	XF_2ndScript_CheckIfScriptIsRunnung()
	_ShowLoginScreen()
EndIf

;~ Func XF_CheckIfScriptIsRunnung()
;~ 	;~ search this names XinoFarmer_$XF_Version.exe XinoFarmer.exe xinofarmer.exe  
;~ 	$aProcesses = ProcessList("XinoFarmer.exe")
;~ 	If $aProcesses[0][0] > 0 Then
;~ 		MsgBox(16, "Error", "XinoFarmer is already running")
;~ 		Exit
;~ 	EndIf
;~ 	$aProcesses = ProcessList("XinoFarmer_" & $XF_Version & ".exe")
;~ 	If $aProcesses[0][0] > 0 Then
;~ 		MsgBox(16, "Error", "XinoFarmer is already running")
;~ 		Exit
;~ 	EndIf
;~ EndFunc