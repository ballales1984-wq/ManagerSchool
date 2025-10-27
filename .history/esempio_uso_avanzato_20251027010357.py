"""
Esempi di utilizzo dei moduli avanzati del Registro Scolastico Intelligente.
Mostra come usare indicatori, accesso, report e interfaccia.
"""

from main import RegistroScolastico
from indicatori import CalcolatoreIndicatori
from report import GeneratoreReport
from accesso import GestoreAccessi, VistaPubblica, VistaPrivata, Ruolo


def esempio_indicator():
    """Esempio di utilizzo degli indicatori sintetici."""
    print("\n" + "="*80)
    print("ESEMPIO: Indicatori Sintetici")
    print("="*80 + "\n")
    
    # Crea sistema con dati
    registro = RegistroScolastico()
    
    # Genera dati di esempio
    print("Generazione dati di esempio...")
    registro.anagrafica.genera_studenti(50)
    registro.insegnanti.genera_insegnanti(10)
    registro.simulazione_completa()
    print("✅ Dati generati!\n")
    
    # Crea calcolatore indicatori
    calcolatore = CalcolatoreIndicatori(
        registro.anagrafica,
        registro.voti,
        registro.insegnanti,
        registro.analisi
    )
    
    # Calcola indicatori
    print("📊 CALCOLO INDICATORI\n")
    
    indicatore_qualita = calcolatore.indice_qualita_scolastica()
    print(f"Indice Qualità Scolastica: {indicatore_qualita.valore}/100")
    
    indicatore_equita = calcolatore.indice_equita_educativa()
    print(f"Indice Equità Educativa: {indicatore_equita.valore}/100")
    
    indicatore_efficacia = calcolatore.indice_efficacia_didattica()
    print(f"Indice Efficacia Didattica: {indicatore_efficacia.valore}/100")
    
    # Sintesi completa
    sintesi = calcolatore.sintesi_indicatori()
    print(f"\n📈 Sintesi Generale: {sintesi['media_generale']}/100")
    print(f"Valutazione: {sintesi['valutazione']}")
    
    print("\n🎯 Raccomandazioni:")
    for racc in sintesi['raccomandazioni']:
        print(f"  • {racc}")


def esempio_report():
    """Esempio di generazione report."""
    print("\n" + "="*80)
    print("ESEMPIO: Generazione Report")
    print("="*80 + "\n")
    
    # Crea sistema con dati
    registro = RegistroScolastico()
    registro.anagrafica.genera_studenti(50)
    registro.insegnanti.genera_insegnanti(10)
    registro.simulazione_completa()
    
    # Crea generatore report
    calcolatore = CalcolatoreIndicatori(
        registro.anagrafica,
        registro.voti,
        registro.insegnanti,
        registro.analisi
    )
    
    generatore = GeneratoreReport(
        registro.anagrafica,
        registro.voti,
        registro.insegnanti,
        registro.analisi,
        calcolatore
    )
    
    # Genera report sintetico
    print("📄 REPORT SINTETICO:\n")
    report_sintetico = generatore.report_sintetico()
    print(report_sintetico)
    
    # Genera report equità
    print("\n📊 REPORT EQUITÀ EDUCATIVA:")
    report_equita = generatore.report_equita_educativa()
    print(f"Gap pedagogico: {report_equita['gap_pedagogico']['valore']}")
    print(f"Interpretazione: {report_equita['gap_pedagogico']['interpretazione']}")


def esempio_accesso():
    """Esempio di sistema di accesso."""
    print("\n" + "="*80)
    print("ESEMPIO: Sistema di Accesso")
    print("="*80 + "\n")
    
    # Crea gestore accessi
    gestore = GestoreAccessi()
    
    # Registra utenti
    print("👥 Registrazione utenti:")
    gestore.registra_utente("admin", "admin123", Ruolo.AMMINISTRATORE, "Amministratore Sistema")
    gestore.registra_utente("mrossi", "pass123", Ruolo.INSEGNANTE, "Mario Rossi", 1)
    gestore.registra_utente("gverdi", "pass456", Ruolo.STUDENTE, "Giulia Verdi", 2)
    gestore.registra_utente("visitatore", "", Ruolo.PUBBLICO, "Visitatore")
    print("✅ Utenti registrati\n")
    
    # Test accesso
    print("🔐 Test di accesso:")
    
    # Accesso amministratore
    if gestore.autentica("admin", "admin123"):
        print("✅ Accesso admin effettuato")
        print(f"   Ruolo: {gestore.get_ruolo_corrente().value}")
        print(f"   Permessi gestione studenti: {gestore.verifica_permesso('gestione_studenti')}")
        gestore.disconnetti()
    
    # Accesso studente
    if gestore.autentica("gverdi", "pass456"):
        print("✅ Accesso studente effettuato")
        print(f"   Ruolo: {gestore.get_ruolo_corrente().value}")
        print(f"   Permessi gestione voti: {gestore.verifica_permesso('gestione_voti')}")
        gestore.disconnetti()
    
    # Statistiche
    print("\n📊 Statistiche accessi:")
    stats = gestore.statistiche_accessi()
    print(f"Totale utenti: {stats['totale_utenti']}")
    print(f"Utenti attivi: {stats['utenti_attivi']}")
    print(f"Distribuzione ruoli: {stats['distribuzione_ruoli']}")


def esempio_interfaccia():
    """Esempio di interfaccia avanzata."""
    print("\n" + "="*80)
    print("ESEMPIO: Interfaccia Avanzata")
    print("="*80 + "\n")
    
    # Crea sistema
    registro = RegistroScolastico()
    registro.anagrafica.genera_studenti(30)
    registro.insegnanti.genera_insegnanti(5)
    registro.simulazione_completa()
    
    print("✅ Sistema inizializzato con dati di esempio")
    print("✅ Interfaccia disponibile tramite interfaccia.py")
    print("\nPer usare l'interfaccia completa, esegui:")
    print("  python interfaccia.py")
    print("\noppure:")
    print("  from interfaccia import InterfacciaMenu")
    print("  from main import RegistroScolastico")
    print("  registro = RegistroScolastico()")
    print("  interfaccia = InterfacciaMenu(registro)")
    print("  interfaccia.esegui()")


def esempio_completo():
    """Esempio completo che integra tutti i moduli."""
    print("\n" + "="*80)
    print("ESEMPIO COMPLETO: Sistema Integrato")
    print("="*80 + "\n")
    
    # 1. Inizializzazione sistema
    print("1️⃣ Inizializzazione sistema...")
    registro = RegistroScolastico()
    registro.anagrafica.genera_studenti(50)
    registro.insegnanti.genera_insegnanti(10)
    registro.simulazione_completa()
    print("   ✅ Sistema pronto\n")
    
    # 2. Calcolo indicatori
    print("2️⃣ Calcolo indicatori sintetici...")
    calcolatore = CalcolatoreIndicatori(
        registro.anagrafica,
        registro.voti,
        registro.insegnanti,
        registro.analisi
    )
    sintesi = calcolatore.sintesi_indicatori()
    print(f"   📊 Valutazione: {sintesi['valutazione']} ({sintesi['media_generale']}/100)\n")
    
    # 3. Generazione report
    print("3️⃣ Generazione report...")
    generatore = GeneratoreReport(
        registro.anagrafica,
        registro.voti,
        registro.insegnanti,
        registro.analisi,
        calcolatore
    )
    report_annuale = generatore.report_annuale()
    print(f"   📄 Report generato per anno {report_annuale['anno']}\n")
    
    # 4. Sistema di accesso
    print("4️⃣ Configurazione accessi...")
    gestore = GestoreAccessi()
    gestore.registra_utente("admin", "admin", Ruolo.AMMINISTRATORE, "Admin")
    print("   🔐 Sistema di accesso configurato\n")
    
    # 5. Riepilogo
    print("✅ SISTEMA COMPLETO E OPERATIVO\n")
    print("Funzionalità disponibili:")
    print("  • Gestione studenti e insegnanti")
    print("  • Calcolo indicatori di qualità")
    print("  • Generazione report analitici")
    print("  • Sistema di accesso basato su ruoli")
    print("  • Interfaccia utente interattiva")
    
    return registro, calcolatore, generatore, gestore


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🏫 REGISTRO SCOLASTICO INTELLIGENTE - ESEMPI USO AVANZATO")
    print("="*80)
    
    # Esegui esempi
    esempio_indicator()
    esempio_report()
    esempio_accesso()
    esempio_interfaccia()
    esempio_completo()
    
    print("\n" + "="*80)
    print("✅ Tutti gli esempi completati!")
    print("="*80 + "\n")
