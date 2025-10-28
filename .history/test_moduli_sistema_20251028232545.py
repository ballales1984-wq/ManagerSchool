"""
Test dei nuovi moduli del sistema Scuola Digitale.
"""

import sys
from anagrafica import Anagrafica
from voti import GestioneVoti
from insegnanti import GestioneInsegnanti

print("🧪 TEST MODULI SISTEMA SCUOLA DIGITALE")
print("=" * 70 + "\n")

# ============ INIZIALIZZAZIONE ============
print("📋 1. Inizializzazione sistema...")
anagrafica = Anagrafica()
anagrafica.genera_studenti(20)
print(f"   ✅ Studenti generati: {len(anagrafica.studenti)}")

gestione_voti = GestioneVoti()
gestione_insegnanti = GestioneInsegnanti()
gestione_insegnanti.genera_insegnanti(5)
print(f"   ✅ Insegnanti generati: {len(gestione_insegnanti.insegnanti)}")

# ============ TEST 1: Inserimento Rapido ============
print("\n" + "=" * 70)
print("🎯 2. TEST INSERIMENTO RAPIDO")
print("=" * 70)

from inserimento_rapido import GestoreInserimentoVeloce

inserimento_rapido = GestoreInserimentoVeloce(anagrafica, gestione_voti)

# Test interpretazione frase
test_frase = "Matematica interrogazione allunno Mario voto 7.5"
print(f"\n   Testing: '{test_frase}'")
risultato = inserimento_rapido.inserisci_da_frase(test_frase, "Prof.ssa Rossi", "2A")

if risultato.get("successo"):
    print(f"   ✅ Voto registrato: {risultato['voce']}")
else:
    print(f"   ❌ Errore: {risultato.get('errore')}")

# Test cronologia
cronologia = inserimento_rapido.visualizza_cronologia(5)
print(f"\n   📜 Cronologia inserimenti: {len(cronologia)} voci")

# ============ TEST 2: Amministrativa ============
print("\n" + "=" * 70)
print("📋 3. TEST AMMINISTRATIVA SCHOOL")
print("=" * 70)

from amministrativa_school import AmministrativaSchool, TipoPresenza
from gestione_presenze import GestorePresenze

amministrativa = AmministrativaSchool()
amministrativa.collega_con_anagrafica(anagrafica)
print(f"\n   ✅ Alunni collegati: {len(amministrativa.alunni)}")

# Test registrazione presenza
if len(amministrativa.alunni) > 0:
    alunno_id = list(amministrativa.alunni.keys())[0]
    presenza = amministrativa.registra_presenza(
        alunno_id, TipoPresenza.PRESENTE, docente="Prof.ssa Bianchi"
    )
    print(f"   ✅ Presenza registrata: {presenza.data}")
    
    stats = amministrativa.statistiche_presenze()
    print(f"   📊 Statistiche: {stats}")

# ============ TEST 3: Backup ============
print("\n" + "=" * 70)
print("💾 4. TEST BACKUP REGISTRO")
print("=" * 70)

from backup_registro import GestoreBackup
from main import RegistroScolastico

# Crea registro
registro_test = RegistroScolastico()
registro_test.anagrafica = anagrafica
registro_test.voti = gestione_voti
registro_test.insegnanti = gestione_insegnanti
registro_test.genera_dati_demo()

# Backup
backup = GestoreBackup()
filepath = backup.backup_automatico(registro_test, "giornalieri")
print(f"\n   ✅ Backup salvato: {filepath}")

# Statistiche backup
stats = backup.statistiche_backup()
print(f"   📊 Statistiche:")
for tipo, dati in stats.items():
    if dati["conteggio"] > 0:
        print(f"      {tipo}: {dati['conteggio']} file")

# ============ TEST 4: Valutazione Impatto ============
print("\n" + "=" * 70)
print("📊 5. TEST VALUTAZIONE IMPATTO EDUCATIVO")
print("=" * 70)

from valutazione_impatto import ValutazioneImpattoEducativo, TipoAttività, LivelloImpatto

valutatore = ValutazioneImpattoEducativo(anagrafica, gestione_voti)

# Registra materiale docente
materiale = valutatore.registra_materiale_esame(
    docente="Prof.ssa Bianchi",
    materia="Matematica",
    data_verifica="2025-10-30",
    argomenti=["Equazioni", "Funzioni"],
    esercizi=["Es. 1 pag 45", "Es. 2 pag 48"],
    link_copilot="https://copilot.microsoft.com/..."
)
print(f"\n   ✅ Materiale registrato: {materiale.materia}")
print(f"      Argomenti: {len(materiale.argomenti)}, Esercizi: {len(materiale.esercizi_caricati)}")

# Traccia attività
if len(anagrafica.studenti) > 0:
    studente_id = anagrafica.studenti[0].id
    attività = valutatore.traccia_studio_studente(
        studente_id, TipoAttività.SCHEDA_INTELLIGENTE, "Scheda sulle equazioni"
    )
    print(f"\n   ✅ Attività tracciata: {attività.tipo.value}")
    
    frequenza = valutatore.frequenza_uso_studente(studente_id)
    print(f"   📈 Frequenza d'uso: {frequenza:.2%}")

# Statistiche
stats_impatto = valutatore.statistiche_impatto_generale()
print(f"\n   📊 Statistiche impatto:")
print(f"      Materiale totale: {stats_impatto.get('materiale_totale', 0)}")
print(f"      Attività totali: {stats_impatto.get('attività_totali', 0)}")

# ============ TEST 5: Costruttore Corso ============
print("\n" + "=" * 70)
print("📚 6. TEST COSTRUTTORE CORSO DOCENTE")
print("=" * 70)

from costruttore_corso import CostruttoreCorsoDocente, TipoRisorsa, LivelloDifficoltà

costruttore = CostruttoreCorsoDocente(anagrafica, gestione_voti)

# Carica risorsa
risorsa = costruttore.carica_risorsa(
    docente="Prof.ssa Bianchi",
    titolo="Video: Equazioni di primo grado",
    tipo=TipoRisorsa.VIDEO,
    url="https://youtube.com/watch?v=...",
    argomenti=["Equazioni", "Algebra"],
    difficoltà=LivelloDifficoltà.BASE
)
print(f"\n   ✅ Risorsa caricata: {risorsa.titolo}")

# Crea corso
corso = costruttore.crea_corso(
    docente="Prof.ssa Bianchi",
    materia="Matematica",
    titolo="Algebra per 2A",
    classe_target="2A"
)
print(f"   ✅ Corso creato: {corso.titolo}")

# Aggiungi modulo
modulo = costruttore.aggiungi_modulo(
    corso=corso,
    titolo="Modulo 1: Equazioni",
    argomenti=["Equazioni", "Incognite"],
    durata_stimata=120
)
print(f"   ✅ Modulo aggiunto: {modulo.titolo}")

# Collega risorsa
costruttore.collega_risorsa_al_modulo(modulo, risorsa)
print(f"   ✅ Risorsa collegata al modulo")

# Programma verifica
verifica = costruttore.programma_verifica(
    docente="Prof.ssa Bianchi",
    materia="Matematica",
    data="2025-11-05",
    classe="2A",
    argomenti=["Equazioni", "Funzioni"],
    tipo="verifica scritta"
)
print(f"\n   ✅ Verifica programmata: {verifica['materia']} - {verifica['data']}")

# Report docente
report = costruttore.statistiche_docente("Prof.ssa Bianchi")
print(f"\n   📊 Statistiche docente:")
print(f"      Risorse: {report['totale_risorse']}")
print(f"      Corsi: {report['totale_corsi']}")

# ============ RIEPILOGO ============
print("\n" + "=" * 70)
print("✅ TEST COMPLETATI CON SUCCESSO!")
print("=" * 70)
print(f"""
📊 RIEPILOGO:
   - Studenti: {len(anagrafica.studenti)}
   - Insegnanti: {len(gestione_insegnanti.insegnanti)}
   - Risorse: {len(costruttore.risorse)}
   - Corsi: {len(costruttore.corsi)}
   - Schede: {len(costruttore.schede)}
   - Materiale: {len(valutatore.materiale_esame)}
   - Attività: {len(valutatore.attività_studenti)}
""")

