# Changelog - Registro Scolastico Intelligente

Tutti i cambiamenti rilevanti del progetto verranno documentati in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce a [Semantic Versioning](https://semver.org/lang/it/).

---

## [2.1] - 2024-11-27

### ✨ Aggiunto
- 💡 **Simulatore Interventi Educativi** (`interventi.py`)
  - 4 tipi di interventi (Reddito, Famiglia, Salute, Completo)
  - 3 livelli di intensità (Bassa, Media, Alta)
  - Simulazione impatto su fragilità e voti
  - Calcolo efficacia e costi
  - Report studenti prioritari
  
- 🧪 **Suite Test Automatici**
  - `tests/test_interventi.py` (10 test)
  - `tests/test_fragilita.py` (5 test)
  - `tests/test_integrazione.py` (6 test)
  - Totale: 21 test, tutti passati ✅

- 📚 **Documentazione Completa**
  - `CONTRIBUTING.md` - Linee guida contributi
  - `docs/IMPLEMENTAZIONE_INTERVENTI.md` - Dettagli tecnici
  - `docs/PRESENTAZIONE.md` - Presentazione professionale
  - `docs/SLIDE_PRESENTAZIONE.md` - 17 slide pronte
  - `docs/RIEPILOGO_FASI.md` - Riepilogo completo
  - `tests/README_tests.md` - Guida test

- 🔧 **File Supporto**
  - `.gitignore` - Esclusioni Git
  - `requirements.txt` - Dipendenze future
  - `.github/workflows/test.yml` - CI/CD
  - `.github/PULL_REQUEST_TEMPLATE.md` - Template PR

- 🎨 **Interfaccia Aggiornata**
  - Menu 10: Simulatore Interventi
  - 5 funzionalità complete con helper functions

### 🔄 Modificato
- ✅ **README.md** migliorato con:
  - Badge professionali aggiunti
  - Sezione "Perché Questo Progetto Conta"
  - Guida Utente Rapida dettagliata
  - Sezione "Test e Validazione"
  - Sezione "Come Contribuire"

### ✅ Testato
- 21/21 test passati
- Validazione boundary conditions
- Verifica integrazione moduli

---

## [2.0] - 2024-11

### ✨ Aggiunto
- 📊 Indicatori Sintetici (`indicatori.py`)
  - Indice Qualità Scolastica
  - Indice Equità Educativa
  - Indice Efficacia Didattica
  - Indice Coesione Sociale
  - Indice Benessere Scolastico

- 🔐 Sistema di Accesso (`accesso.py`)
  - RBAC con 5 ruoli
  - Vista pubblica e privata
  - Gestione permessi granulari

- 📄 Generazione Report (`report.py`)
  - Report annuale
  - Report per classe
  - Report per insegnante
  - Report equità educativa

- 🖥️ Interfaccia Avanzata (`interfaccia.py`)
  - Menu indicatori
  - Menu report
  - Menu accesso

- 🌍 Macro-Dati Territoriali (`macro_dati.py`)
  - 5 zone con dati ISTAT/MIUR
  - Calcolo fragilità territoriale
  - Impatto territoriale sui voti

---

## [1.0] - 2024-10

### ✨ Aggiunto
- 📝 **Moduli Core**:
  - `anagrafica.py` - Gestione studenti
  - `insegnanti.py` - Gestione professori
  - `voti.py` - Sistema voti
  - `orari.py` - Gestione orari
  - `analisi.py` - Analisi didattica
  - `utils.py` - Funzioni utility
  - `dati.py` - Generazione dati

- 📊 **Funzionalità**:
  - Calcolo fragilità sociale (0-100)
  - Graduatorie studenti e insegnanti
  - Analisi equità educativa
  - Gap pedagogico
  - Correlazione reddito-rendimento

- 🎲 **Simulazione**:
  - Generazione studenti casuali
  - Generazione insegnanti casuali
  - Assegnazione voti realistici

- 📖 **Esempi**:
  - `esempio_uso.py`
  - `esempio_uso_avanzato.py`
  - `esempio_macro_dati.py`

---

## Tipi di Cambiamenti

- **✨ Aggiunto** - Nuove funzionalità
- **🔄 Modificato** - Modifiche a funzionalità esistenti
- **❌ Deprecato** - Funzionalità che saranno rimosse
- **🗑️ Rimosso** - Funzionalità rimosse
- **🐛 Corretto** - Bug fix
- **🔒 Sicurezza** - Fix vulnerabilità

---

[2.1]: https://github.com/tuonome/registro-scolastico/releases/tag/v2.1
[2.0]: https://github.com/tuonome/registro-scolastico/releases/tag/v2.0
[1.0]: https://github.com/tuonome/registro-scolastico/releases/tag/v1.0

