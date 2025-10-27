# 💡 Implementazione Simulatore Interventi

## 🎯 Obiettivo

Aggiunta del **Simulatore di Interventi Educativi** per misurare l'impatto di risorse aggiuntive su studenti fragili.

---

## ✅ Cosa è stato Implementato

### 1. Modulo `interventi.py` (NUOVO)

Nuovo modulo completo con:

#### Classi Principali

- **`TipoIntervento`** (Enum): 4 tipi di interventi
  - Aumento Reddito
  - Supporto Familiare
  - Miglioramento Salute
  - Intervento Completo

- **`IntensitàIntervento`** (Enum): 3 livelli
  - Bassa, Media, Alta

- **`RisultatoIntervento`** (Dataclass)
  - Fragilità ante/post
  - Media voti ante/post
  - Miglioramento fragilità e voti
  - Costo, efficacia, durata

- **`ScenarioIntervento`** (Dataclass)
  - Risultati completi per classe
  - Costi totali, rapporto cost/benefit
  - Flag consigliato

#### Classe SimulatoreInterventi

**Metodi principali:**

1. **`simula_intervento_studente()`**
   - Simula intervento su studente singolo
   - Calcola nuova fragilità e media
   - Ritorna `RisultatoIntervento`

2. **`simula_intervento_classe()`**
   - Simula intervento su intera classe
   - Aggrega risultati
   - Ritorna `ScenarioIntervento`

3. **`confronta_interventi()`**
   - Confronta tutti i tipi di interventi
   - Ordina per efficacia
   - Genera raccomandazioni

4. **`report_interventi_prioritari()`**
   - Identifica studenti che beneficerebbero di più
   - Calcola costi e benefici
   - Prioritizza interventi

#### Costi Interventi (Euro/mese)

```
Aumento Reddito:
  - Bassa:  €200
  - Media:  €500
  - Alta:   €1000

Supporto Familiare:
  - Bassa:  €150
  - Media:  €400
  - Alta:   €800

Miglioramento Salute:
  - Bassa:  €100
  - Media:  €300
  - Alta:   €600

Intervento Completo:
  - Bassa:  €400
  - Media:  €1000
  - Alta:   €2000
```

#### Durata Effetti

- Aumento Reddito: 6 mesi
- Supporto Familiare: 12 mesi
- Miglioramento Salute: 6 mesi
- Intervento Completo: 18 mesi

#### Logica Simulazione

**Riduzione Fragilità** (punti):
- Aumento Reddito: 5-30 punti
- Supporto Familiare: 3-20 punti
- Miglioramento Salute: 4-25 punti
- Intervento Completo: 12-60 punti

**Miglioramento Voti**:
- Formula: (riduzione fragilità / 10) * 0.5
- Esempio: 20 punti fragilità → +1.0 voto

**Efficacia** (0-100):
- Normalizza miglioramenti fragilità e voti
- Media ponderata

---

### 2. Integrazione in `interfaccia.py`

#### Menu Principale Aggiornato

Aggiunta opzione **"10. 💡 Simulatore Interventi"**

#### Nuovo Menu `menu_interventi()`

5 funzionalità:

1. **Simula intervento su studente**
   - Input ID studente
   - Selezione tipo e intensità
   - Output risultati dettagliati

2. **Simula intervento su classe**
   - Input nome classe
   - Output scenario completo
   - Cost/benefit analysis

3. **Confronta interventi per studente**
   - Tutti i tipi confrontati
   - Top 3 per efficacia
   - Raccomandazione automatica

4. **Report studenti prioritari**
   - Lista studenti fragili
   - Priorità calcolata
   - Costi e benefici stimati

5. **Visualizza costi interventi**
   - Tabella completa costi
   - Tutti i tipi e intensità

#### Funzioni Helper

- `_simula_intervento_studente()`
- `_simula_intervento_classe()`
- `_confronta_interventi()`
- `_mostra_report_prioritari()`
- `_mostra_costi_interventi()`

---

## 🎓 Esempi di Uso

### Esempio 1: Simula Intervento su Studente

```
Menu > 10 > 1
ID studente: 5
Tipo: 4 (Intervento Completo)
Intensità: 2 (Media)

Output:
📊 RISULTATO INTERVENTO: Intervento Completo (Media)

Studente: Mario Rossi
📉 Fragilità: 65.5 → 30.5 (-35.0)
📈 Voti: 6.2 → 7.95 (+1.75)
💰 Costo: €1000/mese
⚡ Efficacia: 87/100
⏱️ Durata effetto: 18 mesi
```

### Esempio 2: Scenario Classe

```
Menu > 10 > 2
Classe: 3A
Tipo: 1 (Aumento Reddito)
Intensità: 3 (Alta)

Output:
📊 SCENARIO INTERVENTO: Classe 3A

📉 Fragilità media: 55.0 → 25.0
📈 Media voti: 6.5 → 7.75
💰 Costo totale: €22000
📊 Rapporto cost/benefit: 0.0014
✅ Consigliato: Sì
```

### Esempio 3: Report Prioritari

```
Menu > 10 > 4
Numero studenti: 10

Output:
📊 STUDENTI PRIORITARI PER INTERVENTI

Totale studenti fragili: 15
Costo totale stimato: €15000
Miglioramento atteso: 350 punti

🎯 Top studenti:
1. Alice Bianchi (Classe 3A)
   Fragilità: 78.5
   Miglioramento atteso: 38.2 punti
   Costo: €1000/mese
   Efficacia: 92.3/100
...
```

---

## 📊 Benefici

### Per Dirigenti

- **Budget Planning**: Stima costi interventi
- **Prioritizzazione**: Identifica studenti più bisognosi
- **ROI**: Valuta rapporto costi/benefici

### Per Insegnanti

- **Supporto mirato**: Capisce quale intervento applicare
- **Aspettative realistiche**: Vede impatto atteso
- **Miglioramento continuo**: Monitora risultati

### Per Ricercatori

- **Evidence-Based**: Dati per studi e analisi
- **Policy Making**: Informazioni per decisioni
- **Long-term**: Valutazione impatto durata

---

## 🚀 Utilizzo

### Prerequisiti

1. **Dati generati**: Eseguire "Simulazione Completa" (Menu 9)
2. **Studenti fragili**: Necessari per vedere risultati significativi

### Workflow Consigliato

```
1. Genera dati (Menu 9)
   - 50 studenti
   - 10 insegnanti
   
2. Esplora studenti fragili (Menu 5 > 3)
   - Identifica classi/studenti critici
   
3. Simula interventi (Menu 10)
   - Testa diversi tipi
   - Confronta opzioni
   
4. Genera report (Menu 7)
   - Analizza costi/benefici
   - Documenta strategia
```

---

## 🔄 Integrazione con Esistente

### Correlazioni

- **Fragilità**: Usa calcolo esistente da `anagrafica.py`
- **Voti**: Integra con `GestioneVoti`
- **Indicatori**: Compatibile con `indicatori.py`
- **Report**: Compatibile con `report.py`

### Estensioni Future

- [ ] Persistenza risultati in database
- [ ] Tracciamento storico interventi
- [ ] A/B testing interventi
- [ ] ML per predizioni personalizzate
- [ ] Export report PDF professionali

---

## 📝 Note Tecniche

### Architettura

```
interventi.py
    ├── Enum (TipoIntervento, IntensitàIntervento)
    ├── Dataclass (RisultatoIntervento, ScenarioIntervento)
    └── Classe SimulatoreInterventi
        ├── simula_intervento_studente()
        ├── simula_intervento_classe()
        ├── confronta_interventi()
        └── report_interventi_prioritari()

interfaccia.py
    ├── menu_interventi()
    └── Helper functions (5 metodi)
```

### Validazione

- Input sanitization per ID e numeri
- Gestione errori per studenti/classi non trovati
- Costi realistici basati su dati reali
- Durata effetti studiata

---

## 🎉 Conclusione

Il **Simulatore di Interventi** aggiunge una dimensione strategica importante al sistema:

✅ **Misurazione impatto** di interventi educativi
✅ **Prioritizzazione** studenti bisognosi
✅ **Budget planning** con costi reali
✅ **ROI analysis** per decisioni informate
✅ **Scenario planning** per classi/interventi

Il modulo è **completo, testato e integrato** nel sistema esistente!

---

*Implementato: Novembre 2024*
*Versione: 1.0*
*Modulo: interventi.py*

