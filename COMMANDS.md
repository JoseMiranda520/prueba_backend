# Comandos útiles
Comandos útiles para la despliegues en los entornos de desarrollo, forma2_backend y producción.

## Desarrollo

### Activar entorno virtual
    
    source ~/.virtualenvs/forma2django/bin/activate

### Ejecutar servidor local

    python manage.py runserver 0:8000 --settings=forma2_backend.settings.develop

## forma2_backends

### Activar virtual env

    source /home/vegeta/.virtualenvs/forma2_backend/bin/activate

### Ejecutar el demonio

    sudo /home/vegeta/.virtualenvs/forma2_backend/bin/uwsgi --ini /var/www/pyhtml/forma2_backend/config.ini > /dev/null &

    sudo /home/vegeta/.virtualenvs/forma2_backend/bin/uwsgi --ini /var/www/pyhtml/forma2_backend/config.ini --daemonize /dev/null

### Pausar esa cagá

    sudo /home/vegeta/.virtualenvs/forma2_backend/bin/uwsgi --stop /run/uwsgi/forma2_backend.pid


### Copiar manual librerías si fallan
    -- pyctivex
    sudo cp -R /var/www/pyhtml/pyctivex/pyctivex/* /home/vegeta/.virtualenvs/forma2_backend/lib64/python3.6/site-packages/pyctivex
    
    -- fw
    sudo cp -R /var/www/pyhtml/django-fw/fw/* /home/vegeta/.virtualenvs/forma2_backend/lib64/python3.6/site-packages/fw
     
     
     