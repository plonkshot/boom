<?php
$newURL = 'https://adoptionsos.org/';

// Set the 301 Moved Permanently header
header("HTTP/1.1 301 Moved Permanently");
header("Location: $newURL");
exit();
?>
