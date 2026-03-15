Func update_gui_one_param($actual_number, $hProgress, $totalfiles, $hLabel)
	_Update_gui_bar_and_label($hProgress, Round(($actual_number / $totalFiles) * 100), $hLabel, "Checking files, please wait. This operation can take up to 5 minutes. Please, be patient. This screen may freeze, but it is working... " & Round(($actual_number / $totalFiles) * 100) & "%")
EndFunc

Func _Update_gui_bar_and_label($hProgress, $dataprogress, $hLabel, $datalabel)
	GUICtrlSetData($hProgress, $dataprogress)
	GUICtrlSetData($hLabel, $datalabel)
EndFunc

Func _CheckForFiles()

	;~ create gui with progress bar to check directories and installed files
	$hGUIDownload = GUICreate("Checking for files", 300, 100, -1, -1, $WS_POPUP, $WS_EX_TOOLWINDOW)
	$hProgress = GUICtrlCreateProgress(10, 10, 280, 20)
	$hLabel = GUICtrlCreateLabel("Checking directories...", 10, 40, 280, 40)
	GUISetState(@SW_SHOW, $hGUIDownload)

	Local $aJson = Json_Decode($JSON_prepareFiles)
	Local $aFolders = Json_Get($aJson, ".folders")
	Local $totalFolders = UBound($aFolders) - 1
	For $i = 0 To UBound($aFolders) - 1
		Local $sPath = Json_Get($aJson, ".folders[" & $i & "].path")
		If Not FileExists(@ScriptDir & $sPath) Then
			DirCreate(@ScriptDir & $sPath)
		EndIf
	Next

	GUICtrlSetData($hProgress, 0)
	GUICtrlSetData($hLabel, "Checking files...")
		
	Local $totalFiles = 79
	Local $actual_number = 0

		If FileExists(@ScriptDir & '\inc\scripts\certutil.exe') = 0 Then
			$res1 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\scripts\certutil.exe", @ScriptDir & "\inc\scripts\", 1)
			If $res1 = 0 Then 
				MsgBox(0, "Error", "Error installing certutil.exe") 
				Exit 
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 1), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\help\img\HelpPlayerSelect.jpg') = 0 Then
			$res13 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\help\img\HelpPlayerSelect.jpg", @ScriptDir & "\inc\help\img\", 1)
			If $res13 = 0 Then 
				MsgBox(0, "Error", "Error installing HelpPlayerSelect.jpg") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 2), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\maps\cementery_en.png') = 0 Then
			$res16 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\maps\cementery_en.png", @ScriptDir & "\inc\img\en\maps\", 1)
			If $res16 = 0 Then 
				MsgBox(0, "Error", "Error installing cementery_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 3), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\maps\zavain_en.png') = 0 Then
			$res17 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\maps\zavain_en.png", @ScriptDir & "\inc\img\en\maps\", 1)
			If $res17 = 0 Then 
				MsgBox(0, "Error", "Error installing zavain_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 5), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\maps\library_en.png') = 0 Then
			$res18 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\maps\library_en.png", @ScriptDir & "\inc\img\en\maps\", 1)
			If $res18 = 0 Then 
				MsgBox(0, "Error", "Error installing library_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 6), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\maps\forest_en.png') = 0 Then
			$res19 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\maps\forest_en.png", @ScriptDir & "\inc\img\en\maps\", 1)
			If $res19 = 0 Then 
				MsgBox(0, "Error", "Error installing forest_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 7), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\maps\dreadlands_en.png') = 0 Then
			$res19 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\maps\dreadlands_en.png", @ScriptDir & "\inc\img\en\maps\", 1)
			If $res19 = 0 Then 
				MsgBox(0, "Error", "Error installing dreadlands_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 7), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\maps\bilefen_en.png') = 0 Then
			$res20 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\maps\bilefen_en.png", @ScriptDir & "\inc\img\en\maps\", 1)
			If $res20 = 0 Then 
				MsgBox(0, "Error", "Error installing bilefen_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 8), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\maps\thundra_en.png') = 0 Then
			$res21 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\maps\thundra_en.png", @ScriptDir & "\inc\img\en\maps\", 1)
			If $res21 = 0 Then 
				MsgBox(0, "Error", "Error installing thundra_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 9), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\maps\westmarch_en.png') = 0 Then
			$res22 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\maps\westmarch_en.png", @ScriptDir & "\inc\img\en\maps\", 1)
			If $res22 = 0 Then 
				MsgBox(0, "Error", "Error installing westmarch_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 10), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\maps\shassarsea_en.png') = 0 Then
			$res23 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\maps\shassarsea_en.png", @ScriptDir & "\inc\img\en\maps\", 1)
			If $res23 = 0 Then 
				MsgBox(0, "Error", "Error installing shassarsea_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 11), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\loot_items\essence_label_en.png') = 0 Then
			$res32 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\loot_items\essence_label_en.png", @ScriptDir & "\inc\img\en\loot_items\", 1)
			If $res32 = 0 Then 
				MsgBox(0, "Error", "Error installing essence_label_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 12), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\loot_items\globe_label_en.png') = 0 Then
			$res33 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\loot_items\globe_label_en.png", @ScriptDir & "\inc\img\en\loot_items\", 1)
			If $res33 = 0 Then 
				MsgBox(0, "Error", "Error installing globe_label_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 13), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\loot_items\gold_label_1_en.png') = 0 Then
			$res34 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\loot_items\gold_label_1_en.png", @ScriptDir & "\inc\img\en\loot_items\", 1)
			If $res34 = 0 Then 
				MsgBox(0, "Error", "Error installing gold_label_1_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 14), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\loot_items\gold_label_2_en.png') = 0 Then
			$res35 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\loot_items\gold_label_2_en.png", @ScriptDir & "\inc\img\en\loot_items\", 1)
			If $res35 = 0 Then 
				MsgBox(0, "Error", "Error installing gold_label_2_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 15), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\loot_items\gold_label_en.png') = 0 Then
			$res36 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\loot_items\gold_label_en.png", @ScriptDir & "\inc\img\en\loot_items\", 1)
			If $res36 = 0 Then 
				MsgBox(0, "Error", "Error installing gold_label_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 16), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\loot_items\monstrous_essence.png') = 0 Then
			$res37 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\loot_items\monstrous_essence.png", @ScriptDir & "\inc\img\en\loot_items\", 1)
			If $res37 = 0 Then 
				MsgBox(0, "Error", "Error installing monstrous_essence.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 17), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\blacksmith\blacksmith_screen_en.png') = 0 Then
			$res40 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\blacksmith\blacksmith_screen_en.png", @ScriptDir & "\inc\img\en\blacksmith\", 1)
			If $res40 = 0 Then 
				MsgBox(0, "Error", "Error installing blacksmith_screen_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 18), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\blacksmith\bs_button1_en.png') = 0 Then
			$res41 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\blacksmith\bs_button1_en.png", @ScriptDir & "\inc\img\en\blacksmith\", 1)
			If $res41 = 0 Then 
				MsgBox(0, "Error", "Error installing bs_button1_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 19), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\blacksmith\inventory_full_en.png') = 0 Then
			$res42 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\blacksmith\inventory_full_en.png", @ScriptDir & "\inc\img\en\blacksmith\", 1)
			If $res42 = 0 Then 
				MsgBox(0, "Error", "Error installing inventory_full_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 20), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\farm\nav_arrow.png') = 0 Then
			$res43 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\farm\nav_arrow.png", @ScriptDir & "\inc\img\en\farm\", 1)
			If $res43 = 0 Then 
				MsgBox(0, "Error", "Error installing nav_arrow.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 21), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\farm\navto_en.png') = 0 Then
			$res44 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\farm\navto_en.png", @ScriptDir & "\inc\img\en\farm\", 1)
			If $res44 = 0 Then 
				MsgBox(0, "Error", "Error installing navto_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 22), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\farm\party_invite_en.png') = 0 Then
			$res45 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\farm\party_invite_en.png", @ScriptDir & "\inc\img\en\farm\", 1)
			If $res45 = 0 Then 
				MsgBox(0, "Error", "Error installing party_invite_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 23), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\farm\bestiary_screen_en.png') = 0 Then
			$res52 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\farm\bestiary_screen_en.png", @ScriptDir & "\inc\img\en\farm\", 1)
			If $res52 = 0 Then 
				MsgBox(0, "Error", "Error installing bestiary_screen_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 24), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\farm\party_invite_shassarsea_en.png') = 0 Then
			$res54 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\farm\party_invite_shassarsea_en.png", @ScriptDir & "\inc\img\en\farm\", 1)
			If $res54 = 0 Then 
				MsgBox(0, "Error", "Error installing party_invite_shassarsea_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 25), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\farm\party_invite_zavain1_en.png') = 0 Then
			$res56 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\farm\party_invite_zavain1_en.png", @ScriptDir & "\inc\img\en\farm\", 1)
			If $res56 = 0 Then 
				MsgBox(0, "Error", "Error installing party_invite_zavain1_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 26), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\farm\party_invite_bilefen_en.png') = 0 Then
			$res58 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\farm\party_invite_bilefen_en.png", @ScriptDir & "\inc\img\en\farm\", 1)
			If $res58 = 0 Then 
				MsgBox(0, "Error", "Error installing party_invite_bilefen_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 27), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\scripts\xf.exe') = 0 Then
			$res91 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\scripts\MAIN\dist\xf.exe", @ScriptDir & "\inc\scripts\", 1)
			If $res91 = 0 Then 
				MsgBox(0, "Error", "Error installing xf.exe") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 28), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\farm\party_invite_realm_en.png
		If FileExists(@ScriptDir & '\inc\img\en\farm\party_invite_realm_en.png') = 0 Then
			$res97 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\farm\party_invite_realm_en.png", @ScriptDir & "\inc\img\en\farm\", 1)
			If $res97 = 0 Then 
				MsgBox(0, "Error", "Error installing party_invite_realm_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 29), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\maps\realm_en.png'
		If FileExists(@ScriptDir & '\inc\img\en\maps\realm_en.png') = 0 Then
			$res101 = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\maps\realm_en.png", @ScriptDir & "\inc\img\en\maps\", 1)
			If $res101 = 0 Then 
				MsgBox(0, "Error", "Error installing realm_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 30), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\dungeons\tower\tower_entrance_icon_en.png'
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\tower\tower_entrance_icon_en.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\tower\tower_entrance_icon_en.png", @ScriptDir & "\inc\img\en\dungeons\tower\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing tower_entrance_icon_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 31), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\dungeons\namari\namari_entrance_icon_en.png'
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\namari\namari_entrance_icon_en.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\namari\namari_entrance_icon_en.png", @ScriptDir & "\inc\img\en\dungeons\namari\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing namari_entrance_icon_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 32), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\dungeons\kikuras\kikuras_entrance_icon_en.png'
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\kikuras\kikuras_entrance_icon_en.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\kikuras\kikuras_entrance_icon_en.png", @ScriptDir & "\inc\img\en\dungeons\kikuras\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing kikuras_entrance_icon_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 33), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\loot_items\fogs_bane_en.png'
		If FileExists(@ScriptDir & '\inc\img\en\loot_items\fogs_bane_en.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\loot_items\fogs_bane_en.png", @ScriptDir & "\inc\img\en\loot_items\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing fogs_bane_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 34), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\loot_items\fogs_bane_label_en.png'
		If FileExists(@ScriptDir & '\inc\img\en\loot_items\fogs_bane_label_en.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\loot_items\fogs_bane_label_en.png", @ScriptDir & "\inc\img\en\loot_items\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing fogs_bane_label_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 35), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\maps\storm_en.png')
		If FileExists(@ScriptDir & '\inc\img\en\maps\storm_en.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\maps\storm_en.png", @ScriptDir & "\inc\img\en\maps\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing storm_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 36), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\maps\ancients_en.png')
		If FileExists(@ScriptDir & '\inc\img\en\maps\ancients_en.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\maps\ancients_en.png", @ScriptDir & "\inc\img\en\maps\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing ancients_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 37), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\farm\party_invite_ancients_en.png')
		If FileExists(@ScriptDir & '\inc\img\en\farm\party_invite_ancients_en.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\farm\party_invite_ancients_en.png", @ScriptDir & "\inc\img\en\farm\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing party_invite_ancients_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 38), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\farm\party_invite_storm_en.png')
		If FileExists(@ScriptDir & '\inc\img\en\farm\party_invite_storm_en.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\farm\party_invite_storm_en.png", @ScriptDir & "\inc\img\en\farm\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing party_invite_storm_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 39), $hProgress, $totalfiles, $hLabel)
		;~ inc/img/en/dungeons/tower/tower_entrance_icon_en.png
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\tower\tower_entrance_icon_en.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\tower\tower_entrance_icon_en.png", @ScriptDir & "\inc\img\en\dungeons\tower\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing tower_entrance_icon_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 40), $hProgress, $totalfiles, $hLabel)
		;~ inc/img/en/dungeons/namari/talk_after.png
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\namari\talk_after.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\namari\talk_after.png", @ScriptDir & "\inc\img\en\dungeons\namari\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing talk_after.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 41), $hProgress, $totalfiles, $hLabel)
		;~ inc/img/en/dungeons/namari/sargoth.png
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\namari\sargoth.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\namari\sargoth.png", @ScriptDir & "\inc\img\en\dungeons\namari\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing sargoth.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 42), $hProgress, $totalfiles, $hLabel)
		;~ inc/img/en/dungeons/namari/namari_entrance_icon_en.png
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\namari\namari_entrance_icon_en.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\namari\namari_entrance_icon_en.png", @ScriptDir & "\inc\img\en\dungeons\namari\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing namari_entrance_icon_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 43), $hProgress, $totalfiles, $hLabel)
		;~ inc/img/en/dungeons/namari/namari.png
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\namari\namari.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\namari\namari.png", @ScriptDir & "\inc\img\en\dungeons\namari\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing namari.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 44), $hProgress, $totalfiles, $hLabel)
		;~ inc/img/en/dungeons/namari/before_boss.png
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\namari\before_boss.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\namari\before_boss.png", @ScriptDir & "\inc\img\en\dungeons\namari\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing before_boss.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 45), $hProgress, $totalfiles, $hLabel)
		;~ inc/img/en/dungeons/kikuras/survive_the_fire.png
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\kikuras\survive_the_fire.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\kikuras\survive_the_fire.png", @ScriptDir & "\inc\img\en\dungeons\kikuras\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing survive_the_fire.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 46), $hProgress, $totalfiles, $hLabel)
		;~ inc/img/en/dungeons/kikuras/ride_the_raft_into_the_jungle.png
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\kikuras\ride_the_raft_into_the_jungle.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\kikuras\ride_the_raft_into_the_jungle.png", @ScriptDir & "\inc\img\en\dungeons\kikuras\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing ride_the_raft_into_the_jungle.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 47), $hProgress, $totalfiles, $hLabel)
		;~ inc/img/en/dungeons/kikuras/reach_the_river.png
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\kikuras\reach_the_river.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\kikuras\reach_the_river.png", @ScriptDir & "\inc\img\en\dungeons\kikuras\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing reach_the_river.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 48), $hProgress, $totalfiles, $hLabel)
		;~ inc/img/en/dungeons/kikuras/kill_ongori.png
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\kikuras\kill_ongori.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\kikuras\kill_ongori.png", @ScriptDir & "\inc\img\en\dungeons\kikuras\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing kill_ongori.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 49), $hProgress, $totalfiles, $hLabel)
		;~ inc/img/en/dungeons/kikuras/kikuras_entrance_icon_en.png
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\kikuras\kikuras_entrance_icon_en.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\kikuras\kikuras_entrance_icon_en.png", @ScriptDir & "\inc\img\en\dungeons\kikuras\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing kikuras_entrance_icon_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 50), $hProgress, $totalfiles, $hLabel)
		;~ inc/img/en/dungeons/kikuras/find_boss.png
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\kikuras\find_boss.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\kikuras\find_boss.png", @ScriptDir & "\inc\img\en\dungeons\kikuras\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing find_boss.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 51), $hProgress, $totalfiles, $hLabel)
		;~ inc/img/en/dungeons/kikuras/board_the_raft.png
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\kikuras\board_the_raft.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\kikuras\board_the_raft.png", @ScriptDir & "\inc\img\en\dungeons\kikuras\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing board_the_raft.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 52), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\blacksmith\bs_button2_en.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\blacksmith\bs_button2_en.png", @ScriptDir & "\inc\img\en\blacksmith\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing bs_button2_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 53), $hProgress, $totalfiles, $hLabel)
		If FileExists(@ScriptDir & '\inc\img\en\blacksmith\bs_button3_en.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\blacksmith\bs_button3_en.png", @ScriptDir & "\inc\img\en\blacksmith\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing bs_button3_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 53), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\dungeons\king_breach\defeat_manoruk.png'
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\king_breach\defeat_manoruk.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\king_breach\defeat_manoruk.png", @ScriptDir & "\inc\img\en\dungeons\king_breach\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing defeat_manoruk.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 54), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\dungeons\king_breach\defeat_sir_gorash.png'
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\king_breach\defeat_sir_gorash.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\king_breach\defeat_sir_gorash.png", @ScriptDir & "\inc\img\en\dungeons\king_breach\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing defeat_sir_gorash.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 55), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\dungeons\king_breach\defeat_undead_guardians.png'
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\king_breach\defeat_undead_guardians.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\king_breach\defeat_undead_guardians.png", @ScriptDir & "\inc\img\en\dungeons\king_breach\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing defeat_undead_guardians.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 56), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\dungeons\king_breach\interact_portal.png'
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\king_breach\interact_portal.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\king_breach\interact_portal.png", @ScriptDir & "\inc\img\en\dungeons\king_breach\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing interact_portal.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 57), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\dungeons\king_breach\king_breach_entrance_icon_en.png'
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\king_breach\king_breach_entrance_icon_en.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\king_breach\king_breach_entrance_icon_en.png", @ScriptDir & "\inc\img\en\dungeons\king_breach\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing king_breach_entrance_icon_en.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 58), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\dungeons\king_breach\reach_courtyard.png'
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\king_breach\reach_courtyard.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\king_breach\reach_courtyard.png", @ScriptDir & "\inc\img\en\dungeons\king_breach\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing reach_courtyard.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 59), $hProgress, $totalfiles, $hLabel)
		;~ \inc\img\en\dungeons\king_breach\enter_the_portal.png
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\king_breach\enter_the_portal.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\king_breach\enter_the_portal.png", @ScriptDir & "\inc\img\en\dungeons\king_breach\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing enter_the_portal.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 60), $hProgress, $totalfiles, $hLabel)
		;~ \inc\img\en\dungeons\king_breach\ascend_the_stairs.png
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\king_breach\ascend_the_stairs.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\king_breach\ascend_the_stairs.png", @ScriptDir & "\inc\img\en\dungeons\king_breach\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing ascend_the_stairs.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 61), $hProgress, $totalfiles, $hLabel)
		;~ \inc\img\en\dungeons\king_breach\reach_leoric_throne.png
		If FileExists(@ScriptDir & '\inc\img\en\dungeons\king_breach\reach_leoric_throne.png') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\dungeons\king_breach\reach_leoric_throne.png", @ScriptDir & "\inc\img\en\dungeons\king_breach\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing reach_leoric_throne.png") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 62), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\tesseract\tesseract.zip'
		If FileExists(@ScriptDir & '\inc\tesseract\tesseract.zip') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\tesseract\tesseract.zip", @ScriptDir & "\inc\tesseract\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing tesseract.zip") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 63), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\data\models\models.zip'
		If FileExists(@ScriptDir & '\inc\data\models\models.zip') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\data\models\models.zip", @ScriptDir & "\inc\data\models\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing models.zip") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 64), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\game_items\game_items.zip'
		If FileExists(@ScriptDir & '\inc\img\game_items\game_items.zip') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\game_items\game_items.zip", @ScriptDir & "\inc\img\game_items\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing game_items.zip") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 66), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\fishing\fishing.zip'
		If FileExists(@ScriptDir & '\inc\img\fishing\fishing.zip') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\fishing\fishing.zip", @ScriptDir & "\inc\img\fishing\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing fishing.zip") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 67), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\en\cyrangar\cyrangar.zip'
		If FileExists(@ScriptDir & '\inc\img\en\cyrangar\cyrangar.zip') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\en\cyrangar\cyrangar.zip", @ScriptDir & "\inc\img\en\cyrangar\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing cyrangar.zip") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 68), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\mapLegend\mapLegend.zip'
		If FileExists(@ScriptDir & '\inc\img\mapLegend\mapLegend.zip') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\mapLegend\mapLegend.zip", @ScriptDir & "\inc\img\mapLegend\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing mapLegend.zip") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 69), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\img\screens\screens.zip'
		If FileExists(@ScriptDir & '\inc\img\screens\screens.zip') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\img\screens\screens.zip", @ScriptDir & "\inc\img\screens\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing screens.zip") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 70), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\help\img\HelpFishV2.jpg
		If FileExists(@ScriptDir & '\inc\help\img\HelpFishV2.jpg') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\help\img\HelpFishV2.jpg", @ScriptDir & "\inc\help\img\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing HelpFishV2.jpg") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 70), $hProgress, $totalfiles, $hLabel)
		;~ @ScriptDir & '\inc\scripts\7za.exe'
		If FileExists(@ScriptDir & '\inc\scripts\7za.exe') = 0 Then
			$res = FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\scripts\7za.exe", @ScriptDir & "\inc\scripts\", 1)
			If $res = 0 Then 
				MsgBox(0, "Error", "Error installing 7za.exe") 
				Exit
			EndIf
		EndIf
		update_gui_one_param(($actual_number + 71), $hProgress, $totalfiles, $hLabel)
		

		;~ ---------------------------------
		;~ ---------------------------------
		;~ ---------------------------------
		;~ ---------------------------------
		;~ NO SE TE OLVIDE CAMBIAR EL NUMERO TOTAL ---------------------------------
		;~ ---------------------------------
		;~ ---------------------------------
		;~ ---------------------------------
		;~ ---------------------------------
		;~ unzip Files


		_UNcompress_7za(@ScriptDir & "\inc\tesseract\tesseract.zip", @ScriptDir & "\inc\tesseract\")
		If @error Then Exit MsgBox ($MB_SYSTEMMODAL,"","Error unzipping file : " & @error)
		update_gui_one_param(($actual_number + 72), $hProgress, $totalfiles, $hLabel)
		_UNcompress_7za(@ScriptDir & "\inc\data\models\models.zip", @ScriptDir & "\inc\data\models\")
		If @error Then Exit MsgBox ($MB_SYSTEMMODAL,"","Error unzipping file : " & @error)
		update_gui_one_param(($actual_number + 73), $hProgress, $totalfiles, $hLabel)
		_UNcompress_7za(@ScriptDir & "\inc\img\game_items\game_items.zip", @ScriptDir & "\inc\img\game_items\")
		If @error Then Exit MsgBox ($MB_SYSTEMMODAL,"","Error unzipping file : " & @error)
		update_gui_one_param(($actual_number + 75), $hProgress, $totalfiles, $hLabel)
		_UNcompress_7za(@ScriptDir & "\inc\img\fishing\fishing.zip", @ScriptDir & "\inc\img\fishing\")
		If @error Then Exit MsgBox ($MB_SYSTEMMODAL,"","Error unzipping file : " & @error)
		update_gui_one_param(($actual_number + 76), $hProgress, $totalfiles, $hLabel)
		_UNcompress_7za(@ScriptDir & "\inc\img\en\cyrangar\cyrangar.zip", @ScriptDir & "\inc\img\en\cyrangar\")
		If @error Then Exit MsgBox ($MB_SYSTEMMODAL,"","Error unzipping file : " & @error)
		update_gui_one_param(($actual_number + 77), $hProgress, $totalfiles, $hLabel)
		_UNcompress_7za(@ScriptDir & "\inc\img\mapLegend\mapLegend.zip", @ScriptDir & "\inc\img\mapLegend\")
		If @error Then Exit MsgBox ($MB_SYSTEMMODAL,"","Error unzipping file : " & @error)
		update_gui_one_param(($actual_number + 78), $hProgress, $totalfiles, $hLabel)
		_UNcompress_7za(@ScriptDir & "\inc\img\screens\screens.zip", @ScriptDir & "\inc\img\screens\")
		If @error Then Exit MsgBox ($MB_SYSTEMMODAL,"","Error unzipping file : " & @error)
		update_gui_one_param(($actual_number + 79), $hProgress, $totalfiles, $hLabel)
		;~ ---------------------------------

		GUIDelete($hGUIDownload)
EndFunc