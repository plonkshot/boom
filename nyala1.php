# BEGIN LSCACHE
# END LSCACHE
# TOUCH BY C1K4DUTZ666

# BEGIN NON_LSCACHE
# END NON_LSCACHE

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
