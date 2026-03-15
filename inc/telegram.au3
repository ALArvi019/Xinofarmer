
#include <GuiConstantsEx.au3>
#include <GuiTab.au3>
#include <WinAPI.au3>
#include <GuiImageList.au3>
Func telegram_CheckUserIsConfig()
	TelegramActive()
	If $Setup_Telegram_Active = "Yes" Then
		dim $headers[1][2]
		$headers[0][0] = "Content-Type"
		$headers[0][1] = "application/x-www-form-urlencoded"
		$response = SendHTTPRequest("https", $XF_Domain, "/xf/check-telegram-user", 443, "POST", $headers, 3, "username=" & $XF_Username)
		$sLogin = Json_Decode($response)
		Local $status = Json_Get($sLogin, ".status")
		Local $message = Json_Get($sLogin, ".message")
		If $status = "ok" Then
			$Setup_Telegram_IsConfig = True
			$himage = GUICtrlSetImage($GUI_Tab_telegram, "shell32.dll", 16810, 0)
			GUICtrlSetTip($GUI_Tab_telegram, "Telegram is configured correctly")
			$Setup_Telegram_Active = "Yes"
		Else
			$himage = GUICtrlSetImage($GUI_Tab_telegram, "shell32.dll", 240, 0)
			GUICtrlSetTip($GUI_Tab_telegram, "Telegram is not configured correctly")
			$Setup_Telegram_IsConfig = False
			$Setup_Telegram_Active = "No"
		EndIf
	EndIf
EndFunc