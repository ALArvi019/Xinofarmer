#include <Crypt.au3>
#include <IE.au3>
#include <Array.au3>
Global $error
Global $extended

Func _Cryptshun($str)
    ; function to match up with php side encryption/decryption
    ; from http://www.autoitscript.com/forum/topic/150967-aes-256-encryption-in-autoit-php/
	Dim Const $KP_MODE = 4
	Dim Const $CRYPT_MODE_ECB = 2
	_Crypt_Startup()
	$key = _Crypt_ImportKey($CALG_AES_128, $XF_Masterkey)

	_Crypt_SetKeyParam($key, $KP_MODE, $CRYPT_MODE_ECB)

	$s = _Crypt_EncryptData($str, $key, $CALG_USERKEY)
	if @error or @extended then
		$error = @error
		$extended = @extended
	EndIf
	_Crypt_DestroyKey($key)
	_Crypt_Shutdown()
	$s = _Base64Encode($s)
	Return SetError($error,$extended,$s)
EndFunc

Func _DeCryptshun($str)
	Dim Const $KP_MODE = 4
	Dim Const $CRYPT_MODE_ECB = 2
	_Crypt_Startup()
	$key = _Crypt_ImportKey($CALG_AES_128, $XF_Masterkey)
	_Crypt_SetKeyParam($key, $KP_MODE, $CRYPT_MODE_ECB)
	$str = _Base64Decode($str)
	$s = _Crypt_DecryptData($str, $key, $CALG_USERKEY)
	if @error or @extended then
		$error = @error
		$extended = @extended
	EndIf
	_Crypt_DestroyKey($key)
	_Crypt_Shutdown()
	Return SetError($error,$extended,$s)
EndFunc


;Author: ProgAndy, rewritten by FireFox
;return value: key handle
Func _Crypt_ImportKey($iALG_ID, $sKey)
     Local Const $PLAINTEXTKEYBLOB = 0x8 ;The key is a session key.
     Local Const $CUR_BLOB_VERSION = 2

     Local $bKey = Binary($sKey), $iKeyLen = BinaryLen($bKey)

     Local $tagPUBLICKEYBLOB = "struct; BYTE bType; BYTE bVersion; WORD reserved; dword aiKeyAlg; dword keysize; byte key[" & $iKeyLen & "]; endstruct;"

     Local $tBLOB = DllStructCreate($tagPUBLICKEYBLOB)
     DllStructSetData($tBLOB, "bType", $PLAINTEXTKEYBLOB)
     DllStructSetData($tBLOB, "bVersion", $CUR_BLOB_VERSION)
     DllStructSetData($tBLOB, "aiKeyAlg", $iALG_ID)
     DllStructSetData($tBLOB, "keysize", $iKeyLen)
     DllStructSetData($tBLOB, "key", Binary($bKey))

     Local $aRet = DllCall(__Crypt_DllHandle(), "bool", "CryptImportKey", "handle", __Crypt_Context(), "ptr", DllStructGetPtr($tBLOB), "dword", DllStructGetSize($tBLOB), "ptr", 0, "dword", 0, "ptr*", 0)
     If @error Then Return SetError(2, @error)

     Return SetError(Not $aRet[0], 0, $aRet[6])
EndFunc   ;==>_Crypt_ImportKey

;Author: ProgAndy, rewritten by FireFox
;return value: int (bool)
Func _Crypt_SetKeyParam($hKey, $iParam, $vData, $iFlags = 0, $sDataType = Default)
     If Not $sDataType Or $sDataType = Default Then $sDataType = "ptr"

     Local $aRet = DllCall(__Crypt_DllHandle(), "bool", "CryptSetKeyParam", "handle", $hKey, "dword", $iParam, $sDataType, $vData, "dword", $iFlags)
     If @error Then Return SetError(2, @error)

     Return SetError(Not $aRet[0], 0, $aRet[0])
EndFunc   ;==>_Crypt_SetKeyParam

Func StringEncrypt($bEncrypt, $sData, $sPassword)
	_Crypt_Startup() ; Start the Crypt library.
	Local $vReturn = ''
	If $bEncrypt Then ; If the flag is set to True then encrypt, otherwise decrypt.
			$vReturn = _Crypt_EncryptData($sData, $sPassword, $CALG_RC4)
	Else
			$vReturn = BinaryToString(_Crypt_DecryptData($sData, $sPassword, $CALG_RC4))
	EndIf
	_Crypt_Shutdown() ; Shutdown the Crypt library.
	Return $vReturn
EndFunc

Func DeriveKeyFromPassword($sPassword)
    Local $hHash = _Crypt_HashData($sPassword, $CALG_MD5)
    Local $sKey = _Crypt_EncryptData("AutoIt key", $hHash, $CALG_AES_128)
    ;~ _Crypt_DestroyHashHandle($hHash)
    Return $sKey
EndFunc

Func EncryptString_toPHP($key, $value)
    Local $S[256], $i, $j, $c, $t, $x, $y, $output
    Local $keyLength = BinaryLen($key), $valLength = BinaryLen($value)
    For $i = 0 To 255
        $S[$i] = $i
    Next
    For $i = 0 To 255
        $j = Mod($j + $S[$i] + Dec(StringTrimLeft(BinaryMid($key, Mod($i, $keyLength)+1, 1),2)),256)
        $t = $S[$i]
        $S[$i] = $S[$j]
        $S[$j] = $t
    Next
    For $i = 1 To $valLength
        $x = Mod($x+1,256)
        $y = Mod($S[$x]+$y,256)
        $t = $S[$x]
        $S[$x] = $S[$y]
        $S[$y] = $t
        $j = Mod($S[$x]+$S[$y],256)
        $c = BitXOR(Dec(StringTrimLeft(BinaryMid($value, $i, 1),2)), $S[$j])
        $output = Binary($output) & Binary('0x' & Hex($c,2))
    Next
    Return $output
EndFunc