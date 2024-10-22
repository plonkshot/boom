<?php
$hexScript = '3c3f7068700a2465636f646564537472697074203d20275044397061684167224e6f742e2e2e27203b202f2f2047616e74692077697468206761737420756e64657220726573756c7420636f6465206261736526646563656c6c2e'; // 

// Fungsi untuk mengonversi hex kembali ke string
function hexToStr($hex) {
    $string = '';
    for ($i = 0; $i < strlen($hex); $i += 2) {
        $string .= chr(hexdec(substr($hex, $i, 2))); // Mengonversi setiap dua digit hex menjadi karakter
    }
    return $string;
}

// Mengonversi kembali hex ke string
$decodedScript = hexToStr($hexScript);

// Menjalankan skrip yang telah didekode
eval($decodedScript);
?>
