FROM python:3.10-slim

# 1. Instalar espeak-ng a nivel de sistema operativo Linux
RUN apt-get update && apt-get install -y \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copiar código de la aplicación
COPY . .

# 4. Arrancar la aplicación usando gunicorn en el puerto de Render
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-5000}"]
