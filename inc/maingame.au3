#include <Array.au3>
#include 'UDF/JSON.au3'



Func ExecuteMainGameLoop()
	AddTextLog( "ExecuteMainGameLoop")
	Local $count = 0
	While 1
		$windowPos = GetPositionOfWindow($Setup_Main_VMName)
		;~ set active window
		WinActivate($Setup_Main_VMName)
		Local $resp = checkWhatWindowIsOpen()
		If $resp = -1 Then
			$count = $count + 1
			$masterCount = $masterCount + 1
			If $masterCount = 100 Then
				AddTextLog( "STuck Open Game")
				RunWait($Setup_Main_LDPath & " reboot --name " & $Setup_Main_VMName, "", @SW_MAXIMIZE)
				$masterCount = 0
			EndIf
			If $count = 10 Then
				AddTextLog( "Restarting game")
				Main()
				$count = 0
			EndIf
		Else
			$masterCount = 0
			$count = 0
		EndIf
	WEnd
EndFunc


Func checkWhatWindowIsOpen() 
	$oJson = Json_Decode($JSON_screens)
	AddTextLog( "Checking what window is open")
	Local $SCREENS = Json_Get($oJson, '.screens')
	Local $language = TranslateLanguage($Setup_Main_Language)
	;~ Local $array[UBound($SCREENS)][3]
	For $i = 0 To UBound($SCREENS) - 1 Step 1
		Local $screenName = Json_Get($oJson, '.screens' & '[' & $i & '].name')
		Local $functionName = Json_Get($oJson, '.screens' & '[' & $i & '].function')
		Local $positions = Json_Get($oJson, '.screens' & '[' & $i & '].positions')
		Local $imagesToFind = Json_Get($oJson, '.screens' & '[' & $i & '].images_to_find')
		Local $ScreenFound = False
		
		For $z = 0 To UBound($positions) - 1 Step 1
				Local $x = Json_Get($oJson, '.screens' & '[' & $i & '].positions' & '[' & $z & '].x')
				Local $y = Json_Get($oJson, '.screens' & '[' & $i & '].positions' & '[' & $z & '].y')
				Local $color = Json_Get($oJson, '.screens' & '[' & $i & '].positions' & '[' & $z & '].color')
				;~ DEBUG CODE COLOR ----------------->
				If $screenName = "main_screen111" Then
					$windowPos = GetPositionOfWindow($Setup_Main_VMName)
					MouseMove($windowPos[0], $windowPos[1])
					Sleep(5000)
					MouseMove($x + $windowPos[0], $y + $windowPos[1])
					_GUICtrlEdit_AppendText($cEdit , "Position: " & $x & " " & $y)
					AddTextLog( "Color: " & $color)
					AddTextLog( "Realcolor: " & "0x" & Hex(PixelGetColor($x + $windowPos[0], $y + $windowPos[1]), 6))
					AddTextLog( "---------------------------------")
				EndIf
				;~ DEBUG CODE COLOR ----------------->
				If CheckIfPositionContainsColor($x, $y, $color) Then
					$ScreenFound = True
				Else
					$ScreenFound = False
					;~ AddTextLog( "Not found position: " & $x & " " & $y & " " & $color)
					ExitLoop
				EndIf
		Next
		
		If ($ScreenFound) Then
			AddTextLog( "Found screen: " & $screenName, 'yellow')
			Call($functionName)
			ExitLoop
		Else
			WinActivate($Setup_Main_VMName)
		EndIf

	Next
	If $ScreenFound <> True Then
		For $i = 0 To UBound($SCREENS) - 1 Step 1
			Local $imagesToFind = Json_Get($oJson, '.screens' & '[' & $i & '].images_to_find')
			For $y = 0 To UBound($imagesToFind) - 1 Step 1
				Local $image = Json_Get($oJson, '.screens' & '[' & $i & '].images_to_find' & '[' & $y & '].image')
				If FindImageInScreen($image & '_' & $language, $XF_image_folder & "\screens")[0] <> False Then
					$ScreenFound = True
				Else
					$ScreenFound = False
					;~ AddTextLog( "Not found position: " & $x & " " & $y & " " & $color)
					ExitLoop
				EndIf
			Next
			If ($ScreenFound) Then
				AddTextLog( "Found match screen: " & $screenName)
				Call($functionName)
				ExitLoop
			Else
				WinActivate($Setup_Main_VMName)
			EndIf
		Next
	EndIf
	CheckLife()
	Sleep(5000)
	return -1
EndFunc

