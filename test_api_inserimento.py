"""
Script per testare l'inserimento dati via API REST
"""

import requests
import json

def test_inserimento_api():
    """Testa l'inserimento dati tramite API."""
    
    BASE_URL = "http://127.0.0.1:5000"
    
    # 1. Login (necessario per le API)
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    session = requests.Session()
    
    # Effettua login
    response = session.post(f"{BASE_URL}/login", data=login_data)
    if response.status_code != 200:
        print("❌ Errore login")
        return
    
    print("✅ Login effettuato")
    
    # 2. Inserisci nuovo studente via API
    nuovo_studente = {
        "nome": "Luca",
        "cognome": "Ferrari",
        "eta": 16,
        "classe": "2C",
        "reddito_familiare": 42000,
        "categoria_reddito": "MEDIO",
        "condizione_salute": "BUONA", 
        "situazione_familiare": "STABILE"
    }
    
    response = session.post(
        f"{BASE_URL}/api/studenti", 
        json=nuovo_studente,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 201:
        studente_creato = response.json()
        print(f"✅ Studente creato: {studente_creato['nome']} {studente_creato['cognome']}")
        print(f"   ID: {studente_creato['id']}")
        print(f"   Fragilità: {studente_creato['fragilita']:.1f}")
    else:
        print(f"❌ Errore creazione studente: {response.status_code}")
    
    # 3. Ottieni lista studenti
    response = session.get(f"{BASE_URL}/api/studenti")
    if response.status_code == 200:
        studenti = response.json()
        print(f"\n📊 Totale studenti nel sistema: {len(studenti)}")
        
        # Mostra ultimi 3 studenti
        print("\n🎓 Ultimi studenti inseriti:")
        for studente in studenti[-3:]:
            print(f"   • {studente['nome']} {studente['cognome']} - Classe {studente['classe']}")

if __name__ == "__main__":
    print("🌐 TEST INSERIMENTO VIA API")
    print("="*50)
    print("⚠️  ASSICURATI CHE IL SERVER SIA ATTIVO!")
    print("   python avvia_erp.py")
    print()
    
    try:
        test_inserimento_api()
    except requests.exceptions.ConnectionError:
        print("❌ Server non raggiungibile. Avvia prima: python avvia_erp.py")
    except Exception as e:
        print(f"❌ Errore: {e}")
