# 🤝 Contribuire al Registro Scolastico Intelligente

Grazie per l'interesse a contribuire al progetto! Questo documento fornisce linee guida per contribuire efficacemente.

---

## 📋 Indice

- [Codice di Condotta](#codice-di-condotta)
- [Come Contribuire](#come-contribuire)
- [Processo di Sviluppo](#processo-di-sviluppo)
- [Linee Guida per il Codice](#linee-guida-per-il-codice)
- [Standard di Commit](#standard-di-commit)
- [Aree di Contributo](#aree-di-contributo)

---

## 📜 Codice di Condotta

Questo progetto aderisce a un codice di condotta basato sul rispetto e la collaborazione:

- ✅ **Rispetto**: Tratta tutti con rispetto e cortesia
- ✅ **Costruttività**: Fornisci feedback costruttivo e utile
- ✅ **Inclusività**: Accogli nuove prospettive e approcci diversi
- ✅ **Collaborazione**: Lavora insieme per raggiungere obiettivi comuni

---

## 🚀 Come Contribuire

### 1. Report Bug

Se trovi un bug, crea una issue includendo:

- **Descrizione chiara** del problema
- **Passi per riprodurlo** (se possibile)
- **Comportamento atteso** vs. **comportamento attuale**
- **Screenshot** (se rilevante)
- **Versione Python** e ambiente

### 2. Proporre Funzionalità

Per nuove funzionalità:

- **Descrivi il problema** che risolve
- **Spiega l'approccio** proposto
- **Fornisci esempi di utilizzo**
- **Considera l'impatto** sul sistema esistente

### 3. Contribuire con Codice

1. **Fork** del repository
2. **Clone** la tua fork
3. **Crea un branch** (`git checkout -b feature/NuovaFeature`)
4. **Fai le modifiche** seguendo le linee guida
5. **Testa** le modifiche
6. **Commit** con messaggi chiari
7. **Push** al branch
8. **Apri una Pull Request**

---

## 🔄 Processo di Sviluppo

### Setup Ambiente

```bash
# Clone la repository
git clone <url-della-tua-fork>
cd managers

# Crea un branch
git checkout -b feature/MiaFunzionalita
```

### Struttura del Progetto

```
managers/
├── main.py                 # Entry point
├── anagrafica.py           # Gestione studenti
├── insegnanti.py           # Gestione insegnanti
├── voti.py                 # Sistema voti
├── analisi.py              # Analisi avanzate
├── indicatori.py           # Indicatori sintetici
├── accesso.py              # Sistema RBAC
├── report.py               # Generazione report
├── interfaccia.py          # UI
├── macro_dati.py           # Dati territoriali
├── dati.py                 # Dati casuali
├── utils.py                # Utility
└── tests/                  # Test (da creare)
```

### Workflow

1. **Lavora su un branch** dedicato per ogni feature
2. **Mantieni il branch aggiornato** con `main`
3. **Testa localmente** prima di fare push
4. **Scrivi commit significativi**
5. **Apri PR con descrizione chiara**

---

## 📝 Linee Guida per il Codice

### Stile Python

Segui le convenzioni **PEP 8**:

```python
# ✅ Corretto
def calcola_fragilita(studente: Studente) -> float:
    """Calcola la fragilità sociale.
    
    Args:
        studente: Studente da analizzare
        
    Returns:
        Valore di fragilità (0-100)
    """
    return studente.fragilità_sociale

# ❌ Evitare
def calc(studente):
    return studente.frag
```

### Convenzioni

- **Nomi variabili**: `snake_case` (es. `nome_studente`)
- **Nomi classi**: `PascalCase` (es. `Anagrafica`)
- **Nomi costanti**: `UPPER_SNAKE_CASE` (es. `MAX_STUDENTI`)
- **Docstrings**: Sempre presenti per classi e funzioni pubbliche
- **Type hints**: Sempre presenti
- **Commenti**: In italiano, quando necessario per chiarezza

### Documentazione

```python
"""Modulo per la gestione dell'anagrafica studenti.
Gestisce dati personali, reddito, salute e situazione familiare.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Studente:
    """Rappresenta uno studente nel sistema.
    
    Attributes:
        id: Identificativo univoco
        nome: Nome dello studente
        cognome: Cognome dello studente
        eta: Età dello studente
        classe: Classe frequentata
        reddito_familiare: Reddito annuale della famiglia
        categoria_reddito: Categoria del reddito
        condizione_salute: Condizione di salute
        situazione_familiare: Struttura familiare
    """
    
    id: int
    nome: str
    cognome: str
    # ...
```

### Testing

Quando aggiungi nuove funzionalità:

```python
# Esempio test (da creare in tests/)
def test_fragilita_sociale():
    """Test calcolo fragilità sociale."""
    studente = Studente(
        id=1,
        nome="Mario",
        cognome="Rossi",
        eta=16,
        classe="3A",
        reddito_familiare=20000,
        categoria_reddito=CategoriaReddito.BASSO,
        condizione_salute=CondizioneSalute.BUONA,
        situazione_familiare="Nucleo tradizionale"
    )
    
    assert 0 <= studente.fragilità_sociale <= 100
    assert studente.fragilità_sociale > 0
```

---

## 💬 Standard di Commit

Usa messaggi di commit chiari e descrittivi:

```
feat: aggiunto calcolo resilienza studenti
fix: corretto bug nella generazione report
docs: aggiornato README con sezione contributi
refactor: riorganizzato modulo analisi
test: aggiunti test per fragilità sociale
style: formattato codice secondo PEP 8
```

### Formato

```
<tipo>: <descrizione breve>

[corpo opzionale con dettagli]

[footer opzionale con riferimenti issue]
```

### Tipi

- `feat`: Nuova funzionalità
- `fix`: Bug fix
- `docs`: Documentazione
- `style`: Formattazione
- `refactor`: Refactoring
- `test`: Test
- `chore`: Manutenzione

---

## 🎯 Aree di Contributo

### Funzionalità Prioritarie

1. **Test Automatizzati**
   - Unit test per tutti i moduli
   - Integration test per workflow completi
   - Coverage > 80%

2. **Interfaccia Web**
   - Flask/Django per web interface
   - Dashboard con visualizzazioni
   - API REST

3. **Database Persistente**
   - SQLite/PostgreSQL
   - Migrazioni
   - Backup/restore

4. **Visualizzazioni**
   - Grafici matplotlib/plotly
   - Dashboard interattiva
   - Export PDF

5. **Internazionalizzazione**
   - Traduzione in inglese
   - Supporto multi-lingua
   - Localizzazione

6. **Machine Learning**
   - Predizioni performance
   - Analisi pattern
   - Raccomandazioni

### Aree Specializzate

- **Frontend**: Miglioramenti UI/UX, nuovi menu
- **Backend**: Ottimizzazioni, nuove analisi
- **Data Science**: Nuovi indicatori, correlazioni
- **Documentazione**: Tutorial, esempi, guide
- **DevOps**: CI/CD, containerizzazione
- **Testing**: Suite test completa

---

## 📞 Contatti

- **Issue**: Apri una issue su GitHub
- **Pull Request**: Invia una PR con descrizione dettagliata
- **Discussioni**: Usa GitHub Discussions per domande

---

## ✅ Checklist PR

Prima di aprire una Pull Request:

- [ ] Codice formattato secondo PEP 8
- [ ] Documentazione aggiornata
- [ ] Type hints presenti
- [ ] Docstrings per funzioni pubbliche
- [ ] Test eseguiti (se applicabile)
- [ ] Commit con messaggi chiari
- [ ] Nessun errore di linting
- [ ] Descrizione PR completa
- [ ] Riferimento a issue (se presente)

---

## 🙏 Ringraziamenti

Ogni contributo, grande o piccolo, è apprezzato e fa la differenza!

**Grazie per contribuire al Registro Scolastico Intelligente! 🚀**

