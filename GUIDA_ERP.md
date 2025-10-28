# 🚀 Guida Rapida - Interfaccia ERP

## Installazione e Avvio

### 1. Installa Flask

```bash
pip install flask
```

### 2. Avvia l'Interfaccia ERP

```bash
# Metodo automatico (consigliato)
python avvia_erp.py

# O manualmente
python interfaccia_erp.py
```

### 3. Accedi al Browser

Apri: **http://127.0.0.1:5000**

## Account Demo

| Username | Password | Ruolo |
|----------|----------|-------|
| **admin** | admin123 | Amministratore |
| **dirigente** | dirigente123 | Dirigente |
| **insegnante** | insegnante123 | Insegnante |
| **studente** | studente123 | Studente |

## Funzionalità

### 📊 Dashboard
- Statistiche in tempo reale
- Cards con metriche principali
- Grafici e visualizzazioni

### 🔐 Sistema di Accesso
- Login sicuro
- Ruoli multipli (RBAC)
- Permessi granulari

### 📈 API RESTful
Tutte le API restituiscono JSON:

- **GET** `/api/studenti` - Lista studenti
- **GET** `/api/insegnanti` - Lista insegnanti  
- **GET** `/api/analisi/graduatoria` - Graduatoria
- **GET** `/api/indicatori` - Indicatori sintetici
- **GET** `/api/report/annuale` - Report annuale
- **GET** `/api/interventi/prioritari` - Studenti prioritari

## Esempi d'Uso

### Visualizzare Dashboard
1. Accedi a http://127.0.0.1:5000
2. Login con `admin/admin123`
3. Dashboard automatica

### Esportare Dati (JavaScript)
```javascript
fetch('/api/studenti')
    .then(res => res.json())
    .then(data => console.log(data));
```

### Esportare Dati (curl)
```bash
# Con autenticazione
curl -X GET http://127.0.0.1:5000/api/studenti \
     -H "Cookie: session=..." \
     -o studenti.json
```

## Personalizzazione

### Modificare Porta

In `interfaccia_erp.py`:
```python
erp.run(host='127.0.0.1', port=8080)
```

### Aggiungere Nuova Route

```python
@self.app.route('/api/mia-funzione')
@self.richiede_accesso
def mia_funzione():
    return jsonify({"messaggio": "Nuova funzionalità"})
```

## Troubleshooting

### Flask non installato
```bash
pip install flask
```

### Template non trovati
```bash
mkdir templates static
```

### Porta occupata
Cambia porta in `interfaccia_erp.py`

## Documentazione Completa

Vedi: **docs/INTERFACCIA_ERP.md**

---

**Pronto per usare l'interfaccia ERP! 🎉**


