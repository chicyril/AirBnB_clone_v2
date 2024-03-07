#!/usr/bin/env bash
# Set up your web servers for the deployment of web_static.

sudo apt update

sudo apt install -y nginx

sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/

echo "<html><head></head><body>Test Page</body></html>" \
    | sudo tee /data/web_static/releases/test/index.html > /dev/null

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -hR ubuntu:ubuntu /data/

sudo cp /etc/nginx/sites-available/default \
    /etc/nginx/sites-available/default_backup

sudo sed -i '/^\tadd_header X-Served-By $hostname;/a\
\tlocation /hbnb_static {\
\t\talias /data/web_static/current/;\
\t}' /etc/nginx/sites-available/default

sudo service nginx restart
