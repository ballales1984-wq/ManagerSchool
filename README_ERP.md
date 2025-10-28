# 🖥️ Interfaccia ERP - Guida Rapida

## 🚀 Avvio Rapido

### Installazione

```bash
# Installa Flask
pip install flask

# Oppure
pip install -r requirements.txt
```

### Avvio

```bash
# Metodo 1: Script automatico (consigliato)
python avvia_erp.py

# Metodo 2: Manuale
python interfaccia_erp.py
```

### Accesso

Apri il browser su: **http://127.0.0.1:5000**

---

## 👤 Account Demo

| Username | Password | Ruolo |
|----------|----------|-------|
| **admin** | admin123 | 🔑 Amministratore |
| **dirigente** | dirigente123 | 👔 Dirigente |
| **insegnante** | insegnante123 | 👨‍🏫 Insegnante |
| **studente** | studente123 | 👨‍🎓 Studente |

---

## 📋 Funzionalità

### 🌐 Interfaccia Web
- Dashboard con statistiche in tempo reale
- Menu sidebar per navigazione
- Design moderno e responsive
- Bootstrap 5 + Icons

### 🔐 Sistema di Accesso
- Login con username/password
- Ruoli multipli (RBAC)
- Permessi granulari
- Sessione protetta

### 📊 API RESTful
- **GET** `/api/studenti` - Lista studenti
- **GET** `/api/insegnanti` - Lista insegnanti
- **GET** `/api/analisi/*` - Analisi e statistiche
- **GET** `/api/indicatori` - Indicatori sintetici
- **GET** `/api/report/*` - Report completi
- **GET** `/api/interventi/*` - Simulatore interventi

### 📈 Esportazione
- JSON format
- API endpoints per integrazioni
- Download dati completi

---

## 🎯 Esempi d'Uso

### 1. Visualizzare Dashboard

1. Accedi: http://127.0.0.1:5000
2. Login con `admin/admin123`
3. Vai su Dashboard
4. Visualizza statistiche

### 2. Export Dati Studente

```bash
curl http://127.0.0.1:5000/api/studenti \
     -H "Cookie: session=..." \
     -o studenti.json
```

### 3. Usare API da JavaScript

```javascript
fetch('/api/indicatori')
    .then(res => res.json())
    .then(data => console.log(data));
```

### 4. Visualizzare Graduatorie

1. Login → Dashboard
2. Click "Graduatorie"
3. Visualizza Top 20 studenti

---

## 🏗️ Architettura

```
interfaccia_erp.py     # Server Flask principale
├── Routes pubbliche   # /, /login
├── Routes autenticate # /dashboard, /api/*
├── Decorators        # @richiede_accesso, @richiede_permesso
└── API endpoints     # JSON responses

templates/            # HTML Templates
├── base.html         # Template base (sidebar)
├── home.html         # Home page pubblica
├── login.html        # Login form
└── dashboard.html    # Dashboard principale
```

---

## 🔧 Configurazione

### Modificare Porta

```python
# In interfaccia_erp.py
erp.run(host='127.0.0.1', port=8080)
```

### Modificare Host

```python
# Accesso da rete locale
erp.run(host='0.0.0.0', port=5000)
```

### Debug Mode

```python
# Attiva debug (auto-reload)
erp.run(debug=True)
```

---

## 📚 Documentazione Completa

Vedi: **docs/INTERFACCIA_ERP.md** per documentazione dettagliata.

---

## 🐛 Troubleshooting

### Server non si avvia
```bash
pip install flask
```

### Template non trovati
```bash
mkdir templates static
```

### Porta già in uso
```python
# Cambia porta in interfaccia_erp.py
erp.run(port=8080)
```

---

## ✅ Checklist

- [x] Flask installato
- [x] Directory templates/ creata
- [x] Server avviato
- [x] Browser su http://127.0.0.1:5000
- [x] Login eseguito
- [x] Dashboard funzionante

---

**Buon utilizzo! 🚀**


