# 🖥️ Guida Interfaccia ERP

## 📋 Indice

1. [Introduzione](#introduzione)
2. [Installazione](#installazione)
3. [Avvio](#avvio)
4. [Architettura](#architettura)
5. [API Documentation](#api-documentation)
6. [Utilizzo](#utilizzo)

---

## 🎯 Introduzione

L'**Interfaccia ERP** è un sistema web-based che fornisce un'interfaccia moderna e completa per il Registro Scolastico Intelligente, permettendo l'accesso a tutte le funzionalità del sistema tramite browser.

### Caratteristiche Principali

- ✅ **Interfaccia Web** moderna e responsive
- ✅ **API RESTful** complete
- ✅ **Sistema di autenticazione** basato su ruoli (RBAC)
- ✅ **Dashboard** con statistiche in tempo reale
- ✅ **Multi-ruolo** (Admin, Dirigente, Insegnante, Studente)
- ✅ **Esportazione dati** in formato JSON
- ✅ **Architettura modulare** e estendibile

---

## 🚀 Installazione

### Requisiti

```bash
Python 3.8+
Flask (installato tramite requirements.txt)
```

### Installazione Dipendenze

```bash
pip install flask
```

Oppure:

```bash
pip install -r requirements.txt
```

---

## 🔥 Avvio

### Modalità Standard

```bash
python interfaccia_erp.py
```

Il server si avvierà su: `http://127.0.0.1:5000`

### Custom Host/Port

```python
# In interfaccia_erp.py, modifica:
erp.run(host='0.0.0.0', port=8080, debug=False)
```

---

## 🏗️ Architettura

### Struttura File

```
managers/
├── interfaccia_erp.py      # Server Flask principale
├── templates/               # Template HTML
│   ├── base.html           # Template base
│   ├── home.html           # Home page pubblica
│   ├── login.html          # Pagina login
│   └── dashboard.html      # Dashboard principale
└── static/                 # File statici (CSS, JS, immagini)
```

### Componenti Principali

#### 1. **InterfacciaERP Class**
- Gestisce inizializzazione Flask
- Inizializza tutti i moduli del sistema
- Registra routes
- Gestisce autenticazione

#### 2. **Routes Pubbliche**
- `/` - Home page
- `/login` - Login form
- `/logout` - Logout

#### 3. **Routes Autenticate**
- `/dashboard` - Dashboard principale
- `/api/studenti` - API studenti
- `/api/insegnanti` - API insegnanti
- `/api/voti` - API voti
- `/api/analisi/*` - API analisi
- `/api/indicatori/*` - API indicatori
- `/api/report/*` - API report

---

## 📚 API Documentation

### Autenticazione

#### POST /login
Login utente.

**Body:**
```json
{
    "username": "admin",
    "password": "admin123"
}
```

**Response:**
```json
{
    "successo": true,
    "redirect": "/dashboard"
}
```

---

### API Studenti

#### GET /api/studenti
Lista tutti gli studenti.

**Response:**
```json
[
    {
        "id": 1,
        "nome": "Mario",
        "cognome": "Rossi",
        "classe": "1A",
        "fragilita": 35.5
    }
]
```

#### GET /api/studenti/<id>
Dettaglio studente.

**Response:**
```json
{
    "studente": {...},
    "voti": [...],
    "media": 7.5
}
```

#### POST /api/studenti
Crea nuovo studente (richiede permesso: `gestione_studenti`).

---

### API Analisi

#### GET /api/analisi/graduatoria
Graduatoria studenti (Top 20).

**Response:**
```json
[
    {
        "posizione": 1,
        "nome": "Mario Rossi",
        "media": 9.5
    }
]
```

#### GET /api/analisi/fragilita
Analisi fragilità sociale.

**Response:**
```json
{
    "gap_pedagogico": 1.2,
    "equita_educativa": "Da migliorare"
}
```

#### GET /api/analisi/correlazione
Correlazione reddito-rendimento.

**Response:**
```json
{
    "Bassa": {"media_rendimento": 7.2},
    "Media": {"media_rendimento": 8.1}
}
```

---

### API Indicatori

#### GET /api/indicatori
Tutti gli indicatori sintetici (richiede permesso: `visualizza_indicatori_privati`).

**Response:**
```json
{
    "qualita_scolastica": {
        "nome": "Indice Qualità Scolastica",
        "valore": 75.3,
        "componenti": {...}
    },
    ...
}
```

#### GET /api/indicatori/<nome>
Singolo indicatore.

**Nomi disponibili:**
- `qualita`
- `equita`
- `efficacia`
- `coesione`
- `benessere`

---

### API Report

#### GET /api/report/annuale
Report annuale completo (richiede permesso: `visualizza_report_completi`).

#### GET /api/report/equita
Report equità educativa.

---

### API Interventi

#### GET /api/interventi/prioritari?limit=10
Studenti prioritari per interventi educativi.

**Response:**
```json
{
    "totale_fragili": 15,
    "studenti_prioritari": [...],
    "costo_totale_stimato": 5000,
    "miglioramento_atteso": 25.5
}
```

---

### API Macro-dati

#### GET /api/macro-dati
Macro-dati territoriali (ISTAT/MIUR).

---

## 👤 Utilizzo

### Account Demo

Il sistema include account demo per test:

| Username | Password | Ruolo |
|----------|----------|-------|
| admin | admin123 | Amministratore |
| dirigente | dirigente123 | Dirigente |
| insegnante | insegnante123 | Insegnante |
| studente | studente123 | Studente |

### Workflow Base

1. **Accedi al sistema**: `http://127.0.0.1:5000`
2. **Fai login** con uno degli account demo
3. **Visualizza la Dashboard** con statistiche generali
4. **Naviga** tra le sezioni via menu sidebar
5. **Utilizza le API** per integrazioni esterne

### Esempi di Utilizzo API

#### Esempio 1: Fetch Dati Studenti (JavaScript)

```javascript
fetch('/api/studenti')
    .then(res => res.json())
    .then(data => {
        console.log('Studenti:', data);
    });
```

#### Esempio 2: Creare Studenti (Python)

```python
import requests

response = requests.post(
    'http://127.0.0.1:5000/api/studenti',
    json={'nome': 'Luigi', 'cognome': 'Verdi', 'classe': '2A'},
    cookies=session_cookies  # Dopo login
)
```

#### Esempio 3: Export Dati (curl)

```bash
curl http://127.0.0.1:5000/api/studenti -o studenti.json
curl http://127.0.0.1:5000/api/indicatori -o indicatori.json
```

---

## 🔐 Sistema di Permessi

Ogni ruolo ha permessi specifici:

### Ruolo: PUBBLICO
- ❌ Nessun accesso (solo home page)

### Ruolo: STUDENTE
- ✅ Visualizza propri dati
- ✅ Visualizza propri voti
- ✅ Statistiche generali

### Ruolo: INSEGNANTE
- ✅ Tutti i permessi STUDENTE
- ✅ Gestione voti classe
- ✅ Visualizza studenti classe

### Ruolo: DIRIGENTE
- ✅ Tutti i permessi INSEGNANTE
- ✅ Report completi
- ✅ Analisi complete
- ✅ Gestione studenti/insegnanti

### Ruolo: AMMINISTRATORE
- ✅ Tutti i permessi DIRIGENTE
- ✅ Gestione utenti
- ✅ Permessi speciali
- ✅ Accesso completo

---

## 🎨 Personalizzazione

### Modificare i Template

I template HTML sono in `templates/`:
- `base.html` - Template base con sidebar
- `home.html` - Home page pubblica
- `login.html` - Form login
- `dashboard.html` - Dashboard principale

### Aggiungere Nuove Routes

In `interfaccia_erp.py`, aggiungi nella funzione `_registra_routes()`:

```python
@self.app.route('/api/nuova-funzione')
@self.richiede_accesso
def nuova_funzione():
    return jsonify({"messaggio": "Nuova funzionalità"})
```

### Modificare Dashboard Stats

Modifica `_calcola_statistiche_dashboard()` per aggiungere nuove statistiche:

```python
def _calcola_statistiche_dashboard(self) -> Dict:
    return {
        "nuova_statistica": valore,
        ...
    }
```

---

## 🐛 Troubleshooting

### Server non si avvia

```bash
# Verifica che Flask sia installato
pip install flask

# Verifica che la porta 5000 sia libera
netstat -an | grep 5000
```

### Template non trovati

```bash
# Crea la directory templates se non esiste
mkdir -p templates
mkdir -p static
```

### Errore 404 per API

Verifica che:
1. Tu sia autenticato (session valida)
2. Tu abbia i permessi necessari
3. La route sia registrata in `_registra_routes()`

---

## 📊 Sviluppi Futuri

### Funzionalità Pianificate

1. **Dashboard Avanzata**
   - Grafici interattivi (Chart.js)
   - Real-time updates (WebSocket)

2. **Gestione File Statici**
   - CSS personalizzato
   - JavaScript modules
   - Immagini e icone

3. **Export Avanzati**
   - PDF reports
   - Excel exports
   - CSV exports

4. **Database Persistente**
   - SQLite per sviluppo
   - PostgreSQL per produzione
   - Migrazioni automatiche

5. **API Authentication**
   - JWT tokens
   - OAuth2
   - API keys

---

## 🤝 Contribuire

Vedi [CONTRIBUTING.md](../CONTRIBUTING.md) per linee guida.

### Aree di Contributo

- **Frontend**: Miglioramenti UI/UX
- **Backend**: Nuove API/endpoints
- **Testing**: Unit test e integration test
- **Documentation**: Miglioramenti doc

---

## 📞 Supporto

Per domande o problemi:
1. Apri una [Issue su GitHub](https://github.com/your-repo/issues)
2. Consulta la [documentazione completa](../README.md)
3. Controlla i [test esistenti](../tests/)

---

## ✅ Checklist Utilizzo

Prima di usare l'interfaccia ERP:

- [ ] Python 3.8+ installato
- [ ] Flask installato (`pip install flask`)
- [ ] Directory `templates/` creata
- [ ] Server avviato (`python interfaccia_erp.py`)
- [ ] Accesso a `http://127.0.0.1:5000`
- [ ] Login con account demo
- [ ] Dashboard visibile con statistiche

---

**Buon utilizzo! 🚀**




