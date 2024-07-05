#!/bin/bash

# Ejecutar supercronic en segundo plano
supercronic cron.txt &

# Esperar unos segundos para asegurarse de que supercronic inicie correctamente (ajusta según sea necesario)
sleep 5

# Iniciar Gunicorn
exec gunicorn --certfile certs/fullchain.pem --keyfile certs/privkey.pem --bind 0.0.0.0:8888 config.wsgi:application
