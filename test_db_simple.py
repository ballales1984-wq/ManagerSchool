"""
Test semplificato database SQLite.
"""

print("TEST DATABASE SQLITE")
print("=" * 60)

# Import
from anagrafica import Anagrafica
from database_manager import DatabaseManager

print("\n1. Setup...")
anagrafica = Anagrafica()
anagrafica.genera_studenti(10)
print(f"   {len(anagrafica.studenti)} studenti generati")

print("\n2. Database...")
db = DatabaseManager("test_simple.db")

print("\n3. Inserimento studenti...")
count = 0
for studente in anagrafica.studenti:
    try:
        studente_dict = {
            'id': studente.id,
            'nome': studente.nome,
            'cognome': studente.cognome,
            'eta': studente.eta,
            'classe': studente.classe,
            'reddito_familiare': studente.reddito_familiare,
            'categoria_reddito': str(studente.categoria_reddito.value),
            'condizione_salute': str(studente.condizione_salute.value),
            'situazione_familiare': studente.situazione_familiare,
            'note': studente.note
        }
        db.aggiungi_studente(studente_dict)
        count += 1
    except Exception as e:
        print(f"   Errore: {e}")

print(f"   {count} studenti inseriti")

print("\n4. Query...")
studenti_db = db.ottieni_studenti()
print(f"   Studenti nel database: {len(studenti_db)}")

print("\n5. Statistiche...")
stats = db.statistiche_database()
print(f"   Studenti: {stats['studenti']}")
print(f"   Voti: {stats['voti']}")
print(f"   Classi: {stats['classi']}")

db.close()
print("\nTEST COMPLETATO!")

