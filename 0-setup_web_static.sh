#!/usr/bin/env bash
# Set up web servers for deployment of web static.

# Update packages and install nginx if not already installed
command -v nginx &> /dev/null
# shellcheck disable=SC2181
if [ $? -ne 0 ]; then
    sudo apt update
    sudo apt install -y nginx
fi

# Make sure HTTP trafic is allowed through firewall
sudo ufw allow "Nginx HTTP"

# Set up document root while creating a html sub directory.
docroot="/var/www/botcyba.tech"
if [ ! -d "$docroot/html" ]; then
    sudo mkdir -p "$docroot/html"
    sudo chown -R "$USER":"$USER" "$docroot"
    chmod 755 -R "$docroot"
fi

# Create a basic index.html document
if [ ! -f "$docroot/html/index.html" ]; then
    echo -e "Hello World!" > "$docroot/html/index.html"
fi

# Nginx server block config
conf=\
"server {
\tlisten 80 default_server;
\tlisten [::]:80 default_server;
\tserver_name botcyba.tech www.botcyba.tech;
\troot $docroot;
\tindex index.html index.htm;
\tlocation / {
\t\troot $docroot/html;
\t\ttry_files \$uri \$uri/ = 404;
\t}
}"

# Write config to file and enable it if not exist
if [ ! -f "/etc/nginx/sites-available/botcyba.tech" ]; then
    echo -e "$conf" | \
        sudo tee /etc/nginx/sites-available/botcyba.tech > /dev/null
    sudo ln -s /etc/nginx/sites-available/botcyba.tech /etc/nginx/sites-enabled/
fi

# Make sure the Nginx default site configuration is not enabled.
if [ -f "/etc/nginx/sites-enabled/default" ]; then
    sudo rm -f /etc/nginx/sites-enabled/default
fi

# Implement redirection for a specific request uri using rewrite directive and
# implement handler for 404 errors in config file.
# ============================================================================

# Create a 404 error html page
if [ ! -f "$docroot/html/error_404.html" ]; then
    echo -e "Ceci n'est pas une page\n" > "$docroot/html/error_404.html"
fi

# Modify config file using sed to make sure both redirect and error404 are
# implemented.
# shellcheck disable=SC1004
sudo sed -i '
\|rewrite ^/redirect_me| {n; b err404}
\|location /|! b
i\
\trewrite ^/redirect_me https://youtube.com permanent;
:err404
\|error_page 404| b end
$! {h; n; b err404}
h
i\
\terror_page 404 /error_404.html;
:end; n; b end
' /etc/nginx/sites-available/botcyba.tech

# Add a custom header to the config file using sed
# shellcheck disable=SC1004
sudo sed -i '
\|server_name|! b
n
\|add_header X-Served-By| b
i\
\tadd_header X-Served-By $hostname;
' /etc/nginx/sites-available/botcyba.tech

# Make sure /data/ and sub directories exist
if [ ! -d "/data" ]; then
    sudo mkdir -p /data/web_static/{releases/test,shared}
    sudo chown -R "$USER":"$USER" /data/
fi

# Make sure an html doc exist in the /data/web_static/releases/test/ directory
if [ ! -f "/data/web_static/releases/test/index.html" ]; then
    echo "<html><head></head><body>HBNB Test</body></html>" \
        > /data/web_static/releases/test/index.html
fi

# Make sure a new symlink is created every time the script is run
ln -sfT /data/web_static/releases/test /data/web_static/current

# Modify nginx config to make nginx serve the content of
# /data/web_static/current for /hbnb_static request path.
# shellcheck disable=SC1004
sudo sed -i '
\|location /hbnb_static| b end
\|error_page 404|! b
i\
\tlocation /hbnb_static {\
\t\talias /data/web_static/current;\
\t}
:end; n; b end
' /etc/nginx/sites-available/botcyba.tech

# Make sure nginx is runnig, and changes are loaded and applied
if ! service nginx status &> /dev/null; then
    sudo service nginx restart
else
    sudo nginx -s reload
fi
