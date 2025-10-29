# 🚀 Guida Deployment ManagerSchool

## 📦 Docker Deployment

### Quick Start

```bash
# Build immagine
docker build -t managerschool .

# Avvia container
docker-compose up -d

# Verifica logs
docker-compose logs -f

# Stop
docker-compose down
```

## 🔧 Docker Compose

Deploy completo con volume persistenti:

```bash
docker-compose up -d
```

Sistema accessibile su: `http://localhost:5000`

## 📊 Gestione Volumi

```bash
# Backup database
docker exec managerschool_app python backup_registro.py

# Esporta PDF
docker exec managerschool_app python -c "from pdf_exporter import PDFExporter; ..."
```

## 🌐 Production Deployment

### DigitalOcean Droplet

```bash
# 1. Setup server
ssh root@your-server

# 2. Installa Docker
apt-get update
apt-get install docker.io docker-compose

# 3. Clone repository
git clone https://github.com/ballales1984-wq/ManagerSchool.git
cd ManagerSchool

# 4. Build e run
docker-compose up -d --build
```

### Heroku (Python native)

```bash
# 1. Installa Heroku CLI
heroku login
heroku create managerschool-app

# 2. Deploy
git push heroku main

# 3. Migra database
heroku run python database_manager.py
```

## 📧 Email Setup

### Configurazione SMTP

Editare `email_notifications.py`:

```python
class EmailNotifier:
    def __init__(self):
        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 587
        self.smtp_user = "your-email@gmail.com"
        self.smtp_password = "your-app-password"
        self.demo_mode = False  # Switch to real mode
```

### Gmail App Password

1. Google Account → Sicurezza
2. Abilita "Verifica in 2 passaggi"
3. Genera "Password app"
4. Usa la password generata

## 📄 PDF Export

### Uso base

```python
from pdf_exporter import PDFExporter

exporter = PDFExporter()
exporter.esporta_pagella(studente, voti, 'pagella.pdf')
```

### Integrazione web

Aggiungi route in `interfaccia_erp.py`:

```python
@app.route('/api/export-pagella-pdf/<int:studente_id>')
def export_pagella_pdf(studente_id):
    exporter = PDFExporter()
    # ... recupera dati
    exporter.esporta_pagella(studente, voti, f'pagella_{studente_id}.pdf')
    return send_file(f'pagella_{studente_id}.pdf', as_attachment=True)
```

## 🔐 Security

### HTTPS con nginx

Creare `nginx.conf`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### SSL con Let's Encrypt

```bash
certbot --nginx -d your-domain.com
```

## 📱 Mobile App Build

### Android

```bash
cd app_mobile
npx expo build:android -t apk
# Oppure con EAS
eas build --platform android
```

### iOS

```bash
eas build --platform ios
# Richiede Apple Developer account
```

## 🧪 Testing Production

```bash
# Test DB
docker exec managerschool_app python test_database_completo.py

# Test PDF
docker exec managerschool_app python pdf_exporter.py

# Test Email
docker exec managerschool_app python email_notifications.py
```

## 🔄 Updates

### Aggiornare applicazione

```bash
git pull
docker-compose build
docker-compose up -d --force-recreate
```

### Database migration

```bash
docker exec managerschool_app python database_manager.py --migrate
```

## 📊 Monitoring

### Logs

```bash
docker-compose logs -f managerschool
```

### Health check

```bash
curl http://localhost:5000/api/health
```

## 🐛 Troubleshooting

### Database locked

```bash
docker exec managerschool_app python -c "import sqlite3; conn = sqlite3.connect('managerschool.db'); conn.close()"
```

### Port already in use

```bash
# Cambia porta in docker-compose.yml
ports:
  - "5001:5000"
```

---

**Deployment pronto!** 🎉

