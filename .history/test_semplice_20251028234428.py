"""
Test semplificato dei nuovi moduli.
"""

print("TEST MODULI SISTEMA")
print("=" * 50 + "\n")

# Import
from anagrafica import Anagrafica
from voti import GestioneVoti

print("1. Inizializzazione...")
anagrafica = Anagrafica()
anagrafica.genera_studenti(10)
print(f"   Studenti: {len(anagrafica.studenti)}")

print("\n2. Test Inserimento Rapido...")
from inserimento_rapido import GestoreInserimentoVeloce
ins_rapido = GestoreInserimentoVeloce(anagrafica, GestioneVoti())
print("   OK")

print("\n3. Test Amministrativa...")
from amministrativa_school import AmministrativaSchool
admin = AmministrativaSchool()
admin.collega_con_anagrafica(anagrafica)
print(f"   Alunni: {len(admin.alunni)}")

print("\n4. Test Backup...")
from backup_registro import GestoreBackup
backup = GestoreBackup()
print("   OK")

print("\n5. Test Valutazione Impatto...")
from valutazione_impatto import ValutazioneImpattoEducativo
valutatore = ValutazioneImpattoEducativo(anagrafica, GestioneVoti())
print("   OK")

print("\n6. Test Costruttore Corso...")
from costruttore_corso import CostruttoreCorsoDocente
costruttore = CostruttoreCorsoDocente(anagrafica, GestioneVoti())
print("   OK")

print("\n" + "=" * 50)
print("TUTTI I TEST PASSATI!")

