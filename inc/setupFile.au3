Func ReadSetupFile()

	Local $INIFIlesexist = FileExists(@ScriptDir & "\setup.ini")

	Local $oJson = Json_Decode($JSON_setup)
	Local $SETOPJSON = Json_Get($oJson, '.setup')

	;~ get the total vlues for create array
	Local $iTotalValues = 0
	Local $jTotalValues = 0
	For $i = 0 To UBound($SETOPJSON) - 1 Step 1
		Local $SETOPJSON2 = Json_Get($oJson, '.setup[' & $i & '].values')
		$iTotalValues = $iTotalValues + 1
		For $j = 0 To UBound($SETOPJSON2) - 1 Step 1
			$jTotalValues = $jTotalValues + 1
		Next
	Next

	dim $oSetup[$iTotalValues][$jTotalValues][4]

	For $i = 0 To UBound($SETOPJSON) - 1 Step 1
		Local $SETOPJSON2 = Json_Get($oJson, '.setup[' & $i & '].values')
		For $j = 0 To UBound($SETOPJSON2) - 1 Step 1
			Local $iniGroup = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].iniGroup')
			Local $iniProp = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].iniProp')
			Local $defaultValue = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].defaultValue')
			If $INIFIlesexist Then
				$oSetup[$i][$j][0] = $iniGroup
				$oSetup[$i][$j][1] = $iniProp
				$oSetup[$i][$j][2] = $defaultValue
				$oSetup[$i][$j][3] = IniRead(@ScriptDir & "\setup.ini", $iniGroup, $iniProp, $defaultValue)
			Else
				IniWrite(@ScriptDir & "\setup.ini", $iniGroup, $iniProp, $defaultValue)
				$oSetup[$i][$j][0] = $iniGroup
				$oSetup[$i][$j][1] = $iniProp
				$oSetup[$i][$j][2] = $defaultValue
				$oSetup[$i][$j][3] = IniRead(@ScriptDir & "\setup.ini", $iniGroup, $iniProp, $defaultValue)
			EndIf
		Next
	Next

	Return $oSetup

EndFunc

Func WriteSetupFile($type , $data)
	Local $oJson = Json_Decode($JSON_setup)
	Local $SETOPJSON = Json_Get($oJson, '.setup')
	For $i = 0 To UBound($SETOPJSON) - 1 Step 1
		Local $SETOPJSON2 = Json_Get($oJson, '.setup[' & $i & '].values')
		For $j = 0 To UBound($SETOPJSON2) - 1 Step 1
			Local $iniGroup = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].iniGroup')
			Local $iniProp = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].iniProp')
			Local $defaultValue = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].defaultValue')
			If $type = $iniGroup & "_" & $iniProp Then
				$setupFile = IniWrite(@ScriptDir & "\setup.ini", $iniGroup, $iniProp, $data)
				Return
			EndIf
		Next
	Next
EndFunc

Func OverWriteFileINI()
	Local $oJson = Json_Decode($JSON_setup)
	Local $SETOPJSON = Json_Get($oJson, '.setup')
	For $i = 0 To UBound($SETOPJSON) - 1 Step 1
		Local $SETOPJSON2 = Json_Get($oJson, '.setup[' & $i & '].values')
		For $j = 0 To UBound($SETOPJSON2) - 1 Step 1
			;~ $Setup_Main_Action = GUICtrlRead($GUI_Action)
			;~ WriteSetupFile('Main_VMName', $Setup_Main_VMName)
			Local $iniGroup = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].iniGroup')
			Local $iniProp = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].iniProp')
			Local $GUIVariable = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUIVariable')
			Local $GUITypeField = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUITypeField')
			Local $GUIValue = GUICtrlRead(Eval($GUIVariable))
			If $GUITypeField <> "internal" Then
				If $GUIVariable = "GUI_Action" Then
					If $GUIValue <> $Setup_Main_Action Then 
						$XF_ActualDifficult = "init"
					EndIf
				EndIf
				;~ If $GUIVariable = "GUI_FarmDifficulty" Then
				;~ 	If $GUIValue <> $Setup_Farm_Difficulty Then 
				;~ 		$XF_ActualDifficult = "init"
				;~ 	EndIf
				;~ EndIf
				If $GUIVariable = "GUI_FishDifficult" Then
					If $GUIValue <> $Setup_Fish_Difficult Then 
						$XF_ActualDifficult = "init"
					EndIf
				EndIf
				WriteSetupFile($iniGroup & "_" & $iniProp, $GUIValue)
				;~ set the value to the variable Eval("Setup_" & $iniGroup & "_" & $iniProp)
				Eval("Setup_" & $iniGroup & "_" & $iniProp & " = " & $GUIValue)
			EndIf
		Next
	Next

	InitialSetupFile()

EndFunc


Func XF_CreateGUI()

	Opt("GUIOnEventMode", 1)

	;~ create the GUI title XinoFarmer & $XF_Username
	$hGUI = GUICreate("XinoFarmer - " & $XF_Username & " - Your bot stops at " & $XF_LefTime, 650, 340)

	GUISetOnEvent($GUI_EVENT_CLOSE, "Terminate")

	;~ create edit and set read only with _GUICtrlRichEdit_Create
	$cEdit = _GUICtrlRichEdit_Create($hGUI, "", 10, 10, 250, 290, BitOR($ES_READONLY, $ES_MULTILINE, $ES_AUTOVSCROLL, $ES_AUTOHSCROLL))
	GUICtrlSetLimit($cEdit, 15000)

	GUICtrlCreateLabel("Version: " & $XF_Version, 5, 313, 100, 20)

	$XF_Label_Running_Time = GUICtrlCreateLabel("Running time: 00:00:00", 170, 313, 150, 20)
	;~ set the window to be always on top
	WinSetOnTop($hGUI, "", 1)

	Local $oJson = Json_Decode($JSON_setup)

	;~ CREATE GENERAL TAB
	Local $oGeneralTab = Json_Get($oJson, '.tab')
	If Json_Get($oJson, '.tab.generalTab[0].name') <> "" And Json_Get($oJson, '.tab.generalTab[0].values') <> "" Then
		$pPalTb = Json_Get($oJson, '.tab.generalTab')
		For $i = 0 To UBound($pPalTb) - 1 Step 1
			Local $value1 = Json_Get($oJson, '.tab.generalTab[' & $i & '].values[0]')
			Local $value2 = Json_Get($oJson, '.tab.generalTab[' & $i & '].values[1]')
			Local $value3 = Json_Get($oJson, '.tab.generalTab[' & $i & '].values[2]')
			Local $value4 = Json_Get($oJson, '.tab.generalTab[' & $i & '].values[3]')
			If $value1 <> "" And $value2 <> "" And $value3 <> "" And $value4 <> "" Then
				$GUI_Tab = GUICtrlCreateTab($value1, $value2, $value3, $value4)
			EndIf
		Next
	EndIf

	;~  CREATE BUTTONS
	 Local $oButtons = Json_Get($oJson, '.buttons')
	 If Json_Get($oJson, '.buttons.guibuttons[0].name') <> "" And Json_Get($oJson, '.buttons.guibuttons[0].values') <> "" Then
	 	$oGUIButtons = Json_Get($oJson, '.buttons.guibuttons')
	 	For $i = 0 To UBound($oGUIButtons) - 1 Step 1
	 		Local $name = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].name')
	 		Local $value1 = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].values[0]')
	 		Local $value2 = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].values[1]')
	 		Local $value3 = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].values[2]')
	 		Local $value4 = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].values[3]')
	 		Local $value5 = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].values[4]')
	 		Local $callbak = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].callback')
	 		Local $hide = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].hide')
	 		Local $hotkey = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].hotkey')
	 		Local $hotkeyFunc = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].hotkeyFunc')
	 		If $name <> "" And $value1 <> "" And $value2 <> "" And $value3 <> "" And $value4 <> "" And $value5 <> "" And $callbak <> "" Then
	 			$dynamicVariableNameButton = "Button_" & $name
	 			Global $dynamicVariableNameButton
	 			Assign($dynamicVariableNameButton, GUICtrlCreateButton($value5, $value1, $value2, $value3, $value4), $ASSIGN_FORCEGLOBAL)
	 			If $hide = "true" Then
	 				GUICtrlSetState(Eval($dynamicVariableNameButton), $GUI_HIDE)
	 			EndIf
	 			
				;~ set buttons to inactive
				enableOrDisableButtons("disable")
	 		EndIf
	 	Next
	 EndIf

	;~ CREATE GUI ITEMS
	Local $SETOPJSON = Json_Get($oJson, '.setup')
	For $i = 0 To UBound($SETOPJSON) - 1 Step 1
		Local $TabName = Json_Get($oJson, '.setup[' & $i & '].name')
		Local $SETOPJSON2 = Json_Get($oJson, '.setup[' & $i & '].values')
		If (Json_Get($oJson, '.setup[' & $i & '].values[0].GUITypeField')) <> "internal" Then
			;~ delete al whitespaces and set all to lowercase
			$TabName_proc = StringLower(StringReplace($TabName, " ", ""))
			Assign("GUI_Tab_" & $TabName_proc, GUICtrlCreateTabItem(CapitalLetter($TabName)), $ASSIGN_FORCEGLOBAL)
		EndIf
		For $j = 0 To UBound($SETOPJSON2) - 1 Step 1
			Local $iniGroup = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].iniGroup')
			Local $iniProp = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].iniProp')
			Local $defaultValue = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].defaultValue')
			Local $GUILabel = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUILabel')
			Local $GUILabelPosition = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUILabelPosition')
			Local $GUIVariable = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUIVariable')
			Local $GUITypeField = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUITypeField')
			Local $GUIComboValues = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUIComboValues')
			Local $GUIVariablePosition = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUIVariablePosition')
			Local $GUITabItem = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUITabItem')
			Local $GUIJSON = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUIJSON')
			Local $GUIJSONKEY = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUIJSONKEY')
			Local $HELPIconFile = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].HELPIconFile')
			Local $HELPIconIndex = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].HELPIconIndex')
			Local $HELPIconText = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].HELPIconText')
			Local $HELPIconSize = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].HELPIconSize')
			Local $HELPIconPosition = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].HELPIconPosition')
			Local $HELPIconCallback = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].HELPIconCallback')
			Local $ComboEvent = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].ComboEvent')
			Local $hide = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].hide')
			Local $GUILabelVariable = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUILabelVariable')
			Local $GUISetFont = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUISetFont')
			Local $GUISetFontSize = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUISetSize')
			Local $GUISetFontColor = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUISetColor')
			Local $GUISetCursor = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUISetCursor')
			Local $GUIWM_COMMAND = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].GUIWM_COMMAND')
			Local $NumericMin = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].NumericMin')
			Local $NumericMax = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].NumericMax')

			$dynamicVariableNameLabel = ''
			
			Switch $GUITypeField
				Case "text"
					GUICtrlCreateLabel($GUILabel, $GUILabelPosition[0], $GUILabelPosition[1], $GUILabelPosition[2], $GUILabelPosition[3])
					$dynamicVariableName = $GUIVariable
					Global $dynamicVariableName
					Assign($dynamicVariableName, GUICtrlCreateInput(Eval("Setup_" & $iniGroup & "_" & $iniProp), $GUIVariablePosition[0], $GUIVariablePosition[1], $GUIVariablePosition[2], $GUIVariablePosition[3]), $ASSIGN_FORCEGLOBAL)
				Case "combo"
					GUICtrlCreateLabel($GUILabel, $GUILabelPosition[0], $GUILabelPosition[1], $GUILabelPosition[2], $GUILabelPosition[3])
					$dynamicVariableName = $GUIVariable
					Global $dynamicVariableName
					Assign($dynamicVariableName, GUICtrlCreateCombo("", $GUIVariablePosition[0], $GUIVariablePosition[1], $GUIVariablePosition[2], $GUIVariablePosition[3], BitOR($CBS_DROPDOWNLIST, $LBS_STANDARD)), $ASSIGN_FORCEGLOBAL)
					If $GUIComboValues <> "" And $GUIJSON = "" Then
						GUICtrlSetData(Eval($dynamicVariableName), $GUIComboValues, Eval("Setup_" & $iniGroup & "_" & $iniProp))
					EndIf
					If $GUIJSON <> "" And $GUIJSONKEY <> "" Then
						$JsonSetup = Json_Decode(Eval($GUIJSON))
						$JSONSetupValue = Json_Get($JsonSetup, '.' & $GUIJSONKEY)
						If $GUIComboValues <> "" Then
							$sAllValues = $GUIComboValues & "|"
						Else
							$sAllValues = ""
						EndIf
						For $k = 0 To UBound($JSONSetupValue) - 1 Step 1
							$value = Json_Get($JsonSetup, '.' & $GUIJSONKEY & '[' & $k & '].name')
							If $GUIJSON = "JSON_runs" Then
								If $GUIVariable = "GUI_FishMaps" Or $GUIVariable = "GUI_Fish2Maps" Then
									If Json_Get($JsonSetup, '.' & $GUIJSONKEY & '[' & $k & '].fish') = "False" Then
										ContinueLoop
									EndIf
								EndIf
								If $GUIVariable = "GUI_FarmMap" Then
									If Json_Get($JsonSetup, '.' & $GUIJSONKEY & '[' & $k & '].farm') = "False" Then
										ContinueLoop
									EndIf
								EndIf
								If $GUIVariable = "GUI_SpotFarmMap" Then
									If Json_Get($JsonSetup, '.' & $GUIJSONKEY & '[' & $k & '].Spotfarm') = "False" Then
										ContinueLoop
									EndIf
								EndIf
								If $GUIVariable = "GUI_SpotFarmCustomModelMap" Then
									If Json_Get($JsonSetup, '.' & $GUIJSONKEY & '[' & $k & '].CustomSpotfarm') = "False" Then
										ContinueLoop
									EndIf
								EndIf
							EndIf
							$firstChar = StringUpper(StringLeft($value, 1))
							$restOfString = StringMid($value, 2)
							$sAllValues &= $firstChar & $restOfString & "|"
						Next
						If $GUIVariable = "GUI_SpotFarmMap" Then
							$files = _FileListToArray(@ScriptDir & "\inc\data\models", "model_*.dat", 1)
							If Not @error Then
								For $p = 1 To UBound($files) - 1 Step 1
									$restOfString = StringLeft($files[$p], StringLen($files[$p]) - 4)
									$sAllValues &= $restOfString & "|"
								Next
								
							EndIf
						EndIf
						$sAllValues = StringTrimRight($sAllValues, 1)
						GUICtrlSetData(Eval($dynamicVariableName), $sAllValues, Eval("Setup_" & $iniGroup & "_" & $iniProp))
					EndIf
					If $ComboEvent <> "" Then
						;~ MsgBox(0, "ComboEvent", $ComboEvent & " " & $dynamicVariableName)
						GUICtrlSetOnEvent(Eval($dynamicVariableName), $ComboEvent)
					EndIf
				Case "textExplore"
					GUICtrlCreateLabel($GUILabel, $GUILabelPosition[0], $GUILabelPosition[1], $GUILabelPosition[2], $GUILabelPosition[3])
					$dynamicVariableName = $GUIVariable
					Global $dynamicVariableName
				 	Assign($dynamicVariableName, GUICtrlCreateInput(Eval("Setup_" & $iniGroup & "_" & $iniProp), $GUIVariablePosition[0], $GUIVariablePosition[1], $GUIVariablePosition[2], $GUIVariablePosition[3]), $ASSIGN_FORCEGLOBAL)
				 	$dynamicVariableNameButton = $GUIVariable & "Button"
				 	Global $dynamicVariableNameButton
				 	Assign($dynamicVariableNameButton, GUICtrlCreateButton("...", $GUIVariablePosition[0] + $GUIVariablePosition[2] + 5, $GUIVariablePosition[1], 30, 20), $ASSIGN_FORCEGLOBAL)
				 	GUICtrlSetOnEvent(Eval($dynamicVariableNameButton), "Explore_" & $iniGroup & "_" & $iniProp)
				case "help_text"
					$dynamicVariableNameLabel = $GUIVariable & "Label"
					Assign($dynamicVariableNameLabel, GUICtrlCreateLabel($GUILabel, $GUILabelPosition[0], $GUILabelPosition[1], $GUILabelPosition[2], $GUILabelPosition[3]), $ASSIGN_FORCEGLOBAL)
					If $GUISetFont <> "" Then
						GUICtrlSetFont(Eval($dynamicVariableNameLabel), $GUISetFontSize, $GUISetFontColor, $GUISetFont)
					EndIf
					If $GUISetCursor <> "" Then
						GUICtrlSetCursor(Eval($dynamicVariableNameLabel), $GUISetCursor)
					EndIf
					If $GUIWM_COMMAND <> "" Then
						GUICtrlSetOnEvent(Eval($dynamicVariableNameLabel), $GUIWM_COMMAND)
					EndIf
				case "readonly"
					$dynamicVariableNameLabel = $GUIVariable & "Label"
					Assign($dynamicVariableNameLabel, GUICtrlCreateLabel($GUILabel, $GUILabelPosition[0], $GUILabelPosition[1], $GUILabelPosition[2], $GUILabelPosition[3]), $ASSIGN_FORCEGLOBAL)
					;~ GUICtrlCreateLabel($GUILabel, $GUILabelPosition[0], $GUILabelPosition[1], $GUILabelPosition[2], $GUILabelPosition[3])
					$dynamicVariableName = $GUIVariable
					Global $dynamicVariableName
					Assign($dynamicVariableName, GUICtrlCreateInput(Eval("Setup_" & $iniGroup & "_" & $iniProp), $GUIVariablePosition[0], $GUIVariablePosition[1], $GUIVariablePosition[2], $GUIVariablePosition[3], $ES_READONLY), $ASSIGN_FORCEGLOBAL)
					If $GUIVariable == 'GUI_TelegramToken' Then
						;~ set devfault value to 1234
						GUICtrlSetData(Eval($dynamicVariableName), LoadPasswordEncryptFromRegistry())
					EndIf
				Case "numeric"
					GUICtrlCreateLabel($GUILabel, $GUILabelPosition[0], $GUILabelPosition[1], $GUILabelPosition[2], $GUILabelPosition[3])
					$dynamicVariableName = $GUIVariable
					Global $dynamicVariableName
					Assign($dynamicVariableName, GUICtrlCreateInput(Eval("Setup_" & $iniGroup & "_" & $iniProp), $GUIVariablePosition[0], $GUIVariablePosition[1], $GUIVariablePosition[2], $GUIVariablePosition[3]), $ASSIGN_FORCEGLOBAL)
					GUICtrlCreateUpdown(Eval($dynamicVariableName))
					GUICtrlSetLimit(-1, $NumericMin, $NumericMax)
			EndSwitch
			If $HELPIconFile <> "" Then
				$hIcon = GUICtrlCreateIcon($HELPIconFile, $HELPIconIndex, $HELPIconPosition[0], $HELPIconPosition[1], $HELPIconSize, $HELPIconSize)
				GUICtrlSetOnEvent($hIcon, $HELPIconCallback)
				GUICtrlSetTip($hIcon, $HELPIconText)
			EndIf
			If $hide = "True" Then
				GUICtrlSetState(Eval($dynamicVariableName), $GUI_HIDE)
				If $dynamicVariableNameLabel <> "" Then
					GUICtrlSetState(Eval($dynamicVariableNameLabel), $GUI_HIDE)
				EndIf
			EndIf
		Next
	Next

	GUISetState(@SW_SHOW)

EndFunc

Func TelegramActive()
	$actualValue = GUICtrlRead($GUI_TelegramActive)
	If $actualValue == 'Yes' Then
		;~ show this field $GUI_TelegramToken
		GUICtrlSetState($GUI_TelegramToken, $GUI_SHOW)
		GUICtrlSetState($GUI_TelegramTokenLabel, $GUI_SHOW)
		GUICtrlSetState($GUI_text2Label, $GUI_SHOW)
		GUICtrlSetState($GUI_text3Label, $GUI_SHOW)
		GUICtrlSetState($GUI_text4Label, $GUI_SHOW)
	Else
		;~ hide this field $GUI_TelegramToken
		GUICtrlSetState($GUI_TelegramToken, $GUI_HIDE)
		GUICtrlSetState($GUI_TelegramTokenLabel, $GUI_HIDE)
		GUICtrlSetState($GUI_text2Label, $GUI_HIDE)
		GUICtrlSetState($GUI_text3Label, $GUI_HIDE)
		GUICtrlSetState($GUI_text4Label, $GUI_HIDE)
	EndIf
EndFunc	

Func DungeonSelect()
	$actualValue = GUICtrlRead($GUI_Dungeon)
	Local $JsonDungeon = Json_Decode($JSON_dungeons)
	$JsonDungeonValue = Json_Get($JsonDungeon, '.dungeons')
	For $i = 0 To UBound($JsonDungeonValue) - 1 Step 1
		$value = Json_Get($JsonDungeon, '.dungeons[' & $i & '].name')
		$mode = Json_Get($JsonDungeon, '.dungeons[' & $i & '].mode')
		;~ set to uppercase
		If StringUpper($value) = StringUpper($actualValue) Then
			;~ set data to combo
			GUICtrlSetData($GUI_DungeonTeamSolo, "", $Setup_Dungeon_Team_solo)
			GUICtrlSetData($GUI_DungeonTeamSolo, $mode, $Setup_Dungeon_Team_solo)
			ExitLoop
		EndIf
	Next
EndFunc

Func FishZonesSelect()
	;~ MsgBox(0, "FishZonesSelect", "FishZonesSelect")
	$actualValue = GUICtrlRead($GUI_Fish2Maps)
	Local $JsonFish2Zones = Json_Decode($JSON_fish)
	$JsonFish2ZonesValue = Json_Get($JsonFish2Zones, '.fish')
	For $i = 0 To UBound($JsonFish2ZonesValue) - 1 Step 1
		$value = Json_Get($JsonFish2Zones, '.fish[' & $i & '].mapname')
		$zones = Json_Get($JsonFish2Zones, '.fish[' & $i & '].zones')
		;~ set to uppercase
		;~ MsgBox(0, "value", "value: " & StringUpper($value) & " actualValue: " & StringUpper($actualValue))
		If StringUpper($value) = StringUpper($actualValue) Then
			;~ set data to combo
			GUICtrlSetData($GUI_FishZones, "", $Setup_Fish2_Zones)
			GUICtrlSetData($GUI_FishZones, $zones, $Setup_Fish2_Zones)
			;~ foreach all combo values and select the first one
			ExitLoop
		EndIf
	Next
EndFunc

Func SetMinMaxFishIters()
	$minValue = Int(GUICtrlRead($GUI_Fish2IterationsMin))
	$maxValue = Int(GUICtrlRead($GUI_Fish2IterationsMax))
	;~ max value always must be greater or equal to min value
	If $maxValue < $minValue Then
		;~ sum 1 to max value
		$maxValue = $minValue + 1
		If $maxValue >= 16 Then
			$maxValue = 15
		EndIf
		GUICtrlSetData($GUI_Fish2IterationsMax, $maxValue)
	EndIf
EndFunc

Func CustomModelActive()
	GUICtrlSetState($GUI_SpotFarmCustomModelMap, $GUI_HIDE)
	$actualValue = GUICtrlRead($GUI_SpotFarmMap)
	;~ if map start With "model_" then
	If StringLeft($actualValue, 6) = "model_" Then
		;~ show this field $GUI_CustomModel
		GUICtrlSetState($GUI_SpotFarmCustomModelMap, $GUI_SHOW)
		;~ GUICtrlSetState($GUI_SpotFarmCustomModelMapLabel, $GUI_SHOW)
	Else
		;~ hide this field $GUI_CustomModel
		GUICtrlSetState($GUI_SpotFarmCustomModelMap, $GUI_HIDE)
		;~ GUICtrlSetState($GUI_SpotFarmCustomModelMapLabel, $GUI_HIDE)
	EndIf
EndFunc

Func GoToTelegramurl()
	; Configure your Telegram bot URL here
	; ShellExecute("https://t.me/YOUR_BOT_HERE")
EndFunc

Func enableOrDisableButtons($action)
	Local $oJson = Json_Decode($JSON_setup)
	Local $oButtons = Json_Get($oJson, '.buttons')
	If Json_Get($oJson, '.buttons.guibuttons[0].name') <> "" And Json_Get($oJson, '.buttons.guibuttons[0].values') <> "" Then
		$oGUIButtons = Json_Get($oJson, '.buttons.guibuttons')
	 	For $i = 0 To UBound($oGUIButtons) - 1 Step 1
	 		Local $name = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].name')
	 		Local $value1 = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].values[0]')
	 		Local $value2 = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].values[1]')
	 		Local $value3 = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].values[2]')
	 		Local $value4 = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].values[3]')
	 		Local $value5 = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].values[4]')
	 		Local $callbak = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].callback')
	 		Local $hide = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].hide')
	 		Local $hotkey = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].hotkey')
	 		Local $hotkeyFunc = Json_Get($oJson, '.buttons.guibuttons[' & $i & '].hotkeyFunc')
	 		If $name <> "" And $value1 <> "" And $value2 <> "" And $value3 <> "" And $value4 <> "" And $value5 <> "" And $callbak <> "" Then
	 			$dynamicVariableNameButton = "Button_" & $name
				Global $dynamicVariableNameButton
				If $action = "enable" Then
					GUICtrlSetState(Eval($dynamicVariableNameButton), $GUI_ENABLE)
					GUICtrlSetOnEvent(Eval($dynamicVariableNameButton), $callbak)
					If $hotkey <> "" And $hotkeyFunc <> "" Then
						HotKeySet($hotkey, $hotkeyFunc)
					EndIf
				ElseIf $action = "disable" Then
					GUICtrlSetState(Eval($dynamicVariableNameButton), $GUI_DISABLE)
				EndIf
			EndIf
		Next
	EndIf
EndFunc

;~ INITIAL SETUP FILE
Func InitialSetupFile()
	$SetupFile = ReadSetupFile()
	;~ Declare all global variables from config File
	Local $oJson = Json_Decode($JSON_setup)
	Local $SETOPJSON = Json_Get($oJson, '.setup')
	For $i = 0 To UBound($SETOPJSON) - 1 Step 1
		Local $SETOPJSON2 = Json_Get($oJson, '.setup[' & $i & '].values')
		For $j = 0 To UBound($SETOPJSON2) - 1 Step 1
			Local $iniGroup = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].iniGroup')
			Local $iniProp = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].iniProp')
			Local $defaultValue = Json_Get($oJson, '.setup[' & $i & '].values[' & $j & '].defaultValue')
			$dynamicVariableName = "Setup_" & $iniGroup & "_" & $iniProp
			Global $dynamicVariableName
			Assign($dynamicVariableName, $SetupFile[$i][$j][3], $ASSIGN_FORCEGLOBAL)
		Next
	Next
EndFunc

InitialSetupFile()
