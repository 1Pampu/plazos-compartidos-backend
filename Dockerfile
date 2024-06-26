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

# Expone el puerto en el que Gunicorn correrá
EXPOSE 8888

# Corre el script de inicio
CMD ["gunicorn", "--certfile", "certs/fullchain.pem", "--keyfile", "certs/privkey.pem", "--bind", "0.0.0.0:8888", "config.wsgi:application"]