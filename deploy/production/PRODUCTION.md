# Deploy app
All commands must be with sudo prefix

## Enable virtualenv

    source  /home/vegeta/virtualenv/forma2_backend/bin/activate

## Create virtualenv
Ruta `$HOME/virtualenv/forma2_backend`

    sudo python3.6 -m virtualenv forma2_backend

## Collect statics
    
    /home/vegeta/virtualenv/forma2_backend/bin/python manage.py collectstatic --settings=forma2_backend.settings.production
    
## Migrate
    
    /home/vegeta/virtualenv/forma2_backend/bin/python manage.py migrate --settings=forma2_backend.settings.production
    
## Virtualenv
Enabling virtual env

    source /home/vegeta/virtualenv/forma2_backend/bin/activate
    
Move to project directory
    
    cd /var/www/pyhtml/forma2_backend

## Install Python wsgi

    pip install uwsgi
    
## Set Nginx config

    sudo cp /var/www/pyhtml/forma2_backend/deploy/production/nginx.conf /etc/nginx/conf.d/forma2_backend.conf
     
Reload service
    
    sudo systemctl reload nginx
    
    sudo systemctl restart nginx

Logs nginx
    
    sudo journalctl -f -u nginx --since now

## Deploy WSGI

Stop uwsgi

    /home/vegeta/virtualenv/forma2_backend/bin/uwsgi --stop /run/uwsgi/forma2_backend.pid

Ejecutar wsgi

    /home/vegeta/virtualenv/forma2_backend/bin/uwsgi --ini /var/www/pyhtml/forma2_backend/deploy/production/config.ini --daemonize /dev/null
