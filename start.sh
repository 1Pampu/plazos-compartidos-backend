#!/bin/bash

# Iniciar el servicio cron
service cron start

# Agregar el cronjob
python manage.py crontab add

# Iniciar Gunicorn
exec gunicorn --certfile certs/fullchain.pem --keyfile certs/privkey.pem --bind 0.0.0.0:8888 config.wsgi:application