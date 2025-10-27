"""
Modulo per l'interfaccia utente.
Fornisce un menu interattivo per navigare il sistema.
"""

from typing import Optional
import os
import json
from datetime import datetime


class InterfacciaMenu:
    """Gestisce l'interfaccia utente del sistema."""
    
    def __init__(self, registro):
        """Inizializza l'interfaccia.
        
        Args:
            registro: Istanza di RegistroScolastico
        """
        self.registro = registro
        self.storia_navigazione = []
    
    def mostra_menu_principale(self):
        """Mostra il menu principale."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n" + "="*100)
        print("🏫 REGISTRO SCOLASTICO INTELLIGENTE - SISTEMA AVANZATO".center(100))
        print("="*100)
        print("\n📋 MENU PRINCIPALE\n")
        print("1.  👥 Gestione Studenti")
        print("2.  👨‍🏫 Gestione Insegnanti")
        print("3.  📝 Gestione Voti")
        print("4.  📅 Gestione Orari")
        print("5.  📊 Analisi e Statistiche")
        print("6.  🎯 Indicatori Sintetici")
        print("7.  📄 Report e Analisi")
        print("8.  🔐 Sistema di Accesso")
        print("9.  🤖 Simulazione Completa")
        print("10. 💡 Simulatore Interventi")
        print("0.  ❌ Esci")
        print("\n" + "="*100)
    
    def menu_indicatori(self):
        """Menu per gli indicatori sintetici."""
        from indicatori import CalcolatoreIndicatori
        
        calcolatore = CalcolatoreIndicatori(
            self.registro.anagrafica,
            self.registro.voti,
            self.registro.insegnanti,
            self.registro.analisi
        )
        
        while True:
            print("\n📊 INDICATORI SINTETICI")
            print("-" * 100)
            print("1. Indice Qualità Scolastica")
            print("2. Indice Equità Educativa")
            print("3. Indice Efficacia Didattica")
            print("4. Indice Coesione Sociale")
            print("5. Indice Benessere Scolastico")
            print("6. Quadro Indicatori Completo")
            print("7. Sintesi e Raccomandazioni")
            print("0. Torna al menu principale")
            
            scelta = input("\nScelta: ").strip()
            
            if scelta == "1":
                indice = calcolatore.indice_qualita_scolastica()
                self._mostra_indice(indice)
            elif scelta == "2":
                indice = calcolatore.indice_equita_educativa()
                self._mostra_indice(indice)
            elif scelta == "3":
                indice = calcolatore.indice_efficacia_didattica()
                self._mostra_indice(indice)
            elif scelta == "4":
                indice = calcolatore.indice_coesione_sociale()
                self._mostra_indice(indice)
            elif scelta == "5":
                indice = calcolatore.indice_benessere_scolastico()
                self._mostra_indice(indice)
            elif scelta == "6":
                self._mostra_quadro_completo(calcolatore)
            elif scelta == "7":
                self._mostra_sintesi(calcolatore)
            elif scelta == "0":
                break
            else:
                print("❌ Scelta non valida!")
    
    def menu_report(self):
        """Menu per i report."""
        from report import GeneratoreReport
        from indicatori import CalcolatoreIndicatori
        
        calcolatore = CalcolatoreIndicatori(
            self.registro.anagrafica,
            self.registro.voti,
            self.registro.insegnanti,
            self.registro.analisi
        )
        
        generatore = GeneratoreReport(
            self.registro.anagrafica,
            self.registro.voti,
            self.registro.insegnanti,
            self.registro.analisi,
            calcolatore
        )
        
        while True:
            print("\n📄 REPORT E ANALISI")
            print("-" * 100)
            print("1. Report Annuale Completo")
            print("2. Report per Classe")
            print("3. Report per Insegnante")
            print("4. Report Equità Educativa")
            print("5. Report Performance")
            print("6. Report Sintetico (Testuale)")
            print("7. Esporta Report (JSON)")
            print("0. Torna al menu principale")
            
            scelta = input("\nScelta: ").strip()
            
            if scelta == "1":
                self._mostra_report(generatore.report_annuale())
            elif scelta == "2":
                classe = input("Inserisci nome classe: ").strip()
                self._mostra_report(generatore.report_classe(classe))
            elif scelta == "3":
                try:
                    insegnante_id = int(input("Inserisci ID insegnante: "))
                    self._mostra_report(generatore.report_insegnante(insegnante_id))
                except ValueError:
                    print("❌ ID non valido!")
            elif scelta == "4":
                self._mostra_report(generatore.report_equita_educativa())
            elif scelta == "5":
                self._mostra_report(generatore.report_performance())
            elif scelta == "6":
                print("\n" + generatore.report_sintetico())
                input("\nPremi INVIO per continuare...")
            elif scelta == "7":
                self._esporta_report(generatore)
            elif scelta == "0":
                break
            else:
                print("❌ Scelta non valida!")
    
    def menu_accesso(self):
        """Menu per il sistema di accesso."""
        from accesso import GestoreAccessi, VistaPubblica, VistaPrivata, Ruolo
        
        gestore = GestoreAccessi()
        vista_pubblica = VistaPubblica()
        vista_privata = VistaPrivata()
        
        # Crea utente demo
        gestore.registra_utente("admin", "admin", Ruolo.AMMINISTRATORE, "Amministratore Demo")
        gestore.registra_utente("studente", "password", Ruolo.STUDENTE, "Studente Demo", 1)
        
        while True:
            print("\n🔐 SISTEMA DI ACCESSO")
            print("-" * 100)
            
            if gestore.get_utente_corrente():
                print(f"✅ Accesso effettuato come: {gestore.get_utente_corrente().nome_completo}")
                print(f"   Ruolo: {gestore.get_utente_corrente().ruolo.value}")
                print("\n1. Visualizza dati (vedi permessi)")
                print("2. Vista pubblica")
                print("3. Lista utenti")
                print("4. Statistiche accessi")
                print("5. Disconnetti")
                print("0. Torna al menu principale")
            else:
                print("❌ Nessun accesso effettuato")
                print("\n1. Accesso")
                print("2. Registrazione")
                print("3. Vista pubblica (senza accesso)")
                print("0. Torna al menu principale")
            
            scelta = input("\nScelta: ").strip()
            
            if scelta == "1" and gestore.get_utente_corrente():
                self._mostra_permessi(gestore, vista_privata)
            elif scelta == "2" and gestore.get_utente_corrente():
                self._mostra_vista_pubblica(vista_pubblica)
            elif scelta == "3" and gestore.get_utente_corrente():
                self._mostra_utenti(gestore)
            elif scelta == "4" and gestore.get_utente_corrente():
                self._mostra_statistiche_accessi(gestore)
            elif scelta == "5" and gestore.get_utente_corrente():
                gestore.disconnetti()
                print("✅ Disconnesso")
            elif scelta == "1" and not gestore.get_utente_corrente():
                self._esegui_login(gestore)
            elif scelta == "2" and not gestore.get_utente_corrente():
                self._registra_utente(gestore)
            elif scelta == "3" and not gestore.get_utente_corrente():
                self._mostra_vista_pubblica(vista_pubblica)
            elif scelta == "0":
                break
            else:
                print("❌ Scelta non valida!")
    
    def _mostra_indice(self, indice):
        """Mostra un indice."""
        print(f"\n{'='*100}")
        print(f"📊 {indice.nome}")
        print(f"{'='*100}")
        print(f"\nValore: {indice.valore}/100")
        print("\nComponenti:")
        for componente, valore in indice.componenti.items():
            barra = "█" * int(valore / 2)
            print(f"  {componente:30} {valore:6.2f} {barra}")
        
        input("\nPremi INVIO per continuare...")
    
    def _mostra_quadro_completo(self, calcolatore):
        """Mostra il quadro completo degli indicatori."""
        quadro = calcolatore.quadro_indicatori_completo()
        
        print("\n" + "="*100)
        print("📊 QUADRO INDICATORI COMPLETO")
        print("="*100 + "\n")
        
        for chiave, indice in quadro.items():
            print(f"{indice.nome}: {indice.valore}/100")
            for componente, valore in indice.componenti.items():
                print(f"  • {componente}: {valore:.2f}")
            print()
        
        input("Premi INVIO per continuare...")
    
    def _mostra_sintesi(self, calcolatore):
        """Mostra la sintesi degli indicatori."""
        sintesi = calcolatore.sintesi_indicatori()
        
        print("\n" + "="*100)
        print("📈 SINTESI INDICATORI")
        print("="*100 + "\n")
        
        print(f"Media Generale: {sintesi['media_generale']}/100")
        print(f"Valutazione: {sintesi['valutazione']}\n")
        
        print("🎯 RACCOMANDAZIONI:")
        for racc in sintesi['raccomandazioni']:
            print(f"  • {racc}")
        
        input("\nPremi INVIO per continuare...")
    
    def _mostra_report(self, report):
        """Mostra un report."""
        print("\n" + "="*100)
        print("📄 REPORT")
        print("="*100 + "\n")
        
        # Formatta il report in modo leggibile
        for chiave, valore in report.items():
            if isinstance(valore, dict):
                print(f"\n{chiave.upper().replace('_', ' ')}:")
                for k, v in valore.items():
                    print(f"  {k}: {v}")
            elif isinstance(valore, list):
                print(f"\n{chiave.upper().replace('_', ' ')}:")
                for item in valore[:10]:  # Limita a 10 elementi
                    if isinstance(item, dict):
                        print(f"  {item}")
                    else:
                        print(f"  {item}")
                if len(valore) > 10:
                    print(f"  ... e altri {len(valore) - 10} elementi")
            else:
                print(f"{chiave}: {valore}")
        
        input("\n\nPremi INVIO per continuare...")
    
    def _esporta_report(self, generatore):
        """Esporta i report in JSON."""
        nome_file = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_completo = {
            "report_annuale": generatore.report_annuale(),
            "report_equita": generatore.report_equita_educativa(),
            "report_performance": generatore.report_performance()
        }
        
        with open(nome_file, 'w', encoding='utf-8') as f:
            json.dump(report_completo, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Report esportato in: {nome_file}")
        input("\nPremi INVIO per continuare...")
    
    def _esegui_login(self, gestore):
        """Esegue il login."""
        from accesso import Ruolo
        
        print("\n🔐 ACCESSO")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        if gestore.autentica(username, password):
            print(f"✅ Accesso effettuato come {username}")
        else:
            print("❌ Credenziali non valide!")
        
        input("\nPremi INVIO per continuare...")
    
    def _registra_utente(self, gestore):
        """Registra un nuovo utente."""
        from accesso import Ruolo
        
        print("\n📝 REGISTRAZIONE")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        nome = input("Nome completo: ").strip()
        
        print("\nRuoli disponibili:")
        for ruolo in Ruolo:
            print(f"  {ruolo.value}")
        
        ruolo_str = input("\nRuolo: ").strip()
        
        try:
            ruolo = Ruolo[ruolo_str.upper()]
            if gestore.registra_utente(username, password, ruolo, nome):
                print("✅ Utente registrato!")
            else:
                print("❌ Username già esistente!")
        except KeyError:
            print("❌ Ruolo non valido!")
        
        input("\nPremi INVIO per continuare...")
    
    def _mostra_permessi(self, gestore, vista_privata):
        """Mostra i permessi dell'utente."""
        print("\n🔐 PERMESSI UTENTE")
        print("-" * 100)
        
        utente = gestore.get_utente_corrente()
        print(f"Username: {utente.username}")
        print(f"Ruolo: {utente.ruolo.value}")
        
        if gestore.verifica_permesso("visualizza_propri_dati"):
            print("✅ Accesso ai dati personali")
        
        if gestore.verifica_permesso("gestione_studenti"):
            print("✅ Gestione studenti")
        
        if gestore.verifica_permesso("gestione_insegnanti"):
            print("✅ Gestione insegnanti")
        
        if gestore.verifica_permesso("visualizza_report_completi"):
            print("✅ Report completi")
        
        input("\nPremi INVIO per continuare...")
    
    def _mostra_vista_pubblica(self, vista_pubblica):
        """Mostra la vista pubblica."""
        print("\n🌐 VISTA PUBBLICA")
        print("-" * 100)
        
        stats = vista_pubblica.visualizza_statistiche_generali(
            self.registro.anagrafica,
            self.registro.voti
        )
        
        print(f"Studenti totali: {stats['totale_studenti']}")
        print(f"Classi totali: {stats['totale_classi']}")
        print(f"Media generale: {stats['media_generale']}")
        
        input("\nPremi INVIO per continuare...")
    
    def _mostra_utenti(self, gestore):
        """Mostra la lista utenti."""
        print("\n👥 LISTA UTENTI")
        print("-" * 100)
        
        utenti = gestore.lista_utenti()
        for utente in utenti:
            print(f"{utente['username']:20} {utente['ruolo']:20} {utente['nome']}")
        
        input("\nPremi INVIO per continuare...")
    
    def _mostra_statistiche_accessi(self, gestore):
        """Mostra statistiche accessi."""
        print("\n📊 STATISTICHE ACCESSI")
        print("-" * 100)
        
        stats = gestore.statistiche_accessi()
        for chiave, valore in stats.items():
            print(f"{chiave}: {valore}")
        
        input("\nPremi INVIO per continuare...")
    
    def esegui(self):
        """Esegue l'interfaccia principale."""
        while True:
            self.mostra_menu_principale()
            scelta = input("\nScelta: ").strip()
            
            if scelta == "1":
                self.registro.gestione_studenti()
            elif scelta == "2":
                self.registro.gestione_insegnanti()
            elif scelta == "3":
                self.registro.gestione_voti()
            elif scelta == "4":
                print("Gestione Orari non implementata nel menu base")
                input("Premi INVIO per continuare...")
            elif scelta == "5":
                self.registro.analisi_statistiche()
            elif scelta == "6":
                self.menu_indicatori()
            elif scelta == "7":
                self.menu_report()
            elif scelta == "8":
                self.menu_accesso()
            elif scelta == "9":
                self.registro.simulazione_completa()
            elif scelta == "0":
                print("\n👋 Arrivederci!")
                break
            else:
                print("❌ Scelta non valida!")
                input("Premi INVIO per continuare...")
