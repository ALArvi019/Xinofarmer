#RequireAdmin
#include <WinAPIFiles.au3>
_WinAPI_Wow64EnableWow64FsRedirection(False)
FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\scripts\MAIN\msvcp140.dll","C:\Windows\System32\",1)
FileInstall("C:\Users\Alex\Desktop\immortal_xinofarmer\inc\scripts\MAIN\msvcp140_1.dll","C:\Windows\System32\",1)
_WinAPI_Wow64EnableWow64FsRedirection(True)

