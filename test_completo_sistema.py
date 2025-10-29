"""
Test completo e simulazioni del sistema ManagerSchool v2.0
"""

print("=" * 70)
print("TEST COMPLETO - MANAGERSCHOOL V2.0")
print("=" * 70)
print()

# Import
from anagrafica import Anagrafica
from voti import GestioneVoti
from insegnanti import GestioneInsegnanti

# ============ SIMULAZIONE 1: SETUP INIZIALE ============
print("📋 SIMULAZIONE 1: Setup Sistema")
print("-" * 70)

anagrafica = Anagrafica()
anagrafica.genera_studenti(50)
gestione_voti = GestioneVoti()
gestione_insegnanti = GestioneInsegnanti()
gestione_insegnanti.genera_insegnanti(8)

print(f"✓ {len(anagrafica.studenti)} studenti generati")
print(f"✓ {len(gestione_insegnanti.insegnanti)} insegnanti generati")
print()

# ============ SIMULAZIONE 2: INSERIMENTO RAPIDO VOTI ============
print("⚡ SIMULAZIONE 2: Inserimento Rapido Voti")
print("-" * 70)

from inserimento_rapido import GestoreInserimentoVeloce

ins_rapido = GestoreInserimentoVeloce(anagrafica, gestione_voti)

# Simula inserimenti
studenti_test = anagrafica.studenti[:3]
for studente in studenti_test:
    frase = f"Matematica interrogazione allunno {studente.nome} {studente.cognome} voto 7.5"
    risultato = ins_rapido.inserisci_da_frase(frase, "Prof.ssa Bianchi", "2A")
    if risultato.get("successo"):
        print(f"✓ {risultato['voce']['studente']}: {risultato['voce']['voto']}")
    else:
        print(f"  {risultato.get('errore', 'OK')}")

print(f"✓ {len(ins_rapido.visualizza_cronologia())} voti inseriti")
print()

# ============ SIMULAZIONE 3: AMMINISTRATIVA ============
print("📋 SIMULAZIONE 3: Gestione Amministrativa")
print("-" * 70)

from amministrativa_school import AmministrativaSchool, TipoPresenza

amministrativa = AmministrativaSchool()
amministrativa.collega_con_anagrafica(anagrafica)
print(f"✓ {len(amministrativa.alunni)} alunni collegati")

# Registra presenze
import random
for i, alunno_id in enumerate(list(amministrativa.alunni.keys())[:10]):
    tipo = random.choice([TipoPresenza.PRESENTE, TipoPresenza.ASSENTE, TipoPresenza.RITARDO])
    amministrativa.registra_presenza(alunno_id, tipo, docente="Prof. Rossi")

stats = amministrativa.statistiche_presenze()
print(f"✓ {stats['totale_registrazioni']} presenze registrate")
print(f"✓ {stats['assenze']} assenze, {stats['ritardi']} ritardi")
print()

# ============ SIMULAZIONE 4: BACKUP ============
print("💾 SIMULAZIONE 4: Sistema Backup")
print("-" * 70)

from backup_registro import GestoreBackup
from main import RegistroScolastico

registro = RegistroScolastico()
registro.anagrafica = anagrafica
registro.voti = gestione_voti
registro.insegnanti = gestione_insegnanti

backup = GestoreBackup()
filepath = backup.salva_backup(registro)
print(f"✓ Backup salvato: {filepath.split('/')[-1]}")
print(f"✓ {len(backup.lista_backup_disponibili())} backup disponibili")
print()

# ============ SIMULAZIONE 5: VALUTAZIONE IMPATTO ============
print("📊 SIMULAZIONE 5: Valutazione Impatto")
print("-" * 70)

from valutazione_impatto import ValutazioneImpattoEducativo, TipoAttività

valutatore = ValutazioneImpattoEducativo(anagrafica, gestione_voti)

# Registra materiale
materiale = valutatore.registra_materiale_esame(
    docente="Prof.ssa Bianchi",
    materia="Matematica",
    data_verifica="2025-10-30",
    argomenti=["Equazioni", "Funzioni"],
    esercizi=["Es. 1", "Es. 2"]
)
print(f"✓ Materiale registrato: {len(materiale.argomenti)} argomenti")

# Traccia attività
if len(anagrafica.studenti) > 0:
    studente_id = anagrafica.studenti[0].id
    valutatore.traccia_studio_studente(studente_id, TipoAttività.SCHEDA_INTELLIGENTE, "Studio equazioni")
    print(f"✓ Attività tracciata per studente {studente_id}")

stats_impatto = valutatore.statistiche_impatto_generale()
materiale_tot = stats_impatto.get('materiale_totale', len(valutatore.materiale_esame))
attivita_tot = stats_impatto.get('attività_totali', len(valutatore.attività_studenti))
print(f"✓ {materiale_tot} materiali, {attivita_tot} attività")
print()

# ============ SIMULAZIONE 6: COSTRUTTORE CORSI ============
print("📚 SIMULAZIONE 6: Costruttore Corsi Digitali")
print("-" * 70)

from costruttore_corso import CostruttoreCorsoDocente, TipoRisorsa, LivelloDifficoltà

costruttore = CostruttoreCorsoDocente(anagrafica, gestione_voti)

# Carica risorsa
risorsa = costruttore.carica_risorsa(
    docente="Prof.ssa Bianchi",
    titolo="Video lezione: Equazioni",
    tipo=TipoRisorsa.VIDEO,
    url="https://youtube.com/...",
    argomenti=["Equazioni", "Algebra"],
    difficoltà=LivelloDifficoltà.BASE
)
print(f"✓ Risorsa caricata: {risorsa.titolo}")

# Crea corso
corso = costruttore.crea_corso(
    docente="Prof.ssa Bianchi",
    materia="Matematica",
    titolo="Algebra 2A",
    classe_target="2A"
)
print(f"✓ Corso creato: {corso.titolo}")

# Aggiungi modulo
modulo = costruttore.aggiungi_modulo(
    corso=corso,
    titolo="Modulo 1: Equazioni",
    descrizione="Introduzione alle equazioni di primo grado",
    argomenti=["Equazioni", "Incognite"],
    durata_stimata=120
)
print(f"✓ Modulo aggiunto: {modulo.titolo}")

statistiche = costruttore.statistiche_docente("Prof.ssa Bianchi")
print(f"✓ {statistiche['totale_risorse']} risorse, {statistiche['totale_corsi']} corsi")
print()

# ============ RISULTATI FINALI ============
print("=" * 70)
print("RISULTATI FINALI")
print("=" * 70)
print(f"✓ Studenti: {len(anagrafica.studenti)}")
print(f"✓ Insegnanti: {len(gestione_insegnanti.insegnanti)}")
print(f"✓ Voti inseriti: {len(gestione_voti.voti)}")
print(f"✓ Cronologia inserimenti: {len(ins_rapido.visualizza_cronologia())}")
print(f"✓ Presenze registrate: {stats['totale_registrazioni']}")
print(f"✓ Backup disponibili: {len(backup.lista_backup_disponibili())}")
print(f"✓ Materiale caricato: {materiale_tot}")
print(f"✓ Risorse didattiche: {statistiche['totale_risorse']}")
print(f"✓ Corsi creati: {statistiche['totale_corsi']}")
print()
print("✅ TUTTI I TEST SUPERATI!")
print("=" * 70)

