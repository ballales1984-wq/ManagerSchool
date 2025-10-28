"""
Registro Scolastico Intelligente
Main entry point con menu interattivo
"""

import os
from anagrafica import Anagrafica
from insegnanti import GestioneInsegnanti
from voti import GestioneVoti
from orari import GestioneOrari
from analisi import AnalisiDidattica
from comunicazioni import GestioneComunicazioni
import utils


class RegistroScolastico:
    """Sistema completo di gestione scolastica."""
    
    def __init__(self):
        """Inizializza il sistema."""
        self.anagrafica = Anagrafica()
        self.insegnanti = GestioneInsegnanti()
        self.voti = GestioneVoti()
        self.orari = GestioneOrari()
        self.analisi = AnalisiDidattica(self.anagrafica, self.voti)
        self.comunicazioni = GestioneComunicazioni()
    
    def menu_principale(self):
        """Mostra il menu principale."""
        print("\n" + "="*80)
        print("🏫 REGISTRO SCOLASTICO INTELLIGENTE".center(80))
        print("="*80)
        print("\n1.  Gestione Studenti")
        print("2.  Gestione Insegnanti")
        print("3.  Gestione Voti")
        print("4.  Gestione Orari")
        print("5.  Analisi e Statistiche")
        print("6.  Simulazione Completa (Genera Dati)")
        print("0.  Esci")
        print("\n" + "="*80)
    
    def gestione_studenti(self):
        """Menu gestione studenti."""
        while True:
            print("\n📚 GESTIONE STUDENTI")
            print("-" * 80)
            print("1. Visualizza studenti")
            print("2. Aggiungi studente")
            print("3. Cerca studente")
            print("4. Statistiche anagrafica")
            print("5. Genera studenti casuali")
            print("0. Torna al menu principale")
            
            scelta = input("\nScelta: ").strip()
            
            if scelta == "1":
                self._visualizza_studenti()
            elif scelta == "2":
                self._aggiungi_studente()
            elif scelta == "3":
                self._cerca_studente()
            elif scelta == "4":
                self._statistiche_anagrafica()
            elif scelta == "5":
                self._genera_studenti_casuali()
            elif scelta == "0":
                break
            else:
                print("❌ Scelta non valida!")
    
    def gestione_insegnanti(self):
        """Menu gestione insegnanti."""
        while True:
            print("\n👨‍🏫 GESTIONE INSEGNANTI")
            print("-" * 80)
            print("1. Visualizza insegnanti")
            print("2. Aggiungi insegnante")
            print("3. Statistiche insegnanti")
            print("4. Genera insegnanti casuali")
            print("0. Torna al menu principale")
            
            scelta = input("\nScelta: ").strip()
            
            if scelta == "1":
                self._visualizza_insegnanti()
            elif scelta == "2":
                self._aggiungi_insegnante()
            elif scelta == "3":
                self._statistiche_insegnanti()
            elif scelta == "4":
                self._genera_insegnanti_casuali()
            elif scelta == "0":
                break
            else:
                print("❌ Scelta non valida!")
    
    def gestione_voti(self):
        """Menu gestione voti."""
        while True:
            print("\n📝 GESTIONE VOTI")
            print("-" * 80)
            print("1. Aggiungi voto")
            print("2. Visualizza voti studente")
            print("3. Visualizza media studente")
            print("4. Crea pagella")
            print("5. Statistiche voti")
            print("0. Torna al menu principale")
            
            scelta = input("\nScelta: ").strip()
            
            if scelta == "1":
                self._aggiungi_voto()
            elif scelta == "2":
                self._visualizza_voti_studente()
            elif scelta == "3":
                self._media_studente()
            elif scelta == "4":
                self._crea_pagella()
            elif scelta == "5":
                self._statistiche_voti()
            elif scelta == "0":
                break
            else:
                print("❌ Scelta non valida!")
    
    def analisi_statistiche(self):
        """Menu analisi e statistiche."""
        while True:
            print("\n📊 ANALISI E STATISTICHE")
            print("-" * 80)
            print("1. Graduatoria studenti")
            print("2. Graduatoria insegnanti")
            print("3. Analisi impatto fragili")
            print("4. Correlazione reddito-rendimento")
            print("5. Analisi completa")
            print("0. Torna al menu principale")
            
            scelta = input("\nScelta: ").strip()
            
            if scelta == "1":
                self._graduatoria_studenti()
            elif scelta == "2":
                self._graduatoria_insegnanti()
            elif scelta == "3":
                self._analisi_fragili()
            elif scelta == "4":
                self._correlazione_reddito()
            elif scelta == "5":
                self._analisi_completa()
            elif scelta == "0":
                break
            else:
                print("❌ Scelta non valida!")
    
    def simulazione_completa(self):
        """Genera una simulazione completa con dati casuali."""
        print("\n🎲 SIMULAZIONE COMPLETA")
        print("-" * 80)
        
        try:
            n_studenti = int(input("Quanti studenti generare? (default: 50): ") or "50")
            n_insegnanti = int(input("Quanti insegnanti generare? (default: 10): ") or "10")
        except ValueError:
            print("⚠️  Valore non valido, uso default")
            n_studenti = 50
            n_insegnanti = 10
        
        # Genera studenti
        print(f"\n📚 Generando {n_studenti} studenti...")
        self.anagrafica.genera_studenti(n_studenti)
        print(f"✅ {len(self.anagrafica.studenti)} studenti creati!")
        
        # Genera insegnanti
        print(f"\n👨‍🏫 Generando {n_insegnanti} insegnanti...")
        self.insegnanti.genera_insegnanti(n_insegnanti)
        print(f"✅ {len(self.insegnanti.insegnanti)} insegnanti creati!")
        
        # Genera voti
        print("\n📝 Generando voti...")
        # Materie complete per pagelle realistiche
        materie = ["Matematica", "Italiano", "Inglese", "Storia", "Educazione Fisica", "Religione"]
        voti_creati = 0
        
        for studente in self.anagrafica.studenti:
            for materia in materie:
                # Genera 2-6 voti per materia
                import random
                n_voti = random.randint(2, 6)
                
                for _ in range(n_voti):
                    # Voto leggermente influenzato dalla fragilità
                    base = 6.5 - (studente.fragilità_sociale / 100)
                    # Aggiusta base per materie specifiche
                    if materia == "Educazione Fisica":
                        base += 0.4  # Voti tendenzialmente più alti
                    elif materia == "Religione": 
                        base += 0.3  # Voti generalmente buoni
                    self.voti.aggiungi_voto_casuale(studente.id, materia, base)
                    voti_creati += 1
        
        print(f"✅ {voti_creati} voti creati!")
        print("\n✅ Simulazione completata! Puoi ora esplorare le funzionalità.")
    
    # Metodi helper per le singole operazioni
    def _visualizza_studenti(self):
        """Visualizza tutti gli studenti."""
        if not self.anagrafica.studenti:
            print("📭 Nessuno studente registrato")
            return
        
        righe = []
        for s in self.anagrafica.studenti[:20]:  # Mostra solo i primi 20
            righe.append([
                str(s.id), s.nome_completo, s.classe, 
                str(s.fragilità_sociale)
            ])
        
        utils.stampa_tabella(righe, ["ID", "Nome", "Classe", "Fragilità"])
        if len(self.anagrafica.studenti) > 20:
            print(f"\n... e altri {len(self.anagrafica.studenti) - 20} studenti")
    
    def _aggiungi_studente(self):
        """Aggiunge uno studente manualmente."""
        print("\nAggiungi nuovo studente:")
        # Implementazione semplificata
        studente = self.anagrafica.crea_studente_casuale()
        print(f"✅ Creato: {studente.nome_completo}")
    
    def _cerca_studente(self):
        """Cerca uno studente."""
        nome = input("Cerca studente: ").strip()
        risultati = self.anagrafica.trova_per_nome(nome)
        
        if risultati:
            print(f"\nTrovati {len(risultati)} studenti:")
            for s in risultati:
                print(f"  • {s.nome_completo} ({s.classe})")
        else:
            print("❌ Nessuno studente trovato")
    
    def _statistiche_anagrafica(self):
        """Mostra statistiche anagrafica."""
        stats = self.anagrafica.statistiche_generali()
        print("\n📊 STATISTICHE ANAGRAFICA")
        print(f"Totale studenti: {stats['totale_studenti']}")
        print(f"Reddito medio: €{stats['reddito_medio']:,}")
        print("\nFragilità sociale:")
        frag = stats['statistica_fragilita']
        print(f"  Media: {frag['media']}")
        print(f"  Alta: {frag['percentuale_alta']}%")
    
    def _genera_studenti_casuali(self):
        """Genera studenti casuali."""
        n = int(input("Quanti studenti generare? ") or "10")
        self.anagrafica.genera_studenti(n)
        print(f"✅ Generati {n} studenti!")
    
    def _visualizza_insegnanti(self):
        """Visualizza tutti gli insegnanti."""
        if not self.insegnanti.insegnanti:
            print("📭 Nessun insegnante registrato")
            return
        
        righe = []
        for i in self.insegnanti.insegnanti:
            righe.append([
                str(i.id), i.nome_completo, ", ".join(i.materie[:2]),
                str(i.totale_ore_settimanali)
            ])
        
        utils.stampa_tabella(righe, ["ID", "Nome", "Materie", "Ore"])
    
    def _aggiungi_insegnante(self):
        """Aggiunge un insegnante manualmente."""
        insegnante = self.insegnanti.crea_insegnante_casuale()
        print(f"✅ Creato: {insegnante.nome_completo}")
    
    def _statistiche_insegnanti(self):
        """Mostra statistiche insegnanti."""
        stats = self.insegnanti.statistiche_generali()
        print("\n📊 STATISTICHE INSEGNANTI")
        print(f"Totale: {stats['totale_insegnanti']}")
        print(f"Ore medie: {stats['ore_medie']}")
    
    def _genera_insegnanti_casuali(self):
        """Genera insegnanti casuali."""
        n = int(input("Quanti insegnanti generare? ") or "5")
        self.insegnanti.genera_insegnanti(n)
        print(f"✅ Generati {n} insegnanti!")
    
    def _aggiungi_voto(self):
        """Aggiunge un voto."""
        stud_id = int(input("ID studente: "))
        materia = input("Materia: ").strip()
        voto = float(input("Voto (3-10): "))
        
        self.voti.aggiungi_voto(stud_id, materia, voto)
        print("✅ Voto aggiunto!")
    
    def _visualizza_voti_studente(self):
        """Visualizza voti di uno studente."""
        stud_id = int(input("ID studente: "))
        voti = self.voti.voti_studente(stud_id)
        
        if voti:
            print(f"\n📝 Voti studente:")
            for v in voti[:10]:
                print(f"  {v.materia}: {v.voto:.1f} ({v.tipo})")
        else:
            print("❌ Nessun voto trovato")
    
    def _media_studente(self):
        """Mostra media di uno studente."""
        stud_id = int(input("ID studente: "))
        media = self.voti.media_studente(stud_id)
        print(f"📊 Media: {media:.2f}")
    
    def _crea_pagella(self):
        """Crea una pagella."""
        stud_id = int(input("ID studente: "))
        quad = int(input("Quadrimestre (1/2): "))
        
        pagella = self.voti.crea_pagella(stud_id, quad)
        print(f"\n📋 PAGELLA - Media: {pagella.media_generale:.2f}")
    
    def _statistiche_voti(self):
        """Mostra statistiche voti."""
        stats = self.voti.statistiche_generali()
        print("\n📊 STATISTICHE VOTI")
        print(f"Totale voti: {stats['totale_voti']}")
        print(f"Voto medio: {stats['voto_medio']:.2f}")
    
    def _graduatoria_studenti(self):
        """Mostra graduatoria studenti."""
        grad = self.analisi.graduatoria_studenti()[:10]
        
        print("\n🏆 TOP 10 STUDENTI")
        righe = []
        for s in grad:
            righe.append([str(s['posizione']), s['nome'], 
                         s['classe'], f"{s['media']:.2f}"])
        
        utils.stampa_tabella(righe, ["Pos", "Nome", "Classe", "Media"])
    
    def _graduatoria_insegnanti(self):
        """Mostra graduatoria insegnanti."""
        grad = self.analisi.graduatoria_insegnanti(self.insegnanti)[:5]
        
        print("\n🏆 TOP 5 INSEGNANTI")
        for i in grad:
            print(f"  {i['nome']} - Efficacia: {i['efficacia']}")
    
    def _analisi_fragili(self):
        """Mostra analisi fragili."""
        analisi = self.analisi.impatto_didattico_fragili()
        print("\n📊 IMPATTO SU STUDENTI FRAGILI")
        print(f"Gap pedagogico: {analisi['gap_pedagogico']:.2f}")
        print(f"Equità: {analisi['equita_educativa']}")
    
    def _correlazione_reddito(self):
        """Mostra correlazione reddito."""
        correl = self.analisi.correlazione_reddito_rendimento()
        print("\n📊 CORRELAZIONE REDDITO-RENDIMENTO")
        for fascia, dati in correl.items():
            print(f"{fascia}: Media {dati['media_rendimento']:.2f}")
    
    def _analisi_completa(self):
        """Mostra analisi completa."""
        print("\n🔍 ESECUZIONE ANALISI COMPLETA...")
        risultati = self.analisi.analisi_completa(self.insegnanti)
        
        print("\n✅ ANALISI COMPLETATA!")
        print(f"\nClasse migliore: {risultati['classe_migliore']['classe']}")
        print(f"Media: {risultati['classe_migliore']['media']}")
    
    def run(self):
        """Avvia il sistema."""
        print("\n🎓 Benvenuto nel Registro Scolastico Intelligente!")
        print("💡 Suggerimento: Inizia con la 'Simulazione Completa' per popolare il sistema.\n")
        
        while True:
            self.menu_principale()
            scelta = input("\nScelta: ").strip()
            
            if scelta == "1":
                self.gestione_studenti()
            elif scelta == "2":
                self.gestione_insegnanti()
            elif scelta == "3":
                self.gestione_voti()
            elif scelta == "4":
                print("\n⚠️  Funzionalità orari in sviluppo")
            elif scelta == "5":
                self.analisi_statistiche()
            elif scelta == "6":
                self.simulazione_completa()
            elif scelta == "0":
                print("\n👋 Arrivederci!")
                break
            else:
                print("\n❌ Scelta non valida!")


if __name__ == "__main__":
    # Crea e avvia il sistema
    sistema = RegistroScolastico()
    sistema.run()
