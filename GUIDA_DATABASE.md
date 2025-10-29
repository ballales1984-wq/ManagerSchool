# 📚 Guida Database SQLite - ManagerSchool

## 🎯 Cos'è il Database SQLite

Il sistema ora usa **SQLite** per salvare i dati persistentemente tra le sessioni.

### Vantaggi
- ✅ Dati persistenti tra riavvii
- ✅ Query veloci e efficienti
- ✅ Backup facile
- ✅ Database leggero e portabile
- ✅ Transaction safety

---

## 🚀 Come Usare

### 1. Database Automatico

Il database si inizializza **automaticamente** all'avvio del sistema.

```python
# Il file managerschool.db viene creato automaticamente
# nella directory principale del progetto
```

### 2. Operazioni Database

#### Salvare uno Studente
```python
from database_manager import DatabaseManager

db = DatabaseManager()

studente = {
    'id': 1,
    'nome': 'Mario',
    'cognome': 'Rossi',
    'eta': 15,
    'classe': '2A',
    'reddito_familiare': 30000,
    'categoria_reddito': 'MEDIO',
    'condizione_salute': 'BUONA',
    'situazione_familiare': 'Nucleo tradizionale',
    'note': ''
}

db.aggiungi_studente(studente)
```

#### Salvare un Voto
```python
voto = {
    'id_studente': 1,
    'materia': 'Matematica',
    'voto': 8.5,
    'tipo': 'Interrogazione',
    'data': '2025-10-28',
    'note': 'Ottimo lavoro'
}

db.aggiungi_voto(voto)
```

#### Ottenere Studenti
```python
# Tutti gli studenti
studenti = db.ottieni_studenti()

# Per classe
studenti_2A = db.ottieni_studenti("2A")
```

#### Calcolare Media
```python
# Media generale
media = db.media_studente(studente_id)

# Media per materia
media_matematica = db.media_studente(studente_id, "Matematica")
```

---

## 📊 API REST Disponibili

### Statistiche Database
```
GET /api/database/stats
```
Restituisce statistiche sul database:
- Numero studenti
- Numero voti
- Numero presenze
- Classi attive

### Backup Database
```
POST /api/database/backup
```
Crea un backup del database.

### Sincronizzazione
```
POST /api/database/sync
```
Sincronizza dati in-memory con il database.

### Lista Voti
```
GET /api/database/voti
GET /api/database/voti?studente_id=123
```
Ottiene voti dal database.

---

## 🔧 Configurazione

### Cambiare percorso database

```python
from database_manager import DatabaseManager

# Percorso personalizzato
db = DatabaseManager("percorso/personalizzato/mydb.db")
```

### Backup Manuale

```python
db = DatabaseManager()
backup_path = db.backup_database("backup_custom.db")
```

---

## 📈 Performance

### Indici Ottimizzati

Il database ha indici su:
- `studenti.classe` - Ricerca per classe veloce
- `voti.id_studente` - Query voti studente
- `voti.materia` - Filtro per materia
- `presenze.id_studente` - Presenze studente
- `presenze.data` - Filtro per data

### Query Efficienti

```python
# Query ottimizzata per classe
studenti = db.ottieni_studenti("2A")
# Usa indice automaticamente

# Statistiche con JOIN
stats = db.statistiche_presenze("2A")
# Ottimizzata per performance
```

---

## 🛠️ Manutenzione

### Backup Automatico

Il sistema crea backup automatici in:
- `backup_db_YYYYMMDD_HHMMSS.db`

### Pulizia Database Vecchio

```python
# Rimuovi database vecchio
import os
os.remove("managerschool_old.db")
```

### Vedo Statistiche

```python
stats = db.statistiche_database()
print(f"Studenti: {stats['studenti']}")
print(f"Voti: {stats['voti']}")
print(f"Classi: {stats['classi']}")
```

---

## 🚨 Troubleshooting

### Database non si apre

**Problema**: `Error opening database`

**Soluzione**:
```python
import os
# Rimuovi database corrotto
os.remove("managerschool.db")
# Ricrea database
db = DatabaseManager()
```

### Dati duplicati

**Problema**: Studenti inseriti più volte

**Soluzione**: Usa `INSERT OR IGNORE` nel codice:

```python
cursor.execute("""
    INSERT OR IGNORE INTO studenti (...) 
    VALUES (...)
""")
```

---

## 📝 Esempio Completo

```python
from database_manager import DatabaseManager
from anagrafica import Anagrafica

# Setup
anagrafica = Anagrafica()
anagrafica.genera_studenti(50)

# Database
db = DatabaseManager()

# Sincronizza
for studente in anagrafica.studenti:
    db.aggiungi_studente({
        'id': studente.id,
        'nome': studente.nome,
        'cognome': studente.cognome,
        'eta': studente.eta,
        'classe': studente.classe,
        # ... altri campi
    })

# Query
studenti_db = db.ottieni_studenti("2A")
print(f"Studenti 2A: {len(studenti_db)}")

# Aggiungi voto
db.aggiungi_voto({
    'id_studente': studenti_db[0]['id'],
    'materia': 'Matematica',
    'voto': 8.0,
    'tipo': 'Interrogazione',
    'data': '2025-10-28'
})

# Backup
db.backup_database()

db.close()
```

---

## 🎯 Prossimi Sviluppi

### PostgreSQL Production
Per produzione, considera PostgreSQL:
- Maggiore scalabilità
- Multi-user
- Performance ottimizzate

### Migrazione Guidata
```bash
python migrate_to_postgresql.py
```

---

**Database SQLite**: Semplicità e potenza per ManagerSchool! 🚀

