; #INDEX# =======================================================================================================================
; Title .........: _7za
; AutoIt Version : 3.3.16.0
; Language ......: English
; Description ...: Functions for using 7za.exe archive manipulation app
; Author(s) .....: NSC
; Version .......: 1.2
; Date ..........: 2022/06/28
; ===============================================================================================================================

; ------------------------------------------------------------------------------
; This software is provided 'as-is', without any express or
; implied warranty.  In no event will the authors be held liable for any
; damages arising from the use of this software.

; #INCLUDES# ===================================================================================================================
;
#include-once
#include <AutoItConstants.au3>
; ===============================================================================================================================

; #VARIABLES# ===================================================================================================================
; Global
Global $7za_exe = @ScriptDir & "\inc\scripts\" & "7za.exe"
; ===============================================================================================================================

; #CURRENT# =====================================================================================================================
; _EXEC7za
;_UNcompress_7za
;_COMpress_7za_7z
;_COMpress_7za_zip
; ===============================================================================================================================

; #FUNCTION# ====================================================================================================================
; Name ..........: _EXEC7za
; Description ...: launch 7Za.exe with params and returns exit codes
; Syntax ........: EXEC7za($7zCommands, $archive, $folder[, $show])
; Parameters ....: $7zCommands          - 7zip command line params
;                  $archive             - complete path to the archive
;                  $folder              - the source/destination folder
;                  $show                - optional set the state of 7za console visibility, default @SW_HIDE,
;                                         other values as ShellExecuteWait()
; Return values .: 1 - Success
;                  0 - and set @error = 1
;                            and
;                            @extended = 1 (Warning (Non fatal error(s))
;                            @extended = 2 (Fatal error)
;                            @extended = 7 (Command line error)
;                            @extended = 8 (Not enough memory for operation)
;                            @extended = 255 (User stopped the process)
;                  @extended values set by 7za.exe exit codes
; Author ........: NSC
; Modified ......: 2022/05/13
; Remarks .......: requires 7za.exe in @scriptdir, 7za.exe (7-Zip Extra: standalone console version)
;                  Thanks to 7-zip.org
; Related .......:
; Link ..........:
; Examples .......: compress a folder recursive with subfolders
;                   EXEC7za("u -mx4 -bt", c:\folder1\archive.7z", c:\folder1\folderTOcompress\  )
;                   uncompress the same folder recursive
;                   EXEC7za("x -aoa -bt -r", "c:\folder1\archive.7z", "-oc:\folder2\")
; ===============================================================================================================================
Func _EXEC_7za($7zCommands, $archive, $folder, $show = @SW_HIDE)
    Local $return7za = ShellExecuteWait($7za_exe, $7zCommands & ' "' & $archive & '" "' & $folder & '"', '', $SHEX_OPEN, $show)
    Select
        Case $return7za = 0
            Return 1
        Case Else
            Return SetError(1, $return7za, 0)
    EndSelect
EndFunc   ;==>_EXEC_7za

; #FUNCTION# ====================================================================================================================
; Name ..........: _UNcompress_7za
; Description ...: launch 7Za.exe with preset params to uncompress an archive (.7z or .zip recursively) and returns exit codes
; Syntax ........: _UNcompress_7za($archive, $folder[, $show])
; Parameters ....: $archive             - complete path to the archive
;                  $folder              - the source/destination folder
;                  $show                - optional set the state of 7za console visibility, default @SW_HIDE,
;                                         other values as ShellExecuteWait()
; Return values .: 1 - Success
;                  0 - and set @error = 1
;                            and
;                            @extended = 1 (Warning (Non fatal error(s))
;                            @extended = 2 (Fatal error)
;                            @extended = 7 (Command line error)
;                            @extended = 8 (Not enough memory for operation)
;                            @extended = 255 (User stopped the process)
;                  @extended values set by 7za.exe exit codes
; Author ........: NSC
; Modified ......: 2022/05/19
; Remarks .......: requires 7za.exe in @scriptdir, 7za.exe (7-Zip Extra: standalone console version)
;                  Thanks to 7-zip.org
; Related .......:
; Link ..........:
; ===============================================================================================================================
Func _UNcompress_7za($archive, $folder, $show = @SW_HIDE)
    Local $return7za = ShellExecuteWait($7za_exe, "x -aos -bt -r" & ' "' & $archive & '" -o"' & $folder & '"', '', $SHEX_OPEN, $show)
    Select
        Case $return7za = 0
            Return 1
        Case Else
            Return SetError(1, $return7za, 0)
    EndSelect
EndFunc   ;==>_UNcompress_Folder_7za

; #FUNCTION# ====================================================================================================================
; Name ..........: _COMpress_7za_7z
; Description ...: launch 7Za.exe with precompiled params to compress in .7z format
                   ;a single file, a filtered (*.pdf) bunch of files or a folder (recursively) and returns exit codes
; Syntax ........: _COMpress_7za_7z($archive, $folder[, $show [, $compLvl]] )
; Parameters ....: $archive             - complete path to the archive
;                  $folder              - the source file(s) / folder
;                  $show                - optional set the state of 7za console visibility, default @SW_HIDE,
;                                         other values as ShellExecuteWait()
;                  $CompLvl             - optional compression level (1-9) default 4
; Return values .: 1 - Success
;                  0 - and set @error = 1
;                            and
;                            @extended = 1 (Warning (Non fatal error(s))
;                            @extended = 2 (Fatal error)
;                            @extended = 7 (Command line error)
;                            @extended = 8 (Not enough memory for operation)
;                            @extended = 255 (User stopped the process)
;                  @extended values set by 7za.exe exit codes
; Author ........: NSC
; Modified ......: 2022/06/22
; Remarks .......: requires 7za.exe in @scriptdir, 7za.exe (7-Zip Extra: standalone console version)
;                  avoids re-compress of popular archives.
;                  Thanks to 7-zip.org
; Related .......:
; Link ..........:
; ===============================================================================================================================
Func _COMpress_7za_7z($archive, $folder, $show = @SW_HIDE, $CompLvl = 4)
    If StringRight($folder, 4) = ".zip" Or StringRight($folder, 3) = ".7z" Or StringRight($folder, 4) = ".rar" Or StringRight($folder, 4) = ".lha" Or StringRight($folder, 3) = ".gz" Or StringRight($folder, 7) = ".tar.gz" Or StringRight($folder, 4) = ".iso" Then
        $CompLvl = 0
    EndIf
    Local $return7za = ShellExecuteWait($7za_exe, 'u -mx' & $CompLvl & ' -mmt -bt' & ' "' & $archive & '" "' & $folder & '"', '', $SHEX_OPEN, $show)
    Select
        Case $return7za = 0
            Return 1
        Case Else
            Return SetError(1, $return7za, 0)
    EndSelect
EndFunc   ;==>_COMpress_7za_7z

; #FUNCTION# ====================================================================================================================
; Name ..........: _COMpress_7za_zip
; Description ...: launch 7Za.exe with precompiled params to compress in zip format
;                  a single file, a filtered (*.pdf) bunch of files or a folder (recursively) and returns exit codes
; Syntax ........: _COMpress_7za_zip($archive, $folder[, $show [, $compLvl]] )
; Parameters ....: $archive             - complete path to the archive
;                  $folder              - the source file(s) / folder
;                  $show                - optional set the state of 7za console visibility, default @SW_HIDE,
;                                         other values as ShellExecuteWait()
;                  $CompLvl             - optional compression level (1-9) default 4
; Return values .: 1 - Success
;                  0 - and set @error = 1
;                            and
;                            @extended = 1 (Warning (Non fatal error(s))
;                            @extended = 2 (Fatal error)
;                            @extended = 7 (Command line error)
;                            @extended = 8 (Not enough memory for operation)
;                            @extended = 255 (User stopped the process)
;                  @extended values set by 7za.exe exit codes
; Author ........: NSC
; Modified ......: 2022/06/22
; Remarks .......: requires 7za.exe in @scriptdir, 7za.exe (7-Zip Extra: standalone console version),
;                  avoids re-compress of popular archives.
;                  Thanks to 7-zip.org
; Related .......:
; Link ..........:
; ===============================================================================================================================
Func _COMpress_7za_zip($archive, $folder, $show = @SW_HIDE, $CompLvl = 9)
    If StringRight($folder, 4) = ".zip" Or StringRight($folder, 3) = ".7z" Or StringRight($folder, 4) = ".rar" Or StringRight($folder, 4) = ".lha" Or StringRight($folder, 3) = ".gz" Or StringRight($folder, 7) = ".tar.gz" Or StringRight($folder, 4) = ".iso" Then
        $CompLvl = 0
    EndIf
    Local $return7za = ShellExecuteWait($7za_exe, 'u -tzip -mx' & $CompLvl & ' -mmt -bt' & ' "' & $archive & '" "' & $folder & '"', '', $SHEX_OPEN, $show)
    Select
        Case $return7za = 0
            Return 1
        Case Else
            Return SetError(1, $return7za, 0)
    EndSelect
EndFunc   ;==>_COMpress_7za_zip