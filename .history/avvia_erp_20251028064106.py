"""
Script di avvio per l'interfaccia ERP.
Genera dati demo e avvia il server web.
"""

from main import RegistroScolastico
from interfaccia_erp import InterfacciaERP
import os


def main():
    """Avvia l'interfaccia ERP con dati demo."""
    print("\n" + "="*80)
    print("🚀 AVVIO INTERFACCIA ERP".center(80))
    print("="*80 + "\n")
    
    # Crea directory necessarie
    if not os.path.exists('templates'):
        os.makedirs('templates')
        print("✅ Creata directory: templates/")
    
    if not os.path.exists('static'):
        os.makedirs('static')
        print("✅ Creata directory: static/")
    
    # Genera dati demo (opzionale)
    print("\n📊 Generazione dati demo...")
    registro = RegistroScolastico()
    
    # Genera studenti e insegnanti se non ci sono dati
    if len(registro.anagrafica.studenti) == 0:
        print("   → Generando 30 studenti...")
        registro.anagrafica.genera_studenti(30)
    
    if len(registro.insegnanti.insegnanti) == 0:
        print("   → Generando 12 insegnanti specializzati...")
        registro.insegnanti.genera_insegnanti_per_materia()
    
    # Genera voti se non ci sono
    if len(registro.voti.voti) == 0:
        print("   → Generando voti...")
        # Materie complete come richiesto
        materie = ["Matematica", "Italiano", "Inglese", "Storia", "Educazione Fisica", "Religione"]
        for studente in registro.anagrafica.studenti:
            for materia in materie:
                import random
                n_voti = random.randint(2, 6)  # Più voti per materia
                for _ in range(n_voti):
                    base = 6.5 - (studente.fragilità_sociale / 100)
                    # Aggiusta base per materie specifiche
                    if materia == "Educazione Fisica":
                        base += 0.4  # Voti tendenzialmente più alti
                    elif materia == "Religione":
                        base += 0.3  # Voti generalmente buoni
                    registro.voti.aggiungi_voto_casuale(studente.id, materia, base)
    
    print(f"   ✅ Generati {len(registro.anagrafica.studenti)} studenti")
    print(f"   ✅ Generati {len(registro.insegnanti.insegnanti)} insegnanti")
    print(f"   ✅ Generati {len(registro.voti.voti)} voti")
    
    # Crea e avvia l'interfaccia ERP
    print("\n🌐 Avvio server web...")
    erp = InterfacciaERP()
    
    # Passa i dati del registro all'ERP
    erp.anagrafica = registro.anagrafica
    erp.insegnanti = registro.insegnanti
    erp.voti = registro.voti
    erp.analisi = registro.analisi
    
    print("\n" + "="*80)
    print("✅ INTERFACCIA ERP PRONTA!".center(80))
    print("="*80)
    print("\n📝 INFO ACCESSO:")
    print("   URL: http://127.0.0.1:5000")
    print("\n👤 ACCOUNT DEMO:")
    print("   - admin / admin123 (Amministratore)")
    print("   - dirigente / dirigente123 (Dirigente)")
    print("   - insegnante / insegnante123 (Insegnante)")
    print("   - studente / studente123 (Studente)")
    print("\n" + "="*80)
    print("\n⚡ Inizia a usare l'interfaccia ERP...")
    print("   Premi CTRL+C per fermare il server\n")
    
    # Avvia il server
    erp.run()


if __name__ == "__main__":
    main()


