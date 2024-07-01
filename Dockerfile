# Usa una imagen base oficial de Python 3.10
FROM python:3.10-slim

# Instala librerias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmariadb-dev-compat \
    pkg-config \
 && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requisitos y el código del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Define el argumento de build para SSL_PATH
ARG SSL_PATH

# Asegura que SSL_PATH esté definido o establece un valor por defecto
ENV SSL_PATH=${SSL_PATH:-}

# Verifica que SSL_PATH esté definido y no esté vacío antes de copiar los archivos
RUN if [ -n "$SSL_PATH" ]; then mkdir -p /app/certs && \
    cp ${SSL_PATH}/fullchain.pem /app/certs/ && \
    cp ${SSL_PATH}/privkey.pem /app/certs/; fi

# Expone el puerto en el que Gunicorn correrá
EXPOSE 8888

# Corre Gunicorn para servir la aplicación Django
CMD ["gunicorn", "--certfile", "certs/fullchain.pem", "--keyfile", "certs/privkey.pem", "--bind", "0.0.0.0:8888", "config.wsgi:application"]