Global $JSON_setup = '{' & @CRLF & _
'"setup": [' & @CRLF & _
	'{' & @CRLF & _
		'"name": "general",' & @CRLF & _
		'"values": [' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Main",' & @CRLF & _
				'"iniProp": "Action",' & @CRLF & _
				'"defaultValue": "Farm",' & @CRLF & _
				'"GUILabel": "Action",' & @CRLF & _
				'"GUILabelPosition": [280, 45, 80, 20],' & @CRLF & _
				'"GUIVariable": "GUI_Action",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "Fish|Fish2.0|SpotFarm|Dungeon|Cyrangar",' & @CRLF & _
				'"GUIVariablePosition": [390, 40, 100, 20],' & @CRLF & _
				'"GUITabItem": "General",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Main",' & @CRLF & _
				'"iniProp": "Player",' & @CRLF & _
				'"defaultValue": "1",' & @CRLF & _
				'"GUILabel": "Player",' & @CRLF & _
				'"GUILabelPosition": [280, 75, 80, 20],' & @CRLF & _
				'"GUIVariable": "GUI_Player",' & @CRLF & _
				'"GUITypeField": "numeric",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"NumericMin": "1",' & @CRLF & _
				'"NumericMax": "5",' & @CRLF & _
				'"GUIVariablePosition": [390, 70, 100, 20],' & @CRLF & _
				'"GUITabItem": "General",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "Select the player to use for botting.",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [495, 72],' & @CRLF & _
				'"HELPIconCallback": "HELP_Main_Player",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Main",' & @CRLF & _
				'"iniProp": "Language",' & @CRLF & _
				'"defaultValue": "English",' & @CRLF & _
				'"GUILabel": "Game language",' & @CRLF & _
				'"GUILabelPosition": [280, 105, 80, 20],' & @CRLF & _
				'"GUIVariable": "GUI_Language",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "English",' & @CRLF & _
				'"GUIVariablePosition": [390, 100, 100, 20],' & @CRLF & _
				'"GUITabItem": "General",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Main",' & @CRLF & _
				'"iniProp": "StopBotAfter",' & @CRLF & _
				'"defaultValue": "0",' & @CRLF & _
				'"GUILabel": "Stop bot after (hours)",' & @CRLF & _
				'"GUILabelPosition": [280, 135, 100, 20],' & @CRLF & _
				'"GUIVariable": "GUI_StopBotAfter",' & @CRLF & _
				'"GUITypeField": "numeric",' & @CRLF & _
				'"NumericMin": "0",' & @CRLF & _
				'"NumericMax": "24",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [390, 130, 100, 20],' & @CRLF & _
				'"GUITabItem": "General",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "Select the number of hours the bot will run before stopping. If you select 0 the bot will run until you stop it manually.",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [495, 132],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Main",' & @CRLF & _
				'"iniProp": "AttackMethod",' & @CRLF & _
				'"defaultValue": "Precise",' & @CRLF & _
				'"GUILabel": "Monster detection",' & @CRLF & _
				'"GUILabelPosition": [280, 195, 100, 20],' & @CRLF & _
				'"GUIVariable": "GUI_AttackMethod",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "Precise|Old",' & @CRLF & _
				'"GUIVariablePosition": [390, 190, 100, 20],' & @CRLF & _
				'"GUITabItem": "General",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "The precise detection method detects monsters better. The old detection method also detects monsters, but it is possible that if your skin or abilities emit red color and may be confused with monsters around you and the character will attack to the air. Use this method if you run bot inside virtual machine (This applies to Spotfarm and dungeons)",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [495, 192],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Main",' & @CRLF & _
				'"iniProp": "LootMethod",' & @CRLF & _
				'"defaultValue": "Stop",' & @CRLF & _
				'"GUILabel": "Loot method",' & @CRLF & _
				'"GUILabelPosition": [280, 225, 100, 20],' & @CRLF & _
				'"GUIVariable": "GUI_LootMethod",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "NonStop|Stop",' & @CRLF & _
				'"GUIVariablePosition": [390, 220, 100, 20],' & @CRLF & _
				'"GUITabItem": "General",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "Non-Stop will try to run towards the loot without stopping until it is detected on screen, creating continuous movement of the character. The Stop method will make the character stop to retrieve the loot before continuing with the task he was doing (This applies to Spotfarm and dungeons).",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [495, 222],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Main",' & @CRLF & _
				'"iniProp": "HealthPlayerAt",' & @CRLF & _
				'"defaultValue": "60",' & @CRLF & _
				'"GUILabel": "Health player at (%)",' & @CRLF & _
				'"GUILabelPosition": [280, 255, 100, 20],' & @CRLF & _
				'"GUIVariable": "GUI_HealthPlayerAt",' & @CRLF & _
				'"GUITypeField": "numeric",' & @CRLF & _
				'"NumericMin": "10",' & @CRLF & _
				'"NumericMax": "90",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [390, 250, 100, 20],' & @CRLF & _
				'"GUITabItem": "General",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "Select the percentage of health that the character will try to maintain before using a potion. (This applies to Spotfarm, endless and dungeons)",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [495, 252],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Main",' & @CRLF & _
				'"iniProp": "IHavePetWithBlacksmith",' & @CRLF & _
				'"defaultValue": "No",' & @CRLF & _
				'"GUILabel": "I have pet to recycle",' & @CRLF & _
				'"GUILabelPosition": [280, 285, 100, 20],' & @CRLF & _
				'"GUIVariable": "GUI_IHavePetWithBlacksmith",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "Yes|No",' & @CRLF & _
				'"GUIVariablePosition": [390, 280, 100, 20],' & @CRLF & _
				'"GUITabItem": "General",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "If you select yes, the bot will try to use the pet to recycle the items.",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [495, 282],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
		'], ' & @CRLF & _
	'},' & @CRLF & _
	'{' & @CRLF & _
		'"name": "dungeon (Alpha)",' & @CRLF & _
		'"values": [' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Dungeon",' & @CRLF & _
				'"iniProp": "name",' & @CRLF & _
				'"defaultValue": "kikuras",' & @CRLF & _
				'"GUILabel": "Dungeon",' & @CRLF & _
				'"GUILabelPosition": [280, 45, 80, 20],' & @CRLF & _
				'"GUIVariable": "GUI_Dungeon",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [370, 40, 100, 20],' & @CRLF & _
				'"GUITabItem": "Dungeons",' & @CRLF & _
				'"GUIJSON": "JSON_dungeons",' & @CRLF & _
				'"GUIJSONKEY": "dungeons",' & @CRLF & _
				'"ComboEvent": "DungeonSelect",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Dungeon",' & @CRLF & _
				'"iniProp": "Team_solo",' & @CRLF & _
				'"defaultValue": "Solo",' & @CRLF & _
				'"GUILabel": "Team/Solo",' & @CRLF & _
				'"GUILabelPosition": [280, 105, 80, 20],' & @CRLF & _
				'"GUIVariable": "GUI_DungeonTeamSolo",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "Solo|Team",' & @CRLF & _
				'"GUIVariablePosition": [370, 100, 100, 20],' & @CRLF & _
				'"GUITabItem": "Dungeons",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Dungeon",' & @CRLF & _
				'"iniProp": "Time_to_exit",' & @CRLF & _
				'"defaultValue": "600",' & @CRLF & _
				'"GUILabel": "Time to force exit",' & @CRLF & _
				'"GUILabelPosition": [280, 135, 100, 20],' & @CRLF & _
				'"GUIVariable": "GUI_DungeonTimeToExit",' & @CRLF & _
				'"GUITypeField": "numeric",' & @CRLF & _
				'"NumericMin": "60",' & @CRLF & _
				'"NumericMax": "3600",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [370, 130, 100, 20],' & @CRLF & _
				'"GUITabItem": "Dungeons",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "Select the time in seconds that the bot will force the exit of the dungeon if it is not finished.",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [495, 132],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Dungeon",' & @CRLF & _
				'"iniProp": "Time_to_wait_party",' & @CRLF & _
				'"defaultValue": "400",' & @CRLF & _
				'"GUILabel": "Time to wait party",' & @CRLF & _
				'"GUILabelPosition": [280, 165, 100, 20],' & @CRLF & _
				'"GUIVariable": "GUI_DungeonTimeToWaitParty",' & @CRLF & _
				'"GUITypeField": "numeric",' & @CRLF & _
				'"NumericMin": "60",' & @CRLF & _
				'"NumericMax": "600",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [370, 160, 100, 20],' & @CRLF & _
				'"GUITabItem": "Dungeons",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "Select the time in seconds that the bot will wait for the party to be formed before starting the dungeon.",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [495, 162],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Dungeon",' & @CRLF & _
				'"iniProp": "text_count_dungeon",' & @CRLF & _
				'"defaultValue": "",' & @CRLF & _
				'"GUILabel": "Number of dungeons completed: 0",' & @CRLF & _
				'"GUILabelPosition": [280, 195, 200, 20],' & @CRLF & _
				'"GUIVariable": "text_count_dungeon",' & @CRLF & _
				'"GUITypeField": "help_text",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [],' & @CRLF & _
				'"GUITabItem": "Dungeons",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
			'},' & @CRLF & _
		'], ' & @CRLF & _
	'},' & @CRLF & _
	'{' & @CRLF & _
		'"name": "Cyrangar",' & @CRLF & _
		'"values": [' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Cyrangar",' & @CRLF & _
				'"iniProp": "Mode",' & @CRLF & _
				'"defaultValue": "Endless",' & @CRLF & _
				'"GUILabel": "Mode",' & @CRLF & _
				'"GUILabelPosition": [280, 45, 80, 20],' & @CRLF & _
				'"GUIVariable": "GUI_Mode",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "Endless",' & @CRLF & _
				'"GUIVariablePosition": [370, 40, 100, 20],' & @CRLF & _
				'"GUITabItem": "Cyrangar",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Cyrangar",' & @CRLF & _
				'"iniProp": "StayAtTheDoor",' & @CRLF & _
				'"defaultValue": "No",' & @CRLF & _
				'"GUILabel": "Stay at the door",' & @CRLF & _
				'"GUILabelPosition": [280, 75, 80, 20],' & @CRLF & _
				'"GUIVariable": "GUI_StayAtTheDoor",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "Yes|No",' & @CRLF & _
				'"GUIVariablePosition": [370, 70, 100, 20],' & @CRLF & _
				'"GUITabItem": "Cyrangar",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "If you select yes, the bot will stay at the door all the time.",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [475, 72],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Cyrangar",' & @CRLF & _
				'"iniProp": "Time_to_exit",' & @CRLF & _
				'"defaultValue": "600",' & @CRLF & _
				'"GUILabel": "Time to force Fight",' & @CRLF & _
				'"GUILabelPosition": [280, 105, 100, 20],' & @CRLF & _
				'"GUIVariable": "GUI_Time_to_exit",' & @CRLF & _
				'"GUITypeField": "numeric",' & @CRLF & _
				'"NumericMin": "60",' & @CRLF & _
				'"NumericMax": "999",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [370, 100, 100, 20],' & @CRLF & _
				'"GUITabItem": "Cyrangar",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "Select the time in seconds that the bot will force the exit of the defense. If you dont want to force the exit, select high value.",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [495, 102],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Cyrangar",' & @CRLF & _
				'"iniProp": "get_fog_bane",' & @CRLF & _
				'"defaultValue": "Yes",' & @CRLF & _
				'"GUILabel": "Get Fog Bane",' & @CRLF & _
				'"GUILabelPosition": [280, 135, 100, 20],' & @CRLF & _
				'"GUIVariable": "GUI_get_fog_bane",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "Yes|No",' & @CRLF & _
				'"GUIVariablePosition": [370, 130, 100, 20],' & @CRLF & _
				'"GUITabItem": "Cyrangar",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "If you select yes, the bot will try to get the fog bane.",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [475, 132],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
		'],' & @CRLF & _
	'},' & @CRLF & _ 
	'{' & @CRLF & _
		'"name": "fish",' & @CRLF & _
		'"values": [' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Fish",' & @CRLF & _
				'"iniProp": "FishType",' & @CRLF & _
				'"defaultValue": "Gold",' & @CRLF & _
				'"GUILabel": "Fish Type",' & @CRLF & _
				'"GUILabelPosition": [280, 45, 80, 20],' & @CRLF & _
				'"GUIVariable": "GUI_FishType",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "White|Blue|Gold|Legendary|Epic",' & @CRLF & _
				'"GUIVariablePosition": [370, 40, 100, 20],' & @CRLF & _
				'"GUITabItem": "Fish",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "Legendary and epic fish do not guarantee capture, the bot simply waits longer to fish them.",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [475, 42],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Fish",' & @CRLF & _
				'"iniProp": "Fish_Iter",' & @CRLF & _
				'"defaultValue": "10",' & @CRLF & _
				'"GUILabel": "Fish Iterations",' & @CRLF & _
				'"GUILabelPosition": [280, 75, 80, 20],' & @CRLF & _
				'"GUIVariable": "GUI_FishIterations",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "1|5|10",' & @CRLF & _
				'"GUIVariablePosition": [370, 70, 100, 20],' & @CRLF & _
				'"GUITabItem": "Fish",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Fish",' & @CRLF & _
				'"iniProp": "Maps",' & @CRLF & _
				'"defaultValue": "cementery",' & @CRLF & _
				'"GUILabel": "Fish Maps",' & @CRLF & _
				'"GUILabelPosition": [280, 105, 80, 20],' & @CRLF & _
				'"GUIVariable": "GUI_FishMaps",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [370, 100, 100, 20],' & @CRLF & _
				'"GUITabItem": "Fish",' & @CRLF & _
				'"GUIJSON": "JSON_runs",' & @CRLF & _
				'"GUIJSONKEY": "maps",' & @CRLF & _
			'},' & @CRLF & _
		'], ' & @CRLF & _
	'},' & @CRLF & _
	'{' & @CRLF & _
		'"name": "fish 2.0",' & @CRLF & _
		'"values": [' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Fish2",' & @CRLF & _
				'"iniProp": "Fish2Type",' & @CRLF & _
				'"defaultValue": "Gold",' & @CRLF & _
				'"GUILabel": "Fish Type",' & @CRLF & _
				'"GUILabelPosition": [280, 45, 80, 20],' & @CRLF & _
				'"GUIVariable": "GUI_Fish2Type",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "White|Blue|Gold|Legendary|Epic",' & @CRLF & _
				'"GUIVariablePosition": [370, 40, 100, 20],' & @CRLF & _
				'"GUITabItem": "Fish2",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "Legendary and epic fish do not guarantee capture, the bot simply waits longer to fish them.",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [475, 42],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Fish2",' & @CRLF & _
				'"iniProp": "Fish2_IterMin",' & @CRLF & _
				'"defaultValue": "10",' & @CRLF & _
				'"GUILabel": "MIN Fish Iterations",' & @CRLF & _
				'"GUILabelPosition": [280, 75, 100, 20],' & @CRLF & _
				'"GUIVariable": "GUI_Fish2IterationsMin",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "1|2|3|4|5|6|7|8|9|10|11|12|13|14|15",' & @CRLF & _
				'"GUIVariablePosition": [370, 70, 50, 20],' & @CRLF & _
				'"GUITabItem": "Fish2",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"ComboEvent": "SetMinMaxFishIters",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Fish2",' & @CRLF & _
				'"iniProp": "Fish2_IterMax",' & @CRLF & _
				'"defaultValue": "10",' & @CRLF & _
				'"GUILabel": "MAX Fish Iterations",' & @CRLF & _
				'"GUILabelPosition": [430, 75, 100, 20],' & @CRLF & _
				'"GUIVariable": "GUI_Fish2IterationsMax",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "1|2|3|4|5|6|7|8|9|10|11|12|13|14|15",' & @CRLF & _
				'"GUIVariablePosition": [530, 70, 50, 20],' & @CRLF & _
				'"GUITabItem": "Fish2",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "The bot will select a random number of iterations between the minimum and maximum values selected here.",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [585, 72],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
				'"ComboEvent": "SetMinMaxFishIters",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Fish2",' & @CRLF & _
				'"iniProp": "Maps",' & @CRLF & _
				'"defaultValue": "cementery",' & @CRLF & _
				'"GUILabel": "Fish Maps",' & @CRLF & _
				'"GUILabelPosition": [280, 105, 80, 20],' & @CRLF & _
				'"GUIVariable": "GUI_Fish2Maps",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [370, 100, 100, 20],' & @CRLF & _
				'"GUITabItem": "Fish2",' & @CRLF & _
				'"GUIJSON": "JSON_runs",' & @CRLF & _
				'"GUIJSONKEY": "maps",' & @CRLF & _
				'"ComboEvent": "FishZonesSelect",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Fish2",' & @CRLF & _
				'"iniProp": "Zones",' & @CRLF & _
				'"defaultValue": "bridge1",' & @CRLF & _
				'"GUILabel": "Fish Zone",' & @CRLF & _
				'"GUILabelPosition": [280, 135, 80, 20],' & @CRLF & _
				'"GUIVariable": "GUI_FishZones",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "bridge1",' & @CRLF & _
				'"GUIVariablePosition": [370, 130, 200, 20],' & @CRLF & _
				'"GUITabItem": "Fish2",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "Select the zone where you want to fish. If you select random, the bot will change the zone every iteratios selected in the previous field.",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [575, 132],' & @CRLF & _
				'"HELPIconCallback": "HELP_Fish_zones",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Fish2",' & @CRLF & _
				'"iniProp": "roundcicles",' & @CRLF & _
				'"defaultValue": "3",' & @CRLF & _
				'"GUILabel": "Loot turns",' & @CRLF & _
				'"GUILabelPosition": [470, 165, 80, 20],' & @CRLF & _
				'"GUIVariable": "GUI_Fish2roundcicles",' & @CRLF & _
				'"GUITypeField": "numeric",' & @CRLF & _
				'"NumericMin": "0",' & @CRLF & _
				'"NumericMax": "10",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [530, 160, 50, 20],' & @CRLF & _
				'"GUITabItem": "Fish2",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "Select how many times you want the character to turn around to loot the fish exchange. (You may want to leave it at 0 if you have a pet).",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [425, 192],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Fish2",' & @CRLF & _
				'"iniProp": "CHeckInventoryPercent",' & @CRLF & _
				'"defaultValue": "40",' & @CRLF & _
				'"GUILabel": "Check Inventory (%)",' & @CRLF & _
				'"GUILabelPosition": [280, 195, 100, 20],' & @CRLF & _
				'"GUIVariable": "GUI_CheckInventoryPercent",' & @CRLF & _
				'"GUITypeField": "numeric",' & @CRLF & _
				'"NumericMin": "5",' & @CRLF & _
				'"NumericMax": "90",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [390, 190, 100, 20],' & @CRLF & _
				'"GUITabItem": "Fish2",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "Select the percentage of inventory that the bot will try to maintain before going to sell the Dust and Scrap.",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [495, 192],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Fish2",' & @CRLF & _
				'"iniProp": "text_count_yellow_dust",' & @CRLF & _
				'"defaultValue": "",' & @CRLF & _
				'"GUILabel": "Yellow dust: 0",' & @CRLF & _
				'"GUILabelPosition": [280, 225, 200, 20],' & @CRLF & _
				'"GUIVariable": "text_count_yellow_dust",' & @CRLF & _
				'"GUITypeField": "help_text",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [],' & @CRLF & _
				'"GUITabItem": "Fish2",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Fish2",' & @CRLF & _
				'"iniProp": "text_count_scrap",' & @CRLF & _
				'"defaultValue": "",' & @CRLF & _
				'"GUILabel": "Scrap: 0",' & @CRLF & _
				'"GUILabelPosition": [280, 255, 200, 20],' & @CRLF & _
				'"GUIVariable": "text_count_scrap",' & @CRLF & _
				'"GUITypeField": "help_text",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [],' & @CRLF & _
				'"GUITabItem": "Fish2",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Fish2",' & @CRLF & _
				'"iniProp": "text_actual_iter",' & @CRLF & _
				'"defaultValue": "",' & @CRLF & _
				'"GUILabel": "Actual iteration: 0",' & @CRLF & _
				'"GUILabelPosition": [280, 285, 200, 20],' & @CRLF & _
				'"GUIVariable": "text_actual_iter",' & @CRLF & _
				'"GUITypeField": "help_text",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [],' & @CRLF & _
				'"GUITabItem": "Fish2",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
			'},' & @CRLF & _
		'], ' & @CRLF & _
	'},' & @CRLF & _
	'{' & @CRLF & _
		'"name": "SpotFarm",' & @CRLF & _
		'"values": [' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "SpotFarm",' & @CRLF & _
				'"iniProp": "SpotFarmMap",' & @CRLF & _
				'"defaultValue": "shassarsea",' & @CRLF & _
				'"GUILabel": "SpotFarm Map",' & @CRLF & _
				'"GUILabelPosition": [280, 45, 180, 20],' & @CRLF & _
				'"GUIVariable": "GUI_SpotFarmMap",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [500, 40, 100, 20],' & @CRLF & _
				'"GUITabItem": "SpotFarm",' & @CRLF & _
				'"GUIJSON": "JSON_runs",' & @CRLF & _
				'"GUIJSONKEY": "maps",' & @CRLF & _		
				'"ComboEvent": "CustomModelActive",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "SpotFarm",' & @CRLF & _
				'"iniProp": "SpotFarmCustomModelMap",' & @CRLF & _
				'"defaultValue": "",' & @CRLF & _
				'"GUILabel": "Model map zone",' & @CRLF & _
				'"GUILabelPosition": [280, 75, 180, 20],' & @CRLF & _
				'"GUIVariable": "GUI_SpotFarmCustomModelMap",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [500, 70, 100, 20],' & @CRLF & _
				'"GUITabItem": "SpotFarm",' & @CRLF & _
				'"GUIJSON": "JSON_runs",' & @CRLF & _
				'"GUIJSONKEY": "maps",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "SpotFarm",' & @CRLF & _
				'"iniProp": "AcceptPartyInvites",' & @CRLF & _
				'"defaultValue": "Yes",' & @CRLF & _
				'"GUILabel": "Accept Party Invites",' & @CRLF & _
				'"GUILabelPosition": [280, 105, 180, 20],' & @CRLF & _
				'"GUIVariable": "GUI_AcceptPartyInvites",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "Yes|No",' & @CRLF & _
				'"GUIVariablePosition": [500, 100, 100, 20],' & @CRLF & _
				'"GUITabItem": "SpotFarm",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "If you select yes, the bot will accept party invites from other players. (default yes)",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [605, 102],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "SpotFarm",' & @CRLF & _
				'"iniProp": "CheckPartyLeader",' & @CRLF & _
				'"defaultValue": "Yes",' & @CRLF & _
				'"GUILabel": "Check Party Leader",' & @CRLF & _
				'"GUILabelPosition": [280, 135, 180, 20],' & @CRLF & _
				'"GUIVariable": "GUI_CheckPartyLeader",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "Yes|No",' & @CRLF & _
				'"GUIVariablePosition": [500, 130, 100, 20],' & @CRLF & _
				'"GUITabItem": "SpotFarm",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "If you select yes, the bot will check if you are the party leader, then it will pass the leader to the next player in the party list. (default yes)",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [605, 132],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "SpotFarm",' & @CRLF & _
				'"iniProp": "CheckBestyaryEveryIfNotification",' & @CRLF & _
				'"defaultValue": "10",' & @CRLF & _
				'"GUILabel": "Check Bestiary every x if notification FOUND",' & @CRLF & _
				'"GUILabelPosition": [280, 165, 250, 20],' & @CRLF & _
				'"GUIVariable": "GUI_CheckBestyaryEveryIfNotification",' & @CRLF & _
				'"GUITypeField": "numeric",' & @CRLF & _
				'"NumericMin": "10",' & @CRLF & _
				'"NumericMax": "300",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [500, 160, 100, 20],' & @CRLF & _
				'"GUITabItem": "SpotFarm",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "Select the time in seconds that the bot will check the bestiary if a left bell notification is FOUND. (default 10)",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [605, 162],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "SpotFarm",' & @CRLF & _
				'"iniProp": "CheckBestyaryEveryIfNotificationNotFound",' & @CRLF & _
				'"defaultValue": "120",' & @CRLF & _
				'"GUILabel": "Check Bestiary every x if notification NOT found",' & @CRLF & _
				'"GUILabelPosition": [280, 195, 250, 20],' & @CRLF & _
				'"GUIVariable": "GUI_CheckBestyaryEveryIfNotificationNotFound",' & @CRLF & _
				'"GUITypeField": "numeric",' & @CRLF & _
				'"NumericMin": "10",' & @CRLF & _
				'"NumericMax": "600",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [500, 190, 100, 20],' & @CRLF & _
				'"GUITabItem": "SpotFarm",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "Select the time in seconds that the bot will check the bestiary if a left bell notification is NOT FOUND. (default 120)",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [605, 192],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "SpotFarm",' & @CRLF & _
				'"iniProp": "StopIfDetectMonster",' & @CRLF & _
				'"defaultValue": "Yes",' & @CRLF & _
				'"GUILabel": "Stop if detect monster",' & @CRLF & _
				'"GUILabelPosition": [280, 225, 180, 20],' & @CRLF & _
				'"GUIVariable": "GUI_StopIfDetectMonster",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "Yes|No",' & @CRLF & _
				'"GUIVariablePosition": [500, 220, 100, 20],' & @CRLF & _
				'"GUITabItem": "SpotFarm",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "If you select YES, when the bot detects monsters around it it will try to stop to defeat them before continuing walking.",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [605, 222],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "SpotFarm",' & @CRLF & _
				'"iniProp": "text_count_yellow_dust2",' & @CRLF & _
				'"defaultValue": "",' & @CRLF & _
				'"GUILabel": "Yellow dust: 0",' & @CRLF & _
				'"GUILabelPosition": [280, 255, 200, 20],' & @CRLF & _
				'"GUIVariable": "text_count_yellow_dust2",' & @CRLF & _
				'"GUITypeField": "help_text",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [],' & @CRLF & _
				'"GUITabItem": "SpotFarm",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "SpotFarm",' & @CRLF & _
				'"iniProp": "text_count_scrap2",' & @CRLF & _
				'"defaultValue": "",' & @CRLF & _
				'"GUILabel": "Scrap: 0",' & @CRLF & _
				'"GUILabelPosition": [280, 285, 200, 20],' & @CRLF & _
				'"GUIVariable": "text_count_scrap2",' & @CRLF & _
				'"GUITypeField": "help_text",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [],' & @CRLF & _
				'"GUITabItem": "SpotFarm",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
			'},' & @CRLF & _
		']' & @CRLF & _
	'},' & @CRLF & _
	'{' & @CRLF & _
		'"name": "Telegram",' & @CRLF & _
		'"values": [' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Telegram",' & @CRLF & _
				'"iniProp": "text",' & @CRLF & _
				'"defaultValue": "",' & @CRLF & _
				'"GUILabel": "By configuring telegram, you will receive a telegram message with a screenshot of the game when any player whispers (purple message) to you in private, so you can see what is happening at that moment",' & @CRLF & _
				'"GUILabelPosition": [280, 45, 330, 50],' & @CRLF & _
				'"GUIVariable": "",' & @CRLF & _
				'"GUITypeField": "help_text",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [],' & @CRLF & _
				'"GUITabItem": "Telegram",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Telegram",' & @CRLF & _
				'"iniProp": "Active",' & @CRLF & _
				'"defaultValue": "No",' & @CRLF & _
				'"GUILabel": "Active",' & @CRLF & _
				'"GUILabelPosition": [280, 105, 80, 20],' & @CRLF & _
				'"GUIVariable": "GUI_TelegramActive",' & @CRLF & _
				'"GUITypeField": "combo",' & @CRLF & _
				'"GUIComboValues": "Yes|No",' & @CRLF & _
				'"GUIVariablePosition": [370, 100, 100, 20],' & @CRLF & _
				'"GUITabItem": "Telegram",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"HELPIconFile": "shell32.dll",' & @CRLF & _
				'"HELPIconIndex": 24,' & @CRLF & _
				'"HELPIconText": "Activate or deactivate telegram notifications.",' & @CRLF & _
				'"HELPIconSize": 16,' & @CRLF & _
				'"HELPIconPosition": [475, 102],' & @CRLF & _
				'"HELPIconCallback": "",' & @CRLF & _
				'"ComboEvent": "TelegramActive",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Telegram",' & @CRLF & _
				'"iniProp": "Token",' & @CRLF & _
				'"defaultValue": "",' & @CRLF & _
				'"GUILabel": "Confirmation code",' & @CRLF & _
				'"GUILabelPosition": [280, 135, 90, 20],' & @CRLF & _
				'"GUIVariable": "GUI_TelegramToken",' & @CRLF & _
				'"GUITypeField": "readonly",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [370, 130, 230, 20],' & @CRLF & _
				'"GUITabItem": "Telegram",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"hide": "True",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Telegram",' & @CRLF & _
				'"iniProp": "text2",' & @CRLF & _
				'"defaultValue": "",' & @CRLF & _
				'"GUILabel": "To activate telegram notifications, you must send the following message \"/configure\" (without quotes) to your Telegram bot",' & @CRLF & _
				'"GUILabelPosition": [280, 165, 330, 50],' & @CRLF & _
				'"GUIVariable": "GUI_text2",' & @CRLF & _
				'"GUITypeField": "help_text",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [],' & @CRLF & _
				'"GUITabItem": "Telegram",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"hide": "True",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Telegram",' & @CRLF & _
				'"iniProp": "text3",' & @CRLF & _
				'"defaultValue": "",' & @CRLF & _
				'"GUILabel": "Configure your Telegram bot handle in the settings",' & @CRLF & _
				'"GUISetFont": "Arial",' & @CRLF & _
				'"GUISetSize": 10,' & @CRLF & _
				'"GUISetColor": 0x2986CC,' & @CRLF & _
				'"GUISetCursor": "Hand",' & @CRLF & _
				'"GUIWM_COMMAND": "GoToTelegramurl",' & @CRLF & _
				'"GUILabelPosition": [280, 205, 330, 50],' & @CRLF & _
				'"GUIVariable": "GUI_text3",' & @CRLF & _
				'"GUITypeField": "help_text",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [],' & @CRLF & _
				'"GUITabItem": "Telegram",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"hide": "True",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Telegram",' & @CRLF & _
				'"iniProp": "text4",' & @CRLF & _
				'"defaultValue": "",' & @CRLF & _
				'"GUILabel": "You will need to enter the email with which you registered with the bot and the confirmation code provided on this screen.",' & @CRLF & _
				'"GUILabelPosition": [280, 245, 330, 50],' & @CRLF & _
				'"GUIVariable": "GUI_text4",' & @CRLF & _
				'"GUITypeField": "help_text",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [],' & @CRLF & _
				'"GUITabItem": "Telegram",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
				'"hide": "True",' & @CRLF & _
			'},' & @CRLF & _
		']' & @CRLF & _
	'},' & @CRLF & _
	'{' & @CRLF & _
		'"name": "LDPayer",' & @CRLF & _
		'"values": [' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Main",' & @CRLF & _
				'"iniProp": "VMName",' & @CRLF & _
				'"defaultValue": "VMName",' & @CRLF & _
				'"GUILabel": "VM Name",' & @CRLF & _
				'"GUILabelPosition": [280, 45, 80, 20],' & @CRLF & _
				'"GUIVariable": "GUI_VMName",' & @CRLF & _
				'"GUITypeField": "text",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [370, 40, 100, 20],' & @CRLF & _
				'"GUITabItem": "General",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "Main",' & @CRLF & _
				'"iniProp": "LDPath",' & @CRLF & _
				'"defaultValue": "C:\\LDPlayer\\LDPlayer9\\ldconsole.exe",' & @CRLF & _
				'"GUILabel": "LD Path",' & @CRLF & _
				'"GUILabelPosition": [280, 75, 80, 20],' & @CRLF & _
				'"GUIVariable": "GUI_LDPath",' & @CRLF & _
				'"GUITypeField": "textExplore",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [370, 70, 210, 20],' & @CRLF & _
				'"GUITabItem": "General",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
			'},' & @CRLF & _
		']' & @CRLF & _
	'},' & @CRLF & _
	'{' & @CRLF & _
		'"name": "lastrun",' & @CRLF & _
		'"values": [' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "LastRun",' & @CRLF & _
				'"iniProp": "mapName",' & @CRLF & _
				'"defaultValue": "cementery",' & @CRLF & _
				'"GUILabel": "",' & @CRLF & _
				'"GUILabelPosition": [],' & @CRLF & _
				'"GUIVariable": "",' & @CRLF & _
				'"GUITypeField": "internal",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [],' & @CRLF & _
				'"GUITabItem": "",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "LastRun",' & @CRLF & _
				'"iniProp": "step",' & @CRLF & _
				'"defaultValue": "step1",' & @CRLF & _
				'"GUILabel": "",' & @CRLF & _
				'"GUILabelPosition": [],' & @CRLF & _
				'"GUIVariable": "",' & @CRLF & _
				'"GUITypeField": "internal",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [],' & @CRLF & _
				'"GUITabItem": "",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
			'},' & @CRLF & _
			'{' & @CRLF & _
				'"iniGroup": "LastRun",' & @CRLF & _
				'"iniProp": "position",' & @CRLF & _
				'"defaultValue": "0",' & @CRLF & _
				'"GUILabel": "",' & @CRLF & _
				'"GUILabelPosition": [],' & @CRLF & _
				'"GUIVariable": "",' & @CRLF & _
				'"GUITypeField": "internal",' & @CRLF & _
				'"GUIComboValues": "",' & @CRLF & _
				'"GUIVariablePosition": [],' & @CRLF & _
				'"GUITabItem": "",' & @CRLF & _
				'"GUIJSON": "",' & @CRLF & _
				'"GUIJSONKEY": "",' & @CRLF & _
			'},' & @CRLF & _
		'], ' & @CRLF & _
	'}' & @CRLF & _
'],' & @CRLF & _
'"tab": {' & @CRLF & _
	'"generalTab": [' & @CRLF & _
		'{' & @CRLF & _
			'"name": "generalTab",' & @CRLF & _
			'"values": [270, 10, 360, 290], ' & @CRLF & _
		'},' & @CRLF & _
	'],' & @CRLF & _
'},' & @CRLF & _
'"buttons": {' & @CRLF & _
	'"guibuttons": [' & @CRLF & _
		'{' & @CRLF & _
			'"name": "stop",' & @CRLF & _
			'"values": [420, 310, 100, 20, "Pause (F9)"],' & @CRLF & _
			'"callback": "Stop",' & @CRLF & _
			'"hotkey": "{F9}",' & @CRLF & _
			'"hotkeyFunc": "Stop",' & @CRLF & _
			'"hide": "true",' & @CRLF & _
		'},' & @CRLF & _
		'{' & @CRLF & _
			'"name": "start",' & @CRLF & _
			'"values": [420, 310, 100, 20, "Start (F8)"],' & @CRLF & _
			'"callback": "Start",' & @CRLF & _
			'"hotkey": "{F8}",' & @CRLF & _
			'"hotkeyFunc": "Start",' & @CRLF & _
			'"hide": "false",' & @CRLF & _
		'},' & @CRLF & _
		'{' & @CRLF & _
			'"name": "exit",' & @CRLF & _
			'"values": [530, 310, 100, 20, "Exit (F10)"],' & @CRLF & _
			'"callback": "Terminate",' & @CRLF & _
			'"hotkey": "{F10}",' & @CRLF & _
			'"hotkeyFunc": "Terminate",' & @CRLF & _
			'"hide": "false",' & @CRLF & _
		'},' & @CRLF & _
		'{' & @CRLF & _
			'"name": "save",' & @CRLF & _
			'"values": [310, 310, 100, 20, "Save (F7)"],' & @CRLF & _
			'"callback": "Save",' & @CRLF & _
			'"hotkey": "{F7}",' & @CRLF & _
			'"hotkeyFunc": "Save",' & @CRLF & _
			'"hide": "false",' & @CRLF & _
		'},' & @CRLF & _
	'],' & @CRLF & _
'}' & @CRLF & _
'}' 