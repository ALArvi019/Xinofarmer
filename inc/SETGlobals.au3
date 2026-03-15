;~ AutoItSetOption("TCPTimeout", 1000)

Global $hGUILogin, $hGUIDownload, $hGUI, $cEdit
Global $isPaused = False
Global $isStarted = False
Global $masterCount = 0
Global $firstRun = True
Global $StopBotAfter = TimerInit()
Global $logEvery30Minutes = TimerInit()
Global $logEvery1Minutes = TimerInit()
Global $XF_Username = ""
Global $XF_LefTime = ""
Global $XF_Timer = 0
Global $XF_Last_Timer = 0
Global $XF_Label_Running_Time
Global $XF_Domain = "example.com" ; Set your domain here
Global $XF_Masterkey = "CHANGE_ME_16CHARS" ; Set your master key here (16 characters)
Global $XF_ActualDifficult = "init"
Global $XF_2ndScript_SOCKET = False
Global $XF_clave_registro = "HKEY_CURRENT_USER\Software\XinoFarmer"
Global $XF_image_folder =  @ScriptDir & "\inc\img"
Global $spotFarmRunning = False
Global $dungeonRunning = False
Global $fishingRunning = False
Global $count_dungeon = 0
Global $count_yellow_dust = 0
Global $count_scrap = 0
Global $foundBlacksmithInsideDungeon = False
Global $replay_dungeon = 'NO'
Global $endlessRunning = False
Global $Setup_Telegram_IsConfig = False
Global $Setup_Main_CheckDifficult = False

