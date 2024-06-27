# Usa una imagen base oficial de Python 3.10
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requisitos y el código del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Expone el puerto en el que Gunicorn correrá
EXPOSE 8888

# Corre Gunicorn para servir la aplicación Django
CMD ["gunicorn", "--bind", "0.0.0.0:8888", "config.wsgi:application"]