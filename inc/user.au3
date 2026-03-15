
Func Register($username, $password)
	dim $headers[1][2]
	$headers[0][0] = "Content-Type"
	$headers[0][1] = "application/x-www-form-urlencoded"
	return SendHTTPRequest("https", $XF_Domain, "/xf/register", 443, "POST", $headers, 3, "username=" & $username & "&password=" & $password)
EndFunc

Func Login($username, $password)
	dim $headers[1][2]
	$headers[0][0] = "Content-Type"
	$headers[0][1] = "application/x-www-form-urlencoded"
	return SendHTTPRequest("https", $XF_Domain, "/xf/login", 443, "POST", $headers, 3, "username=" & $username & "&password=" & $password)
EndFunc

Func ForgotPassword($username)
	dim $headers[1][2]
	$headers[0][0] = "Content-Type"
	$headers[0][1] = "application/x-www-form-urlencoded"
	return SendHTTPRequest("https", $XF_Domain, "/xf/forgot-password", 443, "POST", $headers, 3, "username=" & $username)
EndFunc

Func SaveDataInTheRegistry($valor_registro, $data)
	If LoadDataFromTheRegistry($valor_registro) <> "" Then
		DeleteDataFromTheRegistry($valor_registro)
	EndIf

	RegWrite($XF_clave_registro, $valor_registro, "REG_SZ", $data)
EndFunc

Func LoadDataFromTheRegistry($valor_registro)
	Return RegRead($XF_clave_registro, $valor_registro)
EndFunc

Func DeleteDataFromTheRegistry($valor_registro)
	RegDelete($XF_clave_registro, $valor_registro)
EndFunc

Func SaveLoginDataInRegistry($username, $password)
	; Definir las claves y valores del registro donde se almacenarán los datos cifrados
	$valor_registro = "AccessData"
	
	; Cifrar los datos de acceso
	$usuario_cifrado = StringEncrypt(True, $username, $XF_Masterkey)
	$contrasena_cifrada = StringEncrypt(True, $password, $XF_Masterkey)

	SaveDataInTheRegistry($valor_registro, $usuario_cifrado & "|" & $contrasena_cifrada)
EndFunc

Func LoadLoginDataInRegistry()
	; Definir las claves y valores del registro donde se almacenaron los datos cifrados
	$valor_registro = "AccessData"

	; Leer los datos cifrados del registro de Windows
	$datos_cifrados = LoadDataFromTheRegistry($valor_registro)

	;~ check if $datos_cifrados is empty
	If $datos_cifrados = "" Then
		Return ""
	EndIf

	; Descifrar los datos de acceso
	$datos = StringSplit($datos_cifrados, "|")
	$usuario_descifrado = StringEncrypt(False, $datos[1], $XF_Masterkey)
	$contrasena_descifrada = StringEncrypt(False, $datos[2], $XF_Masterkey)

	; Devolver los datos de acceso
	Return $usuario_descifrado & "|" & $contrasena_descifrada
EndFunc

Func LoadPasswordEncryptFromRegistry()
	; Definir las claves y valores del registro donde se almacenaron los datos cifrados
	$valor_registro = "AccessData"

	; Leer los datos cifrados del registro de Windows
	$datos_cifrados = LoadDataFromTheRegistry($valor_registro)

	;~ check if $datos_cifrados is empty
	If $datos_cifrados = "" Then
		Return ""
	EndIf

	; Descifrar los datos de acceso
	$datos = StringSplit($datos_cifrados, "|")
	$contrasena_descifrada = StringEncrypt(False, $datos[2], $XF_Masterkey)
	$contrasena_cifrada = EncryptString_toPHP($XF_Masterkey, $contrasena_descifrada)
	return $contrasena_cifrada
EndFunc

Func DeleteLoginDataInRegistry()
	; Definir las claves y valores del registro donde se almacenaron los datos cifrados
	$valor_registro = "AccessData"

	;~ if the regitry entry exists, delete it
	If LoadDataFromTheRegistry($valor_registro) <> "" Then
		DeleteDataFromTheRegistry($valor_registro)
	EndIf
EndFunc
