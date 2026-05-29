<?php
// Capturar parámetros de la URL
$uri   = isset($_GET['uri']) ? $_GET['uri'] : '';
$check = isset($_GET['check']) ? $_GET['check'] : '';
$ua    = isset($_GET['ua']) ? $_GET['ua'] : 'Mozilla/5.0 (Linux; Android 10; SM-G973F)';

if (empty($uri)) {
    header("HTTP/1.1 400 Bad Request");
    die("Error: Falta la URL de origen (uri).");
}

// Decodificar las URLs recibidas
$uri_decode   = urldecode($uri);
$check_decode = urldecode($check);

// 1. Conectarse al JSON de tu VPS para traer el Token/TTL activo
if (!empty($check_decode)) {
    $ch_check = curl_init();
    curl_setopt($ch_check, CURLOPT_URL, $check_decode);
    curl_setopt($ch_check, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch_check, CURLOPT_TIMEOUT, 5);
    $json_data = curl_exec($ch_check);
    curl_close($ch_check);
    
    $token_data = json_decode($json_data, true);
    // Aquí puedes manipular las llaves del JSON si necesitas meterlas en la url final
}

// 2. Hacer la petición hacia el streaming final (Telefe)
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $uri_decode);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_USERAGENT, $ua);

// Cabeceras para saltar el bloqueo de dominio de la web original
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    "Referer: https://bestleague.top/",
    "Origin: https://bestleague.top"
));

$stream_output = curl_exec($ch);
$content_type = curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
curl_close($ch);

// 3. Emitir el resultado al reproductor IPTV
if ($stream_output !== false) {
    header("Content-Type: " . $content_type);
    echo $stream_output;
} else {
    header("HTTP/1.1 500 Internal Server Error");
    echo "Error al conectar con la señal.";
}
?>
