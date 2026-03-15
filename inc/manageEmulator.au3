Func CheckIfEmulatorIsOpen()
	If Not CheckProgramIsOpenByTitle($Setup_Main_VMName) Then
	 	AddTextLog( "Emulator is not Open, the name is " & $Setup_Main_VMName & "?")
		;~ execute OpenTheLauncher() function and wait for it to finish
		OpenTheEmulator()
	EndIf
	OrderWindows()
	PrepareDiabloWindow()
EndFunc

Func OrderWindows()
	;~ get the window handle of the emulator and set always on top
	$EmulatorWindow = WinGetHandle($Setup_Main_VMName)
	WinSetOnTop($EmulatorWindow, "", 1)
	;~ get the window handle of the emulator and set always on top
	$XinoWindow = WinGetHandle($hGUI)
	WinSetOnTop($XinoWindow, "", 1)

	;~ the emulator windows is 960x540 and the xino window is 650x340 so we need to move the emulator window to the top and xino window to the bottom whitout separating them
	$middleOfHorizontalScreen = @DesktopWidth / 2 - 960 / 2
	$middleOfVerticalScreen = (@DesktopHeight / 2 - 540 / 2) - 340 / 2

	WinMove($EmulatorWindow, "", $middleOfHorizontalScreen, $middleOfVerticalScreen)
	WinMove($XinoWindow, "", $middleOfHorizontalScreen, $middleOfVerticalScreen + 540)
	Sleep(2000)

EndFunc

Func OpenTheEmulator() 
	;~ execute C:\LDPlayer\LDPlayer9\ldconsole.exe launch --name $Setup_Main_VMName command
	AddTextLog( "Opening emulator...")
	RunWait($Setup_Main_LDPath & " launch --name " & $Setup_Main_VMName, "", @SW_MAXIMIZE)
	Sleep(15000)
	CheckIfEmulatorIsOpen()
EndFunc

Func PrepareDiabloWindow()
	AddTextLog( "Emulator is open.")
	;~ get the window handle of the emulator and set always on top
	$EmulatorWindow = WinGetHandle($Setup_Main_VMName)
	If XF_CheckSizeOfWindow($Setup_Main_VMName, 1002, 575) = False And XF_CheckSizeOfWindow($Setup_Main_VMName, 962, 575) = False Then
		MsgBox(16, "Error", "The emulator LDPlayer window is not the correct size, please configure it to 960x540 and try again.")
		XF_2ndScript_CloseAndKill()
		Exit
	EndIf
	WinSetOnTop($EmulatorWindow, "", 1)
	;~ set to topmost
	;~ execute C:\LDPlayer\LDPlayer9\ldconsole.exe runapp --name $Setup_Main_VMName --packagename com.blizzard.diablo.immortal
	RunWait($Setup_Main_LDPath & " runapp --name " & $Setup_Main_VMName & " --packagename com.blizzard.diablo.immortal", "", @SW_MAXIMIZE)
EndFunc