#!/bin/bash

# Crear el directorio certs si no existe
mkdir -p certs

# Copiar los archivos desde el volumen montado a /app/certs
cp bind/fullchain.pem certs/
cp bind/privkey.pem certs/

# Corre Gunicorn para servir la aplicación Django
gunicorn --certfile certs/fullchain.pem --keyfile certs/privkey.pem --bind 0.0.0.0:8888 config.wsgi:application
