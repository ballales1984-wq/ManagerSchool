"""
Esempio di utilizzo del modulo macro_dati.py
Mostra come integrare macro-dati territoriali nel sistema scolastico.
"""

from macro_dati import GestoreMacroDati, ZonaTerritoriale
from anagrafica import Anagrafica
import random


def esempio_macro_dati():
    """Esempio completo di utilizzo dei macro-dati."""
    
    print("\n" + "="*80)
    print("ESEMPIO: Macro-Dati Territoriali")
    print("="*80 + "\n")
    
    # 1. Inizializza gestore macro-dati
    print("1️⃣ Inizializzazione GestoreMacroDati...")
    gestore = GestoreMacroDati()
    print("   ✅ Gestore creato con", len(gestore.zone), "zone\n")
    
    # 2. Mostra zone disponibili
    print("2️⃣ Zone territoriali disponibili:")
    for nome, zona in gestore.zone.items():
        print(f"   • {nome}: reddito {zona.reddito_medio_familiare}€, "
              f"ISU {zona.indice_sviluppo_umano}")
    print()
    
    # 3. Mostra fragilità territoriale
    print("3️⃣ Indice di fragilità territoriale:")
    for nome in gestore.zone.keys():
        frag = gestore.calcola_indice_fragilita_territoriale(nome)
        print(f"   • {nome}: {frag}/100")
    print()
    
    # 4. Assegna studenti a zone
    print("4️⃣ Assegnazione studenti a zone (casuale):")
    for studente_id in range(1, 11):
        zona = gestore.assegna_studente_casuale(studente_id)
        macro = gestore.macro_dati_studente(studente_id)
        print(f"   Studente {studente_id} → {zona} (reddito medio: {macro.reddito_medio_familiare}€)")
    print()
    
    # 5. Statistiche per zona
    print("5️⃣ Statistiche aggregate per zona:")
    stats = gestore.statistiche_zone()
    for zona, dati in stats.items():
        print(f"   {zona}:")
        print(f"     - Studenti: {dati['studenti']}")
        print(f"     - Reddito medio: {dati['reddito_medio']}€")
        print(f"     - Fragilità: {dati['fragilita_territoriale']}/100")
    print()
    
    # 6. Report comparativo
    print("6️⃣ Report comparativo zone:")
    confronto = gestore.report_comparativo_zone()
    print(f"   {'Zona':<15} {'ISU':<8} {'Reddito':<12} {'Fragilità':<12} {'Studenti'}")
    print("   " + "-"*70)
    for r in confronto:
        print(f"   {r['zona']:<15} {r['indice_sviluppo']:<8.2f} "
              f"{r['reddito_medio']:<12.0f} {r['fragilita_territoriale']:<12.2f} "
              f"{r['studenti']}")
    print()
    
    # 7. Salva su file
    print("7️⃣ Salvataggio su file...")
    gestore.salva_su_file("macro_dati_esempio.json")
    print("   ✅ Salvato in macro_dati_esempio.json\n")
    
    # 8. Carica da file
    print("8️⃣ Caricamento da file...")
    gestore2 = GestoreMacroDati()
    if gestore2.carica_da_file("macro_dati_esempio.json"):
        print("   ✅ Caricato correttamente")
        print(f"   Studenti assegnati: {len(gestore2.assegnazioni_studenti)}")
    else:
        print("   ❌ Errore nel caricamento")
    print()
    
    # 9. Impatto sui voti
    print("9️⃣ Impatto territoriale sui voti:")
    for nome in gestore.zone.keys():
        impatto = gestore.calcola_impatto_reddito_territoriale(nome)
        simbolo = "+" if impatto > 0 else ""
        print(f"   {nome}: {simbolo}{impatto:.2f} voti")
    print()


def esempio_integrazione_anagrafica():
    """Mostra come integrare macro-dati con anagrafica studenti."""
    
    print("\n" + "="*80)
    print("ESEMPIO: Integrazione con Anagrafica")
    print("="*80 + "\n")
    
    # Crea anagrafica
    anagrafica = Anagrafica()
    anagrafica.genera_studenti(20)
    
    # Crea gestore macro-dati
    gestore = GestoreMacroDati()
    
    # Assegna ogni studente a una zona
    print("🔗 Collegamento studenti → zone territoriali:")
    for studente in anagrafica.studenti:
        zona = gestore.assegna_studente_casuale(studente.id)
        macro = gestore.macro_dati_studente(studente.id)
        
        # Modifica reddito studente in base alla zona
        variazione = random.uniform(-5000, 5000)
        studente.reddito_familiare = macro.reddito_medio_familiare + variazione
    
    print("   ✅ 20 studenti assegnati a zone\n")
    
    # Statistiche per zona
    print("📊 Distribuzione studenti per zona:")
    stats = gestore.statistiche_zone()
    for zona, dati in stats.items():
        print(f"   {zona}: {dati['studenti']} studenti")
    print()
    
    # Analisi fragilità
    print("⚠️  Fragilità territoriale:")
    for zona in gestore.zone.keys():
        studenti_zona = [s for s in anagrafica.studenti 
                         if gestore.assegnazioni_studenti.get(s.id) == zona]
        frag = gestore.calcola_indice_fragilita_territoriale(zona)
        
        if studenti_zona:
            redditi = [s.reddito_familiare for s in studenti_zona]
            reddito_medio = sum(redditi) / len(redditi)
            print(f"   {zona}: {len(studenti_zona)} studenti, "
                  f"fragilità {frag}/100, reddito medio {reddito_medio:.0f}€")
    print()


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🏫 MACRO-DATI TERRITORIALI - ESEMPI D'USO")
    print("="*80)
    
    # Esegui esempi
    esempio_macro_dati()
    esempio_integrazione_anagrafica()
    
    print("\n" + "="*80)
    print("✅ Esempi completati!")
    print("="*80 + "\n")
