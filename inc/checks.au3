;~ XF_CheckSizeOfWindow($EmulatorWindow, 960, 540)
Func XF_CheckSizeOfWindow($EmulatorWindow, $Width, $Height)
	Local $EmulatorWindowWidth = WinGetPos($EmulatorWindow)[2]
	Local $EmulatorWindowHeight = WinGetPos($EmulatorWindow)[3]
	If $EmulatorWindowWidth = $Width And $EmulatorWindowHeight = $Height Then
		Return True
	Else
		Return False
	EndIf
EndFunc