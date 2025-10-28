"""
Script per importare studenti da file CSV
"""

import csv
from anagrafica import Anagrafica, Studente
from dati import CategoriaReddito, CondizioneSalute, SituazioneFamiliare

def importa_studenti_da_csv(file_csv: str):
    """Importa studenti da file CSV.
    
    Formato CSV atteso:
    nome,cognome,eta,classe,reddito_familiare
    Mario,Rossi,16,3A,35000
    Giulia,Bianchi,17,3B,28000
    """
    
    anagrafica = Anagrafica()
    
    try:
        with open(file_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Crea studente da riga CSV
                studente = Studente(
                    id=0,
                    nome=row['nome'],
                    cognome=row['cognome'],
                    eta=int(row['eta']),
                    classe=row['classe'],
                    reddito_familiare=int(row['reddito_familiare']),
                    categoria_reddito=categoria_da_reddito(int(row['reddito_familiare'])),
                    condizione_salute=CondizioneSalute.BUONA,  # Default
                    situazione_familiare=SituazioneFamiliare.STABILE  # Default
                )
                
                anagrafica.aggiungi_studente(studente)
                print(f"✅ Importato: {studente.nome_completo}")
        
        print(f"\n🎉 Importati {len(anagrafica.studenti)} studenti da {file_csv}")
        return anagrafica
        
    except FileNotFoundError:
        print(f"❌ File {file_csv} non trovato")
        return None
    except Exception as e:
        print(f"❌ Errore importazione: {e}")
        return None

def categoria_da_reddito(reddito: int) -> CategoriaReddito:
    """Determina categoria reddito da importo."""
    if reddito < 15000:
        return CategoriaReddito.MOLTO_BASSO
    elif reddito < 25000:
        return CategoriaReddito.BASSO  
    elif reddito < 45000:
        return CategoriaReddito.MEDIO
    elif reddito < 75000:
        return CategoriaReddito.ALTO
    else:
        return CategoriaReddito.MOLTO_ALTO

def crea_csv_esempio():
    """Crea un file CSV di esempio."""
    
    dati_esempio = [
        ["nome", "cognome", "eta", "classe", "reddito_familiare"],
        ["Mario", "Rossi", "16", "3A", "35000"],
        ["Giulia", "Bianchi", "17", "3A", "28000"], 
        ["Francesco", "Verde", "15", "2B", "18000"],
        ["Sofia", "Neri", "16", "3B", "45000"],
        ["Lorenzo", "Blu", "17", "3C", "32000"]
    ]
    
    with open('studenti_esempio.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(dati_esempio)
    
    print("✅ File studenti_esempio.csv creato")

if __name__ == "__main__":
    print("📊 IMPORTAZIONE DA CSV")
    print("="*40)
    
    # Crea file di esempio
    crea_csv_esempio()
    
    # Importa dal CSV
    anagrafica = importa_studenti_da_csv('studenti_esempio.csv')
    
    if anagrafica:
        print("\n📋 Studenti importati:")
        for s in anagrafica.studenti:
            print(f"   • {s.nome_completo} - {s.classe} - €{s.reddito_familiare:,}")
