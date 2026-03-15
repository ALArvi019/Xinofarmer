Global $JSON_screens = '{ ' & @CRLF & _
	'"screens": [' & @CRLF & _
		'{ ' & @CRLF & _
			'"name": "game_die", "positions": [' & @CRLF & _
				'{ "x": 259, "y": 442, "color": "0x652711" },' & @CRLF & _
				'{ "x": 345, "y": 441, "color": "0x5D2610" },' & @CRLF & _
				'{ "x": 576, "y": 233, "color": "0x91472D" }'  & @CRLF & _
			'],' & @CRLF & _
			'"function": "game_die",' & @CRLF & _
			'"images_to_find": [' & @CRLF & _
				'{ "image": "character_die" } ' & @CRLF & _
			']' & @CRLF & _
		'},' & @CRLF & _
		'{ ' & @CRLF & _
			'"name": "special_event", "positions": [' & @CRLF & _
				'{ "x": 10, "y": 10, "color": "0x652711" },' & @CRLF & _
				'{ "x": 10, "y": 10, "color": "0x5D2610" },' & @CRLF & _
				'{ "x": 10, "y": 10, "color": "0x91472D" }'  & @CRLF & _
			'],' & @CRLF & _
			'"function": "special_event",' & @CRLF & _
			'"images_to_find": [' & @CRLF & _
				'{ "image": "dungeon_special_event" } ' & @CRLF & _
			']' & @CRLF & _
		'},' & @CRLF & _
		'{ ' & @CRLF & _
			'"name": "main_screen", ' & @CRLF & _
			'"positions": [' & @CRLF & _
				'{ "x": 910, "y": 89, "color": "0xCFC4AA" },' & @CRLF & _
				'{ "x": 157, "y": 97, "color": "0x006FB2" },' & @CRLF & _
				'{ "x": 909, "y": 143, "color": "0xCFC5AA" },' & @CRLF & _
		    '],' & @CRLF & _
			'"function": "game_main_screen",' & @CRLF & _
			'"images_to_find": [' & @CRLF & _
				'{ "image": "main_screen" } ' & @CRLF & _
			']' & @CRLF & _ 
		'},' & @CRLF & _
		'{ ' & @CRLF & _
			'"name": "select_character", ' & @CRLF & _
			'"positions": [' & @CRLF & _
				'{ "x": 923, "y": 58, "color": "0x882C0C" },' & @CRLF & _
				'{ "x": 790, "y": 535, "color": "0x622612" },' & @CRLF & _
				'{ "x": 804, "y": 522, "color": "0xEEDAB1" }' & @CRLF & _
				'],' & @CRLF & _
			'"function": "game_select_character",' & @CRLF & _
			'"images_to_find": [' & @CRLF & _
				'{ "image": "character_selection" } ' & @CRLF & _
			']' & @CRLF & _
		'},' & @CRLF & _
		'{ ' & @CRLF & _
			'"name": "select_character_english", ' & @CRLF & _
			'"positions": [' & @CRLF & _
				'{ "x": 923, "y": 58, "color": "0x882C0C" },' & @CRLF & _
				'{ "x": 790, "y": 535, "color": "0x622612" },' & @CRLF & _
				'{ "x": 804, "y": 522, "color": "0xF0DAB0" }' & @CRLF & _
			'],' & @CRLF & _
			'"function": "game_select_character" ' & @CRLF & _
		'},' & @CRLF & _
	'{ "name": "blizzard_message_shit", "positions": [' & @CRLF & _
		'{ "x": 313, "y": 358, "color": "0x3D1F1A" },' & @CRLF & _
		'{ "x": 442, "y": 352, "color": "0x3E201C" },' & @CRLF & _
		'{ "x": 638, "y": 355, "color": "0x42211D" }],' & @CRLF & _
	'"function": "game_blizzard_message_shit" },' & @CRLF & _
	'{ "name": "blizzard_message_local_events", "positions": [' & @CRLF & _
		'{ "x": 893, "y": 119, "color": "0xC7A589" },' & @CRLF & _
		'{ "x": 899, "y": 120, "color": "0x8A3514" }],' & @CRLF & _
	'"function": "game_blizzard_message_local_events" },' & @CRLF & _
	'{ "name": "blizzard_message_events", "positions": [' & @CRLF & _
		'{ "x": 924, "y": 105, "color": "0xD8C4A0" }],' & @CRLF & _
	'"function": "game_blizzard_message_events" },' & @CRLF & _
	'{ "name": "game_die_en", "positions": [' & @CRLF & _
		'{ "x": 259, "y": 442, "color": "0x652711" },' & @CRLF & _
		'{ "x": 345, "y": 441, "color": "0x5D2610" },' & @CRLF & _
		'{ "x": 576, "y": 233, "color": "0x602616" }],' & @CRLF & _
	'"function": "game_die" },' & @CRLF & _
	'{ "name": "game_disconnect", "positions": [' & @CRLF & _
		'{ "x": 417, "y": 354, "color": "0x46231E" },' & @CRLF & _
		'{ "x": 492, "y": 356, "color": "0xA99D7F" },' & @CRLF & _
		'{ "x": 546, "y": 354, "color": "0x391D1A" }],' & @CRLF & _
	'"function": "game_disconnect" },' & @CRLF & _
	'{ "name": "elder_rift", "positions": [' & @CRLF & _
		'{ "x": 543, "y": 492, "color": "0x5C230D" },' & @CRLF & _
		'{ "x": 897, "y": 496, "color": "0x62240F" },' & @CRLF & _
		'{ "x": 934, "y": 59, "color": "0x903815" },' & @CRLF & _
		'{ "x": 153, "y": 60, "color": "0x3F3023" }],' & @CRLF & _
	'"function": "game_elder_rift" },' & @CRLF & _
		'{ ' & @CRLF & _
			'"name": "fishing", "positions": [' & @CRLF & _
				'{ "x": 851, "y": 454, "color": "0x9B917D" },' & @CRLF & _
				'{ "x": 878, "y": 347, "color": "0xCF9E0D" }' & @CRLF & _
			'],' & @CRLF & _
			'"function": "game_fishing" ,' & @CRLF & _
			'"images_to_find": [' & @CRLF & _
				'{ "image": "fishing" } ' & @CRLF & _
			']' & @CRLF & _
		'},' & @CRLF & _
	'{ "name": "blizz_support_web", "positions": [' & @CRLF & _
		'{ "x": 921, "y": 531, "color": "0x158EFD" },' & @CRLF & _
		'{ "x": 922, "y": 237, "color": "0x178BFF" }],' & @CRLF & _
	'"function": "game_blizz_support_web" },' & @CRLF & _
	'{ "name": "ldpayer_stuck", "positions": [' & @CRLF & _
		'{ "x": 246, "y": 323, "color": "0x008577" },' & @CRLF & _
		'{ "x": 702, "y": 217, "color": "0xFFFFFF" }],' & @CRLF & _
	'"function": "game_ldpayer_stuck" },' & @CRLF & _
	'{ "name": "ldpayer_stuck2", "positions": [' & @CRLF & _
		'{ "x": 247, "y": 374, "color": "0x008577" },' & @CRLF & _
		'{ "x": 633, "y": 235, "color": "0xFFFFFF" }],' & @CRLF & _
	'"function": "game_ldpayer_stuck2" },' & @CRLF & _
	'{ "name": "any_open_screen_last_property", "positions": [' & @CRLF & _
		'{ "x": 927, "y": 72, "color": "0x792E12" }],' & @CRLF & _
	'"function": "game_any_open_screen_last_property" },' & @CRLF & _
		'{ ' & @CRLF & _
			'"name": "in_game", "positions": [' & @CRLF & _
				'{ "x": 884, "y": 286, "color": "0x851711" },' & @CRLF & _
				'{ "x": 881, "y": 281, "color": "0xDF3524" },' & @CRLF & _
				'{ "x": 886, "y": 287, "color": "0x791310" }' & @CRLF & _
			'],' & @CRLF & _
			'"function": "game_in_game",' & @CRLF & _
			'"images_to_find": [' & @CRLF & _
				'{ "image": "in_game" } ' & @CRLF & _
			']' & @CRLF & _
		'},' & @CRLF & _
']}' 