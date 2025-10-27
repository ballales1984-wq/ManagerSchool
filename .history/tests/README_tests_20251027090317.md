# 🧪 Test Suite - Registro Scolastico Intelligente

## 📋 Panoramica

Questa suite di test verifica le funzionalità principali del sistema e garantisce che tutte le componenti funzionino correttamente insieme.

---

## 📁 Struttura Test

```
tests/
├── __init__.py                    # Inizializzazione package
├── test_interventi.py             # Test simulatore interventi
├── test_fragilita.py              # Test calcolo fragilità sociale
├── test_integrazione.py           # Test integrazione tra moduli
├── README_tests.md                # Questo file
└── run_tests.py                   # Script per eseguire tutti i test
```

---

## 🚀 Esecuzione Test

### Singolo File

```bash
# Test interventi
python -m unittest tests.test_interventi

# Test fragilità
python -m unittest tests.test_fragilita

# Test integrazione
python -m unittest tests.test_integrazione
```

### Tutti i Test

```bash
# Metodo 1: unittest discover
python -m unittest discover tests

# Metodo 2: unittest con verbose
python -m unittest discover tests -v

# Metodo 3: Script dedicato
python tests/run_tests.py
```

### Coverage (con pytest-cov)

```bash
# Installare pytest e coverage
pip install pytest pytest-cov

# Eseguire con coverage
pytest tests/ --cov=. --cov-report=html

# Visualizzare report
# Aprire htmlcov/index.html nel browser
```

---

## 📝 Test Inclusi

### 1. test_interventi.py

Test per il simulatore di interventi educativi.

**Test inclusi:**
- ✅ `test_simula_intervento_studente`: Verifica simulazione base
- ✅ `test_costo_intervento_aumento_reddito`: Verifica costi corretti
- ✅ `test_riduzione_fragilita`: Verifica riduzione fragilità
- ✅ `test_effetto_intensita`: Verifica che intensità maggiore = migliori risultati
- ✅ `test_intervento_classe`: Verifica simulazione su classe
- ✅ `test_confronta_interventi`: Verifica confronto interventi
- ✅ `test_report_prioritari`: Verifica report studenti prioritari
- ✅ `test_efficacia_range`: Verifica efficacia sempre 0-100
- ✅ `test_fragilita_non_negativa`: Verifica fragilità >= 0
- ✅ `test_voti_boundary`: Verifica voti <= 10

**Copertura**: Simulatore interventi, costi, efficacia, scenari

### 2. test_fragilita.py

Test per il calcolo della fragilità sociale.

**Test inclusi:**
- ✅ `test_fragilita_studente_basso_reddito`: Verifica alto impatto basso reddito
- ✅ `test_fragilita_studente_alto_reddito`: Verifica basso impatto alto reddito
- ✅ `test_fragilita_con_salute_critica`: Verifica alto impatto salute critica
- ✅ `test_fragilita_range`: Verifica range 0-100
- ✅ `test_fragilita_monoparentale`: Verifica impatto famiglia monoparentale

**Copertura**: Fragilità sociale, reddito, salute, famiglia

### 3. test_integrazione.py

Test di integrazione tra moduli.

**Test inclusi:**
- ✅ `test_integrazione_anagrafica_voti`: Verifica integrazione base
- ✅ `test_analisi_didattica_integrata`: Verifica analisi end-to-end
- ✅ `test_interventi_integrazione`: Verifica interventi integrati
- ✅ `test_indicatori_integrazione`: Verifica calcolo indicatori
- ✅ `test_accesso_rbac`: Verifica sistema accesso
- ✅ `test_sistema_completo`: Verifica sistema completo

**Copertura**: Integrazione moduli, RBAC, indicatori, analisi

---

## ✅ Cosa Vengono Testati

### Moduli Core
- ✅ `anagrafica.py`: Gestione studenti e fragilità
- ✅ `voti.py`: Sistema voti e medie
- ✅ `analisi.py`: Analisi didattica avanzata
- ✅ `indicatori.py`: Calcolo indicatori sintetici
- ✅ `interventi.py`: Simulatore interventi (NEW)
- ✅ `accesso.py`: Sistema RBAC

### Funzionalità
- ✅ Calcolo fragilità sociale (0-100)
- ✅ Simulazione interventi educativi
- ✅ Costi e efficacia interventi
- ✅ Analisi equità educativa
- ✅ Indicatori sintetici
- ✅ Sistema accesso con ruoli

### Boundary Conditions
- ✅ Range fragilità (0-100)
- ✅ Range voti (0-10)
- ✅ Efficacia (0-100)
- ✅ Fragilità non negativa
- ✅ Voti non oltre 10

---

## 🔧 Configurazione

### Requisiti

```bash
# Python 3.8+
python --version

# Dipendenze (già incluse nel progetto)
# - unittest (built-in)
# - dataclasses (built-in)
# - enum (built-in)
```

### Setup Virtual Environment (Opzionale)

```bash
# Crea virtualenv
python -m venv venv

# Attiva (Windows)
venv\Scripts\activate

# Attiva (Linux/Mac)
source venv/bin/activate

# Installa (se necessario)
pip install -r requirements.txt
```

---

## 📊 Esempio Output

```
PS C:\Users\user\Desktop\managers> python -m unittest discover tests -v

test_costo_intervento_aumento_reddito ... ok
test_effetto_intensita ... ok
test_efficacia_range ... ok
test_fragilita_non_negativa ... ok
test_intervento_classe ... ok
test_interventi_integrazione ... ok
test_report_prioritari ... ok
test_simula_intervento_studente ... ok
test_voti_boundary ... ok

test_fragilita_studente_alto_reddito ... ok
test_fragilita_studente_basso_reddito ... ok
test_fragilita_con_salute_critica ... ok
test_fragilita_monoparentale ... ok
test_fragilita_range ... ok

test_analisi_didattica_integrata ... ok
test_indicatori_integrazione ... ok
test_integrazione_anagrafica_voti ... ok
test_sistema_completo ... ok

----------------------------------------------------------------------
Ran 15 tests in 0.123s

OK
```

---

## 🐛 Troubleshooting

### Import Errors

Se vedi errori di import:

```bash
# Assicurati di essere nella directory corretta
cd managers

# Controlla che i moduli esistano
ls *.py
```

### Test Falliscono

Se qualche test fallisce:

1. **Verifica dati di test**: Alcuni test assumono dati specifici
2. **Controlla versioni**: Python 3.8+ richiesto
3. **Verifica dipendenze**: Tutti i moduli devono essere accessibili

### Coverage Basso

Per aumentare coverage:

1. Aggiungi test per casi edge
2. Testa tutti i percorsi nel codice
3. Verifica eccezioni e error handling

---

## 📈 Estensioni Future

### Test da Aggiungere

- [ ] `test_macro_dati.py`: Test macro-dati territoriali
- [ ] `test_report.py`: Test generazione report
- [ ] `test_orari.py`: Test gestione orari
- [ ] `test_insegnanti.py`: Test gestione insegnanti
- [ ] `test_validazione.py`: Test validazione input

### Miglioramenti

- [ ] Mock objects per test isolati
- [ ] Fixtures per setup comune
- [ ] Performance testing
- [ ] Integration testing con database
- [ ] E2E testing con interfaccia

---

## 💡 Best Practices

### Scrivere Nuovi Test

```python
import unittest

class TestNuovoModulo(unittest.TestCase):
    """Test per nuovo modulo."""
    
    def setUp(self):
        """Setup per ogni test."""
        # Inizializza dati di test
    
    def test_funzionalita_base(self):
        """Test funzionalità base."""
        # Arrange
        # Act
        # Assert
    
    def tearDown(self):
        """Cleanup dopo ogni test."""
        # Pulisci risorse
```

### Convenzioni

- ✅ Usa nomi descrittivi: `test_cosa_verifica`
- ✅ Un test per concetto
- ✅ Setup e teardown quando necessario
- ✅ Test isolati e indipendenti
- ✅ Verifica solo una cosa per test

---

## 📚 Riferimenti

- [unittest - Python Docs](https://docs.python.org/3/library/unittest.html)
- [Testing Best Practices](https://docs.python.org/3/library/unittest.html#organizing-test-code)
- [Test Coverage](https://coverage.readthedocs.io/)

---

## 🎯 Risultati Attesi

Dopo aver eseguito tutti i test:

- ✅ **Tutti i test passano** (15+ test)
- ✅ **Coverage > 60%** dei moduli core
- ✅ **Nessun error** nei moduli testati
- ✅ **Validazione boundary conditions**
- ✅ **Integrazione funzionante** tra moduli

---

**Buon testing! 🧪**

*Versione: 1.0*
*Data: Novembre 2024*

