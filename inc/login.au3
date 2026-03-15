Func _ShowLoginScreen()

	$GUIWidth = 650
	$GUIHeight = 340

	;~ create gui to login
	$hGUILogin = GUICreate("XinoFarmer", $GUIWidth, $GUIHeight)

	$AccessData = LoadLoginDataInRegistry()
	;~ $datos = StringSplit($AccessData, "@|@")
	If $AccessData <> "" Then
		$RegUsername = StringSplit($AccessData, "|")[1]
		$RegPassword = StringSplit($AccessData, "|")[2]
		$REgRemember = 1
	Else
		$RegUsername = ""
		$RegPassword = ""
		$REgRemember = 0
	EndIf
	

	;~ create label for username field in the center of the screen
	$hUsernameLabel = GUICtrlCreateLabel("Email:", $GUIWidth / 2 - 100, 10, 100, 20)
	;~ create text field for username
	$hUsername = GUICtrlCreateInput($RegUsername, $GUIWidth / 2 - 100, 40, 200, 20)

	;~ create label for password
	$hPasswordLabel = GUICtrlCreateLabel("Password:", $GUIWidth / 2 - 100, 70, 100, 20)
	;~ create password field for password with asterisks
	$hPassword = GUICtrlCreateInput($RegPassword, $GUIWidth / 2 - 100, 100, 200, 20, $ES_PASSWORD)



	;~ create label for the checkbox to remember the username and password
	$hRememberLabel = GUICtrlCreateLabel("Remember me:", $GUIWidth / 2 - 100, 130, 100, 20)
	;~ create checkbox to remember the username and password
	$hRemember = GUICtrlCreateCheckbox("", $GUIWidth / 2 - 100, 160, 200, 20)
	GUICtrlSetState($hRemember, $REgRemember)

	;~ create button to login
	$hLogin = GUICtrlCreateButton("Login", $GUIWidth / 2 - 100, 190, 200, 20)

	;~ create button to register
	$hRegister = GUICtrlCreateButton("Register", $GUIWidth / 2 - 100, 220, 200, 20)

	;~ create button for forgot password
	$hForgotPassword = GUICtrlCreateButton("Forgot password", $GUIWidth / 2 - 100, 250, 200, 20)

	;~ create button to exit
	$hExit = GUICtrlCreateButton("Exit", $GUIWidth / 2 - 100, 280, 200, 20)


	GUISetState(@SW_SHOW)

	;~ set the window to be always on top
	WinSetOnTop($hGUILogin, "", 1)

	;~ push button login if username and password are saved in the registry
	If $RegUsername <> "" And $RegPassword <> "" Then
		;~ send click to login button
		GUICtrlSendMsg($hLogin, $BM_CLICK, 0, 0)
	EndIf

	;~ loop to check for button clicks
	While 1
		$nMsg = GUIGetMsg()
		Switch $nMsg
			Case $GUI_EVENT_CLOSE
				XF_2ndScript_CloseAndKill()
				Exit
			Case $hLogin
				$sUsername = GUICtrlRead($hUsername)
				$sPassword = GUICtrlRead($hPassword)
				$sRemember = GUICtrlRead($hRemember)
				If $sUsername = "" Or $sPassword = "" Then
					ShowMsgBox("Please enter a email and password", "Error", 16, $hGUILogin)
				Else
					If CheckUsernameAndPassword($sUsername, $sPassword) = True Then
						$sLogin = Login($sUsername, $sPassword)
						$sLogin = Json_Decode($sLogin)
						Local $status = Json_Get($sLogin, ".status")
						Local $message = Json_Get($sLogin, ".message")
						If $status = "ok" Then
							ShowMsgBox("You have successfully logged in", "Success", 64, $hGUILogin, 2)
							If $sRemember = 1 Then
								;~ save username and password to file
								SaveLoginDataInRegistry($sUsername, $sPassword)
							Else
								;~ delete username and password from file
								DeleteLoginDataInRegistry()
							EndIf
							$usuario_cifrado = StringEncrypt(True, $sUsername, $XF_Masterkey)
							SaveDataInTheRegistry('SecureAccess', $usuario_cifrado)
							$XF_Username = $sUsername
							$XF_LefTime = $message
							XF_Openbot()
						Else
							ShowMsgBox($message, "Error", 16, $hGUILogin)
						EndIf
					EndIf
				EndIf
			Case $hRegister
				$sUsername = GUICtrlRead($hUsername)
				$sPassword = GUICtrlRead($hPassword)
				If $sUsername = "" Or $sPassword = "" Then
					ShowMsgBox("Please enter a email and password", "Error", 16, $hGUILogin)
				Else
					If CheckUsernameAndPassword($sUsername, $sPassword) = True Then
						$lData = LoadDataFromTheRegistry('SecureAccess')
						If $lData <> "" Then
							$usuario_descifrado = StringEncrypt(False, $lData, $XF_Masterkey)
							If $usuario_descifrado <> "" And $usuario_descifrado <> $sUsername Then
								ShowMsgBox("You already have an account, please use " & $usuario_descifrado & " to login", "Error", 16, $hGUILogin) 
								XF_2ndScript_CloseAndKill()
								Exit
							EndIf
						EndIf
						
						$sRegister = Register($sUsername, $sPassword)
						;~ $sRegister = {"status":"error","message":"User already exists"}
						;~ $sRegister = {"status":"ok"}
						$sRegister = Json_Decode($sRegister)
						Local $status = Json_Get($sRegister, ".status")
						Local $message = Json_Get($sRegister, ".message")
						If $status = "ok" Then
							ShowMsgBox("You have successfully registered, you can now login", "Success", 64, $hGUILogin)
						Else
							ShowMsgBox($message, "Error", 16, $hGUILogin)
						EndIf
					EndIf
				EndIf
			Case $hForgotPassword
				$sUsername = GUICtrlRead($hUsername)
				If $sUsername = "" Then
					ShowMsgBox("Please enter a email", "Error", 16, $hGUILogin)
				Else
					If CheckUsernameAndPassword($sUsername, '12345678') = True Then
						$sForgotPassword = ForgotPassword($sUsername)
						;~ $sForgotPassword = {"status":"error","message":"User does not exist"}
						;~ $sForgotPassword = {"status":"ok"}
						$sForgotPassword = Json_Decode($sForgotPassword)
						Local $status = Json_Get($sForgotPassword, ".status")
						Local $message = Json_Get($sForgotPassword, ".message")
						If $status = "ok" Then
							ShowMsgBox("You received an email with a new password, please check your spam folder if you don't see it in your inbox", "Success", 64, $hGUILogin)
						Else
							ShowMsgBox($message, "Error", 16, $hGUILogin)
						EndIf
					EndIf
				EndIf
			Case $hExit
				XF_2ndScript_CloseAndKill()
				Exit
		EndSwitch
	WEnd

EndFunc


Func CheckUsernameAndPassword($username, $password)
;~ check if username is an email address
	If StringInStr($username, "@") Then
		;~ check if the email address is valid
		If StringRegExp($username, "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$") Then
			;~ check if the password at least 8 characters long and max 16 characters long
			If StringRegExp($password, "^[a-zA-Z0-9]{8,14}$") Then
				Return True
			Else
				ShowMsgBox("Invalid password, password must be at least 8 characters long and max 14 characters long and can only contain letters and numbers", "Error", 16, $hGUILogin)
				Return False
			EndIf
		Else
			ShowMsgBox("Invalid email address, please enter a valid email address", "Error", 16, $hGUILogin)
			Return False
		EndIf
	Else
		ShowMsgBox("Invalid email address, please enter a valid email address", "Error", 16, $hGUILogin)
		Return False
	EndIf
EndFunc