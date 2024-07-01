#!/bin/bash

# Verifica si SSL_PATH está definido y no está vacío
if [ -n "$SSL_PATH" ]; then
    echo "SSL_PATH está definido. Copiando archivos SSL..."
    mkdir -p /app/certs
    cp ${SSL_PATH}/fullchain.pem /app/certs/
    cp ${SSL_PATH}/privkey.pem /app/certs/
else
    echo "SSL_PATH no está definido. No se copiarán los archivos SSL."
fi

# Corre Gunicorn para servir la aplicación Django
gunicorn --certfile certs/fullchain.pem --keyfile certs/privkey.pem --bind 0.0.0.0:8888 config.wsgi:application
