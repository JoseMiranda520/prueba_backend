# Deploy app
All commands must be with sudo prefix

## Enable virtualenv

    source /home/.virtualenvs/virtualenv/forma2_backend/bin/activate

## Create virtualenv
Ruta `$HOME/.virtualenvs/forma2_backend`

    sudo python3.6 -m virtualenv chat_emtelco

## Collect statics
    
    sudo /home/vegeta/.virtualenvs/forma2_backend/bin/python manage.py collectstatic --settings=forma2_backend.settings.staging
    
## Migrate
    
    sudo /home/vegeta/.virtualenvs/forma2_backend/bin/python manage.py migrate --settings=forma2_backend.settings.staging

## Makemigrations 

    sudo /home/vegeta/.virtualenvs/forma2_backend/bin/python manage.py makemigrations --settings=forma2_backend.settings.staging
    
## Virtualenv
Enabling virtual env

    source /home/vegeta/.virtualenvs/forma2_backend/bin/activate
    
Move to project directory
    
    cd /var/www/pyhtml/forma2_backend

## Install Python wsgi

    pip install uwsgi
    
## Set Nginx config

    sudo cp /var/www/pyhtml/forma2_backend/deploy/staging/nginx.conf /etc/nginx/conf.d/forma2_backend.conf
     
Reload service
    
    sudo systemctl reload nginx
    
    sudo systemctl restart nginx

Logs nginx
    
    sudo journalctl -f -u nginx --since now

## Deploy WSGI

Stop uwsgi

    sudo /home/vegeta/.virtualenvs/forma2_backend/bin/uwsgi --stop /run/uwsgi/forma2_backend.pid

Ejecutar wsgi

    sudo /home/vegeta/.virtualenvs/forma2_backend/bin/uwsgi --ini /var/www/pyhtml/forma2_backend/deploy/staging/config.ini --daemonize /dev/null
