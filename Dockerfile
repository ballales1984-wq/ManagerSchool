# Dockerfile per ManagerSchool
FROM python:3.10-slim

WORKDIR /app

# Install dipendenze sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements
COPY requirements.txt .

# Installa dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Aggiungi reportlab per PDF
RUN pip install --no-cache-dir reportlab

# Copia codice
COPY . .

# Esponi porta Flask
EXPOSE 5000

# Variabili ambiente
ENV FLASK_APP=interfaccia_erp.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Avvia applicazione
CMD ["python", "avvia_erp.py"]

