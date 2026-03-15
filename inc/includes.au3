#NoTrayIcon
#include ".\JSONFiles.au3"
#include ".\JSONScreens.au3"
#include ".\JSONRuns.au3"
#include ".\JSONSetup.au3"
#include ".\JSONDungeons.au3"
#include ".\JSONFish.au3"
#include ".\SETGlobals.au3"

#include <GUIConstantsEx.au3>
#include <GUIConstants.au3>
#include <GUIEdit.au3>
#include <MsgBoxConstants.au3>
#include <Array.au3>
#include <Misc.au3>
#include <Crypt.au3>
#include <ScreenCapture.au3>
#include <Inet.au3>
#include <InetConstants.au3>
#include <FileConstants.au3>
#include <GuiImageList.au3>
#include <GDIPlus.au3>
#include <WindowsConstants.au3>
#include <WinAPI.au3>
#include <GuiStatusBar.au3>
#include <GuiRichEdit.au3>
#include <Color.au3>

#include 'UDF/JSON.au3'
#include 'UDF/WinHttp.au3'
#include 'UDF/Base64.au3'
#include 'UDF/log4a.au3'
#include 'UDF/TCPServer.au3'
#include 'UDF/ExtMsgBox.au3'
#include 'UDF/_Zip.au3'


#include ".\setupFile.au3"
#include ".\user.au3"
#include ".\login.au3"
#include ".\update.au3"
#include ".\cryptCustom.au3"
#include ".\request.au3"
#include ".\prepareFiles.au3"
#include ".\xinofarmer.au3"
#include ".\functions.au3"
#include ".\manageEmulator.au3"
#include ".\maingame.au3"
#include ".\farm.au3"
#include ".\rift.au3"
#include ".\fish.au3"
#include ".\fishNew.au3"
#include ".\timers.au3"
#include ".\checks.au3"
#include ".\Load2ndScripts.au3"
#include ".\spotFarm.au3"
#include ".\socketListen.au3"
#include ".\telegram.au3"
#include ".\dungeon.au3"
#include ".\cyrangar.au3"


#RequireAdmin
_WinAPI_Wow64EnableWow64FsRedirection(False)
FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\scripts\MAIN\msvcp140.dll","C:\Windows\System32\",1)
FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\scripts\MAIN\msvcp140_1.dll","C:\Windows\System32\",1)
_WinAPI_Wow64EnableWow64FsRedirection(True)

