#!/bin/bash

touch /var/log/cron.log
printenv | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID|LANG|PWD|GPG_KEY|_=' >> /etc/environment

python manage.py crontab remove
python manage.py crontab add
service cron start

# Iniciar Gunicorn
exec gunicorn --certfile certs/fullchain.pem --keyfile certs/privkey.pem --bind 0.0.0.0:8888 config.wsgi:application